// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
//! # milan_datapath — PS-less Milan TSN datapath wrapper (migration §A.9)
//!
//! `milan_top.sv` **minus the Zynq PS** (`milan_dma_wrapper`) **and minus the MAC**.
//! This is the single clean HW/gateware boundary the LiteX SoC (sw/litex/milan_soc.py)
//! instantiates for the fully-FPGA RISC-V build — it contains everything that is
//! vendor-neutral RTL and therefore fully open-toolchain verifiable (Verilator +
//! Yosys), with **no Xilinx PS7 and no verilog-ethernet dependency**.
//!
//! What it owns (identical instances/wiring to `milan_top`):
//!   milan_csr · traffic_controller_802_1q (classify + CBS) · ptp_ts_top ·
//!   rx_mac_filter (TCAM) · adp_advertiser + adp_tx_arbiter · ethernet_events.
//!
//! What moved OUT to the integration layer:
//!   * the **Zynq PS + AXI-DMA** → replaced by the exposed AXI4-Lite CSR **slave**
//!     + the three DMA AXIS ports (the LiteX CPU bridge + §A.6 DMA drive these);
//!   * the **1G RGMII MAC** → exposed as a **MAC-facing AXIS pair** + MAC cfg/status
//!     ports, so the MAC is attached at the board layer (LiteEth `LiteEthMAC`, or
//!     Forencich `eth_mac_1g_rgmii_fifo`). This keeps the wrapper synth/sim-clean and
//!     lets the MAC be chosen per host. `milan_top.sv` remains the Zynq variant with
//!     the MAC + PS in place.
//!
//! Boundary summary:
//!   CPU  ── AXI4-Lite slave (s_axi_*, 16-bit offset) ─────► control plane
//!   DMA  ── s_axis_tx_* (DRAM→) / m_axis_rx_* (→DRAM) / m_axis_ts_* (→DRAM)
//!   MAC  ── m_axis_mac_tx_* (→MAC) / s_axis_mac_rx_* (MAC→) + o_mac_* cfg / i_mac_* status
//!   IRQ  ── o_irq_csr (milan_csr aggregate; DMA-done IRQs come from the §A.6 engine)

`default_nettype none
`include "ethernet_events.svh"

module milan_datapath import ethernet_packet_pkg::*; #(
  parameter int TDATA_WIDTH = 64,
  parameter int NUM_QUEUES  = NUMBER_OF_QUEUES,
  //! axis_clk frequency (AX7101 100 MHz, Arty 50 MHz) — AECP lock-timer divider.
  parameter int MILAN_CLK_FREQ_HZ = 100_000_000,
  //! NxN dataplane width (docs/NXN_ARCHITECTURE.md P0): AAF stream contexts
  //! per shared engine (listener sinks = talker sources = N_STREAMS). The
  //! N = 1 default is today's shape, bit-compatible (no-regression axiom).
  parameter int N_STREAMS = 1,
parameter int PB_PREFILL_C = 0     //! playback prefill release (0 = midpoint;
                                   //! TBs shrink it to keep injections short)
)(
  //! axis_clk domain (system clock, ~100 MHz) + active-low sync reset
  input  wire axis_clk,
  input  wire        clk_audio_i,      //! clean MMCM audio clock (24.576 MHz nominal) for the I2S DAC serializer
  input  wire axis_resetn,
  //! gtx_clk domain (125 MHz) used by the MAC-RX timestamping in ptp_ts_top
  input  wire gtx_clk,
  input  wire gtx_resetn,

  // ---- AXI4-Lite CSR slave (from the CPU bus bridge; low 16 bits = offset) ----
  input  wire [15:0] s_axi_awaddr,
  input  wire        s_axi_awvalid,
  output wire        s_axi_awready,
  input  wire [31:0] s_axi_wdata,
  input  wire [3:0]  s_axi_wstrb,
  input  wire        s_axi_wvalid,
  output wire        s_axi_wready,
  output wire [1:0]  s_axi_bresp,
  output wire        s_axi_bvalid,
  input  wire        s_axi_bready,
  input  wire [15:0] s_axi_araddr,
  input  wire        s_axi_arvalid,
  output wire        s_axi_arready,
  output wire [31:0] s_axi_rdata,
  output wire [1:0]  s_axi_rresp,
  output wire        s_axi_rvalid,
  input  wire        s_axi_rready,

  // ---- TX DMA: DRAM → datapath (feeds the 802.1Q shaper) ----
  // ---- Pmod I2S2 (AAF talker audio in; fabric is I2S clock master) ----
  output wire                     i2s_mclk_o,
  output wire                     i2s_sclk_o,
  output wire                     i2s_lrck_o,
  input  wire                     i2s_sdout_i,
  // ---- Pmod I2S2 DAC (line-out): zero-CPU playback of the bound stream ----
  output wire                     i2s_dac_mclk_o,
  output wire                     i2s_dac_sclk_o,
  output wire                     i2s_dac_lrck_o,
  output wire                     i2s_dac_sdin_o,

  input  wire [TDATA_WIDTH-1:0]   s_axis_tx_tdata,
  input  wire [TDATA_WIDTH/8-1:0] s_axis_tx_tkeep,
  input  wire                     s_axis_tx_tvalid,
  input  wire                     s_axis_tx_tlast,
  output wire                     s_axis_tx_tready,

  // ---- RX DMA: datapath (after the dest-MAC filter) → DRAM ----
  output wire [TDATA_WIDTH-1:0]   m_axis_rx_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_axis_rx_tkeep,
  output wire                     m_axis_rx_tvalid,
  output wire                     m_axis_rx_tlast,
  input  wire                     m_axis_rx_tready,

  // ---- TS-metadata: PTP core → DRAM (timestamp + seq_id + direction) ----
  output wire [TDATA_WIDTH-1:0]   m_axis_ts_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_axis_ts_tkeep,
  output wire                     m_axis_ts_tvalid,
  output wire                     m_axis_ts_tlast,
  input  wire                     m_axis_ts_tready,

  // ---- PCM payload: AAF RX depacketizer → DRAM PCM ring (full 8-B beats,
  //      wire byte order = S32BE interleaved; one AXIS frame per PDU).
  //      tuser = stream index s (NXN §1.3 P3: the per-stream ring writer
  //      key, ring base + s*stride at the SoC layer) ----
  output wire [TDATA_WIDTH-1:0]   m_axis_pcm_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_axis_pcm_tkeep,
  output wire                     m_axis_pcm_tvalid,
  output wire                     m_axis_pcm_tlast,
  output wire [3:0]               m_axis_pcm_tuser,
  input  wire                     m_axis_pcm_tready,

  // ---- MAC-facing TX: datapath (shaper→PTP→ADP arbiter) → external MAC ----
  output wire [TDATA_WIDTH-1:0]   m_axis_mac_tx_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_axis_mac_tx_tkeep,
  output wire                     m_axis_mac_tx_tvalid,
  output wire                     m_axis_mac_tx_tlast,
  input  wire                     m_axis_mac_tx_tready,

  // ---- MAC-facing RX: external MAC → datapath (into PTP-RX timestamping) ----
  input  wire [TDATA_WIDTH-1:0]   s_axis_mac_rx_tdata,
  input  wire [TDATA_WIDTH/8-1:0] s_axis_mac_rx_tkeep,
  input  wire                     s_axis_mac_rx_tvalid,
  input  wire                     s_axis_mac_rx_tlast,
  output wire                     s_axis_mac_rx_tready,

  // ---- MAC configuration (to the external MAC) ----
  output wire        o_mac_tx_en,
  output wire        o_mac_rx_en,
  output wire        o_mac_promisc,
  output wire        o_mac_allmulti,
  output wire        o_mac_is_1g,
  output wire [7:0]  o_mac_ifg,
  output wire [47:0] o_mac_addr,
  output wire [63:0] o_mc_hash,
  output wire        o_phy_reset_n,

  // ---- MAC status (from the external MAC) ----
  input  wire [1:0]  i_mac_speed,
  input  wire        i_link_up,
  output wire        o_mac_reinit,     //! link guard | LINK_CTRL[1] -> SoC MAC sys-side reset
  output wire        o_eth_rst,        //! link guard sequenced eth-side CDC reset request
                                       //! (SoC syncs it into eth_tx/eth_rx as the MAC's
                                       //! eth-domain reset; released BEFORE o_mac_reinit)
  input  wire        i_full_duplex,
  //! async divide-by-2 toggles from the SoC's eth clock domains (link guard
  //! liveness sensing; tie high on TBs/tops without a PHY - a static level
  //! reads as a dead clock only until the guard is disabled via LINK_CTRL[2])
  input  wire        i_ethrx_tgl,
  input  wire        i_ethtx_tgl,
  input  wire        i_ethact_tgl,
  //! RMON event pulses from the external MAC (lane index == ethernet_events_t
  //! enum). Lanes TX_FIFO_GOOD_FRAME/RX_FIFO_GOOD_FRAME are IGNORED here: the
  //! datapath derives them itself from the MAC AXIS boundary handshake (RMON
  //! never-worked-on-silicon fix, 2026-07-22 - the LiteX SoC glue tied this
  //! whole bus to 0 because LiteEth exposes no Forencich-style event pulses,
  //! so every lane counted nothing on both boards). Integrations supply only
  //! the MAC-internal lanes (underflow/overflow/bad-frame/bad-FCS); tie 0
  //! when the MAC exposes none.
  input  wire [_ETH_EVENT_COUNTER-1:0] i_mac_events,

  // ---- interrupt (milan_csr aggregate: tx_ts_ready | link_change | rmon_rollover) ----
  output wire        o_irq_csr,

  // ---- AECP IDENTIFY control (Milan FR-MGT-01): board LED blink hook ----
  output wire        o_identify
);

  // ==========================================================================
  //  Internal AXIS hops (identical topology to milan_top)
  // ==========================================================================
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_shaper();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_shaper_to_ts();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_dp_to_arb();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_mac();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_to_ts();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_ptp_to_filt();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_to_dma();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) ts_metadata_axis();

  // ---- boundary flat ports <-> internal interfaces ----
  // TX DMA in -> shaper
  //! host TX -> shaper (unchanged path)
  assign tx_axis_to_shaper.tdata  = s_axis_tx_tdata;
  assign tx_axis_to_shaper.tkeep  = s_axis_tx_tkeep;
  assign tx_axis_to_shaper.tvalid = s_axis_tx_tvalid;
  assign tx_axis_to_shaper.tlast  = s_axis_tx_tlast;
  assign s_axis_tx_tready         = tx_axis_to_shaper.tready;

  //! I2S divider scale: mclk = clk/2^N ~= 12.5 MHz -> 48.8 kHz sample rate
  //! on EITHER datapath clock. Un-parameterized, the 100 MHz AX sampled at
  //! 97.7 kHz while advertising 48 k (silicon: 16.9k fr/s, servo pegged).
  localparam int MCLK_DIV_LOG2_C = $clog2(MILAN_CLK_FREQ_HZ / 12_500_000);


  KL_tone_gen #(.MCLK_DIV_LOG2(MCLK_DIV_LOG2_C)) tone_gen (
    .clk_i (clk_audio_i), .rst_n (axis_resetn), .adv_i (1'b1),
    .enable_i (cfg_tone_enable), .att_i (cfg_tone_att), .smp_o (tone_smp)
  );

  //! NXN P4: the flat aaf_talker_i2s splits into the physical capture
  //! front-end (x1) + the shared N-context packetizer (TCTX). Talker 0
  //! aliases the legacy CSR config (golden byte-compare proven); talkers
  //! 1..N-1 arm via the TCTX window in P11.
  wire        aafcap_pv_w;
  wire [3:0]  aafcap_slot_w;
  wire [23:0] aafcap_l_w, aafcap_r_w;

  KL_aaf_capture_i2s aaf_capture (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .clk_audio_i (clk_audio_i),
    .tone_en_i (cfg_tone_enable), .tone_smp_i (tone_smp),
    .i2s_mclk_o (i2s_mclk_o), .i2s_sclk_o (i2s_sclk_o),
    .i2s_lrck_o (i2s_lrck_o), .i2s_sdout_i (i2s_sdout_i),
    .pair_valid_o (aafcap_pv_w), .pair_slot_o (aafcap_slot_w),
    .pair_l_o (aafcap_l_w), .pair_r_o (aafcap_r_w),
    .pairs_captured_o (aaf_pairs_w)
  );

  KL_aaf_packetizer #(.N_TALKERS_P(N_STREAMS)) aaf_packetizer (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .pair_valid_i (aafcap_pv_w), .pair_slot_i (aafcap_slot_w),
    .pair_l_i (aafcap_l_w), .pair_r_i (aafcap_r_w),
    //! t0 = the legacy admission gate; t>0 arm via TCTX CTRL + the P5
    //! per-stream bw-gate outputs once the P11 window provisions them
    .stream_en_i (N_STREAMS'(aaf_gate)),
    .dest_mac_i (eff_aaf_dmac),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .vlan_vid_i (cfg_aaf_vid),
    .transit_ns_i (aecp_pres_offset),
    .ptp_ns_i (ptp_now_w),
    .tctx_wr_en_i (1'b0), .tctx_wr_addr_i (7'd0),   //! P11 window hook
    .tctx_wr_data_i (32'd0), .tctx_wr_rdy_o (),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (aaf_tx_tdata), .m_axis_tkeep (aaf_tx_tkeep),
    .m_axis_tvalid(aaf_tx_tvalid), .m_axis_tlast (aaf_tx_tlast),
    .m_axis_tready(aaf_tx_tready),
    .frames_sent_o (aaf_frames_w)
  );
  // arbiter out -> MAC-facing TX
  assign m_axis_mac_tx_tdata  = tx_axis_to_mac.tdata;
  assign m_axis_mac_tx_tkeep  = tx_axis_to_mac.tkeep;
  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;
  assign m_axis_mac_tx_tlast  = tx_axis_to_mac.tlast;
  assign tx_axis_to_mac.tready = m_axis_mac_tx_tready;
  // MAC-facing RX -> PTP RX
  assign rx_axis_to_ts.tdata  = s_axis_mac_rx_tdata;
  assign rx_axis_to_ts.tkeep  = s_axis_mac_rx_tkeep;
  assign rx_axis_to_ts.tvalid = s_axis_mac_rx_tvalid;
  assign rx_axis_to_ts.tlast  = s_axis_mac_rx_tlast;
  assign s_axis_mac_rx_tready = rx_axis_to_ts.tready;
  // filter out -> RX DMA
  assign m_axis_rx_tdata  = rx_axis_to_dma.tdata;
  assign m_axis_rx_tkeep  = rx_axis_to_dma.tkeep;
  assign m_axis_rx_tvalid = rx_axis_to_dma.tvalid;
  assign m_axis_rx_tlast  = rx_axis_to_dma.tlast;
  assign rx_axis_to_dma.tready = m_axis_rx_tready;
  // PTP metadata -> TS DMA
  assign m_axis_ts_tdata  = ts_metadata_axis.tdata;
  assign m_axis_ts_tkeep  = ts_metadata_axis.tkeep;
  assign m_axis_ts_tvalid = ts_metadata_axis.tvalid;
  assign m_axis_ts_tlast  = ts_metadata_axis.tlast;
  assign ts_metadata_axis.tready = m_axis_ts_tready;

  // ==========================================================================
  //  CSR <-> datapath signals
  // ==========================================================================
  wire        cfg_mac_tx_en, cfg_mac_rx_en, cfg_mac_promisc, cfg_mac_allmulti, cfg_mac_is_1g;
  wire [7:0]  cfg_mac_ifg;
  wire [47:0] cfg_mac_addr;
  wire [63:0] cfg_mc_hash;
  wire        cfg_phy_reset_n;

  wire        cfg_stats_snapshot, cfg_stats_reset;
  wire [32*9-1:0] stats_counts;
  wire        stats_rollover;

  wire        cfg_cls_use_pcp, cfg_cls_dmac_check;
  wire [2:0]  cfg_cls_default_pcp;
  wire [23:0] cfg_cls_pcp_tc_map, cfg_cls_prio_regen;
  wire [31:0] cfg_cls_tc_queue_map;

  wire [32*NUM_QUEUES-1:0] cfg_cbs_idle_slope, cfg_cbs_hi_credit, cfg_cbs_lo_credit;
  wire [NUM_QUEUES-1:0]    cfg_cbs_enable;

  wire        cfg_ptp_enable;
  wire [31:0] cfg_ptp_incr, cfg_ptp_adj;
  wire [63:0] cfg_ptp_tod_wr, cfg_ptp_offset;
  wire        cfg_ptp_cmd_load, cfg_ptp_cmd_adjust, cfg_ptp_cmd_snapshot;
  wire [31:0] cfg_ptp_ingress_lat, cfg_ptp_egress_lat;
  wire [63:0] ptp_tod_rd;
  wire        ptp_tod_rd_valid;
  wire        evt_tx_ts_ready;

  wire        cfg_adp_enable;
  wire [4:0]  cfg_adp_valid_time;
  wire [63:0] cfg_adp_entity_id, cfg_adp_entity_model_id, cfg_adp_gptp_gm, cfg_adp_association_id;
  wire [31:0] cfg_adp_entity_caps, cfg_adp_controller_caps;
  wire [15:0] cfg_adp_talker_sources, cfg_adp_talker_caps;
  wire [15:0] cfg_adp_listener_sinks, cfg_adp_listener_caps;
  wire [7:0]  cfg_adp_gptp_domain;
  wire [31:0] cfg_gptp_pdelay_ns;
  wire [15:0] cfg_adp_current_config, cfg_adp_identify_index, cfg_adp_interface_index;
  wire        cfg_adp_advertise_p, cfg_adp_depart_p;
  wire [31:0] adp_available_index;
  wire [7:0]  adp_depart_cnt, adp_rearm_cnt;
  wire [1:0]  adp_depart_src;
  wire [TDATA_WIDTH-1:0]   adp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] adp_tx_tkeep;
  wire                     adp_tx_tvalid, adp_tx_tlast, adp_tx_tready;

  //! AECP/AEM listener (KL_aecp_top) — response AXIS + status + ADP-discover.
  wire [TDATA_WIDTH-1:0]   aecp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] aecp_tx_tkeep;
  wire                     aecp_tx_tvalid, aecp_tx_tlast, aecp_tx_tready;
  wire                     aecp_discover_p;
  wire                     aecp_locked;
  wire [15:0]              aecp_current_config, aecp_cmd_count, aecp_resp_count;
  //! ACMP stateless responder (KL_acmp_responder) — response AXIS + counters.
  wire [TDATA_WIDTH-1:0]   acmp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] acmp_tx_tkeep;
  wire                     acmp_tx_tvalid, acmp_tx_tlast, acmp_tx_tready;
  wire [TDATA_WIDTH-1:0]   ctl2_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctl2_tx_tkeep;
  wire                     ctl2_tx_tvalid, ctl2_tx_tlast, ctl2_tx_tready;
  wire [15:0]              acmp_cmd_count, acmp_resp_count;
  //! AAF talker (aaf_talker_i2s): CSR control + frame stream + PHC time
  wire                     cfg_aaf_enable;
  wire                     cfg_aaf_bypass;
  wire [47:0]              cfg_aaf_dmac;
  wire [11:0]              cfg_aaf_vid;
  //! Milan talker SM (docs/design/MILAN_TALKER_SM.md): ACMP probe state,
  //! the lwSRP listener socket (CSR override retained as the manual lever),
  //! the AECP presentation offset, and the resolved AAF gate.
  wire                     cfg_acmp_lobs;
  wire                     acmp_talker_active, acmp_probe_armed;
  wire [31:0]              aecp_pres_offset;
  //! lwSRP engine (KL_lwsrp_top, docs/LWSRP_FPGA_ARCHITECTURE.md)
  wire        cfg_lwsrp_enable, cfg_lwsrp_talker_en;
  wire [1:0]  cfg_lwsrp_qidx;
  wire [11:0] cfg_lwsrp_vid;
  wire [47:0] cfg_lwsrp_dmac;
  wire [15:0] cfg_lwsrp_max_frame, cfg_lwsrp_interval;
  wire [31:0] cfg_lwsrp_latency;
  wire        lwsrp_stream_gate, lwsrp_slope_en, lwsrp_res_active;
  wire [31:0] lwsrp_idle_slope;
  wire        lwsrp_listener_ready, lwsrp_listener_reg;
  wire [1:0]  lwsrp_listener_decl;
  wire        lwsrp_domain_ok, lwsrp_over_limit, lwsrp_talker_declared;
  wire        lwsrp_tfail_valid;
  wire [7:0]  lwsrp_tfail_code, lwsrp_rx_drops;
  wire [15:0] lwsrp_tx_count, lwsrp_rx_pdus;
  wire [TDATA_WIDTH-1:0]   lwsrp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] lwsrp_tx_tkeep;
  wire                     lwsrp_tx_tvalid, lwsrp_tx_tlast, lwsrp_tx_tready;
  //! CRF sink-1 bind record (same listener SM) + 0x4B BSCAN forensics
  wire        acmpl1_bound;
  wire [63:0] acmpl1_sid;
  wire [47:0] acmpl1_dmac;
  wire [31:0] aecp_bdbg0_w, aecp_bdbg1_w, aecp_bdbg2_w;
  //! ACMP listener SM (KL_acmp_listener, STREAM_INPUT[0] sink)
  acmp_pkg::acmp_lsm_t acmpl_state;
  wire        acmpl_bound = (acmpl_state != acmp_pkg::LSM_UNBOUND_S);
  wire [63:0] acmpl_talker, acmpl_sid;
  wire [15:0] acmpl_tuid;
  wire [4:0]  acmpl_status;
  wire [1:0]  acmpl_probing;
  wire        acmpl_tk_avail, acmpl_lstn_declare, acmpl_active;
  wire [11:0] acmpl_vlan;
  wire [47:0] acmpl_dmac;
  wire [15:0] acmpl_cmd_count, acmpl_probe_count;
  wire [7:0]  acmpl_tx_wedge;
  wire [31:0] acmpl_dbg;
  wire        lwsrp_ta_registered, lwsrp_ta_failed;
  wire [7:0]  lwsrp_ta_fail_code;
  wire [11:0] lwsrp_ta_vlan;
  wire [31:0] lwsrp_ta_acclat;
  wire [63:0] lwsrp_ta_fail_bridge, lwsrp_tfail_bridge;
  wire        lwsrp_lstn_declared;
  wire [TDATA_WIDTH-1:0]   acmpl_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] acmpl_tx_tkeep;
  wire                     acmpl_tx_tvalid, acmpl_tx_tlast, acmpl_tx_tready;
  //! AVTP RX monitor (KL_avtp_rx_monitor, STREAM_INPUT[0] Table 7-156)
  wire        avtprx_match, avtprx_tu_bit;
  wire [7:0]  avtprx_subtype, avtprx_seq;
  wire        avtprx_parse_p;
  wire [7:0]  avtprx_b3;
  wire [63:0] avtprx_sid_frame, avtprx_fsh2;
  wire signed [31:0] crf_delta_w, crf_rate_w;
  wire [15:0] crf_pducnt_w;
  wire [7:0]  crf_fmterr_w, crf_seqerr_w;
  wire        crf_locked_w;
  wire [31:0] crf_cnt_locked_w, crf_cnt_unlocked_w;
  //! CRF talker (KL_crf_tx): CSR control + PDU stream into the control merge
  wire        cfg_crft_en;
  wire [63:0] cfg_crft_sid;
  wire [47:0] cfg_crft_dmac;
  wire [31:0] crft_count_w;
  wire [TDATA_WIDTH-1:0]   crft_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] crft_tx_tkeep;
  wire                     crft_tx_tvalid, crft_tx_tlast, crft_tx_tready;
  wire [63:0] avtprx_fsh;
  wire [63:0] aecp_in0_fmt;
  wire [15:0] aecp_clk_src;
  wire        i2spb_converged;
  wire [31:0] i2spb_dbg_frame;
  wire [31:0] avtprx_locked_c, avtprx_unlocked_c, avtprx_intr_c;
  wire [31:0] avtprx_seqmm_c, avtprx_tu_c, avtprx_unsupp_c, avtprx_frx_c;
  wire        avtprx_locked, avtprx_dirty_p;
  wire        avtprx_accept_p;
  wire [31:0] avtprx_ts, avtprx_last_ts, avtprx_last_tsd;
  wire [15:0] pcmrx_pdus, pcmrx_drops;
  wire [15:0] i2spb_underruns, i2spb_overruns;
  wire        cfg_i2spb_clru, cfg_i2spb_clro;   //! I2SPB_STAT W1C strobes
  wire signed [15:0] i2spb_trim;
  wire [15:0] i2spb_fill;
  wire        i2spb_reset_p;
  wire [31:0] avtprx_mreset_c, avtprx_late_c, avtprx_early_c;
  wire        cfg_tone_enable;
  wire [2:0]  cfg_tone_att;
  wire [23:0] tone_smp;
  //! MAAP engine (KL_maap, IEEE 1722 Annex B; docs/design/MAAP_FABRIC.md)
  wire        cfg_maap_enable, cfg_maap_seed_valid;
  wire [7:0]  cfg_maap_count;
  wire [15:0] cfg_maap_seed_offset;
  wire [47:0] maap_addr;
  wire        maap_addr_valid;
  wire [1:0]  maap_state;
  wire [15:0] maap_offset;
  wire [7:0]  maap_conflicts, maap_defends;
  wire [TDATA_WIDTH-1:0]   maap_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] maap_tx_tkeep;
  wire                     maap_tx_tvalid, maap_tx_tlast, maap_tx_tready;
  //! effective stream DMAC: MAAP claim when enabled+valid, CSR value else
  //! (en=0 keeps the static-provisioning behavior bit-exact)
  wire [47:0] eff_aaf_dmac = (cfg_maap_enable && maap_addr_valid)
                             ? maap_addr : cfg_aaf_dmac;
  //! listener_observed: the lwSRP Listener registrar is the real source once
  //! the engine is enabled; A_ACMP_LOBS stays as the manual override socket.
  wire listener_observed_w = cfg_acmp_lobs |
                             (cfg_lwsrp_enable & lwsrp_listener_ready);
  //! AAF admission: probe-gated as before; with lwSRP enabled a reservation
  //! is additionally required (FR-SRP-03: no reservation -> no stream tx).
  //! The bypass bit stays the legacy stream-whenever-enabled escape hatch.
  wire aaf_gate = cfg_aaf_enable & (~cfg_maap_enable | maap_addr_valid) &
                  (cfg_aaf_bypass |
                  (acmp_talker_active & (~cfg_lwsrp_enable | lwsrp_stream_gate)));
  wire [63:0]              ptp_now_w;
  wire [31:0]              aaf_frames_w, aaf_pairs_w;
  wire [TDATA_WIDTH-1:0]   aaf_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] aaf_tx_tkeep;
  wire                     aaf_tx_tvalid, aaf_tx_tlast, aaf_tx_tready;
  //! merged low-rate control stream (ADP advertise + AECP response)
  wire [TDATA_WIDTH-1:0]   ctl_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctl_tx_tkeep;
  wire                     ctl_tx_tvalid, ctl_tx_tlast, ctl_tx_tready;

  wire        cfg_sw_link, cfg_mac_reinit;
  wire [63:0] cfg_entity_name8;
  wire        cfg_lpf_enable;
  wire        cfg_crf_en;
  wire [63:0] cfg_crf_sid;
  wire [63:0] cfg_as_parent_ckid;
  wire [63:0] pcm_lpf_tdata;
  wire        pcm_lpf_tvalid;
  wire        pcm_lpf_active;
  //! effective PHY link: the SoC's i_link_up (constant 1 on boards without
  //! HW tracking) gated by the daemon-maintained LINK_CTRL[0] - drives the
  //! AVB_INTERFACE LinkUp/LinkDown counters and the ADP link behavior
  wire        eff_link_w;
  wire        cfg_tcam_default_pass, cfg_tcam_wr_en, cfg_tcam_wr_valid;
  wire [4:0]  cfg_tcam_wr_index;
  wire [47:0] cfg_tcam_wr_key, cfg_tcam_wr_mask;
  wire [7:0]  cfg_tcam_wr_action;

  // ---- MAC config outputs (driven by milan_csr) ----
  assign o_mac_tx_en    = cfg_mac_tx_en;
  assign o_mac_rx_en    = cfg_mac_rx_en;
  assign o_mac_promisc  = cfg_mac_promisc;
  assign o_mac_allmulti = cfg_mac_allmulti;
  assign o_mac_is_1g    = cfg_mac_is_1g;
  assign o_mac_ifg      = cfg_mac_ifg;
  assign o_mac_addr     = cfg_mac_addr;
  assign o_mc_hash      = cfg_mc_hash;
  assign o_phy_reset_n  = cfg_phy_reset_n;
  assign o_irq_csr      = csr_irq;
  wire   csr_irq;

  //! Synchronise the MAC speed[] indication (i_mac_speed, gtx_clk-domain) into
  //! axis_clk before it is used by the CSR readback and link-change detector.
  (* ASYNC_REG = "TRUE" *) reg [1:0] speed_meta, speed_sync;
  always_ff @(posedge axis_clk) begin : mac_speed_cdc
    if (!axis_resetn) begin
      speed_meta <= 2'b10; speed_sync <= 2'b10;
    end else begin
      speed_meta <= i_mac_speed;
      speed_sync <= speed_meta;
    end
  end

  //! Link-status change detector (for IRQ / stats), on the synchronised speed.
  reg  [1:0] speed_q;
  reg        evt_link_change;
  always_ff @(posedge axis_clk) begin : link_change_detect
    if (!axis_resetn) begin
      speed_q <= 2'b10; evt_link_change <= 1'b0;
    end else begin
      speed_q <= speed_sync;
      evt_link_change <= (speed_q != speed_sync);
    end
  end

  // ==========================================================================
  //  Memory-mapped control plane
  // ==========================================================================
  milan_csr #(
    .NUM_QUEUES(NUM_QUEUES),
    .ADDR_WIDTH(16)
  ) csr (
    .aclk    (axis_clk),
    .aresetn (axis_resetn),
    .s_axi_awaddr (s_axi_awaddr),
    .s_axi_awvalid(s_axi_awvalid),
    .s_axi_awready(s_axi_awready),
    .s_axi_wdata  (s_axi_wdata),
    .s_axi_wstrb  (s_axi_wstrb),
    .s_axi_wvalid (s_axi_wvalid),
    .s_axi_wready (s_axi_wready),
    .s_axi_bresp  (s_axi_bresp),
    .s_axi_bvalid (s_axi_bvalid),
    .s_axi_bready (s_axi_bready),
    .s_axi_araddr (s_axi_araddr),
    .s_axi_arvalid(s_axi_arvalid),
    .s_axi_arready(s_axi_arready),
    .s_axi_rdata  (s_axi_rdata),
    .s_axi_rresp  (s_axi_rresp),
    .s_axi_rvalid (s_axi_rvalid),
    .s_axi_rready (s_axi_rready),
    // MAC control/status
    .o_mac_tx_en   (cfg_mac_tx_en),
    .o_mac_rx_en   (cfg_mac_rx_en),
    .o_mac_promisc (cfg_mac_promisc),
    .o_mac_allmulti(cfg_mac_allmulti),
    .o_mac_is_1g   (cfg_mac_is_1g),
    .o_mac_ifg     (cfg_mac_ifg),
    .o_mac_addr    (cfg_mac_addr),
    .o_mc_hash     (cfg_mc_hash),
    .o_phy_reset_n (cfg_phy_reset_n),
    .i_link_up     (i_link_up),
    .i_speed       (speed_sync),
    .i_full_duplex (i_full_duplex),
    // statistics
    .o_stats_snapshot(cfg_stats_snapshot),
    .o_stats_reset   (cfg_stats_reset),
    .i_stats         (stats_counts),
    // classifier
    .o_cls_use_pcp     (cfg_cls_use_pcp),
    .o_cls_dmac_check  (cfg_cls_dmac_check),
    .o_cls_default_pcp (cfg_cls_default_pcp),
    .o_cls_pcp_tc_map  (cfg_cls_pcp_tc_map),
    .o_cls_prio_regen  (cfg_cls_prio_regen),
    .o_cls_tc_queue_map(cfg_cls_tc_queue_map),
    // CBS
    .o_cbs_idle_slope(cfg_cbs_idle_slope),
    .o_cbs_hi_credit (cfg_cbs_hi_credit),
    .o_cbs_lo_credit (cfg_cbs_lo_credit),
    .o_cbs_enable    (cfg_cbs_enable),
    // PTP
    .o_ptp_enable      (cfg_ptp_enable),
    .o_ptp_incr        (cfg_ptp_incr),
    .o_ptp_adj         (cfg_ptp_adj),
    .o_ptp_tod_wr      (cfg_ptp_tod_wr),
    .o_ptp_offset      (cfg_ptp_offset),
    .o_ptp_cmd_load    (cfg_ptp_cmd_load),
    .o_ptp_cmd_adjust  (cfg_ptp_cmd_adjust),
    .o_ptp_cmd_snapshot(cfg_ptp_cmd_snapshot),
    .o_ptp_ingress_lat (cfg_ptp_ingress_lat),
    .o_ptp_egress_lat  (cfg_ptp_egress_lat),
    .i_ptp_tod         (ptp_tod_rd),
    .i_ptp_tod_valid   (ptp_tod_rd_valid),
    // ADP advertiser identity/control (0x600 group, FR-DISC-*)
    .o_adp_enable         (cfg_adp_enable),
    .o_adp_valid_time     (cfg_adp_valid_time),
    .o_adp_entity_id      (cfg_adp_entity_id),
    .o_adp_entity_model_id(cfg_adp_entity_model_id),
    .o_adp_entity_caps    (cfg_adp_entity_caps),
    .o_adp_talker_sources (cfg_adp_talker_sources),
    .o_adp_talker_caps    (cfg_adp_talker_caps),
    .o_adp_listener_sinks (cfg_adp_listener_sinks),
    .o_adp_listener_caps  (cfg_adp_listener_caps),
    .o_adp_controller_caps(cfg_adp_controller_caps),
    .o_adp_gptp_gm        (cfg_adp_gptp_gm),
    .o_gptp_pdelay_ns     (cfg_gptp_pdelay_ns),
    .o_adp_gptp_domain    (cfg_adp_gptp_domain),
    .o_adp_current_config (cfg_adp_current_config),
    .o_adp_identify_index (cfg_adp_identify_index),
    .o_adp_interface_index(cfg_adp_interface_index),
    .o_adp_association_id (cfg_adp_association_id),
    .o_adp_advertise_p    (cfg_adp_advertise_p),
    .o_adp_depart_p       (cfg_adp_depart_p),
    .i_adp_available_index(adp_available_index),
    .i_adp_depart_cnt     (adp_depart_cnt),
    .i_adp_rearm_cnt      (adp_rearm_cnt),
    .i_adp_depart_src     (adp_depart_src),
    .i_aecp_locked        (aecp_locked),
    .i_aecp_current_config(aecp_current_config),
    .i_aecp_cmd_count     (aecp_cmd_count),
    .i_aecp_resp_count    (aecp_resp_count),
    .i_acmp_cmd_count     (acmp_cmd_count),
    .i_acmp_resp_count    (acmp_resp_count),
    .o_aaf_enable         (cfg_aaf_enable),
    .o_aaf_bypass         (cfg_aaf_bypass),
    .o_acmp_lobs          (cfg_acmp_lobs),
    .i_acmp_probe_armed   (acmp_probe_armed),
    .i_acmp_talker_active (acmp_talker_active),
    .i_aaf_gate           (aaf_gate),
    .o_aaf_dest_mac       (cfg_aaf_dmac),
    .o_aaf_vid            (cfg_aaf_vid),
    .i_aaf_frames         (aaf_frames_w),
    .i_aaf_pairs          (aaf_pairs_w),
    // lwSRP engine (0x680 group)
    .o_lwsrp_enable       (cfg_lwsrp_enable),
    .o_lwsrp_talker_en    (cfg_lwsrp_talker_en),
    .o_lwsrp_qidx         (cfg_lwsrp_qidx),
    .o_lwsrp_vid          (cfg_lwsrp_vid),
    .o_lwsrp_dest_mac     (cfg_lwsrp_dmac),
    .o_lwsrp_max_frame    (cfg_lwsrp_max_frame),
    .o_lwsrp_interval     (cfg_lwsrp_interval),
    .o_lwsrp_latency      (cfg_lwsrp_latency),
    .i_lwsrp_status       ({lwsrp_rx_drops, lwsrp_tfail_code, 5'd0,
                            lwsrp_tfail_valid, lwsrp_slope_en,
                            lwsrp_stream_gate, lwsrp_over_limit,
                            lwsrp_res_active, lwsrp_domain_ok,
                            lwsrp_talker_declared, lwsrp_listener_ready,
                            lwsrp_listener_reg, lwsrp_listener_decl}),
    .i_lwsrp_slope        (lwsrp_idle_slope),
    .i_lwsrp_cnt          ({lwsrp_rx_pdus, lwsrp_tx_count}),
    // ACMP listener SM (0x6A4 group, RO); bit 31 = CRF sink-1 bound
    .i_acmpl_state        ({acmpl1_bound, 3'd0, acmpl_vlan, acmpl_tk_avail,
                            acmpl_probing, acmpl_status,
                            lwsrp_ta_failed, lwsrp_ta_registered,
                            acmpl_lstn_declare, acmpl_active,
                            acmpl_bound, acmpl_state}),
    .i_acmpl_talker_lo    (acmpl_talker[31:0]),
    .i_acmpl_talker_hi    (acmpl_talker[63:32]),
    .i_acmpl_cnt          ({acmpl_probe_count, acmpl_cmd_count}),
    .i_acmpl_tuid         ({acmpl_tx_wedge, lwsrp_ta_fail_code, acmpl_tuid}),
    .i_acmpl_dbg          (acmpl_dbg),
    .i_avtprx_tsd         (avtprx_last_tsd),
    .i_i2spb_dbg          (i2spb_dbg_frame),
    .i_avtprx_stat        ({avtprx_intr_c[7:0], avtprx_unlocked_c[7:0],
                            avtprx_locked_c[7:0], 7'd0, avtprx_locked}),
    .i_avtprx_frx         (avtprx_frx_c),
    .i_avtprx_err         ({avtprx_seqmm_c[15:0], avtprx_unsupp_c[7:0],
                            avtprx_tu_c[7:0]}),
    .i_pcmrx_cnt          ({pcmrx_drops, pcmrx_pdus}),
    .i_pcmrx_ts           (avtprx_last_ts),
    .i_i2spb_stat         ({i2spb_underruns, i2spb_overruns}),
    .o_i2spb_clr_under    (cfg_i2spb_clru),
    .o_i2spb_clr_over     (cfg_i2spb_clro),
    .i_i2spb_trim         ({i2spb_trim, i2spb_fill}),
    .i_maap_stat0         ({maap_conflicts, maap_defends, maap_offset}),
    .i_maap_stat1         ({29'd0, maap_addr_valid, maap_state}),
    .o_maap_enable        (cfg_maap_enable),
    .o_maap_seed_valid    (cfg_maap_seed_valid),
    .o_maap_count         (cfg_maap_count),
    .o_maap_seed_offset   (cfg_maap_seed_offset),
    .o_tone_enable        (cfg_tone_enable),
    .o_tone_att           (cfg_tone_att),
    // RX dest-MAC TCAM filter programming (0x700 group)
    .o_sw_link          (cfg_sw_link),
    .o_mac_reinit       (cfg_mac_reinit),
    .o_entity_name8     (cfg_entity_name8),
    .o_lpf_enable       (cfg_lpf_enable),
    .o_crf_en           (cfg_crf_en),
    .o_crf_sid          (cfg_crf_sid),
    .i_crf_delta        (crf_delta_w),
    .i_crf_rate         (crf_rate_w),
    .i_crf_status       ({crf_pducnt_w, crf_fmterr_w, crf_seqerr_w}),
    .i_crf_locked       (crf_locked_w),
    .o_crft_en          (cfg_crft_en),
    .o_crft_sid         (cfg_crft_sid),
    .o_crft_dest_mac    (cfg_crft_dmac),
    .i_crft_count       (crft_count_w),
    .i_bdbg0            (aecp_bdbg0_w),
    .i_bdbg1            (aecp_bdbg1_w),
    .i_bdbg2            (aecp_bdbg2_w),
    .i_linkg_stat       (linkg_stat_w),
    .i_mac_reinit       (linkg_reinit_w),
    .o_linkg_dis        (cfg_linkg_dis),
    .o_linkg_freeze     (cfg_linkg_freeze),
    .o_as_parent_ckid   (cfg_as_parent_ckid),
    .o_tcam_default_pass(cfg_tcam_default_pass),
    .o_tcam_wr_en       (cfg_tcam_wr_en),
    .o_tcam_wr_index    (cfg_tcam_wr_index),
    .o_tcam_wr_valid    (cfg_tcam_wr_valid),
    .o_tcam_wr_key      (cfg_tcam_wr_key),
    .o_tcam_wr_mask     (cfg_tcam_wr_mask),
    .o_tcam_wr_action   (cfg_tcam_wr_action),
    // interrupts
    .i_evt_tx_ts_ready  (evt_tx_ts_ready),
    .i_evt_link_change  (evt_link_change),
    .i_evt_rmon_rollover(stats_rollover),
    .o_irq              (csr_irq)
  );

  // ==========================================================================
  //  802.1Q classify + 802.1Qav CBS shaper (CSR-configured)
  // ==========================================================================
  //! lwSRP slope MUX (LWSRP_FPGA_ARCHITECTURE.md §5): an ACTIVE reservation
  //! drives the class-A queue's idleSlope from the granted TSpec and shapes
  //! the queue; the 0x400 CSR values stay intact and win back the moment the
  //! grant releases. No CSR write-back.
  logic [32*NUM_QUEUES-1:0] cbs_idle_slope_mux;
  logic [NUM_QUEUES-1:0]    cbs_enable_mux;
  always_comb begin
    cbs_idle_slope_mux = cfg_cbs_idle_slope;
    cbs_enable_mux     = cfg_cbs_enable;
    if (lwsrp_slope_en) begin
      cbs_idle_slope_mux[32*cfg_lwsrp_qidx +: 32] = lwsrp_idle_slope;
      cbs_enable_mux[cfg_lwsrp_qidx]              = 1'b1;
    end
  end

  traffic_controller_802_1q #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(0),
    .NUMBER_OF_QUEUES(NUM_QUEUES)
  ) traffic_controller(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .is_1g_i(cfg_mac_is_1g),
    .cls_use_pcp_i     (cfg_cls_use_pcp),
    .cls_dmac_check_i  (cfg_cls_dmac_check),
    .cls_default_pcp_i (cfg_cls_default_pcp),
    .cls_pcp_tc_map_i  (cfg_cls_pcp_tc_map),
    .cls_prio_regen_i  (cfg_cls_prio_regen),
    .cls_tc_queue_map_i(cfg_cls_tc_queue_map),
    .cbs_idle_slope_i  (cbs_idle_slope_mux),
    .cbs_hi_credit_i   (cfg_cbs_hi_credit),
    .cbs_lo_credit_i   (cfg_cbs_lo_credit),
    .cbs_shaped_i      (cbs_enable_mux),
    .s_axis(tx_axis_to_shaper),
    .m_axis(tx_axis_shaper_to_ts)
  );

  // ==========================================================================
  //  PTP hardware clock + TX/RX timestamping (CSR-configured)
  // ==========================================================================
  // BIG_ENDIAN(0) + natural 0x88F7: the MAC-side streams carry the FIRST wire
  // byte in tdata[7:0] (Forencich AXIS convention - stated and SILICON-PROVEN
  // by adp_advertiser.sv, whose frames egress correctly through this very
  // path). A 2026-07-13 misdiagnosis flipped this to BIG_ENDIAN(1) after
  // trusting a wrong-convention harness comment - that build (hwts3) parsed
  // src-MAC bytes as the ethertype and emitted nothing; the OOC A/B + the
  // advertiser's comment settled the truth. The redesigned core picks header
  // bytes explicitly, so ETH_TYPE is the natural wire value (no pre-swapped
  // F788 constant).
  ptp_ts_top #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(0),
    .ETH_TYPE(16'h88F7)
  ) ptp_timestamp (
    .gtx_clk(gtx_clk),
    .gtx_resetn(gtx_resetn),
    .axis_clk(axis_clk),
    .axis_resetn(axis_resetn),

    .i_ptp_enable      (cfg_ptp_enable),
    .i_ptp_incr        (cfg_ptp_incr),
    .i_ptp_adj         (cfg_ptp_adj),
    .i_ptp_tod_wr      (cfg_ptp_tod_wr),
    .i_ptp_offset      (cfg_ptp_offset),
    .i_ptp_cmd_load    (cfg_ptp_cmd_load),
    .i_ptp_cmd_adjust  (cfg_ptp_cmd_adjust),
    .i_ptp_cmd_snapshot(cfg_ptp_cmd_snapshot),
    .o_ptp_tod_rd      (ptp_tod_rd),
    .o_ptp_tod_rd_valid(ptp_tod_rd_valid),
    .o_tx_ts_ready     (evt_tx_ts_ready),
    .o_ptp_now         (ptp_now_w),

    .s_axis_tx_tdata(tx_axis_shaper_to_ts.tdata),
    .s_axis_tx_tvalid(tx_axis_shaper_to_ts.tvalid),
    .s_axis_tx_tready(tx_axis_shaper_to_ts.tready),
    .s_axis_tx_tlast(tx_axis_shaper_to_ts.tlast),
    .s_axis_tx_tkeep(tx_axis_shaper_to_ts.tkeep),

    .m_axis_tx_tdata(tx_axis_dp_to_arb.tdata),
    .m_axis_tx_tvalid(tx_axis_dp_to_arb.tvalid),
    .m_axis_tx_tready(tx_axis_dp_to_arb.tready),
    .m_axis_tx_tlast(tx_axis_dp_to_arb.tlast),
    .m_axis_tx_tkeep(tx_axis_dp_to_arb.tkeep),

    .s_axis_rx_tdata(rx_axis_to_ts.tdata),
    .s_axis_rx_tvalid(rx_axis_to_ts.tvalid),
    .s_axis_rx_tready(rx_axis_to_ts.tready),
    .s_axis_rx_tlast(rx_axis_to_ts.tlast),
    .s_axis_rx_tkeep(rx_axis_to_ts.tkeep),

    .m_axis_rx_tdata(rx_axis_ptp_to_filt.tdata),
    .m_axis_rx_tvalid(rx_axis_ptp_to_filt.tvalid),
    .m_axis_rx_tready(rx_axis_ptp_to_filt.tready),
    .m_axis_rx_tlast(rx_axis_ptp_to_filt.tlast),
    .m_axis_rx_tkeep(rx_axis_ptp_to_filt.tkeep),

    .ts_m_axis_tdata(ts_metadata_axis.tdata),
    .ts_m_axis_tvalid(ts_metadata_axis.tvalid),
    .ts_m_axis_tready(ts_metadata_axis.tready),
    .ts_m_axis_tlast(ts_metadata_axis.tlast),
    .ts_m_axis_tkeep(ts_metadata_axis.tkeep)
  );

  // ==========================================================================
  //  RX destination-MAC filter (TCAM, REQ-MAC-02)
  // ==========================================================================
  //! link guard: hardware eth-clock liveness -> automatic MAC reinit across
  //! link bounces (the 2026-07-19 TX-wedge class), plus the first hardware
  //! link estimate. LINK_CTRL[1] stays OR-ed in as the daemon fallback.
  wire [31:0] linkg_stat_w;
  wire        cfg_linkg_dis, cfg_linkg_freeze;
  wire        linkg_reinit_w, linkg_eth_rst_w, linkg_est_w;

  KL_link_guard link_guard (
    .clk_i        (axis_clk),
    .rst_n        (axis_resetn),
    .rx_tgl_i     (i_ethrx_tgl),
    .tx_tgl_i     (i_ethtx_tgl),
    .act_tgl_i    (i_ethact_tgl),
    .dis_i        (cfg_linkg_dis),
    .freeze_i     (cfg_linkg_freeze),
    .man_reinit_i (cfg_mac_reinit),
    .reinit_o     (linkg_reinit_w),
    .eth_rst_o    (linkg_eth_rst_w),
    .link_est_o   (linkg_est_w),
    .stat_o       (linkg_stat_w)
  );

  assign eff_link_w = i_link_up & cfg_sw_link &
                      (cfg_linkg_dis | linkg_est_w);
  //! Counter-only link view: PHY + guard, WITHOUT the linkmon daemon term.
  //! One physical flap = guard pair (41us detect/21ms settle) + a second
  //! sw_link pair 7-14s later (rx-liveness lags the recovered link) -> the
  //! Milan LINK_UP/LINK_DOWN counters read +2 per flap on eff_link. The
  //! counters follow the physical event; eff_link keeps gating ADP/datapath.
  wire cnt_link_w;
  assign cnt_link_w = i_link_up & (cfg_linkg_dis | linkg_est_w);
  assign o_mac_reinit = linkg_reinit_w;
  assign o_eth_rst    = linkg_eth_rst_w;

  rx_mac_filter #(.TDATA_WIDTH(TDATA_WIDTH)) rx_filter (
    .clk_i(axis_clk), .rst_n(axis_resetn),
    .default_pass_i (cfg_tcam_default_pass),
    .tcam_wr_en_i   (cfg_tcam_wr_en),
    .tcam_wr_index_i(cfg_tcam_wr_index[3:0]),
    .tcam_wr_valid_i(cfg_tcam_wr_valid),
    .tcam_wr_key_i  (cfg_tcam_wr_key),
    .tcam_wr_mask_i (cfg_tcam_wr_mask),
    .tcam_wr_action_i(cfg_tcam_wr_action),
    .s_tdata (rx_axis_ptp_to_filt.tdata),
    .s_tkeep (rx_axis_ptp_to_filt.tkeep),
    .s_tvalid(rx_axis_ptp_to_filt.tvalid),
    .s_tlast (rx_axis_ptp_to_filt.tlast),
    .s_tready(rx_axis_ptp_to_filt.tready),
    .m_tdata (rx_axis_to_dma.tdata),
    .m_tkeep (rx_axis_to_dma.tkeep),
    .m_tvalid(rx_axis_to_dma.tvalid),
    .m_tlast (rx_axis_to_dma.tlast),
    .m_tready(rx_axis_to_dma.tready),
    .frame_action_o(), .frame_match_o(), .frame_dropped_o()
  );

  // ==========================================================================
  //  ADP advertiser (IEEE 1722.1 / Milan v1.2) + MAC-TX arbiter
  // ==========================================================================
  //! 1-second tick for the ADP re-advertise timer. MUST track the actual
  //! datapath clock: the old hardcoded 100_000_000 made a 50 MHz datapath
  //! (Arty) tick every 2 s, stretching the re-advertise period to 62 s =
  //! exactly the ADP validity horizon (2*valid_time at valid_time 31) with
  //! zero margin, instead of the intended half-validity cadence.
  localparam int ADP_TICK_DIV = MILAN_CLK_FREQ_HZ;
  reg [26:0] adp_tick_cnt;
  reg        adp_tick_1s;
  always_ff @(posedge axis_clk) begin : adp_tick_gen
    if (!axis_resetn) begin
      adp_tick_cnt <= 27'd0; adp_tick_1s <= 1'b0;
    end else if (adp_tick_cnt >= ADP_TICK_DIV-1) begin
      adp_tick_cnt <= 27'd0; adp_tick_1s <= 1'b1;
    end else begin
      adp_tick_cnt <= adp_tick_cnt + 27'd1; adp_tick_1s <= 1'b0;
    end
  end

  //! Link edge -> advertise (up) / depart (down). ALSO synthesize the link-up
  //! event on an ADP-ENABLE rising edge while the link is already up: on the
  //! fully-FPGA SoC i_link_up is constant 1 (no MDIO tracking yet), so its only
  //! real edge fires one cycle after reset while ADP is still disabled (CSR
  //! reset default) - without this, enabling ADP later could NEVER reach the
  //! advertiser's available state (available_r needs link_up_i && enable_i;
  //! silicon-diagnosed 2026-07-11: strobes swallowed, available_index stuck 0).
  //! Per 1722.1 semantics an entity being enabled on a live link advertises.
  reg link_up_q; reg adp_en_q; reg adp_link_up_p, adp_link_down_p;
  always_ff @(posedge axis_clk) begin : adp_link_edge
    if (!axis_resetn) begin
      link_up_q <= 1'b0; adp_en_q <= 1'b0;
      adp_link_up_p <= 1'b0; adp_link_down_p <= 1'b0;
    end else begin
      link_up_q       <= i_link_up;
      adp_en_q        <= cfg_adp_enable;
      adp_link_up_p   <= (i_link_up & ~link_up_q) |
                         (cfg_adp_enable & ~adp_en_q & i_link_up);
      adp_link_down_p <= ~i_link_up &  link_up_q;
    end
  end

  //! discover-DELAY range scaled by the datapath clock (the params are in
  //! clk cycles; unscaled, the 100 MHz AX halved the wall-time range and
  //! failed the CERT es-2.1 randomness spread). BASE = 200 ms; the mask
  //! passes the full 26-bit LFSR = up to ~0.67 s @100 MHz / ~1.34 s @50 MHz
  //! (both << the 4.5 s TMR_DELAY bound).
  adp_advertiser #(
    .DISC_DLY_BASE (MILAN_CLK_FREQ_HZ / 5),
    .DISC_DLY_MASK (26'h3FF_FFFF)
  ) adp_adv (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .tick_i   (adp_tick_1s),
    .link_level_i  (eff_link_w),
    .link_up_i     (adp_link_up_p),
    .link_down_i   (adp_link_down_p),
    .shutdown_i    (cfg_adp_depart_p),
    .gm_change_i   (1'b0),
    .info_changed_i(cfg_adp_advertise_p),
    .rcv_discover_i(aecp_discover_p),   // ENTITY_DISCOVER decoded by KL_aecp_ingress
    // cfg_mac_addr is the PLATFORM (CSR) convention: [7:0] = FIRST wire byte
    // (the driver packs MAC_ADDR_LO/HI that way and the RX filter consumes it
    // that way). The advertiser's port is a numeric EUI-48 ([47:40] = first
    // byte, matching its harness + the 1722.1 field constants), so byte-reverse
    // at the boundary. Without this the ADP source MAC egressed byte-swapped =
    // a MULTICAST source address (01:..), which 802.1D bridges MUST discard -
    // silicon-diagnosed 2026-07-11 through the AVB switch (index bumped, wire
    // silent).
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .valid_time_i  (cfg_adp_valid_time),
    .entity_id_i             (cfg_adp_entity_id),
    .entity_model_id_i       (cfg_adp_entity_model_id),
    .entity_capabilities_i   (cfg_adp_entity_caps),
    .talker_stream_sources_i (cfg_adp_talker_sources),
    .talker_capabilities_i   (cfg_adp_talker_caps),
    .listener_stream_sinks_i (cfg_adp_listener_sinks),
    .listener_capabilities_i (cfg_adp_listener_caps),
    .controller_capabilities_i(cfg_adp_controller_caps),
    .gptp_grandmaster_id_i   (cfg_adp_gptp_gm),
    .gptp_domain_number_i    (cfg_adp_gptp_domain),
    .current_configuration_index_i(cfg_adp_current_config),
    .identify_control_index_i(cfg_adp_identify_index),
    .interface_index_i       (cfg_adp_interface_index),
    .association_id_i        (cfg_adp_association_id),
    .m_axis_tdata (adp_tx_tdata),
    .m_axis_tkeep (adp_tx_tkeep),
    .m_axis_tvalid(adp_tx_tvalid),
    .m_axis_tlast (adp_tx_tlast),
    .m_axis_tready(adp_tx_tready),
    .available_index_o(adp_available_index),
    .busy_o (),
    .frame_sent_o (),
    .depart_cnt_o (adp_depart_cnt),
    .rearm_cnt_o  (adp_rearm_cnt),
    .depart_src_o (adp_depart_src)
  );

  // ==========================================================================
  //  AECP / AEM listener (IEEE 1722.1 / Milan v1.2). Non-intrusive MONITOR of
  //  the post-filter RX stream (rx_axis_to_dma — reads only, never drives its
  //  tready) answers AECP commands against the 5-descriptor Milan entity and
  //  decodes ENTITY_DISCOVER -> aecp_discover_p. Response frames merge with the
  //  advertiser in a low-rate arbiter that takes the ADP slot below. Identity =
  //  the milan_csr 0x600 group, so ADP and AEM cannot disagree.
  // ==========================================================================
  KL_aecp_top #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) aecp_listener (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .entity_id_i       (cfg_adp_entity_id),
    .entity_model_id_i (cfg_adp_entity_model_id),
    .entity_name8_i    (cfg_entity_name8),
    .entity_caps_i     (cfg_adp_entity_caps),
    .talker_sources_i  (cfg_adp_talker_sources),
    .talker_caps_i     (cfg_adp_talker_caps),
    .listener_sinks_i  (cfg_adp_listener_sinks),
    .listener_caps_i   (cfg_adp_listener_caps),
    .controller_caps_i (cfg_adp_controller_caps),
    .available_index_i (adp_available_index),
    .association_id_i  (cfg_adp_association_id),
    .gptp_gm_id_i      (cfg_adp_gptp_gm),
    .pdelay_ns_i       (cfg_gptp_pdelay_ns),
    .gptp_domain_i     (cfg_adp_gptp_domain),
    .aaf_dmac_i (eff_aaf_dmac), .aaf_vid_i (cfg_aaf_vid),
    .talker_active_i (acmp_talker_active),
    .listener_observed_i (listener_observed_w),
    .pres_offset_o (aecp_pres_offset),
    .identify_o    (o_identify),
    .link_up_i     (cnt_link_w),
    .frames_tx_i   (aaf_frames_w),
    .lstn_bound_i   (acmpl_bound),
    .lstn_sid_i     (acmpl_sid),
    .lstn_dmac_i    (acmpl_dmac),
    .lstn1_bound_i  (acmpl1_bound),
    .lstn1_sid_i    (acmpl1_sid),
    .lstn1_dmac_i   (acmpl1_dmac),
    .bdbg0_o        (aecp_bdbg0_w),
    .bdbg1_o        (aecp_bdbg1_w),
    .bdbg2_o        (aecp_bdbg2_w),
    .lstn_vlan_i    (acmpl_vlan),
    .lstn_pbsta_i   (acmpl_probing),
    .lstn_acmpsta_i (acmpl_status),
    .lstn_ta_reg_i  (lwsrp_ta_registered),
    .lstn_ta_fail_i (lwsrp_ta_failed),
    .as_parent_ckid_i   (cfg_as_parent_ckid),
    .lstn_fail_code_i   (lwsrp_ta_fail_code),
    .lstn_fail_bridge_i (lwsrp_ta_fail_bridge),
    .lstn_ta_vlan_i     (lwsrp_ta_vlan),
    .lstn_ta_acclat_i   (lwsrp_ta_acclat),
    .tk_fail_valid_i    (lwsrp_tfail_valid),
    .tk_fail_code_i     (lwsrp_tfail_code),
    .tk_fail_bridge_i   (lwsrp_tfail_bridge),
    .srp_domain_vid_i   (cfg_lwsrp_vid),
    //! CLOCK_DOMAIN lock events follow the ACTIVE clock source: index 2 =
    //! the CRF input engine, else the AAF media-lock monitor (Milan 5.4.4)
    .in0_cnt_locked_i      ((aecp_clk_src == 16'd2) ? crf_cnt_locked_w
                                                    : avtprx_locked_c),
    .in0_cnt_unlocked_i    ((aecp_clk_src == 16'd2) ? crf_cnt_unlocked_w
                                                    : avtprx_unlocked_c),
    .in0_cnt_interrupted_i (avtprx_intr_c),
    .in0_cnt_seqmm_i       (avtprx_seqmm_c),
    .in0_cnt_tu_i          (avtprx_tu_c),
    .in0_cnt_unsupp_i      (avtprx_unsupp_c),
    .in0_cnt_frx_i         (avtprx_frx_c),
    .in0_cnt_mreset_i      (avtprx_mreset_c),
    .in0_cnt_late_i        (avtprx_late_c),
    .in0_cnt_early_i       (avtprx_early_c),
    .in0_cnt_dirty_p_i     (avtprx_dirty_p),
    .in0_fmt_o             (aecp_in0_fmt),
    .clk_src_o             (aecp_clk_src),
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tdata_i  (rx_axis_to_dma.tdata),
    .rx_tkeep_i  (rx_axis_to_dma.tkeep),
    .rx_tlast_i  (rx_axis_to_dma.tlast),
    .adp_discover_o (aecp_discover_p),
    .m_axis_tdata (aecp_tx_tdata), .m_axis_tkeep (aecp_tx_tkeep),
    .m_axis_tvalid(aecp_tx_tvalid), .m_axis_tlast (aecp_tx_tlast),
    .m_axis_tready(aecp_tx_tready),
    .locked_o(aecp_locked), .current_config_o(aecp_current_config),
    .cmd_count_o(aecp_cmd_count), .resp_count_o(aecp_resp_count)
  );

  // ==========================================================================
  //  ACMP stateless responder (Milan v1.2 §5.5) — same monitor-tap pattern.
  //  GET_TX_STATE -> SUCCESS/count=0; GET_TX_CONNECTION + CONNECT/DISCONNECT_TX
  //  -> NOT_SUPPORTED (connection POLICY is the softcore's, via a future
  //  mailbox — docs/ARCHITECTURE_HW_SW_SPLIT.md).
  // ==========================================================================
  KL_acmp_responder acmp_responder (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .aaf_dmac_i (eff_aaf_dmac), .aaf_vid_i (cfg_aaf_vid),
    .tick_1s_i (adp_tick_1s),
    .listener_observed_i (listener_observed_w),
    .talker_active_o (acmp_talker_active),
    .probe_armed_o (acmp_probe_armed),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .entity_id_i (cfg_adp_entity_id),
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tdata_i  (rx_axis_to_dma.tdata),
    .rx_tkeep_i  (rx_axis_to_dma.tkeep),
    .rx_tlast_i  (rx_axis_to_dma.tlast),
    .m_axis_tdata (acmp_tx_tdata), .m_axis_tkeep (acmp_tx_tkeep),
    .m_axis_tvalid(acmp_tx_tvalid), .m_axis_tlast (acmp_tx_tlast),
    .m_axis_tready(acmp_tx_tready),
    .cmd_count_o (acmp_cmd_count), .resp_count_o (acmp_resp_count)
  );

  // ==========================================================================
  //  ACMP listener SM (Milan v1.2 §5.5, FR-CONN-01) — the STREAM_INPUT[0]
  //  sink: BIND_RX/UNBIND_RX/GET_RX_STATE + the talker-probe ladder; SRP
  //  coupling through the lwSRP TalkerAdvertise registrar + the Listener
  //  attribute applicant below.
  // ==========================================================================
  KL_acmp_listener #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) acmp_listener_sm (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .entity_id_i (cfg_adp_entity_id),
    .tick_1s_i (adp_tick_1s),
    .ta_registered_i (lwsrp_ta_registered),
    .ta_failed_i     (lwsrp_ta_failed),
    .lstn_declare_o  (acmpl_lstn_declare),
    .bound_sid_o     (acmpl_sid),
    .stream_vlan_o   (acmpl_vlan),
    .stream_dmac_o   (acmpl_dmac),
    .stream_active_o (acmpl_active),
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tdata_i  (rx_axis_to_dma.tdata),
    .rx_tkeep_i  (rx_axis_to_dma.tkeep),
    .rx_tlast_i  (rx_axis_to_dma.tlast),
    .m_axis_tdata (acmpl_tx_tdata), .m_axis_tkeep (acmpl_tx_tkeep),
    .m_axis_tvalid(acmpl_tx_tvalid), .m_axis_tlast (acmpl_tx_tlast),
    .m_axis_tready(acmpl_tx_tready),
    .state_o (acmpl_state),
    .bound_talker_o (acmpl_talker),
    .bound_tuid_o   (acmpl_tuid),
    .acmp_status_o  (acmpl_status),
    .probing_o      (acmpl_probing),
    .tk_avail_o     (acmpl_tk_avail),
    .cmd_count_o    (acmpl_cmd_count),
    .probe_count_o  (acmpl_probe_count),
    .tx_wedge_cnt_o (acmpl_tx_wedge),
    .dbg_o          (acmpl_dbg),
    .s1_bound_o     (acmpl1_bound),
    .s1_sid_o       (acmpl1_sid),
    .s1_dmac_o      (acmpl1_dmac)
  );

  // ==========================================================================
  //  AVTP RX monitor (Milan v1.2 §5.4.5.3, Table 7-156) — non-intrusive
  //  parser on the same RX tap, matched to the BOUND stream_id from the ACMP
  //  listener SM; the counter engine feeds AECP GET_COUNTERS(STREAM_INPUT 0),
  //  its 1 Hz unsolicited push, and the 0x6B8 CSR observability group.
  // ==========================================================================
  //! NXN §1.1 (P1): stream-table classification authority. Entry 0 aliases
  //! the ACMP bound record combinationally (bit-exact N=1 legacy); entries
  //! 1..N-1 + bench overrides arrive via the 0x800 CSR window (phase P11 -
  //! the write port is parked until then).
  localparam int NSIDX_W_C = (N_STREAMS <= 1) ? 1 : $clog2(N_STREAMS);
  wire [64*N_STREAMS-1:0] strtbl_sid_w;
  wire [N_STREAMS-1:0]    strtbl_en_w;
  wire [N_STREAMS-1:0]    strtbl_bind_rise_w;
  wire [NSIDX_W_C-1:0]    avtprx_idx;

  KL_stream_table #(.N_LISTENERS_P(N_STREAMS)) stream_table (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .bound0_i (acmpl_bound), .sid0_i (acmpl_sid),
    .wr_en_i (1'b0), .wr_idx_i (4'd0),          //! P11 CSR-window hook
    .wr_sid_i (64'd0), .wr_valid_i (1'b0),
    .tbl_sid_o (strtbl_sid_w), .tbl_en_o (strtbl_en_w),
    .bind_rise_o (strtbl_bind_rise_w)
  );

  avtp_stream_parser #(
    .TDATA_WIDTH (TDATA_WIDTH), .BIG_ENDIAN (0), .N_STREAMS (N_STREAMS)
  ) avtp_rx_parser (
    .clk (axis_clk), .resetn (axis_resetn),
    .cfg_stream_id_i (strtbl_sid_w),
    .cfg_stream_en_i (strtbl_en_w),
    //! PRE-FILTER tap (2026-07-19): the media path must not depend on the
    //! kernel's dest-MAC filter config - the TCAM now shields the CPU from
    //! the AVTP multicast flood (16 kfps ate the 1-hart kernel: 55k RX
    //! drops, pdelay responses down to 35% = asCapable flaps at the switch)
    //! while the fabric keeps consuming the stream here.
    .s_tdata_i  (rx_axis_ptp_to_filt.tdata),
    .s_tkeep_i  (rx_axis_ptp_to_filt.tkeep),
    .s_tvalid_i (rx_axis_ptp_to_filt.tvalid),
    .s_tready_i (rx_axis_ptp_to_filt.tready),
    .s_tlast_i  (rx_axis_ptp_to_filt.tlast),
    .match_valid_o (avtprx_match),
    .match_index_o (avtprx_idx),
    .stream_id_o   (avtprx_sid_frame),
    .avtp_ts_o     (avtprx_ts),
    .subtype_o     (avtprx_subtype),
    .ts_valid_o    (),
    .seq_num_o     (avtprx_seq),
    .ts_uncertain_o(avtprx_tu_bit),
    .fsh_o         (avtprx_fsh),
    .fsh2_o        (avtprx_fsh2),
    .parse_valid_o (avtprx_parse_p),
    .b3_o          (avtprx_b3),
    .avtp_frames_o (),
    .matched_frames_o ()
  );

  // ==========================================================================
  //  CRF Media Clock Input engine (Milan 7.3.2) - measurement half: parses
  //  and validates the Avnu Pro Audio CRF stream selected by the CRF CSRs,
  //  produces the phase/frequency error the media-clock servo consumes and
  //  the CLOCK_DOMAIN lock events for clock_source = CRF. The ACMP sink-1
  //  bind chain is the remaining CRF work (MILAN_COMPLIANCE_GAPS.md).
  // ==========================================================================
  KL_crf_rx #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) crf_rx (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .frame_p_i   (avtprx_parse_p),
    .subtype_i   (avtprx_subtype),
    .seq_i       (avtprx_seq),
    .sid_frame_i (avtprx_sid_frame),
    .pullbase_i  (avtprx_ts),
    .fsh_i       (avtprx_fsh),
    .fsh2_i      (avtprx_fsh2),
    .type_i      (avtprx_b3),
    .ptp_now_i   (ptp_now_w),
    //! ACMP sink-1 bind wins; the CSR pair stays the manual bench lever
    .en_i        (cfg_crf_en | acmpl1_bound),
    .sid_i       (acmpl1_bound ? acmpl1_sid : cfg_crf_sid),
    .delta_o     (crf_delta_w),
    .rate_o      (crf_rate_w),
    .pdu_count_o (crf_pducnt_w),
    .fmt_err_o   (crf_fmterr_w),
    .seq_err_o   (crf_seqerr_w),
    .locked_o    (crf_locked_w),
    .cnt_locked_o   (crf_cnt_locked_w),
    .cnt_unlocked_o (crf_cnt_unlocked_w)
  );

  // ==========================================================================
  //  CRF Media Clock Output engine (Milan 7.3.1) - talker half: emits the
  //  Avnu Pro Audio CRF stream (500 PDU/s) with gPTP timestamps captured on
  //  the REAL audio-MMCM 96-sample event grid. Joins the low-rate control
  //  merge untagged (no MSRP TA yet - see the module header).
  // ==========================================================================
  KL_crf_tx crf_tx (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .clk_audio_i (clk_audio_i),
    .enable_i      (cfg_crft_en),
    .sid_i         (cfg_crft_sid),
    .dest_mac_i    (cfg_crft_dmac),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    //! Milan: the presentation time offset applies to CRF like any stream -
    //! same source of truth as the AAF framer (SET_STREAM_INFO ACC_LAT/MTT)
    .transit_ns_i  (aecp_pres_offset),
    .ptp_ns_i      (ptp_now_w),
    .m_axis_tdata (crft_tx_tdata), .m_axis_tkeep (crft_tx_tkeep),
    .m_axis_tvalid(crft_tx_tvalid), .m_axis_tlast (crft_tx_tlast),
    .m_axis_tready(crft_tx_tready),
    .tx_count_o (crft_count_w)
  );

  //! wire-truth channel count (USER 1-to-1 rule): the RENDER path follows
  //! the last accepted PDU's channels_per_frame, never the AEM store
  wire [7:0] mon_wire_chans_w;

  //! NXN P2: the shared monitor engine (LCTX context RAM, N_STREAMS
  //! contexts) replaces the flat single-stream KL_avtp_rx_monitor. All
  //! legacy 0x6B8-group wires alias stream 0 (no-regression axiom); the
  //! LCTX window port is parked until the P11 indexed CSR window.
  wire        avtprx_accept_p_w;
  wire [3:0]  avtprx_accept_idx_w;
  wire        pcmrx_pdu_p_w, pcmrx_drop_p_w;
  wire [3:0]  pcmrx_pdu_idx_w, pcmrx_drop_idx_w;
  assign avtprx_accept_p = avtprx_accept_p_w;

  KL_avtp_rx_monitor_ctx #(
    .N_LISTENERS_P (N_STREAMS),
    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ)
  ) avtp_rx_monitor (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .match_valid_i  (avtprx_match),
    .match_index_i  (4'(avtprx_idx)),
    .subtype_i      (avtprx_subtype),
    .seq_num_i      (avtprx_seq),
    .ts_uncertain_i (avtprx_tu_bit),
    .avtp_ts_i      (avtprx_ts),
    .fsh_i          (avtprx_fsh),
    .bound_i        (strtbl_en_w),
    .bind_rise_i    (strtbl_bind_rise_w),
    .sid0_i         (acmpl_sid),
    .fmt0_i         (aecp_in0_fmt),
    .ptp_now_i      (ptp_now_w[31:0]),
    .pres_ofs_i     (aecp_pres_offset),
    .media_reset_p_i(i2spb_reset_p),
    .clk_src_i      (aecp_clk_src),
    .servo_conv_i   (i2spb_converged),
    .render_sel_i   (route_render_sel_w),  //! route policy's RENDER stream
    .depkt_pdu_p_i    (pcmrx_pdu_p_w),
    .depkt_pdu_idx_i  (pcmrx_pdu_idx_w),
    .depkt_drop_p_i   (pcmrx_drop_p_w),
    .depkt_drop_idx_i (pcmrx_drop_idx_w),
    .lctx_wr_en_i (1'b0), .lctx_wr_addr_i (8'd0),   //! P11 window hook
    .lctx_wr_data_i (32'd0), .lctx_wr_rdy_o (),
    .lctx_rd_en_i (1'b0), .lctx_rd_addr_i (8'd0),
    .lctx_rd_data_o (), .lctx_rd_valid_o (),
    .cnt_media_locked_o       (avtprx_locked_c),
    .cnt_media_unlocked_o     (avtprx_unlocked_c),
    .cnt_stream_interrupted_o (avtprx_intr_c),
    .cnt_seq_mismatch_o       (avtprx_seqmm_c),
    .cnt_ts_uncertain_o       (avtprx_tu_c),
    .cnt_unsupported_fmt_o    (avtprx_unsupp_c),
    .cnt_frames_rx_o          (avtprx_frx_c),
    .wire_chans_o             (mon_wire_chans_w),
    .cnt_media_reset_o (avtprx_mreset_c),
    .cnt_late_ts_o     (avtprx_late_c),
    .cnt_early_ts_o    (avtprx_early_c),
    .media_locked_o (avtprx_locked),
    .dirty_p_o      (avtprx_dirty_p),
    .pdu_accept_p_o   (avtprx_accept_p_w),
    .pdu_accept_idx_o (avtprx_accept_idx_w),
    .last_ts_o      (avtprx_last_ts),
    .last_tsd_o     (avtprx_last_tsd)
  );

  // ==========================================================================
  //  AAF RX depacketizer (listener media path) — same RX tap; the monitor's
  //  accept pulse is the commit verdict, so the PCM ring receives exactly
  //  the PDUs FRAMES_RX counts. Payload leaves as full 8-byte beats in wire
  //  order (S32BE interleaved) toward the SoC DRAM PCM ring writer.
  // ==========================================================================
  KL_aaf_rx_depacketizer aaf_rx_depkt (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    //! pre-filter tap - see avtp_rx_parser note
    .s_tdata_i  (rx_axis_ptp_to_filt.tdata),
    .s_tkeep_i  (rx_axis_ptp_to_filt.tkeep),
    .s_tvalid_i (rx_axis_ptp_to_filt.tvalid),
    .s_tready_i (rx_axis_ptp_to_filt.tready),
    .s_tlast_i  (rx_axis_ptp_to_filt.tlast),
    .pdu_accept_p_i (avtprx_accept_p),
    //! NXN §1.1 tuser tag: the shared monitor's per-stream accept index
    .pdu_accept_idx_i (avtprx_accept_idx_w),
    .m_axis_tdata (dpkt_pcm_tdata_w),
    .m_axis_tkeep (m_axis_pcm_tkeep),
    .m_axis_tvalid(dpkt_pcm_tvalid_w),
    .m_axis_tlast (dpkt_pcm_tlast_w),
    .m_axis_tuser (dpkt_pcm_tuser_w),
    .m_axis_tready(dpkt_pcm_tready_w),
    .pdus_o  (pcmrx_pdus),
    .drops_o (pcmrx_drops),
    .pdu_out_p_o (pcmrx_pdu_p_w), .pdu_out_idx_o (pcmrx_pdu_idx_w),
    .drop_p_o (pcmrx_drop_p_w), .drop_idx_o (pcmrx_drop_idx_w)
  );

  // ==========================================================================
  //  PCM routing policy (NXN §1.3, P3) — per-stream route field between the
  //  shared depacketizer and the sinks: RENDER (lowest-indexed wins) feeds
  //  the LPF + I2S playback tap, DMA streams ride the ring output tagged
  //  with tuser = s, NULL discards. Reset default (s0 = RENDER, others
  //  NULL) is today's shape bit-exactly; the route write port is parked
  //  until the P11 CSR window.
  // ==========================================================================
  wire [TDATA_WIDTH-1:0] dpkt_pcm_tdata_w;
  wire                   dpkt_pcm_tvalid_w, dpkt_pcm_tlast_w;
  wire [3:0]             dpkt_pcm_tuser_w;
  wire                   dpkt_pcm_tready_w;
  wire [TDATA_WIDTH-1:0] rend_pcm_tdata_w;
  wire                   rend_pcm_tvalid_w, rend_pcm_tlast_w;
  wire [3:0]             route_render_sel_w;

  KL_pcm_route #(.N_LISTENERS_P(N_STREAMS)) pcm_route (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_tdata_i (dpkt_pcm_tdata_w), .s_tvalid_i (dpkt_pcm_tvalid_w),
    .s_tlast_i (dpkt_pcm_tlast_w), .s_tuser_i (dpkt_pcm_tuser_w),
    .s_tready_o (dpkt_pcm_tready_w),
    .route_wr_en_i (1'b0), .route_wr_idx_i (4'd0),   //! P11 window hook
    .route_wr_val_i (2'd0),
    .m_axis_tdata (m_axis_pcm_tdata), .m_axis_tvalid (m_axis_pcm_tvalid),
    .m_axis_tlast (m_axis_pcm_tlast), .m_axis_tuser (m_axis_pcm_tuser),
    .m_axis_tready (m_axis_pcm_tready),
    .render_tvalid_o (rend_pcm_tvalid_w), .render_tdata_o (rend_pcm_tdata_w),
    .render_tlast_o (rend_pcm_tlast_w),
    .render_sel_o (route_render_sel_w), .render_active_o ()
  );

  // ==========================================================================
  //  I2S playback (Pmod I2S2 DAC) — zero-CPU audible listener: taps the
  //  depacketizer PCM transfers and serializes ch0/ch1 on the line-out.
  //  Free-running local 48 kHz (MVP): drift vs the talker is absorbed by
  //  the FIFO rails and MEASURED via I2SPB_STAT until CRF media-clock
  //  discipline lands.
  // ==========================================================================
  //! 2nd-order Butterworth LPF on the DAC render tap only (the DMA-ring /
  //! AVB copies stay bit-true): band-limits the analog output feeding the
  //! loop ADC. LPF_CTRL 0x72C[0], default on; auto-bypass for !=2ch.
  //! render tap = the route policy's RENDER stream share of the ring
  //! handshake (bit-identical to the flat m_axis_pcm tap at N=1)
  KL_pcm_lpf pcm_lpf (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_lpf_enable),
    .chans_i  ({2'b0, mon_wire_chans_w}),   //! wire truth (2ch engages)
    .s_tdata  (rend_pcm_tdata_w),
    .s_tvalid (rend_pcm_tvalid_w),
    .s_tready (m_axis_pcm_tready),
    .m_tdata  (pcm_lpf_tdata),
    .m_tvalid (pcm_lpf_tvalid),
    .active_o (pcm_lpf_active)
  );

  KL_i2s_playback #(.MCLK_DIV_LOG2(MCLK_DIV_LOG2_C),
                    .CLK_FREQ_HZ(MILAN_CLK_FREQ_HZ),
                    .PREFILL_C(PB_PREFILL_C)) i2s_player (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .clk_audio_i  (clk_audio_i),
    .servo_en_i   (aecp_clk_src != 16'd0),
    .pcm_tdata_i  (rend_pcm_tdata_w),
    .lpf_tdata_i  (pcm_lpf_tdata),
    .lpf_tvalid_i (pcm_lpf_tvalid),
    .lpf_active_i (pcm_lpf_active),
    .pcm_tvalid_i (rend_pcm_tvalid_w),
    .pcm_tready_i (m_axis_pcm_tready),
    .pcm_tlast_i  (rend_pcm_tlast_w),
    .wire_chans_i (mon_wire_chans_w),
    .i2s_mclk_o (i2s_dac_mclk_o), .i2s_sclk_o (i2s_dac_sclk_o),
    .i2s_lrck_o (i2s_dac_lrck_o), .i2s_sdin_o (i2s_dac_sdin_o),
    .clr_under_i (cfg_i2spb_clru), .clr_over_i (cfg_i2spb_clro),
    .underruns_o (i2spb_underruns), .overruns_o (i2spb_overruns),
    .trim_o (i2spb_trim), .fill_o (i2spb_fill),
    .media_reset_p_o (i2spb_reset_p),
    .converged_o     (i2spb_converged),
    .dbg_frame_o     (i2spb_dbg_frame)
  );

  // ==========================================================================
  //  MAAP engine (IEEE 1722 Annex B) — dynamic stream-DMAC allocation.
  //  Same monitor-tap + low-rate-TX recipe; addr_valid gates AAF admission
  //  and muxes the effective stream DMAC when MAAP_CTRL.en=1.
  // ==========================================================================
  KL_maap #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) maap_engine (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_maap_enable),
    .count_i  (cfg_maap_count),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .seed_offset_i (cfg_maap_seed_offset),
    .seed_valid_i  (cfg_maap_seed_valid),
    .rx_tdata_i  (rx_axis_to_dma.tdata),
    .rx_tkeep_i  (rx_axis_to_dma.tkeep),
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tready_i (rx_axis_to_dma.tready),
    .rx_tlast_i  (rx_axis_to_dma.tlast),
    .m_axis_tdata (maap_tx_tdata), .m_axis_tkeep (maap_tx_tkeep),
    .m_axis_tvalid(maap_tx_tvalid), .m_axis_tlast (maap_tx_tlast),
    .m_axis_tready(maap_tx_tready),
    .addr_o (maap_addr), .addr_valid_o (maap_addr_valid),
    .state_o (maap_state), .offset_o (maap_offset),
    .conflicts_o (maap_conflicts), .defends_o (maap_defends)
  );

  // ==========================================================================
  //  lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 §5.6) — same monitor-tap +
  //  low-rate-TX recipe. Declares Domain/TalkerAdvertise/VID, registers the
  //  Listener attribute for our stream, and resolves the reservation into
  //  the AAF admission gate + the CBS class-A slope (mux above).
  // ==========================================================================
  KL_lwsrp_top #(.CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ)) lwsrp (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .enable_i (cfg_lwsrp_enable),
    .talker_en_i (cfg_lwsrp_talker_en),
    .is_1g_i (cfg_mac_is_1g),
    .lstn_bound_i   (acmpl_bound),
    .lstn_declare_i (acmpl_lstn_declare),
    .lstn_sid_i     (acmpl_sid),
    .ta_registered_o (lwsrp_ta_registered),
    .ta_failed_o     (lwsrp_ta_failed),
    .ta_fail_code_o  (lwsrp_ta_fail_code),
    .ta_vlan_o       (lwsrp_ta_vlan),
    .ta_acclat_o     (lwsrp_ta_acclat),
    .ta_fail_bridge_o(lwsrp_ta_fail_bridge),
    .tfail_bridge_o  (lwsrp_tfail_bridge),
    .lstn_declared_o (lwsrp_lstn_declared),
    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],
                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],
                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),
    .unique_id_i (16'd0),          // stream_id = {station_mac, 0} everywhere
    .dest_mac_i (cfg_lwsrp_dmac),
    .vid_i (cfg_lwsrp_vid),
    .max_frame_i (cfg_lwsrp_max_frame),
    .interval_frames_i (cfg_lwsrp_interval),
    .latency_i (cfg_lwsrp_latency),
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tdata_i  (rx_axis_to_dma.tdata),
    .rx_tkeep_i  (rx_axis_to_dma.tkeep),
    .rx_tlast_i  (rx_axis_to_dma.tlast),
    .m_axis_tdata (lwsrp_tx_tdata), .m_axis_tkeep (lwsrp_tx_tkeep),
    .m_axis_tvalid(lwsrp_tx_tvalid), .m_axis_tlast (lwsrp_tx_tlast),
    .m_axis_tready(lwsrp_tx_tready),
    .stream_gate_o (lwsrp_stream_gate),
    .slope_en_o (lwsrp_slope_en), .idle_slope_o (lwsrp_idle_slope),
    .res_active_o (lwsrp_res_active),
    .listener_ready_o (lwsrp_listener_ready),
    .talker_declared_o (lwsrp_talker_declared),
    .listener_reg_o (lwsrp_listener_reg), .listener_decl_o (lwsrp_listener_decl),
    .domain_ok_o (lwsrp_domain_ok), .over_limit_o (lwsrp_over_limit),
    .tfail_valid_o (lwsrp_tfail_valid), .tfail_code_o (lwsrp_tfail_code),
    .tx_count_o (lwsrp_tx_count),
    .rx_pdus_o (lwsrp_rx_pdus), .rx_drops_o (lwsrp_rx_drops)
  );

  //! AECP response (s_data) + ACMP response (s_adp) -> one control stream.
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) aecp_acmp_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (aecp_tx_tdata),  .s_data_tkeep (aecp_tx_tkeep),
    .s_data_tvalid(aecp_tx_tvalid), .s_data_tlast (aecp_tx_tlast),
    .s_data_tready(aecp_tx_tready),
    .s_adp_tdata (acmp_tx_tdata),  .s_adp_tkeep (acmp_tx_tkeep),
    .s_adp_tvalid(acmp_tx_tvalid), .s_adp_tlast (acmp_tx_tlast),
    .s_adp_tready(acmp_tx_tready),
    .m_tdata (ctl2_tx_tdata), .m_tkeep (ctl2_tx_tkeep),
    .m_tvalid(ctl2_tx_tvalid), .m_tlast (ctl2_tx_tlast), .m_tready(ctl2_tx_tready)
  );

  //! Low-rate control merge: ADP advertise (s_data) + AECP response (s_adp).
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) ctl_tx_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (adp_tx_tdata),  .s_data_tkeep (adp_tx_tkeep),
    .s_data_tvalid(adp_tx_tvalid), .s_data_tlast (adp_tx_tlast),
    .s_data_tready(adp_tx_tready),
    .s_adp_tdata (ctl2_tx_tdata),  .s_adp_tkeep (ctl2_tx_tkeep),
    .s_adp_tvalid(ctl2_tx_tvalid), .s_adp_tlast (ctl2_tx_tlast),
    .s_adp_tready(ctl2_tx_tready),
    .m_tdata (ctl_tx_tdata), .m_tkeep (ctl_tx_tkeep),
    .m_tvalid(ctl_tx_tvalid), .m_tlast (ctl_tx_tlast), .m_tready(ctl_tx_tready)
  );

  //! ...then merge the lwSRP MRPDUs (4th low-rate source, established pattern).
  wire [TDATA_WIDTH-1:0]   ctlf_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlf_tx_tkeep;
  wire                     ctlf_tx_tvalid, ctlf_tx_tlast, ctlf_tx_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) srp_ctl_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (ctl_tx_tdata),  .s_data_tkeep (ctl_tx_tkeep),
    .s_data_tvalid(ctl_tx_tvalid), .s_data_tlast (ctl_tx_tlast),
    .s_data_tready(ctl_tx_tready),
    .s_adp_tdata (lwsrp_tx_tdata),  .s_adp_tkeep (lwsrp_tx_tkeep),
    .s_adp_tvalid(lwsrp_tx_tvalid), .s_adp_tlast (lwsrp_tx_tlast),
    .s_adp_tready(lwsrp_tx_tready),
    .m_tdata (ctlf_tx_tdata), .m_tkeep (ctlf_tx_tkeep),
    .m_tvalid(ctlf_tx_tvalid), .m_tlast (ctlf_tx_tlast), .m_tready(ctlf_tx_tready)
  );

  //! ...and the ACMP listener's responses/probes (5th low-rate source).
  wire [TDATA_WIDTH-1:0]   ctlg_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlg_tx_tkeep;
  wire                     ctlg_tx_tvalid, ctlg_tx_tlast, ctlg_tx_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) lstn_ctl_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (ctlf_tx_tdata),  .s_data_tkeep (ctlf_tx_tkeep),
    .s_data_tvalid(ctlf_tx_tvalid), .s_data_tlast (ctlf_tx_tlast),
    .s_data_tready(ctlf_tx_tready),
    .s_adp_tdata (acmpl_tx_tdata),  .s_adp_tkeep (acmpl_tx_tkeep),
    .s_adp_tvalid(acmpl_tx_tvalid), .s_adp_tlast (acmpl_tx_tlast),
    .s_adp_tready(acmpl_tx_tready),
    .m_tdata (ctlg_tx_tdata), .m_tkeep (ctlg_tx_tkeep),
    .m_tvalid(ctlg_tx_tvalid), .m_tlast (ctlg_tx_tlast), .m_tready(ctlg_tx_tready)
  );

  wire [TDATA_WIDTH-1:0]   ctlh_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlh_tx_tkeep;
  wire                     ctlh_tx_tvalid, ctlh_tx_tlast, ctlh_tx_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) maap_ctl_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (ctlg_tx_tdata),  .s_data_tkeep (ctlg_tx_tkeep),
    .s_data_tvalid(ctlg_tx_tvalid), .s_data_tlast (ctlg_tx_tlast),
    .s_data_tready(ctlg_tx_tready),
    .s_adp_tdata (maap_tx_tdata),  .s_adp_tkeep (maap_tx_tkeep),
    .s_adp_tvalid(maap_tx_tvalid), .s_adp_tlast (maap_tx_tlast),
    .s_adp_tready(maap_tx_tready),
    .m_tdata (ctlh_tx_tdata), .m_tkeep (ctlh_tx_tkeep),
    .m_tvalid(ctlh_tx_tvalid), .m_tlast (ctlh_tx_tlast), .m_tready(ctlh_tx_tready)
  );

  //! Merge datapath (ptp_ts_top output) + low-rate control into the MAC TX.
  //! AAF injected AFTER the shaper (MVP: bypasses CBS for continuous emission,
  //! like ADP; class-A shaping = the is_1g follow-up). Merge shaped-data + AAF.
  wire [TDATA_WIDTH-1:0]   dpaaf_tdata;
  wire [TDATA_WIDTH/8-1:0] dpaaf_tkeep;
  wire                     dpaaf_tvalid, dpaaf_tlast, dpaaf_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) aaf_final_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (tx_axis_dp_to_arb.tdata),  .s_data_tkeep (tx_axis_dp_to_arb.tkeep),
    .s_data_tvalid(tx_axis_dp_to_arb.tvalid), .s_data_tlast (tx_axis_dp_to_arb.tlast),
    .s_data_tready(tx_axis_dp_to_arb.tready),
    .s_adp_tdata (aaf_tx_tdata),  .s_adp_tkeep (aaf_tx_tkeep),
    .s_adp_tvalid(aaf_tx_tvalid), .s_adp_tlast (aaf_tx_tlast),
    .s_adp_tready(aaf_tx_tready),
    .m_tdata (dpaaf_tdata), .m_tkeep (dpaaf_tkeep),
    .m_tvalid(dpaaf_tvalid), .m_tlast (dpaaf_tlast), .m_tready(dpaaf_tready)
  );

  //! ...and the CRF talker's PDUs (6th low-rate source, 500/s untagged).
  wire [TDATA_WIDTH-1:0]   ctli_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] ctli_tx_tkeep;
  wire                     ctli_tx_tvalid, ctli_tx_tlast, ctli_tx_tready;
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) crf_ctl_mux (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_data_tdata (ctlh_tx_tdata),  .s_data_tkeep (ctlh_tx_tkeep),
    .s_data_tvalid(ctlh_tx_tvalid), .s_data_tlast (ctlh_tx_tlast),
    .s_data_tready(ctlh_tx_tready),
    .s_adp_tdata (crft_tx_tdata),  .s_adp_tkeep (crft_tx_tkeep),
    .s_adp_tvalid(crft_tx_tvalid), .s_adp_tlast (crft_tx_tlast),
    .s_adp_tready(crft_tx_tready),
    .m_tdata (ctli_tx_tdata), .m_tkeep (ctli_tx_tkeep),
    .m_tvalid(ctli_tx_tvalid), .m_tlast (ctli_tx_tlast), .m_tready(ctli_tx_tready)
  );

  //! min-IFG gasket on the CONTROL lane ONLY (2026-07-19): the MilanMAC
  //! (cut-through core + milan_cd->sys CDC) silently eats a frame that
  //! enters back-to-back behind another (silicon: the MVRP half of the
  //! MSRP+MVRP pair, and the intermittent ACMP CONNECT_RX_RESPONSE that
  //! follows another control frame). Spacing every control frame here fixes
  //! ALL of them WITHOUT touching data/AAF throughput (the data lane
  //! bypasses this gasket). Replaces lwSRP's local gap workaround.
  wire [TDATA_WIDTH-1:0]   ctlg2_tdata;
  wire [TDATA_WIDTH/8-1:0] ctlg2_tkeep;
  wire                     ctlg2_tvalid, ctlg2_tlast, ctlg2_tready;
  tx_ifg_gasket #(.DATA_WIDTH(TDATA_WIDTH), .GAP_CYCLES(512)) ctl_ifg (
    .clk_i (axis_clk), .rst_n (axis_resetn),
    .s_tdata (ctli_tx_tdata),  .s_tkeep (ctli_tx_tkeep),
    .s_tvalid(ctli_tx_tvalid), .s_tlast (ctli_tx_tlast), .s_tready(ctli_tx_tready),
    .m_tdata (ctlg2_tdata),  .m_tkeep (ctlg2_tkeep),
    .m_tvalid(ctlg2_tvalid), .m_tlast (ctlg2_tlast), .m_tready(ctlg2_tready)
  );

  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) adp_tx_mux (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .s_data_tdata (dpaaf_tdata),
    .s_data_tkeep (dpaaf_tkeep),
    .s_data_tvalid(dpaaf_tvalid),
    .s_data_tlast (dpaaf_tlast),
    .s_data_tready(dpaaf_tready),
    .s_adp_tdata (ctlg2_tdata),
    .s_adp_tkeep (ctlg2_tkeep),
    .s_adp_tvalid(ctlg2_tvalid),
    .s_adp_tlast (ctlg2_tlast),
    .s_adp_tready(ctlg2_tready),
    .m_tdata (tx_axis_to_mac.tdata),
    .m_tkeep (tx_axis_to_mac.tkeep),
    .m_tvalid(tx_axis_to_mac.tvalid),
    .m_tlast (tx_axis_to_mac.tlast),
    .m_tready(tx_axis_to_mac.tready)
  );

  // ==========================================================================
  //  RMON event counters
  // ==========================================================================
  //! Good-frame lanes are derived HERE from the MAC AXIS boundary handshake
  //! (one accepted `tlast` beat = one frame), so they count on every
  //! integration - including the LiteX SoCs, whose glue has no MAC event
  //! pulses to offer (i_mac_events tied 0 there = the "RMON never worked on
  //! silicon" root cause). The remaining MAC-internal lanes pass through from
  //! i_mac_events; its good-frame bits are ignored to make double-counting
  //! structurally impossible.
  wire tx_mac_good_w = m_axis_mac_tx_tvalid & m_axis_mac_tx_tready
                     & m_axis_mac_tx_tlast;
  wire rx_mac_good_w = s_axis_mac_rx_tvalid & s_axis_mac_rx_tready
                     & s_axis_mac_rx_tlast;
  logic [_ETH_EVENT_COUNTER-1:0] mac_events_w;
  always_comb begin : mac_event_merge
    mac_events_w = i_mac_events;
    mac_events_w[TX_FIFO_GOOD_FRAME] = tx_mac_good_w;
    mac_events_w[RX_FIFO_GOOD_FRAME] = rx_mac_good_w;
  end : mac_event_merge

  ethernet_events ethernet_counters(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .stats_reset(cfg_stats_reset),
    .events(mac_events_w),
    .counts_o(stats_counts),
    .rollover_o(stats_rollover)
  );

endmodule

`default_nettype wire

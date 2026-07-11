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
  parameter int NUM_QUEUES  = NUMBER_OF_QUEUES
)(
  //! axis_clk domain (system clock, ~100 MHz) + active-low sync reset
  input  wire axis_clk,
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
  input  wire        i_full_duplex,
  //! RMON event pulses from the external MAC (lane index == ethernet_events_t enum)
  input  wire [_ETH_EVENT_COUNTER-1:0] i_mac_events,

  // ---- interrupt (milan_csr aggregate: tx_ts_ready | link_change | rmon_rollover) ----
  output wire        o_irq_csr
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
  assign tx_axis_to_shaper.tdata  = s_axis_tx_tdata;
  assign tx_axis_to_shaper.tkeep  = s_axis_tx_tkeep;
  assign tx_axis_to_shaper.tvalid = s_axis_tx_tvalid;
  assign tx_axis_to_shaper.tlast  = s_axis_tx_tlast;
  assign s_axis_tx_tready         = tx_axis_to_shaper.tready;
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
  wire [15:0] cfg_adp_current_config, cfg_adp_identify_index, cfg_adp_interface_index;
  wire        cfg_adp_advertise_p, cfg_adp_depart_p;
  wire [31:0] adp_available_index;
  wire [TDATA_WIDTH-1:0]   adp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] adp_tx_tkeep;
  wire                     adp_tx_tvalid, adp_tx_tlast, adp_tx_tready;

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
    .o_adp_gptp_domain    (cfg_adp_gptp_domain),
    .o_adp_current_config (cfg_adp_current_config),
    .o_adp_identify_index (cfg_adp_identify_index),
    .o_adp_interface_index(cfg_adp_interface_index),
    .o_adp_association_id (cfg_adp_association_id),
    .o_adp_advertise_p    (cfg_adp_advertise_p),
    .o_adp_depart_p       (cfg_adp_depart_p),
    .i_adp_available_index(adp_available_index),
    // RX dest-MAC TCAM filter programming (0x700 group)
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
    .cbs_idle_slope_i  (cfg_cbs_idle_slope),
    .cbs_hi_credit_i   (cfg_cbs_hi_credit),
    .cbs_lo_credit_i   (cfg_cbs_lo_credit),
    .cbs_shaped_i      (cfg_cbs_enable),
    .s_axis(tx_axis_to_shaper),
    .m_axis(tx_axis_shaper_to_ts)
  );

  // ==========================================================================
  //  PTP hardware clock + TX/RX timestamping (CSR-configured)
  // ==========================================================================
  ptp_ts_top #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(0),
    .ETH_TYPE(16'hF788)
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
  //! 1-second tick for the ADP re-advertise timer (axis_clk = 100 MHz).
  localparam int ADP_TICK_DIV = 100_000_000;
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

  adp_advertiser adp_adv (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .tick_i   (adp_tick_1s),
    .link_up_i     (adp_link_up_p),
    .link_down_i   (adp_link_down_p),
    .shutdown_i    (cfg_adp_depart_p),
    .gm_change_i   (1'b0),
    .info_changed_i(cfg_adp_advertise_p),
    .rcv_discover_i(1'b0),
    .station_mac_i (cfg_mac_addr),
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
    .frame_sent_o ()
  );

  //! Merge datapath (ptp_ts_top output) + ADP into the single MAC TX stream.
  adp_tx_arbiter #(.DATA_WIDTH(TDATA_WIDTH)) adp_tx_mux (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .s_data_tdata (tx_axis_dp_to_arb.tdata),
    .s_data_tkeep (tx_axis_dp_to_arb.tkeep),
    .s_data_tvalid(tx_axis_dp_to_arb.tvalid),
    .s_data_tlast (tx_axis_dp_to_arb.tlast),
    .s_data_tready(tx_axis_dp_to_arb.tready),
    .s_adp_tdata (adp_tx_tdata),
    .s_adp_tkeep (adp_tx_tkeep),
    .s_adp_tvalid(adp_tx_tvalid),
    .s_adp_tlast (adp_tx_tlast),
    .s_adp_tready(adp_tx_tready),
    .m_tdata (tx_axis_to_mac.tdata),
    .m_tkeep (tx_axis_to_mac.tkeep),
    .m_tvalid(tx_axis_to_mac.tvalid),
    .m_tlast (tx_axis_to_mac.tlast),
    .m_tready(tx_axis_to_mac.tready)
  );

  // ==========================================================================
  //  RMON event counters (fed by the external MAC's event pulses)
  // ==========================================================================
  ethernet_events ethernet_counters(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .stats_reset(cfg_stats_reset),
    .events(i_mac_events),
    .counts_o(stats_counts),
    .rollover_o(stats_rollover)
  );

endmodule

`default_nettype wire

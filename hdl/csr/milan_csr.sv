/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : milan_csr.sv
  Author      : Kebag Logic

  Date        : 2026-07-01
  Description : AXI4-Lite control/status-register (CSR) block for the Milan TSN
                network interface. This is the memory-mapped control plane
                (REQUIREMENTS.md REQ-CSR-*) that the Linux driver binds to; it
                turns the previously compile-time-only TSN knobs (MAC config,
                802.1Q classifier map, 802.1Qav CBS slopes, PTP clock control)
                into runtime-writable registers, and exposes MAC statistics,
                link status and interrupts back to software.

                The full register map / ABI is documented in
                docs/reference/REGISTER_MAP.md and mirrored by the self-checking harness
                in tb/verilator/csr. Register groups:

                  0x000  ID / VERSION / CAPABILITIES / IRQ
                  0x100  MAC control + status
                  0x200  Statistics (RMON) snapshot window
                  0x300  802.1Q classifier (PCP->TC map, default priority)
                  0x400  802.1Qav CBS, per queue (stride 0x20)
                  0x500  PTP hardware clock (adjfine/adjtime/settime/gettime)

                Design notes:
                  * AXI4-Lite slave uses the combinational-ready, single-
                    outstanding pattern: a transfer commits on the same rising
                    edge that *READY is asserted, so a master that drops *VALID
                    right after the handshake still commits (no lost writes).
                  * Configuration values leave on flat o_* output ports for the
                    rest of milan_top to consume. Status (link, RMON counters,
                    PTP TOD) and event pulses arrive on i_* input ports.
                  * Command strobes (PTP settime/adjtime/snapshot, stats
                    snapshot/reset) are emitted as single-cycle o_*_cmd_* /
                    o_stats_* pulses. Fields consumed in the gtx_clk (PTP/TX)
                    domain must be CDC-synchronised at the consumer using these
                    apply strobes (REQ-CSR-03); this block is purely in the
                    aclk (AXI) domain.
                  * s_axi_wstrb is intentionally ignored: the ABI mandates full
                    32-bit register writes.

  Company     : Kebag Logic
  Project     : Milan FPGA Platform
------------------------------------------------------------------------------
*/

`default_nettype none

module milan_csr #(
  parameter int NUM_QUEUES  = 4,             //! Number of HW traffic-class queues (reported in CAP.num_queues)
  parameter int ADDR_WIDTH  = 16,            //! Byte-address width of the AXI-Lite window (16 => 64 KB)
  parameter logic [31:0] VERSION = 32'h0001_0004 //! Value returned by the read-only VERSION register ([31:16] major, [15:0] minor); 0x0004 = pre-filter AVTP taps (TCAM kernel-shield safe to arm)
)(
  input  wire                    aclk,           //! AXI-Lite clock (aclk / axis_clk domain)
  input  wire                    aresetn,        //! AXI-Lite active-low synchronous reset

  // ---- AXI4-Lite slave ----
  input  wire [ADDR_WIDTH-1:0]   s_axi_awaddr,   //! Write address (byte offset into the register window)
  input  wire                    s_axi_awvalid,  //! Write address valid
  output wire                    s_axi_awready,  //! Write address ready (combinational)
  input  wire [31:0]             s_axi_wdata,    //! Write data
  input  wire [3:0]              s_axi_wstrb,    //! Write byte strobes (ignored; full 32-bit writes only)
  input  wire                    s_axi_wvalid,   //! Write data valid
  output wire                    s_axi_wready,   //! Write data ready (combinational)
  output wire [1:0]              s_axi_bresp,    //! Write response (always OKAY)
  output wire                    s_axi_bvalid,   //! Write response valid
  input  wire                    s_axi_bready,   //! Write response ready
  input  wire [ADDR_WIDTH-1:0]   s_axi_araddr,   //! Read address (byte offset into the register window)
  input  wire                    s_axi_arvalid,  //! Read address valid
  output wire                    s_axi_arready,  //! Read address ready (combinational)
  output wire [31:0]             s_axi_rdata,    //! Read data
  output wire [1:0]              s_axi_rresp,    //! Read response (always OKAY)
  output wire                    s_axi_rvalid,   //! Read data valid
  input  wire                    s_axi_rready,   //! Read data ready

  // ---- MAC control / status (REQ-MAC-01..03) ----
  output wire                    o_mac_tx_en,    //! MAC transmit enable (MAC_CTRL[0])
  output wire                    o_mac_rx_en,    //! MAC receive enable (MAC_CTRL[1])
  output wire                    o_mac_promisc,  //! Promiscuous mode: accept all frames (MAC_CTRL[2])
  output wire                    o_mac_allmulti, //! Accept all multicast (MAC_CTRL[3])
  output wire                    o_mac_is_1g,    //! Link-rate select: 1 = 1 Gb/s, 0 = 100 Mb/s (MAC_CTRL[4])
  output wire [7:0]              o_mac_ifg,      //! Inter-frame gap, bytes (MAC_IFG)
  output wire [47:0]             o_mac_addr,     //! Station MAC address {MAC_ADDR_HI[15:0], MAC_ADDR_LO}
  output wire [63:0]             o_mc_hash,      //! Multicast hash filter {MC_HASH_HI, MC_HASH_LO}
  output wire                    o_phy_reset_n,  //! PHY reset, active-low (PHY_RESET[0])
  input  wire                    i_link_up,      //! Link status from PHY/MAC (MAC_STATUS[0])
  input  wire [1:0]              i_speed,        //! Negotiated speed 0=10,1=100,2=1000 (MAC_STATUS[2:1])
  input  wire                    i_full_duplex,  //! Full-duplex indication (MAC_STATUS[3])

  // ---- Statistics / RMON (REQ-MAC-04) ----
  output wire                    o_stats_snapshot, //! 1-cycle pulse: latch live counters into the read window
  output wire                    o_stats_reset,    //! 1-cycle pulse: clear the external event counters
  input  wire [32*9-1:0]         i_stats,          //! Live RMON counters, packed {STAT8,...,STAT0}, 9x32b

  // ---- 802.1Q classifier (REQ-CLS-01..04) ----
  output wire                    o_cls_use_pcp,      //! 1 = classify by PCP table, 0 = legacy EtherType (CLS_CTRL[0])
  output wire                    o_cls_dmac_check,   //! Enable reserved-DMAC validation (CLS_CTRL[1])
  output wire [2:0]              o_cls_default_pcp,  //! Default port priority for untagged frames (CLS_DEFAULT_PCP)
  output wire [23:0]             o_cls_pcp_tc_map,   //! Priority->traffic-class table, 8x3 bits (CLS_PCP_TC_MAP)
  output wire [23:0]             o_cls_prio_regen,   //! Priority regeneration table, 8x3 bits (CLS_PRIO_REGEN)
  output wire [31:0]             o_cls_tc_queue_map, //! Traffic-class->queue map (CLS_TC_QUEUE_MAP)

  // ---- 802.1Qav CBS, per queue, packed [q*32 +: 32] (REQ-CBS-01..03) ----
  output wire [32*NUM_QUEUES-1:0] o_cbs_idle_slope, //! Per-queue idleSlope, bits/s (CBS_IDLE_SLOPE)
  output wire [32*NUM_QUEUES-1:0] o_cbs_hi_credit,  //! Per-queue hiCredit, signed bytes (CBS_HI_CREDIT)
  output wire [32*NUM_QUEUES-1:0] o_cbs_lo_credit,  //! Per-queue loCredit, signed bytes (CBS_LO_CREDIT)
  output wire [NUM_QUEUES-1:0]    o_cbs_enable,     //! Per-queue shaped-enable; 0 = strict priority (CBS_CTRL[0])

  // ---- PTP hardware clock (REQ-PTP-01..04,06) ----
  output wire                    o_ptp_enable,      //! PTP counter enable (PTP_CTRL[0])
  output wire [31:0]             o_ptp_incr,        //! Nominal per-tick increment, ns.frac (PTP_INCR)
  output wire [31:0]             o_ptp_adj,         //! Signed adjfine addend added each tick (PTP_ADJ)
  output wire [63:0]             o_ptp_tod_wr,      //! settime target TOD {PTP_TOD_WR_HI, PTP_TOD_WR_LO}
  output wire [63:0]             o_ptp_offset,      //! adjtime signed delta {PTP_OFFSET_HI, PTP_OFFSET_LO}
  output wire                    o_ptp_cmd_load,    //! settime apply strobe (1-cycle pulse, PTP_CMD[0])
  output wire                    o_ptp_cmd_adjust,  //! adjtime apply strobe (1-cycle pulse, PTP_CMD[1])
  output wire                    o_ptp_cmd_snapshot,//! gettime latch strobe (1-cycle pulse, PTP_CMD[2])
  output wire [31:0]             o_ptp_ingress_lat, //! Ingress latency correction, ns (PTP_INGRESS_LAT)
  output wire [31:0]             o_ptp_egress_lat,  //! Egress latency correction, ns (PTP_EGRESS_LAT)
  input  wire [63:0]             i_ptp_tod,         //! gettime snapshot value from the PHC (gtx_clk, synchronised)
  input  wire                    i_ptp_tod_valid,   //! 1-cycle pulse: latch i_ptp_tod into PTP_TOD_RD (REQ-PTP-03/CSR-03)

  // ---- ADP advertiser identity/control (IEEE 1722.1 / Milan v1.2, FR-DISC-*) ----
  output wire                    o_adp_enable,        //! ADP advertising enable (ADP_CTRL[0])
  output wire [4:0]              o_adp_valid_time,    //! ADP valid_time, units of 2 s (ADP_CTRL[12:8])
  output wire [63:0]             o_adp_entity_id,     //! Entity ID (EUI-64) {ADP_EID_HI, ADP_EID_LO}
  output wire [63:0]             o_adp_entity_model_id, //! Entity model ID (EUI-64) {ADP_MID_HI, ADP_MID_LO}
  output wire [31:0]             o_adp_entity_caps,   //! entity_capabilities (ADP_ECAPS)
  output wire [15:0]             o_adp_talker_sources,//! talker_stream_sources (ADP_TALK[15:0])
  output wire [15:0]             o_adp_talker_caps,   //! talker_capabilities (ADP_TALK[31:16])
  output wire [15:0]             o_adp_listener_sinks,//! listener_stream_sinks (ADP_LIST[15:0])
  output wire [15:0]             o_adp_listener_caps, //! listener_capabilities (ADP_LIST[31:16])
  output wire [31:0]             o_adp_controller_caps, //! controller_capabilities (ADP_CCAPS)
  output wire [63:0]             o_adp_gptp_gm,       //! gptp_grandmaster_id {ADP_GM_HI, ADP_GM_LO}
  output wire [31:0]             o_gptp_pdelay_ns,    //! measured propagation delay ns (GPTP_PDELAY)
  input  wire [31:0]             i_acmpl_dbg,         //! listener walker forensics (RO 0x6E8)
  input  wire [31:0]             i_avtprx_tsd,        //! last accepted ts_delta (RO 0x6EC)
  input  wire [31:0]             i_i2spb_dbg,         //! DAC serial forensics (RO 0x6F0)
  output wire [7:0]              o_adp_gptp_domain,   //! gptp_domain_number (ADP_DOMAIN[7:0])
  output wire [15:0]             o_adp_current_config,//! current_configuration_index (ADP_IDX0[15:0])
  output wire [15:0]             o_adp_identify_index,//! identify_control_index (ADP_IDX0[31:16])
  output wire [15:0]             o_adp_interface_index, //! interface_index (ADP_IDX1[15:0])
  output wire [63:0]             o_adp_association_id,//! association_id {ADP_ASSOC_HI, ADP_ASSOC_LO}
  output wire                    o_adp_advertise_p,   //! 1-cycle: advertise now + bump available_index (ADP_CMD[0])
  output wire                    o_adp_depart_p,      //! 1-cycle: send ENTITY_DEPARTING (ADP_CMD[1])
  input  wire [7:0]              i_adp_depart_cnt,    //! DIAG: depart events taken (A_ADP_DIAG[7:0])
  input  wire [7:0]              i_adp_rearm_cnt,     //! DIAG: dormancy self-re-arms (A_ADP_DIAG[15:8])
  input  wire [1:0]              i_adp_depart_src,    //! DIAG: last depart cause {shutdown, link_down} (A_ADP_DIAG[17:16])
  input  wire [31:0]             i_adp_available_index, //! current available_index from the advertiser (ADP_STATUS)
  //! AECP/AEM listener status (KL_aecp_top) — read-only, 0x648/0x64C
  input  wire                    i_aecp_locked,         //! entity is LOCK_ENTITY-locked
  input  wire [15:0]             i_aecp_current_config, //! live current_configuration_index
  input  wire [15:0]             i_aecp_cmd_count,      //! AECP commands accepted
  input  wire [15:0]             i_aecp_resp_count,     //! AECP responses sent
  input  wire [15:0]             i_acmp_cmd_count,      //! ACMP commands accepted (0x650)
  input  wire [15:0]             i_acmp_resp_count,     //! ACMP responses sent (0x650)
  output wire                    o_aaf_enable,          //! AAF talker enable (AAF_CTRL[0])
  output wire                    o_aaf_bypass,          //! AAF gate bypass (AAF_CTRL[1]) — 1 = stream whenever enabled (legacy); 0 = Milan probe-gated
  output wire [47:0]             o_aaf_dest_mac,        //! AAF stream DMAC {DMHI[15:0],DMLO}
  output wire [11:0]             o_aaf_vid,             //! AAF SR VID (AAF_CTRL[27:16])
  output wire                    o_acmp_lobs,           //! listener_observed override (A_ACMP_LOBS[0], the lwSRP socket)
  input  wire                    i_acmp_probe_armed,    //! ACMP probe SM state (A_ACMP_TALKER RO)
  input  wire                    i_acmp_talker_active,
  input  wire                    i_aaf_gate,            //! resolved AAF gate
  input  wire [31:0]             i_aaf_frames,          //! AAF frames sent (RO, 0x660)
  input  wire [31:0]             i_aaf_pairs,           //! AAF I2S pairs captured (RO, 0x664)

  // ---- lwSRP engine (0x680 group, docs/LWSRP_FPGA_ARCHITECTURE.md) ----
  output wire                    o_lwsrp_enable,        //! LWSRP_CTRL[0] engine enable
  output wire                    o_lwsrp_talker_en,     //! LWSRP_CTRL[1] TalkerAdvertise declare
  output wire [1:0]              o_lwsrp_qidx,          //! LWSRP_CTRL[3:2] class-A queue (slope MUX target)
  output wire [11:0]             o_lwsrp_vid,           //! LWSRP_VID[11:0] SR VID
  output wire [47:0]             o_lwsrp_dest_mac,      //! stream DMAC {DMHI[15:0], DMLO}
  output wire [15:0]             o_lwsrp_max_frame,     //! LWSRP_TSPEC[15:0] MaxFrameSize
  output wire [15:0]             o_lwsrp_interval,      //! LWSRP_TSPEC[31:16] MaxIntervalFrames
  output wire [31:0]             o_lwsrp_latency,       //! LWSRP_LATENCY AccumulatedLatency (ns)
  input  wire [31:0]             i_lwsrp_status,        //! packed engine status (RO 0x694)
  input  wire [31:0]             i_lwsrp_slope,         //! granted idleSlope bps (RO 0x698)
  input  wire [31:0]             i_lwsrp_cnt,           //! {rx_pdus[31:16], tx_pdus[15:0]} (RO 0x69C)

  // ---- ACMP listener SM (0x6A4 group, Milan v1.2 §5.5 listener) ----
  input  wire [31:0]             i_acmpl_state,         //! packed SM status (RO 0x6A4)
  input  wire [31:0]             i_acmpl_talker_lo,     //! bound talker EID (RO 0x6A8)
  input  wire [31:0]             i_acmpl_talker_hi,     //! (RO 0x6AC)
  input  wire [31:0]             i_acmpl_cnt,           //! {probes[31:16], cmds[15:0]} (RO 0x6B0)
  input  wire [31:0]             i_acmpl_tuid,          //! {fail_code[23:16], tuid[15:0]} (RO 0x6B4)
  input  wire [31:0]             i_avtprx_stat,         //! AVTP RX monitor status (RO 0x6B8)
  input  wire [31:0]             i_avtprx_frx,          //! STREAM_INPUT FRAMES_RX (RO 0x6BC)
  input  wire [31:0]             i_avtprx_err,          //! packed error counters (RO 0x6C0)
  input  wire [31:0]             i_pcmrx_cnt,           //! {drops[31:16], pdus[15:0]} (RO 0x6C4)
  input  wire [31:0]             i_pcmrx_ts,            //! last accepted avtp_ts (RO 0x6C8)
  input  wire [31:0]             i_i2spb_stat,          //! {underruns, overruns} (RO 0x6D8)
  input  wire [31:0]             i_i2spb_trim,          //! {servo trim, fifo fill} (RO 0x6E0)
  input  wire [31:0]             i_maap_stat0,          //! {conflicts, defends, offset} (RO 0x6D0)
  input  wire [31:0]             i_maap_stat1,          //! {addr_valid, state} (RO 0x6D4)
  output wire                    o_maap_enable,         //! MAAP engine enable
  output wire                    o_maap_seed_valid,     //! first probe uses seed
  output wire [7:0]              o_maap_count,          //! block size (reset 8)
  output wire [15:0]             o_maap_seed_offset,    //! provisioning seed
  output wire                    o_tone_enable,
  output wire [2:0]              o_tone_att,          //! pilot-tone -6dB steps (TONE_CTRL[3:1])         //! 1 kHz 0 dBFS pilot tone

  // ---- RX dest-MAC TCAM filter programming (REQ-MAC-02) ----
  output wire                    o_sw_link,           //! LINK_CTRL[0]: daemon-tracked PHY link
  output wire                    o_mac_reinit,        //! LINK_CTRL[1]: MAC sys-side reset (recovery daemon)
  output wire                    o_tcam_default_pass, //! accept frames that miss the TCAM (TCAM_CTRL[0])
  output wire                    o_tcam_wr_en,        //! 1-cycle: commit an entry write to the TCAM
  output wire [4:0]              o_tcam_wr_index,     //! entry index (TCAM_CMD[4:0])
  output wire                    o_tcam_wr_valid,     //! 1 = add/update, 0 = remove (TCAM_CMD[8])
  output wire [47:0]             o_tcam_wr_key,       //! match key {TCAM_KEY_HI[15:0], TCAM_KEY_LO}
  output wire [47:0]             o_tcam_wr_mask,      //! care mask {TCAM_MASK_HI[15:0], TCAM_MASK_LO}
  output wire [7:0]              o_tcam_wr_action,    //! action/tag (TCAM_ACTION[7:0])

  // ---- Interrupt (REQ-CSR-04) ----
  input  wire                    i_evt_tx_ts_ready,   //! Event: TX egress timestamp available (sets IRQ_STATUS[0])
  input  wire                    i_evt_link_change,   //! Event: link/speed change (sets IRQ_STATUS[1])
  input  wire                    i_evt_rmon_rollover, //! Event: RMON counter rollover (sets IRQ_STATUS[2])
  output wire                    o_irq                //! Level interrupt to PS = |(IRQ_STATUS & IRQ_MASK)
);

  // ==========================================================================
  //  Local parameters
  // ==========================================================================
  localparam int NS = 9;                         //! Number of RMON statistics counters
  localparam int QW = (NUM_QUEUES <= 1) ? 1 : $clog2(NUM_QUEUES); //! Queue-index width

  // --------------------------------------------------------------------------
  //  Register byte offsets (single HDL source of the map; see docs/reference/REGISTER_MAP.md)
  //
  //    0x000 ID          0x100 MAC_CTRL     0x300 CLS_CTRL     0x500 PTP_CTRL
  //    0x004 VERSION     0x104 MAC_IFG      0x304 CLS_DEF_PCP  0x504 PTP_INCR
  //    0x008 CAP         0x108 MAC_ADDR_LO  0x308 CLS_PCP_TC   0x508 PTP_ADJ
  //    0x00C SCRATCH     0x10C MAC_ADDR_HI  0x30C CLS_REGEN    0x510 PTP_TOD_WR_LO
  //    0x010 IRQ_STATUS  0x110 MAC_STATUS   0x310 CLS_TC_QUEUE 0x514 PTP_TOD_WR_HI
  //    0x014 IRQ_MASK    0x114 MC_HASH_LO                      0x518 PTP_OFFSET_LO
  //    0x018 IRQ_RAW     0x118 MC_HASH_HI   0x400+q*0x20 CBS:  0x51C PTP_OFFSET_HI
  //                      0x11C PHY_RESET      +0x00 IDLE_SLOPE 0x520 PTP_CMD
  //    0x200 STATS_CTRL                       +0x04 HI_CREDIT  0x530 PTP_TOD_RD_LO
  //    0x210..0x230 STAT0..STAT8              +0x08 LO_CREDIT  0x534 PTP_TOD_RD_HI
  //                                           +0x0C CTRL       0x540 PTP_INGRESS_LAT
  //                                                            0x544 PTP_EGRESS_LAT
  // --------------------------------------------------------------------------
  localparam [ADDR_WIDTH-1:0]
    A_ID          = 'h000, A_VERSION = 'h004, A_CAP     = 'h008, A_SCRATCH  = 'h00C,
    A_IRQ_STATUS  = 'h010, A_IRQ_MASK= 'h014, A_IRQ_RAW = 'h018,
    A_MAC_CTRL    = 'h100, A_MAC_IFG = 'h104, A_MAC_ALO = 'h108, A_MAC_AHI  = 'h10C,
    A_MAC_STATUS  = 'h110, A_MC_LO   = 'h114, A_MC_HI   = 'h118, A_PHY_RST  = 'h11C,
    A_STATS_CTRL  = 'h200,
    A_CLS_CTRL    = 'h300, A_CLS_DPCP= 'h304, A_CLS_MAP = 'h308, A_CLS_REGEN= 'h30C,
    A_CLS_TCQ     = 'h310,
    A_PTP_CTRL    = 'h500, A_PTP_INCR= 'h504, A_PTP_ADJ = 'h508,
    A_PTP_TWLO    = 'h510, A_PTP_TWHI= 'h514, A_PTP_OFLO= 'h518, A_PTP_OFHI = 'h51C,
    A_PTP_CMD     = 'h520, A_PTP_TRLO= 'h530, A_PTP_TRHI= 'h534,
    A_PTP_ILAT    = 'h540, A_PTP_ELAT= 'h544,
    // ---- 0x600 ADP advertiser (IEEE 1722.1 / Milan v1.2) ----
    A_ADP_CTRL    = 'h600, A_ADP_EIDLO= 'h604, A_ADP_EIDHI= 'h608, A_ADP_MIDLO = 'h60C,
    A_ADP_MIDHI   = 'h610, A_ADP_ECAPS= 'h614, A_ADP_TALK = 'h618, A_ADP_LIST  = 'h61C,
    A_ADP_CCAPS   = 'h620, A_ADP_GMLO = 'h624, A_ADP_GMHI = 'h628, A_ADP_DOMAIN= 'h62C,
    A_ADP_IDX0    = 'h630, A_ADP_IDX1 = 'h634, A_ADP_ASLO = 'h638, A_ADP_ASHI  = 'h63C,
    A_ADP_CMD     = 'h640, A_ADP_STATUS='h644,
    A_AECP_STAT0  = 'h648, A_AECP_STAT1='h64C,   //! AECP listener status (RO)
    A_ACMP_STAT   = 'h650,                        //! ACMP responder status (RO)
    A_AAF_CTRL    = 'h654, A_AAF_DMLO = 'h658, A_AAF_DMHI = 'h65C, //! AAF talker
    A_AAF_FRAMES  = 'h660, A_AAF_PAIRS = 'h664,   //! AAF talker status (RO)
    A_ADP_DIAG    = 'h668,                        //! ADP dormancy diagnostics (RO)
    A_ACMP_TALKER = 'h66C,                        //! Milan talker SM state (RO)
    A_ACMP_LOBS   = 'h670,                        //! listener_observed override (RW, lwSRP socket)
    // ---- 0x680 lwSRP engine (re-homed from the stale 0x660 sketch) ----
    A_LWSRP_CTRL  = 'h680, A_LWSRP_VID = 'h684, A_LWSRP_DMLO = 'h688,
    A_LWSRP_DMHI  = 'h68C, A_LWSRP_TSPEC = 'h690,
    A_LWSRP_STATUS= 'h694, A_LWSRP_SLOPE = 'h698, A_LWSRP_CNT = 'h69C,
    A_LWSRP_LAT   = 'h6A0,
    // ---- 0x6A4 ACMP listener SM (RO) ----
    A_ACMPL_STATE = 'h6A4, A_ACMPL_TKLO = 'h6A8, A_ACMPL_TKHI = 'h6AC,
    A_ACMPL_CNT   = 'h6B0, A_ACMPL_TUID = 'h6B4,
    A_AVTPRX_STAT = 'h6B8, A_AVTPRX_FRX = 'h6BC, A_AVTPRX_ERR = 'h6C0,
    A_PCMRX_CNT   = 'h6C4, A_PCMRX_TS   = 'h6C8,
    A_MAAP_CTRL   = 'h6CC, A_MAAP_STAT0 = 'h6D0, A_MAAP_STAT1 = 'h6D4,
    A_I2SPB_STAT  = 'h6D8, A_TONE_CTRL = 'h6DC, A_I2SPB_TRIM = 'h6E0,
    A_GPTP_PDELAY = 'h6E4,   //! RW: measured gPTP neighbor propagation delay (ns), written by the softcore gptp daemon
    A_ACMPL_DBG   = 'h6E8,   //! RO live: listener walker forensics {classify_cnt, fc_cnt, fc_flags, base_hits}
    A_AVTPRX_TSD  = 'h6EC,   //! RO live: signed ts_delta at last accepted PDU (stream-sync error signal)
    A_I2SPB_DBG   = 'h6F0,   //! RO live: exact 32 serial bits of the last LEFT half-frame at the DAC pin
    // ---- 0x700 RX dest-MAC TCAM filter ----
    A_TCAM_CTRL   = 'h700, A_TCAM_KLO = 'h704, A_TCAM_KHI = 'h708, A_TCAM_MLO  = 'h70C,
    A_TCAM_MHI    = 'h710, A_TCAM_ACT = 'h714, A_TCAM_CMD = 'h718;
  localparam [ADDR_WIDTH-1:0] A_LINK_CTRL = 'h71C;   //! [0] sw_link (daemon), [1] mac_reinit (hold MAC sys-side in reset)
  localparam [ADDR_WIDTH-1:0] A_RST_EPOCH = 'h720;   //! RO live: datapath reset-release count (shadow-lie canary)
  localparam [ADDR_WIDTH-1:0] A_STATS_BASE = 'h210;                        //! STAT0 base; STAT0..8 at stride 4
  localparam [ADDR_WIDTH-1:0] A_CBS_BASE   = 'h400;                        //! CBS queue 0 base; stride 0x20
  localparam [ADDR_WIDTH-1:0] A_STATS_END  = A_STATS_BASE + ADDR_WIDTH'(NS*4);          //! One past last STAT
  localparam [ADDR_WIDTH-1:0] A_CBS_END    = A_CBS_BASE   + ADDR_WIDTH'(NUM_QUEUES*32); //! One past last CBS reg

  // ==========================================================================
  //  AXI4-Lite slave handshake (combinational-ready, single outstanding).
  //
  //  Area-70 config-in-RAM (USER directive 2026-07-15): reads of plain-RW
  //  configuration registers are served from a write-through SHADOW BRAM
  //  instead of the old ~90-entry combinational mux; only live/W1C/status
  //  registers keep a (much smaller) mux. Because BRAM cannot reset, a
  //  DEFAULTS ROM (config-time init) is swept into the shadow after every
  //  reset (513 cycles; AXI *READY is held low meanwhile), so soft-reset
  //  readback semantics are IDENTICAL to the register file. Reads take one
  //  extra cycle (BRAM latency) — AXI4-Lite handshake absorbs it.
  // ==========================================================================
  logic         b_valid;                 //! Write-response valid, held until BREADY
  logic         r_valid;                 //! Read-data valid, held until RREADY
  logic         rd_pend;                 //! BRAM read latency stage
  logic [31:0]  r_data;                  //! Registered read data
  logic [ADDR_WIDTH-1:0] rd_addr_q;      //! Latched read address (decode stage)
  logic         sweep_busy;              //! defaults -> shadow copy after reset
  logic [9:0]   sweep_cnt;

  wire wr_fire = s_axi_awvalid && s_axi_wvalid && !b_valid && !sweep_busy;
  wire rd_fire = s_axi_arvalid && !r_valid && !rd_pend && !sweep_busy;
  wire [ADDR_WIDTH-1:0] wr_addr = s_axi_awaddr;             //! Decoded write address
  wire [ADDR_WIDTH-1:0] rd_addr = s_axi_araddr;             //! Decoded read address

  assign s_axi_awready = wr_fire;
  assign s_axi_wready  = wr_fire;
  assign s_axi_arready = rd_fire;
  assign s_axi_bvalid  = b_valid;
  assign s_axi_bresp   = 2'b00;
  assign s_axi_rvalid  = r_valid;
  assign s_axi_rdata   = r_data;
  assign s_axi_rresp   = 2'b00;

  //! AXI response-channel valids: raise on a transfer, clear when accepted
  always_ff @(posedge aclk) begin : axi_resp_fsm
    if (!aresetn) begin
      b_valid <= 1'b0; r_valid <= 1'b0; rd_pend <= 1'b0; rd_addr_q <= '0;
    end else begin
      if (wr_fire)           b_valid <= 1'b1;
      else if (s_axi_bready) b_valid <= 1'b0;
      rd_pend <= rd_fire;
      if (rd_fire)           rd_addr_q <= rd_addr;
      if (rd_pend)           r_valid <= 1'b1;
      else if (s_axi_rready) r_valid <= 1'b0;
    end
  end

  // ==========================================================================
  //  Register storage
  // ==========================================================================
  logic [31:0] scratch;                  //! SCRATCH: R/W bus-liveness test register
  logic [31:0] irq_mask;                 //! IRQ_MASK: 1 = interrupt source enabled
  logic [31:0] irq_status;               //! IRQ_STATUS: W1C latched event bits
  logic [31:0] mac_ctrl;                 //! MAC_CTRL: tx/rx enable, promisc, allmulti, is_1g
  logic [31:0] mac_ifg;                  //! MAC_IFG: inter-frame gap (bytes)
  logic [31:0] mac_alo;                  //! MAC_ADDR_LO: station MAC [31:0]
  logic [31:0] mac_ahi;                  //! MAC_ADDR_HI: station MAC [47:32]
  logic [31:0] mc_lo;                    //! MC_HASH_LO: multicast hash [31:0]
  logic [31:0] mc_hi;                    //! MC_HASH_HI: multicast hash [63:32]
  logic [31:0] phy_rst;                  //! PHY_RESET: PHY reset (active-low bit 0)
  logic [31:0] cls_ctrl;                 //! CLS_CTRL: classifier mode bits
  logic [31:0] cls_dpcp;                 //! CLS_DEFAULT_PCP: default port priority
  logic [31:0] cls_map;                  //! CLS_PCP_TC_MAP: PCP->TC table
  logic [31:0] cls_regen;                //! CLS_PRIO_REGEN: priority regeneration table
  logic [31:0] cls_tcq;                  //! CLS_TC_QUEUE_MAP: TC->queue map
  logic [31:0] ptp_ctrl;                 //! PTP_CTRL: PTP clock enable
  logic [31:0] ptp_incr;                 //! PTP_INCR: nominal per-tick increment
  logic [31:0] ptp_adj;                  //! PTP_ADJ: signed adjfine addend
  logic [31:0] ptp_twlo;                 //! PTP_TOD_WR_LO: settime target low
  logic [31:0] ptp_twhi;                 //! PTP_TOD_WR_HI: settime target high
  logic [31:0] ptp_oflo;                 //! PTP_OFFSET_LO: adjtime delta low
  logic [31:0] ptp_ofhi;                 //! PTP_OFFSET_HI: adjtime delta high
  logic [31:0] ptp_ilat;                 //! PTP_INGRESS_LAT: ingress latency correction
  logic [31:0] ptp_elat;                 //! PTP_EGRESS_LAT: egress latency correction
  logic [63:0] ptp_tod_rd;               //! PTP_TOD_RD: TOD latched on snapshot (gettime)
  logic [31:0] stat_snap [0:NS-1];       //! Coherent snapshot of the RMON counters

  logic [31:0] cbs_idle [0:NUM_QUEUES-1];//! Per-queue CBS idleSlope (bits/s)
  logic [31:0] cbs_hi   [0:NUM_QUEUES-1];//! Per-queue CBS hiCredit (signed bytes)
  logic [31:0] cbs_lo   [0:NUM_QUEUES-1];//! Per-queue CBS loCredit (signed bytes)
  logic [NUM_QUEUES-1:0] cbs_en;         //! Per-queue CBS shaped-enable

  logic stats_snap_p;                    //! Stats snapshot command strobe (1 cycle)
  logic stats_rst_p;                     //! Stats reset command strobe (1 cycle)
  logic ptp_load_p;                      //! PTP settime apply strobe (1 cycle)
  logic ptp_adj_p;                       //! PTP adjtime apply strobe (1 cycle)
  logic ptp_snap_p;                      //! PTP gettime snapshot strobe (1 cycle)

  // ADP advertiser identity/control registers (0x600 group)
  logic [31:0] adp_ctrl;                 //! ADP_CTRL: [0]=enable, [12:8]=valid_time
  logic [31:0] aaf_ctrl, aaf_dmlo, aaf_dmhi; //! AAF talker: ctrl {vid[27:16], bypass[1], en[0]}, DMAC
  logic [31:0] acmp_lobs;                    //! A_ACMP_LOBS: [0] listener_observed override
  logic [31:0] lwsrp_ctrl;               //! LWSRP_CTRL: [0]=en, [1]=talker, [3:2]=classA queue
  logic [31:0] maap_ctrl;
  logic [31:0] link_ctrl;               //! LINK_CTRL: [0] sw_link                //! MAAP_CTRL: [0]=en, [1]=seed_valid, [15:8]=count, [31:16]=seed_offset
  logic [31:0] tone_ctrl;                //! TONE_CTRL: [0]=en (pilot tone)
  logic [31:0] gptp_pdelay;              //! GPTP_PDELAY: neighbor pdelay (ns)
  logic [31:0] lwsrp_vid;                //! LWSRP_VID: [11:0] SR VID
  logic [31:0] lwsrp_dmlo, lwsrp_dmhi;   //! lwSRP stream DMAC {dmhi[15:0], dmlo}
  logic [31:0] lwsrp_tspec;              //! LWSRP_TSPEC: {interval[31:16], max_frame[15:0]}
  logic [31:0] lwsrp_lat;                //! LWSRP_LATENCY: AccumulatedLatency (ns)
  logic [31:0] adp_eidlo, adp_eidhi;     //! ADP_EID: entity_id (EUI-64)
  logic [31:0] adp_midlo, adp_midhi;     //! ADP_MID: entity_model_id (EUI-64)
  logic [31:0] adp_ecaps;                //! ADP_ECAPS: entity_capabilities
  logic [31:0] adp_talk;                 //! ADP_TALK: {talker_caps[31:16], talker_sources[15:0]}
  logic [31:0] adp_list;                 //! ADP_LIST: {listener_caps[31:16], listener_sinks[15:0]}
  logic [31:0] adp_ccaps;                //! ADP_CCAPS: controller_capabilities
  logic [31:0] adp_gmlo, adp_gmhi;       //! ADP_GM: gptp_grandmaster_id
  logic [31:0] adp_domain;               //! ADP_DOMAIN: [7:0]=gptp_domain_number
  logic [31:0] adp_idx0;                 //! ADP_IDX0: {identify_control_index[31:16], current_config[15:0]}
  logic [31:0] adp_idx1;                 //! ADP_IDX1: [15:0]=interface_index
  logic [31:0] adp_aslo, adp_ashi;       //! ADP_ASSOC: association_id
  logic adp_adv_p;                       //! ADP advertise/info-changed strobe (1 cycle)
  logic adp_dep_p;                       //! ADP depart strobe (1 cycle)

  // RX dest-MAC TCAM filter programming (0x700 group)
  logic [31:0] tcam_ctrl;                //! TCAM_CTRL: [0]=default_pass
  logic [31:0] tcam_klo, tcam_khi;       //! TCAM key {khi[15:0], klo}
  logic [31:0] tcam_mlo, tcam_mhi;       //! TCAM mask {mhi[15:0], mlo}
  logic [31:0] tcam_act;                 //! TCAM action ([7:0])
  logic        tcam_wr_p;                //! entry-commit strobe (1 cycle)
  logic [4:0]  tcam_wr_index;            //! latched entry index for the commit
  logic        tcam_wr_valid_r;          //! latched add(1)/remove(0) for the commit

  // CBS power-on defaults: slope/credit values mirror ethernet_packet_pkg SR
  // classes (idleSlopes sum to 750 Mb/s = 75 % of the 1 Gb/s port rate, REQ-CBS-03;
  // hi/lo credit are calc_hi/lo_credit(idleSlope, 1e9) for MAX_FRAME_SIZE = 1522) —
  // but NO queue is shaped at reset. CBS shapes RESERVED SR classes only, never
  // best-effort (REQ-CBS-02); software (SRP/AVDECC reservation, `tc ... cbs`) opts a
  // queue in by setting CBS_CTRL[0]. The old default 4'b0011 contradicted the default
  // class map: cls_tcq=0xE4 routes untagged/BE traffic to q0, so shaping q0 at
  // idleSlope 300 Mb/s silently paced ALL best-effort TX to ~250 Mbit/s — measured on
  // silicon 2026-07-07 (datapath-input stall 42 % -> 0.4 % and TX wall moved to the
  // CPU the moment q0's en bit was cleared live via devmem 0x9000_040C).
  localparam int CBS_IDLE_RST [0:3] = '{300_000_000, 200_000_000, 150_000_000, 100_000_000}; //! idleSlope bps
  localparam int CBS_HI_RST   [0:3] = '{456, 304, 228, 152};       //! hiCredit bytes
  localparam int CBS_LO_RST   [0:3] = '{-1065, -1217, -1293, -1369}; //! loCredit bytes
  localparam bit [3:0] CBS_EN_RST   = 4'b0000;                    //! ALL unshaped at reset (BE must never be CBS-paced)

  integer i;                             //! Loop index for reset/stats iteration

  //! Register file write path: synchronous reset defaults, hardware event
  //! latching (before W1C), AXI-Lite register writes, W1C on IRQ_STATUS, and
  //! the single-cycle command strobes (stats snapshot/reset, PTP load/adjust/
  //! snapshot). Per-queue CBS registers live in the 0x400 window.
  always_ff @(posedge aclk) begin : register_write
    if (!aresetn) begin
      scratch <= 32'h0; irq_mask <= 32'h0; irq_status <= 32'h0;
      mac_ctrl <= 32'h13; mac_ifg <= 32'h0C; mac_alo <= 32'h0; mac_ahi <= 32'h0;
      mc_lo <= 32'h0; mc_hi <= 32'h0; phy_rst <= 32'h1;
      cls_ctrl <= 32'h1; cls_dpcp <= 32'h0; cls_map <= 32'h00FAC688;
      // PRIO_REGEN resets to IDENTITY (0xFAC688 packs p->p at 3 bits/entry).
      // The previous 0x688FAC half-swapped priorities (0..3 <-> 4..7), silently
      // regenerating PCP 1..3 to 5..7 so SR-class frames landed in the wrong
      // queue (HW-diagnosed 2026-07-05 during the CBS interference bring-up).
      cls_regen <= 32'h00FAC688; cls_tcq <= 32'h000000E4;
      ptp_ctrl <= 32'h1; ptp_incr <= 32'h0800_0000; ptp_adj <= 32'h0;
      ptp_twlo <= 32'h0; ptp_twhi <= 32'h0; ptp_oflo <= 32'h0; ptp_ofhi <= 32'h0;
      ptp_ilat <= 32'h0; ptp_elat <= 32'h0; ptp_tod_rd <= 64'h0;
      for (i = 0; i < NS; i = i + 1) stat_snap[i] <= 32'h0;
      for (i = 0; i < NUM_QUEUES; i = i + 1) begin
        cbs_idle[i] <= (i < 4) ? CBS_IDLE_RST[i][31:0] : 32'h0;
        cbs_hi[i]   <= (i < 4) ? CBS_HI_RST[i][31:0]   : 32'h0;
        cbs_lo[i]   <= (i < 4) ? CBS_LO_RST[i][31:0]   : 32'h0;
      end
      cbs_en <= CBS_EN_RST[NUM_QUEUES-1:0];
      adp_ctrl <= 32'h0000_1F00;   // enable=0, valid_time=31 (validity 62 s)
      // enable=0, bypass=1 (bit1: legacy stream-whenever-enabled — the
      // Milan probe-gated mode is opt-in until silicon-proven), VID=2
      aaf_ctrl <= 32'h0002_0002;
      acmp_lobs <= 32'h0;
      aaf_dmlo <= 32'hF000_FE01;   // MAAP-range default 91:E0:F0:00:FE:01
      aaf_dmhi <= 32'h0000_91E0;
      // lwSRP: disabled; class-A queue 3 (the reset PCP3->TC3->q3 map);
      // VID/DMAC mirror the AAF defaults; TSpec {interval 1, max_frame 224}
      lwsrp_ctrl <= 32'h0000_000C;
      maap_ctrl  <= 32'h0000_0800;
      link_ctrl  <= 32'h0000_0001;      //! link assumed UP until a daemon says otherwise
      tone_ctrl  <= 32'h0;
      gptp_pdelay <= 32'h0;
      lwsrp_vid  <= 32'h0000_0002;
      lwsrp_dmlo <= 32'hF000_FE01;
      lwsrp_dmhi <= 32'h0000_91E0;
      lwsrp_tspec<= 32'h0001_00E0;
      lwsrp_lat  <= 32'h0;
      adp_eidlo <= 32'h0; adp_eidhi <= 32'h0; adp_midlo <= 32'h0; adp_midhi <= 32'h0;
      adp_ecaps <= 32'h0; adp_talk <= 32'h0; adp_list <= 32'h0; adp_ccaps <= 32'h0;
      adp_gmlo <= 32'h0; adp_gmhi <= 32'h0; adp_domain <= 32'h0;
      adp_idx0 <= 32'h0; adp_idx1 <= 32'h0; adp_aslo <= 32'h0; adp_ashi <= 32'h0;
      tcam_ctrl <= 32'h1;   // default_pass = 1 (accept-all until software programs entries)
      tcam_klo <= 32'h0; tcam_khi <= 32'h0; tcam_mlo <= 32'h0; tcam_mhi <= 32'h0;
      tcam_act <= 32'h0; tcam_wr_index <= 5'h0; tcam_wr_valid_r <= 1'b0;
    end else begin
      // command strobes are single-cycle: default low, pulsed by writes below
      stats_snap_p <= 1'b0; stats_rst_p <= 1'b0;
      ptp_load_p <= 1'b0; ptp_adj_p <= 1'b0; ptp_snap_p <= 1'b0;
      adp_adv_p <= 1'b0; adp_dep_p <= 1'b0;
      tcam_wr_p <= 1'b0;

      // gettime result: latch the PHC snapshot when it returns (crosses CDC
      // asynchronously to the snapshot command, REQ-PTP-03/CSR-03).
      if (i_ptp_tod_valid) ptp_tod_rd <= i_ptp_tod;

      if (wr_fire) begin
        unique case (wr_addr)
          A_SCRATCH:   scratch  <= s_axi_wdata;
          A_IRQ_MASK:  irq_mask <= s_axi_wdata;
          A_IRQ_STATUS: begin // write-1-to-clear
            if (s_axi_wdata[0]) irq_status[0] <= 1'b0;
            if (s_axi_wdata[1]) irq_status[1] <= 1'b0;
            if (s_axi_wdata[2]) irq_status[2] <= 1'b0;
          end
          A_MAC_CTRL:  mac_ctrl <= s_axi_wdata;
          A_MAC_IFG:   mac_ifg  <= s_axi_wdata;
          A_MAC_ALO:   mac_alo  <= s_axi_wdata;
          A_MAC_AHI:   mac_ahi  <= s_axi_wdata;
          A_MC_LO:     mc_lo    <= s_axi_wdata;
          A_MC_HI:     mc_hi    <= s_axi_wdata;
          A_PHY_RST:   phy_rst  <= s_axi_wdata;
          A_STATS_CTRL: begin
            if (s_axi_wdata[0]) begin // snapshot: latch all counters coherently
              stats_snap_p <= 1'b1;
              for (i = 0; i < NS; i = i + 1)
                stat_snap[i] <= i_stats[i*32 +: 32];
            end
            if (s_axi_wdata[1]) stats_rst_p <= 1'b1; // reset external counters
          end
          A_CLS_CTRL:  cls_ctrl  <= s_axi_wdata;
          A_CLS_DPCP:  cls_dpcp  <= s_axi_wdata;
          A_CLS_MAP:   cls_map   <= s_axi_wdata;
          A_CLS_REGEN: cls_regen <= s_axi_wdata;
          A_CLS_TCQ:   cls_tcq   <= s_axi_wdata;
          A_PTP_CTRL:  ptp_ctrl  <= s_axi_wdata;
          A_PTP_INCR:  ptp_incr  <= s_axi_wdata;
          A_PTP_ADJ:   ptp_adj   <= s_axi_wdata;
          A_PTP_TWLO:  ptp_twlo  <= s_axi_wdata;
          A_PTP_TWHI:  ptp_twhi  <= s_axi_wdata;
          A_PTP_OFLO:  ptp_oflo  <= s_axi_wdata;
          A_PTP_OFHI:  ptp_ofhi  <= s_axi_wdata;
          A_PTP_ILAT:  ptp_ilat  <= s_axi_wdata;
          A_PTP_ELAT:  ptp_elat  <= s_axi_wdata;
          A_PTP_CMD: begin // command strobes, self-clearing (read back 0)
            if (s_axi_wdata[0]) ptp_load_p <= 1'b1;
            if (s_axi_wdata[1]) ptp_adj_p  <= 1'b1;
            if (s_axi_wdata[2]) ptp_snap_p <= 1'b1; // gettime; PTP_TOD_RD latched on i_ptp_tod_valid
          end
          A_AAF_CTRL:   aaf_ctrl  <= s_axi_wdata;
          A_ACMP_LOBS:  acmp_lobs <= s_axi_wdata;
          A_LWSRP_CTRL: lwsrp_ctrl <= s_axi_wdata;
          A_MAAP_CTRL:  maap_ctrl  <= s_axi_wdata;
          A_LINK_CTRL:  link_ctrl  <= s_axi_wdata;
          A_TONE_CTRL:  tone_ctrl  <= s_axi_wdata;
          A_GPTP_PDELAY: gptp_pdelay <= s_axi_wdata;
          A_LWSRP_VID:  lwsrp_vid  <= s_axi_wdata;
          A_LWSRP_DMLO: lwsrp_dmlo <= s_axi_wdata;
          A_LWSRP_DMHI: lwsrp_dmhi <= s_axi_wdata;
          A_LWSRP_TSPEC: lwsrp_tspec <= s_axi_wdata;
          A_LWSRP_LAT:  lwsrp_lat  <= s_axi_wdata;
          A_AAF_DMLO:   aaf_dmlo  <= s_axi_wdata;
          A_AAF_DMHI:   aaf_dmhi  <= s_axi_wdata;
          A_ADP_CTRL:   adp_ctrl  <= s_axi_wdata;
          A_ADP_EIDLO:  adp_eidlo <= s_axi_wdata;
          A_ADP_EIDHI:  adp_eidhi <= s_axi_wdata;
          A_ADP_MIDLO:  adp_midlo <= s_axi_wdata;
          A_ADP_MIDHI:  adp_midhi <= s_axi_wdata;
          A_ADP_ECAPS:  adp_ecaps <= s_axi_wdata;
          A_ADP_TALK:   adp_talk  <= s_axi_wdata;
          A_ADP_LIST:   adp_list  <= s_axi_wdata;
          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;
          A_ADP_GMLO:   adp_gmlo  <= s_axi_wdata;
          A_ADP_GMHI:   adp_gmhi  <= s_axi_wdata;
          A_ADP_DOMAIN: adp_domain<= s_axi_wdata;
          A_ADP_IDX0:   adp_idx0  <= s_axi_wdata;
          A_ADP_IDX1:   adp_idx1  <= s_axi_wdata;
          A_ADP_ASLO:   adp_aslo  <= s_axi_wdata;
          A_ADP_ASHI:   adp_ashi  <= s_axi_wdata;
          A_ADP_CMD: begin // W1S self-clearing strobes
            if (s_axi_wdata[0]) adp_adv_p <= 1'b1; // advertise now + bump available_index
            if (s_axi_wdata[1]) adp_dep_p <= 1'b1; // send ENTITY_DEPARTING
          end
          A_TCAM_CTRL: tcam_ctrl <= s_axi_wdata;
          A_TCAM_KLO:  tcam_klo  <= s_axi_wdata;
          A_TCAM_KHI:  tcam_khi  <= s_axi_wdata;
          A_TCAM_MLO:  tcam_mlo  <= s_axi_wdata;
          A_TCAM_MHI:  tcam_mhi  <= s_axi_wdata;
          A_TCAM_ACT:  tcam_act  <= s_axi_wdata;
          A_TCAM_CMD: begin // [4:0] index, [8] valid, [16] commit (W1S) -> pulse entry write
            if (s_axi_wdata[16]) begin
              tcam_wr_p       <= 1'b1;
              tcam_wr_index   <= s_axi_wdata[4:0];
              tcam_wr_valid_r <= s_axi_wdata[8];
            end
          end
          default: begin
            // per-queue CBS window 0x400 + q*0x20 (stride 0x20 => off[5+:QW] = queue)
            if (wr_addr >= A_CBS_BASE && wr_addr < A_CBS_END) begin
              logic [ADDR_WIDTH-1:0] off;
              off = wr_addr - A_CBS_BASE;
              case (off[4:0])
                5'h00: cbs_idle[off[5 +: QW]] <= s_axi_wdata;
                5'h04: cbs_hi  [off[5 +: QW]] <= s_axi_wdata;
                5'h08: cbs_lo  [off[5 +: QW]] <= s_axi_wdata;
                5'h0C: cbs_en  [off[5 +: QW]] <= s_axi_wdata[0];
                default: ;
              endcase
            end
          end
        endcase
      end

      // Hardware-set event latches, applied AFTER the W1C write above so a
      // hardware event coincident with a software acknowledge is NOT lost: the
      // set wins the same-cycle race (REQ-CSR-04).
      if (i_evt_tx_ts_ready)   irq_status[0] <= 1'b1;
      if (i_evt_link_change)   irq_status[1] <= 1'b1;
      if (i_evt_rmon_rollover) irq_status[2] <= 1'b1;
    end
  end

  // ==========================================================================
  //  Config-in-RAM read path (area-70): shadow BRAM + defaults ROM + sweep
  // ==========================================================================

  //! reset/readback value per byte address — the single source shared by the
  //! defaults ROM init (must mirror the register_write reset block above)
  function automatic [31:0] csr_default(input [10:0] a);
    csr_default = 32'h0;
    unique case (a)
      A_ID[10:0]:         csr_default = 32'h4D49_4C4E;      // "MILN"
      A_VERSION[10:0]:    csr_default = VERSION;
      A_CAP[10:0]:        csr_default = { 8'h00, 8'd64,
                                          1'b0, 1'b1, 1'b1, 1'b1,
                                          1'b1, 1'b1, 1'b1, 1'b1,
                                          4'h0, 4'(NUM_QUEUES) };
      A_MAC_CTRL[10:0]:   csr_default = 32'h13;
      A_MAC_IFG[10:0]:    csr_default = 32'h0C;
      A_PHY_RST[10:0]:    csr_default = 32'h1;
      A_CLS_CTRL[10:0]:   csr_default = 32'h1;
      A_CLS_MAP[10:0]:    csr_default = 32'h00FAC688;
      A_CLS_REGEN[10:0]:  csr_default = 32'h00FAC688;
      A_CLS_TCQ[10:0]:    csr_default = 32'h000000E4;
      A_PTP_CTRL[10:0]:   csr_default = 32'h1;
      A_PTP_INCR[10:0]:   csr_default = 32'h0800_0000;
      A_ADP_CTRL[10:0]:   csr_default = 32'h0000_1F00;
      A_AAF_CTRL[10:0]:   csr_default = 32'h0002_0002;
      A_AAF_DMLO[10:0]:   csr_default = 32'hF000_FE01;
      A_AAF_DMHI[10:0]:   csr_default = 32'h0000_91E0;
      A_LWSRP_CTRL[10:0]: csr_default = 32'h0000_000C;
      A_LWSRP_VID[10:0]:  csr_default = 32'h0000_0002;
      A_LWSRP_DMLO[10:0]: csr_default = 32'hF000_FE01;
      A_LWSRP_DMHI[10:0]: csr_default = 32'h0000_91E0;
      A_LWSRP_TSPEC[10:0]: csr_default = 32'h0001_00E0;
      A_TCAM_CTRL[10:0]:  csr_default = 32'h1;
      A_LINK_CTRL[10:0]:  csr_default = 32'h1;   // link assumed up at boot
      A_MAAP_CTRL[10:0]:  csr_default = 32'h0000_0800;   // count=8, en=0
      default: begin
        if (a >= A_CBS_BASE[10:0] && a < A_CBS_END[10:0]) begin
          case (a[4:0])
            5'h00:   csr_default = CBS_IDLE_RST[a[5 +: QW]][31:0];
            5'h04:   csr_default = CBS_HI_RST[a[5 +: QW]][31:0];
            5'h08:   csr_default = CBS_LO_RST[a[5 +: QW]][31:0];
            default: csr_default = 32'h0;   // CTRL: en resets 0
          endcase
        end
      end
    endcase
  endfunction

  //! plain-RW register (readback == stored word): served by the shadow.
  //! Strobe/W1C/live registers and unmapped addresses are NOT shadow-written.
  function automatic logic is_plain_rw(input [ADDR_WIDTH-1:0] a);
    is_plain_rw = 1'b0;
    unique case (a)
      A_SCRATCH, A_IRQ_MASK,
      A_MAC_CTRL, A_MAC_IFG, A_MAC_ALO, A_MAC_AHI, A_MC_LO, A_MC_HI, A_PHY_RST,
      A_CLS_CTRL, A_CLS_DPCP, A_CLS_MAP, A_CLS_REGEN, A_CLS_TCQ,
      A_PTP_CTRL, A_PTP_INCR, A_PTP_ADJ, A_PTP_TWLO, A_PTP_TWHI,
      A_PTP_OFLO, A_PTP_OFHI, A_PTP_ILAT, A_PTP_ELAT,
      A_ADP_CTRL, A_ADP_EIDLO, A_ADP_EIDHI, A_ADP_MIDLO, A_ADP_MIDHI,
      A_ADP_ECAPS, A_ADP_TALK, A_ADP_LIST, A_ADP_CCAPS, A_ADP_GMLO,
      A_ADP_GMHI, A_ADP_DOMAIN, A_ADP_IDX0, A_ADP_IDX1, A_ADP_ASLO, A_ADP_ASHI,
      A_AAF_CTRL, A_AAF_DMLO, A_AAF_DMHI, A_ACMP_LOBS,
      A_LWSRP_CTRL, A_LWSRP_VID, A_LWSRP_DMLO, A_LWSRP_DMHI,
      A_LWSRP_TSPEC, A_LWSRP_LAT,
      A_TCAM_CTRL, A_TCAM_KLO, A_TCAM_KHI, A_TCAM_MLO, A_TCAM_MHI, A_TCAM_ACT,
      A_MAAP_CTRL, A_TONE_CTRL, A_GPTP_PDELAY, A_LINK_CTRL:
        is_plain_rw = 1'b1;
      default:
        if (a >= A_CBS_BASE && a < A_CBS_END)
          is_plain_rw = (a[4:0] == 5'h00) || (a[4:0] == 5'h04) ||
                        (a[4:0] == 5'h08) || (a[4:0] == 5'h0C);
    endcase
  endfunction

  //! CBS_CTRL readback is masked to bit 0: shadow stores the READBACK value
  wire is_cbs_en_wr = (wr_addr >= A_CBS_BASE) && (wr_addr < A_CBS_END) &&
                      (wr_addr[4:0] == 5'h0C);
  wire [31:0] shadow_wval = is_cbs_en_wr ? {31'h0, s_axi_wdata[0]} : s_axi_wdata;

  (* ram_style = "block" *) logic [31:0] shadow_ram [0:511];
  (* ram_style = "block" *) logic [31:0] dflt_rom   [0:511];
  initial begin
    for (int k = 0; k < 512; k++) dflt_rom[k] = csr_default(11'(k * 4));
  end

  logic [31:0] shadow_q, dflt_q;
  wire         shadow_axi_we = wr_fire && !(|wr_addr[ADDR_WIDTH-1:11]) &&
                               is_plain_rw(wr_addr);
  //! sweep pipeline: ROM word for sweep_cnt lands one cycle later
  wire         sweep_wr = sweep_busy && (sweep_cnt >= 10'd1) && (sweep_cnt <= 10'd512);

  //! single muxed write port: two `if` arms with distinct address expressions
  //! infer TWO write ports and push the RAM to LUTRAM (Synth 8-6849 infeasible)
  wire         sh_we    = sweep_wr || shadow_axi_we;
  wire [8:0]   sh_waddr = sweep_wr ? 9'(sweep_cnt - 10'd1) : wr_addr[10:2];
  wire [31:0]  sh_wdata = sweep_wr ? dflt_q : shadow_wval;

  always_ff @(posedge aclk) begin : shadow_mem
    dflt_q <= dflt_rom[sweep_cnt[8:0]];
    if (sh_we)
      shadow_ram[sh_waddr] <= sh_wdata;
    shadow_q <= shadow_ram[rd_addr[10:2]];
  end

  always_ff @(posedge aclk) begin : shadow_sweep
    if (!aresetn) begin
      sweep_busy <= 1'b1;
      sweep_cnt  <= 10'd0;
    end else if (sweep_busy) begin
      sweep_cnt <= sweep_cnt + 10'd1;
      if (sweep_cnt == 10'd513) sweep_busy <= 1'b0;
    end
  end

  // ==========================================================================
  //  Read decode — LIVE registers only (status/W1C/counters/windows); every
  //  plain-RW config register reads from the shadow BRAM.
  // ==========================================================================
  logic [31:0] live_mux;
  logic        live_hit;

  always_comb begin : read_mux
    logic [ADDR_WIDTH-1:0] soff;         //! STAT window offset
    live_mux = 32'h0;
    live_hit = 1'b1;
    soff = rd_addr_q - A_STATS_BASE;
    unique case (rd_addr_q)
      A_IRQ_STATUS: live_mux = irq_status;
      A_IRQ_RAW:    live_mux = irq_status;
      A_MAC_STATUS: live_mux = { 28'h0, i_full_duplex, i_speed, i_link_up };
      A_PTP_TRLO:   live_mux = ptp_tod_rd[31:0];
      A_PTP_TRHI:   live_mux = ptp_tod_rd[63:32];
      A_ADP_STATUS: live_mux = i_adp_available_index;       // RO available_index
      A_ADP_DIAG:   live_mux = {14'd0, i_adp_depart_src, i_adp_rearm_cnt, i_adp_depart_cnt};
      // AECP: [16]=locked, [15:0]=cmd_count | resp_count[31:16], current_config[15:0]
      A_AECP_STAT0: live_mux = {15'd0, i_aecp_locked, i_aecp_cmd_count};
      A_AECP_STAT1: live_mux = {i_aecp_resp_count, i_aecp_current_config};
      A_ACMP_STAT:  live_mux = {i_acmp_resp_count, i_acmp_cmd_count};
      A_ACMP_TALKER: live_mux = {28'd0, i_aaf_gate, o_acmp_lobs, i_acmp_talker_active, i_acmp_probe_armed};
      A_AAF_FRAMES: live_mux = i_aaf_frames;
      A_AAF_PAIRS:  live_mux = i_aaf_pairs;
      A_LWSRP_STATUS: live_mux = i_lwsrp_status;
      A_LWSRP_SLOPE: live_mux = i_lwsrp_slope;
      A_LWSRP_CNT:  live_mux = i_lwsrp_cnt;
      A_ACMPL_STATE: live_mux = i_acmpl_state;
      A_ACMPL_TKLO: live_mux = i_acmpl_talker_lo;
      A_ACMPL_TKHI: live_mux = i_acmpl_talker_hi;
      A_ACMPL_CNT:  live_mux = i_acmpl_cnt;
      A_ACMPL_TUID: live_mux = i_acmpl_tuid;
      A_AVTPRX_STAT: live_mux = i_avtprx_stat;
      A_AVTPRX_FRX:  live_mux = i_avtprx_frx;
      A_AVTPRX_ERR:  live_mux = i_avtprx_err;
      A_PCMRX_CNT:   live_mux = i_pcmrx_cnt;
      A_PCMRX_TS:    live_mux = i_pcmrx_ts;
      A_MAAP_STAT0:  live_mux = i_maap_stat0;
      A_MAAP_STAT1:  live_mux = i_maap_stat1;
      A_I2SPB_STAT:  live_mux = i_i2spb_stat;
      A_I2SPB_TRIM:  live_mux = i_i2spb_trim;
      A_ACMPL_DBG:  live_mux = i_acmpl_dbg;
      A_AVTPRX_TSD: live_mux = i_avtprx_tsd;
      A_RST_EPOCH:  live_mux = {24'd0, rst_epoch_r};
      A_I2SPB_DBG:  live_mux = i_i2spb_dbg;
      default: begin
        if (rd_addr_q >= A_STATS_BASE && rd_addr_q < A_STATS_END)
          live_mux = stat_snap[soff[2 +: 4]];
        else
          live_hit = 1'b0;                //! -> shadow (or 0 above the window)
      end
    endcase
  end

  //! Register read data one cycle after the AR handshake (BRAM latency);
  //! RDATA is held stable while RVALID is asserted.
  wire rd_in_window = ~|rd_addr_q[ADDR_WIDTH-1:11];
  always_ff @(posedge aclk) begin : read_data_reg
    if (!aresetn) r_data <= 32'h0;
    else if (rd_pend)
      r_data <= !rd_in_window ? 32'h0
              : live_hit      ? live_mux
              : shadow_q;
  end

  // ==========================================================================
  //  Output wiring (register fields -> flat config ports)
  // ==========================================================================
  assign o_mac_tx_en    = mac_ctrl[0];
  assign o_mac_rx_en    = mac_ctrl[1];
  assign o_mac_promisc  = mac_ctrl[2];
  assign o_mac_allmulti = mac_ctrl[3];
  assign o_mac_is_1g    = mac_ctrl[4];
  assign o_mac_ifg      = mac_ifg[7:0];
  assign o_mac_addr     = {mac_ahi[15:0], mac_alo};
  assign o_mc_hash      = {mc_hi, mc_lo};
  assign o_phy_reset_n  = phy_rst[0];

  assign o_stats_snapshot = stats_snap_p;
  assign o_stats_reset    = stats_rst_p;

  assign o_cls_use_pcp      = cls_ctrl[0];
  assign o_cls_dmac_check   = cls_ctrl[1];
  assign o_cls_default_pcp  = cls_dpcp[2:0];
  assign o_cls_pcp_tc_map   = cls_map[23:0];
  assign o_cls_prio_regen   = cls_regen[23:0];
  assign o_cls_tc_queue_map = cls_tcq;

  genvar g;
  generate
    for (g = 0; g < NUM_QUEUES; g = g + 1) begin : gen_cbs_out
      assign o_cbs_idle_slope[g*32 +: 32] = cbs_idle[g];
      assign o_cbs_hi_credit [g*32 +: 32] = cbs_hi[g];
      assign o_cbs_lo_credit [g*32 +: 32] = cbs_lo[g];
      assign o_cbs_enable[g]              = cbs_en[g];
    end
  endgenerate

  assign o_ptp_enable       = ptp_ctrl[0];
  assign o_ptp_incr         = ptp_incr;
  assign o_ptp_adj          = ptp_adj;
  assign o_ptp_tod_wr       = {ptp_twhi, ptp_twlo};
  assign o_ptp_offset       = {ptp_ofhi, ptp_oflo};
  assign o_ptp_cmd_load     = ptp_load_p;
  assign o_ptp_cmd_adjust   = ptp_adj_p;
  assign o_ptp_cmd_snapshot = ptp_snap_p;
  assign o_ptp_ingress_lat  = ptp_ilat;
  assign o_ptp_egress_lat   = ptp_elat;

  assign o_aaf_enable          = aaf_ctrl[0];
  assign o_aaf_bypass          = aaf_ctrl[1];
  assign o_acmp_lobs           = acmp_lobs[0];
  assign o_tone_enable      = tone_ctrl[0];
  assign o_tone_att         = tone_ctrl[3:1];
  //! Reset-epoch canary: counts datapath reset RELEASES in flops WITHOUT a
  //! reset clause (bitstream-init 0, survive axis resets). Software compares
  //! epochs to detect hidden fabric resets that the config shadow masks
  //! (the 2026-07-19 link-bounce forensics: CSR reads lied after a reset).
  reg [7:0] rst_epoch_r = 8'd0;
  reg       rstn_seen_r = 1'b0;
  always @(posedge aclk) begin : epoch_cnt
    rstn_seen_r <= aresetn;
    if (aresetn && !rstn_seen_r) rst_epoch_r <= rst_epoch_r + 8'd1;
  end : epoch_cnt

  assign o_sw_link          = link_ctrl[0];
  assign o_mac_reinit       = link_ctrl[1];
  assign o_maap_enable      = maap_ctrl[0];
  assign o_maap_seed_valid  = maap_ctrl[1];
  assign o_maap_count       = maap_ctrl[15:8];
  assign o_maap_seed_offset = maap_ctrl[31:16];

  assign o_lwsrp_enable        = lwsrp_ctrl[0];
  assign o_lwsrp_talker_en     = lwsrp_ctrl[1];
  assign o_lwsrp_qidx          = lwsrp_ctrl[3:2];
  assign o_lwsrp_vid           = lwsrp_vid[11:0];
  assign o_lwsrp_dest_mac      = {lwsrp_dmhi[15:0], lwsrp_dmlo};
  assign o_lwsrp_max_frame     = lwsrp_tspec[15:0];
  assign o_lwsrp_interval      = lwsrp_tspec[31:16];
  assign o_lwsrp_latency       = lwsrp_lat;
  assign o_aaf_vid             = aaf_ctrl[27:16];
  assign o_aaf_dest_mac        = {aaf_dmhi[15:0], aaf_dmlo};
  assign o_adp_enable          = adp_ctrl[0];
  assign o_adp_valid_time      = adp_ctrl[12:8];
  assign o_adp_entity_id       = {adp_eidhi, adp_eidlo};
  assign o_adp_entity_model_id = {adp_midhi, adp_midlo};
  assign o_adp_entity_caps     = adp_ecaps;
  assign o_adp_talker_sources  = adp_talk[15:0];
  assign o_adp_talker_caps     = adp_talk[31:16];
  assign o_adp_listener_sinks  = adp_list[15:0];
  assign o_adp_listener_caps   = adp_list[31:16];
  assign o_adp_controller_caps = adp_ccaps;
  assign o_adp_gptp_gm         = {adp_gmhi, adp_gmlo};
  assign o_gptp_pdelay_ns      = gptp_pdelay;
  assign o_adp_gptp_domain     = adp_domain[7:0];
  assign o_adp_current_config  = adp_idx0[15:0];
  assign o_adp_identify_index  = adp_idx0[31:16];
  assign o_adp_interface_index = adp_idx1[15:0];
  assign o_adp_association_id  = {adp_ashi, adp_aslo};
  assign o_adp_advertise_p     = adp_adv_p;
  assign o_adp_depart_p        = adp_dep_p;

  assign o_tcam_default_pass = tcam_ctrl[0];
  assign o_tcam_wr_en        = tcam_wr_p;
  assign o_tcam_wr_index     = tcam_wr_index;
  assign o_tcam_wr_valid     = tcam_wr_valid_r;
  assign o_tcam_wr_key       = {tcam_khi[15:0], tcam_klo};
  assign o_tcam_wr_mask      = {tcam_mhi[15:0], tcam_mlo};
  assign o_tcam_wr_action    = tcam_act[7:0];

  assign o_irq = |(irq_status & irq_mask);

  //! wstrb is intentionally ignored (ABI: full 32-bit writes); tie off to satisfy lint
  wire _unused_ok = &{1'b0, s_axi_wstrb};

endmodule

`default_nettype wire

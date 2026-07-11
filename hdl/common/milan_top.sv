/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : milan_top.sv
  Author      : Oguz Kahraman / Kebag Logic

  Date        : 2025-07-18 (CSR integration 2026-07-01)
  Description : Top-level integration module for the Milan FPGA platform.

                Subsystems:
                - milan_dma_wrapper  : Zynq PS + DMA + AXI interconnect, and the
                                       AXI4-Lite CSR master (M_AXI_GP0 -> milan_csr)
                - milan_csr          : memory-mapped TSN control plane (REQ-CSR-*)
                - traffic_controller : IEEE 802.1Q classify + 802.1Qav CBS shaper
                - ptp_timestamp      : PTP hardware clock + TX/RX timestamping
                - ethernet_mac       : 1G RGMII MAC with TX/RX FIFOs
                - ethernet_counters  : Ethernet RMON event statistics

                TX path: DMA -> Traffic Shaper -> PTP TS -> MAC -> RGMII
                RX path: RGMII -> MAC -> PTP TS -> DMA

                All previously hard-wired knobs (link speed, MAC enables/IFG,
                classifier map, CBS slopes, PTP rate, stats reset) are now driven
                by milan_csr registers; status (link, RMON counters, PTP TOD) and
                events (TX-timestamp-ready, link-change, RMON-rollover) flow back
                into milan_csr and out to the PS interrupt.

  Company     : Kebag Logic
  Project     : Milan FPGA Platform
------------------------------------------------------------------------------
*/

`default_nettype none
`include "ethernet_events.svh"
`include "ethernet_packet_pkg.sv"

module milan_top import ethernet_packet_pkg::*; #(
  parameter int TDATA_WIDTH = 64,
  parameter int TX_FIFO_DEPTH = 2048,
  parameter int RX_FIFO_DEPTH = 2048,
  parameter int NUM_QUEUES = NUMBER_OF_QUEUES,
  //! MAC synthesis target (portability, docs/OPEN_SOURCE_MIGRATION.md T2.1):
  //! "XILINX" for the Artix/Zynq bitstream; "GENERIC" for open flows / other
  //! devices / Verilator (the Forencich MAC then uses generic DDR I/O, no SelectIO).
  parameter MAC_TARGET      = "XILINX",
  parameter MAC_IODDR_STYLE = "IODDR",   //! "IODDR" (Xilinx) or "IODDR2"/"GENERIC"
  parameter MAC_CLK_STYLE   = "BUFR"     //! "BUFR"/"BUFG" (Xilinx) or "GENERIC"
)(
  inout wire [14:0] DDR_addr,
  inout wire [2:0] DDR_ba,
  inout wire DDR_cas_n,
  inout wire DDR_ck_n,
  inout wire DDR_ck_p,
  inout wire DDR_cke,
  inout wire DDR_cs_n,
  inout wire [3:0] DDR_dm,
  inout wire [31:0] DDR_dq,
  inout wire [3:0] DDR_dqs_n,
  inout wire [3:0] DDR_dqs_p,
  inout wire DDR_odt,
  inout wire DDR_ras_n,
  inout wire DDR_reset_n,
  inout wire DDR_we_n,
  inout wire FIXED_IO_ddr_vrn,
  inout wire FIXED_IO_ddr_vrp,
  inout wire [53:0] FIXED_IO_mio,
  inout wire FIXED_IO_ps_clk,
  inout wire FIXED_IO_ps_porb,
  inout wire FIXED_IO_ps_srstb,

  output wire MDIO_link_1_mdc,
  inout wire MDIO_link_1_mdio_io,
  input wire rgmii_rx_clk,
  input wire [3:0] rgmii_rxd,
  input wire rgmii_rx_ctl,
  output wire rgmii_tx_clk,
  output wire [3:0] rgmii_txd,
  output wire rgmii_tx_ctl

);

  //! AXI-Stream logic clock (from PS, 100 MHz)
  wire axis_clk;
  //! Active-low synchronous reset for axis_clk domain
  wire axis_resetn;
  //! 125 MHz TX clock, 90° phase shifted for RGMII DDR alignment
  wire gtx90_clk;
  //! 125 MHz Gigabit TX reference clock
  wire gtx_clk;
  //! Active-low synchronous reset for gtx_clk domain
  wire gtx_resetn;


  //! RX path: MAC output → PTP timestamping core
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_to_ts();
  //! RX path: PTP timestamping output → RX dest-MAC filter
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_ptp_to_filt();
  //! RX path: dest-MAC filter output → DMA
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_to_dma();
  //! TX path: DMA output → 802.1Q traffic shaper
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_shaper();
  //! TX path: Traffic shaper output → PTP timestamping core
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_shaper_to_ts();
  //! TX path: PTP timestamping output → ADP/datapath TX arbiter
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_dp_to_arb();
  //! TX path: TX arbiter output (datapath + ADP merged) → MAC
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_mac();
  //! PTP timestamp metadata stream: PTP core → DMA (timestamp + seq_id + direction)
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) ts_metadata_axis();

  // ==========================================================================
  //  CSR <-> datapath signals
  // ==========================================================================
  //! AXI4-Lite CSR bus from the PS (M_AXI_GP0 via milan_dma_wrapper).
  wire [31:0] csr_awaddr;  wire [2:0] csr_awprot; wire csr_awvalid, csr_awready;
  wire [31:0] csr_wdata;   wire [3:0] csr_wstrb;  wire csr_wvalid,  csr_wready;
  wire [1:0]  csr_bresp;   wire csr_bvalid, csr_bready;
  wire [31:0] csr_araddr;  wire [2:0] csr_arprot; wire csr_arvalid, csr_arready;
  wire [31:0] csr_rdata;   wire [1:0] csr_rresp;  wire csr_rvalid,  csr_rready;
  wire        csr_irq;

  //! MAC control / status
  wire        cfg_mac_tx_en, cfg_mac_rx_en, cfg_mac_promisc, cfg_mac_allmulti, cfg_mac_is_1g;
  wire [7:0]  cfg_mac_ifg;
  wire [47:0] cfg_mac_addr;      // reserved for RX address filter (REQ-MAC-02)
  wire [63:0] cfg_mc_hash;       // reserved for multicast hash (REQ-MAC-02)
  wire        cfg_phy_reset_n;   // reserved for PHY reset GPIO (REQ-MAC-06)
  wire [1:0]  mac_speed;         // from MAC speed[] indication

  //! Statistics
  wire        cfg_stats_snapshot, cfg_stats_reset;
  wire [32*9-1:0] stats_counts;
  wire        stats_rollover;

  //! Classifier config
  wire        cfg_cls_use_pcp, cfg_cls_dmac_check;
  wire [2:0]  cfg_cls_default_pcp;
  wire [23:0] cfg_cls_pcp_tc_map, cfg_cls_prio_regen;
  wire [31:0] cfg_cls_tc_queue_map;

  //! CBS config (packed per queue)
  wire [32*NUM_QUEUES-1:0] cfg_cbs_idle_slope, cfg_cbs_hi_credit, cfg_cbs_lo_credit;
  wire [NUM_QUEUES-1:0]    cfg_cbs_enable;

  //! PTP config / status
  wire        cfg_ptp_enable;
  wire [31:0] cfg_ptp_incr, cfg_ptp_adj;
  wire [63:0] cfg_ptp_tod_wr, cfg_ptp_offset;
  wire        cfg_ptp_cmd_load, cfg_ptp_cmd_adjust, cfg_ptp_cmd_snapshot;
  wire [31:0] cfg_ptp_ingress_lat, cfg_ptp_egress_lat;
  wire [63:0] ptp_tod_rd;
  wire        ptp_tod_rd_valid;
  wire        evt_tx_ts_ready;

  //! ADP advertiser config (from milan_csr 0x600 group) + status
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
  //! ADP advertiser TX AXIS (flat) → TX arbiter s_adp
  wire [TDATA_WIDTH-1:0]   adp_tx_tdata;
  wire [TDATA_WIDTH/8-1:0] adp_tx_tkeep;
  wire                     adp_tx_tvalid, adp_tx_tlast, adp_tx_tready;

  //! RX dest-MAC TCAM filter programming (from milan_csr 0x700 group)
  wire        cfg_tcam_default_pass, cfg_tcam_wr_en, cfg_tcam_wr_valid;
  wire [4:0]  cfg_tcam_wr_index;
  wire [47:0] cfg_tcam_wr_key, cfg_tcam_wr_mask;
  wire [7:0]  cfg_tcam_wr_action;

  //! `mac_speed` is generated in the MAC's gtx_clk (125 MHz) domain; synchronise
  //! it into axis_clk with a 2-FF synchroniser before it is used by the CSR
  //! status readback and the link-change detector (avoids latching a transient
  //! mixed code while the two bits settle).
  (* ASYNC_REG = "TRUE" *) reg [1:0] speed_meta, speed_sync;
  always_ff @(posedge axis_clk) begin : mac_speed_cdc
    if (!axis_resetn) begin
      speed_meta <= 2'b10; speed_sync <= 2'b10;
    end else begin
      speed_meta <= mac_speed;
      speed_sync <= speed_meta;
    end
  end

  //! Link-status change detector (for IRQ / stats), on the synchronised speed.
  wire        link_up   = 1'b1;              // TODO: derive from PHY/MAC status (REQ-MAC-03)
  wire        full_dpx  = 1'b1;
  reg  [1:0]  speed_q;
  reg         evt_link_change;
  always_ff @(posedge axis_clk) begin : link_change_detect
    if (!axis_resetn) begin
      speed_q <= 2'b10; evt_link_change <= 1'b0;
    end else begin
      speed_q <= speed_sync;
      evt_link_change <= (speed_q != speed_sync);
    end
  end


  milan_dma_wrapper milan_wrapper(
    .m_axi_csr_awaddr(csr_awaddr),
    .m_axi_csr_awprot(csr_awprot),
    .m_axi_csr_awvalid(csr_awvalid),
    .m_axi_csr_awready(csr_awready),
    .m_axi_csr_wdata(csr_wdata),
    .m_axi_csr_wstrb(csr_wstrb),
    .m_axi_csr_wvalid(csr_wvalid),
    .m_axi_csr_wready(csr_wready),
    .m_axi_csr_bresp(csr_bresp),
    .m_axi_csr_bvalid(csr_bvalid),
    .m_axi_csr_bready(csr_bready),
    .m_axi_csr_araddr(csr_araddr),
    .m_axi_csr_arprot(csr_arprot),
    .m_axi_csr_arvalid(csr_arvalid),
    .m_axi_csr_arready(csr_arready),
    .m_axi_csr_rdata(csr_rdata),
    .m_axi_csr_rresp(csr_rresp),
    .m_axi_csr_rvalid(csr_rvalid),
    .m_axi_csr_rready(csr_rready),
    .irq_csr(csr_irq),
    .DDR_addr(DDR_addr),
    .DDR_ba(DDR_ba),
    .DDR_cas_n(DDR_cas_n),
    .DDR_ck_n(DDR_ck_n),
    .DDR_ck_p(DDR_ck_p),
    .DDR_cke(DDR_cke),
    .DDR_cs_n(DDR_cs_n),
    .DDR_dm(DDR_dm),
    .DDR_dq(DDR_dq),
    .DDR_dqs_n(DDR_dqs_n),
    .DDR_dqs_p(DDR_dqs_p),
    .DDR_odt(DDR_odt),
    .DDR_ras_n(DDR_ras_n),
    .DDR_reset_n(DDR_reset_n),
    .DDR_we_n(DDR_we_n),
    .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
    .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
    .FIXED_IO_mio(FIXED_IO_mio),
    .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
    .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
    .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
    .MDIO_link_1_mdc(MDIO_link_1_mdc),
    .MDIO_link_1_mdio_io(MDIO_link_1_mdio_io),
    .axis_clk(axis_clk),
    .axis_resetn(axis_resetn),
    .gtx90_clk(gtx90_clk),
    .gtx_clk(gtx_clk),
    .gtx_reset_n(gtx_resetn),
    .m_axis_tx_eth_tdata(tx_axis_to_shaper.tdata),
    .m_axis_tx_eth_tkeep(tx_axis_to_shaper.tkeep),
    .m_axis_tx_eth_tlast(tx_axis_to_shaper.tlast),
    .m_axis_tx_eth_tready(tx_axis_to_shaper.tready),
    .m_axis_tx_eth_tvalid(tx_axis_to_shaper.tvalid),
    .s_axis_rx_eth_tdata(rx_axis_to_dma.tdata),
    .s_axis_rx_eth_tkeep(rx_axis_to_dma.tkeep),
    .s_axis_rx_eth_tlast(rx_axis_to_dma.tlast),
    .s_axis_rx_eth_tready(rx_axis_to_dma.tready),
    .s_axis_rx_eth_tvalid(rx_axis_to_dma.tvalid),
    .s_axis_ts_metadata_tdata(ts_metadata_axis.tdata),
    .s_axis_ts_metadata_tkeep(ts_metadata_axis.tkeep),
    .s_axis_ts_metadata_tlast(ts_metadata_axis.tlast),
    .s_axis_ts_metadata_tready(ts_metadata_axis.tready),
    .s_axis_ts_metadata_tvalid(ts_metadata_axis.tvalid)
  );

  // ==========================================================================
  //  Memory-mapped control plane
  // ==========================================================================
  milan_csr #(
    .NUM_QUEUES(NUM_QUEUES),
    .ADDR_WIDTH(16)
  ) csr (
    .aclk    (axis_clk),
    .aresetn (axis_resetn),
    // AXI4-Lite slave (low 16 bits of the CSR master address = register offset)
    .s_axi_awaddr (csr_awaddr[15:0]),
    .s_axi_awvalid(csr_awvalid),
    .s_axi_awready(csr_awready),
    .s_axi_wdata  (csr_wdata),
    .s_axi_wstrb  (csr_wstrb),
    .s_axi_wvalid (csr_wvalid),
    .s_axi_wready (csr_wready),
    .s_axi_bresp  (csr_bresp),
    .s_axi_bvalid (csr_bvalid),
    .s_axi_bready (csr_bready),
    .s_axi_araddr (csr_araddr[15:0]),
    .s_axi_arvalid(csr_arvalid),
    .s_axi_arready(csr_arready),
    .s_axi_rdata  (csr_rdata),
    .s_axi_rresp  (csr_rresp),
    .s_axi_rvalid (csr_rvalid),
    .s_axi_rready (csr_rready),
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
    .i_link_up     (link_up),
    .i_speed       (speed_sync),
    .i_full_duplex (full_dpx),
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
  //  RX destination-MAC filter (TCAM, REQ-MAC-02): accept/drop RX frames by
  //  destination MAC, programmed from the milan_csr 0x700 TCAM group. Sits after
  //  PTP timestamping so accepted frames keep their RX timestamp. default_pass=1
  //  at reset => accept-all until software installs entries (safe bring-up).
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
  //  The advertiser builds ADPDU frames from the milan_csr 0x600 identity/control
  //  registers; adp_tx_arbiter merges them into the MAC TX stream between frames.
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

  //! Link-status edge pulses drive advertise (up) / depart (down). `link_up` is
  //! still tied high today (REQ-MAC-03 TODO) so the up-pulse fires once after
  //! reset — the entity advertises on power-up, which is the desired behaviour.
  reg link_up_q; reg adp_link_up_p, adp_link_down_p;
  always_ff @(posedge axis_clk) begin : adp_link_edge
    if (!axis_resetn) begin
      link_up_q <= 1'b0; adp_link_up_p <= 1'b0; adp_link_down_p <= 1'b0;
    end else begin
      link_up_q       <= link_up;
      adp_link_up_p   <=  link_up & ~link_up_q;
      adp_link_down_p <= ~link_up &  link_up_q;
    end
  end

  adp_advertiser adp_adv (
    .clk_i (axis_clk),
    .rst_n (axis_resetn),
    .enable_i (cfg_adp_enable),
    .tick_i   (adp_tick_1s),
    .link_up_i     (adp_link_up_p),
    .link_down_i   (adp_link_down_p),
    .shutdown_i    (cfg_adp_depart_p),   // software depart (ADP_CMD[1])
    .gm_change_i   (1'b0),               // TODO: from gPTP GM tracking (REQ-PTP)
    .info_changed_i(cfg_adp_advertise_p),// software advertise / field change (ADP_CMD[0])
    .rcv_discover_i(1'b0),               // TODO: from KL_adp_parser.rcv_adp_discover_o (§B.1)
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


  logic [_ETH_EVENT_COUNTER-1:0] mac_events;

  ethernet_events ethernet_counters(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .stats_reset(cfg_stats_reset),
    .events(mac_events),
    .counts_o(stats_counts),
    .rollover_o(stats_rollover)
  );

  eth_mac_1g_rgmii_fifo #(
    .TARGET(MAC_TARGET),
    .IODDR_STYLE(MAC_IODDR_STYLE),
    .CLOCK_INPUT_STYLE(MAC_CLK_STYLE),
    .AXIS_DATA_WIDTH(TDATA_WIDTH),
    .TX_FIFO_DEPTH(TX_FIFO_DEPTH),
    .RX_FIFO_DEPTH(RX_FIFO_DEPTH)
  ) ethernet_mac(
    .gtx_clk(gtx_clk),
    .gtx_clk90(gtx90_clk),
    .gtx_rst(!gtx_resetn),

    .logic_clk(axis_clk),
    .logic_rst(!axis_resetn),

    .tx_axis_tdata(tx_axis_to_mac.tdata),
    .tx_axis_tkeep(tx_axis_to_mac.tkeep),
    .tx_axis_tvalid(tx_axis_to_mac.tvalid),
    .tx_axis_tready(tx_axis_to_mac.tready),
    .tx_axis_tlast(tx_axis_to_mac.tlast),

    .rx_axis_tdata(rx_axis_to_ts.tdata),
    .rx_axis_tkeep(rx_axis_to_ts.tkeep),
    .rx_axis_tvalid(rx_axis_to_ts.tvalid),
    .rx_axis_tready(rx_axis_to_ts.tready),
    .rx_axis_tlast(rx_axis_to_ts.tlast),

    .rgmii_rx_clk(rgmii_rx_clk),
    .rgmii_rxd(rgmii_rxd),
    .rgmii_rx_ctl(rgmii_rx_ctl),
    .rgmii_tx_clk(rgmii_tx_clk),
    .rgmii_txd(rgmii_txd),
    .rgmii_tx_ctl(rgmii_tx_ctl),

    .tx_error_underflow(mac_events[TX_ERROR_UNDERFLOW]),
    .tx_fifo_overflow(mac_events[TX_FIFO_OVERFLOW]),
    .tx_fifo_bad_frame(mac_events[TX_FIFO_BAD_FRAME]),
    .tx_fifo_good_frame(mac_events[TX_FIFO_GOOD_FRAME]),
    .rx_error_bad_frame(mac_events[RX_ERROR_BAD_FRAME]),
    .rx_error_bad_fcs(mac_events[RX_ERROR_BAD_FCS]),
    .rx_fifo_overflow(mac_events[RX_FIFO_OVERFLOW]),
    .rx_fifo_bad_frame(mac_events[RX_FIFO_BAD_FRAME]),
    .rx_fifo_good_frame(mac_events[RX_FIFO_GOOD_FRAME]),
    .speed(mac_speed),

    //! MAC configuration now driven by milan_csr (REQ-MAC-01)
    .cfg_ifg(cfg_mac_ifg),
    .cfg_tx_enable(cfg_mac_tx_en),
    .cfg_rx_enable(cfg_mac_rx_en)
  );


endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : milan_top.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-18
  Description : Top-level integration module for the Milan FPGA platform.

                Subsystems:
                - milan_dma_wrapper  : Zynq PS + DMA + AXI interconnect
                - traffic_controller : IEEE 802.1Q CBS-based egress shaper
                - ptp_timestamp      : PTP hardware timestamping (TX + RX)
                - ethernet_mac       : 1G RGMII MAC with TX/RX FIFOs
                - ethernet_counters  : Ethernet event statistics

                TX path: DMA -> Traffic Shaper -> PTP TS -> MAC -> RGMII
                RX path: RGMII -> MAC -> PTP TS -> DMA

  Company     : Kebag Logic
  Project     : Milan FPGA Platform
------------------------------------------------------------------------------
*/

`default_nettype none
`include "ethernet_events.svh"

module milan_top#(
  parameter int TDATA_WIDTH = 64,
  parameter int TX_FIFO_DEPTH = 2048,
  parameter int RX_FIFO_DEPTH = 2048
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
  //! RX path: PTP timestamping output → DMA
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) rx_axis_to_dma();
  //! TX path: DMA output → 802.1Q traffic shaper
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_shaper();
  //! TX path: Traffic shaper output → PTP timestamping core
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_shaper_to_ts();
  //! TX path: PTP timestamping output → MAC
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) tx_axis_to_mac();
  //! PTP timestamp metadata stream: PTP core → DMA (timestamp + seq_id + direction)
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) ts_metadata_axis();


  milan_dma_wrapper milan_wrapper(
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

  traffic_controller_802_1q #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(0)
  ) traffic_controller(
    .clk(axis_clk),
    .resetn(axis_resetn),
    .is_1g_i('d1),

    .s_axis(tx_axis_to_shaper),
    .m_axis(tx_axis_shaper_to_ts)
  );

  ptp_ts_top #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(0),
    .ETH_TYPE(16'hF788)
  ) ptp_timestamp (
    .gtx_clk(gtx_clk),
    .gtx_resetn(gtx_resetn),
    .axis_clk(axis_clk),
    .axis_resetn(axis_resetn),
    
    .s_axis_tx_tdata(tx_axis_shaper_to_ts.tdata),
    .s_axis_tx_tvalid(tx_axis_shaper_to_ts.tvalid),
    .s_axis_tx_tready(tx_axis_shaper_to_ts.tready),
    .s_axis_tx_tlast(tx_axis_shaper_to_ts.tlast),
    .s_axis_tx_tkeep(tx_axis_shaper_to_ts.tkeep),
    
    .m_axis_tx_tdata(tx_axis_to_mac.tdata),
    .m_axis_tx_tvalid(tx_axis_to_mac.tvalid),
    .m_axis_tx_tready(tx_axis_to_mac.tready),
    .m_axis_tx_tlast(tx_axis_to_mac.tlast),
    .m_axis_tx_tkeep(tx_axis_to_mac.tkeep),
    
    .s_axis_rx_tdata(rx_axis_to_ts.tdata),
    .s_axis_rx_tvalid(rx_axis_to_ts.tvalid),
    .s_axis_rx_tready(rx_axis_to_ts.tready),
    .s_axis_rx_tlast(rx_axis_to_ts.tlast),
    .s_axis_rx_tkeep(rx_axis_to_ts.tkeep),
    
    .m_axis_rx_tdata(rx_axis_to_dma.tdata),
    .m_axis_rx_tvalid(rx_axis_to_dma.tvalid),
    .m_axis_rx_tready(rx_axis_to_dma.tready),
    .m_axis_rx_tlast(rx_axis_to_dma.tlast),
    .m_axis_rx_tkeep(rx_axis_to_dma.tkeep),
    
    .ts_m_axis_tdata(ts_metadata_axis.tdata),
    .ts_m_axis_tvalid(ts_metadata_axis.tvalid),
    .ts_m_axis_tready(ts_metadata_axis.tready),
    .ts_m_axis_tlast(ts_metadata_axis.tlast),
    .ts_m_axis_tkeep(ts_metadata_axis.tkeep)
  );


  logic [_ETH_EVENT_COUNTER-1:0] mac_events;
  wire [1:0] speed_w;

  ethernet_events ethernet_counters(
    .clk(axis_clk),
    .resetn(axis_resetn),
    // TODO Add VIO
    .stats_reset(1'b0),
    .events(mac_events)
  );

  eth_mac_1g_rgmii_fifo #(
    .TARGET("XILINX"),
    .IODDR_STYLE("IODDR"),
    .CLOCK_INPUT_STYLE("BUFR"),
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

    //! TODO: status counters to PS
    .tx_error_underflow(mac_events[TX_ERROR_UNDERFLOW]),
    .tx_fifo_overflow(mac_events[TX_FIFO_OVERFLOW]),
    .tx_fifo_bad_frame(mac_events[TX_FIFO_BAD_FRAME]),
    .tx_fifo_good_frame(mac_events[TX_FIFO_GOOD_FRAME]),
    .rx_error_bad_frame(mac_events[RX_ERROR_BAD_FRAME]),
    .rx_error_bad_fcs(mac_events[RX_ERROR_BAD_FCS]),
    .rx_fifo_overflow(mac_events[RX_FIFO_OVERFLOW]),
    .rx_fifo_bad_frame(mac_events[RX_FIFO_BAD_FRAME]),
    .rx_fifo_good_frame(mac_events[RX_FIFO_GOOD_FRAME]),
    .speed(speed_w),

    .cfg_ifg('d12),
    .cfg_tx_enable('d1),
    .cfg_rx_enable('d1)
  );


endmodule

`default_nettype wire
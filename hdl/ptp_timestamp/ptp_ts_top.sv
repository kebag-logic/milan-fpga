/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ptp_ts_top.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-18
  Description : Top-level module for ptp timestamping.

                It includes:

                - Timestamp counter
                - TX and RX timestamping cores
                - Metadata arbitration and buffering

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC

  ------------------------------------------------------------------------------
*/

`default_nettype none

module ptp_ts_top#(
  parameter int TDATA_WIDTH = 64,          //! AXI-Stream data width
  parameter int TS_WIDTH = 64,             //! Timestamp width
  parameter int STEP_SIZE = 8,             //! Step size per clock cycle
  parameter int METADATA_TDATA_WIDTH = 64, //! Metadata output width
  parameter bit BIG_ENDIAN = 0,            //! Endianness for field extraction
  parameter bit [15:0] ETH_TYPE = 'hF788  //! EtherType for PTP
)(

  //! Timestamp clock domain
  input  wire gtx_clk,
  //! Timestamp reset domain
  input  wire gtx_resetn,
  //! AXIS clock domain
  input  wire axis_clk,
  //! AXIS reset domain
  input  wire axis_resetn,

  //! TX AXI-Stream inputs
  input  wire [TDATA_WIDTH-1:0] s_axis_tx_tdata,
  input  wire s_axis_tx_tvalid,
  output wire s_axis_tx_tready,
  input  wire s_axis_tx_tlast,
  input  wire [(TDATA_WIDTH/8)-1:0] s_axis_tx_tkeep,

  //! TX AXI-Stream outputs
  output wire [TDATA_WIDTH-1:0] m_axis_tx_tdata,
  output wire m_axis_tx_tvalid,
  input  wire m_axis_tx_tready,
  output wire m_axis_tx_tlast,
  output wire [(TDATA_WIDTH/8)-1:0] m_axis_tx_tkeep,

  //! RX AXI-Stream inputs
  input  wire [TDATA_WIDTH-1:0] s_axis_rx_tdata,
  input  wire s_axis_rx_tvalid,
  output wire s_axis_rx_tready,
  input  wire s_axis_rx_tlast,
  input  wire [(TDATA_WIDTH/8)-1:0] s_axis_rx_tkeep,

  //! RX AXI-Stream outputs
  output wire [TDATA_WIDTH-1:0] m_axis_rx_tdata,
  output wire m_axis_rx_tvalid,
  input  wire m_axis_rx_tready,
  output wire m_axis_rx_tlast,
  output wire [(TDATA_WIDTH/8)-1:0] m_axis_rx_tkeep,

  output wire [METADATA_TDATA_WIDTH-1:0] ts_m_axis_tdata,
  output wire ts_m_axis_tvalid,
  input  wire ts_m_axis_tready,
  output wire ts_m_axis_tlast,
  output wire [(METADATA_TDATA_WIDTH/8)-1:0] ts_m_axis_tkeep

  //TODO: add DMA engine signals

);

  // ===========================================================================
  //! AXI-Stream Interface Declarations
  // ===========================================================================
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis_tx();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis_rx();

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_tx();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_rx();
  
  axi_stream_if #(.TDATA_WIDTH_P(METADATA_TDATA_WIDTH)) ts_m_axis_tx();
  axi_stream_if #(.TDATA_WIDTH_P(METADATA_TDATA_WIDTH)) ts_m_axis_rx();

  axi_stream_if #(.TDATA_WIDTH_P(METADATA_TDATA_WIDTH)) ts_tx_buffered();
  axi_stream_if #(.TDATA_WIDTH_P(METADATA_TDATA_WIDTH)) ts_rx_buffered();

  axi_stream_if #(.TDATA_WIDTH_P(METADATA_TDATA_WIDTH)) ts_switch_to_fifo();

  //! internal timestamp signal
  wire[TS_WIDTH-1:0] timestamp;

  // ===========================================================================
  // AXI-Stream Assignments
  // ===========================================================================
  assign s_axis_tx.tdata = s_axis_tx_tdata;
  assign s_axis_tx.tvalid = s_axis_tx_tvalid;
  assign s_axis_tx_tready = s_axis_tx.tready;
  assign s_axis_tx.tlast = s_axis_tx_tlast;
  assign s_axis_tx.tkeep = s_axis_tx_tkeep;

  assign s_axis_rx.tdata = s_axis_rx_tdata;
  assign s_axis_rx.tvalid = s_axis_rx_tvalid;
  assign s_axis_rx_tready = s_axis_rx.tready;
  assign s_axis_rx.tlast = s_axis_rx_tlast;
  assign s_axis_rx.tkeep = s_axis_rx_tkeep;

  assign m_axis_tx_tdata = m_axis_tx.tdata;
  assign m_axis_tx_tvalid = m_axis_tx.tvalid;
  assign m_axis_tx.tready = m_axis_tx_tready;
  assign m_axis_tx_tlast = m_axis_tx.tlast;
  assign m_axis_tx_tkeep = m_axis_tx.tkeep;

  assign m_axis_rx_tdata = m_axis_rx.tdata;
  assign m_axis_rx_tvalid = m_axis_rx.tvalid;
  assign m_axis_rx.tready = m_axis_rx_tready;
  assign m_axis_rx_tlast = m_axis_rx.tlast;
  assign m_axis_rx_tkeep = m_axis_rx.tkeep;


  // ---------------------------------------------------------------------------
  //! ts_counter: 64-bit counter for time stamping packets
  // ---------------------------------------------------------------------------

  timestamp_counter #(
    .COUNTER_WIDTH(TS_WIDTH),
    .STEP_SIZE(STEP_SIZE)
  )
  ts_counter(
    .clk(gtx_clk),
    .resetn(gtx_resetn),
    .timestamp_out(timestamp)
  );

  // ---------------------------------------------------------------------------
  //! TX packets timestamping
  // ---------------------------------------------------------------------------
  ptp_ts_core #(
    .IS_TX(1),
    .TDATA_WIDTH(TDATA_WIDTH),
    .TS_WIDTH(TS_WIDTH),
    .METADATA_TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(BIG_ENDIAN),
    .ETH_TYPE(ETH_TYPE)
  )
  ptp_ts_tx(
    .ts_src_clk(gtx_clk),
    .ts_src_resetn(gtx_resetn),

    .ts_dst_clk(axis_clk),
    .ts_dst_resetn(axis_resetn),
    .ts_in(timestamp),

    .s_axis(s_axis_tx),
    .m_axis(m_axis_tx),
    .ts_m_axis(ts_m_axis_tx)
  );

  // ---------------------------------------------------------------------------
  //! RX packets timestamping
  // ---------------------------------------------------------------------------
  ptp_ts_core #(
    .IS_TX(0),
    .TDATA_WIDTH(TDATA_WIDTH),
    .TS_WIDTH(TS_WIDTH),
    .METADATA_TDATA_WIDTH(TDATA_WIDTH),
    .BIG_ENDIAN(BIG_ENDIAN),
    .ETH_TYPE(ETH_TYPE)
  )
  ptp_ts_rx(
    .ts_src_clk(gtx_clk),
    .ts_src_resetn(gtx_resetn),

    .ts_dst_clk(axis_clk),
    .ts_dst_resetn(axis_resetn),
    .ts_in(timestamp),

    .s_axis(s_axis_rx),
    .m_axis(m_axis_rx),
    .ts_m_axis(ts_m_axis_rx)
  );

  // ===========================================================================
  // TX Timestamp Buffer FIFO (Pre-Switch)
  // ===========================================================================
  xpm_fifo_axis #(
    .CLOCKING_MODE("common_clock"),
    .FIFO_DEPTH(16),
    .FIFO_MEMORY_TYPE("distributed"),
    .PACKET_FIFO("false"),
    .TDATA_WIDTH(METADATA_TDATA_WIDTH)
  )
  tx_ts_buffer(
   .s_aclk(axis_clk),
   .s_aresetn(axis_resetn),
 
   .s_axis_tdata(ts_m_axis_tx.tdata),
   .s_axis_tkeep(ts_m_axis_tx.tkeep),
   .s_axis_tlast(ts_m_axis_tx.tlast),
   .s_axis_tready(ts_m_axis_tx.tready),
   .s_axis_tvalid(ts_m_axis_tx.tvalid),
 
   .m_axis_tdata(ts_tx_buffered.tdata),
   .m_axis_tkeep(ts_tx_buffered.tkeep),
   .m_axis_tlast(ts_tx_buffered.tlast),
   .m_axis_tready(ts_tx_buffered.tready),
   .m_axis_tvalid(ts_tx_buffered.tvalid)
  );

  // ===========================================================================
  // RX Timestamp Buffer FIFO (Pre-Switch)
  // ===========================================================================
  xpm_fifo_axis #(
    .CLOCKING_MODE("common_clock"),
    .FIFO_DEPTH(16),
    .FIFO_MEMORY_TYPE("distributed"),
    .PACKET_FIFO("false"),
    .TDATA_WIDTH(METADATA_TDATA_WIDTH)
  )
  rx_ts_buffer(
   .s_aclk(axis_clk),
   .s_aresetn(axis_resetn),
 
   .s_axis_tdata(ts_m_axis_rx.tdata),
   .s_axis_tkeep(ts_m_axis_rx.tkeep),
   .s_axis_tlast(ts_m_axis_rx.tlast),
   .s_axis_tready(ts_m_axis_rx.tready),
   .s_axis_tvalid(ts_m_axis_rx.tvalid),
 
   .m_axis_tdata(ts_rx_buffered.tdata),
   .m_axis_tkeep(ts_rx_buffered.tkeep),
   .m_axis_tlast(ts_rx_buffered.tlast),
   .m_axis_tready(ts_rx_buffered.tready),
   .m_axis_tvalid(ts_rx_buffered.tvalid)
  );

  // ===========================================================================
  //! AXIS mux to combine buffered TX and RX streams
  // ===========================================================================
  axis_mux_rr_2in_1out #(
  .TDATA_WIDTH(METADATA_TDATA_WIDTH)
  ) axis_tx_rx_ts_switch_rr(
    .clk(axis_clk),
    .rst_n(axis_resetn),

    .s0_tdata(ts_rx_buffered.tdata),
    .s0_tvalid(ts_rx_buffered.tvalid),
    .s0_tready(ts_rx_buffered.tready),
    .s0_tlast(ts_rx_buffered.tlast),
    .s0_tkeep(ts_rx_buffered.tkeep),

    .s1_tdata(ts_tx_buffered.tdata),
    .s1_tvalid(ts_tx_buffered.tvalid),
    .s1_tready(ts_tx_buffered.tready),
    .s1_tlast(ts_tx_buffered.tlast),
    .s1_tkeep(ts_tx_buffered.tkeep),

    .m_tdata(ts_switch_to_fifo.tdata),
    .m_tvalid(ts_switch_to_fifo.tvalid),
    .m_tready(ts_switch_to_fifo.tready),
    .m_tlast(ts_switch_to_fifo.tlast),
    .m_tkeep(ts_switch_to_fifo.tkeep)
);

  // ---------------------------------------------------------------------------
  //! AXIS fifo to store timestamp before DMA engine
  // ---------------------------------------------------------------------------
  xpm_fifo_axis #(
    .CLOCKING_MODE("common_clock"),
    .FIFO_DEPTH(16),
    .FIFO_MEMORY_TYPE("distributed"),
    .PACKET_FIFO("false"),
    .TDATA_WIDTH(METADATA_TDATA_WIDTH)
  )
  ts_buffer_to_ps(
   .s_aclk(axis_clk),
   .s_aresetn(axis_resetn),
 
   .s_axis_tdata(ts_switch_to_fifo.tdata),
   .s_axis_tkeep(ts_switch_to_fifo.tkeep),
   .s_axis_tlast(ts_switch_to_fifo.tlast),
   .s_axis_tready(ts_switch_to_fifo.tready),
   .s_axis_tvalid(ts_switch_to_fifo.tvalid),
 
   .m_axis_tdata(ts_m_axis_tdata),
   .m_axis_tkeep(ts_m_axis_tkeep),
   .m_axis_tlast(ts_m_axis_tlast),
   .m_axis_tready(ts_m_axis_tready), //m_axis_fifo_to_dma.tready),
   .m_axis_tvalid(ts_m_axis_tvalid)
  );

  // ---------------------------------------------------------------------------
  //! DMA engine to sent timestamp metadata info to PS
  // ---------------------------------------------------------------------------

endmodule

`default_nettype wire

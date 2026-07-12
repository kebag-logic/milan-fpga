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
  parameter int INCR_WIDTH = 32,           //! PHC increment/addend width
  parameter int FRAC_WIDTH = 24,           //! PHC fractional-ns bits: PTP_INCR is Q8.24
  parameter int METADATA_TDATA_WIDTH = 64, //! Metadata output width
  parameter bit BIG_ENDIAN = 0,            //! Endianness for field extraction
  parameter bit [15:0] ETH_TYPE = 'hF788  //! EtherType for PTP
)(

  //! Timestamp clock domain (PHC clock — fixed 125 MHz recommended, REQ-PTP-07)
  input  wire gtx_clk,
  //! Timestamp reset domain
  input  wire gtx_resetn,
  //! AXIS clock domain
  input  wire axis_clk,
  //! AXIS reset domain
  input  wire axis_resetn,

  //! --- PTP hardware clock control (from milan_csr, axis_clk domain, REQ-PTP-01..04) ---
  input  wire                 i_ptp_enable,       //! PHC enable
  input  wire [INCR_WIDTH-1:0] i_ptp_incr,        //! Nominal per-tick increment, Q(INT).FRAC ns
  input  wire [INCR_WIDTH-1:0] i_ptp_adj,         //! Signed adjfine addend, Q(INT).FRAC ns
  input  wire [TS_WIDTH-1:0]  i_ptp_tod_wr,       //! settime target time-of-day, ns
  input  wire [TS_WIDTH-1:0]  i_ptp_offset,       //! adjtime signed delta, ns
  input  wire                 i_ptp_cmd_load,     //! settime apply strobe (axis_clk)
  input  wire                 i_ptp_cmd_adjust,   //! adjtime apply strobe (axis_clk)
  input  wire                 i_ptp_cmd_snapshot, //! gettime apply strobe (axis_clk)
  output wire [TS_WIDTH-1:0]  o_ptp_tod_rd,       //! gettime result, ns (axis_clk)
  output wire                 o_ptp_tod_rd_valid, //! gettime result valid (1 axis_clk pulse)
  output wire                 o_tx_ts_ready,      //! TX egress timestamp available (IRQ pulse, axis_clk)
  output wire [TS_WIDTH-1:0]  o_ptp_now,          //! live counter value (gtx_clk domain; on the
                                                  //! Arty gtx==cd_milan so the AAF talker reads it
                                                  //! directly — revisit for a 125 MHz gtx part)

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

  //! PHC control signals synchronised into the gtx_clk (PHC) domain.
  wire                  ptp_enable_ts;
  wire [INCR_WIDTH-1:0] ptp_incr_ts;
  wire [INCR_WIDTH-1:0] ptp_adj_ts;
  wire [TS_WIDTH-1:0]   ptp_tod_wr_ts;
  wire                  ptp_cmd_load_ts;
  wire [TS_WIDTH-1:0]   ptp_offset_ts;
  wire                  ptp_cmd_adjust_ts;
  wire                  ptp_cmd_snapshot_ts;
  wire [TS_WIDTH-1:0]   ptp_tod_snapshot_ts;
  wire                  ptp_tod_snapshot_valid_ts;

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

  //! CSR -> PHC clock-domain crossing (axis_clk -> gtx_clk + snapshot return).
  ptp_csr_sync #(
    .TS_WIDTH(TS_WIDTH),
    .INCR_WIDTH(INCR_WIDTH)
  ) ptp_sync (
    .aclk           (axis_clk),
    .aresetn        (axis_resetn),
    .a_enable       (i_ptp_enable),
    .a_incr         (i_ptp_incr),
    .a_adj          (i_ptp_adj),
    .a_tod_wr       (i_ptp_tod_wr),
    .a_offset       (i_ptp_offset),
    .a_cmd_load     (i_ptp_cmd_load),
    .a_cmd_adjust   (i_ptp_cmd_adjust),
    .a_cmd_snapshot (i_ptp_cmd_snapshot),
    .a_tod_rd       (o_ptp_tod_rd),
    .a_tod_rd_valid (o_ptp_tod_rd_valid),

    .ts_clk         (gtx_clk),
    .ts_resetn      (gtx_resetn),
    .t_enable       (ptp_enable_ts),
    .t_incr         (ptp_incr_ts),
    .t_adj          (ptp_adj_ts),
    .t_tod_wr       (ptp_tod_wr_ts),
    .t_cmd_load     (ptp_cmd_load_ts),
    .t_offset       (ptp_offset_ts),
    .t_cmd_adjust   (ptp_cmd_adjust_ts),
    .t_cmd_snapshot (ptp_cmd_snapshot_ts),
    .t_tod_snapshot       (ptp_tod_snapshot_ts),
    .t_tod_snapshot_valid (ptp_tod_snapshot_valid_ts)
  );

  timestamp_counter #(
    .COUNTER_WIDTH(TS_WIDTH),
    .INCR_WIDTH(INCR_WIDTH),
    .FRAC_WIDTH(FRAC_WIDTH)
  )
  ts_counter(
    .clk(gtx_clk),
    .resetn(gtx_resetn),
    .enable_i(ptp_enable_ts),
    .incr_i(ptp_incr_ts),
    .adj_i(ptp_adj_ts),
    .tod_wr_i(ptp_tod_wr_ts),
    .cmd_load_i(ptp_cmd_load_ts),
    .offset_i(ptp_offset_ts),
    .cmd_adjust_i(ptp_cmd_adjust_ts),
    .cmd_snapshot_i(ptp_cmd_snapshot_ts),
    .timestamp_out(timestamp),
    .tod_snapshot_o(ptp_tod_snapshot_ts),
    .tod_snapshot_valid_o(ptp_tod_snapshot_valid_ts)
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

  //! TX egress-timestamp ready pulse (REQ-PTP-04): assert for one axis_clk cycle
  //! when a completed TX timestamp record (last metadata beat) is accepted into
  //! the TX ts buffer. milan_csr latches this into IRQ_STATUS[0].
  reg tx_ts_ready_r;
  always_ff @(posedge axis_clk) begin : tx_ts_ready_pulse
    if (!axis_resetn)
      tx_ts_ready_r <= 1'b0;
    else
      tx_ts_ready_r <= ts_m_axis_tx.tvalid && ts_m_axis_tx.tready && ts_m_axis_tx.tlast;
  end
  assign o_tx_ts_ready = tx_ts_ready_r;

  // ===========================================================================
  // TX Timestamp Buffer FIFO (Pre-Switch)
  // ===========================================================================
  //! Open-core AXIS FIFO (Forencich verilog-axis) — replaces xpm_fifo_axis
  //! (docs/integration/OPEN_SOURCE_MIGRATION.md Track 1.2). Common-clock, non-packet.
  axis_fifo #(
    .DEPTH(16),
    .DATA_WIDTH(METADATA_TDATA_WIDTH),
    .KEEP_ENABLE(1), .KEEP_WIDTH(METADATA_TDATA_WIDTH/8),
    .LAST_ENABLE(1), .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0), .FRAME_FIFO(0)
  )
  tx_ts_buffer(
   .clk(axis_clk),
   .rst(~axis_resetn),

   .s_axis_tdata(ts_m_axis_tx.tdata),
   .s_axis_tkeep(ts_m_axis_tx.tkeep),
   .s_axis_tvalid(ts_m_axis_tx.tvalid),
   .s_axis_tready(ts_m_axis_tx.tready),
   .s_axis_tlast(ts_m_axis_tx.tlast),
   .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),

   .m_axis_tdata(ts_tx_buffered.tdata),
   .m_axis_tkeep(ts_tx_buffered.tkeep),
   .m_axis_tvalid(ts_tx_buffered.tvalid),
   .m_axis_tready(ts_tx_buffered.tready),
   .m_axis_tlast(ts_tx_buffered.tlast),
   .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),

   .pause_req(1'b0), .pause_ack(),
   .status_depth(), .status_depth_commit(),
   .status_overflow(), .status_bad_frame(), .status_good_frame()
  );

  // ===========================================================================
  // RX Timestamp Buffer FIFO (Pre-Switch)
  // ===========================================================================
  //! Open-core AXIS FIFO (Forencich verilog-axis) — replaces xpm_fifo_axis.
  axis_fifo #(
    .DEPTH(16),
    .DATA_WIDTH(METADATA_TDATA_WIDTH),
    .KEEP_ENABLE(1), .KEEP_WIDTH(METADATA_TDATA_WIDTH/8),
    .LAST_ENABLE(1), .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0), .FRAME_FIFO(0)
  )
  rx_ts_buffer(
   .clk(axis_clk),
   .rst(~axis_resetn),

   .s_axis_tdata(ts_m_axis_rx.tdata),
   .s_axis_tkeep(ts_m_axis_rx.tkeep),
   .s_axis_tvalid(ts_m_axis_rx.tvalid),
   .s_axis_tready(ts_m_axis_rx.tready),
   .s_axis_tlast(ts_m_axis_rx.tlast),
   .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),

   .m_axis_tdata(ts_rx_buffered.tdata),
   .m_axis_tkeep(ts_rx_buffered.tkeep),
   .m_axis_tvalid(ts_rx_buffered.tvalid),
   .m_axis_tready(ts_rx_buffered.tready),
   .m_axis_tlast(ts_rx_buffered.tlast),
   .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),

   .pause_req(1'b0), .pause_ack(),
   .status_depth(), .status_depth_commit(),
   .status_overflow(), .status_bad_frame(), .status_good_frame()
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
  //! Open-core AXIS FIFO (Forencich verilog-axis) — replaces xpm_fifo_axis.
  axis_fifo #(
    .DEPTH(16),
    .DATA_WIDTH(METADATA_TDATA_WIDTH),
    .KEEP_ENABLE(1), .KEEP_WIDTH(METADATA_TDATA_WIDTH/8),
    .LAST_ENABLE(1), .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0), .FRAME_FIFO(0)
  )
  ts_buffer_to_ps(
   .clk(axis_clk),
   .rst(~axis_resetn),

   .s_axis_tdata(ts_switch_to_fifo.tdata),
   .s_axis_tkeep(ts_switch_to_fifo.tkeep),
   .s_axis_tvalid(ts_switch_to_fifo.tvalid),
   .s_axis_tready(ts_switch_to_fifo.tready),
   .s_axis_tlast(ts_switch_to_fifo.tlast),
   .s_axis_tid('0), .s_axis_tdest('0), .s_axis_tuser('0),

   .m_axis_tdata(ts_m_axis_tdata),
   .m_axis_tkeep(ts_m_axis_tkeep),
   .m_axis_tvalid(ts_m_axis_tvalid),
   .m_axis_tready(ts_m_axis_tready),
   .m_axis_tlast(ts_m_axis_tlast),
   .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),

   .pause_req(1'b0), .pause_ack(),
   .status_depth(), .status_depth_commit(),
   .status_overflow(), .status_bad_frame(), .status_good_frame()
  );

  // ---------------------------------------------------------------------------
  //! DMA engine to sent timestamp metadata info to PS
  // ---------------------------------------------------------------------------

  assign o_ptp_now = timestamp;

endmodule

`default_nettype wire
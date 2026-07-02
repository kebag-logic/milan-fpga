/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Flat-port wrapper around traffic_classifier (which uses axi_stream_if ports)
 * so the Verilator harness can drive it. Also proves traffic_classifier now
 * Verilates end-to-end after the xpm_fifo_axis -> axis_fifo (Forencich) swap.
 */
`default_nettype none

module classifier_wrap #(
  parameter int TDATA_WIDTH = 64,
  parameter int NUMBER_OF_QUEUES = 4,
  parameter int TDEST_WIDTH = (NUMBER_OF_QUEUES <= 1) ? 1 : $clog2(NUMBER_OF_QUEUES)
)(
  input  wire                     clk,
  input  wire                     resetn,
  input  wire                     use_pcp_i,
  input  wire                     dmac_check_i,
  input  wire [2:0]               default_pcp_i,
  input  wire [23:0]              pcp_tc_map_i,
  input  wire [23:0]              prio_regen_i,
  input  wire [31:0]              tc_queue_map_i,
  // slave in
  input  wire [TDATA_WIDTH-1:0]   s_tdata,
  input  wire [TDATA_WIDTH/8-1:0] s_tkeep,
  input  wire                     s_tvalid,
  input  wire                     s_tlast,
  output wire                     s_tready,
  // master out
  output wire [TDATA_WIDTH-1:0]   m_tdata,
  output wire [TDATA_WIDTH/8-1:0] m_tkeep,
  output wire                     m_tvalid,
  output wire                     m_tlast,
  output wire [TDEST_WIDTH-1:0]   m_tdest,
  input  wire                     m_tready
);

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) s_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) m_axis();

  assign s_axis.tdata  = s_tdata;
  assign s_axis.tkeep  = s_tkeep;
  assign s_axis.tvalid = s_tvalid;
  assign s_axis.tlast  = s_tlast;
  assign s_tready      = s_axis.tready;

  assign m_tdata  = m_axis.tdata;
  assign m_tkeep  = m_axis.tkeep;
  assign m_tvalid = m_axis.tvalid;
  assign m_tlast  = m_axis.tlast;
  assign m_tdest  = m_axis.tdest;
  assign m_axis.tready = m_tready;

  traffic_classifier #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES)
  ) dut (
    .clk(clk),
    .resetn(resetn),
    .use_pcp_i(use_pcp_i),
    .dmac_check_i(dmac_check_i),
    .default_pcp_i(default_pcp_i),
    .pcp_tc_map_i(pcp_tc_map_i),
    .prio_regen_i(prio_regen_i),
    .tc_queue_map_i(tc_queue_map_i),
    .s_axis(s_axis),
    .m_axis(m_axis)
  );

endmodule

`default_nettype wire

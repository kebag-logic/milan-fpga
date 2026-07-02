/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Flat-port wrapper around traffic_controller_802_1q (classifier + queues + CBS
 * shaper) for the T1.5 end-to-end datapath harness. Proves the whole de-Xilinx'd
 * TSN TX datapath (Forencich axis_fifo/demux/arb_mux + open RTL) Verilates and
 * works as one pipeline.
 */
`default_nettype none

module datapath_wrap #(
  parameter int TDATA_WIDTH = 64,
  parameter int NUMBER_OF_QUEUES = 4,
  parameter int TDEST_WIDTH = (NUMBER_OF_QUEUES <= 1) ? 1 : $clog2(NUMBER_OF_QUEUES)
)(
  input  wire                          clk,
  input  wire                          resetn,
  input  wire                          is_1g_i,
  // classifier config
  input  wire                          cls_use_pcp_i,
  input  wire                          cls_dmac_check_i,
  input  wire [2:0]                    cls_default_pcp_i,
  input  wire [23:0]                   cls_pcp_tc_map_i,
  input  wire [23:0]                   cls_prio_regen_i,
  input  wire [31:0]                   cls_tc_queue_map_i,
  // CBS config (packed per queue)
  input  wire [32*NUMBER_OF_QUEUES-1:0] cbs_idle_slope_i,
  input  wire [32*NUMBER_OF_QUEUES-1:0] cbs_hi_credit_i,
  input  wire [32*NUMBER_OF_QUEUES-1:0] cbs_lo_credit_i,
  input  wire [NUMBER_OF_QUEUES-1:0]    cbs_shaped_i,
  // AXIS in
  input  wire [TDATA_WIDTH-1:0]        s_tdata,
  input  wire [TDATA_WIDTH/8-1:0]      s_tkeep,
  input  wire                          s_tvalid,
  input  wire                          s_tlast,
  output wire                          s_tready,
  // AXIS out (shaped)
  output wire [TDATA_WIDTH-1:0]        m_tdata,
  output wire [TDATA_WIDTH/8-1:0]      m_tkeep,
  output wire                          m_tvalid,
  output wire                          m_tlast,
  output wire [TDEST_WIDTH-1:0]        m_tdest,
  input  wire                          m_tready
);

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) s_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P(TDEST_WIDTH)) m_axis();

  assign s_axis.tdata = s_tdata; assign s_axis.tkeep = s_tkeep;
  assign s_axis.tvalid = s_tvalid; assign s_axis.tlast = s_tlast; assign s_tready = s_axis.tready;
  assign s_axis.tdest = '0;
  assign m_tdata = m_axis.tdata; assign m_tkeep = m_axis.tkeep;
  assign m_tvalid = m_axis.tvalid; assign m_tlast = m_axis.tlast; assign m_tdest = m_axis.tdest;
  assign m_axis.tready = m_tready;

  traffic_controller_802_1q #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NUMBER_OF_QUEUES)
  ) dut (
    .clk(clk), .resetn(resetn), .is_1g_i(is_1g_i),
    .cls_use_pcp_i(cls_use_pcp_i), .cls_dmac_check_i(cls_dmac_check_i),
    .cls_default_pcp_i(cls_default_pcp_i), .cls_pcp_tc_map_i(cls_pcp_tc_map_i),
    .cls_prio_regen_i(cls_prio_regen_i), .cls_tc_queue_map_i(cls_tc_queue_map_i),
    .cbs_idle_slope_i(cbs_idle_slope_i), .cbs_hi_credit_i(cbs_hi_credit_i),
    .cbs_lo_credit_i(cbs_lo_credit_i), .cbs_shaped_i(cbs_shaped_i),
    .s_axis(s_axis), .m_axis(m_axis)
  );

endmodule

`default_nettype wire

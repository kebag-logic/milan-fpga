/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Verilator wrapper for traffic_controller_802_1q — the full classify -> queue ->
 * CBS chain. Flattens the AXIS interface ports so sim_main.cpp can drive
 * back-to-back frames and measure per-frame byte integrity at the egress. See
 * README.md / docs/findings/CBS_DATAPATH_BUG.md: this reproduces an OPEN datapath bug.
 */
`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;
`default_nettype none

module controller_rate_wrap #(
  parameter int TDATA_WIDTH = 64,
  parameter int NQ          = 4
)(
  input  wire clk,
  input  wire resetn,
  input  wire is_1g_i,
  input  wire        cls_use_pcp_i,
  input  wire [2:0]  cls_default_pcp_i,
  input  wire [23:0] cls_pcp_tc_map_i,
  input  wire [23:0] cls_prio_regen_i,
  input  wire [31:0] cls_tc_queue_map_i,
  input  wire [32*NQ-1:0] cbs_idle_slope_i,
  input  wire [32*NQ-1:0] cbs_hi_credit_i,
  input  wire [32*NQ-1:0] cbs_lo_credit_i,
  input  wire [NQ-1:0]    cbs_shaped_i,
  input  wire [TDATA_WIDTH-1:0]     s_tdata,
  input  wire [(TDATA_WIDTH/8)-1:0] s_tkeep,
  input  wire                       s_tvalid,
  input  wire                       s_tlast,
  input  wire                       m_tready,
  output wire                       s_tready,
  output wire [TDATA_WIDTH-1:0]     m_tdata,
  output wire [(TDATA_WIDTH/8)-1:0] m_tkeep,
  output wire                       m_tvalid,
  output wire                       m_tlast,
  output wire [1:0]                 m_tdest,
  // classifier tdest-sideband state probes (XMR)
  output wire [5:0] p_tq_wr,
  output wire [5:0] p_tq_rd,
  output wire       p_tq_pushed,
  output wire       p_tq_empty,
  output wire       p_fifo_v,
  output wire [3:0] p_grant,
  output wire [3:0] p_hasdata,
  output wire [3:0] p_allow,
  output wire       p_hold,
  output wire [1:0] p_active,
  output wire [10:0] p_dep0,
  output wire [10:0] p_dep1,
  output wire       p_q2s_v2, output wire p_q2s_r2
);
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P($clog2(NQ))) s_if();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P($clog2(NQ))) m_if();
  assign s_if.tdata = s_tdata; assign s_if.tkeep = s_tkeep;
  assign s_if.tvalid = s_tvalid; assign s_if.tlast = s_tlast; assign s_if.tdest = '0;
  assign s_tready = s_if.tready;
  assign m_tdata = m_if.tdata; assign m_tkeep = m_if.tkeep;
  assign m_tvalid = m_if.tvalid; assign m_tlast = m_if.tlast;
  assign m_if.tready = m_tready;
  assign p_tq_wr     = dut.classifier.tq_wr;
  assign p_tq_rd     = dut.classifier.tq_rd;
  assign p_tq_pushed = dut.classifier.tq_pushed;
  assign p_tq_empty  = dut.classifier.tq_empty;
  assign p_fifo_v    = dut.classifier.m_axis_fifo.tvalid;
  assign p_grant   = dut.traffic_shaper.grant_queue_o;
  assign p_hasdata = dut.buffer_queues.queue_has_data_o;
  assign p_allow   = dut.traffic_shaper.allow_transmit;
  assign p_hold    = dut.traffic_shaper.hold_grant;
  assign p_active  = dut.traffic_shaper.active_queue;
  assign p_dep0    = dut.buffer_queues.fifo_gen[0].depth;
  assign p_dep1    = dut.buffer_queues.fifo_gen[1].depth;
  assign p_q2s_v2  = dut.queue_to_shaper.tvalid;
  assign p_q2s_r2  = dut.queue_to_shaper.tready;

  traffic_controller_802_1q #(
    .TDATA_WIDTH(TDATA_WIDTH), .BIG_ENDIAN(0), .NUMBER_OF_QUEUES(NQ)
  ) dut (
    .clk(clk), .resetn(resetn), .is_1g_i(is_1g_i),
    .cls_use_pcp_i(cls_use_pcp_i), .cls_dmac_check_i(1'b0),
    .cls_default_pcp_i(cls_default_pcp_i), .cls_pcp_tc_map_i(cls_pcp_tc_map_i),
    .cls_prio_regen_i(cls_prio_regen_i), .cls_tc_queue_map_i(cls_tc_queue_map_i),
    .cbs_idle_slope_i(cbs_idle_slope_i), .cbs_hi_credit_i(cbs_hi_credit_i),
    .cbs_lo_credit_i(cbs_lo_credit_i), .cbs_shaped_i(cbs_shaped_i),
    .s_axis(s_if), .m_axis(m_if)
  );
endmodule
`default_nettype wire

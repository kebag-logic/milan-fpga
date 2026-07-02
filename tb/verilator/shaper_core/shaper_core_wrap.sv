/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Verilator verification wrapper for traffic_shaping_core (802.1Qav multi-queue
 * arbiter + per-queue CBS). Flattens the AXI-Stream interface ports to plain
 * signals and cross-module-references each queue's CBS credit so the C++ harness
 * (sim_main.cpp) can check grant exclusivity, tlast-held grants, strict-priority
 * ordering, the shaped/unshaped bypass and credit depletion.
 */

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module shaper_core_wrap #(
  parameter int TDATA_WIDTH = 64,      //! AXI-Stream data width
  parameter int NQ          = 4        //! Number of queues
)(
  input  wire            clk,          //! Clock
  input  wire            resetn,       //! Active-low synchronous reset
  input  wire [NQ-1:0]   queue_has_data_i, //! Per-queue data-available
  input  wire            is_1g_i,      //! Link rate select

  input  wire [32*NQ-1:0] cbs_idle_slope_i, //! Per-queue idleSlope (bits/s)
  input  wire [32*NQ-1:0] cbs_hi_credit_i,  //! Per-queue hiCredit (signed bytes)
  input  wire [32*NQ-1:0] cbs_lo_credit_i,  //! Per-queue loCredit (signed bytes)
  input  wire [NQ-1:0]    cbs_shaped_i,     //! Per-queue shaped-enable

  // flattened s_axis (stimulus) / m_axis (drain) handshake
  input  wire [TDATA_WIDTH-1:0]     s_tdata,   //! Stimulus tdata
  input  wire [(TDATA_WIDTH/8)-1:0] s_tkeep,   //! Stimulus tkeep (byte count = ones)
  input  wire                       s_tvalid,  //! Stimulus tvalid
  input  wire                       s_tlast,   //! Stimulus tlast (packet boundary)
  input  wire                       m_tready,  //! Downstream ready

  output wire                       s_tready,  //! Stimulus ready (= m_tready)
  output wire                       m_tvalid,  //! Egress valid (= s_tvalid)
  output wire                       m_tlast,   //! Egress tlast
  output wire [NQ-1:0]              grant_o,   //! One-hot grant

  output wire signed [47:0]         dbg_credit0, //! Queue-0 CBS credit (Q16)
  output wire signed [47:0]         dbg_credit1, //! Queue-1 CBS credit (Q16)
  output wire signed [47:0]         dbg_credit2, //! Queue-2 CBS credit (Q16)
  output wire signed [47:0]         dbg_credit3, //! Queue-3 CBS credit (Q16)
  output wire [NQ-1:0]             dbg_allow    //! Per-queue allow_transmit
);

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P($clog2(NQ))) s_if();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH), .TDEST_WIDTH_P($clog2(NQ))) m_if();

  assign s_if.tdata  = s_tdata;
  assign s_if.tkeep  = s_tkeep;
  assign s_if.tvalid = s_tvalid;
  assign s_if.tlast  = s_tlast;
  assign s_if.tdest  = '0;
  assign s_tready    = s_if.tready;

  assign m_if.tready = m_tready;
  assign m_tvalid    = m_if.tvalid;
  assign m_tlast     = m_if.tlast;

  traffic_shaping_core #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .NUMBER_OF_QUEUES(NQ)
  ) u_core (
    .clk               (clk),
    .resetn            (resetn),
    .queue_has_data_i  (queue_has_data_i),
    .is_1g_i           (is_1g_i),
    .cbs_idle_slope_i  (cbs_idle_slope_i),
    .cbs_hi_credit_i   (cbs_hi_credit_i),
    .cbs_lo_credit_i   (cbs_lo_credit_i),
    .cbs_shaped_i      (cbs_shaped_i),
    .grant_queue_o     (grant_o),
    .s_axis            (s_if),
    .m_axis            (m_if)
  );

  // XMR into the per-queue CBS instances (read-only observability).
  assign dbg_credit0 = u_core.gen_cbs[0].u_cbs.credit;
  assign dbg_credit1 = u_core.gen_cbs[1].u_cbs.credit;
  assign dbg_credit2 = u_core.gen_cbs[2].u_cbs.credit;
  assign dbg_credit3 = u_core.gen_cbs[3].u_cbs.credit;
  assign dbg_allow   = u_core.allow_transmit;

endmodule

`default_nettype wire

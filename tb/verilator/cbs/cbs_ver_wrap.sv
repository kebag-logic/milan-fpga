/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Verilator verification wrapper for credit_based_shaper.
 *
 * Purpose: instantiate the *unmodified* DUT and expose its internal
 * fixed-point state (credit + per-cycle/per-byte slope terms) via
 * cross-module references so the C++ harness (sim_main.cpp) can check the
 * arithmetic cycle-by-cycle against an independent reference model.
 *
 * The shaper configuration (idleSlope / hiCredit / loCredit / shaped-enable)
 * is now runtime, so those are wrapper input ports too and the harness can
 * reprogram the DUT mid-run to verify live reconfiguration and the strict-
 * priority bypass.
 */

`default_nettype none

module cbs_ver_wrap #(
  parameter int CLK_FREQ_HZ = 100_000_000  //! CBS clock frequency, Hz (constant divisor)
)(
  input  wire        clk,               //! Clock (CBS runs in the axis_clk domain)
  input  wire        resetn,            //! Active-low synchronous reset

  input  wire        shaped_i,          //! 1 = apply CBS; 0 = strict priority
  input  wire [31:0] idle_slope_i,      //! idleSlope for current link rate, bits/s
  input  wire signed [31:0] hi_credit_i,//! hiCredit clamp, signed bytes
  input  wire signed [31:0] lo_credit_i,//! loCredit clamp, signed bytes

  input  wire        queue_has_data_i,  //! Queue has frames waiting to send
  input  wire        is_transmitting_i, //! This queue is actively transmitting
  input  wire        is_1g_i,           //! Link rate select: 1 = 1 Gb/s, 0 = 100 Mb/s
  input  wire        is_granted_i,      //! This queue currently holds the grant
  input  wire [15:0] bytes_sent_i,      //! Bytes transmitted this cycle (tkeep ones)

  output wire        allow_transmit_o,  //! Credit >= 0 (or unshaped): transmission eligible

  // --- verification-only observability (cross-module refs into the DUT) ---
  output wire signed [47:0] dbg_credit,               //! DUT internal Q16 credit
  output wire signed [47:0] dbg_idle_slope_per_cycle, //! DUT idle_slope_per_cycle term
  output wire signed [47:0] dbg_send_slope_per_byte,  //! DUT send_slope_per_byte term
  output wire signed [47:0] dbg_send_delta,           //! DUT registered send delta
  output wire signed [47:0] dbg_credit_add_idle       //! DUT registered idle increment
);

  credit_based_shaper #(
    .CLK_FREQ_HZ(CLK_FREQ_HZ)
  ) u_cbs (
    .clk               (clk),
    .resetn            (resetn),
    .shaped_i          (shaped_i),
    .idle_slope_i      (idle_slope_i),
    .hi_credit_i       (hi_credit_i),
    .lo_credit_i       (lo_credit_i),
    .queue_has_data_i  (queue_has_data_i),
    .is_transmitting_i (is_transmitting_i),
    .is_1g_i           (is_1g_i),
    .is_granted_i      (is_granted_i),
    .bytes_sent_i      (bytes_sent_i),
    .allow_transmit_o  (allow_transmit_o)
  );

  // Downward cross-module references to internal DUT state (read-only).
  // The slope taps observe the ENGINE-COMMITTED registers (the values the
  // credit datapath actually consumes), not a combinational cone: since the
  // sequential slope engine, per-cycle comb slope wires no longer exist.
  assign dbg_credit               = u_cbs.credit;
  assign dbg_idle_slope_per_cycle = u_cbs.idle_slope_per_cycle_r;
  assign dbg_send_slope_per_byte  = u_cbs.send_slope_per_byte_r;
  assign dbg_send_delta           = u_cbs.send_delta;
  assign dbg_credit_add_idle      = u_cbs.credit_add_idle;

endmodule

`default_nettype wire

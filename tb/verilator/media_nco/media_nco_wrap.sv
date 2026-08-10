/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : media_nco_wrap.sv
  Author      : Kebag Logic

  Date        : 2026-08-10
  Description : Verilator wrap for KL_media_nco. Two instances at the two
                datapath clocks the project actually ships (AX7101 100 MHz,
                Arty 50 MHz) so one binary proves the trim LSB really is
                1/CLK_FREQ_HZ_P and not a 100 MHz coincidence, and exposes
                the counter and the fractional accumulator so the harness can
                check the period BOUNDS, not just the average.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

`default_nettype none

module media_nco_wrap (
  input  wire         clk_i,
  input  wire         rst_n,

  //! A: the AX7101 shipping shape
  input  wire signed [17:0] a_trim_i,
  output wire               a_tick_o,
  output wire [15:0]        a_phase_o,
  output wire [31:0]        a_cnt_o,

  //! B: the Arty shape - same FS, different datapath clock
  input  wire signed [17:0] b_trim_i,
  output wire               b_tick_o,
  output wire [15:0]        b_phase_o,
  output wire [31:0]        b_cnt_o
);

  wire [15:0] a_ph_w, b_ph_w;

  KL_media_nco #(
    .CLK_FREQ_HZ_P (100_000_000),
    .FS_HZ_P       (48_000),
    .TRIMW_P       (18)
  ) nco_a (
    .clk_i   (clk_i),
    .rst_n   (rst_n),
    .trim_i  (a_trim_i),
    .tick_o  (a_tick_o),
    .phase_o (a_ph_w)
  );

  KL_media_nco #(
    .CLK_FREQ_HZ_P (50_000_000),
    .FS_HZ_P       (48_000),
    .TRIMW_P       (18)
  ) nco_b (
    .clk_i   (clk_i),
    .rst_n   (rst_n),
    .trim_i  (b_trim_i),
    .tick_o  (b_tick_o),
    .phase_o (b_ph_w)
  );

  assign a_phase_o = a_ph_w;
  assign b_phase_o = b_ph_w;

  //! cross-module reference to the free counter: the harness needs the
  //! instantaneous period, which the ports alone cannot show
  assign a_cnt_o = 32'(nco_a.cnt_r);
  assign b_cnt_o = 32'(nco_b.cnt_r);

endmodule

`default_nettype wire

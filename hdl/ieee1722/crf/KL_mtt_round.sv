/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_mtt_round.sv
  Author      : Kebag Logic

  Date        : 2026-10-20
  Description : The presentation offsets of one clock domain's stream outputs,
                each rounded UP to a whole number of media clock periods
                (#632, R678-1-F2).

                IEEE 1722-2016 4.3.5 asks the streams generated from one media
                clock to stay whole periods apart, and 10.8 Eq. 15 puts the
                timestamps of a talker that follows CRF within +/-5 % of a
                period of the CRF timing points. The domain's outputs all stamp
                one grid of frame instants (KL_media_domain_event), so each
                output's offset must itself be whole periods: a raw 2,010,000
                ns at 48 kHz leaves 10,000 ns modulo Ps, 0.48 Ps off the grid.

                THE RULE IS KL_crf_tx's, 10.7 Equation (14), applied to every
                row:
                  periods   = ceil(TTmax / P)   = ceil(TTmax * DEN / NUM)
                  offset_ns = ceil(periods * P) = ceil(periods * NUM / DEN)
                with P = NUM / DEN ns exactly (62500 / 3 at 48 kHz). The
                ceiling leaves offset_ns at most 1 ns above periods * P, five
                orders of magnitude inside the 10.8 band, and never below the
                Max Transit Time. This module serves every output of the
                domain, the AAF talkers and the CRF output (KL_crf_tx with
                ROUND_MTT_P = 0, its own converter not elaborated), and the
                GET_STREAM_INFO readback of every row, so what a controller
                reads is what every output stamps.

                NOT IDEMPOTENT, as Equation 14 is not in whole ns: a whole
                number of periods that is no multiple of three (97 periods,
                2,020,833.33 ns) is applied as its ceiling, 2,020,834 ns, and
                that value set again is above 97 periods, so it applies as
                98. Values a controller ordinarily sets, multiples of
                62,500 ns (0.25, 0.5, 1 and 2 ms), are exact and idempotent.

                SEQUENTIAL, ONE DIVIDER, NO MULTIPLIER. The rows change at
                register rate (SET_STREAM_INFO), so one restoring divider
                converts them in turn, round and round (two passes of DIVW_C
                steps each, so a row set by a controller is applied within
                N_P conversions, about 75 cycles each). Pass 1's numerator
                TTmax * DEN is shifted adds of the small constant DEN, and
                pass 2's, periods * NUM, is pass 1's numerator less its
                remainder. A row's output only ever moves to a
                whole conversion, never a half-converted value. Reset loads
                every row's output with the rounding of RESET_NS_P, its
                factory value, computed at elaboration, so no row reads 0 at
                power-on.

                THE OUTPUT IS 32 BITS: the low half of the rounded value. An
                AVTP timestamp is the low 32 bits of gPTP time, so a talker
                adding it stamps exactly what the whole value would. At 48 kHz
                an input above 4,294,958,333 ns (whose rounding, 206,158
                periods or 4,294,958,334 ns, is the largest under 2^32) rounds
                past 2^32 and reads back modulo 2^32.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Presentation offsets rounded up to whole media clock periods (IEEE
//! 1722-2016 10.7 Eq. 14, 4.3.5, 10.8 Eq. 15), one shared sequential divider,
//! factory values rounded at elaboration.

`default_nettype none

module KL_mtt_round #(
  parameter int unsigned N_P       = 2,       //! offset rows
  parameter int unsigned BASE_HZ_P = 48000,   //! the media clock's nominal rate
  //! each row's factory value, ns (row k = [32k +: 32])
  parameter logic [N_P*32-1:0] RESET_NS_P = {N_P{32'd2_000_000}}
)(
  input  wire              clk_i,          //! datapath clock
  input  wire              rst_n,          //! active-low synchronous reset
  input  wire [N_P*32-1:0] raw_ns_i,       //! the rows as set, ns
  output logic [N_P*32-1:0] ofs_ns_o       //! the rows as applied, ns (low 32 bits)
);

  //! P = NUM / DEN ns exactly, reduced as KL_crf_tx reduces it and checked
  localparam int unsigned NS_PER_S_C = 1_000_000_000;
  localparam int unsigned RED_C      = 16_000;
  localparam int unsigned NUM_C      = NS_PER_S_C / RED_C;
  localparam int unsigned DEN_C      = BASE_HZ_P / RED_C;
  if ((NS_PER_S_C % RED_C) != 0 || (BASE_HZ_P % RED_C) != 0 || DEN_C == 0) begin : g_rational
    $error("KL_mtt_round: RED_C=%0d does not divide both 1e9 and BASE_HZ_P=%0d, so NUM/DEN is not the media clock period.",
           RED_C, BASE_HZ_P);
  end : g_rational
  if (N_P < 1 || N_P > 16) begin : g_rows
    $error("KL_mtt_round: N_P=%0d must be 1..16.", N_P);
  end : g_rows

  //! divider sizing from the two passes' worst-case numerators (KL_crf_tx's)
  localparam longint unsigned TT_MAX_C   = 64'hFFFF_FFFF;
  localparam longint unsigned NUM1_MAX_C = TT_MAX_C * 64'(DEN_C) + 64'(NUM_C) - 64'd1;
  localparam longint unsigned PER_MAX_C  = NUM1_MAX_C / 64'(NUM_C);
  localparam longint unsigned NUM2_MAX_C = PER_MAX_C * 64'(NUM_C) + 64'(DEN_C) - 64'd1;
  localparam int unsigned DIVW_C  = $clog2(((NUM1_MAX_C > NUM2_MAX_C) ? NUM1_MAX_C : NUM2_MAX_C) + 64'd1);
  localparam int unsigned REMW_C  = $clog2(NUM_C + 1) + 1;
  localparam int unsigned STEPW_C = $clog2(DIVW_C + 1);
  localparam int unsigned IW_C    = (N_P > 1) ? $clog2(N_P) : 1;

  //! the rule at elaboration, for the factory values
  function automatic logic [31:0] round_c(input longint unsigned t);
    longint unsigned per;
    per = (t * 64'(DEN_C) + 64'(NUM_C) - 64'd1) / 64'(NUM_C);
    round_c = 32'((per * 64'(NUM_C) + 64'(DEN_C) - 64'd1) / 64'(DEN_C));
  endfunction

  logic [IW_C-1:0]    row_r;          //! the row the divider converts

  //! x * DEN as shifted adds: DEN is a small elaboration constant (3 at
  //! 48 kHz), so this is adders, never a multiplier block
  function automatic logic [DIVW_C-1:0] mul_den(input logic [31:0] x);
    logic [DIVW_C-1:0] acc;
    acc = '0;
    for (int b = 0; b < 32; b++)
      if (((DEN_C >> b) & 1) != 0) acc = acc + (DIVW_C'(x) << b);
    return acc;
  endfunction

  logic [DIVW_C-1:0]  dv_n1_r;        //! pass 1's numerator, kept for pass 2
  logic [DIVW_C-1:0]  dv_num_r;
  logic [DIVW_C-1:0]  dv_quot_r;
  logic [REMW_C-1:0]  dv_rem_r;
  logic [STEPW_C-1:0] dv_step_r;
  logic               dv_busy_r;
  logic               dv_pass2_r;     //! 0 = TTmax -> periods, 1 = periods -> ns

  //! each pass divides by its own constant: NUM, then DEN
  wire [REMW_C-1:0] dv_div_w = dv_pass2_r ? REMW_C'(DEN_C) : REMW_C'(NUM_C);
  wire [REMW_C-1:0] dv_rsh_w = {dv_rem_r[REMW_C-2:0], dv_num_r[DIVW_C-1]};
  wire              dv_ge_w  = (dv_rsh_w >= dv_div_w);
  //! the served row's input, and the row after it
  wire [31:0]       raw_row_w = raw_ns_i[32*row_r +: 32];
  //! pass 1 divides TTmax * DEN + NUM - 1 by NUM: quotient periods, remainder
  //! r. So periods * NUM is that numerator less r, and pass 2's numerator,
  //! periods * NUM + DEN - 1, needs no multiplier either
  wire [DIVW_C-1:0] dv_n1_w   = mul_den(raw_row_w) + DIVW_C'(NUM_C - 1);
  wire [DIVW_C-1:0] dv_n2_w   = dv_n1_r - DIVW_C'(dv_rem_r) + DIVW_C'(DEN_C - 1);
  wire [IW_C-1:0]   row_nx_w  = (32'(row_r) == N_P - 1) ? '0 : row_r + 1'b1;

  always_ff @(posedge clk_i) begin : rounder
    if (!rst_n) begin
      for (int unsigned k = 0; k < N_P; k++)
        ofs_ns_o[32*k +: 32] <= round_c(64'(RESET_NS_P[32*k +: 32]));
      row_r      <= '0;
      dv_n1_r    <= '0;
      dv_num_r   <= '0;
      dv_quot_r  <= '0;
      dv_rem_r   <= '0;
      dv_step_r  <= '0;
      dv_busy_r  <= 1'b0;
      dv_pass2_r <= 1'b0;
    end else if (!dv_busy_r) begin
      //! the next row's conversion: pass 1 answers ceil(TTmax * DEN / NUM)
      dv_n1_r    <= dv_n1_w;
      dv_num_r   <= dv_n1_w;
      dv_quot_r  <= '0;
      dv_rem_r   <= '0;
      dv_step_r  <= STEPW_C'(DIVW_C);
      dv_pass2_r <= 1'b0;
      dv_busy_r  <= 1'b1;
    end else if (dv_step_r != '0) begin
      dv_rem_r  <= dv_ge_w ? (dv_rsh_w - dv_div_w) : dv_rsh_w;
      dv_quot_r <= {dv_quot_r[DIVW_C-2:0], dv_ge_w};
      dv_num_r  <= {dv_num_r[DIVW_C-2:0], 1'b0};
      dv_step_r <= dv_step_r - 1'b1;
    end else if (!dv_pass2_r) begin
      //! pass 1 answered ceil(TTmax / P); pass 2 turns it back into ns,
      //! rounded up again
      dv_num_r   <= dv_n2_w;
      dv_quot_r  <= '0;
      dv_rem_r   <= '0;
      dv_step_r  <= STEPW_C'(DIVW_C);
      dv_pass2_r <= 1'b1;
    end else begin
      //! only now does the row's output move, to the whole conversion
      ofs_ns_o[32*row_r +: 32] <= dv_quot_r[31:0];
      dv_busy_r             <= 1'b0;
      row_r                 <= row_nx_w;
    end
  end : rounder

  //! the rounded value's bits above 32 are the modulo-2^32 wrap (banner)
  wire _unused_ok = &{1'b0, dv_quot_r[DIVW_C-1:32], 1'b0};

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_timers.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP centralised timer module.

                Provides all periodic strobes required by the AECP pipeline:

                tick_1khz_o
                  Generated from a 17-bit internal counter at 125 MHz,
                  producing a one-cycle pulse every 125 000 clock cycles
                  (exactly 1 ms / 1 kHz).  Does NOT depend on ptp_ts_i so
                  it is available immediately after reset.  ptp_ts_i is
                  reserved for future phase-locked improvements.

                lock_expired_o
                  17-bit downcounter reloaded to LOCK_TIMER_TICKS_C on
                  lock_start_i, asserts for one cycle when it reaches zero.
                  Cleared (de-asserted and counter stopped) by lock_clear_i.

                counter_gate_o
                  10-bit downcounter reloaded to COUNTER_THROTTLE_TICKS_C on
                  each tick_1khz_o pulse.  Asserts for one cycle when the
                  counter reaches zero (i.e. once per second).

                stale_tick_o
                  Simplified: directly re-exports tick_1khz_o.  Future
                  versions should gate this per-controller.

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9; Milan v1.2 §5.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_timers #(
  //! Datapath clock (AX7101 100 MHz, Arty 50 MHz; legacy default 125 MHz)
  parameter int unsigned CLK_FREQ_HZ_P = 125_000_000
) (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire [63:0]   ptp_ts_i,          //! 64-bit gPTP timestamp (ns) — reserved
  output logic         tick_1khz_o,        //! 1 kHz pulse (1 ms period)
  // ENTITY_LOCK timer (driven by KL_aecp_l0_state inputs)
  input  wire          lock_start_i,
  input  wire          lock_clear_i,
  output logic         lock_expired_o,
  // GET_COUNTERS throttle (per-controller, simplified to global 1-s gate)
  output logic         counter_gate_o,
  // Controller staleness pulse (one per registered controller per second)
  output logic         stale_tick_o
);

  // ------------------------------------------------------------------ //
  // 1 kHz generator                                                      //
  // 125 MHz / 125 000 = 1 kHz exactly.                                   //
  // ------------------------------------------------------------------ //
  localparam int unsigned TICK_DIV_C     = CLK_FREQ_HZ_P / 1_000;
  localparam int unsigned TICK_CNT_W_C   = $clog2(TICK_DIV_C);

  logic [TICK_CNT_W_C-1:0] ms_ctr_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ms_ctr_r    <= '0;
      tick_1khz_o <= 1'b0;
    end else begin
      tick_1khz_o <= 1'b0;
      if (ms_ctr_r == TICK_CNT_W_C'(TICK_DIV_C - 1)) begin
        ms_ctr_r    <= '0;
        tick_1khz_o <= 1'b1;
      end else begin
        ms_ctr_r <= ms_ctr_r + 1'b1;
      end
    end
  end

  // ------------------------------------------------------------------ //
  // ENTITY_LOCK downcounter                                              //
  // Reloaded to LOCK_TIMER_TICKS_C (60 000) on lock_start_i.            //
  // Decrements once per tick_1khz_o pulse.                               //
  // lock_expired_o pulses for one cycle when counter hits zero.          //
  // lock_clear_i stops the counter and clears lock_expired_o.            //
  // ------------------------------------------------------------------ //
  logic [16:0] lock_ctr_r;
  logic        lock_running_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      lock_ctr_r     <= 17'd0;
      lock_running_r <= 1'b0;
      lock_expired_o <= 1'b0;
    end else begin
      lock_expired_o <= 1'b0;   // default: clear strobe

      if (lock_clear_i) begin
        lock_ctr_r     <= 17'd0;
        lock_running_r <= 1'b0;
      end else if (lock_start_i) begin
        lock_ctr_r     <= LOCK_TIMER_TICKS_C;
        lock_running_r <= 1'b1;
      end else if (lock_running_r && tick_1khz_o) begin
        if (lock_ctr_r == 17'd0) begin
          lock_running_r <= 1'b0;
          lock_expired_o <= 1'b1;
        end else begin
          lock_ctr_r <= lock_ctr_r - 17'd1;
        end
      end
    end
  end

  // ------------------------------------------------------------------ //
  // GET_COUNTERS throttle gate                                           //
  // 10-bit downcounter, reloaded to 1000 on each tick_1khz_o.           //
  // counter_gate_o pulses when counter reaches zero (once per second).  //
  // ------------------------------------------------------------------ //
  logic [9:0] gate_ctr_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      gate_ctr_r     <= COUNTER_THROTTLE_TICKS_C;
      counter_gate_o <= 1'b0;
    end else begin
      counter_gate_o <= 1'b0;
      if (tick_1khz_o) begin
        if (gate_ctr_r == 10'd0) begin
          gate_ctr_r     <= COUNTER_THROTTLE_TICKS_C;
          counter_gate_o <= 1'b1;
        end else begin
          gate_ctr_r <= gate_ctr_r - 10'd1;
        end
      end
    end
  end

  // ------------------------------------------------------------------ //
  // Staleness tick                                                       //
  // Simplified: re-export tick_1khz_o.                                  //
  // TODO: implement per-controller staleness tracking using              //
  //       STALE_TIMER_TICKS_C and the unsolicited table.                 //
  // ------------------------------------------------------------------ //
  assign stale_tick_o = tick_1khz_o;

  // ------------------------------------------------------------------ //
  // Suppress unused-input warning for ptp_ts_i (reserved)              //
  // ------------------------------------------------------------------ //
  // verilator lint_off UNUSED
  wire [63:0] unused_ptp = ptp_ts_i;
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire

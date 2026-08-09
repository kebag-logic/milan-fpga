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

                mon_expired_o (gh #59, Milan v1.2 §5.4.5.3)
                  Per-registration-slot monitor timers: 16-bit MILLISECOND
                  downcounters off tick_1khz_o, reloaded on slot birth
                  (mon_arm_i) and on every "heard" event (mon_heard_i) with
                  MONITOR_MIN_MS_P + a fold of a free-running LFSR seeded
                  from the entity id.  The clause asks for "a random value
                  between 30 seconds and 60 seconds" PER CONTROLLER; the
                  entity-id seed is what keeps two boards on the same wire
                  from probing in lockstep forever (identical reload
                  sequences would make every device on the segment fire its
                  CONTROLLER_AVAILABLE burst in the same millisecond).
                  mon_expired_o[s] pulses for one cycle when slot s's
                  counter reaches zero, and the counter STOPS there — the
                  builder owns the outcome (reply -> heard -> reload,
                  silence -> evict -> clear).
                  mon_force_exp_i zeroes every RUNNING counter, which is the
                  5.4.2.21 "may" arm: a refused registration sweeps the whole
                  table so dead slots free within about a second.

                ack_expired_o (IEEE 1722.1-2021 §9.3.2.6 / §9.3.6)
                  The shared acknowledgement downcounter for the ONE
                  outstanding CONTROLLER_AVAILABLE probe: 250 ms by default,
                  started by the builder when the probe frame CONCLUDES (so
                  arbitration delay can never fake a timeout) and cleared
                  when the answer arrives.

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
  parameter int unsigned CLK_FREQ_HZ_P = 125_000_000,
  //! Registration slots monitored (= KL_aecp_response_builder UNSOL_SLOTS_C)
  parameter int unsigned MON_SLOTS_P = 4,
  //! Monitor timer floor, milliseconds (Milan 5.4.5.3: 30 s)
  parameter int unsigned MONITOR_MIN_MS_P = 30_000,
  //! ...and the random span above it (30 s -> the clause's 30..60 s window).
  //! The testbench shrinks both so a full silent-eviction walk simulates.
  parameter int unsigned MONITOR_RND_MS_P = 30_000,
  //! CONTROLLER_AVAILABLE acknowledgement timeout (1722.1-2021 9.3.2.6)
  parameter int unsigned ACK_MS_P = 250
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
  // ---- gh #59: departing-controller monitors (Milan v1.2 §5.4.5.3) ----
  input  wire [63:0]   entity_id_i,               //! LFSR seed
  input  wire [MON_SLOTS_P-1:0] mon_arm_i,        //! slot birth: start + reload
  input  wire [MON_SLOTS_P-1:0] mon_heard_i,      //! liveness: reload
  input  wire [MON_SLOTS_P-1:0] mon_clear_i,      //! slot death: stop
  input  wire          mon_force_exp_i,           //! 5.4.2.21 NO_RESOURCES sweep
  output logic [MON_SLOTS_P-1:0] mon_expired_o,   //! 1-cycle per slot
  // ---- ...and the shared 250 ms acknowledgement counter ---------------
  input  wire          ack_start_i,
  input  wire          ack_clear_i,
  output logic         ack_expired_o
);

  // ------------------------------------------------------------------ //
  // 1 kHz generator                                                      //
  // 125 MHz / 125 000 = 1 kHz exactly.                                   //
  // ------------------------------------------------------------------ //
  localparam int unsigned TICK_DIV_C     = CLK_FREQ_HZ_P / 1_000;
  localparam int unsigned TICK_CNT_W_C   = $clog2(TICK_DIV_C);

  logic [TICK_CNT_W_C-1:0] ms_ctr_r;

  always_ff @(posedge clk_i) begin
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

  always_ff @(posedge clk_i) begin
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

  always_ff @(posedge clk_i) begin
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
  // Departing-controller monitors (Milan v1.2 §5.4.5.3)                  //
  //                                                                      //
  // Reload randomiser: a free-running 32-bit maximal LFSR (x^32 + x^22 + //
  // x^2 + x + 1) SEEDED FROM THE ENTITY ID the first cycle a non-zero id //
  // is present. The id arrives over CSR after reset, so seeding at reset //
  // alone would seed every board with the same zero; seeding on the      //
  // first non-zero value is what actually decorrelates two devices. The  //
  // seed is OR'd with 1 because an all-zero LFSR state is absorbing.     //
  //                                                                      //
  // The fold takes clog2(RND) bits and conditionally subtracts RND once, //
  // which lands strictly inside [0, RND) for every RND >= 2 (2^clog2(R)  //
  // < 2R always). No divider, no modulo, one comparator. The residual    //
  // bias towards the low end is irrelevant here: the value only has to   //
  // be unpredictable enough that two entities drift apart, and the       //
  // clause's own bound (30..60 s) is what the range check enforces.      //
  // ------------------------------------------------------------------ //
  localparam int unsigned MON_RND_W_C =
      (MONITOR_RND_MS_P < 2) ? 1 : $clog2(MONITOR_RND_MS_P);
  //! Downcounter width DERIVED from the law it enforces, never mirrored:
  //! the shipping 30 000 + 29 999 needs exactly 16 bits, so the deployed
  //! flop count is the 16-bit one the design was sized for, and a
  //! testbench that stretches or shrinks the window gets a counter that
  //! actually holds its own reload instead of a silent wrap. (A mirrored
  //! `16` is the defect class docs/limitations/RECURRING_DEFECT_PATTERNS.md
  //! names: it agrees with the parameter on day one and diverges in
  //! silence.) Same rule for the acknowledgement counter.
  localparam int unsigned MON_W_C =
      $clog2(MONITOR_MIN_MS_P + MONITOR_RND_MS_P + 1);
  localparam int unsigned ACK_W_C = (ACK_MS_P < 2) ? 1 : $clog2(ACK_MS_P + 1);

  logic [31:0] lfsr_r;
  logic        seeded_r;
  wire  [31:0] w_seed = (entity_id_i[31:0] ^ entity_id_i[63:32]) | 32'd1;
  wire         w_lfsr_fb = lfsr_r[31] ^ lfsr_r[21] ^ lfsr_r[1] ^ lfsr_r[0];

  always_ff @(posedge clk_i) begin : mon_lfsr
    if (!rst_n) begin
      lfsr_r   <= 32'd1;
      seeded_r <= 1'b0;
    end else if (!seeded_r && entity_id_i != 64'd0) begin
      lfsr_r   <= w_seed;
      seeded_r <= 1'b1;
    end else begin
      lfsr_r <= {lfsr_r[30:0], w_lfsr_fb};
    end
  end : mon_lfsr

  wire [MON_RND_W_C-1:0] w_fold = lfsr_r[MON_RND_W_C-1:0];
  wire [MON_W_C-1:0] w_mon_rnd =
      (MONITOR_RND_MS_P < 2)                              ? '0 :
      (MON_W_C'(w_fold) >= MON_W_C'(MONITOR_RND_MS_P))
          ? MON_W_C'(w_fold) - MON_W_C'(MONITOR_RND_MS_P)
          : MON_W_C'(w_fold);
  wire [MON_W_C-1:0] w_mon_reload = MON_W_C'(MONITOR_MIN_MS_P) + w_mon_rnd;

  logic [MON_W_C-1:0] mon_ctr_r [MON_SLOTS_P];
  logic [MON_SLOTS_P-1:0] mon_run_r;

  always_ff @(posedge clk_i) begin : mon_timers
    if (!rst_n) begin
      for (int s = 0; s < MON_SLOTS_P; s++) mon_ctr_r[s] <= '0;
      mon_run_r     <= '0;
      mon_expired_o <= '0;
    end else begin
      mon_expired_o <= '0;   // default: clear strobes
      for (int s = 0; s < MON_SLOTS_P; s++) begin
        if (mon_clear_i[s]) begin
          mon_ctr_r[s] <= '0;
          mon_run_r[s] <= 1'b0;
        end else if (mon_arm_i[s] || mon_heard_i[s]) begin
          mon_ctr_r[s] <= w_mon_reload;
          mon_run_r[s] <= 1'b1;
        end else if (mon_force_exp_i && mon_run_r[s]) begin
          //! 5.4.2.21 sweep: every live monitor expires on the next tick.
          //! A controller that ANSWERS its probe is re-armed by mon_heard_i
          //! and is never deregistered — "shall not automatically deregister
          //! another controller that is responding" holds by construction.
          mon_ctr_r[s] <= '0;
        end else if (mon_run_r[s] && tick_1khz_o) begin
          if (mon_ctr_r[s] == '0) begin
            mon_run_r[s]     <= 1'b0;   // the builder owns the outcome now
            mon_expired_o[s] <= 1'b1;
          end else begin
            mon_ctr_r[s] <= mon_ctr_r[s] - MON_W_C'(1);
          end
        end
      end
    end
  end : mon_timers

  // ------------------------------------------------------------------ //
  // CONTROLLER_AVAILABLE acknowledgement counter (9.3.2.6: 250 ms).      //
  // ONE outstanding probe at a time, so ONE counter. Started at the      //
  // probe frame's CONCLUDE, cleared by the answer.                       //
  // ------------------------------------------------------------------ //
  logic [ACK_W_C-1:0] ack_ctr_r;
  logic               ack_run_r;

  always_ff @(posedge clk_i) begin : ack_timer
    if (!rst_n) begin
      ack_ctr_r    <= '0;
      ack_run_r    <= 1'b0;
      ack_expired_o <= 1'b0;
    end else begin
      ack_expired_o <= 1'b0;
      if (ack_clear_i) begin
        ack_ctr_r <= '0;
        ack_run_r <= 1'b0;
      end else if (ack_start_i) begin
        ack_ctr_r <= ACK_W_C'(ACK_MS_P);
        ack_run_r <= 1'b1;
      end else if (ack_run_r && tick_1khz_o) begin
        if (ack_ctr_r == '0) begin
          ack_run_r     <= 1'b0;
          ack_expired_o <= 1'b1;
        end else begin
          ack_ctr_r <= ack_ctr_r - ACK_W_C'(1);
        end
      end
    end
  end : ack_timer

  // ------------------------------------------------------------------ //
  // Suppress unused-input warning for ptp_ts_i (reserved)              //
  // ------------------------------------------------------------------ //
  // verilator lint_off UNUSED
  wire [63:0] unused_ptp = ptp_ts_i;
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire

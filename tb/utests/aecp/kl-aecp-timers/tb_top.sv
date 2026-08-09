/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`default_nettype none

module tb_top();

  import aecp_pkg::*;

  //! Clock parameter: T=8 → 125 MHz
  parameter T = 8;

  bit clk;
  bit rst_n;

  //! Clock generation
  always #(T/2) clk = ~clk;

  //! gh #59 monitor slots (= aecp_pkg::AECP_UNSOL_SLOTS_C)
  localparam int unsigned SLOTS = AECP_UNSOL_SLOTS_C;

  //! DUT inputs
  logic [63:0] ptp_ts    = '0;
  logic        lock_start;
  logic        lock_clear;
  logic [63:0] entity_id = 64'h0200_00FF_FE00_0001;
  logic [SLOTS-1:0] mon_arm, mon_heard, mon_clear;
  logic        mon_force_exp;
  logic        ack_start, ack_clear;

  //! DUT outputs
  logic tick_1khz_out;
  logic lock_expired;
  logic counter_gate;
  logic [SLOTS-1:0] mon_expired;
  logic ack_expired;

  //! DUT instantiation. The monitor timers are shrunk here exactly as
  //! tb/verilator/aecp/sim_ctrlavail.cpp shrinks them: the clause's
  //! 30..60 s / 250 ms would take a simulated minute to walk.
  KL_aecp_timers #(
    .MON_SLOTS_P      (SLOTS),
    .MONITOR_MIN_MS_P (100),
    .MONITOR_RND_MS_P (50),
    .ACK_MS_P         (20)
  ) DUT (
    .clk_i          (clk),
    .rst_n          (rst_n),
    .ptp_ts_i       (ptp_ts),
    .tick_1khz_o    (tick_1khz_out),
    .lock_start_i   (lock_start),
    .lock_clear_i   (lock_clear),
    .lock_expired_o (lock_expired),
    .counter_gate_o (counter_gate),
    .entity_id_i    (entity_id),
    .mon_arm_i      (mon_arm),
    .mon_heard_i    (mon_heard),
    .mon_clear_i    (mon_clear),
    .mon_force_exp_i(mon_force_exp),
    .mon_expired_o  (mon_expired),
    .ack_start_i    (ack_start),
    .ack_clear_i    (ack_clear),
    .ack_expired_o  (ack_expired)
  );

  //! Monitoring variables
  int tick_count        = 0;
  int first_tick_cycle  = -1;
  int second_tick_cycle = -1;

  //! Monitor tick_1khz_o: record cycle numbers for first two edges
  always @(posedge clk) begin
    if (tick_1khz_out) begin
      tick_count++;
      if (first_tick_cycle < 0)
        first_tick_cycle  = int'($time / T);
      else if (second_tick_cycle < 0)
        second_tick_cycle = int'($time / T);
    end
  end

  // ------------------------------------------------------------------
  //! Task: reset DUT and initialise inputs to safe defaults.
  task reset_dut;
    lock_start    = 1'b0;
    lock_clear    = 1'b0;
    mon_arm       = '0;
    mon_heard     = '0;
    mon_clear     = '0;
    mon_force_exp = 1'b0;
    ack_start     = 1'b0;
    ack_clear     = 1'b0;
    #100;
    $display("[INFO][TOP] : Resetting the DUT");
    rst_n = 1'b1;
  endtask

  //! pulse one signal for a single clock
  task automatic pulse_arm(input int unsigned s);
    @(posedge clk); mon_arm[s] = 1'b1;
    @(posedge clk); mon_arm[s] = 1'b0;
  endtask
  task automatic pulse_heard(input int unsigned s);
    @(posedge clk); mon_heard[s] = 1'b1;
    @(posedge clk); mon_heard[s] = 1'b0;
  endtask

  //! Main TB
  initial begin
    reset_dut();

    // ------------------------------------------------------------------
    // Test 1: verify tick_1khz_o period = 125 000 clock cycles (1 ms @ 125 MHz)
    // Wait for two rising edges of tick_1khz_o then measure interval.
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 1 — verify tick_1khz_o period ≈ 125 000 cycles");
    wait (tick_count >= 2);
    begin
      int period_cycles;
      period_cycles = second_tick_cycle - first_tick_cycle;
      if (period_cycles < 124_900 || period_cycles > 125_100)
        $fatal(1, "[FATAL][TOP] Test 1 FAIL: tick_1khz_o period = %0d cycles (expected ~125000)",
               period_cycles);
      $display("[INFO][TOP] : Test 1 PASS — tick period = %0d cycles", period_cycles);
    end

    // ------------------------------------------------------------------
    // Test 2: lock timer — start it and verify lock_expired_o after
    //         LOCK_TIMER_TICKS_C (60 000) tick pulses.
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 2 — lock timer expires after ~60 000 ticks");
    begin
      int start_tick;
      int elapsed_ticks;
      @(posedge clk); lock_start = 1'b1;
      @(posedge clk); lock_start = 1'b0;
      start_tick = tick_count;
      wait (lock_expired);
      elapsed_ticks = tick_count - start_tick;
      if (elapsed_ticks < 59_990 || elapsed_ticks > 60_010)
        $fatal(1, "[FATAL][TOP] Test 2 FAIL: lock_expired at %0d ticks (expected ~60000)",
               elapsed_ticks);
      $display("[INFO][TOP] : Test 2 PASS — lock_expired after %0d ticks", elapsed_ticks);
    end

    // ------------------------------------------------------------------
    // Test 3: counter_gate_o fires every 1 000 ticks (1 s ÷ 1 kHz intervals)
    // Observe for 5 ms (625 000 cycles) and count gate pulses.
    // Expected: approximately 5 gate pulses (one per 1 000 ticks, 5 000 ticks total).
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 3 — counter_gate_o fires every ~1 000 ticks");
    begin
      int gate_count = 0;
      fork
        begin
          // Observation window: 5 ms = 5 000 ticks = 625 000 cycles
          #(T * 125_000 * 5);
        end
        begin
          forever begin
            @(posedge clk iff counter_gate);
            gate_count++;
          end
        end
      join_any
      disable fork;
      if (gate_count < 4 || gate_count > 6)
        $fatal(1, "[FATAL][TOP] Test 3 FAIL: counter_gate count=%0d in 5 ms (expected ~5)",
               gate_count);
      $display("[INFO][TOP] : Test 3 PASS — counter_gate fired %0d times in 5 ms", gate_count);
    end

    // ------------------------------------------------------------------
    // Test 4 (gh #59, Milan v1.2 5.4.5.3): a monitor timer reloads inside
    //         [MIN+1, MIN+RND] ms, "heard" re-arms it, and two consecutive
    //         reloads differ (the entity-id-seeded LFSR is what stops two
    //         boards probing in lockstep).
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 4 — monitor timer range + reload randomness");
    begin
      int t0, span0, span1;
      pulse_arm(0);
      t0 = tick_count;
      wait (mon_expired[0]);
      span0 = tick_count - t0;
      if (span0 < 101 || span0 > 150)
        $fatal(1, "[FATAL][TOP] Test 4 FAIL: monitor span %0d ms outside 101..150",
               span0);
      // a "heard" event re-arms the stopped timer with a NEW reload
      pulse_heard(0);
      t0 = tick_count;
      wait (mon_expired[0]);
      span1 = tick_count - t0;
      if (span1 < 101 || span1 > 150)
        $fatal(1, "[FATAL][TOP] Test 4 FAIL: reloaded span %0d ms outside 101..150",
               span1);
      if (span0 == span1)
        $fatal(1, "[FATAL][TOP] Test 4 FAIL: consecutive reloads identical (%0d ms) — the LFSR is not turning",
               span0);
      $display("[INFO][TOP] : Test 4 PASS — spans %0d ms then %0d ms", span0, span1);
    end

    // ------------------------------------------------------------------
    // Test 5: mon_clear_i stops a monitor for good (an explicit
    //         DEREGISTER), and mon_force_exp_i sweeps every RUNNING one
    //         (the Milan 5.4.2.21 NO_RESOURCES arm).
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 5 — clear stops, force-expire sweeps");
    begin
      int guard;
      pulse_arm(1);
      @(posedge clk); mon_clear[1] = 1'b1;
      @(posedge clk); mon_clear[1] = 1'b0;
      guard = tick_count;
      wait (tick_count > guard + 200);
      if (mon_expired[1] !== 1'b0)
        $fatal(1, "[FATAL][TOP] Test 5 FAIL: a cleared monitor still expired");

      pulse_arm(2);
      pulse_arm(3);
      @(posedge clk); mon_force_exp = 1'b1;
      @(posedge clk); mon_force_exp = 1'b0;
      guard = tick_count;
      fork
        begin wait (mon_expired[2]); end
        begin wait (tick_count > guard + 5)
              $fatal(1, "[FATAL][TOP] Test 5 FAIL: force-expire did not sweep slot 2"); end
      join_any
      disable fork;
      $display("[INFO][TOP] : Test 5 PASS — clear silences, force-expire sweeps");
    end

    // ------------------------------------------------------------------
    // Test 6: the shared acknowledgement counter (IEEE 1722.1-2021
    //         9.3.2.6's 250 ms, shrunk to 20 ms here) fires once, and
    //         ack_clear_i cancels it — that is the answered probe.
    // ------------------------------------------------------------------
    $display("[INFO][TOP] : Test 6 — acknowledgement window + cancel");
    begin
      int t0, span, guard;
      @(posedge clk); ack_start = 1'b1;
      @(posedge clk); ack_start = 1'b0;
      t0 = tick_count;
      wait (ack_expired);
      span = tick_count - t0;
      if (span < 20 || span > 22)
        $fatal(1, "[FATAL][TOP] Test 6 FAIL: acknowledgement window %0d ms (expected 21)",
               span);
      @(posedge clk); ack_start = 1'b1;
      @(posedge clk); ack_start = 1'b0;
      @(posedge clk); ack_clear = 1'b1;
      @(posedge clk); ack_clear = 1'b0;
      guard = tick_count;
      wait (tick_count > guard + 40);
      if (ack_expired !== 1'b0)
        $fatal(1, "[FATAL][TOP] Test 6 FAIL: a cancelled window still expired");
      $display("[INFO][TOP] : Test 6 PASS — window %0d ms, cancel holds", span);
    end

    $display("[INFO][TOP] : kl-aecp-timers utest PASS");
    $finish;
  end

endmodule

`default_nettype wire

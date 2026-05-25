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

  //! DUT inputs
  logic [63:0] ptp_ts    = '0;
  logic        lock_start;
  logic        lock_clear;

  //! DUT outputs
  logic tick_1khz_out;
  logic lock_expired;
  logic counter_gate;
  logic stale_tick;

  //! DUT instantiation
  KL_aecp_timers DUT (
    .clk_i          (clk),
    .rst_n          (rst_n),
    .ptp_ts_i       (ptp_ts),
    .tick_1khz_o    (tick_1khz_out),
    .lock_start_i   (lock_start),
    .lock_clear_i   (lock_clear),
    .lock_expired_o (lock_expired),
    .counter_gate_o (counter_gate),
    .stale_tick_o   (stale_tick)
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
    lock_start = 1'b0;
    lock_clear = 1'b0;
    #100;
    $display("[INFO][TOP] : Resetting the DUT");
    rst_n = 1'b1;
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

    $display("[INFO][TOP] : kl-aecp-timers utest PASS");
    $finish;
  end

endmodule

`default_nettype wire

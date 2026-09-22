/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : timestamp_counter.sv
  Author      : Oguz Kahraman / Kebag Logic

  Date        : 2025-07-12 (PHC rework 2026-07-01)
  Description : Register-controlled nanosecond timestamp counter for the PTP
                hardware clock (PHC). Replaces the fixed "+STEP_SIZE" counter
                with a fractional-nanosecond phase accumulator so software can
                discipline the clock rate and time (REQ-PTP-01..03):

                  * rate    (adjfine): each tick adds (incr_i + adj_i), both in
                    Q(INT).(FRAC_WIDTH) nanoseconds. incr_i is the nominal
                    per-tick step (e.g. 8.0 ns at 125 MHz); adj_i is the signed
                    fine-frequency addend written by ptp adjfine().
                  * settime (adjtime abs): cmd_load_i loads tod_wr_i into the
                    integer-ns field and clears the fraction.
                  * adjtime (offset): cmd_adjust_i adds the signed offset_i (ns)
                    to the integer-ns field on top of the normal tick.
                  * gettime: cmd_snapshot_i latches the current integer-ns value
                    into tod_snapshot_o (read back through milan_csr).

                The accumulator is {ns[COUNTER_WIDTH-1:0], frac[FRAC_WIDTH-1:0]};
                timestamp_out exposes the integer-ns field for TX/RX capture.
                All control inputs are expected to be already synchronised into
                this clock domain (see ptp_csr_sync); this block is single-clock
                and therefore directly unit-testable in Verilator.

                PPS OUTPUT (PPS_P, default OFF - issue #260). A metrology pin
                that lets a scope compare this device's notion of a second
                boundary against an external reference, instead of the device
                grading itself from its own servo error. It lives HERE, in the
                counter's own clock domain, and is a PURE COMPARATOR: one
                64-bit compare against a target register. That makes the edge
                deterministic to a single tick (8 ns at 125 MHz), two orders
                inside the Milan sub-microsecond requirement. Emitting it from
                the gPTP engine instead would carry that engine's dispatch and
                microprogram latency - microseconds of jitter, which is not a
                PPS - and would sit on the far side of an unresolved crossing.

                THE ERROR DOES NOT ACCUMULATE, which is the whole point. The
                accumulator is fractional, so the integer-ns field never lands
                exactly on a multiple of 1e9 and "ns % 1e9 == 0" is both wrong
                and expensive. Instead the target ADVANCES BY EXACTLY
                1,000,000,000 on every hit, so each edge is within one
                increment of the true boundary and the overshoot of one edge is
                not carried into the next. Over N pulses the boundary error
                stays bounded by one increment rather than growing with N.

                WHERE THAT BOUND IS MEASURED. "Within one increment" describes
                the SAMPLE the comparator accepted, not the pad. The compare
                reads the registered time during a cycle and pps_r is set at
                the end of that cycle, so the pin rises one PHC clock period
                after the sample that satisfied it. At the pad the edge
                therefore lags its boundary by less than one increment PLUS one
                clock period - under 16 ns at 125 MHz - before the pad's own
                clock-to-out and the board trace. Those extra terms are a
                CONSTANT offset a bench run calibrates out once; the claim that
                matters for the instrument is that no term of it grows with N.

                ARMING. Software writes an absolute target (a multiple of 1e9
                in PHC ns, i.e. a TAI second boundary) and strobes pps_arm_i;
                hardware owns the register from then on and pps_target_ns_o reads
                it back live, so "the target advanced by exactly 1e9 and
                nothing else touched it" is observable rather than asserted.
                Hardware cannot self-align without a 64-bit modulo, which is
                the division this design refuses to pay for; software already
                knows the boundary it wants.  A target armed in the PAST is
                defined, not undefined: the comparator hits every tick and the
                target catches up at 1e9 ns per tick, holding the output high
                until it reaches the live time - after which the grid is exact
                again.

                PULSE WIDTH / CYCLE MATH. PPS_WIDTH_CYC_P is a count of
                THIS CLOCK's cycles, not a time: width_seconds =
                PPS_WIDTH_CYC_P / f_clk. The 125000 default is 1.000 ms at the
                recommended 125 MHz PHC clock (REQ-PTP-07) and would be
                1.250 ms if the block were elaborated in a 100 MHz domain, so a
                build that does not run at 125 MHz must scale the parameter
                (milan_datapath derives it as MILAN_CLK_FREQ_HZ / 1000). 1 ms
                is conventional and easy to trigger on; only the RISING edge
                carries time.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC
------------------------------------------------------------------------------
*/

`default_nettype none

module timestamp_counter #(
  parameter int COUNTER_WIDTH = 64, //! Width of the integer-nanosecond field
  parameter int INCR_WIDTH    = 32, //! Width of the per-tick increment/addend
  parameter int FRAC_WIDTH    = 24, //! Fractional-nanosecond bits: PTP_INCR is Q8.24 (8 int ns + 24 frac)
  parameter bit PPS_P         = 1'b0,   //! 1 = build the PPS alarm; 0 = prune it and park pps_o at 0
  parameter int PPS_WIDTH_CYC_P = 125000 //! Stretched pulse width in CLK CYCLES (1.000 ms at 125 MHz)
)(
  input  wire clk,                              //! PHC clock (fixed 125 MHz source recommended, REQ-PTP-07)
  input  wire resetn,                           //! Active-low synchronous reset

  input  wire enable_i,                         //! 1 = counter runs; 0 = hold (rate updates paused)
  input  wire [INCR_WIDTH-1:0]        incr_i,   //! Nominal per-tick increment, Q(INT).FRAC ns
  input  wire signed [INCR_WIDTH-1:0] adj_i,    //! Signed adjfine addend, Q(INT).FRAC ns
  input  wire [COUNTER_WIDTH-1:0]     tod_wr_i, //! settime target time-of-day, ns
  input  wire                         cmd_load_i,   //! settime apply strobe (1 cycle, this domain)
  input  wire signed [COUNTER_WIDTH-1:0] offset_i,  //! adjtime signed delta, ns
  input  wire                         cmd_adjust_i, //! adjtime apply strobe (1 cycle)
  input  wire                         cmd_snapshot_i,//! gettime latch strobe (1 cycle)

  //! --- PPS alarm (PPS_P only; all three are ignored and pruned when PPS_P = 0) ---
  input  wire                         pps_enable_i, //! Runtime PPS enable (this domain); 0 = comparator idle, pps_o low
  input  wire [COUNTER_WIDTH-1:0]     pps_target_ns_i, //! Armed absolute target, ns (write a multiple of 1e9)
  input  wire                         pps_arm_i,    //! Load pps_target_ns_i into the live target (1 cycle, this domain)

  output wire [COUNTER_WIDTH-1:0] timestamp_out,      //! Live integer-ns time (for packet capture)
  output wire [COUNTER_WIDTH-1:0] tod_snapshot_o,     //! Integer-ns value latched on snapshot
  output wire                     tod_snapshot_valid_o,//! 1-cycle pulse when a snapshot is latched
  output wire                     pps_o,              //! PPS pin: rising edge = second boundary. Structural 0 when PPS_P = 0
  output wire [COUNTER_WIDTH-1:0] pps_target_ns_o        //! Live target, ns (advances by exactly 1e9 per pulse). 0 when PPS_P = 0
);

  localparam int ACC_WIDTH = COUNTER_WIDTH + FRAC_WIDTH;
  //! One second in integer nanoseconds - the exact amount the target advances.
  localparam logic [COUNTER_WIDTH-1:0] PPS_PERIOD_NS_C = COUNTER_WIDTH'(64'd1_000_000_000);
  //! Width of the pulse stretcher's down-counter.
  localparam int PPS_CNT_W = (PPS_WIDTH_CYC_P <= 2) ? 1 : $clog2(PPS_WIDTH_CYC_P);

  //! Phase accumulator: high COUNTER_WIDTH bits are integer ns, low FRAC_WIDTH are the fraction.
  logic [ACC_WIDTH-1:0] acc;
  //! Latched integer-ns snapshot for gettime.
  logic [COUNTER_WIDTH-1:0] tod_snapshot;
  //! Snapshot-valid pulse.
  logic tod_snapshot_valid;

  //! Per-tick signed step = nominal increment + adjfine addend (Q.FRAC ns).
  //! Sign-extended to the accumulator width before the add.
  wire signed [ACC_WIDTH-1:0] tick_step =
      ACC_WIDTH'($signed({1'b0, incr_i})) + ACC_WIDTH'($signed(adj_i));

  //! adjtime offset promoted to accumulator units (ns shifted into integer field).
  wire signed [ACC_WIDTH-1:0] offset_acc =
      ACC_WIDTH'($signed(offset_i)) <<< FRAC_WIDTH;

  assign timestamp_out        = acc[ACC_WIDTH-1 -: COUNTER_WIDTH];
  assign tod_snapshot_o       = tod_snapshot;
  assign tod_snapshot_valid_o = tod_snapshot_valid;

  //! Time-of-day accumulator with settime/adjtime/rate control.
  always_ff @(posedge clk) begin : tod_accumulator
    if (!resetn) begin
      acc <= '0;
    end
    else if (cmd_load_i) begin
      //! settime: load integer ns, clear fraction (absolute set wins over ticking)
      acc <= {tod_wr_i, {FRAC_WIDTH{1'b0}}};
    end
    else begin
      //! normal rate tick (when enabled), plus optional one-shot adjtime offset
      logic signed [ACC_WIDTH-1:0] next;
      next = $signed(acc);
      if (enable_i)     next = next + tick_step;
      if (cmd_adjust_i) next = next + offset_acc;
      acc <= next;
    end
  end

  //! gettime snapshot latch.
  always_ff @(posedge clk) begin : snapshot_latch
    if (!resetn) begin
      tod_snapshot       <= '0;
      tod_snapshot_valid <= 1'b0;
    end
    else begin
      tod_snapshot_valid <= cmd_snapshot_i;
      if (cmd_snapshot_i)
        tod_snapshot <= acc[ACC_WIDTH-1 -: COUNTER_WIDTH];
    end
  end

  // ---------------------------------------------------------------------------
  //! PPS alarm: one 64-bit compare, one 64-bit add, one pulse stretcher (#260).
  //! PPS_P = 0 prunes all three to nothing and parks the pin at 0.
  // ---------------------------------------------------------------------------
  generate
    if (PPS_P) begin : g_pps
      //! Live target. Loaded by pps_arm_i, then owned by this block.
      logic [COUNTER_WIDTH-1:0] pps_target_r;
      //! Stretcher down-counter (cycles remaining after the launch edge).
      logic [PPS_CNT_W-1:0]     pps_cnt_r;
      //! The pin.
      logic                     pps_r;
      //! Has a target ever been loaded? Set by the first pps_arm_i and then
      //! sticky. THIS IS NOT A CONVENIENCE. pps_enable_i and pps_arm_i reach
      //! this clock domain by two different crossings (a 2-flop synchroniser
      //! and a toggle plus edge-detect plus delay, both in ptp_csr_sync), so
      //! the one CSR word that carries both arrives here as enable FIRST by a
      //! couple of cycles. Without this flag those cycles compare the live
      //! time against the reset target of zero, which every real time passes,
      //! and the pin's first ever edge is a two-cycle runt that the arriving
      //! arm then clears. The gate lives here, in the ts_clk domain, rather
      //! than being argued away from the SoC's axis_clk = gtx_clk tie: the
      //! skew is a property of the two CDC shapes, not of the clock ratio.
      logic                     pps_armed_r;

      //! The comparator: >= rather than == because the fractional accumulator
      //! steps over the boundary, it never lands on it - qualified by a target
      //! that was actually armed, never by the reset zero.
      wire pps_hit_w = pps_enable_i && pps_armed_r && (timestamp_out >= pps_target_r);

      always_ff @(posedge clk) begin : pps_alarm
        if (!resetn) begin
          pps_target_r <= '0;
          pps_cnt_r    <= '0;
          pps_r        <= 1'b0;
          pps_armed_r  <= 1'b0;
        end
        else if (pps_arm_i) begin
          //! Arming wins over a hit and clears any pulse in flight, so the
          //! first edge after an arm is always the armed boundary. The arm
          //! strobe carries a settled payload: ptp_csr_sync captures the
          //! target one cycle BEFORE it raises this strobe.
          pps_target_r <= pps_target_ns_i;
          pps_cnt_r    <= '0;
          pps_r        <= 1'b0;
          pps_armed_r  <= 1'b1;
        end
        else if (pps_hit_w) begin
          //! EXACTLY 1e9, never "now + 1e9": that is what keeps the error
          //! bounded by one increment instead of integrating over pulses.
          //! Bound at the SAMPLE; the pin adds this register's own cycle.
          pps_target_r <= pps_target_r + PPS_PERIOD_NS_C;
          pps_cnt_r    <= PPS_CNT_W'(PPS_WIDTH_CYC_P - 1);
          pps_r        <= 1'b1;
        end
        else if (pps_cnt_r != '0) begin
          pps_cnt_r <= pps_cnt_r - 1'b1;
        end
        else begin
          pps_r <= 1'b0;
        end
      end : pps_alarm

      assign pps_o           = pps_r;
      assign pps_target_ns_o = pps_target_r;
    end : g_pps
    else begin : g_pps_parked
      //! Option OFF: the pin is a structural zero, not a runtime-low signal -
      //! no comparator, no target register, no stretcher is elaborated.
      assign pps_o           = 1'b0;
      assign pps_target_ns_o = '0;
      wire _unused_pps = &{1'b0, pps_enable_i, pps_target_ns_i, pps_arm_i, 1'b0};
    end : g_pps_parked
  endgenerate

endmodule

`default_nettype wire

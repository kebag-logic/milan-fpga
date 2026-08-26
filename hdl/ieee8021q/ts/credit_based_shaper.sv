/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : credit_based_shaper.sv
  Author      : Oguz Kahraman / Kebag Logic

  Date        : 2025-07-05 (runtime-config rework 2026-07-01)
  Description : Credit-Based Shaper (CBS) implementing IEEE 802.1Qav traffic
                shaping for a single traffic class. Maintains a Q31.16 credit
                counter that governs transmission eligibility:

                  - credit accrues at idleSlope while the queue waits with data
                  - credit drains at sendSlope (= idleSlope - portRate) while
                    transmitting
                  - transmission is allowed only when credit >= 0
                  - credit is clamped to [loCredit, hiCredit]

                Runtime configuration (REQ-CBS-01): idleSlope, hiCredit and
                loCredit arrive on input ports driven by the milan_csr CBS
                register block instead of being compile-time parameters, so the
                host CBS offload path can reprogram the shaper live. The
                per-cycle/per-byte Q16 slope terms are derived in hardware by a
                SEQUENTIAL slope engine (one shared serial restoring divider on
                a fixed 100-cycle cadence, see slope_engine below): steady-state
                results are bit-identical to the SystemVerilog '/' operator, but
                a config change now takes effect at the next engine commit, at
                most 200 cycles later, instead of 1 cycle. Config latency is not
                part of the 802.1Qav shaping contract. The previous per-cycle
                combinational constant divides cost ~2.3K LUTs per queue on
                xc7a100t (measured 2026-07-11, ~18 percent of the whole SoC over
                4 queues) and needed a multicycle XDC exception. The Verilator
                reference model in tb/verilator/cbs mirrors the engine cadence
                cycle-exactly.

                Strict-priority classes (REQ-CBS-02): when `shaped_i` is 0 the
                queue is not credit-shaped - `allow_transmit_o` is forced high
                and the credit counter is parked at 0 so re-enabling shaping
                starts from a clean state.

                Backpressure accrual (REQ-CBS-04): when this queue holds the
                grant but the downstream is not ready (is_granted & !transmit),
                credit keeps accruing at idleSlope (bounded by hiCredit) instead
                of being frozen, matching 802.1Qav "queue has a frame ready and
                is waiting" semantics - qualified since REQ-CBS-07 by the
                wire-time debt below (no accrual while our own bytes are still
                serializing on the wire).

                Wire-time debt (REQ-CBS-07): 802.1Q-2018 8.6.8.2 (d)/(e) accrue
                idleSlope only while `transmit` is FALSE, and `transmit` covers
                the frame's real occupation of the wire - not the single clock
                in which this shaper hands 8 bytes to the MAC FIFO (at 100 MHz
                a beat leaves in 10 ns while 8 bytes occupy 64 ns of 1 Gb/s
                wire, so accruing on every non-transmitting cycle over-delivered
                9.6 / 20.5 percent at idleSlope 100 / 200 Mb/s, measured).
                `wire_debt_r` is a per-queue Q16 BYTE-denominated model of that
                occupation: it grows by the accepted bytes each beat, grows by
                the per-frame overhead (24 = preamble 7 + SFD 1 + FCS 4 +
                IFG 12, plus the MAC min-frame pad max(0, 60 - frame_bytes) -
                the pad matters for CRF-size frames) at tlast, and drains at
                the port byte rate every cycle. wire_transmit = (debt > 0) is
                the 8.6.8.2 (e) `transmit` variable: while it is TRUE the
                credit neither accrues (d) nor takes the queue-empty decay (f).
                The per-byte sendSlope debit (g) is unchanged - it already
                lands exactly once per accepted byte.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper
------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module credit_based_shaper #(
  parameter int CLK_FREQ_HZ = 100_000_000  //! Shaper clock frequency in Hz (constant divisor for idleSlope/cycle)
)(
  input  wire        clk,                   //! Clock signal (axis_clk domain)
  input  wire        resetn,                //! Synchronous active-low reset

  //! --- runtime configuration (from milan_csr CBS register group, REQ-CBS-01) ---
  input  wire        shaped_i,              //! 1 = apply CBS; 0 = strict priority (always eligible)
  input  wire [31:0] idle_slope_i,          //! idleSlope for the current link rate, bits/s
  input  wire signed [31:0] hi_credit_i,    //! hiCredit clamp, signed bytes
  input  wire signed [31:0] lo_credit_i,    //! loCredit clamp, signed bytes

  //! --- datapath status ---
  input  wire        queue_has_data_i,      //! Queue has a frame ready to send
  input  wire        is_transmitting_i,     //! Queue is actively transmitting this cycle
  input  wire        is_1g_i,               //! Link rate: 1 = 1 Gb/s, 0 = 100 Mb/s
  input  wire        is_granted_i,          //! Queue currently holds the transmit grant
  input  wire [15:0] bytes_sent_i,          //! Bytes transmitted this cycle (tkeep ones)
  input  wire        tlast_i,               //! bytes_sent_i carries the frame's last beat

  output wire        allow_transmit_o       //! High when credit allows transmission (or unshaped)
);

  //! Credit counter in Q31.16 fixed-point format (48-bit signed)
  (* use_dsp = "yes" *) logic signed [47:0] credit;

  //! Q.16 hiCredit / loCredit clamps (config bytes scaled by FP_DECIMAL_POINT)
  logic signed [47:0] hi_credit_q16;
  logic signed [47:0] lo_credit_q16;

  //! Slope result registers, written only by the slope engine's commit state.
  //! The per-cycle credit datapath below consumes these registered copies, so
  //! its timing is one register-to-DSP hop and needs no XDC exception.
  logic signed [47:0] idle_slope_per_cycle_r;
  logic signed [47:0] send_slope_per_byte_r;

  // --------------------------------------------------------------------------
  //  Sequential slope engine
  //
  //  idle_slope_per_cycle_r = (idle_slope <<< 16) / CLK_FREQ_HZ / BYTE_TO_BIT
  //  send_slope_per_byte_r  = ((idle_slope - link_rate) <<< 16) / link_rate
  //
  //  Both terms are functions ONLY of quasi-static config (idle_slope_i,
  //  is_1g_i). The 2026-07-01 rework computed them with per-cycle combinational
  //  constant-divisor cones; measured on xc7a100t 2026-07-11 those cost ~2.3K
  //  LUTs per queue (~9.3K over 4 queues, 18 percent of the SoC, partly
  //  attributed to milan_csr by cross-boundary optimization) and required a
  //  multicycle XDC. This engine computes the same two quotients with one
  //  31-bit serial restoring divider, 1 bit per cycle, on a FIXED 100-cycle
  //  cadence (data-independent, free-running):
  //
  //    cnt 0        sample idle_slope_i / is_1g_i
  //    cnt 1        load dividend |idle_slope <<< 16|, divisor CLK_FREQ_HZ*8
  //    cnt 2..49    48 divide iterations -> idle_slope_per_cycle quotient
  //    cnt 50       stash quotient 1; load |send_slope <<< 16|, divisor link
  //    cnt 51..98   48 divide iterations -> send_slope_per_byte quotient
  //    cnt 99       commit BOTH results atomically, wrap to cnt 0
  //
  //  Steady-state results are the exact rational quotients ROUNDED TO NEAREST,
  //  ties away from zero (REQ-CBS-06) - NOT the SystemVerilog '/' operator,
  //  which truncates toward zero and therefore biased sendSlope toward
  //  under-debiting. The 48-bit <<< wrap on out-of-range configs is unchanged.
  //  The divider runs magnitude / positive-divisor and reapplies the dividend
  //  sign, so the rounding is applied to the magnitude. Note (a/b)/c == a/(b*c) exactly for trunc
  //  division with positive divisors, so the two chained constant divides of
  //  the old RTL collapse into the single CLK_FREQ_HZ*BYTE_TO_BIT divisor.
  //  A config write takes effect at the next commit, at most 2 passes = 200
  //  cycles (2 us at 100 MHz) later. After reset the slope terms read 0 until
  //  the first commit (99 cycles), during which shaped queues simply accrue
  //  no credit; link auto-negotiation is orders of magnitude slower.
  //
  //  The cadence is mirrored cycle-exactly by SlopeEngineRef in
  //  tb/verilator/cbs/cbs_ref_model.h. Do NOT change the state timing or the
  //  commit atomicity without updating that model: the cbs harness compares
  //  the engine registers against the model every cycle, bit for bit.
  // --------------------------------------------------------------------------
  //! Divisor for idle_slope_per_cycle (fits 31 bits for CLK_FREQ_HZ <= 268 MHz)
  localparam logic [30:0] SLOPE_DEN1 = 31'(CLK_FREQ_HZ * BYTE_TO_BIT);

  logic [6:0]         eng_cnt;    //! engine cadence counter, 0..99
  logic signed [47:0] eng_idle_s; //! sampled idle_slope_i (sign extended)
  logic               eng_is1g_s; //! sampled link-rate select
  logic               eng_sign;   //! dividend sign of the divide in flight
  logic [47:0]        eng_num;    //! dividend magnitude shift register
  logic [30:0]        eng_rem;    //! partial remainder (invariant: < divisor)
  logic [47:0]        eng_quo;    //! quotient shift register
  logic signed [47:0] eng_q1;     //! stashed signed quotient of divide 1
  logic [30:0]        eng_den;    //! active divisor

  // --------------------------------------------------------------------------
  //  Wire-time debt constants (REQ-CBS-07). Port byte rate per shaper clock in
  //  Q16, DERIVED from CLK_FREQ_HZ at elaboration (derive-never-mirror), one
  //  constant per link rate, selected at runtime by the registered is_1g:
  //    1 Gb/s   = 125,000,000 B/s -> 1.25  B/cycle at 100 MHz (Q16 81920)
  //    100 Mb/s =  12,500,000 B/s -> 0.125 B/cycle at 100 MHz (Q16  8192)
  //  Rounded to nearest (exact for the shipping 100 MHz / 50 MHz clocks).
  // --------------------------------------------------------------------------
  localparam logic [31:0] WIRE_DRAIN_1G_Q16_C =
      32'(((64'd125_000_000 << 17) / 64'(CLK_FREQ_HZ) + 64'd1) >> 1);
  localparam logic [31:0] WIRE_DRAIN_100M_Q16_C =
      32'(((64'd12_500_000 << 17) / 64'(CLK_FREQ_HZ) + 64'd1) >> 1);
  //! per-frame wire overhead: preamble 7 + SFD 1 + FCS 4 + IFG 12 octets
  localparam logic [15:0] WIRE_OVERHEAD_BYTES_C = 16'd24;
  //! minimum MAC-client frame (64 wire octets less the 4-octet FCS): a
  //! shorter frame is padded to this by the MAC, and the pad is wire time
  localparam logic [15:0] MIN_FRAME_BYTES_C = 16'd60;

  //! stage-1 pipeline registers (registered for timing; see stage1_pipe)
  logic signed [47:0] send_delta;
  logic signed [47:0] credit_add_idle;
  logic is_transmitting;
  logic queue_has_data;
  logic is_granted;
  logic shaped;
  //! wire-debt stage-1 state: per-frame byte counter over the ACCEPTED beats
  //! and the registered Q16 debt increment this beat contributes
  logic [15:0] frame_cnt_r;
  logic [23:0] debt_add_r;
  logic        is_1g_r;
  //! the debt accumulator itself (stage 2): Q16 bytes still owed to the wire.
  //! 48 bits unsigned = the same numeric span as the credit register; the
  //! update clamps at 0 (drain never borrows) and saturates at all-ones.
  logic [47:0] wire_debt_r;

  //! 8.6.8.2 (e) `transmit`, wire-honest: our bytes are still serializing
  wire wire_transmit_w = (wire_debt_r != 48'd0);

  //! stage-1 combinational helpers for the debt increment. frame_len_w is
  //! the frame's total accepted bytes INCLUDING this beat; on the tlast beat
  //! the increment carries the fixed overhead plus the MAC min-frame pad.
  wire [15:0] frame_len_w = frame_cnt_r + bytes_sent_i;
  wire [15:0] frame_pad_w = (frame_len_w < MIN_FRAME_BYTES_C)
                            ? (MIN_FRAME_BYTES_C - frame_len_w) : 16'd0;
  wire [15:0] debt_add_bytes_w =
      bytes_sent_i + (tlast_i ? (WIRE_OVERHEAD_BYTES_C + frame_pad_w) : 16'd0);

  //! Clamp scaling (pure shifts, combinational from the config ports; the
  //! hi/lo clamps deliberately do NOT go through the slope engine so a
  //! reconfiguration that lowers hiCredit shrinks the burst allowance on the
  //! very next cycle, REQ-CBS-01).
  always_comb begin : clamp_calc
    hi_credit_q16 = 48'(signed'(hi_credit_i)) <<< FP_DECIMAL_POINT;
    lo_credit_q16 = 48'(signed'(lo_credit_i)) <<< FP_DECIMAL_POINT;
  end

  //! Slope engine combinational helpers: dividend selection (with the same
  //! 48-bit <<< wrap semantics as the old combinational divides), magnitude
  //! extraction, one restoring-divider iteration, and sign reapplication.
  wire signed [47:0] eng_link  = eng_is1g_s ? 48'sd1_000_000_000 : 48'sd100_000_000;
  wire signed [47:0] eng_ss    = eng_idle_s - eng_link;
  wire signed [47:0] eng_ldval = (eng_cnt == 7'd1) ? 48'(eng_idle_s <<< FP_DECIMAL_POINT)
                                                   : 48'(eng_ss     <<< FP_DECIMAL_POINT);
  wire               eng_ldsign = eng_ldval[47];
  wire        [47:0] eng_ldmag  = eng_ldsign ? (~eng_ldval + 48'd1) : eng_ldval;
  wire        [31:0] eng_trial  = {eng_rem, eng_num[47]};
  wire               eng_ge     = (eng_trial >= {1'b0, eng_den});
  wire        [31:0] eng_diff   = eng_trial - {1'b0, eng_den};
  //! REQ-CBS-06: ROUND-TO-NEAREST instead of truncating toward zero. The
  //! restoring divider leaves `eng_rem` = the true remainder and `eng_den` =
  //! the divisor of the divide that just finished, so `2*rem >= den` is exactly
  //! "the discarded fraction is >= 1/2". Rounding the MAGNITUDE and then
  //! reapplying the sign gives round-half-away-from-zero, which is unbiased -
  //! truncation was not: it always shrank |quotient|, so idleSlope accrued
  //! slightly SLOW (harmless, conservative) while sendSlope - a NEGATIVE term -
  //! debited slightly LESS than it should (not conservative: the queue keeps
  //! credit it has spent). With idleSlope runtime-programmable the residual is
  //! no longer a compile-time-known constant, which is why REQ-CBS-06 waited
  //! for REQ-CBS-01. Cost: one 32-bit compare and a 48-bit +1, both outside
  //! the 96 iteration cycles. Overflow-safe: a +1 could only carry out of 48
  //! bits if the quotient were all ones, which needs den == 1 - and den == 1
  //! leaves remainder 0, so the round bit is 0.
  wire               eng_round  = ({eng_rem, 1'b0} >= {1'b0, eng_den});
  wire        [47:0] eng_quo_r  = eng_quo + {47'd0, eng_round};
  wire signed [47:0] eng_quo_s  = eng_sign ? -$signed(eng_quo_r) : $signed(eng_quo_r);

  //! Slope engine sequencer (see the cadence table above). The iterate arm is
  //! the catch-all: every cnt value that is not sample/load/commit is one of
  //! the 96 divide iterations by construction.
  always_ff @(posedge clk) begin : slope_engine
    if (!resetn) begin
      eng_cnt    <= '0;
      eng_idle_s <= '0;
      eng_is1g_s <= 1'b0;
      eng_sign   <= 1'b0;
      eng_num    <= '0;
      eng_rem    <= '0;
      eng_quo    <= '0;
      eng_q1     <= '0;
      eng_den    <= 31'd1;
      idle_slope_per_cycle_r <= '0;
      send_slope_per_byte_r  <= '0;
    end else begin
      eng_cnt <= (eng_cnt == 7'd99) ? 7'd0 : (eng_cnt + 7'd1);
      if (eng_cnt == 7'd0) begin
        eng_idle_s <= 48'(signed'(idle_slope_i));
        eng_is1g_s <= is_1g_i;
      end else if (eng_cnt == 7'd1 || eng_cnt == 7'd50) begin
        if (eng_cnt == 7'd50) eng_q1 <= eng_quo_s;
        eng_sign <= eng_ldsign;
        eng_num  <= eng_ldmag;
        eng_rem  <= '0;
        eng_quo  <= '0;
        eng_den  <= (eng_cnt == 7'd1) ? SLOPE_DEN1
                    : (eng_is1g_s ? 31'd1_000_000_000 : 31'd100_000_000);
      end else if (eng_cnt == 7'd99) begin
        idle_slope_per_cycle_r <= eng_q1;
        send_slope_per_byte_r  <= eng_quo_s;
      end else begin
        eng_rem <= eng_ge ? eng_diff[30:0] : eng_trial[30:0];
        eng_quo <= {eng_quo[46:0], eng_ge};
        eng_num <= {eng_num[46:0], 1'b0};
      end
    end
  end

  //! Allow transmit if shaping is disabled (strict priority) or credit >= 0.
  //!
  //! REQ-CBS-05: this was a REGISTERED copy of (credit >= 0), so the arbiter's
  //! 802.1Qav transmissionAllowed test ran against the credit of the PREVIOUS
  //! cycle and could start a frame on a queue whose credit had already gone
  //! negative. Reading the sign bit of the credit register directly removes
  //! that cycle at ZERO cost in logic depth: the output was already
  //! reg -> 2:1 mux -> arbitration (`shaped` is itself a stage-1 register), and
  //! it still is - one register bit simply swaps for another.
  //!
  //! The REMAINING skew is the credit datapath's input pipeline, deliberately
  //! kept: `traffic_shaping_core` registers is_transmitting/bytes_sent off the
  //! AXIS handshake and stage1 here registers send_delta, so a transmitted beat
  //! reaches `credit` 2 cycles later. Collapsing that would move the
  //! send_slope x bytes_sent multiply into the tkeep/$countones cone, and this
  //! design places at 99.93 percent slice packing with WNS margins in the tens
  //! of picoseconds - not a change to make without a Vivado run. The residual
  //! is a fixed 2-cycle phase shift of an INTEGRAL, not an accumulating error
  //! (every beat is still debited exactly once), and tb/verilator/cbs pins the
  //! lag at exactly 2 so a future collapse has a number to beat.
  assign allow_transmit_o = shaped ? (credit >= 0) : 1'b1;

  //! Register every input for better timing (stage 1 of the credit pipeline).
  //! send_delta / credit_add_idle derive from the engine-registered slope
  //! terms, so this cycle only pays for the send_slope_per_byte_r * bytes_sent
  //! multiply.
  always_ff @(posedge clk) begin : stage1_pipe
    if(!resetn)begin
      send_delta      <= 'd0;
      credit_add_idle <= 'd0;
      is_transmitting <= 'd0;
      queue_has_data  <= 'd0;
      is_granted      <= 'd0;
      shaped          <= 'd0;
    end
    else begin
      send_delta      <= send_slope_per_byte_r * $signed(bytes_sent_i);
      credit_add_idle <= idle_slope_per_cycle_r;
      is_transmitting <= is_transmitting_i;
      queue_has_data  <= queue_has_data_i;
      is_granted      <= is_granted_i;
      shaped          <= shaped_i;
    end
  end

  //! Wire-debt stage 1: the per-frame byte counter walks the ACCEPTED beats
  //! (the same beats the sendSlope debit counts) and the Q16 debt increment
  //! is registered so stage 2 only pays an add. Kept out of stage1_pipe so
  //! its reset list stays the REQ-CBS-07 state alone.
  always_ff @(posedge clk) begin : debt_stage1
    if (!resetn) begin
      frame_cnt_r <= '0;
      debt_add_r  <= '0;
      is_1g_r     <= 1'b0;
    end
    else begin
      if (is_transmitting_i)
        frame_cnt_r <= tlast_i ? 16'd0 : frame_len_w;
      debt_add_r <= is_transmitting_i ? {debt_add_bytes_w[7:0], 16'b0}
                                      : 24'd0;
      is_1g_r    <= is_1g_i;
    end
  end : debt_stage1

  //! Wire-debt stage 2: debt += this beat's increment, -= the port byte
  //! rate, clamped at 0 (the wire cannot owe us time) and saturating at
  //! all-ones (unreachable with a sane config; insurance against wrap).
  //! Parked at 0 while unshaped, exactly like the credit (REQ-CBS-02).
  wire [31:0] wire_drain_q16_w = is_1g_r ? WIRE_DRAIN_1G_Q16_C
                                         : WIRE_DRAIN_100M_Q16_C;
  logic signed [49:0] debt_nx_c;
  always_comb begin : debt_next
    debt_nx_c = $signed({2'b00, wire_debt_r})
              + $signed({26'd0, debt_add_r})
              - $signed({18'd0, wire_drain_q16_w});
  end : debt_next

  always_ff @(posedge clk) begin : debt_update
    if (!resetn)
      wire_debt_r <= '0;
    else if (!shaped)
      wire_debt_r <= '0;
    else if (debt_nx_c < 0)
      wire_debt_r <= '0;
    else if (debt_nx_c > $signed({2'b00, {48{1'b1}}}))
      wire_debt_r <= '1;
    else
      wire_debt_r <= debt_nx_c[47:0];
  end : debt_update

  //! Credit update logic (stage 2). Uses the registered stage-1 signals.
  always_ff @(posedge clk) begin : credit_update_logic
    if(!resetn)begin
      credit <= '0;
    end
    else if(!shaped) begin
      //! Strict-priority class: park credit at 0 while unshaped (REQ-CBS-02)
      credit <= '0;
    end
    else begin
      if(is_transmitting) begin
        //! Apply send slope during transmission (bounded by loCredit)
        if(credit + send_delta < lo_credit_q16)
          credit <= lo_credit_q16;
        else
          credit <= credit + send_delta;
      end
      //! REQ-CBS-07: the wire is still serializing bytes this queue already
      //! handed over - 8.6.8.2 (e) transmit is TRUE, so neither the (d)
      //! idleSlope accrual nor the (f) queue-empty decay may run. The
      //! credit HOLDS until the debt drains to zero.
      else if (wire_transmit_w) begin
        credit <= credit;
      end
      //! If queue is empty and not transmitting, decay credit toward zero
      else if (!queue_has_data && credit >= 0) begin
        credit <= '0;
      end
      else if (!queue_has_data)begin
        //! Queue empty and credit negative: increment credit up to 0
        if(credit < 0)begin
          credit <= (credit + credit_add_idle >= 0) ? 'd0 : credit + credit_add_idle;
        end
        else begin
          credit <= 'd0;
        end
      end
      //! Queue has data and is waiting (eligible, or granted but back-pressured,
      //! REQ-CBS-04): accumulate credit at idleSlope, bounded by hiCredit. The
      //! comparison also clamps credit *down* to hiCredit if a runtime
      //! reconfiguration lowered hiCredit below the current credit (REQ-CBS-01),
      //! so the burst allowance shrinks immediately instead of persisting.
      else begin
        credit <= (credit + credit_add_idle > hi_credit_q16) ?
                  hi_credit_q16 : credit + credit_add_idle;
      end
    end
  end

endmodule

`default_nettype wire

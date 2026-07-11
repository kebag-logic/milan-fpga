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
                Linux `tc ... cbs` offload can reprogram the shaper live. The
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
                is waiting" semantics.

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
  //  Steady-state results are bit-identical to the SystemVerilog '/' operator
  //  (signed division truncating toward zero, including the 48-bit <<< wrap on
  //  out-of-range configs): the divider runs magnitude / positive-divisor and
  //  reapplies the dividend sign. Note (a/b)/c == a/(b*c) exactly for trunc
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

  //! registered allow_transmit signal
  logic allow_transmit_reg;

  //! stage-1 pipeline registers (registered for timing; see stage1_pipe)
  logic signed [47:0] send_delta;
  logic signed [47:0] credit_add_idle;
  logic is_transmitting;
  logic queue_has_data;
  logic is_granted;
  logic shaped;

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
  wire signed [47:0] eng_quo_s  = eng_sign ? -$signed(eng_quo) : $signed(eng_quo);

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

  //! Allow transmit if shaping is disabled (strict priority) or credit >= 0
  assign allow_transmit_o = shaped ? allow_transmit_reg : 1'b1;

  //! allow_transmit registered
  always_ff @(posedge clk) begin : allow_transmit
    if(!resetn)begin
      allow_transmit_reg <= '0;
    end else begin
      allow_transmit_reg <= (credit >= 0);
    end
  end

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

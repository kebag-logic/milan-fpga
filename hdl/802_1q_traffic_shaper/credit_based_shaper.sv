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
                per-cycle/per-byte Q16 slope terms are still derived in hardware,
                but every divisor is a compile-time constant (CLK_FREQ_HZ,
                BYTE_TO_BIT, and the two possible port rates 1e9/1e8), so the
                synthesiser maps them to constant-divisor logic rather than a
                general divider. The arithmetic is bit-identical to the previous
                parameterised version, so the Verilator reference model in
                tb/verilator/cbs still matches cycle-for-cycle.

                Strict-priority classes (REQ-CBS-02): when `shaped_i` is 0 the
                queue is not credit-shaped — `allow_transmit_o` is forced high
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

  //! Active idle slope (bps), sign-extended from the 32-bit config port
  logic signed [47:0] idle_slope;
  //! Active send slope (bps): idle_slope - link_rate (always negative)
  logic signed [47:0] send_slope;
  //! Active link rate (bps): 1_000_000_000 or 100_000_000
  logic signed [47:0] link_rate;
  //! Q.16 credit bytes earned per clock cycle during idle
  logic signed [47:0] idle_slope_per_cycle;
  //! Q.16 credit bytes lost per data byte transmitted
  logic signed [47:0] send_slope_per_byte;

  //! Q.16 hiCredit / loCredit clamps (config bytes scaled by FP_DECIMAL_POINT)
  logic signed [47:0] hi_credit_q16;
  logic signed [47:0] lo_credit_q16;

  //! stage-0 pipeline registers: the two constant-divide slope terms, held for
  //! timing. idle_slope_per_cycle / send_slope_per_byte are functions only of
  //! the quasi-static config (idle_slope_i, is_1g_i), so registering them here
  //! isolates the wide constant-divide combinational cone from the per-cycle
  //! multiply/accumulate below — the divide no longer shares a single clock
  //! period with `send_slope_per_byte * bytes_sent`. Because the source config
  //! is stable for millions of cycles, the config->slope_r path is declared a
  //! multicycle path in the SoC XDC (see milan_soc.py). Bit-exactly modelled by
  //! the Verilator FixedPointRef (one extra slope register stage).
  //! dont_touch keeps these as real fabric registers: without it the synthesiser
  //! absorbs them into the credit/send_delta DSP input registers, which (a) leaves
  //! the wide constant-divide combinational into the DSP (still a single-period
  //! ~21 ns path) and (b) erases the cell the multicycle XDC in milan_soc.py
  //! targets. Preserved, they form the register boundary the multicycle relies on.
  (* dont_touch = "true" *) logic signed [47:0] idle_slope_per_cycle_r;
  (* dont_touch = "true" *) logic signed [47:0] send_slope_per_byte_r;

  //! registered allow_transmit signal
  logic allow_transmit_reg;

  //! stage-1 pipeline registers (registered for timing; see stage1_pipe)
  logic signed [47:0] send_delta;
  logic signed [47:0] credit_add_idle;
  logic is_transmitting;
  logic queue_has_data;
  logic is_granted;
  logic shaped;

  //! Dynamic slope calculation. Divisors are compile-time constants
  //! (CLK_FREQ_HZ*BYTE_TO_BIT, and 1e9/1e8 selected by is_1g_i), so this maps
  //! to constant-divisor logic, not a general hardware divider.
  always_comb begin : slope_calc
    link_rate  = is_1g_i ? 48'sd1_000_000_000 : 48'sd100_000_000;
    idle_slope = 48'(signed'(idle_slope_i));
    send_slope = idle_slope - link_rate;

    // (idle << FP) / CLK_FREQ_HZ / BYTE_TO_BIT : two constant divides, exactly
    // as the original parameterised RTL (kept for bit-exact verification).
    idle_slope_per_cycle = (idle_slope <<< FP_DECIMAL_POINT) / CLK_FREQ_HZ / BYTE_TO_BIT;

    // (send << FP) / link_rate, but with a constant divisor on each branch.
    send_slope_per_byte = is_1g_i ? ((send_slope <<< FP_DECIMAL_POINT) / 48'sd1_000_000_000)
                                   : ((send_slope <<< FP_DECIMAL_POINT) / 48'sd100_000_000);

    hi_credit_q16 = 48'(signed'(hi_credit_i)) <<< FP_DECIMAL_POINT;
    lo_credit_q16 = 48'(signed'(lo_credit_i)) <<< FP_DECIMAL_POINT;
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

  //! Stage 0: register the constant-divide slope terms (multicycle-constrained
  //! config->slope_r path; see the declaration comment). Purely combinational
  //! divides feed these; the per-cycle datapath below uses the registered copies.
  always_ff @(posedge clk) begin : slope_pipe
    if(!resetn)begin
      idle_slope_per_cycle_r <= 'd0;
      send_slope_per_byte_r  <= 'd0;
    end
    else begin
      idle_slope_per_cycle_r <= idle_slope_per_cycle;
      send_slope_per_byte_r  <= send_slope_per_byte;
    end
  end

  //! Register every input for better timing (stage 1 of the credit pipeline).
  //! send_delta / credit_add_idle now derive from the *registered* slope terms
  //! (send_slope_per_byte_r / idle_slope_per_cycle_r), so this cycle only pays
  //! for the send_slope_per_byte_r * bytes_sent multiply, not the divide.
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

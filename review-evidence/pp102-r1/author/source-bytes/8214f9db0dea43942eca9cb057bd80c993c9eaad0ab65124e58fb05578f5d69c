/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_timer_service.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/08 §2/§3
//                F08.2 timebase + 08 §5 deadline RAM; 09 §3 TIM hook)
//
//  Description : The protocol-processor timer service: a prescaler chain
//                (core clock -> 1 µs tick -> 1 ms tick), a free-running
//                absolute ms timebase, and a SLOTS_P-deep deadline store
//                swept one slot per cycle after every ms tick. Arming is
//                O(1) (absolute-ms deadline written to the slot); expiry
//                detection is bounded by SLOTS_P per ms; expired slots
//                disarm themselves; simultaneous expiries serialize at one
//                owner-tagged event per cycle onto the event bus (F08.2).
//                Deadline compare is wrap-safe modular age arithmetic, so
//                an already-past deadline fires on the next sweep.
//
//                The one design decision that matters: the slot store is
//                SPLIT — {owner, deadline_ms} (40 b, the exact 89 x 40 b
//                RAM sizing of 08 §5) lives in a true 1W1R synchronous-read
//                RAM with the arm port as its ONLY writer, while the armed
//                bits live in a SLOTS_P-bit flop vector. Arm, cancel and
//                sweep-disarm then never contend for a RAM write port, and
//                the store infers as RAM — never the flop-mirror +
//                wide-read-mux failure mode the reference platform measured
//                at +894 LUT. On an arm/expiry collision for the same slot,
//                the arm wins: a one-cycle arm shadow suppresses the expiry
//                of a slot whose arm is still inside the sweep's read
//                pipeline (otherwise the sweep fires on the STALE deadline
//                the RAM returned before the write landed); the deferred
//                expiry is re-evaluated on the next sweep, 1 ms later.
//
//                Constraint: one full sweep (SLOTS_P + 2 cycles) must fit
//                inside one ms tick period (DIV_US_P * DIV_MS_P cycles); a
//                tick landing mid-sweep is remembered and the sweep re-runs
//                once, so expiries are never lost, only deferred.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_timer_service #(
    //! core clock frequency (P-CLK-HZ); only feeds the DIV_US_P default
    parameter int unsigned CLK_HZ_P = 100_000_000,
    //! deadline slots — P-TIMER-SLOTS by the 08 §5 formula (89 = SRP build)
    parameter int unsigned SLOTS_P  = pp_pkg::PP_TIMER_SLOTS_C,
    //! clk cycles per 1 µs tick; override to compress time (09 §3 TIM)
    parameter int unsigned DIV_US_P = CLK_HZ_P / 32'd1_000_000,
    //! µs ticks per 1 ms tick; override to compress time (09 §3 TIM)
    parameter int unsigned DIV_MS_P = 1000,
    //! derived slot-index width — do not override
    localparam int unsigned SLOT_AW_C = (SLOTS_P > 32'd1) ? $clog2(SLOTS_P)
                                                          : 32'd1
) (
    input  wire                  clk_i,              //! core clock
    input  wire                  rst_n,              //! sync active-low reset

    output logic                 tick_ms_o,          //! 1-cycle ms-boundary strobe (observability)
    output logic [31:0]          now_ms_o,           //! free-running absolute ms timebase

    input  wire                  arm_valid_i,        //! arm/cancel strobe (always accepted, O(1))
    input  wire                  arm_cancel_i,       //! 1 = cancel the slot, 0 = arm it
    input  wire  [SLOT_AW_C-1:0] arm_slot_i,         //! slot index to arm/cancel
    input  wire  [pp_pkg::PP_TIMER_OWNER_W_C-1:0] arm_owner_i, //! owner tag echoed at expiry
    input  wire  [31:0]          arm_deadline_ms_i,  //! ABSOLUTE deadline in ms (arrival + budget, 08 §4)

    output logic                 exp_valid_o,        //! expiry event (at most one per cycle)
    output logic [SLOT_AW_C-1:0] exp_slot_o,         //! expired slot (qualified by exp_valid_o)
    output logic [pp_pkg::PP_TIMER_OWNER_W_C-1:0] exp_owner_o //! owner tag (qualified by exp_valid_o)
);

  localparam int unsigned SLOT_DW_C = pp_pkg::PP_TIMER_SLOT_DW_C;  // 40 b

  // ------------------------------------------------------------ prescaler
  logic [31:0] us_cnt_r;
  logic [31:0] ms_cnt_r;
  logic [31:0] now_ms_r;
  logic        tick_us_w;
  logic        tick_ms_w;

  assign tick_us_w = (us_cnt_r == DIV_US_P - 32'd1);
  assign tick_ms_w = tick_us_w && (ms_cnt_r == DIV_MS_P - 32'd1);

  always_ff @(posedge clk_i) begin : prescaler
    if (!rst_n) begin
      us_cnt_r <= 32'd0;
      ms_cnt_r <= 32'd0;
      now_ms_r <= 32'd0;
    end else begin
      us_cnt_r <= tick_us_w ? 32'd0 : us_cnt_r + 32'd1;
      if (tick_us_w) begin
        ms_cnt_r <= tick_ms_w ? 32'd0 : ms_cnt_r + 32'd1;
      end
      if (tick_ms_w) begin
        now_ms_r <= now_ms_r + 32'd1;
      end
    end
  end

  assign tick_ms_o = tick_ms_w;
  assign now_ms_o  = now_ms_r;

  // -------------------------------------------------- deadline RAM (1W1R)
  // {owner, deadline_ms} only — 08 §5 sizes this at SLOTS_P x 40 b. The
  // arm port is the single writer; synchronous read feeds the sweep. No
  // reset on the array or its read register: both are part of the RAM.
  logic [SLOT_DW_C-1:0] slot_ram_r [0:SLOTS_P-1];
  logic [SLOT_DW_C-1:0] sweep_rdata_r;

  logic [SLOT_AW_C-1:0] sweep_addr_r;

  always_ff @(posedge clk_i) begin : slot_ram_write
    if (arm_valid_i && !arm_cancel_i) begin
      slot_ram_r[arm_slot_i] <= {arm_owner_i, arm_deadline_ms_i};
    end
  end

  always_ff @(posedge clk_i) begin : slot_ram_read
    sweep_rdata_r <= slot_ram_r[sweep_addr_r];
  end

  // ------------------------------------------------------- sweep control
  // One slot per cycle after each ms tick; a tick during a sweep sets
  // pend and the sweep re-runs once it finishes (expiries deferred, never
  // lost). Read pipeline: addr at cycle n, data + check at cycle n+1.
  logic sweep_act_r;
  logic sweep_pend_r;
  logic                 chk_valid_r;
  logic [SLOT_AW_C-1:0] chk_slot_r;

  always_ff @(posedge clk_i) begin : sweep_ctrl
    if (!rst_n) begin
      sweep_act_r  <= 1'b0;
      sweep_pend_r <= 1'b0;
      sweep_addr_r <= '0;
      chk_valid_r  <= 1'b0;
      chk_slot_r   <= '0;
    end else begin
      chk_valid_r <= sweep_act_r;
      chk_slot_r  <= sweep_addr_r;
      if (sweep_act_r) begin
        if (sweep_addr_r == SLOT_AW_C'(SLOTS_P - 32'd1)) begin
          sweep_act_r  <= 1'b0;
          sweep_addr_r <= '0;
        end else begin
          sweep_addr_r <= sweep_addr_r + SLOT_AW_C'(1);
        end
        if (tick_ms_w) begin
          sweep_pend_r <= 1'b1;  // tick mid-sweep: re-run afterwards
        end
      end else if (tick_ms_w || sweep_pend_r) begin
        sweep_act_r  <= 1'b1;
        sweep_pend_r <= 1'b0;
      end
    end
  end

  // ------------------------------------------------- expiry + armed bits
  // Wrap-safe: expired when the modular age (now - deadline) is not
  // negative, i.e. its MSB is clear — absolute deadlines compare correctly
  // across the 32-bit ms rollover (~49.7 days).
  logic [pp_pkg::PP_TIMER_OWNER_W_C-1:0] chk_owner_w;
  logic [31:0]                           chk_deadline_w;
  logic [31:0]                           age_w;
  logic                                  exp_fire_w;

  logic [SLOTS_P-1:0] armed_r;

  // arm shadow: an arm/cancel to the slot under check — this cycle or the
  // previous one (its RAM write raced the sweep's read of that address) —
  // must not fire on stale data; the slot re-evaluates next sweep.
  logic                 arm_q_valid_r;
  logic [SLOT_AW_C-1:0] arm_q_slot_r;
  logic                 arm_shadow_w;

  always_ff @(posedge clk_i) begin : arm_shadow
    if (!rst_n) begin
      arm_q_valid_r <= 1'b0;
      arm_q_slot_r  <= '0;
    end else begin
      arm_q_valid_r <= arm_valid_i;
      arm_q_slot_r  <= arm_slot_i;
    end
  end

  assign arm_shadow_w = (arm_valid_i   && (arm_slot_i   == chk_slot_r))
                     || (arm_q_valid_r && (arm_q_slot_r == chk_slot_r));

  assign {chk_owner_w, chk_deadline_w} = sweep_rdata_r;
  assign age_w      = now_ms_r - chk_deadline_w;
  assign exp_fire_w = chk_valid_r && armed_r[chk_slot_r] && !age_w[31]
                      && !arm_shadow_w;

  always_ff @(posedge clk_i) begin : armed_flags
    if (!rst_n) begin
      armed_r <= '0;
    end else begin
      if (exp_fire_w) begin
        armed_r[chk_slot_r] <= 1'b0;   // an expired slot disarms itself
      end
      if (arm_valid_i) begin
        armed_r[arm_slot_i] <= !arm_cancel_i;  // arm/cancel wins a collision
      end
    end
  end

  assign exp_valid_o = exp_fire_w;
  assign exp_slot_o  = chk_slot_r;
  assign exp_owner_o = chk_owner_w;

endmodule : KL_pp_timer_service
`default_nettype wire

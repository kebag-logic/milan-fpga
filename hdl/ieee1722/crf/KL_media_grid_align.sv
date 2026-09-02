// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
/*
------------------------------------------------------------------------------
  File        : KL_media_grid_align.sv
  Project     : Milan AVTP media clock (#74 grid alignment)

  Description : Phase servo that makes the packet grid (KL_media_nco's
                tick_o) FOLLOW the physical audio grid (the front-end's
                frame marker), bounded-phase, when a CRF clock source is
                selected.

                WHY IT EXISTS. The datapath runs two 48 kHz grids: the
                physical one (clk_tdm_i through the TDM master's integer
                divider - 47,999.4893 Hz on the shipping divider plan) and
                the packet one (the NCO's exact 48,000.0000 Hz off the
                datapath clock). They meet at latest-sample holds in
                KL_chan_map_capture, where their -10.64 ppm difference slips
                one whole frame every ~1.96 s (bench 2026-08-10; the
                tdm_dup/tdm_skip counters there are this defect's
                observable). The MMCM servo cannot close that gap: it steers
                the physical clock toward CRF, and the NCO mirrors its
                COMMAND, so both grids move together and their NOMINAL
                offset survives.

                THE REFERENCE CHAIN (#74's phase contract, TIME_SYNC.md):
                CRF -> KL_mmcm_drp_servo (hardware, bench-measurable) ->
                clk_audio/clk_tdm -> fsync -> THIS MODULE (arithmetic,
                sim-provable) -> media_tick_p. A chain, not a fork: each
                grid has exactly one master, and each link is falsifiable
                on its own (the servo's status slice under CRF stimulus;
                this loop's bounded phase under the true 391/1591 ratio;
                the J11.8-vs-J11.9 bench probe for the silicon whole).

                clock_source = INTERNAL never reaches this module: sel_i is
                the live CRF selection, and 0 disengages everything, keeping
                the NCO's bit-exact free-run (USER rule: internal media
                clock = free-run, slips accepted - KL_media_nco.sv).

                DETECTOR. A free-running time-since-tick counter is captured
                at each frame marker: at lock that capture is a constant.
                The error is the PLAIN difference against the reference
                captured at engagement, unwrapped by a TRACKING fold: each
                frame picks whichever whole-sample fold lands nearest the
                previous error (exact, because authority caps the true
                per-frame phase step at ~0.4 cycles - see the in-body note
                for the two folding schemes this replaced and why each
                failed). Resolution is one clk_i cycle = 1/DIV_C sample
                (~0.05% of a sample), which is what lets the loop hold the
                phase strictly inside one sample - an integer frame/tick
                detector could not.

                LOOP. PI in NCO servo units (1/16 ppm per LSB, the
                KL_mmcm_drp_servo convention KL_media_nco rescales
                internally; POSITIVE u = SPEED UP, the datapath negation is
                the NCO's own). u_p = clamp(err << KP_LOG2_P); the plant
                gain is DIV_C/16e6 cycles-per-frame per LSB, so at the
                shipping 100 MHz / 48 kHz shape KP_LOG2_P = 2 puts the
                proportional equilibrium for the full -10.64 ppm plan at
                ~42 cycles = 0.02 samples: the phase is bounded WELL inside
                a sample from the first frames, before the integrator has
                moved at all. The integrator (Ki = 2^-KI_LOG2_P per frame)
                then walks the residual to zero; its zero sits a decade
                under the proportional crossover, so the loop is
                overdamped, and both terms clamp at U_LIM_P (200 ppm - the
                actuators' shared authority class) so windup cannot outrun
                the NCO's own clamp.

                FEED WATCHDOG. No frame marker for TIMEOUT_C cycles (a dead
                TDM plane, a bench without the audio clock) = disengage:
                u -> 0, the NCO free-runs at nominal, and the next frame
                re-engages from a fresh reference. A CRF-selected build
                with no physical feed therefore degrades to today's exact
                behaviour rather than stalling or running away.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Bounded-phase follower: the packet grid tracks the physical frame
//! marker while sel_i holds, free-runs otherwise.

`default_nettype none

module KL_media_grid_align #(
  parameter int unsigned CLK_FREQ_HZ_P = 100_000_000, //! datapath clock (Hz)
  parameter int unsigned FS_HZ_P       = 48_000,      //! nominal sample rate
  parameter int unsigned KP_LOG2_P     = 2,   //! u_p = err << KP_LOG2_P
  parameter int unsigned KI_LOG2_P     = 12,  //! acc >> KI_LOG2_P per frame
  //! |u| clamp in 1/16 ppm LSB: 3200 = 200 ppm, the MMCM/NCO authority class
  parameter int unsigned U_LIM_P       = 3200
)(
  input  wire                 clk_i,     //! datapath clock
  input  wire                 rst_n,     //! active-low synchronous reset
  input  wire                 sel_i,     //! live CRF selection; 0 = disengage
  input  wire                 frame_ev_i,//! physical-grid frame marker pulse
  input  wire                 tick_i,    //! the NCO's tick_o
  //! to KL_media_nco.servo_trim_i (positive = speed up; the NCO negates)
  output logic signed [15:0]  u_o,
  output logic                engaged_o, //! reference captured, loop closed
  //! signed phase error in clk_i cycles (+ = frames lead), tb/CSR evidence
  output logic signed [15:0]  err_o
);

  localparam int unsigned DIV_C     = CLK_FREQ_HZ_P / FS_HZ_P;
  localparam int unsigned TSTW_C    = $clog2(2 * DIV_C);
  //! 4 nominal frame periods of silence = the feed is dead
  localparam int unsigned TIMEOUT_C = 4 * DIV_C;
  localparam int unsigned TOW_C     = $clog2(TIMEOUT_C + 1);
  //! whole-sample slip fold: bounded so err_o cannot wrap its width even
  //! with the fold saturated in one direction
  localparam int signed   SLIP_LIM_C = 8;
  localparam int unsigned ACCW_C    = 32;

  if (DIV_C < 16)
    $error("KL_media_grid_align: CLK_FREQ_HZ_P/FS_HZ_P = %0d leaves the detector under 4 bits of sub-sample resolution - this loop cannot bound phase inside a sample there.", DIV_C);
  if ((SLIP_LIM_C + 2) * DIV_C > 32767)
    $error("KL_media_grid_align: DIV_C=%0d puts the saturated fold plus the capture span past err_o's 16-bit range - the truncation would wrap the error sign. Lower SLIP_LIM_C or widen err_o.", DIV_C);
  if (U_LIM_P > 32767 - (2 * DIV_C << KP_LOG2_P))
    $error("KL_media_grid_align: U_LIM_P=%0d cannot absorb a pre-clamp proportional term of +/-%0d without widening u_o.", U_LIM_P, 2 * DIV_C << KP_LOG2_P);

  // ---------------------------------------------------------------------- //
  // Detector: time-since-tick capture + a TRACKING UNWRAPPER               //
  // ---------------------------------------------------------------------- //
  // Two dead ends are recorded here because each one PASSED a desk check
  // and only the closed-loop suite caught it:
  //   1. wrapping (capture - ref) at +/-DIV_C/2: the wrap fires half a
  //      period away from where whole-sample events fold, so the composite
  //      jumps a full period at every crossing;
  //   2. folding on the junction counters' pend/consume law: a coincident
  //      frame+tick consumes WITHOUT folding, and a converged loop sits
  //      exactly where pulses coincide - each coincidence injected a
  //      +/-DIV_C phantom and the loop parked at its clamp.
  // The unwrapper below has neither mode: at each frame it picks the fold
  // (slip_r - 1, slip_r, slip_r + 1) whose error lands NEAREST the previous
  // error. That is exact, not heuristic: the true phase moves well under
  // half a period per frame (authority caps the loop at +/-200 ppm =
  // +/-0.42 cycles per frame, jitter adds one), so the nearest candidate is
  // always the true one, and no pulse alignment can fool it.
  logic [TSTW_C-1:0]        tst_r;       //! clk cycles since the last tick
  logic [TSTW_C-1:0]        ref_r;       //! capture at engagement
  logic signed [4:0]        slip_r;      //! whole-sample fold (+ = ticks lead)
  logic [TOW_C-1:0]         quiet_r;     //! cycles since the last frame
  logic                     engaged_r;

  assign engaged_o = engaged_r;

  wire [TSTW_C-1:0] tst_next_w = tick_i ? '0
                               : (tst_r == TSTW_C'(2 * DIV_C - 1))
                                 ? tst_r : tst_r + 1'b1;

  logic signed [15:0] err_r;
  assign err_o = err_r;

  // ---------------------------------------------------------------------- //
  // PI, updated once per frame event                                        //
  // ---------------------------------------------------------------------- //
  logic signed [ACCW_C-1:0] acc_r;

  function automatic logic signed [15:0] clamp_u(input logic signed [31:0] v);
    begin
      if      (v >  32'(signed'(U_LIM_P))) clamp_u =  16'(signed'(U_LIM_P));
      else if (v < -32'(signed'(U_LIM_P))) clamp_u = -16'(signed'(U_LIM_P));
      else                                 clamp_u = 16'(v);
    end
  endfunction

  //! anti-windup: the integral TERM alone may just reach the output clamp,
  //! never beyond it - a feed that stays wrong (a harness at a wild rate)
  //! parks the loop at the clamp and recovers in frames, not seconds
  localparam logic signed [ACCW_C-1:0] ACC_LIM_C =
      ACCW_C'(signed'(U_LIM_P)) <<< KI_LOG2_P;
  function automatic logic signed [ACCW_C-1:0]
      clamp_acc(input logic signed [ACCW_C-1:0] v);
    begin
      if      (v >  ACC_LIM_C) clamp_acc =  ACC_LIM_C;
      else if (v < -ACC_LIM_C) clamp_acc = -ACC_LIM_C;
      else                     clamp_acc = v;
    end
  endfunction

  //! plain signed capture-minus-reference (no wrap - see the banner above)
  wire signed [31:0] fine_w = 32'(signed'({1'b0, tst_next_w}))
                            - 32'(signed'({1'b0, ref_r}));
  //! the three fold candidates and the tracking choice: nearest to err_r
  wire signed [31:0] base_w  = 32'(slip_r) * 32'(signed'(DIV_C)) + fine_w;
  wire signed [31:0] diff_w  = base_w - 32'(err_r);
  wire fold_dn_w = (diff_w >  32'(signed'(DIV_C / 2)))
                   && (slip_r > -5'(signed'(SLIP_LIM_C)));
  wire fold_up_w = (diff_w < -32'(signed'(DIV_C / 2)))
                   && (slip_r <  5'(signed'(SLIP_LIM_C)));
  wire signed [31:0] err_w = fold_dn_w ? base_w - 32'(signed'(DIV_C))
                           : fold_up_w ? base_w + 32'(signed'(DIV_C))
                                       : base_w;

  always_ff @(posedge clk_i) begin : align_loop
    if (!rst_n) begin
      tst_r     <= '0;
      ref_r     <= '0;
      slip_r    <= '0;
      quiet_r   <= '0;
      engaged_r <= 1'b0;
      err_r     <= '0;
      acc_r     <= '0;
      u_o       <= '0;
    end
    else if (!sel_i) begin
      //! INTERNAL selected: full disengage, free-run at nominal
      tst_r     <= tst_next_w;
      slip_r    <= '0;
      quiet_r   <= '0;
      engaged_r <= 1'b0;
      err_r     <= '0;
      acc_r     <= '0;
      u_o       <= '0;
    end
    else if (!engaged_r || quiet_r >= TOW_C'(TIMEOUT_C)) begin
      //! CRF selected but not (or no longer) locked to a feed: hold the
      //! safe state - u at 0, the NCO free-runs at nominal - and close the
      //! loop on the next frame with a FRESH reference. Freshly-selected
      //! and feed-died land here on the same terms, so re-engagement can
      //! never run against a stale reference.
      tst_r     <= tst_next_w;
      slip_r    <= '0;
      quiet_r   <= frame_ev_i ? '0
                 : (quiet_r >= TOW_C'(TIMEOUT_C)) ? quiet_r : quiet_r + 1'b1;
      engaged_r <= frame_ev_i;
      err_r     <= '0;
      acc_r     <= '0;
      u_o       <= '0;
      if (frame_ev_i) ref_r <= tst_next_w;
    end
    else begin
      tst_r   <= tst_next_w;
      quiet_r <= frame_ev_i ? '0 : quiet_r + 1'b1;
      if (frame_ev_i) begin
        if      (fold_dn_w) slip_r <= slip_r - 1'b1;
        else if (fold_up_w) slip_r <= slip_r + 1'b1;
        err_r <= 16'(err_w);
        //! CONDITIONAL integration, not just a clamp: while the output sits
        //! at a rail and the error still pushes past it (a feed beyond the
        //! +/-200 ppm authority), integrating only stores up windup that
        //! recovery must bleed back at the loop's own slow time constant
        //! (~1.5 s, measured by [G6]'s first cut). Freezing the integrator
        //! in exactly that state makes recovery a re-acquisition - a few
        //! thousand frames - while every in-authority state integrates as a
        //! plain PI.
        if (!((u_o == -16'(signed'(U_LIM_P)) && err_w > 0)
              || (u_o == 16'(signed'(U_LIM_P)) && err_w < 0)))
          acc_r <= clamp_acc(acc_r + ACCW_C'(err_w));
        //! NEGATED: err > 0 = the tick grid runs fast (captures drift up),
        //! and u > 0 = SPEED UP at the NCO port - a positive error must
        //! command a slow-down. The unit suite pins this with a closed loop
        //! in both rate directions; getting it wrong is a runaway, not a
        //! wrong number (KL_media_nco's own sign lesson).
        u_o   <= clamp_u((err_w <<< KP_LOG2_P) * -1
                         - 32'(acc_r >>> KI_LOG2_P));
      end
    end
  end : align_loop

endmodule

`default_nettype wire

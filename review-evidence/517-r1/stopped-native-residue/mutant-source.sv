/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_gptp_txret.sv
  Description : The gPTP plane's EGRESS TIMESTAMP LEDGER (issue #360). It
                owns one ordered entry per admitted frame, reconstructs each
                frame's launch instant from the PHC value captured when its
                launch record crossed into this domain, and hands the engine
                exactly one result per admitted frame - measured, or an
                explicit loss.

                IDENTITY IS POSITION, NOT TAG. KL_gptp_txticket creates one
                ledger entry at the accepted end of each frame's last byte,
                in the order the engine committed the frames. The observer
                counts the frames it attributes at the wire, in the same
                order, because from the byte face to the observation point
                the path is one lane, frame-locked, first in first out, with
                no drop path. The two counts are the SAME per-frame ordinal
                derived independently at the two ends, so a record is
                credited to the frame at the ledger head and the tag
                comparison is an additional check on an identity that is
                already established - not the identity itself. That is what
                makes several live frames carrying the same legal wire tag
                unambiguous, which a set of tags can never be.

                CANCELLATION MARKS, IT NEVER REMOVES. When the plane can no
                longer trust the association context it clears an entry's
                `live` flag and leaves the entry exactly where it is. An
                entry leaves the ledger head only by its own record, or by
                proved destruction, or by a root reset that returns nothing
                and says so. Removing an entry early - which is what
                delivering a loss at cancellation time does - releases
                ownership of a frame whose bytes are still in the transport,
                and the next record then lands on somebody else's entry.

                WHY A RECORD NEEDS A DEPARTED FRAME. A record can only be
                credited to a frame the plane has actually handed to the MAC.
                `n_dep_i`, which KL_gptp_shadow counts at the plane's own
                egress, is that positive gate: without it a record could be
                credited to an entry whose frame is still sitting in the
                plane's transmit FIFO.

                AGE IS A DIAGNOSTIC. The head entry's age is counted and
                published, and it retires nothing. A timeout does not prove
                that a frame cannot still launch, and the only identity a
                surviving frame has is the entry a timeout would remove.

                THE RECONSTRUCTION, and where every term comes from. The
                observer measures the frame's reference octet against its own
                transmit clock and hands the record across a request/
                acknowledge crossing. The PHC value this module registers on
                the destination edge therefore represents an instant a fixed
                number of register stages after the launch:

                  (delta + OBS_LAT_E_CYC_P) transmit cycles  observer pipeline
                  CDC_LAT_D_CYC_P fabric cycles              crossing pipeline
                  half a fabric tick                     mean of the uniform
                                                         sampling phase

                Every term is a named parameter and the sum is derived, so a
                missing term is an elaboration fact rather than a silent bias
                a bench with a wide enough window would absorb.

  Spec refs   : IEEE Std 802.1AS-2020 11.3.9 (the message timestamp point of
                a transmitted event message is the beginning of the first
                symbol following the start-of-frame delimiter - the instant
                every result below is reconstructed to);
                docs/design/GPTP_PLANE.md; docs/litex/CLOCK_DOMAINS.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

//! Own one ordered ledger entry per admitted gPTP frame, reconstruct each
//! frame's launch instant, and serve the engine's result face.
//!
//! **Key Features**
//! - Ordered ledger: cancellation marks an entry and never removes it.
//! - Positional matching with generation, index and departure checks, and a
//!   tag comparison as a cross-check rather than as the identity.
//! - Bounded result queue sized by the same conservation equation the
//!   admission credit is derived from.

`default_nettype none

module KL_gptp_txret #(
    //! live egress identities this plane supports at once
    parameter int unsigned TXTS_CAP_N_P     = 8,
    parameter int unsigned TXTS_OIDX_W_P    = 12,
    parameter int unsigned TXTS_GEN_W_P     = 4,
    parameter int unsigned TXTS_DELTA_W_P   = 8,
    //! transmit-clock period, nanoseconds: the 1 Gb/s GMII shape
    parameter int unsigned ETH_TICK_NS_P    = 8,
    //! fabric clock period, nanoseconds: MILAN_CLK_FREQ_HZ = 50 MHz
    parameter int unsigned DP_TICK_NS_P     = 20,
    //! observer pipeline, transmit cycles, from the tag octet to the cycle
    //! the crossing source latches the record
    parameter int unsigned OBS_LAT_E_CYC_P  = 2,
    //! crossing pipeline, fabric cycles, from the synchronised request to
    //! the edge this module registers the PHC on
    parameter int unsigned CDC_LAT_D_CYC_P  = 2,
    //! the only cycle distance a whole frame can produce
    parameter int unsigned TXTS_DELTA_EXP_P = 45,
    //! consecutive ELIGIBLE fabric cycles a capture needs behind it. It
    //! has to cover the whole reconstructed interval plus every
    //! synchroniser stage between a control change and its effect, so a
    //! trajectory the model does not describe can never be inside the
    //! window a timestamp was reconstructed across.
    parameter int unsigned RECON_GUARD_CYC_P = 64,
    //! the relative frequency envelope, in parts per million, the
    //! published error budget's two frequency terms are computed at. It is
    //! a DECLARED DESIGN CONSTRAINT swept in the bench, not a measured
    //! property of any board's oscillators, and the applied PHC rate is
    //! held to it rather than assumed to obey it.
    parameter int unsigned RECON_REL_PPM_P  = 200,
    //! this plane's clock, the same number the producer's micro-code
    //! generator is given. The addend envelope below is derived from it
    //! rather than from the tick, so it is THE SAME QUANTITY the
    //! producer's own servo integrator is clamped to: the plane then
    //! refuses exactly the steady rates its producer refuses to ask for,
    //! and a transient proportional excursion past that clamp is a
    //! counted loss rather than a plausible wrong timestamp.
    parameter int unsigned PHC_CLK_HZ_P     = 50_000_000,
    //! head-entry age that raises the counted stall diagnostic. It retires
    //! nothing; see the banner.
    parameter int unsigned STALL_AGE_CYC_P  = 1_000_000,
    //! fabric cycles between two offers of the seal to the observer. The
    //! crossing's destination side is in the observer's reset domain, so an
    //! offer made while the observer is held in reset is simply not seen and
    //! the next one carries the same generation.
    parameter int unsigned SEAL_RETRY_CYC_P = 256,
    //! THE BOARD'S EGRESS LATENCY, nanoseconds (issue #358): the physical
    //! transmit path beyond this reconstruction's reference plane. The
    //! reconstruction below lands on the frame's LAUNCH as the observer saw
    //! it, one register stage before the pads; the wire departure is that
    //! much LATER, so the published t1 is EARLY by this constant and the
    //! constant is ADDED. It is a per-board fact the builder carries from
    //! the board configuration, not a measured property of this logic, so
    //! it is kept OUT of the derived digital correction below and folded
    //! into the same single subtraction. Zero reproduces the uncorrected
    //! reconstruction bit for bit.
    parameter int unsigned EGRESS_LAT_NS_P = 0,
    //! fabric cycles between two recovery requests while a demand is
    //! unmet. It is a REQUEST CADENCE and never a completion authority:
    //! nothing is resolved or unsealed because this expired. It exists so
    //! a request the guard could not accept - because it was busy, or
    //! because the firmware's own manual level masked the edge - is tried
    //! again instead of being lost, and so the request line spends most of
    //! its time low, which is what lets the guard's edge detector re-arm.
    parameter int unsigned RECOV_RETRY_CYC_P = 1024
) (
    input  wire clk_i,                 //! plane clock (axis_clk)
    input  wire rst_n,                 //! synchronous active-low reset

    //! the live PHC, in this clock's domain
    input  wire [63:0] phc_ns_i,

    //! THE COUNTER'S OWN EFFECTIVE CONTROL NETS - the five signals that
    //! literally drive `timestamp_counter`, in ITS clock domain, after
    //! every synchroniser. Not the CSR side and not the plane's own
    //! upstream addend: both of those change before the counter applies
    //! them, so a reconstruction qualified against them would call a
    //! window eligible while the accumulator was still on the old
    //! trajectory - or ineligible while it was not. The whole point of
    //! this qualification is that it describes what the accumulator DID.
    input  wire        phc_en_eff_i,        //! counter enable, effective
    input  wire [31:0] phc_incr_eff_ns_i,   //! Q8.24 nominal step, ns
    input  wire signed [31:0] phc_adj_eff_ns_i, //! Q8.24 signed addend, ns
    input  wire        phc_load_eff_i,      //! settime applied here
    input  wire        phc_adjust_eff_i,    //! adjtime applied here

    //! allocation from KL_gptp_txticket, one per admitted frame
    input  wire        alloc_i,
    input  wire  [3:0] alloc_type_i,
    input  wire [15:0] alloc_seq_i,
    input  wire        alloc_tagged_i,
    //! the allocator's own occupancy, for the conservation invariant
    input  wire [$clog2(TXTS_CAP_N_P + 1):0] outstanding_i,

    //! launch records from KL_gptp_gmii_launch, already in this domain
    input  wire                      rec_valid_i,
    input  wire                      rec_kind_i,   //! 0 = frame, 1 = echo
    input  wire [TXTS_OIDX_W_P-1:0]  rec_oidx_i,   //! observer position
    input  wire  [TXTS_GEN_W_P-1:0]  rec_gen_i,    //! adopted generation
    input  wire                [3:0] rec_type_i,   //! messageType octet
    input  wire               [15:0] rec_seq_i,    //! the frame's sequenceId
    input  wire [TXTS_DELTA_W_P-1:0] rec_delta_i,  //! measured cycle distance
    input  wire                      rec_abort_i,  //! no measurement here

    //! frames this plane has handed to the MAC and not yet resolved
    input  wire [$clog2(TXTS_CAP_N_P + 1):0] n_dep_i,
    //! one pulse per resolution, so the shadow can retire its departure
    output logic dep_take_o,

    //! THE DEPARTURE FENCE. `egress_hold_o` asks the plane to stop its own
    //! egress at a frame boundary; `fence_held_i` reports that it has, with
    //! any torn frame already discarded and counted as departed. The fence
    //! is what splits the ledger into the entries a recovery episode will
    //! destroy and the entries still whole inside the plane.
    output logic egress_hold_o,
    input  wire  fence_held_i,

    //! the seal offered to the observer, and the crossing's delivery report
    output logic                    seal_req_o,
    output logic [TXTS_GEN_W_P-1:0] seal_gen_o,
    input  wire                     seal_ack_i,

    //! MAC recovery levels, the barrier trigger. They are LEVELS and
    //! nothing more: `mac_reinit_i` also carries the firmware's own manual
    //! request, so neither of them can tell a completed episode from an
    //! aborted one. That is what the three episode signals below are for.
    input  wire mac_reinit_i,
    input  wire mac_eth_rst_i,
    //! the link guard's own episode evidence, and whether it is disabled
    input  wire epi_start_i,
    input  wire epi_done_i,
    input  wire epi_busy_i,
    //! the guard is disabled: it will refuse every trigger, so a request
    //! would only put a one-cycle pulse on the shared manual net and
    //! disturb the MAC system side for nothing. The demand stands and the
    //! seal stays closed, which is the stated behaviour for a disabled
    //! guard; re-enabling it is what lets the demand make progress.
    input  wire epi_dis_i,
    //! one-cycle recovery request, OR-ed into the guard's manual trigger
    output logic recov_req_o,

    //! the engine's result face (FPGA-gPTP #31): the whole tuple is held
    //! until the engine takes it
    output logic        txts_valid_o,
    input  wire         txts_ready_i,
    output logic [63:0] txts_ns_o,
    output logic [15:0] txts_seq_o,
    output logic  [3:0] txts_type_o,
    output logic        txts_ok_o,
    output logic [TXTS_GEN_W_P-1:0] txts_gen_o,

    //! hold the admission credit low: the plane is sealed
    output wire  credit_hold_o,
    //! one pulse per result the engine accepted
    output wire  res_accept_o,

    //! results retired without a measurement, every counted cause
    output logic [15:0] dbg_lost_o,
    //! records taken off the crossing and discarded
    output logic [15:0] dbg_disc_o,
    //! barriers raised
    output logic [15:0] dbg_barrier_o,
    //! head-entry age expiries: a diagnostic, never a retirement
    output logic [15:0] dbg_stall_o,
    //! results refused because the PHC trajectory across the reconstructed
    //! interval was not the one the model describes
    output logic [15:0] dbg_phc_lost_o,
    //! the history guard itself: how many more eligible cycles a capture
    //! still needs behind it. Published so a bench can prove the reload
    //! and the countdown rather than infer them from the refusals.
    output wire   [7:0] dbg_phc_dirty_cyc_o,
    //! {seal, echo established, ledger occupancy}
    output wire  [15:0] dbg_state_o
);

  // ======================================================================= //
  //  Derived constants                                                      //
  // ======================================================================= //
  //! THE DIGITAL CORRECTION, derived from the register stages above rather
  //! than written down. Removing any term changes this number, which is what
  //! makes a dropped stage a measurable bias instead of a comment.
  localparam int unsigned TXTS_CORR_NS_P =
      (TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P) * ETH_TICK_NS_P
    + CDC_LAT_D_CYC_P * DP_TICK_NS_P
    + DP_TICK_NS_P / 2;
  //! ...and what the single subtraction below actually removes: the digital
  //! correction MINUS the board's egress latency (issue #358), because
  //! subtracting less is adding. Kept as one SIGNED constant so a board
  //! whose physical transmit path exceeds the digital stages still lands on
  //! one subtractor at the same width, and so the digital term above stays
  //! readable as the derived sum of register stages it is.
  localparam longint signed TXTS_NET_NS_C =
      longint'(TXTS_CORR_NS_P) - longint'(EGRESS_LAT_NS_P);

  localparam int unsigned PTR_W_C = $clog2(TXTS_CAP_N_P);
  localparam int unsigned OCC_W_C = $clog2(TXTS_CAP_N_P + 1) + 1;
  localparam int unsigned AGE_W_C = $clog2(STALL_AGE_CYC_P + 1);
  localparam int unsigned SRT_W_C = $clog2(SEAL_RETRY_CYC_P + 1);
  localparam int unsigned RTW_C   = $clog2(RECOV_RETRY_CYC_P + 1);
  localparam int unsigned GDW_C   = $clog2(RECON_GUARD_CYC_P + 1);
  //! THE NOMINAL INCREMENT, DERIVED. `timestamp_counter` adds a Q8.24
  //! nanosecond step every enabled tick, so at this plane's tick the
  //! nominal step is the tick itself in that format. A mirrored literal
  //! would go stale the first time the datapath clock moved, and that
  //! staleness would look exactly like a clock the model does not
  //! describe: every timestamp refused, for no visible reason.
  localparam logic [31:0] PHC_INCR_NOM_C = 32'(DP_TICK_NS_P << 24);
  //! ...and the addend envelope. An addend unit adds 2^-24 ns per tick,
  //! so `ppm` of relative frequency is `ppm * 2^24 * 1000 / clk_hz` units
  //! - the producer's generator computes its integrator clamp with
  //! exactly this expression, rounded the same way, which is why the two
  //! agree to the unit. Computed at 64 bits: the product overflows 32.
  localparam longint unsigned PHC_ADJ_MAX_C =
      (longint'(RECON_REL_PPM_P) * (longint'(1) << 24) * 1000
       + longint'(PHC_CLK_HZ_P) / 2) / longint'(PHC_CLK_HZ_P);

  // ---- elaboration contract ---------------------------------------------
  //! ONE format string per $error: later arguments print as values.
  if (TXTS_CAP_N_P < 6 || TXTS_CAP_N_P > 16) begin : g_refuse_cap
    $error("KL_gptp_txret: TXTS_CAP_N_P=%0d is outside the supported 6..16. The ledger and the result queue are both this deep and the conservation equation sizes them together.",
           TXTS_CAP_N_P);
  end else if (DP_TICK_NS_P == 0 || ETH_TICK_NS_P == 0)
  begin : g_refuse_ticks
    $error("KL_gptp_txret: ETH_TICK_NS_P=%0d and DP_TICK_NS_P=%0d must both be non-zero; the reconstruction is a sum of clock periods and a zero period would silently drop its whole term.",
           ETH_TICK_NS_P, DP_TICK_NS_P);
  end else if (TXTS_GEN_W_P < 2) begin : g_refuse_gen
    $error("KL_gptp_txret: TXTS_GEN_W_P=%0d leaves no non-zero generation to adopt; generation 0 is reserved for a crossing whose source was reset.",
           TXTS_GEN_W_P);
  end else if ((longint'(PHC_INCR_NOM_C) >> 24) != longint'(DP_TICK_NS_P))
  begin : g_refuse_incr
    $error("KL_gptp_txret: the derived nominal increment 0x%08x is not DP_TICK_NS_P=%0d nanoseconds in Q8.24. The eligibility test compares the counter's own increment against this value, so a mismatch would call every cycle ineligible and refuse every timestamp.",
           PHC_INCR_NOM_C, DP_TICK_NS_P);
  end else if (PHC_ADJ_MAX_C == 0) begin : g_refuse_envelope
    $error("KL_gptp_txret: the derived addend envelope is zero at PHC_CLK_HZ_P=%0d and RECON_REL_PPM_P=%0d, so any applied rate correction at all would be refused.",
           PHC_CLK_HZ_P, RECON_REL_PPM_P);
  end

  // ======================================================================= //
  //  Declarations (Vivado's front end refuses a use above a declaration)    //
  // ======================================================================= //
  logic  [3:0] led_type_r [0:TXTS_CAP_N_P-1];
  logic [15:0] led_seq_r  [0:TXTS_CAP_N_P-1];
  logic        led_tag_r  [0:TXTS_CAP_N_P-1];
  logic        led_live_r [0:TXTS_CAP_N_P-1];
  logic [PTR_W_C-1:0] led_head_r;
  logic [OCC_W_C-1:0] n_led_r;

  logic [63:0] res_ns_r   [0:TXTS_CAP_N_P-1];
  logic [15:0] res_seq_r  [0:TXTS_CAP_N_P-1];
  logic  [3:0] res_type_r [0:TXTS_CAP_N_P-1];
  logic        res_ok_r   [0:TXTS_CAP_N_P-1];
  logic [TXTS_GEN_W_P-1:0] res_gen_r [0:TXTS_CAP_N_P-1];
  logic [PTR_W_C-1:0] res_head_r;
  logic [OCC_W_C-1:0] n_res_r;

  logic                      cap_v_r;
  logic                      cap_kind_r;
  logic [TXTS_OIDX_W_P-1:0]  cap_oidx_r;
  logic  [TXTS_GEN_W_P-1:0]  cap_gen_r;
  logic                [3:0] cap_type_r;
  logic               [15:0] cap_seq_r;
  logic [TXTS_DELTA_W_P-1:0] cap_delta_r;
  logic                      cap_abort_r;
  logic               [63:0] cap_phc_r;
  //! was the PHC trajectory eligible across the whole window behind this
  //! capture?
  logic                      cap_elig_r;
  logic [GDW_C-1:0]          phc_dirty_r;
  logic                      phc_en_d_r;
  logic [31:0]               phc_incr_d_r;
  logic signed [31:0]        phc_adj_d_r;
  logic                      elig_d_r;
  logic [GDW_C-1:0]          dirty_d_r;

  logic [TXTS_GEN_W_P-1:0]  gen_r;
  logic [TXTS_OIDX_W_P-1:0] exp_oidx_r;
  logic                     seal_r;
  logic                     echo_ok_r;
  //! the pre-fence prefix: how many ledger entries had already been handed
  //! to the MAC when the fence closed, and whether that count is known yet
  logic [OCC_W_C-1:0]       n_pre_r;
  logic                     n_pre_v_r;
  logic                     fence_held_r;
  //! THE RECOVERY DEMAND. It is owed to the LATEST fence and it is only
  //! discharged by an episode that the guard actually accepted and
  //! sequenced to completion after that fence.
  logic                     demand_r;    //! a fence is owed an episode
  logic                     epi_cover_r; //! an episode that began after it
  logic                     destroyed_r; //! ...and completed its sequence
  logic [RTW_C-1:0]         retry_r;
  logic                     eth_rst_r;
  logic [SRT_W_C-1:0]       seal_tmr_r;
  logic [AGE_W_C-1:0]       age_r;
  logic                     mac_rst_r;

  logic barrier_w;
  logic resolve_w;
  logic push_res_w;
  logic [63:0] res_ns_w;
  logic        res_ok_w;

  // ======================================================================= //
  //  Ledger and result-queue index arithmetic (any capacity in 6..16)       //
  // ======================================================================= //
  //! modulo-capacity tail index, computed one bit wide so the wrap is a
  //! comparison rather than a truncation
  logic [PTR_W_C:0] led_tail_sum_w;
  logic [PTR_W_C-1:0] led_tail_w;
  assign led_tail_sum_w = {1'b0, led_head_r} + (PTR_W_C+1)'(n_led_r);
  assign led_tail_w = (led_tail_sum_w >= (PTR_W_C+1)'(TXTS_CAP_N_P))
                      ? PTR_W_C'(led_tail_sum_w - (PTR_W_C+1)'(TXTS_CAP_N_P))
                      : PTR_W_C'(led_tail_sum_w);

  logic [PTR_W_C:0] res_tail_sum_w;
  logic [PTR_W_C-1:0] res_tail_w;
  assign res_tail_sum_w = {1'b0, res_head_r} + (PTR_W_C+1)'(n_res_r);
  assign res_tail_w = (res_tail_sum_w >= (PTR_W_C+1)'(TXTS_CAP_N_P))
                      ? PTR_W_C'(res_tail_sum_w - (PTR_W_C+1)'(TXTS_CAP_N_P))
                      : PTR_W_C'(res_tail_sum_w);

  // ======================================================================= //
  //  PHC eligibility: the history the reconstruction is valid across       //
  // ======================================================================= //
  //! The reconstruction subtracts a fixed number of clock periods from a
  //! captured PHC value. That arithmetic is only true if the counter was
  //! running, at its nominal step, with a bounded addend, for the WHOLE
  //! interval it reaches back across - so eligibility is a property of a
  //! window of history and not of the capture instant. Subtracting a fixed
  //! nominal duration from a post-step value does not reconstruct a
  //! pre-step event, and no plausible-looking number is published for one.
  //!
  //! The guard is RELOADED on every ineligible cycle, on every change of
  //! the three continuous controls, and on either one-shot command, and it
  //! DECREMENTS ONLY WHILE ELIGIBLE. A disable held beyond the window
  //! keeps it loaded for the whole hold and for the window after it; an
  //! excessive addend restored just before a capture still fails, because
  //! the guard was reloaded while the excursion stood.
  logic signed [31:0] adj_eff_w;
  logic [31:0]        adj_abs_w;
  assign adj_eff_w = phc_adj_eff_ns_i;
  assign adj_abs_w = adj_eff_w[31] ? unsigned'(-adj_eff_w) : unsigned'(adj_eff_w);

  logic elig_now_w, phc_chg_w;
  assign elig_now_w = phc_en_eff_i
                   && (phc_incr_eff_ns_i == PHC_INCR_NOM_C)
                   && (longint'(adj_abs_w) <= PHC_ADJ_MAX_C);
  assign phc_chg_w  = (phc_en_eff_i   != phc_en_d_r)
                   || (phc_incr_eff_ns_i != phc_incr_d_r)
                   || (phc_adj_eff_ns_i  != phc_adj_d_r)
                   || phc_load_eff_i || phc_adjust_eff_i;

  always_ff @(posedge clk_i) begin : phc_history
    if (!rst_n) begin
      phc_dirty_r  <= GDW_C'(RECON_GUARD_CYC_P);
      phc_en_d_r   <= 1'b0;
      phc_incr_d_r <= 32'd0;
      phc_adj_d_r  <= 32'sd0;
      elig_d_r     <= 1'b0;
      dirty_d_r    <= GDW_C'(RECON_GUARD_CYC_P);
    end else begin
      phc_en_d_r   <= phc_en_eff_i;
      phc_incr_d_r <= phc_incr_eff_ns_i;
      phc_adj_d_r  <= phc_adj_eff_ns_i;
      elig_d_r     <= elig_now_w & ~phc_chg_w;
      dirty_d_r    <= phc_dirty_r;

      if (!elig_now_w || phc_chg_w)  phc_dirty_r <= GDW_C'(RECON_GUARD_CYC_P);
      else if (|phc_dirty_r)         phc_dirty_r <= phc_dirty_r - GDW_C'(1);

`ifndef SYNTHESIS
      //! the two behaviours the guard exists for, asserted directly rather
      //! than argued from the code above
      if (!elig_d_r && (phc_dirty_r != GDW_C'(RECON_GUARD_CYC_P)))
        $error("KL_gptp_txret: the PHC history guard did not reload while ineligible");
      if (!elig_d_r && (phc_dirty_r < dirty_d_r))
        $error("KL_gptp_txret: the PHC history guard decremented while ineligible");
`endif
    end
  end : phc_history

  // ======================================================================= //
  //  Record capture: the destination edge of the crossing                   //
  // ======================================================================= //
  //! The crossing presents `dest_req` across exactly one edge, and the PHC
  //! value present over that interval is the one written on the previous
  //! edge. Registering both here is what fixes `CDC_LAT_D_CYC_P`: change this
  //! stage and the correction above is wrong by a whole fabric tick.
  always_ff @(posedge clk_i) begin : record_capture
    if (!rst_n) begin
      cap_v_r     <= 1'b0;
      cap_kind_r  <= 1'b0;
      cap_oidx_r  <= '0;
      cap_gen_r   <= '0;
      cap_type_r  <= 4'd0;
      cap_seq_r   <= 16'd0;
      cap_delta_r <= '0;
      cap_abort_r <= 1'b0;
      cap_phc_r   <= 64'd0;
      cap_elig_r  <= 1'b0;
    end else begin
      cap_v_r <= rec_valid_i;
      if (rec_valid_i) begin
        //! the whole window behind this capture was inside the model
        cap_elig_r  <= (phc_dirty_r == GDW_C'(0));
        cap_kind_r  <= rec_kind_i;
        cap_oidx_r  <= rec_oidx_i;
        cap_gen_r   <= rec_gen_i;
        cap_type_r  <= rec_type_i;
        cap_seq_r   <= rec_seq_i;
        cap_delta_r <= rec_delta_i;
        cap_abort_r <= rec_abort_i;
        cap_phc_r   <= phc_ns_i;
      end
`ifndef SYNTHESIS
      if (rec_valid_i && cap_v_r)
        $error("KL_gptp_txret: a launch record arrived while the previous one was still being processed");
`endif
    end
  end : record_capture

  // ======================================================================= //
  //  Acceptance                                                             //
  // ======================================================================= //
  //! A frame record resolves the ledger head only if ALL of these hold. The
  //! order is the order a reviewer has to be able to check them in: the
  //! generation rejects a crossing replay, the position establishes which
  //! frame this is, the departure proves the frame left, and the tag is the
  //! cross-check on a position that is already established.
  logic gen_ok_w, oidx_ok_w, have_entry_w, departed_w, tag_ok_w;
  assign gen_ok_w     = (cap_gen_r != '0) && (cap_gen_r == gen_r);
  assign oidx_ok_w    = (cap_oidx_r == exp_oidx_r);
  assign have_entry_w = (n_led_r != OCC_W_C'(0));
  assign departed_w   = (n_dep_i != '0);
  assign tag_ok_w     = cap_abort_r
                     || ((cap_type_r == led_type_r[led_head_r]) &&
                         (cap_seq_r  == led_seq_r [led_head_r]));

  logic frame_rec_w, echo_rec_w;
  assign frame_rec_w = cap_v_r & ~cap_kind_r;
  assign echo_rec_w  = cap_v_r &  cap_kind_r;

  //! the echo establishes the observer position base and consumes no frame
  logic echo_take_w;
  assign echo_take_w = echo_rec_w & seal_r & (cap_gen_r == gen_r) &
                       (cap_gen_r != '0);

  assign resolve_w = frame_rec_w & ~seal_r & gen_ok_w & oidx_ok_w &
                     have_entry_w & departed_w & tag_ok_w;

  //! THE PRE-FENCE PREFIX, resolved in order and only as counted loss. Its
  //! frames are past this plane and their records can no longer be trusted
  //! to arrive, so each entry is closed with its OWN tag and no
  //! measurement. Nothing here is a timeout: the prefix is a count fixed at
  //! the fence, and it is only resolved once destruction is established.
  //! DESTRUCTION IS ESTABLISHED, not inferred. All four of these, together:
  //!  - an episode that BEGAN after this fence completed its full sequence
  //!    (`destroyed_r`), which a disable, a reset or an aborted episode can
  //!    never set, because the guard publishes completion on one path only;
  //!  - both recovery levels are low NOW, so a firmware hand still holding
  //!    LINK_CTRL[1] keeps the MAC system side in reset and keeps the seal
  //!    closed with it;
  //!  - the pre-fence prefix is known, which means the fence really closed;
  //!  - the observer has echoed THIS generation, so it is out of reset and
  //!    its position base is re-established.
  logic destroyed_w, pre_resolve_w;
  assign destroyed_w   = destroyed_r & ~mac_reinit_i & ~mac_eth_rst_i &
                         n_pre_v_r & echo_ok_r;
  assign pre_resolve_w = seal_r & destroyed_w & (n_pre_r != OCC_W_C'(0)) &
                         have_entry_w & departed_w;

  //! a frame record that is not credited is counted and discarded; a record
  //! that contradicts an established position is also an invariant
  //! violation and raises the barrier
  logic disc_w, mismatch_w;
  assign disc_w     = cap_v_r & ~resolve_w & ~echo_take_w;
  assign mismatch_w = frame_rec_w & ~seal_r &
                      (~gen_ok_w | ~oidx_ok_w | ~have_entry_w | ~tag_ok_w);

  // ======================================================================= //
  //  Reconstruction                                                         //
  // ======================================================================= //
  //! The head entry's outcome. Only a live, tagged entry whose record
  //! carries the expected cycle distance can produce a measurement; every
  //! other path delivers an explicit loss and is counted.
  assign res_ok_w = resolve_w & led_live_r[led_head_r] & led_tag_r[led_head_r] &
                    ~cap_abort_r & cap_elig_r &
                    (cap_delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P));
  //! a result refused ONLY because the trajectory was outside the model:
  //! the frame was whole and it was this entry's, and it still gets an
  //! explicit loss rather than a plausible wrong time
  logic phc_lost_w;
  assign phc_lost_w = resolve_w & led_live_r[led_head_r] & led_tag_r[led_head_r] &
                      ~cap_abort_r & ~cap_elig_r &
                      (cap_delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P));
  //! modular by construction: the PHC wraps and a launch a few hundred
  //! nanoseconds before a wrap must reconstruct to the value before it
  assign res_ns_w = res_ok_w ? (cap_phc_r - 64'(TXTS_NET_NS_C)) : 64'd0;

  assign push_res_w = resolve_w | pre_resolve_w;

  // ======================================================================= //
  //  Barrier                                                                //
  // ======================================================================= //
  //! The MAC recovery levels, as one trigger. A rising edge raises the
  //! barrier; the level is what the destruction evidence is read from.
  logic mac_rst_w;
  assign mac_rst_w = mac_reinit_i | mac_eth_rst_i;

  //! An echo outside a seal is not evidence that a frame was lost - the
  //! observer answers every generation it adopts and a re-offer in flight
  //! can land just after the seal lifts - so it is counted and discarded
  //! rather than treated as a barrier.
  //! A barrier while ALREADY SEALED is not a new fence: the egress has
  //! been held since the last one, so nothing has departed since and the
  //! prefix cannot have grown. Re-fencing on the very episode this module
  //! asked for is also how a recovery request turns into a self-trigger
  //! loop, which is why the edge is qualified on `~seal_r` rather than
  //! suppressed by a timer. What a reset DOES invalidate while sealed is
  //! handled separately below: an eth-side reset clears the observer, so
  //! its echo has to be earned again.
  assign barrier_w = (~seal_r & (mac_rst_w & ~mac_rst_r)) | mismatch_w;

  // ======================================================================= //
  //  The ledger                                                             //
  // ======================================================================= //


  always_ff @(posedge clk_i) begin : ledger
    if (!rst_n) begin
      led_head_r <= '0;
      n_led_r    <= OCC_W_C'(0);
      for (int unsigned li = 0; li < TXTS_CAP_N_P; li++) begin
        led_type_r[li] <= 4'd0;
        led_seq_r [li] <= 16'd0;
        led_tag_r [li] <= 1'b0;
        led_live_r[li] <= 1'b0;
      end
    end else begin
      //! CANCELLATION MARKS. A barrier clears the `live` flag of every
      //! entry that ALREADY EXISTS and removes none of them, so each
      //! admitted frame keeps its ordered owner and closes as a counted
      //! loss when its own record arrives or its destruction is proved.
      if (barrier_w) begin
        for (int unsigned li = 0; li < TXTS_CAP_N_P; li++) led_live_r[li] <= 1'b0;
      end

      //! one entry per admitted frame, in allocation order. An entry
      //! allocated AFTER the fence is live: the egress is held, so its
      //! frame cannot have departed, its record cannot arrive before the
      //! echo re-establishes the position base, and when it does arrive it
      //! is that frame's own. Written after the cancellation above so a
      //! frame admitted in the same cycle as a barrier is the new epoch's,
      //! not the old one's.
      if (alloc_i && (n_led_r != OCC_W_C'(TXTS_CAP_N_P))) begin
        led_type_r[led_tail_w] <= alloc_type_i;
        led_seq_r [led_tail_w] <= alloc_seq_i;
        led_tag_r [led_tail_w] <= alloc_tagged_i;
        led_live_r[led_tail_w] <= 1'b1;
      end

      //! resolution consumes the head, whichever kind it was
      if (resolve_w || pre_resolve_w) begin
        led_head_r <= (led_head_r == PTR_W_C'(TXTS_CAP_N_P - 1))
                      ? PTR_W_C'(0) : led_head_r + PTR_W_C'(1);
      end

      if (alloc_i && !(resolve_w || pre_resolve_w)) begin
        if (n_led_r != OCC_W_C'(TXTS_CAP_N_P)) n_led_r <= n_led_r + OCC_W_C'(1);
      end else if (!alloc_i && (resolve_w || pre_resolve_w)) begin
        n_led_r <= n_led_r - OCC_W_C'(1);
      end

`ifndef SYNTHESIS
      if (alloc_i && (n_led_r == OCC_W_C'(TXTS_CAP_N_P)))
        $error("KL_gptp_txret: an allocation arrived with the ledger full");
      if (outstanding_i != (n_led_r + n_res_r))
        $error("KL_gptp_txret: outstanding is not the ledger plus the result queue");
      if (n_dep_i > n_led_r)
        $error("KL_gptp_txret: more frames have departed than the ledger holds");
`endif
    end
  end : ledger

  // ======================================================================= //
  //  The result queue and the engine's face                                 //
  // ======================================================================= //
  assign res_accept_o = txts_valid_o & txts_ready_i;

  always_ff @(posedge clk_i) begin : result_queue
    if (!rst_n) begin
      res_head_r <= '0;
      n_res_r    <= OCC_W_C'(0);
      for (int unsigned li = 0; li < TXTS_CAP_N_P; li++) begin
        res_ns_r  [li] <= 64'd0;
        res_seq_r [li] <= 16'd0;
        res_type_r[li] <= 4'd0;
        res_ok_r  [li] <= 1'b0;
        res_gen_r [li] <= '0;
      end
    end else begin
      if (push_res_w) begin
        res_ns_r  [res_tail_w] <= res_ns_w;
        res_seq_r [res_tail_w] <= led_seq_r [led_head_r];
        res_type_r[res_tail_w] <= led_type_r[led_head_r];
        res_ok_r  [res_tail_w] <= res_ok_w;
        res_gen_r [res_tail_w] <= gen_r;
      end
      if (res_accept_o) begin
        res_head_r <= (res_head_r == PTR_W_C'(TXTS_CAP_N_P - 1))
                      ? PTR_W_C'(0) : res_head_r + PTR_W_C'(1);
      end
      if (push_res_w && !res_accept_o) begin
        n_res_r <= n_res_r + OCC_W_C'(1);
      end else if (!push_res_w && res_accept_o) begin
        n_res_r <= n_res_r - OCC_W_C'(1);
      end
`ifndef SYNTHESIS
      //! the conservation equation is what guarantees this can never happen,
      //! so it is asserted rather than handled
      if (push_res_w && (n_res_r == OCC_W_C'(TXTS_CAP_N_P)))
        $error("KL_gptp_txret: a resolution found the result queue full");
      //! and the qualification is structural, not advisory
      if (push_res_w && res_ok_w && !cap_elig_r)
        $error("KL_gptp_txret: a measurement was published across an ineligible PHC window");
`endif
    end
  end : result_queue

  assign txts_valid_o = (n_res_r != OCC_W_C'(0));
  assign txts_ns_o    = res_ns_r  [res_head_r];
  assign txts_seq_o   = res_seq_r [res_head_r];
  assign txts_type_o  = res_type_r[res_head_r];
  assign txts_ok_o    = res_ok_r  [res_head_r];
  assign txts_gen_o   = res_gen_r [res_head_r];

  assign dep_take_o    = resolve_w | pre_resolve_w;
  assign dbg_phc_dirty_cyc_o = 8'(phc_dirty_r);
  assign credit_hold_o = seal_r;

  // ======================================================================= //
  //  Generation, seal and the observer position base                        //
  // ======================================================================= //
  //! The plane starts SEALED: at a root reset the ledger is empty, the
  //! observer has not been reset with it, and the position base has to be
  //! re-established before any record can be credited.
  always_ff @(posedge clk_i) begin : seal_state
    if (!rst_n) begin
      gen_r      <= TXTS_GEN_W_P'(1);
      exp_oidx_r <= '0;
      seal_r     <= 1'b1;
      echo_ok_r  <= 1'b0;
      seal_tmr_r <= '0;
      seal_req_o <= 1'b0;
      seal_gen_o <= TXTS_GEN_W_P'(1);
      mac_rst_r  <= 1'b0;
      //! A ROOT RESET starts the plane sealed AND fenced. The ledger is
      //! empty, but the observer was not reset with it and the MAC path
      //! still holds whatever this plane handed over before the reset, so
      //! nothing may launch until the observer's position base is
      //! re-established. The pre-reset epoch is DISCARDED: its entries are
      //! gone and no result is promised for them.
      egress_hold_o <= 1'b1;
      n_pre_r       <= OCC_W_C'(0);
      n_pre_v_r     <= 1'b1;
      fence_held_r  <= 1'b0;
      //! Root startup follows the SAME rule. A root reset erases this
      //! plane's own state, but it does not clear the store-and-forward
      //! FIFO or the MAC core that still hold the frames this plane handed
      //! over before it, so an episode is owed here too. The only
      //! exception is the erased epoch itself: nothing is returned for an
      //! entry the reset removed, and the plane says so.
      demand_r     <= 1'b1;
      epi_cover_r  <= 1'b0;
      destroyed_r  <= 1'b0;
      retry_r      <= '0;
      recov_req_o  <= 1'b0;
      eth_rst_r    <= 1'b0;
    end else begin
      mac_rst_r    <= mac_rst_w;
      fence_held_r <= fence_held_i;
      eth_rst_r    <= mac_eth_rst_i;
      recov_req_o  <= 1'b0;

      // ---- the recovery demand ----------------------------------------
      //! AN EPISODE THAT STOPPED WITHOUT COMPLETING IS NOT EVIDENCE. The
      //! guard leaves its running state for a disable or a reset with both
      //! outputs low and no completion, which is precisely the abort that
      //! must not be mistaken for recovery. Withdraw the cover; the demand
      //! stays and is requested again. This is written FIRST so the two
      //! arms below, which describe an episode that is really happening,
      //! take precedence on the edges where both would apply.
      if (!epi_busy_i && !epi_done_i)     epi_cover_r <= 1'b0;
      //! An episode that begins while a demand is unmet is the one that
      //! covers this fence. An episode already running when the fence was
      //! taken is NOT: it cannot assert a reset after the fence, which is
      //! the whole point.
      if (epi_start_i && demand_r)        epi_cover_r <= 1'b1;
      //! ...and only its completion discharges anything.
      if (epi_done_i && epi_cover_r) begin
        destroyed_r <= 1'b1;
        epi_cover_r <= 1'b0;
      end
      //! An eth-side reset while sealed resets the observer with the MAC,
      //! so the generation it had adopted is gone and the echo has to be
      //! earned again.
      if (seal_r && mac_eth_rst_i && !eth_rst_r) echo_ok_r <= 1'b0;

      //! THE REQUEST. One cycle high, then low for a whole retry interval,
      //! so a guard that could not accept this edge - busy, or masked by a
      //! firmware level held on the same net - sees a fresh rising edge on
      //! the next attempt. An ignored pulse discharges nothing: `demand_r`
      //! is cleared by the unseal below and by nothing else.
      if (|retry_r) begin
        retry_r <= retry_r - RTW_C'(1);
      end else if (demand_r && !destroyed_r && !epi_cover_r && !epi_busy_i &&
                   !epi_dis_i) begin
        recov_req_o <= 1'b1;
        retry_r     <= RTW_C'(RECOV_RETRY_CYC_P);
      end

      //! The observer position advances on every frame record taken off the
      //! crossing, credited or not, so a discarded record does not break the
      //! continuity that detects a lost one.
      if (frame_rec_w) exp_oidx_r <= cap_oidx_r + TXTS_OIDX_W_P'(1);

      if (barrier_w) begin
        //! generation 1..max, never 0
        gen_r      <= (gen_r == {TXTS_GEN_W_P{1'b1}}) ? TXTS_GEN_W_P'(1)
                                                      : gen_r + TXTS_GEN_W_P'(1);
        seal_r     <= 1'b1;
        echo_ok_r  <= 1'b0;
        seal_req_o <= 1'b0;
        seal_tmr_r <= '0;
        //! TAKE THE FENCE. A NESTED barrier retakes it and forgets the
        //! prefix it had measured, because a count taken before this
        //! barrier does not describe what this one has to destroy - and it
        //! invalidates every piece of recovery evidence with it, because
        //! an episode that completed before this fence cannot have
        //! destroyed what departed after it.
        egress_hold_o <= 1'b1;
        n_pre_v_r     <= 1'b0;
        n_pre_r       <= OCC_W_C'(0);
        demand_r      <= 1'b1;
        epi_cover_r   <= epi_start_i;
        destroyed_r   <= 1'b0;
        retry_r       <= '0;
      end else begin
        //! the fence has closed: the prefix is exactly the entries already
        //! handed over, including any frame this plane had to tear
        if (fence_held_i && !fence_held_r && !n_pre_v_r) begin
          n_pre_r   <= n_dep_i;
          n_pre_v_r <= 1'b1;
        end
        if (pre_resolve_w && (n_pre_r != OCC_W_C'(0)))
          n_pre_r <= n_pre_r - OCC_W_C'(1);
        //! the echo establishes the base and is not a frame
        if (echo_take_w) begin
          exp_oidx_r <= cap_oidx_r;
          echo_ok_r  <= 1'b1;
        end

        //! Re-offer the seal until the echo answers. The offer has to go low
        //! between attempts: the crossing latches on the RISING edge of the
        //! request, so a level held through an observer reset would never be
        //! delivered again.
        if (seal_r && !echo_ok_r) begin
          seal_gen_o <= gen_r;
          if (seal_tmr_r == SRT_W_C'(SEAL_RETRY_CYC_P)) begin
            seal_tmr_r <= '0;
            seal_req_o <= ~seal_req_o;
          end else begin
            seal_tmr_r <= seal_tmr_r + SRT_W_C'(1);
          end
        end else begin
          seal_req_o <= 1'b0;
          seal_tmr_r <= '0;
        end

        //! The seal lifts, and the egress releases with it, once the
        //! observer has answered for THIS generation AND the whole
        //! pre-fence prefix has been resolved. A retained frame launches
        //! after that and resolves its own entry.
        if (seal_r && destroyed_w &&
            (n_pre_r == OCC_W_C'(0)) && !pre_resolve_w) begin
          seal_r        <= 1'b0;
          egress_hold_o <= 1'b0;
          demand_r      <= 1'b0;
          destroyed_r   <= 1'b0;
        end
      end
    end
  end : seal_state

  // ======================================================================= //
  //  Diagnostics                                                            //
  // ======================================================================= //
  //! The head entry's age. It counts, it publishes, and it retires nothing.
  logic age_hit_w;
  assign age_hit_w = 1'b0 && (n_led_r != OCC_W_C'(0)) &&
                     (age_r == AGE_W_C'(STALL_AGE_CYC_P));

  always_ff @(posedge clk_i) begin : diagnostics
    if (!rst_n) begin
      age_r         <= '0;
      dbg_lost_o    <= 16'd0;
      dbg_disc_o    <= 16'd0;
      dbg_barrier_o <= 16'd0;
      dbg_stall_o    <= 16'd0;
      dbg_phc_lost_o <= 16'd0;
    end else begin
      if (phc_lost_w) dbg_phc_lost_o <= dbg_phc_lost_o + 16'd1;
      if (resolve_w || (n_led_r == OCC_W_C'(0)) || age_hit_w) age_r <= '0;
      else if (n_led_r != OCC_W_C'(0))                        age_r <= age_r + AGE_W_C'(1);

      if (age_hit_w)             dbg_stall_o   <= dbg_stall_o + 16'd1;
      if (push_res_w && !res_ok_w) dbg_lost_o  <= dbg_lost_o + 16'd1;
      if (disc_w)                dbg_disc_o    <= dbg_disc_o + 16'd1;
      if (barrier_w)             dbg_barrier_o <= dbg_barrier_o + 16'd1;
    end
  end : diagnostics

  assign dbg_state_o = {seal_r, echo_ok_r, demand_r, destroyed_r, 4'(gen_r),
                        4'(n_res_r), 4'(n_led_r)};

  //! `seal_ack_i` reports that the seal crossing delivered a generation. It
  //! is deliberately NOT a completion: the observer's echo is, and this
  //! module waits for the echo. The port exists so a bench can tell a lost
  //! delivery from an unanswered one.
  logic unused_w;
  assign unused_w = seal_ack_i;

endmodule : KL_gptp_txret

`default_nettype wire

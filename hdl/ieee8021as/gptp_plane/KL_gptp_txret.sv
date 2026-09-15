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

                  (delta + OBS_LAT_E_P) transmit cycles  observer pipeline
                  CDC_LAT_D_P fabric cycles              crossing pipeline
                  half a fabric tick                     mean of the uniform
                                                         sampling phase

                Every term is a named parameter and the sum is derived, so a
                missing term is an elaboration fact rather than a silent bias
                a bench with a wide enough window would absorb.

  Spec refs   : IEEE Std 802.1AS-2020 10.2 (egress event ownership);
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
    parameter int unsigned OBS_LAT_E_P      = 2,
    //! crossing pipeline, fabric cycles, from the synchronised request to
    //! the edge this module registers the PHC on
    parameter int unsigned CDC_LAT_D_P      = 2,
    //! the only cycle distance a whole frame can produce
    parameter int unsigned TXTS_DELTA_EXP_P = 45,
    //! head-entry age that raises the counted stall diagnostic. It retires
    //! nothing; see the banner.
    parameter int unsigned STALL_AGE_CYC_P  = 1_000_000,
    //! fabric cycles between two offers of the seal to the observer. The
    //! crossing's destination side is in the observer's reset domain, so an
    //! offer made while the observer is held in reset is simply not seen and
    //! the next one carries the same generation.
    parameter int unsigned SEAL_RETRY_CYC_P = 256
) (
    input  wire clk_i,                 //! plane clock (axis_clk)
    input  wire rst_n,                 //! synchronous active-low reset

    //! the live PHC, in this clock's domain
    input  wire [63:0] phc_ns_i,

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
    input  wire [TXTS_OIDX_W_P-1:0]  rec_oidx_i,
    input  wire  [TXTS_GEN_W_P-1:0]  rec_gen_i,
    input  wire                [3:0] rec_type_i,
    input  wire               [15:0] rec_seq_i,
    input  wire [TXTS_DELTA_W_P-1:0] rec_delta_i,
    input  wire                      rec_abort_i,

    //! frames this plane has handed to the MAC and not yet resolved
    input  wire [$clog2(TXTS_CAP_N_P + 1):0] n_dep_i,
    //! one pulse per resolution, so the shadow can retire its departure
    output logic dep_take_o,

    //! the seal offered to the observer, and the crossing's delivery report
    output logic                    seal_req_o,
    output logic [TXTS_GEN_W_P-1:0] seal_gen_o,
    input  wire                     seal_ack_i,

    //! MAC recovery levels, the barrier trigger
    input  wire mac_reinit_i,
    input  wire mac_eth_rst_i,

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
      (TXTS_DELTA_EXP_P + OBS_LAT_E_P) * ETH_TICK_NS_P
    + CDC_LAT_D_P * DP_TICK_NS_P
    + DP_TICK_NS_P / 2;

  localparam int unsigned PTR_W_C = $clog2(TXTS_CAP_N_P);
  localparam int unsigned OCC_W_C = $clog2(TXTS_CAP_N_P + 1) + 1;
  localparam int unsigned AGE_W_C = $clog2(STALL_AGE_CYC_P + 1);
  localparam int unsigned SRT_W_C = $clog2(SEAL_RETRY_CYC_P + 1);

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

  logic [TXTS_GEN_W_P-1:0]  gen_r;
  logic [TXTS_OIDX_W_P-1:0] exp_oidx_r;
  logic                     seal_r;
  logic                     echo_ok_r;
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
  //  Record capture: the destination edge of the crossing                   //
  // ======================================================================= //
  //! The crossing presents `dest_req` across exactly one edge, and the PHC
  //! value present over that interval is the one written on the previous
  //! edge. Registering both here is what fixes `CDC_LAT_D_P`: change this
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
    end else begin
      cap_v_r <= rec_valid_i;
      if (rec_valid_i) begin
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
  assign res_ok_w = led_live_r[led_head_r] & led_tag_r[led_head_r] &
                    ~cap_abort_r &
                    (cap_delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P));
  //! modular by construction: the PHC wraps and a launch a few hundred
  //! nanoseconds before a wrap must reconstruct to the value before it
  assign res_ns_w = res_ok_w ? (cap_phc_r - 64'(TXTS_CORR_NS_P)) : 64'd0;

  assign push_res_w = resolve_w;

  // ======================================================================= //
  //  Barrier                                                                //
  // ======================================================================= //
  //! The MAC recovery levels, as one trigger. A rising edge raises the
  //! barrier; the level is what the destruction evidence is read from.
  logic mac_rst_w;
  assign mac_rst_w = mac_reinit_i | mac_eth_rst_i;

  assign barrier_w = (mac_rst_w & ~mac_rst_r) | mismatch_w |
                     (echo_rec_w & ~seal_r);

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
      //! one entry per admitted frame, in allocation order
      if (alloc_i && (n_led_r != OCC_W_C'(TXTS_CAP_N_P))) begin
        led_type_r[led_tail_w] <= alloc_type_i;
        led_seq_r [led_tail_w] <= alloc_seq_i;
        led_tag_r [led_tail_w] <= alloc_tagged_i;
        //! an entry admitted while the plane is sealed is created NOT live:
        //! the association context is not trusted, and it still owns its own
        //! position until its own record arrives
        led_live_r[led_tail_w] <= ~seal_r;
      end

      //! CANCELLATION MARKS. A barrier clears every entry's `live` flag and
      //! removes nothing, so each admitted frame keeps its ordered owner.
      if (barrier_w) begin
        for (int unsigned li = 0; li < TXTS_CAP_N_P; li++) led_live_r[li] <= 1'b0;
      end

      //! resolution consumes the head
      if (resolve_w) begin
        led_head_r <= (led_head_r == PTR_W_C'(TXTS_CAP_N_P - 1))
                      ? PTR_W_C'(0) : led_head_r + PTR_W_C'(1);
      end

      if (alloc_i && !resolve_w) begin
        if (n_led_r != OCC_W_C'(TXTS_CAP_N_P)) n_led_r <= n_led_r + OCC_W_C'(1);
      end else if (!alloc_i && resolve_w) begin
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
`endif
    end
  end : result_queue

  assign txts_valid_o = (n_res_r != OCC_W_C'(0));
  assign txts_ns_o    = res_ns_r  [res_head_r];
  assign txts_seq_o   = res_seq_r [res_head_r];
  assign txts_type_o  = res_type_r[res_head_r];
  assign txts_ok_o    = res_ok_r  [res_head_r];
  assign txts_gen_o   = res_gen_r [res_head_r];

  assign dep_take_o    = resolve_w;
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
    end else begin
      mac_rst_r <= mac_rst_w;

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
      end else begin
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

        //! the seal lifts once the observer has answered for THIS generation
        if (seal_r && echo_ok_r) seal_r <= 1'b0;
      end
    end
  end : seal_state

  // ======================================================================= //
  //  Diagnostics                                                            //
  // ======================================================================= //
  //! The head entry's age. It counts, it publishes, and it retires nothing.
  logic age_hit_w;
  assign age_hit_w = (n_led_r != OCC_W_C'(0)) &&
                     (age_r == AGE_W_C'(STALL_AGE_CYC_P));

  always_ff @(posedge clk_i) begin : diagnostics
    if (!rst_n) begin
      age_r         <= '0;
      dbg_lost_o    <= 16'd0;
      dbg_disc_o    <= 16'd0;
      dbg_barrier_o <= 16'd0;
      dbg_stall_o   <= 16'd0;
    end else begin
      if (resolve_w || (n_led_r == OCC_W_C'(0)) || age_hit_w) age_r <= '0;
      else if (n_led_r != OCC_W_C'(0))                        age_r <= age_r + AGE_W_C'(1);

      if (age_hit_w)             dbg_stall_o   <= dbg_stall_o + 16'd1;
      if (push_res_w && !res_ok_w) dbg_lost_o  <= dbg_lost_o + 16'd1;
      if (disc_w)                dbg_disc_o    <= dbg_disc_o + 16'd1;
      if (barrier_w)             dbg_barrier_o <= dbg_barrier_o + 16'd1;
    end
  end : diagnostics

  assign dbg_state_o = {seal_r, echo_ok_r, 2'b00, 4'(gen_r),
                        4'(n_res_r), 4'(n_led_r)};

  //! `seal_ack_i` reports that the seal crossing delivered a generation. It
  //! is deliberately NOT a completion: the observer's echo is, and this
  //! module waits for the echo. The port exists so a bench can tell a lost
  //! delivery from an unanswered one.
  logic unused_w;
  assign unused_w = seal_ack_i;

endmodule : KL_gptp_txret

`default_nettype wire

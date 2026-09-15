/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_gptp_txticket.sv
  Description : Admission and identity allocator for the gPTP plane's egress
                timestamps (issue #360). It watches the ENGINE TX BYTE FACE
                inside KL_gptp_shadow, allocates exactly one ledger entry per
                frame the engine commits, and publishes the admission credit
                the three initiating micro-code legs consult before they
                commit a new frame.

                WHY IT WATCHES THE BYTE FACE AND NOT THE LANE. The identity a
                returning launch record is matched against has to exist from
                the instant the frame becomes unstoppable, which is the
                accepted end of its last byte at the engine: from there to
                the wire the path is one lane, frame-locked, first in first
                out, with no drop path. Allocating later - at the lane, at
                the MAC boundary - would leave a window in which a frame
                exists with no owner.

                ACCEPTED BEATS ONLY. `tx_eof_i` is a HELD LEVEL while the
                last byte is stalled (the donor's KL_gptp_tx_slot holds
                `ser_run_r` through a stalled final byte), so an allocation
                armed on the level would fire once per stalled cycle and
                give one frame several owners. Every count and every capture
                here is qualified by `tx_valid_i && tx_ready_i`, the idiom
                the gearbox beside it already uses.

                ADMISSION IS CONSULTED, NEVER APPLIED. Credit is a level the
                producer reads BEFORE it commits. Back-pressuring the byte
                face would stall the very dispatch that releases the previous
                result, so a frame already in flight is never held here. The
                reservation `MAND_RSV_C` keeps room for the mandatory work
                that has no retry path: the Pdelay_Resp send and both
                Follow_Up companions are not credit gated, so capacity is
                reserved for them instead and the reserve is sized by the
                bound proof rather than assumed.

                OUTSTANDING, AND WHY IT HAS EXACTLY TWO COMMIT POINTS. It
                rises when a frame is admitted and falls when that frame's
                RESULT is accepted at the donor face. Nothing else moves it,
                so it equals the ledger occupancy plus the result-queue
                occupancy every cycle - the conservation equation
                KL_gptp_txret asserts - and two stores of `TXTS_CAP_N_P`
                entries are then enough for every reachable state.

  Spec refs   : IEEE Std 802.1AS-2020 10.6.2 (common header layout);
                docs/design/GPTP_PLANE.md (egress timestamp path)
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

//! Allocate one egress-timestamp identity per committed gPTP frame and
//! publish the transmit admission credit.
//!
//! **Key Features**
//! - Allocation on the ACCEPTED end-of-frame beat, so a held EOF level
//!   cannot allocate twice.
//! - `{messageType, sequenceId}` parsed from the frame's own octets at the
//!   contracted offsets, with a `tagged` flag for a frame too short to carry
//!   one.
//! - One `outstanding` counter with two commit points, and a credit level
//!   that reserves capacity for the un-gated mandatory frames.

`default_nettype none

module KL_gptp_txticket #(
    //! live egress identities this plane supports at once
    parameter int unsigned TXTS_CAP_N_P  = 8,
    //! capacity reserved for the frames that are NOT credit gated: one
    //! Pdelay_Resp plus the two Follow_Up companions, and the one gated
    //! frame that passed the gate while the other three were counted
    parameter int unsigned MAND_RSV_C    = 4,
    //! width of the free-running allocation index carried for diagnostics
    parameter int unsigned TXTS_AIDX_W_P = 12,
    //! frame octet offsets of the two tag fields (802.1AS-2020 10.6.2)
    parameter int unsigned TYPE_IDX_P    = 14,
    parameter int unsigned SEQ_IDX_HI_P  = 44,
    parameter int unsigned SEQ_IDX_LO_P  = 45
) (
    input  wire clk_i,               //! plane clock (axis_clk)
    input  wire rst_n,               //! synchronous active-low reset

    //! engine TX byte face, OBSERVED: a beat is real when valid and ready
    input  wire       tx_valid_i,
    input  wire       tx_ready_i,
    input  wire       tx_sof_i,
    input  wire       tx_eof_i,
    input  wire [7:0] tx_data_i,

    //! one pulse per admitted frame, the cycle after its accepted
    //! end-of-frame beat; the ledger and `outstanding` move on this pulse so
    //! the conservation equation holds on every edge
    output logic                     alloc_o,
    output logic               [3:0] alloc_type_o,
    output logic              [15:0] alloc_seq_o,
    //! 0 = the frame ended before its sequenceId octets, so it can only ever
    //! retire as a loss; no gPTP PDU is that short
    output logic                     alloc_tagged_o,
    //! free-running allocation index, carried for diagnostics and for
    //! wrap detection; it is not part of the frame's identity
    output logic [TXTS_AIDX_W_P-1:0] alloc_aidx_o,

    //! one pulse per result accepted at the donor face
    input  wire  res_accept_i,
    //! hold credit low whatever the occupancy is (the plane is sealed)
    input  wire  credit_hold_i,

    //! admission credit, a LEVEL the initiating legs read before committing
    output wire  tx_credit_o,
    //! live count of admitted frames whose result has not been accepted
    output wire [$clog2(TXTS_CAP_N_P + 1):0] outstanding_o,
    //! an allocation that would exceed the capacity bound: an internal
    //! invariant violation, counted and never a silent drop
    output logic [15:0] dbg_alloc_ovf_o
);

  //! occupancy counter width, one bit above the capacity so the saturation
  //! guard below is expressible instead of wrapping into a plausible value
  localparam int unsigned OCC_W_C = $clog2(TXTS_CAP_N_P + 1) + 1;
  //! frame octet counter width: it only has to reach the last tag octet and
  //! then saturate, because nothing past it is parsed
  localparam int unsigned BCNT_W_C = $clog2(SEQ_IDX_LO_P + 2);
  localparam logic [BCNT_W_C-1:0] BCNT_MAX_C = BCNT_W_C'(SEQ_IDX_LO_P + 1);

  // ---- elaboration contract ---------------------------------------------
  //! ONE format string per $error: later arguments print as values.
  if (TXTS_CAP_N_P < MAND_RSV_C + 2 || TXTS_CAP_N_P > 16) begin : g_refuse_cap
    $error("KL_gptp_txticket: TXTS_CAP_N_P=%0d is outside MAND_RSV_C+2=%0d..16. Below the reserve plus one gated frame the admission bound does not hold and the un-gated mandatory frames could be refused capacity; above 16 the carried indices stop separating a live window from a wrapped one.",
           TXTS_CAP_N_P, MAND_RSV_C + 2);
  end else if (SEQ_IDX_LO_P != SEQ_IDX_HI_P + 1 || TYPE_IDX_P >= SEQ_IDX_HI_P)
  begin : g_refuse_offsets
    $error("KL_gptp_txticket: tag offsets TYPE_IDX_P=%0d, SEQ_IDX_HI_P=%0d, SEQ_IDX_LO_P=%0d are not the 802.1AS common header layout (messageType ahead of a contiguous big-endian sequenceId).",
           TYPE_IDX_P, SEQ_IDX_HI_P, SEQ_IDX_LO_P);
  end

  // ======================================================================= //
  //  Frame parse, on accepted beats only                                    //
  // ======================================================================= //
  logic beat_w;
  assign beat_w = tx_valid_i & tx_ready_i;

  logic [BCNT_W_C-1:0] bcnt_r;
  logic [BCNT_W_C-1:0] bcnt_w;
  //! the index of the octet THIS accepted beat carries. A start-of-frame
  //! beat is octet 0 whatever the counter held, which is what keeps a lost
  //! or spurious end-of-frame from shifting a later frame's parse.
  assign bcnt_w = tx_sof_i ? BCNT_W_C'(0)
                           : ((bcnt_r == BCNT_MAX_C) ? BCNT_MAX_C
                                                     : bcnt_r + BCNT_W_C'(1));

  logic  [3:0] type_r;
  logic [15:0] seq_r;
  logic        tagged_r;
  //! this accepted beat carries the last tag octet, so the allocation below
  //! has to read the octet rather than the register it will land in
  logic seq_lo_w;
  assign seq_lo_w = (bcnt_w == BCNT_W_C'(SEQ_IDX_LO_P));

  always_ff @(posedge clk_i) begin : frame_parse
    if (!rst_n) begin
      bcnt_r   <= BCNT_W_C'(0);
      type_r   <= 4'd0;
      seq_r    <= 16'd0;
      tagged_r <= 1'b0;
    end else if (beat_w) begin
      bcnt_r <= bcnt_w;
      if (tx_sof_i) begin
        //! a new frame owns none of the previous frame's tag
        type_r   <= 4'd0;
        seq_r    <= 16'd0;
        tagged_r <= 1'b0;
      end
      //! messageType is the LOW nibble of its octet; the high nibble is
      //! transportSpecific and is not part of the identity
      if (bcnt_w == BCNT_W_C'(TYPE_IDX_P))   type_r      <= tx_data_i[3:0];
      if (bcnt_w == BCNT_W_C'(SEQ_IDX_HI_P)) seq_r[15:8] <= tx_data_i;
      if (seq_lo_w) begin
        seq_r[7:0] <= tx_data_i;
        tagged_r   <= 1'b1;
      end
    end
  end : frame_parse

  // ======================================================================= //
  //  Allocation                                                             //
  // ======================================================================= //
  logic alloc_w;
  //! exactly one allocation per frame: the ACCEPTED beat that carries the
  //! end of frame, never the held level around it
  assign alloc_w = beat_w & tx_eof_i;

  logic [TXTS_AIDX_W_P-1:0] aidx_r;

  always_ff @(posedge clk_i) begin : allocate
    if (!rst_n) begin
      alloc_o        <= 1'b0;
      alloc_type_o   <= 4'd0;
      alloc_seq_o    <= 16'd0;
      alloc_tagged_o <= 1'b0;
      alloc_aidx_o   <= '0;
      aidx_r         <= '0;
    end else begin
      alloc_o <= alloc_w;
      if (alloc_w) begin
        //! the end-of-frame beat may itself be a tag octet, so the published
        //! tag takes THIS beat's parse rather than the register it lands in
        alloc_type_o   <= (bcnt_w == BCNT_W_C'(TYPE_IDX_P)) ? tx_data_i[3:0]
                                                            : type_r;
        alloc_seq_o    <= seq_lo_w ? {seq_r[15:8], tx_data_i} : seq_r;
        alloc_tagged_o <= tagged_r | seq_lo_w;
        alloc_aidx_o   <= aidx_r;
        aidx_r         <= aidx_r + TXTS_AIDX_W_P'(1);
      end
    end
  end : allocate

  // ======================================================================= //
  //  Outstanding and credit                                                 //
  // ======================================================================= //
  logic [OCC_W_C-1:0] outst_r;
  assign outstanding_o = outst_r;

  //! Saturating rather than wrapping. The admission bound makes an overflow
  //! unreachable, so reaching it is an internal invariant violation: it is
  //! counted and published, because a wrapped occupancy would re-open
  //! admission at the exact moment the plane had lost track of a frame.
  logic ovf_w;
  assign ovf_w = alloc_o & ~res_accept_i & (outst_r == OCC_W_C'(TXTS_CAP_N_P));

  always_ff @(posedge clk_i) begin : outstanding_count
    if (!rst_n) begin
      outst_r         <= OCC_W_C'(0);
      dbg_alloc_ovf_o <= 16'd0;
    end else begin
      if (ovf_w) dbg_alloc_ovf_o <= dbg_alloc_ovf_o + 16'd1;
      //! the two commit points, netted so a simultaneous admission and
      //! result acceptance leaves the count where it was
      if (alloc_o & ~res_accept_i) begin
        if (!ovf_w) outst_r <= outst_r + OCC_W_C'(1);
      end else if (~alloc_o & res_accept_i) begin
        if (|outst_r) outst_r <= outst_r - OCC_W_C'(1);
      end
`ifndef SYNTHESIS
      if (outst_r > OCC_W_C'(TXTS_CAP_N_P))
        $error("KL_gptp_txticket: outstanding exceeded TXTS_CAP_N_P");
      if (res_accept_i && (outst_r == OCC_W_C'(0)))
        $error("KL_gptp_txticket: a result was accepted with nothing outstanding");
`endif
    end
  end : outstanding_count

  assign tx_credit_o = ~credit_hold_i &
                       (outst_r <= OCC_W_C'(TXTS_CAP_N_P - MAND_RSV_C));

endmodule : KL_gptp_txticket

`default_nettype wire

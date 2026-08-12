/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pp_maap_shim.sv
  Description : Adapter between this fabric's BLOCK allocator (KL_maap, IEEE
                1722 Annex B, hdl/ieee1722/maap/KL_maap.sv) and the
                protocol-processor's PER-SOURCE address-allocation face
                (protocol_processor_top's maap face, 02 section 4.2).

                THE TWO MODELS. KL_maap claims ONE contiguous block out of the
                91:E0:F0 pool - a base `addr_o` plus `count_i` addresses - and
                publishes `addr_valid_o` only while it is in ANNOUNCE, i.e.
                only while the claim has been probed and is being defended. It
                has no notion of a source, no per-source request, and no
                per-source release. The processor, by contrast, asks PER
                SOURCE: a held valid/ready ALLOC_DA or RELEASE_DA naming one
                source index, answered by exactly one response carrying a
                48-bit DA, plus a per-source conflict event.

                THE MAPPING is forced by the two models and is ALREADY the
                fabric's own convention: milan_datapath.sv assigns stream j the
                address `eff_aaf_dmac + j` (acmp_src_dmac_w, and the CRF talker
                takes + CRF_TUID_C on the same rule). So source s here gets
                `addr_o + s`, and the processor's talker therefore ends up
                declaring EXACTLY the address the shipping AAF talker already
                puts on the wire for that stream. Any other mapping would have
                the two planes disagree about the same stream's DA.

                --------------------------------------------------------------
                DESIGN DECISIONS (each one is a question the two models do not
                answer between them; recorded here because the next reader
                will ask):

                1. `req_ready_o` = "no response is already in flight". NOT
                   "the block is valid".

                   The processor's rule (KL_acmp_talker) is that an accepted
                   request MUST be answered - its allocator-busy flag is
                   cleared only by a response - while an UNACCEPTED request is
                   abandoned after P-MAAP-ACCEPT-CYC (1024) cycles and the
                   source degrades to no-DA. Two ways to satisfy that:

                     (a) hold ready low until the block is valid, and let the
                         processor time out when it is not;
                     (b) accept immediately and answer ok = 0 when we cannot
                         grant.

                   (b) is strictly better and is what this shim does, because
                   S_EV_MAAP is on the talker's SINGLE walker - the same
                   walker that serves PROBE_TX / DISCONNECT_TX / GET_TX_STATE
                   for EVERY source. Under (a) a MAAP that is merely still
                   PROBING (a legal state that lasts ~1.5 s) would park that
                   walker for 1024 cycles per attempt, so the whole talker
                   half of ACMP goes deaf while the fabric is doing exactly
                   what it is supposed to. Under (b) the same situation costs
                   two cycles and reaches the identical end state (the source
                   stays in GS_NO_DA, PROBE_TX answers TALKER_DEST_MAC_FAILED,
                   which is the honest answer).

                   The hazard this is written against: accept and then never
                   respond, and the processor's maap_busy_r sticks forever and
                   that source can never allocate again. So the answer is a
                   PURELY COMBINATIONAL function of the block state sampled at
                   the accepting cycle, latched into the response register in
                   the same cycle. There is no path by which an accepted
                   request fails to complete on the next clock - not a full
                   FIFO, not a busy engine, not a missing allocator. Bounded
                   at one cycle, unconditionally.

                2. ok = 0 versus ok = 1. ok = 1 only when the block is VALID
                   (KL_maap in ANNOUNCE: probed and defended) AND the source
                   index is inside the claimed count. Both terms matter:

                     - not valid: an address from a block still being probed
                       may be withdrawn by a conflicting peer, and handing it
                       out would put a stream on an address we do not own;
                     - s >= count: outside the claimed block the address
                       belongs to nobody, so granting it is a wire defect that
                       only shows up as somebody else's audio dropping out.

                   A refusal is NOT an error condition, it is the "no DA yet"
                   state, and the processor already models it.

                3. RELEASE_DA is accepted and acknowledged, and frees nothing.
                   KL_maap owns ONE block for the whole engine and holds it
                   for as long as it is enabled; there is no per-source claim
                   to release and no partial-release message in Annex B. So a
                   release here is a NO-OP acknowledgement: the response is
                   returned (the processor's tracker needs it to clear its
                   busy flag) with ok = 0 and da = 0, and the port contract
                   says ok is ignored on RELEASE_DA. Recorded rather than
                   silently dropped, because "release did nothing" is a real
                   property of this pairing: the block stays claimed and the
                   address stays reserved for that source index until the
                   whole block moves.

                4. CONFLICTS. KL_maap's conflict is a BLOCK event - when it
                   loses a probe or is defended against it re-randomises the
                   whole block and re-enters PROBE, which moves EVERY source's
                   address at once. The processor's face is per-source, so one
                   block event has to be fanned out to N per-source events.
                   This shim raises one for EVERY source, not only for sources
                   inside the count, because the count is CSR-writable and a
                   source that got a DA under a larger count must still be
                   told when the block moves under it. A source that holds no
                   DA takes the event harmlessly (KL_acmp_talker's EVC_CONFLICT
                   from GS_NO_DA clears an already-clear da_valid).

                   The TRIGGER is the block identity {valid, addr, count}
                   changing away from a state we were granting from - NOT
                   KL_maap's `conflicts_o` counter. That counter is a
                   saturating 8-bit event count that cannot distinguish "we
                   re-addressed" from "we defended and kept the address", and
                   it saturates; the identity tuple is the ground truth about
                   what we actually handed out. Every re-address necessarily
                   leaves ANNOUNCE (KL_maap sets state PROBE), so the falling
                   edge of `blk_valid_i` catches every case the counter would
                   have, plus the enable-dropped and count-shrunk cases the
                   counter would miss.

                5. NO ALLOCATOR AT ALL (MAAP_P = 0, or MAAP_CTRL.en = 0) needs
                   no special case: `blk_valid_i` is 0, every ALLOC is
                   answered ok = 0 in one cycle, and the processor degrades
                   cleanly. That is deliberately the SAME code path as "the
                   block is still probing" - a build without an allocator must
                   not take an untested branch.

  Interfaces  : block side = KL_maap's addr_o / addr_valid_o / count_i;
                processor side = the 10-pin maap face of
                protocol_processor_top, names and directions unchanged.
------------------------------------------------------------------------------
*/

`default_nettype none

module KL_pp_maap_shim #(
    //! number of talker sources (the processor's N_STREAM_OUT_P). Sources are
    //! indexed 0..N_SRC_P-1 and map onto block offsets 0..N_SRC_P-1.
    parameter int unsigned N_SRC_P = 8,
    //! derived source-index width — do not override. Clamped exactly as
    //! KL_acmp_talker clamps its own SRC_W_C, so a 1-source shape is legal.
    localparam int unsigned SRC_W_C = (N_SRC_P > 32'd1) ? $clog2(N_SRC_P)
                                                        : 32'd1
) (
    input  wire                clk_i,            //! core clock
    input  wire                rst_n,            //! active-low reset

    //! ---- block face (KL_maap) --------------------------------------------
    input  wire [47:0]         blk_addr_i,       //! claimed base DMAC (index 0)
    input  wire                blk_valid_i,      //! 1 = ANNOUNCE (claim held)
    input  wire [7:0]          blk_count_i,      //! addresses claimed from the base

    //! ---- per-source request face (protocol_processor_top) ----------------
    input  wire                req_valid_i,      //! ALLOC/RELEASE offered, held until ready
    output logic               req_ready_o,      //! this shim accepts the request
    input  wire                req_release_i,    //! 0 = ALLOC_DA, 1 = RELEASE_DA
    input  wire [SRC_W_C-1:0]  req_src_i,        //! source index of the request
    output logic               rsp_valid_o,      //! exactly one response per accepted request
    output logic               rsp_ok_o,         //! ALLOC_DA granted (ignored on RELEASE_DA)
    output logic [47:0]        rsp_da_o,         //! granted DA (valid with rsp_ok_o)
    output logic               conflict_valid_o, //! per-source conflict, held until acked
    output logic [SRC_W_C-1:0] conflict_src_o,   //! the source being told
    input  wire                conflict_ack_i    //! processor took the event (combinational)
);

  // ======================================================================= //
  //  Grant predicate — combinational, sampled at the accepting cycle        //
  // ======================================================================= //
  //! source index widened to the count's width for the in-block compare.
  //! N_SRC_P can never exceed 256 in this fabric (the processor's own
  //! N_STREAM_OUT_P is a small stream count), so 8 bits is the right compare
  //! width and matches KL_maap's count_i exactly.
  logic [7:0] src8_w;
  assign src8_w = 8'(req_src_i);

  logic in_block_w;
  assign in_block_w = blk_valid_i && (src8_w < blk_count_i);

  //! DA = base + s, computed on the 16-bit OFFSET half only. KL_maap's
  //! rand_offset() clamps the offset to POOL_SIZE - count, so offset + s for
  //! s < count can never leave the 0x0000..0xFDFF pool window and can never
  //! carry into the 91:E0:F0 prefix. Adding on the low half makes that
  //! STRUCTURAL rather than a property of the arithmetic: a grant physically
  //! cannot name an address outside the MAAP pool.
  logic [15:0] off_w;
  logic [47:0] da_w;
  assign off_w = blk_addr_i[15:0] + 16'(req_src_i);
  assign da_w  = {blk_addr_i[47:16], off_w};

  //! a request is taken whenever no response is already in flight
  assign req_ready_o = ~rsp_valid_o;

  logic        rsp_valid_r, rsp_ok_r;
  logic [47:0] rsp_da_r;
  assign rsp_valid_o = rsp_valid_r;
  assign rsp_ok_o    = rsp_ok_r;
  assign rsp_da_o    = rsp_da_r;

  //! grant term for THIS cycle's offered request (0 on a RELEASE_DA — see
  //! decision 3: a release frees nothing and reports nothing)
  logic grant_w;
  assign grant_w = ~req_release_i & in_block_w;

  always_ff @(posedge clk_i or negedge rst_n) begin : rsp_path
    if (!rst_n) begin
      rsp_valid_r <= 1'b0;
      rsp_ok_r    <= 1'b0;
      rsp_da_r    <= 48'd0;
    end else begin
      //! one-cycle response pulse; the accept below re-arms it
      rsp_valid_r <= 1'b0;
      if (req_valid_i & req_ready_o) begin
        rsp_valid_r <= 1'b1;
        rsp_ok_r    <= grant_w;
        rsp_da_r    <= grant_w ? da_w : 48'd0;
      end
    end
  end : rsp_path

  // ======================================================================= //
  //  Block-move detector -> per-source conflict fan-out                     //
  // ======================================================================= //
  logic        blk_valid_r;
  logic [47:0] blk_addr_r;
  logic [7:0]  blk_count_r;

  //! The block we were GRANTING FROM has gone away or moved. Only a block we
  //! were actually granting from (blk_valid_r) can strand a source, so the
  //! rising edge of blk_valid_i - good news, nobody holds a stale DA - raises
  //! nothing.
  logic moved_w;
  assign moved_w = blk_valid_r
                   && (!blk_valid_i
                       || (blk_addr_i  != blk_addr_r)
                       || (blk_count_i != blk_count_r));

  logic [N_SRC_P-1:0] confl_pend_r;
  assign conflict_valid_o = |confl_pend_r;

  //! lowest pending source first (descending sweep, last write wins)
  always_comb begin : confl_pick
    conflict_src_o = '0;
    for (int unsigned i = N_SRC_P; i > 0; i--) begin
      if (confl_pend_r[i-1]) conflict_src_o = SRC_W_C'(i - 1);
    end
  end : confl_pick

  always_ff @(posedge clk_i or negedge rst_n) begin : confl_path
    if (!rst_n) begin
      blk_valid_r  <= 1'b0;
      blk_addr_r   <= 48'd0;
      blk_count_r  <= 8'd0;
      confl_pend_r <= '0;
    end else begin
      blk_valid_r <= blk_valid_i;
      blk_addr_r  <= blk_addr_i;
      blk_count_r <= blk_count_i;
      //! a fresh move supersedes an in-flight sweep: every source must hear
      //! about the LATEST move, including one already acked for the previous
      if (moved_w) begin
        confl_pend_r <= '1;
      end else if (conflict_valid_o & conflict_ack_i) begin
        confl_pend_r[conflict_src_o] <= 1'b0;
      end
    end
  end : confl_path

endmodule

`default_nettype wire

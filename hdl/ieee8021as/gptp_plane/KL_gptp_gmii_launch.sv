/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_gptp_gmii_launch.sv
  Description : PER-FRAME LAUNCH OBSERVER for the gPTP plane (issue #360). It
                watches the MAC's transmit stream one register stage before
                the GMII pads, attributes each frame, measures WHEN its
                reference octet was launched relative to the octet that
                carries the frame's identity, and hands the fabric one record
                per observed frame.

                WHY A LAUNCH OBSERVER AT ALL. The plane used to latch the PHC
                at the first accepted beat of a frame at the datapath's MAC
                boundary. Between that beat and the wire the frame still
                crosses two AXIS clock-domain FIFOs, a store-and-forward
                packet FIFO, a width converter, padding, FCS, preamble and
                gap insertion, and one registered output stage - a delay that
                depends on how much other traffic is queued ahead of it.
                Every one of those nanoseconds went into t1 and biased the
                computed peer delay. The event has to be observed where it
                happens.

                WHERE IT OBSERVES, AND WHY NOT THE PAD. The observation point
                is the MAC's `phy.sink` stream, the source feeding the PHY's
                transmit register stage. The pads themselves are not tapped:
                their launch flip-flops are pad-locked (`set_property IOB
                TRUE`) because an unlocked GMII launch is a per-seed
                clock-to-out lottery on this board, and a fan-out to an
                observer would defeat that packing. The PHY stage registers
                `sink.valid` into `tx_en` and `sink.data` into `tx_data` on
                the same edge and holds `sink.ready` at 1, so the pad and
                this observer see the same octet on the same clock edge: the
                relationship between the two seams is one register stage, not
                an assumption.

                PURE OBSERVER: this module drives nothing on the stream it
                watches.

                WHAT A RECORD CARRIES, and why each field is there.

                  oidx    this observer's own position in the attributed
                          frame stream. The fabric's ledger position and this
                          index are the SAME per-frame ordinal, derived
                          independently at the two ends, which is what makes
                          identity positional rather than a tag lookup.
                  gen     the generation the fabric last sealed into this
                          observer. It is never 0 once adopted, so an
                          all-zero record from a crossing whose source was
                          reset is rejected rather than credited.
                  type,
                  seq     the frame's own tag octets: an additional check on
                          a position that is already established.
                  delta   transmit-clock cycles from the reference octet to
                          the tag octet. On a whole frame it is exactly the
                          octet distance; anything else means the frame was
                          fragmented on the wire, and the record is an abort
                          rather than a successful measurement carrying a
                          different correction.
                  abort   the frame ended before its tag octets, or `delta`
                          was not the expected distance.

                THE ECHO, and what it is for. After the fabric raises a
                barrier it seals the plane and has to re-establish which
                observer position the next surviving frame will take. It
                cannot read that off a frame record, because it does not yet
                know which frames survived. It sends the new generation
                across instead, and this observer answers with an ECHO record
                carrying its own current `oidx`. The echo consumes no frame
                and is not counted as one; it is positive evidence that the
                observer is out of reset, has adopted the generation, and is
                at that position.

                GAPS INSIDE A FRAME. `phy.sink.valid` cannot legally bubble
                inside a frame: the store-and-forward FIFO releases a frame
                only once it is completely buffered, and the PHY stage never
                back-pressures. A short low run inside a frame is therefore a
                fragment on the wire, and this observer deliberately keeps
                the frame OPEN across it (up to `GAP_CLOSE_CYC_P` cycles) so
                the cycle count still reaches the tag octet and the measured
                `delta` reports the fragmentation. A longer low run is the
                inter-frame gap, whose legal minimum is twelve octets.

  Spec refs   : IEEE Std 802.1AS-2020 10.2 and 11.3.2 (the message timestamp
                point is the beginning of the first symbol after the
                start-of-frame delimiter); docs/design/GPTP_PLANE.md;
                docs/litex/CLOCK_DOMAINS.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

//! Observe every frame the MAC launches and report the gPTP ones to the
//! fabric as ordered launch records.
//!
//! **Key Features**
//! - Attribution by preamble, start-of-frame delimiter, the gPTP destination
//!   address and the EtherType, so foreign traffic is excluded structurally.
//! - `delta` measured in transmit-clock cycles, so a fragmented frame aborts
//!   instead of yielding a plausible timestamp.
//! - Owns both clock-domain crossings: records out, the seal in, and the
//!   echo that re-establishes the observer position after a reset.

`default_nettype none

module KL_gptp_gmii_launch #(
    //! observation index of the reference octet: frame octet 0, the first
    //! symbol after the start-of-frame delimiter
    parameter int unsigned REF_IDX_P        = 8,
    //! observation index of the PTP header octet carrying messageType
    parameter int unsigned TYPE_IDX_P       = 22,
    //! observation indices of the sequenceId octets, high then low
    parameter int unsigned TAG_IDX_HI_P     = 52,
    parameter int unsigned TAG_IDX_LO_P     = 53,
    //! the only cycle distance a whole frame can produce
    parameter int unsigned TXTS_DELTA_EXP_P = 45,
    parameter int unsigned TXTS_DELTA_W_P   = 8,
    parameter int unsigned TXTS_OIDX_W_P    = 12,
    parameter int unsigned TXTS_GEN_W_P     = 4,
    //! transmit-clock cycles of `valid` low that end a frame. Well under the
    //! twelve-octet legal inter-frame gap and well over any fragment, so a
    //! fragment is measured rather than mistaken for a frame boundary.
    parameter int unsigned GAP_CLOSE_CYC_P  = 4
) (
    // ---- transmit domain (the MAC's eth_tx clock and its reset) ----------
    input  wire eth_clk_i,   //! the MAC transmit clock the pads launch on
    input  wire eth_rst_n,   //! synchronous active-low reset, `eth_clk_i`;
                             //! the same reset that clears the LiteEth
                             //! transmit side and the PHY transmit stage
    //! `phy.sink`, OBSERVED ONLY
    input  wire       gmii_tvalid_i,
    input  wire [7:0] gmii_tdata_i,

    // ---- fabric domain (the plane's axis_clk) ----------------------------
    input  wire dp_clk_i,    //! the plane's clock, which is the PHC's
    input  wire dp_rst_n,    //! synchronous active-low reset, `dp_clk_i`

    //! one record, one cycle in the fabric domain
    output wire                      rec_valid_o,
    output wire                      rec_kind_o,    //! 0 = frame, 1 = echo
    output wire [TXTS_OIDX_W_P-1:0]  rec_oidx_o,   //! observer position
    output wire  [TXTS_GEN_W_P-1:0]  rec_gen_o,    //! adopted generation
    output wire                [3:0] rec_type_o,   //! messageType octet
    output wire               [15:0] rec_seq_o,    //! sequenceId octets
    output wire [TXTS_DELTA_W_P-1:0] rec_delta_o,  //! measured cycle distance
    output wire                      rec_abort_o,  //! no measurement here

    //! the seal: the fabric offers a generation and re-offers it until the
    //! echo comes back. `seal_ack_o` says the crossing delivered it, which
    //! is NOT the same thing as the observer having adopted it, and the
    //! fabric treats it as an observation only.
    input  wire                    seal_req_i,
    input  wire [TXTS_GEN_W_P-1:0] seal_gen_i,
    output wire                    seal_ack_o,

    //! a record was ready while the record crossing and both queue slots
    //! were busy. Structurally unreachable at the minimum frame spacing;
    //! counted because the frame it belongs to still advanced `oidx`, so the
    //! fabric sees the hole as a position discontinuity and raises a
    //! barrier - nothing is dropped in silence.
    output logic [15:0] dbg_overrun_o
);

  //! the gPTP destination address, IEEE Std 802.1AS-2020 Table 10-1, in wire
  //! octet order: octet 0 is the most significant field below
  localparam logic [47:0] DA_GPTP_C  = 48'h01_80_C2_00_00_0E;
  localparam logic [15:0] ET_GPTP_C  = 16'h88F7;
  localparam logic  [7:0] PREAMBLE_C = 8'h55;
  localparam logic  [7:0] SFD_C      = 8'hD5;

  //! the observation index only has to reach the last tag octet and then
  //! stop; nothing past it is parsed
  localparam int unsigned IDX_W_C = $clog2(TAG_IDX_LO_P + 2);
  localparam logic [IDX_W_C-1:0] IDX_MAX_C = IDX_W_C'(TAG_IDX_LO_P + 1);
  localparam int unsigned GAP_W_C = $clog2(GAP_CLOSE_CYC_P + 1);
  //! record payload: kind, position, generation and the frame's own facts
  localparam int unsigned REC_W_C = 1 + TXTS_OIDX_W_P + TXTS_GEN_W_P + 4 + 16
                                  + TXTS_DELTA_W_P + 1;
  localparam logic [TXTS_DELTA_W_P-1:0] DELTA_MAX_C = '1;

  // ---- elaboration contract ---------------------------------------------
  //! ONE format string per $error: later arguments print as values.
  if (TXTS_DELTA_EXP_P != TAG_IDX_LO_P - REF_IDX_P) begin : g_refuse_delta
    $error("KL_gptp_gmii_launch: TXTS_DELTA_EXP_P=%0d is not TAG_IDX_LO_P-REF_IDX_P=%0d. The expected cycle distance IS the octet distance on a whole frame; a literal that does not derive from the two indices would let a fragmented frame produce a plausible timestamp.",
           TXTS_DELTA_EXP_P, TAG_IDX_LO_P - REF_IDX_P);
  end else if (TXTS_DELTA_EXP_P >= (1 << TXTS_DELTA_W_P) - 1)
  begin : g_refuse_delta_width
    $error("KL_gptp_gmii_launch: TXTS_DELTA_W_P=%0d cannot carry TXTS_DELTA_EXP_P=%0d below its saturation value, so a saturated count would be indistinguishable from the expected one.",
           TXTS_DELTA_W_P, TXTS_DELTA_EXP_P);
  end else if (GAP_CLOSE_CYC_P < 1 || GAP_CLOSE_CYC_P > 11)
  begin : g_refuse_gap
    $error("KL_gptp_gmii_launch: GAP_CLOSE_CYC_P=%0d is outside 1..11. At or above the twelve-octet legal inter-frame gap a real frame boundary would be read as a fragment inside one frame.",
           GAP_CLOSE_CYC_P);
  end

  // ======================================================================= //
  //  Declarations, both domains (Vivado's front end refuses a use above a   //
  //  declaration and drops the whole module when it finds one)              //
  // ======================================================================= //
  logic                      inf_r;    //! a frame is open
  logic [IDX_W_C-1:0]        idx_r;    //! index of the last observed octet
  logic [GAP_W_C-1:0]        gap_r;    //! consecutive low cycles inside it
  logic                      cand_r;   //! every attribution check has held
  logic                      mine_r;   //! attribution complete and positive
  logic                      ref_r;    //! the reference octet was launched
  logic                      done_r;   //! the tag octets are captured
  logic [TXTS_DELTA_W_P-1:0] delta_r;
  logic                [3:0] type_r;
  logic               [15:0] seq_r;
  logic [TXTS_OIDX_W_P-1:0]  oidx_r;
  logic  [TXTS_GEN_W_P-1:0]  gen_r;
  logic                      emit_pend_r;
  logic                      echo_pend_r;
  logic                      send_r, busy_r;
  logic [REC_W_C-1:0]        src_in_r;
  logic                      q0_v_r, q1_v_r;
  logic [REC_W_C-1:0]        q0_r, q1_r;
  logic                      ovr_pulse_r;

  logic                      src_rcv_w;
  logic                      ovr_dest_w;
  logic [REC_W_C-1:0]        rec_dest_w;
  logic                      seal_dest_req_w;
  logic [TXTS_GEN_W_P-1:0]   seal_gen_dest_w;
  //! A seal delivery is adopted only if it names a real generation.
  //! Generation 0 reaches this side exactly once: the crossing's SOURCE is
  //! in the fabric's reset domain, so a fabric reset clears its request
  //! toggle and its held data together and the destination sees one
  //! transfer of all zeros. Adopting it would make this observer answer
  //! with generation 0, which the fabric must reject - and the seal would
  //! then never lift. The fabric re-offers the real generation until the
  //! echo arrives, so refusing the replay costs one retry interval.
  logic seal_take_w;
  assign seal_take_w = seal_dest_req_w & (seal_gen_dest_w != '0);

  // ======================================================================= //
  //  Transmit domain: attribute, measure, assemble                          //
  // ======================================================================= //
  //! the index this cycle's octet carries
  logic [IDX_W_C-1:0] nidx_w;
  assign nidx_w = (!inf_r) ? IDX_W_C'(0)
                           : ((idx_r == IDX_MAX_C) ? IDX_MAX_C
                                                   : idx_r + IDX_W_C'(1));

  //! the expected destination-address octet at this index, spelled out
  //! rather than computed by a variable part-select, so the constant stays
  //! in wire order and the selection stays portable
  logic [2:0] da_j_w;
  logic [7:0] da_oct_w;
  assign da_j_w = 3'(nidx_w - IDX_W_C'(REF_IDX_P));
  always_comb begin : da_octet
    unique case (da_j_w)
      3'd0:    da_oct_w = DA_GPTP_C[47:40];
      3'd1:    da_oct_w = DA_GPTP_C[39:32];
      3'd2:    da_oct_w = DA_GPTP_C[31:24];
      3'd3:    da_oct_w = DA_GPTP_C[23:16];
      3'd4:    da_oct_w = DA_GPTP_C[15:8];
      default: da_oct_w = DA_GPTP_C[7:0];
    endcase
  end : da_octet

  //! the attribution verdict for THIS octet. Every index the standard fixes
  //! is checked; every other index passes, because a frame is attributed by
  //! its header and never by its payload.
  logic chk_w;
  always_comb begin : attribution_check
    chk_w = 1'b1;
    if (nidx_w < IDX_W_C'(REF_IDX_P - 1))
      chk_w = (gmii_tdata_i == PREAMBLE_C);
    else if (nidx_w == IDX_W_C'(REF_IDX_P - 1))
      chk_w = (gmii_tdata_i == SFD_C);
    else if (nidx_w < IDX_W_C'(REF_IDX_P + 6))
      chk_w = (gmii_tdata_i == da_oct_w);
    else if (nidx_w == IDX_W_C'(REF_IDX_P + 12))
      chk_w = (gmii_tdata_i == ET_GPTP_C[15:8]);
    else if (nidx_w == IDX_W_C'(REF_IDX_P + 13))
      chk_w = (gmii_tdata_i == ET_GPTP_C[7:0]);
  end : attribution_check

  //! the last octet of the header the frame has to prove its identity with
  logic att_done_w;
  assign att_done_w = (nidx_w == IDX_W_C'(REF_IDX_P + 13));
  logic cand_w;
  assign cand_w = (inf_r ? cand_r : 1'b1) & chk_w;

  //! a frame closes when `valid` has been low long enough to be the
  //! inter-frame gap rather than a fragment
  logic close_w;
  assign close_w = inf_r & ~gmii_tvalid_i &
                   (gap_r == GAP_W_C'(GAP_CLOSE_CYC_P - 1));

  logic frame_push_w;   //! the tag octets landed on the previous cycle
  logic abort_push_w;   //! the frame closed without reaching them
  assign frame_push_w = emit_pend_r;
  assign abort_push_w = close_w & mine_r & ~done_r;

  logic [REC_W_C-1:0] frame_rec_w;
  assign frame_rec_w = {1'b0,                       //! kind: frame
                        oidx_r, gen_r, type_r, seq_r, delta_r,
                        (delta_r != TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P))};
  logic [REC_W_C-1:0] abort_rec_w;
  assign abort_rec_w = {1'b0,                       //! kind: frame
                        oidx_r, gen_r, type_r, seq_r, delta_r, 1'b1};
  logic [REC_W_C-1:0] echo_rec_w;
  assign echo_rec_w  = {1'b1,                       //! kind: echo
                        oidx_r, gen_r, 4'd0, 16'd0,
                        TXTS_DELTA_W_P'(0), 1'b0};

  always_ff @(posedge eth_clk_i) begin : observe
    if (!eth_rst_n) begin
      inf_r       <= 1'b0;
      idx_r       <= IDX_W_C'(0);
      gap_r       <= GAP_W_C'(0);
      cand_r      <= 1'b0;
      mine_r      <= 1'b0;
      ref_r       <= 1'b0;
      done_r      <= 1'b0;
      delta_r     <= '0;
      type_r      <= 4'd0;
      seq_r       <= 16'd0;
      oidx_r      <= '0;
      emit_pend_r <= 1'b0;
      //! generation 0 means "this observer has not been sealed"; the fabric
      //! rejects every record carrying it
      gen_r       <= '0;
    end else begin
      emit_pend_r <= 1'b0;

      //! `delta` counts CYCLES, not octets. Inside a whole frame the two are
      //! the same; across a fragment they are not, and that difference is
      //! the measurement that refuses the record.
      if (inf_r && ref_r && !done_r && (delta_r != DELTA_MAX_C))
        delta_r <= delta_r + TXTS_DELTA_W_P'(1);

      if (gmii_tvalid_i) begin
        gap_r <= GAP_W_C'(0);
        inf_r <= 1'b1;
        idx_r <= nidx_w;
        if (!inf_r) begin
          //! a new frame owns none of the previous one's findings
          mine_r  <= 1'b0;
          ref_r   <= 1'b0;
          done_r  <= 1'b0;
          delta_r <= '0;
          type_r  <= 4'd0;
          seq_r   <= 16'd0;
        end
        cand_r <= cand_w;
        //! the reference octet: frame octet 0, launched at this edge
        if ((nidx_w == IDX_W_C'(REF_IDX_P)) && cand_w) begin
          ref_r   <= 1'b1;
          delta_r <= '0;
        end
        if (att_done_w) mine_r <= cand_w;
        if (nidx_w == IDX_W_C'(TYPE_IDX_P))   type_r      <= gmii_tdata_i[3:0];
        if (nidx_w == IDX_W_C'(TAG_IDX_HI_P)) seq_r[15:8] <= gmii_tdata_i;
        if ((nidx_w == IDX_W_C'(TAG_IDX_LO_P)) && mine_r && !done_r) begin
          seq_r[7:0]  <= gmii_tdata_i;
          done_r      <= 1'b1;
          //! the record leaves on the NEXT edge, by which time `delta_r`
          //! above has reached the distance this frame actually produced
          emit_pend_r <= 1'b1;
        end
      end else begin
        if (inf_r && (gap_r != GAP_W_C'(GAP_CLOSE_CYC_P)))
          gap_r <= gap_r + GAP_W_C'(1);
        if (close_w) begin
          inf_r  <= 1'b0;
          cand_r <= 1'b0;
          mine_r <= 1'b0;
          ref_r  <= 1'b0;
          done_r <= 1'b0;
          idx_r  <= IDX_W_C'(0);
          gap_r  <= GAP_W_C'(0);
        end
      end

      //! one position per attributed frame, whatever its outcome was
      if (frame_push_w || abort_push_w) oidx_r <= oidx_r + TXTS_OIDX_W_P'(1);
      if (seal_take_w)                  gen_r  <= seal_gen_dest_w;
    end
  end : observe

  // ======================================================================= //
  //  Record crossing, with a two-slot order-preserving queue in front       //
  // ======================================================================= //
  //! The echo is QUEUED rather than raced against a frame record: both are
  //! positions in one ordered stream and the fabric reads them in order.
  logic               push_w;
  logic               push_echo_w;
  logic [REC_W_C-1:0] push_rec_w;
  always_comb begin : record_select
    push_w      = 1'b1;
    push_echo_w = 1'b0;
    push_rec_w  = frame_rec_w;
    if (frame_push_w)      push_rec_w  = frame_rec_w;
    else if (abort_push_w) push_rec_w  = abort_rec_w;
    else if (echo_pend_r) begin
      push_rec_w  = echo_rec_w;
      push_echo_w = 1'b1;
    end
    else                   push_w      = 1'b0;
  end : record_select

  //! straight to the crossing when nothing is in front of it, which is the
  //! only path a legally spaced frame stream ever takes
  logic start_w;
  assign start_w = push_w & ~busy_r & ~send_r & ~q0_v_r;
  //! the crossing is free and a queued record is waiting
  logic drain_w;
  assign drain_w = ~push_w & ~busy_r & ~send_r & q0_v_r;
  //! the push found somewhere to go
  logic push_ok_w;
  assign push_ok_w = start_w | (push_w & ~start_w & (~q0_v_r | ~q1_v_r));

  always_ff @(posedge eth_clk_i) begin : record_out
    if (!eth_rst_n) begin
      send_r      <= 1'b0;
      busy_r      <= 1'b0;
      src_in_r    <= '0;
      q0_v_r      <= 1'b0;
      q1_v_r      <= 1'b0;
      q0_r        <= '0;
      q1_r        <= '0;
      echo_pend_r <= 1'b0;
      ovr_pulse_r <= 1'b0;
    end else begin
      ovr_pulse_r <= 1'b0;

      if (src_rcv_w) begin
        send_r <= 1'b0;
        busy_r <= 1'b0;
      end

      if (start_w) begin
        send_r   <= 1'b1;
        busy_r   <= 1'b1;
        src_in_r <= push_rec_w;
      end else if (drain_w) begin
        send_r   <= 1'b1;
        busy_r   <= 1'b1;
        src_in_r <= q0_r;
        q0_v_r   <= q1_v_r;
        q0_r     <= q1_r;
        q1_v_r   <= 1'b0;
      end else if (push_w) begin
        if (!q0_v_r) begin
          q0_v_r <= 1'b1;
          q0_r   <= push_rec_w;
        end else if (!q1_v_r) begin
          q1_v_r <= 1'b1;
          q1_r   <= push_rec_w;
        end else begin
          ovr_pulse_r <= 1'b1;
        end
      end

      //! the echo is owed from the cycle the seal lands until it is placed,
      //! and a NEWER seal always re-arms it: an echo for an obsolete
      //! generation would establish a base the fabric no longer expects
      if (seal_take_w)                  echo_pend_r <= 1'b1;
      else if (push_echo_w & push_ok_w) echo_pend_r <= 1'b0;
    end
  end : record_out

  cdc_pulse #(.DEST_SYNC_FF(2)) u_overrun_cdc (
      .src_clk    (eth_clk_i),
      .src_rst_n  (eth_rst_n),
      .src_pulse  (ovr_pulse_r),
      .dest_clk   (dp_clk_i),
      .dest_rst_n (dp_rst_n),
      .dest_pulse (ovr_dest_w)
  );

  always_ff @(posedge dp_clk_i) begin : overrun_count
    if (!dp_rst_n)       dbg_overrun_o <= 16'd0;
    else if (ovr_dest_w) dbg_overrun_o <= dbg_overrun_o + 16'd1;
  end : overrun_count

  cdc_handshake #(.WIDTH(REC_W_C), .DEST_SYNC_FF(2), .SRC_SYNC_FF(2))
  u_rec_cdc (
      .src_clk    (eth_clk_i),
      .src_rst_n  (eth_rst_n),
      .src_in     (src_in_r),
      .src_send   (send_r),
      .src_rcv    (src_rcv_w),
      .dest_clk   (dp_clk_i),
      .dest_rst_n (dp_rst_n),
      .dest_out   (rec_dest_w),
      .dest_req   (rec_valid_o)
  );

  assign {rec_kind_o, rec_oidx_o, rec_gen_o, rec_type_o, rec_seq_o,
          rec_delta_o, rec_abort_o} = rec_dest_w;

  // ======================================================================= //
  //  Seal crossing: the fabric's generation into the transmit domain        //
  // ======================================================================= //
  cdc_handshake #(.WIDTH(TXTS_GEN_W_P), .DEST_SYNC_FF(2), .SRC_SYNC_FF(2))
  u_seal_cdc (
      .src_clk    (dp_clk_i),
      .src_rst_n  (dp_rst_n),
      .src_in     (seal_gen_i),
      .src_send   (seal_req_i),
      .src_rcv    (seal_ack_o),
      .dest_clk   (eth_clk_i),
      .dest_rst_n (eth_rst_n),
      .dest_out   (seal_gen_dest_w),
      .dest_req   (seal_dest_req_w)
  );

endmodule : KL_gptp_gmii_launch

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_tdm_render_master.sv
  Author      : Kebag Logic

  Date        : 2026-09-14
  Description : TDM MASTER audio-render front-end - the OUTPUT half of the
                master bus KL_tdm_capture_master already owns (issue #447).
                The mapping fabric writes SLOTS_P per-slot 24-bit samples into
                a bank on clk_i; a whole-frame gray-pointer CDC carries each
                committed frame into clk_tdm_i, where the serializer shifts it
                onto tdm_dout_o MSB first, 24-in-SLOT_BITS_P left justified.

                THE ONE DESIGN DECISION. This module does NOT generate bus
                timing. There is exactly one TDM bus - bclk and fsync are
                shared pins - so a second free-running frame divider on the
                render side would be a protocol defect on real hardware even
                when both divide the same clock, because nothing constrains
                their relative frame phase. KL_tdm_capture_master stays the
                sole timing owner and exports bclk_rise_o / bclk_fall_o /
                frame_pos_o; this module runs in the SAME clk_tdm_i and
                consumes those enables. That is also why it is a SIBLING of
                KL_tdm_render rather than a role parameter on it: the slave
                genuinely clocks on `posedge tdm_bclk_i` and a master cannot,
                without synthesising a clock net in fabric. The clean-clock
                discipline (KL_aaf_capture_i2s 07-18 lineage) holds: bclk is a
                SIGNAL with a rising-edge ENABLE, never a clock.

                THE PIN-LEVEL EDGE CONTRACT. Write E(p) for the bclk pin rise
                produced at the end of the bclk_rise_i cycle whose pre-edge
                frame_pos_i is p, and "bit period p" for the interval in which
                frame_pos_i == p. fsync occupies bit period 0 and data starts
                in bit period 1, so slot k bit b occupies bit period
                1 + SLOT_BITS_P*k + b. An external receiver sees fsync rise at
                E(FRAME_C - 1) and samples slot 0's MSB at E(1): TWO bclk rises
                after the observed fsync rise. That is the phase the in-tree
                external codec model of this same master bus already presents
                to the capture direction, so both directions read one bus the
                same way. Concretely, on the bclk_rise_i cycle with pre-edge
                position p this module latches the bit for bit period p + 1 -
                slot p / SLOT_BITS_P, bit p % SLOT_BITS_P - and registers it
                onto tdm_dout_o on the following bclk_fall_i cycle, which lies
                inside bit period p + 1 and gives the receiver half a bit
                period of setup.

                THE RENDER EPOCH (reset, clock stoppage and bind loss). Both
                FIFO sides reset SYNCHRONOUSLY to their own clock, so a reset
                asserted and released entirely while clk_tdm_i is stopped
                would reset one pointer and leave the other, the active frame
                and the prefetched frame from the old run. A pulse cannot be
                seen by a clock that is not running, so the epoch protocol is
                four-phase over RETAINED LEVELS and each side waits for the
                other:

                  epoch_req_r (clk_i,     reset 1) the producer demands a
                                                   common epoch
                  ser_flush_r (clk_tdm_i, reset 1) the serial side is flushed
                                                   and its FIFO read side is
                                                   held in reset
                  ser_ack_r   (clk_tdm_i, reset 0) the serial side has
                                                   acknowledged a request
                  commit_en_r (clk_i,     reset 0) commits and FIFO writes are
                                                   permitted

                A serial-domain reset shows as ser_flush_r high with ser_ack_r
                low, which the producer answers with a request, so there is no
                state in which one side waits for a round trip the other never
                started. The FIFO reset ports are driven from the epoch
                (wrst_n = rst_n && !epoch_req_r, rrst_n = srst && !ser_flush_r)
                so both pointers are proven zero before any commit is admitted.

                HARD RESET AND GRACEFUL FLUSH ARE DIFFERENT. A hard serial
                reset clears the serializer state where it stands: it INTERRUPTS
                the frame in flight and that serial interval is invalid, which
                is the existing timing owner's behavior preserved. A GRACEFUL
                flush (a bind-loss or reset-release epoch while clk_tdm_i keeps
                running) zeroes active_r at FRAME STARTS only, so the frame in
                flight completes WHOLE and every frame after it is digital
                silence until the epoch reopens.

                SURPLUS IS DROP-OLDEST, COUNTED. The producer commits one frame
                per media tick; the serializer consumes one per frame start,
                and on the shipping divider plan the producer leads by
                -10.64 ppm. KL_tdm_render drops the NEWEST commit when its CDC
                is full, which lets the FIFO fill and ratchets the
                commit-to-pin delay upward. This module keeps prefetching while
                the CDC is non-empty, so next_r always holds the freshest
                committed frame, the CDC stays near empty and the delay stays
                bounded; every overwritten frame is ONE counted skip. A skip is
                counted when the frame is overwritten, which is BEFORE the
                decoded frame that exposes the ordinal jump, so a consumer
                reconciling counts against decoded frames must allow a counted
                skip to remain pending until the adoption it affects is
                observed.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! TDM MASTER serializer (item-4 front-end family, OUTPUT side): a clk_i slot
//! bank -> packed-frame gray-pointer CDC -> active/next double buffer ->
//! MSB-first 24-in-SLOT_BITS_P TDM frame on tdm_dout_o, scheduled entirely
//! from the capture master's exported bit-clock enables and frame position.
//! Four-phase retained-level render epoch over reset, clock stoppage and bind
//! loss; drop-oldest surplus; gray-coded counter export.

`default_nettype none

module KL_tdm_render_master #(
  parameter int unsigned SLOTS_P       = 8,   //! TDM slots per frame (8/16/32)
  //! bit clocks per slot. A POWER OF TWO: the bit schedule is a slice of the
  //! exported frame position rather than a divider of its own, which is what
  //! keeps this module free of a second frame counter. The guard below
  //! refuses anything else instead of framing at the wrong offset.
  parameter int unsigned SLOT_BITS_P   = 32,
  parameter int unsigned FIFO_LOG2_P   = 2,   //! frame CDC depth = 2^N (>= 2
                                              //! for the active/next pair)
  //! width of frame_pos_i = $clog2(SLOTS_P * SLOT_BITS_P) at the timing owner
  parameter int unsigned FRAME_POS_W_P = 8
)(
  input  wire         clk_i,             //! datapath clock (producer domain)
  input  wire         rst_n,             //! active-low synchronous reset (clk_i)

  // ---- producer side (clk_i domain; slot-indexed writes) ---------------
  input  wire         smp_wr_en_i,       //! one-cycle per-slot write strobe
  input  wire [$clog2(SLOTS_P)-1:0] smp_wr_slot_i, //! target slot index
  input  wire [23:0]  smp_wr_data_i,     //! 24-bit sample (MSB-justified)
  input  wire         tick_i,            //! one-cycle frame commit: latch the
                                         //! bank as written up to the prior
                                         //! cycle into the CDC toward the bus

  // ---- render epoch, producer face (clk_i domain) ----------------------
  input  wire         epoch_evt_i,       //! one-cycle: close the epoch (a
                                         //! qualified bind fall on a stream
                                         //! this lane renders)
  input  wire         fresh_i,           //! level: every stream this lane
                                         //! renders has left prefill AND
                                         //! popped a post-flush event, so the
                                         //! upstream selection is fresh again
  output wire         commit_en_o,       //! level: the adapter may walk the
                                         //! bank and commit a frame

  // ---- TDM bus (we are MASTER: the timing owner drives bclk/fsync) ------
  input  wire         clk_tdm_i,         //! the timing owner's clock domain
  input  wire         bclk_rise_i,       //! KL_tdm_capture_master.bclk_rise_o
  input  wire         bclk_fall_i,       //! KL_tdm_capture_master.bclk_fall_o
  input  wire [FRAME_POS_W_P-1:0] frame_pos_i, //! ...frame_pos_o (pre-edge)
  output logic        tdm_dout_o,        //! serial data out, MSB first,
                                         //! launched on the bclk falling edge

  // ---- serial-domain observation points (clk_tdm_i) --------------------
  //! The two registered instants a latency measurement needs. They are
  //! OBSERVATION points, not control: nothing in this module or above it
  //! consumes them, and the pin-level proof decoder is forbidden to read
  //! them - it sees bclk, fsync and dout and nothing else.
  output wire         frame_start_o,     //! one cycle at every frame start
  output wire         adopt_p_o,         //! ...and at those that ADOPT a
                                         //! freshly committed frame

  // ---- status (clk_i domain; gray-crossed from the serial side) --------
  output wire  [15:0] frames_o,          //! frames serialized onto the bus
  output wire  [15:0] underruns_o,       //! frame starts with no fresh frame
                                         //! (last frame repeated)
  output wire  [15:0] skips_o,           //! prefetched frames overwritten by a
                                         //! fresher commit (drop-oldest)
  output wire  [15:0] overruns_o,        //! tick_i frames dropped (CDC full)
  output wire  [15:0] epochs_o           //! completed epoch reopenings
);

  localparam int unsigned SW_C    = $clog2(SLOTS_P);       //! slot-index width
  localparam int unsigned SBW_C   = $clog2(SLOT_BITS_P);   //! bit-index width
  localparam int unsigned DBITS_C =
      (SLOT_BITS_P < 24) ? SLOT_BITS_P : 24;               //! data bits/slot
  localparam int unsigned FRAME_BITS_C = SLOTS_P * 24;     //! packed frame
  localparam int unsigned FRAME_C = SLOTS_P * SLOT_BITS_P; //! bclks per frame

  //! The bit schedule is a SLICE of frame_pos_i (slot = pos / SLOT_BITS_P,
  //! bit = pos % SLOT_BITS_P), which is only a slice when SLOT_BITS_P is a
  //! power of two. A non-power-of-two width would need its own divider and a
  //! second frame counter - the very thing this module exists not to have -
  //! so it is refused rather than silently mis-framed.
  if (SLOT_BITS_P != (1 << SBW_C)) begin : g_slot_bits_guard
    $error("KL_tdm_render_master: SLOT_BITS_P=%0d must be a power of two (the bit schedule is a slice of the timing owner's frame position).",
           SLOT_BITS_P);
  end : g_slot_bits_guard
  if (32'(FRAME_POS_W_P) != $clog2(FRAME_C)) begin : g_frame_pos_guard
    $error("KL_tdm_render_master: FRAME_POS_W_P=%0d does not match $clog2(SLOTS_P*SLOT_BITS_P)=%0d, so the exported frame position is not the one this schedule slices.",
           FRAME_POS_W_P, $clog2(FRAME_C));
  end : g_frame_pos_guard

  // ======================================================================
  //  Cross-domain level synchronisers (2-FF, the blessed idiom).
  // ======================================================================
  logic [1:0] srst_n_r;                  //! rst_n into clk_tdm_i
  always_ff @(posedge clk_tdm_i) srst_n_r <= {srst_n_r[0], rst_n};
  wire srst_n_w = srst_n_r[1];

  logic       epoch_req_r;               //! clk_i:     retained request level
  logic       commit_en_r;               //! clk_i:     commits permitted
  logic       ser_flush_r;               //! clk_tdm_i: retained flush level
  logic       ser_ack_r;                 //! clk_tdm_i: retained ack level

  logic [1:0] req_s_r;                   //! epoch_req_r into clk_tdm_i
  always_ff @(posedge clk_tdm_i) begin : t_req_sync
    if (!srst_n_w) req_s_r <= 2'b11;     //! reset-time request, not a glitch
    else           req_s_r <= {req_s_r[0], epoch_req_r};
  end : t_req_sync
  wire req_s_w = req_s_r[1];

  logic [1:0] flush_s_r, ack_s_r;        //! the two serial levels into clk_i
  always_ff @(posedge clk_i) begin : t_ser_sync
    if (!rst_n) begin
      flush_s_r <= 2'b11;                //! assume flushed until proven otherwise
      ack_s_r   <= 2'b00;
    end else begin
      flush_s_r <= {flush_s_r[0], ser_flush_r};
      ack_s_r   <= {ack_s_r[0], ser_ack_r};
    end
  end : t_ser_sync
  wire flush_s_w = flush_s_r[1];
  wire ack_s_w   = ack_s_r[1];

  // ======================================================================
  //  clk_i domain: the producer half of the four-phase epoch.
  //
  //  Phase 0 idle    : commit_en_r = 1, epoch_req_r = 0
  //  Phase 1 request : an epoch event, or a serial side that is flushed
  //                    WITHOUT having acknowledged anything (its own reset),
  //                    raises epoch_req_r and drops commit_en_r. The FIFO
  //                    write side is now held in reset.
  //  Phase 2 clear   : the acknowledgement clears epoch_req_r. Commits stay
  //                    blocked.
  //  Phase 3 resume  : the acknowledgement has fallen (so the serial side is
  //                    out of flush with both pointers at zero) AND the
  //                    upstream selection is fresh: commit_en_r rises.
  // ======================================================================
  wire ser_reset_w = flush_s_w && !ack_s_w;

  always_ff @(posedge clk_i) begin : t_epoch_producer
    if (!rst_n) begin
      epoch_req_r <= 1'b1;               //! reset IS an epoch event
      commit_en_r <= 1'b0;
    end else if (epoch_evt_i || ser_reset_w) begin
      epoch_req_r <= 1'b1;
      commit_en_r <= 1'b0;
    end else if (ack_s_w) begin
      epoch_req_r <= 1'b0;
      commit_en_r <= 1'b0;
    end else if (!epoch_req_r && fresh_i) begin
      commit_en_r <= 1'b1;
    end
  end : t_epoch_producer

  assign commit_en_o = commit_en_r;

  // ======================================================================
  //  clk_i domain: slot bank + frame commit into the gray-pointer CDC
  // ======================================================================
  logic [23:0]            bank_r [SLOTS_P];
  logic [15:0]            overruns_r;
  wire  [FRAME_BITS_C-1:0] bank_flat_w;
  wire                     wfull_w;

  genvar gs;
  generate
    for (gs = 0; gs < SLOTS_P; gs++) begin : g_pack
      assign bank_flat_w[gs*24 +: 24] = bank_r[gs];
    end
  endgenerate

  //! a commit is admitted only inside an OPEN epoch; the FIFO self-guards on
  //! !wfull, and bank_flat_w reflects writes up to the prior cycle
  wire fifo_wen_w = tick_i && commit_en_r && !wfull_w;

  always_ff @(posedge clk_i) begin : t_producer
    if (!rst_n) begin
      overruns_r <= '0;
      for (int i = 0; i < SLOTS_P; i++) bank_r[i] <= '0;
    end else begin
      if (smp_wr_en_i) bank_r[smp_wr_slot_i] <= smp_wr_data_i;
      if (tick_i && commit_en_r && wfull_w)
        overruns_r <= (&overruns_r) ? overruns_r : overruns_r + 16'd1;
    end
  end : t_producer

  // ======================================================================
  //  clk_i -> clk_tdm_i frame crossing. The blessed gray-pointer primitive,
  //  UNMODIFIED; only its reset ports are driven from the epoch, so both
  //  pointers are proven zero before the first admitted commit. The payload
  //  is one WHOLE frame, so a torn frame is structurally impossible rather
  //  than timed against.
  // ======================================================================
  wire [FRAME_BITS_C-1:0] rdata_w;
  wire                    rempty_w;
  logic                   ren_r;

  cdc_pair_fifo #(.WIDTH(FRAME_BITS_C), .LOG2D(FIFO_LOG2_P)) u_fcdc (
    .wclk_i  (clk_i),
    .wrst_n  (rst_n && !epoch_req_r),
    .wen_i   (fifo_wen_w),
    .wdata_i (bank_flat_w),
    .wfull_o (wfull_w),
    .rclk_i  (clk_tdm_i),
    .rrst_n  (srst_n_w && !ser_flush_r),
    .ren_i   (ren_r),
    .rdata_o (rdata_w),
    .rempty_o(rempty_w)
  );

  // ======================================================================
  //  clk_tdm_i domain: the serial half of the epoch, the drop-oldest
  //  prefetch, the double buffer and the bit schedule.
  // ======================================================================
  logic [FRAME_BITS_C-1:0] active_r;     //! frame currently serializing
  logic [FRAME_BITS_C-1:0] next_r;       //! prefetched frame (double buffer)
  logic                    have_next_r;  //! next_r holds a fresh frame
  logic                    fetch_v_r;    //! rdata_w is valid this cycle
  logic                    dout_nxt_r;   //! bit for the next falling edge
  logic [15:0]             frames_b_r, unders_b_r, skips_b_r, epochs_b_r;

  //! the frame start: the timing owner's own position compare, so the render
  //! frame can never drift from the fsync it is framed by
  wire frame_start_w = bclk_rise_i && (32'(frame_pos_i) == 0);

  //! how many committed frames are available at this edge, and which is the
  //! freshest. Two means the older one is being dropped: ONE counted skip.
  wire [1:0] avail_w = {1'b0, fetch_v_r} + {1'b0, have_next_r};
  wire [FRAME_BITS_C-1:0] fresh_frame_w = fetch_v_r ? rdata_w : next_r;

  //! the frame that will be serialized during bit period frame_pos_i + 1
  wire [FRAME_BITS_C-1:0] frame_sel_w =
      !frame_start_w ? active_r
      : ser_flush_r  ? '0
      : (avail_w != 2'd0) ? fresh_frame_w
      : active_r;

  assign frame_start_o = frame_start_w;
  assign adopt_p_o     = frame_start_w && !ser_flush_r && (avail_w != 2'd0);

  //! slot k bit b occupies bit period 1 + SLOT_BITS_P*k + b, so the bit for
  //! bit period p + 1 is slot p[.. : SBW_C], bit p[SBW_C-1 : 0]
  wire [SW_C-1:0]  bit_slot_w = frame_pos_i[FRAME_POS_W_P-1 -: SW_C];
  wire [SBW_C-1:0] bit_idx_w  = frame_pos_i[SBW_C-1 : 0];
  wire [23:0]      bit_smp_w  = frame_sel_w[24*bit_slot_w +: 24];
  //! MSB first, the top DBITS_C bits of the slot are data, the rest pad ZERO
  wire [4:0]       didx_w     = 5'd23 - 5'(bit_idx_w);
  wire             dbit_w     = (32'(bit_idx_w) < DBITS_C) ? bit_smp_w[didx_w]
                                                           : 1'b0;

  always_ff @(posedge clk_tdm_i) begin : t_ser
    if (!srst_n_w) begin
      //! A HARD RESET INTERRUPTS THE FRAME IN FLIGHT. The serializer state
      //! goes where it stands, dout is held low, and the serial interval is
      //! invalid until the next observable frame boundary. This is the
      //! existing timing owner's behavior, preserved rather than softened.
      ser_flush_r <= 1'b1;
      ser_ack_r   <= 1'b0;
      active_r    <= '0;
      next_r      <= '0;
      have_next_r <= 1'b0;
      ren_r       <= 1'b0;
      fetch_v_r   <= 1'b0;
      dout_nxt_r  <= 1'b0;
      tdm_dout_o  <= 1'b0;
      frames_b_r  <= '0;
      unders_b_r  <= '0;
      skips_b_r   <= '0;
      epochs_b_r  <= '0;
    end else begin
      // ---- drop-OLDEST prefetch: keep reading while the CDC is non-empty -
      ren_r     <= 1'b0;
      fetch_v_r <= ren_r;
      if (!ser_flush_r && !ren_r && !fetch_v_r && !rempty_w) ren_r <= 1'b1;

      if (!ser_flush_r) begin
        if (avail_w == 2'd2)
          skips_b_r <= (&skips_b_r) ? skips_b_r : skips_b_r + 16'd1;
        if (frame_start_w) begin
          have_next_r <= 1'b0;
          if (avail_w != 2'd0) active_r <= fresh_frame_w;
          else unders_b_r <= (&unders_b_r) ? unders_b_r : unders_b_r + 16'd1;
        end else if (fetch_v_r) begin
          next_r      <= rdata_w;
          have_next_r <= 1'b1;
        end
      end

      // ---- the GRACEFUL flush zeroes the active frame at FRAME STARTS
      //      only, so the frame in flight completes WHOLE ----------------
      if (frame_start_w) begin
        frames_b_r <= (&frames_b_r) ? frames_b_r : frames_b_r + 16'd1;
        if (ser_flush_r) begin
          active_r    <= '0;
          have_next_r <= 1'b0;
        end
      end

      // ---- the serial half of the four-phase epoch. LAST in the block, so
      //      reset/flush takes PRIORITY over prefetch and adoption: a
      //      prefetched pre-boundary frame is discarded on the very edge the
      //      request is seen, whatever the prefetch decided above ---------
      if (req_s_w) begin
        ser_flush_r <= 1'b1;
        ser_ack_r   <= 1'b1;
        next_r      <= '0;
        have_next_r <= 1'b0;
      end else if (ser_flush_r && ser_ack_r && frame_start_w) begin
        //! the request has cleared: reopen on this frame start, pointers at
        //! zero, and count the reopening so a silence interval is
        //! distinguishable from stale audio by observation
        ser_flush_r <= 1'b0;
        ser_ack_r   <= 1'b0;
        epochs_b_r  <= (&epochs_b_r) ? epochs_b_r : epochs_b_r + 16'd1;
      end

      // ---- the bit schedule: latch on the rise, launch on the fall -----
      if (bclk_rise_i) dout_nxt_r <= dbit_w;
      if (bclk_fall_i) tdm_dout_o <= dout_nxt_r;
    end
  end : t_ser

  // ======================================================================
  //  Counter export, clk_tdm_i -> clk_i.
  //
  //  A per-bit two-flop synchroniser on a BINARY counter does not produce a
  //  coherent sample: several bits change on one increment and the
  //  destination can latch a value the counter never held. Each counter is
  //  therefore held in binary and its GRAY image is REGISTERED in the source
  //  domain - the settled code, never a combinational network whose carries
  //  can glitch while it is being sampled, which is the same discipline
  //  cdc_pair_fifo's own pointers use.
  //
  //  Consecutive gray codes differ in exactly one bit, so a destination
  //  sample is either the pre-increment or the post-increment value. The
  //  argument needs the source to be stable across a destination sample, not
  //  a rate: increments are at least one serial clock apart, and the fastest
  //  of them is the drop-oldest skip, which cannot repeat faster than one per
  //  two serial clocks (the read-enable / read-data pair). The destination
  //  clock is faster than the serial clock on every shape this elaborates, so
  //  at most one bit is ever in flight at a sample. This is a COHERENCE
  //  argument about the digital model; it is not a claim that an ordinary
  //  zero-delay simulation demonstrates metastability behavior.
  // ======================================================================
  function automatic logic [15:0] bin2gray16(input logic [15:0] b);
    bin2gray16 = b ^ (b >> 1);
  endfunction

  function automatic logic [15:0] gray2bin16(input logic [15:0] g);
    logic [15:0] b;
    b = g;
    for (int i = 1; i < 16; i++) b = b ^ (g >> i);
    gray2bin16 = b;
  endfunction

  logic [15:0] fr_g_r, un_g_r, sk_g_r, ep_g_r;   //! REGISTERED gray, source
  always_ff @(posedge clk_tdm_i) begin : t_cnt_gray
    if (!srst_n_w) begin
      fr_g_r <= '0; un_g_r <= '0; sk_g_r <= '0; ep_g_r <= '0;
    end else begin
      fr_g_r <= bin2gray16(frames_b_r);
      un_g_r <= bin2gray16(unders_b_r);
      sk_g_r <= bin2gray16(skips_b_r);
      ep_g_r <= bin2gray16(epochs_b_r);
    end
  end : t_cnt_gray

  logic [15:0] fr_1_r, fr_2_r, un_1_r, un_2_r;
  logic [15:0] sk_1_r, sk_2_r, ep_1_r, ep_2_r;
  always_ff @(posedge clk_i) begin : t_cnt_sync
    if (!rst_n) begin
      fr_1_r <= '0; fr_2_r <= '0; un_1_r <= '0; un_2_r <= '0;
      sk_1_r <= '0; sk_2_r <= '0; ep_1_r <= '0; ep_2_r <= '0;
    end else begin
      {fr_2_r, fr_1_r} <= {fr_1_r, fr_g_r};
      {un_2_r, un_1_r} <= {un_1_r, un_g_r};
      {sk_2_r, sk_1_r} <= {sk_1_r, sk_g_r};
      {ep_2_r, ep_1_r} <= {ep_1_r, ep_g_r};
    end
  end : t_cnt_sync

  assign frames_o    = gray2bin16(fr_2_r);
  assign underruns_o = gray2bin16(un_2_r);
  assign skips_o     = gray2bin16(sk_2_r);
  assign epochs_o    = gray2bin16(ep_2_r);
  assign overruns_o  = overruns_r;       //! clk_i native: no crossing

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_chan_map_capture.sv
  Author      : Kebag Logic

  Date        : 2026-07-23
  Description : Per-pair-slot TX source multiplexer (docs/fpga/FPGA_DESIGN.md
                section 2 capture family; the SW-defined end-station channel map).
                Sits between the several pair-stream sources and the shared
                KL_aaf_packetizer's pair-injection interface: for every one of
                the N_SLOTS_P TX pair slots (the prefix-sum slot space; talker
                t owns chans/2 consecutive slots - see the packetizer header)
                a small map RAM selects which audio source feeds that slot.

                8 talker streams x up to 8 channels = up to 32 stereo PAIR
                slots, so the map is 32 entries deep and the emitted
                pair_slot_o is the full 5-bit (0..31) space the packetizer now
                accepts (the pair_slot widening).

                MAP ENTRY (13 bits, ONE PER STREAM CHANNEL - 0x0027,
                USER 2026-08-06 "one cluster == one audio channel"):
                  {en[12], half[11], src[10:8], idxh[7:4], idx[3:0]}
                  en   - 1 = this channel carries its mono cluster;
                         0 = DIGITAL SILENCE. Either way the channel is
                         injected every media tick: Milan v1.2 5.3.9.1
                         lets a channel be "not mapped", 5.3.7.3 still
                         requires the Stream Output to be streaming.
                  half - WHICH half of the source pair is this channel's
                         mono cluster (0 = L/even, 1 = R/odd). With it,
                         ANY cluster lands on ANY channel: the old parity
                         and pair-slot vendor rules (2 and 3) do not exist
                         in this store - each channel is independent.
                  src - the source bucket:
                          0 ZERO    : digital silence (L=R=0)
                          1 I2S_IN  : the stereo I2S capture pair (idx unused)
                          2 TDM_IN  : TDM pair idx (0..N_TDM_P/2-1; slot pair
                                      idx carries TDM slots {2*idx, 2*idx+1})
                          3 RING    : ALSA playback ring pair idx (the
                                      KL_pcm_tx pair-channel index)
                          4 TONE    : the pilot tone on BOTH channels
                          5 LOOP    : a RECEIVED AAF stream's channel pair -
                                      the rx -> talker LOOPBACK (below)
                        (6..7 reserved -> silence)
                  idx  - the within-source pair index (see src).
                  idxh - the within-source STREAM index. ONLY the LOOP bucket
                         reads it; every other bucket ignores it, which is why
                         it can sit above the legacy byte (see next para).

                SOURCE BUCKETS (wire-truth, free-running): the latest pair per
                FRONT-END source is latched into a hold register the instant
                its pair_valid pulse arrives, so the tick-time walk always
                injects the freshest sample. The tone bucket is the live
                tone_smp_i (both L/R). No CDC lives here - every source has
                already crossed into clk_i. The LOOP bucket is the one
                exception: it is a BURSTY source (a whole PDU of samples at
                wire speed), so it is QUEUED, not held - see LOOP QUEUE.

                LOOP BUCKET (rx -> talker loopback). The other multi-channel
                sources are the board's physical capture front-ends, and the
                tone is by construction the SAME value on L and R, so a
                received AAF stream is a source of real, per-channel DISTINCT
                audio: this bucket makes any (rx stream, channel pair) a
                talker pair source.

                CORRECTED 0x0042 - this paragraph used to say the AX7101 has
                NO physical capture front end ("no pmoda -> i2s_sdout tied 0;
                the TDM slave pins are tied 0 on every SoC"). That was written
                before the item-4 TDM header existed and is now false twice
                over: the AX7101 routes a TDM8 bus on J11.3-J11.8 and the
                shipping shape drives it as a bus MASTER, which generates its
                own bclk/fsync and is therefore a real front end with or
                without a codec behind it. The claim about TDM SLAVE pins
                remains true and is a different statement. The practical
                consequence of the stale version was that the slot-indexed
                TDM bucket below looked pointless, so milan_datapath tied
                tdm_pair_valid_i to 1'b0 and every capture pair collapsed into
                the single-pair I2S hold - see that port's comment.

                It consumes the depacketizer payload AXIS exactly as
                KL_chan_map_render does (that de-interleave is the proven
                one and this is a deliberate mirror of it): 64-bit beats = 2
                consecutive S32BE samples in wire order, one AXIS frame per
                PDU, tuser = stream index. CLONE QUALIFIER: this tap never
                backpressures (no tready), so lb_tvalid_i must be the
                ACCEPTED-beat strobe (tvalid && tready) of the tapped link.

                De-interleave per IEEE 1722-2016 7.3.5: an AAF-PCM payload
                carries its sample events chronologically and, within one
                event, one sample per channel in channel order, so payload
                sample k belongs to wire channel k % channels_per_frame
                (7.3.3, the count the RX monitors report on lb_wire_chans_i;
                0 = pre-first-accept, treated as 2). The position counter
                advances by wrap-compare (no modulo hardware) and restarts at
                every tlast, so back-to-back PDUs of different streams /
                channel counts stay aligned. Channels beyond N_LB_CH_P are
                virtual: counted for the interleave, never queued.

                PAIRING, and why L/R cannot cross: a pair p of the entry is
                wire channels {2p, 2p+1} = {L, R} - the same pairing the
                packetizer applies on the way out (pair slot p of a talker
                emits its L into channel 2p and its R into 2p+1), so a pair
                that goes round the loop keeps its channel identity. The
                de-interleave assembles each sample EVENT's {L, R} by the
                samples' own channel parity, never by arrival order, so an
                odd-length beat boundary or a mid-frame stall cannot swap
                them. An event whose R channel does not exist on the wire
                (odd channels_per_frame: the dangling last channel, or the
                1-channel mono wire) commits {L, 24'd0}.

                LOOP QUEUE (paced sequence replay - the 0x0036 rework). The
                pre-queue bucket was a latest-sample hold, the same slip
                policy as the front-end buckets - CORRECT for once-per-sample
                sources, WRONG for a source that bursts a 6-sample PDU at
                wire speed: the walk read the block's last sample ~5 times
                and skipped the rest, a dup+skip stair on the 8 kHz PDU
                lattice (user audio capture 2026-08-09: 9895 glitches/s with
                8000 +/- 1000 Hz sidebands; tb/verilator/milan_dp [T68]
                measured 76 dup / 56 skip per 60 sent at the desk). That slip
                law is SUPERSEDED for this bucket by a per-pair elastic
                queue:

                  * STORAGE: LB_PAIRS_C x LB_QDEPTH_C x 48 b, one flat
                    single-write single-read array (256 x 48 at the 8x8 ship
                    shape = one RAMB36 or ~200 LUT of LUTRAM; the array takes
                    no reset - the per-pair pointers make unwritten words
                    unreachable). LB_QDEPTH_C = 8 = one class-A PDU (6 sample
                    events, Milan 6.3.5) + 2 events of arrival-jitter margin.
                  * PUSH: the de-interleave commits one complete {L, R}
                    sample event per pair as its samples arrive. A beat can
                    carry TWO commits (the 1-channel mono wire puts both of
                    its samples on pair 0; an odd-channel wire can close one
                    event and end another in the same beat), so commits pass
                    through a 4-deep skid that drains one push per cycle into
                    the array. Wire beats are >= 8 clk_i apart (64-bit beats
                    from the byte-serial MAC), so the skid cannot
                    sustainably overflow; if a harness drives faster anyway
                    the NEWEST commit is refused and counted on
                    lb_skip_cnt_o.
                  * POP: each media tick runs a PRE-WALK of LB_PAIRS_C + 1
                    cycles before the slot walk, popping exactly one event
                    per non-empty pair into the lb_hold_r bank; the slot walk
                    then reads the holds exactly as before. EVERY fed pair is
                    popped, mapped or not, so a remap never replays samples
                    that queued up while the pair was unmapped.
                  * PRIME: a pair starts popping only after its stream's
                    first complete PDU (the accepted tlast beat) - popping
                    mid-first-burst would re-open the premature-read the
                    queue exists to close. Priming is per stream, cleared
                    only by reset/flush.
                  * SLIP, HONEST AND BOUNDED: queue empty at a tick
                    (upstream slower) = the hold repeats the last event, ONE
                    dup, counted on lb_dup_cnt_o (primed AND fed pairs only,
                    so an idle pair counts nothing). Queue full at a push
                    (upstream faster) = the OLDEST event is dropped, ONE
                    skip, counted on lb_skip_cnt_o. Both counters saturate
                    at 16'hFFFF. With locked clocks both stay at ZERO - the
                    acceptance state ([T68] LB_SEQ_FIXED).
                  * FLUSH: lb_flush_i[s] (bind wipe / stream-table eviction)
                    empties stream s's pair queues, un-primes and un-feeds
                    them, kills its in-flight skid entries and assembly
                    stash, and zeroes its holds - no stale samples replay on
                    a rebind. loop_fed_r (the R5 capability rail) stays
                    sticky since reset: it answers "does the tap reach this
                    module at all", which a bind cycle does not change.

                MAPPED-BUT-UNFED (docs/testing/methodology.md R5): a loopback
                slot with no payload behind it emits 24'd0 - the same bytes a
                working, quiet slot emits. The map readback therefore carries
                a two-bit CAPABILITY MASK (see map_rd_data_o) so "not
                connected" and "connected and silent" are never the same
                reading. This matters more than it looks: the AX7101 routes
                no audio pins in either direction, so on that board EVERY
                talker's audio comes through this bucket and a lying zero
                here is a lying zero for the whole product.

                VERIFICATION (methodology levels / oracles):
                  L0 tb/verilator/chmap_capture - this module against the
                     clause-derived expectation, per-channel DISTINCT values
                     throughout (R4), with TWO negative controls: a
                     single-parity inversion (11 failures) and a full L/R
                     swap (17 failures, values perfectly transposed). The
                     queue law's own legs: paced in-order replay (oldest
                     first), empty-tick repeat counted, overflow drop-oldest
                     counted, flush-on-rebind, the mono degenerate wire, and
                     the all-32-pairs concurrent ramp.
                  L2 the same harness runs the pairs through the REAL
                     KL_aaf_packetizer and reads the emitted AVTPDU payload
                     bytes - the oracle is the frame on the AXIS port, not
                     an internal signal.
                  L3 tests/features/chmap_capture_identity.feature - the
                     clause itself (7.3.3 / 7.3.5 / 1722.1 7.2.19) restated
                     as an independent model, so a model/RTL divergence is a
                     disagreement rather than two copies of one mistake.
                  L1 the milan_datapath binding is NOT provable from inside
                     this file: the loopback pins are DEFAULTED, so an
                     unwired integration elaborates, synthesises and passes
                     every L0/L2 check while carrying no audio at all. That
                     is exactly what the capability mask exists to catch -
                     loop_mapped=1 with loop_fed=0 IS the unwired binding,
                     and it is the first thing the silicon procedure reads.
                     The paced-replay law at the datapath level is
                     tb/verilator/milan_dp [T68]: zero dup / zero skip /
                     zero alien against a paced ramp through the whole RX ->
                     loop -> TX path.

                EMIT (media sample tick): on tick_i the engine first runs the
                LOOP pre-walk (pop one queued event per fed pair into
                lb_hold_r), then walks the slot map low-to-high; EVERY slot
                injects one pair (pair_valid_o one-cycle pulse + pair_slot_o
                + pair_l_o/pair_r_o) then idles GAP_CYC_P cycles before the
                next slot - the proven inject cadence the packetizer admits
                (one pair per cycle with a settle gap, mirroring the golden
                NxN TB's pair()). An unmapped slot injects silence rather
                than being skipped: it is the packetizer's per-sample slot
                coverage that decides whether a talker frames at all, and
                while this crossbar is armed it OWNS that coverage -
                milan_datapath muxes the KL_pair_zero_fill guard out of the
                path. Skipping therefore cost the WHOLE talker its stream,
                not one channel its audio (Milan v1.2 5.3.7.3). Six media
                ticks (6 samples/ch) fill one AVTPDU per talker on the shared
                6-sample cadence; a tick arriving mid-walk is queued one deep
                (never dropped).

                WALK BUDGET: the pre-walk costs LB_PAIRS_C + 1 cycles (one
                pop issue per pair, one data-return drain), then a slot costs
                one CM_STEP_S cycle plus the GAP_CYC_P+1 cycles CM_GAP_S
                takes to count GAP_CYC_P down to zero AND advance, so the
                walk is 1 + (LB_PAIRS_C + 1) + N_SLOTS_P * (GAP_CYC_P + 2)
                cycles including the CM_IDLE_S cycle that starts it, and it
                must fit inside one media tick. At the shipping 8x8 that is
                1 + 33 + 32*26 = 866 against MILAN_CLK_FREQ_HZ/48000 (2083
                at 100 MHz, 1041 at 50 MHz - the worst-case budget). Covering
                the unmapped slots does not raise that ceiling - a fully
                mapped board already pays all 32, and the shipped 8x8 map is
                fully mapped - it only stops a sparsely mapped board from
                finishing early. tb/verilator/chmap_capture [A4] MEASURES
                the walk against the budget rather than restating it, with
                an all-unmapped map, which is now the worst case.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Per-pair-slot TX source mux (NXN §2.1 capture family): a 32-slot map RAM
//! ({half, idxh, en, src, idx}) routes each packetizer pair slot to a source
//! bucket, with a per-half enable so one stream channel of a slot can be
//! mapped while its sibling stays silent
//! (I2S capture / TDM / ALSA ring / tone / RX-stream loopback / silence);
//! free-running source holds, per-tick low-to-high slot walk emitting the
//! packetizer inject cadence (one pulse + GAP_CYC_P settle) on EVERY slot,
//! unmapped ones carrying PCM silence so an unmapped channel never costs its
//! talker the stream. The loopback bucket de-interleaves the depacketizer
//! payload clone
//! (IEEE 1722-2016 7.3.3/7.3.5) into per-(stream, channel pair) elastic
//! queues (depth 8 = one PDU + margin) popped one event per media tick -
//! paced in-order replay of a bursty source, dup-on-empty / drop-oldest-on-
//! full counted honestly, flushed on bind wipe. Single clock, no CDC.

`default_nettype none

module KL_chan_map_capture #(
  parameter int unsigned N_SLOTS_P = 32,   //! TX pair slots (prefix-sum space)
  parameter int unsigned N_TDM_P   = 8,    //! TDM slots (pairs = N_TDM_P/2)
  parameter int unsigned N_RING_P  = 16,   //! ALSA ring pair sources (idx 0..15)
  parameter int unsigned GAP_CYC_P = 24,   //! settle cycles between slot injects
  //! LOOP bucket sizing: the RX stream-channel space kept as pair queues
  //! (N_LB_STREAMS_P * N_LB_CH_P/2 pair queues x LB_QDEPTH_C x 48 b).
  //! Elaborate it down (1 / 2) on a build that has no listener to loop back
  //! from.
  parameter int unsigned N_LB_STREAMS_P = 8, //! RX streams kept (idxh < this)
  parameter int unsigned N_LB_CH_P      = 8  //! wire channels kept per stream
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset

  //! --- map RAM write port (the AEM mirror / CSR debug window / TB) -------
  //! PER-CHANNEL since 0x0027 (USER 2026-08-06: "one cluster == one audio
  //! channel"): the store holds one entry PER STREAM CHANNEL, each
  //! independently selecting one MONO cluster = {source bucket, stream
  //! (idxh), pair idx, half}. No pair coupling exists anywhere in the map:
  //! the old slot-granular store forced ATDECC edits into remove-both/
  //! add-both pair dances (vendor rules 2 and 3), which is exactly what
  //! this rework retires.
  input  wire         map_wr_en_i,       //! one-cycle write strobe
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_wr_addr_i, //! CHANNEL key
  input  wire [12:0]  map_wr_data_i,     //! {en[12], half[11], src[10:8],
                                         //!  idxh[7:4], idx[3:0]}
  //! --- map RAM readback port (registered, 1-cycle latency) ---------------
  input  wire         map_rd_en_i,       //! one-cycle read request
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_rd_addr_i, //! CHANNEL key
  //! {loop_fed[14], loop_mapped[13], entry[12:0]}. entry = the addressed
  //! CHANNEL's word {en, half, src, idxh, idx}. [14:13] is the LOOP bucket's
  //! CAPABILITY MASK: a loopback channel that is mapped but has never been
  //! FED emits 24'd0, bit-for-bit what a working-but-quiet one emits -
  //! without the mask an unwired listener side reports a LYING ZERO no
  //! counter contradicts (the AX7101 routes no audio pins, so its talkers
  //! depend ENTIRELY on the loop bucket).
  //!   mapped=0            : the bucket is not in use
  //!   mapped=1, fed=0     : mapped and NEVER FED - a silent talker here is
  //!                         a BINDING or stream fault, not quiet audio
  //!   mapped=1, fed=1     : live; zeros in the payload are real silence
  output logic [14:0] map_rd_data_o,     //! (valid with rd_valid)
  output logic        map_rd_valid_o,    //! read data valid this cycle
  //! the whole store as wires (the render side's map_flat_o precedent):
  //! entry k = channel k's {en, half, src, idxh, idx}. Pure fan-out of
  //! flops that already exist - zero logic - so the fabric's GET_AUDIO_MAP
  //! answer block can walk the OUTPUT-side mappings the same way it walks
  //! the render map, without arbitrating the CSR's read port.
  output logic [2*N_SLOTS_P*13-1:0] map_flat_o,

  //! --- I2S capture pair source (single stereo pair) ----------------------
  input  wire         i2s_pair_valid_i,  //! latch pulse
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,

  //! --- TDM capture pair sources (indexed by pair slot) -------------------
  //! public_flat_rd: milan_datapath tied this to 1'b0 until 0x0042, which
  //! collapsed every capture pair into the SINGLE-pair I2S hold and made a
  //! physical cluster past channel 1 unbackable on every shape. "Does this
  //! port ever pulse" is the tie-off detector - and it must be the PORT, not
  //! the hold register behind it: a harness that leaves the codec data pins
  //! at zero writes the hold with zeros forever, so watching the hold for a
  //! CHANGE reports a dead feed as healthy (it did, first try).
  input  wire         tdm_pair_valid_i /* verilator public_flat_rd */,  //! latch pulse
  input  wire [3:0]   tdm_pair_slot_i,   //! TDM pair index (0..N_TDM_P/2-1)
  input  wire [23:0]  tdm_l_i,
  input  wire [23:0]  tdm_r_i,

  //! --- ALSA ring pair sources (KL_pcm_tx output, indexed by pair slot) ---
  //! The slot bus is the widened 5-bit KL_pcm_tx space; pairs >= N_RING_P
  //! are REFUSED by the bounds check below (dropped, never aliased), so a
  //! 16-deep bucket covers ring pairs 0..15 = playback streams 0..3 of the
  //! 8x8x8 shape and the rest need N_RING_P raised, not a wider idx.
  input  wire         ring_pair_valid_i, //! latch pulse
  input  wire [4:0]   ring_pair_slot_i,  //! ring pair-channel index (0..N-1)
  input  wire [23:0]  ring_l_i,
  input  wire [23:0]  ring_r_i,

  //! --- tone generator sample (live; drives both L/R when TONE) -----------
  input  wire [23:0]  tone_smp_i,

  //! --- LOOP source: the depacketizer payload AXIS clone (rx -> talker) ---
  //! Never backpressured (no tready): drive lb_tvalid_i with the tapped
  //! link's ACCEPTED beats (tvalid && tready), the same clone discipline as
  //! KL_chan_map_render's tap.
  //! ALL DEFAULTED: an integration that has not wired the listener side
  //! leaves them off and gets a bucket that is permanently silent - a
  //! DEFINED state, not a dangling pin.
  input  wire [63:0]  lb_tdata_i  = 64'd0, //! 2 consecutive S32BE samples,
                                         //! wire (channel-interleaved) order
  input  wire         lb_tvalid_i = 1'b0, //! accepted-beat strobe
  input  wire         lb_tlast_i  = 1'b0, //! one AXIS frame per PDU
  input  wire [3:0]   lb_tuser_i  = 4'd0, //! RX stream index s of this PDU
  //! per-stream wire channels_per_frame (7.3.3) - RX monitors' wire_chans_o
  input  wire [N_LB_STREAMS_P*4-1:0] lb_wire_chans_i = '0, //! fields; 0 -> 2
  //! bind wipe / stream-table eviction pulse per RX stream: empties the
  //! stream's pair queues, un-primes them and zeroes its holds, so no stale
  //! samples replay on a rebind. Defaulted off: an integration without a
  //! bind plane keeps the free-running behaviour.
  input  wire [N_LB_STREAMS_P-1:0] lb_flush_i = '0,

  //! --- media sample tick (one walk of the enabled slots per pulse) -------
  input  wire         tick_i,

  //! --- pair injection to the shared packetizer (its capture contract) ----
  output logic        pair_valid_o,      //! one-cycle pulse per L/R pair
  output logic [4:0]  pair_slot_o,       //! pair slot 0..31 (widened space)
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  //! --- LOOP queue slip evidence (saturating; ZERO with locked clocks) ----
  output logic [15:0] lb_dup_cnt_o,      //! empty-at-tick repeats (fed pairs)
  output logic [15:0] lb_skip_cnt_o      //! dropped events (full / skid ovf)
);

  // ---------------------------------------------------------------------- //
  // Derived sizing                                                          //
  // ---------------------------------------------------------------------- //
  localparam int unsigned SLOTW_C      = $clog2(N_SLOTS_P);
  localparam int unsigned N_TDM_PAIRS_C = (N_TDM_P < 2) ? 1 : N_TDM_P / 2;
  localparam int unsigned TDMPW_C      = (N_TDM_PAIRS_C <= 1) ? 1
                                                      : $clog2(N_TDM_PAIRS_C);
  localparam int unsigned RINGPW_C     = (N_RING_P <= 1) ? 1
                                                      : $clog2(N_RING_P);
  //! LOOP bucket: pair queues per stream, then the flat bank and its address
  localparam int unsigned LB_PPS_C     = (N_LB_CH_P < 2) ? 1 : N_LB_CH_P / 2;
  localparam int unsigned LB_PAIRS_C   = N_LB_STREAMS_P * LB_PPS_C;
  localparam int unsigned LBPW_C       = (LB_PAIRS_C <= 1) ? 1
                                                      : $clog2(LB_PAIRS_C);
  //! LOOP queue: 8 events deep = one class-A PDU (6 sample events) + 2 of
  //! arrival-jitter margin; skid depth 4 absorbs the 2-commits-per-beat
  //! degenerate beats (mono wire) at the >= 8-cycle wire beat spacing
  localparam int unsigned LB_QDEPTH_C  = 8;
  localparam int unsigned LB_QPTRW_C   = $clog2(LB_QDEPTH_C);
  //! the flat queue RAM's own index width - {pair,ptr} can be one bit
  //! wider than the array needs when LB_PAIRS_C is not a power of two,
  //! and the surplus high bit is always zero (pair < LB_PAIRS_C).
  localparam int unsigned LB_QAW_C     = $clog2(LB_PAIRS_C * LB_QDEPTH_C);
  localparam int unsigned LB_SKID_C    = 4;
  //! pre-walk pop index space (0..LB_PAIRS_C, the +1 is the drain cycle)
  localparam int unsigned LB_POPW_C    = $clog2(LB_PAIRS_C + 1);

  //! map entry field encoding (src[6:4])
  localparam logic [2:0] SRC_ZERO_C = 3'd0, SRC_I2S_C = 3'd1, SRC_TDM_C = 3'd2,
                         SRC_RING_C = 3'd3, SRC_TONE_C = 3'd4,
                         SRC_LOOP_C = 3'd5;

  // ---------------------------------------------------------------------- //
  // Map RAM (small config store: flop register file, like KL_pcm_route)     //
  //   one sync write process; combinational reads for the walk; the         //
  //   readback port registers a snapshot (RAM house style read turnaround)  //
  // ---------------------------------------------------------------------- //
  //! one 13-bit entry PER STREAM CHANNEL (2 per pair slot)
  logic [12:0] map_r [2*N_SLOTS_P];

  for (genvar gmf = 0; gmf < 2*N_SLOTS_P; gmf++) begin : g_map_flat
    assign map_flat_o[gmf*13 +: 13] = map_r[gmf];
  end

  always_ff @(posedge clk_i) begin : map_write_port
    if (!rst_n) begin
      for (int s = 0; s < 2*N_SLOTS_P; s++) map_r[s] <= 13'h0000;
    end
    else if (map_wr_en_i) begin
      map_r[map_wr_addr_i] <= map_wr_data_i;
    end
  end : map_write_port

  //! --- LOOP capability mask (the R5 "never a lying 0" rail) --------------
  //! mapped: LIVE - any enabled entry selecting the LOOP bucket. Declared by
  //! the map, so it answers "is this board's talker supposed to be carrying
  //! received audio right now?" without looking at a sample.
  logic loop_mapped_w;
  always_comb begin : loop_mapped_scan
    loop_mapped_w = 1'b0;
    for (int s = 0; s < 2*N_SLOTS_P; s++) begin
      if (map_r[s][12] && (map_r[s][10:8] == SRC_LOOP_C)) loop_mapped_w = 1'b1;
    end
  end : loop_mapped_scan

  //! fed: STICKY since reset - at least one loopback payload beat has been
  //! ACCEPTED. Deliberately not "recently" and deliberately NOT cleared by
  //! lb_flush_i: this bit separates "the listener side is not connected to
  //! me at all" (the binding fault) from "it is connected and the stream is
  //! silent or stopped", which the RX monitors' own live counters already
  //! answer - a bind cycle does not change the wiring.
  logic loop_fed_r;

  always_ff @(posedge clk_i) begin : map_read_port
    if (!rst_n) begin
      map_rd_data_o  <= 15'h0000;
      map_rd_valid_o <= 1'b0;
    end
    else begin
      map_rd_valid_o <= 1'b0;
      if (map_rd_en_i) begin
        map_rd_data_o  <= {loop_fed_r, loop_mapped_w,
                           map_r[map_rd_addr_i]};
        map_rd_valid_o <= 1'b1;
      end
    end
  end : map_read_port

  // ---------------------------------------------------------------------- //
  // Source hold buckets (latch the latest pair per source; wire-truth)      //
  // ---------------------------------------------------------------------- //
  logic [47:0] i2s_hold_r;               //! the single stereo I2S pair
  //! public_flat_rd: the slot-indexed physical bucket. It was tied off in
  //! milan_datapath until 0x0042, so "was it ever written" is the check that
  //! a physical cluster beyond channels 0..1 can be backed at all - and it is
  //! the one a tie-off regression would trip.
  logic [47:0] tdm_hold_r  [N_TDM_PAIRS_C] /* verilator public_flat_rd */;
  logic [47:0] ring_hold_r [N_RING_P];

  always_ff @(posedge clk_i) begin : source_latch
    if (!rst_n) begin
      i2s_hold_r <= '0;
      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_hold_r[t]  <= '0;
      for (int r = 0; r < N_RING_P;      r++) ring_hold_r[r] <= '0;
    end
    else begin
      if (i2s_pair_valid_i) i2s_hold_r <= {i2s_l_i, i2s_r_i};
      if (tdm_pair_valid_i && (32'(tdm_pair_slot_i) < N_TDM_PAIRS_C))
        tdm_hold_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= {tdm_l_i, tdm_r_i};
      if (ring_pair_valid_i && (32'(ring_pair_slot_i) < N_RING_P))
        ring_hold_r[ring_pair_slot_i[RINGPW_C-1:0]] <= {ring_l_i, ring_r_i};
    end
  end : source_latch

  // ---------------------------------------------------------------------- //
  // LOOP bucket stage 1: de-interleave the depacketizer payload clone into  //
  // complete {L, R} sample-event COMMITS, one per pair per event.           //
  //                                                                         //
  // This mirrors KL_chan_map_render's sample_latch deliberately - same beat //
  // format, same wrap-compare position counter, same tlast restart, same    //
  // "virtual channels are walked but never kept" rule - because that is     //
  // the de-interleave that has been proven on the wire. The store shape is  //
  // PAIR-granular (§4.2): an event's L (even channel) and R (odd channel)   //
  // are joined into one 48-bit commit by the samples' own channel PARITY,   //
  // so arrival order cannot swap them; an event whose R channel does not    //
  // exist on the wire (odd channels_per_frame / mono) commits {L, 24'd0}.   //
  // ---------------------------------------------------------------------- //
  logic [3:0]  lb_chpos_r;               //! wire channel of the beat's smp0

  //! channels_per_frame of the in-flight stream (constant-base mux, guarded
  //! against tuser >= N_LB_STREAMS_P; 0 treated as 2 - the pre-first-accept
  //! rule KL_chan_map_render and KL_i2s_playback both apply)
  logic [3:0] lb_chans_raw_w;
  always_comb begin : lb_chans_lookup
    lb_chans_raw_w = 4'd0;
    for (int s = 0; s < N_LB_STREAMS_P; s++) begin
      if (32'(lb_tuser_i) == s) lb_chans_raw_w = lb_wire_chans_i[s*4 +: 4];
    end
  end : lb_chans_lookup
  wire [3:0] lb_chans_w = (lb_chans_raw_w == 4'd0) ? 4'd2 : lb_chans_raw_w;

  //! increment-with-wrap (ch is always < chans, so +1 never runs past the
  //! compare) - the modulo of 7.3.5 without a divider
  function automatic logic [3:0] lb_chwrap(input logic [3:0] ch,
                                           input logic [3:0] chans);
    lb_chwrap = ((4'(ch + 4'd1)) == chans) ? 4'd0 : 4'(ch + 4'd1);
  endfunction

  //! flat pair address of (stream s, wire channel c) = s*(N_LB_CH_P/2) + c/2
  function automatic logic [LBPW_C-1:0] lb_addr(input logic [3:0] s,
                                                input logic [3:0] c);
    lb_addr = LBPW_C'(32'(s) * LB_PPS_C + (32'(c) >> 1));
  endfunction

  //! the beat's two S32BE samples: wire byte first = MSB, byte lane j = wire
  //! byte j (the depacketizer's out_assemble); the top 24 bits are the
  //! 24-in-32 left-justified audio, the pad byte (lanes 3/7) is dropped
  wire [23:0] lb_smp0_w = {lb_tdata_i[7:0],   lb_tdata_i[15:8],
                           lb_tdata_i[23:16]};
  wire [23:0] lb_smp1_w = {lb_tdata_i[39:32], lb_tdata_i[47:40],
                           lb_tdata_i[55:48]};
  wire [3:0]  lb_ch0_w  = lb_chpos_r;
  wire [3:0]  lb_ch1_w  = lb_chwrap(lb_ch0_w, lb_chans_w);

  wire lb_ok_w = lb_tvalid_i && (32'(lb_tuser_i) < N_LB_STREAMS_P);
  wire lb_w0_w = lb_ok_w && (32'(lb_ch0_w) < N_LB_CH_P);
  wire lb_w1_w = lb_ok_w && (32'(lb_ch1_w) < N_LB_CH_P);

  //! ---- loopback indexing as PLAIN COMB WIRES (hazard-class hoist) --------
  //! Hazard class: an `automatic` function temporary computed and consumed
  //! INSIDE a clocked process, feeding a RAM write address / lane select /
  //! source index. Vivado has bound such temporaries against a re-timed copy
  //! of an advancing register while Verilator matched the RTL intent - the
  //! VERSION 0x0030 seeder hoist in KL_aecp_response_builder (w_odsd_v /
  //! w_odsd_t, the 0x002D silicon +1-key shift) is the precedent, and the
  //! t532 capture-side find (silicon 2026-08-09: fabric-side map writes and
  //! LOOP taps landing off-by-one against a byte-exact AECP store) is the
  //! same signature on THIS path. lb_addr()/lb_chwrap() are evaluated here
  //! at module scope; every clocked process below indexes ONLY through
  //! these wires, so nothing is left for synthesis to re-time against the
  //! position walk.
  wire [LBPW_C-1:0] lb_a0_w  = lb_addr(lb_tuser_i, lb_ch0_w);
  wire [LBPW_C-1:0] lb_a1_w  = lb_addr(lb_tuser_i, lb_ch1_w);
  wire [3:0]        lb_nxt_w = lb_tlast_i ? 4'd0
                                          : lb_chwrap(lb_ch1_w, lb_chans_w);

  //! ---- event assembly: the one dangling L an in-flight frame can carry ---
  //! Frames never interleave beats (one AXIS frame per PDU), so a single
  //! stash suffices: an even non-final channel opens it, the odd channel
  //! that follows closes it into a commit. It cannot survive a frame end -
  //! tlast either force-commits it ({L, 0}, the truncated-frame rule) or
  //! finds it already consumed.
  logic        stash_vld_r;
  logic [23:0] stash_val_r;
  logic [3:0]  stash_strm_r;

  //! smp0/smp1 event roles (chronological order per 7.3.5). ch1 odd implies
  //! ch1 = ch0+1 with ch0 even non-final (the wrap lands on 0 = even), so
  //! the "aligned full pair in one beat" case below is exhaustive for it.
  wire lb_last0_w = (32'(lb_ch0_w) == 32'(lb_chans_w) - 1);
  wire lb_last1_w = (32'(lb_ch1_w) == 32'(lb_chans_w) - 1);
  //! smp0: odd channel closes the stash; even final channel is an {L, 0}
  //! event of its own (mono / odd channel count)
  wire cm0_v_w    = lb_w0_w && (lb_ch0_w[0] || lb_last0_w);
  wire [23:0] cm0_l_w = stash_vld_r ? stash_val_r : 24'd0;
  wire [47:0] cm0_data_w = lb_ch0_w[0] ? {cm0_l_w, lb_smp0_w}
                                       : {lb_smp0_w, 24'd0};
  wire [LBPW_C-1:0] cm0_addr_w = lb_a0_w;
  //! smp1: consumed by smp0 into one aligned {smp0, smp1} commit, or an
  //! {L, 0} event of its own, or it opens the stash (force-committed {L, 0}
  //! when the frame ends on this very beat)
  wire lb_pair01_w = lb_w0_w && lb_w1_w && !lb_ch0_w[0] && !lb_last0_w;
  wire cm1_solo_v_w = !lb_pair01_w && lb_w1_w && !lb_ch1_w[0]
                      && (lb_last1_w || lb_tlast_i);
  wire cm1_v_w    = lb_pair01_w || cm1_solo_v_w;
  wire [47:0] cm1_data_w = lb_pair01_w ? {lb_smp0_w, lb_smp1_w}
                                       : {lb_smp1_w, 24'd0};
  wire [LBPW_C-1:0] cm1_addr_w = lb_pair01_w ? lb_a0_w : lb_a1_w;
  wire stash_open_w = !lb_pair01_w && lb_w1_w && !lb_ch1_w[0]
                      && !lb_last1_w && !lb_tlast_i;

  //! flush aimed at the stash's own stream (scan style as lb_chans_lookup)
  logic stash_flush_w;
  always_comb begin : stash_flush_scan
    stash_flush_w = 1'b0;
    for (int s = 0; s < N_LB_STREAMS_P; s++) begin
      if (lb_flush_i[s] && (32'(stash_strm_r) == s)) stash_flush_w = 1'b1;
    end
  end : stash_flush_scan

  //! flush aimed at the IN-FLIGHT beat's stream: its commits must not slip
  //! into the queue on the very cycle the bind wipe empties it
  logic beat_flush_w;
  always_comb begin : beat_flush_scan
    beat_flush_w = 1'b0;
    for (int s = 0; s < N_LB_STREAMS_P; s++) begin
      if (lb_flush_i[s] && (32'(lb_tuser_i) == s)) beat_flush_w = 1'b1;
    end
  end : beat_flush_scan

  always_ff @(posedge clk_i) begin : loopback_deinterleave
    if (!rst_n) begin
      lb_chpos_r   <= 4'd0;
      loop_fed_r   <= 1'b0;
      stash_vld_r  <= 1'b0;
      stash_val_r  <= 24'd0;
      stash_strm_r <= 4'd0;
    end
    else begin
      //! the capability rail: ANY accepted beat, even one whose stream index
      //! this build does not keep - the question it answers is whether the
      //! payload clone reaches this module at all
      if (lb_tvalid_i) loop_fed_r <= 1'b1;
      //! the walk advances on EVERY accepted beat (a beat of an unkept
      //! stream still consumes two payload samples) and restarts at tlast;
      //! position/next come ONLY from the module-scope hoists above (the
      //! 0x0030 hazard-class rule)
      if (lb_tvalid_i) begin
        lb_chpos_r  <= lb_nxt_w;
        stash_vld_r <= stash_open_w;
        if (stash_open_w) begin
          stash_val_r  <= lb_smp1_w;
          stash_strm_r <= lb_tuser_i;
        end
      end
      //! a bind wipe kills the wiped stream's half-assembled event
      if (stash_flush_w) stash_vld_r <= 1'b0;
    end
  end : loopback_deinterleave

  // ---------------------------------------------------------------------- //
  // LOOP bucket stage 2: the per-pair elastic queues (paced replay).        //
  //   skid (4 deep, up to 2 commits in / 1 push out per cycle)              //
  //   -> flat queue array LB_PAIRS_C x LB_QDEPTH_C x 48 b (1W/1R, no reset) //
  //   -> pre-walk pop, one event per fed pair per media tick, into          //
  //      lb_hold_r, which the slot walk reads exactly as before.            //
  // ---------------------------------------------------------------------- //
  logic [47:0] lb_q_r [LB_PAIRS_C * LB_QDEPTH_C]; //! pointer-guarded, no rst
  logic [LB_QPTRW_C-1:0] q_wr_r  [LB_PAIRS_C];
  logic [LB_QPTRW_C-1:0] q_rd_r  [LB_PAIRS_C];
  logic [LB_QPTRW_C:0]   q_cnt_r [LB_PAIRS_C];   //! 0..LB_QDEPTH_C
  logic [LB_PAIRS_C-1:0] q_fed_r;                //! pushed since reset/flush
  logic [LB_PAIRS_C-1:0] q_primed_r;             //! first whole PDU seen
  logic [47:0] lb_hold_r [LB_PAIRS_C];           //! the walk's read bank

  //! ---- skid (flop FIFO; entries also carry the stream for flush kills) --
  logic [47:0]       skid_data_r [LB_SKID_C];
  logic [LBPW_C-1:0] skid_addr_r [LB_SKID_C];
  logic [3:0]        skid_strm_r [LB_SKID_C];
  logic [LB_SKID_C-1:0] skid_v_r;
  logic [1:0]        skid_wp_r, skid_rp_r;
  logic [2:0]        skid_cnt_r;

  //! drain one entry per cycle whenever the skid holds any; a head entry
  //! killed by a flush is skipped (advances, writes nothing)
  wire skid_drain_w = (skid_cnt_r != 3'd0);
  wire push_ram_w   = skid_drain_w && skid_v_r[skid_rp_r];
  wire [LBPW_C-1:0] push_pair_w = skid_addr_r[skid_rp_r];
  wire [47:0]       push_data_w = skid_data_r[skid_rp_r];

  //! enqueue admission: up to 2 commits per beat, drop the NEWEST (counted)
  //! if a harness outruns the >= 8-cycle wire beat spacing; a same-cycle
  //! flush of the beat's own stream refuses its commits outright (uncounted:
  //! the wipe, not congestion, discarded them)
  wire [2:0] skid_free_w = 3'(LB_SKID_C) - skid_cnt_r
                           + (skid_drain_w ? 3'd1 : 3'd0);
  wire skid_acc0_w = cm0_v_w && !beat_flush_w && (skid_free_w >= 3'd1);
  wire skid_acc1_w = cm1_v_w && !beat_flush_w
                     && (skid_free_w >= (cm0_v_w ? 3'd2 : 3'd1));
  wire skid_ovf0_w = cm0_v_w && !beat_flush_w && !skid_acc0_w;
  wire skid_ovf1_w = cm1_v_w && !beat_flush_w && !skid_acc1_w;
  //! slot 0 of the enqueue carries cm0 when present, else cm1
  wire enq0_v_w = cm0_v_w ? skid_acc0_w : skid_acc1_w;
  wire [47:0]       enq0_data_w = cm0_v_w ? cm0_data_w : cm1_data_w;
  wire [LBPW_C-1:0] enq0_addr_w = cm0_v_w ? cm0_addr_w : cm1_addr_w;
  wire enq1_v_w = cm0_v_w && skid_acc1_w;
  wire [1:0] skid_wp0_w = skid_wp_r;
  wire [1:0] skid_wp1_w = skid_wp_r + 2'd1;
  wire [1:0] skid_enq_n_w = 2'(enq0_v_w) + 2'(enq1_v_w);

  //! flush kill mask over the live skid entries (comb scan, constant unroll)
  logic [LB_SKID_C-1:0] skid_kill_w;
  always_comb begin : skid_kill_scan
    skid_kill_w = '0;
    for (int k = 0; k < int'(LB_SKID_C); k++) begin
      for (int s = 0; s < N_LB_STREAMS_P; s++) begin
        if (skid_v_r[k] && lb_flush_i[s] && (32'(skid_strm_r[k]) == s))
          skid_kill_w[k] = 1'b1;
      end
    end
  end : skid_kill_scan

  // ---- pre-walk pop control (sequenced by the emit FSM below) ----------- //
  typedef enum logic [1:0] {
    CM_IDLE_S,     //! wait for a media tick
    CM_POP_S,      //! LOOP pre-walk: pop one queued event per fed pair
    CM_STEP_S,     //! decide the current slot: emit
    CM_GAP_S       //! settle gap after a pair pulse
  } cstate_t;

  cstate_t                st_r;
  logic [LB_POPW_C-1:0]   pop_idx_r;     //! pre-walk pair cursor
  wire  [LBPW_C-1:0]      pop_pair_w = pop_idx_r[LBPW_C-1:0];
  wire pop_visit_w = (st_r == CM_POP_S) && (32'(pop_idx_r) < LB_PAIRS_C);
  //! pop only primed pairs: popping mid-first-PDU would re-open the
  //! premature read; dup only fed pairs: an idle pair repeating silence is
  //! not a slip
  wire [LB_QPTRW_C:0] pop_cnt_w = q_cnt_r[pop_pair_w];
  wire pop_act_w = pop_visit_w && q_primed_r[pop_pair_w]
                   && (pop_cnt_w != '0);
  wire pop_dup_w = pop_visit_w && q_primed_r[pop_pair_w]
                   && q_fed_r[pop_pair_w] && (pop_cnt_w == '0);
  wire [LB_QPTRW_C-1:0] pop_rd_w = q_rd_r[pop_pair_w];
  //! queue array addresses (read the pre-advance rd pointer)
  wire [LBPW_C+LB_QPTRW_C-1:0] pop_raddr_w  = {pop_pair_w, pop_rd_w};
  wire [LBPW_C+LB_QPTRW_C-1:0] push_waddr_w = {push_pair_w,
                                               q_wr_r[push_pair_w]};

  //! push-side pointer maths, POST-pop when both touch the same pair the
  //! same cycle (the pop freed a slot, so the push is not full)
  wire push_same_w = push_ram_w && pop_act_w && (push_pair_w == pop_pair_w);
  wire [LB_QPTRW_C:0] push_cnt1_w = q_cnt_r[push_pair_w]
                                    - (LB_QPTRW_C+1)'(push_same_w);
  wire push_drop_w = push_ram_w && (32'(push_cnt1_w) == LB_QDEPTH_C);
  wire [LB_QPTRW_C-1:0] push_rd1_w = q_rd_r[push_pair_w]
                                     + LB_QPTRW_C'(push_same_w);

  //! prime the whole stream at its accepted tlast beat (constant unroll;
  //! the final commits may still be in the skid, but a tick landing inside
  //! that <= 2-beat window pops what has landed - order is unaffected)
  logic [LB_PAIRS_C-1:0] prime_set_w;
  always_comb begin : prime_set_scan
    prime_set_w = '0;
    for (int pp = 0; pp < int'(LB_PAIRS_C); pp++) begin
      if (lb_ok_w && lb_tlast_i && (32'(lb_tuser_i) == pp / int'(LB_PPS_C)))
        prime_set_w[pp] = 1'b1;
    end
  end : prime_set_scan

  //! flush clear mask, pair-granular from the per-stream pulse
  logic [LB_PAIRS_C-1:0] flush_clr_w;
  always_comb begin : flush_clr_scan
    flush_clr_w = '0;
    for (int pp = 0; pp < int'(LB_PAIRS_C); pp++) begin
      for (int s = 0; s < N_LB_STREAMS_P; s++) begin
        if (lb_flush_i[s] && (s == pp / int'(LB_PPS_C)))
          flush_clr_w[pp] = 1'b1;
      end
    end
  end : flush_clr_scan

  //! saturating slip evidence: dups are one per starved fed pair per tick,
  //! skips are drop-oldest (queue full) plus refused commits (skid overflow,
  //! not reachable at wire beat spacing) - up to 3 events in one cycle
  wire [1:0] skip_inc_w = 2'(push_drop_w) + 2'(skid_ovf0_w)
                          + 2'(skid_ovf1_w);
  wire [16:0] skip_sum_w = 17'(lb_skip_cnt_o) + 17'(skip_inc_w);
  wire [16:0] dup_sum_w  = 17'(lb_dup_cnt_o) + 17'(pop_dup_w);

  //! pop data-return pipeline (registered array read = BRAM-shaped)
  logic [47:0]       q_rdata_r;
  logic              pop_ret_v_r;
  logic [LBPW_C-1:0] pop_ret_pair_r;

  always_ff @(posedge clk_i) begin : loop_queue_engine
    if (!rst_n) begin
      for (int pp = 0; pp < int'(LB_PAIRS_C); pp++) begin
        q_wr_r[pp]     <= '0;
        q_rd_r[pp]     <= '0;
        q_cnt_r[pp]    <= '0;
        lb_hold_r[pp]  <= 48'd0;
      end
      q_fed_r        <= '0;
      q_primed_r     <= '0;
      skid_v_r       <= '0;
      skid_wp_r      <= 2'd0;
      skid_rp_r      <= 2'd0;
      skid_cnt_r     <= 3'd0;
      q_rdata_r      <= 48'd0;
      pop_ret_v_r    <= 1'b0;
      pop_ret_pair_r <= '0;
      lb_dup_cnt_o   <= 16'd0;
      lb_skip_cnt_o  <= 16'd0;
    end
    else begin
      //! ---- skid enqueue (up to 2) / drain (1) --------------------------
      if (enq0_v_w) begin
        skid_data_r[skid_wp0_w] <= enq0_data_w;
        skid_addr_r[skid_wp0_w] <= enq0_addr_w;
        skid_strm_r[skid_wp0_w] <= lb_tuser_i;
      end
      if (enq1_v_w) begin
        skid_data_r[skid_wp1_w] <= cm1_data_w;
        skid_addr_r[skid_wp1_w] <= cm1_addr_w;
        skid_strm_r[skid_wp1_w] <= lb_tuser_i;
      end
      skid_wp_r  <= skid_wp_r + 2'(skid_enq_n_w);
      skid_rp_r  <= skid_rp_r + (skid_drain_w ? 2'd1 : 2'd0);
      skid_cnt_r <= skid_cnt_r + 3'(skid_enq_n_w)
                    - (skid_drain_w ? 3'd1 : 3'd0);
      //! validity as ONE vector update: drain clears the OLD head, flush
      //! kills matching survivors, the enqueues set their (possibly just
      //! drained) slots - in that order, so a same-slot re-enqueue lives
      skid_v_r <= ((skid_v_r
                    & ~(skid_drain_w ? (LB_SKID_C)'(1) << skid_rp_r : '0)
                    & ~skid_kill_w)
                   | (enq0_v_w ? (LB_SKID_C)'(1) << skid_wp0_w : '0)
                   | (enq1_v_w ? (LB_SKID_C)'(1) << skid_wp1_w : '0));

      //! ---- queue array ports (one write, one registered read) ----------
      //! the return is refused at ISSUE time for a just-flushed pair; a
      //! flush landing on the RETURN cycle wins by the flush loop below
      //! being the last writer of lb_hold_r
      if (push_ram_w) lb_q_r[LB_QAW_C'(push_waddr_w)] <= push_data_w;
      q_rdata_r      <= lb_q_r[LB_QAW_C'(pop_raddr_w)];
      pop_ret_v_r    <= pop_act_w && !flush_clr_w[pop_pair_w];
      pop_ret_pair_r <= pop_pair_w;

      //! ---- per-pair pointers: pop first, then push (composed wires) ----
      if (pop_act_w) begin
        q_rd_r[pop_pair_w]  <= pop_rd_w + 1'b1;
        q_cnt_r[pop_pair_w] <= pop_cnt_w - 1'b1;
      end
      if (push_ram_w) begin
        q_wr_r[push_pair_w] <= q_wr_r[push_pair_w] + 1'b1;
        if (push_drop_w) q_rd_r[push_pair_w] <= push_rd1_w + 1'b1;
        q_cnt_r[push_pair_w] <= push_drop_w ? push_cnt1_w
                                            : push_cnt1_w + 1'b1;
        q_fed_r[push_pair_w] <= 1'b1;
      end
      q_primed_r <= (q_primed_r | prime_set_w) & ~flush_clr_w;

      //! ---- pop data return into the walk's hold bank -------------------
      if (pop_ret_v_r) lb_hold_r[pop_ret_pair_r] <= q_rdata_r;

      //! ---- slip evidence (saturating) ----------------------------------
      lb_dup_cnt_o  <= dup_sum_w[16]  ? 16'hFFFF : dup_sum_w[15:0];
      lb_skip_cnt_o <= skip_sum_w[16] ? 16'hFFFF : skip_sum_w[15:0];

      //! ---- bind wipe: empty, un-prime, un-feed, silence (LAST = wins,   --
      //! ---- including over a same-cycle pop data return) -----------------
      for (int pp = 0; pp < int'(LB_PAIRS_C); pp++) begin
        if (flush_clr_w[pp]) begin
          q_wr_r[pp]    <= '0;
          q_rd_r[pp]    <= '0;
          q_cnt_r[pp]   <= '0;
          q_fed_r[pp]   <= 1'b0;
          lb_hold_r[pp] <= 48'd0;
        end
      end
    end
  end : loop_queue_engine

  // ---------------------------------------------------------------------- //
  // Source select for the current walk slot (combinational)                 //
  // ---------------------------------------------------------------------- //
  logic [SLOTW_C-1:0] slot_r;            //! walk pointer

  //! the pair step reads BOTH channel entries of the slot and resolves
  //! each independently - "one cluster == one audio channel" (USER 08-06)
  wire [12:0] ent_l_w = map_r[{slot_r, 1'b0}];   //! even channel 2p
  wire [12:0] ent_r_w = map_r[{slot_r, 1'b1}];   //! odd channel 2p+1

  //! per-channel resolver: entry {en, half, src, idxh, idx} -> the 24-bit
  //! sample of ITS mono cluster (the selected half of the source pair).
  //! An entry naming a stream/pair the build does not keep resolves to
  //! silence (the §5 "illegal encoding behaves as disabled" rule); the
  //! TONE bucket carries the same value on both halves by construction.
  function automatic logic [23:0] resolve_ch(input logic [12:0] e);
    logic        en_f;
    logic        half_f;
    logic [2:0]  src_f;
    logic [3:0]  idxh_f, idx_f;
    logic [47:0] pair_f;
    logic        lbok_f;
    begin
      en_f = e[12]; half_f = e[11]; src_f = e[10:8];
      idxh_f = e[7:4]; idx_f = e[3:0];
      lbok_f = (32'(idxh_f) < N_LB_STREAMS_P) && (32'(idx_f) < LB_PPS_C);
      unique case (en_f ? src_f : 3'd0)
        SRC_I2S_C : pair_f = i2s_hold_r;
        SRC_TDM_C : pair_f = (32'(idx_f) < N_TDM_PAIRS_C)
                               ? tdm_hold_r[idx_f[TDMPW_C-1:0]] : 48'd0;
        SRC_RING_C: pair_f = (32'(idx_f) < N_RING_P)
                               ? ring_hold_r[idx_f[RINGPW_C-1:0]] : 48'd0;
        SRC_TONE_C: pair_f = {tone_smp_i, tone_smp_i};
        SRC_LOOP_C: pair_f = lbok_f
                               ? lb_hold_r[LBPW_C'(32'(idxh_f) * LB_PPS_C
                                                   + 32'(idx_f))]
                               : 48'd0;
        default   : pair_f = 48'd0;
      endcase
      resolve_ch = half_f ? pair_f[23:0] : pair_f[47:24];
    end
  endfunction

  //! An UNMAPPED channel resolves to DIGITAL SILENCE rather than dropping
  //! out of the walk (Milan v1.2 5.3.9.1 lets a channel be "not mapped";
  //! 5.3.7.3 still owes the stream its packets). The resolver gates on the
  //! entry's own enable, so the FSM below stays branch-free.
  wire [23:0] out_l_w = resolve_ch(ent_l_w);
  wire [23:0] out_r_w = resolve_ch(ent_r_w);

  // ---------------------------------------------------------------------- //
  // Emit walk FSM (pre-walk pop, then the slot walk)                        //
  // ---------------------------------------------------------------------- //
  logic                       tick_pend_r;   //! one-deep tick queue
  logic [$clog2(GAP_CYC_P+1)-1:0] gap_r;
  wire  last_slot_w = (32'(slot_r) == N_SLOTS_P - 1);

  always_ff @(posedge clk_i) begin : emit_engine
    if (!rst_n) begin
      st_r         <= CM_IDLE_S;
      tick_pend_r  <= 1'b0;
      slot_r       <= '0;
      pop_idx_r    <= '0;
      gap_r        <= '0;
      pair_valid_o <= 1'b0;
      pair_slot_o  <= '0;
      pair_l_o     <= '0;
      pair_r_o     <= '0;
    end
    else begin
      unique case (st_r)
        // -------- wait for the media tick --------------------------------
        CM_IDLE_S : begin
          pair_valid_o <= 1'b0;
          if (tick_pend_r) begin
            tick_pend_r <= 1'b0;           //! a coincident tick re-arms below
            slot_r      <= '0;
            pop_idx_r   <= '0;
            st_r        <= CM_POP_S;
          end
        end

        // -------- LOOP pre-walk: pop one event per fed pair --------------
        //! LB_PAIRS_C + 1 cycles: one pop issue per pair, one final cycle
        //! for the last data return to land in lb_hold_r before the slot
        //! walk reads it. The pop/dup work itself lives in
        //! loop_queue_engine, keyed off pop_visit_w/pop_act_w.
        CM_POP_S : begin
          if (32'(pop_idx_r) == LB_PAIRS_C) st_r <= CM_STEP_S;
          else                              pop_idx_r <= pop_idx_r + 1'b1;
        end

        // -------- inject the current slot --------------------------------
        //! EVERY slot injects, mapped or not (the resolver already turned
        //! unmapped channels into silence). Skipping the unmapped ones is what
        //! made a talker with one unmapped channel stop framing ALTOGETHER:
        //! the packetizer advances nsamp_r per slot it is fed, so a slot that
        //! never pulses stalls that talker's frame forever, and while this
        //! crossbar is armed milan_datapath has muxed KL_pair_zero_fill - the
        //! guard that covers exactly this for the front-end path - out of the
        //! packetizer's input. Milan v1.2 5.3.7.3 gives a bound Stream Output
        //! no way to be silent except by sending silence.
        CM_STEP_S : begin
          pair_valid_o <= 1'b1;
          pair_slot_o  <= 5'(slot_r);
          pair_l_o     <= out_l_w;
          pair_r_o     <= out_r_w;
          gap_r        <= ($clog2(GAP_CYC_P+1))'(GAP_CYC_P);
          st_r         <= CM_GAP_S;
        end

        // -------- settle gap between injects ------------------------------
        CM_GAP_S : begin
          pair_valid_o <= 1'b0;            //! the pulse was one cycle only
          if (gap_r == '0) begin
            if (last_slot_w) st_r <= CM_IDLE_S;
            else begin
              slot_r <= slot_r + 1'b1;
              st_r   <= CM_STEP_S;
            end
          end
          else gap_r <= gap_r - 1'b1;
        end

        default : st_r <= CM_IDLE_S;
      endcase

      //! media-tick capture (after the case: a tick coincident with an
      //! IDLE consume re-arms the one-deep queue instead of being dropped)
      if (tick_i) tick_pend_r <= 1'b1;
    end
  end : emit_engine

endmodule

`default_nettype wire

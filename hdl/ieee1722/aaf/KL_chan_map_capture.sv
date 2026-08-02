/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_chan_map_capture.sv
  Author      : Kebag Logic

  Date        : 2026-07-23
  Description : Per-pair-slot TX source multiplexer (docs/NXN_ARCHITECTURE.md
                §2.1 capture family; the SW-defined end-station channel map).
                Sits between the several pair-stream sources and the shared
                KL_aaf_packetizer's pair-injection interface: for every one of
                the N_SLOTS_P TX pair slots (the prefix-sum slot space; talker
                t owns chans/2 consecutive slots - see the packetizer header)
                a small map RAM selects which audio source feeds that slot.

                8 talker streams x up to 8 channels = up to 32 stereo PAIR
                slots, so the map is 32 entries deep and the emitted
                pair_slot_o is the full 5-bit (0..31) space the packetizer now
                accepts (the pair_slot widening).

                MAP ENTRY (12 bits, one per slot):
                  {idxh[11:8], en[7], src[6:4], idx[3:0]}
                  en  - 1 = this slot is live and injected every media tick;
                        0 = the slot emits nothing (skipped in the walk).
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

                WHY idxh SITS ABOVE THE LEGACY BYTE (deliberate, not tidy):
                bits [7:0] of the entry are bit-for-bit the pre-loopback 8-bit
                entry and arrive on the SAME 8-bit map_wr_data_i pin, so every
                map word ever written - and the CSR slice in milan_datapath
                that produces it (docs/CHANNEL_MAP_64.md §5, capture column) -
                keeps its EXACT meaning and its exact width. idxh arrives on
                its own defaulted pin (map_wr_idxh_i, default 0), so a writer
                that predates the loopback can only ever say "RX stream 0" -
                never a re-interpretation of a live map. §5's capture word
                already reserves CHMAP_WORD[7:4] for exactly this field
                ("source stream/lane"); the datapath dropped it only because
                no source needed it before the loopback, and wiring it in is
                the one-line change that arms this bucket from the CSR.

                SOURCE BUCKETS (wire-truth, free-running): the latest pair per
                source is latched into a hold register the instant its
                pair_valid pulse arrives, so the tick-time walk always injects
                the freshest sample. The tone bucket is the live tone_smp_i
                (both L/R). No CDC lives here - every source has already
                crossed into clk_i.

                LOOP BUCKET (rx -> talker loopback). The board's physical
                capture front-ends are the only other multi-channel sources
                and on the AX7101 there are none (no pmoda -> i2s_sdout tied
                0; the TDM slave pins are tied 0 on every SoC), while the tone
                is by construction the SAME value on L and R. A received AAF
                stream is therefore the only source of real, per-channel
                DISTINCT audio on that board, so this bucket makes any
                (rx stream, channel pair) a talker pair source.

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
                virtual: counted for the interleave, never latched.

                PAIRING, and why L/R cannot cross: a pair p of the entry is
                wire channels {2p, 2p+1} = {L, R} - the same pairing the
                packetizer applies on the way out (pair slot p of a talker
                emits its L into channel 2p and its R into 2p+1), so a pair
                that goes round the loop keeps its channel identity. L and R
                are latched into the two HALVES of one hold word by the
                sample's own channel parity, never by arrival order, so an
                odd-length beat boundary or a mid-frame stall cannot swap
                them.

                SLIP: latest-sample, free-running, no queueing - the RX
                stream and the local media tick are different clocks in
                general (docs/CHANNEL_MAP_64.md §9): a starved loopback pair
                repeats its last value, a fast one drops. Same slip policy as
                every other bucket here.

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
                     swap (17 failures, values perfectly transposed).
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

                EMIT (media sample tick): on tick_i the engine walks the slot
                map low-to-high; each ENABLED slot injects one pair
                (pair_valid_o one-cycle pulse + pair_slot_o + pair_l_o/
                pair_r_o) then idles GAP_CYC_P cycles before the next slot -
                the proven inject cadence the packetizer admits (one pair per
                cycle with a settle gap, mirroring the golden NxN TB's
                pair()). Disabled slots are skipped with no pulse. Six media
                ticks (6 samples/ch) fill one AVTPDU per talker on the shared
                6-sample cadence; a tick arriving mid-walk is queued one deep
                (never dropped).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Per-pair-slot TX source mux (NXN §2.1 capture family): a 32-slot map RAM
//! ({idxh, en, src, idx}) routes each packetizer pair slot to a source bucket
//! (I2S capture / TDM / ALSA ring / tone / RX-stream loopback / silence);
//! free-running source holds, per-tick low-to-high slot walk emitting the
//! packetizer inject cadence (one pulse + GAP_CYC_P settle), disabled slots
//! silent. The loopback bucket de-interleaves the depacketizer payload clone
//! (IEEE 1722-2016 7.3.3/7.3.5) into per-(stream, channel pair) holds, so a
//! received stream's channels can feed a talker. Single clock, no CDC.

`default_nettype none

module KL_chan_map_capture #(
  parameter int unsigned N_SLOTS_P = 32,   //! TX pair slots (prefix-sum space)
  parameter int unsigned N_TDM_P   = 8,    //! TDM slots (pairs = N_TDM_P/2)
  parameter int unsigned N_RING_P  = 16,   //! ALSA ring pair sources (idx 0..15)
  parameter int unsigned GAP_CYC_P = 24,   //! settle cycles between slot injects
  //! LOOP bucket sizing: the RX stream-channel space kept as pair holds
  //! (N_LB_STREAMS_P * N_LB_CH_P/2 x 48 b). Elaborate it down (1 / 2) on a
  //! build that has no listener to loop back from.
  parameter int unsigned N_LB_STREAMS_P = 8, //! RX streams kept (idxh < this)
  parameter int unsigned N_LB_CH_P      = 8  //! wire channels kept per stream
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset

  //! --- map RAM write port (CSR window / TB) ------------------------------
  input  wire         map_wr_en_i,       //! one-cycle write strobe
  input  wire [$clog2(N_SLOTS_P)-1:0] map_wr_addr_i, //! slot index
  input  wire [7:0]   map_wr_data_i,     //! {en[7], src[6:4], idx[3:0]} -
                                         //!  the legacy byte, UNCHANGED
  //! the entry's high nibble, carried on its own pin so the legacy write
  //! port keeps its exact width and meaning; a writer that does not drive it
  //! (default 0) can only ever mean "RX stream 0", never a re-interpretation
  input  wire [3:0]   map_wr_idxh_i = 4'd0, //! LOOP: RX stream index

  //! --- map RAM readback port (registered, 1-cycle latency) ---------------
  input  wire         map_rd_en_i,       //! one-cycle read request
  input  wire [$clog2(N_SLOTS_P)-1:0] map_rd_addr_i,
  //! {loop_fed[15], loop_mapped[14], 2'b0, entry[11:0]}.
  //! [11:0] is the addressed entry {idxh, en, src, idx}. [15:14] is the LOOP
  //! bucket's CAPABILITY MASK, and it rides this existing pin on purpose: a
  //! loopback slot that is mapped but has never been FED emits 24'd0, which
  //! is bit-for-bit what a working-but-quiet slot emits. Without the mask a
  //! board whose listener side is not wired at all - or is wired and simply
  //! receiving nothing - reports a LYING ZERO that no counter contradicts.
  //! That risk is not hypothetical: the AX7101 routes no audio pins in
  //! either direction, so its talkers depend ENTIRELY on this bucket.
  //!   mapped=0            : the bucket is not in use
  //!   mapped=1, fed=0     : mapped and NEVER FED - a silent talker here is
  //!                         a BINDING or stream fault, not quiet audio
  //!   mapped=1, fed=1     : live; zeros in the payload are real silence
  output logic [15:0] map_rd_data_o,     //! (valid with rd_valid)
  output logic        map_rd_valid_o,    //! read data valid this cycle

  //! --- I2S capture pair source (single stereo pair) ----------------------
  input  wire         i2s_pair_valid_i,  //! latch pulse
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,

  //! --- TDM capture pair sources (indexed by pair slot) -------------------
  input  wire         tdm_pair_valid_i,  //! latch pulse
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

  //! --- media sample tick (one walk of the enabled slots per pulse) -------
  input  wire         tick_i,

  //! --- pair injection to the shared packetizer (its capture contract) ----
  output logic        pair_valid_o,      //! one-cycle pulse per L/R pair
  output logic [4:0]  pair_slot_o,       //! pair slot 0..31 (widened space)
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o
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
  //! LOOP bucket: pair holds per stream, then the flat bank and its address
  localparam int unsigned LB_PPS_C     = (N_LB_CH_P < 2) ? 1 : N_LB_CH_P / 2;
  localparam int unsigned LB_PAIRS_C   = N_LB_STREAMS_P * LB_PPS_C;
  localparam int unsigned LBPW_C       = (LB_PAIRS_C <= 1) ? 1
                                                      : $clog2(LB_PAIRS_C);

  //! map entry field encoding (src[6:4])
  localparam logic [2:0] SRC_ZERO_C = 3'd0, SRC_I2S_C = 3'd1, SRC_TDM_C = 3'd2,
                         SRC_RING_C = 3'd3, SRC_TONE_C = 3'd4,
                         SRC_LOOP_C = 3'd5;

  // ---------------------------------------------------------------------- //
  // Map RAM (small config store: flop register file, like KL_pcm_route)     //
  //   one sync write process; combinational reads for the walk; the         //
  //   readback port registers a snapshot (RAM house style read turnaround)  //
  // ---------------------------------------------------------------------- //
  logic [11:0] map_r [N_SLOTS_P];

  always_ff @(posedge clk_i) begin : map_write_port
    if (!rst_n) begin
      for (int s = 0; s < N_SLOTS_P; s++) map_r[s] <= 12'h000;
    end
    else if (map_wr_en_i) begin
      map_r[map_wr_addr_i] <= {map_wr_idxh_i, map_wr_data_i};
    end
  end : map_write_port

  //! --- LOOP capability mask (the R5 "never a lying 0" rail) --------------
  //! mapped: LIVE - any enabled entry selecting the LOOP bucket. Declared by
  //! the map, so it answers "is this board's talker supposed to be carrying
  //! received audio right now?" without looking at a sample.
  logic loop_mapped_w;
  always_comb begin : loop_mapped_scan
    loop_mapped_w = 1'b0;
    for (int s = 0; s < N_SLOTS_P; s++) begin
      if (map_r[s][7] && (map_r[s][6:4] == SRC_LOOP_C)) loop_mapped_w = 1'b1;
    end
  end : loop_mapped_scan

  //! fed: STICKY since reset - at least one loopback payload beat has been
  //! ACCEPTED. Deliberately not "recently": this bit separates "the listener
  //! side is not connected to me at all" (the binding fault) from "it is
  //! connected and the stream is silent or stopped", which the RX monitors'
  //! own live counters already answer.
  logic loop_fed_r;

  always_ff @(posedge clk_i) begin : map_read_port
    if (!rst_n) begin
      map_rd_data_o  <= 16'h0000;
      map_rd_valid_o <= 1'b0;
    end
    else begin
      map_rd_valid_o <= 1'b0;
      if (map_rd_en_i) begin
        map_rd_data_o  <= {loop_fed_r, loop_mapped_w, 2'b00,
                           map_r[map_rd_addr_i]};
        map_rd_valid_o <= 1'b1;
      end
    end
  end : map_read_port

  // ---------------------------------------------------------------------- //
  // Source hold buckets (latch the latest pair per source; wire-truth)      //
  // ---------------------------------------------------------------------- //
  logic [47:0] i2s_hold_r;               //! the single stereo I2S pair
  logic [47:0] tdm_hold_r  [N_TDM_PAIRS_C];
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
  // LOOP bucket: de-interleave the depacketizer payload clone into one       //
  // latest-sample hold per (RX stream, channel pair).                        //
  //                                                                          //
  // This mirrors KL_chan_map_render's sample_latch deliberately - same beat  //
  // format, same wrap-compare position counter, same tlast restart, same     //
  // "virtual channels are walked but never latched" rule - because that is   //
  // the de-interleave that has been proven on the wire. The one difference   //
  // is the store shape: the capture side is PAIR-granular (§4.2), so the     //
  // bank holds 48-bit {L, R} words and a sample lands in the half its own    //
  // channel PARITY picks (even = L = [47:24], odd = R = [23:0], per          //
  // 7.3.5 channel order). Arrival order therefore cannot swap L and R, and   //
  // ONE 48-bit read port serves the walk.                                    //
  // ---------------------------------------------------------------------- //
  logic [47:0] lb_hold_r [LB_PAIRS_C];
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

  always_ff @(posedge clk_i) begin : loopback_latch
    if (!rst_n) begin
      lb_chpos_r <= 4'd0;
      loop_fed_r <= 1'b0;
      for (int p = 0; p < int'(LB_PAIRS_C); p++) lb_hold_r[p] <= 48'd0;
    end
    else begin
      //! the capability rail: ANY accepted beat, even one whose stream index
      //! this build does not keep - the question it answers is whether the
      //! payload clone reaches this module at all
      if (lb_tvalid_i) loop_fed_r <= 1'b1;
      //! smp0 then smp1 = chronological order (7.3.5): on a degenerate
      //! 1-channel stream both land on the same half and the NEWER sample
      //! must win, exactly like the render bank's last-write-wins order.
      if (lb_w0_w) begin
        if (lb_ch0_w[0])
          lb_hold_r[lb_addr(lb_tuser_i, lb_ch0_w)][23:0]  <= lb_smp0_w;
        else
          lb_hold_r[lb_addr(lb_tuser_i, lb_ch0_w)][47:24] <= lb_smp0_w;
      end
      if (lb_w1_w) begin
        if (lb_ch1_w[0])
          lb_hold_r[lb_addr(lb_tuser_i, lb_ch1_w)][23:0]  <= lb_smp1_w;
        else
          lb_hold_r[lb_addr(lb_tuser_i, lb_ch1_w)][47:24] <= lb_smp1_w;
      end
      //! the walk advances on EVERY accepted beat (a beat of an unkept
      //! stream still consumes two payload samples) and restarts at tlast
      if (lb_tvalid_i)
        lb_chpos_r <= lb_tlast_i ? 4'd0 : lb_chwrap(lb_ch1_w, lb_chans_w);
    end
  end : loopback_latch

  // ---------------------------------------------------------------------- //
  // Source select for the current walk slot (combinational)                 //
  // ---------------------------------------------------------------------- //
  logic [SLOTW_C-1:0] slot_r;            //! walk pointer

  wire [11:0] ent_w  = map_r[slot_r];
  wire        en_w   = ent_w[7];
  wire [2:0]  src_w  = ent_w[6:4];
  wire [3:0]  idx_w  = ent_w[3:0];
  wire [3:0]  idxh_w = ent_w[11:8];      //! LOOP only: RX stream index

  //! LOOP read: {stream idxh, channel pair idx} -> one hold word. An entry
  //! naming a stream or pair the build does not keep resolves to silence
  //! (the §5 "illegal encoding behaves as disabled" rule) and its address is
  //! forced to 0 so the bank is never indexed out of range.
  wire lb_sel_ok_w = (32'(idxh_w) < N_LB_STREAMS_P) && (32'(idx_w) < LB_PPS_C);
  wire [LBPW_C-1:0] lb_sel_addr_w =
         lb_sel_ok_w ? LBPW_C'(32'(idxh_w) * LB_PPS_C + 32'(idx_w))
                     : LBPW_C'(0);
  wire [47:0] lb_sel_w = lb_sel_ok_w ? lb_hold_r[lb_sel_addr_w] : 48'd0;

  logic [23:0] sel_l_w, sel_r_w;
  always_comb begin : source_mux
    unique case (src_w)
      SRC_I2S_C : {sel_l_w, sel_r_w} = i2s_hold_r;
      SRC_TDM_C : {sel_l_w, sel_r_w} =
                    (32'(idx_w) < N_TDM_PAIRS_C)
                      ? tdm_hold_r[idx_w[TDMPW_C-1:0]] : 48'd0;
      SRC_RING_C : {sel_l_w, sel_r_w} =
                    (32'(idx_w) < N_RING_P)
                      ? ring_hold_r[idx_w[RINGPW_C-1:0]] : 48'd0;
      SRC_TONE_C : {sel_l_w, sel_r_w} = {tone_smp_i, tone_smp_i};
      //! rx -> talker loopback: L = wire channel 2*idx, R = 2*idx+1 of RX
      //! stream idxh (7.3.5 channel order), latest sample of each
      SRC_LOOP_C : {sel_l_w, sel_r_w} = lb_sel_w;
      default    : {sel_l_w, sel_r_w} = 48'd0;   //! ZERO + reserved = silence
    endcase
  end : source_mux

  // ---------------------------------------------------------------------- //
  // Emit walk FSM                                                           //
  // ---------------------------------------------------------------------- //
  typedef enum logic [1:0] {
    CM_IDLE_S,     //! wait for a media tick
    CM_STEP_S,     //! decide the current slot: skip / emit
    CM_GAP_S       //! settle gap after a pair pulse
  } cstate_t;

  cstate_t                    st_r;
  logic                       tick_pend_r;   //! one-deep tick queue
  logic [$clog2(GAP_CYC_P+1)-1:0] gap_r;
  wire  last_slot_w = (32'(slot_r) == N_SLOTS_P - 1);

  always_ff @(posedge clk_i) begin : emit_engine
    if (!rst_n) begin
      st_r         <= CM_IDLE_S;
      tick_pend_r  <= 1'b0;
      slot_r       <= '0;
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
            st_r        <= CM_STEP_S;
          end
        end

        // -------- decide the current slot --------------------------------
        CM_STEP_S : begin
          if (en_w) begin
            //! inject one pair for this enabled slot (1-cycle pulse next)
            pair_valid_o <= 1'b1;
            pair_slot_o  <= 5'(slot_r);
            pair_l_o     <= sel_l_w;
            pair_r_o     <= sel_r_w;
            gap_r        <= ($clog2(GAP_CYC_P+1))'(GAP_CYC_P);
            st_r         <= CM_GAP_S;
          end
          else begin
            //! disabled slot: emit nothing, advance immediately
            pair_valid_o <= 1'b0;
            if (last_slot_w) st_r <= CM_IDLE_S;
            else             slot_r <= slot_r + 1'b1;
          end
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

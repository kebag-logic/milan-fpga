/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_lat_history_ring.sv
  Description : Per-stage AAF latency HISTORY ring (roadmap item 11, DDR3 arm).

                KL_aaf_latency_taps (PR #17, CSR base 0x870) exposes only the
                LATEST min/last/max inter-stage deltas over CSR - a snapshot.
                This module turns each individual latency sample into a
                fixed-size RECORD and streams it into a wrapping DRAM ring, so
                userspace gets a TIME-SERIES it can post-process (jitter
                histograms, tail latency, per-frame envelopes) rather than one
                instantaneous value.

                The ring-writer CSR ABI is mirrored bit-for-bit from the PCM
                ring (_PCMRingNxN / milan_dma_pcm, LiteX bank 0xf0003120:
                BASE_HI/BASE_LO/LENGTH/ENABLE/LOOP/OFFSET) so the userspace
                mmap+chase recipe (pw-milan-ring-source style: program base +
                length + enable, then chase the OFFSET write pointer and parse
                fixed records) is reused unchanged. See
                docs/LATENCY_HISTORY_RING.md.

                RECORD (RECORD_BYTES_P = 16 bytes, LITTLE-ENDIAN in DRAM):
                  bytes  0..7  : ptp_ns     (uint64) gPTP ns at the sample
                  bytes  8..11 : latency_ns (uint32) measured stage latency
                  byte  12     : stage_id   (uint8)  documented tap point
                  byte  13     : stream_idx (uint8)  AAF stream index
                  bytes 14..15 : flags      (uint16) {gap[15],rsvd[14:12],seq[11:0]}
                where seq is a per-accepted-record rolling counter (userspace
                detects lost/reordered records) and gap = the first record
                after one or more samples were dropped (writer stalled / ring
                full in stop mode) - a self-describing hole marker.

                At DATA_W = 64 a record is two beats: beat 0 = ptp_ns, beat 1 =
                {flags, stream_idx, stage_id, latency_ns} (latency in the low
                32 bits). Each beat is emitted to a simple write-request master
                (wr_valid/wr_data/wr_addr/wr_last/wr_ready) that the existing
                milan_dma DRAM writer carries - the SAME downstream shape as
                the PCM ring's WishboneDMAWriter sink.

                NON-STALLABLE datapath rule (mf52 lesson, KL_pcm_ring_bram):
                the latency-sample producer is a fire-and-forget pulse and is
                NEVER back-pressured. If a sample arrives while the previous
                record is still draining to DRAM (wr_ready low) - or, in
                stop-mode (loop=0), after the ring is full - the sample is
                DROPPED and `dropped_o` bumps; the write master's ready gates
                only the emitter, never the producer.

                INPUT CONTRACT is a FRESH clean per-sample bus (the taps module
                publishes deltas, not a sample stream); a thin adapter maps each
                completed taps inter-stage delta -> one sample here (stage_id =
                the stage index, latency_ns = delta * ns/cycle, stream_idx =
                the AAF stream, ptp_ns = the chain epoch). Documented in
                docs/LATENCY_HISTORY_RING.md.

  Spec refs   : docs/LATENCY_HISTORY_RING.md (record + ABI + read recipe);
                hdl/ieee1722/aaf/KL_pcm_ring_bram.sv (ring pattern);
                _PCMRingNxN / milan_dma_pcm (CSR ABI mirrored)
  House style : mirrors hdl/ieee1722/aaf/KL_pcm_ring_bram.sv.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_lat_history_ring #(
  parameter int unsigned DATA_W         = 64,   //! downstream bus/word width (bits)
  parameter int unsigned RECORD_BYTES_P = 16,   //! bytes per latency record
  parameter int unsigned ADDR_W         = 32    //! byte-address width toward the DRAM writer
) (
  input  wire                   clk_i,          //! datapath clock
  input  wire                   rst_n,          //! sync reset, active low

  //! --- latency sample bus (fire-and-forget; taps adapter feeds it) --------
  input  wire                   sample_valid_i, //! 1-cycle pulse: one completed sample
  input  wire  [31:0]           sample_lat_ns_i,//! measured stage latency (ns or cycles)
  input  wire  [7:0]            sample_stage_i, //! documented tap-point id
  input  wire  [7:0]            sample_stream_i,//! AAF stream index
  input  wire  [63:0]           ptp_ns_i,       //! gPTP ns timestamp at the sample

  //! --- CSR config (mirrors the PCM ring ABI; wired in the migen glue) -----
  input  wire  [63:0]           ring_base_i,    //! BASE_HI:BASE_LO ring base (bytes)
  input  wire  [31:0]           ring_len_i,     //! LENGTH: ring size (bytes, multiple of RECORD_BYTES_P)
  input  wire                   enable_i,       //! ENABLE: 0 = clear wptr + drop
  input  wire                   loop_i,         //! LOOP: 1 = wrap+overwrite, 0 = stop when full
  output wire  [31:0]           wptr_o,         //! OFFSET readback: byte write pointer (userspace chase)
  output wire  [31:0]           dropped_o,      //! dropped-record counter (RO, saturating)

  //! --- downstream write-request master toward the DRAM writer -------------
  output wire                   wr_valid_o,     //! record beat valid
  output wire  [DATA_W-1:0]     wr_data_o,      //! record beat data (LE record words)
  output wire  [ADDR_W-1:0]     wr_addr_o,      //! byte address for this beat (base + off)
  output wire                   wr_last_o,      //! last beat of the current record
  input  wire                   wr_ready_i      //! DRAM writer ready (gates the emitter only)
);

  // ------------------------------------------------------------------ //
  // Geometry                                                            //
  // ------------------------------------------------------------------ //
  localparam int unsigned NB       = DATA_W / 8;                 //! bytes per beat
  localparam int unsigned SHIFT    = $clog2(NB);                 //! byte->beat shift (3 @ 64b)
  localparam int unsigned REC_BITS = RECORD_BYTES_P * 8;         //! record width (bits)
  localparam int unsigned BEATS    = REC_BITS / DATA_W;          //! beats per record (2 @ 64b/16B)
  localparam int unsigned BCW      = (BEATS <= 1) ? 1 : $clog2(BEATS); //! beat-counter width

  // ------------------------------------------------------------------ //
  // Record assembly + emitter state                                     //
  // ------------------------------------------------------------------ //
  logic [REC_BITS-1:0] rec_r;        //! latched record being streamed
  logic [BCW-1:0]      beat_r;       //! beat index within the record
  logic                busy_r;       //! a record is draining to DRAM
  logic [31:0]         wp_r;         //! byte write pointer within the ring
  logic                full_r;       //! stop-mode: ring filled, accept no more
  logic [11:0]         seq_r;        //! per-accepted-record rolling counter
  logic                gap_r;        //! sticky: a drop happened since the last accept
  logic [31:0]         dropped_r;    //! dropped-record counter

  //! record bytes, LSB = lowest DRAM address: ptp_ns at bytes 0..7, then
  //! latency_ns / stage_id / stream_idx / flags. Matches the packed LE struct
  //! userspace reads (see docs/LATENCY_HISTORY_RING.md).
  wire [15:0] flags_w = {gap_r, 3'b000, seq_r};
  wire [REC_BITS-1:0] record_w =
       {flags_w, sample_stream_i, sample_stage_i, sample_lat_ns_i, ptp_ns_i};

  //! room for one more record when writing sequentially (stop-mode gate)
  wire has_room_w  = loop_i | ~full_r;
  //! accept a fresh sample only when enabled, idle, and space is available
  wire accept_w    = sample_valid_i & enable_i & ~busy_r & has_room_w;
  //! any offered sample that is NOT accepted while enabled is a counted drop
  wire drop_w      = sample_valid_i & enable_i & ~accept_w;

  //! last beat of the current record handshakes out this cycle
  wire last_beat_w = busy_r & enable_i & wr_ready_i & (beat_r == BCW'(BEATS-1));

  // ------------------------------------------------------------------ //
  // Emitter: assemble on accept, stream beats, advance the write pointer //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i) begin : emitter
    if (!rst_n) begin
      rec_r     <= '0;
      beat_r    <= '0;
      busy_r    <= 1'b0;
      wp_r      <= 32'd0;
      full_r    <= 1'b0;
      seq_r     <= 12'd0;
      gap_r     <= 1'b0;
      dropped_r <= 32'd0;
    end
    else if (!enable_i) begin
      //! disabled: clear the write pointer + fill state (matches the PCM
      //! ring's disable), abort any in-flight record. Lifetime stats
      //! (seq/dropped) persist until a hard reset.
      beat_r <= '0;
      busy_r <= 1'b0;
      wp_r   <= 32'd0;
      full_r <= 1'b0;
      gap_r  <= 1'b0;
    end
    else begin
      //! -------- accept a new sample (only when idle) --------
      if (accept_w) begin
        rec_r  <= record_w;
        beat_r <= '0;
        busy_r <= 1'b1;
        seq_r  <= seq_r + 12'd1;
        gap_r  <= 1'b0;      //! consumed into this record's flags
      end

      //! -------- drain the current record to DRAM --------
      if (busy_r && wr_ready_i) begin
        if (last_beat_w) begin
          busy_r <= 1'b0;
          //! advance the byte write pointer by one record; wrap to 0 in loop
          //! mode, else advance to the end and latch full (stop mode). The
          //! wrap predicate mirrors _PCMRingNxN's `offset + nb >= length`.
          if (wp_r + 32'(RECORD_BYTES_P) >= ring_len_i) begin
            if (loop_i) begin
              wp_r <= 32'd0;
            end
            else begin
              wp_r   <= wp_r + 32'(RECORD_BYTES_P);  //! -> ring_len (bytes written)
              full_r <= 1'b1;                        //! stop: accept no more
            end
          end
          else begin
            wp_r <= wp_r + 32'(RECORD_BYTES_P);
          end
        end
        else begin
          beat_r <= beat_r + BCW'(1);
        end
      end

      //! -------- drop bookkeeping (never back-pressures the producer) ------
      if (drop_w) begin
        gap_r <= 1'b1;
        if (!(&dropped_r)) dropped_r <= dropped_r + 32'd1;  //! saturating
      end
    end
  end : emitter

  // ------------------------------------------------------------------ //
  // Write-request master outputs                                        //
  // ------------------------------------------------------------------ //
  //! current beat data sliced out of the latched record (LSB beat first)
  wire [DATA_W-1:0] beat_data_w = rec_r[beat_r*DATA_W +: DATA_W];
  //! byte address = ring base + record start (wp_r) + this beat's offset
  wire [31:0]       beat_addr_w = ring_base_i[31:0] + wp_r
                                  + ({29'd0, beat_r} << SHIFT);

  assign wr_valid_o = busy_r & enable_i;
  assign wr_data_o  = beat_data_w;
  assign wr_addr_o  = beat_addr_w[ADDR_W-1:0];
  assign wr_last_o  = busy_r & (beat_r == BCW'(BEATS-1));

  assign wptr_o     = wp_r;
  assign dropped_o  = dropped_r;

endmodule

`default_nettype wire

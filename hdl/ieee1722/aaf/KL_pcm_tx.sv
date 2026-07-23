/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pcm_tx.sv
  Description : Host PCM ring -> AAF pair-stream source: the PLAYBACK (ALSA
                aplay -> AAF talker) counterpart of KL_aaf_rx_depacketizer.
                It is the exact TX inverse of the RX media path, and a drop-in
                replacement for the physical capture front-end
                (KL_aaf_capture_i2s / KL_tdm_capture): it emits the SAME
                {pair_valid, pair_slot, pair_l, pair_r} contract that
                KL_aaf_packetizer consumes, but the samples come from a
                host-written DRAM/BRAM ring rather than an ADC.

                RING ABI (mirrors the RX PCM ring, read direction):
                  ring_base   - byte base of stream 0's sub-ring.
                  ring_len    - per-stream sub-ring length in BYTES (wrap
                                point; MUST be an 8-byte multiple).
                  ring_stride - bytes between adjacent stream sub-ring bases
                                (stream s base = ring_base + s*stride), exactly
                                the _PCMRingNxN layout (RX writer) read back.
                  wr_ptr[s]   - ABSOLUTE monotonic byte count the HOST has
                                filled (per stream; wraps at 2^32). This is the
                                driver-advanced write pointer (one CSR write per
                                buffer refill, mirroring RingDMAReader.wr_ptr).
                  rd_ptr[s]   - ABSOLUTE monotonic byte count CONSUMED (per
                                stream, published so the host knows free space).
                fill[s] = wr_ptr[s] - rd_ptr[s] (unsigned). Empty when < 8.
                The physical fetch address = ring_base + s*stride + rd_off[s],
                where rd_off[s] is the wrapped offset (rd_ptr mod ring_len)
                maintained incrementally. Because ring_len is the wrap period,
                advancing rd_ptr by exactly ring_len (an overrun lap-drop) leaves
                rd_off invariant - so the wrap register never needs a modulo.

                PACING (Milan class A, 6 samples / 125 us): one media sample
                tick emits ONE audio sample for EVERY stream and EVERY channel
                pair (all pair slots), so 6 ticks fill one AVTPDU per stream on
                the shared 6-sample cadence KL_aaf_packetizer expects. The tick
                is either the internal divider (SAMPLE_DIV_C = clk/f_s; the
                aaf_talker_i2s local-clock MVP, the accepted +ppm offset) or an
                external strobe (USE_EXT_TICK_P) driven from the recovered media
                clock / CRF servo so TX matches the network media clock.

                DE-INTERLEAVE (S32BE, wire byte order = the RX ring's bytes):
                each 8-byte ring word is one channel pair {L,R} with the FIRST
                wire byte in lane 0, INT32 left-justified (sample<<8, low byte 0)
                - byte-identical to KL_aaf_packetizer's payload and
                KL_aaf_rx_depacketizer's output, so ring->pkt->wire->depkt->ring
                is byte-exact. The 24-bit sample handed to the packetizer is the
                top three bytes; the packetizer re-appends the zero low byte.
                A C-channel stream stores C/2 words per sample frame (pair p =
                channels {2p, 2p+1}); the walk reads them in payload order so
                pair_slot's channel-pair offset (pown_o) lands structurally.

                UNDERRUN (ring empty at a tick): the pair is STILL emitted so
                the media cadence and channel alignment never skew - the
                substitute is the last sample (repeat, underrun_silence_i=0) or
                digital silence (underrun_silence_i=1). Counted per stream; the
                read pointer is NOT advanced (nothing was consumed).
                OVERRUN (host lapped us: fill > ring_len): the oldest ring lap
                was overwritten; rd_ptr is fast-forwarded one lap (rd_off
                invariant, see above) to resume on the freshest intact ring, and
                the event is counted per stream. Handled only while idle so it
                never contends with the emit walk for the read pointer.

                FETCH PORT: a simple synchronous request/response word port
                (mem_rd_o + mem_addr_o -> mem_data_i + mem_valid_i, any latency)
                - the on-chip BRAM ring reads it in one cycle; a DRAM ring wraps
                it in a tiny Wishbone/AXI read shim. Control/status are flat
                ports for the migen CSR glue (see docs / the integration diff).

  Spec refs   : IEEE 1722-2016 clause 7 (AAF-PCM); docs/NXN_ARCHITECTURE.md
                §1.3 (per-stream PCM ring); ARCHITECTURE_HW_SW_SPLIT (DMA PCM
                ring); the RX mirror KL_aaf_rx_depacketizer.sv + _PCMRingNxN.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_pcm_tx #(
  parameter int unsigned N_STREAMS_P   = 1,      //! talker streams (NxN)
  parameter int unsigned CHANS_P       = 2,      //! channels/stream (even 2..8)
  parameter int unsigned SAMPLE_DIV_C  = 2048,   //! clk cycles per sample tick
                                                 //! (clk/f_s; 100 MHz/48.8 kHz)
  parameter bit          USE_EXT_TICK_P = 1'b0   //! 1 = pace on smp_tick_i
) (
  input  wire        clk_i,           //! datapath clock
  input  wire        rst_n,           //! active-low synchronous reset

  //! --- global + per-stream enable / policy -------------------------------
  input  wire        enable_i,             //! master play enable
  input  wire [N_STREAMS_P-1:0] stream_en_i,//! per-stream play gate
  input  wire        underrun_silence_i,   //! 0 = repeat last, 1 = silence

  //! --- ring configuration (CSR; mirrors the RX PCM ring, read dir) -------
  input  wire [63:0] ring_base_i,          //! stream-0 sub-ring byte base
  input  wire [31:0] ring_len_i,           //! per-stream sub-ring bytes (mult 8)
  input  wire [31:0] ring_stride_i,        //! bytes between stream sub-ring bases

  //! --- per-stream host write pointers (ABSOLUTE byte counts, packed) -----
  input  wire [N_STREAMS_P*32-1:0] wr_ptr_i,

  //! --- media-clock pace (external option) --------------------------------
  input  wire        smp_tick_i,           //! 1-cyc sample strobe (USE_EXT_TICK_P)

  //! --- word fetch port (BRAM one-cycle read / DRAM read shim) ------------
  output logic [31:0] mem_addr_o,          //! byte address of the wanted word
  output logic        mem_rd_o,            //! read request (1-cycle strobe)
  input  wire [63:0]  mem_data_i,          //! returned ring word (wire byte order)
  input  wire         mem_valid_i,         //! read data valid strobe

  //! --- AAF pair stream out (the KL_aaf_packetizer capture contract) ------
  output logic        pair_valid_o,        //! one-cycle pulse per L/R pair
  output logic [3:0]  pair_slot_o,         //! pair slot = t*(C/2) + chpair
  output logic [23:0] pair_l_o,            //! left  sample (top 24 bits, MSB..)
  output logic [23:0] pair_r_o,            //! right sample

  //! --- status (CSR readback) ---------------------------------------------
  output logic [N_STREAMS_P*32-1:0] rd_ptr_o,   //! per-stream consumed bytes
  output logic [N_STREAMS_P*16-1:0] underrun_o, //! per-stream underrun count
  output logic [N_STREAMS_P*16-1:0] overrun_o,  //! per-stream overrun count
  output logic        smp_tick_o,          //! media sample tick (observability)
  output logic        playing_o            //! engine walking a sample tick
);

  // ---------------------------------------------------------------------- //
  // Derived sizing                                                          //
  // ---------------------------------------------------------------------- //
  localparam int unsigned PAIRS_C = (CHANS_P < 2) ? 1 : CHANS_P / 2;
  localparam int unsigned SLOTS_C = N_STREAMS_P * PAIRS_C;   //! <= 16 (pair_slot 4b)
  localparam int unsigned TW_C = (N_STREAMS_P <= 1) ? 1 : $clog2(N_STREAMS_P);
  localparam int unsigned PW_C = (PAIRS_C     <= 1) ? 1 : $clog2(PAIRS_C);
  localparam int unsigned DIVW_C = (SAMPLE_DIV_C <= 1) ? 1 : $clog2(SAMPLE_DIV_C);

  // ---------------------------------------------------------------------- //
  // Media-clock pace: internal divider or external strobe                   //
  // ---------------------------------------------------------------------- //
  logic [DIVW_C-1:0] pace_r;
  logic              tick_r;

  always_ff @(posedge clk_i) begin : pace_div
    if (!rst_n) begin
      pace_r <= '0;
      tick_r <= 1'b0;
    end
    else if (USE_EXT_TICK_P) begin
      pace_r <= '0;
      tick_r <= 1'b0;
    end
    else if (pace_r == DIVW_C'(SAMPLE_DIV_C - 1)) begin
      pace_r <= '0;
      tick_r <= 1'b1;
    end
    else begin
      pace_r <= pace_r + 1'b1;
      tick_r <= 1'b0;
    end
  end : pace_div

  wire tick_w = USE_EXT_TICK_P ? smp_tick_i : tick_r;
  assign smp_tick_o = tick_w;

  // ---------------------------------------------------------------------- //
  // Per-stream ring state                                                   //
  // ---------------------------------------------------------------------- //
  logic [31:0] rd_ptr_r [N_STREAMS_P];   //! absolute consumed byte count
  logic [31:0] rd_off_r [N_STREAMS_P];   //! wrapped offset (rd_ptr mod ring_len)
  logic [15:0] under_r  [N_STREAMS_P];   //! underrun count
  logic [15:0] over_r   [N_STREAMS_P];   //! overrun count
  logic [47:0] hold_r   [SLOTS_C];       //! last {L,R} per slot (repeat policy)

  //! current stream fill (bytes the host queued ahead of us)
  function automatic [31:0] fill_f(input [31:0] wr, input [31:0] rd);
    fill_f = wr - rd;                    //! unsigned modular subtract
  endfunction

  // ---------------------------------------------------------------------- //
  // Emit walk FSM                                                           //
  // ---------------------------------------------------------------------- //
  typedef enum logic [1:0] {
    PT_IDLE_S,     //! wait for the sample tick; run the overrun scan
    PT_STEP_S,     //! decide the current slot: skip / underrun / read
    PT_READ_S      //! wait the fetched word, then emit + advance
  } pstate_t;

  pstate_t         st_r;
  logic [TW_C-1:0] cur_t_r;              //! stream being emitted
  logic [PW_C-1:0] cur_p_r;              //! channel-pair within the stream

  wire [TW_C-1:0] tmax_w = TW_C'(N_STREAMS_P - 1);
  wire [PW_C-1:0] pmax_w = PW_C'(PAIRS_C - 1);
  wire last_pair_w = (cur_p_r == pmax_w);
  wire last_slot_w = last_pair_w && (cur_t_r == tmax_w);

  //! absolute pair slot the packetizer sees (t owns [t*C/2, (t+1)*C/2))
  wire [3:0] slot_w = 4'(32'(cur_t_r) * PAIRS_C + 32'(cur_p_r));

  //! live fill / availability for the current stream
  wire [31:0] cur_wr_w  = wr_ptr_i[cur_t_r*32 +: 32];
  wire [31:0] cur_fill_w = fill_f(cur_wr_w, rd_ptr_r[cur_t_r]);
  wire        cur_en_w   = enable_i && stream_en_i[cur_t_r];
  wire        cur_avail_w = cur_en_w && (cur_fill_w >= 32'd8);

  //! fetch address for the current stream's next word
  wire [31:0] cur_addr_w = ring_base_i[31:0] +
                           32'(cur_t_r) * ring_stride_i +
                           rd_off_r[cur_t_r];

  //! de-interleave the fetched S32BE word: byte 0 (L MSB) sits in lane 0
  wire [23:0] deint_l_w = {mem_data_i[7:0],   mem_data_i[15:8],  mem_data_i[23:16]};
  wire [23:0] deint_r_w = {mem_data_i[39:32], mem_data_i[47:40], mem_data_i[55:48]};

  assign mem_rd_o   = (st_r == PT_STEP_S) && cur_avail_w;
  assign mem_addr_o = cur_addr_w;
  assign playing_o  = (st_r != PT_IDLE_S);

  //! next wrapped offset after consuming one 8-byte word
  wire [31:0] noff_w = ((rd_off_r[cur_t_r] + 32'd8) >= ring_len_i)
                       ? (rd_off_r[cur_t_r] + 32'd8 - ring_len_i)
                       : (rd_off_r[cur_t_r] + 32'd8);

  always_ff @(posedge clk_i) begin : emit_engine
    if (!rst_n) begin
      st_r         <= PT_IDLE_S;
      cur_t_r      <= '0;
      cur_p_r      <= '0;
      pair_valid_o <= 1'b0;
      pair_slot_o  <= '0;
      pair_l_o     <= '0;
      pair_r_o     <= '0;
      for (int s = 0; s < N_STREAMS_P; s++) begin
        rd_ptr_r[s] <= '0;
        rd_off_r[s] <= '0;
        under_r[s]  <= '0;
        over_r[s]   <= '0;
      end
      for (int k = 0; k < int'(SLOTS_C); k++) hold_r[k] <= '0;
    end
    else begin
      pair_valid_o <= 1'b0;              //! default: no pair this cycle

      unique case (st_r)
        // -------- wait for the media tick; scan for overrun --------------
        PT_IDLE_S : begin
          //! overrun lap-drop (idle only: no contention on rd_ptr): the host
          //! lapped us, so the oldest ring is gone - skip forward one lap and
          //! resume on the freshest intact ring (rd_off invariant under +len).
          for (int s = 0; s < N_STREAMS_P; s++) begin
            if (enable_i && stream_en_i[s] &&
                (fill_f(wr_ptr_i[s*32 +: 32], rd_ptr_r[s]) > ring_len_i)) begin
              rd_ptr_r[s] <= rd_ptr_r[s] + ring_len_i;
              over_r[s]   <= over_r[s] + 16'd1;
            end
          end
          if (tick_w && enable_i) begin
            cur_t_r <= '0;
            cur_p_r <= '0;
            st_r    <= PT_STEP_S;
          end
        end

        // -------- decide the current slot --------------------------------
        PT_STEP_S : begin
          if (!cur_en_w) begin
            //! disabled stream: emit nothing, leave its ring untouched
            if (last_slot_w) st_r <= PT_IDLE_S;
            else if (last_pair_w) begin cur_t_r <= cur_t_r + 1'b1; cur_p_r <= '0; end
            else                  cur_p_r <= cur_p_r + 1'b1;
          end
          else if (cur_avail_w) begin
            //! data present: the read is in flight (mem_rd_o asserted this
            //! cycle) - wait for the word, then emit + advance in PT_READ
            st_r <= PT_READ_S;
          end
          else begin
            //! underrun: emit the substitute pair (cadence must not skew),
            //! count it, do NOT advance the ring
            pair_valid_o <= 1'b1;
            pair_slot_o  <= slot_w;
            pair_l_o     <= underrun_silence_i ? 24'd0 : hold_r[slot_w][47:24];
            pair_r_o     <= underrun_silence_i ? 24'd0 : hold_r[slot_w][23:0];
            under_r[cur_t_r] <= under_r[cur_t_r] + 16'd1;
            if (last_slot_w) st_r <= PT_IDLE_S;
            else if (last_pair_w) begin cur_t_r <= cur_t_r + 1'b1; cur_p_r <= '0; end
            else                  cur_p_r <= cur_p_r + 1'b1;
          end
        end

        // -------- fetched word arrives: emit + advance -------------------
        PT_READ_S : begin
          if (mem_valid_i) begin
            pair_valid_o <= 1'b1;
            pair_slot_o  <= slot_w;
            pair_l_o     <= deint_l_w;
            pair_r_o     <= deint_r_w;
            hold_r[slot_w] <= {deint_l_w, deint_r_w};
            //! consume one word
            rd_ptr_r[cur_t_r] <= rd_ptr_r[cur_t_r] + 32'd8;
            rd_off_r[cur_t_r] <= noff_w;
            if (last_slot_w) st_r <= PT_IDLE_S;
            else begin
              st_r <= PT_STEP_S;
              if (last_pair_w) begin cur_t_r <= cur_t_r + 1'b1; cur_p_r <= '0; end
              else                  cur_p_r <= cur_p_r + 1'b1;
            end
          end
        end

        default : st_r <= PT_IDLE_S;
      endcase

      //! master disable aborts any walk in progress (pointers preserved)
      if (!enable_i) begin
        st_r         <= PT_IDLE_S;
        pair_valid_o <= 1'b0;
      end
    end
  end : emit_engine

  // ---------------------------------------------------------------------- //
  // Pack per-stream status to the flat CSR ports                            //
  // ---------------------------------------------------------------------- //
  always_comb begin : status_pack
    for (int s = 0; s < N_STREAMS_P; s++) begin
      rd_ptr_o  [s*32 +: 32] = rd_ptr_r[s];
      underrun_o[s*16 +: 16] = under_r[s];
      overrun_o [s*16 +: 16] = over_r[s];
    end
  end : status_pack

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_chan_map_render.sv
  Author      : Kebag Logic

  Date        : 2026-07-23
  Description : 64 stream-channel -> physical render crossbar (NxN render
                stage). Consumes a clone of the shared AAF RX depacketizer
                payload stream (KL_aaf_rx_depacketizer m_axis: 64-bit beats
                = 2 consecutive S32BE samples of the wire-interleaved
                payload, tuser = stream index, one AXIS frame per PDU, full
                8-byte beats) and maintains a latest-sample wire-truth
                latch cur_r[s][c] of the top 24 bits of every
                (stream, wire channel) sample - free-running, no media
                queueing (the physical outputs run on their own 48 kHz
                tick; slips follow the house free-run rule).

                CLONE QUALIFIER: the tap never backpressures (no tready
                here), so s_tvalid_i must be the ACCEPTED-beat strobe of
                the tapped link (tvalid && tready), the same discipline as
                the depacketizer's own tap side and the KL_pcm_route
                render-tap consumers.

                De-interleave: payload sample k belongs to wire channel
                k % chans[s] (channel-interleaved wire order, 6 samples/ch
                per Milan 48k PDU); chans[s] comes from the RX monitors'
                wire_chans_o (flat 4-bit fields, 0 treated as 2 - same
                pre-first-accept rule as KL_i2s_playback). The position
                counter advances incrementally (wrap compare, no modulo
                hardware) and restarts at every frame's tlast, so
                back-to-back PDUs of different streams / channel counts
                stay aligned. Wire channels beyond N_CH_P are virtual:
                counted for the interleave, never latched.

                PLAYBACK SOURCE (item-7): the host PCM ring is the OTHER
                thing a physical output can carry, so KL_pcm_tx's pair bus
                ({pair_valid, pair_slot, L, R} - the same contract the
                packetizer consumes) feeds a second latest-sample latch
                pbcur_r, indexed by the LINEAR playback channel
                pbch = 2*pair_slot + (0 L / 1 R). It is the exact mirror of
                the AVB latch: free-running, latest-sample, no queueing -
                the render tick decides when it is observed. Without it the
                only route from the ALSA playback ring to the line-out was
                "packetize onto the wire and receive your own stream back".

                Render: a map RAM (one write port, entry format
                {en[7], src[6], idx[5:0]}) routes ANY source channel to any
                of the N_PHYS_P physical output channels (default 10:
                I2S-out L/R = phys 0/1, TDM8-out lane0 slots 0..7 = phys
                2..9). src selects which latch idx indexes:
                  src = 0  AVB listener: idx = {stream[5:3], ch[2:0]} - the
                           original field split, so every map word written
                           before this existed (AEM projector and CSR alike
                           emit bit 6 = 0) means EXACTLY what it did.
                  src = 1  host playback ring: idx[5:0] = the linear
                           playback channel pbch above.
                On every tick_i (one pulse per 48 kHz output media frame)
                the whole phys vector is registered in one shot and
                phys_valid_o pulses - map writes between ticks are never
                visible on the outputs (glitch-free at frame rate).
                Unmapped (en = 0) and out-of-range phys channels render
                24'd0.

                Ownership of the write port (AEM audio-map engine or CSR)
                is upstream and out of scope - the port is only exposed.
                Single clock domain; tick_i arrives already synchronized.

  Company     : Kebag Logic
  Project     : Milan AVTP

  Notes       :
    - Map stream/ch fields are 3 bits: the format caps N_STREAMS_P and
      N_CH_P at 8 (the 8x8 = 64 stream-channel shape). Smaller builds are
      guarded (out-of-range entries render 0); larger need a wider entry.
    - The playback idx is the FULL 6 bits, so N_PB_SLOTS_P <= 32 pair
      slots (64 playback channels) fit the same entry width.
------------------------------------------------------------------------------
*/

//! 64 stream-channel -> physical render crossbar: latches the top 24 bits
//! of every (stream, wire channel) sample from the depacketizer payload
//! clone AND of every host-playback pair (KL_pcm_tx) - both latest-sample
//! wire-truth and free-running - then on each 48 kHz tick renders N_PHYS_P
//! outputs through a map RAM ({en[7], src[6], idx[5:0]}; src 0 = AVB
//! {stream,ch}, 1 = linear playback channel; unmapped = 0) - registered in
//! one shot, so map writes are only ever visible at tick boundaries.

`default_nettype none

module KL_chan_map_render #(
  parameter int unsigned N_STREAMS_P = 8,   //! RX streams (map field: <= 8)
  parameter int unsigned N_CH_P      = 8,   //! wire channels kept per stream
                                            //! (map field: <= 8)
  parameter int unsigned N_PHYS_P    = 10,  //! physical output channels
                                            //! (default: I2S L/R = 0/1,
                                            //! TDM8 lane0 slots = 2..9)
  parameter int unsigned N_PB_SLOTS_P = 8   //! host-playback pair slots kept
                                            //! (2 channels each; <= 32)
)(
  input  wire                        clk_i,         //! Global clock
  input  wire                        rst_n,         //! Active-low synchronous
                                                    //! reset

  //! --- depacketizer payload AXIS clone (never backpressured; drive
  //! --- s_tvalid_i with the tapped link's ACCEPTED beats) -----------------
  input  wire [63:0]                 s_tdata_i,     //! 2 consecutive S32BE
                                                    //! samples, wire order
  input  wire                        s_tvalid_i,
  input  wire                        s_tlast_i,     //! one AXIS frame per PDU
  input  wire [3:0]                  s_tuser_i,     //! stream index s

  //! --- per-stream wire channel count (RX monitors' wire_chans_o) ---------
  input  wire [N_STREAMS_P*4-1:0]    wire_chans_i,  //! 4-bit fields; 0 -> 2

  //! --- host playback pair bus (KL_pcm_tx; src = 1 map entries) -----------
  input  wire                        pb_valid_i,    //! one pulse per L/R pair
  input  wire [3:0]                  pb_slot_i,     //! pair slot t*(C/2)+chpair
  input  wire [23:0]                 pb_l_i,        //! left  sample (top 24)
  input  wire [23:0]                 pb_r_i,        //! right sample

  //! --- output media frame tick (one pulse per 48 kHz frame) --------------
  input  wire                        tick_i,

  //! --- map RAM write port (AEM audio-map engine / CSR upstream) ----------
  input  wire                        map_wr_en_i,   //! one-cycle write strobe
  input  wire [$clog2(N_PHYS_P)-1:0] map_wr_addr_i, //! phys channel p
  input  wire [7:0]                  map_wr_data_i, //! {en[7], src[6],
                                                    //!  idx[5:0]}

  //! --- map readback (combinational) --------------------------------------
  input  wire [$clog2(N_PHYS_P)-1:0] map_rd_addr_i,
  output logic [7:0]                 map_rd_data_o,

  //! --- rendered physical channels (registered at tick_i) -----------------
  output logic [N_PHYS_P*24-1:0]     phys_smp_o,    //! phys p = [p*24 +: 24]
  output logic                       phys_valid_o,  //! one-cycle pulse
  output logic [N_PHYS_P-1:0]        mapped_mask_o, //! live en bits (comb)
  output logic [N_PHYS_P-1:0]        pb_mask_o      //! live en & src=PB (comb)
);

  //! map entry field positions ({en, src, idx[5:0]}; src 0 splits idx into
  //! {stream[2:0], ch[2:0]})
  localparam int unsigned MAP_EN_B_C  = 7;
  localparam int unsigned MAP_SRC_B_C = 6;

  //! linear playback channels kept (2 per pair slot)
  localparam int unsigned PB_CH_C = 2 * N_PB_SLOTS_P;

  // ------------------------------------------------------------------ //
  // Map RAM: N_PHYS_P x 8, one write port + combinational readback      //
  // ------------------------------------------------------------------ //
  logic [7:0] map_r [N_PHYS_P];

  always_ff @(posedge clk_i) begin : map_write
    if (!rst_n) begin
      for (int p = 0; p < N_PHYS_P; p++) map_r[p] <= 8'h00;
    end
    else if (map_wr_en_i && (32'(map_wr_addr_i) < N_PHYS_P)) begin
      map_r[map_wr_addr_i] <= map_wr_data_i;
    end
  end : map_write

  always_comb begin : map_read
    map_rd_data_o = 8'h00;
    for (int p = 0; p < N_PHYS_P; p++) begin
      if (32'(map_rd_addr_i) == p) map_rd_data_o = map_r[p];
      mapped_mask_o[p] = map_r[p][MAP_EN_B_C];
      pb_mask_o[p]     = map_r[p][MAP_EN_B_C] && map_r[p][MAP_SRC_B_C];
    end
  end : map_read

  // ------------------------------------------------------------------ //
  // De-interleave walker: wire channel of each payload sample.          //
  // 2 samples per beat; the counter wraps at the stream's channel count //
  // and restarts at tlast (frames are atomic - tuser is frame-stable).  //
  // ------------------------------------------------------------------ //
  logic [3:0] chpos_r;     //! wire channel of the current beat's FIRST sample

  //! channel count of the in-flight stream (constant-base mux, guarded
  //! against tuser >= N_STREAMS_P; 0 treated as 2 - pre-first-accept rule)
  logic [3:0] chans_raw_w;
  always_comb begin : chans_lookup
    chans_raw_w = 4'd0;
    for (int s = 0; s < N_STREAMS_P; s++) begin
      if (32'(s_tuser_i) == s) chans_raw_w = wire_chans_i[s*4 +: 4];
    end
  end : chans_lookup
  wire [3:0] eff_chans_w = (chans_raw_w == 4'd0) ? 4'd2 : chans_raw_w;

  //! increment-with-wrap (ch is always < chans, so +1 never overflows past
  //! the compare)
  function automatic [3:0] chwrap(input [3:0] ch, input [3:0] chans);
    chwrap = ((4'(ch + 4'd1)) == chans) ? 4'd0 : 4'(ch + 4'd1);
  endfunction

  //! the two S32BE samples of the beat: wire byte first = MSB, byte lane j
  //! = wire byte j (depacketizer out_assemble); top 24 bits keep the
  //! 24-in-32 left-justified audio, the pad byte (lanes 3/7) is dropped
  wire [23:0] smp0_w = {s_tdata_i[7:0],   s_tdata_i[15:8],  s_tdata_i[23:16]};
  wire [23:0] smp1_w = {s_tdata_i[39:32], s_tdata_i[47:40], s_tdata_i[55:48]};
  wire [3:0]  ch0_w  = chpos_r;
  wire [3:0]  ch1_w  = chwrap(ch0_w, eff_chans_w);

  // ------------------------------------------------------------------ //
  // Latest-sample wire-truth latch: cur_r[s][c] free-runs on the clone  //
  // ------------------------------------------------------------------ //
  logic [23:0] cur_r [N_STREAMS_P][N_CH_P];

  always_ff @(posedge clk_i) begin : sample_latch
    if (!rst_n) begin
      chpos_r <= '0;
      for (int s = 0; s < N_STREAMS_P; s++) begin
        for (int c = 0; c < N_CH_P; c++) cur_r[s][c] <= 24'd0;
      end
    end
    else if (s_tvalid_i) begin
      if (32'(s_tuser_i) < N_STREAMS_P) begin
        //! wire channels beyond N_CH_P are virtual: walked, never latched
        if (32'(ch0_w) < N_CH_P) cur_r[s_tuser_i[2:0]][ch0_w[2:0]] <= smp0_w;
        if (32'(ch1_w) < N_CH_P) cur_r[s_tuser_i[2:0]][ch1_w[2:0]] <= smp1_w;
      end
      chpos_r <= s_tlast_i ? 4'd0 : chwrap(ch1_w, eff_chans_w);
    end
  end : sample_latch

  // ------------------------------------------------------------------ //
  // Host playback latch: the SAME latest-sample discipline over          //
  // KL_pcm_tx's pair bus. pbch = 2*pair_slot + (0 L / 1 R), so a         //
  // C-channel talker stream t occupies pbch [t*C, (t+1)*C) exactly as    //
  // its pair slots do - the map's linear idx needs no divider.           //
  // ------------------------------------------------------------------ //
  logic [23:0] pbcur_r [PB_CH_C];

  wire        pb_in_range_w = (32'(pb_slot_i) < N_PB_SLOTS_P);
  wire [5:0]  pb_lch_w      = 6'(32'(pb_slot_i) * 2);

  always_ff @(posedge clk_i) begin : pb_latch
    if (!rst_n) begin
      for (int k = 0; k < int'(PB_CH_C); k++) pbcur_r[k] <= 24'd0;
    end
    else if (pb_valid_i && pb_in_range_w) begin
      pbcur_r[pb_lch_w]              <= pb_l_i;
      pbcur_r[6'(pb_lch_w + 6'd1)]   <= pb_r_i;
    end
  end : pb_latch

  // ------------------------------------------------------------------ //
  // Render: the whole phys vector registers in one shot on tick_i, so   //
  // map writes between ticks are never visible (glitch-free at 48 kHz)  //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i) begin : render_tick
    if (!rst_n) begin
      phys_smp_o   <= '0;
      phys_valid_o <= 1'b0;
    end
    else begin
      phys_valid_o <= tick_i;
      if (tick_i) begin
        for (int p = 0; p < N_PHYS_P; p++) begin
          logic [7:0] m;
          m = map_r[p];
          if (!m[MAP_EN_B_C])
            phys_smp_o[p*24 +: 24] <= 24'd0;
          else if (m[MAP_SRC_B_C])
            //! host playback ring: idx is the LINEAR playback channel
            phys_smp_o[p*24 +: 24] <= (32'(m[5:0]) < int'(PB_CH_C))
                                      ? pbcur_r[m[5:0]] : 24'd0;
          else
            //! AVB listener: idx splits into {stream[5:3], ch[2:0]}
            phys_smp_o[p*24 +: 24] <=
              ((32'(m[5:3]) < N_STREAMS_P) && (32'(m[2:0]) < N_CH_P))
                ? cur_r[m[5:3]][m[2:0]] : 24'd0;
        end
      end
    end
  end : render_tick

endmodule

`default_nettype wire

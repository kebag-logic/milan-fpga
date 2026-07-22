/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_i2s_playback.sv
  Author      : Kebag Logic

  Date        : 2026-07-18 (clean-clock rework; original 2026-07-17)
  Description : Zero-CPU I2S playback of the received AAF stream on the Pmod
                I2S2 DAC (CS4344), CLEAN-CLOCK edition.

                History: the first NCO design derived MCLK from a fractional
                accumulator - true 48 kHz average but +-1 sys-cycle edge
                jitter (~10 ns at 12.2 MHz, alternating 4/5-cycle periods).
                The CS4344's delta-sigma core tolerates ~ps of MCLK jitter:
                measured analog THD+N collapsed to -4.5 dB (H3 -7.7 dBc)
                at ANY level. Fix: the serializer now lives in a dedicated
                MMCM audio clock domain (clk_audio_i = 24.576 MHz nominal,
                +-ppm): MCLK/SCLK/LRCK are plain registered dividers
                (/2 /8 /512) = jitter-free; samples cross via a gray-pointer
                dual-clock FIFO (cdc_pair_fifo).

                Rate matching: the audio domain free-runs at the MMCM's ppm
                offset vs the talker's 48 kHz (USER rule: internal media
                clock = free-run, slips accepted). Underrun repeats the
                last pair, overrun drops - both counted. The NCO trim servo
                is retired (trim_o reads 0); exact stream-clock recovery
                for CLOCK_SOURCE=stream returns as MMCM-DRP discipline
                later. converged_o keeps its fill-window semantics on the
                producer-side FIFO.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! I2S DAC serializer, clean-clocked: PCM tap (wire-order S32BE interleave,
//! re-strided from the live channel count) -> pair FIFO (clk_i) ->
//! cdc_pair_fifo -> audio-domain Philips I2S at 64 fs from plain dividers.

`default_nettype none

module KL_i2s_playback #(
  parameter int MCLK_DIV_LOG2 = 2,      //! legacy param (kept for the
                                        //! instantiation interface; the
                                        //! clean-clock path does not use it)
  parameter int CLK_FREQ_HZ   = 50_000_000, //! clk_i frequency (kept: the
                                        //! per-ms servo tick derives from it)
  parameter int FIFO_LOG2     = 9,      //! sample-pair FIFO depth (2^N)
  parameter int PREFILL_C     = 0       //! underrun-recenter release level
                                        //! in pairs (0 = FIFO midpoint)
)(
  input  wire         clk_i,            //! datapath clock (PCM tap domain)
  input  wire         rst_n,            //! active-low sync reset (clk_i)
  input  wire         clk_audio_i,      //! CLEAN audio clock (MMCM, 24.576 MHz
                                        //! nominal; MCLK = /2, fs = /512)
  input  wire         servo_en_i,       //! USER rule hook: exact recovery only
                                        //! for bound-stream clock sources.
                                        //! No NCO actuator remains - kept for
                                        //! the future MMCM-DRP servo; the
                                        //! convergence observer still runs.

  //! --- PCM tap (depacketizer m_axis, observed transfers) -----------------
  input  wire [63:0]  pcm_tdata_i,
  input  wire         pcm_tvalid_i,
  input  wire         pcm_tready_i,
  input  wire         pcm_tlast_i,
  //! serial-MAC LPF render source (KL_pcm_lpf): filtered pairs on their
  //! own valid; active selects them over the raw AXIS tap
  input  wire [63:0]  lpf_tdata_i,
  input  wire         lpf_tvalid_i,
  input  wire         lpf_active_i,
  input  wire [7:0]   wire_chans_i,      //! WIRE-truth channels/frame from
                                         //! KL_avtp_rx_monitor (last accepted
                                         //! PDU; 0 until first accept -> 2).
                                         //! USER 1-to-1 rule: the physical
                                         //! 2ch render maps stream ch0/ch1,
                                         //! extra channels are virtual
                                         //! (skipped), mono renders L + R=0

  //! --- I2S DAC (Pmod I2S2 line-out) --------------------------------------
  output logic        i2s_mclk_o,
  output logic        i2s_sclk_o,
  output logic        i2s_lrck_o,
  output logic        i2s_sdin_o,        //! serial data to the CS4344

  //! --- observability (CSR I2SPB_STAT / I2SPB_TRIM) ------------------------
  input  wire         clr_under_i,       //! 1-cycle (clk_i): W1C restart of the
                                         //! underrun rail (I2SPB_STAT[31:16]
                                         //! write; crosses to audio via
                                         //! cdc_pulse)
  input  wire         clr_over_i,        //! 1-cycle (clk_i): W1C restart of the
                                         //! overrun rail (I2SPB_STAT[15:0])
  output logic [15:0] underruns_o,       //! audio frames padded (CDC empty)
  output logic [15:0] overruns_o,        //! sample pairs dropped (FIFO full)
  output logic signed [15:0] trim_o,     //! retired NCO trim - always 0
  output logic [15:0] fill_o,            //! producer FIFO fill (sample pairs)
  output logic        media_reset_p_o,   //! rail event = media-clock reset
  output logic        converged_o,       //! fill in MID±64 sustained 100 ms
                                         //! (exit ±128) - the EXTERNAL
                                         //! media-lock condition (USER rule)
  output logic [31:0] dbg_frame_o        //! DAC-serial forensics: the exact
                                         //! 32 bits shifted out in the last
                                         //! LEFT half-frame. NOTE the window
                                         //! is LRCK-aligned, so CORRECT
                                         //! Philips data (1-bit delay) reads
                                         //! sample = (word >> 7) & 0xFFFFFF
                                         //! (loops i2s_sdin_o
                                         //! back digitally - shows what the
                                         //! CS4344 receives, no scope needed)
);

  assign trim_o = 16'sd0;                //! NCO retired (clean-clock rework)

  // ------------------------------------------------------------------ //
  // PCM tap: half-beat position walker (USER 1-to-1 mapping rule).       //
  // A frame of C channels is exactly C half-beats (4-byte S32BE groups), //
  // so one position counter mod C serves every C in 1..8: position 0     //
  // latches ch0, position 1 completes the {L,R} pair. Even C = the old   //
  // beat-aligned stride; odd C>=3 straddles ch1 into the next beat via   //
  // the latch; C==1 pushes {s,0} per half-beat (two per beat) through    //
  // the staging queue. tlast (PDU = whole frames) re-zeros the walk.     //
  // ------------------------------------------------------------------ //
  wire        pcm_acc_w  = pcm_tvalid_i && pcm_tready_i;
  wire [2:0]  c_eff_w    = (wire_chans_i == 8'd0 || wire_chans_i > 8'd8)
                           ? 3'd2 : 3'(wire_chans_i);
  logic [2:0] pos_r;                     //! half-beat position in frame
  logic [23:0] lhold_r;                  //! ch0 awaiting a straddled ch1

  wire [23:0] s0_w = {pcm_tdata_i[7:0],  pcm_tdata_i[15:8],
                      pcm_tdata_i[23:16]};                    // lanes 0..3
  wire [23:0] s1_w = {pcm_tdata_i[39:32], pcm_tdata_i[47:40],
                      pcm_tdata_i[55:48]};                    // lanes 4..7

  wire [2:0] p0_w = pos_r;
  wire [2:0] p1_w = (pos_r + 3'd1 == c_eff_w) ? 3'd0 : pos_r + 3'd1;
  wire [2:0] pn_w = (p1_w  + 3'd1 == c_eff_w) ? 3'd0 : p1_w  + 3'd1;

  //! LPF path pairs (wire order): only meaningful when lpf_active_i
  wire [23:0] lpf_l_w = {lpf_tdata_i[7:0],  lpf_tdata_i[15:8],
                         lpf_tdata_i[23:16]};
  wire [23:0] lpf_r_w = {lpf_tdata_i[39:32], lpf_tdata_i[47:40],
                         lpf_tdata_i[55:48]};

  //! staging queue: up to 2 pair-writes per cycle (C==1), drained 1/cycle
  //! into the producer FIFO - unifies raw walker + LPF sources
  logic [47:0] stg_r [0:3];
  logic [1:0]  stg_wp_r, stg_rp_r;
  logic [2:0]  stg_cnt_r;

  // ------------------------------------------------------------------ //
  // Producer-side sample-pair FIFO (clk_i)                               //
  // ------------------------------------------------------------------ //
  logic [47:0] fifo_r [0:(1<<FIFO_LOG2)-1];
  logic [FIFO_LOG2:0] wptr_r, rptr_r;
  wire  [FIFO_LOG2:0] fill_w  = wptr_r - rptr_r;
  wire                full_w  = fill_w[FIFO_LOG2];
  wire                empty_w = (fill_w == '0);
  localparam logic [FIFO_LOG2:0] MID_C = 1 << (FIFO_LOG2 - 1);
  localparam logic [FIFO_LOG2:0] PREFILL_LVL_C =
      (PREFILL_C == 0) ? MID_C : (FIFO_LOG2+1)'(PREFILL_C);
  assign fill_o = 16'(fill_w);

  //! feeder: keep the small CDC FIFO topped up from the main FIFO
  logic        cdc_wen_r;
  logic [47:0] cdc_wdata_r;
  wire         cdc_wfull_w;

  //! per-ms tick for the convergence observer
  localparam int MS_DIV_C = CLK_FREQ_HZ / 1000;
  logic [$clog2(MS_DIV_C)-1:0] ms_div_r;
  logic [6:0]  conv_ms_r;
  logic        was_filled_r;   //! fill has been nonzero since last reset

  //! walker push selection (comb; hoisted per the no-block-automatics rule)
  //  C==1: two pushes {s,0}; C>=2: p0==0 -> {s0,s1} (ch1 same beat),
  //  p0==1 -> {lhold, s0} (straddled ch1), p1==0 -> latch s1 (frame starts
  //  in the upper half-beat; odd C only)
  logic        pushA_w, pushB_w;
  logic [47:0] pairA_w, pairB_w;

  always_comb begin : walker_sel
    pushA_w = 1'b0; pushB_w = 1'b0;
    pairA_w = '0;   pairB_w = '0;
    if (lpf_active_i) begin
      pushA_w = lpf_tvalid_i;
      pairA_w = {lpf_l_w, lpf_r_w};
    end
    else if (pcm_acc_w) begin
      if (c_eff_w == 3'd1) begin
        pushA_w = 1'b1; pairA_w = {s0_w, 24'h0};
        pushB_w = 1'b1; pairB_w = {s1_w, 24'h0};
      end
      else if (p0_w == 3'd0) begin
        pushA_w = 1'b1; pairA_w = {s0_w, s1_w};
      end
      else if (p0_w == 3'd1) begin
        pushA_w = 1'b1; pairA_w = {lhold_r, s0_w};
      end
    end
  end : walker_sel

  wire        stg_drain_w = (stg_cnt_r != 3'd0) && !full_w;
  wire [2:0]  stg_space_w = 3'd4 - stg_cnt_r + (stg_drain_w ? 3'd1 : 3'd0);
  wire        wA_ok_w     = pushA_w && (stg_space_w >= 3'd1);
  wire        wB_ok_w     = pushB_w && (stg_space_w >= (pushA_w ? 3'd2 : 3'd1));
  wire [1:0]  stg_wr_n_w  = {1'b0, wA_ok_w} + {1'b0, wB_ok_w};
  wire        stg_drop_w  = (pushA_w && !wA_ok_w) || (pushB_w && !wB_ok_w);

  logic prefill_r;   //! consumption held until fill >= MID_C (underrun rail
                     //! recenter - one bounded gap instead of a per-sample
                     //! repeat storm; also the clean power-up behavior)

  always_ff @(posedge clk_i) begin : producer_side
    if (!rst_n) begin
      pos_r <= '0; lhold_r <= '0; wptr_r <= '0; rptr_r <= '0;
      stg_wp_r <= '0; stg_rp_r <= '0; stg_cnt_r <= '0;
      overruns_o <= '0; cdc_wen_r <= 1'b0; cdc_wdata_r <= '0;
      ms_div_r <= '0; conv_ms_r <= '0; converged_o <= 1'b0;
      media_reset_p_o <= 1'b0; was_filled_r <= 1'b0;
      prefill_r <= 1'b1;
    end
    else begin
      media_reset_p_o <= 1'b0;

      // ---- walker state -----------------------------------------------
      if (pcm_acc_w) begin
        pos_r <= pcm_tlast_i ? 3'd0 : pn_w;
        if (p1_w == 3'd0 && c_eff_w != 3'd1) lhold_r <= s1_w;
      end

      // ---- staging queue writes + drain into the producer FIFO --------
      if (wA_ok_w) stg_r[stg_wp_r] <= pairA_w;
      if (wB_ok_w) stg_r[wA_ok_w ? 2'(stg_wp_r + 2'd1) : stg_wp_r] <= pairB_w;
      stg_wp_r  <= stg_wp_r + 2'(stg_wr_n_w);
      stg_cnt_r <= stg_cnt_r + 3'(stg_wr_n_w) - (stg_drain_w ? 3'd1 : 3'd0);
      if (stg_drain_w) begin
        fifo_r[wptr_r[FIFO_LOG2-1:0]] <= stg_r[stg_rp_r];
        stg_rp_r <= stg_rp_r + 2'd1;
        wptr_r   <= wptr_r + 1'b1;
      end
      if (stg_drop_w) begin
        media_reset_p_o <= was_filled_r;   //! overrun rail = media reset
        was_filled_r    <= 1'b0;
      end
      //! overrun rail: saturating count, W1C restart (gaps 5b - a stuck
      //! 0xFFFF rail was blind forever). A clear coincident with a drop
      //! restarts at that drop's count so no event is lost.
      if (clr_over_i)      overruns_o <= stg_drop_w ? 16'd1 : 16'd0;
      else if (stg_drop_w) overruns_o <= (&overruns_o) ? overruns_o
                                                       : overruns_o + 16'd1;
      if (!empty_w) was_filled_r <= 1'b1;

      // ---- underrun rail: enter prefill (one gap, then recenter) ------
      if (!prefill_r && empty_w && was_filled_r) begin
        prefill_r       <= 1'b1;
        media_reset_p_o <= 1'b1;
        was_filled_r    <= 1'b0;
      end
      else if (prefill_r && fill_w >= PREFILL_LVL_C) prefill_r <= 1'b0;

      // ---- feeder into the CDC FIFO (held during prefill) -------------
      cdc_wen_r <= 1'b0;
      if (!empty_w && !prefill_r && !cdc_wfull_w && !cdc_wen_r) begin
        cdc_wdata_r <= fifo_r[rptr_r[FIFO_LOG2-1:0]];
        rptr_r      <= rptr_r + 1'b1;
        cdc_wen_r   <= 1'b1;
      end

      // ---- convergence observer (per ms) ------------------------------
      ms_div_r <= (ms_div_r == MS_DIV_C - 1) ? '0 : ms_div_r + 1'b1;
      if (ms_div_r == MS_DIV_C - 1) begin
        if (fill_w > MID_C - 64 && fill_w < MID_C + 64) begin
          if (conv_ms_r != 7'd100) conv_ms_r <= conv_ms_r + 7'd1;
          else                     converged_o <= 1'b1;
        end
        else if (fill_w < MID_C - 128 || fill_w > MID_C + 128) begin
          conv_ms_r   <= '0;
          converged_o <= 1'b0;
        end
      end
    end
  end : producer_side

  // ------------------------------------------------------------------ //
  // Clock-domain crossing                                                //
  // ------------------------------------------------------------------ //
  logic [1:0] arst_n_r;                  //! audio-domain reset sync
  wire        rd_empty_w;
  wire [47:0] rd_pair_w;
  logic       rd_en_r;

  cdc_pair_fifo #(.WIDTH(48), .LOG2D(4)) u_cdc (
    .wclk_i  (clk_i),
    .wrst_n  (rst_n),
    .wen_i   (cdc_wen_r),
    .wdata_i (cdc_wdata_r),
    .wfull_o (cdc_wfull_w),
    .rclk_i  (clk_audio_i),
    .rrst_n  (arst_n_r[1]),
    .ren_i   (rd_en_r),
    .rdata_o (rd_pair_w),
    .rempty_o(rd_empty_w)
  );

  // ------------------------------------------------------------------ //
  // Audio domain: reset sync + clean dividers + Philips I2S serializer   //
  //   clk_audio = 24.576 MHz: MCLK = /2 (12.288), SCLK = /8 (3.072,      //
  //   64 fs), LRCK = /512 (48.000 kHz)                                   //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_audio_i) begin : audio_rst_sync
    arst_n_r <= {arst_n_r[0], rst_n};
  end : audio_rst_sync

  //! W1C clear of the audio-domain underrun rail: CSR strobes are clk_i
  //! pulses, the counter lives on clk_audio_i - cdc_pulse carries it over
  //! (spacing is CSR-write-rate, far beyond the round-trip constraint)
  wire clr_under_a_w;

  cdc_pulse u_clr_under_cdc (
    .src_clk    (clk_i),
    .src_rst_n  (rst_n),
    .src_pulse  (clr_under_i),
    .dest_clk   (clk_audio_i),
    .dest_rst_n (arst_n_r[1]),
    .dest_pulse (clr_under_a_w)
  );

  logic [8:0]  adiv_r;                   //! /512 master divider
  wire         mclk_w = adiv_r[0];
  wire         sclk_w = adiv_r[2];
  wire         lrck_w = adiv_r[8];
  //! SCLK falling edge = data change point (Philips: MSB 1 SCLK after LRCK)
  wire         sclk_fall_w = (adiv_r[2:0] == 3'b111);
  wire         frame_start_w = (adiv_r == 9'h1FF);   //! next cycle starts LEFT

  logic [31:0] shift_r;
  logic [31:0] dbg_sh_r, dbg_frame_a_r;  //! DAC-serial forensics (audio domain)
  logic [23:0] pend_right_r;
  logic [15:0] underrun_a_r;             //! audio-domain underrun count
  logic [5:0]  bit_r;

  always_ff @(posedge clk_audio_i) begin : audio_engine
    if (!arst_n_r[1]) begin
      adiv_r <= '0; shift_r <= '0; pend_right_r <= '0;
      dbg_sh_r <= '0; dbg_frame_a_r <= '0;
      rd_en_r <= 1'b0;
      underrun_a_r <= '0; bit_r <= '0;
      i2s_mclk_o <= 1'b0; i2s_sclk_o <= 1'b0; i2s_lrck_o <= 1'b0;
      i2s_sdin_o <= 1'b0;
    end
    else begin
      adiv_r <= adiv_r + 1'b1;
      i2s_mclk_o <= mclk_w;
      i2s_sclk_o <= sclk_w;
      i2s_lrck_o <= lrck_w;
      rd_en_r <= 1'b0;

      //! underrun rail: saturating count, W1C restart (gaps 5b); a clear
      //! coincident with an underrun frame restarts at that frame's count
      if (clr_under_a_w)
        underrun_a_r <= (frame_start_w && rd_empty_w) ? 16'd1 : 16'd0;
      else if (frame_start_w && rd_empty_w)
        underrun_a_r <= (&underrun_a_r) ? underrun_a_r
                                        : underrun_a_r + 16'd1;

      //! pop one pair per audio frame; on empty repeat the last pair
      //! (slip-dup; the underrun rail above counts it)
      if (frame_start_w) begin
        if (!rd_empty_w) begin
          rd_en_r <= 1'b1;               //! rdata registered -> use next frame
        end
        //! load the serializer from the last popped data
        shift_r  <= {rd_pair_w[47:24], 8'h00};   //! left, 24-in-32 justified
        pend_right_r <= rd_pair_w[23:0];
        bit_r <= 6'd0;
      end
      else if (sclk_fall_w) begin
        bit_r <= bit_r + 6'd1;
        //! forensics: record the serial bits of the LEFT half as sent
        if (bit_r < 6'd32) dbg_sh_r <= {dbg_sh_r[30:0], i2s_sdin_o};
        if (bit_r == 6'd32) dbg_frame_a_r <= dbg_sh_r;
        //! Philips 1-bit delay comes from the OUTPUT REGISTER pipeline: sdin
        //! set at fall N reaches the chip's rise N, and the fall at each LRCK
        //! boundary is consumed by frame-start/reload - so the chip's delay
        //! slot already carries the previous half's zero tail. Bit slot 0
        //! must therefore send the MSB itself; an explicit pad here doubles
        //! the delay and puts the sign bit at magnitude weight 2^22 (the
        //! silicon level-independent sign-square, 2026-07-18).
        if (bit_r == 6'd32) begin        //! RIGHT half: MSB + reload
          i2s_sdin_o <= pend_right_r[23];
          shift_r    <= {pend_right_r[22:0], 9'h000};
        end
        else begin
          i2s_sdin_o <= shift_r[31];
          shift_r    <= {shift_r[30:0], 1'b0};
        end
      end
    end
  end : audio_engine

  //! underrun count into the clk_i CSR view (quasi-static, 2-FF sync per bit
  //! is unnecessary - the count is monotonic and read for trends only)
  logic [15:0] under_meta_r, under_sync_r;
  logic [31:0] dbgf_meta_r, dbgf_sync_r;
  always_ff @(posedge clk_i) begin : under_cdc
    {under_sync_r, under_meta_r} <= {under_meta_r, underrun_a_r};
    {dbgf_sync_r, dbgf_meta_r}   <= {dbgf_meta_r, dbg_frame_a_r};
  end : under_cdc
  assign underruns_o = under_sync_r;
  assign dbg_frame_o = dbgf_sync_r;

  //! keep the interface quiet about the unused legacy hooks
  wire _unused_ok = &{1'b0, servo_en_i, MCLK_DIV_LOG2[0], pcm_tlast_i, 1'b0};

endmodule

`default_nettype wire

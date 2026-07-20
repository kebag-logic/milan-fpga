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
  parameter int FIFO_LOG2     = 9       //! sample-pair FIFO depth (2^N)
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
  input  wire [9:0]   chans_i,           //! channels/frame (fmt[31:22]; >=2)

  //! --- I2S DAC (Pmod I2S2 line-out) --------------------------------------
  output logic        i2s_mclk_o,
  output logic        i2s_sclk_o,
  output logic        i2s_lrck_o,
  output logic        i2s_sdin_o,        //! serial data to the CS4344

  //! --- observability (CSR I2SPB_STAT / I2SPB_TRIM) ------------------------
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
                                         //! LEFT half-frame (loops i2s_sdin_o
                                         //! back digitally - shows what the
                                         //! CS4344 receives, no scope needed)
);

  assign trim_o = 16'sd0;                //! NCO retired (clean-clock rework)

  // ------------------------------------------------------------------ //
  // PCM tap: first beat of each channel-frame carries ch0 (lanes 0..3,   //
  // S32BE) + ch1 (lanes 4..7); stride = chans/2 beats per frame          //
  // ------------------------------------------------------------------ //
  wire        pcm_acc_w  = pcm_tvalid_i && pcm_tready_i;
  wire [8:0]  stride_w   = (chans_i[9:1] == 9'd0) ? 9'd1 : chans_i[9:1];
  logic [8:0] beat_r;

  //! render source: the serial-MAC LPF publishes filtered pairs on its own
  //! valid (a few cycles after the AXIS beat); when it is inactive
  //! (disabled / chans != 2) the raw first-beat-of-frame path is used
  wire [63:0] eff_tdata_w = lpf_active_i ? lpf_tdata_i : pcm_tdata_i;
  wire [23:0] smp_l_w = {eff_tdata_w[7:0],  eff_tdata_w[15:8],
                         eff_tdata_w[23:16]};                  // bytes 0..2
  wire [23:0] smp_r_w = {eff_tdata_w[39:32], eff_tdata_w[47:40],
                         eff_tdata_w[55:48]};                  // bytes 4..6

  // ------------------------------------------------------------------ //
  // Producer-side sample-pair FIFO (clk_i)                               //
  // ------------------------------------------------------------------ //
  logic [47:0] fifo_r [0:(1<<FIFO_LOG2)-1];
  logic [FIFO_LOG2:0] wptr_r, rptr_r;
  wire  [FIFO_LOG2:0] fill_w  = wptr_r - rptr_r;
  wire                full_w  = fill_w[FIFO_LOG2];
  wire                empty_w = (fill_w == '0);
  localparam logic [FIFO_LOG2:0] MID_C = 1 << (FIFO_LOG2 - 1);
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

  always_ff @(posedge clk_i) begin : producer_side
    if (!rst_n) begin
      beat_r <= '0; wptr_r <= '0; rptr_r <= '0;
      overruns_o <= '0; cdc_wen_r <= 1'b0; cdc_wdata_r <= '0;
      ms_div_r <= '0; conv_ms_r <= '0; converged_o <= 1'b0;
      media_reset_p_o <= 1'b0; was_filled_r <= 1'b0;
    end
    else begin
      media_reset_p_o <= 1'b0;

      // ---- PCM tap write side -----------------------------------------
      if (pcm_acc_w) begin
        beat_r <= pcm_tlast_i               ? 9'd0
                : (beat_r == stride_w - 9'd1) ? 9'd0
                : beat_r + 9'd1;
      end
      if (lpf_active_i ? lpf_tvalid_i : (pcm_acc_w && beat_r == 9'd0)) begin
        if (!full_w) begin
          fifo_r[wptr_r[FIFO_LOG2-1:0]] <= {smp_l_w, smp_r_w};
          wptr_r <= wptr_r + 1'b1;
        end
        else begin
          overruns_o <= (&overruns_o) ? overruns_o : overruns_o + 16'd1;
          media_reset_p_o <= was_filled_r;   //! rail = media reset event
          was_filled_r    <= 1'b0;
        end
      end
      if (!empty_w) was_filled_r <= 1'b1;

      // ---- feeder into the CDC FIFO -----------------------------------
      cdc_wen_r <= 1'b0;
      if (!empty_w && !cdc_wfull_w && !cdc_wen_r) begin
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

      //! pop one pair per audio frame; on empty repeat the last pair
      //! (slip-dup) and count the underrun
      if (frame_start_w) begin
        if (!rd_empty_w) begin
          rd_en_r <= 1'b1;               //! rdata registered -> use next frame
        end
        else begin
          underrun_a_r <= (&underrun_a_r) ? underrun_a_r
                                          : underrun_a_r + 16'd1;
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

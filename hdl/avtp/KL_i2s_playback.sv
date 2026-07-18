/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_i2s_playback.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : Zero-CPU I2S playback of the received AAF stream — the
                listener's audible output on the Pmod I2S2 DAC (CS4344).
                Taps the depacketizer PCM stream (observed transfers, never
                backpressures), takes channels 0..1 of each interleaved
                sample frame (S32BE, top 24 bits), buffers in a sample FIFO
                and serializes Philips-I2S (64 fs, 1-bit delay, data changes
                on SCLK falling) on the SAME free-running divider scheme the
                AAF talker uses as I2S clock master, so ADC and DAC share
                MCLK/SCLK/LRCK waveforms.

                MVP clocking: the local 48 kHz free-runs vs the talker's
                media clock, so the FIFO drifts by the ppm difference. The
                rails handle it audibly-benignly (underrun -> emit silence;
                overrun -> drop the incoming pair) and each event is
                counted (CSR I2SPB_STAT) so silicon can MEASURE the drift.
                The CRF media-clock task disciplines this divider later
                (NCO) and retires the rails.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! I2S DAC serializer for the AAF listener: PCM tap (wire-order S32BE
//! interleaved) -> stereo 24-bit sample FIFO -> Philips I2S at 64 fs on the
//! shared free-running divider (same scheme as `aaf_talker_i2s`). Underrun
//! plays silence, overrun drops a pair; both counted for drift measurement.

`default_nettype none

module KL_i2s_playback #(
  parameter int MCLK_DIV_LOG2 = 2,      //! clk -> MCLK divide (log2), = talker
  parameter int CLK_FREQ_HZ   = 50_000_000, //! datapath clock: sets the TRUE
                                        //! 48 kHz nominal NCO step (07-18: the
                                        //! 0x8000 half-rate nominal was clk/2^N
                                        //! = 48,828 Hz - the talker bug mirrored)
  parameter int FIFO_LOG2     = 9       //! sample-pair FIFO depth (2^N)
)(
  input  wire         clk_i,            //! Global clock (I2S master domain)
  input  wire         rst_n,            //! Active-low synchronous reset

  //! --- PCM tap (depacketizer m_axis, observed transfers) -----------------
  input  wire [63:0]  pcm_tdata_i,
  input  wire         pcm_tvalid_i,
  input  wire         pcm_tready_i,
  input  wire         pcm_tlast_i,
  input  wire [9:0]   chans_i,           //! channels/frame (fmt[31:22]; >=2)

  //! --- I2S DAC (Pmod I2S2 line-out; clocks shared with the ADC side) -----
  output wire         i2s_mclk_o,
  output wire         i2s_sclk_o,
  output wire         i2s_lrck_o,
  output logic        i2s_sdin_o,        //! serial data to the CS4344

  //! --- observability (CSR I2SPB_STAT / I2SPB_TRIM) ------------------------
  output logic [15:0] underruns_o,       //! LRCK frames started with FIFO empty
  output logic [15:0] overruns_o,        //! sample pairs dropped (FIFO full)
  output logic signed [15:0] trim_o,     //! NCO servo trim (LSB = 15.3 ppm)
  output logic [15:0] fill_o,            //! FIFO fill (sample pairs)
  output logic        media_reset_p_o,   //! rail event = media-clock reset
  output logic        converged_o        //! recovered clock near nominal:
                                         //! fill in MID±64 sustained 100 ms
                                         //! (exit at MID±128) - the EXTERNAL
                                         //! media-lock condition (USER rule)
);

  // ------------------------------------------------------------------ //
  // NCO-disciplined I2S divider: same waveform scheme as aaf_talker_i2s //
  // but the counter advances through a fractional accumulator whose     //
  // step is trimmed by a FIFO-fill servo — the fill integrates the      //
  // talker-vs-local rate difference, so steering it to midpoint IS      //
  // media-clock recovery (reference parity: pipewire recovers from the  //
  // bound stream, its CRF handler is consume-and-ignore).               //
  // ------------------------------------------------------------------ //
  //! HALF-RATE NCO (silicon find: a 0x10000 nominal step carries every
  //! cycle, so the divider could slow but NEVER exceed nominal - positive
  //! trim was a no-op and a high FIFO could never drain). Nominal step
  //! 0x8000 advances the (one-bit-narrower) counter every 2nd cycle;
  //! trim ±512/0x8000 = ±1.56 % in BOTH directions.
  logic [MCLK_DIV_LOG2+7-1:0] cnt_r;
  logic [15:0]        frac_r;
  logic signed [15:0] trim_r;
  //! nominal step for EXACTLY 48 kHz from CLK_FREQ_HZ (integer-truncated:
  //! -8 ppm, absorbed by the servo); 50 MHz/LOG2 2 and 100 MHz/LOG2 3 both
  //! give 32212 (vs the old 32768 = +1.7 % fast)
  localparam int NOM_STEP_C =
      int'((64'd48_000 * (64'd1 << (MCLK_DIV_LOG2+7)) * 64'd65536) / CLK_FREQ_HZ);
  wire  [16:0] step_w = 17'(NOM_STEP_C) + 17'(trim_r);
  wire  [16:0] acc_w  = {1'b0, frac_r} + step_w;
  wire         adv_w  = acc_w[16];
  assign trim_o = trim_r;
  assign i2s_mclk_o = cnt_r[MCLK_DIV_LOG2-2];
  assign i2s_sclk_o = cnt_r[MCLK_DIV_LOG2];
  assign i2s_lrck_o = cnt_r[MCLK_DIV_LOG2+6];

  //! SCLK falling edge (data change point): the advance that wraps the
  //! low bits so sclk goes 1 -> 0
  wire sclk_fall = adv_w &&
                   (cnt_r[MCLK_DIV_LOG2:0] == {1'b1, {MCLK_DIV_LOG2{1'b1}}});
  logic lrck_q;
  wire  lrck_edge = sclk_fall && (i2s_lrck_o != lrck_q);

  // ------------------------------------------------------------------ //
  // PCM tap: first beat of each channel-frame carries ch0 (lanes 0..3,   //
  // S32BE) + ch1 (lanes 4..7); stride = chans/2 beats per frame          //
  // ------------------------------------------------------------------ //
  wire        pcm_acc_w  = pcm_tvalid_i && pcm_tready_i;
  wire [8:0]  stride_w   = (chans_i[9:1] == 9'd0) ? 9'd1 : chans_i[9:1];
  logic [8:0] beat_r;

  wire [23:0] smp_l_w = {pcm_tdata_i[7:0],  pcm_tdata_i[15:8],
                         pcm_tdata_i[23:16]};                  // bytes 0..2
  wire [23:0] smp_r_w = {pcm_tdata_i[39:32], pcm_tdata_i[47:40],
                         pcm_tdata_i[55:48]};                  // bytes 4..6
  wire take_pair_w = pcm_acc_w && (beat_r == 9'd0);

  // ------------------------------------------------------------------ //
  // Sample-pair FIFO (BRAM/LUTRAM; 48-bit {L,R})                         //
  // ------------------------------------------------------------------ //
  logic [47:0] fifo_r [0:(1<<FIFO_LOG2)-1];
  logic [FIFO_LOG2:0] wptr_r, rptr_r;
  wire  [FIFO_LOG2:0] fill_w  = wptr_r - rptr_r;
  wire                full_w  = fill_w[FIFO_LOG2];
  wire                empty_w = (fill_w == '0);
  localparam logic [FIFO_LOG2:0] MID_C = 1 << (FIFO_LOG2 - 1);
  logic [5:0]  servo_ms_r;
  logic [6:0]  conv_ms_r;      //! consecutive ms inside the entry window
  logic        was_playing_r;   //! a pair has popped since the last empty
  assign fill_o = 16'(fill_w);
  logic [47:0] rd_pair_r;

  // ------------------------------------------------------------------ //
  // I2S shift engine: load at each LRCK edge, shift on SCLK falling.     //
  // Philips I2S: 1-bit delay, MSB first, LEFT while LRCK=0.              //
  // ------------------------------------------------------------------ //
  logic [31:0] shift_r;
  logic [23:0] pend_right_r;

  always_ff @(posedge clk_i) begin : playback
    if (!rst_n) begin
      cnt_r        <= '0;
      frac_r       <= '0;
      trim_r       <= '0;
      servo_ms_r   <= '0;
      was_playing_r <= 1'b0;
      media_reset_p_o <= 1'b0;
      conv_ms_r    <= '0;
      converged_o  <= 1'b0;
      lrck_q       <= 1'b0;
      beat_r       <= '0;
      wptr_r       <= '0;
      rptr_r       <= '0;
      rd_pair_r    <= '0;
      shift_r      <= '0;
      pend_right_r <= '0;
      i2s_sdin_o   <= 1'b0;
      underruns_o  <= '0;
      overruns_o   <= '0;
    end
    else begin
      media_reset_p_o <= 1'b0;
      frac_r <= acc_w[15:0];
      if (adv_w) cnt_r <= cnt_r + 1'b1;

      // ---- fill servo: at ~1 ms cadence steer the fill to midpoint ----
      if (adv_w && cnt_r == '1) begin          // one LRCK frame elapsed
        servo_ms_r <= servo_ms_r + 6'd1;
        if (servo_ms_r == 6'd47) begin         // 48 frames = 1 ms @48 kHz
          servo_ms_r <= '0;
          if (fill_w != '0) begin        //! stream present: steer to midpoint
            if (fill_w > MID_C + 1 && trim_r <  16'sd512) trim_r <= trim_r + 16'sd1;
            if (fill_w < MID_C - 1 && trim_r > -16'sd512) trim_r <= trim_r - 16'sd1;
          end
          //! convergence hysteresis (per-ms): enter ±64/100 ms, exit ±128
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

      // ---- PCM tap write side -------------------------------------
      if (pcm_acc_w) begin
        beat_r <= pcm_tlast_i          ? 9'd0
                : (beat_r == stride_w - 9'd1) ? 9'd0
                : beat_r + 9'd1;
        if (beat_r == 9'd0) begin
          if (!full_w) begin
            fifo_r[wptr_r[FIFO_LOG2-1:0]] <= {smp_l_w, smp_r_w};
            wptr_r <= wptr_r + 1'b1;
          end
          else begin
            overruns_o <= (&overruns_o) ? overruns_o : overruns_o + 16'd1;
            media_reset_p_o <= 1'b1;
          end
        end
      end

      // ---- I2S serializer -------------------------------------------
      if (sclk_fall) begin
        lrck_q <= i2s_lrck_o;
        if (lrck_edge) begin
          if (i2s_lrck_o == 1'b0) begin
            //! LEFT half begins: pop a pair (or play silence)
            if (!empty_w) begin
              rd_pair_r <= fifo_r[rptr_r[FIFO_LOG2-1:0]];
              //! out bit at the NEXT fall = shift[31]; the lrck-edge fall
              //! itself drives the single I2S delay bit (0)
              shift_r   <= {fifo_r[rptr_r[FIFO_LOG2-1:0]][47:24], 8'b0};
              pend_right_r <= fifo_r[rptr_r[FIFO_LOG2-1:0]][23:0];
              rptr_r    <= rptr_r + 1'b1;
              was_playing_r <= 1'b1;
            end
            else begin
              shift_r      <= '0;
              pend_right_r <= '0;
              underruns_o  <= (&underruns_o) ? underruns_o
                                             : underruns_o + 16'd1;
              //! reset event only on the playing -> starved transition
              media_reset_p_o <= was_playing_r;
              was_playing_r   <= 1'b0;
            end
          end
          else begin
            //! RIGHT half begins
            shift_r <= {pend_right_r, 8'b0};
          end
        end
        else begin
          shift_r <= {shift_r[30:0], 1'b0};
        end
        i2s_sdin_o <= lrck_edge ? 1'b0 : shift_r[31];
      end
    end
  end : playback

endmodule

`default_nettype wire

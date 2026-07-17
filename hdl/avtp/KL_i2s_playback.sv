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

  //! --- observability (CSR I2SPB_STAT) -------------------------------------
  output logic [15:0] underruns_o,       //! LRCK frames started with FIFO empty
  output logic [15:0] overruns_o         //! sample pairs dropped (FIFO full)
);

  // ------------------------------------------------------------------ //
  // Free-running I2S divider — identical scheme to aaf_talker_i2s so    //
  // both converters see the same waveforms (phase-locked by common      //
  // reset and clock).                                                    //
  // ------------------------------------------------------------------ //
  logic [MCLK_DIV_LOG2+8-1:0] cnt_r;
  assign i2s_mclk_o = cnt_r[MCLK_DIV_LOG2-1];
  assign i2s_sclk_o = cnt_r[MCLK_DIV_LOG2+1];
  assign i2s_lrck_o = cnt_r[MCLK_DIV_LOG2+7];

  //! SCLK falling edge (data change point) and LRCK edge detection
  wire sclk_fall = (cnt_r[MCLK_DIV_LOG2+1:0] == {2'b11, {MCLK_DIV_LOG2{1'b1}}});
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
      cnt_r <= cnt_r + 1'b1;

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
            end
            else begin
              shift_r      <= '0;
              pend_right_r <= '0;
              underruns_o  <= (&underruns_o) ? underruns_o
                                             : underruns_o + 16'd1;
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

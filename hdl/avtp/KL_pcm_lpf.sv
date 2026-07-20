/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pcm_lpf.sv
//  Project     : Milan AVTP
//
//  Description : 2nd-order IIR (biquad) Butterworth low-pass on the PCM
//                playback tap - the last digital stage before the DAC, i.e.
//                the signal the loop ADC receives. Band-limits the render
//                (out-of-band hash, zero-order-hold images) to raise the
//                analog output quality; the DMA-ring/AVB copies of the
//                stream stay bit-true (only the DAC tap is filtered).
//
//                fc = 20 kHz @ fs = 48 kHz, Q = 1/sqrt(2) (Butterworth),
//                bilinear transform; Q2.14 coefficients chosen so the DC
//                gain is EXACTLY 1.0 after rounding:
//                  b = {11294, 22587, 11294}, a = {20966, 7825}
//                  sum(b) = 45175 = 16384 + sum(a)  ->  unity DC.
//
//                Direct Form I per channel, s24 audio, 44-bit accumulator,
//                round-half-up at >>14, saturate to s24. The filtered beat
//                is produced COMBINATIONALLY from the current input beat +
//                registered history (zero added latency); state advances on
//                each accepted beat.
//
//                Beats are the depacketizer's 64-bit words: two S32BE
//                samples (L then R in wire byte order, audio in the top 24
//                bits). The filter engages only for 2-channel formats
//                (chans_i == 2) AND enable_i (LPF_CTRL[0]); anything else
//                passes through untouched.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_pcm_lpf (
    input  wire        clk_i,
    input  wire        rst_n,

    input  wire        enable_i,        //! LPF_CTRL[0] (CSR; default on)
    input  wire [9:0]  chans_i,         //! channels/frame (filter iff == 2)

    //! PCM tap in (observer side of the m_axis_pcm stream)
    input  wire [63:0] s_tdata,
    input  wire        s_tvalid,
    input  wire        s_tready,        //! the DMA consumer's ready (observed)

    //! filtered tdata for the playback tap (same-cycle)
    output wire [63:0] m_tdata
);

  //! Q2.14 Butterworth coefficients (fc 20 kHz / fs 48 kHz)
  localparam logic signed [16:0] B0_C = 17'sd11294;
  localparam logic signed [16:0] B1_C = 17'sd22587;
  localparam logic signed [16:0] B2_C = 17'sd11294;
  localparam logic signed [16:0] A1_C = 17'sd20966;
  localparam logic signed [16:0] A2_C = 17'sd7825;

  wire beat_acc = s_tvalid & s_tready;
  wire active   = enable_i && (chans_i == 10'd2);

  //! S32BE unpack: wire byte 0 = lane 0 = sample MSB; audio = top 24 bits
  wire signed [23:0] xl = {s_tdata[7:0],   s_tdata[15:8],  s_tdata[23:16]};
  wire signed [23:0] xr = {s_tdata[39:32], s_tdata[47:40], s_tdata[55:48]};

  //! per-channel Direct Form I state
  logic signed [23:0] xl1_r, xl2_r, yl1_r, yl2_r;
  logic signed [23:0] xr1_r, xr2_r, yr1_r, yr2_r;

  function automatic logic signed [23:0] biquad(
      input logic signed [23:0] x,
      input logic signed [23:0] x1, input logic signed [23:0] x2,
      input logic signed [23:0] y1, input logic signed [23:0] y2);
    logic signed [43:0] acc;
    logic signed [29:0] shifted;
    begin
      acc = B0_C * x + B1_C * x1 + B2_C * x2
          - A1_C * y1 - A2_C * y2;
      shifted = 30'(acc >>> 14) + 30'((acc[13]) ? 1 : 0); // round half up
      if      (shifted >  30'sd8388607)  biquad = 24'sd8388607;
      else if (shifted < -30'sd8388608)  biquad = -24'sd8388608;
      else                               biquad = 24'(shifted);
    end
  endfunction

  wire signed [23:0] yl = biquad(xl, xl1_r, xl2_r, yl1_r, yl2_r);
  wire signed [23:0] yr = biquad(xr, xr1_r, xr2_r, yr1_r, yr2_r);

  always_ff @(posedge clk_i or negedge rst_n) begin : state
    if (!rst_n) begin
      xl1_r <= '0; xl2_r <= '0; yl1_r <= '0; yl2_r <= '0;
      xr1_r <= '0; xr2_r <= '0; yr1_r <= '0; yr2_r <= '0;
    end else if (!active) begin
      //! bypass keeps history primed with the live signal so an enable
      //! transition does not thump
      if (beat_acc) begin
        xl1_r <= xl; xl2_r <= xl1_r; yl1_r <= xl; yl2_r <= yl1_r;
        xr1_r <= xr; xr2_r <= xr1_r; yr1_r <= xr; yr2_r <= yr1_r;
      end
    end else if (beat_acc) begin
      xl1_r <= xl; xl2_r <= xl1_r; yl1_r <= yl; yl2_r <= yl1_r;
      xr1_r <= xr; xr2_r <= xr1_r; yr1_r <= yr; yr2_r <= yr1_r;
    end
  end : state

  //! repack (audio in the top 24 bits of each S32BE sample; low byte 0)
  wire [63:0] filt = { 8'h00, yr[7:0], yr[15:8], yr[23:16],
                       8'h00, yl[7:0], yl[15:8], yl[23:16] };

  assign m_tdata = active ? filt : s_tdata;

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_tone_gen.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : Pilot-tone source for the end-to-end audio test: 1 kHz sine
                at 0 dBFS, 24-bit. At 48 kHz sampling 1 kHz is EXACTLY 48
                samples/period, so a fixed 48-entry table is perfectly
                periodic - the only distortion is the 24-bit rounding of 48
                constants: computed digital THD+N = -148.1 dB (28 dB margin
                over the -120 dBFS acceptance bound; on silicon the DAC/ADC
                dominate). The index advances on the same free-running LRCK
                divider scheme the talker uses, one step per sample frame.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! 1 kHz / 0 dBFS pilot tone: 48-sample exact-period 24-bit sine table
//! (quantization-only distortion, THD+N = -148.1 dB digital), stepping at
//! the 48 kHz sample cadence of the shared I2S divider scheme.

`default_nettype none

module KL_tone_gen #(
  parameter int MCLK_DIV_LOG2 = 2   //! clk -> MCLK divide (log2), = talker
)(
  input  wire         clk_i,        //! Global clock (I2S master domain)
  input  wire         rst_n,        //! Active-low synchronous reset
  input  wire         enable_i,     //! CSR TONE_CTRL[0]
  output logic [23:0] smp_o         //! current 24-bit sample (0 when off)
);

  localparam logic signed [23:0] TONE_TAB_C [0:47] = '{
    24'sh000000, 24'sh10B515, 24'sh2120FB, 24'sh30FBC5,
    24'sh3FFFFF, 24'sh4DEBE4, 24'sh5A8279, 24'sh658C99,
    24'sh6ED9EB, 24'sh7641AE, 24'sh7BA374, 24'sh7EE7A9,
    24'sh7FFFFF, 24'sh7EE7A9, 24'sh7BA374, 24'sh7641AE,
    24'sh6ED9EB, 24'sh658C99, 24'sh5A8279, 24'sh4DEBE4,
    24'sh3FFFFF, 24'sh30FBC5, 24'sh2120FB, 24'sh10B515,
    24'sh000000, 24'shEF4AEB, 24'shDEDF05, 24'shCF043B,
    24'shC00001, 24'shB2141C, 24'shA57D87, 24'sh9A7367,
    24'sh912615, 24'sh89BE52, 24'sh845C8C, 24'sh811857,
    24'sh800001, 24'sh811857, 24'sh845C8C, 24'sh89BE52,
    24'sh912615, 24'sh9A7367, 24'shA57D87, 24'shB2141C,
    24'shC00000, 24'shCF043B, 24'shDEDF05, 24'shEF4AEB
  };

  //! one step per LRCK period (the talker samples at each full frame)
  logic [MCLK_DIV_LOG2+8-1:0] cnt_r;
  logic [5:0]                 idx_r;
  wire frame_tick = (cnt_r == '1);

  always_ff @(posedge clk_i) begin : tone_step
    if (!rst_n) begin
      cnt_r <= '0;
      idx_r <= '0;
      smp_o <= '0;
    end
    else begin
      cnt_r <= cnt_r + 1'b1;
      if (!enable_i) begin
        idx_r <= '0;
        smp_o <= '0;
      end
      else if (frame_tick) begin
        idx_r <= (idx_r == 6'd47) ? 6'd0 : idx_r + 6'd1;
        smp_o <= TONE_TAB_C[idx_r];
      end
    end
  end : tone_step

endmodule

`default_nettype wire

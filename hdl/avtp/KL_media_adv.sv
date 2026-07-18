/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_media_adv.sv
  Author      : Kebag Logic

  Date        : 2026-07-18
  Description : Fractional-N media-clock advance strobe. The talker's I2S
                divider chain is a binary ripple of clk, so its sample rate
                is clk / 2^(MCLK_DIV_LOG2+8) = 48,828.125 Hz on both 50 and
                100 MHz datapaths (+1.725 % vs the declared 48 kHz - outside
                the listener servo's +/-1.56 % capture range: audible
                pumping, measured on wire 2026-07-18 as exactly 122,880 ns
                per 6-sample frame). This module deletes ~1.7 % of counter
                advances so the chain averages TRUE 48 kHz: an accumulator
                adds TICK_HZ (= fs * 2^(MCLK_DIV_LOG2+8)) each cycle and
                asserts adv_o on wrap against CLK_FREQ_HZ. Consumers advance
                their free counters ONLY when adv_o is high and must qualify
                counter-equality strobes with adv_o (a paused counter holds
                the compare true for more than one cycle). Jitter is one clk
                cycle on MCLK - fine for the fabric tone/framer path; a
                physical ADC fed from this MCLK inherits that jitter (CRF or
                a real 12.288 MHz source remains the audiophile path).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Fractional-N advance strobe: adv_o duty = TICK_HZ / CLK_FREQ_HZ exactly
//! (long-term average), one-cycle jitter. TICK_HZ must be < CLK_FREQ_HZ.

`default_nettype none

module KL_media_adv #(
  parameter int CLK_FREQ_HZ = 50_000_000,  //! datapath clock (Hz)
  parameter int TICK_HZ     = 49_152_000   //! target advance rate (Hz)
)(
  input  wire  clk_i,   //! Global clock
  input  wire  rst_n,   //! Active-low synchronous reset
  output logic adv_o    //! advance strobe (TICK_HZ average rate)
);

  localparam int ACC_W_C = $clog2(CLK_FREQ_HZ) + 1;

  logic [ACC_W_C-1:0] acc_r;
  wire  [ACC_W_C:0]   sum_w = {1'b0, acc_r} + (ACC_W_C+1)'(TICK_HZ);
  wire                wrap_w = (sum_w >= (ACC_W_C+1)'(CLK_FREQ_HZ));

  always_ff @(posedge clk_i) begin : adv_gen
    if (!rst_n) begin
      acc_r <= '0;
      adv_o <= 1'b0;
    end
    else begin
      acc_r <= wrap_w ? ACC_W_C'(sum_w - (ACC_W_C+1)'(CLK_FREQ_HZ))
                      : ACC_W_C'(sum_w);
      adv_o <= wrap_w;
    end
  end : adv_gen

endmodule

`default_nettype wire

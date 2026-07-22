/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aaf_capture_i2s.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : Physical-interface audio capture front-end (docs/
                NXN_ARCHITECTURE.md §2.1, phase P4) - the audio-domain half
                split VERBATIM out of aaf_talker_i2s (clean-clock 07-18
                lineage): I2S master clocking for the Pmod I2S2 ADC
                (CS5343) from the 24.576 MHz audio MMCM (MCLK /2, SCLK /8
                = 64 fs, LRCK /512 = 48.000 kHz), 24-bit Philips capture,
                pilot-tone override, gray-pointer CDC into the datapath
                clock, one pair popped at a time.

                The front-end is physical-interface-scoped (x1 per spec
                §2.1); the emitted pair stream carries slot_o = 0 today
                (stereo I2S = the first talker stream's channels). The
                item-4 TDM8/16 deserializer replaces this module 1:1 and
                widens slot_o - the shared packetizer (KL_aaf_packetizer)
                is already indexed by it.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Audio capture front-end (NXN §2.1 / P4): the I2S/CDC half of the old
//! aaf_talker_i2s, emitting a {slot, L, R} pair stream in the datapath
//! clock toward the shared AAF packetizer. Bit-exact extraction (clean-
//! clock dividers, tone override, gray-pointer pair CDC, pop pacing).

`default_nettype none

module KL_aaf_capture_i2s (
    input  wire         clk_i,             //! datapath clock
    input  wire         rst_n,             //! active-low synchronous reset
    input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

    //! pilot tone override (CSR TONE_CTRL: when set, ADC samples are
    //! replaced by tone_smp_i on both channels)
    input  wire         tone_en_i,
    input  wire [23:0]  tone_smp_i,

    // ---- Pmod I2S2 ADC (line-in row; we are the clock master) -----------
    output wire         i2s_mclk_o,
    output wire         i2s_sclk_o,
    output wire         i2s_lrck_o,
    input  wire         i2s_sdout_i,       //! ADC serial data

    // ---- pair stream out (clk_i domain; one pulse per L/R pair) ---------
    output logic        pair_valid_o,      //! one-cycle pulse per pair
    output logic [3:0]  pair_slot_o,       //! talker stream slot (0 today)
    output logic [23:0] pair_l_o,
    output logic [23:0] pair_r_o,

    // ---- status (Linux-observable via CSR) ------------------------------
    output reg  [31:0]  pairs_captured_o   //! pairs captured (liveness)
);

  //! CLEAN-CLOCK front-end (07-18): plain registered dividers of
  //! clk_audio_i; fractional-N edge jitter distorted the CS5343 (-4.5 dB
  //! THD+N from the ADC leg alone)
  logic [1:0] tarst_n_r;                //! audio-domain reset sync
  always_ff @(posedge clk_audio_i) begin : t_audio_rst
    tarst_n_r <= {tarst_n_r[0], rst_n};
  end : t_audio_rst

  logic [8:0] tdiv_r;
  always_ff @(posedge clk_audio_i) begin : t_audio_div
    if (!tarst_n_r[1]) tdiv_r <= '0;
    else               tdiv_r <= tdiv_r + 1'b1;
  end : t_audio_div
  assign i2s_mclk_o = tdiv_r[0];
  assign i2s_sclk_o = tdiv_r[2];
  assign i2s_lrck_o = tdiv_r[8];

  //! SCLK rising edge (sample SDOUT): tdiv[2:0] wraps 011 -> 100
  wire tsclk_rise_w = (tdiv_r[2:0] == 3'b011);
  logic        tlrck_q_r;
  logic [31:0] tshift_r;
  logic [23:0] tsample_l_r;
  logic [23:0] cap_l_r, cap_r_r;
  logic        cap_wen_r;
  wire         cap_full_w;

  always_ff @(posedge clk_audio_i) begin : t_audio_cap
    if (!tarst_n_r[1]) begin
      tlrck_q_r <= 1'b0; tshift_r <= '0; tsample_l_r <= '0;
      cap_l_r <= '0; cap_r_r <= '0; cap_wen_r <= 1'b0;
    end else begin
      cap_wen_r <= 1'b0;
      if (tsclk_rise_w) begin
        if (i2s_lrck_o != tlrck_q_r) begin
          // the half that just ENDED: tlrck_q==0 -> LEFT ended
          if (!tlrck_q_r) tsample_l_r <= tone_en_i ? tone_smp_i : tshift_r[30:7];
          else begin
            //! tone: both channels carry the same sample
            cap_l_r   <= tsample_l_r;
            cap_r_r   <= tone_en_i ? tsample_l_r : tshift_r[30:7];
            cap_wen_r <= !cap_full_w;
          end
          tshift_r <= {31'd0, i2s_sdout_i};
        end else begin
          tshift_r <= {tshift_r[30:0], i2s_sdout_i};
        end
        tlrck_q_r <= i2s_lrck_o;
      end
    end
  end : t_audio_cap

  //! pairs into the datapath clock domain
  wire        cap_rempty_w;
  wire [47:0] cap_pair_w;
  logic       cap_ren_r;
  cdc_pair_fifo #(.WIDTH(48), .LOG2D(3)) u_tcdc (
    .wclk_i  (clk_audio_i),
    .wrst_n  (tarst_n_r[1]),
    .wen_i   (cap_wen_r),
    .wdata_i ({cap_l_r, cap_r_r}),
    .wfull_o (cap_full_w),
    .rclk_i  (clk_i),
    .rrst_n  (rst_n),
    .ren_i   (cap_ren_r),
    .rdata_o (cap_pair_w),
    .rempty_o(cap_rempty_w)
  );

  //! clk_i side: pop one pair at a time; pair_valid pulses per pop
  always_ff @(posedge clk_i or negedge rst_n) begin : t_pop
    if (!rst_n) begin
      pair_l_o <= '0; pair_r_o <= '0;
      pair_valid_o <= 1'b0; cap_ren_r <= 1'b0;
      pairs_captured_o <= '0;
    end else begin
      pair_valid_o <= cap_ren_r;        //! rdata registered: valid follows ren
      if (cap_ren_r) begin
        pair_l_o <= cap_pair_w[47:24];
        pair_r_o <= cap_pair_w[23:0];
      end
      cap_ren_r <= !cap_rempty_w && !cap_ren_r && !pair_valid_o;
      if (pair_valid_o) pairs_captured_o <= pairs_captured_o + 1'b1;
    end
  end : t_pop

  assign pair_slot_o = 4'd0;            //! stereo I2S = talker stream 0

endmodule

`default_nettype wire

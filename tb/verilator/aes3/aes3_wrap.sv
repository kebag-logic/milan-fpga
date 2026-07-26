/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : aes3_wrap.sv
  Author      : Kebag Logic

  Date        : 2026-07-26
  Description : Verilator harness wrapper for the AES3/S-PDIF ser/des pair.
                One KL_aes3_tx drives ONE biphase-mark line; four KL_aes3_rx
                instances listen to it at once, which is what makes the
                width and dialect checks exact - they all decode the SAME
                wire, so any difference is the parameter under test:

                  r24  WORD_BITS_P=24, CONSUMER_P=0  the reference receiver
                  r20  WORD_BITS_P=20                truncation at 20 bits
                  r16  WORD_BITS_P=16                truncation at 16 bits
                  rc   CONSUMER_P=1                  IEC 60958-3 dialect

                flip_i XORs the line, so a short assertion injects a pair of
                extra transitions - a real biphase violation, not a modelled
                error flag - which is how the lock/error contract is tested.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

`default_nettype none

module aes3_wrap (
  input  wire        clk,               //! datapath clock
  input  wire        rst_n,             //! active-low synchronous reset
  input  wire        clk_audio,         //! serial / oversampling clock

  // ---- transmitter ------------------------------------------------------
  input  wire        pair_valid_i,
  input  wire [23:0] pair_l_i,
  input  wire [23:0] pair_r_i,
  input  wire        smp_invalid_i,
  input  wire [31:0] cs_bits_i,
  output wire        pair_ready_o,
  output wire [31:0] tx_frames_o,
  output wire [15:0] tx_blocks_o,
  output wire [15:0] tx_under_o,

  // ---- line + fault injection -------------------------------------------
  output wire        line_o,            //! the raw transmitted line
  input  wire        flip_i,            //! XOR the line (inject transitions)

  // ---- reference receiver (24-bit, AES3 professional) -------------------
  output wire        r24_pv_o,
  output wire [3:0]  r24_slot_o,
  output wire [23:0] r24_l_o,
  output wire [23:0] r24_r_o,
  output wire [31:0] r24_pairs_o,
  output wire        r24_lock_o,
  output wire        r24_csv_o,
  output wire [31:0] r24_cs_o,
  output wire        r24_pro_o,
  output wire [3:0]  r24_fs_o,
  output wire [2:0]  r24_emph_o,
  output wire        r24_mism_o,
  output wire [15:0] r24_blocks_o,
  output wire [15:0] r24_par_o,
  output wire [15:0] r24_inv_o,
  output wire [15:0] r24_loss_o,

  // ---- narrow-word receivers -------------------------------------------
  output wire        r20_pv_o,
  output wire [23:0] r20_l_o,
  output wire [23:0] r20_r_o,
  output wire        r20_lock_o,
  output wire        r16_pv_o,
  output wire [23:0] r16_l_o,
  output wire [23:0] r16_r_o,
  output wire        r16_lock_o,

  // ---- consumer-dialect receiver ---------------------------------------
  output wire        rc_csv_o,
  output wire        rc_pro_o,
  output wire [3:0]  rc_fs_o,
  output wire [2:0]  rc_emph_o,
  output wire        rc_mism_o
);

  wire tline_w;
  assign line_o = tline_w;
  //! the wire every receiver actually sees
  wire rxline_w = tline_w ^ flip_i;

  KL_aes3_tx #(.OVERSAMPLE_P(4), .WORD_BITS_P(24), .CONSUMER_P(1'b0)) u_tx (
    .clk_i        (clk),
    .rst_n        (rst_n),
    .clk_audio_i  (clk_audio),
    .pair_valid_i (pair_valid_i),
    .pair_l_i     (pair_l_i),
    .pair_r_i     (pair_r_i),
    .smp_invalid_i(smp_invalid_i),
    .pair_ready_o (pair_ready_o),
    .cs_bits_i    (cs_bits_i),
    .aes_tx_o     (tline_w),
    .frames_o     (tx_frames_o),
    .blocks_o     (tx_blocks_o),
    .underrun_o   (tx_under_o)
  );

  KL_aes3_rx #(.CONSUMER_P(1'b0), .WORD_BITS_P(24)) u_r24 (
    .clk_i           (clk),
    .rst_n           (rst_n),
    .clk_audio_i     (clk_audio),
    .aes_rx_i        (rxline_w),
    .pair_valid_o    (r24_pv_o),
    .pair_slot_o     (r24_slot_o),
    .pair_l_o        (r24_l_o),
    .pair_r_o        (r24_r_o),
    .pairs_captured_o(r24_pairs_o),
    .locked_o        (r24_lock_o),
    .cs_valid_o      (r24_csv_o),
    .cs_bits_o       (r24_cs_o),
    .cs_pro_o        (r24_pro_o),
    .cs_fs_code_o    (r24_fs_o),
    .cs_emphasis_o   (r24_emph_o),
    .cs_mismatch_o   (r24_mism_o),
    .blocks_o        (r24_blocks_o),
    .parity_err_o    (r24_par_o),
    .invalid_o       (r24_inv_o),
    .sync_loss_o     (r24_loss_o)
  );

  KL_aes3_rx #(.CONSUMER_P(1'b0), .WORD_BITS_P(20)) u_r20 (
    .clk_i           (clk),
    .rst_n           (rst_n),
    .clk_audio_i     (clk_audio),
    .aes_rx_i        (rxline_w),
    .pair_valid_o    (r20_pv_o),
    .pair_slot_o     (),
    .pair_l_o        (r20_l_o),
    .pair_r_o        (r20_r_o),
    .pairs_captured_o(),
    .locked_o        (r20_lock_o),
    .cs_valid_o      (),
    .cs_bits_o       (),
    .cs_pro_o        (),
    .cs_fs_code_o    (),
    .cs_emphasis_o   (),
    .cs_mismatch_o   (),
    .blocks_o        (),
    .parity_err_o    (),
    .invalid_o       (),
    .sync_loss_o     ()
  );

  KL_aes3_rx #(.CONSUMER_P(1'b0), .WORD_BITS_P(16)) u_r16 (
    .clk_i           (clk),
    .rst_n           (rst_n),
    .clk_audio_i     (clk_audio),
    .aes_rx_i        (rxline_w),
    .pair_valid_o    (r16_pv_o),
    .pair_slot_o     (),
    .pair_l_o        (r16_l_o),
    .pair_r_o        (r16_r_o),
    .pairs_captured_o(),
    .locked_o        (r16_lock_o),
    .cs_valid_o      (),
    .cs_bits_o       (),
    .cs_pro_o        (),
    .cs_fs_code_o    (),
    .cs_emphasis_o   (),
    .cs_mismatch_o   (),
    .blocks_o        (),
    .parity_err_o    (),
    .invalid_o       (),
    .sync_loss_o     ()
  );

  KL_aes3_rx #(.CONSUMER_P(1'b1), .WORD_BITS_P(24)) u_rc (
    .clk_i           (clk),
    .rst_n           (rst_n),
    .clk_audio_i     (clk_audio),
    .aes_rx_i        (rxline_w),
    .pair_valid_o    (),
    .pair_slot_o     (),
    .pair_l_o        (),
    .pair_r_o        (),
    .pairs_captured_o(),
    .locked_o        (),
    .cs_valid_o      (rc_csv_o),
    .cs_bits_o       (),
    .cs_pro_o        (rc_pro_o),
    .cs_fs_code_o    (rc_fs_o),
    .cs_emphasis_o   (rc_emph_o),
    .cs_mismatch_o   (rc_mism_o),
    .blocks_o        (),
    .parity_err_o    (),
    .invalid_o       (),
    .sync_loss_o     ()
  );

endmodule

`default_nettype wire

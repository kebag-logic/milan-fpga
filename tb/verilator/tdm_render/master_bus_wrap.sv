/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//! #584: the 8x8's render lane on its real timing owner. KL_tdm_capture_master
//! owns a TDM32 bus (32 slots of 32 bit clocks, fsync one bit early) and
//! exports its bit-clock enables and frame position; KL_tdm_render_master
//! renders the first SLOTS_P of its BUS_SLOTS_P slots from them, as
//! milan_datapath composes the two on a master build.
`default_nettype none
module bus_wrap #(
  parameter int unsigned SLOTS_P     = 1,
  parameter int unsigned BUS_SLOTS_P = 32
)(
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire        clk_audio_i,
  input  wire        smp_wr_en_i,
  input  wire        smp_wr_slot_i,
  input  wire [23:0] smp_wr_data_i,
  input  wire        tick_i,
  output wire        commit_en_o,
  output wire        tdm_bclk_o,
  output wire        tdm_fsync_o,
  output wire        tdm_dout_o,
  output wire [15:0] frames_o
);
  localparam int unsigned POS_W_C = $clog2(BUS_SLOTS_P * 32);
  wire               rise_w, fall_w;
  wire [POS_W_C-1:0] pos_w;
  KL_tdm_capture_master #(
    .SLOTS_P (BUS_SLOTS_P), .WORD_BITS_P (32), .BCLK_HALF_P (1), .DATA_DELAY_P (1'b1)
  ) u_owner (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (tdm_bclk_o), .tdm_fsync_o (tdm_fsync_o),
    .tdm_data_i (1'b0), .bclk_rise_o (rise_w), .bclk_fall_o (fall_w), .frame_pos_o (pos_w),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (), .pairs_captured_o ()
  );
  KL_tdm_render_master #(
    .SLOTS_P (SLOTS_P), .BUS_SLOTS_P (BUS_SLOTS_P), .SLOT_BITS_P (32), .FIFO_LOG2_P (2),
    .FRAME_POS_W_P (POS_W_C)
  ) u_render (
    .clk_i (clk_i), .rst_n (rst_n),
    .smp_wr_en_i (smp_wr_en_i), .smp_wr_slot_i (smp_wr_slot_i), .smp_wr_data_i (smp_wr_data_i),
    .tick_i (tick_i), .epoch_evt_i (1'b0), .fresh_i (1'b1), .commit_en_o (commit_en_o),
    .clk_tdm_i (clk_audio_i), .bclk_rise_i (rise_w), .bclk_fall_i (fall_w), .frame_pos_i (pos_w),
    .tdm_dout_o (tdm_dout_o), .frame_start_o (), .adopt_p_o (),
    .frames_o (frames_o), .underruns_o (), .skips_o (), .overruns_o (), .epochs_o ()
  );
endmodule
`default_nettype wire

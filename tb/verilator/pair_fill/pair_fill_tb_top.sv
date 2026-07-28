/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : pair_fill_tb_top.sv
//  Description : Verilator TB top for the HANDOVER 8.3b capture-pair pieces:
//                KL_pair_blend (I2S pair at slot 0 + TDM pairs at 1..S/2)
//                and KL_pair_zero_fill (the Milan v1.2 5.3.7.3 silence
//                filler, fed-tracked on the media tick). Shapes match the
//                Arty 4x4: TDM8 blend (5 physical pair slots) and an
//                8-pair-slot fill span (4 talkers x 4ch / 2). tick_i is
//                harness-driven: the clk_audio/512 divider + cdc_pulse that
//                produce it in milan_datapath are covered by the cdc suite
//                and check_wire_accountability W5.
//---------------------------------------------------------------------------//

`default_nettype none

module pair_fill_tb_top (
  input  wire        clk_i,
  input  wire        rst_n,

  // ---- KL_pair_blend ---------------------------------------------------
  input  wire        b_i2s_pv_i,
  input  wire [23:0] b_i2s_l_i,
  input  wire [23:0] b_i2s_r_i,
  input  wire        b_tdm_pv_i,
  input  wire [3:0]  b_tdm_slot_i,
  input  wire [23:0] b_tdm_l_i,
  input  wire [23:0] b_tdm_r_i,
  output wire        b_pv_o,
  output wire [3:0]  b_slot_o,
  output wire [23:0] b_l_o,
  output wire [23:0] b_r_o,
  output wire [31:0] b_merged_o,

  // ---- KL_pair_zero_fill ------------------------------------------------
  input  wire        z_tick_i,
  input  wire        z_pv_i,
  input  wire [4:0]  z_slot_i,
  input  wire [23:0] z_l_i,
  input  wire [23:0] z_r_i,
  output wire        z_pv_o,
  output wire [4:0]  z_slot_o,
  output wire [23:0] z_l_o,
  output wire [23:0] z_r_o,
  output wire [31:0] z_fill_cnt_o
);

  KL_pair_blend #(.TDM_SLOTS_P (8)) u_blend (
    .clk_i (clk_i), .rst_n (rst_n),
    .i2s_pair_valid_i (b_i2s_pv_i),
    .i2s_pair_l_i (b_i2s_l_i), .i2s_pair_r_i (b_i2s_r_i),
    .tdm_pair_valid_i (b_tdm_pv_i), .tdm_pair_slot_i (b_tdm_slot_i),
    .tdm_pair_l_i (b_tdm_l_i), .tdm_pair_r_i (b_tdm_r_i),
    .pair_valid_o (b_pv_o), .pair_slot_o (b_slot_o),
    .pair_l_o (b_l_o), .pair_r_o (b_r_o),
    .pairs_merged_o (b_merged_o)
  );

  KL_pair_zero_fill #(.TOTAL_P (8), .SLOT_W_P (5)) u_fill (
    .clk_i (clk_i), .rst_n (rst_n), .tick_i (z_tick_i),
    .pair_valid_i (z_pv_i), .pair_slot_i (z_slot_i),
    .pair_l_i (z_l_i), .pair_r_i (z_r_i),
    .pair_valid_o (z_pv_o), .pair_slot_o (z_slot_o),
    .pair_l_o (z_l_o), .pair_r_o (z_r_o),
    .fill_cnt_o (z_fill_cnt_o)
  );

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Lockstep wrapper (#640 M6): the shipping KL_chan_map_capture beside the
//! pre-change reference, KL_chan_map_capture_ref
//! (reference/KL_chan_map_capture_ref.sv: the module of dev e8454e27,
//! byte-identical except its module name). Both take the SAME inputs every
//! cycle and every output of both is a port, so sim_lockstep.cpp compares
//! them cycle by cycle. The interface did not change shape.

`default_nettype none

module chmap_lockstep_wrap #(
  parameter int unsigned N_SLOTS_P         = 4,
  parameter int unsigned N_TDM_P           = 8,
  parameter int unsigned TDM_FRAME_PAIRS_P = 4,
  parameter int unsigned GAP_CYC_P         = 24,
  parameter int unsigned N_LB_STREAMS_P    = 1,
  parameter int unsigned N_LB_CH_P         = 8
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         map_wr_en_i,
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_wr_addr_i,
  input  wire [12:0]  map_wr_data_i,
  input  wire         map_rd_en_i,
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_rd_addr_i,
  input  wire         i2s_pair_valid_i,
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,
  input  wire         tdm_pair_valid_i,
  input  wire [3:0]   tdm_pair_slot_i,
  input  wire [23:0]  tdm_l_i,
  input  wire [23:0]  tdm_r_i,
  input  wire [23:0]  tone_smp_i,
  input  wire [63:0]  lb_tdata_i,
  input  wire         lb_tvalid_i,
  input  wire         lb_tlast_i,
  input  wire [3:0]   lb_tuser_i,
  input  wire [N_LB_STREAMS_P*4-1:0] lb_wire_chans_i,
  input  wire [N_LB_STREAMS_P-1:0]   lb_flush_i,
  input  wire [N_LB_STREAMS_P-1:0]   lb_recentre_i,
  input  wire         tick_i,

  output wire [14:0]  ref_map_rd_data_o,
  output wire         ref_map_rd_valid_o,
  output wire [2*N_SLOTS_P*13-1:0] ref_map_flat_o,
  output wire         ref_pair_valid_o,
  output wire [4:0]   ref_pair_slot_o,
  output wire [23:0]  ref_pair_l_o,
  output wire [23:0]  ref_pair_r_o,
  output wire [15:0]  ref_lb_dup_cnt_o,
  output wire [15:0]  ref_lb_skip_cnt_o,
  output wire [15:0]  ref_tdm_dup_cnt_o,
  output wire [15:0]  ref_tdm_skip_cnt_o,

  output wire [14:0]  dut_map_rd_data_o,
  output wire         dut_map_rd_valid_o,
  output wire [2*N_SLOTS_P*13-1:0] dut_map_flat_o,
  output wire         dut_pair_valid_o,
  output wire [4:0]   dut_pair_slot_o,
  output wire [23:0]  dut_pair_l_o,
  output wire [23:0]  dut_pair_r_o,
  output wire [15:0]  dut_lb_dup_cnt_o,
  output wire [15:0]  dut_lb_skip_cnt_o,
  output wire [15:0]  dut_tdm_dup_cnt_o,
  output wire [15:0]  dut_tdm_skip_cnt_o
);

  KL_chan_map_capture_ref #(
    .N_SLOTS_P (N_SLOTS_P), .N_TDM_P (N_TDM_P),
    .TDM_FRAME_PAIRS_P (TDM_FRAME_PAIRS_P), .GAP_CYC_P (GAP_CYC_P),
    .N_LB_STREAMS_P (N_LB_STREAMS_P), .N_LB_CH_P (N_LB_CH_P)
  ) u_ref (
    .clk_i, .rst_n, .map_wr_en_i, .map_wr_addr_i, .map_wr_data_i,
    .map_rd_en_i, .map_rd_addr_i,
    .map_rd_data_o (ref_map_rd_data_o), .map_rd_valid_o (ref_map_rd_valid_o),
    .map_flat_o (ref_map_flat_o),
    .i2s_pair_valid_i, .i2s_l_i, .i2s_r_i,
    .tdm_pair_valid_i, .tdm_pair_slot_i, .tdm_l_i, .tdm_r_i, .tone_smp_i,
    .lb_tdata_i, .lb_tvalid_i, .lb_tlast_i, .lb_tuser_i, .lb_wire_chans_i,
    .lb_flush_i, .lb_recentre_i, .tick_i,
    .pair_valid_o (ref_pair_valid_o), .pair_slot_o (ref_pair_slot_o),
    .pair_l_o (ref_pair_l_o), .pair_r_o (ref_pair_r_o),
    .lb_dup_cnt_o (ref_lb_dup_cnt_o), .lb_skip_cnt_o (ref_lb_skip_cnt_o),
    .tdm_dup_cnt_o (ref_tdm_dup_cnt_o), .tdm_skip_cnt_o (ref_tdm_skip_cnt_o)
  );

  KL_chan_map_capture #(
    .N_SLOTS_P (N_SLOTS_P), .N_TDM_P (N_TDM_P),
    .TDM_FRAME_PAIRS_P (TDM_FRAME_PAIRS_P), .GAP_CYC_P (GAP_CYC_P),
    .N_LB_STREAMS_P (N_LB_STREAMS_P), .N_LB_CH_P (N_LB_CH_P)
  ) u_dut (
    .clk_i, .rst_n, .map_wr_en_i, .map_wr_addr_i, .map_wr_data_i,
    .map_rd_en_i, .map_rd_addr_i,
    .map_rd_data_o (dut_map_rd_data_o), .map_rd_valid_o (dut_map_rd_valid_o),
    .map_flat_o (dut_map_flat_o),
    .i2s_pair_valid_i, .i2s_l_i, .i2s_r_i,
    .tdm_pair_valid_i, .tdm_pair_slot_i, .tdm_l_i, .tdm_r_i, .tone_smp_i,
    .lb_tdata_i, .lb_tvalid_i, .lb_tlast_i, .lb_tuser_i, .lb_wire_chans_i,
    .lb_flush_i, .lb_recentre_i, .tick_i,
    .pair_valid_o (dut_pair_valid_o), .pair_slot_o (dut_pair_slot_o),
    .pair_l_o (dut_pair_l_o), .pair_r_o (dut_pair_r_o),
    .lb_dup_cnt_o (dut_lb_dup_cnt_o), .lb_skip_cnt_o (dut_lb_skip_cnt_o),
    .tdm_dup_cnt_o (dut_tdm_dup_cnt_o), .tdm_skip_cnt_o (dut_tdm_skip_cnt_o)
  );

endmodule

`default_nettype wire

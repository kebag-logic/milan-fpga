/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tkdiag_tb_top.sv
//  Description : Verilator TB top for KL_talker_diag_ctx - the Milan v1.2
//                Table 5.4 Stream Output diagnostic counters. Three
//                contexts (two AAF talkers + a CRF output), observation
//                interval shrunk to 64 cycles so a case sees many interval
//                boundaries in simulation time (the clause only bounds the
//                interval from above, at 1 s).
//
//                Also instantiates KL_media_clock_restart on the SAME frame
//                feed, so the mr bit the counter observes is the bit the
//                4.4.4.3 generator produced - the two are verified as one
//                chain rather than against each other's assumptions.
//---------------------------------------------------------------------------//

`default_nettype none

module tkdiag_tb_top (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire [2:0]  streaming_i,
  input  wire        frame_p_i,
  input  wire [3:0]  frame_idx_i,
  input  wire        tu_i,
  //! the mr bit the announced PDU carried (drive it directly to test the
  //! counter; mcr_* below exercise the generator that produces it in fabric)
  input  wire        frame_mr_i,
  //! media-clock restart request into the 4.4.4.3 generator
  input  wire        mcr_restart_p_i,
  //! the live media clock source: a CHANGE here is 4.4.4.3's primary trigger
  input  wire [15:0] mcr_clk_src_i,
  input  wire [1:0]  mcr_streaming_i,
  output wire [1:0]  mcr_mr_o,
  input  wire [3:0]  rd_idx_i,
  output wire [31:0] rd_start_o,
  output wire [31:0] rd_stop_o,
  output wire [31:0] rd_mreset_o,
  output wire [31:0] rd_tu_o,
  output wire [31:0] rd_ftx_o
);

  KL_talker_diag_ctx #(.N_CTX_P (3), .TICK_CYC_P (64)) u_diag (
    .clk_i (clk_i), .rst_n (rst_n),
    .streaming_i (streaming_i),
    .frame_p_i (frame_p_i), .frame_idx_i (frame_idx_i),
    .tu_i (tu_i),
    .frame_mr_i (frame_mr_i),
    .rd_idx_i (rd_idx_i),
    .rd_start_o (rd_start_o), .rd_stop_o (rd_stop_o),
    .rd_mreset_o (rd_mreset_o), .rd_tu_o (rd_tu_o), .rd_ftx_o (rd_ftx_o)
  );

  //! the 4.4.4.3 level generator on the same PDU feed. HOLD_PDU_P stays at
  //! the clause floor of 8 so the hold cases below test the shipped number.
  KL_media_clock_restart #(.N_TALKERS_P (2), .HOLD_PDU_P (8)) u_mcr (
    .clk_i (clk_i), .rst_n (rst_n),
    .restart_p_i (mcr_restart_p_i),
    .clk_src_i (mcr_clk_src_i),
    .streaming_i (mcr_streaming_i),
    .frame_p_i (frame_p_i), .frame_idx_i (frame_idx_i),
    .frame_mr_i (frame_mr_i),
    .mr_o (mcr_mr_o)
  );

endmodule

`default_nettype wire

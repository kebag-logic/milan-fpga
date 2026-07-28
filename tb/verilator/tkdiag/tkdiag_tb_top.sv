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
//---------------------------------------------------------------------------//

`default_nettype none

module tkdiag_tb_top (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire [2:0]  streaming_i,
  input  wire        frame_p_i,
  input  wire [3:0]  frame_idx_i,
  input  wire        tu_i,
  input  wire        mr_p_i,
  input  wire [3:0]  mr_idx_i,
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
    .mr_p_i (mr_p_i), .mr_idx_i (mr_idx_i),
    .rd_idx_i (rd_idx_i),
    .rd_start_o (rd_start_o), .rd_stop_o (rd_stop_o),
    .rd_mreset_o (rd_mreset_o), .rd_tu_o (rd_tu_o), .rd_ftx_o (rd_ftx_o)
  );

endmodule

`default_nettype wire

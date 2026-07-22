/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper: KL_stream_table (N=4) feeding avtp_stream_parser
//! — the milan_datapath P1 pairing (docs/NXN_ARCHITECTURE.md §1.1): table
//! authority (ACMP entry-0 alias + CSR-window overrides) + tuser stream-index
//! classification.

`default_nettype none

module stream_table_wrap #(
  parameter int unsigned N_LISTENERS_P = 4
)(
  input  wire        clk,
  input  wire        resetn,

  //! stream-0 legacy authority (ACMP bound record)
  input  wire        bound0_i,
  input  wire [63:0] sid0_i,

  //! CSR-window override port
  input  wire        wr_en_i,
  input  wire [3:0]  wr_idx_i,
  input  wire [63:0] wr_sid_i,
  input  wire        wr_valid_i,

  //! monitored RX AXI-Stream
  input  wire [63:0] s_tdata_i,
  input  wire [7:0]  s_tkeep_i,
  input  wire        s_tvalid_i,
  input  wire        s_tlast_i,

  output wire        match_valid_o,
  output wire [1:0]  match_index_o,
  output wire [63:0] stream_id_o,
  output wire        parse_valid_o,
  output wire [N_LISTENERS_P-1:0] bind_rise_o,
  output wire [N_LISTENERS_P-1:0] tbl_en_o
);

  wire [64*N_LISTENERS_P-1:0] tbl_sid_w;

  KL_stream_table #(.N_LISTENERS_P(N_LISTENERS_P)) u_tbl (
    .clk_i (clk), .rst_n (resetn),
    .bound0_i (bound0_i), .sid0_i (sid0_i),
    .wr_en_i (wr_en_i), .wr_idx_i (wr_idx_i),
    .wr_sid_i (wr_sid_i), .wr_valid_i (wr_valid_i),
    .tbl_sid_o (tbl_sid_w), .tbl_en_o (tbl_en_o),
    .bind_rise_o (bind_rise_o)
  );

  avtp_stream_parser #(
    .TDATA_WIDTH (64), .BIG_ENDIAN (0), .N_STREAMS (N_LISTENERS_P)
  ) u_par (
    .clk (clk), .resetn (resetn),
    .cfg_stream_id_i (tbl_sid_w),
    .cfg_stream_en_i (tbl_en_o),
    .s_tdata_i (s_tdata_i), .s_tkeep_i (s_tkeep_i),
    .s_tvalid_i (s_tvalid_i), .s_tready_i (1'b1), .s_tlast_i (s_tlast_i),
    .match_valid_o (match_valid_o),
    .match_index_o (match_index_o),
    .stream_id_o (stream_id_o),
    .avtp_ts_o (), .subtype_o (), .ts_valid_o (),
    .seq_num_o (), .ts_uncertain_o (), .fsh_o (), .fsh2_o (),
    .parse_valid_o (parse_valid_o), .b3_o (),
    .avtp_frames_o (), .matched_frames_o ()
  );

endmodule

`default_nettype wire

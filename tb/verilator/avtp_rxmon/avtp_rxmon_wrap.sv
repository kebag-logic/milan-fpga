/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper: avtp_stream_parser (1-entry table = the bound
//! stream) feeding KL_avtp_rx_monitor — the exact milan_datapath pairing.

`default_nettype none

module avtp_rxmon_wrap #(
  parameter int unsigned CLK_FREQ_HZ_P = 10000   //! scaled: 100 ms = 1000 cyc
)(
  input  wire        clk,
  input  wire        resetn,

  input  wire [63:0] cfg_sid_i,        //! bound stream_id (match table entry)
  input  wire        bound_i,          //! listener bound (enables the match)
  input  wire [63:0] fmt_i,            //! current STREAM_INPUT[0] format u64

  input  wire [63:0] s_tdata_i,
  input  wire [7:0]  s_tkeep_i,
  input  wire        s_tvalid_i,
  input  wire        s_tlast_i,

  output wire [31:0] cnt_media_locked_o,
  output wire [31:0] cnt_media_unlocked_o,
  output wire [31:0] cnt_stream_interrupted_o,
  output wire [31:0] cnt_seq_mismatch_o,
  output wire [31:0] cnt_ts_uncertain_o,
  output wire [31:0] cnt_unsupported_fmt_o,
  output wire [31:0] cnt_frames_rx_o,
  output wire        media_locked_o,
  output wire        dirty_p_o,
  output wire        match_o
);

  wire        match_w, tu_w;
  wire [7:0]  subtype_w, seq_w;
  wire [63:0] fsh_w;

  avtp_stream_parser #(
    .TDATA_WIDTH (64), .BIG_ENDIAN (0), .N_STREAMS (1)
  ) u_par (
    .clk (clk), .resetn (resetn),
    .cfg_stream_id_i (cfg_sid_i),
    .cfg_stream_en_i (bound_i),
    .s_tdata_i (s_tdata_i), .s_tkeep_i (s_tkeep_i),
    .s_tvalid_i (s_tvalid_i), .s_tready_i (1'b1), .s_tlast_i (s_tlast_i),
    .match_valid_o (match_w),
    .match_index_o (), .stream_id_o (), .avtp_ts_o (),
    .subtype_o (subtype_w), .ts_valid_o (),
    .seq_num_o (seq_w), .ts_uncertain_o (tu_w), .fsh_o (fsh_w),
    .avtp_frames_o (), .matched_frames_o ()
  );

  KL_avtp_rx_monitor #(.CLK_FREQ_HZ_P(CLK_FREQ_HZ_P)) u_mon (
    .clk_i (clk), .rst_n (resetn),
    .match_valid_i (match_w), .subtype_i (subtype_w), .seq_num_i (seq_w),
    .ts_uncertain_i (tu_w), .fsh_i (fsh_w),
    .bound_i (bound_i), .fmt_i (fmt_i),
    .cnt_media_locked_o (cnt_media_locked_o),
    .cnt_media_unlocked_o (cnt_media_unlocked_o),
    .cnt_stream_interrupted_o (cnt_stream_interrupted_o),
    .cnt_seq_mismatch_o (cnt_seq_mismatch_o),
    .cnt_ts_uncertain_o (cnt_ts_uncertain_o),
    .cnt_unsupported_fmt_o (cnt_unsupported_fmt_o),
    .cnt_frames_rx_o (cnt_frames_rx_o),
    .media_locked_o (media_locked_o),
    .dirty_p_o (dirty_p_o)
  );

  assign match_o = match_w;

endmodule

`default_nettype wire

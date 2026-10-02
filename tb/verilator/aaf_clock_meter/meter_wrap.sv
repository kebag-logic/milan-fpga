// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : meter_wrap.sv
  Description : KL_aaf_clock_meter beside KL_crf_rx, for the meter suite
                (#629). The meter takes the parser bundle the harness drives
                for two AAF listeners; KL_crf_rx takes the EQUIVALENT CRF
                stimulus (one CRF PDU per group of 16 AAF PDUs, carrying the
                group's PDU 0 timestamp), so the meter's rate is compared
                with the proven receiver's on the same talker clock. Both run
                at the suite's compressed clk_i (CLK_HZ_P), which only sets
                the 100 ms timeouts: every rate is timestamp arithmetic.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module meter_wrap #(
  parameter int unsigned CLK_HZ_P = 200_000
)(
  input  wire         clk_i,
  input  wire         rst_n,
  //! meter: selection and listener state
  input  wire         en_i,
  input  wire         follow_idx_i,
  input  wire [1:0]   bind_rise_i,
  input  wire [1:0]   stopped_i,
  //! meter: the parser bundle
  input  wire         match_p_i,
  input  wire         match_idx_i,
  input  wire [7:0]   subtype_i,
  input  wire         tv_i,
  input  wire         tu_i,
  input  wire         mr_i,
  input  wire [7:0]   seq_i,
  input  wire [31:0]  ts_i,
  input  wire [63:0]  fsh_i,
  output wire         locked_o,
  output wire signed [31:0] rate_o,
  output wire         rate_valid_o,
  output wire         disrupt_p_o,
  output wire         mr_toggle_p_o,
  output wire [31:0]  status_o,
  //! the equivalent CRF stream into KL_crf_rx
  input  wire         crf_p_i,
  input  wire [7:0]   crf_seq_i,
  input  wire [63:0]  crf_ts_i,
  output wire signed [31:0] crf_rate_o,
  output wire         crf_rate_valid_o
);

  KL_aaf_clock_meter #(
    .CLK_FREQ_HZ_P (CLK_HZ_P),
    .N_LISTENERS_P (2)
  ) meter (
    .clk_i, .rst_n, .en_i, .follow_idx_i, .bind_rise_i, .stopped_i,
    .match_p_i, .match_idx_i, .subtype_i, .tv_i, .tu_i, .mr_i, .seq_i,
    .ts_ns_i (ts_i), .fsh_i, .locked_o, .rate_ns_o (rate_o), .rate_valid_o,
    .disrupt_p_o, .mr_toggle_p_o, .status_o
  );

  KL_crf_rx #(.CLK_FREQ_HZ_P(CLK_HZ_P)) crf (
    .clk_i (clk_i), .rst_n (rst_n), .frame_p_i (crf_p_i),
    .subtype_i (8'd4), .seq_i (crf_seq_i), .sid_frame_i (64'd1),
    .pullbase_i (32'd48000), .type_i (8'd1),
    .fsh_i ({16'd8, 16'd96, crf_ts_i[63:32]}),
    .fsh2_i ({crf_ts_i[31:0], 32'd0}),
    .mr_i (1'b0), .tu_i (1'b0), .ptp_now_i (64'd0),
    .en_i (1'b1), .sid_i (64'd1), .stop_i (1'b0),
    .rate_o (crf_rate_o), .rate_valid_o (crf_rate_valid_o),
    .delta_o (), .pdu_count_o (), .fmt_err_o (), .seq_err_o (),
    .mr_cnt_o (), .tu_cnt_o (), .late_cnt_o (), .early_cnt_o (),
    .locked_o (), .cnt_locked_o (), .cnt_unlocked_o (), .cnt_intr_o (),
    .dirty_p_o (), .mr_toggle_p_o ()
  );

endmodule

`default_nettype wire

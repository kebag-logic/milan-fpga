/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Lockstep wrapper (#640 M6): the shipping KL_avtp_rx_monitor_ctx beside
//! the pre-change reference, KL_avtp_rx_monitor_ctx_ref
//! (reference/KL_avtp_rx_monitor_ctx_ref.sv: the module of dev e8454e27,
//! byte-identical except its module name). Both take the SAME inputs every
//! cycle; every output of both is a port, so sim_lockstep.cpp compares them
//! cycle by cycle. The GET_COUNTERS read is the one interface that changed
//! shape: the reference presents a sink's twelve counters at once
//! (ref_diag_cnt_o), the shipping module one counter named by column
//! (dut_diag_q_o). The harness compares column c of the first against the
//! second for the same sink.

`default_nettype none

module avtp_rxmon_lockstep_wrap #(
  parameter int unsigned N_LISTENERS_P = 1,
  parameter int unsigned CLK_FREQ_HZ_P = 10000,  //! 1 ms = 10 cycles
  parameter int unsigned IVAL_CYC_P    = 500     //! Table 5.6 interval
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         match_valid_i,
  input  wire [3:0]   match_index_i,
  input  wire [7:0]   subtype_i,
  input  wire [7:0]   seq_num_i,
  input  wire         ts_uncertain_i,
  input  wire         ts_valid_i,
  input  wire         media_restart_i,
  input  wire [31:0]  avtp_ts_i,
  input  wire [63:0]  fsh_i,
  input  wire [N_LISTENERS_P-1:0] bound_i,
  input  wire [N_LISTENERS_P-1:0] bind_rise_i,
  input  wire [N_LISTENERS_P-1:0] bind_fall_i,
  input  wire [63:0]  sid0_i,
  input  wire [63:0]  fmt0_i,
  input  wire [31:0]  ptp_now_i,
  input  wire [31:0]  pres_ofs_i,
  input  wire [3:0]   render_sel_i,
  input  wire         depkt_pdu_p_i,
  input  wire [3:0]   depkt_pdu_idx_i,
  input  wire         depkt_drop_p_i,
  input  wire [3:0]   depkt_drop_idx_i,
  input  wire         lctx_wr_en_i,
  input  wire [7:0]   lctx_wr_addr_i,
  input  wire [31:0]  lctx_wr_data_i,
  input  wire         lctx_rd_en_i,
  input  wire [7:0]   lctx_rd_addr_i,
  input  wire [3:0]   diag_idx_i,
  input  wire [3:0]   diag_col_i,

  //! the reference's outputs
  output wire         ref_lctx_wr_rdy_o,
  output wire [31:0]  ref_lctx_rd_data_o,
  output wire         ref_lctx_rd_valid_o,
  output wire [12*32-1:0] ref_legacy_o,   //! ML,MU,SI,SM,TU,UF,FRX,MR,LT,ET,TV,TNV
  output wire         ref_media_locked_o,
  output wire [N_LISTENERS_P-1:0] ref_dirty_p_o,
  output wire         ref_pdu_accept_p_o,
  output wire [3:0]   ref_pdu_accept_idx_o,
  output wire [7:0]   ref_wire_chans_o,
  output wire [N_LISTENERS_P*4-1:0] ref_wire_chans_all_o,
  output wire [12*32-1:0] ref_diag_cnt_o,
  output wire [31:0]  ref_last_ts_o,
  output wire [31:0]  ref_last_tsd_o,

  //! the shipping module's outputs
  output wire         dut_lctx_wr_rdy_o,
  output wire [31:0]  dut_lctx_rd_data_o,
  output wire         dut_lctx_rd_valid_o,
  output wire [12*32-1:0] dut_legacy_o,
  output wire         dut_media_locked_o,
  output wire [N_LISTENERS_P-1:0] dut_dirty_p_o,
  output wire         dut_pdu_accept_p_o,
  output wire [3:0]   dut_pdu_accept_idx_o,
  output wire [7:0]   dut_wire_chans_o,
  output wire [N_LISTENERS_P*4-1:0] dut_wire_chans_all_o,
  output wire [31:0]  dut_diag_q_o,
  output wire [31:0]  dut_last_ts_o,
  output wire [31:0]  dut_last_tsd_o
);

  KL_avtp_rx_monitor_ctx_ref #(
    .N_LISTENERS_P (N_LISTENERS_P), .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P),
    .IVAL_CYC_P (IVAL_CYC_P)
  ) u_ref (
    .clk_i, .rst_n, .match_valid_i, .match_index_i, .subtype_i, .seq_num_i,
    .ts_uncertain_i, .ts_valid_i, .media_restart_i, .avtp_ts_i, .fsh_i,
    .bound_i, .bind_rise_i, .bind_fall_i, .sid0_i, .fmt0_i, .ptp_now_i,
    .pres_ofs_i, .clk_src_i (16'd0), .servo_conv_i (1'b0), .render_sel_i,
    .depkt_pdu_p_i, .depkt_pdu_idx_i, .depkt_drop_p_i, .depkt_drop_idx_i,
    .lctx_wr_en_i, .lctx_wr_addr_i, .lctx_wr_data_i,
    .lctx_wr_rdy_o (ref_lctx_wr_rdy_o),
    .lctx_rd_en_i, .lctx_rd_addr_i,
    .lctx_rd_data_o (ref_lctx_rd_data_o),
    .lctx_rd_valid_o (ref_lctx_rd_valid_o),
    .cnt_media_locked_o       (ref_legacy_o[ 0*32 +: 32]),
    .cnt_media_unlocked_o     (ref_legacy_o[ 1*32 +: 32]),
    .cnt_stream_interrupted_o (ref_legacy_o[ 2*32 +: 32]),
    .cnt_seq_mismatch_o       (ref_legacy_o[ 3*32 +: 32]),
    .cnt_ts_uncertain_o       (ref_legacy_o[ 4*32 +: 32]),
    .cnt_unsupported_fmt_o    (ref_legacy_o[ 5*32 +: 32]),
    .cnt_frames_rx_o          (ref_legacy_o[ 6*32 +: 32]),
    .cnt_media_reset_o        (ref_legacy_o[ 7*32 +: 32]),
    .cnt_late_ts_o            (ref_legacy_o[ 8*32 +: 32]),
    .cnt_early_ts_o           (ref_legacy_o[ 9*32 +: 32]),
    .cnt_ts_valid_o           (ref_legacy_o[10*32 +: 32]),
    .cnt_ts_not_valid_o       (ref_legacy_o[11*32 +: 32]),
    .media_locked_o (ref_media_locked_o), .dirty_p_o (ref_dirty_p_o),
    .pdu_accept_p_o (ref_pdu_accept_p_o),
    .pdu_accept_idx_o (ref_pdu_accept_idx_o),
    .wire_chans_o (ref_wire_chans_o), .wire_chans_all_o (ref_wire_chans_all_o),
    .diag_idx_i, .diag_cnt_o (ref_diag_cnt_o),
    .last_ts_o (ref_last_ts_o), .last_tsd_o (ref_last_tsd_o)
  );

  KL_avtp_rx_monitor_ctx #(
    .N_LISTENERS_P (N_LISTENERS_P), .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P),
    .IVAL_CYC_P (IVAL_CYC_P)
  ) u_dut (
    .clk_i, .rst_n, .match_valid_i, .match_index_i, .subtype_i, .seq_num_i,
    .ts_uncertain_i, .ts_valid_i, .media_restart_i, .avtp_ts_i, .fsh_i,
    .bound_i, .bind_rise_i, .bind_fall_i, .sid0_i, .fmt0_i, .ptp_now_i,
    .pres_ofs_i, .clk_src_i (16'd0), .servo_conv_i (1'b0), .render_sel_i,
    .depkt_pdu_p_i, .depkt_pdu_idx_i, .depkt_drop_p_i, .depkt_drop_idx_i,
    .lctx_wr_en_i, .lctx_wr_addr_i, .lctx_wr_data_i,
    .lctx_wr_rdy_o (dut_lctx_wr_rdy_o),
    .lctx_rd_en_i, .lctx_rd_addr_i,
    .lctx_rd_data_o (dut_lctx_rd_data_o),
    .lctx_rd_valid_o (dut_lctx_rd_valid_o),
    .cnt_media_locked_o       (dut_legacy_o[ 0*32 +: 32]),
    .cnt_media_unlocked_o     (dut_legacy_o[ 1*32 +: 32]),
    .cnt_stream_interrupted_o (dut_legacy_o[ 2*32 +: 32]),
    .cnt_seq_mismatch_o       (dut_legacy_o[ 3*32 +: 32]),
    .cnt_ts_uncertain_o       (dut_legacy_o[ 4*32 +: 32]),
    .cnt_unsupported_fmt_o    (dut_legacy_o[ 5*32 +: 32]),
    .cnt_frames_rx_o          (dut_legacy_o[ 6*32 +: 32]),
    .cnt_media_reset_o        (dut_legacy_o[ 7*32 +: 32]),
    .cnt_late_ts_o            (dut_legacy_o[ 8*32 +: 32]),
    .cnt_early_ts_o           (dut_legacy_o[ 9*32 +: 32]),
    .cnt_ts_valid_o           (dut_legacy_o[10*32 +: 32]),
    .cnt_ts_not_valid_o       (dut_legacy_o[11*32 +: 32]),
    .media_locked_o (dut_media_locked_o), .dirty_p_o (dut_dirty_p_o),
    .pdu_accept_p_o (dut_pdu_accept_p_o),
    .pdu_accept_idx_o (dut_pdu_accept_idx_o),
    .wire_chans_o (dut_wire_chans_o), .wire_chans_all_o (dut_wire_chans_all_o),
    .diag_idx_i, .diag_col_i, .diag_q_o (dut_diag_q_o),
    .last_ts_o (dut_last_ts_o), .last_tsd_o (dut_last_tsd_o)
  );

endmodule

`default_nettype wire

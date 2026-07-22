/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper for the NxN lane-A RX stack (NXN_ARCHITECTURE
//! phases P1+P2+P3): KL_stream_table (N=4) -> avtp_stream_parser ->
//! KL_avtp_rx_monitor_ctx (LCTX) -> KL_aaf_rx_depacketizer (tuser tag) ->
//! KL_pcm_route (routing policy). The exact milan_datapath pairing at N=4.

`default_nettype none

module avtp_rxmon_nx_wrap #(
  parameter int unsigned N_STREAMS_P   = 4,
  parameter int unsigned CLK_FREQ_HZ_P = 10000   //! scaled: 100 ms = 1000 cyc
)(
  input  wire        clk,
  input  wire        resetn,

  //! stream-0 legacy authority (ACMP bound record)
  input  wire        bound0_i,
  input  wire [63:0] sid0_i,
  input  wire [63:0] fmt0_i,

  //! stream-table CSR-window port
  input  wire        tbl_wr_en_i,
  input  wire [3:0]  tbl_wr_idx_i,
  input  wire [63:0] tbl_wr_sid_i,
  input  wire        tbl_wr_valid_i,

  //! LCTX window port
  input  wire        lctx_wr_en_i,
  input  wire [7:0]  lctx_wr_addr_i,
  input  wire [31:0] lctx_wr_data_i,
  output wire        lctx_wr_rdy_o,
  input  wire        lctx_rd_en_i,
  input  wire [7:0]  lctx_rd_addr_i,
  output wire [31:0] lctx_rd_data_o,
  output wire        lctx_rd_valid_o,

  //! media-clock context
  input  wire [31:0] ptp_now_i,
  input  wire [31:0] pres_ofs_i,
  input  wire        media_reset_p_i,
  input  wire [15:0] clk_src_i,
  input  wire        servo_conv_i,

  //! route policy write port (P3)
  input  wire        route_wr_en_i,
  input  wire [3:0]  route_wr_idx_i,
  input  wire [1:0]  route_wr_val_i,

  //! monitored RX AXI-Stream
  input  wire [63:0] s_tdata_i,
  input  wire [7:0]  s_tkeep_i,
  input  wire        s_tvalid_i,
  input  wire        s_tlast_i,

  //! stream-0 legacy counter view (0x6B8 alias)
  output wire [31:0] cnt_media_locked_o,
  output wire [31:0] cnt_media_unlocked_o,
  output wire [31:0] cnt_stream_interrupted_o,
  output wire [31:0] cnt_seq_mismatch_o,
  output wire [31:0] cnt_ts_uncertain_o,
  output wire [31:0] cnt_unsupported_fmt_o,
  output wire [31:0] cnt_frames_rx_o,
  output wire [31:0] cnt_media_reset_o,
  output wire [31:0] cnt_late_ts_o,
  output wire [31:0] cnt_early_ts_o,
  output wire        media_locked_o,
  output wire        pdu_accept_p_o,
  output wire [3:0]  pdu_accept_idx_o,
  output wire [7:0]  wire_chans_o,
  output wire [31:0] last_ts_o,

  //! PCM ring output (post-route) + render tap
  output wire [63:0] pcm_tdata_o,
  output wire        pcm_tvalid_o,
  output wire        pcm_tlast_o,
  output wire [3:0]  pcm_tuser_o,
  input  wire        pcm_tready_i,
  output wire        render_tvalid_o,
  output wire [63:0] render_tdata_o,
  output wire        render_tlast_o,
  output wire [3:0]  render_sel_o,
  output wire [15:0] pcm_pdus_o,
  output wire [15:0] pcm_drops_o
);

  wire        match_w, tu_w;
  wire [7:0]  subtype_w, seq_w;
  wire [1:0]  midx_w;
  wire [31:0] ts_w;
  wire [63:0] fsh_w;
  wire [64*N_STREAMS_P-1:0] tbl_sid_w;
  wire [N_STREAMS_P-1:0]    tbl_en_w, bind_rise_w;

  KL_stream_table #(.N_LISTENERS_P(N_STREAMS_P)) u_tbl (
    .clk_i (clk), .rst_n (resetn),
    .bound0_i (bound0_i), .sid0_i (sid0_i),
    .wr_en_i (tbl_wr_en_i), .wr_idx_i (tbl_wr_idx_i),
    .wr_sid_i (tbl_wr_sid_i), .wr_valid_i (tbl_wr_valid_i),
    .tbl_sid_o (tbl_sid_w), .tbl_en_o (tbl_en_w),
    .bind_rise_o (bind_rise_w)
  );

  avtp_stream_parser #(
    .TDATA_WIDTH (64), .BIG_ENDIAN (0), .N_STREAMS (N_STREAMS_P)
  ) u_par (
    .clk (clk), .resetn (resetn),
    .cfg_stream_id_i (tbl_sid_w),
    .cfg_stream_en_i (tbl_en_w),
    .s_tdata_i (s_tdata_i), .s_tkeep_i (s_tkeep_i),
    .s_tvalid_i (s_tvalid_i), .s_tready_i (1'b1), .s_tlast_i (s_tlast_i),
    .match_valid_o (match_w),
    .match_index_o (midx_w), .stream_id_o (), .avtp_ts_o (ts_w),
    .subtype_o (subtype_w), .ts_valid_o (),
    .seq_num_o (seq_w), .ts_uncertain_o (tu_w), .fsh_o (fsh_w),
    .fsh2_o (), .parse_valid_o (), .b3_o (),
    .avtp_frames_o (), .matched_frames_o ()
  );

  wire        depkt_pdu_p_w, depkt_drop_p_w;
  wire [3:0]  depkt_pdu_idx_w, depkt_drop_idx_w;

  KL_avtp_rx_monitor_ctx #(
    .N_LISTENERS_P (N_STREAMS_P), .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P)
  ) u_mon (
    .clk_i (clk), .rst_n (resetn),
    .match_valid_i (match_w), .match_index_i ({2'b00, midx_w}),
    .subtype_i (subtype_w), .seq_num_i (seq_w),
    .ts_uncertain_i (tu_w), .avtp_ts_i (ts_w), .fsh_i (fsh_w),
    .bound_i (tbl_en_w), .bind_rise_i (bind_rise_w),
    .sid0_i (sid0_i), .fmt0_i (fmt0_i),
    .ptp_now_i (ptp_now_i), .pres_ofs_i (pres_ofs_i),
    .media_reset_p_i (media_reset_p_i),
    .clk_src_i (clk_src_i), .servo_conv_i (servo_conv_i),
    .render_sel_i (render_sel_o),
    .depkt_pdu_p_i (depkt_pdu_p_w), .depkt_pdu_idx_i (depkt_pdu_idx_w),
    .depkt_drop_p_i (depkt_drop_p_w), .depkt_drop_idx_i (depkt_drop_idx_w),
    .lctx_wr_en_i (lctx_wr_en_i), .lctx_wr_addr_i (lctx_wr_addr_i),
    .lctx_wr_data_i (lctx_wr_data_i), .lctx_wr_rdy_o (lctx_wr_rdy_o),
    .lctx_rd_en_i (lctx_rd_en_i), .lctx_rd_addr_i (lctx_rd_addr_i),
    .lctx_rd_data_o (lctx_rd_data_o), .lctx_rd_valid_o (lctx_rd_valid_o),
    .cnt_media_locked_o (cnt_media_locked_o),
    .cnt_media_unlocked_o (cnt_media_unlocked_o),
    .cnt_stream_interrupted_o (cnt_stream_interrupted_o),
    .cnt_seq_mismatch_o (cnt_seq_mismatch_o),
    .cnt_ts_uncertain_o (cnt_ts_uncertain_o),
    .cnt_unsupported_fmt_o (cnt_unsupported_fmt_o),
    .cnt_frames_rx_o (cnt_frames_rx_o),
    .cnt_media_reset_o (cnt_media_reset_o),
    .cnt_late_ts_o (cnt_late_ts_o),
    .cnt_early_ts_o (cnt_early_ts_o),
    .media_locked_o (media_locked_o),
    .dirty_p_o (),
    .pdu_accept_p_o (pdu_accept_p_o),
    .pdu_accept_idx_o (pdu_accept_idx_o),
    .wire_chans_o (wire_chans_o),
    .last_ts_o (last_ts_o), .last_tsd_o ()
  );

  wire [63:0] dp_tdata_w;
  wire        dp_tvalid_w, dp_tlast_w;
  wire [3:0]  dp_tuser_w;
  wire        dp_tready_w;

  KL_aaf_rx_depacketizer u_depkt (
    .clk_i (clk), .rst_n (resetn),
    .s_tdata_i (s_tdata_i), .s_tkeep_i (s_tkeep_i),
    .s_tvalid_i (s_tvalid_i), .s_tready_i (1'b1), .s_tlast_i (s_tlast_i),
    .pdu_accept_p_i (pdu_accept_p_o),
    .pdu_accept_idx_i (pdu_accept_idx_o),
    .m_axis_tdata (dp_tdata_w), .m_axis_tkeep (),
    .m_axis_tvalid (dp_tvalid_w), .m_axis_tlast (dp_tlast_w),
    .m_axis_tuser (dp_tuser_w),
    .m_axis_tready (dp_tready_w),
    .pdus_o (pcm_pdus_o), .drops_o (pcm_drops_o),
    .pdu_out_p_o (depkt_pdu_p_w), .pdu_out_idx_o (depkt_pdu_idx_w),
    .drop_p_o (depkt_drop_p_w), .drop_idx_o (depkt_drop_idx_w)
  );

  KL_pcm_route #(.N_LISTENERS_P(N_STREAMS_P)) u_route (
    .clk_i (clk), .rst_n (resetn),
    .s_tdata_i (dp_tdata_w), .s_tvalid_i (dp_tvalid_w),
    .s_tlast_i (dp_tlast_w), .s_tuser_i (dp_tuser_w),
    .s_tready_o (dp_tready_w),
    .route_wr_en_i (route_wr_en_i), .route_wr_idx_i (route_wr_idx_i),
    .route_wr_val_i (route_wr_val_i),
    .m_axis_tdata (pcm_tdata_o), .m_axis_tvalid (pcm_tvalid_o),
    .m_axis_tlast (pcm_tlast_o), .m_axis_tuser (pcm_tuser_o),
    .m_axis_tready (pcm_tready_i),
    .render_tvalid_o (render_tvalid_o), .render_tdata_o (render_tdata_o),
    .render_tlast_o (render_tlast_o),
    .render_sel_o (render_sel_o), .render_active_o ()
  );

endmodule

`default_nettype wire

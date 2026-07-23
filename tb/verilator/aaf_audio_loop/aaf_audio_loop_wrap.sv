/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness: the FULL digital audio loop - talker media half
//! (KL_aaf_packetizer, N=1, direct L/R pair injection) wired straight into
//! the listener media half (avtp_stream_parser -> KL_avtp_rx_monitor ->
//! KL_aaf_rx_depacketizer), the exact milan_datapath TX/RX pairing.
//!
//! Injected PCM pairs are packetized into IEEE-1722 AAF-PCM class-A frames,
//! the frames are format/stream-matched and accepted by the RX monitor, and
//! the depacketizer re-emits ONLY the sample payload (S32BE). The sim_main
//! drives a coherent 1 kHz tone in and proves the recovered payload is
//! bit-exact to the source (the path adds nothing) and measures its THD+N.
//! No board, no bench - this closes the "is the talker->listener AUDIO path
//! transparent?" gap that the per-block unit TBs never covered.

`default_nettype none

module aaf_audio_loop_wrap #(
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000   //! monitor silence timer
)(
  input  wire        clk,
  input  wire        rst_n,

  //! --- talker (t0) config: direct CSR-alias inputs -----------------------
  input  wire [47:0] dest_mac_i,        //! t0 stream DMAC
  input  wire [47:0] station_mac_i,     //! src MAC (stream_id high 48)
  input  wire [11:0] vlan_vid_i,        //! SR class VID
  input  wire [31:0] transit_ns_i,      //! presentation offset
  input  wire [63:0] ptp_ns_i,          //! live PHC ns
  input  wire        stream_en_i,       //! enable t0

  //! --- talker stimulus: one L/R pair per pulse ---------------------------
  input  wire        pair_valid_i,
  input  wire [23:0] pair_l_i,
  input  wire [23:0] pair_r_i,

  //! --- listener binding (AECP/ACMP state the SM would install) -----------
  input  wire [63:0] cfg_sid_i,         //! bound stream_id (= {station_mac,uid})
  input  wire        bound_i,           //! listener sink 0 bound
  input  wire [63:0] fmt_i,             //! current STREAM_INPUT[0] format u64
  input  wire [31:0] ptp_now_i,         //! PHC ns for LATE/EARLY (non-gating)
  input  wire [31:0] pres_ofs_i,        //! presentation offset ns
  input  wire        servo_conv_i,      //! playback clock converged

  //! --- recovered PCM payload out (toward the DRAM ring) ------------------
  output wire [63:0] pcm_tdata_o,
  output wire        pcm_tvalid_o,
  output wire        pcm_tlast_o,
  input  wire        pcm_tready_i,
  output wire [15:0] pcm_pdus_o,
  output wire [15:0] pcm_drops_o,
  output wire [31:0] frames_rx_o,       //! FRAMES_RX (accepted PDUs)
  output wire [31:0] unsupported_fmt_o, //! UNSUPPORTED_FORMAT (should stay 0)

  //! --- TX frame tap (visibility) -----------------------------------------
  output wire [63:0] tx_tdata_o,
  output wire [7:0]  tx_tkeep_o,
  output wire        tx_tvalid_o,
  output wire        tx_tlast_o,
  output wire [31:0] frames_sent_o
);

  // ---- talker media half: shared packetizer, N=1 --------------------------
  wire [63:0] ax_tdata;
  wire [7:0]  ax_tkeep;
  wire        ax_tvalid, ax_tlast;

  KL_aaf_packetizer #(.N_TALKERS_P(1)) u_tx (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (pair_valid_i), .pair_slot_i (4'd0),
    .pair_l_i (pair_l_i), .pair_r_i (pair_r_i),
    .stream_en_i (stream_en_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    .tctx_wr_en_i (1'b0), .tctx_wr_addr_i (7'd0), .tctx_wr_data_i (32'd0),
    .tctx_wr_rdy_o (),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (ax_tdata), .m_axis_tkeep (ax_tkeep),
    .m_axis_tvalid (ax_tvalid), .m_axis_tlast (ax_tlast),
    .m_axis_tready (1'b1),          //! RX taps never backpressure the datapath
    .frames_sent_o (frames_sent_o)
  );

  assign tx_tdata_o  = ax_tdata;
  assign tx_tkeep_o  = ax_tkeep;
  assign tx_tvalid_o = ax_tvalid;
  assign tx_tlast_o  = ax_tlast;

  // ---- listener media half: parser -> monitor -> depacketizer -------------
  wire        match_w, tu_w;
  wire [7:0]  subtype_w, seq_w;
  wire [31:0] ts_w;
  wire [63:0] fsh_w;
  wire        accept_w;

  avtp_stream_parser #(
    .TDATA_WIDTH (64), .BIG_ENDIAN (0), .N_STREAMS (1)
  ) u_par (
    .clk (clk), .resetn (rst_n),
    .cfg_stream_id_i (cfg_sid_i),
    .cfg_stream_en_i (bound_i),
    .s_tdata_i (ax_tdata), .s_tkeep_i (ax_tkeep),
    .s_tvalid_i (ax_tvalid), .s_tready_i (1'b1), .s_tlast_i (ax_tlast),
    .match_valid_o (match_w),
    .match_index_o (), .stream_id_o (), .avtp_ts_o (ts_w),
    .subtype_o (subtype_w), .ts_valid_o (),
    .seq_num_o (seq_w), .ts_uncertain_o (tu_w), .fsh_o (fsh_w),
    .avtp_frames_o (), .matched_frames_o ()
  );

  KL_avtp_rx_monitor #(.CLK_FREQ_HZ_P(CLK_FREQ_HZ_P)) u_mon (
    .clk_i (clk), .rst_n (rst_n),
    .match_valid_i (match_w), .subtype_i (subtype_w), .seq_num_i (seq_w),
    .ts_uncertain_i (tu_w), .avtp_ts_i (ts_w), .fsh_i (fsh_w),
    .bound_i (bound_i), .fmt_i (fmt_i),
    .ptp_now_i (ptp_now_i), .pres_ofs_i (pres_ofs_i),
    .media_reset_p_i (1'b0),
    .clk_src_i (16'd0), .servo_conv_i (servo_conv_i),
    .cnt_media_locked_o (), .cnt_media_unlocked_o (),
    .cnt_stream_interrupted_o (), .cnt_seq_mismatch_o (),
    .cnt_ts_uncertain_o (), .cnt_unsupported_fmt_o (unsupported_fmt_o),
    .cnt_frames_rx_o (frames_rx_o), .cnt_media_reset_o (),
    .cnt_late_ts_o (), .cnt_early_ts_o (),
    .media_locked_o (), .dirty_p_o (), .pdu_accept_p_o (accept_w),
    .last_ts_o (), .last_tsd_o ()
  );

  KL_aaf_rx_depacketizer u_depkt (
    .clk_i (clk), .rst_n (rst_n),
    .s_tdata_i (ax_tdata), .s_tkeep_i (ax_tkeep),
    .s_tvalid_i (ax_tvalid), .s_tready_i (1'b1), .s_tlast_i (ax_tlast),
    .pdu_accept_p_i (accept_w),
    .pdu_accept_idx_i (4'd0),           //! N=1 shape
    .m_axis_tdata (pcm_tdata_o), .m_axis_tkeep (),
    .m_axis_tvalid (pcm_tvalid_o), .m_axis_tlast (pcm_tlast_o),
    .m_axis_tuser (),
    .m_axis_tready (pcm_tready_i),
    .pdus_o (pcm_pdus_o), .drops_o (pcm_drops_o),
    .pdu_out_p_o (), .pdu_out_idx_o (), .drop_p_o (), .drop_idx_o ()
  );

endmodule

`default_nettype wire

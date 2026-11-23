// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//! Wire receive through mapped RAM to wire transmit, with real media blocks.
`default_nettype none
module loopback_wrap #(
  parameter int N_STREAMS_P = 8,
  parameter int INPUT_FIRST_P = 1,
  parameter int INPUT_CH_P = 63,
  parameter int LEAD_P = 1
)(
  input wire clk, //! media logic clock
  input wire rst_n, //! synchronous reset
  input wire [63:0] rx_data_i, //! incoming Ethernet beat
  input wire [7:0] rx_keep_i, //! incoming byte enables
  input wire rx_valid_i, rx_last_i, //! incoming beat and frame end
  input wire ev_i, tick_i, close_i, //! domain event, capture tick and close
  input wire [31:0] frame_ns_i, //! domain and capture frame instant
  input wire [511:0] map_i, //! committed input-map image
  input wire invalidate_i, //! committed mapping invalidation
  input wire [N_STREAMS_P-1:0] flush_i, //! bind loss
  input wire out_write_i, //! output-map edit
  input wire [2:0] out_addr_i, //! outgoing channel
  input wire [12:0] out_word_i, //! source template
  output wire pair_valid_o, //! capture result
  output wire [4:0] pair_slot_o, //! capture pair index
  output wire [23:0] pair_l_o, pair_r_o, //! capture samples
  output wire [63:0] tx_data_o, //! outgoing Ethernet beat
  output wire [7:0] tx_keep_o, //! outgoing byte enables
  output wire tx_valid_o, tx_last_o, //! outgoing beat and frame end
  output wire [15:0] pdus_o //! accepted payload frames
);
  localparam int IDXW_C = (N_STREAMS_P == 1) ? 1 : $clog2(N_STREAMS_P);
  wire [N_STREAMS_P*64-1:0] sid_w;
  wire match_w, tu_w, mr_w;
  wire [IDXW_C-1:0] match_idx_w;
  wire [7:0] subtype_w, seq_w;
  wire [31:0] ts_w;
  wire [63:0] fsh_w;
  wire [N_STREAMS_P-1:0] accept_w;
  logic [3:0] accept_idx_w;
  for (genvar i = 0; i < N_STREAMS_P; i++) begin : g_monitor
    assign sid_w[64*i +: 64] = 64'h0200_0000_0002_0000 + 64'(i);
    KL_avtp_rx_monitor #(.CLK_FREQ_HZ_P(49_152_000)) mon (
      .clk_i(clk), .rst_n(rst_n),
      .match_valid_i(match_w && 32'(match_idx_w) == i),
      .subtype_i(subtype_w), .seq_num_i(seq_w), .ts_uncertain_i(tu_w),
      .avtp_ts_i(ts_w), .fsh_i(fsh_w), .media_restart_i(mr_w),
      .bound_i(!flush_i[i]), .fmt_i(64'h0205_0220_0200_6000),
      .ptp_now_i(frame_ns_i), .pres_ofs_i(32'd2_000_000),
      .clk_src_i(16'd0), .servo_conv_i(1'b1), .pdu_accept_p_o(accept_w[i])
    );
  end
  always_comb begin : accepted_index
    accept_idx_w = '0;
    for (int i = 0; i < N_STREAMS_P; i++)
      if (accept_w[i]) accept_idx_w = 4'(i);
  end
  avtp_stream_parser #(.N_STREAMS(N_STREAMS_P)) parser (
    .clk(clk), .resetn(rst_n), .cfg_stream_id_i(sid_w), .cfg_stream_en_i('1),
    .s_tdata_i(rx_data_i), .s_tkeep_i(rx_keep_i), .s_tvalid_i(rx_valid_i),
    .s_tready_i(1'b1), .s_tlast_i(rx_last_i),
    .match_valid_o(match_w), .match_index_o(match_idx_w), .avtp_ts_o(ts_w),
    .subtype_o(subtype_w), .media_restart_o(mr_w), .seq_num_o(seq_w),
    .ts_uncertain_o(tu_w), .fsh_o(fsh_w)
  );
  wire [63:0] pcm_w;
  wire pcm_valid_w, pcm_last_w, hdr_w, hdr_tv_w;
  wire [3:0] pcm_stream_w;
  wire [31:0] hdr_ts_w;
  KL_aaf_rx_depacketizer #(.PAY_LEAD_CYC_P(16)) depacketizer (
    .clk_i(clk), .rst_n(rst_n), .s_tdata_i(rx_data_i), .s_tkeep_i(rx_keep_i),
    .s_tvalid_i(rx_valid_i), .s_tready_i(1'b1), .s_tlast_i(rx_last_i),
    .pdu_accept_p_i(|accept_w), .pdu_accept_idx_i(accept_idx_w),
    .m_axis_tdata(pcm_w), .m_axis_tvalid(pcm_valid_w), .m_axis_tlast(pcm_last_w),
    .m_axis_tuser(pcm_stream_w), .m_axis_tready(1'b1),
    .hdr_p_o(hdr_w), .hdr_ts_o(hdr_ts_w), .hdr_tv_o(hdr_tv_w), .pdus_o(pdus_o)
  );
  wire capture_w, read_w;
  wire [5:0] addr_w;
  wire [23:0] sample_w;
  wire [31:0] walk_ns_w;
  KL_render_queue #(.N_STREAMS_P(N_STREAMS_P), .N_CH_P(8),
    .IF_LEAD_P(32'(LEAD_P)), .CLK_FREQ_HZ_P(49_152_000),
    .INPUT_LOOPBACK_P(1), .INPUT_KEYS_P(64),
    .INPUT_FIRST_P(INPUT_FIRST_P), .INPUT_CH_P(INPUT_CH_P)) queue (
    .clk_i(clk), .rst_n(rst_n), .hdr_p_i(hdr_w), .hdr_ts_ns_i(hdr_ts_w), .hdr_tv_i(hdr_tv_w),
    .s_tdata_i(pcm_w), .s_tvalid_i(pcm_valid_w), .s_tlast_i(pcm_last_w), .s_tuser_i(pcm_stream_w),
    .wire_chans_i({N_STREAMS_P{4'd8}}), .ev_p_i(ev_i), .ev_ns_i(frame_ns_i), .flush_i(flush_i),
    .input_map_i(map_i), .input_invalidate_i(invalidate_i), .input_capture_i(capture_w),
    .input_read_i(read_w), .input_addr_i(addr_w), .input_capture_ns_i(walk_ns_w), .input_sample_o(sample_w)
  );
  KL_chan_map_capture #(.N_SLOTS_P(4), .N_TDM_P(2), .N_LB_STREAMS_P(1),
    .N_LB_CH_P(2), .INPUT_LOOPBACK_P(1)) capture (
    .clk_i(clk), .rst_n(rst_n), .map_wr_en_i(out_write_i), .map_wr_addr_i(out_addr_i),
    .map_wr_data_i(out_word_i), .map_rd_en_i(1'b0), .map_rd_addr_i('0),
    .i2s_pair_valid_i(1'b0), .i2s_l_i('0), .i2s_r_i('0),
    .tdm_pair_valid_i(close_i), .tdm_pair_slot_i('0), .tdm_l_i('0), .tdm_r_i('0),
    .tdm_close_ns_i(frame_ns_i), .tone_smp_i('0), .tick_i(tick_i),
    .input_capture_o(capture_w), .input_read_o(read_w), .input_addr_o(addr_w),
    .input_sample_i(sample_w), .tdm_walk_ns_o(walk_ns_w),
    .pair_valid_o(pair_valid_o), .pair_slot_o(pair_slot_o), .pair_l_o(pair_l_o), .pair_r_o(pair_r_o)
  );
  KL_aaf_packetizer #(.N_TALKERS_P(1), .WIRE_CHANS_P(8)) packetizer (
    .clk_i(clk), .rst_n(rst_n), .pair_valid_i(pair_valid_o), .pair_slot_i(pair_slot_o),
    .pair_l_i(pair_l_o), .pair_r_i(pair_r_o), .stream_en_i(1'b1),
    .dest_mac_i(48'h91e0_f000_0000), .station_mac_i(48'h0200_0000_0001),
    .vlan_vid_i(12'd2), .vlan_pcp_i(3'd3), .dom_ovr_i(1'b0), .transit_ns_i(32'd2_000_000),
    .ptp_ns_i({32'd0, walk_ns_w}), .ts_uncertain_i(1'b0), .mr_i('0),
    .tctx_wr_en_i(1'b0), .tctx_wr_addr_i('0), .tctx_wr_data_i('0),
    .tctx_rd_en_i(1'b0), .tctx_rd_addr_i('0),
    .m_axis_tdata(tx_data_o), .m_axis_tkeep(tx_keep_o), .m_axis_tvalid(tx_valid_o),
    .m_axis_tlast(tx_last_o), .m_axis_tready(1'b1)
  );
endmodule
`default_nettype wire

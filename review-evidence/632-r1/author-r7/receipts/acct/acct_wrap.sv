`default_nettype none
module acct_wrap (
  input  wire        clk_i, rst_n, clk_audio_i,
  input  wire [63:0] ptp_now_i,
  output wire        bclk_o, fsync_o,
  output wire [63:0] tdata_o,
  output wire        tvalid_o, tlast_o
);
  KL_tdm_capture_master #(.SLOTS_P(8), .WORD_BITS_P(32), .BCLK_HALF_P(1), .DATA_DELAY_P(1'b1)) u_cap (
    .clk_i(clk_i), .rst_n(rst_n), .clk_audio_i(clk_audio_i), .tdm_mclk_o(), .tdm_bclk_o(bclk_o),
    .tdm_fsync_o(fsync_o), .tdm_data_i(1'b0), .bclk_rise_o(), .bclk_fall_o(), .frame_pos_o(),
    .pair_valid_o(), .pair_slot_o(), .pair_l_o(), .pair_r_o(), .pairs_captured_o());
  KL_crf_tx u_tx (
    .clk_i(clk_i), .rst_n(rst_n), .clk_audio_i(clk_audio_i), .enable_i(1'b1),
    .sid_i(64'h1), .dest_mac_i(48'h91E0F000FE00), .station_mac_i(48'h001122334455),
    .transit_ns_i(32'd2000000), .ptp_ns_i(ptp_now_i), .ts_uncertain_i(1'b0), .mr_i(1'b0),
    .tu_last_o(), .mr_last_o(), .vlan_en_i(1'b0), .vlan_pcp_i(3'd3), .vlan_vid_i(12'd2),
    .m_axis_tdata(tdata_o), .m_axis_tkeep(), .m_axis_tvalid(tvalid_o), .m_axis_tlast(tlast_o),
    .m_axis_tready(1'b1), .tx_count_o());
endmodule
`default_nettype wire

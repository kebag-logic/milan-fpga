// Review probe (not repository code): the Arty blend shape's two capture
// interfaces, the I2S front end at merged pair 0 and the TDM8 master at pairs
// 1..4, on one audio clock and one reset, with the domain media event bound
// as milan_datapath binds it for AUDIO_IF_I2S_PAIR_P = 1.
`default_nettype none
module blend_wrap (
  input  wire        clk_i, rst_n, clk_audio_i,
  input  wire [63:0] ptp_now_i,
  output wire        i2s_lrck_o, i2s_sclk_o,
  output wire        tdm_fsync_o, tdm_bclk_o,
  output wire        pv_o,
  output wire [3:0]  slot_o,
  output wire        ev_p_o,
  output wire [63:0] ev_ns_o,
  //! the I2S-only shape's binding (AUDIO_IF_SLOTS_P = 0): the I2S pair is the
  //! frame marker, 64 bits at 64 x fs, five 512 x fs cycles of write
  output wire        i2s_ev_p_o,
  output wire [63:0] i2s_ev_ns_o
);
  import KL_media_if_latency_pkg::*;
  localparam int FRAME_PAIRS_C = 4;           // min(1 + 8/2, 4)
  localparam int CLOSE_C = close_pair(FRAME_PAIRS_C, 1);
  localparam int unsigned LAT_C = 32'(mark_lat_ns(pair_end_bits(CLOSE_C, 32, 1),
                                      64'd12_288_000, 64'd24_576_000, 64'd1, 64'd50_000_000));
  wire        i_pv; wire [23:0] i_l, i_r;
  wire        t_pv; wire [3:0] t_slot; wire [23:0] t_l, t_r;
  KL_aaf_capture_i2s u_i2s (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tone_en_i (1'b0), .tone_smp_i (24'd0),
    .i2s_mclk_o (), .i2s_sclk_o (i2s_sclk_o), .i2s_lrck_o (i2s_lrck_o), .i2s_sdout_i (1'b0),
    .pair_valid_o (i_pv), .pair_slot_o (), .pair_l_o (i_l), .pair_r_o (i_r),
    .pairs_captured_o ());
  KL_tdm_capture_master #(.SLOTS_P (8), .WORD_BITS_P (32), .BCLK_HALF_P (1), .DATA_DELAY_P (1'b1)) u_tdm (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (tdm_bclk_o), .tdm_fsync_o (tdm_fsync_o), .tdm_data_i (1'b0),
    .bclk_rise_o (), .bclk_fall_o (), .frame_pos_o (),
    .pair_valid_o (t_pv), .pair_slot_o (t_slot), .pair_l_o (t_l), .pair_r_o (t_r),
    .pairs_captured_o ());
  KL_pair_blend #(.TDM_SLOTS_P (8)) u_blend (
    .clk_i (clk_i), .rst_n (rst_n),
    .i2s_pair_valid_i (i_pv), .i2s_pair_l_i (i_l), .i2s_pair_r_i (i_r),
    .tdm_pair_valid_i (t_pv), .tdm_pair_slot_i (t_slot), .tdm_pair_l_i (t_l), .tdm_pair_r_i (t_r),
    .pair_valid_o (pv_o), .pair_slot_o (slot_o), .pair_l_o (), .pair_r_o (),
    .pairs_merged_o ());
  KL_media_domain_event #(.MARK_LAT_NS_P (LAT_C), .TIMEOUT_CYC_P (4167)) u_dom (
    .clk_i (clk_i), .rst_n (rst_n),
    .mark_i (pv_o && (32'(slot_o) == FRAME_PAIRS_C - 1)), .alt_i (1'b0),
    .ptp_ns_i (ptp_now_i), .ev_p_o (ev_p_o), .ev_ns_o (ev_ns_o), .mark_ns_o (), .live_o ());
  localparam int unsigned I2S_LAT_C = 32'(mark_lat_ns(pair_end_bits(close_pair(1, 0), 32, 1),
                                          64'd3_072_000, 64'd24_576_000, 64'd5, 64'd50_000_000));
  KL_media_domain_event #(.MARK_LAT_NS_P (I2S_LAT_C), .TIMEOUT_CYC_P (4167)) u_i2s_dom (
    .clk_i (clk_i), .rst_n (rst_n), .mark_i (i_pv), .alt_i (1'b0),
    .ptp_ns_i (ptp_now_i), .ev_p_o (i2s_ev_p_o), .ev_ns_o (i2s_ev_ns_o), .mark_ns_o (), .live_o ());
endmodule
`default_nettype wire

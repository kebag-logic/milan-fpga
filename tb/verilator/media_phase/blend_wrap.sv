// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The IN-TREE two-interface shape (#632): the Arty 4x4 and 8ch
// capture, AUDIO_IF_I2S_PAIR_P = 1. Two front ends share one clock domain,
// the stereo I2S master (KL_aaf_capture_i2s) at merged pair slot 0 and the
// TDM8 master (KL_tdm_capture_master) at slots 1..4, merged by KL_pair_blend
// and banked by the real capture crossbar (KL_chan_map_capture), whose
// frame bank and its instant are what the talkers stamp. Bound as
// milan_datapath binds them on that shape, every constant from
// KL_media_if_latency_pkg: the frames-pairs kept, the closing pair (the I2S
// pair, the last of its frame to arrive) and its marker latency (the I2S
// front end's). One audio clock drives both masters, as on the board.
`default_nettype none
module blend_wrap #(
  parameter int unsigned CLK_HZ_P = 50_000_000,
  parameter int unsigned AUD_HZ_P = 24_576_000
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire  [63:0] ptp_now_i,
  //! the pins
  output wire         i2s_sclk_o, i2s_lrck_o,
  input  wire         i2s_sdout_i,
  output wire         tdm_bclk_o, tdm_fsync_o,
  input  wire         tdm_data_i,
  //! the domain event
  output wire         ev_p_o,
  output wire  [63:0] ev_ns_o
);
  import KL_media_if_latency_pkg::*;
  localparam int unsigned FS_C       = 48_000;
  localparam int unsigned TDM_SLOTS_C = 8;
  //! milan_datapath: AIF_PAIRS_C (the I2S pair plus the TDM pairs), the
  //! crossbar's eight TDM key slots, the pairs it keeps and the one closing
  localparam int unsigned SUPPLY_C   = TDM_SLOTS_C / 2 + 1;
  localparam int unsigned CMAP_SLOTS_C = 8;
  localparam int unsigned KEPT_C     = (SUPPLY_C < CMAP_SLOTS_C / 2) ? SUPPLY_C : CMAP_SLOTS_C / 2;
  localparam int unsigned CLOSE_C    = close_slot(KEPT_C, 1);
  localparam bit          I2S_CLOSE_C = close_is_i2s(TDM_SLOTS_C, 1);
  localparam longint BIT_HZ_C = I2S_CLOSE_C ? 64'(64 * FS_C) : 64'(TDM_SLOTS_C * 32 * FS_C);
  localparam longint WR_HZ_C  = I2S_CLOSE_C ? 64'(512 * FS_C) : 64'(AUD_HZ_P);
  localparam longint WR_CYC_C = I2S_CLOSE_C ? 64'd5 : 64'd1;
  localparam int unsigned LAT_C = 32'(mark_lat_ns(
      pair_end_bits(I2S_CLOSE_C ? 0 : close_pair(KEPT_C), 32, 1),
      BIT_HZ_C, WR_HZ_C, WR_CYC_C, CLK_HZ_P));

  wire        i_pv_w;
  wire [23:0] i_l_w, i_r_w;
  wire        t_pv_w;
  wire [3:0]  t_slot_w;
  wire [23:0] t_l_w, t_r_w;
  KL_aaf_capture_i2s u_i2s (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tone_en_i (1'b0), .tone_smp_i (24'd0),
    .i2s_mclk_o (), .i2s_sclk_o (i2s_sclk_o), .i2s_lrck_o (i2s_lrck_o),
    .i2s_sdout_i (i2s_sdout_i),
    .pair_valid_o (i_pv_w), .pair_slot_o (), .pair_l_o (i_l_w), .pair_r_o (i_r_w),
    .pairs_captured_o ()
  );
  KL_tdm_capture_master #(
    .SLOTS_P (TDM_SLOTS_C), .WORD_BITS_P (32),
    .BCLK_HALF_P (32'(AUD_HZ_P / (2 * TDM_SLOTS_C * 32 * FS_C))), .DATA_DELAY_P (1'b1)
  ) u_tdm (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (tdm_bclk_o), .tdm_fsync_o (tdm_fsync_o),
    .tdm_data_i (tdm_data_i), .bclk_rise_o (), .bclk_fall_o (), .frame_pos_o (),
    .pair_valid_o (t_pv_w), .pair_slot_o (t_slot_w), .pair_l_o (t_l_w), .pair_r_o (t_r_w),
    .pairs_captured_o ()
  );
  wire        pv_w;
  wire [3:0]  slot_w;
  wire [23:0] l_w, r_w;
  KL_pair_blend #(.TDM_SLOTS_P (TDM_SLOTS_C)) u_blend (
    .clk_i (clk_i), .rst_n (rst_n),
    .i2s_pair_valid_i (i_pv_w), .i2s_pair_l_i (i_l_w), .i2s_pair_r_i (i_r_w),
    .tdm_pair_valid_i (t_pv_w), .tdm_pair_slot_i (t_slot_w),
    .tdm_pair_l_i (t_l_w), .tdm_pair_r_i (t_r_w),
    .pair_valid_o (pv_w), .pair_slot_o (slot_w), .pair_l_o (l_w), .pair_r_o (r_w),
    .pairs_merged_o ()
  );

  //! the domain's media event: the closing pair's strobe, back-dated
  wire [63:0] mark_ns_w;
  KL_media_domain_event #(
    .MARK_LAT_NS_P (LAT_C), .TIMEOUT_CYC_P (4 * (CLK_HZ_P / FS_C))
  ) u_dom (
    .clk_i (clk_i), .rst_n (rst_n),
    .mark_i (pv_w && (32'(slot_w) == CLOSE_C)), .alt_i (1'b0),
    .ptp_ns_i (ptp_now_i), .ev_p_o (ev_p_o), .ev_ns_o (ev_ns_o),
    .mark_ns_o (mark_ns_w), .live_o ()
  );

  //! the crossbar: its frame bank (tdm_frame_r) and that frame's instant
  //! (tdm_frame_ns_r) are what the walk hands the talkers (chmap_capture
  //! grades the walk carrying them together)
  KL_chan_map_capture #(
    .N_SLOTS_P (4), .N_TDM_P (CMAP_SLOTS_C),
    .TDM_FRAME_PAIRS_P (KEPT_C), .TDM_CLOSE_SLOT_P (CLOSE_C),
    .N_LB_STREAMS_P (1), .N_LB_CH_P (2)
  ) u_cmap (
    .clk_i (clk_i), .rst_n (rst_n),
    .map_wr_en_i (1'b0), .map_wr_addr_i ('0), .map_wr_data_i (13'd0),
    .map_rd_en_i (1'b0), .map_rd_addr_i ('0), .map_rd_data_o (), .map_rd_valid_o (),
    .map_flat_o (),
    .i2s_pair_valid_i (pv_w), .i2s_l_i (l_w), .i2s_r_i (r_w),
    .tdm_pair_valid_i (pv_w), .tdm_pair_slot_i (slot_w), .tdm_l_i (l_w), .tdm_r_i (r_w),
    .tdm_close_ns_i (mark_ns_w[31:0]),
    .tone_smp_i (24'd0),
    .tick_i (1'b0),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (),
    .lb_dup_cnt_o (), .lb_skip_cnt_o (), .tdm_dup_cnt_o (), .tdm_skip_cnt_o (),
    .tdm_walk_ns_o ()
  );
endmodule
`default_nettype wire

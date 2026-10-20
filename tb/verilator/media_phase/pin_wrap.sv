// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// A SYNTHETIC clock domain with two media interfaces (#632, the owner's
// multi-interface requirement): no in-tree shape frames two independent
// capture buses on one domain, so this wrapper plays the integration. Both
// are real KL_tdm_capture_master instances on the one audio clock, framing
// the same 48 kHz grid with different geometry, so their latencies differ:
//   A  TDM8 x 32 bits, bit clock 12.288 MHz, slot-0 MSB one bit after the sync
//      (data delay 1): the domain's frame-timing owner;
//   B  TDM4 x 32 bits, bit clock 6.144 MHz, slot-0 MSB on the sync edge
//      (data delay 0).
// The domain has ONE media event, A's (KL_media_domain_event), which the one
// KL_crf_tx stamps. Each interface carries its OWN constant, derived from its
// own parameters by KL_media_if_latency_pkg: its marker latency, which turns
// the strobe of its frame's last pair back into the instant that frame
// started at its pins. B's instant is what its talkers would stamp. Adding B
// added its constant and a second back-dating, never a second loop.
`default_nettype none
module pin_wrap #(
  parameter int unsigned CLK_HZ_P = 50_000_000,
  parameter int unsigned AUD_HZ_P = 24_576_000
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire  [63:0] ptp_now_i,
  output wire         a_bclk_o, a_fsync_o,
  output wire         b_bclk_o, b_fsync_o,
  //! the domain event (interface A's frame instant) and B's frame instant
  output wire         a_ev_p_o,
  output wire  [63:0] a_ns_o,
  output wire         b_ev_p_o,
  output wire  [63:0] b_ns_o,
  //! the domain's CRF output
  output wire  [63:0] crft_tdata_o,
  output wire         crft_tvalid_o,
  output wire         crft_tlast_o
);
  import KL_media_if_latency_pkg::*;
  localparam int unsigned FS_C = 48_000;
  //! interface geometry: slots, word bits, data delay, bit clock
  localparam int unsigned A_SLOTS_C = 8, A_DD_C = 1;
  localparam int unsigned B_SLOTS_C = 4, B_DD_C = 0;
  localparam longint A_BIT_HZ_C = longint'(A_SLOTS_C) * 32 * FS_C;
  localparam longint B_BIT_HZ_C = longint'(B_SLOTS_C) * 32 * FS_C;
  //! each interface's constant, from its own parameters (one clk_audio_i
  //! cycle from its last bit to its FIFO write, as KL_tdm_capture_master)
  localparam int unsigned A_LAT_C =
      32'(mark_lat_ns(FS_C, A_BIT_HZ_C, A_DD_C, AUD_HZ_P, 1, CLK_HZ_P));
  localparam int unsigned B_LAT_C =
      32'(mark_lat_ns(FS_C, B_BIT_HZ_C, B_DD_C, AUD_HZ_P, 1, CLK_HZ_P));

  wire       a_pv_w, b_pv_w;
  wire [3:0] a_slot_w, b_slot_w;
  KL_tdm_capture_master #(
    .SLOTS_P (A_SLOTS_C), .WORD_BITS_P (32),
    .BCLK_HALF_P (32'(AUD_HZ_P / (2 * A_BIT_HZ_C))), .DATA_DELAY_P (1'(A_DD_C))
  ) u_a (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (a_bclk_o), .tdm_fsync_o (a_fsync_o),
    .tdm_data_i (1'b0), .bclk_rise_o (), .bclk_fall_o (), .frame_pos_o (),
    .pair_valid_o (a_pv_w), .pair_slot_o (a_slot_w), .pair_l_o (), .pair_r_o (),
    .pairs_captured_o ()
  );
  KL_tdm_capture_master #(
    .SLOTS_P (B_SLOTS_C), .WORD_BITS_P (32),
    .BCLK_HALF_P (32'(AUD_HZ_P / (2 * B_BIT_HZ_C))), .DATA_DELAY_P (1'(B_DD_C))
  ) u_b (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .tdm_mclk_o (), .tdm_bclk_o (b_bclk_o), .tdm_fsync_o (b_fsync_o),
    .tdm_data_i (1'b0), .bclk_rise_o (), .bclk_fall_o (), .frame_pos_o (),
    .pair_valid_o (b_pv_w), .pair_slot_o (b_slot_w), .pair_l_o (), .pair_r_o (),
    .pairs_captured_o ()
  );

  //! the domain's media event: the owner's frame marker, back-dated
  KL_media_domain_event #(
    .MARK_LAT_NS_P (A_LAT_C), .TIMEOUT_CYC_P (4 * (CLK_HZ_P / FS_C))
  ) u_dom (
    .clk_i (clk_i), .rst_n (rst_n),
    .mark_i (a_pv_w && (32'(a_slot_w) == A_SLOTS_C / 2 - 1)), .alt_i (1'b0),
    .ptp_now_i (ptp_now_i), .ev_p_o (a_ev_p_o), .ev_ns_o (a_ns_o), .live_o ()
  );
  //! interface B's own frame instant: its marker, back-dated by its constant
  KL_media_domain_event #(
    .MARK_LAT_NS_P (B_LAT_C), .TIMEOUT_CYC_P (4 * (CLK_HZ_P / FS_C))
  ) u_b_time (
    .clk_i (clk_i), .rst_n (rst_n),
    .mark_i (b_pv_w && (32'(b_slot_w) == B_SLOTS_C / 2 - 1)), .alt_i (1'b0),
    .ptp_now_i (ptp_now_i), .ev_p_o (b_ev_p_o), .ev_ns_o (b_ns_o), .live_o ()
  );

  KL_crf_tx u_tx (
    .clk_i (clk_i), .rst_n (rst_n), .ev_p_i (a_ev_p_o), .ev_ns_i (a_ns_o),
    .enable_i (1'b1), .sid_i (64'h0011_2233_4455_0001),
    .dest_mac_i (48'h91E0_F000_FE00), .station_mac_i (48'h0011_2233_4455),
    .transit_ns_i (32'd2_000_000), .ts_uncertain_i (1'b0), .mr_i (1'b0),
    .tu_last_o (), .mr_last_o (), .vlan_en_i (1'b0), .vlan_pcp_i (3'd3),
    .vlan_vid_i (12'd2), .m_axis_tdata (crft_tdata_o), .m_axis_tkeep (),
    .m_axis_tvalid (crft_tvalid_o), .m_axis_tlast (crft_tlast_o),
    .m_axis_tready (1'b1), .tx_count_o ()
  );
endmodule
`default_nettype wire

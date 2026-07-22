/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper for the NxN talker lane (NXN_ARCHITECTURE
//! §2.1-§2.3, phases P4): side-by-side golden pairing - the flat
//! aaf_talker_i2s vs KL_aaf_capture_i2s + KL_aaf_packetizer(N=1) on the
//! same stimulus (byte-compare gate), plus a second packetizer at N=2 with
//! direct pair injection for the two-talker interleave checks.

`default_nettype none

module aaf_nx_wrap (
  input  wire         clk,
  input  wire         clk_audio,
  input  wire         rst_n,

  //! shared config/stimulus (the flat TB's exact drive)
  input  wire         enable_i,
  input  wire         i2s_sdout_i,
  input  wire [47:0]  dest_mac_i,
  input  wire [47:0]  station_mac_i,
  input  wire [11:0]  vlan_vid_i,
  input  wire [31:0]  transit_ns_i,
  input  wire [63:0]  ptp_ns_i,

  //! golden (flat talker) AXIS
  output wire [63:0]  g_tdata_o,
  output wire [7:0]   g_tkeep_o,
  output wire         g_tvalid_o,
  output wire         g_tlast_o,
  input  wire         g_tready_i,

  //! DUT (capture + shared packetizer, N=1) AXIS
  output wire [63:0]  d_tdata_o,
  output wire [7:0]   d_tkeep_o,
  output wire         d_tvalid_o,
  output wire         d_tlast_o,
  input  wire         d_tready_i,
  output wire [31:0]  d_frames_o,

  //! N=2 packetizer with direct pair injection (interleave checks)
  input  wire         p2_pair_valid_i,
  input  wire [3:0]   p2_pair_slot_i,
  input  wire [23:0]  p2_pair_l_i,
  input  wire [23:0]  p2_pair_r_i,
  input  wire [1:0]   p2_en_i,
  input  wire         p2_tctx_wr_en_i,
  input  wire [6:0]   p2_tctx_wr_addr_i,
  input  wire [31:0]  p2_tctx_wr_data_i,
  output wire         p2_tctx_wr_rdy_o,
  input  wire         p2_tctx_rd_en_i,
  input  wire [6:0]   p2_tctx_rd_addr_i,
  output wire [31:0]  p2_tctx_rd_data_o,
  output wire         p2_tctx_rd_valid_o,
  output wire [63:0]  p2_tdata_o,
  output wire [7:0]   p2_tkeep_o,
  output wire         p2_tvalid_o,
  output wire         p2_tlast_o,
  input  wire         p2_tready_i
);

  // ---- golden: the flat talker --------------------------------------------
  aaf_talker_i2s u_gold (
    .clk_i (clk), .rst_n (rst_n), .adv_i (1'b1),
    .clk_audio_i (clk_audio),
    .enable_i (enable_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .transit_ns_i (transit_ns_i), .vlan_vid_i (vlan_vid_i),
    .ptp_ns_i (ptp_ns_i),
    .tone_en_i (1'b0), .tone_smp_i (24'd0),
    .i2s_mclk_o (), .i2s_sclk_o (), .i2s_lrck_o (),
    .i2s_sdout_i (i2s_sdout_i),
    .m_axis_tdata (g_tdata_o), .m_axis_tkeep (g_tkeep_o),
    .m_axis_tvalid (g_tvalid_o), .m_axis_tlast (g_tlast_o),
    .m_axis_tready (g_tready_i),
    .frames_sent_o (), .pairs_captured_o ()
  );

  // ---- DUT: split front-end + shared packetizer at N=1 --------------------
  wire        c_pv_w;
  wire [3:0]  c_slot_w;
  wire [23:0] c_l_w, c_r_w;

  KL_aaf_capture_i2s u_cap (
    .clk_i (clk), .rst_n (rst_n), .clk_audio_i (clk_audio),
    .tone_en_i (1'b0), .tone_smp_i (24'd0),
    .i2s_mclk_o (), .i2s_sclk_o (), .i2s_lrck_o (),
    .i2s_sdout_i (i2s_sdout_i),
    .pair_valid_o (c_pv_w), .pair_slot_o (c_slot_w),
    .pair_l_o (c_l_w), .pair_r_o (c_r_w),
    .pairs_captured_o ()
  );

  KL_aaf_packetizer #(.N_TALKERS_P(1)) u_pkt1 (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (c_pv_w), .pair_slot_i (c_slot_w),
    .pair_l_i (c_l_w), .pair_r_i (c_r_w),
    .stream_en_i (enable_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    .tctx_wr_en_i (1'b0), .tctx_wr_addr_i (7'd0),
    .tctx_wr_data_i (32'd0), .tctx_wr_rdy_o (),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (d_tdata_o), .m_axis_tkeep (d_tkeep_o),
    .m_axis_tvalid (d_tvalid_o), .m_axis_tlast (d_tlast_o),
    .m_axis_tready (d_tready_i),
    .frames_sent_o (d_frames_o)
  );

  // ---- N=2 packetizer, direct pair injection ------------------------------
  KL_aaf_packetizer #(.N_TALKERS_P(2)) u_pkt2 (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (p2_pair_valid_i), .pair_slot_i (p2_pair_slot_i),
    .pair_l_i (p2_pair_l_i), .pair_r_i (p2_pair_r_i),
    .stream_en_i (p2_en_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    .tctx_wr_en_i (p2_tctx_wr_en_i), .tctx_wr_addr_i (p2_tctx_wr_addr_i),
    .tctx_wr_data_i (p2_tctx_wr_data_i), .tctx_wr_rdy_o (p2_tctx_wr_rdy_o),
    .tctx_rd_en_i (p2_tctx_rd_en_i), .tctx_rd_addr_i (p2_tctx_rd_addr_i),
    .tctx_rd_data_o (p2_tctx_rd_data_o), .tctx_rd_valid_o (p2_tctx_rd_valid_o),
    .m_axis_tdata (p2_tdata_o), .m_axis_tkeep (p2_tkeep_o),
    .m_axis_tvalid (p2_tvalid_o), .m_axis_tlast (p2_tlast_o),
    .m_axis_tready (p2_tready_i),
    .frames_sent_o ()
  );

endmodule

`default_nettype wire

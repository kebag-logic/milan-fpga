/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper for the per-pair-slot TX source mux
//! (KL_chan_map_capture) feeding the shared KL_aaf_packetizer. Two lanes:
//!   A: chmap(32 slots) -> packetizer(N=2, t0=2ch slot0 / t1=8ch slots1..4) -
//!      routing, mid-run remap, ZERO-source and disabled-slot (absence) tests.
//!   B: chmap(32 slots) -> packetizer(N=8, all 8ch = 32 slots) - exercises the
//!      widened pair_slot up to slot 31 (talker 7 pair 3).
//! Both chmaps share the source-pair stimulus pins; each has its own map
//! write/read port and media tick.

`default_nettype none

module chmap_wrap (
  input  wire         clk,
  input  wire         rst_n,

  //! --- shared packetizer config (t0 CSR aliases / all-stream fields) ------
  input  wire [47:0]  dest_mac_i,
  input  wire [47:0]  station_mac_i,
  input  wire [11:0]  vlan_vid_i,
  input  wire [31:0]  transit_ns_i,
  input  wire [63:0]  ptp_ns_i,

  //! --- shared source pair stimulus (latched free-running by both chmaps) --
  input  wire         i2s_pair_valid_i,
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,
  input  wire         tdm_pair_valid_i,
  input  wire [3:0]   tdm_pair_slot_i,
  input  wire [23:0]  tdm_l_i,
  input  wire [23:0]  tdm_r_i,
  input  wire         ring_pair_valid_i,
  input  wire [3:0]   ring_pair_slot_i,
  input  wire [23:0]  ring_l_i,
  input  wire [23:0]  ring_r_i,
  input  wire [23:0]  tone_smp_i,

  //! --- lane A: chmap map ports + tick -------------------------------------
  input  wire         a_map_wr_en_i,
  input  wire [4:0]   a_map_wr_addr_i,
  input  wire [7:0]   a_map_wr_data_i,
  input  wire         a_map_rd_en_i,
  input  wire [4:0]   a_map_rd_addr_i,
  output wire [7:0]   a_map_rd_data_o,
  output wire         a_map_rd_valid_o,
  input  wire         a_tick_i,

  //! --- lane A: packetizer (N=2) gate + TCTX window + AXIS -----------------
  input  wire [1:0]   a_en_i,
  input  wire         a_tctx_wr_en_i,
  input  wire [6:0]   a_tctx_wr_addr_i,
  input  wire [31:0]  a_tctx_wr_data_i,
  output wire         a_tctx_wr_rdy_o,
  input  wire         a_tctx_rd_en_i,
  input  wire [6:0]   a_tctx_rd_addr_i,
  output wire [31:0]  a_tctx_rd_data_o,
  output wire         a_tctx_rd_valid_o,
  output wire [63:0]  a_tdata_o,
  output wire [7:0]   a_tkeep_o,
  output wire         a_tvalid_o,
  output wire         a_tlast_o,
  input  wire         a_tready_i,

  //! --- lane B: chmap map ports + tick -------------------------------------
  input  wire         b_map_wr_en_i,
  input  wire [4:0]   b_map_wr_addr_i,
  input  wire [7:0]   b_map_wr_data_i,
  input  wire         b_map_rd_en_i,
  input  wire [4:0]   b_map_rd_addr_i,
  output wire [7:0]   b_map_rd_data_o,
  output wire         b_map_rd_valid_o,
  input  wire         b_tick_i,

  //! --- lane B: packetizer (N=8) gate + TCTX window + AXIS -----------------
  input  wire [7:0]   b_en_i,
  input  wire         b_tctx_wr_en_i,
  input  wire [6:0]   b_tctx_wr_addr_i,
  input  wire [31:0]  b_tctx_wr_data_i,
  output wire         b_tctx_wr_rdy_o,
  input  wire         b_tctx_rd_en_i,
  input  wire [6:0]   b_tctx_rd_addr_i,
  output wire [31:0]  b_tctx_rd_data_o,
  output wire         b_tctx_rd_valid_o,
  output wire [63:0]  b_tdata_o,
  output wire [7:0]   b_tkeep_o,
  output wire         b_tvalid_o,
  output wire         b_tlast_o,
  input  wire         b_tready_i
);

  // ====================================================================== //
  //  Lane A: chmap -> packetizer(N=2)                                       //
  // ====================================================================== //
  wire        a_pv_w;
  wire [4:0]  a_slot_w;
  wire [23:0] a_l_w, a_r_w;

  KL_chan_map_capture #(
    .N_SLOTS_P (32), .N_TDM_P (8), .N_RING_P (16), .GAP_CYC_P (24)
  ) u_chmap_a (
    .clk_i (clk), .rst_n (rst_n),
    .map_wr_en_i (a_map_wr_en_i), .map_wr_addr_i (a_map_wr_addr_i),
    .map_wr_data_i (a_map_wr_data_i),
    .map_rd_en_i (a_map_rd_en_i), .map_rd_addr_i (a_map_rd_addr_i),
    .map_rd_data_o (a_map_rd_data_o), .map_rd_valid_o (a_map_rd_valid_o),
    .i2s_pair_valid_i (i2s_pair_valid_i), .i2s_l_i (i2s_l_i), .i2s_r_i (i2s_r_i),
    .tdm_pair_valid_i (tdm_pair_valid_i), .tdm_pair_slot_i (tdm_pair_slot_i),
    .tdm_l_i (tdm_l_i), .tdm_r_i (tdm_r_i),
    .ring_pair_valid_i (ring_pair_valid_i), .ring_pair_slot_i (ring_pair_slot_i),
    .ring_l_i (ring_l_i), .ring_r_i (ring_r_i),
    .tone_smp_i (tone_smp_i),
    .tick_i (a_tick_i),
    .pair_valid_o (a_pv_w), .pair_slot_o (a_slot_w),
    .pair_l_o (a_l_w), .pair_r_o (a_r_w)
  );

  KL_aaf_packetizer #(.N_TALKERS_P(2)) u_pkt_a (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (a_pv_w), .pair_slot_i (a_slot_w),
    .pair_l_i (a_l_w), .pair_r_i (a_r_w),
    .stream_en_i (a_en_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    .tctx_wr_en_i (a_tctx_wr_en_i), .tctx_wr_addr_i (a_tctx_wr_addr_i),
    .tctx_wr_data_i (a_tctx_wr_data_i), .tctx_wr_rdy_o (a_tctx_wr_rdy_o),
    .tctx_rd_en_i (a_tctx_rd_en_i), .tctx_rd_addr_i (a_tctx_rd_addr_i),
    .tctx_rd_data_o (a_tctx_rd_data_o), .tctx_rd_valid_o (a_tctx_rd_valid_o),
    .m_axis_tdata (a_tdata_o), .m_axis_tkeep (a_tkeep_o),
    .m_axis_tvalid (a_tvalid_o), .m_axis_tlast (a_tlast_o),
    .m_axis_tready (a_tready_i),
    .frames_sent_o ()
  );

  // ====================================================================== //
  //  Lane B: chmap -> packetizer(N=8, all 8ch = 32 slots, slot 31 reach)    //
  // ====================================================================== //
  wire        b_pv_w;
  wire [4:0]  b_slot_w;
  wire [23:0] b_l_w, b_r_w;

  KL_chan_map_capture #(
    .N_SLOTS_P (32), .N_TDM_P (8), .N_RING_P (16), .GAP_CYC_P (24)
  ) u_chmap_b (
    .clk_i (clk), .rst_n (rst_n),
    .map_wr_en_i (b_map_wr_en_i), .map_wr_addr_i (b_map_wr_addr_i),
    .map_wr_data_i (b_map_wr_data_i),
    .map_rd_en_i (b_map_rd_en_i), .map_rd_addr_i (b_map_rd_addr_i),
    .map_rd_data_o (b_map_rd_data_o), .map_rd_valid_o (b_map_rd_valid_o),
    .i2s_pair_valid_i (i2s_pair_valid_i), .i2s_l_i (i2s_l_i), .i2s_r_i (i2s_r_i),
    .tdm_pair_valid_i (tdm_pair_valid_i), .tdm_pair_slot_i (tdm_pair_slot_i),
    .tdm_l_i (tdm_l_i), .tdm_r_i (tdm_r_i),
    .ring_pair_valid_i (ring_pair_valid_i), .ring_pair_slot_i (ring_pair_slot_i),
    .ring_l_i (ring_l_i), .ring_r_i (ring_r_i),
    .tone_smp_i (tone_smp_i),
    .tick_i (b_tick_i),
    .pair_valid_o (b_pv_w), .pair_slot_o (b_slot_w),
    .pair_l_o (b_l_w), .pair_r_o (b_r_w)
  );

  KL_aaf_packetizer #(.N_TALKERS_P(8)) u_pkt_b (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (b_pv_w), .pair_slot_i (b_slot_w),
    .pair_l_i (b_l_w), .pair_r_i (b_r_w),
    .stream_en_i (b_en_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    .tctx_wr_en_i (b_tctx_wr_en_i), .tctx_wr_addr_i (b_tctx_wr_addr_i),
    .tctx_wr_data_i (b_tctx_wr_data_i), .tctx_wr_rdy_o (b_tctx_wr_rdy_o),
    .tctx_rd_en_i (b_tctx_rd_en_i), .tctx_rd_addr_i (b_tctx_rd_addr_i),
    .tctx_rd_data_o (b_tctx_rd_data_o), .tctx_rd_valid_o (b_tctx_rd_valid_o),
    .m_axis_tdata (b_tdata_o), .m_axis_tkeep (b_tkeep_o),
    .m_axis_tvalid (b_tvalid_o), .m_axis_tlast (b_tlast_o),
    .m_axis_tready (b_tready_i),
    .frames_sent_o ()
  );

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Verilator harness wrapper for the item-4 TDM front-end family:
//!   * cap A: KL_tdm_capture TDM16, DATA_DELAY_P=1 - driven with the
//!     one-bclk PULSE frame sync (TI DSP / Philips-heritage delay); feeds
//!     a KL_aaf_packetizer(N=2) partitioned t0=8ch (pairs 0..3) +
//!     t1=2ch (pair 4) via the TCTX chans field.
//!   * cap B: KL_tdm_capture TDM16, DATA_DELAY_P=0 - driven with the
//!     50%-duty long frame sync (the other documented fsync mode); its
//!     pair stream is checked sample-exact against the same stimulus.
//!   * cap M: KL_tdm_capture_master TDM32 - the MASTER role (2026-07-28).
//!     Nobody drives it: it makes its own bclk/fsync from clk_tdm, which
//!     is the whole reason it exists (the slave's bclk/fsync are tied to 0
//!     on every SoC in this tree, so it yields no pairs at all and every
//!     talker built on it emits NO FRAME). The harness therefore checks the
//!     BUS IT GENERATES as well as the pairs it produces, and feeds those
//!     pairs to a second packetizer so the 8-channel PDU the AX7101's 8x8
//!     talkers advertise is proven byte-exact off a real front-end.
//!   * cap M2: the same master at SLOTS_P=8 / BCLK_HALF_P=2 - the boundary
//!     cases of both parameters (a divider > 1, and the smallest slot count
//!     the family supports).

`default_nettype none

module tdm_wrap (
  input  wire         clk,
  input  wire         clk_audio,
  input  wire         clk_tdm,
  input  wire         rst_n,

  //! TDM bus A (pulse fsync, data delay 1)
  input  wire         a_bclk_i,
  input  wire         a_fsync_i,
  input  wire         a_data_i,
  //! TDM bus B (50%-duty fsync, data delay 0)
  input  wire         b_bclk_i,
  input  wire         b_fsync_i,
  input  wire         b_data_i,
  //! TDM MASTER buses: only DATA is an input - we generate the rest
  input  wire         m_data_i,
  input  wire         m2_data_i,

  //! cap M generated bus + pair stream
  output wire         m_bclk_o,
  output wire         m_fsync_o,
  output wire         m_mclk_o,
  output wire         m_pv_o,
  output wire [3:0]   m_slot_o,
  output wire [23:0]  m_l_o,
  output wire [23:0]  m_r_o,
  output wire [31:0]  m_pairs_o,
  //! cap M2 (SLOTS_P=8, BCLK_HALF_P=2) generated bus + pair stream
  output wire         m2_bclk_o,
  output wire         m2_fsync_o,
  output wire         m2_pv_o,
  output wire [3:0]   m2_slot_o,
  output wire [23:0]  m2_l_o,
  output wire [23:0]  m2_r_o,

  //! cap A pair stream (also feeds the packetizer)
  output wire         a_pv_o,
  output wire [3:0]   a_slot_o,
  output wire [23:0]  a_l_o,
  output wire [23:0]  a_r_o,
  output wire [31:0]  a_pairs_o,
  //! cap B pair stream
  output wire         b_pv_o,
  output wire [3:0]   b_slot_o,
  output wire [23:0]  b_l_o,
  output wire [23:0]  b_r_o,

  //! packetizer config/stimulus (t0 legacy aliases + TCTX window)
  input  wire [1:0]   en_i,
  input  wire [47:0]  dest_mac_i,
  input  wire [47:0]  station_mac_i,
  input  wire [11:0]  vlan_vid_i,
  input  wire [31:0]  transit_ns_i,
  input  wire [63:0]  ptp_ns_i,
  input  wire         tctx_wr_en_i,
  input  wire [6:0]   tctx_wr_addr_i,
  input  wire [31:0]  tctx_wr_data_i,
  output wire         tctx_wr_rdy_o,

  //! AAF frames out
  output wire [63:0]  m_tdata_o,
  output wire [7:0]   m_tkeep_o,
  output wire         m_tvalid_o,
  output wire         m_tlast_o,
  input  wire         m_tready_i,

  //! MASTER-fed packetizer (one 8-channel talker on pairs 0..3)
  input  wire         mp_en_i,
  input  wire [47:0]  mp_dest_mac_i,
  output wire [63:0]  mp_tdata_o,
  output wire [7:0]   mp_tkeep_o,
  output wire         mp_tvalid_o,
  output wire         mp_tlast_o,
  input  wire         mp_tready_i
);

  KL_tdm_capture #(
    .SLOTS_P (16), .WORD_BITS_P (32), .DATA_DELAY_P (1'b1)
  ) u_cap_a (
    .clk_i (clk), .rst_n (rst_n), .clk_audio_i (clk_audio),
    .tdm_mclk_o (), .tdm_bclk_i (a_bclk_i),
    .tdm_fsync_i (a_fsync_i), .tdm_data_i (a_data_i),
    .pair_valid_o (a_pv_o), .pair_slot_o (a_slot_o),
    .pair_l_o (a_l_o), .pair_r_o (a_r_o),
    .pairs_captured_o (a_pairs_o)
  );

  KL_tdm_capture #(
    .SLOTS_P (16), .WORD_BITS_P (32), .DATA_DELAY_P (1'b0)
  ) u_cap_b (
    .clk_i (clk), .rst_n (rst_n), .clk_audio_i (clk_audio),
    .tdm_mclk_o (), .tdm_bclk_i (b_bclk_i),
    .tdm_fsync_i (b_fsync_i), .tdm_data_i (b_data_i),
    .pair_valid_o (b_pv_o), .pair_slot_o (b_slot_o),
    .pair_l_o (b_l_o), .pair_r_o (b_r_o),
    .pairs_captured_o ()
  );

  //! ---- cap M: the MASTER, TDM32 x 32-bit slots, BCLK_HALF_P = 1 --------
  //! the shipping AX7101 8x8 shape: 32 slots = 16 pairs, so four 8-channel
  //! talkers (4 pair slots each) can be fully backed. bclk = clk_tdm/2.
  KL_tdm_capture_master #(
    .SLOTS_P (32), .WORD_BITS_P (32), .BCLK_HALF_P (1), .DATA_DELAY_P (1'b1)
  ) u_cap_m (
    .clk_i (clk), .rst_n (rst_n), .clk_audio_i (clk_tdm),
    .tdm_mclk_o (m_mclk_o), .tdm_bclk_o (m_bclk_o),
    .tdm_fsync_o (m_fsync_o), .tdm_data_i (m_data_i),
    .pair_valid_o (m_pv_o), .pair_slot_o (m_slot_o),
    .pair_l_o (m_l_o), .pair_r_o (m_r_o),
    .pairs_captured_o (m_pairs_o)
  );

  //! ---- cap M2: BOUNDARY of both parameters - the smallest slot count the
  //! family supports (8) and a divider > 1 (BCLK_HALF_P = 2). Same clk_tdm,
  //! so its bclk is clk_tdm/4 and its frame is 8*32 = 256 bclks.
  KL_tdm_capture_master #(
    .SLOTS_P (8), .WORD_BITS_P (32), .BCLK_HALF_P (2), .DATA_DELAY_P (1'b1)
  ) u_cap_m2 (
    .clk_i (clk), .rst_n (rst_n), .clk_audio_i (clk_tdm),
    .tdm_mclk_o (), .tdm_bclk_o (m2_bclk_o),
    .tdm_fsync_o (m2_fsync_o), .tdm_data_i (m2_data_i),
    .pair_valid_o (m2_pv_o), .pair_slot_o (m2_slot_o),
    .pair_l_o (m2_l_o), .pair_r_o (m2_r_o),
    .pairs_captured_o ()
  );

  //! the master's pairs into a packetizer: THE END-TO-END CLAIM of this lane
  //! is that an 8-channel AAF PDU comes off a front-end nobody drives, so
  //! prove it here and not only at the pair boundary. Defaults = 2ch, so the
  //! WIRE_CHANS_P override is what milan_datapath's TALKER_WIRE_CHANS_P does.
  KL_aaf_packetizer #(.N_TALKERS_P(1), .WIRE_CHANS_P(8)) u_pkt_m (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (m_pv_o), .pair_slot_i (m_slot_o),
    .pair_l_i (m_l_o), .pair_r_i (m_r_o),
    .stream_en_i (mp_en_i),
    .dest_mac_i (mp_dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i), .ts_uncertain_i (1'b0),
    .tctx_wr_en_i (1'b0), .tctx_wr_addr_i (7'd0),
    .tctx_wr_data_i (32'd0), .tctx_wr_rdy_o (),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (mp_tdata_o), .m_axis_tkeep (mp_tkeep_o),
    .m_axis_tvalid (mp_tvalid_o), .m_axis_tlast (mp_tlast_o),
    .m_axis_tready (mp_tready_i),
    .frames_sent_o ()
  );

  KL_aaf_packetizer #(.N_TALKERS_P(2)) u_pkt (
    .clk_i (clk), .rst_n (rst_n),
    .pair_valid_i (a_pv_o), .pair_slot_i (a_slot_o),
    .pair_l_i (a_l_o), .pair_r_i (a_r_o),
    .stream_en_i (en_i),
    .dest_mac_i (dest_mac_i), .station_mac_i (station_mac_i),
    .vlan_vid_i (vlan_vid_i), .transit_ns_i (transit_ns_i),
    .ptp_ns_i (ptp_ns_i),
    //! tu: this harness is not about clock validity - the honest
    //! synchronised case, and the pre-2026-07-27 wire bytes
    .ts_uncertain_i (1'b0),
    .tctx_wr_en_i (tctx_wr_en_i), .tctx_wr_addr_i (tctx_wr_addr_i),
    .tctx_wr_data_i (tctx_wr_data_i), .tctx_wr_rdy_o (tctx_wr_rdy_o),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (m_tdata_o), .m_axis_tkeep (m_tkeep_o),
    .m_axis_tvalid (m_tvalid_o), .m_axis_tlast (m_tlast_o),
    .m_axis_tready (m_tready_i),
    .frames_sent_o ()
  );

endmodule

`default_nettype wire

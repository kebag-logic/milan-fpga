// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Several AAF outputs and the CRF output of one clock domain, each with its
// own presentation offset (#632), bound as milan_datapath binds
// them: the per-STREAM_OUTPUT rows go through KL_mtt_round, whose applied
// rows the talkers stamp (the low 32 bits) and the CRF output stamps (all 33,
// KL_crf_tx ROUND_MTT_P = 0), and whose readback GET_STREAM_INFO serves. The
// factory rows sit at the 2^32 boundary, so reset loads a carry. The domain's
// frame grid comes from the harness: an event per frame with its instant,
// the time base of the pairs injected after it, as the capture walk hands
// the talkers a frame and its instant together.
`default_nettype none
module ofs_wrap #(
  parameter int unsigned N_AAF_P = 4,
  //! the factory rows (sim_ofs.cpp's kReset): talkers 2,000,000 / 2,010,000
  //! / 4,294,958,333 (the largest rounding under 2^32) / 4,294,958,334 (the
  //! first past it), the CRF output 0xFFFFFFFF
  parameter logic [(N_AAF_P+1)*32-1:0] RESET_NS_P =
    {32'hFFFF_FFFF, 32'd4_294_958_334, 32'd4_294_958_333, 32'd2_010_000, 32'd2_000_000}
)(
  input  wire                      clk_i,
  input  wire                      rst_n,
  //! the rows as set: AAF talkers 0..N_AAF_P-1, then the CRF output
  input  wire [(N_AAF_P+1)*32-1:0] raw_ns_i,
  //! the rows as applied: the low 32 bits of each, and each one's bit 32
  output wire [(N_AAF_P+1)*32-1:0] applied_ns_o,
  output wire [N_AAF_P:0]          applied_c_o,
  //! GET_STREAM_INFO's readback of row rb_row_i
  input  wire [2:0]                rb_row_i,
  output wire [31:0]               rb_ns_o,

  //! the domain's frame grid: one event per frame and its instant
  input  wire                      ev_p_i,
  input  wire  [63:0]              ev_ns_i,
  //! the talkers' pairs and time base (the instant of the frame they carry)
  input  wire                      pair_valid_i,
  input  wire  [4:0]               pair_slot_i,
  input  wire  [63:0]              tbase_ns_i,
  input  wire                      tctx_wr_en_i,
  input  wire  [6:0]               tctx_wr_addr_i,
  input  wire  [31:0]              tctx_wr_data_i,
  output wire                      tctx_wr_rdy_o,

  output wire  [63:0]              aaf_tdata_o,
  output wire  [7:0]               aaf_tkeep_o,
  output wire                      aaf_tvalid_o,
  output wire                      aaf_tlast_o,
  output wire  [63:0]              crf_tdata_o,
  output wire                      crf_tvalid_o,
  output wire                      crf_tlast_o
);
  KL_mtt_round #(
    .N_P        (N_AAF_P + 1),
    .BASE_HZ_P  (48000),
    .RESET_NS_P (RESET_NS_P)
  ) u_round (
    .clk_i (clk_i), .rst_n (rst_n),
    .raw_ns_i (raw_ns_i), .ofs_ns_o (applied_ns_o), .ofs_c_o (applied_c_o),
    .rb_row_i (rb_row_i), .rb_ns_o (rb_ns_o)
  );

  KL_aaf_packetizer #(.N_TALKERS_P (N_AAF_P)) u_pkt (
    .clk_i (clk_i), .rst_n (rst_n),
    .pair_valid_i (pair_valid_i), .pair_slot_i (pair_slot_i),
    .pair_l_i (24'h123456), .pair_r_i (24'h654321),
    .stream_en_i ({N_AAF_P{1'b1}}),
    .dest_mac_i (48'h91E0_F000_FE01), .station_mac_i (48'h0011_2233_4455),
    .vlan_vid_i (12'd2), .vlan_pcp_i (3'd3), .dom_ovr_i (1'b0),
    //! each talker stamps its OWN row as applied, as milan_datapath wires it
    .transit_ns_i (applied_ns_o[N_AAF_P*32-1:0]),
    .ptp_ns_i (tbase_ns_i), .ts_uncertain_i (1'b0), .mr_i ('0),
    .tctx_wr_en_i (tctx_wr_en_i), .tctx_wr_addr_i (tctx_wr_addr_i),
    .tctx_wr_data_i (tctx_wr_data_i), .tctx_wr_rdy_o (tctx_wr_rdy_o),
    .tctx_rd_en_i (1'b0), .tctx_rd_addr_i (7'd0),
    .tctx_rd_data_o (), .tctx_rd_valid_o (),
    .m_axis_tdata (aaf_tdata_o), .m_axis_tkeep (aaf_tkeep_o),
    .m_axis_tvalid (aaf_tvalid_o), .m_axis_tlast (aaf_tlast_o),
    .m_axis_tready (1'b1),
    .frames_sent_o (), .frame_p_o (), .frame_idx_o (), .frame_tu_o (), .frame_mr_o ()
  );

  KL_crf_tx #(.ROUND_MTT_P (1'b0)) u_crf (
    .clk_i (clk_i), .rst_n (rst_n), .ev_p_i (ev_p_i), .ev_ns_i (ev_ns_i),
    .enable_i (1'b1), .sid_i (64'h0011_2233_4455_0009),
    .dest_mac_i (48'h91E0_F000_FE00), .station_mac_i (48'h0011_2233_4455),
    //! the applied row, all 33 bits, as milan_datapath wires it
    .transit_ns_i (applied_ns_o[N_AAF_P*32 +: 32]),
    .transit_c_i (applied_c_o[N_AAF_P]),
    .ts_uncertain_i (1'b0), .mr_i (1'b0),
    .tu_last_o (), .mr_last_o (), .vlan_en_i (1'b0), .vlan_pcp_i (3'd3),
    .vlan_vid_i (12'd2), .m_axis_tdata (crf_tdata_o), .m_axis_tkeep (),
    .m_axis_tvalid (crf_tvalid_o), .m_axis_tlast (crf_tlast_o),
    .m_axis_tready (1'b1), .tx_count_o ()
  );
endmodule
`default_nettype wire

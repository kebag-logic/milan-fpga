// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Several AAF outputs and the CRF output of one clock domain, each with its
// own presentation offset (#632), bound as milan_datapath binds
// them: the AAF talkers stamp their rows as set (Milan v1.2 5.4.2.9), and
// only the CRF output's row goes through KL_mtt_round, whose applied row it
// stamps (all 33 bits, KL_crf_tx ROUND_MTT_P = 0). GET_STREAM_INFO reads an
// AAF row as set and the CRF row through the rounder's readback (5.4.2.10.2).
// The CRF row's factory value sits past the 2^32 boundary, so reset loads a
// carry. The domain's frame grid comes from the harness: an event per frame
// with its instant, the time base of the pairs injected after it, as the
// capture walk hands the talkers a frame and its instant together.
`default_nettype none
module ofs_wrap #(
  parameter int unsigned N_AAF_P = 4,
  //! the CRF output's factory row (sim_ofs.cpp's kCrfReset), rounded past
  //! 2^32: the AAF rows have none here, the harness drives them as set
  parameter logic [31:0] CRF_RESET_NS_P = 32'hFFFF_FFFF
)(
  input  wire                      clk_i,
  input  wire                      rst_n,
  //! the rows as set: AAF talkers 0..N_AAF_P-1, then the CRF output
  input  wire [(N_AAF_P+1)*32-1:0] raw_ns_i,
  //! the CRF row as applied: its low 32 bits and its bit 32
  output wire [31:0]               crf_applied_ns_o,
  output wire                      crf_applied_c_o,
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
  //! the CRF row alone is rounded (milan_datapath's g_pres_crf)
  wire [31:0] crf_rb_w;
  KL_mtt_round #(
    .N_P        (1),
    .BASE_HZ_P  (48000),
    .RESET_NS_P (CRF_RESET_NS_P)
  ) u_round (
    .clk_i (clk_i), .rst_n (rst_n),
    .raw_ns_i (raw_ns_i[N_AAF_P*32 +: 32]),
    .ofs_ns_o (crf_applied_ns_o), .ofs_c_o (crf_applied_c_o),
    .rb_row_i (1'b0), .rb_ns_o (crf_rb_w)
  );
  //! GET_STREAM_INFO word 3: an AAF row as set, the CRF row as applied
  assign rb_ns_o = (32'(rb_row_i) == N_AAF_P) ? crf_rb_w
                 : (32'(rb_row_i) < N_AAF_P) ? raw_ns_i[32*rb_row_i +: 32] : 32'd0;

  KL_aaf_packetizer #(.N_TALKERS_P (N_AAF_P)) u_pkt (
    .clk_i (clk_i), .rst_n (rst_n),
    .pair_valid_i (pair_valid_i), .pair_slot_i (pair_slot_i),
    .pair_l_i (24'h123456), .pair_r_i (24'h654321),
    .stream_en_i ({N_AAF_P{1'b1}}),
    .dest_mac_i (48'h91E0_F000_FE01), .station_mac_i (48'h0011_2233_4455),
    .vlan_vid_i (12'd2), .vlan_pcp_i (3'd3), .dom_ovr_i (1'b0),
    //! each talker stamps its OWN row as set, as milan_datapath wires it
    .transit_ns_i (raw_ns_i[N_AAF_P*32-1:0]),
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
    .transit_ns_i (crf_applied_ns_o),
    .transit_c_i (crf_applied_c_o),
    .ts_uncertain_i (1'b0), .mr_i (1'b0),
    .tu_last_o (), .mr_last_o (), .vlan_en_i (1'b0), .vlan_pcp_i (3'd3),
    .vlan_vid_i (12'd2), .m_axis_tdata (crf_tdata_o), .m_axis_tkeep (),
    .m_axis_tvalid (crf_tvalid_o), .m_axis_tlast (crf_tlast_o),
    .m_axis_tready (1'b1), .tx_count_o ()
  );
endmodule
`default_nettype wire

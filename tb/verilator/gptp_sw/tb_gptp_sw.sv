// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tb_gptp_sw.sv - gPTP in firmware against modelled peers (#884, #665 F6): the fabric half of each port, as the
// split datapath builds it with GPTP_SW_EN_P, once per interface (Milan v1.2 8.3.4: one gPTP time-aware end
// station an AVB interface, so one PHC and one timestamp unit a MAC; #884's ruling of 2026-11-21, item 5). For
// each: the MAC's transmit stream (GMII, the eth clock) feeds the launch observer (KL_gptp_gmii_launch), whose
// records reach the timestamp unit (KL_gptp_tsu) in the datapath clock; the receive tap feeds both the unit and the
// split's control tap (KL_ctrl_split, GPTP_P), which hands each gPTP frame to the mailbox with its ingress stamp
// after it; the PHC (timestamp_counter) is the one both stamp with and the firmware's servo steers. sim_main.cpp
// runs the firmware over the host mailbox model, the GMII streams, the taps and the peers.
`default_nettype none
module tb_gptp_sw #(
  parameter int N_IF = 2
) (
  input  wire                 dp_clk_i, dp_rst_n,
  input  wire                 eth_clk_i, eth_rst_n,
  // each MAC's transmit stream, observed
  input  wire [N_IF-1:0]      gmii_tvalid_i,
  input  wire [N_IF*8-1:0]    gmii_tdata_i,
  // each receive tap
  input  wire [N_IF*64-1:0]   rx_tdata_i,
  input  wire [N_IF*8-1:0]    rx_tkeep_i,
  input  wire [N_IF-1:0]      rx_tvalid_i,
  input  wire [N_IF-1:0]      rx_tlast_i,
  // each PHC's controls (the CSR's PTP block, already in this clock)
  input  wire [N_IF*32-1:0]   phc_adj_i,
  input  wire [N_IF*64-1:0]   phc_offset_i,
  input  wire [N_IF-1:0]      phc_adjust_i,
  output wire [N_IF*64-1:0]   phc_ns_o,
  // each unit's egress record FIFO head, and its take
  output wire [N_IF-1:0]      ts_valid_o,
  output wire [N_IF*86-1:0]   ts_data_o,
  input  wire [N_IF-1:0]      ts_take_i,
  output wire [N_IF*16-1:0]   ts_drop_o, ts_lost_o,
  // each control tap's bytes toward the mailbox, and its drops
  output wire [N_IF-1:0]      s_rx_valid_o,
  output wire [N_IF*8-1:0]    s_rx_data_o,
  output wire [N_IF-1:0]      s_rx_last_o,
  input  wire [N_IF-1:0]      s_rx_ready_i,
  output wire [N_IF*8-1:0]    s_rx_drops_o
);
  localparam logic [31:0] INCR_C = 32'(20 << 24);   // 20 ns a tick: the 50 MHz PHC
  for (genvar i = 0; i < N_IF; i++) begin : g_if
    wire [63:0] phc_w;
    timestamp_counter u_phc (
      .clk(dp_clk_i), .resetn(dp_rst_n), .enable_i(1'b1), .incr_i(INCR_C), .adj_i(signed'(phc_adj_i[32*i +: 32])),
      .tod_wr_i(64'd0), .cmd_load_i(1'b0), .offset_i(signed'(phc_offset_i[64*i +: 64])),
      .cmd_adjust_i(phc_adjust_i[i]), .cmd_snapshot_i(1'b0), .pps_enable_i(1'b0), .pps_target_ns_i(64'd0),
      .pps_arm_i(1'b0), .timestamp_out(phc_w), .tod_snapshot_o(), .tod_snapshot_valid_o(), .pps_o(),
      .pps_target_ns_o());
    assign phc_ns_o[64*i +: 64] = phc_w;

    wire        rec_valid, rec_kind, rec_abort, seal_req, seal_ack;
    wire [11:0] rec_oidx;
    wire [3:0]  rec_gen, rec_type, seal_gen;
    wire [15:0] rec_seq;
    wire [7:0]  rec_delta;
    KL_gptp_gmii_launch u_obs (
      .eth_clk_i, .eth_rst_n, .gmii_tvalid_i(gmii_tvalid_i[i]), .gmii_tready_i(1'b1),
      .gmii_tdata_i(gmii_tdata_i[8*i +: 8]), .dp_clk_i, .dp_rst_n,
      .rec_valid_o(rec_valid), .rec_kind_o(rec_kind), .rec_oidx_o(rec_oidx), .rec_gen_o(rec_gen),
      .rec_type_o(rec_type), .rec_seq_o(rec_seq), .rec_delta_o(rec_delta), .rec_abort_o(rec_abort),
      .seal_req_i(seal_req), .seal_gen_i(seal_gen), .seal_ack_o(seal_ack), .dbg_overrun_o());

    wire [63:0] rx_stamp_w;
    wire        rx_event_w;
    KL_gptp_tsu #(.PHC_CLK_HZ_P(50_000_000)) u_tsu (
      .clk_i(dp_clk_i), .rst_n(dp_rst_n),
      .rx_tdata_i(rx_tdata_i[64*i +: 64]), .rx_tkeep_i(rx_tkeep_i[8*i +: 8]), .rx_tvalid_i(rx_tvalid_i[i]),
      .rx_tready_i(1'b1), .rx_tlast_i(rx_tlast_i[i]),
      .phc_ns_i(phc_w), .phc_en_eff_i(1'b1), .phc_incr_eff_ns_i(INCR_C), .phc_adj_eff_ns_i(signed'(phc_adj_i[32*i +: 32])),
      .phc_load_eff_i(1'b0), .phc_adjust_eff_i(phc_adjust_i[i]),
      .rec_valid_i(rec_valid), .rec_kind_i(rec_kind), .rec_oidx_i(rec_oidx), .rec_gen_i(rec_gen),
      .rec_type_i(rec_type), .rec_seq_i(rec_seq), .rec_delta_i(rec_delta), .rec_abort_i(rec_abort),
      .seal_req_o(seal_req), .seal_gen_o(seal_gen), .seal_ack_i(seal_ack),
      .rx_stamp_o(rx_stamp_w), .rx_event_o(rx_event_w),
      .ts_valid_o(ts_valid_o[i]), .ts_data_o(ts_data_o[86*i +: 86]), .ts_take_p_i(ts_take_i[i]),
      .dbg_drop_o(ts_drop_o[16*i +: 16]), .dbg_lost_o(ts_lost_o[16*i +: 16]));

    wire [63:0] tx_tdata_w;
    wire [7:0]  tx_tkeep_w;
    wire        tx_tvalid_w, tx_tlast_w, tx_ready_w;
    wire [15:0] rx_frames_w, tx_frames_w;
    KL_ctrl_split #(.TDATA_WIDTH_P(64), .GPTP_P(1'b1)) u_tap (
      .clk_i(dp_clk_i), .rst_n(dp_rst_n),
      .rx_tdata_i(rx_tdata_i[64*i +: 64]), .rx_tkeep_i(rx_tkeep_i[8*i +: 8]), .rx_tvalid_i(rx_tvalid_i[i]),
      .rx_tready_i(1'b1), .rx_tlast_i(rx_tlast_i[i]),
      .rx_stamp_i(rx_stamp_w), .rx_event_i(rx_event_w),
      .rx_valid_o(s_rx_valid_o[i]), .rx_data_o(s_rx_data_o[8*i +: 8]), .rx_last_o(s_rx_last_o[i]),
      .rx_ready_i(s_rx_ready_i[i]),
      .tx_valid_i(1'b0), .tx_data_i(8'd0), .tx_last_i(1'b0), .tx_ready_o(tx_ready_w),
      .m_axis_tx_tdata(tx_tdata_w), .m_axis_tx_tkeep(tx_tkeep_w), .m_axis_tx_tvalid(tx_tvalid_w),
      .m_axis_tx_tlast(tx_tlast_w), .m_axis_tx_tready(1'b1),
      .rx_frames_o(rx_frames_w), .rx_drops_o(s_rx_drops_o[8*i +: 8]), .tx_frames_o(tx_frames_w));
    wire unused_w = ^{tx_tdata_w, tx_tkeep_w, tx_tvalid_w, tx_tlast_w, tx_ready_w, rx_frames_w, tx_frames_w};
  end
endmodule
`default_nettype wire

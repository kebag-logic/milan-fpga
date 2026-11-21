// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tb_gptp_sw.sv - gPTP in firmware against a modelled peer (#884, #665 F6): the fabric half of one port, as the
// split datapath builds it with GPTP_SW_EN_P. The MAC's transmit stream (GMII, the eth clock) feeds the launch
// observer (KL_gptp_gmii_launch), whose records reach the timestamp unit (KL_gptp_tsu) in the datapath clock beside
// the receive tap; the PHC (timestamp_counter) is the one both stamp with and the firmware's servo steers.
// sim_main.cpp runs the firmware over the host mailbox model, the GMII stream, the tap and the peer.
`default_nettype none
module tb_gptp_sw (
  input  wire        dp_clk_i, dp_rst_n,
  input  wire        eth_clk_i, eth_rst_n,
  // the MAC's transmit stream, observed
  input  wire        gmii_tvalid_i,
  input  wire [7:0]  gmii_tdata_i,
  // the receive tap
  input  wire [63:0] rx_tdata_i,
  input  wire [7:0]  rx_tkeep_i,
  input  wire        rx_tvalid_i,
  input  wire        rx_tlast_i,
  // the PHC's controls (the CSR's PTP block, already in this clock)
  input  wire [31:0] phc_adj_i,
  input  wire [63:0] phc_offset_i,
  input  wire        phc_adjust_i,
  output wire [63:0] phc_ns_o,
  // the record FIFO head, and its take
  output wire        ts_valid_o,
  output wire [85:0] ts_data_o,
  input  wire        ts_take_i,
  output wire [15:0] ts_drop_o, ts_lost_o
);
  localparam logic [31:0] INCR_C = 32'(20 << 24);   // 20 ns a tick: the 50 MHz PHC
  wire [63:0] phc_w;
  timestamp_counter u_phc (
    .clk(dp_clk_i), .resetn(dp_rst_n), .enable_i(1'b1), .incr_i(INCR_C), .adj_i(signed'(phc_adj_i)),
    .tod_wr_i(64'd0), .cmd_load_i(1'b0), .offset_i(signed'(phc_offset_i)), .cmd_adjust_i(phc_adjust_i),
    .cmd_snapshot_i(1'b0), .pps_enable_i(1'b0), .pps_target_ns_i(64'd0), .pps_arm_i(1'b0),
    .timestamp_out(phc_w), .tod_snapshot_o(), .tod_snapshot_valid_o(), .pps_o(), .pps_target_ns_o());
  assign phc_ns_o = phc_w;

  wire        rec_valid, rec_kind, rec_abort, seal_req, seal_ack;
  wire [11:0] rec_oidx;
  wire [3:0]  rec_gen, rec_type, seal_gen;
  wire [15:0] rec_seq;
  wire [7:0]  rec_delta;
  KL_gptp_gmii_launch u_obs (
    .eth_clk_i, .eth_rst_n, .gmii_tvalid_i, .gmii_tready_i(1'b1), .gmii_tdata_i,
    .dp_clk_i, .dp_rst_n,
    .rec_valid_o(rec_valid), .rec_kind_o(rec_kind), .rec_oidx_o(rec_oidx), .rec_gen_o(rec_gen),
    .rec_type_o(rec_type), .rec_seq_o(rec_seq), .rec_delta_o(rec_delta), .rec_abort_o(rec_abort),
    .seal_req_i(seal_req), .seal_gen_i(seal_gen), .seal_ack_o(seal_ack), .dbg_overrun_o());

  KL_gptp_tsu #(.PHC_CLK_HZ_P(50_000_000)) u_tsu (
    .clk_i(dp_clk_i), .rst_n(dp_rst_n),
    .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .phc_ns_i(phc_w), .phc_en_eff_i(1'b1), .phc_incr_eff_ns_i(INCR_C), .phc_adj_eff_ns_i(signed'(phc_adj_i)),
    .phc_load_eff_i(1'b0), .phc_adjust_eff_i(phc_adjust_i),
    .rec_valid_i(rec_valid), .rec_kind_i(rec_kind), .rec_oidx_i(rec_oidx), .rec_gen_i(rec_gen),
    .rec_type_i(rec_type), .rec_seq_i(rec_seq), .rec_delta_i(rec_delta), .rec_abort_i(rec_abort),
    .seal_req_o(seal_req), .seal_gen_o(seal_gen), .seal_ack_i(seal_ack),
    .ts_valid_o, .ts_data_o, .ts_take_p_i(ts_take_i), .dbg_drop_o(ts_drop_o), .dbg_lost_o(ts_lost_o));
endmodule
`default_nettype wire

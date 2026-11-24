// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tb_gptp_tsu.sv - the timestamp unit (KL_gptp_tsu, #884) at both transmit
// shapes the fabric plane publishes a bound for: GMII 1 Gb/s with the AX7101's
// latency constants (656 ns ingress, 219 ns egress), and MII 100 Mb/s with none.
// Both share one receive tap, one PHC and one launch-record bus. The GMII unit
// feeds the split's control tap, KL_ctrl_split with its gptp trailer (GPTP_P),
// as milan_datapath wires them, so an ingress stamp is read where the mailbox
// reads it: the eight octets after its frame's bytes. sim_main.cpp drives them
// and reads each unit's egress record FIFO and the tap's bytes.
`default_nettype none
module tb_gptp_tsu (
  input  wire        clk_i,
  input  wire        rst_n,
  input  wire [63:0] rx_tdata_i,
  input  wire [7:0]  rx_tkeep_i,
  input  wire        rx_tvalid_i,
  input  wire        rx_tlast_i,
  input  wire [63:0] phc_ns_i,
  input  wire        phc_en_i,
  input  wire [31:0] phc_incr_i,
  input  wire [31:0] phc_adj_i,
  input  wire        phc_load_i,
  input  wire        phc_adjust_i,
  input  wire        rec_valid_i,
  input  wire        rec_kind_i,
  input  wire [3:0]  rec_gen_i,
  input  wire [3:0]  rec_type_i,
  input  wire [15:0] rec_seq_i,
  input  wire [7:0]  rec_delta_g_i,   //! the cycle distance the GMII unit sees
  input  wire [7:0]  rec_delta_m_i,   //! ...and the MII unit
  input  wire        rec_abort_i,
  output wire        g_seal_req_o, m_seal_req_o,
  output wire [3:0]  g_seal_gen_o, m_seal_gen_o,
  output wire        g_ts_valid_o, m_ts_valid_o,
  output wire [85:0] g_ts_data_o, m_ts_data_o,
  input  wire        g_ts_take_i, m_ts_take_i,
  output wire [15:0] g_drop_o, g_lost_o, m_drop_o, m_lost_o,
  //! the MII unit's ingress stamp, read at a frame's last beat
  output wire [63:0] m_rx_stamp_o,
  output wire        m_rx_event_o,
  //! the control tap's bytes toward the mailbox, and its counters
  output wire        s_rx_valid_o,
  output wire [7:0]  s_rx_data_o,
  output wire        s_rx_last_o,
  input  wire        s_rx_ready_i,
  output wire [15:0] s_rx_frames_o,
  output wire [7:0]  s_rx_drops_o
);
  wire [63:0] g_rx_stamp_w;
  wire        g_rx_event_w;
  KL_gptp_tsu #(.ETH_TICK_NS_P(8), .ETH_CYC_PER_OCTET_P(1), .TXTS_DELTA_EXP_P(45), .DP_TICK_NS_P(20),
                .PHC_CLK_HZ_P(50_000_000), .INGRESS_LAT_NS_P(656), .EGRESS_LAT_NS_P(219)) u_g (
    .clk_i, .rst_n, .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .phc_ns_i, .phc_en_eff_i(phc_en_i), .phc_incr_eff_ns_i(phc_incr_i), .phc_adj_eff_ns_i(signed'(phc_adj_i)),
    .phc_load_eff_i(phc_load_i), .phc_adjust_eff_i(phc_adjust_i),
    .rec_valid_i, .rec_kind_i, .rec_oidx_i(12'd0), .rec_gen_i, .rec_type_i, .rec_seq_i, .rec_delta_i(rec_delta_g_i),
    .rec_abort_i, .seal_req_o(g_seal_req_o), .seal_gen_o(g_seal_gen_o), .seal_ack_i(1'b0),
    .rx_stamp_o(g_rx_stamp_w), .rx_event_o(g_rx_event_w),
    .ts_valid_o(g_ts_valid_o), .ts_data_o(g_ts_data_o), .ts_take_p_i(g_ts_take_i),
    .dbg_drop_o(g_drop_o), .dbg_lost_o(g_lost_o));
  KL_gptp_tsu #(.ETH_TICK_NS_P(40), .ETH_CYC_PER_OCTET_P(2), .TXTS_DELTA_EXP_P(90), .DP_TICK_NS_P(20),
                .PHC_CLK_HZ_P(50_000_000)) u_m (
    .clk_i, .rst_n, .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .phc_ns_i, .phc_en_eff_i(phc_en_i), .phc_incr_eff_ns_i(phc_incr_i), .phc_adj_eff_ns_i(signed'(phc_adj_i)),
    .phc_load_eff_i(phc_load_i), .phc_adjust_eff_i(phc_adjust_i),
    .rec_valid_i, .rec_kind_i, .rec_oidx_i(12'd0), .rec_gen_i, .rec_type_i, .rec_seq_i, .rec_delta_i(rec_delta_m_i),
    .rec_abort_i, .seal_req_o(m_seal_req_o), .seal_gen_o(m_seal_gen_o), .seal_ack_i(1'b0),
    .rx_stamp_o(m_rx_stamp_o), .rx_event_o(m_rx_event_o),
    .ts_valid_o(m_ts_valid_o), .ts_data_o(m_ts_data_o), .ts_take_p_i(m_ts_take_i),
    .dbg_drop_o(m_drop_o), .dbg_lost_o(m_lost_o));
  //! the split's control tap, its transmit side idle
  wire [63:0] s_tx_tdata_w;
  wire [7:0]  s_tx_tkeep_w;
  wire        s_tx_tvalid_w, s_tx_tlast_w, s_tx_ready_w;
  wire [15:0] s_tx_frames_w;
  KL_ctrl_split #(.TDATA_WIDTH_P(64), .GPTP_P(1'b1)) u_s (
    .clk_i, .rst_n, .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .rx_stamp_i(g_rx_stamp_w), .rx_event_i(g_rx_event_w),
    .rx_valid_o(s_rx_valid_o), .rx_data_o(s_rx_data_o), .rx_last_o(s_rx_last_o), .rx_ready_i(s_rx_ready_i),
    .tx_valid_i(1'b0), .tx_data_i(8'd0), .tx_last_i(1'b0), .tx_ready_o(s_tx_ready_w),
    .m_axis_tx_tdata(s_tx_tdata_w), .m_axis_tx_tkeep(s_tx_tkeep_w), .m_axis_tx_tvalid(s_tx_tvalid_w),
    .m_axis_tx_tlast(s_tx_tlast_w), .m_axis_tx_tready(1'b1),
    .rx_frames_o(s_rx_frames_o), .rx_drops_o(s_rx_drops_o), .tx_frames_o(s_tx_frames_w));
  wire unused_w = ^{s_tx_tdata_w, s_tx_tkeep_w, s_tx_tvalid_w, s_tx_tlast_w, s_tx_ready_w, s_tx_frames_w};
endmodule
`default_nettype wire

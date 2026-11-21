// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tb_gptp_tsu.sv - the timestamp unit (KL_gptp_tsu, #884) at both transmit
// shapes the fabric plane publishes a bound for: GMII 1 Gb/s with the AX7101's
// latency constants (656 ns ingress, 219 ns egress), and MII 100 Mb/s with none.
// Both share one receive tap, one PHC and one launch-record bus; sim_main.cpp
// drives them and reads each unit's record FIFO.
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
  output wire [15:0] g_drop_o, g_lost_o, m_drop_o, m_lost_o
);
  KL_gptp_tsu #(.ETH_TICK_NS_P(8), .ETH_CYC_PER_OCTET_P(1), .TXTS_DELTA_EXP_P(45), .DP_TICK_NS_P(20),
                .PHC_CLK_HZ_P(50_000_000), .INGRESS_LAT_NS_P(656), .EGRESS_LAT_NS_P(219)) u_g (
    .clk_i, .rst_n, .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .phc_ns_i, .phc_en_eff_i(phc_en_i), .phc_incr_eff_ns_i(phc_incr_i), .phc_adj_eff_ns_i(signed'(phc_adj_i)),
    .phc_load_eff_i(phc_load_i), .phc_adjust_eff_i(phc_adjust_i),
    .rec_valid_i, .rec_kind_i, .rec_oidx_i(12'd0), .rec_gen_i, .rec_type_i, .rec_seq_i, .rec_delta_i(rec_delta_g_i),
    .rec_abort_i, .seal_req_o(g_seal_req_o), .seal_gen_o(g_seal_gen_o), .seal_ack_i(1'b0),
    .ts_valid_o(g_ts_valid_o), .ts_data_o(g_ts_data_o), .ts_take_p_i(g_ts_take_i),
    .dbg_drop_o(g_drop_o), .dbg_lost_o(g_lost_o));
  KL_gptp_tsu #(.ETH_TICK_NS_P(40), .ETH_CYC_PER_OCTET_P(2), .TXTS_DELTA_EXP_P(90), .DP_TICK_NS_P(20),
                .PHC_CLK_HZ_P(50_000_000)) u_m (
    .clk_i, .rst_n, .rx_tdata_i, .rx_tkeep_i, .rx_tvalid_i, .rx_tready_i(1'b1), .rx_tlast_i,
    .phc_ns_i, .phc_en_eff_i(phc_en_i), .phc_incr_eff_ns_i(phc_incr_i), .phc_adj_eff_ns_i(signed'(phc_adj_i)),
    .phc_load_eff_i(phc_load_i), .phc_adjust_eff_i(phc_adjust_i),
    .rec_valid_i, .rec_kind_i, .rec_oidx_i(12'd0), .rec_gen_i, .rec_type_i, .rec_seq_i, .rec_delta_i(rec_delta_m_i),
    .rec_abort_i, .seal_req_o(m_seal_req_o), .seal_gen_o(m_seal_gen_o), .seal_ack_i(1'b0),
    .ts_valid_o(m_ts_valid_o), .ts_data_o(m_ts_data_o), .ts_take_p_i(m_ts_take_i),
    .dbg_drop_o(m_drop_o), .dbg_lost_o(m_lost_o));
endmodule
`default_nettype wire

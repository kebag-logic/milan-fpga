// Lockstep compare: the head wrapper and the same wrapper with the arm's encoder.
`default_nettype none
module diff_top (
    input  wire         clk_i, input wire rst_n,
    input  wire         ev_valid_i, input wire ev_app_i,
    input  wire [7:0]   ev_type_i, input wire [2:0] ev_event_i, input wire [1:0] ev_fp_i,
    input  wire [271:0] ev_value_i,
    input  wire [1:0]   join_i, input wire [1:0] la_i, input wire prepare_i,
    input  wire         txreq_ready_i, input wire ser_req_i, input wire [2:0] ser_slot_i,
    input  wire         ser_ready_i,
    output logic        h_ready_o, output logic a_ready_o,
    output logic [31:0] h_vec_o, output logic [31:0] a_vec_o,
    output logic        h_txv_o, output logic [2:0] h_txs_o,
    output logic        h_done_o,
    output logic        h_serv_o, output logic h_serl_o,
    output logic [4:0]  h_st_o, output logic h_go0_o
);
  logic h_drop, h_tx, h_alloc, h_commit, h_serv, h_serl, h_done, h_latx, h_txv;
  logic a_drop, a_tx, a_alloc, a_commit, a_serv, a_serl, a_done, a_latx, a_txv;
  logic [2:0] h_txs, a_txs;
  logic [3:0] h_cm, h_cv, a_cm, a_cv;
  logic [7:0] h_serd, a_serd;
  srp_tb_wrap u_h (.clk_i, .rst_n, .enc_ev_valid_i(ev_valid_i), .enc_ev_ready_o(h_ready_o),
    .enc_ev_app_i(ev_app_i), .enc_ev_attr_type_i(ev_type_i), .enc_ev_event_i(ev_event_i),
    .enc_ev_fourpack_i(ev_fp_i), .enc_ev_value_i(ev_value_i), .enc_ev_drop_o(h_drop),
    .enc_join_tick_i(join_i), .enc_leaveall_i(la_i), .enc_la_prepare_i(prepare_i),
    .enc_la_done_o(h_done), .enc_la_tx_o(h_latx), .enc_own_mac_i(48'h0200_0000_0001),
    .enc_txreq_valid_o(h_txv), .enc_txreq_slot_o(h_txs), .enc_txreq_ready_i(txreq_ready_i),
    .enc_tx_mvrp_o(h_tx), .enc_dbg_cnt_msrp_o(h_cm), .enc_dbg_cnt_mvrp_o(h_cv),
    .dbg_alloc_gnt_o(h_alloc), .dbg_commit_o(h_commit), .ser_req_i, .ser_slot_i,
    .ser_valid_o(h_serv), .ser_data_o(h_serd), .ser_last_o(h_serl), .ser_ready_i);
  srp_tb_wrap_arm u_a (.clk_i, .rst_n, .enc_ev_valid_i(ev_valid_i), .enc_ev_ready_o(a_ready_o),
    .enc_ev_app_i(ev_app_i), .enc_ev_attr_type_i(ev_type_i), .enc_ev_event_i(ev_event_i),
    .enc_ev_fourpack_i(ev_fp_i), .enc_ev_value_i(ev_value_i), .enc_ev_drop_o(a_drop),
    .enc_join_tick_i(join_i), .enc_leaveall_i(la_i), .enc_la_prepare_i(prepare_i),
    .enc_la_done_o(a_done), .enc_la_tx_o(a_latx), .enc_own_mac_i(48'h0200_0000_0001),
    .enc_txreq_valid_o(a_txv), .enc_txreq_slot_o(a_txs), .enc_txreq_ready_i(txreq_ready_i),
    .enc_tx_mvrp_o(a_tx), .enc_dbg_cnt_msrp_o(a_cm), .enc_dbg_cnt_mvrp_o(a_cv),
    .dbg_alloc_gnt_o(a_alloc), .dbg_commit_o(a_commit), .ser_req_i, .ser_slot_i,
    .ser_valid_o(a_serv), .ser_data_o(a_serd), .ser_last_o(a_serl), .ser_ready_i);
  assign h_vec_o = {h_serd, h_cm, h_cv, h_txs, h_txv, h_drop, h_tx, h_alloc, h_commit, h_serv, h_serl, h_done, h_latx};
  assign a_vec_o = {a_serd, a_cm, a_cv, a_txs, a_txv, a_drop, a_tx, a_alloc, a_commit, a_serv, a_serl, a_done, a_latx};
  assign h_txv_o = h_txv; assign h_txs_o = h_txs; assign h_done_o = h_done;
  assign h_serv_o = h_serv; assign h_serl_o = h_serl;
  assign h_st_o = u_h.u_enc.st_r;
  assign h_go0_o = u_h.u_enc.go0_w;
endmodule

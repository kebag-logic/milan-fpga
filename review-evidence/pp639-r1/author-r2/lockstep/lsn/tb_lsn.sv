`default_nettype none
module tb_lsn import pp_pkg::*; import pp_acmp_pkg::*; #(
  parameter int unsigned N_SINKS_P = 2,
  localparam int unsigned SINK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1
) (
  input  wire clk_i, input wire rst_n,
  input  wire [63:0] entity_id_i,
  input  wire txn_valid_i,
  input  wire [PP_TXN_W_C-1:0] txn_raw_i,
  input  wire txn_acmp_i, input wire [3:0] txn_msg_i, input wire txn_eid_ours_i,
  input  wire [63:0] txn_ctlr_i, input wire [15:0] txn_uid_i, input wire [2:0] txn_slot_i,
  input  wire [4:0] txn_status_i, input wire [15:0] txn_seq_i,
  input  wire evt_tk_valid_i, input wire [1:0] evt_tk_kind_i, input wire evt_tk_failed_i,
  input  wire [15:0] evt_tk_sink_i,
  input  wire pre_valid_i, input wire [15:0] pre_sink_i, input wire [63:0] pre_talker_eid_i,
  input  wire [15:0] pre_talker_uid_i, input wire [63:0] pre_ctlr_eid_i, input wire pre_sw_i,
  input  wire pre_started_i,
  input  wire strm_set_valid_i, input wire [15:0] strm_set_sink_i, input wire strm_set_val_i,
  input  wire [31:0] now_ms_i,
  input  wire tmr_exp_valid_i, input wire [6:0] tmr_exp_slot_i, input wire [7:0] tmr_exp_owner_i,
  input  wire draw_busy_i, input wire draw_valid_i, input wire [15:0] draw_ms_i,
  input  wire [7:0] rxs_rd_data_i,
  input  wire txs_alloc_gnt_i, input wire [2:0] txs_alloc_slot_i,
  input  wire lock_held_i, input wire [63:0] lock_ctlr_i,
  output logic [(1) + (1) + (1) + (1) + (1) + (N_SINKS_P) + (1) + (1) + (7) + (8) + (32) + (1) + (3) + (2) + (10) + (1) + (1) + (2) + (1) + (1) + (3) + (11) + (1) + (8) + (1) + (11) + (1) + (3) + (1) + (64) + (48) + (12) + (1) + (1) + (64) + (1) + (1) + (1) + (1) + (SINK_W_C) + (1) + (16) + (1) + (1) + (1) + (SINK_W_C) + (384)-1:0] r_all_o,
  output logic [(1) + (1) + (1) + (1) + (1) + (N_SINKS_P) + (1) + (1) + (7) + (8) + (32) + (1) + (3) + (2) + (10) + (1) + (1) + (2) + (1) + (1) + (3) + (11) + (1) + (8) + (1) + (11) + (1) + (3) + (1) + (64) + (48) + (12) + (1) + (1) + (64) + (1) + (1) + (1) + (1) + (SINK_W_C) + (1) + (16) + (1) + (1) + (1) + (SINK_W_C) + (384)-1:0] d_all_o,
  output logic [4:0] r_xs_o, output logic [4:0] d_xs_o
);
  pp_txn_t txn_i;
  always_comb begin : txn_build
    txn_i = pp_txn_t'(txn_raw_i);
    if (txn_acmp_i) txn_i.protocol = PP_PROTO_ACMP;
    txn_i.msg_type = txn_msg_i;
    if (txn_eid_ours_i) txn_i.target_eid = entity_id_i;
    txn_i.controller_eid = txn_ctlr_i;
    txn_i.operands.unique_id = txn_uid_i;
    txn_i.rx_slot = txn_slot_i;
    txn_i.status_in = txn_status_i;
    txn_i.sequence_id = txn_seq_i;
  end
  logic [1-1:0] r_txn_ready_o;
  logic [1-1:0] r_evt_tk_ready_o;
  logic [1-1:0] r_pre_ready_o;
  logic [1-1:0] r_strm_set_ready_o;
  logic [1-1:0] r_strm_set_error_o;
  logic [N_SINKS_P-1:0] r_strm_started_o;
  logic [1-1:0] r_tmr_arm_valid_o;
  logic [1-1:0] r_tmr_arm_cancel_o;
  logic [7-1:0] r_tmr_arm_slot_o;
  logic [8-1:0] r_tmr_arm_owner_o;
  logic [32-1:0] r_tmr_arm_deadline_ms_o;
  logic [1-1:0] r_draw_req_o;
  logic [3-1:0] r_draw_kind_o;
  logic [2-1:0] r_rxs_rd_slot_o;
  logic [10-1:0] r_rxs_rd_addr_o;
  logic [1-1:0] r_rxs_rd_en_o;
  logic [1-1:0] r_rxs_free_o;
  logic [2-1:0] r_rxs_free_slot_o;
  logic [1-1:0] r_txs_alloc_req_o;
  logic [1-1:0] r_txs_oversize_o;
  logic [3-1:0] r_txs_wr_slot_o;
  logic [11-1:0] r_txs_wr_addr_o;
  logic [1-1:0] r_txs_wr_valid_o;
  logic [8-1:0] r_txs_wr_data_o;
  logic [1-1:0] r_txs_wr_commit_o;
  logic [11-1:0] r_txs_wr_len_o;
  logic [1-1:0] r_txreq_valid_o;
  logic [3-1:0] r_txreq_slot_o;
  logic [1-1:0] r_act_settle_o;
  logic [64-1:0] r_act_settle_sid_o;
  logic [48-1:0] r_act_settle_da_o;
  logic [12-1:0] r_act_settle_vlan_o;
  logic [1-1:0] r_act_teardown_o;
  logic [1-1:0] r_act_disc_arm_o;
  logic [64-1:0] r_act_disc_talker_eid_o;
  logic [1-1:0] r_act_disc_disarm_o;
  logic [1-1:0] r_act_nvm_o;
  logic [1-1:0] r_act_nvm_set_o;
  logic [1-1:0] r_act_notify_o;
  logic [SINK_W_C-1:0] r_act_sink_o;
  logic [1-1:0] r_dbg_busy_o;
  logic [16-1:0] r_dbg_strq_drop_o;
  logic [1-1:0] r_act_strt_chg_o;
  logic [1-1:0] r_act_strt_cmd_chg_o;
  logic [1-1:0] r_dbg_recwr_o;
  logic [SINK_W_C-1:0] r_dbg_recwr_sink_o;
  logic [384-1:0] r_dbg_recwr_rec_o;
  logic [1-1:0] d_txn_ready_o;
  logic [1-1:0] d_evt_tk_ready_o;
  logic [1-1:0] d_pre_ready_o;
  logic [1-1:0] d_strm_set_ready_o;
  logic [1-1:0] d_strm_set_error_o;
  logic [N_SINKS_P-1:0] d_strm_started_o;
  logic [1-1:0] d_tmr_arm_valid_o;
  logic [1-1:0] d_tmr_arm_cancel_o;
  logic [7-1:0] d_tmr_arm_slot_o;
  logic [8-1:0] d_tmr_arm_owner_o;
  logic [32-1:0] d_tmr_arm_deadline_ms_o;
  logic [1-1:0] d_draw_req_o;
  logic [3-1:0] d_draw_kind_o;
  logic [2-1:0] d_rxs_rd_slot_o;
  logic [10-1:0] d_rxs_rd_addr_o;
  logic [1-1:0] d_rxs_rd_en_o;
  logic [1-1:0] d_rxs_free_o;
  logic [2-1:0] d_rxs_free_slot_o;
  logic [1-1:0] d_txs_alloc_req_o;
  logic [1-1:0] d_txs_oversize_o;
  logic [3-1:0] d_txs_wr_slot_o;
  logic [11-1:0] d_txs_wr_addr_o;
  logic [1-1:0] d_txs_wr_valid_o;
  logic [8-1:0] d_txs_wr_data_o;
  logic [1-1:0] d_txs_wr_commit_o;
  logic [11-1:0] d_txs_wr_len_o;
  logic [1-1:0] d_txreq_valid_o;
  logic [3-1:0] d_txreq_slot_o;
  logic [1-1:0] d_act_settle_o;
  logic [64-1:0] d_act_settle_sid_o;
  logic [48-1:0] d_act_settle_da_o;
  logic [12-1:0] d_act_settle_vlan_o;
  logic [1-1:0] d_act_teardown_o;
  logic [1-1:0] d_act_disc_arm_o;
  logic [64-1:0] d_act_disc_talker_eid_o;
  logic [1-1:0] d_act_disc_disarm_o;
  logic [1-1:0] d_act_nvm_o;
  logic [1-1:0] d_act_nvm_set_o;
  logic [1-1:0] d_act_notify_o;
  logic [SINK_W_C-1:0] d_act_sink_o;
  logic [1-1:0] d_dbg_busy_o;
  logic [16-1:0] d_dbg_strq_drop_o;
  logic [1-1:0] d_act_strt_chg_o;
  logic [1-1:0] d_act_strt_cmd_chg_o;
  logic [1-1:0] d_dbg_recwr_o;
  logic [SINK_W_C-1:0] d_dbg_recwr_sink_o;
  logic [384-1:0] d_dbg_recwr_rec_o;
  KL_pp_acmp_listener_ref #(.N_SINKS_P(N_SINKS_P), .STRM_TIMEOUT_CYC_P(32)) u_r (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .entity_id_i(entity_id_i),
    .txn_valid_i(txn_valid_i),
    .txn_i(txn_i),
    .evt_tk_valid_i(evt_tk_valid_i),
    .evt_tk_kind_i(evt_tk_kind_i),
    .evt_tk_failed_i(evt_tk_failed_i),
    .evt_tk_sink_i(evt_tk_sink_i),
    .pre_valid_i(pre_valid_i),
    .pre_sink_i(pre_sink_i),
    .pre_talker_eid_i(pre_talker_eid_i),
    .pre_talker_uid_i(pre_talker_uid_i),
    .pre_ctlr_eid_i(pre_ctlr_eid_i),
    .pre_sw_i(pre_sw_i),
    .pre_started_i(pre_started_i),
    .strm_set_valid_i(strm_set_valid_i),
    .strm_set_sink_i(strm_set_sink_i),
    .strm_set_val_i(strm_set_val_i),
    .now_ms_i(now_ms_i),
    .tmr_exp_valid_i(tmr_exp_valid_i),
    .tmr_exp_slot_i(tmr_exp_slot_i),
    .tmr_exp_owner_i(tmr_exp_owner_i),
    .draw_busy_i(draw_busy_i),
    .draw_valid_i(draw_valid_i),
    .draw_ms_i(draw_ms_i),
    .rxs_rd_data_i(rxs_rd_data_i),
    .txs_alloc_gnt_i(txs_alloc_gnt_i),
    .txs_alloc_slot_i(txs_alloc_slot_i),
    .lock_held_i(lock_held_i),
    .lock_ctlr_i(lock_ctlr_i),
    .txn_ready_o(r_txn_ready_o),
    .evt_tk_ready_o(r_evt_tk_ready_o),
    .pre_ready_o(r_pre_ready_o),
    .strm_set_ready_o(r_strm_set_ready_o),
    .strm_set_error_o(r_strm_set_error_o),
    .strm_started_o(r_strm_started_o),
    .tmr_arm_valid_o(r_tmr_arm_valid_o),
    .tmr_arm_cancel_o(r_tmr_arm_cancel_o),
    .tmr_arm_slot_o(r_tmr_arm_slot_o),
    .tmr_arm_owner_o(r_tmr_arm_owner_o),
    .tmr_arm_deadline_ms_o(r_tmr_arm_deadline_ms_o),
    .draw_req_o(r_draw_req_o),
    .draw_kind_o(r_draw_kind_o),
    .rxs_rd_slot_o(r_rxs_rd_slot_o),
    .rxs_rd_addr_o(r_rxs_rd_addr_o),
    .rxs_rd_en_o(r_rxs_rd_en_o),
    .rxs_free_o(r_rxs_free_o),
    .rxs_free_slot_o(r_rxs_free_slot_o),
    .txs_alloc_req_o(r_txs_alloc_req_o),
    .txs_oversize_o(r_txs_oversize_o),
    .txs_wr_slot_o(r_txs_wr_slot_o),
    .txs_wr_addr_o(r_txs_wr_addr_o),
    .txs_wr_valid_o(r_txs_wr_valid_o),
    .txs_wr_data_o(r_txs_wr_data_o),
    .txs_wr_commit_o(r_txs_wr_commit_o),
    .txs_wr_len_o(r_txs_wr_len_o),
    .txreq_valid_o(r_txreq_valid_o),
    .txreq_slot_o(r_txreq_slot_o),
    .act_settle_o(r_act_settle_o),
    .act_settle_sid_o(r_act_settle_sid_o),
    .act_settle_da_o(r_act_settle_da_o),
    .act_settle_vlan_o(r_act_settle_vlan_o),
    .act_teardown_o(r_act_teardown_o),
    .act_disc_arm_o(r_act_disc_arm_o),
    .act_disc_talker_eid_o(r_act_disc_talker_eid_o),
    .act_disc_disarm_o(r_act_disc_disarm_o),
    .act_nvm_o(r_act_nvm_o),
    .act_nvm_set_o(r_act_nvm_set_o),
    .act_notify_o(r_act_notify_o),
    .act_sink_o(r_act_sink_o),
    .dbg_busy_o(r_dbg_busy_o),
    .dbg_strq_drop_o(r_dbg_strq_drop_o),
    .act_strt_chg_o(r_act_strt_chg_o),
    .act_strt_cmd_chg_o(r_act_strt_cmd_chg_o),
    .dbg_recwr_o(r_dbg_recwr_o),
    .dbg_recwr_sink_o(r_dbg_recwr_sink_o),
    .dbg_recwr_rec_o(r_dbg_recwr_rec_o)
  );
  assign r_all_o = {r_txn_ready_o, r_evt_tk_ready_o, r_pre_ready_o, r_strm_set_ready_o, r_strm_set_error_o, r_strm_started_o, r_tmr_arm_valid_o, r_tmr_arm_cancel_o, r_tmr_arm_slot_o, r_tmr_arm_owner_o, r_tmr_arm_deadline_ms_o, r_draw_req_o, r_draw_kind_o, r_rxs_rd_slot_o, r_rxs_rd_addr_o, r_rxs_rd_en_o, r_rxs_free_o, r_rxs_free_slot_o, r_txs_alloc_req_o, r_txs_oversize_o, r_txs_wr_slot_o, r_txs_wr_addr_o, r_txs_wr_valid_o, r_txs_wr_data_o, r_txs_wr_commit_o, r_txs_wr_len_o, r_txreq_valid_o, r_txreq_slot_o, r_act_settle_o, r_act_settle_sid_o, r_act_settle_da_o, r_act_settle_vlan_o, r_act_teardown_o, r_act_disc_arm_o, r_act_disc_talker_eid_o, r_act_disc_disarm_o, r_act_nvm_o, r_act_nvm_set_o, r_act_notify_o, r_act_sink_o, r_dbg_busy_o, r_dbg_strq_drop_o, r_act_strt_chg_o, r_act_strt_cmd_chg_o, r_dbg_recwr_o, r_dbg_recwr_sink_o, r_dbg_recwr_rec_o};
  assign r_xs_o = 5'(u_r.xs_r);
  KL_pp_acmp_listener #(.N_SINKS_P(N_SINKS_P), .STRM_TIMEOUT_CYC_P(32)) u_d (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .entity_id_i(entity_id_i),
    .txn_valid_i(txn_valid_i),
    .txn_i(txn_i),
    .evt_tk_valid_i(evt_tk_valid_i),
    .evt_tk_kind_i(evt_tk_kind_i),
    .evt_tk_failed_i(evt_tk_failed_i),
    .evt_tk_sink_i(evt_tk_sink_i),
    .pre_valid_i(pre_valid_i),
    .pre_sink_i(pre_sink_i),
    .pre_talker_eid_i(pre_talker_eid_i),
    .pre_talker_uid_i(pre_talker_uid_i),
    .pre_ctlr_eid_i(pre_ctlr_eid_i),
    .pre_sw_i(pre_sw_i),
    .pre_started_i(pre_started_i),
    .strm_set_valid_i(strm_set_valid_i),
    .strm_set_sink_i(strm_set_sink_i),
    .strm_set_val_i(strm_set_val_i),
    .now_ms_i(now_ms_i),
    .tmr_exp_valid_i(tmr_exp_valid_i),
    .tmr_exp_slot_i(tmr_exp_slot_i),
    .tmr_exp_owner_i(tmr_exp_owner_i),
    .draw_busy_i(draw_busy_i),
    .draw_valid_i(draw_valid_i),
    .draw_ms_i(draw_ms_i),
    .rxs_rd_data_i(rxs_rd_data_i),
    .txs_alloc_gnt_i(txs_alloc_gnt_i),
    .txs_alloc_slot_i(txs_alloc_slot_i),
    .lock_held_i(lock_held_i),
    .lock_ctlr_i(lock_ctlr_i),
    .txn_ready_o(d_txn_ready_o),
    .evt_tk_ready_o(d_evt_tk_ready_o),
    .pre_ready_o(d_pre_ready_o),
    .strm_set_ready_o(d_strm_set_ready_o),
    .strm_set_error_o(d_strm_set_error_o),
    .strm_started_o(d_strm_started_o),
    .tmr_arm_valid_o(d_tmr_arm_valid_o),
    .tmr_arm_cancel_o(d_tmr_arm_cancel_o),
    .tmr_arm_slot_o(d_tmr_arm_slot_o),
    .tmr_arm_owner_o(d_tmr_arm_owner_o),
    .tmr_arm_deadline_ms_o(d_tmr_arm_deadline_ms_o),
    .draw_req_o(d_draw_req_o),
    .draw_kind_o(d_draw_kind_o),
    .rxs_rd_slot_o(d_rxs_rd_slot_o),
    .rxs_rd_addr_o(d_rxs_rd_addr_o),
    .rxs_rd_en_o(d_rxs_rd_en_o),
    .rxs_free_o(d_rxs_free_o),
    .rxs_free_slot_o(d_rxs_free_slot_o),
    .txs_alloc_req_o(d_txs_alloc_req_o),
    .txs_oversize_o(d_txs_oversize_o),
    .txs_wr_slot_o(d_txs_wr_slot_o),
    .txs_wr_addr_o(d_txs_wr_addr_o),
    .txs_wr_valid_o(d_txs_wr_valid_o),
    .txs_wr_data_o(d_txs_wr_data_o),
    .txs_wr_commit_o(d_txs_wr_commit_o),
    .txs_wr_len_o(d_txs_wr_len_o),
    .txreq_valid_o(d_txreq_valid_o),
    .txreq_slot_o(d_txreq_slot_o),
    .act_settle_o(d_act_settle_o),
    .act_settle_sid_o(d_act_settle_sid_o),
    .act_settle_da_o(d_act_settle_da_o),
    .act_settle_vlan_o(d_act_settle_vlan_o),
    .act_teardown_o(d_act_teardown_o),
    .act_disc_arm_o(d_act_disc_arm_o),
    .act_disc_talker_eid_o(d_act_disc_talker_eid_o),
    .act_disc_disarm_o(d_act_disc_disarm_o),
    .act_nvm_o(d_act_nvm_o),
    .act_nvm_set_o(d_act_nvm_set_o),
    .act_notify_o(d_act_notify_o),
    .act_sink_o(d_act_sink_o),
    .dbg_busy_o(d_dbg_busy_o),
    .dbg_strq_drop_o(d_dbg_strq_drop_o),
    .act_strt_chg_o(d_act_strt_chg_o),
    .act_strt_cmd_chg_o(d_act_strt_cmd_chg_o),
    .dbg_recwr_o(d_dbg_recwr_o),
    .dbg_recwr_sink_o(d_dbg_recwr_sink_o),
    .dbg_recwr_rec_o(d_dbg_recwr_rec_o)
  );
  assign d_all_o = {d_txn_ready_o, d_evt_tk_ready_o, d_pre_ready_o, d_strm_set_ready_o, d_strm_set_error_o, d_strm_started_o, d_tmr_arm_valid_o, d_tmr_arm_cancel_o, d_tmr_arm_slot_o, d_tmr_arm_owner_o, d_tmr_arm_deadline_ms_o, d_draw_req_o, d_draw_kind_o, d_rxs_rd_slot_o, d_rxs_rd_addr_o, d_rxs_rd_en_o, d_rxs_free_o, d_rxs_free_slot_o, d_txs_alloc_req_o, d_txs_oversize_o, d_txs_wr_slot_o, d_txs_wr_addr_o, d_txs_wr_valid_o, d_txs_wr_data_o, d_txs_wr_commit_o, d_txs_wr_len_o, d_txreq_valid_o, d_txreq_slot_o, d_act_settle_o, d_act_settle_sid_o, d_act_settle_da_o, d_act_settle_vlan_o, d_act_teardown_o, d_act_disc_arm_o, d_act_disc_talker_eid_o, d_act_disc_disarm_o, d_act_nvm_o, d_act_nvm_set_o, d_act_notify_o, d_act_sink_o, d_dbg_busy_o, d_dbg_strq_drop_o, d_act_strt_chg_o, d_act_strt_cmd_chg_o, d_dbg_recwr_o, d_dbg_recwr_sink_o, d_dbg_recwr_rec_o};
  assign d_xs_o = 5'(u_d.xs_r);
endmodule
`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : d3s4_listener_admit.sv   (AREA WRAPPER, design evidence)
//  Project     : milan-fpga #500, saved-state scope D3, seam S4
//
//  Description : The pinned KL_pp_acmp_listener with the proposed admission
//                gate KL_pp_acmp_lsn_admit in front of its four work faces,
//                wired as d3_top.sv and the page's section 5.1 wire them:
//                every other listener port passes straight through. Only for
//                an out-of-context area row: its difference from the
//                listener alone is the gate's cost IN PLACE, beside the
//                gate's own row. Not product wiring and not a measurement of
//                the integrated processor.
//---------------------------------------------------------------------------//
`default_nettype none

module d3s4_listener_admit
  import pp_pkg::*;
  import pp_acmp_pkg::*;
#(
    parameter int unsigned N_SINKS_P = 8,
    localparam int unsigned SINK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1
) (
    input  wire                          clk_i,
    input  wire                          rst_n,
    input  wire  [63:0]                  entity_id_i,
    //! the gate's release input and outputs
    input  wire                          walk_done_i,
    output logic                         own_o,
    output logic                         released_o,
    output logic [15:0]                  dbg_exp_drop_o,
    //! the four work faces, producer side
    input  wire                          txn_valid_i,
    input  wire  pp_txn_t                txn_i,
    output logic                         txn_ready_o,
    input  wire                          evt_tk_valid_i,
    input  wire  [1:0]                   evt_tk_kind_i,
    input  wire                          evt_tk_failed_i,
    input  wire  [15:0]                  evt_tk_sink_i,
    output logic                         evt_tk_ready_o,
    input  wire                          strm_set_valid_i,
    input  wire  [15:0]                  strm_set_sink_i,
    input  wire                          strm_set_val_i,
    output logic                         strm_set_ready_o,
    output logic                         strm_set_error_o,
    input  wire                          tmr_exp_valid_i,
    input  wire  [6:0]                   tmr_exp_slot_i,
    input  wire  [7:0]                   tmr_exp_owner_i,
    //! every other listener face, straight through
    input  wire                          pre_valid_i,
    input  wire  [15:0]                  pre_sink_i,
    input  wire  [63:0]                  pre_talker_eid_i,
    input  wire  [15:0]                  pre_talker_uid_i,
    input  wire  [63:0]                  pre_ctlr_eid_i,
    input  wire                          pre_sw_i,
    input  wire                          pre_started_i,
    output logic                         pre_ready_o,
    output logic [N_SINKS_P-1:0]         strm_started_o,
    input  wire  [31:0]                  now_ms_i,
    output logic                         tmr_arm_valid_o,
    output logic                         tmr_arm_cancel_o,
    output logic [6:0]                   tmr_arm_slot_o,
    output logic [7:0]                   tmr_arm_owner_o,
    output logic [31:0]                  tmr_arm_deadline_ms_o,
    output logic                         draw_req_o,
    output logic [2:0]                   draw_kind_o,
    input  wire                          draw_busy_i,
    input  wire                          draw_valid_i,
    input  wire  [15:0]                  draw_ms_i,
    output logic [1:0]                   rxs_rd_slot_o,
    output logic [9:0]                   rxs_rd_addr_o,
    output logic                         rxs_rd_en_o,
    input  wire  [7:0]                   rxs_rd_data_i,
    output logic                         rxs_free_o,
    output logic [1:0]                   rxs_free_slot_o,
    output logic                         txs_alloc_req_o,
    output logic                         txs_oversize_o,
    input  wire                          txs_alloc_gnt_i,
    input  wire  [2:0]                   txs_alloc_slot_i,
    output logic [2:0]                   txs_wr_slot_o,
    output logic [10:0]                  txs_wr_addr_o,
    output logic                         txs_wr_valid_o,
    output logic [7:0]                   txs_wr_data_o,
    output logic                         txs_wr_commit_o,
    output logic [10:0]                  txs_wr_len_o,
    output logic                         txreq_valid_o,
    output logic [2:0]                   txreq_slot_o,
    input  wire                          lock_held_i,
    input  wire  [63:0]                  lock_ctlr_i,
    output logic                         act_settle_o,
    output logic [63:0]                  act_settle_sid_o,
    output logic [47:0]                  act_settle_da_o,
    output logic [11:0]                  act_settle_vlan_o,
    output logic                         act_teardown_o,
    output logic                         act_disc_arm_o,
    output logic [63:0]                  act_disc_talker_eid_o,
    output logic                         act_disc_disarm_o,
    output logic                         act_nvm_o,
    output logic                         act_nvm_set_o,
    output logic                         act_notify_o,
    output logic [SINK_W_C-1:0]          act_sink_o,
    output logic                         dbg_busy_o,
    output logic [15:0]                  dbg_strq_drop_o,
    output logic                         act_strt_chg_o,
    output logic                         act_strt_cmd_chg_o,
    output logic                         dbg_recwr_o,
    output logic [SINK_W_C-1:0]          dbg_recwr_sink_o,
    output logic [ACMP_REC_W_C-1:0]      dbg_recwr_rec_o
);

  logic l_txn_valid_w, l_txn_ready_w, l_tk_valid_w, l_tk_ready_w, l_strm_valid_w, l_exp_valid_w;

  KL_pp_acmp_lsn_admit #(
      .N_SINKS_P        (N_SINKS_P),
      .TMR_OWNER_BASE_P (32),
      .OWNER_W_P        (8)
  ) u_admit (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .walk_done_i    (walk_done_i),
      .pre_valid_i    (pre_valid_i),
      .lsn_busy_i     (dbg_busy_o),
      .lsn_arm_i      (act_disc_arm_o),
      .own_o          (own_o),
      .released_o     (released_o),
      .p_txn_valid_i  (txn_valid_i),
      .p_txn_ready_o  (txn_ready_o),
      .l_txn_valid_o  (l_txn_valid_w),
      .l_txn_ready_i  (l_txn_ready_w),
      .p_tk_valid_i   (evt_tk_valid_i),
      .p_tk_ready_o   (evt_tk_ready_o),
      .l_tk_valid_o   (l_tk_valid_w),
      .l_tk_ready_i   (l_tk_ready_w),
      .p_strm_valid_i (strm_set_valid_i),
      .l_strm_valid_o (l_strm_valid_w),
      .p_exp_valid_i  (tmr_exp_valid_i),
      .p_exp_owner_i  (tmr_exp_owner_i),
      .l_exp_valid_o  (l_exp_valid_w),
      .dbg_exp_drop_o (dbg_exp_drop_o)
  );

  KL_pp_acmp_listener #(
      .N_SINKS_P (N_SINKS_P)
  ) u_lsn (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_id_i           (entity_id_i),
      .txn_valid_i           (l_txn_valid_w),
      .txn_i                 (txn_i),
      .txn_ready_o           (l_txn_ready_w),
      .evt_tk_valid_i        (l_tk_valid_w),
      .evt_tk_kind_i         (evt_tk_kind_i),
      .evt_tk_failed_i       (evt_tk_failed_i),
      .evt_tk_sink_i         (evt_tk_sink_i),
      .evt_tk_ready_o        (l_tk_ready_w),
      .pre_valid_i           (pre_valid_i),
      .pre_sink_i            (pre_sink_i),
      .pre_talker_eid_i      (pre_talker_eid_i),
      .pre_talker_uid_i      (pre_talker_uid_i),
      .pre_ctlr_eid_i        (pre_ctlr_eid_i),
      .pre_sw_i              (pre_sw_i),
      .pre_started_i         (pre_started_i),
      .pre_ready_o           (pre_ready_o),
      .strm_set_valid_i      (l_strm_valid_w),
      .strm_set_sink_i       (strm_set_sink_i),
      .strm_set_val_i        (strm_set_val_i),
      .strm_set_ready_o      (strm_set_ready_o),
      .strm_set_error_o      (strm_set_error_o),
      .strm_started_o        (strm_started_o),
      .now_ms_i              (now_ms_i),
      .tmr_arm_valid_o       (tmr_arm_valid_o),
      .tmr_arm_cancel_o      (tmr_arm_cancel_o),
      .tmr_arm_slot_o        (tmr_arm_slot_o),
      .tmr_arm_owner_o       (tmr_arm_owner_o),
      .tmr_arm_deadline_ms_o (tmr_arm_deadline_ms_o),
      .tmr_exp_valid_i       (l_exp_valid_w),
      .tmr_exp_slot_i        (tmr_exp_slot_i),
      .tmr_exp_owner_i       (tmr_exp_owner_i),
      .draw_req_o            (draw_req_o),
      .draw_kind_o           (draw_kind_o),
      .draw_busy_i           (draw_busy_i),
      .draw_valid_i          (draw_valid_i),
      .draw_ms_i             (draw_ms_i),
      .rxs_rd_slot_o         (rxs_rd_slot_o),
      .rxs_rd_addr_o         (rxs_rd_addr_o),
      .rxs_rd_en_o           (rxs_rd_en_o),
      .rxs_rd_data_i         (rxs_rd_data_i),
      .rxs_free_o            (rxs_free_o),
      .rxs_free_slot_o       (rxs_free_slot_o),
      .txs_alloc_req_o       (txs_alloc_req_o),
      .txs_oversize_o        (txs_oversize_o),
      .txs_alloc_gnt_i       (txs_alloc_gnt_i),
      .txs_alloc_slot_i      (txs_alloc_slot_i),
      .txs_wr_slot_o         (txs_wr_slot_o),
      .txs_wr_addr_o         (txs_wr_addr_o),
      .txs_wr_valid_o        (txs_wr_valid_o),
      .txs_wr_data_o         (txs_wr_data_o),
      .txs_wr_commit_o       (txs_wr_commit_o),
      .txs_wr_len_o          (txs_wr_len_o),
      .txreq_valid_o         (txreq_valid_o),
      .txreq_slot_o          (txreq_slot_o),
      .lock_held_i           (lock_held_i),
      .lock_ctlr_i           (lock_ctlr_i),
      .act_settle_o          (act_settle_o),
      .act_settle_sid_o      (act_settle_sid_o),
      .act_settle_da_o       (act_settle_da_o),
      .act_settle_vlan_o     (act_settle_vlan_o),
      .act_teardown_o        (act_teardown_o),
      .act_disc_arm_o        (act_disc_arm_o),
      .act_disc_talker_eid_o (act_disc_talker_eid_o),
      .act_disc_disarm_o     (act_disc_disarm_o),
      .act_nvm_o             (act_nvm_o),
      .act_nvm_set_o         (act_nvm_set_o),
      .act_notify_o          (act_notify_o),
      .act_sink_o            (act_sink_o),
      .dbg_busy_o            (dbg_busy_o),
      .dbg_strq_drop_o       (dbg_strq_drop_o),
      .act_strt_chg_o        (act_strt_chg_o),
      .act_strt_cmd_chg_o    (act_strt_cmd_chg_o),
      .dbg_recwr_o           (dbg_recwr_o),
      .dbg_recwr_sink_o      (dbg_recwr_sink_o),
      .dbg_recwr_rec_o       (dbg_recwr_rec_o)
  );

endmodule

`default_nettype wire

// Reviewer lockstep harness: main's KL_aecp_notify (renamed KL_aecp_notify_ref)
// beside the candidate's KL_aecp_notify, one input set, every output and the
// internal rx_cmd_hit_w concatenated and compared. Candidate internals are
// exported for stimulus bias and coverage only (never for the verdict).
`default_nettype none
module lockstep_top
  import pp_pkg::*;
#(
    parameter int unsigned N_CTRL_P = 16,
    parameter int unsigned N_STREAM_IN_P = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter bit EN_IDENTIFY_NOTIF_P = 1'b0,
    localparam int unsigned TMR_SLOTS_P = 89,
    localparam int unsigned TMR_AW_C = $clog2(TMR_SLOTS_P),
    localparam int unsigned CIX_W_C = (N_CTRL_P > 1) ? $clog2(N_CTRL_P) : 1,
    // width of the concatenated outputs below
    localparam int unsigned OW_C = 64 + 1 + 1 + 3 + 1 + 4 + 64 + 48 + 1 + 4
                                 + 1 + 4 + 16 + 16 + 64 + 48 + 16 + 1 + 16 + 16 + 16
                                 + 1 + 1 + 64
                                 + 1 + 1 + TMR_AW_C + 8 + 32
                                 + 1 + 1 + TMR_AW_C + 8 + 32
                                 + 8 + 16 + 8
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         rgy_req_i,
    input  wire         rgy_state_i,
    input  wire  [1:0]  rgy_op_i,
    input  wire  [63:0] rgy_eid_i,
    input  wire  [47:0] rgy_mac_i,
    input  wire         rgy_tl_i,
    input  wire  [N_STREAM_IN_P-1:0]  ev_stri_in_i,
    input  wire  [N_STREAM_OUT_P-1:0] ev_stri_out_i,
    input  wire         ev_avb_i,
    input  wire         ev_asp_i,
    input  wire         ev_amap_i,
    input  wire         ev_amap_remove_i,
    input  wire  [15:0] ev_amap_type_i,
    input  wire  [15:0] ev_amap_index_i,
    input  wire  [15:0] ev_amap_count_i,
    input  wire  [63:0] ev_amap_excl_eid_i,
    input  wire         ev_ctr_i,
    input  wire  [15:0] ev_ctr_type_i,
    input  wire  [15:0] ev_ctr_index_i,
    input  wire         ev_cmd_i,
    input  wire  [3:0]  ev_cmd_class_i,
    input  wire  [15:0] ev_cmd_type_i,
    input  wire  [15:0] ev_cmd_index_i,
    input  wire  [15:0] ev_cmd_arg0_i,
    input  wire  [15:0] ev_cmd_arg1_i,
    input  wire  [63:0] ev_cmd_excl_eid_i,
    input  wire         identify_button_i,
    input  wire  [15:0] identify_index_i,
    input  wire         rx_cmd_valid_i,
    input  wire  [63:0] rx_cmd_eid_i,
    input  wire  [47:0] rx_cmd_mac_i,
    input  wire         prng_draw_busy_i,
    input  wire         prng_draw_valid_i,
    input  wire  [15:0] prng_draw_ms_i,
    input  wire         ca_ready_i,
    input  wire         ca_rsp_valid_i,
    input  wire  [3:0]  ca_rsp_owner_i,
    input  wire         ca_fail_valid_i,
    input  wire  [3:0]  ca_fail_owner_i,
    input  wire         uns_done_i,
    input  wire         uns_tx_busy_i,
    input  wire  [31:0] now_ms_i,
    input  wire         tmr_exp_valid_i,
    input  wire  [TMR_AW_C-1:0] tmr_exp_slot_i,
    input  wire  [7:0]  tmr_exp_owner_i,

    output logic [OW_C-1:0]     ref_out_o,
    output logic [OW_C-1:0]     dut_out_o,
    output logic [N_CTRL_P-1:0] ref_hit_o,
    output logic [N_CTRL_P-1:0] dut_hit_o,
    output logic                mismatch_o,
    // candidate internals, stimulus bias and coverage only
    output logic                dut_ix_clr_o,
    output logic                dut_ix_set_o,
    output logic                dut_wr_en_o,
    output logic [CIX_W_C-1:0]  dut_wr_ix_o,
    output logic [111:0]        dut_wr_row_id_o,   // rows_r[wr_ix_r] identity, as read
    output logic [111:0]        dut_wr_new_id_o,   // wr_row_r identity
    output logic [N_CTRL_P-1:0] dut_valid_o,
    output logic                rgy_wait_ref_o,
    output logic [63:0]         rgy_data_ref_o,
    output logic                uns_valid_ref_o,
    output logic [7:0]          own_ntfy_o,
    output logic [7:0]          own_lock_o,
    output logic [7:0]          own_cmon_o,
    output logic [7:0]          own_ident_o
);
  assign own_ntfy_o  = PP_OWN_NTFY_C;
  assign own_lock_o  = PP_OWN_LOCK_C;
  assign own_cmon_o  = PP_OWN_CMON_C;
  assign own_ident_o = PP_OWN_IDENT_C;

`define LS_OUTS(p) \
  logic [63:0] p``rgy_data; logic p``rgy_wait; logic p``prng_req; logic [2:0] p``prng_kind; \
  logic p``ca_valid; logic [3:0] p``ca_owner; logic [63:0] p``ca_eid; logic [47:0] p``ca_mac; \
  logic p``ca_cv; logic [3:0] p``ca_co; logic p``uns_valid; logic [3:0] p``uns_kind; \
  logic [15:0] p``uns_dt, p``uns_di; logic [63:0] p``uns_eid; logic [47:0] p``uns_mac; \
  logic [15:0] p``uns_seq; logic p``uns_rm; logic [15:0] p``uns_cnt, p``uns_a0, p``uns_a1; \
  logic p``amap_busy; logic p``lk_held; logic [63:0] p``lk_ctlr; \
  logic p``ta_v, p``ta_c; logic [TMR_AW_C-1:0] p``ta_s; logic [7:0] p``ta_o; logic [31:0] p``ta_d; \
  logic p``ma_v, p``ma_c; logic [TMR_AW_C-1:0] p``ma_s; logic [7:0] p``ma_o; logic [31:0] p``ma_d; \
  logic [7:0] p``dbg_reg; logic [15:0] p``dbg_uns; logic [7:0] p``dbg_co;

  `LS_OUTS(r_)
  `LS_OUTS(d_)

`define LS_INST(MOD, NAME, p) \
  MOD #(.N_CTRL_P(N_CTRL_P), .N_STREAM_IN_P(N_STREAM_IN_P), .N_STREAM_OUT_P(N_STREAM_OUT_P), \
        .EN_IDENTIFY_NOTIF_P(EN_IDENTIFY_NOTIF_P)) NAME ( \
    .clk_i, .rst_n, .rgy_req_i, .rgy_state_i, .rgy_op_i, .rgy_eid_i, .rgy_mac_i, .rgy_tl_i, \
    .rgy_data_o(p``rgy_data), .rgy_wait_o(p``rgy_wait), \
    .ev_stri_in_i, .ev_stri_out_i, .ev_avb_i, .ev_asp_i, .ev_amap_i, .ev_amap_remove_i, \
    .ev_amap_type_i, .ev_amap_index_i, .ev_amap_count_i, .ev_amap_excl_eid_i, \
    .ev_ctr_i, .ev_ctr_type_i, .ev_ctr_index_i, .ev_cmd_i, .ev_cmd_class_i, .ev_cmd_type_i, \
    .ev_cmd_index_i, .ev_cmd_arg0_i, .ev_cmd_arg1_i, .ev_cmd_excl_eid_i, \
    .identify_button_i, .identify_index_i, \
    .rx_cmd_valid_i, .rx_cmd_eid_i, .rx_cmd_mac_i, \
    .prng_draw_req_o(p``prng_req), .prng_draw_kind_o(p``prng_kind), .prng_draw_busy_i, \
    .prng_draw_valid_i, .prng_draw_ms_i, \
    .ca_valid_o(p``ca_valid), .ca_owner_o(p``ca_owner), .ca_ctlr_eid_o(p``ca_eid), \
    .ca_mac_o(p``ca_mac), .ca_ready_i, .ca_cancel_valid_o(p``ca_cv), \
    .ca_cancel_owner_o(p``ca_co), .ca_rsp_valid_i, .ca_rsp_owner_i, .ca_fail_valid_i, \
    .ca_fail_owner_i, \
    .uns_valid_o(p``uns_valid), .uns_kind_o(p``uns_kind), .uns_desc_type_o(p``uns_dt), \
    .uns_desc_index_o(p``uns_di), .uns_ctlr_eid_o(p``uns_eid), .uns_mac_o(p``uns_mac), \
    .uns_seq_o(p``uns_seq), .uns_amap_remove_o(p``uns_rm), .uns_amap_count_o(p``uns_cnt), \
    .uns_arg0_o(p``uns_a0), .uns_arg1_o(p``uns_a1), .uns_done_i, .uns_tx_busy_i, \
    .amap_busy_o(p``amap_busy), .lock_held_o(p``lk_held), .lock_ctlr_o(p``lk_ctlr), \
    .tmr_arm_valid_o(p``ta_v), .tmr_arm_cancel_o(p``ta_c), .tmr_arm_slot_o(p``ta_s), \
    .tmr_arm_owner_o(p``ta_o), .tmr_arm_deadline_ms_o(p``ta_d), .now_ms_i, \
    .tmr_exp_valid_i, .tmr_exp_slot_i, .tmr_exp_owner_i, \
    .mon_arm_valid_o(p``ma_v), .mon_arm_cancel_o(p``ma_c), .mon_arm_slot_o(p``ma_s), \
    .mon_arm_owner_o(p``ma_o), .mon_arm_deadline_ms_o(p``ma_d), \
    .dbg_reg_cnt_o(p``dbg_reg), .dbg_uns_cnt_o(p``dbg_uns), .dbg_coalesce_o(p``dbg_co));

  `LS_INST(KL_aecp_notify_ref, u_ref, r_)
  `LS_INST(KL_aecp_notify,     u_dut, d_)

`define LS_CAT(p) { p``rgy_data, p``rgy_wait, p``prng_req, p``prng_kind, p``ca_valid, \
    p``ca_owner, p``ca_eid, p``ca_mac, p``ca_cv, p``ca_co, p``uns_valid, p``uns_kind, \
    p``uns_dt, p``uns_di, p``uns_eid, p``uns_mac, p``uns_seq, p``uns_rm, p``uns_cnt, \
    p``uns_a0, p``uns_a1, p``amap_busy, p``lk_held, p``lk_ctlr, \
    p``ta_v, p``ta_c, p``ta_s, p``ta_o, p``ta_d, p``ma_v, p``ma_c, p``ma_s, p``ma_o, p``ma_d, \
    p``dbg_reg, p``dbg_uns, p``dbg_co }

  assign ref_out_o  = `LS_CAT(r_);
  assign dut_out_o  = `LS_CAT(d_);
  assign ref_hit_o  = u_ref.rx_cmd_hit_w;
  assign dut_hit_o  = u_dut.rx_cmd_hit_w;
  assign mismatch_o = (ref_out_o != dut_out_o) || (ref_hit_o != dut_hit_o);

  assign dut_ix_clr_o    = u_dut.ix_clr_r;
  assign dut_ix_set_o    = u_dut.ix_set_r;
  assign dut_wr_en_o     = u_dut.wr_en_r;
  assign dut_wr_ix_o     = u_dut.wr_ix_r;
  assign dut_wr_row_id_o = u_dut.ix_wr_row_w[127:16];
  assign dut_wr_new_id_o = u_dut.wr_row_r[127:16];
  assign dut_valid_o     = u_dut.valid_r;
  assign rgy_wait_ref_o  = r_rgy_wait;
  assign rgy_data_ref_o  = r_rgy_data;
  assign uns_valid_ref_o = r_uns_valid;
endmodule
`default_nettype wire

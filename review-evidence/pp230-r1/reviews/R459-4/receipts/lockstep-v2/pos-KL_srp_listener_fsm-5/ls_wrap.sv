module ls_wrap (
    output logic [26:0] mm_o,
    output logic [26:0] act_o,
    input  wire clk_i,
    input  wire rst_n,
    input  wire p2p_i,
    input  wire ctl_valid_i,
    input  wire ctl_settle_i,
    input  wire [2:0] ctl_sink_i,
    input  wire [63:0] ctl_stream_id_i,
    input  wire [47:0] ctl_da_i,
    input  wire [11:0] ctl_vid_i,
    input  wire evt_valid_i,
    input  wire evt_msrp_i,
    input  wire [7:0] evt_attr_type_i,
    input  wire [63:0] evt_stream_id_i,
    input  wire [47:0] evt_da_i,
    input  wire [15:0] evt_vid_i,
    input  wire [2:0] evt_mrp_event_i,
    input  wire [31:0] evt_acc_latency_i,
    input  wire [63:0] evt_failure_system_id_i,
    input  wire [7:0] evt_failure_code_i,
    input  wire join_tick_i,
    input  wire periodic_tick_i,
    input  wire [3:0] leaveall_rx_i,
    input  wire leaveall_own_i,
    input  wire ev_ready_i,
    input  wire user_ready_i,
    input  wire [31:0] now_ms_i,
    input  wire exp_valid_i,
    input  wire [6:0] exp_slot_i
);
  wire a_ctl_ready_o, b_ctl_ready_o;
  wire a_txop_done_o, b_txop_done_o;
  wire a_ev_valid_o, b_ev_valid_o;
  wire a_ev_app_o, b_ev_app_o;
  wire [7:0] a_ev_attr_type_o, b_ev_attr_type_o;
  wire [2:0] a_ev_event_o, b_ev_event_o;
  wire [1:0] a_ev_fourpack_o, b_ev_fourpack_o;
  wire [271:0] a_ev_value_o, b_ev_value_o;
  wire a_user_valid_o, b_user_valid_o;
  wire a_user_join_o, b_user_join_o;
  wire [11:0] a_user_vid_o, b_user_vid_o;
  wire a_arm_valid_o, b_arm_valid_o;
  wire a_arm_cancel_o, b_arm_cancel_o;
  wire [6:0] a_arm_slot_o, b_arm_slot_o;
  wire [7:0] a_arm_owner_o, b_arm_owner_o;
  wire [31:0] a_arm_deadline_ms_o, b_arm_deadline_ms_o;
  wire [4:0] a_evt_tk_registered_o, b_evt_tk_registered_o;
  wire [4:0] a_evt_tk_unregistered_o, b_evt_tk_unregistered_o;
  wire [4:0] a_evt_tk_fail_chg_o, b_evt_tk_fail_chg_o;
  wire [4:0] a_evt_tk_latency_chg_o, b_evt_tk_latency_chg_o;
  wire [9:0] a_tk_reg_state_o, b_tk_reg_state_o;
  wire [9:0] a_lstn_decl_state_o, b_lstn_decl_state_o;
  wire [159:0] a_acc_latency_o, b_acc_latency_o;
  wire [39:0] a_msrp_fail_code_o, b_msrp_fail_code_o;
  wire [319:0] a_msrp_fail_bridge_o, b_msrp_fail_bridge_o;
  wire [19:0] a_dbg_app_state_o, b_dbg_app_state_o;
  wire [9:0] a_dbg_reg_state_o, b_dbg_reg_state_o;
  B_KL_srp_listener_fsm #(.N_SINKS_P(5)) u_a (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .p2p_i(p2p_i),
    .ctl_valid_i(ctl_valid_i),
    .ctl_settle_i(ctl_settle_i),
    .ctl_sink_i(ctl_sink_i),
    .ctl_stream_id_i(ctl_stream_id_i),
    .ctl_da_i(ctl_da_i),
    .ctl_vid_i(ctl_vid_i),
    .evt_valid_i(evt_valid_i),
    .evt_msrp_i(evt_msrp_i),
    .evt_attr_type_i(evt_attr_type_i),
    .evt_stream_id_i(evt_stream_id_i),
    .evt_da_i(evt_da_i),
    .evt_vid_i(evt_vid_i),
    .evt_mrp_event_i(evt_mrp_event_i),
    .evt_acc_latency_i(evt_acc_latency_i),
    .evt_failure_system_id_i(evt_failure_system_id_i),
    .evt_failure_code_i(evt_failure_code_i),
    .join_tick_i(join_tick_i),
    .periodic_tick_i(periodic_tick_i),
    .leaveall_rx_i(leaveall_rx_i),
    .leaveall_own_i(leaveall_own_i),
    .ev_ready_i(ev_ready_i),
    .user_ready_i(user_ready_i),
    .now_ms_i(now_ms_i),
    .exp_valid_i(exp_valid_i),
    .exp_slot_i(exp_slot_i),
    .ctl_ready_o(a_ctl_ready_o),
    .txop_done_o(a_txop_done_o),
    .ev_valid_o(a_ev_valid_o),
    .ev_app_o(a_ev_app_o),
    .ev_attr_type_o(a_ev_attr_type_o),
    .ev_event_o(a_ev_event_o),
    .ev_fourpack_o(a_ev_fourpack_o),
    .ev_value_o(a_ev_value_o),
    .user_valid_o(a_user_valid_o),
    .user_join_o(a_user_join_o),
    .user_vid_o(a_user_vid_o),
    .arm_valid_o(a_arm_valid_o),
    .arm_cancel_o(a_arm_cancel_o),
    .arm_slot_o(a_arm_slot_o),
    .arm_owner_o(a_arm_owner_o),
    .arm_deadline_ms_o(a_arm_deadline_ms_o),
    .evt_tk_registered_o(a_evt_tk_registered_o),
    .evt_tk_unregistered_o(a_evt_tk_unregistered_o),
    .evt_tk_fail_chg_o(a_evt_tk_fail_chg_o),
    .evt_tk_latency_chg_o(a_evt_tk_latency_chg_o),
    .tk_reg_state_o(a_tk_reg_state_o),
    .lstn_decl_state_o(a_lstn_decl_state_o),
    .acc_latency_o(a_acc_latency_o),
    .msrp_fail_code_o(a_msrp_fail_code_o),
    .msrp_fail_bridge_o(a_msrp_fail_bridge_o),
    .dbg_app_state_o(a_dbg_app_state_o),
    .dbg_reg_state_o(a_dbg_reg_state_o));
  KL_srp_listener_fsm #(.N_SINKS_P(5)) u_b (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .p2p_i(p2p_i),
    .ctl_valid_i(ctl_valid_i),
    .ctl_settle_i(ctl_settle_i),
    .ctl_sink_i(ctl_sink_i),
    .ctl_stream_id_i(ctl_stream_id_i),
    .ctl_da_i(ctl_da_i),
    .ctl_vid_i(ctl_vid_i),
    .evt_valid_i(evt_valid_i),
    .evt_msrp_i(evt_msrp_i),
    .evt_attr_type_i(evt_attr_type_i),
    .evt_stream_id_i(evt_stream_id_i),
    .evt_da_i(evt_da_i),
    .evt_vid_i(evt_vid_i),
    .evt_mrp_event_i(evt_mrp_event_i),
    .evt_acc_latency_i(evt_acc_latency_i),
    .evt_failure_system_id_i(evt_failure_system_id_i),
    .evt_failure_code_i(evt_failure_code_i),
    .join_tick_i(join_tick_i),
    .periodic_tick_i(periodic_tick_i),
    .leaveall_rx_i(leaveall_rx_i),
    .leaveall_own_i(leaveall_own_i),
    .ev_ready_i(ev_ready_i),
    .user_ready_i(user_ready_i),
    .now_ms_i(now_ms_i),
    .exp_valid_i(exp_valid_i),
    .exp_slot_i(exp_slot_i),
    .ctl_ready_o(b_ctl_ready_o),
    .txop_done_o(b_txop_done_o),
    .ev_valid_o(b_ev_valid_o),
    .ev_app_o(b_ev_app_o),
    .ev_attr_type_o(b_ev_attr_type_o),
    .ev_event_o(b_ev_event_o),
    .ev_fourpack_o(b_ev_fourpack_o),
    .ev_value_o(b_ev_value_o),
    .user_valid_o(b_user_valid_o),
    .user_join_o(b_user_join_o),
    .user_vid_o(b_user_vid_o),
    .arm_valid_o(b_arm_valid_o),
    .arm_cancel_o(b_arm_cancel_o),
    .arm_slot_o(b_arm_slot_o),
    .arm_owner_o(b_arm_owner_o),
    .arm_deadline_ms_o(b_arm_deadline_ms_o),
    .evt_tk_registered_o(b_evt_tk_registered_o),
    .evt_tk_unregistered_o(b_evt_tk_unregistered_o),
    .evt_tk_fail_chg_o(b_evt_tk_fail_chg_o),
    .evt_tk_latency_chg_o(b_evt_tk_latency_chg_o),
    .tk_reg_state_o(b_tk_reg_state_o),
    .lstn_decl_state_o(b_lstn_decl_state_o),
    .acc_latency_o(b_acc_latency_o),
    .msrp_fail_code_o(b_msrp_fail_code_o),
    .msrp_fail_bridge_o(b_msrp_fail_bridge_o),
    .dbg_app_state_o(b_dbg_app_state_o),
    .dbg_reg_state_o(b_dbg_reg_state_o));
  assign mm_o[0] = (a_ctl_ready_o != b_ctl_ready_o);
  assign act_o[0] = |b_ctl_ready_o;
  assign mm_o[1] = (a_txop_done_o != b_txop_done_o);
  assign act_o[1] = |b_txop_done_o;
  assign mm_o[2] = (a_ev_valid_o != b_ev_valid_o);
  assign act_o[2] = |b_ev_valid_o;
  assign mm_o[3] = (a_ev_app_o != b_ev_app_o);
  assign act_o[3] = |b_ev_app_o;
  assign mm_o[4] = (a_ev_attr_type_o != b_ev_attr_type_o);
  assign act_o[4] = |b_ev_attr_type_o;
  assign mm_o[5] = (a_ev_event_o != b_ev_event_o);
  assign act_o[5] = |b_ev_event_o;
  assign mm_o[6] = (a_ev_fourpack_o != b_ev_fourpack_o);
  assign act_o[6] = |b_ev_fourpack_o;
  assign mm_o[7] = (a_ev_value_o != b_ev_value_o);
  assign act_o[7] = |b_ev_value_o;
  assign mm_o[8] = (a_user_valid_o != b_user_valid_o);
  assign act_o[8] = |b_user_valid_o;
  assign mm_o[9] = (a_user_join_o != b_user_join_o);
  assign act_o[9] = |b_user_join_o;
  assign mm_o[10] = (a_user_vid_o != b_user_vid_o);
  assign act_o[10] = |b_user_vid_o;
  assign mm_o[11] = (a_arm_valid_o != b_arm_valid_o);
  assign act_o[11] = |b_arm_valid_o;
  assign mm_o[12] = (a_arm_cancel_o != b_arm_cancel_o);
  assign act_o[12] = |b_arm_cancel_o;
  assign mm_o[13] = (a_arm_slot_o != b_arm_slot_o);
  assign act_o[13] = |b_arm_slot_o;
  assign mm_o[14] = (a_arm_owner_o != b_arm_owner_o);
  assign act_o[14] = |b_arm_owner_o;
  assign mm_o[15] = (a_arm_deadline_ms_o != b_arm_deadline_ms_o);
  assign act_o[15] = |b_arm_deadline_ms_o;
  assign mm_o[16] = (a_evt_tk_registered_o != b_evt_tk_registered_o);
  assign act_o[16] = |b_evt_tk_registered_o;
  assign mm_o[17] = (a_evt_tk_unregistered_o != b_evt_tk_unregistered_o);
  assign act_o[17] = |b_evt_tk_unregistered_o;
  assign mm_o[18] = (a_evt_tk_fail_chg_o != b_evt_tk_fail_chg_o);
  assign act_o[18] = |b_evt_tk_fail_chg_o;
  assign mm_o[19] = (a_evt_tk_latency_chg_o != b_evt_tk_latency_chg_o);
  assign act_o[19] = |b_evt_tk_latency_chg_o;
  assign mm_o[20] = (a_tk_reg_state_o != b_tk_reg_state_o);
  assign act_o[20] = |b_tk_reg_state_o;
  assign mm_o[21] = (a_lstn_decl_state_o != b_lstn_decl_state_o);
  assign act_o[21] = |b_lstn_decl_state_o;
  assign mm_o[22] = (a_acc_latency_o != b_acc_latency_o);
  assign act_o[22] = |b_acc_latency_o;
  assign mm_o[23] = (a_msrp_fail_code_o != b_msrp_fail_code_o);
  assign act_o[23] = |b_msrp_fail_code_o;
  assign mm_o[24] = (a_msrp_fail_bridge_o != b_msrp_fail_bridge_o);
  assign act_o[24] = |b_msrp_fail_bridge_o;
  assign mm_o[25] = (a_dbg_app_state_o != b_dbg_app_state_o);
  assign act_o[25] = |b_dbg_app_state_o;
  assign mm_o[26] = (a_dbg_reg_state_o != b_dbg_reg_state_o);
  assign act_o[26] = |b_dbg_reg_state_o;
endmodule

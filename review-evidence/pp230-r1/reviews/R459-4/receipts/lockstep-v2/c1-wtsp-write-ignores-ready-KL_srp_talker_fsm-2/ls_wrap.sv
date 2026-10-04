module ls_wrap (
    output logic [23:0] mm_o,
    output logic [23:0] act_o,
    input  wire clk_i,
    input  wire rst_n,
    input  wire [47:0] own_mac_i,
    input  wire p2p_i,
    input  wire gate_valid_i,
    input  wire gate_open_i,
    input  wire gate_src_i,
    input  wire [63:0] gate_stream_id_i,
    input  wire [47:0] gate_da_i,
    input  wire [11:0] gate_vid_i,
    input  wire [15:0] gate_max_frame_i,
    input  wire [15:0] gate_max_interval_i,
    input  wire [2:0] gate_prio_i,
    input  wire gate_rank_i,
    input  wire [31:0] gate_acc_lat_i,
    input  wire [1:0] sr_admitted_i,
    input  wire evt_valid_i,
    input  wire evt_msrp_i,
    input  wire [7:0] evt_attr_type_i,
    input  wire [63:0] evt_stream_id_i,
    input  wire [47:0] evt_da_i,
    input  wire [15:0] evt_vid_i,
    input  wire [2:0] evt_mrp_event_i,
    input  wire [1:0] evt_fourpacked_i,
    input  wire join_tick_i,
    input  wire periodic_tick_i,
    input  wire [3:0] leaveall_rx_i,
    input  wire leaveall_own_i,
    input  wire ev_ready_i,
    input  wire user_ready_i,
    input  wire [3:0] vid_sent_i,
    input  wire [47:0] vid_val_i,
    input  wire [31:0] now_ms_i,
    input  wire exp_valid_i,
    input  wire [6:0] exp_slot_i
);
  wire a_gate_ready_o, b_gate_ready_o;
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
  wire [1:0] a_lstn_reg_change_o, b_lstn_reg_change_o;
  wire [3:0] a_tk_decl_state_o, b_tk_decl_state_o;
  wire [3:0] a_lstn_reg_state_o, b_lstn_reg_state_o;
  wire [1:0] a_active_o, b_active_o;
  wire [15:0] a_msrp_fail_code_o, b_msrp_fail_code_o;
  wire [127:0] a_msrp_fail_bridge_o, b_msrp_fail_bridge_o;
  wire [7:0] a_dbg_app_state_o, b_dbg_app_state_o;
  wire [3:0] a_dbg_reg_state_o, b_dbg_reg_state_o;
  B_KL_srp_talker_fsm #(.N_SOURCES_P(2)) u_a (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .own_mac_i(own_mac_i),
    .p2p_i(p2p_i),
    .gate_valid_i(gate_valid_i),
    .gate_open_i(gate_open_i),
    .gate_src_i(gate_src_i),
    .gate_stream_id_i(gate_stream_id_i),
    .gate_da_i(gate_da_i),
    .gate_vid_i(gate_vid_i),
    .gate_max_frame_i(gate_max_frame_i),
    .gate_max_interval_i(gate_max_interval_i),
    .gate_prio_i(gate_prio_i),
    .gate_rank_i(gate_rank_i),
    .gate_acc_lat_i(gate_acc_lat_i),
    .sr_admitted_i(sr_admitted_i),
    .evt_valid_i(evt_valid_i),
    .evt_msrp_i(evt_msrp_i),
    .evt_attr_type_i(evt_attr_type_i),
    .evt_stream_id_i(evt_stream_id_i),
    .evt_da_i(evt_da_i),
    .evt_vid_i(evt_vid_i),
    .evt_mrp_event_i(evt_mrp_event_i),
    .evt_fourpacked_i(evt_fourpacked_i),
    .join_tick_i(join_tick_i),
    .periodic_tick_i(periodic_tick_i),
    .leaveall_rx_i(leaveall_rx_i),
    .leaveall_own_i(leaveall_own_i),
    .ev_ready_i(ev_ready_i),
    .user_ready_i(user_ready_i),
    .vid_sent_i(vid_sent_i),
    .vid_val_i(vid_val_i),
    .now_ms_i(now_ms_i),
    .exp_valid_i(exp_valid_i),
    .exp_slot_i(exp_slot_i),
    .gate_ready_o(a_gate_ready_o),
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
    .lstn_reg_change_o(a_lstn_reg_change_o),
    .tk_decl_state_o(a_tk_decl_state_o),
    .lstn_reg_state_o(a_lstn_reg_state_o),
    .active_o(a_active_o),
    .msrp_fail_code_o(a_msrp_fail_code_o),
    .msrp_fail_bridge_o(a_msrp_fail_bridge_o),
    .dbg_app_state_o(a_dbg_app_state_o),
    .dbg_reg_state_o(a_dbg_reg_state_o));
  KL_srp_talker_fsm #(.N_SOURCES_P(2)) u_b (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .own_mac_i(own_mac_i),
    .p2p_i(p2p_i),
    .gate_valid_i(gate_valid_i),
    .gate_open_i(gate_open_i),
    .gate_src_i(gate_src_i),
    .gate_stream_id_i(gate_stream_id_i),
    .gate_da_i(gate_da_i),
    .gate_vid_i(gate_vid_i),
    .gate_max_frame_i(gate_max_frame_i),
    .gate_max_interval_i(gate_max_interval_i),
    .gate_prio_i(gate_prio_i),
    .gate_rank_i(gate_rank_i),
    .gate_acc_lat_i(gate_acc_lat_i),
    .sr_admitted_i(sr_admitted_i),
    .evt_valid_i(evt_valid_i),
    .evt_msrp_i(evt_msrp_i),
    .evt_attr_type_i(evt_attr_type_i),
    .evt_stream_id_i(evt_stream_id_i),
    .evt_da_i(evt_da_i),
    .evt_vid_i(evt_vid_i),
    .evt_mrp_event_i(evt_mrp_event_i),
    .evt_fourpacked_i(evt_fourpacked_i),
    .join_tick_i(join_tick_i),
    .periodic_tick_i(periodic_tick_i),
    .leaveall_rx_i(leaveall_rx_i),
    .leaveall_own_i(leaveall_own_i),
    .ev_ready_i(ev_ready_i),
    .user_ready_i(user_ready_i),
    .vid_sent_i(vid_sent_i),
    .vid_val_i(vid_val_i),
    .now_ms_i(now_ms_i),
    .exp_valid_i(exp_valid_i),
    .exp_slot_i(exp_slot_i),
    .gate_ready_o(b_gate_ready_o),
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
    .lstn_reg_change_o(b_lstn_reg_change_o),
    .tk_decl_state_o(b_tk_decl_state_o),
    .lstn_reg_state_o(b_lstn_reg_state_o),
    .active_o(b_active_o),
    .msrp_fail_code_o(b_msrp_fail_code_o),
    .msrp_fail_bridge_o(b_msrp_fail_bridge_o),
    .dbg_app_state_o(b_dbg_app_state_o),
    .dbg_reg_state_o(b_dbg_reg_state_o));
  assign mm_o[0] = (a_gate_ready_o != b_gate_ready_o);
  assign act_o[0] = |b_gate_ready_o;
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
  assign mm_o[16] = (a_lstn_reg_change_o != b_lstn_reg_change_o);
  assign act_o[16] = |b_lstn_reg_change_o;
  assign mm_o[17] = (a_tk_decl_state_o != b_tk_decl_state_o);
  assign act_o[17] = |b_tk_decl_state_o;
  assign mm_o[18] = (a_lstn_reg_state_o != b_lstn_reg_state_o);
  assign act_o[18] = |b_lstn_reg_state_o;
  assign mm_o[19] = (a_active_o != b_active_o);
  assign act_o[19] = |b_active_o;
  assign mm_o[20] = (a_msrp_fail_code_o != b_msrp_fail_code_o);
  assign act_o[20] = |b_msrp_fail_code_o;
  assign mm_o[21] = (a_msrp_fail_bridge_o != b_msrp_fail_bridge_o);
  assign act_o[21] = |b_msrp_fail_bridge_o;
  assign mm_o[22] = (a_dbg_app_state_o != b_dbg_app_state_o);
  assign act_o[22] = |b_dbg_app_state_o;
  assign mm_o[23] = (a_dbg_reg_state_o != b_dbg_reg_state_o);
  assign act_o[23] = |b_dbg_reg_state_o;
endmodule

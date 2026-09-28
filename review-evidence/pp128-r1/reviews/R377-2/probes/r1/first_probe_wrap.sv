// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer reconstruction of the unpublished #606 wiring: the processor's
// real ACMP talker (module renamed KL_acmp_talker_core in a scratch copy)
// wired to the parent's real KL_pp_maap_shim. The wrapper keeps the talker's
// port names so tb/acmp_talker/sim_main.cpp's Hn drives it unchanged:
// maap_req_ready_i becomes the SHIM's ready (an output here, observed by Hn),
// and the remaining maap_* inputs Hn writes are accepted and ignored.
// Block face: base 91:E0:F0:00:68:17, count 8, valid = block_valid_i.
`default_nettype none
module KL_acmp_talker
  import pp_pkg::*;
#(
    parameter int unsigned N_STREAM_OUT_P = 8,
    parameter int unsigned RX_SLOTS_P = 4,
    parameter int unsigned RX_SLOT_BYTES_P = 576,
    parameter int unsigned TMR_SLOTS_P = pp_pkg::PP_TIMER_SLOTS_C,
    localparam int unsigned SRC_W_C = (N_STREAM_OUT_P > 32'd1) ? $clog2(N_STREAM_OUT_P) : 32'd1,
    localparam int unsigned RXS_W_C = (RX_SLOTS_P > 32'd1) ? $clog2(RX_SLOTS_P) : 32'd1,
    localparam int unsigned RXA_W_C = $clog2(RX_SLOT_BYTES_P),
    localparam int unsigned RXL_W_C = $clog2(RX_SLOT_BYTES_P + 1),
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 32'd1) ? $clog2(TMR_SLOTS_P) : 32'd1
) (
    input  wire clk_i, input wire rst_n,
    input  wire [63:0] own_entity_id_i,
    input  wire [N_STREAM_OUT_P-1:0] cfg_src_en_i,
    input  wire [N_STREAM_OUT_P*2-1:0] cfg_src_iface_i,
    input  wire [N_STREAM_OUT_P*64-1:0] cfg_stream_id_i,
    input  wire [N_STREAM_OUT_P*2-1:0] srp_lsn_reg_state_i,
    input  wire [11:0] srp_class_vid_i,
    input  wire srp_pcp_change_i,
    input  wire txn_valid_i,
    input  wire [PP_TXN_W_C-1:0] txn_i,
    output logic txn_ready_o,
    output logic [RXS_W_C-1:0] rxs_rd_slot_o,
    output logic [RXA_W_C-1:0] rxs_rd_addr_o,
    output logic rxs_rd_en_o,
    input  wire [7:0] rxs_rd_data_i,
    input  wire [RXL_W_C-1:0] rxs_slot_len_i,
    output logic rxs_free_o,
    output logic [RXS_W_C-1:0] rxs_free_slot_o,
    output logic resp_valid_o,
    output logic [3:0] resp_msg_type_o,
    output logic [4:0] resp_status_o,
    output logic [63:0] resp_stream_id_o, resp_controller_eid_o, resp_talker_eid_o, resp_listener_eid_o,
    output logic [15:0] resp_talker_uid_o, resp_listener_uid_o,
    output logic [47:0] resp_dest_mac_o,
    output logic [15:0] resp_conn_count_o, resp_seq_id_o, resp_flags_o, resp_vlan_id_o,
    output logic [1:0] resp_if_index_o,
    output logic maap_req_valid_o,
    output logic maap_req_ready_i,            // shim ready, observed by the BFM
    output logic maap_req_release_o,
    output logic [SRC_W_C-1:0] maap_req_src_o,
    input  wire maap_rsp_valid_i,             // ignored (BFM writes it)
    input  wire maap_rsp_ok_i,                // ignored
    input  wire [47:0] maap_rsp_da_i,         // ignored
    input  wire maap_conflict_valid_i,        // ignored
    input  wire [SRC_W_C-1:0] maap_conflict_src_i, // ignored
    output logic maap_conflict_ack_o,
    output logic [N_STREAM_OUT_P-1:0] declaring_o,
    output logic gate_open_o, gate_close_o,
    output logic [SRC_W_C-1:0] gate_src_o,
    output logic [63:0] gate_stream_id_o,
    output logic [47:0] gate_da_o,
    output logic [11:0] gate_vlan_o,
    input  wire [31:0] now_ms_i,
    output logic tmr_arm_valid_o, tmr_arm_cancel_o,
    output logic [TMR_AW_C-1:0] tmr_arm_slot_o,
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o,
    output logic [31:0] tmr_arm_deadline_ms_o,
    input  wire tmr_exp_valid_i,
    input  wire [TMR_AW_C-1:0] tmr_exp_slot_i,
    input  wire [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i,
    output logic prng_draw_req_o,
    output logic [2:0] prng_draw_kind_o,
    input  wire prng_draw_busy_i, prng_draw_valid_i,
    input  wire [15:0] prng_draw_ms_i,
    input  wire block_valid_i                 // parent block state (KL_maap ANNOUNCE)
);
  logic rdy_w, rsp_v_w, rsp_ok_w, cf_v_w, cf_ack_w;
  logic [47:0] rsp_da_w;
  logic [SRC_W_C-1:0] cf_src_w;
  assign maap_req_ready_i = rdy_w;
  assign maap_conflict_ack_o = cf_ack_w;
  KL_acmp_talker_core #(.N_STREAM_OUT_P(N_STREAM_OUT_P), .RX_SLOTS_P(RX_SLOTS_P),
      .RX_SLOT_BYTES_P(RX_SLOT_BYTES_P), .TMR_SLOTS_P(TMR_SLOTS_P)) u_tk (
    .clk_i, .rst_n, .own_entity_id_i, .cfg_src_en_i, .cfg_src_iface_i, .cfg_stream_id_i,
    .srp_lsn_reg_state_i, .srp_class_vid_i, .srp_pcp_change_i, .txn_valid_i, .txn_i, .txn_ready_o,
    .rxs_rd_slot_o, .rxs_rd_addr_o, .rxs_rd_en_o, .rxs_rd_data_i, .rxs_slot_len_i, .rxs_free_o,
    .rxs_free_slot_o, .resp_valid_o, .resp_msg_type_o, .resp_status_o, .resp_stream_id_o,
    .resp_controller_eid_o, .resp_talker_eid_o, .resp_listener_eid_o, .resp_talker_uid_o,
    .resp_listener_uid_o, .resp_dest_mac_o, .resp_conn_count_o, .resp_seq_id_o, .resp_flags_o,
    .resp_vlan_id_o, .resp_if_index_o,
    .maap_req_valid_o, .maap_req_ready_i(rdy_w), .maap_req_release_o, .maap_req_src_o,
    .maap_rsp_valid_i(rsp_v_w), .maap_rsp_ok_i(rsp_ok_w), .maap_rsp_da_i(rsp_da_w),
    .maap_conflict_valid_i(cf_v_w), .maap_conflict_src_i(cf_src_w), .maap_conflict_ack_o(cf_ack_w),
    .declaring_o, .gate_open_o, .gate_close_o, .gate_src_o, .gate_stream_id_o, .gate_da_o, .gate_vlan_o,
    .now_ms_i, .tmr_arm_valid_o, .tmr_arm_cancel_o, .tmr_arm_slot_o, .tmr_arm_owner_o,
    .tmr_arm_deadline_ms_o, .tmr_exp_valid_i, .tmr_exp_slot_i, .tmr_exp_owner_i,
    .prng_draw_req_o, .prng_draw_kind_o, .prng_draw_busy_i, .prng_draw_valid_i, .prng_draw_ms_i);
  KL_pp_maap_shim #(.N_SRC_P(N_STREAM_OUT_P)) u_shim (
    .clk_i, .rst_n,
    .blk_addr_i(48'h91E0F0006817), .blk_valid_i(block_valid_i), .blk_count_i(8'(N_STREAM_OUT_P)),
    .req_valid_i(maap_req_valid_o), .req_ready_o(rdy_w), .req_release_i(maap_req_release_o),
    .req_src_i(maap_req_src_o), .rsp_valid_o(rsp_v_w), .rsp_ok_o(rsp_ok_w), .rsp_da_o(rsp_da_w),
    .conflict_valid_o(cf_v_w), .conflict_src_o(cf_src_w), .conflict_ack_i(cf_ack_w));
endmodule
`default_nettype wire

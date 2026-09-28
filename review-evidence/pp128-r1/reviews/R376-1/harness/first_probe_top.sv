// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer reconstruction: the processor's ACMP talker joined to the parent's
// unmodified MAAP shim. The talker's port list is kept so the donor's talker
// bench drives it unchanged; the MAAP inputs of the talker become outputs here
// (driven by the shim), and block_valid_i is the test-controlled block state.
// Block base and count are fixed so source s is granted 91:e0:f0:00:68:17 + s.
`default_nettype none
module first_probe_top
  import pp_pkg::*;
#(
    parameter int unsigned N_STREAM_OUT_P = 8,
    localparam int unsigned SRC_W_C = 3,
    localparam int unsigned RXS_W_C = 2,
    localparam int unsigned RXA_W_C = $clog2(576),
    localparam int unsigned RXL_W_C = $clog2(577),
    localparam int unsigned TMR_AW_C = (pp_pkg::PP_TIMER_SLOTS_C > 32'd1)
                                       ? $clog2(pp_pkg::PP_TIMER_SLOTS_C) : 32'd1
) (
    input  wire                          clk_i,
    input  wire                          rst_n,
    input  wire                          block_valid_i,
    input  wire [63:0]                   own_entity_id_i,
    input  wire [N_STREAM_OUT_P-1:0]     cfg_src_en_i,
    input  wire [N_STREAM_OUT_P*2-1:0]   cfg_src_iface_i,
    input  wire [N_STREAM_OUT_P*64-1:0]  cfg_stream_id_i,
    input  wire [N_STREAM_OUT_P*2-1:0]   srp_lsn_reg_state_i,
    input  wire [11:0]                   srp_class_vid_i,
    input  wire                          srp_pcp_change_i,
    input  wire                          txn_valid_i,
    input  wire [PP_TXN_W_C-1:0]         txn_i,
    output logic                         txn_ready_o,
    output logic [RXS_W_C-1:0]           rxs_rd_slot_o,
    output logic [RXA_W_C-1:0]           rxs_rd_addr_o,
    output logic                         rxs_rd_en_o,
    input  wire  [7:0]                   rxs_rd_data_i,
    input  wire  [RXL_W_C-1:0]           rxs_slot_len_i,
    output logic                         rxs_free_o,
    output logic [RXS_W_C-1:0]           rxs_free_slot_o,
    output logic                         resp_valid_o,
    output logic [3:0]                   resp_msg_type_o,
    output logic [4:0]                   resp_status_o,
    output logic [63:0]                  resp_stream_id_o,
    output logic [63:0]                  resp_controller_eid_o,
    output logic [63:0]                  resp_talker_eid_o,
    output logic [63:0]                  resp_listener_eid_o,
    output logic [15:0]                  resp_talker_uid_o,
    output logic [15:0]                  resp_listener_uid_o,
    output logic [47:0]                  resp_dest_mac_o,
    output logic [15:0]                  resp_conn_count_o,
    output logic [15:0]                  resp_seq_id_o,
    output logic [15:0]                  resp_flags_o,
    output logic [15:0]                  resp_vlan_id_o,
    output logic [1:0]                   resp_if_index_o,
    output logic                         maap_req_valid_o,
    output logic                         maap_req_ready_i,
    output logic                         maap_req_release_o,
    output logic [SRC_W_C-1:0]           maap_req_src_o,
    output logic                         maap_rsp_valid_i,
    output logic                         maap_rsp_ok_i,
    output logic [47:0]                  maap_rsp_da_i,
    output logic                         maap_conflict_valid_i,
    output logic [SRC_W_C-1:0]           maap_conflict_src_i,
    output logic                         maap_conflict_ack_o,
    output logic [N_STREAM_OUT_P-1:0]    declaring_o,
    output logic                         gate_open_o,
    output logic                         gate_close_o,
    output logic [SRC_W_C-1:0]           gate_src_o,
    output logic [63:0]                  gate_stream_id_o,
    output logic [47:0]                  gate_da_o,
    output logic [11:0]                  gate_vlan_o,
    input  wire  [31:0]                  now_ms_i,
    output logic                         tmr_arm_valid_o,
    output logic                         tmr_arm_cancel_o,
    output logic [TMR_AW_C-1:0]          tmr_arm_slot_o,
    output logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_o,
    output logic [31:0]                  tmr_arm_deadline_ms_o,
    input  wire                          tmr_exp_valid_i,
    input  wire  [TMR_AW_C-1:0]          tmr_exp_slot_i,
    input  wire  [PP_TIMER_OWNER_W_C-1:0] tmr_exp_owner_i,
    output logic                         prng_draw_req_o,
    output logic [2:0]                   prng_draw_kind_o,
    input  wire                          prng_draw_busy_i,
    input  wire                          prng_draw_valid_i,
    input  wire  [15:0]                  prng_draw_ms_i
);
  KL_acmp_talker #(.N_STREAM_OUT_P(N_STREAM_OUT_P)) u_talker (.*);

  KL_pp_maap_shim #(.N_SRC_P(N_STREAM_OUT_P)) u_shim (
      .clk_i, .rst_n,
      .blk_addr_i       (48'h91e0f0006817),
      .blk_valid_i      (block_valid_i),
      .blk_count_i      (8'(N_STREAM_OUT_P)),
      .req_valid_i      (maap_req_valid_o),
      .req_ready_o      (maap_req_ready_i),
      .req_release_i    (maap_req_release_o),
      .req_src_i        (maap_req_src_o),
      .rsp_valid_o      (maap_rsp_valid_i),
      .rsp_ok_o         (maap_rsp_ok_i),
      .rsp_da_o         (maap_rsp_da_i),
      .conflict_valid_o (maap_conflict_valid_i),
      .conflict_src_o   (maap_conflict_src_i),
      .conflict_ack_i   (maap_conflict_ack_o));
endmodule
`default_nettype wire

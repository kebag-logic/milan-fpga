// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R377-2): observational lockstep of KL_acmp_talker (reference)
// against KL_acmp_talker_mut (a single planted edit). Both copies receive the
// same inputs every cycle; diff_o is set when ANY output of the two differs.
`default_nettype none
module lockstep
  import pp_pkg::*;
#(
    parameter int unsigned N = 8,
    localparam int unsigned SW = $clog2(N),
    localparam int unsigned TAW = $clog2(pp_pkg::PP_TIMER_SLOTS_C)
) (
    input  wire              clk_i,
    input  wire              rst_n,
    input  wire [N-1:0]      cfg_src_en_i,
    input  wire [N*2-1:0]    cfg_src_iface_i,
    input  wire [N*2-1:0]    srp_lsn_reg_state_i,
    input  wire              srp_pcp_change_i,
    input  wire              txn_valid_i,
    input  wire [1:0]        t_msg_i,
    input  wire [3:0]        t_uid_i,
    input  wire [1:0]        t_if_i,
    input  wire [2:0]        t_slot_i,
    input  wire              t_tgt_i,
    input  wire [15:0]       t_seq_i,
    input  wire [7:0]        rxs_rd_data_i,
    input  wire [9:0]        rxs_slot_len_i,
    input  wire              maap_req_ready_i,
    input  wire              maap_rsp_valid_i,
    input  wire              maap_rsp_ok_i,
    input  wire [47:0]       maap_rsp_da_i,
    input  wire              maap_conflict_valid_i,
    input  wire [SW-1:0]     maap_conflict_src_i,
    input  wire [31:0]       now_ms_i,
    input  wire              tmr_exp_valid_i,
    input  wire [TAW-1:0]    tmr_exp_slot_i,
    input  wire [7:0]        tmr_exp_owner_i,
    input  wire              prng_draw_busy_i,
    input  wire              prng_draw_valid_i,
    input  wire [15:0]       prng_draw_ms_i,
    output logic             diff_o,
    output logic             a_txn_ready_o,
    output logic             a_maap_req_valid_o,
    output logic             a_maap_req_release_o,
    output logic [SW-1:0]    a_maap_req_src_o,
    output logic             a_prng_draw_req_o,
    output logic             a_resp_valid_o,
    output logic [4:0]       a_resp_status_o,
    output logic [N-1:0]     a_declaring_o
);
  localparam logic [63:0] OWN_C = 64'h0011_2233_4455_6677;
  logic [3:0] mt_w;
  always_comb begin
    unique case (t_msg_i)
      2'd0: mt_w = 4'd0;   // PROBE_TX
      2'd1: mt_w = 4'd2;   // DISCONNECT_TX
      2'd2: mt_w = 4'd4;   // GET_TX_STATE
      default: mt_w = 4'd12; // GET_TX_CONNECTION
    endcase
  end
  pp_txn_t t_w;
  always_comb begin
    t_w = '0;
    t_w.interface_index    = t_if_i;
    t_w.protocol           = PP_PROTO_ACMP;
    t_w.msg_type           = mt_w;
    t_w.controller_eid     = 64'hC0C0_0000_0000_0001;
    t_w.target_eid         = t_tgt_i ? OWN_C : 64'hBAD0;
    t_w.sequence_id        = t_seq_i;
    t_w.operands.unique_id = {12'd0, t_uid_i};
    t_w.rx_slot            = t_slot_i;
  end

  // Every output of each copy, zero-extended into one wide compare vector.
  logic [1023:0] oa, ob;

`define LS_INST(NAME, MOD, OUT) \
  if (1) begin : NAME \
    logic txn_ready, rxs_rd_en, rxs_free, resp_valid, maap_req_valid, \
          maap_req_release, maap_conflict_ack, gate_open, gate_close, \
          tmr_arm_valid, tmr_arm_cancel, prng_draw_req; \
    logic [1:0] rxs_rd_slot, rxs_free_slot, resp_if; \
    logic [9:0] rxs_rd_addr; \
    logic [3:0] resp_mt; logic [4:0] resp_st; \
    logic [63:0] resp_sid, resp_ceid, resp_teid, resp_leid, gate_sid; \
    logic [15:0] resp_tuid, resp_luid, resp_cc, resp_seq, resp_flags, resp_vlan; \
    logic [47:0] resp_dmac, gate_da; \
    logic [SW-1:0] maap_req_src, gate_src; \
    logic [N-1:0] declaring; \
    logic [11:0] gate_vlan; \
    logic [TAW-1:0] tmr_slot; logic [7:0] tmr_owner; logic [31:0] tmr_dl; \
    logic [2:0] prng_kind; \
    MOD #(.N_STREAM_OUT_P(N)) u ( \
      .clk_i, .rst_n, .own_entity_id_i(OWN_C), .cfg_src_en_i, .cfg_src_iface_i, \
      .cfg_stream_id_i({N{64'h5151_0000_0000_0000}} ^ {N{64'(N)}}), \
      .srp_lsn_reg_state_i, .srp_class_vid_i(12'd2), .srp_pcp_change_i, \
      .txn_valid_i, .txn_i(t_w), .txn_ready_o(txn_ready), \
      .rxs_rd_slot_o(rxs_rd_slot), .rxs_rd_addr_o(rxs_rd_addr), .rxs_rd_en_o(rxs_rd_en), \
      .rxs_rd_data_i, .rxs_slot_len_i, .rxs_free_o(rxs_free), .rxs_free_slot_o(rxs_free_slot), \
      .resp_valid_o(resp_valid), .resp_msg_type_o(resp_mt), .resp_status_o(resp_st), \
      .resp_stream_id_o(resp_sid), .resp_controller_eid_o(resp_ceid), \
      .resp_talker_eid_o(resp_teid), .resp_listener_eid_o(resp_leid), \
      .resp_talker_uid_o(resp_tuid), .resp_listener_uid_o(resp_luid), \
      .resp_dest_mac_o(resp_dmac), .resp_conn_count_o(resp_cc), .resp_seq_id_o(resp_seq), \
      .resp_flags_o(resp_flags), .resp_vlan_id_o(resp_vlan), .resp_if_index_o(resp_if), \
      .maap_req_valid_o(maap_req_valid), .maap_req_ready_i, \
      .maap_req_release_o(maap_req_release), .maap_req_src_o(maap_req_src), \
      .maap_rsp_valid_i, .maap_rsp_ok_i, .maap_rsp_da_i, .maap_conflict_valid_i, \
      .maap_conflict_src_i, .maap_conflict_ack_o(maap_conflict_ack), \
      .declaring_o(declaring), .gate_open_o(gate_open), .gate_close_o(gate_close), \
      .gate_src_o(gate_src), .gate_stream_id_o(gate_sid), .gate_da_o(gate_da), \
      .gate_vlan_o(gate_vlan), .now_ms_i, .tmr_arm_valid_o(tmr_arm_valid), \
      .tmr_arm_cancel_o(tmr_arm_cancel), .tmr_arm_slot_o(tmr_slot), \
      .tmr_arm_owner_o(tmr_owner), .tmr_arm_deadline_ms_o(tmr_dl), \
      .tmr_exp_valid_i, .tmr_exp_slot_i, .tmr_exp_owner_i, \
      .prng_draw_req_o(prng_draw_req), .prng_draw_kind_o(prng_kind), \
      .prng_draw_busy_i, .prng_draw_valid_i, .prng_draw_ms_i); \
    assign OUT = 1024'({txn_ready, resp_mt, resp_st, resp_sid, resp_ceid, resp_teid, \
                  resp_dmac, resp_tuid, resp_luid, resp_cc, resp_seq, resp_flags, \
                  resp_vlan, resp_if, rxs_rd_slot, resp_valid, maap_req_valid, \
                  maap_req_src, maap_req_release, declaring, 2'b00, gate_src, \
                  gate_sid, gate_da, gate_vlan, prng_kind, gate_open, gate_close, \
                  tmr_slot, tmr_owner, tmr_dl, tmr_arm_valid, 3'b000, \
                  tmr_arm_cancel, prng_draw_req, maap_conflict_ack, rxs_free_slot, \
                  (rxs_rd_en ? rxs_rd_addr : 10'd0), rxs_rd_en, rxs_free, \
                  resp_leid}); \
  end

  `LS_INST(ref_i, KL_acmp_talker, oa)
  `LS_INST(mut_i, KL_acmp_talker_mut, ob)

  assign diff_o = (oa != ob);

  assign a_txn_ready_o        = ref_i.txn_ready;
  assign a_maap_req_valid_o   = ref_i.maap_req_valid;
  assign a_maap_req_release_o = ref_i.maap_req_release;
  assign a_maap_req_src_o     = ref_i.maap_req_src;
  assign a_prng_draw_req_o    = ref_i.prng_draw_req;
  assign a_resp_valid_o       = ref_i.resp_valid;
  assign a_resp_status_o      = ref_i.resp_st;
  assign a_declaring_o        = ref_i.declaring;
endmodule
`default_nettype wire

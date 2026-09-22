/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tb_dispatch_top.sv
//  Project     : IEEE 1722.1 protocol processor — dispatch suite harness
//
//  Description : Pure wiring: KL_pp_normalizer -> KL_pp_dispatch, so the
//                suite exercises the whole 03 §4/§5 normalize -> enqueue ->
//                pop path through one top. No logic of its own beyond the
//                two-signal seam (n2d_*) — anything else would shadow the
//                DUTs.
//---------------------------------------------------------------------------//
`default_nettype none

module tb_dispatch_top
  import pp_pkg::*;
#(
    parameter int unsigned ADP_DEPTH_P  = 4,
    parameter int unsigned ACMP_DEPTH_P = 4,
    parameter int unsigned AECP_DEPTH_P = 4,
    parameter int unsigned MAAP_DEPTH_P = 2
) (
    input  wire                    clk_i,
    input  wire                    rst_n,

    input  wire  [31:0]            now_ms_i,
    input  wire  [15:0]            budget_adp_ms_i,
    input  wire  [15:0]            budget_acmp_ms_i,
    input  wire  [15:0]            budget_aecp_ms_i,

    input  wire                    rx_valid_i,
    output logic                   rx_ready_o,
    input  wire  [1:0]             rx_if_index_i,
    input  wire  [2:0]             rx_protocol_i,
    input  wire  [3:0]             rx_msg_type_i,
    input  wire  [4:0]             rx_status_i,
    input  wire  [10:0]            rx_cdl_i,
    input  wire  [47:0]            rx_src_mac_i,
    input  wire  [63:0]            rx_controller_eid_i,
    input  wire  [63:0]            rx_target_eid_i,
    input  wire  [15:0]            rx_sequence_id_i,
    input  wire                    rx_u_i,
    input  wire                    rx_cr_i,
    input  wire  [15:0]            rx_opcode_i,
    input  wire  [63:0]            rx_operands_i,
    input  wire  [2:0]             rx_slot_i,

    output logic                   hz_valid_o,
    output logic [2:0]             hz_protocol_o,
    output logic [15:0]            hz_opcode_o,
    input  wire  [3:0]             hz_class_i,
    input  wire  [15:0]            hz_key_i,

    input  wire                    tmr_valid_i,
    input  wire  [PP_TXN_W_C-1:0]  tmr_txn_i,
    output logic                   tmr_ready_o,
    input  wire                    self_valid_i,
    input  wire  [PP_TXN_W_C-1:0]  self_txn_i,
    output logic                   self_ready_o,
    input  wire                    mgmt_valid_i,
    input  wire  [PP_TXN_W_C-1:0]  mgmt_txn_i,
    output logic                   mgmt_ready_o,

    output logic                   adp_txn_valid_o,
    output logic [PP_TXN_W_C-1:0]  adp_txn_o,
    input  wire                    adp_txn_ready_i,
    output logic                   acmp_txn_valid_o,
    output logic [PP_TXN_W_C-1:0]  acmp_txn_o,
    input  wire                    acmp_txn_ready_i,
    output logic                   aecp_txn_valid_o,
    output logic [PP_TXN_W_C-1:0]  aecp_txn_o,
    input  wire                    aecp_txn_ready_i,
    output logic                   maap_txn_valid_o,
    output logic [PP_TXN_W_C-1:0]  maap_txn_o,
    input  wire                    maap_txn_ready_i,

    output logic [7:0]             adp_level_o,
    output logic [7:0]             acmp_level_o,
    output logic [7:0]             aecp_level_o,
    output logic [7:0]             maap_level_o,
    output logic [15:0]            adp_stall_count_o,
    output logic [15:0]            acmp_stall_count_o,
    output logic [15:0]            aecp_stall_count_o,
    output logic [15:0]            maap_stall_count_o
);

  logic                   n2d_valid_w;
  logic [PP_TXN_W_C-1:0]  n2d_txn_w;
  logic                   n2d_ready_w;

  KL_pp_normalizer u_norm (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .now_ms_i            (now_ms_i),
      .budget_adp_ms_i     (budget_adp_ms_i),
      .budget_acmp_ms_i    (budget_acmp_ms_i),
      .budget_aecp_ms_i    (budget_aecp_ms_i),
      .rx_valid_i          (rx_valid_i),
      .rx_ready_o          (rx_ready_o),
      .rx_if_index_i       (rx_if_index_i),
      .rx_protocol_i       (rx_protocol_i),
      .rx_msg_type_i       (rx_msg_type_i),
      .rx_status_i         (rx_status_i),
      .rx_cdl_i            (rx_cdl_i),
      .rx_src_mac_i        (rx_src_mac_i),
      .rx_controller_eid_i (rx_controller_eid_i),
      .rx_target_eid_i     (rx_target_eid_i),
      .rx_sequence_id_i    (rx_sequence_id_i),
      .rx_u_i              (rx_u_i),
      .rx_cr_i             (rx_cr_i),
      .rx_opcode_i         (rx_opcode_i),
      .rx_operands_i       (rx_operands_i),
      .rx_slot_i           (rx_slot_i),
      .hz_valid_o          (hz_valid_o),
      .hz_protocol_o       (hz_protocol_o),
      .hz_opcode_o         (hz_opcode_o),
      .hz_class_i          (hz_class_i),
      .hz_key_i            (hz_key_i),
      .tmr_valid_i         (tmr_valid_i),
      .tmr_txn_i           (tmr_txn_i),
      .tmr_ready_o         (tmr_ready_o),
      .self_valid_i        (self_valid_i),
      .self_txn_i          (self_txn_i),
      .self_ready_o        (self_ready_o),
      .mgmt_valid_i        (mgmt_valid_i),
      .mgmt_txn_i          (mgmt_txn_i),
      .mgmt_ready_o        (mgmt_ready_o),
      .txn_valid_o         (n2d_valid_w),
      .txn_o               (n2d_txn_w),
      .txn_ready_i         (n2d_ready_w)
  );

  KL_pp_dispatch #(
      .ADP_DEPTH_P  (ADP_DEPTH_P),
      .ACMP_DEPTH_P (ACMP_DEPTH_P),
      .AECP_DEPTH_P (AECP_DEPTH_P),
      .MAAP_DEPTH_P (MAAP_DEPTH_P)
  ) u_disp (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .enq_valid_i        (n2d_valid_w),
      .enq_txn_i          (n2d_txn_w),
      .enq_ready_o        (n2d_ready_w),
      .adp_txn_valid_o    (adp_txn_valid_o),
      .adp_txn_o          (adp_txn_o),
      .adp_txn_ready_i    (adp_txn_ready_i),
      .acmp_txn_valid_o   (acmp_txn_valid_o),
      .acmp_txn_o         (acmp_txn_o),
      .acmp_txn_ready_i   (acmp_txn_ready_i),
      .aecp_txn_valid_o   (aecp_txn_valid_o),
      .aecp_txn_o         (aecp_txn_o),
      .aecp_txn_ready_i   (aecp_txn_ready_i),
      .maap_txn_valid_o   (maap_txn_valid_o),
      .maap_txn_o         (maap_txn_o),
      .maap_txn_ready_i   (maap_txn_ready_i),
      .adp_level_o        (adp_level_o),
      .acmp_level_o       (acmp_level_o),
      .aecp_level_o       (aecp_level_o),
      .maap_level_o       (maap_level_o),
      .adp_stall_count_o  (adp_stall_count_o),
      .acmp_stall_count_o (acmp_stall_count_o),
      .aecp_stall_count_o (aecp_stall_count_o),
      .maap_stall_count_o (maap_stall_count_o)
  );

endmodule : tb_dispatch_top
`default_nettype wire

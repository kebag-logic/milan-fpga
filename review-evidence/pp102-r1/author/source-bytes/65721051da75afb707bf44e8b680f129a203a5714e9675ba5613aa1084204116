/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : maap_wrap.sv
//  Project     : IEEE 1722.1 protocol processor — maap suite harness
//
//  Description : KL_pp_maap with its REAL services: KL_pp_prng (the kinds
//                5/6/7 it draws), KL_pp_timer_service (time compressed to
//                1 ms = 10 clk so the Annex B intervals run for real at
//                simulation speed) and KL_pp_tx_slots (the frame bytes the
//                suite grades come out of the pool's serialize port, driven
//                by the C++ side playing the TX arbiter's lane). The
//                dispatch record is packed HERE from flat ports — pure
//                wiring, no logic that could shadow the DUT. The timer
//                slots are deliberately based at 1 (not 0) so a
//                base-parameterization defect cannot hide.
//---------------------------------------------------------------------------//
`default_nettype none

module maap_wrap
  import pp_pkg::*;
(
    input  wire         clk_i,
    input  wire         rst_n,

    // quasi-static configuration + level status
    input  wire         cfg_en_i,
    input  wire  [7:0]  cfg_count_i,
    input  wire  [15:0] cfg_seed_offset_i,
    input  wire         cfg_seed_valid_i,
    input  wire  [47:0] own_mac_i,
    input  wire  [63:0] entity_id_i,
    input  wire         link_up_i,

    // flat RX record injection (packed to pp_txn_t here)
    input  wire         txn_valid_i,
    input  wire  [3:0]  txn_msg_i,
    input  wire  [4:0]  txn_status_i,
    input  wire  [47:0] txn_src_mac_i,
    input  wire  [63:0] txn_req_i,      // requested_start(48) + count(16)
    input  wire  [63:0] txn_conf_i,     // conflict_start(48) + count(16)
    output logic        txn_ready_o,

    // the allocator seam (the shim's processor face)
    input  wire         alloc_req_valid_i,
    output logic        alloc_req_ready_o,
    input  wire         alloc_req_release_i,
    input  wire  [2:0]  alloc_req_src_i,
    output logic        alloc_rsp_valid_o,
    output logic        alloc_rsp_ok_o,
    output logic [47:0] alloc_rsp_da_o,
    output logic        conflict_valid_o,
    output logic [2:0]  conflict_src_o,
    input  wire         conflict_ack_i,

    // claim publication
    output logic [47:0] addr_o,
    output logic        addr_valid_o,
    output logic [1:0]  state_o,
    output logic [7:0]  conflicts_o,
    output logic [7:0]  defends_o,

    // TX lane (C++ plays the arbiter) + the pool's serialize port
    output logic        txreq_valid_o,
    output logic [2:0]  txreq_slot_o,
    input  wire         txreq_ready_i,
    input  wire         ser_req_i,
    input  wire  [2:0]  ser_slot_i,
    output logic        ser_valid_o,
    output logic [7:0]  ser_data_o,
    output logic        ser_last_o,
    input  wire         ser_ready_i,

    // observability
    output logic [31:0] now_ms_o,
    output logic        rxs_free_o
);

  // 1 ms = 1 x 10 clk; the 4-slot sweep (6 cycles) fits inside the tick
  localparam int unsigned TB_SLOTS_C = 4;

  logic        prng_req_w;
  logic [2:0]  prng_kind_w;
  logic        prng_busy_w, prng_valid_w;
  logic [15:0] prng_ms_w;
  logic [63:0] prng_lfsr_nc_w;
  logic        prng_seeded_nc_w;

  KL_pp_prng u_prng (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .entity_id_i  (entity_id_i),
      .link_up_i    (link_up_i),
      .draw_req_i   (prng_req_w),
      .draw_kind_i  (prng_kind_w),
      .draw_busy_o  (prng_busy_w),
      .draw_valid_o (prng_valid_w),
      .draw_ms_o    (prng_ms_w),
      .dbg_lfsr_o   (prng_lfsr_nc_w),
      .dbg_seeded_o (prng_seeded_nc_w)
  );

  logic        tick_ms_nc_w;
  logic        arm_valid_w, arm_cancel_w;
  logic [1:0]  arm_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] arm_owner_w;
  logic [31:0] arm_deadline_w;
  logic        exp_valid_w;
  logic [1:0]  exp_slot_w;
  logic [PP_TIMER_OWNER_W_C-1:0] exp_owner_w;

  KL_pp_timer_service #(
      .SLOTS_P  (TB_SLOTS_C),
      .DIV_US_P (1),
      .DIV_MS_P (10)
  ) u_timer (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .tick_ms_o         (tick_ms_nc_w),
      .now_ms_o          (now_ms_o),
      .arm_valid_i       (arm_valid_w),
      .arm_cancel_i      (arm_cancel_w),
      .arm_slot_i        (arm_slot_w),
      .arm_owner_i       (arm_owner_w),
      .arm_deadline_ms_i (arm_deadline_w),
      .exp_valid_o       (exp_valid_w),
      .exp_slot_o        (exp_slot_w),
      .exp_owner_o       (exp_owner_w)
  );

  logic        txs_alloc_req_w, txs_oversize_w, txs_alloc_gnt_w;
  logic [2:0]  txs_alloc_slot_w;
  logic [2:0]  txs_wr_slot_w;
  logic [10:0] txs_wr_addr_w, txs_wr_len_w;
  logic        txs_wr_valid_w, txs_wr_commit_w;
  logic [7:0]  txs_wr_data_w;
  logic [4:0]  txs_ready_nc_w;
  logic [2:0]  txs_free_nc_w;

  KL_pp_tx_slots #(
      .TX_STD_SLOTS_P      (4),
      .TX_STD_BYTES_P      (576),
      .TX_OVERSIZE_BYTES_P (1600)
  ) u_tx_slots (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .alloc_req_i   (txs_alloc_req_w),
      .oversize_i    (txs_oversize_w),
      .alloc_gnt_o   (txs_alloc_gnt_w),
      .alloc_slot_o  (txs_alloc_slot_w),
      .wr_slot_i     (txs_wr_slot_w),
      .wr_addr_i     (txs_wr_addr_w),
      .wr_valid_i    (txs_wr_valid_w),
      .wr_data_i     (txs_wr_data_w),
      .wr_commit_i   (txs_wr_commit_w),
      .wr_len_i      (txs_wr_len_w),
      .hold_valid_i  (1'b0),
      .hold_slot_i   ('0),
      .release_valid_i(1'b0),
      .release_slot_i('0),
      .ser_req_i     (ser_req_i),
      .ser_slot_i    (ser_slot_i),
      .ser_valid_o   (ser_valid_o),
      .ser_data_o    (ser_data_o),
      .ser_last_o    (ser_last_o),
      .ser_ready_i   (ser_ready_i),
      .slots_ready_o (txs_ready_nc_w),
      .slots_free_o  (txs_free_nc_w)
  );

  // ---- the record, packed from the flat ports (wiring only) --------------
  pp_txn_t txn_w;
  always_comb begin : txn_pack
    txn_w                  = pp_txn_t'({PP_TXN_W_C{1'b0}});
    txn_w.origin           = PP_ORIGIN_RX;
    txn_w.protocol         = PP_PROTO_MAAP;
    txn_w.msg_type         = txn_msg_i;
    txn_w.status_in        = txn_status_i;
    txn_w.cdl              = 11'd16;
    txn_w.src_mac          = txn_src_mac_i;
    txn_w.controller_eid   = txn_req_i;
    txn_w.opcode           = {12'd0, txn_msg_i};
    txn_w.operands         = pp_operands_t'(txn_conf_i);
    txn_w.rx_slot          = PP_SLOT_NULL_C;
  end

  logic [2:0] rxs_free_slot_nc_w;

  KL_pp_maap #(
      .N_SRC_P             (8),
      .RX_SLOTS_P          (4),
      .TMR_SLOTS_P         (TB_SLOTS_C),
      .TMR_SLOT_BASE_P     (1),
      .TMR_OWNER_BASE_P    (PP_OWN_MAAP_C),
      .TX_STD_SLOTS_P      (4),
      .TX_OVERSIZE_BYTES_P (1600)
  ) u_dut (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .cfg_en_i            (cfg_en_i),
      .cfg_count_i         (cfg_count_i),
      .cfg_seed_offset_i   (cfg_seed_offset_i),
      .cfg_seed_valid_i    (cfg_seed_valid_i),
      .own_mac_i           (own_mac_i),
      .link_up_i           (link_up_i),
      .txn_valid_i         (txn_valid_i),
      .txn_i               (PP_TXN_W_C'(txn_w)),
      .txn_ready_o         (txn_ready_o),
      .rxs_free_o          (rxs_free_o),
      .rxs_free_slot_o     (rxs_free_slot_nc_w),
      .prng_draw_req_o     (prng_req_w),
      .prng_draw_kind_o    (prng_kind_w),
      .prng_draw_busy_i    (prng_busy_w),
      .prng_draw_valid_i   (prng_valid_w),
      .prng_draw_ms_i      (prng_ms_w),
      .now_ms_i            (now_ms_o),
      .tmr_arm_valid_o     (arm_valid_w),
      .tmr_arm_cancel_o    (arm_cancel_w),
      .tmr_arm_slot_o      (arm_slot_w),
      .tmr_arm_owner_o     (arm_owner_w),
      .tmr_arm_deadline_ms_o (arm_deadline_w),
      .tmr_exp_valid_i     (exp_valid_w),
      .tmr_exp_slot_i      (exp_slot_w),
      .tmr_exp_owner_i     (exp_owner_w),
      .txs_alloc_req_o     (txs_alloc_req_w),
      .txs_oversize_o      (txs_oversize_w),
      .txs_alloc_gnt_i     (txs_alloc_gnt_w),
      .txs_alloc_slot_i    (txs_alloc_slot_w),
      .txs_wr_slot_o       (txs_wr_slot_w),
      .txs_wr_addr_o       (txs_wr_addr_w),
      .txs_wr_valid_o      (txs_wr_valid_w),
      .txs_wr_data_o       (txs_wr_data_w),
      .txs_wr_commit_o     (txs_wr_commit_w),
      .txs_wr_len_o        (txs_wr_len_w),
      .txreq_valid_o       (txreq_valid_o),
      .txreq_slot_o        (txreq_slot_o),
      .txreq_ready_i       (txreq_ready_i),
      .alloc_req_valid_i   (alloc_req_valid_i),
      .alloc_req_ready_o   (alloc_req_ready_o),
      .alloc_req_release_i (alloc_req_release_i),
      .alloc_req_src_i     (alloc_req_src_i),
      .alloc_rsp_valid_o   (alloc_rsp_valid_o),
      .alloc_rsp_ok_o      (alloc_rsp_ok_o),
      .alloc_rsp_da_o      (alloc_rsp_da_o),
      .conflict_valid_o    (conflict_valid_o),
      .conflict_src_o      (conflict_src_o),
      .conflict_ack_i      (conflict_ack_i),
      .addr_o              (addr_o),
      .addr_valid_o        (addr_valid_o),
      .state_o             (state_o),
      .conflicts_o         (conflicts_o),
      .defends_o           (defends_o)
  );

endmodule : maap_wrap
`default_nettype wire

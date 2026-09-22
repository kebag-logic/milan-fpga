/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tb_adp_top.sv
//  Project     : IEEE 1722.1 protocol processor — ADP engine suite harness
//
//  Description : Pure wiring: KL_adp_engine + the REAL KL_pp_prng, so the
//                suite proves the two DISTINCT delay-draw kinds (T-ADP-
//                DELAY-START vs T-ADP-DELAY, review §8 item 5) against the
//                real rejection sampler, not a stub. The draw port is
//                tapped (tap_*) for the statistical range checks. Every
//                other face (dispatch, rx/tx slots, timer service, events)
//                passes straight through to the C++ models. No logic of
//                its own beyond the five-signal prng seam.
//---------------------------------------------------------------------------//
`default_nettype none

module tb_adp_top
  import pp_pkg::*;
#(
    parameter int unsigned N_IF_P   = 1,
    parameter int unsigned N_SINK_P = 8
) (
    input  wire                    clk_i,
    input  wire                    rst_n,

    input  wire                    entity_enable_i,
    input  wire  [N_IF_P-1:0]      link_up_i,
    input  wire  [N_IF_P-1:0]      gm_change_i,
    input  wire  [N_IF_P*64-1:0]   gm_id_i,
    input  wire  [N_IF_P*8-1:0]    gptp_domain_i,

    input  wire  [63:0]            entity_id_i,
    input  wire  [63:0]            entity_model_id_i,
    input  wire  [47:0]            own_mac_i,
    input  wire  [15:0]            talker_sources_i,
    input  wire  [15:0]            talker_caps_i,
    input  wire  [15:0]            listener_sinks_i,
    input  wire  [15:0]            listener_caps_i,
    input  wire  [15:0]            current_cfg_i,
    input  wire  [15:0]            identify_index_i,

    input  wire                    txn_valid_i,
    input  wire  [PP_TXN_W_C-1:0]  txn_i,
    output logic                   txn_ready_o,

    output logic [1:0]             rxs_rd_slot_o,
    output logic [9:0]             rxs_rd_addr_o,
    output logic                   rxs_rd_en_o,
    input  wire  [7:0]             rxs_rd_data_i,
    output logic                   rxs_free_o,
    output logic [1:0]             rxs_free_slot_o,

    input  wire  [31:0]            now_ms_i,
    output logic                   tmr_arm_valid_o,
    output logic                   tmr_arm_cancel_o,
    output logic [6:0]             tmr_arm_slot_o,
    output logic [7:0]             tmr_arm_owner_o,
    output logic [31:0]            tmr_arm_deadline_ms_o,
    input  wire                    tmr_exp_valid_i,
    input  wire  [6:0]             tmr_exp_slot_i,
    input  wire  [7:0]             tmr_exp_owner_i,

    output logic                   txs_alloc_req_o,
    output logic                   txs_oversize_o,
    input  wire                    txs_alloc_gnt_i,
    input  wire  [2:0]             txs_alloc_slot_i,
    output logic [2:0]             txs_wr_slot_o,
    output logic [10:0]            txs_wr_addr_o,
    output logic                   txs_wr_valid_o,
    output logic [7:0]             txs_wr_data_o,
    output logic                   txs_wr_commit_o,
    output logic [10:0]            txs_wr_len_o,

    output logic                   txreq_valid_o,
    output logic [2:0]             txreq_slot_o,
    output logic [0:0]             txreq_if_o,

    input  wire  [N_SINK_P-1:0]    bound_i,
    input  wire  [N_SINK_P*64-1:0] bound_talker_eid_i,

    output logic                   evt_valid_o,
    output logic                   evt_departed_o,
    output logic [2:0]             evt_sink_o,
    output logic [N_IF_P-1:0]      gm_changed_tick_o,

    output logic [N_IF_P*2-1:0]    dbg_adv_state_o,
    output logic [N_IF_P*32-1:0]   dbg_avail_index_o,
    output logic [N_SINK_P-1:0]    dbg_tk_discovered_o,

    // ---- KL_pp_prng draw-port taps (observability) ------------------------
    output logic                   tap_draw_req_o,
    output logic [2:0]             tap_draw_kind_o,
    output logic                   tap_draw_busy_o,
    output logic                   tap_draw_valid_o,
    output logic [15:0]            tap_draw_ms_o,
    output logic                   tap_prng_seeded_o
);

  logic        p_req_w;
  logic [2:0]  p_kind_w;
  logic        p_busy_w;
  logic        p_valid_w;
  logic [15:0] p_ms_w;
  logic [63:0] p_dbg_lfsr_w;
  logic        p_seeded_w;

  KL_adp_engine #(
      .N_IF_P   (N_IF_P),
      .N_SINK_P (N_SINK_P)
  ) u_engine (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_enable_i       (entity_enable_i),
      .link_up_i             (link_up_i),
      .gm_change_i           (gm_change_i),
      .gm_id_i               (gm_id_i),
      .gptp_domain_i         (gptp_domain_i),
      .entity_id_i           (entity_id_i),
      .entity_model_id_i     (entity_model_id_i),
      .own_mac_i             (own_mac_i),
      .talker_sources_i      (talker_sources_i),
      .talker_caps_i         (talker_caps_i),
      .listener_sinks_i      (listener_sinks_i),
      .listener_caps_i       (listener_caps_i),
      .current_cfg_i         (current_cfg_i),
      .identify_index_i      (identify_index_i),
      .txn_valid_i           (txn_valid_i),
      .txn_i                 (txn_i),
      .txn_ready_o           (txn_ready_o),
      .rxs_rd_slot_o         (rxs_rd_slot_o),
      .rxs_rd_addr_o         (rxs_rd_addr_o),
      .rxs_rd_en_o           (rxs_rd_en_o),
      .rxs_rd_data_i         (rxs_rd_data_i),
      .rxs_free_o            (rxs_free_o),
      .rxs_free_slot_o       (rxs_free_slot_o),
      .prng_draw_req_o       (p_req_w),
      .prng_draw_kind_o      (p_kind_w),
      .prng_draw_busy_i      (p_busy_w),
      .prng_draw_valid_i     (p_valid_w),
      .prng_draw_ms_i        (p_ms_w),
      .now_ms_i              (now_ms_i),
      .tmr_arm_valid_o       (tmr_arm_valid_o),
      .tmr_arm_cancel_o      (tmr_arm_cancel_o),
      .tmr_arm_slot_o        (tmr_arm_slot_o),
      .tmr_arm_owner_o       (tmr_arm_owner_o),
      .tmr_arm_deadline_ms_o (tmr_arm_deadline_ms_o),
      .tmr_exp_valid_i       (tmr_exp_valid_i),
      .tmr_exp_slot_i        (tmr_exp_slot_i),
      .tmr_exp_owner_i       (tmr_exp_owner_i),
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
      .txreq_if_o            (txreq_if_o),
      .bound_i               (bound_i),
      .bound_talker_eid_i    (bound_talker_eid_i),
      .evt_valid_o           (evt_valid_o),
      .evt_departed_o        (evt_departed_o),
      .evt_sink_o            (evt_sink_o),
      .gm_changed_tick_o     (gm_changed_tick_o),
      .dbg_adv_state_o       (dbg_adv_state_o),
      .dbg_avail_index_o     (dbg_avail_index_o),
      .dbg_tk_discovered_o   (dbg_tk_discovered_o)
  );

  KL_pp_prng u_prng (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .entity_id_i  (entity_id_i),
      .link_up_i    (link_up_i[0]),
      .draw_req_i   (p_req_w),
      .draw_kind_i  (p_kind_w),
      .draw_busy_o  (p_busy_w),
      .draw_valid_o (p_valid_w),
      .draw_ms_o    (p_ms_w),
      .dbg_lfsr_o   (p_dbg_lfsr_w),
      .dbg_seeded_o (p_seeded_w)
  );

  assign tap_draw_req_o    = p_req_w;
  assign tap_draw_kind_o   = p_kind_w;
  assign tap_draw_busy_o   = p_busy_w;
  assign tap_draw_valid_o  = p_valid_w;
  assign tap_draw_ms_o     = p_ms_w;
  assign tap_prng_seeded_o = p_seeded_w;

  // dbg_lfsr deliberately unconnected upward — the suite checks draws, not
  // raw state; keep the wrapper face minimal
  logic [63:0] unused_lfsr_w;
  assign unused_lfsr_w = p_dbg_lfsr_w;

endmodule : tb_adp_top
`default_nettype wire

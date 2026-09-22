/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : srp_top_wrap.sv
//  Project     : IEEE 1722.1 protocol processor — srp_top suite
//
//  Description : End-to-end harness: the REAL KL_srp_top with the REAL
//                shared services around it — KL_pp_tx_slots (frames are
//                checked byte-exact off its serialize face, the C++ side
//                playing the 03 §8 TX arbiter), KL_pp_timer_service
//                (time-compressed: 1 ms = 40 clk cycles so the 200 ms
//                T-MRP-JOIN, 5 s T-MRP-LEAVE and the PRNG-drawn 10-15 s
//                T-MRP-LEAVEALL all run for real; SLOTS_P = 32 keeps the
//                sweep, 34 cycles, inside the 40-cycle ms) and KL_pp_prng
//                (kind-3 LeaveAll draws, seeded by the first link-up).
//                Only the engine's external contract is exposed: the
//                header-stripped MRP byte stream in, the 02 §4.1 class-B
//                service port, the class-C strobes and the F02.10 class-D
//                dictionary out.
//---------------------------------------------------------------------------//
`default_nettype none

module srp_top_wrap (
    input  wire         clk_i,
    input  wire         rst_n,

    // static identity / config
    input  wire  [47:0] own_mac_i,
    input  wire  [63:0] entity_id_i,
    input  wire         link_up_i,
    input  wire         p2p_i,
    input  wire         cfg_rank_i,
    input  wire  [31:0] cfg_acc_lat_ns_i,
    input  wire  [31:0] port_rate_bps_i,

    // MRP byte stream in (header-stripped: ProtocolVersion first)
    input  wire         mrp_valid_i,
    input  wire  [7:0]  mrp_data_i,
    input  wire         mrp_last_i,
    input  wire         mrp_msrp_i,
    output logic        mrp_ready_o,

    // class-B service port
    input  wire         req_valid_i,
    output logic        req_ready_o,
    input  wire  [2:0]  req_op_i,
    input  wire  [7:0]  req_index_i,
    input  wire  [63:0] req_stream_id_i,
    input  wire  [47:0] req_da_i,
    input  wire  [11:0] req_vid_i,
    input  wire  [15:0] req_max_frame_i,
    input  wire  [15:0] req_max_interval_i,
    input  wire  [1:0]  req_lstn_state_i,
    output logic        rsp_valid_o,
    output logic [1:0]  rsp_status_o,
    output logic [31:0] rsp_data_o,

    // TX capture (the C++ side is the 03 §8 arbiter)
    output logic        txreq_valid_o,
    output logic [2:0]  txreq_slot_o,
    input  wire         txreq_ready_i,
    input  wire         ser_req_i,
    input  wire  [2:0]  ser_slot_i,
    output logic        ser_valid_o,
    output logic [7:0]  ser_data_o,
    output logic        ser_last_o,
    input  wire         ser_ready_i,

    // timebase view
    output logic [31:0] now_ms_o,

    // class-C strobes
    output logic [7:0]  evt_tk_registered_o,
    output logic [7:0]  evt_tk_unregistered_o,
    output logic [7:0]  lstn_reg_change_o,
    output logic        evt_domain_change_o,

    // class-D dictionary
    output logic [2:0]        class_a_prio_o,
    output logic [11:0]       class_a_vid_o,
    output logic              domain_adopted_o,
    output logic [7:0][1:0]   tk_decl_state_o,
    output logic [7:0][1:0]   lstn_reg_state_o,
    output logic [7:0]        active_o,
    output logic [7:0][7:0]   src_fail_code_o,
    output logic [7:0][63:0]  src_fail_bridge_o,
    output logic [7:0][1:0]   tk_reg_state_o,
    output logic [7:0][1:0]   lstn_decl_state_o,
    output logic [7:0][31:0]  acc_latency_o,
    output logic [7:0][7:0]   snk_fail_code_o,
    output logic [7:0][63:0]  snk_fail_bridge_o,
    output logic [7:0][31:0]  granted_slope_bps_o,
    output logic [7:0]        sr_admitted_o,
    output logic [31:0]       sum_slope_bps_o,
    output logic              over_limit_o,

    // observability
    output logic [3:0]  dbg_vid_active_o,
    output logic        dbg_vlan_err_o,
    output logic        dbg_adm_round_o,
    output logic        dbg_pdu_done_o,
    output logic        dbg_pdu_ok_o,
    output logic        dbg_pdu_malformed_o
);

  // time compression: 1 ms = DIV_US x DIV_MS = 40 clk cycles; the 32-slot
  // sweep (34 cycles) fits inside it (KL_pp_timer_service constraint)
  localparam int unsigned TB_SLOTS_C  = 32;
  localparam int unsigned TB_DIV_US_C = 1;
  localparam int unsigned TB_DIV_MS_C = 40;
  localparam int unsigned TB_SLOT_AW_C = $clog2(TB_SLOTS_C);   // 5

  // ---- timer service faces ------------------------------------------------
  logic                    arm_valid_w;
  logic                    arm_cancel_w;
  logic [TB_SLOT_AW_C-1:0] arm_slot_w;
  logic [7:0]              arm_owner_w;
  logic [31:0]             arm_deadline_w;
  logic                    exp_valid_w;
  logic [TB_SLOT_AW_C-1:0] exp_slot_w;
  logic [7:0]              exp_owner_w;
  logic                    tick_ms_w;

  // ---- prng faces -----------------------------------------------------------
  logic        draw_req_w;
  logic [2:0]  draw_kind_w;
  logic        draw_busy_w;
  logic        draw_valid_w;
  logic [15:0] draw_ms_w;
  logic [63:0] dbg_lfsr_w;
  logic        dbg_seeded_w;

  // ---- tx slot pool faces ---------------------------------------------------
  logic        alloc_req_w;
  logic        oversize_w;
  logic [2:0]  alloc_slot_w;
  logic        alloc_gnt_w;
  logic [2:0]  wr_slot_w;
  logic [10:0] wr_addr_w;
  logic        wr_valid_w;
  logic [7:0]  wr_data_w;
  logic        wr_commit_w;
  logic [10:0] wr_len_w;
  logic [4:0]  slots_ready_w;
  logic [2:0]  slots_free_w;

  KL_srp_top #(
      .SLOT_AW_P (TB_SLOT_AW_C)
  ) u_dut (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .own_mac_i           (own_mac_i),
      .link_up_i           (link_up_i),
      .p2p_i               (p2p_i),
      .cfg_rank_i          (cfg_rank_i),
      .cfg_acc_lat_ns_i    (cfg_acc_lat_ns_i),
      .port_rate_bps_i     (port_rate_bps_i),
      .mrp_valid_i         (mrp_valid_i),
      .mrp_data_i          (mrp_data_i),
      .mrp_last_i          (mrp_last_i),
      .mrp_msrp_i          (mrp_msrp_i),
      .mrp_ready_o         (mrp_ready_o),
      .req_valid_i         (req_valid_i),
      .req_ready_o         (req_ready_o),
      .req_op_i            (req_op_i),
      .req_index_i         (req_index_i),
      .req_stream_id_i     (req_stream_id_i),
      .req_da_i            (req_da_i),
      .req_vid_i           (req_vid_i),
      .req_max_frame_i     (req_max_frame_i),
      .req_max_interval_i  (req_max_interval_i),
      .req_lstn_state_i    (req_lstn_state_i),
      .rsp_valid_o         (rsp_valid_o),
      .rsp_status_o        (rsp_status_o),
      .rsp_data_o          (rsp_data_o),
      .alloc_req_o         (alloc_req_w),
      .oversize_o          (oversize_w),
      .alloc_slot_i        (alloc_slot_w),
      .alloc_gnt_i         (alloc_gnt_w),
      .wr_slot_o           (wr_slot_w),
      .wr_addr_o           (wr_addr_w),
      .wr_valid_o          (wr_valid_w),
      .wr_data_o           (wr_data_w),
      .wr_commit_o         (wr_commit_w),
      .wr_len_o            (wr_len_w),
      .txreq_valid_o       (txreq_valid_o),
      .txreq_slot_o        (txreq_slot_o),
      .txreq_ready_i       (txreq_ready_i),
      .now_ms_i            (now_ms_o),
      .arm_valid_o         (arm_valid_w),
      .arm_cancel_o        (arm_cancel_w),
      .arm_slot_o          (arm_slot_w),
      .arm_owner_o         (arm_owner_w),
      .arm_deadline_ms_o   (arm_deadline_w),
      .exp_valid_i         (exp_valid_w),
      .exp_slot_i          (exp_slot_w),
      .draw_req_o          (draw_req_w),
      .draw_kind_o         (draw_kind_w),
      .draw_busy_i         (draw_busy_w),
      .draw_valid_i        (draw_valid_w),
      .draw_ms_i           (draw_ms_w),
      .evt_tk_registered_o (evt_tk_registered_o),
      .evt_tk_unregistered_o (evt_tk_unregistered_o),
      .lstn_reg_change_o   (lstn_reg_change_o),
      .evt_domain_change_o (evt_domain_change_o),
      .class_a_prio_o      (class_a_prio_o),
      .class_a_vid_o       (class_a_vid_o),
      .domain_adopted_o    (domain_adopted_o),
      .tk_decl_state_o     (tk_decl_state_o),
      .lstn_reg_state_o    (lstn_reg_state_o),
      .active_o            (active_o),
      .src_fail_code_o     (src_fail_code_o),
      .src_fail_bridge_o   (src_fail_bridge_o),
      .tk_reg_state_o      (tk_reg_state_o),
      .lstn_decl_state_o   (lstn_decl_state_o),
      .acc_latency_o       (acc_latency_o),
      .snk_fail_code_o     (snk_fail_code_o),
      .snk_fail_bridge_o   (snk_fail_bridge_o),
      .granted_slope_bps_o (granted_slope_bps_o),
      .sr_admitted_o       (sr_admitted_o),
      .sum_slope_bps_o     (sum_slope_bps_o),
      .over_limit_o        (over_limit_o),
      .dbg_vid_active_o    (dbg_vid_active_o),
      .dbg_vlan_err_o      (dbg_vlan_err_o),
      .dbg_adm_round_o     (dbg_adm_round_o),
      .dbg_pdu_done_o      (dbg_pdu_done_o),
      .dbg_pdu_ok_o        (dbg_pdu_ok_o),
      .dbg_pdu_malformed_o (dbg_pdu_malformed_o)
  );

  KL_pp_tx_slots u_tx_slots (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .alloc_req_i   (alloc_req_w),
      .oversize_i    (oversize_w),
      .alloc_gnt_o   (alloc_gnt_w),
      .alloc_slot_o  (alloc_slot_w),
      .wr_slot_i     (wr_slot_w),
      .wr_addr_i     (wr_addr_w),
      .wr_valid_i    (wr_valid_w),
      .wr_data_i     (wr_data_w),
      .wr_commit_i   (wr_commit_w),
      .wr_len_i      (wr_len_w),
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
      .slots_ready_o (slots_ready_w),
      .slots_free_o  (slots_free_w)
  );

  KL_pp_timer_service #(
      .SLOTS_P  (TB_SLOTS_C),
      .DIV_US_P (TB_DIV_US_C),
      .DIV_MS_P (TB_DIV_MS_C)
  ) u_timer (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .tick_ms_o         (tick_ms_w),
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

  KL_pp_prng u_prng (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .entity_id_i  (entity_id_i),
      .link_up_i    (link_up_i),
      .draw_req_i   (draw_req_w),
      .draw_kind_i  (draw_kind_w),
      .draw_busy_o  (draw_busy_w),
      .draw_valid_o (draw_valid_w),
      .draw_ms_o    (draw_ms_w),
      .dbg_lfsr_o   (dbg_lfsr_w),
      .dbg_seeded_o (dbg_seeded_w)
  );

endmodule : srp_top_wrap
`default_nettype wire

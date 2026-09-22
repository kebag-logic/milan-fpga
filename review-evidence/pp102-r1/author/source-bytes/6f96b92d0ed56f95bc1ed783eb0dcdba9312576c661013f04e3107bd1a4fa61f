/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_top.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 — the whole SRP engine: §4 F10.1
//                 block wiring, §6.1-§6.5 behavior, §7 join aggregation,
//                 §9 T-MRP-* ownership; 02 §4.1 srp contract class-B ops +
//                 class-C events + F02.10 class-D dictionary; 08 §2/§5
//                 timer constants + slot pool; 03 §7/§8 TX slot/requester)
//
//  Description : The assembled MSRP/MVRP endpoint participant. The MRP
//                byte stream in is ALREADY header-stripped (ProtocolVersion
//                first — the 14-byte Ethernet strip lives in the processor
//                top, rule V9 of 03 §5) and walks KL_srp_decoder; per-value
//                events fan to the talker/listener stream FSMs and to
//                KL_srp_domain (adapted to its FirstValue face: the
//                decoder's value-k reconstruction means every strobed
//                Domain value is its own one-value vector, so Class A
//                arrives pre-surfaced with NumberOfValues = 1 and the
//                certified two-class bridge shape adopts unchanged).
//                Declaration events from Domain, VLAN and both FSM arrays
//                merge (fixed priority Domain > VLAN > talker > listener;
//                every producer holds until ready, so nothing is lost) into
//                KL_srp_encoder, whose KL_pp_tx_slots write/alloc faces and
//                TX-request face pass through unchanged. KL_srp_admission
//                computes the 10 §6.3 Σ-slope verdicts from the TSpecs
//                captured at DECLARE_TALKER and feeds the talker FSMs'
//                sr_admitted_i (through a short optimistic window: a fresh
//                declaration counts as admitted until the first full
//                admission round after it has been evaluated, so the wire
//                order is always declare-Advertise-then-swap-to-Failed —
//                the exact §6.3 sentence — never a spurious Failed-first).
//                The class-B ops of 02 §4.1 (DECLARE_TALKER 0,
//                WITHDRAW_TALKER 1, DECLARE_LISTENER 2, WITHDRAW_LISTENER 3,
//                GET_DOMAIN 4; status OK 0 / FAIL 1 / UNSUPPORTED 2) serve
//                as the engine's single-outstanding service port. Cadence
//                is owned here: T-MRP-JOIN per participant, T-MRP-PERIODIC,
//                and T-MRP-LEAVEALL per participant drawn from the shared
//                KL_pp_prng (kind 3, 10-15 s) — all armed through ONE
//                merged KL_pp_timer_service face (the two FSMs' registrar-
//                leave strobe faces are absorbed by two small sync-read
//                FIFOs drained round-robin; cadence re-arms fill the idle
//                cycles). An MSRP join expiry ticks the FSM walks FIRST and
//                the encoder drain only after both txop_done strobes (plus
//                a high-water interim drain when the pending table fills
//                mid-walk), so a cadence's messages ride that cadence's
//                MRPDU instead of waiting a full T-MRP-JOIN.
//                P-EN-SRP-ENGINE is elaboration-time: instantiating this
//                module IS the engine; leaving it out leaves the identical
//                srp contract to an external stack (02 §4.1).
//
//  Decision    : the one decision that matters — LeaveAll stays PER
//                APPLICATION end to end (802.1Q §10.7.1, the corrected 10
//                §6.5 rule): two leavealltimer slots, two PRNG draws, two
//                encoder LeaveAll lanes, and the decoder's split la_msrp /
//                la_mvrp strobes are never OR-ed. One merged pulse would
//                let a bridge's MVRP maintenance cycle age a healthy MSRP
//                Listener Ready and flap the stream licence.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_top
  import srp_pkg::*;
#(
    //! stream sources M = P-N-STREAM-OUT
    parameter int unsigned N_SOURCES_P = 8,
    //! stream sinks N = P-N-STREAM-IN
    parameter int unsigned N_SINKS_P   = 8,
    //! T-MRP-JOIN in ms (F08.1: 200)
    parameter int unsigned JOIN_MS_P     = 200,
    //! T-MRP-PERIODIC in ms (F08.1: 1000)
    parameter int unsigned PERIODIC_MS_P = 1000,
    //! T-MRP-LEAVE in ms (F08.1: 5000, coupled to Δ13)
    parameter int unsigned LEAVE_MS_P    = 5000,
    //! default SR class A priority / VID (Milan §4.2.7.2.1)
    parameter logic [7:0]  DOM_DEF_PRIO_P = 8'd3,
    parameter logic [15:0] DOM_DEF_VID_P  = 16'd2,
    //! MVRP membership table entries (10 §6.2: steady state is one VID)
    parameter int unsigned N_VIDS_P    = 4,
    //! VLAN refcount width: >= clog2(P-N-STREAM-IN + P-N-STREAM-OUT + 1)
    parameter int unsigned REFCNT_W_P  = 5,
    //! encoder pending-event table depth per application
    parameter int unsigned ENC_DEPTH_P = 12,
    //! decoder Listener three-packed buffer depth in bytes
    parameter int unsigned TP_DEPTH_P  = 1024,
    //! attached KL_pp_tx_slots geometry (F01.5)
    parameter int unsigned TX_STD_BYTES_P      = 576,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! attached KL_pp_timer_service slot address width ($clog2(SLOTS_P))
    parameter int unsigned SLOT_AW_P       = 7,
    //! five cadence slots {JOIN-MSRP, JOIN-MVRP, PERIODIC, LA-MSRP, LA-MVRP}
    parameter int unsigned CAD_SLOT_BASE_P  = 0,
    parameter logic [7:0]  CAD_OWNER_BASE_P = 8'h20,
    //! talker registrar-leave block (M slots) — F08.4 pool
    parameter int unsigned TK_SLOT_BASE_P   = 16,
    parameter logic [7:0]  TK_OWNER_BASE_P  = 8'h40,
    //! listener registrar-leave block (N slots) — F08.4 pool
    parameter int unsigned LS_SLOT_BASE_P   = 24,
    parameter logic [7:0]  LS_OWNER_BASE_P  = 8'h60,
    //! derived widths — do not override
    localparam int unsigned SRC_W_C  = (N_SOURCES_P > 1) ? $clog2(N_SOURCES_P)
                                                         : 1,
    localparam int unsigned SNK_W_C  = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1,
    localparam int unsigned SLOT_W_C = $bits(pp_pkg::PP_SLOT_NULL_C),
    localparam int unsigned TXA_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire         clk_i,             //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,             //! synchronous active-low reset

    input  wire  [47:0] own_mac_i,         //! station MAC — SA + Talker Failed system id
    input  wire         link_up_i,         //! link status level (2FF-synced upstream)
    input  wire         p2p_i,             //! operPointToPointMAC (Milan ties 1)
    input  wire         cfg_rank_i,        //! declared rank bit (F10.7 byte 20 bit 4; quasi-static)
    input  wire  [31:0] cfg_acc_lat_ns_i,  //! initial accumulated_latency (802.1Q §35.2.2.8.6; quasi-static)
    input  wire  [31:0] port_rate_bps_i,   //! port rate in bps for the admission ceiling (quasi-static)

    // ---- MRP byte stream in (header-stripped: ProtocolVersion first) -----
    input  wire         mrp_valid_i,       //! byte valid (MRPDU RX queue not empty)
    input  wire  [7:0]  mrp_data_i,        //! MRPDU byte, wire order
    input  wire         mrp_last_i,        //! last byte of this MRPDU
    input  wire         mrp_msrp_i,        //! 1 = MSRP (0x22EA), 0 = MVRP (0x88F5)
    output logic        mrp_ready_o,       //! decoder pop (low only while draining packed values)

    // ---- class-B service port (02 §4.1 template: single outstanding) -----
    input  wire         req_valid_i,       //! request offered, held until ready
    output logic        req_ready_o,       //! accept (idle and no response pending)
    input  wire  [2:0]  req_op_i,          //! 0 DECLARE_TALKER / 1 WITHDRAW_TALKER / 2 DECLARE_LISTENER / 3 WITHDRAW_LISTENER / 4 GET_DOMAIN
    input  wire  [7:0]  req_index_i,       //! source/sink index; SR class id for GET_DOMAIN (6 = A)
    input  wire  [63:0] req_stream_id_i,   //! DECLARE_TALKER / DECLARE_LISTENER stream_id
    input  wire  [47:0] req_da_i,          //! DECLARE_TALKER / DECLARE_LISTENER destination MAC
    input  wire  [11:0] req_vid_i,         //! DECLARE_TALKER / DECLARE_LISTENER VLAN id
    input  wire  [15:0] req_max_frame_i,   //! DECLARE_TALKER TSpec MaxFrameSize (Milan Table 4.4)
    input  wire  [15:0] req_max_interval_i,//! DECLARE_TALKER TSpec MaxIntervalFrames (= 1)
    input  wire  [1:0]  req_lstn_state_i,  //! DECLARE_LISTENER state: 0 NONE (teardown) / else settle (declaration follows the match, 10 §6.4)
    output logic        rsp_valid_o,       //! one-cycle response strobe (exactly one per request)
    output logic [1:0]  rsp_status_o,      //! 0 OK / 1 FAIL / 2 UNSUPPORTED
    output logic [31:0] rsp_data_o,        //! GET_DOMAIN: {13'd0, priority[2:0], 4'd0, vid[11:0]}

    // ---- KL_pp_tx_slots allocation face (pass-through, exact port match) --
    output logic                alloc_req_o,   //! slot request (deasserts on grant)
    output logic                oversize_o,    //! never set: an MRPDU drain fits a standard slot
    input  wire  [SLOT_W_C-1:0] alloc_slot_i,  //! granted slot index
    input  wire                 alloc_gnt_i,   //! one-cycle grant pulse from the pool

    // ---- KL_pp_tx_slots write face (pass-through, exact port match) -------
    output logic [SLOT_W_C-1:0] wr_slot_o,     //! slot being written / committed
    output logic [TXA_W_C-1:0]  wr_addr_o,     //! byte offset inside the slot
    output logic                wr_valid_o,    //! byte-write strobe
    output logic [7:0]          wr_data_o,     //! frame byte
    output logic                wr_commit_o,   //! one-cycle commit with wr_len_o
    output logic [TXA_W_C-1:0]  wr_len_o,      //! committed frame length in bytes

    // ---- TX request face (03 §8 arbiter requester) ------------------------
    output logic                txreq_valid_o, //! committed frame ready, held until accepted
    output logic [SLOT_W_C-1:0] txreq_slot_o,  //! committed KL_pp_tx_slots handle
    input  wire                 txreq_ready_i, //! arbiter accepts the request

    // ---- KL_pp_timer_service face (merged single arm port) ---------------
    input  wire  [31:0]          now_ms_i,          //! absolute ms timebase (now_ms_o)
    output logic                 arm_valid_o,       //! arm/cancel strobe (service always accepts)
    output logic                 arm_cancel_o,      //! 1 = cancel the slot
    output logic [SLOT_AW_P-1:0] arm_slot_o,        //! slot index within this engine's blocks
    output logic [7:0]           arm_owner_o,       //! owner tag echoed at expiry
    output logic [31:0]          arm_deadline_ms_o, //! absolute ms deadline
    input  wire                  exp_valid_i,       //! timer-service expiry strobe
    input  wire  [SLOT_AW_P-1:0] exp_slot_i,        //! expired slot index

    // ---- KL_pp_prng face (T-MRP-LEAVEALL draws, kind 3) -------------------
    output logic        draw_req_o,   //! one-cycle draw request (single client assumed)
    output logic [2:0]  draw_kind_o,  //! constant 3 = 10000..15000 ms (F08.2)
    input  wire         draw_busy_i,  //! draw in progress
    input  wire         draw_valid_i, //! one-cycle strobe: draw_ms_i holds the result
    input  wire  [15:0] draw_ms_i,    //! drawn value in ms

    // ---- class-C event strobes (02 §4.1; router makes them sticky) --------
    output logic [N_SINKS_P-1:0]   evt_tk_registered_o,   //! TK_ATTR_REGISTERED{sink}
    output logic [N_SINKS_P-1:0]   evt_tk_unregistered_o, //! TK_ATTR_UNREGISTERED{sink}
    output logic [N_SOURCES_P-1:0] lstn_reg_change_o,     //! LISTENER_REG_CHANGE{source}
    output logic                   evt_domain_change_o,   //! DOMAIN_CHANGE{class A}

    // ---- class-D status dictionary (F02.10) -------------------------------
    output logic [2:0]                    class_a_prio_o,      //! operating Class A priority
    output logic [11:0]                   class_a_vid_o,       //! operating Class A default VID
    output logic                          domain_adopted_o,    //! F10.2 state (0 DEFAULTS / 1 ADOPTED)
    output logic [N_SOURCES_P-1:0][1:0]   tk_decl_state_o,     //! 0 NONE / 1 ADVERTISE / 2 FAILED (self-declared)
    output logic [N_SOURCES_P-1:0][1:0]   lstn_reg_state_o,    //! srp_decl_e code; 0 = NONE/Ignore
    output logic [N_SOURCES_P-1:0]        active_o,            //! ACTIVE(src) streaming level (Δ14 + admission)
    output logic [N_SOURCES_P-1:0][7:0]   src_fail_code_o,     //! msrp_fail_code[src] (1 while self-declared Failed)
    output logic [N_SOURCES_P-1:0][63:0]  src_fail_bridge_o,   //! msrp_fail_bridge[src] ({16'd0, own MAC} while Failed)
    output logic [N_SINKS_P-1:0][1:0]     tk_reg_state_o,      //! 0 NONE / 1 ADVERTISE / 2 FAILED for the settled match
    output logic [N_SINKS_P-1:0][1:0]     lstn_decl_state_o,   //! 0 NONE / 1 ASKING_FAILED / 2 READY
    output logic [N_SINKS_P-1:0][31:0]    acc_latency_o,       //! registered talker attr accumulated_latency
    output logic [N_SINKS_P-1:0][7:0]     snk_fail_code_o,     //! msrp_fail_code[sink] (registered Talker Failed)
    output logic [N_SINKS_P-1:0][63:0]    snk_fail_bridge_o,   //! msrp_fail_bridge[sink] (FailureInformation system id)
    output logic [N_SOURCES_P-1:0][31:0]  granted_slope_bps_o, //! per-source granted idleSlope while admitted, else 0
    output logic [N_SOURCES_P-1:0]        sr_admitted_o,       //! per-source Σ-slope admission verdict
    output logic [31:0]                   sum_slope_bps_o,     //! Σ of granted slopes, bps
    output logic                          over_limit_o,        //! some requested source stands refused

    // ---- observability -----------------------------------------------------
    output logic [N_VIDS_P-1:0] dbg_vid_active_o,    //! MVRP membership-live bits
    output logic                dbg_vlan_err_o,      //! VLAN table full / unknown-VID leave strobe
    output logic                dbg_adm_round_o,     //! admission round-latch strobe
    output logic                dbg_pdu_done_o,      //! decoder: one strobe per walked PDU
    output logic                dbg_pdu_ok_o,        //! decoder: with done, PDU clean
    output logic                dbg_pdu_malformed_o  //! decoder: with done, tolerance discard happened
);

  // ---- class-B op / status codes (02 §4.1) -------------------------------
  localparam logic [2:0] OP_DECLARE_TALKER_C    = 3'd0;
  localparam logic [2:0] OP_WITHDRAW_TALKER_C   = 3'd1;
  localparam logic [2:0] OP_DECLARE_LISTENER_C  = 3'd2;
  localparam logic [2:0] OP_WITHDRAW_LISTENER_C = 3'd3;
  localparam logic [2:0] OP_GET_DOMAIN_C        = 3'd4;
  localparam logic [1:0] RSP_OK_C          = 2'd0;
  localparam logic [1:0] RSP_FAIL_C        = 2'd1;
  localparam logic [1:0] RSP_UNSUPPORTED_C = 2'd2;

  // ---- cadence slot offsets within the CAD block -------------------------
  localparam int unsigned CAD_JOIN_MSRP_C = 0;
  localparam int unsigned CAD_JOIN_MVRP_C = 1;
  localparam int unsigned CAD_PERIODIC_C  = 2;
  localparam int unsigned CAD_LA_MSRP_C   = 3;
  localparam int unsigned CAD_LA_MVRP_C   = 4;
  localparam int unsigned N_CAD_C         = 5;

  // ========================================================================
  // decoder
  // ========================================================================
  logic        dec_evt_valid_w;
  logic        dec_evt_msrp_w;
  logic [7:0]  dec_evt_attr_type_w;
  logic [63:0] dec_evt_stream_id_w;
  logic [47:0] dec_evt_da_w;
  logic [15:0] dec_evt_vid_w;
  logic [2:0]  dec_evt_mrp_event_w;
  logic [1:0]  dec_evt_fourpacked_w;
  logic [15:0] dec_evt_max_frame_w;
  logic [15:0] dec_evt_max_interval_w;
  logic [7:0]  dec_evt_priority_w;
  logic        dec_evt_rank_w;
  logic [31:0] dec_evt_acc_latency_w;
  logic [63:0] dec_evt_fail_sysid_w;
  logic [7:0]  dec_evt_fail_code_w;
  logic [7:0]  dec_evt_class_id_w;
  logic        dec_evt_class_a_w;
  logic        dec_la_msrp_w;
  logic        dec_la_mvrp_w;
  logic [15:0] dec_dbg_listlen_w;
  logic        dec_listlen_bad_w;

  KL_srp_decoder #(
      .TP_DEPTH_P (TP_DEPTH_P)
  ) u_decoder (
      .clk_i                     (clk_i),
      .rst_n                     (rst_n),
      .mrp_valid_i               (mrp_valid_i),
      .mrp_data_i                (mrp_data_i),
      .mrp_last_i                (mrp_last_i),
      .mrp_msrp_i                (mrp_msrp_i),
      .mrp_ready_o               (mrp_ready_o),
      .evt_valid_o               (dec_evt_valid_w),
      .evt_msrp_o                (dec_evt_msrp_w),
      .evt_attr_type_o           (dec_evt_attr_type_w),
      .evt_stream_id_o           (dec_evt_stream_id_w),
      .evt_da_o                  (dec_evt_da_w),
      .evt_vid_o                 (dec_evt_vid_w),
      .evt_mrp_event_o           (dec_evt_mrp_event_w),
      .evt_fourpacked_o          (dec_evt_fourpacked_w),
      .evt_max_frame_size_o      (dec_evt_max_frame_w),
      .evt_max_interval_frames_o (dec_evt_max_interval_w),
      .evt_priority_o            (dec_evt_priority_w),
      .evt_rank_o                (dec_evt_rank_w),
      .evt_acc_latency_o         (dec_evt_acc_latency_w),
      .evt_failure_system_id_o   (dec_evt_fail_sysid_w),
      .evt_failure_code_o        (dec_evt_fail_code_w),
      .evt_class_id_o            (dec_evt_class_id_w),
      .evt_class_a_o             (dec_evt_class_a_w),
      .la_msrp_o                 (dec_la_msrp_w),
      .la_mvrp_o                 (dec_la_mvrp_w),
      .pdu_done_o                (dbg_pdu_done_o),
      .pdu_ok_o                  (dbg_pdu_ok_o),
      .pdu_malformed_o           (dbg_pdu_malformed_o),
      .listlen_bad_o             (dec_listlen_bad_w),
      .dbg_listlen_cnt_o         (dec_dbg_listlen_w)
  );

  // ========================================================================
  // cadence strobes (registered, one cycle) — declared before first use
  // ========================================================================
  logic       p_join_fsm_r;    // T-MRP-JOIN (MSRP): tick the FSM walks
  logic       p_periodic_r;    // T-MRP-PERIODIC: all four participants
  logic       p_la_msrp_r;     // own MSRP leavealltimer expiry
  logic       p_la_mvrp_r;     // own MVRP leavealltimer expiry
  logic [1:0] enc_join_r;      // encoder drain ticks {MVRP, MSRP}
  logic [1:0] enc_la_r;        // encoder LeaveAllEvent lanes {MVRP, MSRP}

  // ========================================================================
  // domain (decoder adapted to its FirstValue face: each strobed value is
  // its own one-value vector — Class A arrives pre-surfaced, 10 §3)
  // ========================================================================
  logic        dom_rx_valid_w;
  logic        dom_rx_reg_w;
  logic        dom_ev_valid_w;
  logic [2:0]  dom_ev_event_w;
  logic [31:0] dom_ev_value_w;
  logic        dom_ev_ready_w;
  logic [2:0]  dom_prio_w;
  logic [11:0] dom_vid_w;

  assign dom_rx_reg_w = (dec_evt_mrp_event_w == 3'(SRP_EV_NEW))
                     || (dec_evt_mrp_event_w == 3'(SRP_EV_JOININ))
                     || (dec_evt_mrp_event_w == 3'(SRP_EV_JOINMT));
  assign dom_rx_valid_w = dec_evt_valid_w && dec_evt_msrp_w
                       && (dec_evt_attr_type_w == SRP_MSRP_ATTR_DOMAIN_C)
                       && dec_evt_class_a_w && dom_rx_reg_w;

  KL_srp_domain #(
      .DEF_PRIO_P (DOM_DEF_PRIO_P),
      .DEF_VID_P  (DOM_DEF_VID_P)
  ) u_domain (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .link_up_i           (link_up_i),
      .rxdom_valid_i       (dom_rx_valid_w),
      .rxdom_class_id_i    (dec_evt_class_id_w),
      .rxdom_prio_i        (dec_evt_priority_w),
      .rxdom_vid_i         (dec_evt_vid_w),
      .rxdom_nov_i         (13'd1),
      .periodic_tick_i     (p_periodic_r),
      .leaveall_tick_i     (dec_la_msrp_w || p_la_msrp_r),
      .dom_ev_valid_o      (dom_ev_valid_w),
      .dom_ev_event_o      (dom_ev_event_w),
      .dom_ev_value_o      (dom_ev_value_w),
      .dom_ev_ready_i      (dom_ev_ready_w),
      .evt_domain_change_o (evt_domain_change_o),
      .class_a_prio_o      (dom_prio_w),
      .class_a_vid_o       (dom_vid_w),
      .adopted_o           (domain_adopted_o)
  );

  assign class_a_prio_o = dom_prio_w;
  assign class_a_vid_o  = dom_vid_w;

  // ========================================================================
  // VLAN participant + user-face mux (talker / listener round-robin)
  // ========================================================================
  logic        vlan_user_valid_w;
  logic        vlan_user_join_w;
  logic [11:0] vlan_user_vid_w;
  logic        vlan_user_ready_w;
  logic        vlan_ev_valid_w;
  logic [2:0]  vlan_ev_event_w;
  logic [15:0] vlan_ev_vid_w;
  logic        vlan_ev_ready_w;

  logic        tk_user_valid_w, tk_user_join_w;
  logic [11:0] tk_user_vid_w;
  logic        ls_user_valid_w, ls_user_join_w;
  logic [11:0] ls_user_vid_w;
  logic        vu_sel_ls_w;
  logic        vrr_r;

  assign vu_sel_ls_w       = ls_user_valid_w && (!tk_user_valid_w || vrr_r);
  assign vlan_user_valid_w = tk_user_valid_w || ls_user_valid_w;
  assign vlan_user_join_w  = vu_sel_ls_w ? ls_user_join_w : tk_user_join_w;
  assign vlan_user_vid_w   = vu_sel_ls_w ? ls_user_vid_w : tk_user_vid_w;

  always_ff @(posedge clk_i) begin : vlan_user_rr
    if (!rst_n) begin
      vrr_r <= 1'b0;
    end else if (vlan_user_valid_w && vlan_user_ready_w) begin
      vrr_r <= ~vrr_r;   // fair alternation between the two user arrays
    end
  end

  KL_srp_vlan #(
      .N_VIDS_P   (N_VIDS_P),
      .REFCNT_W_P (REFCNT_W_P)
  ) u_vlan (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .user_valid_i    (vlan_user_valid_w),
      .user_join_i     (vlan_user_join_w),
      .user_vid_i      (vlan_user_vid_w),
      .user_ready_o    (vlan_user_ready_w),
      .user_err_o      (dbg_vlan_err_o),
      .periodic_tick_i (p_periodic_r),
      .leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),
      .vlan_ev_valid_o (vlan_ev_valid_w),
      .vlan_ev_event_o (vlan_ev_event_w),
      .vlan_ev_vid_o   (vlan_ev_vid_w),
      .vlan_ev_ready_i (vlan_ev_ready_w),
      .vid_active_o    (dbg_vid_active_o)
  );

  // ========================================================================
  // admission (10 §6.3) + the optimistic first-verdict window
  // ========================================================================
  logic [N_SOURCES_P-1:0]       adm_req_r;
  logic [N_SOURCES_P-1:0][15:0] adm_mfs_r;
  logic [N_SOURCES_P-1:0][15:0] adm_mif_r;
  logic [N_SOURCES_P-1:0]       adm_admitted_w;
  logic                         adm_round_w;
  logic [N_SOURCES_P-1:0]       opt_r;
  logic [N_SOURCES_P-1:0][1:0]  opt_cnt_r;
  logic [N_SOURCES_P-1:0]       sr_adm_fsm_w;

  KL_srp_admission #(
      .N_SOURCES_P (N_SOURCES_P)
  ) u_admission (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .req_i               (adm_req_r),
      .max_frame_i         (adm_mfs_r),
      .interval_frames_i   (adm_mif_r),
      .port_rate_bps_i     (port_rate_bps_i),
      .sr_admitted_o       (adm_admitted_w),
      .granted_slope_bps_o (granted_slope_bps_o),
      .sum_slope_bps_o     (sum_slope_bps_o),
      .over_limit_o        (over_limit_o),
      .round_done_o        (adm_round_w)
  );

  assign sr_admitted_o = adm_admitted_w;
  assign dbg_adm_round_o = adm_round_w;
  // a fresh declaration counts as admitted until fully evaluated (banner)
  assign sr_adm_fsm_w = opt_r | adm_admitted_w;

  // ========================================================================
  // talker FSMs
  // ========================================================================
  logic               gate_valid_w;
  logic               gate_ready_w;
  logic               tk_txop_done_w;
  logic               tk_ev_valid_w;
  logic               tk_ev_ready_w;
  logic               tk_ev_app_w;
  logic [7:0]         tk_ev_type_w;
  logic [2:0]         tk_ev_event_w;
  logic [1:0]         tk_ev_fp_w;
  logic [271:0]       tk_ev_value_w;
  logic               tk_user_ready_w;
  logic               tk_arm_v_w;
  logic               tk_arm_cancel_w;
  logic [SLOT_AW_P-1:0] tk_arm_slot_w;
  logic [7:0]         tk_arm_owner_w;
  logic [31:0]        tk_arm_dl_w;
  logic [N_SOURCES_P-1:0][3:0] tk_dbg_app_w;
  logic [N_SOURCES_P-1:0][1:0] tk_dbg_reg_w;

  // service-plane latches (declared before the instances that consume them)
  logic [7:0]  a_idx_r;
  logic [63:0] a_sid_r;
  logic [47:0] a_da_r;
  logic [11:0] a_vid_r;
  logic [15:0] a_mfs_r;
  logic [15:0] a_mif_r;
  logic        a_open_r;

  KL_srp_talker_fsm #(
      .N_SOURCES_P  (N_SOURCES_P),
      .LEAVE_MS_P   (LEAVE_MS_P),
      .SLOT_BASE_P  (TK_SLOT_BASE_P),
      .SLOT_AW_P    (SLOT_AW_P),
      .OWNER_BASE_P (TK_OWNER_BASE_P)
  ) u_talker (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .own_mac_i           (own_mac_i),
      .p2p_i               (p2p_i),
      .gate_valid_i        (gate_valid_w),
      .gate_ready_o        (gate_ready_w),
      .gate_open_i         (a_open_r),
      .gate_src_i          (a_idx_r[SRC_W_C-1:0]),
      .gate_stream_id_i    (a_sid_r),
      .gate_da_i           (a_da_r),
      .gate_vid_i          (a_vid_r),
      .gate_max_frame_i    (a_mfs_r),
      .gate_max_interval_i (a_mif_r),
      .gate_prio_i         (dom_prio_w),
      .gate_rank_i         (cfg_rank_i),
      .gate_acc_lat_i      (cfg_acc_lat_ns_i),
      .sr_admitted_i       (sr_adm_fsm_w),
      .evt_valid_i         (dec_evt_valid_w),
      .evt_msrp_i          (dec_evt_msrp_w),
      .evt_attr_type_i     (dec_evt_attr_type_w),
      .evt_stream_id_i     (dec_evt_stream_id_w),
      .evt_da_i            (dec_evt_da_w),
      .evt_vid_i           (dec_evt_vid_w),
      .evt_mrp_event_i     (dec_evt_mrp_event_w),
      .evt_fourpacked_i    (dec_evt_fourpacked_w),
      .join_tick_i         (p_join_fsm_r),
      .periodic_tick_i     (p_periodic_r),
      .leaveall_rx_i       (dec_la_msrp_w),
      .leaveall_own_i      (p_la_msrp_r),
      .txop_done_o         (tk_txop_done_w),
      .ev_valid_o          (tk_ev_valid_w),
      .ev_ready_i          (tk_ev_ready_w),
      .ev_app_o            (tk_ev_app_w),
      .ev_attr_type_o      (tk_ev_type_w),
      .ev_event_o          (tk_ev_event_w),
      .ev_fourpack_o       (tk_ev_fp_w),
      .ev_value_o          (tk_ev_value_w),
      .user_valid_o        (tk_user_valid_w),
      .user_join_o         (tk_user_join_w),
      .user_vid_o          (tk_user_vid_w),
      .user_ready_i        (tk_user_ready_w),
      .now_ms_i            (now_ms_i),
      .arm_valid_o         (tk_arm_v_w),
      .arm_cancel_o        (tk_arm_cancel_w),
      .arm_slot_o          (tk_arm_slot_w),
      .arm_owner_o         (tk_arm_owner_w),
      .arm_deadline_ms_o   (tk_arm_dl_w),
      .exp_valid_i         (exp_valid_i),
      .exp_slot_i          (exp_slot_i),
      .lstn_reg_change_o   (lstn_reg_change_o),
      .tk_decl_state_o     (tk_decl_state_o),
      .lstn_reg_state_o    (lstn_reg_state_o),
      .active_o            (active_o),
      .msrp_fail_code_o    (src_fail_code_o),
      .msrp_fail_bridge_o  (src_fail_bridge_o),
      .dbg_app_state_o     (tk_dbg_app_w),
      .dbg_reg_state_o     (tk_dbg_reg_w)
  );

  // ========================================================================
  // listener FSMs
  // ========================================================================
  logic               ctl_valid_w;
  logic               ctl_ready_w;
  logic               ls_txop_done_w;
  logic               ls_ev_valid_w;
  logic               ls_ev_ready_w;
  logic               ls_ev_app_w;
  logic [7:0]         ls_ev_type_w;
  logic [2:0]         ls_ev_event_w;
  logic [1:0]         ls_ev_fp_w;
  logic [271:0]       ls_ev_value_w;
  logic               ls_user_ready_w;
  logic               ls_arm_v_w;
  logic               ls_arm_cancel_w;
  logic [SLOT_AW_P-1:0] ls_arm_slot_w;
  logic [7:0]         ls_arm_owner_w;
  logic [31:0]        ls_arm_dl_w;
  logic [N_SINKS_P-1:0][3:0] ls_dbg_app_w;
  logic [N_SINKS_P-1:0][1:0] ls_dbg_reg_w;

  KL_srp_listener_fsm #(
      .N_SINKS_P    (N_SINKS_P),
      .LEAVE_MS_P   (LEAVE_MS_P),
      .SLOT_BASE_P  (LS_SLOT_BASE_P),
      .SLOT_AW_P    (SLOT_AW_P),
      .OWNER_BASE_P (LS_OWNER_BASE_P)
  ) u_listener (
      .clk_i                   (clk_i),
      .rst_n                   (rst_n),
      .p2p_i                   (p2p_i),
      .ctl_valid_i             (ctl_valid_w),
      .ctl_ready_o             (ctl_ready_w),
      .ctl_settle_i            (a_open_r),
      .ctl_sink_i              (a_idx_r[SNK_W_C-1:0]),
      .ctl_stream_id_i         (a_sid_r),
      .ctl_da_i                (a_da_r),
      .ctl_vid_i               (a_vid_r),
      .evt_valid_i             (dec_evt_valid_w),
      .evt_msrp_i              (dec_evt_msrp_w),
      .evt_attr_type_i         (dec_evt_attr_type_w),
      .evt_stream_id_i         (dec_evt_stream_id_w),
      .evt_da_i                (dec_evt_da_w),
      .evt_vid_i               (dec_evt_vid_w),
      .evt_mrp_event_i         (dec_evt_mrp_event_w),
      .evt_acc_latency_i       (dec_evt_acc_latency_w),
      .evt_failure_system_id_i (dec_evt_fail_sysid_w),
      .evt_failure_code_i      (dec_evt_fail_code_w),
      .join_tick_i             (p_join_fsm_r),
      .periodic_tick_i         (p_periodic_r),
      .leaveall_rx_i           (dec_la_msrp_w),
      .leaveall_own_i          (p_la_msrp_r),
      .txop_done_o             (ls_txop_done_w),
      .ev_valid_o              (ls_ev_valid_w),
      .ev_ready_i              (ls_ev_ready_w),
      .ev_app_o                (ls_ev_app_w),
      .ev_attr_type_o          (ls_ev_type_w),
      .ev_event_o              (ls_ev_event_w),
      .ev_fourpack_o           (ls_ev_fp_w),
      .ev_value_o              (ls_ev_value_w),
      .user_valid_o            (ls_user_valid_w),
      .user_join_o             (ls_user_join_w),
      .user_vid_o              (ls_user_vid_w),
      .user_ready_i            (ls_user_ready_w),
      .now_ms_i                (now_ms_i),
      .arm_valid_o             (ls_arm_v_w),
      .arm_cancel_o            (ls_arm_cancel_w),
      .arm_slot_o              (ls_arm_slot_w),
      .arm_owner_o             (ls_arm_owner_w),
      .arm_deadline_ms_o       (ls_arm_dl_w),
      .exp_valid_i             (exp_valid_i),
      .exp_slot_i              (exp_slot_i),
      .evt_tk_registered_o     (evt_tk_registered_o),
      .evt_tk_unregistered_o   (evt_tk_unregistered_o),
      .tk_reg_state_o          (tk_reg_state_o),
      .lstn_decl_state_o       (lstn_decl_state_o),
      .acc_latency_o           (acc_latency_o),
      .msrp_fail_code_o        (snk_fail_code_o),
      .msrp_fail_bridge_o      (snk_fail_bridge_o),
      .dbg_app_state_o         (ls_dbg_app_w),
      .dbg_reg_state_o         (ls_dbg_reg_w)
  );

  // VLAN user-face ready fan-back (only the granted user sees ready)
  assign tk_user_ready_w = vlan_user_ready_w && tk_user_valid_w
                         && !vu_sel_ls_w;
  assign ls_user_ready_w = vlan_user_ready_w && vu_sel_ls_w;

  // ========================================================================
  // encoder + intake mux (fixed priority Domain > VLAN > talker > listener;
  // every producer holds until ready, so priority is only an ordering)
  // ========================================================================
  logic         enc_ev_valid_w;
  logic         enc_ev_ready_w;
  logic         enc_ev_app_w;
  logic [7:0]   enc_ev_type_w;
  logic [2:0]   enc_ev_event_w;
  logic [1:0]   enc_ev_fp_w;
  logic [271:0] enc_ev_value_w;
  logic         enc_ev_drop_w;
  logic [$clog2(ENC_DEPTH_P+1)-1:0] enc_cnt_msrp_w;
  logic [$clog2(ENC_DEPTH_P+1)-1:0] enc_cnt_mvrp_w;

  always_comb begin : enc_intake_mux
    enc_ev_valid_w = 1'b1;
    if (dom_ev_valid_w) begin
      enc_ev_app_w   = 1'b0;
      enc_ev_type_w  = SRP_MSRP_ATTR_DOMAIN_C;
      enc_ev_event_w = dom_ev_event_w;
      enc_ev_fp_w    = 2'd0;
      enc_ev_value_w = {dom_ev_value_w, 240'd0};
    end else if (vlan_ev_valid_w) begin
      enc_ev_app_w   = 1'b1;
      enc_ev_type_w  = SRP_MVRP_ATTR_VID_C;
      enc_ev_event_w = vlan_ev_event_w;
      enc_ev_fp_w    = 2'd0;
      enc_ev_value_w = {vlan_ev_vid_w, 256'd0};
    end else if (tk_ev_valid_w) begin
      enc_ev_app_w   = tk_ev_app_w;
      enc_ev_type_w  = tk_ev_type_w;
      enc_ev_event_w = tk_ev_event_w;
      enc_ev_fp_w    = tk_ev_fp_w;
      enc_ev_value_w = tk_ev_value_w;
    end else if (ls_ev_valid_w) begin
      enc_ev_app_w   = ls_ev_app_w;
      enc_ev_type_w  = ls_ev_type_w;
      enc_ev_event_w = ls_ev_event_w;
      enc_ev_fp_w    = ls_ev_fp_w;
      enc_ev_value_w = ls_ev_value_w;
    end else begin
      enc_ev_valid_w = 1'b0;
      enc_ev_app_w   = 1'b0;
      enc_ev_type_w  = 8'd0;
      enc_ev_event_w = 3'd0;
      enc_ev_fp_w    = 2'd0;
      enc_ev_value_w = 272'd0;
    end
  end

  assign dom_ev_ready_w  = enc_ev_ready_w && dom_ev_valid_w;
  assign vlan_ev_ready_w = enc_ev_ready_w && !dom_ev_valid_w
                         && vlan_ev_valid_w;
  assign tk_ev_ready_w   = enc_ev_ready_w && !dom_ev_valid_w
                         && !vlan_ev_valid_w && tk_ev_valid_w;
  assign ls_ev_ready_w   = enc_ev_ready_w && !dom_ev_valid_w
                         && !vlan_ev_valid_w && !tk_ev_valid_w
                         && ls_ev_valid_w;

  KL_srp_encoder #(
      .DEPTH_P             (ENC_DEPTH_P),
      .TX_STD_BYTES_P      (TX_STD_BYTES_P),
      .TX_OVERSIZE_BYTES_P (TX_OVERSIZE_BYTES_P)
  ) u_encoder (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .ev_valid_i     (enc_ev_valid_w),
      .ev_ready_o     (enc_ev_ready_w),
      .ev_app_i       (enc_ev_app_w),
      .ev_attr_type_i (enc_ev_type_w),
      .ev_event_i     (enc_ev_event_w),
      .ev_fourpack_i  (enc_ev_fp_w),
      .ev_value_i     (enc_ev_value_w),
      .ev_drop_o      (enc_ev_drop_w),
      .join_tick_i    (enc_join_r),
      .leaveall_i     (enc_la_r),
      .own_mac_i      (own_mac_i),
      .alloc_req_o    (alloc_req_o),
      .oversize_o     (oversize_o),
      .alloc_slot_i   (alloc_slot_i),
      .alloc_gnt_i    (alloc_gnt_i),
      .wr_slot_o      (wr_slot_o),
      .wr_addr_o      (wr_addr_o),
      .wr_valid_o     (wr_valid_o),
      .wr_data_o      (wr_data_o),
      .wr_commit_o    (wr_commit_o),
      .wr_len_o       (wr_len_o),
      .txreq_valid_o  (txreq_valid_o),
      .txreq_slot_o   (txreq_slot_o),
      .txreq_ready_i  (txreq_ready_i),
      .dbg_cnt_msrp_o (enc_cnt_msrp_w),
      .dbg_cnt_mvrp_o (enc_cnt_mvrp_w)
  );

  // ========================================================================
  // class-B service plane (02 §4.1 template: single outstanding)
  // ========================================================================
  typedef enum logic [1:0] {
    S_IDLE = 2'd0,   // accept one request
    S_GATE = 2'd1,   // hold the talker DA-gate op until accepted
    S_CTL  = 2'd2,   // hold the listener settle/teardown op until accepted
    S_RSP  = 2'd3    // strobe the response
  } svc_st_e;

  svc_st_e     svc_st_r;
  logic [1:0]  rsp_status_r;
  logic [31:0] rsp_data_r;

  logic svc_acc_w, gate_acc_w, ctl_acc_w;

  assign req_ready_o = (svc_st_r == S_IDLE);
  assign svc_acc_w   = req_valid_i && req_ready_o;
  assign gate_valid_w = (svc_st_r == S_GATE);
  assign ctl_valid_w  = (svc_st_r == S_CTL);
  assign gate_acc_w   = gate_valid_w && gate_ready_w;
  assign ctl_acc_w    = ctl_valid_w && ctl_ready_w;

  always_ff @(posedge clk_i) begin : service_plane
    if (!rst_n) begin
      svc_st_r     <= S_IDLE;
      a_idx_r      <= 8'd0;
      a_sid_r      <= 64'd0;
      a_da_r       <= 48'd0;
      a_vid_r      <= 12'd0;
      a_mfs_r      <= 16'd0;
      a_mif_r      <= 16'd0;
      a_open_r     <= 1'b0;
      rsp_status_r <= RSP_OK_C;
      rsp_data_r   <= 32'd0;
      rsp_valid_o  <= 1'b0;
      adm_req_r    <= '0;
      adm_mfs_r    <= '0;
      adm_mif_r    <= '0;
      opt_r        <= '0;
      opt_cnt_r    <= '0;
    end else begin
      rsp_valid_o <= 1'b0;

      // ---- optimistic-window aging (one full round with the request
      // visible must complete before the verdict is trusted) --------------
      if (adm_round_w) begin
        for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
          if (opt_r[s]) begin
            if (opt_cnt_r[s] != 2'd0) opt_cnt_r[s] <= opt_cnt_r[s] - 2'd1;
            else                      opt_r[s]     <= 1'b0;
          end
        end
      end

      unique case (svc_st_r)
        S_IDLE: begin
          if (svc_acc_w) begin
            a_idx_r <= req_index_i;
            a_sid_r <= req_stream_id_i;
            a_da_r  <= req_da_i;
            a_vid_r <= req_vid_i;
            a_mfs_r <= req_max_frame_i;
            a_mif_r <= req_max_interval_i;
            unique case (req_op_i)
              OP_DECLARE_TALKER_C: begin
                if (32'(req_index_i) < N_SOURCES_P) begin
                  a_open_r <= 1'b1;
                  svc_st_r <= S_GATE;
                end else begin
                  rsp_status_r <= RSP_FAIL_C;
                  svc_st_r     <= S_RSP;
                end
              end
              OP_WITHDRAW_TALKER_C: begin
                if (32'(req_index_i) < N_SOURCES_P) begin
                  a_open_r <= 1'b0;
                  svc_st_r <= S_GATE;
                end else begin
                  rsp_status_r <= RSP_FAIL_C;
                  svc_st_r     <= S_RSP;
                end
              end
              OP_DECLARE_LISTENER_C: begin
                if (32'(req_index_i) < N_SINKS_P) begin
                  // state NONE = teardown; else settle — the declared
                  // parameter itself follows the match (10 §6.4)
                  a_open_r <= (req_lstn_state_i != 2'd0);
                  svc_st_r <= S_CTL;
                end else begin
                  rsp_status_r <= RSP_FAIL_C;
                  svc_st_r     <= S_RSP;
                end
              end
              OP_WITHDRAW_LISTENER_C: begin
                if (32'(req_index_i) < N_SINKS_P) begin
                  a_open_r <= 1'b0;
                  svc_st_r <= S_CTL;
                end else begin
                  rsp_status_r <= RSP_FAIL_C;
                  svc_st_r     <= S_RSP;
                end
              end
              OP_GET_DOMAIN_C: begin
                // only SR class A exists in this profile (10 §1)
                if (req_index_i == SRP_CLASS_A_ID_C) begin
                  rsp_status_r <= RSP_OK_C;
                  rsp_data_r   <= {13'd0, dom_prio_w, 4'd0, dom_vid_w};
                end else begin
                  rsp_status_r <= RSP_FAIL_C;
                  rsp_data_r   <= 32'd0;
                end
                svc_st_r <= S_RSP;
              end
              default: begin
                rsp_status_r <= RSP_UNSUPPORTED_C;
                svc_st_r     <= S_RSP;
              end
            endcase
          end
        end
        S_GATE: begin
          if (gate_acc_w) begin
            if (a_open_r) begin
              // TSpec joins the admission request set; verdict optimistic
              // until one full round has evaluated it (banner)
              adm_req_r[a_idx_r[SRC_W_C-1:0]]   <= 1'b1;
              adm_mfs_r[a_idx_r[SRC_W_C-1:0]]   <= a_mfs_r;
              adm_mif_r[a_idx_r[SRC_W_C-1:0]]   <= a_mif_r;
              opt_r[a_idx_r[SRC_W_C-1:0]]       <= 1'b1;
              opt_cnt_r[a_idx_r[SRC_W_C-1:0]]   <= 2'd2;
            end else begin
              adm_req_r[a_idx_r[SRC_W_C-1:0]]   <= 1'b0;
              opt_r[a_idx_r[SRC_W_C-1:0]]       <= 1'b0;
            end
            rsp_status_r <= RSP_OK_C;
            svc_st_r     <= S_RSP;
          end
        end
        S_CTL: begin
          if (ctl_acc_w) begin
            rsp_status_r <= RSP_OK_C;
            svc_st_r     <= S_RSP;
          end
        end
        default: begin   // S_RSP
          rsp_valid_o <= 1'b1;
          svc_st_r    <= S_IDLE;
        end
      endcase
    end
  end

  assign rsp_status_o = rsp_status_r;
  assign rsp_data_o   = rsp_data_r;

  // ========================================================================
  // cadence + merged timer face + PRNG draws
  // ========================================================================
  // FIFO word: {cancel, slot, owner, deadline}; depth 32 >= 2x the largest
  // per-walk arm burst (one op per source per LeaveAll aging walk)
  localparam int unsigned TFW_C = 1 + SLOT_AW_P + 8 + 32;
  localparam int unsigned TFD_C = 32;

  logic [TFW_C-1:0] tf_ram_r [0:1][0:TFD_C-1];
  logic [TFW_C-1:0] tf_q_r   [0:1];
  logic [4:0]       tf_wptr_r [0:1];
  logic [4:0]       tf_rptr_r [0:1];
  logic [5:0]       tf_cnt_r  [0:1];

  logic [1:0] tf_push_w;
  logic [1:0] tf_pop_w;

  assign tf_push_w[0] = tk_arm_v_w && (tf_cnt_r[0] != 6'(TFD_C));
  assign tf_push_w[1] = ls_arm_v_w && (tf_cnt_r[1] != 6'(TFD_C));

  always_ff @(posedge clk_i) begin : tf_write
    if (tf_push_w[0]) begin
      tf_ram_r[0][tf_wptr_r[0]]
        <= {tk_arm_cancel_w, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w};
    end
    if (tf_push_w[1]) begin
      tf_ram_r[1][tf_wptr_r[1]]
        <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};
    end
  end

  always_ff @(posedge clk_i) begin : tf_read
    tf_q_r[0] <= tf_ram_r[0][tf_rptr_r[0]];
    tf_q_r[1] <= tf_ram_r[1][tf_rptr_r[1]];
  end

  typedef enum logic {
    TM_SEL = 1'b0,   // pick a source: FSM FIFOs round-robin, cadence last
    TM_POP = 1'b1    // issue the FIFO word read in TM_SEL
  } tm_st_e;

  tm_st_e     tm_st_r;
  logic       tm_sel_r;    // 0 = talker FIFO, 1 = listener FIFO
  logic       tm_rr_r;     // round-robin preference

  logic       init_done_r;
  logic [N_CAD_C-1:0]       cad_pend_r;
  logic [N_CAD_C-1:0][31:0] cad_dl_r;
  logic [2:0] cad_ix_w;

  logic [1:0] need_draw_r;
  logic       dr_inflight_r;
  logic       dr_app_r;

  logic       rnd_act_r;    // an MSRP join round is running (walks first)
  logic       td_tk_r;
  logic       td_ls_r;
  logic       hw_full_q_r;
  logic       enc_msrp_full_w;
  logic       cad_hit_w;
  logic [31:0] cad_exp_ix_w;

  // lowest pending cadence index
  always_comb begin : cad_pick
    cad_ix_w = 3'd0;
    for (int i = int'(N_CAD_C) - 1; i >= 0; i--) begin
      if (cad_pend_r[i]) cad_ix_w = 3'(i);
    end
  end

  // unsigned wrap maps below-base slots to huge indices — one bound check
  assign cad_exp_ix_w    = 32'(exp_slot_i) - CAD_SLOT_BASE_P;
  assign cad_hit_w       = exp_valid_i && (cad_exp_ix_w < N_CAD_C);
  assign enc_msrp_full_w = (32'(enc_cnt_msrp_w) == ENC_DEPTH_P);

  assign draw_kind_o = 3'd3;   // T-MRP-LEAVEALL range (F08.2)

  always_ff @(posedge clk_i) begin : timer_cadence_plane
    if (!rst_n) begin
      arm_valid_o       <= 1'b0;
      arm_cancel_o      <= 1'b0;
      arm_slot_o        <= '0;
      arm_owner_o       <= 8'd0;
      arm_deadline_ms_o <= 32'd0;
      tf_wptr_r[0]      <= '0;
      tf_wptr_r[1]      <= '0;
      tf_rptr_r[0]      <= '0;
      tf_rptr_r[1]      <= '0;
      tf_cnt_r[0]       <= '0;
      tf_cnt_r[1]       <= '0;
      tm_st_r           <= TM_SEL;
      tm_sel_r          <= 1'b0;
      tm_rr_r           <= 1'b0;
      init_done_r       <= 1'b0;
      cad_pend_r        <= '0;
      cad_dl_r          <= '0;
      need_draw_r       <= 2'b00;
      dr_inflight_r     <= 1'b0;
      dr_app_r          <= 1'b0;
      draw_req_o        <= 1'b0;
      rnd_act_r         <= 1'b0;
      td_tk_r           <= 1'b0;
      td_ls_r           <= 1'b0;
      hw_full_q_r       <= 1'b0;
      p_join_fsm_r      <= 1'b0;
      p_periodic_r      <= 1'b0;
      p_la_msrp_r       <= 1'b0;
      p_la_mvrp_r       <= 1'b0;
      enc_join_r        <= 2'b00;
      enc_la_r          <= 2'b00;
    end else begin
      // ---- strobe defaults ----------------------------------------------
      arm_valid_o  <= 1'b0;
      draw_req_o   <= 1'b0;
      p_join_fsm_r <= 1'b0;
      p_periodic_r <= 1'b0;
      p_la_msrp_r  <= 1'b0;
      p_la_mvrp_r  <= 1'b0;
      enc_join_r   <= 2'b00;
      enc_la_r     <= 2'b00;

      // ---- FIFO push bookkeeping (drop-never by depth; guarded anyway) --
      for (int unsigned u = 0; u < 2; u++) begin
        if (tf_push_w[u]) tf_wptr_r[u] <= tf_wptr_r[u] + 5'd1;
        tf_cnt_r[u] <= tf_cnt_r[u] + {5'd0, tf_push_w[u]}
                                   - {5'd0, tf_pop_w[u]};
      end

      // ---- merged arm issue (FSM FIFOs round-robin, cadence in idle) ----
      unique case (tm_st_r)
        TM_SEL: begin
          if ((tf_cnt_r[0] != 6'd0) && (!tm_rr_r || (tf_cnt_r[1] == 6'd0)))
          begin
            tm_sel_r <= 1'b0;
            tm_st_r  <= TM_POP;
          end else if (tf_cnt_r[1] != 6'd0) begin
            tm_sel_r <= 1'b1;
            tm_st_r  <= TM_POP;
          end else if (cad_pend_r != '0) begin
            arm_valid_o       <= 1'b1;
            arm_cancel_o      <= 1'b0;
            arm_slot_o        <= SLOT_AW_P'(CAD_SLOT_BASE_P + 32'(cad_ix_w));
            arm_owner_o       <= CAD_OWNER_BASE_P + {5'd0, cad_ix_w};
            arm_deadline_ms_o <= cad_dl_r[cad_ix_w];
            cad_pend_r[cad_ix_w] <= 1'b0;
          end
        end
        default: begin   // TM_POP — tf_q_r[tm_sel_r] is stable (2-cycle rhythm)
          arm_valid_o <= 1'b1;
          {arm_cancel_o, arm_slot_o, arm_owner_o, arm_deadline_ms_o}
            <= tf_q_r[tm_sel_r];
          tf_rptr_r[tm_sel_r] <= tf_rptr_r[tm_sel_r] + 5'd1;
          tm_rr_r <= ~tm_rr_r;
          tm_st_r <= TM_SEL;
        end
      endcase

      // ---- MSRP round completion + high-water interim drain -------------
      if (rnd_act_r && tk_txop_done_w) td_tk_r <= 1'b1;
      if (rnd_act_r && ls_txop_done_w) td_ls_r <= 1'b1;
      if (rnd_act_r && (td_tk_r || tk_txop_done_w)
          && (td_ls_r || ls_txop_done_w)) begin
        enc_join_r[0] <= 1'b1;   // the cadence's messages ride its MRPDU
        rnd_act_r     <= 1'b0;
      end
      hw_full_q_r <= enc_msrp_full_w;
      if (rnd_act_r && enc_msrp_full_w && !hw_full_q_r) begin
        enc_join_r[0] <= 1'b1;   // pending table full mid-walk: interim drain
      end

      // ---- PRNG draws (single client; one outstanding) ------------------
      if (dr_inflight_r) begin
        if (draw_valid_i) begin
          dr_inflight_r <= 1'b0;
          if (dr_app_r) begin
            cad_pend_r[CAD_LA_MVRP_C] <= 1'b1;
            cad_dl_r[CAD_LA_MVRP_C]   <= now_ms_i + {16'd0, draw_ms_i};
          end else begin
            cad_pend_r[CAD_LA_MSRP_C] <= 1'b1;
            cad_dl_r[CAD_LA_MSRP_C]   <= now_ms_i + {16'd0, draw_ms_i};
          end
        end
      end else if (!draw_busy_i && (need_draw_r != 2'b00)) begin
        draw_req_o    <= 1'b1;
        dr_inflight_r <= 1'b1;
        dr_app_r      <= !need_draw_r[0];
        if (need_draw_r[0]) need_draw_r[0] <= 1'b0;
        else                need_draw_r[1] <= 1'b0;
      end

      // ---- startup arming ------------------------------------------------
      if (!init_done_r) begin
        init_done_r <= 1'b1;
        cad_pend_r[CAD_JOIN_MSRP_C] <= 1'b1;
        cad_dl_r[CAD_JOIN_MSRP_C]   <= now_ms_i + JOIN_MS_P;
        cad_pend_r[CAD_JOIN_MVRP_C] <= 1'b1;
        cad_dl_r[CAD_JOIN_MVRP_C]   <= now_ms_i + JOIN_MS_P;
        cad_pend_r[CAD_PERIODIC_C]  <= 1'b1;
        cad_dl_r[CAD_PERIODIC_C]    <= now_ms_i + PERIODIC_MS_P;
        need_draw_r <= 2'b11;
      end

      // ---- cadence expiries (sets after clears: a set wins) --------------
      if (cad_hit_w) begin
        unique case (cad_exp_ix_w[2:0])
          3'(CAD_JOIN_MSRP_C): begin
            p_join_fsm_r <= 1'b1;    // walks first, encoder drain after
            rnd_act_r    <= 1'b1;
            td_tk_r      <= 1'b0;
            td_ls_r      <= 1'b0;
            cad_pend_r[CAD_JOIN_MSRP_C] <= 1'b1;
            cad_dl_r[CAD_JOIN_MSRP_C]   <= now_ms_i + JOIN_MS_P;
          end
          3'(CAD_JOIN_MVRP_C): begin
            enc_join_r[1] <= 1'b1;   // event-driven pushes: drain directly
            cad_pend_r[CAD_JOIN_MVRP_C] <= 1'b1;
            cad_dl_r[CAD_JOIN_MVRP_C]   <= now_ms_i + JOIN_MS_P;
          end
          3'(CAD_PERIODIC_C): begin
            p_periodic_r <= 1'b1;
            cad_pend_r[CAD_PERIODIC_C] <= 1'b1;
            cad_dl_r[CAD_PERIODIC_C]   <= now_ms_i + PERIODIC_MS_P;
          end
          3'(CAD_LA_MSRP_C): begin
            p_la_msrp_r    <= 1'b1;  // FSMs age + txLA!; Domain re-declares
            enc_la_r[0]    <= 1'b1;  // LeaveAllEvent rides the next MSRP PDU
            need_draw_r[0] <= 1'b1;  // fresh 10-15 s draw re-arms the slot
          end
          default: begin             // CAD_LA_MVRP_C
            p_la_mvrp_r    <= 1'b1;  // VLAN re-joins every held VID
            enc_la_r[1]    <= 1'b1;
            need_draw_r[1] <= 1'b1;
          end
        endcase
      end
    end
  end

  assign tf_pop_w[0] = (tm_st_r == TM_POP) && !tm_sel_r;
  assign tf_pop_w[1] = (tm_st_r == TM_POP) && tm_sel_r;

endmodule : KL_srp_top
`default_nettype wire

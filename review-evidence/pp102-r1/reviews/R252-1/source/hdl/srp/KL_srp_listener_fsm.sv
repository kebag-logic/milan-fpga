/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_listener_fsm.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §4 applicant/registrar note, §5 state,
//                 §6.4 F10.5 per-sink matcher + Listener declaration,
//                 §6.5 F10.9 LeaveAll + Δ13, 08 §2 T-MRP-* cadences,
//                 05 §6.x A15/A8 settle/teardown, 02 §4.1 srp contract)
//
//  Description : The per-sink listener-side SRP stream FSMs — all
//                N = P-N-STREAM-IN of them in one module. Each sink carries
//                the 10 §4 pair for its settled stream: a Table 10-4
//                registrar (with Δ13) matching Talker Advertise/Failed
//                values EXACTLY on the ACMP-settled {stream_id, DA, VLAN}
//                (Milan §5.3.8.9 — a divergent attribute is simply no
//                match), and a FULL 802.1Q Table 10-3 applicant declaring
//                the Listener attribute (type 3, FirstValue = stream_id)
//                whose FourPacked parameter follows the match: Ready on a
//                registered Advertise, AskingFailed on a registered Failed
//                (the F10.5 "optionally declare AskingFailed" option IS
//                taken — GET_RX_STATE's RF lineage needs the declaration).
//                The matcher is armed by ACMP settle (A15, + VLAN user++)
//                and torn down by A8 (+ VLAN user--, declaration
//                withdrawn, NO unregister event — teardown edges of F10.5
//                carry none). EVT_TK_REGISTERED strobes on a fresh
//                registration AND on the in-place Advertise↔Failed swap
//                (the type change is an implicit rLv of the old type plus
//                the new registration, 802.1Q §35.2.6 — the registrar
//                never leaves IN, no unregistration event separates the
//                two); EVT_TK_UNREGISTERED strobes on Δ13's immediate
//                IN→MT rLv (on the frame that withdraws the talker — Milan
//                §4.2.7.2.2) and on a LeaveAll-cycle T-MRP-LEAVE expiry,
//                the only LV path. acc_latency[sink] latches the
//                registered attribute's accumulated_latency on every
//                registering event (a refresh re-latches);
//                msrp_fail_code/bridge[sink] latch the Talker Failed
//                FailureInformation while FAILED is the registered type.
//                Messages ride tx!/txLA! walks exactly as in
//                KL_srp_talker_fsm (optional [s]/[sJ]/[sL] never sent;
//                periodic! carries the re-join).
//
//  Decision    : the one decision that matters — same as the talker side:
//                per-sink records and FSM state live in FLOPS with
//                parallel {stream_id, DA, VLAN} comparators, never a
//                shared RAM-shaped record, because KL_srp_decoder emits
//                one unback-pressured event per cycle while draining a
//                packed vector and every sink must compare in that cycle.
//                The Table 10-3/10-4 functions are duplicated from
//                KL_srp_talker_fsm BY DESIGN (the suite walks both
//                against one independently transcribed table, so a
//                divergence cannot land), the applicant's sJ/s/note-8
//                registrar term is tied 0 (a Listener declaration is
//                never reflected back into the sink's port), and an A15
//                settle that lands while the previous binding's applicant
//                is still winding down FORCES it to VO: the un-sent
//                Listener Lv is abandoned and ages out at the bridge on
//                its next LeaveAll cycle — the alternative would couple
//                ACMP settle latency to the T-MRP-JOIN cadence.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_listener_fsm
  import srp_pkg::*;
#(
    //! stream sinks N = P-N-STREAM-IN
    parameter int unsigned N_SINKS_P    = 8,
    //! T-MRP-LEAVE in ms (F08.1: 5000)
    parameter int unsigned LEAVE_MS_P   = 5000,
    //! first KL_pp_timer_service slot of this module's per-sink
    //! registrar-leave block (F08.4 pool); slot k = SLOT_BASE_P + k
    parameter int unsigned SLOT_BASE_P  = 0,
    //! timer-service slot address width ($clog2 of its SLOTS_P)
    parameter int unsigned SLOT_AW_P    = 7,
    //! owner tag of slot k = OWNER_BASE_P + k (echoed at expiry)
    parameter logic [7:0]  OWNER_BASE_P = 8'h60,
    //! derived sink-index width — do not override
    localparam int unsigned SNK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1
) (
    input  wire         clk_i,           //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,           //! synchronous active-low reset

    input  wire         p2p_i,           //! operPointToPointMAC (Table 10-3 notes 4/5); Milan ties 1

    // ---- ACMP settle / teardown (A15 / A8; one op per accept) -------------
    input  wire                ctl_valid_i,     //! op offered, held until ready
    output logic               ctl_ready_o,     //! accept (low on decoder-event cycles)
    input  wire                ctl_settle_i,    //! 1 = A15 arm (params below valid), 0 = A8 teardown
    input  wire  [SNK_W_C-1:0] ctl_sink_i,      //! sink index of the op
    input  wire  [63:0]        ctl_stream_id_i, //! settled stream_id (PROBE_TX_RESPONSE)
    input  wire  [47:0]        ctl_da_i,        //! settled destination MAC
    input  wire  [11:0]        ctl_vid_i,       //! settled VLAN

    // ---- KL_srp_decoder per-value events (exact port widths) --------------
    input  wire         evt_valid_i,             //! one strobe per vector value k
    input  wire         evt_msrp_i,              //! application: 1 = MSRP (MVRP never matches here)
    input  wire  [7:0]  evt_attr_type_i,         //! F10.8 AttributeType
    input  wire  [63:0] evt_stream_id_i,         //! reconstructed k-th stream_id
    input  wire  [47:0] evt_da_i,                //! reconstructed k-th destination_address
    input  wire  [15:0] evt_vid_i,               //! talker vlan_id (0 for Listener values)
    input  wire  [2:0]  evt_mrp_event_i,         //! three-packed event (srp_event_e)
    input  wire  [31:0] evt_acc_latency_i,       //! talker accumulated_latency (§35.2.2.8.6)
    input  wire  [63:0] evt_failure_system_id_i, //! Talker Failed FailureInformation system id
    input  wire  [7:0]  evt_failure_code_i,      //! Talker Failed failure code

    // ---- MSRP participant cadence (timer expiries via the event router) ---
    input  wire         join_tick_i,      //! T-MRP-JOIN: tx! opportunity for every applicant
    input  wire         periodic_tick_i,  //! T-MRP-PERIODIC: periodic! row
    input  wire         leaveall_rx_i,    //! received MSRP LeaveAll (decoder la_msrp_o) — rLA!
    input  wire         leaveall_own_i,   //! own MSRP leavealltimer expiry — next walk is txLA!
    output logic        txop_done_o,      //! one-cycle strobe: tick walk finished, pushes accepted

    // ---- KL_srp_encoder intake face (exact port match) --------------------
    output logic         ev_valid_o,     //! event offered, held until ready
    input  wire          ev_ready_i,     //! encoder accepts the event
    output logic         ev_app_o,       //! constant 0 = MSRP participant
    output logic [7:0]   ev_attr_type_o, //! constant 3 = Listener attribute
    output logic [2:0]   ev_event_o,     //! attribute event (10 §3 alphabet)
    output logic [1:0]   ev_fourpack_o,  //! declared parameter (Ready / AskingFailed)
    output logic [271:0] ev_value_o,     //! FirstValue = stream_id at [271:208]

    // ---- KL_srp_vlan user face (exact port match) -------------------------
    output logic        user_valid_o,    //! membership op, held until ready
    output logic        user_join_o,     //! 1 = join user_vid_o, 0 = leave it
    output logic [11:0] user_vid_o,      //! the sink's settled VID
    input  wire         user_ready_i,    //! KL_srp_vlan accepts the op

    // ---- KL_pp_timer_service faces (exact port match) ---------------------
    input  wire  [31:0]          now_ms_i,          //! absolute ms timebase (now_ms_o)
    output logic                 arm_valid_o,       //! arm/cancel strobe (service always accepts)
    output logic                 arm_cancel_o,      //! 1 = cancel the slot
    output logic [SLOT_AW_P-1:0] arm_slot_o,        //! SLOT_BASE_P + sink
    output logic [7:0]           arm_owner_o,       //! OWNER_BASE_P + sink
    output logic [31:0]          arm_deadline_ms_o, //! now + T-MRP-LEAVE (absolute)
    input  wire                  exp_valid_i,       //! timer-service expiry strobe
    input  wire  [SLOT_AW_P-1:0] exp_slot_i,        //! expired slot index

    // ---- class-C strobes + class-D levels (F02.10) ------------------------
    output logic [N_SINKS_P-1:0]       evt_tk_registered_o,   //! TK_ATTR_REGISTERED{sink}
    output logic [N_SINKS_P-1:0]       evt_tk_unregistered_o, //! TK_ATTR_UNREGISTERED{sink}
    output logic [N_SINKS_P-1:0][1:0]  tk_reg_state_o,        //! 0 NONE / 1 ADVERTISE / 2 FAILED
    output logic [N_SINKS_P-1:0][1:0]  lstn_decl_state_o,     //! 0 NONE / 1 ASKING_FAILED / 2 READY
    output logic [N_SINKS_P-1:0][31:0] acc_latency_o,         //! latched accumulated_latency
    output logic [N_SINKS_P-1:0][7:0]  msrp_fail_code_o,      //! latched failure code while FAILED
    output logic [N_SINKS_P-1:0][63:0] msrp_fail_bridge_o,    //! latched failure system id while FAILED

    // ---- observability (MTXW applicant/registrar walk) --------------------
    output logic [N_SINKS_P-1:0][3:0] dbg_app_state_o, //! Table 10-3 applicant state per sink
    output logic [N_SINKS_P-1:0][1:0] dbg_reg_state_o  //! Table 10-4 registrar {0 MT, 1 IN, 2 LV}
);

  // ---- Table 10-3 applicant states (802.1Q §10.7.1 abbreviations) --------
  localparam logic [3:0] A_VO_C = 4'd0;
  localparam logic [3:0] A_VP_C = 4'd1;
  localparam logic [3:0] A_VN_C = 4'd2;
  localparam logic [3:0] A_AN_C = 4'd3;
  localparam logic [3:0] A_AA_C = 4'd4;
  localparam logic [3:0] A_QA_C = 4'd5;
  localparam logic [3:0] A_LA_C = 4'd6;
  localparam logic [3:0] A_AO_C = 4'd7;
  localparam logic [3:0] A_QO_C = 4'd8;
  localparam logic [3:0] A_AP_C = 4'd9;
  localparam logic [3:0] A_QP_C = 4'd10;
  localparam logic [3:0] A_LO_C = 4'd11;

  // ---- applicant events (Table 10-3 rows; rx codes = srp event + 3) ------
  localparam logic [3:0] AE_NEW_C     = 4'd0;
  localparam logic [3:0] AE_JOIN_C    = 4'd1;
  localparam logic [3:0] AE_LV_C      = 4'd2;
  localparam logic [3:0] AE_RNEW_C    = 4'd3;
  localparam logic [3:0] AE_RJOININ_C = 4'd4;
  localparam logic [3:0] AE_RIN_C     = 4'd5;
  localparam logic [3:0] AE_RJOINMT_C = 4'd6;
  localparam logic [3:0] AE_RMT_C     = 4'd7;
  localparam logic [3:0] AE_RLV_C     = 4'd8;
  localparam logic [3:0] AE_RLA_C     = 4'd9;
  localparam logic [3:0] AE_PER_C     = 4'd10;
  localparam logic [3:0] AE_TX_C      = 4'd11;
  localparam logic [3:0] AE_TXLA_C    = 4'd12;

  // ---- Table 10-4 registrar states ---------------------------------------
  localparam logic [1:0] R_MT_C = 2'd0;
  localparam logic [1:0] R_IN_C = 2'd1;
  localparam logic [1:0] R_LV_C = 2'd2;

  // ---- timer-op pend codes ------------------------------------------------
  localparam logic [1:0] T_NOP_C    = 2'd0;
  localparam logic [1:0] T_ARM_C    = 2'd1;
  localparam logic [1:0] T_CANCEL_C = 2'd2;

  // ---- declaration-request pend codes (registrar -> applicant) -----------
  localparam logic [1:0] D_NOP_C      = 2'd0;
  localparam logic [1:0] D_DECLARE_C  = 2'd1;
  localparam logic [1:0] D_WITHDRAW_C = 2'd2;

  //! Table 10-3 next-state — same transcription as KL_srp_talker_fsm
  //! (duplicated by design, see banner; the suite walks both)
  function automatic logic [3:0] app_next_f(
      input logic [3:0] st,
      input logic [3:0] ev,
      input logic       reg_in_i,
      input logic       p2p
  );
    logic [3:0] nx;
    nx = st;
    case (ev)
      AE_NEW_C:  if (!(st inside {A_VN_C, A_AN_C})) nx = A_VN_C;
      AE_JOIN_C: begin
        case (st)
          A_VO_C:  nx = A_VP_C;
          A_LA_C:  nx = A_AA_C;
          A_AO_C:  nx = A_AP_C;
          A_QO_C:  nx = A_QP_C;
          A_LO_C:  nx = A_VP_C;
          default: nx = st;
        endcase
      end
      AE_LV_C: begin
        case (st)
          A_VP_C:  nx = A_VO_C;
          A_VN_C, A_AN_C, A_AA_C, A_QA_C: nx = A_LA_C;
          A_AP_C:  nx = A_AO_C;
          A_QP_C:  nx = A_QO_C;
          default: nx = st;
        endcase
      end
      AE_RNEW_C: nx = st;
      AE_RJOININ_C: begin
        case (st)
          A_VO_C:  nx = p2p ? st : A_AO_C;   // note 4
          A_VP_C:  nx = p2p ? st : A_AP_C;   // note 4
          A_AA_C:  nx = A_QA_C;
          A_AO_C:  nx = A_QO_C;
          A_AP_C:  nx = A_QP_C;
          default: nx = st;
        endcase
      end
      AE_RIN_C:  if (p2p && (st == A_AA_C)) nx = A_QA_C;   // note 5
      AE_RJOINMT_C, AE_RMT_C: begin
        case (st)
          A_QA_C:  nx = A_AA_C;
          A_QO_C:  nx = A_AO_C;
          A_QP_C:  nx = A_AP_C;
          A_LO_C:  nx = A_VO_C;
          default: nx = st;
        endcase
      end
      AE_RLV_C, AE_RLA_C: begin
        case (st)
          A_VO_C, A_AO_C, A_QO_C: nx = A_LO_C;   // note 1
          A_AN_C:  nx = A_VN_C;
          A_AA_C, A_QA_C, A_AP_C, A_QP_C: nx = A_VP_C;   // note 9
          default: nx = st;                       // VP, VN, LA (note 10), LO
        endcase
      end
      AE_PER_C: begin
        case (st)
          A_QA_C:  nx = A_AA_C;
          A_QP_C:  nx = A_AP_C;
          default: nx = st;
        endcase
      end
      AE_TX_C: begin
        case (st)
          A_VP_C:  nx = A_AA_C;
          A_VN_C:  nx = A_AN_C;
          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8
          A_AA_C:  nx = A_QA_C;
          A_LA_C:  nx = A_VO_C;
          A_AP_C:  nx = A_QA_C;
          A_LO_C:  nx = A_VO_C;
          default: nx = st;
        endcase
      end
      AE_TXLA_C: begin
        case (st)
          A_VO_C, A_LA_C, A_AO_C, A_QO_C: nx = A_LO_C;
          A_VP_C:  nx = A_AA_C;
          A_VN_C:  nx = A_AN_C;
          A_AN_C, A_AA_C, A_AP_C, A_QP_C: nx = A_QA_C;
          default: nx = st;
        endcase
      end
      default: nx = st;
    endcase
    return nx;
  endfunction

  //! Table 10-3 message action on a transmit opportunity — [3] = send,
  //! [2:0] = attribute-event code; optional encodings never sent (banner)
  function automatic logic [3:0] app_msg_f(
      input logic [3:0] st,
      input logic       txla,
      input logic       reg_in_i
  );
    logic [2:0] sj_w;
    logic [2:0] s_w;
    logic [3:0] m;
    sj_w = reg_in_i ? SRP_EV_JOININ : SRP_EV_JOINMT;
    s_w  = reg_in_i ? SRP_EV_IN : SRP_EV_MT;
    if (!txla) begin
      case (st)
        A_VP_C, A_AA_C, A_AP_C: m = {1'b1, sj_w};
        A_VN_C, A_AN_C:         m = {1'b1, SRP_EV_NEW};
        A_LA_C:                 m = {1'b1, SRP_EV_LV};
        A_LO_C:                 m = {1'b1, s_w};
        default:                m = {1'b0, 3'd0};
      endcase
    end else begin
      case (st)
        A_VP_C:                 m = {1'b1, s_w};
        A_VN_C, A_AN_C:         m = {1'b1, SRP_EV_NEW};
        A_AA_C, A_QA_C, A_AP_C, A_QP_C: m = {1'b1, sj_w};
        default:                m = {1'b0, 3'd0};
      endcase
    end
    return m;
  endfunction

  //! declaring = applicant in a member state (F10.5 declared Listener)
  function automatic logic app_declaring_f(input logic [3:0] st);
    return st inside {A_VP_C, A_VN_C, A_AN_C, A_AA_C, A_QA_C, A_AP_C, A_QP_C};
  endfunction

  // ------------------------------------------------------------ registers
  // per-sink settled record (armed by A15, torn down by A8)
  logic [N_SINKS_P-1:0]        rec_valid_r;   // record latched (persists past A8)
  logic [N_SINKS_P-1:0]        armed_r;       // matcher armed (A15..A8 window)
  logic [N_SINKS_P-1:0][63:0]  sid_r;
  logic [N_SINKS_P-1:0][47:0]  da_r;
  logic [N_SINKS_P-1:0][11:0]  vid_r;

  // per-sink applicant plane
  logic [N_SINKS_P-1:0][3:0]   app_r;
  logic [N_SINKS_P-1:0][1:0]   fourpack_r;    // declared parameter
  logic [N_SINKS_P-1:0][1:0]   decl_pend_r;   // registrar -> applicant request
  logic [N_SINKS_P-1:0][1:0]   decl_fp_r;     // parameter riding the request
  logic [N_SINKS_P-1:0]        rla_pend_r;
  logic [N_SINKS_P-1:0]        per_pend_r;

  // tick walk
  typedef enum logic [1:0] {
    W_IDLE = 2'd0,
    W_EVAL = 2'd1,
    W_PUSH = 2'd2,
    W_DONE = 2'd3
  } walk_e;
  walk_e               walk_r;
  logic [SNK_W_C-1:0]  wsrc_r;
  logic                wtxla_r;
  logic                tick_pend_r;
  logic                laown_pend_r;
  logic [2:0]          push_code_r;
  logic [1:0]          push_fp_r;
  logic [271:0]        push_val_r;

  // per-sink registrar plane (talker matcher)
  logic [N_SINKS_P-1:0][1:0]   reg_r;
  logic [N_SINKS_P-1:0]        rtype_r;     // 0 = ADVERTISE, 1 = FAILED
  logic [N_SINKS_P-1:0][31:0]  lat_r;
  logic [N_SINKS_P-1:0][7:0]   fcode_r;
  logic [N_SINKS_P-1:0][63:0]  fsysid_r;
  logic [N_SINKS_P-1:0][1:0]   tpend_r;

  // VLAN membership op pends (join at settle, leave at teardown)
  logic [N_SINKS_P-1:0]        vj_pend_r;
  logic [N_SINKS_P-1:0]        vl_pend_r;
  logic [N_SINKS_P-1:0][11:0]  vj_vid_r;
  logic [N_SINKS_P-1:0][11:0]  vl_vid_r;

  // -------------------------------------------------------- event matching
  logic [N_SINKS_P-1:0] app_rx_hit_w;   // Listener values on own stream_id
  logic [N_SINKS_P-1:0] reg_rx_hit_w;   // Talker Adv/Failed, exact triple
  logic [3:0]           rx_app_ev_w;
  logic                 rx_is_failed_w;
  logic                 rx_registering_w;

  always_comb begin : hit_map
    rx_app_ev_w    = {1'b0, evt_mrp_event_i} + AE_RNEW_C;
    rx_is_failed_w = (evt_attr_type_i == SRP_MSRP_ATTR_TALKER_FAILED_C);
    rx_registering_w = (evt_mrp_event_i == 3'(SRP_EV_NEW))
                    || (evt_mrp_event_i == 3'(SRP_EV_JOININ))
                    || (evt_mrp_event_i == 3'(SRP_EV_JOINMT));
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      app_rx_hit_w[s] = evt_valid_i && evt_msrp_i && rec_valid_r[s]
                     && (evt_attr_type_i == SRP_MSRP_ATTR_LISTENER_C)
                     && (evt_mrp_event_i <= 3'(SRP_EV_LV))
                     && (evt_stream_id_i == sid_r[s]);
      reg_rx_hit_w[s] = evt_valid_i && evt_msrp_i && armed_r[s]
                     && ((evt_attr_type_i == SRP_MSRP_ATTR_TALKER_ADV_C)
                         || (evt_attr_type_i == SRP_MSRP_ATTR_TALKER_FAILED_C))
                     && (evt_stream_id_i == sid_r[s])
                     && (evt_da_i == da_r[s])
                     && (evt_vid_i == {4'd0, vid_r[s]});
    end
  end

  // ------------------------------------------------- registrar indications
  // computed combinationally so the applicant plane can own decl_pend_r
  logic                 leaveall_any_w;
  logic                 exp_hit_w;
  logic [31:0]          exp_idx_w;
  logic [N_SINKS_P-1:0] ind_reg_w;     // fresh registration or type swap
  logic [N_SINKS_P-1:0] ind_unreg_w;   // Δ13 rLv or leavetimer expiry

  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;
  // unsigned wrap maps below-base slots to huge indices — one bound check
  assign exp_idx_w = 32'(exp_slot_i) - SLOT_BASE_P;
  assign exp_hit_w = exp_valid_i && (exp_idx_w < N_SINKS_P);

  always_comb begin : reg_ind
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      ind_reg_w[s] = reg_rx_hit_w[s] && rx_registering_w
                  && ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));
      ind_unreg_w[s] = (reg_rx_hit_w[s]
                        && (evt_mrp_event_i == 3'(SRP_EV_LV))
                        && (reg_r[s] == R_IN_C))
                    || (exp_hit_w && (exp_idx_w == s)
                        && (reg_r[s] == R_LV_C) && (tpend_r[s] != T_ARM_C)
                        && !(reg_rx_hit_w[s] && rx_registering_w));
    end
  end

  // ------------------------------------------------- applicant arbitration
  logic                 ctl_acc_w;
  logic [N_SINKS_P-1:0] app_ev_v_w;
  logic [N_SINKS_P-1:0][3:0] app_ev_w;
  logic [N_SINKS_P-1:0] decl_grant_w;
  logic [N_SINKS_P-1:0] rla_grant_w;
  logic [N_SINKS_P-1:0] per_grant_w;
  logic                 walk_grant_w;

  assign ctl_ready_o = !evt_valid_i;
  assign ctl_acc_w   = ctl_valid_i && ctl_ready_o;

  always_comb begin : app_arb
    walk_grant_w = 1'b0;
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      app_ev_v_w[s]   = 1'b0;
      app_ev_w[s]     = AE_RNEW_C;
      decl_grant_w[s] = 1'b0;
      rla_grant_w[s]  = 1'b0;
      per_grant_w[s]  = 1'b0;
      if (app_rx_hit_w[s]) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = rx_app_ev_w;
      end else if (ctl_acc_w && (ctl_sink_i == SNK_W_C'(s))) begin
        // settle forces VO directly (banner); teardown withdraws
        app_ev_v_w[s] = !ctl_settle_i;
        app_ev_w[s]   = AE_LV_C;
      end else if (decl_pend_r[s] != D_NOP_C) begin
        app_ev_v_w[s]   = 1'b1;
        app_ev_w[s]     = (decl_pend_r[s] == D_DECLARE_C) ? AE_NEW_C : AE_LV_C;
        decl_grant_w[s] = 1'b1;
      end else if (rla_pend_r[s] || leaveall_rx_i) begin
        app_ev_v_w[s]  = 1'b1;
        app_ev_w[s]    = AE_RLA_C;
        rla_grant_w[s] = 1'b1;
      end else if (per_pend_r[s] || periodic_tick_i) begin
        app_ev_v_w[s]  = 1'b1;
        app_ev_w[s]    = AE_PER_C;
        per_grant_w[s] = 1'b1;
      end else if ((walk_r == W_EVAL) && (wsrc_r == SNK_W_C'(s))) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = wtxla_r ? AE_TXLA_C : AE_TX_C;
        walk_grant_w  = 1'b1;
      end
    end
  end

  // Listener FirstValue of the walk sink (F10.8: 8 B stream_id)
  logic [271:0] wval_w;
  logic [3:0]   wmsg_w;
  always_comb begin : walk_msg
    wval_w = 272'd0;
    wval_w[271:208] = sid_r[wsrc_r];
    wmsg_w = app_msg_f(app_r[wsrc_r], wtxla_r, 1'b0);
  end

  // ------------------------------------------------------- applicant plane
  always_ff @(posedge clk_i) begin : app_plane
    if (!rst_n) begin
      rec_valid_r  <= '0;
      armed_r      <= '0;
      sid_r        <= '0;
      da_r         <= '0;
      vid_r        <= '0;
      app_r        <= '0;      // Begin! = VO everywhere
      fourpack_r   <= '0;
      decl_pend_r  <= '0;
      decl_fp_r    <= '0;
      rla_pend_r   <= '0;
      per_pend_r   <= '0;
      walk_r       <= W_IDLE;
      wsrc_r       <= '0;
      wtxla_r      <= 1'b0;
      tick_pend_r  <= 1'b0;
      laown_pend_r <= 1'b0;
      push_code_r  <= 3'd0;
      push_fp_r    <= 2'd0;
      push_val_r   <= '0;
      txop_done_o  <= 1'b0;
    end else begin
      txop_done_o <= 1'b0;

      // ---- per-sink applicant transitions -------------------------------
      for (int unsigned s = 0; s < N_SINKS_P; s++) begin
        if (app_ev_v_w[s]) begin
          app_r[s] <= app_next_f(app_r[s], app_ev_w[s], 1'b0, p2p_i);
        end
        // declaration requests from the registrar indications
        if (ind_reg_w[s]) begin
          decl_pend_r[s] <= D_DECLARE_C;
          decl_fp_r[s]   <= rx_is_failed_w ? 2'(SRP_DECL_ASKING_FAILED)
                                           : 2'(SRP_DECL_READY);
        end else if (ind_unreg_w[s]) begin
          decl_pend_r[s] <= D_WITHDRAW_C;
        end else if (decl_grant_w[s]) begin
          decl_pend_r[s] <= D_NOP_C;
        end
        if (decl_grant_w[s] && (decl_pend_r[s] == D_DECLARE_C)) begin
          fourpack_r[s] <= decl_fp_r[s];
        end
        // deferred-broadcast bookkeeping
        if (leaveall_rx_i && !rla_grant_w[s]
            && (!app_ev_v_w[s] || (app_ev_w[s] != AE_RLA_C))) begin
          rla_pend_r[s] <= 1'b1;
        end else if (rla_grant_w[s]) begin
          rla_pend_r[s] <= 1'b0;
        end
        if (periodic_tick_i && !per_grant_w[s]
            && (!app_ev_v_w[s] || (app_ev_w[s] != AE_PER_C))) begin
          per_pend_r[s] <= 1'b1;
        end else if (per_grant_w[s]) begin
          per_pend_r[s] <= 1'b0;
        end
      end

      // ---- A15 settle / A8 teardown -------------------------------------
      if (ctl_acc_w) begin
        if (ctl_settle_i) begin
          rec_valid_r[ctl_sink_i] <= 1'b1;
          armed_r[ctl_sink_i]     <= 1'b1;
          sid_r[ctl_sink_i]       <= ctl_stream_id_i;
          da_r[ctl_sink_i]        <= ctl_da_i;
          vid_r[ctl_sink_i]       <= ctl_vid_i;
          app_r[ctl_sink_i]       <= A_VO_C;    // abandon a wind-down (banner)
          decl_pend_r[ctl_sink_i] <= D_NOP_C;
          fourpack_r[ctl_sink_i]  <= 2'd0;
        end else begin
          armed_r[ctl_sink_i]     <= 1'b0;
          decl_pend_r[ctl_sink_i] <= D_NOP_C;   // Lv! applied via app_ev this cycle
        end
      end

      // ---- own LeaveAll marks the next walk txLA! -----------------------
      if (leaveall_own_i) laown_pend_r <= 1'b1;

      // ---- tick walk ----------------------------------------------------
      case (walk_r)
        W_IDLE: begin
          if (join_tick_i || tick_pend_r) begin
            tick_pend_r  <= 1'b0;
            wtxla_r      <= laown_pend_r;
            laown_pend_r <= 1'b0;
            wsrc_r       <= '0;
            walk_r       <= W_EVAL;
          end
        end
        W_EVAL: begin
          if (join_tick_i) tick_pend_r <= 1'b1;
          if (walk_grant_w) begin
            if (wmsg_w[3] && rec_valid_r[wsrc_r]) begin
              push_code_r <= wmsg_w[2:0];
              push_fp_r   <= fourpack_r[wsrc_r];
              push_val_r  <= wval_w;
              walk_r      <= W_PUSH;
            end else if (wsrc_r == SNK_W_C'(N_SINKS_P - 1)) begin
              walk_r <= W_DONE;
            end else begin
              wsrc_r <= wsrc_r + SNK_W_C'(1);
            end
          end
        end
        W_PUSH: begin
          if (join_tick_i) tick_pend_r <= 1'b1;
          if (ev_ready_i) begin
            if (wsrc_r == SNK_W_C'(N_SINKS_P - 1)) begin
              walk_r <= W_DONE;
            end else begin
              wsrc_r <= wsrc_r + SNK_W_C'(1);
              walk_r <= W_EVAL;
            end
          end
        end
        default: begin   // W_DONE
          if (join_tick_i) tick_pend_r <= 1'b1;
          txop_done_o <= 1'b1;
          walk_r      <= W_IDLE;
        end
      endcase
    end
  end

  assign ev_valid_o     = (walk_r == W_PUSH);
  assign ev_app_o       = 1'b0;                       // MSRP participant
  assign ev_attr_type_o = SRP_MSRP_ATTR_LISTENER_C;
  assign ev_event_o     = push_code_r;
  assign ev_fourpack_o  = push_fp_r;
  assign ev_value_o     = push_val_r;

  // ------------------------------------------------------- registrar plane
  // Table 10-4 with Δ13 — see KL_srp_talker_fsm; here the tracked
  // attribute is the matched Talker Advertise/Failed, with the in-place
  // type swap kept inside IN (§35.2.6)
  logic               tsel_v_w;
  logic [SNK_W_C-1:0] tsel_ix_w;
  always_comb begin : tissue_sel
    tsel_v_w  = 1'b0;
    tsel_ix_w = '0;
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      if (!tsel_v_w && (tpend_r[s] != T_NOP_C)) begin
        tsel_v_w  = 1'b1;
        tsel_ix_w = SNK_W_C'(s);
      end
    end
  end

  always_ff @(posedge clk_i) begin : reg_plane
    if (!rst_n) begin
      reg_r                 <= '0;
      rtype_r               <= '0;
      lat_r                 <= '0;
      fcode_r               <= '0;
      fsysid_r              <= '0;
      tpend_r               <= '0;
      evt_tk_registered_o   <= '0;
      evt_tk_unregistered_o <= '0;
      arm_valid_o           <= 1'b0;
      arm_cancel_o          <= 1'b0;
      arm_slot_o            <= '0;
      arm_owner_o           <= 8'd0;
      arm_deadline_ms_o     <= 32'd0;
    end else begin
      evt_tk_registered_o   <= '0;
      evt_tk_unregistered_o <= '0;
      arm_valid_o           <= 1'b0;

      // ---- one leave-timer op per cycle (service accepts O(1)); a
      // same-cycle set to the issued sink lands AFTER this clear in the
      // block, so the newer op survives in the pend and issues next -------
      if (tsel_v_w) begin
        arm_valid_o        <= 1'b1;
        arm_cancel_o       <= (tpend_r[tsel_ix_w] == T_CANCEL_C);
        arm_slot_o         <= SLOT_AW_P'(SLOT_BASE_P + 32'(tsel_ix_w));
        arm_owner_o        <= OWNER_BASE_P + {{(8-SNK_W_C){1'b0}}, tsel_ix_w};
        arm_deadline_ms_o  <= now_ms_i + LEAVE_MS_P;
        tpend_r[tsel_ix_w] <= T_NOP_C;
      end

      // ---- per-sink registrar events ------------------------------------
      for (int unsigned s = 0; s < N_SINKS_P; s++) begin
        if (reg_rx_hit_w[s] && rx_registering_w) begin
          // registering event: -> IN; latch type + payloads; a type change
          // while IN/LV is the in-place swap (strobe, no unregistration)
          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_CANCEL_C;
          reg_r[s]   <= R_IN_C;
          rtype_r[s] <= rx_is_failed_w;
          lat_r[s]   <= evt_acc_latency_i;   // refresh re-latches (10 §6.4)
          if (rx_is_failed_w) begin
            fcode_r[s]  <= evt_failure_code_i;
            fsysid_r[s] <= evt_failure_system_id_i;
          end
          if (ind_reg_w[s]) evt_tk_registered_o[s] <= 1'b1;
        end else if (reg_rx_hit_w[s]
                     && (evt_mrp_event_i == 3'(SRP_EV_LV))) begin
          if (reg_r[s] == R_IN_C) begin
            reg_r[s] <= R_MT_C;              // Δ13: no leavetimer on rLv
            evt_tk_unregistered_o[s] <= 1'b1;
          end
          // LV: Table 10-4 rLv on LV is -x- (the LeaveAll aging continues)
        end else if (leaveall_any_w && (reg_r[s] == R_IN_C)) begin
          reg_r[s]   <= R_LV_C;
          tpend_r[s] <= T_ARM_C;
        end else if (exp_hit_w && (exp_idx_w == s)
                     && (reg_r[s] == R_LV_C) && (tpend_r[s] != T_ARM_C)) begin
          reg_r[s] <= R_MT_C;                // leavetimer! -> MT + Lv
          evt_tk_unregistered_o[s] <= 1'b1;
        end
        // A15 arms a fresh matcher; A8 stops matching (no event — F10.5)
        if (ctl_acc_w && (ctl_sink_i == SNK_W_C'(s))) begin
          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_CANCEL_C;
          reg_r[s] <= R_MT_C;
          //! Clear the registration's DATA on BOTH arms, not just A15.
          //! reg_r goes to R_MT_C either way — the registration is gone — so
          //! leaving lat_r/fcode_r/fsysid_r behind on the A8 teardown arm
          //! publishes the accumulated latency of a registration that no
          //! longer exists. acc_latency_o is ungated, so a fabric reading it
          //! would size its presentation offset from a stale value.
          rtype_r[s]  <= 1'b0;
          lat_r[s]    <= 32'd0;
          fcode_r[s]  <= 8'd0;
          fsysid_r[s] <= 64'd0;
        end
      end
    end
  end

  // --------------------------------------------------------- VLAN op plane
  // lowest-index pending op drives the user face; leave before join per
  // sink (a teardown-then-settle on a new VID frees the old refcount first)
  logic               vsel_v_w;
  logic               vsel_join_w;
  logic [SNK_W_C-1:0] vsel_ix_w;
  always_comb begin : vlan_sel
    vsel_v_w    = 1'b0;
    vsel_join_w = 1'b0;
    vsel_ix_w   = '0;
    user_vid_o  = 12'd0;
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      if (!vsel_v_w) begin
        if (vl_pend_r[s]) begin
          vsel_v_w    = 1'b1;
          vsel_join_w = 1'b0;
          vsel_ix_w   = SNK_W_C'(s);
          user_vid_o  = vl_vid_r[s];
        end else if (vj_pend_r[s]) begin
          vsel_v_w    = 1'b1;
          vsel_join_w = 1'b1;
          vsel_ix_w   = SNK_W_C'(s);
          user_vid_o  = vj_vid_r[s];
        end
      end
    end
  end

  assign user_valid_o = vsel_v_w;
  assign user_join_o  = vsel_join_w;

  always_ff @(posedge clk_i) begin : vlan_plane
    if (!rst_n) begin
      vj_pend_r <= '0;
      vl_pend_r <= '0;
      vj_vid_r  <= '0;
      vl_vid_r  <= '0;
    end else begin
      // retire the op currently held on the user face
      if (vsel_v_w && user_ready_i) begin
        if (vsel_join_w) vj_pend_r[vsel_ix_w] <= 1'b0;
        else             vl_pend_r[vsel_ix_w] <= 1'b0;
      end
      // settle joins, teardown leaves; an unissued opposite op on the
      // same VID collapses to nothing
      if (ctl_acc_w) begin
        if (ctl_settle_i) begin
          if (vl_pend_r[ctl_sink_i] && (vl_vid_r[ctl_sink_i] == ctl_vid_i)
              && !(vsel_v_w && user_ready_i && !vsel_join_w
                   && (vsel_ix_w == ctl_sink_i))) begin
            vl_pend_r[ctl_sink_i] <= 1'b0;   // never left: net zero
          end else begin
            vj_pend_r[ctl_sink_i] <= 1'b1;
            vj_vid_r[ctl_sink_i]  <= ctl_vid_i;
          end
        end else begin
          if (vj_pend_r[ctl_sink_i]
              && !(vsel_v_w && user_ready_i && vsel_join_w
                   && (vsel_ix_w == ctl_sink_i))) begin
            vj_pend_r[ctl_sink_i] <= 1'b0;   // never joined: net zero
          end else begin
            vl_pend_r[ctl_sink_i] <= 1'b1;
            vl_vid_r[ctl_sink_i]  <= vid_r[ctl_sink_i];
          end
        end
      end
    end
  end

  // ---------------------------------------------------- class-C/D outputs
  always_comb begin : status_map
    for (int unsigned s = 0; s < N_SINKS_P; s++) begin
      tk_reg_state_o[s] = (armed_r[s] && (reg_r[s] != R_MT_C))
                        ? (rtype_r[s] ? 2'd2 : 2'd1)
                        : 2'd0;
      lstn_decl_state_o[s] = (rec_valid_r[s] && app_declaring_f(app_r[s]))
                           ? fourpack_r[s]
                           : 2'd0;
      acc_latency_o[s] = lat_r[s];
      msrp_fail_code_o[s]   = (tk_reg_state_o[s] == 2'd2) ? fcode_r[s] : 8'd0;
      msrp_fail_bridge_o[s] = (tk_reg_state_o[s] == 2'd2) ? fsysid_r[s] : 64'd0;
      dbg_app_state_o[s] = app_r[s];
      dbg_reg_state_o[s] = reg_r[s];
    end
  end

endmodule : KL_srp_listener_fsm
`default_nettype wire

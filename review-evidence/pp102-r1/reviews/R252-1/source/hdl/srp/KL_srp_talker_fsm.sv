/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_talker_fsm.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §4 applicant/registrar note, §5 state,
//                 §6.3 F10.4 talker declaration + listener tracking,
//                 §6.5 F10.9 LeaveAll + Δ13, 08 §2 T-MRP-* cadences,
//                 05 §6bis F05.12 DA-gate strobes, 02 §4.1 srp contract)
//
//  Description : The per-source talker-side SRP stream FSMs — all
//                M = P-N-STREAM-OUT of them in one module. Each source
//                carries the 10 §4 pair for its stream: a FULL 802.1Q
//                Table 10-3 applicant declaring the Talker Advertise (or,
//                in the one §6.3 failure case, Talker Failed) attribute,
//                and a Table 10-4 registrar (with Δ13) tracking the
//                Listener attribute registered against its stream_id, whose
//                four-packed value {Ignore, AskingFailed, Ready,
//                ReadyFailed} is published as lstn_reg_state[src] with a
//                LISTENER_REG_CHANGE strobe on every change. The F10.4
//                summary states map onto the applicant: GATED = observer
//                states, DECLARING/DECLARED = member states (QA = quiet
//                declared). The DA-gate (F05.12) drives Join!/New! on open
//                and Lv! on close, with the VLAN membership user++/user--
//                riding the same edges toward KL_srp_vlan. ACTIVE(src) =
//                declaring ∧ {Ready, ReadyFailed} registered ∧
//                sr_admitted_i — and on admission loss the declaration
//                swaps IN PLACE to Talker Failed, failure code 1
//                (insufficient bandwidth) with the station's own MAC as the
//                FailureInformation system identifier (802.1Q §35.1.2.1,
//                §35.2.2.8.7; zero-extended to the 8-byte field), published
//                on msrp_fail_code/bridge[src]; admission return swaps
//                back. Both swaps re-declare via New! so the peer sees the
//                type change as an implicit rLv + new registration
//                (§35.2.6). Δ13 (Milan §4.2.7.2.2): outside the LeaveAll
//                cycle a registrar receiving rLv drops IN→MT on that frame
//                — no leavetimer; the LeaveAll cycle is the only path into
//                LV, aged by a per-source T-MRP-LEAVE slot in
//                KL_pp_timer_service. Messages are generated only at tx!
//                opportunities (T-MRP-JOIN ticks; txLA! after an own
//                LeaveAll) and pushed to the KL_srp_encoder intake face one
//                source at a time; optional [s]/[sJ]/[sL] encodings of
//                802.1Q §10.7.6 are never sent — periodic! (QA→AA) makes
//                the next tx! carry the re-join, which is exactly the
//                F10.4 "LeaveAll or periodic / re-join" edge. txLAF! cannot
//                occur (the encoder's DEPTH_P elaboration check proves a
//                full drain fits one slot). rJoinIn/rIn follow the
//                Table 10-3 notes 4/5 via the p2p_i level
//                (operPointToPointMAC — a Milan link ties it 1).
//
//  Decision    : the one decision that matters — the per-source records and
//                FSM state live in FLOPS with parallel match comparators,
//                not a shared RAM-shaped record: KL_srp_decoder emits one
//                unback-pressured event strobe per cycle while draining a
//                packed vector, so every source must compare {stream_id,
//                DA, VLAN} in the same cycle or lose back-to-back vector
//                values; a sync-read shared record cannot serve M matches
//                per cycle, and at M = 8 the flop cost is small. The
//                Table 10-3/10-4 transition FUNCTIONS are pure
//                (module-scope arrays are never read inside them — sv2v),
//                and the applicant's sJ/s/note-8 registrar term is tied 0:
//                the same-attribute registrar of a DECLARED attribute never
//                registers at a Milan endpoint (a bridge does not reflect a
//                declaration back into its ingress port), so sJ is always
//                JoinMt, s is always Empty, and tx! in AN resolves to AA —
//                the 10 §5 state inventory carries exactly one registrar
//                per source, the Listener tracker.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_talker_fsm
  import srp_pkg::*;
#(
    //! stream sources M = P-N-STREAM-OUT
    parameter int unsigned N_SOURCES_P  = 8,
    //! T-MRP-LEAVE in ms (F08.1: 5000)
    parameter int unsigned LEAVE_MS_P   = 5000,
    //! first KL_pp_timer_service slot of this module's per-source
    //! registrar-leave block (F08.4 pool); slot s = SLOT_BASE_P + s
    parameter int unsigned SLOT_BASE_P  = 0,
    //! timer-service slot address width ($clog2 of its SLOTS_P)
    parameter int unsigned SLOT_AW_P    = 7,
    //! owner tag of slot s = OWNER_BASE_P + s (echoed at expiry)
    parameter logic [7:0]  OWNER_BASE_P = 8'h40,
    //! derived source-index width — do not override
    localparam int unsigned SRC_W_C = (N_SOURCES_P > 1) ? $clog2(N_SOURCES_P)
                                                        : 1
) (
    input  wire         clk_i,           //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,           //! synchronous active-low reset

    input  wire  [47:0] own_mac_i,       //! station MAC — Talker Failed FailureInformation system id
    input  wire         p2p_i,           //! operPointToPointMAC (Table 10-3 notes 4/5); Milan ties 1

    // ---- ACMP DA-gate strobes (F05.12; one op per accept) -----------------
    input  wire                  gate_valid_i,        //! gate op offered, held until ready
    output logic                 gate_ready_o,        //! accept (low on decoder-event cycles)
    input  wire                  gate_open_i,         //! 1 = gate opens (params below valid), 0 = closes
    input  wire  [SRC_W_C-1:0]   gate_src_i,          //! source index of the op
    input  wire  [63:0]          gate_stream_id_i,    //! declared stream_id (own MAC + unique_id)
    input  wire  [47:0]          gate_da_i,           //! declared destination MAC (from maap)
    input  wire  [11:0]          gate_vid_i,          //! declared VLAN (Domain VID at open — frozen after)
    input  wire  [15:0]          gate_max_frame_i,    //! TSpec MaxFrameSize (Milan Table 4.4)
    input  wire  [15:0]          gate_max_interval_i, //! TSpec MaxIntervalFrames (= 1)
    input  wire  [2:0]           gate_prio_i,         //! declared PCP (Domain class A priority)
    input  wire                  gate_rank_i,         //! rank bit (F10.7 byte 20 bit 4)
    input  wire  [31:0]          gate_acc_lat_i,      //! initial accumulated_latency (802.1Q §35.2.2.8.6)

    // ---- Σ-slope admission level (computed upstream, 10 §6.3) -------------
    input  wire  [N_SOURCES_P-1:0] sr_admitted_i,     //! per-source admission against the port ceiling

    // ---- KL_srp_decoder per-value events (exact port widths) --------------
    input  wire         evt_valid_i,      //! one strobe per vector value k
    input  wire         evt_msrp_i,       //! application: 1 = MSRP (MVRP never matches here)
    input  wire  [7:0]  evt_attr_type_i,  //! F10.8 AttributeType
    input  wire  [63:0] evt_stream_id_i,  //! reconstructed k-th stream_id
    input  wire  [47:0] evt_da_i,         //! reconstructed k-th destination_address
    input  wire  [15:0] evt_vid_i,        //! talker vlan_id (0 for Listener values)
    input  wire  [2:0]  evt_mrp_event_i,  //! three-packed event (srp_event_e)
    input  wire  [1:0]  evt_fourpacked_i, //! Listener declaration (srp_decl_e)

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
    output logic [7:0]   ev_attr_type_o, //! 1 Talker Advertise / 2 Talker Failed
    output logic [2:0]   ev_event_o,     //! attribute event (10 §3 alphabet)
    output logic [1:0]   ev_fourpack_o,  //! constant 0 (no FourPacked lane on Talker attributes)
    output logic [271:0] ev_value_o,     //! FirstValue, wire byte 0 at [271:264]

    // ---- KL_srp_vlan user face (exact port match) -------------------------
    output logic        user_valid_o,    //! membership op, held until ready
    output logic        user_join_o,     //! 1 = join user_vid_o, 0 = leave it
    output logic [11:0] user_vid_o,      //! the source's frozen stream VID
    input  wire         user_ready_i,    //! KL_srp_vlan accepts the op

    // ---- KL_pp_timer_service faces (exact port match) ---------------------
    input  wire  [31:0]          now_ms_i,          //! absolute ms timebase (now_ms_o)
    output logic                 arm_valid_o,       //! arm/cancel strobe (service always accepts)
    output logic                 arm_cancel_o,      //! 1 = cancel the slot
    output logic [SLOT_AW_P-1:0] arm_slot_o,        //! SLOT_BASE_P + source
    output logic [7:0]           arm_owner_o,       //! OWNER_BASE_P + source
    output logic [31:0]          arm_deadline_ms_o, //! now + T-MRP-LEAVE (absolute)
    input  wire                  exp_valid_i,       //! timer-service expiry strobe
    input  wire  [SLOT_AW_P-1:0] exp_slot_i,        //! expired slot index

    // ---- class-C strobes + class-D levels (F02.10) ------------------------
    output logic [N_SOURCES_P-1:0]      lstn_reg_change_o, //! LISTENER_REG_CHANGE per source
    output logic [N_SOURCES_P-1:0][1:0] tk_decl_state_o,   //! 0 NONE / 1 ADVERTISE / 2 FAILED
    output logic [N_SOURCES_P-1:0][1:0] lstn_reg_state_o,  //! srp_decl_e code; 0 = NONE/Ignore
    output logic [N_SOURCES_P-1:0]      active_o,          //! ACTIVE(src) streaming level (Δ14 + admission)
    output logic [N_SOURCES_P-1:0][7:0] msrp_fail_code_o,  //! 1 while self-declared Failed, else 0
    output logic [N_SOURCES_P-1:0][63:0] msrp_fail_bridge_o, //! {16'd0, own MAC} while Failed, else 0

    // ---- observability (MTXW applicant/registrar walk) --------------------
    output logic [N_SOURCES_P-1:0][3:0] dbg_app_state_o, //! Table 10-3 applicant state per source
    output logic [N_SOURCES_P-1:0][1:0] dbg_reg_state_o  //! Table 10-4 registrar {0 MT, 1 IN, 2 LV}
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
  localparam logic [3:0] AE_NEW_C     = 4'd0;   // New!
  localparam logic [3:0] AE_JOIN_C    = 4'd1;   // Join!
  localparam logic [3:0] AE_LV_C      = 4'd2;   // Lv!
  localparam logic [3:0] AE_RNEW_C    = 4'd3;   // rNew!
  localparam logic [3:0] AE_RJOININ_C = 4'd4;   // rJoinIn!
  localparam logic [3:0] AE_RIN_C     = 4'd5;   // rIn!
  localparam logic [3:0] AE_RJOINMT_C = 4'd6;   // rJoinMt!
  localparam logic [3:0] AE_RMT_C     = 4'd7;   // rMt!
  localparam logic [3:0] AE_RLV_C     = 4'd8;   // rLv!
  localparam logic [3:0] AE_RLA_C     = 4'd9;   // rLA! (Re-declare! shares the row)
  localparam logic [3:0] AE_PER_C     = 4'd10;  // periodic!
  localparam logic [3:0] AE_TX_C      = 4'd11;  // tx!
  localparam logic [3:0] AE_TXLA_C    = 4'd12;  // txLA!

  // ---- Table 10-4 registrar states ---------------------------------------
  localparam logic [1:0] R_MT_C = 2'd0;
  localparam logic [1:0] R_IN_C = 2'd1;
  localparam logic [1:0] R_LV_C = 2'd2;

  // ---- timer-op pend codes ------------------------------------------------
  localparam logic [1:0] T_NOP_C    = 2'd0;
  localparam logic [1:0] T_ARM_C    = 2'd1;
  localparam logic [1:0] T_CANCEL_C = 2'd2;

  //! Table 10-3 next-state — transcribed row by row; a cell not named holds
  //! ("—"). reg_in_i feeds note 8 (tx! in AN: QA iff the same-attribute
  //! registrar is IN); p2p feeds notes 4/5 (rJoinIn ignored in VO/VP when
  //! point-to-point; rIn acts in AA only when point-to-point).
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
      AE_RNEW_C: nx = st;                    // rNew! row is all "—"
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
          default: nx = st;                            // VO, QA, AO, QO, QP
        endcase
      end
      AE_TXLA_C: begin
        case (st)
          A_VO_C, A_LA_C, A_AO_C, A_QO_C: nx = A_LO_C;
          A_VP_C:  nx = A_AA_C;
          A_VN_C:  nx = A_AN_C;
          A_AN_C, A_AA_C, A_AP_C, A_QP_C: nx = A_QA_C;
          default: nx = st;                            // QA, LO
        endcase
      end
      default: nx = st;
    endcase
    return nx;
  endfunction

  //! Table 10-3 message action on a transmit opportunity — [3] = send,
  //! [2:0] = attribute-event code. Optional [s]/[sJ]/[sL] encodings are
  //! never sent (banner); sJ/s encode against reg_in_i (10.7.6.3/.5).
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
    m    = {1'b0, 3'd0};
    if (!txla) begin
      case (st)
        A_VP_C, A_AA_C, A_AP_C: m = {1'b1, sj_w};
        A_VN_C, A_AN_C:         m = {1'b1, SRP_EV_NEW};
        A_LA_C:                 m = {1'b1, SRP_EV_LV};
        A_LO_C:                 m = {1'b1, s_w};
        default:                m = {1'b0, 3'd0};   // VO/QA/AO/QO/QP optional
      endcase
    end else begin
      case (st)
        A_VP_C:                 m = {1'b1, s_w};
        A_VN_C, A_AN_C:         m = {1'b1, SRP_EV_NEW};
        A_AA_C, A_QA_C, A_AP_C, A_QP_C: m = {1'b1, sj_w};
        default:                m = {1'b0, 3'd0};   // VO/LA/AO/QO/LO optional
      endcase
    end
    return m;
  endfunction

  //! declaring = applicant in a member state (F10.4 DECLARING/DECLARED)
  function automatic logic app_declaring_f(input logic [3:0] st);
    return st inside {A_VP_C, A_VN_C, A_AN_C, A_AA_C, A_QA_C, A_AP_C, A_QP_C};
  endfunction

  // ------------------------------------------------------------ registers
  // per-source declared record (frozen while declaring)
  logic [N_SOURCES_P-1:0]        rec_valid_r;
  logic [N_SOURCES_P-1:0][63:0]  sid_r;
  logic [N_SOURCES_P-1:0][47:0]  da_r;
  logic [N_SOURCES_P-1:0][11:0]  vid_r;
  logic [N_SOURCES_P-1:0][15:0]  mfs_r;
  logic [N_SOURCES_P-1:0][15:0]  mif_r;
  logic [N_SOURCES_P-1:0][2:0]   prio_r;
  logic [N_SOURCES_P-1:0]        rank_r;
  logic [N_SOURCES_P-1:0][31:0]  lat_r;

  // per-source applicant plane
  logic [N_SOURCES_P-1:0][3:0]   app_r;
  logic [N_SOURCES_P-1:0]        fail_r;      // declaring the Failed variant
  logic [N_SOURCES_P-1:0]        rla_pend_r;  // deferred rLA! (source busy)
  logic [N_SOURCES_P-1:0]        per_pend_r;  // deferred periodic!

  // tick walk
  typedef enum logic [1:0] {
    W_IDLE = 2'd0,   // wait for a join tick
    W_EVAL = 2'd1,   // apply tx!/txLA! to the current source
    W_PUSH = 2'd2,   // hold the message on the encoder intake
    W_DONE = 2'd3    // strobe txop_done_o
  } walk_e;
  walk_e               walk_r;
  logic [SRC_W_C-1:0]  wsrc_r;
  logic                wtxla_r;      // this walk uses the txLA! rows
  logic                tick_pend_r;  // tick landed mid-walk
  logic                laown_pend_r; // own LeaveAll: next walk is txLA!
  logic [2:0]          push_code_r;
  logic [7:0]          push_type_r;
  logic [271:0]        push_val_r;

  // per-source registrar plane (Listener tracker)
  logic [N_SOURCES_P-1:0][1:0]   reg_r;
  logic [N_SOURCES_P-1:0][1:0]   lstn_val_r;   // latched four-packed code
  logic [N_SOURCES_P-1:0][1:0]   lstn_prev_r;  // last published lstn_reg_state
  logic [N_SOURCES_P-1:0][1:0]   tpend_r;      // leave-timer op pend

  // VLAN membership op pends (join at open, leave at close; leave first)
  logic [N_SOURCES_P-1:0]        vj_pend_r;
  logic [N_SOURCES_P-1:0]        vl_pend_r;
  logic [N_SOURCES_P-1:0][11:0]  vj_vid_r;
  logic [N_SOURCES_P-1:0][11:0]  vl_vid_r;

  // -------------------------------------------------------- event matching
  logic [N_SOURCES_P-1:0] app_rx_hit_w;   // Talker Adv/Failed on own stream
  logic [N_SOURCES_P-1:0] reg_rx_hit_w;   // Listener on own stream_id
  logic [3:0]             rx_app_ev_w;

  always_comb begin : hit_map
    rx_app_ev_w = {1'b0, evt_mrp_event_i} + AE_RNEW_C;   // 0..5 -> rNew..rLv
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      app_rx_hit_w[s] = evt_valid_i && evt_msrp_i && rec_valid_r[s]
                     && ((evt_attr_type_i == SRP_MSRP_ATTR_TALKER_ADV_C)
                         || (evt_attr_type_i == SRP_MSRP_ATTR_TALKER_FAILED_C))
                     && (evt_mrp_event_i <= 3'(SRP_EV_LV))
                     && (evt_stream_id_i == sid_r[s])
                     && (evt_da_i == da_r[s])
                     && (evt_vid_i == {4'd0, vid_r[s]});
      reg_rx_hit_w[s] = evt_valid_i && evt_msrp_i && rec_valid_r[s]
                     && (evt_attr_type_i == SRP_MSRP_ATTR_LISTENER_C)
                     && (evt_stream_id_i == sid_r[s]);
    end
  end

  // ------------------------------------------------- applicant arbitration
  // one applicant event per source per cycle; decoder events outrank the
  // gate (gate_ready_o holds the host off on event cycles), then deferred
  // rLA!, the admission fixer, deferred periodic!, and last the tick walk
  logic                   gate_acc_w;
  logic [N_SOURCES_P-1:0] app_ev_v_w;
  logic [N_SOURCES_P-1:0][3:0] app_ev_w;
  logic [N_SOURCES_P-1:0] adm_grant_w;
  logic [N_SOURCES_P-1:0] rla_grant_w;
  logic [N_SOURCES_P-1:0] per_grant_w;
  logic                   walk_grant_w;
  logic [N_SOURCES_P-1:0] adm_fix_w;

  assign gate_ready_o = !evt_valid_i;
  assign gate_acc_w   = gate_valid_i && gate_ready_o;

  always_comb begin : app_arb
    walk_grant_w = 1'b0;
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      // the Failed swap re-declares whenever the published mode disagrees
      // with the admission level while declaring (10 §6.3)
      adm_fix_w[s] = rec_valid_r[s] && app_declaring_f(app_r[s])
                  && (fail_r[s] != !sr_admitted_i[s]);
      app_ev_v_w[s]  = 1'b0;
      app_ev_w[s]    = AE_RNEW_C;
      adm_grant_w[s] = 1'b0;
      rla_grant_w[s] = 1'b0;
      per_grant_w[s] = 1'b0;
      if (app_rx_hit_w[s]) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = rx_app_ev_w;
      end else if (gate_acc_w && (gate_src_i == SRC_W_C'(s))) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = gate_open_i ? (rec_valid_r[s] ? AE_JOIN_C : AE_NEW_C)
                                    : AE_LV_C;
      end else if (rla_pend_r[s] || leaveall_rx_i) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = AE_RLA_C;
        rla_grant_w[s] = 1'b1;
      end else if (adm_fix_w[s]) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = AE_NEW_C;
        adm_grant_w[s] = 1'b1;
      end else if (per_pend_r[s] || periodic_tick_i) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = AE_PER_C;
        per_grant_w[s] = 1'b1;
      end else if ((walk_r == W_EVAL) && (wsrc_r == SRC_W_C'(s))) begin
        app_ev_v_w[s] = 1'b1;
        app_ev_w[s]   = wtxla_r ? AE_TXLA_C : AE_TX_C;
        walk_grant_w  = 1'b1;
      end
    end
  end

  // FirstValue of the walk source (F10.7 layout; byte 0 at [271:264])
  logic [271:0] wval_w;
  logic [3:0]   wmsg_w;
  always_comb begin : walk_msg
    wval_w = 272'd0;
    wval_w[271:208] = sid_r[wsrc_r];
    wval_w[207:160] = da_r[wsrc_r];
    wval_w[159:144] = {4'd0, vid_r[wsrc_r]};
    wval_w[143:128] = mfs_r[wsrc_r];
    wval_w[127:112] = mif_r[wsrc_r];
    wval_w[111:104] = {prio_r[wsrc_r], rank_r[wsrc_r], 4'd0};
    wval_w[103:72]  = lat_r[wsrc_r];
    if (fail_r[wsrc_r]) begin
      wval_w[71:8] = {16'd0, own_mac_i};   // §35.2.2.8.7 end-station MAC
      wval_w[7:0]  = 8'd1;                 // insufficient bandwidth
    end
    wmsg_w = app_msg_f(app_r[wsrc_r], wtxla_r, 1'b0);
  end

  // ------------------------------------------------------- applicant plane
  always_ff @(posedge clk_i) begin : app_plane
    if (!rst_n) begin
      rec_valid_r <= '0;
      sid_r       <= '0;
      da_r        <= '0;
      vid_r       <= '0;
      mfs_r       <= '0;
      mif_r       <= '0;
      prio_r      <= '0;
      rank_r      <= '0;
      lat_r       <= '0;
      app_r       <= '0;      // Begin! = VO everywhere
      fail_r      <= '0;
      rla_pend_r  <= '0;
      per_pend_r  <= '0;
      walk_r      <= W_IDLE;
      wsrc_r      <= '0;
      wtxla_r     <= 1'b0;
      tick_pend_r <= 1'b0;
      laown_pend_r <= 1'b0;
      push_code_r <= 3'd0;
      push_type_r <= 8'd0;
      push_val_r  <= '0;
      txop_done_o <= 1'b0;
    end else begin
      txop_done_o <= 1'b0;

      // ---- per-source applicant transitions -----------------------------
      for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
        if (app_ev_v_w[s]) begin
          app_r[s] <= app_next_f(app_r[s], app_ev_w[s], 1'b0, p2p_i);
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
        // admission swap flips the declared variant with its New!
        if (adm_grant_w[s]) begin
          fail_r[s] <= !sr_admitted_i[s];
        end
      end

      // ---- DA-gate record capture ---------------------------------------
      if (gate_acc_w) begin
        if (gate_open_i) begin
          rec_valid_r[gate_src_i] <= 1'b1;
          sid_r[gate_src_i]  <= gate_stream_id_i;
          da_r[gate_src_i]   <= gate_da_i;
          vid_r[gate_src_i]  <= gate_vid_i;
          mfs_r[gate_src_i]  <= gate_max_frame_i;
          mif_r[gate_src_i]  <= gate_max_interval_i;
          prio_r[gate_src_i] <= gate_prio_i;
          rank_r[gate_src_i] <= gate_rank_i;
          lat_r[gate_src_i]  <= gate_acc_lat_i;
        end else begin
          fail_r[gate_src_i] <= 1'b0;   // FAILED is published only declared
        end
      end

      // ---- own LeaveAll marks the next walk txLA! -----------------------
      if (leaveall_own_i) laown_pend_r <= 1'b1;

      // ---- tick walk ----------------------------------------------------
      case (walk_r)
        W_IDLE: begin
          if (join_tick_i || tick_pend_r) begin
            tick_pend_r <= 1'b0;
            wtxla_r     <= laown_pend_r;
            laown_pend_r <= 1'b0;
            wsrc_r      <= '0;
            walk_r      <= W_EVAL;
          end
        end
        W_EVAL: begin
          if (join_tick_i) tick_pend_r <= 1'b1;
          if (walk_grant_w) begin
            if (wmsg_w[3] && rec_valid_r[wsrc_r]) begin
              push_code_r <= wmsg_w[2:0];
              push_type_r <= fail_r[wsrc_r] ? SRP_MSRP_ATTR_TALKER_FAILED_C
                                            : SRP_MSRP_ATTR_TALKER_ADV_C;
              push_val_r  <= wval_w;
              walk_r      <= W_PUSH;
            end else if (wsrc_r == SRC_W_C'(N_SOURCES_P - 1)) begin
              walk_r <= W_DONE;
            end else begin
              wsrc_r <= wsrc_r + SRC_W_C'(1);
            end
          end
        end
        W_PUSH: begin
          if (join_tick_i) tick_pend_r <= 1'b1;
          if (ev_ready_i) begin
            if (wsrc_r == SRC_W_C'(N_SOURCES_P - 1)) begin
              walk_r <= W_DONE;
            end else begin
              wsrc_r <= wsrc_r + SRC_W_C'(1);
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
  assign ev_app_o       = 1'b0;               // MSRP participant
  assign ev_attr_type_o = push_type_r;
  assign ev_event_o     = push_code_r;
  assign ev_fourpack_o  = 2'd0;
  assign ev_value_o     = push_val_r;

  // ------------------------------------------------------- registrar plane
  // Table 10-4 with Δ13: rLv on IN drops to MT on the frame (no
  // leavetimer); rLA/own-LeaveAll is the only path into LV, aged by the
  // per-source T-MRP-LEAVE slot; a registering event stops the aging.
  logic        leaveall_any_w;
  logic        exp_hit_w;
  logic [31:0] exp_idx_w;

  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;
  // unsigned wrap maps below-base slots to huge indices — one bound check
  assign exp_idx_w = 32'(exp_slot_i) - SLOT_BASE_P;
  assign exp_hit_w = exp_valid_i && (exp_idx_w < N_SOURCES_P);

  logic [N_SOURCES_P-1:0][1:0] lstn_out_w;
  always_comb begin : lstn_out_map
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      lstn_out_w[s] = (reg_r[s] != R_MT_C) ? lstn_val_r[s] : 2'd0;
    end
  end

  // lowest-index pending leave-timer op (one issue per cycle)
  logic               tsel_v_w;
  logic [SRC_W_C-1:0] tsel_ix_w;
  always_comb begin : tissue_sel
    tsel_v_w  = 1'b0;
    tsel_ix_w = '0;
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      if (!tsel_v_w && (tpend_r[s] != T_NOP_C)) begin
        tsel_v_w  = 1'b1;
        tsel_ix_w = SRC_W_C'(s);
      end
    end
  end

  always_ff @(posedge clk_i) begin : reg_plane
    if (!rst_n) begin
      reg_r             <= '0;
      lstn_val_r        <= '0;
      lstn_prev_r       <= '0;
      tpend_r           <= '0;
      lstn_reg_change_o <= '0;
      arm_valid_o       <= 1'b0;
      arm_cancel_o      <= 1'b0;
      arm_slot_o        <= '0;
      arm_owner_o       <= 8'd0;
      arm_deadline_ms_o <= 32'd0;
    end else begin
      lstn_reg_change_o <= '0;
      arm_valid_o       <= 1'b0;

      // ---- one leave-timer op per cycle (service accepts O(1)); a
      // same-cycle set to the issued source lands AFTER this clear in the
      // block, so the newer op survives in the pend and issues next -------
      if (tsel_v_w) begin
        arm_valid_o       <= 1'b1;
        arm_cancel_o      <= (tpend_r[tsel_ix_w] == T_CANCEL_C);
        arm_slot_o        <= SLOT_AW_P'(SLOT_BASE_P + 32'(tsel_ix_w));
        arm_owner_o       <= OWNER_BASE_P + {{(8-SRC_W_C){1'b0}}, tsel_ix_w};
        arm_deadline_ms_o <= now_ms_i + LEAVE_MS_P;
        tpend_r[tsel_ix_w] <= T_NOP_C;
      end

      // ---- per-source registrar events ----------------------------------
      for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
        if (reg_rx_hit_w[s] && ((evt_mrp_event_i == 3'(SRP_EV_NEW))
                                || (evt_mrp_event_i == 3'(SRP_EV_JOININ))
                                || (evt_mrp_event_i == 3'(SRP_EV_JOINMT)))) begin
          // registering event: -> IN, latch the declaration parameter
          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_CANCEL_C;
          reg_r[s]      <= R_IN_C;
          lstn_val_r[s] <= evt_fourpacked_i;
        end else if (reg_rx_hit_w[s] && (evt_mrp_event_i == 3'(SRP_EV_LV))) begin
          if (reg_r[s] == R_IN_C) begin
            reg_r[s] <= R_MT_C;              // Δ13: no leavetimer on rLv
          end
          // LV: table 10-4 rLv on LV is -x- (the LeaveAll aging continues)
        end else if (leaveall_any_w && (reg_r[s] == R_IN_C)) begin
          reg_r[s]   <= R_LV_C;
          tpend_r[s] <= T_ARM_C;
        end else if (exp_hit_w && (exp_idx_w == s)
                     && (reg_r[s] == R_LV_C) && (tpend_r[s] != T_ARM_C)) begin
          reg_r[s] <= R_MT_C;                // leavetimer! -> MT + Lv
        end
        // gate re-open arms a fresh tracker for the (possibly new) stream
        if (gate_acc_w && gate_open_i && (gate_src_i == SRC_W_C'(s))) begin
          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_CANCEL_C;
          reg_r[s]      <= R_MT_C;
          lstn_val_r[s] <= 2'd0;
        end
      end

      // ---- LISTENER_REG_CHANGE on any published change ------------------
      for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
        if (lstn_out_w[s] != lstn_prev_r[s]) begin
          lstn_prev_r[s]       <= lstn_out_w[s];
          lstn_reg_change_o[s] <= 1'b1;
        end
      end
    end
  end

  // --------------------------------------------------------- VLAN op plane
  // lowest-index pending op drives the user face; leave before join per
  // source (a close-then-reopen on a new VID must free the old refcount
  // first, F10.3)
  logic               vsel_v_w;
  logic               vsel_join_w;
  logic [SRC_W_C-1:0] vsel_ix_w;
  always_comb begin : vlan_sel
    vsel_v_w    = 1'b0;
    vsel_join_w = 1'b0;
    vsel_ix_w   = '0;
    user_vid_o  = 12'd0;
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      if (!vsel_v_w) begin
        if (vl_pend_r[s]) begin
          vsel_v_w    = 1'b1;
          vsel_join_w = 1'b0;
          vsel_ix_w   = SRC_W_C'(s);
          user_vid_o  = vl_vid_r[s];
        end else if (vj_pend_r[s]) begin
          vsel_v_w    = 1'b1;
          vsel_join_w = 1'b1;
          vsel_ix_w   = SRC_W_C'(s);
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
      // gate edges enqueue membership ops (join at open, leave at close);
      // an unissued opposite op on the same VID collapses to nothing
      if (gate_acc_w) begin
        if (gate_open_i) begin
          if (vl_pend_r[gate_src_i] && (vl_vid_r[gate_src_i] == gate_vid_i)
              && !(vsel_v_w && user_ready_i && !vsel_join_w
                   && (vsel_ix_w == gate_src_i))) begin
            vl_pend_r[gate_src_i] <= 1'b0;   // never left: net zero
          end else begin
            vj_pend_r[gate_src_i] <= 1'b1;
            vj_vid_r[gate_src_i]  <= gate_vid_i;
          end
        end else begin
          if (vj_pend_r[gate_src_i]
              && !(vsel_v_w && user_ready_i && vsel_join_w
                   && (vsel_ix_w == gate_src_i))) begin
            vj_pend_r[gate_src_i] <= 1'b0;   // never joined: net zero
          end else begin
            vl_pend_r[gate_src_i] <= 1'b1;
            vl_vid_r[gate_src_i]  <= vid_r[gate_src_i];
          end
        end
      end
    end
  end

  // ---------------------------------------------------- class-C/D outputs
  always_comb begin : status_map
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      tk_decl_state_o[s] = (rec_valid_r[s] && app_declaring_f(app_r[s]))
                         ? (fail_r[s] ? 2'd2 : 2'd1)
                         : 2'd0;
      lstn_reg_state_o[s] = lstn_out_w[s];
      active_o[s] = rec_valid_r[s] && app_declaring_f(app_r[s]) && !fail_r[s]
                 && ((lstn_out_w[s] == 2'(SRP_DECL_READY))
                     || (lstn_out_w[s] == 2'(SRP_DECL_READY_FAILED)))
                 && sr_admitted_i[s];
      msrp_fail_code_o[s]   = (tk_decl_state_o[s] == 2'd2) ? 8'd1 : 8'd0;
      msrp_fail_bridge_o[s] = (tk_decl_state_o[s] == 2'd2)
                            ? {16'd0, own_mac_i} : 64'd0;
      dbg_app_state_o[s] = app_r[s];
      dbg_reg_state_o[s] = reg_r[s];
    end
  end

endmodule : KL_srp_talker_fsm
`default_nettype wire

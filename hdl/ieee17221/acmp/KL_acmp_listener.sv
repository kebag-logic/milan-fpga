/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_listener.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : Compatibility wrapper — the Milan v1.2 LISTENER-side ACMP
//                engine now lives in KL_acmp_lstn_ctx (N bind contexts in a
//                shared SM + context RAM). This wrapper keeps today's proven
//                port surface and pins the per-context POLICY map; at the
//                default N_SINKS_P=2 it is byte/bit-identical to the
//                original single-sink module (the no-regression axiom;
//                pinned by tb/verilator/acmp_lstn):
//
//                  EVERY context runs the full Milan 5.5.3 binding SM
//                    (probe ladder, ADP talker watch, SRP coupling). Milan
//                    v1.2 5.5.3.2 defines the state table per SINK and
//                    5.5.3.5.3 step 5 requires a PROBE_TX_COMMAND on
//                    RCV_BIND_RX_CMD for the sink named by
//                    listener_unique_id, whichever sink that is.
//                  The only per-context policy left is the PROVISIONAL
//                    stream_id a bind records before the probe answers:
//                    context 0 always derives it from {talker EID, tuid}
//                    (sid_from_eid — the documented sink-0 policy);
//                    contexts 1..N-1 honour a nonzero fast-connect
//                    stream_id in the BIND_RX_COMMAND (Milan 5.5.1.2) and
//                    fall back to the derivation when it is zero. Either
//                    way it is only provisional: 5.5.3.5.18 step 4 makes
//                    the PROBE_TX_RESPONSE the authority, and the record
//                    is overwritten from it (sid + dmac + vlan) before any
//                    SRP reservation is initiated.
//                  Contexts are addressed by listener_unique_id = context
//                    index: 0 = STREAM_INPUT[0], 1..N-2 = the further AAF
//                    sinks, last = the CRF Media Clock Input sink.
//
//                P12 (NxN integration): the context-table request/grant
//                port passes through this wrapper (tbl_*) so the 0x800
//                CSR window's ACMP master reads live bind records for
//                EVERY context index < N_SINKS_P.
//
//                Behavioural contract, SM states, timers, REF-BUG fixes,
//                silicon lessons (always-armed capture, TX-grant watchdog,
//                walker forensics): see KL_acmp_lstn_ctx.sv.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_listener #(
    parameter int unsigned CLK_FREQ_HZ_P = 100_000_000,
    //! bind contexts (>= 2: ctx0 media + ctx1 CRF are always present);
    //! the datapath feeds max(2, N_STREAMS)
    parameter int unsigned N_SINKS_P     = 2
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity ------------------------------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- AECP lock view (Milan 5.5.3.5 bound-state step 1) --------------
    //! pass-through to KL_acmp_lstn_ctx: while locked_i, BIND_RX/UNBIND_RX
    //! from any controller but lock_ctlr_i answers CONTROLLER_NOT_
    //! AUTHORIZED with a full command echo; GET_RX_STATE is exempt.
    input  wire         locked_i,
    input  wire [63:0]  lock_ctlr_i,

    // ---- ADP age tick ----------------------------------------------------
    input  wire         tick_1s_i,

    // ---- gPTP view (Milan 5.6.4.5.1 step 1) ------------------------------
    //! pass-through to KL_acmp_lstn_ctx: committed grandmaster pair +
    //! domain number gate the ENTITY_AVAILABLE availability latch; an
    //! all-zero pair stands the check down (see the core's port banner)
    input  wire [63:0]  gm_id_i,
    input  wire [7:0]   gm_domain_i,

    // ---- lwSRP listener-side hooks (PER SINK) ---------------------------
    //! bit c = the lwSRP registrar state of context c's OWN attribute row.
    //! Every context runs the probe SM, so every context needs its own
    //! TalkerAdvertise / TalkerFailed level: 5.5.3.5.42/5.5.3.5.48 turn
    //! SETTLED_NO_RSV into SETTLED_RSV_OK on the registration and back out
    //! on its loss. Bit 0 is the legacy row-0 registrar; a context whose
    //! row does not exist in this shape ties its bit low and simply never
    //! leaves SETTLED_NO_RSV (its TMR_NO_TK re-probe ladder is 5.5.3.5.36).
    input  wire [N_SINKS_P-1:0] ta_registered_i, //! TalkerAdvertise registered
    input  wire [N_SINKS_P-1:0] ta_failed_i,     //! TalkerFailed registered
    output wire         lstn_declare_o,    //! declare the MSRP Listener attribute
    output wire [63:0]  bound_sid_o,       //! bound stream_id (walker compare)
    output wire [11:0]  stream_vlan_o,     //! from the talker's probe response
    output wire [47:0]  stream_dmac_o,
    output wire         stream_active_o,   //! sink open (SETTLED_*)

    // ---- per-sink bind view (ALL contexts; lwSRP listener-row fabric) ---
    //! bound level + bound stream_id per context, and a 1-cycle pulse per
    //! record write — the datapath's lwSRP listener-row provisioner derives
    //! ctx rows 1..N-1 from these (sink 0 keeps the legacy row-0 path)
    output wire [N_SINKS_P-1:0]    lstn_bound_v_o,
    output wire [N_SINKS_P*64-1:0] lstn_sid_v_o,
    //! per-sink probed SRP {dmac, vlan} (Table 5.29 expected pair for the
    //! lwSRP walker; zero until the probe response learns them)
    output wire [N_SINKS_P*48-1:0] lstn_dmac_v_o,
    output wire [N_SINKS_P*12-1:0] lstn_vlan_v_o,
    output wire [N_SINKS_P-1:0]    bind_upd_p_o,

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) -------
    input  wire         rx_tvalid_i,
    input  wire         rx_tready_i,    //! tapped lane's ready (read, never driven)
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- TX AXIS master (little lane; -> TX arbiter) -------------------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status (CSR RO) — the context-0 compatibility view -------------
    output acmp_lsm_t   state_o,
    output wire [63:0]  bound_talker_o,
    output wire [15:0]  bound_tuid_o,
    output wire [4:0]   acmp_status_o,     //! last probe status / timeout
    output wire [1:0]   probing_o,         //! 0 dis / 1 passive / 2 active / 3 done
    output wire         tk_avail_o,        //! bound talker ADP-visible
    output wire [15:0]  cmd_count_o,       //! listener commands accepted
    output wire [31:0]  dbg_o,             //! walker forensics (07-18)
    output wire [7:0]   tx_wedge_cnt_o,    //! responses abandoned (watchdog)
    output wire [15:0]  probe_count_o,     //! PROBE_TX commands sent

    // ---- sink 1 (CRF Media Clock Input) — the context-1 view -----------
    output wire         s1_bound_o,
    output wire [63:0]  s1_sid_o,
    output wire [47:0]  s1_dmac_o,

    // ---- context-table access (P12: the 0x800 CSR window's ACMP master) --
    //! pass-through of KL_acmp_lstn_ctx's tbl_* port: req held until the
    //! 1-cycle gnt; ctx (acmp_lstn_ctx_t, 370 b) valid WITH gnt. Index is
    //! the wrapper's context index (0 = STREAM_INPUT[0], 1 = CRF sink,
    //! 2..N-1 = window streams).
    input  wire         tbl_req_i,
    input  wire [((N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1)-1:0] tbl_idx_i,
    output wire         tbl_gnt_o,
    output acmp_lstn_ctx_t tbl_ctx_o,

    // ---- bind-restore injection (E1, Milan 5.5.3.5.2) pass-through ------
    //! see KL_acmp_lstn_ctx: req held until the 1-cycle ack; status with
    //! ack (0 injected, 1 occupied, 2 bad index / record-only context)
    input  wire         rest_req_i,
    input  wire [3:0]   rest_idx_i,
    input  wire [63:0]  rest_talker_i,
    input  wire [15:0]  rest_tuid_i,
    input  wire [63:0]  rest_ctlr_i,
    input  wire [15:0]  rest_flags_i,
    output wire         rest_ack_o,
    output wire [1:0]   rest_status_o
);

  //! per-context policy map. The probe SM is ON EVERYWHERE (Milan 5.5.3.2 /
  //! 5.5.3.5.3 step 5 — task #64): the record-only branch parked every sink
  //! but 0 in SETTLED_NO_RSV, so seven AAF sinks plus CRF on the shipping
  //! 8x8 shape never sent a PROBE_TX_COMMAND and their lwSRP listener rows
  //! were registered against a stream_id DERIVED from {talker EID, tuid} —
  //! a guess that is only right when the talker happens to derive the same
  //! way. The two maps are now INDEPENDENT (SID_EX is no longer ~SM_EN):
  //! the sid policy below is unchanged from the pinned N=2 pair, it just no
  //! longer doubles as the SM switch.
  localparam logic [N_SINKS_P-1:0] SM_EN_MAP_C  = {N_SINKS_P{1'b1}};
  //! provisional-sid policy: ctx0 derives, every other ctx honours a
  //! nonzero fast-connect stream_id (Milan 5.5.1.2). The probe response
  //! overrides both (5.5.3.5.18 step 4).
  localparam logic [N_SINKS_P-1:0] SID_EX_MAP_C = ~(N_SINKS_P'(1));

  wire [N_SINKS_P-1:0] w_declare, w_active;

  KL_acmp_lstn_ctx #(
    .CLK_FREQ_HZ_P  (CLK_FREQ_HZ_P),
    .N_SINKS_P      (N_SINKS_P),
    .PROBE_SM_EN_P  (SM_EN_MAP_C),
    .SID_EXPLICIT_P (SID_EX_MAP_C)
  ) u_ctx (
    .clk_i           (clk_i),
    .rst_n           (rst_n),
    .enable_i        (enable_i),
    .station_mac_i   (station_mac_i),
    .entity_id_i     (entity_id_i),
    .locked_i        (locked_i),     //! AECP entity lock -> ACMP step 1
    .lock_ctlr_i     (lock_ctlr_i),
    .tick_1s_i       (tick_1s_i),
    .gm_id_i         (gm_id_i),     //! 5.6.4.5.1 step 1 gm/domain gate
    .gm_domain_i     (gm_domain_i),
    //! lwSRP REGISTRAR coupling, one bit per context: bit 0 is the row-0
    //! registrar, bits 1..N-1 are the per-row registrars inside KL_lwsrp_ctx
    //! for the rows the lstn_bound_v/lstn_sid_v bind view provisions. Zero-
    //! extending here (the pre-task-#64 shape) left every sink but 0 unable
    //! to reach SETTLED_RSV_OK, so they re-ran the probe ladder every
    //! TMR_NO_TK forever once the SM was enabled for them.
    .ta_registered_i (ta_registered_i),
    .ta_failed_i     (ta_failed_i),
    .lstn_declare_o  (w_declare),
    .stream_active_o (w_active),
    .lstn_bound_o    (lstn_bound_v_o),
    .lstn_sid_o      (lstn_sid_v_o),
    .lstn_dmac_o     (lstn_dmac_v_o),
    .lstn_vlan_o     (lstn_vlan_v_o),
    .bind_upd_p_o    (bind_upd_p_o),
    .rx_tvalid_i     (rx_tvalid_i),
    .rx_tready_i     (rx_tready_i),
    .rx_tdata_i      (rx_tdata_i),
    .rx_tkeep_i      (rx_tkeep_i),
    .rx_tlast_i      (rx_tlast_i),
    .m_axis_tdata    (m_axis_tdata),
    .m_axis_tkeep    (m_axis_tkeep),
    .m_axis_tvalid   (m_axis_tvalid),
    .m_axis_tlast    (m_axis_tlast),
    .m_axis_tready   (m_axis_tready),
    .view0_state_o   (state_o),
    .view0_talker_o  (bound_talker_o),
    .view0_tuid_o    (bound_tuid_o),
    .view0_sid_o     (bound_sid_o),
    .view0_vlan_o    (stream_vlan_o),
    .view0_dmac_o    (stream_dmac_o),
    .view0_status_o  (acmp_status_o),
    .view0_probing_o (probing_o),
    .view0_tk_avail_o(tk_avail_o),
    .view1_bound_o   (s1_bound_o),
    .view1_sid_o     (s1_sid_o),
    .view1_dmac_o    (s1_dmac_o),
    .cmd_count_o     (cmd_count_o),
    .probe_count_o   (probe_count_o),
    .tx_wedge_cnt_o  (tx_wedge_cnt_o),
    .dbg_o           (dbg_o),
    .tbl_req_i       (tbl_req_i),  //! P12: the CSR window's ACMP tbl master
    .tbl_idx_i       (tbl_idx_i),
    .tbl_gnt_o       (tbl_gnt_o),
    .tbl_ctx_o       (tbl_ctx_o),
    .rest_req_i      (rest_req_i), //! E1: the 0x7A0 bind-restore master
    .rest_idx_i      (rest_idx_i),
    .rest_talker_i   (rest_talker_i),
    .rest_tuid_i     (rest_tuid_i),
    .rest_ctlr_i     (rest_ctlr_i),
    .rest_flags_i    (rest_flags_i),
    .rest_ack_o      (rest_ack_o),
    .rest_status_o   (rest_status_o)
  );

  assign lstn_declare_o  = w_declare[0];
  assign stream_active_o = w_active[0];

endmodule

`default_nettype wire

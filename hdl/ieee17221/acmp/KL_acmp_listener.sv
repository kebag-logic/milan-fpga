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
//                  context 0 = STREAM_INPUT[0] media sink: full Milan 5.5.3
//                    binding SM (probe ladder, ADP talker watch, lwSRP
//                    coupling), sid ALWAYS derived from {talker EID, tuid}
//                    (sid_from_eid — the documented sink-0 policy).
//                  context 1 = CRF Media Clock Input sink: pure bind
//                    record (no probe SM, no MSRP attach, no ADP watch),
//                    explicit fast-connect stream_id honoured (nonzero
//                    command sid wins, zero falls back to the derivation).
//                  contexts 2..N-1 (N-sink round, N_SINKS_P from the
//                    datapath's N_STREAMS): window-provisioned listener
//                    binds for the extra 0x800-window streams — same
//                    record-only + explicit-sid policy as the CRF sink
//                    (the Lane-C/§3.1 per-context config the ctx core
//                    already implements). They bind via CONNECT_RX with
//                    listener_unique_id = context index.
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

    // ---- ADP age tick ----------------------------------------------------
    input  wire         tick_1s_i,

    // ---- lwSRP listener-side hooks (sink 0) -----------------------------
    input  wire         ta_registered_i,   //! TalkerAdvertise registered (bound sid)
    input  wire         ta_failed_i,       //! TalkerFailed registered (bound sid)
    output wire         lstn_declare_o,    //! declare the MSRP Listener attribute
    output wire [63:0]  bound_sid_o,       //! bound stream_id (walker compare)
    output wire [11:0]  stream_vlan_o,     //! from the talker's probe response
    output wire [47:0]  stream_dmac_o,
    output wire         stream_active_o,   //! sink open (SETTLED_*)

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) -------
    input  wire         rx_tvalid_i,
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
    //! 1-cycle gnt; ctx (acmp_lstn_ctx_t, 317 b) valid WITH gnt. Index is
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

  //! per-context policy map (the N-sink round): bit 0 = the full media
  //! binding SM + derived sid; every other context = record-only bind with
  //! the explicit fast-connect sid honoured (ctx1 CRF + window contexts).
  //! N=2 reproduces the original pinned pair {2'b01, 2'b10} exactly.
  localparam logic [N_SINKS_P-1:0] SM_EN_MAP_C  = N_SINKS_P'(1);
  localparam logic [N_SINKS_P-1:0] SID_EX_MAP_C = ~SM_EN_MAP_C;

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
    .tick_1s_i       (tick_1s_i),
    //! lwSRP coupling stays sink-0 only (record-only contexts never attach)
    .ta_registered_i ({{(N_SINKS_P-1){1'b0}}, ta_registered_i}),
    .ta_failed_i     ({{(N_SINKS_P-1){1'b0}}, ta_failed_i}),
    .lstn_declare_o  (w_declare),
    .stream_active_o (w_active),
    .rx_tvalid_i     (rx_tvalid_i),
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

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_responder.sv
//  Project     : Milan ACMP  (IEEE 1722.1-2021 Clause 8, AVnu Milan v1.2 §5.5)
//
//  Description : Compatibility wrapper — the Milan v1.2 talker-side ACMP
//                (PROBE_TX activation SM, docs/design/MILAN_TALKER_SM.md)
//                now lives in KL_acmp_tlkr_ctx (N source contexts sharing
//                one SM + one 1 s window sweep). This wrapper pins today's
//                proven single-source configuration (talker_unique_id 0,
//                stream params from the CSR AAF group), byte/bit-identical
//                to the original module (pinned by tb/verilator/acmp).
//
//                The NxN integration lane consumes KL_acmp_tlkr_ctx
//                directly (per-source dmac/vid config slices + vector
//                activation outputs); this wrapper keeps milan_datapath
//                and the CSR map untouched until then.
//
//                Response tables, Milan §5.5.4 semantics, the area-70
//                frame-RAM recipe and the always-armed capture: see
//                KL_acmp_tlkr_ctx.sv.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module KL_acmp_responder (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! gate (CSR ADP enable)

    // ---- identity (CSR 0x600 group) -----------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [63:0]  entity_id_i,

    // ---- live stream parameters (CSR AAF group — the framer's source) --
    input  wire [47:0]  aaf_dmac_i,        //! stream dest MAC ([47:40] first)
    input  wire [11:0]  aaf_vid_i,         //! stream VLAN id

    // ---- activation state machine --------------------------------------
    input  wire         tick_1s_i,         //! 1 s strobe (shared adp tick)
    input  wire         listener_observed_i, //! lwSRP Listener registrar hook
    output wire         talker_active_o,   //! armed | listener_observed (AAF gate)
    output wire         probe_armed_o,     //! probe seen within the 15 s window

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) -------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- response AXIS master (little lane; -> TX arbiter) ------------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status --------------------------------------------------------
    output wire [15:0]  cmd_count_o,       //! ACMP commands accepted
    output wire [15:0]  resp_count_o       //! responses sent
);

  wire [0:0] w_active, w_armed;

  KL_acmp_tlkr_ctx #(
    .N_SRC_P (1)
  ) u_ctx (
    .clk_i               (clk_i),
    .rst_n               (rst_n),
    .enable_i            (enable_i),
    .station_mac_i       (station_mac_i),
    .entity_id_i         (entity_id_i),
    .src_dmac_i          (aaf_dmac_i),
    .src_vid_i           (aaf_vid_i),
    .tick_1s_i           (tick_1s_i),
    .listener_observed_i (listener_observed_i),
    .talker_active_o     (w_active),
    .probe_armed_o       (w_armed),
    .rx_tvalid_i         (rx_tvalid_i),
    .rx_tdata_i          (rx_tdata_i),
    .rx_tkeep_i          (rx_tkeep_i),
    .rx_tlast_i          (rx_tlast_i),
    .m_axis_tdata        (m_axis_tdata),
    .m_axis_tkeep        (m_axis_tkeep),
    .m_axis_tvalid       (m_axis_tvalid),
    .m_axis_tlast        (m_axis_tlast),
    .m_axis_tready       (m_axis_tready),
    .cmd_count_o         (cmd_count_o),
    .resp_count_o        (resp_count_o)
  );

  assign talker_active_o = w_active[0];
  assign probe_armed_o   = w_armed[0];

endmodule

`default_nettype wire

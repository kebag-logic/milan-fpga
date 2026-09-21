/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_desc_mem_guard.proto.sv   (PROTOTYPE, design evidence)
//  Project     : milan-fpga #500, saved-state scope D3, seam S2
//                (docs/design/SAVED_STATE_MATERIALIZATION.md section 5.1)
//
//  Description : RESPONSE ISOLATION on the descriptor store's memory face.
//                KL_aecp_desc_store keeps ONE burst outstanding and sinks a
//                beat only while it awaits none; its own 4,096-cycle watchdog
//                ABANDONS a burst, and its reset forgets one. A memory path
//                that accepts the next request while an abandoned burst still
//                owes beats (the parent's asynchronous request FIFO in front
//                of pp_desc_bridge does) then hands those late beats to the
//                next burst: a descriptor fetch, or the header, index or name
//                table of a re-walk, filled with another burst's bytes. Only
//                the 32-byte header is checksummed.
//
//                The guard sits between the store and the memory and holds
//                ONE fact the store drops: an accepted burst still owes its
//                terminal beat (last or err). While it does, the store's next
//                request is held (req ready low, and never presented to the
//                memory), and every beat passes through to a store that sinks
//                it. The fact is reset by the HARD reset only, never by the
//                D3 roll-back strobe, so a roll-back cannot forget it; debt_o
//                publishes it, and the D3 writer holds the restorable owners
//                in reset until it clears. A memory that never ends the burst
//                keeps the store's requests held for ever: the store's own
//                watchdog still answers every locate in bounded time, with an
//                error, and the D3 writer's deadline turns the roll-back into
//                its CLOSED terminal.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_desc_mem_guard (
    input  wire         clk_i,
    input  wire         rst_n,           //! the HARD reset only, never the roll-back

    //! ---- the store's memory master (KL_aecp_desc_store mem_*) ----
    input  wire         s_req_valid_i,
    output logic        s_req_ready_o,
    input  wire  [31:0] s_req_addr_i,
    input  wire  [8:0]  s_req_beats_i,
    output logic        s_rsp_valid_o,
    input  wire         s_rsp_ready_i,
    output logic [63:0] s_rsp_data_o,
    output logic        s_rsp_last_o,
    output logic        s_rsp_err_o,

    //! ---- the memory (the integrator's bridge) ----
    output logic        m_req_valid_o,
    input  wire         m_req_ready_i,
    output logic [31:0] m_req_addr_o,
    output logic [8:0]  m_req_beats_o,
    input  wire         m_rsp_valid_i,
    output logic        m_rsp_ready_o,
    input  wire  [63:0] m_rsp_data_i,
    input  wire         m_rsp_last_i,
    input  wire         m_rsp_err_i,

    //! an accepted burst has not yet delivered its terminal beat
    output logic        debt_o
);

  logic owed_r;

  assign m_req_valid_o = s_req_valid_i && !owed_r;
  assign s_req_ready_o = m_req_ready_i && !owed_r;
  assign m_req_addr_o  = s_req_addr_i;
  assign m_req_beats_o = s_req_beats_i;

  assign s_rsp_valid_o = m_rsp_valid_i;
  assign m_rsp_ready_o = s_rsp_ready_i;
  assign s_rsp_data_o  = m_rsp_data_i;
  assign s_rsp_last_o  = m_rsp_last_i;
  assign s_rsp_err_o   = m_rsp_err_i;

  //! set by an accepted request, cleared by the burst's terminal beat
  always_ff @(posedge clk_i) begin : owed_ff
    if (!rst_n) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end
  end

  assign debt_o = owed_r;

endmodule

`default_nettype wire

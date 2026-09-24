/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_desc_mem_guard.sv
//  Project     : IEEE 1722.1 protocol processor
//                (IEEE 1722.1 §7.4.5 READ_DESCRIPTOR;
//                 docs/architecture/07 §3.3.1 memory response isolation)
//
//  Description : Keep the memory's burst debt after the descriptor store's
//                watchdog abandons a fetch. An in-order request FIFO can
//                otherwise accept a new fetch and deliver the abandoned
//                burst's bytes into it. While owed, hold the next request on
//                BOTH faces. Pass every response through unchanged: the store
//                always sinks beats, discarding those it no longer awaits.
//
//                Only the HARD reset clears debt without a terminal beat.
//                Never wire a store-only or D3 rollback reset here. debt_o is
//                the D3 interface: the future writer must hold its restorable
//                owners until debt drains, bounded by its own deadline.
//                This guard has no timeout and does not implement that writer.
//
//                Responses start after request acceptance. An accepted err
//                terminates the burst just like last; no further beats of
//                that burst may follow. Hard reset must flush the memory path.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_desc_mem_guard (
    input  wire         clk_i,           //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,           //! synchronous active-low HARD reset only

    input  wire         s_req_valid_i,   //! store presents a request
    output logic        s_req_ready_o,   //! request accepted only without debt
    input  wire  [31:0] s_req_addr_i,    //! byte address, 8-byte aligned
    input  wire   [8:0] s_req_beats_i,   //! number of 64-bit beats
    output logic        s_rsp_valid_o,   //! memory response, passed through
    input  wire         s_rsp_ready_i,   //! store consumes the response
    output logic [63:0] s_rsp_data_o,    //! response data, unchanged
    output logic        s_rsp_last_o,    //! terminal response beat
    output logic        s_rsp_err_o,     //! terminal error response

    output logic        m_req_valid_o,   //! memory request, suppressed while owed
    input  wire         m_req_ready_i,   //! memory accepts the request
    output logic [31:0] m_req_addr_o,    //! byte address, unchanged
    output logic  [8:0] m_req_beats_o,   //! burst length, unchanged
    input  wire         m_rsp_valid_i,   //! memory presents a response beat
    output logic        m_rsp_ready_o,   //! response ready, passed through
    input  wire  [63:0] m_rsp_data_i,    //! response in big-endian byte order
    input  wire         m_rsp_last_i,    //! final beat of the accepted burst
    input  wire         m_rsp_err_i,     //! error ends the accepted burst

    output logic        debt_o           //! D3: accepted burst still owes a terminal beat
);
  logic owed_r;

  assign m_req_valid_o = s_req_valid_i;
  assign s_req_ready_o = m_req_ready_i;
  assign m_req_addr_o  = s_req_addr_i;
  assign m_req_beats_o = s_req_beats_i;

  assign s_rsp_valid_o = m_rsp_valid_i;
  assign m_rsp_ready_o = s_rsp_ready_i;
  assign s_rsp_data_o  = m_rsp_data_i;
  assign s_rsp_last_o  = m_rsp_last_i;
  assign s_rsp_err_o   = m_rsp_err_i;

  always_ff @(posedge clk_i) begin : owed_ff
    if (!rst_n) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end
  end

  assign debt_o = owed_r;
endmodule : KL_aecp_desc_mem_guard
`default_nettype wire

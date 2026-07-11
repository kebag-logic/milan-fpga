/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_response_builder.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP AEM response frame builder — STUB.

                Assembles the outgoing AECP AEM response frame from:
                  • The mirrored common header (hdr_i) with message_type
                    flipped to MSG_AEM_RESPONSE and status_i inserted.
                  • The descriptor payload read from KL_aecp_aem_store via
                    the accessor response (acc_resp_i).
                  • Dynamic field overrides from KL_aecp_aem_dyn_mux.
                  • L0 state fields needed by ACQUIRE/LOCK responses.

                The raw incoming payload stream (s_axis) is used only to
                extract command-specific fields that must be echoed back.

                tx_done_o pulses for one cycle when the final beat of the
                response has been accepted by m_axis (tlast handshake).

                Ports:
                  hdr_i      — parsed common header
                  status_i   — final status code for this response
                  acc_resp_i — descriptor accessor result
                  l0_state_i — current entity L0 state
                  s_axis     — passthrough of incoming payload (echo fields)
                  m_axis     — assembled response frame
                  tx_done_o  — TX completion strobe

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9.2; Milan v1.2 §5.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_response_builder (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_hdr_t    hdr_i,
  input  wire [4:0]    status_i,
  input  aecp_acc_resp_t acc_resp_i,
  input  aecp_l0_state_t l0_state_i,
  axi_stream_if.slave  s_axis,
  axi_stream_if.master m_axis,
  output logic         tx_done_o
);

  // TODO: implement response assembly FSM

  // Consume slave (echo source), do not forward
  assign s_axis.tready = 1'b1;

  // Drive master outputs to safe defaults
  assign m_axis.tvalid = 1'b0;
  assign m_axis.tdata  = '0;
  assign m_axis.tlast  = 1'b0;
  assign m_axis.tkeep  = '0;
  assign m_axis.tstrb  = '0;
  assign m_axis.tid    = '0;
  assign m_axis.tdest  = '0;
  assign m_axis.tuser  = '0;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      tx_done_o <= 1'b0;
    end else begin
      // TODO: implement
      tx_done_o <= 1'b0;
    end
  end

  // verilator lint_off UNUSED
  wire [4:0] unused_status   = status_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_response_builder not yet implemented");
  end

endmodule

`default_nettype wire

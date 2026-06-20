/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_unsolicited_table.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP unsolicited notification controller table — STUB.

                Maintains the list of controllers that have registered for
                unsolicited notifications via CMD_REGISTER_UNSOLICITED_NOTIFICATION
                (IEEE 1722.1-2021 §9.2.11.2).

                On state_changed_i the module iterates through all registered
                controllers and emits one notification per controller on m_axis.

                Ports:
                  hdr_i         — parsed header (controller_entity_id, command_type)
                  insert_i      — register controller from hdr_i.controller_entity_id
                  remove_i      — deregister controller
                  state_changed_i — AEM state-change event; triggers emission
                  emit_o        — index of controller being notified
                  emit_valid_o  — strobe: emit_o is valid this cycle
                  table_full_o  — table is at MAX_UNSOLICITED_CTLR_C capacity
                  m_axis        — output stream for notification frames

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9.2.11
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_unsolicited_table (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_hdr_t    hdr_i,
  input  wire          insert_i,
  input  wire          remove_i,
  input  wire          state_changed_i,
  output logic [$clog2(MAX_UNSOLICITED_CTLR_C)-1:0] emit_o,
  output logic         emit_valid_o,
  output logic         table_full_o,
  axi_stream_if.master m_axis
);

  // TODO: implement controller table and notification emission FSM

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      emit_o       <= '0;
      emit_valid_o <= 1'b0;
      table_full_o <= 1'b0;
    end else begin
      // TODO: implement
      emit_o       <= '0;
      emit_valid_o <= 1'b0;
      table_full_o <= 1'b0;
    end
  end

  // Drive master outputs to safe defaults
  assign m_axis.tvalid = 1'b0;
  assign m_axis.tdata  = '0;
  assign m_axis.tlast  = 1'b0;
  assign m_axis.tkeep  = '0;
  assign m_axis.tstrb  = '0;
  assign m_axis.tid    = '0;
  assign m_axis.tdest  = '0;
  assign m_axis.tuser  = '0;

  // verilator lint_off UNUSED
  wire unused_ins = insert_i;
  wire unused_rem = remove_i;
  wire unused_sc  = state_changed_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_unsolicited_table not yet implemented");
  end

endmodule

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_cmd_specific_extract.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP command-specific field extractor — STUB.

                Decodes per-command payload fields from the AXI-Stream that
                was forwarded by KL_aecp_common_parser and constructs the
                accessor request bus for KL_aecp_accessor.

                Inputs:
                  hdr_i       — parsed common header (hdr_valid strobe)
                  l0_state_i  — current entity L0 state

                Outputs:
                  acc_req_o   — descriptor lookup request
                  not_impl_o  — command not implemented (STATUS_NOT_IMPLEMENTED)
                  locked_o    — entity locked status flag (for response builder)
                  status_o    — early-out status (override from l0 state check)

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §7.4, §9.2
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_cmd_specific_extract (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_hdr_t    hdr_i,
  input  aecp_l0_state_t l0_state_i,
  output aecp_acc_req_t acc_req_o,
  output logic         not_impl_o,
  output logic         locked_o,
  output logic [4:0]   status_o
);

  // TODO: implement command-specific extraction FSM

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      acc_req_o   <= '0;
      not_impl_o  <= 1'b0;
      locked_o    <= 1'b0;
      status_o    <= STATUS_SUCCESS;
    end else begin
      // TODO: implement
      acc_req_o   <= '0;
      not_impl_o  <= 1'b0;
      locked_o    <= l0_state_i.locked;
      status_o    <= STATUS_NOT_IMPLEMENTED;
    end
  end

  initial begin
    $display("[TODO] KL_aecp_cmd_specific_extract not yet implemented");
  end

endmodule

`default_nettype wire

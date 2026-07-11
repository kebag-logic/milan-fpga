/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_accessor.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP AEM descriptor accessor — STUB.

                Translates an aecp_acc_req_t (config / descriptor-type /
                descriptor-index) into a BRAM byte address and payload size
                by walking the AEM descriptor index table stored in
                KL_aecp_aem_store.

                Inputs:
                  req_i       — accessor request from KL_aecp_cmd_specific_extract
                  bram_data_i — 32-bit read data from KL_aecp_aem_store

                Outputs:
                  resp_o      — resolved BRAM address + size + status
                  bram_addr_o — read address to KL_aecp_aem_store
                  bram_rd_o   — read enable to KL_aecp_aem_store

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §7.3, §7.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_accessor (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_acc_req_t req_i,
  output aecp_acc_resp_t resp_o,
  output logic [15:0]  bram_addr_o,
  output logic         bram_rd_o,
  input  wire  [31:0]  bram_data_i
);

  // TODO: implement descriptor index walk state machine

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      resp_o      <= '0;
      bram_addr_o <= 16'd0;
      bram_rd_o   <= 1'b0;
    end else begin
      // TODO: implement
      bram_rd_o      <= 1'b0;
      bram_addr_o    <= 16'd0;
      resp_o.valid   <= 1'b0;
      resp_o.status  <= STATUS_NOT_IMPLEMENTED;
      resp_o.bram_addr    <= 16'd0;
      resp_o.payload_size <= 16'd0;
      resp_o.dynamic_flag <= 1'b0;
    end
  end

  // verilator lint_off UNUSED
  wire [31:0] unused_bram = bram_data_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_accessor not yet implemented");
  end

endmodule

`default_nettype wire

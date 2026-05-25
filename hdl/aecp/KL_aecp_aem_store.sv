/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_aem_store.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP AEM descriptor BRAM store — STUB.

                Wraps a dual-port BRAM that holds the static AEM descriptor
                tree for the Milan entity.  A factory-reset request causes all
                writable (dynamic) fields to be zeroed back to their
                factory-default values.

                Ports:
                  addr_i            — 16-bit byte read address
                  rd_i              — read enable
                  data_o            — 32-bit read data (1-cycle latency)
                  wr_i              — write enable (from nv_overlay)
                  wr_data_i         — 32-bit write data
                  factory_reset_i   — initiate factory-reset flush
                  flush_in_progress_o — asserted during factory-reset sequence

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §7.3
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_aem_store (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire [15:0]   addr_i,
  input  wire          rd_i,
  output logic [31:0]  data_o,
  input  wire          wr_i,
  input  wire  [31:0]  wr_data_i,
  input  wire          factory_reset_i,
  output logic         flush_in_progress_o
);

  // TODO: implement BRAM inference and factory-reset FSM

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      data_o              <= 32'd0;
      flush_in_progress_o <= 1'b0;
    end else begin
      // TODO: implement
      data_o              <= 32'd0;
      flush_in_progress_o <= 1'b0;
    end
  end

  // verilator lint_off UNUSED
  wire        unused_rd  = rd_i;
  wire [15:0] unused_addr = addr_i;
  wire [31:0] unused_wd  = wr_data_i;
  wire        unused_wr  = wr_i;
  wire        unused_fr  = factory_reset_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_aem_store not yet implemented");
  end

endmodule

`default_nettype wire

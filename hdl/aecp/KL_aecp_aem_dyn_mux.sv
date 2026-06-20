/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_aem_dyn_mux.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP AEM dynamic field multiplexer — STUB.

                Overlays live (dynamic) field values on top of the static BRAM
                content when building GET_* responses.  Dynamic fields include
                items such as stream format, sampling rate, clock source, and
                audio map — values that can be changed at runtime and must be
                served from registers rather than BRAM.

                On epoch_boundary_i (e.g. media clock epoch change) the mux
                may update its register set atomically.

                Ports:
                  hdr_i          — parsed header (command_type, descriptor_type)
                  acc_resp_i     — BRAM address and dynamic_flag from accessor
                  dyn_rd_data_o  — 32-bit dynamic field read data
                  dyn_wr_i       — write enable (from SET_* command path)
                  dyn_wr_data_i  — 32-bit write data
                  epoch_boundary_i — atomic epoch-boundary update strobe

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §7.3; Milan v1.2 §5
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_aem_dyn_mux (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_hdr_t    hdr_i,
  input  aecp_acc_resp_t acc_resp_i,
  output logic [31:0]  dyn_rd_data_o,
  input  wire          dyn_wr_i,
  input  wire  [31:0]  dyn_wr_data_i,
  input  wire          epoch_boundary_i
);

  // TODO: implement dynamic field register file and mux logic

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      dyn_rd_data_o <= 32'd0;
    end else begin
      // TODO: implement
      dyn_rd_data_o <= 32'd0;
    end
  end

  // verilator lint_off UNUSED
  wire        unused_dyn_wr  = dyn_wr_i;
  wire [31:0] unused_dyn_wd  = dyn_wr_data_i;
  wire        unused_epoch   = epoch_boundary_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_aem_dyn_mux not yet implemented");
  end

endmodule

`default_nettype wire

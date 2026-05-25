/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_nv_overlay.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP non-volatile overlay — STUB.

                Sits between KL_aecp_aem_store and the SPI/I2C NV memory
                device (e.g. EEPROM or flash).  On power-up it restores
                previously saved dynamic descriptor fields into the BRAM.
                On a flush request it serialises modified BRAM contents to
                NV storage.

                Ports:
                  bram_addr_i       — read/write address to BRAM
                  bram_rd_i         — read strobe to BRAM
                  bram_data_o       — read data from BRAM (or NV cache)
                  bram_wr_i         — write strobe to BRAM
                  bram_wr_data_i    — write data to BRAM
                  nv_flush_done_o   — pulses when NV write sequence completes
                  flush_in_progress_o — asserted during NV write sequence

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : Milan v1.2 §5.4 (persistent settings)
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_nv_overlay (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire [15:0]   bram_addr_i,
  input  wire          bram_rd_i,
  output logic [31:0]  bram_data_o,
  input  wire          bram_wr_i,
  input  wire  [31:0]  bram_wr_data_i,
  output logic         nv_flush_done_o,
  output logic         flush_in_progress_o
);

  // TODO: implement NV restore-on-boot and flush state machine

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      bram_data_o         <= 32'd0;
      nv_flush_done_o     <= 1'b0;
      flush_in_progress_o <= 1'b0;
    end else begin
      // TODO: implement
      bram_data_o         <= 32'd0;
      nv_flush_done_o     <= 1'b0;
      flush_in_progress_o <= 1'b0;
    end
  end

  // verilator lint_off UNUSED
  wire [15:0] unused_addr = bram_addr_i;
  wire        unused_rd   = bram_rd_i;
  wire        unused_wr   = bram_wr_i;
  wire [31:0] unused_wd   = bram_wr_data_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_nv_overlay not yet implemented");
  end

endmodule

`default_nettype wire

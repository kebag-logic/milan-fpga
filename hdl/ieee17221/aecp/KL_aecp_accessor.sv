/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_accessor.sv
  Description : Descriptor directory lookup: (configuration_index,
                descriptor_type, descriptor_index) -> {base, length} in the
                AEM store, or not-found (NO_SUCH_DESCRIPTOR at the caller).

                The directory is generated (gen/aecp_aem_rom.svh, AEM_DIR_C)
                from the entity model; with the single-configuration Milan
                entity the walk of the aem-and-aecp.md 4-level memory reduces
                to this flat table (the L1/L2 levels collapse — documented
                divergence, revisit when multi-configuration returns).

                Two-level resolve, no comparator scan: the generator asserts
                each type's entries are ONE contiguous, zero-based, ascending
                run of AEM_DIR_C rows and emits the type-direct-indexed
                level-1 table (AEM_L1_CNT_C/AEM_L1_ROW_C, 1:1-checked against
                the linear scan by gen_aem_store.py check_two_level).

                Level 2 lives in BLOCK RAM, read SYNCHRONOUSLY on en_i: a
                combinationally-indexed 252x64 constant array synthesizes as
                distributed ROM (RAMD/F-mux primitives), which is SLICEM-
                locked and does not LUT-combine — it broke slice packing on
                the full tree (the RSC-era lesson). The caller strobes en_i
                one cycle before it dispatches (the DECIDE_S phase-0 resolve
                that used to register this module's combinational outputs);
                the outputs ARE those registers now, frozen until the next
                strobe. Level 1 (64 rows, mostly-constant bits) stays
                combinational — it addresses the BRAM, so it must be.

                Same cycle count and bit-identical answers vs the registered
                combinational lookup it replaces (miss = found 0, base 0,
                len 0; config gate unchanged).

  Spec refs   : IEEE Std 1722.1-2021 §7.4.5 (READ_DESCRIPTOR)
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
  input  wire          en_i,          //! capture strobe: resolve + register
  input  wire  [15:0]  config_idx_i,
  input  wire  [15:0]  desc_type_i,
  input  wire  [15:0]  desc_index_i,
  output logic         found_o,       //! registered; valid the cycle after en_i
  output logic [15:0]  base_o,        //! ...frozen until the next en_i
  output logic [15:0]  len_o
);

  `include "gen/aecp_aem_rom.svh"

  //! directory row address width (252 rows on the 8x8 ship shape)
  localparam int unsigned DIR_AW_C =
      (AEM_DESC_N_C > 1) ? $clog2(AEM_DESC_N_C) : 1;

  //! level-2 directory as block ROM (see banner: distributed ROM broke
  //! slice packing). Same init idiom as KL_aecp_aem_store's mem_r, which
  //! Vivado maps to RAMB.
  (* rom_style = "block" *) logic [63:0] dir_rom_r [0:AEM_DESC_N_C-1];
  initial begin : dir_rom_init
    for (int unsigned k = 0; k < AEM_DESC_N_C; k++)
      dir_rom_r[k] = AEM_DIR_C[k];
  end

  logic                   w_type_ok;  //! type below the level-1 table bound
  logic [AEM_L1_AW_C-1:0] w_l1_idx;   //! level-1 row (type low bits)
  logic [15:0]            w_cnt;      //! entries of this type (0 = absent)
  logic [15:0]            w_row;      //! AEM_DIR_C row of the type's index 0
  logic                   w_idx_ok;   //! descriptor_index inside the run
  logic [DIR_AW_C-1:0]    w_dir_idx;  //! level-2 ROM row

  always_comb begin
    //! level 1: type-direct-indexed {count, first row}. The table is
    //! zero-padded to 1 << AEM_L1_AW_C rows, so the low type bits index it
    //! unclamped: an absent type reads count 0, and a type at/above
    //! AEM_L1_N_C (whose low bits would alias) is excluded by w_type_ok.
    w_type_ok = (desc_type_i < 16'(AEM_L1_N_C));
    w_l1_idx  = desc_type_i[AEM_L1_AW_C-1:0];
    w_cnt     = AEM_L1_CNT_C[w_l1_idx];
    w_row     = AEM_L1_ROW_C[w_l1_idx];
    w_idx_ok  = (desc_index_i < w_cnt);
    //! level 2 address: per-type runs are contiguous, zero-based and
    //! ascending (generator-asserted), so row + index stays inside
    //! AEM_DIR_C whenever w_idx_ok holds (clamped to the run base otherwise)
    w_dir_idx = DIR_AW_C'(w_row + (w_idx_ok ? desc_index_i : 16'd0));
  end

  logic        found_q;  //! registered hit
  logic [63:0] rec_q;    //! registered directory record (BRAM data register)

  always_ff @(posedge clk_i) begin : found_reg
    if (!rst_n)
      found_q <= 1'b0;
    else if (en_i)
      found_q <= (config_idx_i < 16'(NUM_CONFIGURATIONS_C))
                 && w_type_ok && w_idx_ok;
  end

  //! no reset on purpose: this is the BRAM read port (EN = en_i); a reset
  //! here would be a register the RAMB primitive cannot absorb
  always_ff @(posedge clk_i) begin : rec_read
    if (en_i)
      rec_q <= dir_rom_r[w_dir_idx];
  end

  always_comb begin
    found_o = found_q;
    base_o  = found_q ? rec_q[31:16] : 16'd0;
    len_o   = found_q ? rec_q[15:0]  : 16'd0;
  end

endmodule

`default_nettype wire

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
                the linear scan by gen_aem_store.py check_two_level), so the
                lookup is two ROM reads and one index bound check. This
                replaced a 252-entry (8x8 shape) parallel compare + priority
                mux — the accessor's area lever.

                Purely combinational; registered by the caller.

  Spec refs   : IEEE Std 1722.1-2021 §7.4.5 (READ_DESCRIPTOR)
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_accessor (
  input  wire  [15:0]  config_idx_i,
  input  wire  [15:0]  desc_type_i,
  input  wire  [15:0]  desc_index_i,
  output logic         found_o,
  output logic [15:0]  base_o,
  output logic [15:0]  len_o
);

  `include "gen/aecp_aem_rom.svh"

  //! directory row address width (252 rows on the 8x8 ship shape)
  localparam int unsigned DIR_AW_C =
      (AEM_DESC_N_C > 1) ? $clog2(AEM_DESC_N_C) : 1;

  logic                   w_type_ok;  //! type below the level-1 table bound
  logic [AEM_L1_AW_C-1:0] w_l1_idx;   //! level-1 row (type low bits)
  logic [15:0]            w_cnt;      //! entries of this type (0 = absent)
  logic [15:0]            w_row;      //! AEM_DIR_C row of the type's index 0
  logic                   w_idx_ok;   //! descriptor_index inside the run
  logic [DIR_AW_C-1:0]    w_dir_idx;  //! level-2 ROM row
  logic [63:0]            w_rec;      //! its directory record

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
    //! level 2: a direct ROM read. Per-type runs are contiguous, zero-based
    //! and ascending (generator-asserted), so row + index stays inside
    //! AEM_DIR_C whenever w_idx_ok holds (clamped to the run base otherwise)
    w_dir_idx = DIR_AW_C'(w_row + (w_idx_ok ? desc_index_i : 16'd0));
    w_rec     = AEM_DIR_C[w_dir_idx];

    found_o = 1'b0;
    base_o  = 16'd0;
    len_o   = 16'd0;
    if (config_idx_i < 16'(NUM_CONFIGURATIONS_C) && w_type_ok && w_idx_ok)
    begin
      found_o = 1'b1;
      base_o  = w_rec[31:16];
      len_o   = w_rec[15:0];
    end
  end

endmodule

`default_nettype wire

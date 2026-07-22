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

  always_comb begin
    found_o = 1'b0;
    base_o  = 16'd0;
    len_o   = 16'd0;
    if (config_idx_i < 16'(NUM_CONFIGURATIONS_C)) begin
      for (int unsigned n = 0; n < AEM_DESC_N_C; n++) begin
        if (AEM_DIR_C[n][63:48] == desc_type_i &&
            AEM_DIR_C[n][47:32] == desc_index_i) begin
          found_o = 1'b1;
          base_o  = AEM_DIR_C[n][31:16];
          len_o   = AEM_DIR_C[n][15:0];
        end
      end
    end
  end

endmodule

`default_nettype wire

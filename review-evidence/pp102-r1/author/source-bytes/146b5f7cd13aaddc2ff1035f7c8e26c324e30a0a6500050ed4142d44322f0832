/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_release_merge.sv
//  Project     : IEEE 1722.1 protocol processor
//
//  Description : Lossless two-source merge for KL_pp_tx_slots release
//                strobes. Each legal slot handle becomes a bit in a pending
//                set, and at most one bit is retired per cycle through the
//                pool's single release port. Simultaneous distinct releases
//                are therefore serialized instead of priority-dropped.
//
//  Decision    : pending state is tracked per physical slot, not in a finite
//                FIFO. A slot cannot carry two live ownership claims, so
//                duplicate release requests are idempotent while the set has
//                enough capacity for every distinct release that can exist.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_release_merge #(
    parameter int unsigned N_SLOTS_P = 5,
    localparam int unsigned SLOT_W_C = (N_SLOTS_P > 1)
                                           ? $clog2(N_SLOTS_P) : 1
) (
    input  wire                 clk_i,
    input  wire                 rst_n,
    input  wire                 a_valid_i,
    input  wire [SLOT_W_C-1:0]  a_slot_i,
    input  wire                 b_valid_i,
    input  wire [SLOT_W_C-1:0]  b_slot_i,
    output logic                release_valid_o,
    output logic [SLOT_W_C-1:0] release_slot_o
);

  if (N_SLOTS_P < 1) begin : g_slot_count_check
    $error("KL_pp_release_merge: N_SLOTS_P must be positive");
  end

  logic [N_SLOTS_P-1:0] pending_r;
  logic [N_SLOTS_P-1:0] request_w;
  logic [N_SLOTS_P-1:0] available_w;

  always_comb begin : collect_requests
    request_w = '0;
    if (a_valid_i && (32'(a_slot_i) < N_SLOTS_P)) request_w[a_slot_i] = 1'b1;
    if (b_valid_i && (32'(b_slot_i) < N_SLOTS_P)) request_w[b_slot_i] = 1'b1;
  end

  assign available_w = pending_r | request_w;

  always_comb begin : release_pick
    release_valid_o = 1'b0;
    release_slot_o  = '0;
    for (int i = int'(N_SLOTS_P) - 1; i >= 0; i--) begin
      if (available_w[i]) begin
        release_valid_o = 1'b1;
        release_slot_o  = SLOT_W_C'(i);
      end
    end
  end

  always_ff @(posedge clk_i) begin : pending_state
    if (!rst_n) begin
      pending_r <= '0;
    end else begin
      pending_r <= available_w;
      if (release_valid_o) pending_r[release_slot_o] <= 1'b0;
    end
  end

endmodule : KL_pp_release_merge
`default_nettype wire

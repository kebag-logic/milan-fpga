/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_stream_table.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : NxN stream-table authority (docs/NXN_ARCHITECTURE.md §1.1,
                phase P1). The classification table consumed by
                avtp_stream_parser: one 64-bit stream_id + enable per AAF
                listener sink s = 0..N_LISTENERS_P-1. The match key is the
                wire-truth stream_id, never the DMAC.

                Entry sources (spec §1.1):
                  - entry 0 aliases the ACMP listener SM's bound record
                    (bound0_i/sid0_i) COMBINATIONALLY - the exact wires the
                    parser consumed before this table existed, so the N=1
                    shape is bit-identical (no-regression axiom);
                  - entries 1..N-1 (and an explicit bench override of entry
                    0) are written through the CSR-window port (phase P11
                    plugs the 0x800 A_STRMW group in here; TBs drive it
                    directly). An override write with en=0 evicts the entry.

                bind_rise_o pulses one cycle on an entry's not-bound->bound
                edge - the per-stream LCTX counter-reset trigger
                ([M-5.3.8.10], consumed by KL_avtp_rx_monitor_ctx in P2).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! NxN stream-table authority (NXN_ARCHITECTURE §1.1 / P1): per-sink 64-bit
//! stream_id match entries for `avtp_stream_parser`. Entry 0 aliases the ACMP
//! bound record combinationally (bit-exact N=1 legacy); entries 1..N-1 and
//! bench overrides come through the CSR-window write port (P11 hook).
//! `bind_rise_o[s]` pulses on that entry's not-bound->bound edge.

`default_nettype none

module KL_stream_table #(
  parameter int unsigned N_LISTENERS_P = 1   //! AAF listener sinks (table depth)
)(
  input  wire         clk_i,           //! Global clock
  input  wire         rst_n,           //! Active-low synchronous reset

  //! --- stream-0 legacy authority (ACMP listener SM bound record) ---------
  input  wire         bound0_i,        //! listener sink 0 bound (level)
  input  wire [63:0]  sid0_i,          //! sink 0 bound stream_id

  //! --- CSR-window override/write port (P11 hook; TB-driven meanwhile) ----
  input  wire         wr_en_i,         //! one-cycle write strobe
  input  wire [3:0]   wr_idx_i,        //! entry index s
  input  wire [63:0]  wr_sid_i,        //! entry stream_id
  input  wire         wr_valid_i,      //! entry enable (0 = evict)

  //! --- classification table out (avtp_stream_parser cfg pins) ------------
  output logic [64*N_LISTENERS_P-1:0] tbl_sid_o,   //! per-entry stream_id
  output logic [N_LISTENERS_P-1:0]    tbl_en_o,    //! per-entry enable
  output logic [N_LISTENERS_P-1:0]    bind_rise_o  //! not-bound->bound pulse
);

  //! override storage: entry 0 only takes effect once explicitly written
  //! (ovr_armed) so the reset default stays the pure ACMP alias
  logic [63:0] ovr_sid_r   [N_LISTENERS_P];
  logic        ovr_en_r    [N_LISTENERS_P];
  logic        ovr_armed_r [N_LISTENERS_P];

  always_ff @(posedge clk_i) begin : tbl_write
    if (!rst_n) begin
      for (int s = 0; s < N_LISTENERS_P; s++) begin
        ovr_sid_r[s]   <= '0;
        ovr_en_r[s]    <= 1'b0;
        ovr_armed_r[s] <= 1'b0;
      end
    end
    else if (wr_en_i && (32'(wr_idx_i) < N_LISTENERS_P)) begin
      ovr_sid_r[wr_idx_i]   <= wr_sid_i;
      ovr_en_r[wr_idx_i]    <= wr_valid_i;
      ovr_armed_r[wr_idx_i] <= 1'b1;
    end
  end : tbl_write

  //! effective table: entry 0 = ACMP alias unless a bench override armed it
  always_comb begin : tbl_mux
    for (int s = 0; s < N_LISTENERS_P; s++) begin
      if (s == 0 && !ovr_armed_r[0]) begin
        tbl_sid_o[64*s +: 64] = sid0_i;
        tbl_en_o[s]           = bound0_i;
      end
      else begin
        tbl_sid_o[64*s +: 64] = ovr_sid_r[s];
        tbl_en_o[s]           = ovr_en_r[s];
      end
    end
  end : tbl_mux

  //! per-entry bind edge (LCTX CNT-region reset trigger, [M-5.3.8.10])
  logic [N_LISTENERS_P-1:0] en_q_r;
  always_ff @(posedge clk_i) begin : bind_edge
    if (!rst_n) begin
      en_q_r      <= '0;
      bind_rise_o <= '0;
    end
    else begin
      en_q_r      <= tbl_en_o;
      bind_rise_o <= tbl_en_o & ~en_q_r;
    end
  end : bind_edge

endmodule

`default_nettype wire

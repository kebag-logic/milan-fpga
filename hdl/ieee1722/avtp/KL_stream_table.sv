/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_stream_table.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : NxN stream-table authority (docs/fpga/FPGA_DESIGN.md section 2).
                The classification table consumed by
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

                STORAGE DECISION (P12, the lane-K "override sids to RAM"
                lever - evaluated and REJECTED): the override sids stay a
                flop array. The consumer is avtp_stream_parser's N-way
                COMBINATIONAL 64-bit compare - every entry is read every
                cycle in parallel, which a house-rules RAM (ONE explicit
                sync read port, defect-4 lineage) cannot serve; N read
                ports would be exactly the inferred read-port-replica
                divergence defect 4 forbids, and serializing the match
                would put a walk into the frame-classification path (the
                index must ride the frame as tuser, NXN §1.1). Cost at
                N=8 is ~530 FF (8 x 66 b) - not worth a spec exception.

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

  //! --- per-sink ACMP bind view (task #32: the UNBIND must reach the
  //! parser). Sinks 1..N-1 previously had NO alias - only the CSR window
  //! wrote them - so a DISCONNECT_RX left tbl_en high with the stale sid
  //! and the parser delivered the departed stream forever (silicon
  //! 08-07: LATE events armed 1/s pushes = the Hive flapping). Now every
  //! entry defaults to ITS sink's bind level exactly like entry 0 always
  //! did; the window override still WINS while armed (software-owns law).
  input  wire [N_LISTENERS_P-1:0]      bound_v_i,   //! per-sink bind level
  input  wire [64*N_LISTENERS_P-1:0]   sid_v_i,     //! per-sink bound sid

  //! --- CSR-window override/write port (P11 hook; TB-driven meanwhile) ----
  input  wire         wr_en_i,         //! one-cycle write strobe
  input  wire [3:0]   wr_idx_i,        //! entry index s
  input  wire [63:0]  wr_sid_i,        //! entry stream_id
  input  wire         wr_valid_i,      //! entry enable (0 = evict)

  //! --- classification table out (avtp_stream_parser cfg pins) ------------
  output logic [64*N_LISTENERS_P-1:0] tbl_sid_o,   //! per-entry stream_id
  output logic [N_LISTENERS_P-1:0]    tbl_en_o,    //! per-entry enable
  output logic [N_LISTENERS_P-1:0]    bind_rise_o, //! not-bound->bound pulse
  output logic [N_LISTENERS_P-1:0]    bind_fall_o  //! bound->not-bound pulse
                                                   //! (task #32: the wipe
                                                   //! event the monitor's
                                                   //! unlock law rides)
);

  //! override storage: an entry only takes effect once explicitly written
  //! (ovr_armed) so the reset default stays the pure ACMP alias - since
  //! task #32 that law holds for EVERY entry, not just 0
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
      //! RELEASE-TO-ALIAS: an eviction (valid=0) that carries the zero sid
      //! DISARMS the override instead of arming it, so entry 0 can return to
      //! the ACMP alias at runtime. Without this, `ovr_armed_r[0]` was set by
      //! any write and cleared only by reset: one stray window CTRL write
      //! detached the alias for good and every later CONNECT_RX bound but
      //! never matched. Inert for idx>0 (tbl_mux only consults ovr_armed for
      //! entry 0) and for every arming write, so the deployed provisioning
      //! sequence is unchanged.
      ovr_armed_r[wr_idx_i] <= !(!wr_valid_i && (wr_sid_i == 64'd0));
    end
  end : tbl_write

  //! effective table: every entry = its sink's ACMP alias unless a window
  //! override armed it (entry 0's original law, generalized by task #32 -
  //! the release-to-alias eviction above applies per entry the same way).
  //! Entry 0 keeps the dedicated bound0/sid0 pair (the legacy authority);
  //! entries 1..N-1 read the per-sink bind view.
  always_comb begin : tbl_mux
    for (int s = 0; s < N_LISTENERS_P; s++) begin
      if (!ovr_armed_r[s]) begin
        tbl_sid_o[64*s +: 64] = (s == 0) ? sid0_i : sid_v_i[64*s +: 64];
        tbl_en_o[s]           = (s == 0) ? bound0_i : bound_v_i[s];
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
      bind_fall_o <= '0;
    end
    else begin
      en_q_r      <= tbl_en_o;
      bind_rise_o <= tbl_en_o & ~en_q_r;
      bind_fall_o <= ~tbl_en_o & en_q_r;
    end
  end : bind_edge

endmodule

`default_nettype wire

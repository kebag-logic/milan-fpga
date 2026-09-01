/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_pcm_route.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : NxN fabric-render selection between the shared AAF RX
                depacketizer and the physical listener path. The context ABI
                keeps its legacy 2-bit route word, but bit 0 is reserved and
                ignored; bit 1 selects RENDER. If several streams request
                render, the lowest index wins deterministically. Stream 0
                renders after reset and all payload is consumed regardless
                of whether it is selected.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! NxN fabric-render policy: the legacy route word is {RENDER, reserved},
//! RENDER-lowest-wins, and the selected depacketizer stream is exposed as a
//! combinational clone tap. Stream 0 renders after reset.

`default_nettype none

module KL_pcm_route #(
  parameter int unsigned N_LISTENERS_P = 1   //! listener streams
)(
  input  wire         clk_i,           //! Global clock
  input  wire         rst_n,           //! Active-low synchronous reset

  //! --- depacketizer payload in (one AXIS frame per PDU, tuser = s) ------
  input  wire [63:0]  s_tdata_i,
  input  wire         s_tvalid_i,
  input  wire         s_tlast_i,
  input  wire [3:0]   s_tuser_i,
  output logic        s_tready_o,

  //! --- route configuration (P11 CSR window / LCTX w4 CTRL[2:1]) ---------
  input  wire         route_wr_en_i,   //! one-cycle write strobe
  input  wire [3:0]   route_wr_idx_i,  //! stream index s
  input  wire [1:0]   route_wr_val_i,  //! {RENDER, reserved}; bit 0 ignored

  //! --- render tap (RENDER stream only; source is always consumed) -------
  output logic        render_tvalid_o,
  output logic [63:0] render_tdata_o,
  output logic        render_tlast_o,
  output logic [3:0]  render_sel_o,    //! RENDER stream index (lowest wins)
  output logic        render_active_o  //! a RENDER stream is configured
);

  //! The legacy word stays two bits wide at the LCTX/CSR ABI. Bit 0 has no
  //! product implementation and is forced to zero on every write.
  localparam int unsigned ROUTE_RENDER_B_C = 1;  //! bit 1: render candidate
  localparam logic [1:0] ROUTE_NULL_C    = 2'b00;
  localparam logic [1:0] ROUTE_DEFAULT_C = 2'b10;

  //! Per-stream route registers: stream 0 renders at reset; all others are
  //! disabled. The reserved bit reads as zero within this block.
  logic [1:0] route_r [N_LISTENERS_P];

  always_ff @(posedge clk_i) begin : route_cfg
    if (!rst_n) begin
      route_r[0] <= ROUTE_DEFAULT_C;
      for (int s = 1; s < N_LISTENERS_P; s++) route_r[s] <= ROUTE_NULL_C;
    end
    else if (route_wr_en_i && (32'(route_wr_idx_i) < N_LISTENERS_P)) begin
      route_r[route_wr_idx_i] <= {route_wr_val_i[ROUTE_RENDER_B_C], 1'b0};
    end
  end : route_cfg

  //! RENDER-lowest-wins arbitration (spec §1.3, deterministic rule) over
  //! the RENDER flag (the reserved bit does not affect the pick)
  always_comb begin : render_pick
    render_sel_o    = '0;
    render_active_o = 1'b0;
    for (int s = N_LISTENERS_P-1; s >= 0; s--) begin
      if (route_r[s][ROUTE_RENDER_B_C]) begin
        render_sel_o    = 4'(s);
        render_active_o = 1'b1;
      end
    end
  end : render_pick

  wire       is_render_w = render_active_o && (s_tuser_i == render_sel_o);

  //! No queued media sink remains. The depacketizer advances after the live
  //! fabric clone taps sample the beat.
  assign s_tready_o = 1'b1;

  //! Render tap: the selected stream's share of the always-ready source.
  always_comb begin : render_tap
    render_tdata_o  = s_tdata_i;
    render_tlast_o  = s_tlast_i;
    render_tvalid_o = s_tvalid_i && is_render_w;
  end : render_tap

endmodule

`default_nettype wire

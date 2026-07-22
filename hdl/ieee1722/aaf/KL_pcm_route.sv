/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_pcm_route.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : NxN PCM routing policy (docs/NXN_ARCHITECTURE.md §1.3,
                phase P3). Sits between the shared AAF RX depacketizer
                (payload AXIS + tuser stream index) and the sinks:

                  route 0 NULL   - payload discarded (the monitor still
                                   counts, [M-5.3.8.10])
                  route 1 RENDER - feeds the physical render path (LPF +
                                   KL_i2s_playback). Exactly one stream
                                   renders; if several are configured
                                   RENDER, the LOWEST-indexed one wins
                                   (deterministic rule, RTL-enforced).
                  route 2 DMA    - payload to the per-stream PCM DMA ring
                                   (ring base + s*stride at the SoC layer;
                                   the ring output carries tuser = s).

                Reset default: stream 0 = RENDER, others NULL - the N=1
                shape is bit-identical to today (no-regression axiom).

                N=1 COMPAT NOTE (documented spec deviation): in the shipping
                single-stream datapath the RENDER stream's payload ALSO
                flows to the DRAM PCM ring (the PipeWire consumer path).
                A literally-exclusive route field would break that, so
                RENDER frames are forwarded on the ring output AND tapped
                by the render feed - the spec's route semantics are applied
                to the render/discard decision only. NULL alone suppresses
                the ring copy.

                Zero-latency combinational pass-through: at N=1 the ring
                output and the render tap are wire-identical to the
                depacketizer output (the golden TBs prove this).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! NxN PCM routing policy (NXN_ARCHITECTURE §1.3 / P3): per-stream 2-bit
//! route field (NULL/RENDER/DMA), RENDER-lowest-wins arbitration, tuser-
//! tagged ring output, combinational render tap (bit-exact N=1 legacy).

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
  input  wire [1:0]   route_wr_val_i,  //! 0 NULL / 1 RENDER / 2 DMA

  //! --- PCM ring output (RENDER + DMA streams; tuser = s) ----------------
  output logic [63:0] m_axis_tdata,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,
  output logic [3:0]  m_axis_tuser,
  input  wire         m_axis_tready,

  //! --- render tap (RENDER stream only; consumer keeps the ring tready) --
  output logic        render_tvalid_o,
  output logic [63:0] render_tdata_o,
  output logic        render_tlast_o,
  output logic [3:0]  render_sel_o,    //! RENDER stream index (lowest wins)
  output logic        render_active_o  //! a RENDER stream is configured
);

  localparam logic [1:0] ROUTE_NULL_C   = 2'd0;
  localparam logic [1:0] ROUTE_RENDER_C = 2'd1;
  localparam logic [1:0] ROUTE_DMA_C    = 2'd2;

  //! per-stream route registers; reset = today's shape (s0 RENDER, rest NULL)
  logic [1:0] route_r [N_LISTENERS_P];

  always_ff @(posedge clk_i) begin : route_cfg
    if (!rst_n) begin
      route_r[0] <= ROUTE_RENDER_C;
      for (int s = 1; s < N_LISTENERS_P; s++) route_r[s] <= ROUTE_NULL_C;
    end
    else if (route_wr_en_i && (32'(route_wr_idx_i) < N_LISTENERS_P)) begin
      route_r[route_wr_idx_i] <= route_wr_val_i;
    end
  end : route_cfg

  //! RENDER-lowest-wins arbitration (spec §1.3, deterministic rule)
  always_comb begin : render_pick
    render_sel_o    = '0;
    render_active_o = 1'b0;
    for (int s = N_LISTENERS_P-1; s >= 0; s--) begin
      if (route_r[s] == ROUTE_RENDER_C) begin
        render_sel_o    = 4'(s);
        render_active_o = 1'b1;
      end
    end
  end : render_pick

  //! per-frame route of the current beat (tuser is frame-stable)
  logic [1:0] cur_route_w;
  always_comb begin : route_lookup
    cur_route_w = ROUTE_NULL_C;
    for (int s = 0; s < N_LISTENERS_P; s++)
      if (32'(s_tuser_i) == s) cur_route_w = route_r[s];
  end : route_lookup
  wire       is_null_w   = (cur_route_w == ROUTE_NULL_C);
  wire       is_render_w = render_active_o && (s_tuser_i == render_sel_o);

  //! ring output: NULL frames swallowed, everything else passes untouched
  always_comb begin : ring_out
    m_axis_tdata  = s_tdata_i;
    m_axis_tlast  = s_tlast_i;
    m_axis_tuser  = s_tuser_i;
    m_axis_tvalid = s_tvalid_i && !is_null_w;
    s_tready_o    = is_null_w ? 1'b1 : m_axis_tready;
  end : ring_out

  //! render tap: the RENDER stream's share of the ring handshake (the
  //! consumer observes the ring tready exactly as in the flat datapath)
  always_comb begin : render_tap
    render_tdata_o  = s_tdata_i;
    render_tlast_o  = s_tlast_i;
    render_tvalid_o = s_tvalid_i && !is_null_w && is_render_w;
  end : render_tap

endmodule

`default_nettype wire

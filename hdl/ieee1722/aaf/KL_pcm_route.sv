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
                phase P3; flag rework per the ALSA driver design feedback,
                the-private-test-repo fpga/docs/ALSA_DRIVER_DESIGN.md open
                question 4). Sits between the shared AAF RX depacketizer
                (payload AXIS + tuser stream index) and the sinks.

                The 2-bit route field is a pair of INDEPENDENT flags, not
                an exclusive enum:

                  bit 0 DMA    - payload to the per-stream PCM DMA ring
                                 (ring base + s*stride at the SoC layer;
                                 the ring output carries tuser = s).
                  bit 1 RENDER - feeds the physical render path (LPF +
                                 KL_i2s_playback). Exactly one stream
                                 renders; if several carry the RENDER
                                 flag, the LOWEST-indexed one wins
                                 (deterministic rule, RTL-enforced).

                  0b00 NULL       : neither (payload discarded; the
                                    monitor still counts, [M-5.3.8.10])
                  0b01 DMA        : ring only
                  0b10 RENDER     : render only (no ring copy)
                  0b11 RENDER|DMA : capture-while-rendering - the stream
                                    renders AND lands in its DMA ring

                MAPPING FROM THE P3 ENUM (0 NULL / 1 RENDER / 2 DMA):
                  P3 0 NULL   -> 0b00 (same bits, same behavior)
                  P3 1 RENDER -> 0b11 (P3's RENDER de-facto ALSO forwarded
                                 the ring copy - the documented N=1 compat
                                 deviation; the flags now express it
                                 directly as RENDER|DMA)
                  P3 2 DMA    -> 0b01 (bit VALUE changes: 2 now means
                                 RENDER-only)
                Reset default: stream 0 = 0b11 (RENDER|DMA - exactly the
                P3 "RENDER" behavior: render tap + ring copy), others
                0b00 - the N=1 shape is bit-identical to P3
                (no-regression axiom).

                Zero-latency combinational pass-through: at N=1 the ring
                output and the render tap are wire-identical to the
                depacketizer output (the golden TBs prove this).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! NxN PCM routing policy (NXN_ARCHITECTURE §1.3 / P3 + flag rework): per-
//! stream 2-bit route FLAGS {bit1 RENDER, bit0 DMA} - independently
//! combinable (0b11 = capture-while-rendering, 0b00 = NULL), RENDER-lowest-
//! wins arbitration, tuser-tagged ring output, combinational render tap
//! (reset s0 = RENDER|DMA: bit-exact P3/N=1 legacy).

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
  input  wire [1:0]   route_wr_val_i,  //! flags {bit1 RENDER, bit0 DMA}

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

  //! route field = independent flags (see header for the P3 enum mapping)
  localparam int unsigned ROUTE_DMA_B_C    = 0;  //! bit 0: ring copy
  localparam int unsigned ROUTE_RENDER_B_C = 1;  //! bit 1: render candidate
  localparam logic [1:0] ROUTE_NULL_C    = 2'b00;
  localparam logic [1:0] ROUTE_LEGACY0_C = 2'b11; //! P3 s0 default (RENDER
                                                  //! + ring copy) bit-exact

  //! per-stream route registers; reset = the P3 shape (s0 render + ring
  //! copy = today's shipped behavior, rest NULL)
  logic [1:0] route_r [N_LISTENERS_P];

  always_ff @(posedge clk_i) begin : route_cfg
    if (!rst_n) begin
      route_r[0] <= ROUTE_LEGACY0_C;
      for (int s = 1; s < N_LISTENERS_P; s++) route_r[s] <= ROUTE_NULL_C;
    end
    else if (route_wr_en_i && (32'(route_wr_idx_i) < N_LISTENERS_P)) begin
      route_r[route_wr_idx_i] <= route_wr_val_i;
    end
  end : route_cfg

  //! RENDER-lowest-wins arbitration (spec §1.3, deterministic rule) over
  //! the RENDER flag (the DMA flag does not affect the pick)
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

  //! per-frame route of the current beat (tuser is frame-stable)
  logic [1:0] cur_route_w;
  always_comb begin : route_lookup
    cur_route_w = ROUTE_NULL_C;
    for (int s = 0; s < N_LISTENERS_P; s++)
      if (32'(s_tuser_i) == s) cur_route_w = route_r[s];
  end : route_lookup
  wire       to_ring_w   = cur_route_w[ROUTE_DMA_B_C];
  wire       is_render_w = render_active_o && (s_tuser_i == render_sel_o);

  //! ring output: only DMA-flagged frames pass; everything else is
  //! swallowed here (a render-only frame still reaches the tap below -
  //! its beats self-advance since the ring lane does not hold them)
  always_comb begin : ring_out
    m_axis_tdata  = s_tdata_i;
    m_axis_tlast  = s_tlast_i;
    m_axis_tuser  = s_tuser_i;
    m_axis_tvalid = s_tvalid_i && to_ring_w;
    s_tready_o    = to_ring_w ? m_axis_tready : 1'b1;
  end : ring_out

  //! render tap: the RENDER-selected stream's share of the source
  //! handshake (with the DMA flag set the consumer observes the ring
  //! tready exactly as in the flat datapath; render-only frames advance
  //! one beat per cycle)
  always_comb begin : render_tap
    render_tdata_o  = s_tdata_i;
    render_tlast_o  = s_tlast_i;
    render_tvalid_o = s_tvalid_i && is_render_w;
  end : render_tap

endmodule

`default_nettype wire

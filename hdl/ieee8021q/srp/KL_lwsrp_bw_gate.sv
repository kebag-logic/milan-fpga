/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_bw_gate.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : Reservation resolution + bandwidth provisioning, NxN
//                Σ-slope generalization (docs/NXN_ARCHITECTURE.md §2.4/§3.4,
//                phase P5; docs/LWSRP_FPGA_ARCHITECTURE.md §3):
//
//                  ACTIVE(t) := talker declared(t) AND listener READY(t)
//                               AND domain ok AND ADMITTED by the Σ-limit
//
//                Class-A idleSlope per stream from its TSpec:
//                  slope(t)[bps] = MaxIntervalFrames(t) x (MaxFrameSize(t)
//                                  + 42) x 8 x 8000
//                idleSlope(queue) = Σ granted slopes; `over_limit` = some
//                requested stream refused by the 75 % port-rate ceiling.
//
//                Σ-slope arbitration (the spec's deterministic rule):
//                GREEDY IN STREAM-INDEX ORDER - a stream is admitted iff
//                the running Σ including it stays <= the ceiling; a
//                refused stream never displaces a lower-indexed grant.
//                At N=1 this degenerates to the old single compare
//                (refusal = slope > limit), keeping today's behavior
//                bit-compatible.
//
//                Engine shape per timing-risk row T5: SEQUENTIAL walks -
//                one stream's slope through the 3-stage multiply pipeline
//                per cycle, one stream's admission decision per cycle
//                (the CBS sequential-slope-engine pattern). No parallel
//                49-bit adder tree.
//
//                Ordering per stream (FR-SRP-03 - a withdrawn reservation
//                can never leak frames):
//                  activate:  slope joins Σ FIRST, stream_gate(t) opens
//                             HOLD_CYCLES_C later;
//                  teardown:  stream_gate(t) closes IMMEDIATELY, its
//                             slope leaves Σ HOLD_CYCLES_C later.
//---------------------------------------------------------------------------//

//! NxN Σ-slope reservation gate (NXN §2.4/§3.4 / P5): sequential per-stream
//! slope pipeline + greedy index-order admission against the 75 % ceiling;
//! per-stream gate/slope ordering FSMs; Σ of held slopes drives the single
//! class-A idleSlope. N=1 = today's behavior (lwsrp TB golden).

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_bw_gate #(
  parameter int unsigned HOLD_CYCLES_C = 16,
  parameter int unsigned N_STREAMS_P   = 1     //! talker stream contexts
)(
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,            //! lwSRP engine enable (CSR)

    // ---- per-stream reservation inputs ----------------------------------
    input  wire [N_STREAMS_P-1:0] talker_declared_i,  //! KL_lwsrp_tx
    input  wire [N_STREAMS_P-1:0] listener_ready_i,   //! registrar(s)
    input  wire        domain_ok_i,         //! KL_lwsrp_registrar
    input  wire        is_1g_i,             //! port rate (1 = 1 Gb/s)

    // ---- per-stream TSpec (SCTX / CSR stream table) ----------------------
    input  wire [16*N_STREAMS_P-1:0] max_frame_i,
    input  wire [16*N_STREAMS_P-1:0] interval_frames_i,

    // ---- outputs ---------------------------------------------------------
    output logic [N_STREAMS_P-1:0] stream_gate_o,  //! per-stream admission
    output reg         slope_en_o,          //! CBS slope MUX select (any)
    output reg  [31:0] idle_slope_o,        //! Σ granted idleSlope, bps
    output wire [N_STREAMS_P-1:0] res_active_o,    //! reservation ACTIVE
    output reg         over_limit_o         //! some TSpec refused by 75 %
);

  localparam int unsigned IDXW_C = (N_STREAMS_P <= 1) ? 1
                                                      : $clog2(N_STREAMS_P);

  //! 75 % of the port rate, bps
  wire [48:0] limit_w = is_1g_i ? 49'd750_000_000 : 49'd75_000_000;

  //! per-stream request (live level; instant teardown guard)
  wire [N_STREAMS_P-1:0] req_w =
      talker_declared_i & listener_ready_i &
      {N_STREAMS_P{enable_i & domain_ok_i}};

  // -----------------------------------------------------------------------
  // Slope compute walk: one stream per cycle through the registered
  // 3-stage pipeline (quasi-static TSpec inputs), landing in slope_q_r[]
  // -----------------------------------------------------------------------
  logic [IDXW_C-1:0] cidx_r, cidx_q1_r, cidx_q2_r;
  logic [16:0]       frame_bytes_r;
  logic [32:0]       iv_bytes_r;
  logic [48:0]       slope_q_r [N_STREAMS_P];

  always_ff @(posedge clk_i or negedge rst_n) begin : slope_walk
    if (!rst_n) begin
      cidx_r <= '0; cidx_q1_r <= '0; cidx_q2_r <= '0;
      frame_bytes_r <= '0; iv_bytes_r <= '0;
      for (int t = 0; t < N_STREAMS_P; t++) slope_q_r[t] <= '0;
    end else begin
      cidx_r    <= (32'(cidx_r) == N_STREAMS_P-1) ? '0 : cidx_r + 1'b1;
      cidx_q1_r <= cidx_r;
      cidx_q2_r <= cidx_q1_r;
      frame_bytes_r <= 17'(max_frame_i[16*cidx_r +: 16])
                       + 17'(MSRP_FRAME_OVERHEAD_C);
      iv_bytes_r    <= 33'(interval_frames_i[16*cidx_q1_r +: 16])
                       * 33'(frame_bytes_r);
      slope_q_r[cidx_q2_r] <= 49'(iv_bytes_r) * 49'(CLASS_A_INTERVALS_PS_C * 8);
    end
  end : slope_walk

  // -----------------------------------------------------------------------
  // Admission walk: greedy in index order against the Σ-ceiling; also
  // accumulates the Σ of HELD slopes (the ordering FSM's slope phase)
  // -----------------------------------------------------------------------
  logic [IDXW_C-1:0]     aidx_r;
  logic [48:0]           acc_r, sacc_r;
  logic                  over_acc_r;
  logic [N_STREAMS_P-1:0] wgrant_r, grant_r;
  logic [N_STREAMS_P-1:0] slope_on_r;
  logic [48:0]           slope_hold_r [N_STREAMS_P];

  wire [48:0] cand_w    = acc_r + slope_q_r[aidx_r];
  wire        fit_w     = req_w[aidx_r] && (cand_w <= limit_w);
  wire        refuse_w  = req_w[aidx_r] && !fit_w;
  wire        round_w   = (32'(aidx_r) == N_STREAMS_P-1);
  wire [48:0] sacc_nx_w = sacc_r + (slope_on_r[aidx_r]
                                    ? slope_hold_r[aidx_r] : 49'd0);

  logic [N_STREAMS_P-1:0] wgrant_now_w;
  always_comb begin : grant_merge
    wgrant_now_w = wgrant_r;
    wgrant_now_w[aidx_r] = fit_w;
  end : grant_merge

  always_ff @(posedge clk_i or negedge rst_n) begin : admission_walk
    if (!rst_n) begin
      aidx_r <= '0; acc_r <= '0; sacc_r <= '0; over_acc_r <= 1'b0;
      wgrant_r <= '0; grant_r <= '0;
      idle_slope_o <= '0; over_limit_o <= 1'b0;
    end else begin
      if (round_w) begin
        grant_r      <= wgrant_now_w;
        over_limit_o <= over_acc_r | refuse_w;
        idle_slope_o <= 32'(sacc_nx_w);
        aidx_r <= '0; acc_r <= '0; sacc_r <= '0; over_acc_r <= 1'b0;
        wgrant_r <= '0;
      end else begin
        wgrant_r   <= wgrant_now_w;
        acc_r      <= fit_w ? cand_w : acc_r;
        sacc_r     <= sacc_nx_w;
        over_acc_r <= over_acc_r | refuse_w;
        aidx_r     <= aidx_r + 1'b1;
      end
    end
  end : admission_walk

  //! reservation ACTIVE per stream (granted last round AND still requested
  //! - the live AND keeps teardown instantaneous)
  wire [N_STREAMS_P-1:0] active_w = grant_r & req_w;
  assign res_active_o = active_w;

  // -----------------------------------------------------------------------
  // Per-stream gate/slope ordering FSM (the flat gate's exact sequence)
  // -----------------------------------------------------------------------
  localparam int unsigned HOLD_W_C = $clog2(HOLD_CYCLES_C + 1);
  logic [HOLD_W_C-1:0] hold_r [N_STREAMS_P];

  always_ff @(posedge clk_i or negedge rst_n) begin : gate_order
    if (!rst_n) begin
      stream_gate_o <= '0;
      slope_on_r    <= '0;
      slope_en_o    <= 1'b0;
      for (int t = 0; t < N_STREAMS_P; t++) begin
        hold_r[t]       <= '0;
        slope_hold_r[t] <= '0;
      end
    end else begin
      for (int t = 0; t < N_STREAMS_P; t++) begin
        if (active_w[t]) begin
          // activation: slope joins Σ first, gate opens after the hold
          slope_on_r[t] <= 1'b1;
          if (!slope_on_r[t]) begin
            slope_hold_r[t] <= slope_q_r[t];   //! latch the granted slope
            hold_r[t]       <= HOLD_W_C'(HOLD_CYCLES_C);
          end else if (hold_r[t] != '0) begin
            hold_r[t] <= hold_r[t] - 1'b1;
          end else begin
            stream_gate_o[t] <= 1'b1;
          end
        end else begin
          // teardown: gate first, slope leaves Σ after the hold
          stream_gate_o[t] <= 1'b0;
          if (stream_gate_o[t]) begin
            hold_r[t] <= HOLD_W_C'(HOLD_CYCLES_C);
          end else if (hold_r[t] != '0) begin
            hold_r[t] <= hold_r[t] - 1'b1;
          end else begin
            slope_on_r[t] <= 1'b0;
          end
        end
      end
      slope_en_o <= |slope_on_r;
    end
  end : gate_order

endmodule

`default_nettype wire

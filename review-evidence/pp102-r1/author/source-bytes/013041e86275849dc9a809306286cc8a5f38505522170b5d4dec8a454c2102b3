/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_admission.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §6.3 Σ-slope admission,
//                 02 §4.1 srp contract + F02.10 granted_slope_bps[src] /
//                 sr_admitted[src], 802.1Q §34.6.1.1 per-stream idleSlope)
//
//  Description : Per-source Σ-slope admission for the SRP engine's talker
//                plane. Each requesting source carries the TSpec captured
//                at its DECLARE_TALKER (MaxFrameSize, MaxIntervalFrames —
//                the talker declare face of 02 §4.1); its class-A idleSlope
//                follows the Milan v1.2 §4.3.3.2 four-step recipe exactly
//                as the silicon-measured reference (KL_lwsrp_bw_gate):
//
//                  1) F = MaxFrameSize + 22  (L2 header incl. VLAN tag, FCS)
//                  2) if F < 68 then F = 68  (a tagged minimum-size frame —
//                     dropping this step under-reserves every small stream;
//                     the reference measured CRF at 5376 kbps against the
//                     mandated 5632 without it)
//                  3) W = F + 20             (preamble 8 + inter-packet gap 12)
//                  4) slope_bps = W x MaxIntervalFrames x 8000 x 8
//
//                Admission is GREEDY IN STREAM-INDEX ORDER against the 75 %
//                port-rate ceiling (802.1Q §34.3.1 default deltaBandwidth):
//                a source is admitted iff the running Σ including it stays
//                <= the ceiling; a refused source never displaces a
//                lower-indexed grant, and the walk re-runs every round so a
//                refused source is admitted the moment capacity frees.
//                Published per F02.10: granted_slope_bps[src] (the granted
//                idleSlope while sr_admitted[src] = 1, else 0),
//                sr_admitted[src], the Σ of granted slopes and an
//                over_limit view (some requested source stands refused).
//
//  Decision    : the one decision that matters — slopes are carried in
//                SATURATING 32-bit form (the F02.10 field width), never the
//                exact 48-bit product: every slope that can ever be GRANTED
//                is <= the ceiling (75 % of a 32-bit port rate), so an
//                exact slope above 2^32-1 saturates to 32'hFFFF_FFFF and
//                draws the SAME refusal verdict while granted arithmetic
//                stays bit-exact. The engine shape is the reference's
//                sequential walk — one source through the 3-stage slope
//                pipeline per cycle, one admission decision per cycle —
//                never a parallel wide adder tree.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_admission #(
    //! stream sources M = P-N-STREAM-OUT
    parameter int unsigned N_SOURCES_P = 8,
    //! derived source-index width — do not override
    localparam int unsigned SRC_W_C = (N_SOURCES_P > 1) ? $clog2(N_SOURCES_P)
                                                        : 1
) (
    input  wire                           clk_i,        //! core clock (P-CLK-HZ domain)
    input  wire                           rst_n,        //! synchronous active-low reset

    input  wire  [N_SOURCES_P-1:0]        req_i,        //! per-source reservation request level (declaration standing)
    input  wire  [N_SOURCES_P-1:0][15:0]  max_frame_i,  //! per-source TSpec MaxFrameSize (talker declare face)
    input  wire  [N_SOURCES_P-1:0][15:0]  interval_frames_i, //! per-source TSpec MaxIntervalFrames (talker declare face)
    input  wire  [31:0]                   port_rate_bps_i,   //! port rate in bps (quasi-static; 1G = 1_000_000_000)

    output logic [N_SOURCES_P-1:0]        sr_admitted_o,       //! F02.10: admitted against the Σ-slope ceiling (live-AND with req)
    output logic [N_SOURCES_P-1:0][31:0]  granted_slope_bps_o, //! F02.10: granted idleSlope while admitted, else 0
    output logic [31:0]                   sum_slope_bps_o,     //! Σ of granted slopes, bps (round-latched)
    output logic                          over_limit_o,        //! some requested source refused by the ceiling (round-latched)
    output logic                          round_done_o         //! one-cycle strobe: an admission round latched its verdicts
);

  // ---- Milan v1.2 §4.3.3.2 constants (reference-matched) -----------------
  localparam logic [16:0] L2_OVERHEAD_C   = 17'd22;  // header + VLAN tag + FCS
  localparam logic [16:0] MIN_L2_BYTES_C  = 17'd68;  // tagged minimum-size frame
  localparam logic [16:0] WIRE_OVERHEAD_C = 17'd20;  // preamble + IPG
  //! class-A intervals/s x 8 bits/byte = the bps-per-interval-byte factor
  localparam logic [32:0] BPS_PER_IVB_C   = 33'd64000;
  //! largest interval-bytes value whose exact slope fits 32 bits:
  //! (2^32 - 1) / 64000 — beyond it the exact slope exceeds every 32-bit
  //! ceiling, so the saturated carrier draws the identical refusal verdict
  localparam logic [32:0] IV_MAX_C        = 33'd67108;
  localparam logic [31:0] SLOPE_SAT_C     = 32'hFFFF_FFFF;

  //! 75 % of the port rate: rate/2 + rate/4 (exact when rate % 4 == 0 —
  //! true of every Ethernet rate; 1G -> 750_000_000, 100M -> 75_000_000)
  logic [31:0] limit_w;
  assign limit_w = (port_rate_bps_i >> 1) + (port_rate_bps_i >> 2);

  // ------------------------------------------------------------------------
  // Slope walk: one source per cycle through the registered 3-stage
  // pipeline (quasi-static TSpec inputs), landing in slope_q_r[src]
  // ------------------------------------------------------------------------
  logic [SRC_W_C-1:0]          cidx_r;
  logic [SRC_W_C-1:0]          cidx_q1_r;
  logic [SRC_W_C-1:0]          cidx_q2_r;
  logic [16:0]                 frame_bytes_r;   // W = clamped F + wire overhead
  logic [32:0]                 iv_bytes_r;      // W x MaxIntervalFrames
  logic [N_SOURCES_P-1:0][31:0] slope_q_r;

  logic [16:0] f_raw_w;
  logic [32:0] slope_prod_w;

  assign f_raw_w      = {1'b0, max_frame_i[cidx_r]} + L2_OVERHEAD_C;
  assign slope_prod_w = {16'd0, iv_bytes_r[16:0]} * BPS_PER_IVB_C;

  always_ff @(posedge clk_i) begin : slope_walk
    if (!rst_n) begin
      cidx_r        <= '0;
      cidx_q1_r     <= '0;
      cidx_q2_r     <= '0;
      frame_bytes_r <= '0;
      iv_bytes_r    <= '0;
      slope_q_r     <= '0;
    end else begin
      cidx_r    <= (32'(cidx_r) == N_SOURCES_P - 1) ? '0
                                                    : cidx_r + SRC_W_C'(1);
      cidx_q1_r <= cidx_r;
      cidx_q2_r <= cidx_q1_r;
      // stage 1: F clamped to the tagged minimum, plus the wire overhead
      frame_bytes_r <= ((f_raw_w < MIN_L2_BYTES_C) ? MIN_L2_BYTES_C : f_raw_w)
                       + WIRE_OVERHEAD_C;
      // stage 2: interval bytes (16 b x 17 b -> < 2^33)
      iv_bytes_r    <= {16'd0, interval_frames_i[cidx_q1_r]}
                       * {16'd0, frame_bytes_r};
      // stage 3: saturating 32-bit slope (see banner) — iv <= IV_MAX_C is
      // the exact product (67108 x 64000 < 2^32)
      slope_q_r[cidx_q2_r] <= (iv_bytes_r > IV_MAX_C) ? SLOPE_SAT_C
                                                      : slope_prod_w[31:0];
    end
  end

  // ------------------------------------------------------------------------
  // Admission walk: greedy in index order against the Σ ceiling; verdicts
  // (grant vector, granted slopes, Σ, over_limit) latch at round end
  // ------------------------------------------------------------------------
  logic [SRC_W_C-1:0]           aidx_r;
  logic [31:0]                  acc_r;        // running granted Σ <= ceiling
  logic                         over_acc_r;
  logic [N_SOURCES_P-1:0]       wgrant_r;
  logic [N_SOURCES_P-1:0][31:0] wgslope_r;
  logic [N_SOURCES_P-1:0]       grant_r;
  logic [N_SOURCES_P-1:0][31:0] gslope_r;
  logic [31:0]                  sum_r;
  logic                         over_r;

  logic [32:0] cand_w;
  logic        fit_w;
  logic        refuse_w;
  logic        round_w;

  assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r]};
  assign fit_w    = req_i[aidx_r] && (cand_w <= {1'b0, limit_w});
  assign refuse_w = req_i[aidx_r] && !fit_w;
  assign round_w  = (32'(aidx_r) == N_SOURCES_P - 1);

  logic [N_SOURCES_P-1:0]       wgrant_now_w;
  logic [N_SOURCES_P-1:0][31:0] wgslope_now_w;

  always_comb begin : grant_merge
    wgrant_now_w           = wgrant_r;
    wgslope_now_w          = wgslope_r;
    wgrant_now_w[aidx_r]   = fit_w;
    wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[aidx_r] : 32'd0;
  end

  always_ff @(posedge clk_i) begin : admission_walk
    if (!rst_n) begin
      aidx_r       <= '0;
      acc_r        <= 32'd0;
      over_acc_r   <= 1'b0;
      wgrant_r     <= '0;
      wgslope_r    <= '0;
      grant_r      <= '0;
      gslope_r     <= '0;
      sum_r        <= 32'd0;
      over_r       <= 1'b0;
      round_done_o <= 1'b0;
    end else begin
      round_done_o <= 1'b0;
      if (round_w) begin
        grant_r      <= wgrant_now_w;
        gslope_r     <= wgslope_now_w;
        // a FIT candidate sum is <= the ceiling < 2^32: the slice is exact
        sum_r        <= fit_w ? cand_w[31:0] : acc_r;
        over_r       <= over_acc_r | refuse_w;
        round_done_o <= 1'b1;
        aidx_r       <= '0;
        acc_r        <= 32'd0;
        over_acc_r   <= 1'b0;
        wgrant_r     <= '0;
        wgslope_r    <= '0;
      end else begin
        wgrant_r   <= wgrant_now_w;
        wgslope_r  <= wgslope_now_w;
        acc_r      <= fit_w ? cand_w[31:0] : acc_r;
        over_acc_r <= over_acc_r | refuse_w;
        aidx_r     <= aidx_r + SRC_W_C'(1);
      end
    end
  end

  // -------------------------------------------------------------- outputs
  // the live AND with req keeps teardown instantaneous (reference rule);
  // granted_slope is 0 whenever not admitted (F02.10 sample rule)
  always_comb begin : publish
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      sr_admitted_o[s]       = grant_r[s] && req_i[s];
      granted_slope_bps_o[s] = (grant_r[s] && req_i[s]) ? gslope_r[s] : 32'd0;
    end
  end

  assign sum_slope_bps_o = sum_r;
  assign over_limit_o    = over_r;

endmodule : KL_srp_admission
`default_nettype wire

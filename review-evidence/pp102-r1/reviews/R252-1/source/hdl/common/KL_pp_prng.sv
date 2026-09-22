/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_prng.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/08 §3)
//
//  Description : The PRNG of F08.2 — one 64-bit maximal-length Galois LFSR
//                feeding every randomized T-ID draw of F08.1:
//
//                  kind 0 : 0..1000  ms  T-ACMP-DELAY        (Milan Table 5.29)
//                  kind 1 : 0..2000  ms  T-ADP-DELAY-START   (Milan §5.6.3.5.2)
//                  kind 2 : 0..4000  ms  T-ADP-DELAY         (Milan §5.6.3.5.3-.7)
//                  kind 3 : 10000..15000 ms  T-MRP-LEAVEALL  (Milan Table 4.3)
//                  kind 4 : 30000..60000 ms  T-NOTIF-MONITOR (Milan §5.4.5.3)
//                  kind 5 : 501..599 ms  MAAP probe_timer    (1722 B.3.4.2:
//                           strictly 500 < T < 600, so both bounds excluded)
//                  kind 6 : 30001..31999 ms  MAAP announce_timer (1722
//                           B.3.4.1: strictly 30 s < T < 32 s)
//                  kind 7 : 0..0xFDFF  MAAP pool offset — NOT milliseconds:
//                           a uniform draw over the whole Table B.9 dynamic
//                           allocation pool (B.3.6.1); the MAAP engine
//                           rejection-retries values past POOL - count so
//                           the block fit keeps the distribution uniform
//
//                Polynomial x^64 + x^63 + x^61 + x^60 + 1 (primitive),
//                right-shift Galois form: period 2^64-1, state never zero.
//                This clears the IEEE 1722.1-2021 §6.2.4.2.2 sequence-length
//                floor by 32 binary orders of magnitude — the reference
//                platform's 16-bit LFSR (period 65535) does not clear it at
//                all. The LFSR advances EVERY cycle (free-running) by 16
//                elementary steps — decimation by 16, itself maximal because
//                gcd(16, 2^64-1) = 1 — so the 16-bit draw window holds
//                entirely fresh bits each cycle. A 1-step advance leaves 15
//                of the 16 window bits shared between consecutive rejection
//                retries (next attempt = rejected value >> 1), which
//                measurably biases accepted-after-reject draws toward the
//                upper-middle of the span (measured: mean 12854 ms on the
//                10000..15000 range). F08.2's unbiasedness claim requires
//                the fresh-window advance.
//
//                Seed = entity_id_i XOR the free-running cycle counter,
//                latched at the FIRST link_up_i rise only. The one design
//                decision that matters: the seed latches ONCE. Re-seeding on
//                later rises would hand every device on a segment a fresh,
//                link-event-synchronized sequence — but the anti-storm draws
//                (T-ADP-DELAY, T-ACMP-DELAY) exist precisely to spread
//                devices apart after such shared events. Reproducibility
//                across link flaps is the failure mode; divergence between
//                devices is the requirement. Only reset clears the latch.
//
//                Range reduction is by REJECTION SAMPLING: mask the low LFSR
//                bits to the next power of two above the span, accept iff
//                the masked value is inside the span (both endpoints
//                inclusive), else retry next cycle on a fresh state; offset
//                ranges draw the span and add the base. A modulo draw is
//                biased toward low values; a raw mask overshoots the range.
//                Both defects are excluded here by construction.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_prng (
    input  wire         clk_i,        //! core clock (P-CLK-HZ)
    input  wire         rst_n,        //! synchronous active-low reset

    input  wire  [63:0] entity_id_i,  //! own entity_id — one half of the seed
    input  wire         link_up_i,    //! link status; the FIRST rise latches the seed

    input  wire         draw_req_i,   //! one-cycle draw request (ignored while draw_busy_o)
    input  wire   [2:0] draw_kind_i,  //! F08.2 range select 0..7 (all codes assigned)
    output logic        draw_busy_o,  //! draw in progress (high while rejection retries run)
    output logic        draw_valid_o, //! one-cycle strobe: draw_ms_o holds the result
    output logic [15:0] draw_ms_o,    //! drawn value: ms for kinds 0..6, a pool offset for kind 7

    output logic [63:0] dbg_lfsr_o,   //! raw LFSR state — observability for the TB stream check
    output logic        dbg_seeded_o  //! seed latched (first link-up rise consumed)
);

  //! x^64 + x^63 + x^61 + x^60 + 1 (primitive), right-shift Galois feedback mask
  localparam logic [63:0] POLY_C    = 64'hD800_0000_0000_0000;
  //! pre-seed state and zero-seed substitute — any nonzero value keeps the
  //! never-zero invariant; draws before link-up run on this deterministic
  //! stream (no randomized protocol timer is armed before link-up)
  localparam logic [63:0] NONZERO_C = 64'h0000_0000_0000_0001;

  // ------------------------------------------------------------ LFSR core
  logic [63:0] lfsr_r;
  logic [63:0] ctr_r;         // free-running cycle counter — seed entropy
  logic        seeded_r;
  logic        link_up_q_r;

  logic [63:0] lfsr_next_w;
  logic [63:0] seed_w;
  logic        link_rise_w;

  //! one elementary Galois step (right-shift form)
  function automatic logic [63:0] lfsr_step_f(input logic [63:0] s);
    return (s >> 1) ^ (s[0] ? POLY_C : 64'h0);
  endfunction

  //! per-cycle advance = 16 elementary steps (STEPS_C): the low 16 bits seen
  //! by the draw window are completely replaced every cycle, so rejection
  //! retries and back-to-back draws are decorrelated (see banner)
  localparam int unsigned STEPS_C = 16;

  always_comb begin : advance_16
    logic [63:0] s;
    s = lfsr_r;
    for (int unsigned i = 0; i < STEPS_C; i++) begin
      s = lfsr_step_f(s);
    end
    lfsr_next_w = s;
  end

  assign link_rise_w = link_up_i && !link_up_q_r;
  assign seed_w      = entity_id_i ^ ctr_r;

  always_ff @(posedge clk_i) begin : seed_and_advance
    if (!rst_n) begin
      lfsr_r      <= NONZERO_C;
      ctr_r       <= 64'd0;
      seeded_r    <= 1'b0;
      link_up_q_r <= 1'b0;
    end else begin
      ctr_r       <= ctr_r + 64'd1;
      link_up_q_r <= link_up_i;
      if (link_rise_w && !seeded_r) begin
        // first link-up rise only; a seed of exactly zero would freeze a
        // Galois LFSR forever, so substitute a nonzero constant
        lfsr_r   <= (seed_w == 64'd0) ? NONZERO_C : seed_w;
        seeded_r <= 1'b1;
      end else begin
        lfsr_r   <= lfsr_next_w;  // free-running: advances every cycle
      end
    end
  end

  // ------------------------------------------------------------ range draw
  // Per-kind {mask, span limit, base}: mask = next power of two above the
  // span, inclusive limit = span width - 1 in values (both endpoints of the
  // F08.1 range are reachable), base added after acceptance.
  logic  [2:0] kind_r;
  logic        busy_r;
  logic [15:0] mask_w;
  logic [15:0] limit_w;
  logic [15:0] base_w;
  logic [15:0] span_w;
  logic        accept_w;

  always_comb begin : kind_decode
    unique case (kind_r)
      3'd0:    begin mask_w = 16'h03FF; limit_w = 16'd1000;  base_w = 16'd0;     end // T-ACMP-DELAY
      3'd1:    begin mask_w = 16'h07FF; limit_w = 16'd2000;  base_w = 16'd0;     end // T-ADP-DELAY-START
      3'd2:    begin mask_w = 16'h0FFF; limit_w = 16'd4000;  base_w = 16'd0;     end // T-ADP-DELAY
      3'd3:    begin mask_w = 16'h1FFF; limit_w = 16'd5000;  base_w = 16'd10000; end // T-MRP-LEAVEALL
      3'd4:    begin mask_w = 16'h7FFF; limit_w = 16'd30000; base_w = 16'd30000; end // T-NOTIF-MONITOR
      3'd5:    begin mask_w = 16'h007F; limit_w = 16'd98;    base_w = 16'd501;   end // MAAP probe_timer
      3'd6:    begin mask_w = 16'h07FF; limit_w = 16'd1998;  base_w = 16'd30001; end // MAAP announce_timer
      default: begin mask_w = 16'hFFFF; limit_w = 16'hFDFF;  base_w = 16'd0;     end // 7: MAAP pool offset
    endcase
  end

  assign span_w   = lfsr_r[15:0] & mask_w;
  assign accept_w = (span_w <= limit_w);  // inclusive: both endpoints drawable

  always_ff @(posedge clk_i) begin : draw_sm
    if (!rst_n) begin
      busy_r       <= 1'b0;
      kind_r       <= 3'd0;
      draw_valid_o <= 1'b0;
      draw_ms_o    <= 16'd0;
    end else begin
      draw_valid_o <= 1'b0;
      if (!busy_r) begin
        if (draw_req_i) begin
          kind_r <= draw_kind_i;
          busy_r <= 1'b1;
        end
      end else if (accept_w) begin
        draw_ms_o    <= span_w + base_w;
        draw_valid_o <= 1'b1;
        busy_r       <= 1'b0;
      end
      // else: rejected — the LFSR advanced anyway; retry on the fresh state
    end
  end

  assign draw_busy_o  = busy_r;
  assign dbg_lfsr_o   = lfsr_r;
  assign dbg_seeded_o = seeded_r;

endmodule

`default_nettype wire

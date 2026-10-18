/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_event_router.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03 §2
//                F03.1 "Event router" row + 03 §5; class-C event semantics
//                of 02 §5 / F02.6)
//
//  Description : Sticky-event fan-in/fan-out. N_SRC_P producers (the 02 §5
//                catalog rows: adapter events + the 08 §5 timer expiry bus,
//                whose one-owner-tag-per-cycle shape maps directly onto one
//                strobe+payload source) each raise a one-cycle strobe with
//                a PAYLOAD_W_P argument. Per source, one sticky latch holds
//                the event WITH ITS FIRST payload until the consumer acks
//                it (F02.6: "evt holds with its arg until evt_ack"). A
//                registered round-robin scan presents one event at a time
//                on evt_valid_o/evt_src_o/evt_payload_o — held stable until
//                evt_ack_i — and under back-to-back acks drains one event
//                per cycle with the scan base advancing past the delivered
//                source, so no source starves.
//
//                Coalescing (02 §5): a source strobing again while its
//                latch is still un-acked sets the per-source coalesced flag
//                (presented as evt_lost_o with the event) and ticks that
//                source's 8-bit SATURATING lost counter, readable on a thin
//                mux (lost_src_i -> lost_count_o). A strobe landing on the
//                same cycle its event is acked is a NEW event: the old one
//                was delivered, the new payload latches, nothing is lost
//                and nothing ticks. Every strobe is therefore exactly one
//                of {new pending event, lost tick} — an event is NEVER
//                silently dropped without the counter ticking (a counter
//                pegged at 0xFF means ">= 255 coalesced", the documented
//                saturation semantic; V8: never fatal).
//
//                The one design decision that matters: the per-source
//                payload/lost state is FLOPS, deliberately not a RAM — all
//                N_SRC_P sources may strobe in the SAME cycle, so no RAM
//                port count covers the writes. This is not the flop-mirror
//                anti-pattern: there is no RAM being mirrored, and every
//                read side (the presented payload and the lost read port)
//                is a thin mux over this one copy of the state, never a
//                second register file.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_event_router #(
    //! event sources fanned in (02 §5 catalog; F01.5 shape default 16)
    parameter int unsigned N_SRC_P = 16,
    //! event argument width — the F02.6 evt_arg lane
    parameter int unsigned PAYLOAD_W_P = 16,
    //! derived source-index width — do not override
    localparam int unsigned SRC_W_C = (N_SRC_P > 32'd1) ? $clog2(N_SRC_P)
                                                        : 32'd1
) (
    input  wire                                 clk_i,         //! core clock (P-CLK-HZ domain)
    input  wire                                 rst_n,         //! synchronous active-low reset

    //! ---- producer side: one-cycle strobes + payloads ----
    input  wire [N_SRC_P-1:0]                   src_strobe_i,  //! per-source one-cycle event strobe
    input  wire [N_SRC_P-1:0][PAYLOAD_W_P-1:0]  src_payload_i, //! per-source argument, valid with the strobe

    //! ---- consumer side: one event at a time, sticky until acked ----
    output logic                                evt_valid_o,   //! an event is presented
    output logic [SRC_W_C-1:0]                  evt_src_o,     //! its source (stable until ack)
    output logic [PAYLOAD_W_P-1:0]              evt_payload_o, //! its FIRST payload (stable until ack)
    output logic                                evt_lost_o,    //! it coalesced >= 1 re-fires (F02.6 evt_lost)
    input  wire                                 evt_ack_i,     //! consume the presented event (ignored while idle)

    //! ---- lost counter read port (thin mux over the counters) ----
    input  wire  [SRC_W_C-1:0]                  lost_src_i,    //! which source's counter to read
    output logic                          [7:0] lost_count_o   //! its saturating lost count (combinational)
);

  localparam logic [7:0] LOST_MAX_C = 8'hFF;

  // ------------------------------------------------------ per-source state
  logic [N_SRC_P-1:0]     pending_r;                 // latched, un-acked
  logic [N_SRC_P-1:0]     coalesced_r;               // re-fired while pending
  logic [PAYLOAD_W_P-1:0] payload_r  [0:N_SRC_P-1];  // FIRST payload of the event
  logic             [7:0] lost_cnt_r [0:N_SRC_P-1];  // saturating re-fire count

  // ------------------------------------------------- presentation register
  logic                valid_r;  // an event is presented
  logic [SRC_W_C-1:0]  sel_r;    // which source is presented
  logic [SRC_W_C-1:0]  ptr_r;    // round-robin base for the idle-load scan

  logic deliver_w;
  assign deliver_w = valid_r && evt_ack_i;

  logic [N_SRC_P-1:0] delivered_w;
  always_comb begin : delivered_vec
    delivered_w = '0;
    if (deliver_w) delivered_w[sel_r] = 1'b1;
  end

  // wrap-safe increment (N_SRC_P need not be a power of two)
  function automatic logic [SRC_W_C-1:0] rr_next(input logic [SRC_W_C-1:0] s);
    return (s == SRC_W_C'(N_SRC_P - 32'd1)) ? '0 : (s + SRC_W_C'(1));
  endfunction

  // ------------------------------------------------------ round-robin scan
  // Grant from the REGISTERED pending set minus the event delivered this
  // cycle; base = one past the delivered source (or the idle pointer), so
  // consecutive grants rotate and no source starves. A source strobing
  // this very cycle is picked up on a later load — grants never race the
  // producers combinationally.
  logic [N_SRC_P-1:0] pend_after_w;
  always_comb begin : pend_after
    pend_after_w = pending_r;
    if (deliver_w) pend_after_w[sel_r] = 1'b0;
  end

  logic [SRC_W_C-1:0] base_w;
  assign base_w = deliver_w ? rr_next(sel_r) : ptr_r;

  logic               gnt_found_w;
  logic [SRC_W_C-1:0] gnt_src_w;

  always_comb begin : rr_scan
    gnt_found_w = 1'b0;
    gnt_src_w   = '0;
    for (int unsigned k = 0; k < N_SRC_P; k++) begin
      int unsigned idx;
      idx = 32'(base_w) + k;
      if (idx >= N_SRC_P) idx = idx - N_SRC_P;
      if (!gnt_found_w && pend_after_w[idx[SRC_W_C-1:0]]) begin
        gnt_found_w = 1'b1;
        gnt_src_w   = idx[SRC_W_C-1:0];
      end
    end
  end

  // -------------------------------------------------------- state update
  always_ff @(posedge clk_i) begin : evt_state
    if (!rst_n) begin
      pending_r   <= '0;
      coalesced_r <= '0;
      valid_r     <= 1'b0;
      sel_r       <= '0;
      ptr_r       <= '0;
      for (int unsigned s = 0; s < N_SRC_P; s++) begin
        payload_r[s]  <= '0;
        lost_cnt_r[s] <= 8'd0;
      end
    end else begin
      // per-source sticky latch (02 §5)
      for (int unsigned s = 0; s < N_SRC_P; s++) begin
        if (src_strobe_i[s]) begin
          if (!pending_r[s] || delivered_w[s]) begin
            // a NEW event: latch its FIRST payload, fresh coalesce state
            pending_r[s]   <= 1'b1;
            payload_r[s]   <= src_payload_i[s];
            coalesced_r[s] <= 1'b0;
          end else begin
            // re-fire before ack: coalesce + count, payload stays the FIRST
            coalesced_r[s] <= 1'b1;
            if (lost_cnt_r[s] != LOST_MAX_C) begin
              lost_cnt_r[s] <= lost_cnt_r[s] + 8'd1;
            end
          end
        end else if (delivered_w[s]) begin
          pending_r[s]   <= 1'b0;
          coalesced_r[s] <= 1'b0;
        end
      end

      // presentation: load on delivery or from idle; held stable otherwise
      if (deliver_w || !valid_r) begin
        valid_r <= gnt_found_w;
        if (gnt_found_w) sel_r <= gnt_src_w;
      end
      if (deliver_w) ptr_r <= rr_next(sel_r);
    end
  end

  // ------------------------------------------------- outputs (thin muxes)
  assign evt_valid_o   = valid_r;
  assign evt_src_o     = sel_r;
  assign evt_payload_o = payload_r[sel_r];
  assign evt_lost_o    = valid_r && coalesced_r[sel_r];
  assign lost_count_o  = lost_cnt_r[lost_src_i];

endmodule : KL_pp_event_router
`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_mac_rmon_events.sv
  Description : RMON event-pulse synthesiser for the MAC boundary. Turns what
                a soft MAC actually exposes - its frame AXIS handshakes, its
                per-frame "bad frame" flag, and its monotonic FCS / preamble
                error counters - into the `ethernet_events` pulse vector, in
                the datapath's clock domain.

                WHY THIS EXISTS: `ethernet_events` + `event_counter` were
                fully unit-tested, wired into milan_csr, documented at CSR
                0x210..0x230 ... and read ZERO on both boards for months,
                because every SoC integration tied `i_mac_events` to 0 (the
                LiteEth MAC exposes no Forencich-style event pulses, so the
                glue had nothing to hand it). Nothing between the MAC and the
                counter turned MAC facts into pulses. This module is that
                missing piece, and it is deliberately a SEPARATE, testable
                block rather than glue, because glue is exactly what silently
                tied the port off. See docs/limitations/
                RECURRING_DEFECT_PATTERNS.md section 1 (decorative ABI).

                WHAT IS DERIVABLE HERE, AND WHAT IS NOT - the honesty rule:
                a counter that is structurally always zero must not look like
                a counter that is zero because nothing happened. `cap_o` is a
                static per-lane capability mask published to software (CSR
                0x204 STATS_CAP): bit n = 1 means lane n has a real event
                source in THIS build, bit n = 0 means lane n is structurally
                silent and its STAT word is not a measurement. Software that
                reads a 0 count with cap bit 0 must report "not supported",
                never "no errors".

                  lane                   | source                    | cap
                  -----------------------|---------------------------|-----
                  TX_FIFO_GOOD_FRAME     | TX AXIS accepted tlast     | yes
                  RX_FIFO_GOOD_FRAME     | RX AXIS accepted tlast     | yes
                  RX_ERROR_BAD_FCS       | MAC FCS error counter      | opt
                  RX_ERROR_BAD_FRAME     | MAC preamble/align counter | opt
                  RX_FIFO_BAD_FRAME      | RX frame with err flag set | opt
                  TX_ERROR_UNDERFLOW     | -- MAC-internal, unexposed | no
                  TX_FIFO_OVERFLOW       | -- MAC-internal, unexposed | no
                  TX_FIFO_BAD_FRAME      | -- MAC-internal, unexposed | no
                  RX_FIFO_OVERFLOW       | -- MAC-internal, unexposed | no

                The four unexposed lanes are NOT faked from backpressure at
                the AXIS boundary: `rx_tvalid & ~rx_tready` is the datapath
                stalling the MAC, which is the PRECURSOR to an RX FIFO
                overflow, not an overflow - counting it as one would trade a
                lying zero for a lying count. They stay 0 with cap 0.

                CLOCKING: the MAC boundary lives in the SoC's MAC clock
                domain, the counters in the datapath's. Every derived pulse
                crosses on its own `cdc_pulse` toggle synchroniser, which
                requires source pulses spaced wider than the round-trip
                (~4 destination cycles). All events here are per-FRAME, and
                the shortest legal frame plus its inter-frame gap is >= 10
                beats on a 64-bit boundary, so the constraint holds by
                construction; a MAC narrower than 64 bits only widens it.

  Notes       :
    - `attached_i` is the structural "a real MAC drives this boundary" input.
      A CSR-only / stub elaboration ties it 0: every event is then masked AND
      `cap_o` reads 0, so software sees "no MAC, lanes not supported" rather
      than nine zeros that look like a clean link.
    - The two error-counter inputs are monotonic free-running counts (that is
      what LiteEth publishes). An increment becomes one pulse; a counter that
      RESETS to zero (MAC reinit) emits nothing, so a link-guard episode does
      not manufacture a phantom error.
------------------------------------------------------------------------------
*/

//! Derive the `ethernet_events` pulse vector from a soft MAC's boundary
//! signals, and publish which lanes are real.
//!
//! **Key Features**
//! - Per-frame event derivation at the MAC AXIS boundary (no per-beat noise).
//! - Static capability mask so structurally-zero lanes are self-declaring.
//! - Dual-clock: derivation in the MAC domain, pulses handed to the counter
//!   block in the datapath domain via `cdc_pulse`.

`default_nettype none

`include "ethernet_events.svh"

module KL_mac_rmon_events #(
  //! MAC checks FCS and publishes a monotonic error count (`fcs_err_cnt_i`)
  parameter bit HAS_FCS_CHECK_P   = 1'b1,
  //! MAC checks the preamble/alignment and publishes `align_err_cnt_i`
  parameter bit HAS_ALIGN_CHECK_P = 1'b1,
  //! MAC flags a delivered frame as bad on its last beat (`mac_rx_err_i`)
  parameter bit HAS_RX_ERR_FLAG_P = 1'b1
)(
  // ---- MAC-side domain (the SoC's MAC clock; LiteEth `macsys`) ----
  input  wire        mac_clk_i,        //! MAC-boundary clock
  input  wire        mac_rst_n,        //! synchronous active-low reset, `mac_clk_i`
  //! 1 = a real MAC drives this boundary; 0 = stub/CSR-only elaboration
  input  wire        attached_i,
  //! MAC-bound TX AXIS handshake (datapath -> MAC), `mac_clk_i`
  input  wire        mac_tx_tvalid_i,
  input  wire        mac_tx_tready_i,
  input  wire        mac_tx_tlast_i,
  //! MAC-sourced RX AXIS handshake (MAC -> datapath), `mac_clk_i`
  input  wire        mac_rx_tvalid_i,
  input  wire        mac_rx_tready_i,
  input  wire        mac_rx_tlast_i,
  //! MAC's per-frame bad-frame flag, valid on the accepted RX last beat
  //! (LiteEth: FCS failure OR undersize/runt, carried on the `error` field)
  input  wire        mac_rx_err_i,
  //! monotonic MAC FCS-error count (LiteEth `crc_errors`)
  input  wire [31:0] fcs_err_cnt_i,
  //! monotonic MAC preamble/alignment-error count (LiteEth `preamble_errors`)
  input  wire [31:0] align_err_cnt_i,

  // ---- datapath-side domain (`ethernet_events` clock) ----
  input  wire        dp_clk_i,         //! datapath clock (axis_clk)
  input  wire        dp_rst_n,         //! synchronous active-low reset, `dp_clk_i`
  //! event pulses, lane index == `ethernet_events_t`, one cycle in `dp_clk_i`
  output wire [_ETH_EVENT_COUNTER-1:0] events_o,
  //! static capability mask: bit n = 1 => lane n has a real source in this
  //! build; 0 => structurally silent (CSR 0x204 STATS_CAP publishes it)
  output wire [_ETH_EVENT_COUNTER-1:0] cap_o
);

  // ==========================================================================
  //  Capability mask (static; the honesty contract for the zero lanes)
  // ==========================================================================
  localparam int NEV_C = _ETH_EVENT_COUNTER;   //! lane count (ABI: enum order)
  //! Typed localparam: the 32-bit shift expression truncates to NEV_C bits on
  //! assignment, so no size cast on an enum name is needed (sv2v-portable).
  localparam logic [NEV_C-1:0] CAP_SUPPORTED_C =
      (1 << TX_FIFO_GOOD_FRAME)
    | (1 << RX_FIFO_GOOD_FRAME)
    | (HAS_FCS_CHECK_P   ? (1 << RX_ERROR_BAD_FCS)   : 0)
    | (HAS_ALIGN_CHECK_P ? (1 << RX_ERROR_BAD_FRAME) : 0)
    | (HAS_RX_ERR_FLAG_P ? (1 << RX_FIFO_BAD_FRAME)  : 0);

  assign cap_o = attached_i ? CAP_SUPPORTED_C : '0;

  // ==========================================================================
  //  MAC-domain derivation (per FRAME, never per beat)
  // ==========================================================================
  //! one accepted `tlast` beat == one frame handed to the MAC
  wire tx_eof_w = mac_tx_tvalid_i & mac_tx_tready_i & mac_tx_tlast_i;
  //! one accepted `tlast` beat == one frame handed up by the MAC
  wire rx_eof_w = mac_rx_tvalid_i & mac_rx_tready_i & mac_rx_tlast_i;
  //! the MAC's own verdict on that frame, sampled where it is valid
  wire rx_bad_w = rx_eof_w &  mac_rx_err_i & HAS_RX_ERR_FLAG_P;
  //! a frame the MAC did NOT flag. When the MAC exposes no flag the whole
  //! delivered population is reported good - that is what the flag-less
  //! integration can honestly say (and `cap_o` marks BAD_FRAME unsupported).
  wire rx_good_w = rx_eof_w & ~rx_bad_w;

  //! Monotonic MAC error counters -> one pulse per increment. A DECREASE (the
  //! counter reset by a MAC reinit) deliberately emits nothing: a link-guard
  //! episode must not manufacture an error event.
  logic [31:0] fcs_cnt_r, align_cnt_r;
  logic        fcs_evt_r, align_evt_r;
  always_ff @(posedge mac_clk_i) begin : mac_err_delta
    if (!mac_rst_n) begin
      fcs_cnt_r   <= 32'd0;
      align_cnt_r <= 32'd0;
      fcs_evt_r   <= 1'b0;
      align_evt_r <= 1'b0;
    end
    else begin
      fcs_cnt_r   <= fcs_err_cnt_i;
      align_cnt_r <= align_err_cnt_i;
      fcs_evt_r   <= HAS_FCS_CHECK_P   & attached_i & (fcs_err_cnt_i   > fcs_cnt_r);
      align_evt_r <= HAS_ALIGN_CHECK_P & attached_i & (align_err_cnt_i > align_cnt_r);
    end
  end : mac_err_delta

  //! MAC-domain pulse vector, gated by `attached_i` so a stub can never count
  logic [_ETH_EVENT_COUNTER-1:0] src_evt_w;
  always_comb begin : src_event_map
    src_evt_w                       = '0;
    src_evt_w[TX_FIFO_GOOD_FRAME]   = tx_eof_w  & attached_i;
    src_evt_w[RX_FIFO_GOOD_FRAME]   = rx_good_w & attached_i;
    src_evt_w[RX_FIFO_BAD_FRAME]    = rx_bad_w  & attached_i;
    src_evt_w[RX_ERROR_BAD_FCS]     = fcs_evt_r;
    src_evt_w[RX_ERROR_BAD_FRAME]   = align_evt_r;
    // TX_ERROR_UNDERFLOW / TX_FIFO_OVERFLOW / TX_FIFO_BAD_FRAME /
    // RX_FIFO_OVERFLOW: MAC-internal, not exposed at this boundary. Left 0 on
    // purpose, and declared unsupported through `cap_o` - see the banner.
  end : src_event_map

  // ==========================================================================
  //  MAC domain -> datapath domain (one toggle synchroniser per lane)
  // ==========================================================================
  genvar gi;
  generate
    for (gi = 0; gi < _ETH_EVENT_COUNTER; gi++) begin : gen_evt_cdc
      if (CAP_SUPPORTED_C[gi]) begin : gen_live_lane
        cdc_pulse #(.DEST_SYNC_FF(2)) evt_cdc (
          .src_clk    (mac_clk_i),
          .src_rst_n  (mac_rst_n),
          .src_pulse  (src_evt_w[gi]),
          .dest_clk   (dp_clk_i),
          .dest_rst_n (dp_rst_n),
          .dest_pulse (events_o[gi])
        );
      end
      else begin : gen_dead_lane
        //! structurally unsupported lane: tied 0 HERE, declared 0 in `cap_o`
        assign events_o[gi] = 1'b0;
      end
    end : gen_evt_cdc
  endgenerate

endmodule //! KL_mac_rmon_events

`default_nettype wire

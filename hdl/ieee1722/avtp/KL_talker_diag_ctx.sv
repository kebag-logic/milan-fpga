/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_talker_diag_ctx.sv
  Author      : Kebag Logic

  Date        : 2026-07-28
  Description : Milan v1.2 Table 5.4 diagnostic counters, per Stream Output -
                the talker-side mirror of KL_avtp_rx_monitor_ctx's Table 5.6
                set. "For each Stream Output, the PAAD-AE shall keep track of
                the counters in Table 5.4", and 5.4.2.25 Table 5.17 makes a
                PAAD-AE "implement and return" them per descriptor - which is
                why this is a context block and not one register set: before
                it, GET_COUNTERS served STREAM_OUTPUT.0 a 0x1F mask whose
                TIMESTAMP_UNCERTAIN bytes were constant zero (a claimed-valid
                counter serving a frozen zero - the R5 lie), and every other
                index an empty mask.

                THE TABLE 5.4 SEMANTICS, exactly:

                * STREAM_START / STREAM_STOP count edges of the talker's
                  streaming state. The clause's invariant - START == STOP+1
                  while streaming, START == STOP while not - holds by
                  construction because both count edges of the SAME level.
                  The level is the COMPOSED admission gate (ACMP+lwSRP+MAAP
                  terms), i.e. "is this talker licensed and emitting", not a
                  bare enable bit.
                * MEDIA_RESET / TIMESTAMP_UNCERTAIN / FRAMES_TX are
                  OBSERVATION-INTERVAL counts ("incremented at the end of
                  every observation interval during which ..."), interval
                  <= 1 s, and all three "reset to 0 each time the Talker
                  starts streaming". FRAMES_TX therefore advances at 1/s
                  while streaming - NOT at the frame rate; a controller
                  reading the raw frame total where the clause defines an
                  interval count reads a number 8000x off.
                * TIMESTAMP_UNCERTAIN qualifies tu BY TRANSMISSION: "the tu
                  bit has been set in any of the TRANSMITTED Stream Data
                  AVTPDUs" - a set tu with no PDU sent counts nothing, which
                  is what distinguishes this counter from the free-running
                  CLKV_TUCNT (0x780) interval count.
                * MEDIA_RESET counts intervals in which mr toggled on a
                  transmitted PDU. It is derived HERE from the mr bit the
                  packetizer actually stamped into the PDU that frame_p_i
                  announces (frame_mr_i), compared against the previous
                  transmitted PDU of the SAME context - which is the clause
                  sentence turned into logic, and which is why this counter
                  cannot become a claimed-but-unbacked zero. It used to take
                  an mr_p_i EVENT STROBE, and milan_datapath tied that strobe
                  to 1'b0: mask bit 2 (Table 5.17 value 0x00000004) was
                  claimed over a counter with no source, the exact shape of
                  the RMON tie-off that read zero for months (VERSION 0x0013,
                  the STATS_CAP 0x204 rule). A strobe port invites a tie-off
                  and a tie-off is indistinguishable from silence; a port
                  carrying the WIRE'S OWN BIT cannot lie, because if the wire
                  really always carries mr = 0 then "never toggled" is the
                  true answer and 0 is the counted, correct value.

                THE OBSERVATION-INTERVAL BOUNDARY. An event strobe landing on
                the same cycle as the interval tick is harvested INTO THE
                CLOSING interval (the tick marks the interval's end, so a PDU
                transmitted on it was transmitted during it). Folding it only
                into seen_*_r would lose it outright: the tick's whole-vector
                clear is a later nonblocking assignment than the per-bit fold,
                so it wins, and the strobe is one cycle wide and never comes
                back. That cost nothing for FRAMES_TX at 8 kPDU/s (the closing
                interval holds 7999 other frames) but silently dropped SPARSE
                events - a lone tu-stamped PDU, a single mr toggle - from both
                intervals. Same rule at a start edge: the three counters zero
                per Table 5.4, and this cycle's event survives into the fresh
                interval rather than being erased with them.

                The read side is an indexed combinational port: the AECP
                response builder presents the descriptor_index it is
                serving and latches all five counters in its single
                const-load cycle. Context N_CTX_P-1 may be a CRF Media
                Clock Output - same Table 5.4, same machinery; its frame
                pulse is the CRF PDU strobe.

  Spec refs   : Milan v1.2 5.3.7.10 Table 5.4, 5.4.2.25 Table 5.17
  Company     : Kebag Logic
------------------------------------------------------------------------------
*/

//! Per-talker Milan Table 5.4 counters: START/STOP edges of the composed
//! streaming gate, interval-based MEDIA_RESET / TIMESTAMP_UNCERTAIN /
//! FRAMES_TX with reset-on-start, indexed combinational read port.

`default_nettype none

module KL_talker_diag_ctx #(
  parameter int unsigned N_CTX_P       = 2,           //! stream outputs
                                                      //! (AAF talkers + CRF)
  //! observation interval in clk_i cycles; <= 1 s per the clause. TBs
  //! shrink it so a case sees interval boundaries in simulation time.
  parameter int unsigned TICK_CYC_P    = 100_000_000
)(
  input  wire                clk_i,
  input  wire                rst_n,

  //! composed per-output streaming level (the licence + emission state)
  input  wire [N_CTX_P-1:0]  streaming_i,
  //! one-cycle PDU-emitted strobe + which output it belongs to
  input  wire                frame_p_i,
  input  wire [3:0]          frame_idx_i,
  //! AVTP "tu" level stamped into outgoing PDUs (KL_ptp_clock_validity)
  input  wire                tu_i,
  //! AVTP "mr" bit AS STAMPED into the PDU frame_p_i announces (1722-2016
  //! 4.4.4.3). MEDIA_RESET is derived from a change in THIS bit between
  //! consecutive transmitted PDUs of the same context - see the banner on
  //! why the counter takes the wire's bit and not an event strobe.
  input  wire                frame_mr_i,

  //! indexed read: all five Table 5.4 counters for one Stream Output
  input  wire [3:0]          rd_idx_i,
  output logic [31:0]        rd_start_o,
  output logic [31:0]        rd_stop_o,
  output logic [31:0]        rd_mreset_o,
  output logic [31:0]        rd_tu_o,
  output logic [31:0]        rd_ftx_o,

  //! one-cycle per-context pulse the cycle a Table 5.4 counter is WRITTEN
  //! (START/STOP edge or an interval-close increment) - the Milan 5.4.5
  //! Table 5.22 unsolicited GET_COUNTERS trigger ("sent when one of the
  //! counters is updated"). The 1/s-per-descriptor restriction is the
  //! consumer's (KL_aecp_response_builder rate-limits per index); this
  //! port only states the raw fact. A start edge zeroing the three
  //! interval counters rides the SAME pulse as its START increment.
  output logic [N_CTX_P-1:0] dirty_p_o
);

  if (N_CTX_P < 1 || N_CTX_P > 16)
    $error("KL_talker_diag_ctx: N_CTX_P=%0d outside 1..16 (the 4-bit index feeds).",
           N_CTX_P);

  //! context-index width (N_CTX_P == 1 still needs a 1-bit select)
  localparam int unsigned IXW_C = $clog2(N_CTX_P == 1 ? 2 : N_CTX_P);

  //! observation-interval divider (free-running; the clause fixes only an
  //! upper bound on the interval, not its phase)
  localparam int unsigned TICKW_C = $clog2(TICK_CYC_P);
  logic [TICKW_C-1:0] tick_cnt_r;
  logic               tick_p_r;
  always_ff @(posedge clk_i) begin : diag_tick
    if (!rst_n) begin
      tick_cnt_r <= '0;
      tick_p_r   <= 1'b0;
    end else if (32'(tick_cnt_r) == TICK_CYC_P - 1) begin
      tick_cnt_r <= '0;
      tick_p_r   <= 1'b1;
    end else begin
      tick_cnt_r <= tick_cnt_r + 1'b1;
      tick_p_r   <= 1'b0;
    end
  end : diag_tick

  //! the five counters + the per-interval seen flags
  //! Read/write visibility is verification-only. The NxN integration bench
  //! seeds a different signature in every context, then reads every one back
  //! through the real processor GET_COUNTERS path. That makes an aliased or
  //! clamped index fail even when real talkers happen to share event history.
  logic [31:0] start_r  [N_CTX_P] /* verilator public_flat_rw */;
  logic [31:0] stop_r   [N_CTX_P] /* verilator public_flat_rw */;
  logic [31:0] mreset_r [N_CTX_P] /* verilator public_flat_rw */;
  logic [31:0] tuiv_r   [N_CTX_P] /* verilator public_flat_rw */;
  logic [31:0] ftx_r    [N_CTX_P] /* verilator public_flat_rw */;
  logic [N_CTX_P-1:0] seen_f_r;    //! >=1 PDU transmitted this interval
  //! USER 2026-08-05 FRAMES_TX law (ATDECC quantity, Milan cadence): count
  //! FRAMES, publish coalesced at the interval close - the counter advances
  //! by the interval's frame total, not +1. Saturating 16-bit per context.
  logic [N_CTX_P-1:0] seen_tu_r;   //! ... with tu set
  logic [N_CTX_P-1:0] seen_mr_r;   //! ... with mr toggled
  logic [N_CTX_P-1:0] strm_q_r;    //! streaming level, for the edge
  //! mr of each context's LAST transmitted PDU (1722-2016 4.4.4.3: the bit
  //! "stays at its new value until a new media clock restart is needed", so
  //! the toggle IS the difference between consecutive transmitted PDUs).
  //! Reset 0 = the wire's own reset state, so a first PDU carrying mr = 1
  //! counts - a restart really did happen before it.
  logic [N_CTX_P-1:0] mr_q_r;

  //! this cycle's per-context events, decoded once (the interval close reads
  //! them alongside the seen_* flags so a tick-cycle strobe is not lost)
  logic [N_CTX_P-1:0] ev_f_w, ev_tu_w, ev_mr_w;
  always_comb begin : diag_events
    ev_f_w  = '0;
    ev_tu_w = '0;
    ev_mr_w = '0;
    if (frame_p_i && (32'(frame_idx_i) < N_CTX_P)) begin
      ev_f_w[frame_idx_i[IXW_C-1:0]] = 1'b1;
      if (tu_i)
        ev_tu_w[frame_idx_i[IXW_C-1:0]] = 1'b1;
      if (frame_mr_i != mr_q_r[frame_idx_i[IXW_C-1:0]])
        ev_mr_w[frame_idx_i[IXW_C-1:0]] = 1'b1;
    end
  end : diag_events

  always_ff @(posedge clk_i) begin : diag_track
    if (!rst_n) begin
      for (int c = 0; c < N_CTX_P; c++) begin
        start_r[c]  <= '0;
        stop_r[c]   <= '0;
        mreset_r[c] <= '0;
        tuiv_r[c]   <= '0;
        ftx_r[c]    <= '0;
      end
      seen_f_r  <= '0;
      seen_tu_r <= '0;
      seen_mr_r <= '0;
      strm_q_r  <= '0;
      mr_q_r    <= '0;
      dirty_p_o <= '0;
    end else begin
      dirty_p_o <= '0;
      //! PDU events fold into the current interval's flags
      seen_f_r  <= seen_f_r  | ev_f_w;
      for (int c = 0; c < N_CTX_P; c++)
      seen_tu_r <= seen_tu_r | ev_tu_w;
      seen_mr_r <= seen_mr_r | ev_mr_w;
      //! remember the mr this context just put on the wire
      if (frame_p_i && (32'(frame_idx_i) < N_CTX_P))
        mr_q_r[frame_idx_i[IXW_C-1:0]] <= frame_mr_i;

      //! interval close: harvest the flags AND this cycle's events - a strobe
      //! on the tick cycle belongs to the interval the tick is closing, and
      //! folding it only above would lose it (the clear below is the later
      //! nonblocking assignment, and the strobe never returns)
      if (tick_p_r) begin
        for (int c = 0; c < N_CTX_P; c++) begin
          if (seen_f_r[c]  | ev_f_w[c]) begin
            //! Table 5.4 interval semantics: +1 PER OBSERVATION INTERVAL
            //! with frames, never the frame total - the header's "8000x
            //! off" note was live on silicon 2026-08-06 (the pushed
            //! counter read 11M raw frames; tkdiag T3 pinned it at desk,
            //! task #21 round)
            ftx_r[c]  <= ftx_r[c] + 32'd1;
          end
          if (seen_tu_r[c] | ev_tu_w[c]) tuiv_r[c]   <= tuiv_r[c] + 32'd1;
          if (seen_mr_r[c] | ev_mr_w[c]) mreset_r[c] <= mreset_r[c] + 32'd1;
          //! Table 5.22 triggers whenever any counter is updated. This raw
          //! source therefore includes FRAMES_TX interval closes as well as
          //! anomaly counters. Per-controller coalescing and the 1/s limit
          //! belong to the notification scheduler, never to this producer.
          if ((seen_f_r[c]  | ev_f_w[c]) |
              (seen_tu_r[c] | ev_tu_w[c]) |
              (seen_mr_r[c] | ev_mr_w[c]))
            dirty_p_o[c] <= 1'b1;
        end
        seen_f_r  <= '0;
        seen_tu_r <= '0;
        seen_mr_r <= '0;
      end

      //! streaming edges: START/STOP count the SAME level so the clause
      //! invariant (START == STOP or STOP+1) holds structurally; a start
      //! zeroes the three interval counters per Table 5.4
      strm_q_r <= streaming_i;
      for (int c = 0; c < N_CTX_P; c++) begin
        if (streaming_i[c] && !strm_q_r[c]) begin : g_start
          start_r[c]  <= start_r[c] + 32'd1;
          mreset_r[c] <= '0;
          tuiv_r[c]   <= '0;
          ftx_r[c]    <= '0;
          //! and the pending flags: a stop->start inside one interval must
          //! not carry the pre-stop activity into the fresh counters - but
          //! THIS cycle's event belongs to the stream that just started, so
          //! it survives the wipe instead of being erased with the history
          seen_f_r[c]  <= ev_f_w[c];
          seen_tu_r[c] <= ev_tu_w[c];
          seen_mr_r[c] <= ev_mr_w[c];
          dirty_p_o[c] <= 1'b1;
        end
        else if (!streaming_i[c] && strm_q_r[c]) begin : g_stop
          stop_r[c]    <= stop_r[c] + 32'd1;
          dirty_p_o[c] <= 1'b1;
        end : g_stop
      end
    end
  end : diag_track

  //! indexed combinational read (out-of-range index reads context 0's
  //! shape of zeros? No - it reads a CLAMPED index; the AECP builder only
  //! presents directory-served indexes, and a clamp can never invent data)
  wire [IXW_C-1:0] ridx_w = (32'(rd_idx_i) < N_CTX_P)
                            ? rd_idx_i[IXW_C-1:0]
                            : '0;
  always_comb begin : diag_read
    rd_start_o  = start_r[ridx_w];
    rd_stop_o   = stop_r[ridx_w];
    rd_mreset_o = mreset_r[ridx_w];
    rd_tu_o     = tuiv_r[ridx_w];
    rd_ftx_o    = ftx_r[ridx_w];
  end : diag_read

endmodule

`default_nettype wire

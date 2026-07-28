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
                  transmitted PDU. This fabric never toggles mr (media-clock
                  discontinuities surface through CLKV + tu), so the counter
                  is validly zero - and it is COUNTED here, not faked, so
                  the day an mr source exists it starts moving with no AECP
                  change.

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
  //! mr-toggled-on-a-transmitted-PDU strobe (none exists in this fabric
  //! today; wired 0 at the instantiation - the counter stays validly zero)
  input  wire                mr_p_i,
  input  wire [3:0]          mr_idx_i,

  //! indexed read: all five Table 5.4 counters for one Stream Output
  input  wire [3:0]          rd_idx_i,
  output logic [31:0]        rd_start_o,
  output logic [31:0]        rd_stop_o,
  output logic [31:0]        rd_mreset_o,
  output logic [31:0]        rd_tu_o,
  output logic [31:0]        rd_ftx_o
);

  if (N_CTX_P < 1 || N_CTX_P > 16)
    $error("KL_talker_diag_ctx: N_CTX_P=%0d outside 1..16 (the 4-bit index feeds).",
           N_CTX_P);

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
  logic [31:0] start_r  [N_CTX_P];
  logic [31:0] stop_r   [N_CTX_P];
  logic [31:0] mreset_r [N_CTX_P];
  logic [31:0] tuiv_r   [N_CTX_P];
  logic [31:0] ftx_r    [N_CTX_P];
  logic [N_CTX_P-1:0] seen_f_r;    //! >=1 PDU transmitted this interval
  logic [N_CTX_P-1:0] seen_tu_r;   //! ... with tu set
  logic [N_CTX_P-1:0] seen_mr_r;   //! ... with mr toggled
  logic [N_CTX_P-1:0] strm_q_r;    //! streaming level, for the edge

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
    end else begin
      //! PDU events fold into the current interval's flags
      if (frame_p_i && (32'(frame_idx_i) < N_CTX_P)) begin
        seen_f_r[frame_idx_i[$clog2(N_CTX_P == 1 ? 2 : N_CTX_P)-1:0]]
            <= 1'b1;
        if (tu_i)
          seen_tu_r[frame_idx_i[$clog2(N_CTX_P == 1 ? 2 : N_CTX_P)-1:0]]
              <= 1'b1;
      end
      if (mr_p_i && (32'(mr_idx_i) < N_CTX_P))
        seen_mr_r[mr_idx_i[$clog2(N_CTX_P == 1 ? 2 : N_CTX_P)-1:0]] <= 1'b1;

      //! interval close: harvest the flags (last-wins over the folds above
      //! is fine - a strobe ON the tick cycle lands in the next interval)
      if (tick_p_r) begin
        for (int c = 0; c < N_CTX_P; c++) begin
          if (seen_f_r[c])  ftx_r[c]    <= ftx_r[c] + 32'd1;
          if (seen_tu_r[c]) tuiv_r[c]   <= tuiv_r[c] + 32'd1;
          if (seen_mr_r[c]) mreset_r[c] <= mreset_r[c] + 32'd1;
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
          //! not carry the pre-stop activity into the fresh counters
          seen_f_r[c]  <= 1'b0;
          seen_tu_r[c] <= 1'b0;
          seen_mr_r[c] <= 1'b0;
        end
        else if (!streaming_i[c] && strm_q_r[c])
          stop_r[c] <= stop_r[c] + 32'd1;
      end
    end
  end : diag_track

  //! indexed combinational read (out-of-range index reads context 0's
  //! shape of zeros? No - it reads a CLAMPED index; the AECP builder only
  //! presents directory-served indexes, and a clamp can never invent data)
  wire [$clog2(N_CTX_P == 1 ? 2 : N_CTX_P)-1:0] ridx_w =
      (32'(rd_idx_i) < N_CTX_P)
      ? rd_idx_i[$clog2(N_CTX_P == 1 ? 2 : N_CTX_P)-1:0]
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

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_render_setpoint.sv
  Author      : Kebag Logic

  Date        : 2026-09-09
  Description : The listener render path's SETPOINT stage (#386, option a):
                a bounded per-stream elastic queue of media EVENTS (one
                sample per wire channel) between the AAF RX depacketizer
                clone and the render crossbar KL_chan_map_render. Its fill
                IS the accept-to-render latency, and it runs at a constant
                SETPOINT derived by the integration from the class-A frame
                shape - the same law KL_i2s_playback applies to the I2S path
                (task #28, VERSION 0x002F), stated here at the crossbar's
                input grid so it is independent of the audio interface.

                PUSH: every accepted clone beat (2 x S32BE samples, wire
                order, tuser = stream, tlast per PDU) is walked by the same
                position counter the crossbar uses (wire channel = position
                mod channels_per_frame, restart at tlast) and each sample is
                written into lane <channel> of the stream's current event
                row; the row is complete when the last channel lands, which
                advances the write pointer (fill + 1). Wire channels beyond
                N_CH_P are walked, never stored (virtual, the crossbar rule).

                POP: on every tick_i (the media grid) one event per stream is
                presented to the crossbar as PAIRS_C beats in the clone
                format, lanes >= the stream's channel count masked to zero
                and tlast on the last beat, streams in index order; then
                render_tick_p_o fires, so the crossbar registers the popped
                events exactly N_STREAMS_P x PAIRS_C + 2 cycles after the
                media tick (its phys_valid_o on that same edge). The
                crossbar's per-stream channel count is therefore the
                lane count an event carries, 2 x PAIRS_C
                (m_wire_chans_o), whatever the wire says: with N_CH_P
                odd the pad lane of the last beat is a channel the
                crossbar walks and never latches, not a wrap onto
                channel 0. THE POP IS EVENT-ATOMIC: whether a stream
                presents an event this tick, and which row it reads,
                are decided ONCE at its first beat from the registered
                pointers (the event is consumed there); the remaining
                beats read that latched row whatever the stream's
                state does meanwhile, so a PDU end, a rail, a recentre
                or a flush inside the pop window lands between events,
                never inside one (the crossbar's single walker would
                otherwise carry a truncated or mixed event into the
                next stream's channels).

                THE LAW (events; T = one media tick):
                  PDU_EVENTS_P    events per accepted PDU (6 at class A, 48k)
                  SETPOINT_EVT_P  the fill just BEFORE every PDU push, and the
                                  delay of that PDU's first event in ticks
                  TARGET_C        = SETPOINT + PDU_EVENTS: the fill right
                                  AFTER the push (a PDU_EVENTS sawtooth)
                  first-event delay = SETPOINT x T + phase, phase in (0, T]:
                  the accept instant is asynchronous to the grid, so the
                  declared jitter band is one media frame and nothing
                  downstream can narrow it. Event k of a PDU renders k ticks
                  later (IEEE 1722-2016 7.3.3 samples per frame).

                PREFILL (power-up, after an underrun, after a flush): pops
                are held until a PDU end finds fill >= TARGET_C, then the
                read pointer snaps to wptr - TARGET_C (the oldest excess
                events are dropped once) and pops start - one bounded gap,
                never a per-tick repeat storm (the KL_i2s_playback rule).

                BANDS, judged at every PDU END so the sawtooth is factored
                out (dev = fill - TARGET_C):
                  |dev| <= CONV_BAND_EVT_P sustained 100 ms -> converged_o
                  dev >  RESET_BAND_EVT_P  -> snap to TARGET_C (rails_o)
                  dev < -RESET_BAND_EVT_P  -> re-enter prefill (rails_o)
                The reset band is one whole PDU by the integration's choice,
                so a PDU one class-A interval late never trips it; only
                drift does (INTERNAL free-run: slips accepted, at a band).

                RECENTRE (task #22 applied to this path): recentre_p_i (the
                integration's set: a GM identity change, a PHC step, a
                clock-source change once its grid settled) arms a pending
                flag; the NEXT PDU end consumes it as the prefill snap (or a
                prefill entry when the queue is short) and counts it ONCE in
                recentres_o. Nothing walks the fill back at a residual rate.
                A stream in prefill ignores the pulse (nothing to recentre).

                UNDERRUN (a tick finds the queue empty): counted once, the
                stream re-enters prefill; the crossbar holds its last event.
                OVERRUN (an event completes at a full queue): the event is
                dropped and counted; the rail snaps at that PDU's end.
                FLUSH (per stream, bind loss): empty, prefill. A wire
                channel count that moves on a running stream flushes it
                the same way: the queued rows carry the old lane layout.

                STORAGE: event rows of N_CH_P lanes kept as PAIR words so a
                pop reads one 48-bit word per beat with no lane mux: h1 for
                the odd lanes, h0e/h0o for the even lanes split by row
                parity. The parity split is what lets a straddling beat of
                an odd channel count (or a mono beat) write two even lanes
                in one cycle into two different memories; no memory takes
                two writes in a cycle. The memories carry no reset so they
                infer RAM (the KL_i2s_playback fifo_r precedent); every read
                is gated by the pointers to a row the push has written.

                Single clock domain. tick_i arrives already synchronized. The
                schedule takes N_STREAMS_P x PAIRS_C + 1 cycles; a tick that
                lands inside it is queued and served right after.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Render setpoint stage: per-stream elastic queue of media events whose
//! fill is the constant accept-to-render latency (SETPOINT_EVT_P), prefilled
//! to it, band-observed at every PDU end, re-centred once on a GM/PHC step;
//! pops one event per stream per media tick into the render crossbar as
//! clone-format beats and hands the crossbar a delayed render tick.

`default_nettype none

module KL_render_setpoint #(
  parameter int unsigned N_STREAMS_P      = 8,   //! listener streams (<= 8,
                                                 //! the crossbar's map field)
  parameter int unsigned N_CH_P           = 8,   //! wire channels kept per
                                                 //! event row (<= 8)
  parameter int unsigned DEPTH_LOG2_P     = 5,   //! event rows per stream =
                                                 //! 2^N (2 <= N <= 7)
  parameter int unsigned PDU_EVENTS_P     = 6,   //! events per accepted PDU
                                                 //! (the class-A frame shape)
  parameter int unsigned SETPOINT_EVT_P   = 8,   //! the constant: fill in
                                                 //! events just before a
                                                 //! PDU push = first-event
                                                 //! delay in media ticks
  parameter int unsigned CONV_BAND_EVT_P  = 3,   //! convergence band, events
                                                 //! either side of TARGET_C
  parameter int unsigned RESET_BAND_EVT_P = 6,   //! reset rail, events either
                                                 //! side of TARGET_C
  parameter int unsigned CLK_FREQ_HZ_P    = 100_000_000 //! clk_i frequency,
                                                 //! Hz (the observer's
                                                 //! per-millisecond divider)
)(
  input  wire                      clk_i,        //! datapath clock
  input  wire                      rst_n,        //! active-low synchronous
                                                 //! reset

  //! --- depacketizer payload clone (never backpressured; drive s_tvalid_i
  //! --- with the tapped link's ACCEPTED beats, the crossbar discipline) ----
  input  wire [63:0]               s_tdata_i,    //! 2 consecutive S32BE
                                                 //! samples, wire order
  input  wire                      s_tvalid_i,   //! accepted-beat strobe
  input  wire                      s_tlast_i,    //! one AXIS frame per PDU
  input  wire [3:0]                s_tuser_i,    //! stream index s

  //! --- per-stream wire channel count (RX monitors' wire_chans_o) ---------
  input  wire [N_STREAMS_P*4-1:0]  wire_chans_i, //! 4-bit fields; 0 -> 2

  //! --- the media grid and the one-shot events -----------------------------
  input  wire                      tick_i,       //! one pulse per media frame,
                                                 //! at least N_STREAMS_P x
                                                 //! PAIRS_C + 2 cycles apart
                                                 //! (a tick on the edge a
                                                 //! queued tick starts is
                                                 //! not queued again)
  input  wire                      recentre_p_i, //! one-cycle: GM identity
                                                 //! change, PHC step or a
                                                 //! settled clock-source
                                                 //! change
  input  wire [N_STREAMS_P-1:0]    flush_i,      //! one-cycle per stream:
                                                 //! bind loss, empty it

  //! --- to the render crossbar (KL_chan_map_render s_* and tick_i) ---------
  output logic [63:0]              m_tdata_o,    //! S32BE sample pair, wire
                                                 //! order; pad lanes zero
  output logic                     m_tvalid_o,   //! beat strobe (registered)
  output logic                     m_tlast_o,    //! last beat of the event
  output logic [3:0]               m_tuser_o,    //! stream index s
  output logic [N_STREAMS_P*4-1:0] m_wire_chans_o, //! every stream presents
                                                 //! 2 x PAIRS_C lanes (the
                                                 //! pad lane of an odd
                                                 //! N_CH_P and lanes >= the
                                                 //! channel count carry 0)
  output logic                     render_tick_p_o, //! tick_i delayed past
                                                 //! the pop schedule: the
                                                 //! crossbar's tick_i

  //! --- observability (TB taps and the #390 debug-window follow-up) --------
  output logic [N_STREAMS_P-1:0]   pop_p_o,      //! one-cycle per stream: its
                                                 //! event's first beat is
                                                 //! being presented (the
                                                 //! render instant at the
                                                 //! crossbar input grid)
  output logic [N_STREAMS_P*8-1:0] fill_o,       //! per-stream fill, events
  output logic [N_STREAMS_P-1:0]   prefill_o,    //! per-stream: pops held
  output logic [N_STREAMS_P-1:0]   converged_o,  //! per-stream: the last PDU
                                                 //! end of each observer
                                                 //! period inside the
                                                 //! convergence band, 100
                                                 //! periods running; held
                                                 //! between the bands
  output logic [15:0]              underruns_o,  //! ticks that found a stream
                                                 //! empty (saturating)
  output logic [15:0]              overruns_o,   //! events dropped at a full
                                                 //! queue (saturating)
  output logic [15:0]              rails_o,      //! reset-band actions
                                                 //! (saturating)
  output logic [15:0]              recentres_o   //! recentre_p_i actions,
                                                 //! one per stream per pulse
                                                 //! (saturating)
);

  // ------------------------------------------------------------------ //
  // Elaboration contract                                                //
  // ------------------------------------------------------------------ //
  localparam int unsigned ROWS_C   = 1 << DEPTH_LOG2_P;   //! rows per stream
  localparam int unsigned PAIRS_C  = (N_CH_P + 1) / 2;    //! beats per event
  localparam int unsigned PW_C     = DEPTH_LOG2_P + 1;    //! pointer width
  localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P;
  //! the observer's period: one millisecond of clk_i
  localparam int unsigned MS_DIV_C = CLK_FREQ_HZ_P / 1000;
  //! the convergence observer's dwell, in observer periods
  localparam int unsigned CONV_DWELL_C = 100;

  if (N_STREAMS_P < 1 || N_STREAMS_P > 8) begin : g_chk_streams
    $error("KL_render_setpoint: N_STREAMS_P=%0d must be 1..8 (the crossbar's 3-bit stream field)", N_STREAMS_P);
  end : g_chk_streams
  if (N_CH_P < 1 || N_CH_P > 8) begin : g_chk_chans
    $error("KL_render_setpoint: N_CH_P=%0d must be 1..8 (the crossbar's 3-bit channel field)", N_CH_P);
  end : g_chk_chans
  if (DEPTH_LOG2_P < 2 || DEPTH_LOG2_P > 7) begin : g_chk_depth
    $error("KL_render_setpoint: DEPTH_LOG2_P=%0d must be 2..7 (row parity needs two banks; fill_o carries 8 bits)", DEPTH_LOG2_P);
  end : g_chk_depth
  if (PDU_EVENTS_P < 1 || SETPOINT_EVT_P < 1) begin : g_chk_shape
    $error("KL_render_setpoint: PDU_EVENTS_P=%0d and SETPOINT_EVT_P=%0d must both be at least 1", PDU_EVENTS_P, SETPOINT_EVT_P);
  end : g_chk_shape
  if (RESET_BAND_EVT_P < CONV_BAND_EVT_P) begin : g_chk_bands
    $error("KL_render_setpoint: RESET_BAND_EVT_P=%0d below CONV_BAND_EVT_P=%0d - the rail would fire inside the convergence band", RESET_BAND_EVT_P, CONV_BAND_EVT_P);
  end : g_chk_bands
  if (TARGET_C + RESET_BAND_EVT_P + PDU_EVENTS_P > ROWS_C) begin : g_chk_fit
    $error("KL_render_setpoint: SETPOINT_EVT_P + PDU_EVENTS_P + RESET_BAND_EVT_P + one bunched PDU = %0d exceeds the 2^%0d = %0d rows - the reset rail could not act on a bunched PDU before the queue overruns", TARGET_C + RESET_BAND_EVT_P + PDU_EVENTS_P, DEPTH_LOG2_P, ROWS_C);
  end : g_chk_fit
  if (CLK_FREQ_HZ_P < 2000) begin : g_chk_clk
    $error("KL_render_setpoint: CLK_FREQ_HZ_P=%0d cannot divide to a millisecond observer period", CLK_FREQ_HZ_P);
  end : g_chk_clk

  // ------------------------------------------------------------------ //
  // Storage: pair words, odd lanes in h1, even lanes in h0 split by row  //
  // parity. Word address = ((stream * rows) + row) * pairs + pair.       //
  // ------------------------------------------------------------------ //
  localparam int unsigned H1_DEPTH_C = N_STREAMS_P * ROWS_C * PAIRS_C;
  localparam int unsigned H0_DEPTH_C = N_STREAMS_P * (ROWS_C / 2) * PAIRS_C;
  localparam int unsigned H1_AW_C    = $clog2(H1_DEPTH_C);
  localparam int unsigned H0_AW_C    = $clog2(H0_DEPTH_C);

  logic [23:0] h1_r  [H1_DEPTH_C];
  logic [23:0] h0e_r [H0_DEPTH_C];
  logic [23:0] h0o_r [H0_DEPTH_C];

  //! word addresses take the ROW INDEX (the pointer without its wrap bit)
  function automatic logic [H1_AW_C-1:0] h1_addr(input logic [3:0] s,
                                                 input logic [DEPTH_LOG2_P-1:0] row,
                                                 input logic [3:0] pair);
    h1_addr = H1_AW_C'((32'(s) * ROWS_C + 32'(row)) * PAIRS_C + 32'(pair));
  endfunction

  //! the even-lane banks are addressed by the row index WITHOUT its parity
  //! bit (the parity selects the bank)
  function automatic logic [H0_AW_C-1:0] h0_addr(input logic [3:0] s,
                                                 input logic [DEPTH_LOG2_P-2:0] row_hi,
                                                 input logic [3:0] pair);
    h0_addr = H0_AW_C'((32'(s) * (ROWS_C / 2) + 32'(row_hi)) * PAIRS_C + 32'(pair));
  endfunction

  //! increment-with-wrap at the stream's channel count (the crossbar's own)
  function automatic logic [3:0] chwrap(input logic [3:0] ch, input logic [3:0] chans);
    chwrap = ((4'(ch + 4'd1)) == chans) ? 4'd0 : 4'(ch + 4'd1);
  endfunction

  // ------------------------------------------------------------------ //
  // Per-stream state                                                    //
  // ------------------------------------------------------------------ //
  logic [PW_C-1:0] wptr_r      [N_STREAMS_P];
  logic [PW_C-1:0] rptr_r      [N_STREAMS_P];
  logic            prefill_r   [N_STREAMS_P];  //! pops held until the snap
  logic            pend_r      [N_STREAMS_P];  //! a recentre awaits the PDU end
  logic            dev_ok_r    [N_STREAMS_P];  //! last PDU end inside CONV
  logic [6:0]      conv_ms_r   [N_STREAMS_P];  //! observer periods in band
  logic            converged_r [N_STREAMS_P];
  logic [3:0]      chans_q_r   [N_STREAMS_P];  //! channel count of the last
                                               //! accepted beat (0 = none yet)

  logic [3:0]      chpos_r;      //! wire channel of the current beat's FIRST
                                 //! sample (frames are atomic: one counter)
  logic            evt_drop_r;   //! the in-flight event found the queue full

  // ------------------------------------------------------------------ //
  // Push side: walk the clone, write lanes, complete rows               //
  // ------------------------------------------------------------------ //
  wire s_ok_w = s_tvalid_i && (32'(s_tuser_i) < N_STREAMS_P);

  //! the in-flight stream's channel count and pointers (constant-base mux)
  logic [3:0]      chans_in_raw_w, chans_q_in_w;
  logic [PW_C-1:0] wptr_in_w, rptr_in_w;
  always_comb begin : in_lookup
    chans_in_raw_w = 4'd0;
    chans_q_in_w   = 4'd0;
    wptr_in_w      = '0;
    rptr_in_w      = '0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
      if (32'(s_tuser_i) == s) begin
        chans_in_raw_w = wire_chans_i[s*4 +: 4];
        chans_q_in_w   = chans_q_r[s];
        wptr_in_w      = wptr_r[s];
        rptr_in_w      = rptr_r[s];
      end
    end
  end : in_lookup
  wire [3:0] c_in_w = (chans_in_raw_w == 4'd0) ? 4'd2 : chans_in_raw_w;
  //! the stream's wire channel count moved since its last beat: its queued
  //! rows carry the old lane layout, so the beat flushes it (below)
  wire chans_moved_w = s_ok_w && (chans_q_in_w != 4'd0) && (chans_q_in_w != c_in_w);

  //! the two S32BE samples of the beat (the crossbar's decode: wire byte
  //! first = MSB, lane 3/7 = pad, dropped)
  wire [23:0] smp0_w = {s_tdata_i[7:0],   s_tdata_i[15:8],  s_tdata_i[23:16]};
  wire [23:0] smp1_w = {s_tdata_i[39:32], s_tdata_i[47:40], s_tdata_i[55:48]};
  wire [3:0]  ch0_w  = chpos_r;
  wire [3:0]  ch1_w  = chwrap(ch0_w, c_in_w);

  //! a sample completes its event when it is the last wire channel; the
  //! second sample of a straddling beat starts the NEXT row
  wire cmpl0_w  = (ch0_w == 4'(c_in_w - 4'd1));
  wire cmpl1_w  = (ch1_w == 4'(c_in_w - 4'd1));
  wire start0_w = (ch0_w == 4'd0);
  wire start1_w = (ch1_w == 4'd0);

  //! the pop side may consume a row this very cycle (an event's first
  //! beat); the fill the push sees is the one AFTER that pop (rptr_eff_w
  //! below), so a full queue is judged on the same edge the pointers move
  logic            pop_take_w;      //! declared with the pop side below
  logic [3:0]      slot_r;
  wire  [PW_C-1:0] rptr_eff_in_w = rptr_in_w
                                 + PW_C'(pop_take_w && (slot_r == s_tuser_i));
  wire  [PW_C-1:0] fill_in_w  = wptr_in_w - rptr_eff_in_w;
  wire             full0_w    = (fill_in_w == PW_C'(ROWS_C));
  //! an event judged full at its first lane stays dropped to its last lane,
  //! or a pop between the two would let a stale lane 0 into a stored row
  wire             drop0_w    = start0_w ? full0_w : evt_drop_r;
  wire             adv0_w     = s_ok_w && cmpl0_w && !drop0_w;
  //! the row indices (the pointers without their wrap bit)
  wire  [DEPTH_LOG2_P-1:0] row0_w = wptr_in_w[DEPTH_LOG2_P-1:0];
  wire  [DEPTH_LOG2_P-1:0] row1_w = DEPTH_LOG2_P'(wptr_in_w + PW_C'(adv0_w));
  wire             full1_w    = ((fill_in_w + PW_C'(adv0_w)) == PW_C'(ROWS_C));
  wire             drop1_w    = start1_w ? full1_w : drop0_w;
  wire             adv1_w     = s_ok_w && cmpl1_w && !drop1_w;
  wire             st0_w      = s_ok_w && !drop0_w && (32'(ch0_w) < N_CH_P);
  wire             st1_w      = s_ok_w && !drop1_w && (32'(ch1_w) < N_CH_P);
  wire             ovr0_w     = s_ok_w && cmpl0_w && drop0_w;
  wire             ovr1_w     = s_ok_w && cmpl1_w && drop1_w;
  wire  [PW_C-1:0] wptr_nxt_w = wptr_in_w + PW_C'(adv0_w) + PW_C'(adv1_w);

  //! lane -> memory: odd lane -> h1; even lane -> h0e (even row) / h0o (odd
  //! row). Sample 0 and sample 1 never address the same memory (see the
  //! banner), so a simple priority is a tie that cannot occur.
  wire h1_we_w  = (st0_w && ch0_w[0]) || (st1_w && ch1_w[0]);
  wire h0e_we_w = (st0_w && !ch0_w[0] && !row0_w[0]) ||
                  (st1_w && !ch1_w[0] && !row1_w[0]);
  wire h0o_we_w = (st0_w && !ch0_w[0] &&  row0_w[0]) ||
                  (st1_w && !ch1_w[0] &&  row1_w[0]);
  wire h1_sel0_w  = st0_w && ch0_w[0];
  wire h0e_sel0_w = st0_w && !ch0_w[0] && !row0_w[0];
  wire h0o_sel0_w = st0_w && !ch0_w[0] &&  row0_w[0];
  wire [H1_AW_C-1:0] h1_wa_w  = h1_sel0_w  ? h1_addr(s_tuser_i, row0_w, {1'b0, ch0_w[3:1]})
                                           : h1_addr(s_tuser_i, row1_w, {1'b0, ch1_w[3:1]});
  wire [H0_AW_C-1:0] h0e_wa_w = h0e_sel0_w ? h0_addr(s_tuser_i, row0_w[DEPTH_LOG2_P-1:1], {1'b0, ch0_w[3:1]})
                                           : h0_addr(s_tuser_i, row1_w[DEPTH_LOG2_P-1:1], {1'b0, ch1_w[3:1]});
  wire [H0_AW_C-1:0] h0o_wa_w = h0o_sel0_w ? h0_addr(s_tuser_i, row0_w[DEPTH_LOG2_P-1:1], {1'b0, ch0_w[3:1]})
                                           : h0_addr(s_tuser_i, row1_w[DEPTH_LOG2_P-1:1], {1'b0, ch1_w[3:1]});
  wire [23:0] h1_wd_w  = h1_sel0_w  ? smp0_w : smp1_w;
  wire [23:0] h0e_wd_w = h0e_sel0_w ? smp0_w : smp1_w;
  wire [23:0] h0o_wd_w = h0o_sel0_w ? smp0_w : smp1_w;

  always_ff @(posedge clk_i) begin : h1_write
    if (h1_we_w) h1_r[h1_wa_w] <= h1_wd_w;
  end : h1_write
  always_ff @(posedge clk_i) begin : h0e_write
    if (h0e_we_w) h0e_r[h0e_wa_w] <= h0e_wd_w;
  end : h0e_write
  always_ff @(posedge clk_i) begin : h0o_write
    if (h0o_we_w) h0o_r[h0o_wa_w] <= h0o_wd_w;
  end : h0o_write

  always_ff @(posedge clk_i) begin : walker
    if (!rst_n) begin
      chpos_r    <= 4'd0;
      evt_drop_r <= 1'b0;
    end else if (s_ok_w) begin
      chpos_r    <= s_tlast_i ? 4'd0 : chwrap(ch1_w, c_in_w);
      evt_drop_r <= drop1_w;
    end
  end : walker

  // ------------------------------------------------------------------ //
  // Pop side: one event per stream per tick, streams in index order     //
  // ------------------------------------------------------------------ //
  logic       sched_r;    //! the schedule is running
  logic       tick_q_r;   //! a tick landed inside the schedule
  logic       tick_d_r;   //! the last beat has been presented: the render
                          //! tick follows one cycle later so the crossbar
                          //! registers that beat before it renders
  logic [3:0] beat_r;

  wire start_w     = (tick_i || tick_q_r) && !sched_r;
  wire last_beat_w = (32'(beat_r) == PAIRS_C - 1);
  wire last_slot_w = (32'(slot_r) == N_STREAMS_P - 1);

  //! the scheduled stream's channel count and pointers
  logic [3:0]      chans_pop_raw_w;
  logic [PW_C-1:0] wptr_pop_w, rptr_pop_w;
  logic            prefill_pop_w;
  always_comb begin : pop_lookup
    chans_pop_raw_w = 4'd0;
    wptr_pop_w      = '0;
    rptr_pop_w      = '0;
    prefill_pop_w   = 1'b1;
    for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
      if (32'(slot_r) == s) begin
        chans_pop_raw_w = wire_chans_i[s*4 +: 4];
        wptr_pop_w      = wptr_r[s];
        rptr_pop_w      = rptr_r[s];
        prefill_pop_w   = prefill_r[s];
      end
    end
  end : pop_lookup
  wire [3:0]      c_pop_w    = (chans_pop_raw_w == 4'd0) ? 4'd2 : chans_pop_raw_w;
  wire [PW_C-1:0] fill_pop_w = wptr_pop_w - rptr_pop_w;
  wire            first_beat_w = (beat_r == 4'd0);
  //! THE EVENT-ATOMIC POP: whether the scheduled stream presents an event
  //! is decided once, at its first beat, from the registered state; that
  //! beat consumes the event (pop_take_w advances rptr) and latches its
  //! row (ev_row_r), and the remaining beats present the latched row
  //! whatever the pointers or the prefill flag do meanwhile. A PDU end, a
  //! rail, a recentre or a flush inside the window therefore lands between
  //! events, never inside one: the crossbar always receives PAIRS_C beats
  //! of ONE row with tlast on the last
  logic                    ev_ok_r;   //! the event in flight is presented
  logic [DEPTH_LOG2_P-1:0] ev_row_r;  //! its row, latched at the first beat
  assign pop_take_w = sched_r && first_beat_w && !prefill_pop_w && (fill_pop_w != '0);
  wire            pop_ok_w   = first_beat_w ? pop_take_w : ev_ok_r;
  //! an empty stream is judged once per tick, at its first beat
  wire            pop_dry_w  = sched_r && first_beat_w && !prefill_pop_w
                               && (fill_pop_w == '0);
  //! the row this beat reads: the head at the first beat, the latched row
  //! after it
  wire [DEPTH_LOG2_P-1:0] rd_row_w = first_beat_w ? rptr_pop_w[DEPTH_LOG2_P-1:0]
                                                  : ev_row_r;

  //! the beat's two lanes: even lane from h0 (bank by row parity), odd lane
  //! from h1; lanes at or beyond the stream's channel count read zero
  wire [3:0]  lane_e_w = {beat_r[2:0], 1'b0};
  wire [3:0]  lane_o_w = {beat_r[2:0], 1'b1};
  wire [23:0] rd_e_w   = rd_row_w[0] ? h0o_r[h0_addr(slot_r, rd_row_w[DEPTH_LOG2_P-1:1], beat_r)]
                                     : h0e_r[h0_addr(slot_r, rd_row_w[DEPTH_LOG2_P-1:1], beat_r)];
  wire [23:0] rd_o_w   = h1_r[h1_addr(slot_r, rd_row_w, beat_r)];
  wire [23:0] smp_e_w  = (32'(lane_e_w) < 32'(c_pop_w)) ? rd_e_w : 24'd0;
  wire [23:0] smp_o_w  = ((32'(lane_o_w) < 32'(c_pop_w)) && (32'(lane_o_w) < N_CH_P))
                         ? rd_o_w : 24'd0;

  always_ff @(posedge clk_i) begin : pop_schedule
    if (!rst_n) begin
      sched_r  <= 1'b0;
      tick_q_r <= 1'b0;
      slot_r   <= 4'd0;
      beat_r   <= 4'd0;
      m_tvalid_o <= 1'b0;
      m_tdata_o  <= 64'd0;
      m_tlast_o  <= 1'b0;
      m_tuser_o  <= 4'd0;
      tick_d_r   <= 1'b0;
      render_tick_p_o <= 1'b0;
      pop_p_o <= '0;
      ev_ok_r  <= 1'b0;
      ev_row_r <= '0;
    end else begin
      //! the presented beat (registered): S32BE wire order, pad lanes zero
      m_tvalid_o <= pop_ok_w;
      m_tdata_o  <= {8'h00, smp_o_w[7:0], smp_o_w[15:8], smp_o_w[23:16],
                     8'h00, smp_e_w[7:0], smp_e_w[15:8], smp_e_w[23:16]};
      m_tlast_o  <= last_beat_w;
      m_tuser_o  <= slot_r;
      pop_p_o    <= '0;
      for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
        if (pop_take_w && (32'(slot_r) == s)) pop_p_o[s] <= 1'b1;
      end
      tick_d_r        <= sched_r && last_beat_w && last_slot_w;
      render_tick_p_o <= tick_d_r;

      if (start_w) begin
        sched_r  <= 1'b1;
        tick_q_r <= 1'b0;
        slot_r   <= 4'd0;
        beat_r   <= 4'd0;
      end else if (sched_r) begin
        //! the event-atomic latch: taken at the stream's first beat only
        if (first_beat_w) begin
          ev_ok_r  <= pop_take_w;
          ev_row_r <= rptr_pop_w[DEPTH_LOG2_P-1:0];
        end
        if (last_beat_w) begin
          beat_r <= 4'd0;
          if (last_slot_w) sched_r <= 1'b0;
          else             slot_r  <= slot_r + 4'd1;
        end else begin
          beat_r <= beat_r + 4'd1;
        end
        //! a tick inside the schedule is served right after it, never lost
        if (tick_i) tick_q_r <= 1'b1;
      end
    end
  end : pop_schedule

  // ------------------------------------------------------------------ //
  // Per-stream pointers, prefill, bands, recentre, flush                //
  // ------------------------------------------------------------------ //
  //! the fill after this PDU's push, seen at its last beat; the concurrent
  //! pop (if any) is already in rptr_eff_in_w
  wire [PW_C-1:0] fill_end_w = wptr_nxt_w - rptr_eff_in_w;
  wire            pdu_end_w  = s_ok_w && s_tlast_i;
  wire            enough_w   = (32'(fill_end_w) >= TARGET_C);
  wire            high_w     = (32'(fill_end_w) >  TARGET_C + RESET_BAND_EVT_P);
  wire            low_w      = (32'(fill_end_w) + RESET_BAND_EVT_P < TARGET_C);
  wire            in_band_w  = (32'(fill_end_w) <= TARGET_C + CONV_BAND_EVT_P) &&
                               (32'(fill_end_w) + CONV_BAND_EVT_P >= TARGET_C);
  wire [PW_C-1:0] snap_rptr_w = wptr_nxt_w - PW_C'(TARGET_C);

  //! the observer's period
  logic [$clog2(MS_DIV_C)-1:0] ms_div_r;
  wire ms_p_w = (32'(ms_div_r) == MS_DIV_C - 1);

  //! this cycle's counter increments (one PDU end, one dry slot, up to two
  //! dropped events per cycle)
  logic rail_p_w, recentre_p_w;

  always_ff @(posedge clk_i) begin : stream_state
    if (!rst_n) begin
      for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
        wptr_r[s]      <= '0;
        rptr_r[s]      <= '0;
        prefill_r[s]   <= 1'b1;
        pend_r[s]      <= 1'b0;
        dev_ok_r[s]    <= 1'b0;
        conv_ms_r[s]   <= 7'd0;
        converged_r[s] <= 1'b0;
        chans_q_r[s]   <= 4'd0;
      end
    end else begin
      for (int unsigned s = 0; s < N_STREAMS_P; s++) begin : per_stream
        //! pop: the first beat of a presented event consumes it
        if (pop_take_w && (32'(slot_r) == s)) rptr_r[s] <= rptr_r[s] + PW_C'(1);
        //! underrun rail: one bounded gap, then prefill re-snaps
        if (pop_dry_w && (32'(slot_r) == s)) begin
          prefill_r[s]   <= 1'b1;
          dev_ok_r[s]    <= 1'b0;
          conv_ms_r[s]   <= 7'd0;
          converged_r[s] <= 1'b0;
        end
        //! convergence observer: in band at the PDU ends for CONV_DWELL_C
        //! periods; a rail or a prefill clears it, a wander between the
        //! bands holds it
        if (ms_p_w && !prefill_r[s] && dev_ok_r[s]) begin
          if (32'(conv_ms_r[s]) != CONV_DWELL_C) conv_ms_r[s] <= conv_ms_r[s] + 7'd1;
          else                                    converged_r[s] <= 1'b1;
        end
        if (s_ok_w && (32'(s_tuser_i) == s)) begin
          wptr_r[s]    <= wptr_nxt_w;
          chans_q_r[s] <= c_in_w;
          if (s_tlast_i) begin
            if (prefill_r[s] || pend_r[s]) begin
              //! prefill release / recentre: snap the fill to TARGET_C at
              //! the PDU end; a short queue re-enters prefill instead
              if (enough_w) begin
                rptr_r[s]    <= snap_rptr_w;
                prefill_r[s] <= 1'b0;
                pend_r[s]    <= 1'b0;
              end else if (pend_r[s]) begin
                prefill_r[s]   <= 1'b1;
                pend_r[s]      <= 1'b0;
                dev_ok_r[s]    <= 1'b0;
                conv_ms_r[s]   <= 7'd0;
                converged_r[s] <= 1'b0;
              end
            end else begin
              dev_ok_r[s] <= in_band_w;
              if (high_w) begin
                rptr_r[s]      <= snap_rptr_w;
                dev_ok_r[s]    <= 1'b0;
                conv_ms_r[s]   <= 7'd0;
                converged_r[s] <= 1'b0;
              end else if (low_w) begin
                prefill_r[s]   <= 1'b1;
                dev_ok_r[s]    <= 1'b0;
                conv_ms_r[s]   <= 7'd0;
                converged_r[s] <= 1'b0;
              end
            end
          end
        end
        //! a recentre arms the pending flag AFTER the PDU-end block so a
        //! pulse coincident with the snap is a new event for the next one;
        //! a stream in prefill has nothing to recentre
        if (recentre_p_i && !prefill_r[s]) pend_r[s] <= 1'b1;
        //! flush wins over everything: empty, prefill. A wire channel count
        //! that moved on this stream flushes it the same way (the queued
        //! rows carry the old lane layout; this beat's rows go with them)
        if (flush_i[s] || (chans_moved_w && (32'(s_tuser_i) == s))) begin
          rptr_r[s]      <= (s_ok_w && (32'(s_tuser_i) == s)) ? wptr_nxt_w : wptr_r[s];
          prefill_r[s]   <= 1'b1;
          pend_r[s]      <= 1'b0;
          dev_ok_r[s]    <= 1'b0;
          conv_ms_r[s]   <= 7'd0;
          converged_r[s] <= 1'b0;
        end
      end : per_stream
    end
  end : stream_state

  //! the two PDU-end actions that count, named once for the counters
  logic pend_in_w, prefill_in_w;
  always_comb begin : in_flags
    pend_in_w    = 1'b0;
    prefill_in_w = 1'b1;
    for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
      if (32'(s_tuser_i) == s) begin
        pend_in_w    = pend_r[s];
        prefill_in_w = prefill_r[s];
      end
    end
    recentre_p_w = pdu_end_w && pend_in_w && !prefill_in_w;
    rail_p_w     = pdu_end_w && !pend_in_w && !prefill_in_w && (high_w || low_w);
  end : in_flags

  always_ff @(posedge clk_i) begin : observer_and_counters
    if (!rst_n) begin
      ms_div_r    <= '0;
      underruns_o <= 16'd0;
      overruns_o  <= 16'd0;
      rails_o     <= 16'd0;
      recentres_o <= 16'd0;
    end else begin
      ms_div_r <= ms_p_w ? '0 : ms_div_r + 1'b1;
      if (pop_dry_w && !(&underruns_o)) underruns_o <= underruns_o + 16'd1;
      //! up to two events drop in one cycle (a mono beat), so the saturation
      //! guard leaves room for both
      if ((ovr0_w || ovr1_w) && (overruns_o < 16'hFFFE))
        overruns_o <= overruns_o + 16'(ovr0_w) + 16'(ovr1_w);
      else if (ovr0_w || ovr1_w)
        overruns_o <= 16'hFFFF;
      if (rail_p_w && !(&rails_o))         rails_o     <= rails_o + 16'd1;
      if (recentre_p_w && !(&recentres_o)) recentres_o <= recentres_o + 16'd1;
    end
  end : observer_and_counters

  // ------------------------------------------------------------------ //
  // Observability and the crossbar's channel view                       //
  // ------------------------------------------------------------------ //
  //! the pad byte of each S32BE lane is dropped by construction
  wire _unused_ok = &{1'b0, s_tdata_i[63:56], s_tdata_i[31:24], 1'b0};

  //! the fill is a POINTER difference: subtract at the pointer width, then
  //! widen (a cast-context subtraction would wrap at 8 bits and read a
  //! wrapped pointer pair as 200-odd)
  logic [PW_C-1:0] fill_s_w [N_STREAMS_P];
  always_comb begin : taps
    for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
      fill_s_w[s]              = wptr_r[s] - rptr_r[s];
      fill_o[s*8 +: 8]         = 8'(fill_s_w[s]);
      prefill_o[s]             = prefill_r[s];
      converged_o[s]           = converged_r[s];
      m_wire_chans_o[s*4 +: 4] = 4'(2 * PAIRS_C);
    end
  end : taps

endmodule

`default_nettype wire

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_render_setpoint harness (#386): the listener render path's setpoint stage.
//
// The harness plays the depacketizer clone AND the media grid. PDUs of the
// class-A frame shape (PDU_EVENTS events per PDU) are pushed on a cadence
// locked to the tick (one PDU every PDU_EVENTS ticks, the push starting a
// fixed phase after a tick so no tick lands inside a push window), every
// sample encodes {pdu[11:0], event[3:0], channel[7:0]}, and every beat the
// stage presents to the crossbar is decoded back into an event. That is what
// lets the LAW be asserted per PDU rather than on averages:
//
//   * prefill holds pops until a PDU end finds fill >= TARGET, then the fill
//     IS TARGET and the first popped event is the one the snap left at the head;
//   * the fill just before every push is SETPOINT and just after it is TARGET;
//   * the first event of every PDU pops at the (SETPOINT + 1)-th tick at or
//     after its push, event k of the PDU k ticks later - the delay is one
//     constant, not a distribution;
//   * beats are byte-exact for 8, 3 (a straddling odd count), 1 (mono, two
//     events per beat) and 12 (virtual channels) wire channels, pad bytes
//     zero, lanes at or beyond the channel count zero, tlast on the last beat;
//   * the pop schedule visits the streams in order and the render tick trails
//     the media tick by exactly N_STREAMS x PAIRS + 1 cycles;
//   * an underrun is ONE bounded gap; the high rail snaps to TARGET once, the
//     low rail re-enters prefill; a PDU exactly one PDU late trips neither;
//   * the convergence observer rises after its dwell, clears on a rail, and
//     HOLDS between the bands; the recentre is executed once per pulse at the
//     next PDU end and counted once, two pulses in one PDU count once, and a
//     pulse in prefill counts nothing; a flush empties; a tick inside the
//     schedule is queued; an event completing at a full queue is dropped.
//
// The build's -G shape reaches this file as -D constants from the Makefile's
// single statement of it, so the geometry asserted is the geometry built.
#include "../../common/verilator_harness.hpp"
#include "VKL_render_setpoint.h"
#include "verilated.h"

#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <vector>

constexpr int kStreams   = N_STREAMS_TB;   // N_STREAMS_P
constexpr int kCh        = N_CH_TB;        // N_CH_P: lanes per event row
constexpr int kDepthLog2 = DEPTH_LOG2_TB;  // rows per stream = 2^N
constexpr int kPduEvents = PDU_EVENTS_TB;  // events per PDU (class A at 48k)
constexpr int kSetpoint  = SETPOINT_TB;    // the constant, in events
constexpr int kConvBand  = CONV_BAND_TB;   // events either side of TARGET
constexpr int kResetBand = RESET_BAND_TB;  // events either side of TARGET
constexpr int kClkHz     = CLK_HZ_TB;      // CLK_FREQ_HZ_P

constexpr int  kRows        = 1 << kDepthLog2;
constexpr int  kTarget      = kSetpoint + kPduEvents;   // fill right after a push
constexpr int  kPairs       = (kCh + 1) / 2;            // beats per event
constexpr long kTickPeriod  = 100;                      // cycles per media tick
constexpr long kPduPeriod   = kPduEvents * kTickPeriod; // cycles per PDU in lock
//! a push starts this many cycles after a tick: the longest push here is 36
//! beats (12 wire channels), so no tick ever lands inside a push window and
//! the fill sampled at a PDU end is exactly TARGET
constexpr long kPushPhase   = 30;
constexpr int  kObserverPeriod = kClkHz / 1000;         // cycles per observer period
constexpr int  kConvDwell   = 100;                      // observer periods to converge
constexpr int  kResetCycles = 8;
constexpr uint32_t kSampleMask = 0xFFFFFF;
constexpr uint8_t  kPadByte    = 0xA5;    // a nonzero pad on the way in must be dropped
constexpr int  kLawPdus     = 24;         // PDUs the law is asserted over (> the dwell)
constexpr int  kLongPduEvents = 40;       // an event count that overfills a 32-row queue

static_assert(kStreams == 2, "the schedule checks assume two streams");
static_assert(kRows == 32, "the overrun phase counts drops against 32 rows");

//! {pdu[11:0], event[3:0], channel[7:0]}: a sample names where it came from
static uint32_t sample_of(int pdu, int event, int channel) {
  return (static_cast<uint32_t>(pdu & 0xFFF) << 12) |
         (static_cast<uint32_t>(event & 0xF) << 8) |
         static_cast<uint32_t>(channel & 0xFF);
}
static int pdu_of(uint32_t sample)   { return static_cast<int>((sample >> 12) & 0xFFF); }
static int event_of(uint32_t sample) { return static_cast<int>((sample >> 8) & 0xF); }

//! wire-order S32BE beat: byte lane j = wire byte j, sample byte 0 = MSB,
//! lanes 3 and 7 are the pad the stage must drop
static uint64_t beat_of(uint32_t s0, uint32_t s1) {
  uint64_t b = 0;
  b |= static_cast<uint64_t>((s0 >> 16) & 0xFF) << 0;
  b |= static_cast<uint64_t>((s0 >> 8) & 0xFF) << 8;
  b |= static_cast<uint64_t>(s0 & 0xFF) << 16;
  b |= static_cast<uint64_t>(kPadByte) << 24;
  b |= static_cast<uint64_t>((s1 >> 16) & 0xFF) << 32;
  b |= static_cast<uint64_t>((s1 >> 8) & 0xFF) << 40;
  b |= static_cast<uint64_t>(s1 & 0xFF) << 48;
  b |= static_cast<uint64_t>(kPadByte) << 56;
  return b;
}

namespace {

//! one event as the stage presented it to the crossbar
struct Event {
  long first_beat_cycle = 0;
  int  stream = 0;
  int  beats = 0;
  bool tlast_on_last = false;
  bool pads_zero = true;
  std::array<uint32_t, kCh> lane{};
};

class RenderSetpointHarness {
 public:
  int run();

 private:
  const milan::tb::Model<VKL_render_setpoint> model;
  VKL_render_setpoint* dut = model.get();
  milan::tb::Checker check{"render_setpoint"};

  long cycle = 0;                       //! edges so far
  bool ticks_on = true;                 //! the harness plays the media grid
  std::vector<long> tick_cycles;        //! edges that sampled tick_i high
  std::vector<long> render_tick_cycles; //! edges after which render_tick_p_o read 1
  std::array<long, kStreams> pop_count{};
  std::array<Event, kStreams> assembling{};
  std::array<bool, kStreams> assembling_live{};
  std::array<std::deque<Event>, kStreams> popped{};
  std::array<long, kStreams> push_cycle{};   //! the edge that sampled the last push's first beat
  std::array<int, kStreams> chans{};         //! the wire channel count each stream declares

  // ---- the clock, the grid and the observer ----------------------------------
  void set_chans(int stream, int c) {
    chans[stream] = c;
    uint32_t v = 0;
    for (int s = 0; s < kStreams; s++) v |= static_cast<uint32_t>(chans[s] & 0xF) << (4 * s);
    dut->wire_chans_i = v;
  }

  void step() {
    dut->tick_i = (ticks_on && (cycle % kTickPeriod == 0)) ? 1 : 0;
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    cycle++;                                   //! the edge just taken
    if (dut->tick_i) tick_cycles.push_back(cycle);
    dut->tick_i = 0;
    observe();
  }

  void observe() {
    if (dut->render_tick_p_o) render_tick_cycles.push_back(cycle);
    for (int s = 0; s < kStreams; s++)
      if ((dut->pop_p_o >> s) & 1) pop_count[s]++;
    if (!dut->m_tvalid_o) return;
    const int s = dut->m_tuser_o & 0xF;
    if (s >= kStreams) { check.fail("a presented beat names a stream beyond the shape"); return; }
    Event& e = assembling[s];
    if (!assembling_live[s]) { e = Event{}; e.first_beat_cycle = cycle; e.stream = s; assembling_live[s] = true; }
    const uint64_t d = dut->m_tdata_o;
    const uint32_t s0 = (static_cast<uint32_t>(d & 0xFF) << 16) |
                        (static_cast<uint32_t>((d >> 8) & 0xFF) << 8) |
                        static_cast<uint32_t>((d >> 16) & 0xFF);
    const uint32_t s1 = (static_cast<uint32_t>((d >> 32) & 0xFF) << 16) |
                        (static_cast<uint32_t>((d >> 40) & 0xFF) << 8) |
                        static_cast<uint32_t>((d >> 48) & 0xFF);
    if (((d >> 24) & 0xFF) != 0 || ((d >> 56) & 0xFF) != 0) e.pads_zero = false;
    const int lane0 = 2 * e.beats;
    if (lane0 < kCh) e.lane[lane0] = s0;
    if (lane0 + 1 < kCh) e.lane[lane0 + 1] = s1;
    e.beats++;
    if (dut->m_tlast_o) {
      e.tlast_on_last = (e.beats == kPairs);
      popped[s].push_back(e);
      assembling_live[s] = false;
    }
  }

  void idle(long n) {
    dut->s_tvalid_i = 0; dut->s_tlast_i = 0;
    for (long i = 0; i < n; i++) step();
  }
  void run_to(long target) { while (cycle < target) idle(1); }
  int  fill(int s) const { return (dut->fill_o >> (8 * s)) & 0xFF; }
  bool prefill(int s) const { return ((dut->prefill_o >> s) & 1) != 0; }
  bool converged(int s) const { return ((dut->converged_o >> s) & 1) != 0; }

  // ---- the clone: one PDU of `events` events on `stream` -------------------------
  void push_pdu(int stream, int pdu, int events = kPduEvents) {
    const int c = chans[stream];
    const int total = events * c;
    const int beats = (total + 1) / 2;
    push_cycle[stream] = cycle + 1;            //! the edge that samples beat 0
    for (int b = 0; b < beats; b++) {
      const int i0 = 2 * b;
      const int i1 = 2 * b + 1;
      const uint32_t s0 = sample_of(pdu, i0 / c, i0 % c);
      const uint32_t s1 = (i1 < total) ? sample_of(pdu, i1 / c, i1 % c) : 0;
      dut->s_tdata_i  = beat_of(s0, s1);
      dut->s_tvalid_i = 1;
      dut->s_tuser_i  = stream;
      dut->s_tlast_i  = (b == beats - 1) ? 1 : 0;
      step();
    }
    dut->s_tvalid_i = 0; dut->s_tlast_i = 0;
  }

  //! the locked cadence: PDU n of stream 0 starts kPushPhase after tick n x kPduEvents
  long slot_cycle(long n) const { return n * kPduPeriod + kPushPhase; }
  void push_on_cadence(int stream, int pdu, long slot) { run_to(slot_cycle(slot)); push_pdu(stream, pdu); }

  //! the first-event pop delay of PDU `pdu` on `stream`, or -1 if not popped
  long first_event_delay(int stream, int pdu, long pushed_at) const {
    for (const Event& e : popped[stream])
      if (pdu_of(e.lane[0]) == pdu && event_of(e.lane[0]) == 0) return e.first_beat_cycle - pushed_at;
    return -1;
  }
  bool in_law_band(long d) const {
    return d > kSetpoint * kTickPeriod && d <= (kSetpoint + 1) * kTickPeriod + 2;
  }

  // ---- the phases ----------------------------------------------------------------
  void reset();
  void prove_prefill_holds_then_releases_at_the_target();
  void prove_the_law_pdu_after_pdu(long& d0_ref);
  void prove_the_schedule_and_the_render_tick();
  void prove_beats_for_every_channel_count(long d0_ref);
  void prove_an_underrun_is_one_bounded_gap();
  void prove_the_rails();
  void prove_convergence_and_the_one_shot_recentre();
  void prove_flush_queued_tick_and_overrun();
  long push_next(long extra);
  void pulse_recentre();
  long pdu_seq = 0;      //! the next PDU id on stream 0's cadence
  long slot_seq = 0;     //! the next cadence slot on stream 0
  long cadence_phase = 0; //! cycles the cadence runs behind slot_cycle()
  int  pdu_seq1 = 0;     //! the next PDU id on stream 1
  long slot_seq1 = 0;    //! stream 1's cadence slot (its own phase, 60 cycles later)
};

// ---- reset -----------------------------------------------------------------
void RenderSetpointHarness::reset() {
  dut->clk_i = 0; dut->rst_n = 0;
  dut->s_tdata_i = 0; dut->s_tvalid_i = 0; dut->s_tlast_i = 0; dut->s_tuser_i = 0;
  dut->tick_i = 0; dut->recentre_p_i = 0; dut->flush_i = 0;
  set_chans(0, kCh); set_chans(1, kCh);
  ticks_on = false;
  for (int i = 0; i < kResetCycles; i++) step();
  dut->rst_n = 1;
  ticks_on = true;
  check.dec("reset: fill 0 on stream 0", fill(0), 0);
  check.dec("reset: fill 0 on stream 1", fill(1), 0);
  check.that("reset: both streams in prefill", prefill(0) && prefill(1));
  check.dec("reset: crossbar channel view is N_CH_P per stream",
            dut->m_wire_chans_o, (static_cast<uint32_t>(kCh) << 4) | static_cast<uint32_t>(kCh));
}

// ============================================================================
// [P] prefill: two PDUs (12 events) hold; the third (18) releases with the
//     fill snapped to TARGET and the head at event 18 - TARGET of the stream.
// ============================================================================
void RenderSetpointHarness::prove_prefill_holds_then_releases_at_the_target() {
  printf("[P] prefill holds until a PDU end finds fill >= %d\n", kTarget);
  push_on_cadence(0, 0, 0); pdu_seq = 1; slot_seq = 1;
  check.dec("[P] one PDU queued", fill(0), kPduEvents);
  push_on_cadence(0, 1, 1); pdu_seq = 2; slot_seq = 2;
  check.dec("[P] two PDUs queued", fill(0), 2 * kPduEvents);
  run_to(slot_cycle(2) - 1);
  check.dec("[P] no pop during prefill (12 ticks)", pop_count[0], 0);
  check.that("[P] still in prefill", prefill(0));
  push_pdu(0, 2); pdu_seq = 3; slot_seq = 3;
  idle(2);
  check.that("[P] released at the third PDU end", !prefill(0));
  check.dec("[P] fill snapped to TARGET at release", fill(0), kTarget);
  // the head is now event (3 x PDU_EVENTS - TARGET) of the stream
  const int head_index = 3 * kPduEvents - kTarget;
  run_to(tick_cycles.back() + kTickPeriod + 8);
  check.dec("[P] first event popped after release", pop_count[0], 1);
  if (!popped[0].empty()) {
    const Event& e = popped[0].front();
    check.hex("[P] the head is the event the snap left (pdu)", pdu_of(e.lane[0]), head_index / kPduEvents);
    check.hex("[P] the head is the event the snap left (event)", event_of(e.lane[0]), head_index % kPduEvents);
    check.dec("[P] pop_p rose on the first beat", e.first_beat_cycle, tick_cycles.back() + 1);
  }
}

// ============================================================================
// [L] the law, PDU after PDU: fill SETPOINT before every push and TARGET after
//     it; the first event pops at the (SETPOINT+1)-th tick at or after the
//     push, event k k ticks later, the same delay for every PDU.
// ============================================================================
void RenderSetpointHarness::prove_the_law_pdu_after_pdu(long& d0_ref) {
  printf("[L] the delay law over %d PDUs (setpoint %d events)\n", kLawPdus, kSetpoint);
  long fills_before_ok = 0;
  long fills_after_ok = 0;
  std::vector<long> pushed(kLawPdus, 0);
  const int first = static_cast<int>(pdu_seq);
  //! the cadence keeps running past the measured PDUs so the last of them
  //! renders while the queue is still in lock (a stopped cadence drains)
  const int tail = kSetpoint / kPduEvents + 2;
  for (int i = 0; i < kLawPdus + tail; i++) {
    run_to(slot_cycle(slot_seq));
    const bool before_ok = (fill(0) == kSetpoint);
    push_pdu(0, static_cast<int>(pdu_seq));
    idle(2);
    const bool after_ok = (fill(0) == kTarget);
    if (i < kLawPdus) {
      pushed[i] = push_cycle[0];
      if (before_ok) fills_before_ok++;
      if (after_ok) fills_after_ok++;
    }
    pdu_seq++; slot_seq++;
  }
  check.dec("[L] fill == SETPOINT before every push", fills_before_ok, kLawPdus);
  check.dec("[L] fill == TARGET after every PDU end", fills_after_ok, kLawPdus);
  long in_band = 0;
  long dmin = 0;
  long dmax = 0;
  long k_ok = 0;
  for (int i = 0; i < kLawPdus; i++) {
    const long d = first_event_delay(0, first + i, pushed[i]);
    if (d < 0) continue;
    if (in_law_band(d)) in_band++;
    if (i == 0 || d < dmin) dmin = d;
    if (i == 0 || d > dmax) dmax = d;
    // event k of the same PDU pops k ticks after event 0
    for (const Event& e : popped[0]) {
      if (pdu_of(e.lane[0]) != first + i) continue;
      const int k = event_of(e.lane[0]);
      if (e.first_beat_cycle - pushed[i] == d + k * kTickPeriod) k_ok++;
    }
  }
  d0_ref = dmin;
  printf("  first-event delay: min %ld max %ld cycles = %.3f..%.3f ticks (law: %d < d <= %d ticks)\n",
         dmin, dmax, static_cast<double>(dmin) / kTickPeriod, static_cast<double>(dmax) / kTickPeriod,
         kSetpoint, kSetpoint + 1);
  check.dec("[L] every PDU's first event inside the law band", in_band, kLawPdus);
  check.dec("[L] one constant: zero spread across PDUs", dmax - dmin, 0);
  check.dec("[L] event k pops k ticks after event 0 (all events)", k_ok, static_cast<long>(kLawPdus) * kPduEvents);
  check.that("[L] converged after the observer's dwell", converged(0));
  check.dec("[L] no underrun in lock", dut->underruns_o, 0);
  check.dec("[L] no rail in lock", dut->rails_o, 0);
  // the convergence observer ran for the whole phase: its dwell must fit
  check.that("[L] the phase outlasted the dwell",
             static_cast<long>(kLawPdus) * kPduPeriod > static_cast<long>(kConvDwell) * kObserverPeriod);
}

// ============================================================================
// [S] the schedule: streams in order, one beat per cycle, the render tick
//     N_STREAMS x PAIRS + 1 cycles after the media tick, every tick.
// ============================================================================
void RenderSetpointHarness::prove_the_schedule_and_the_render_tick() {
  printf("[S] the pop schedule and the delayed render tick\n");
  long ok = 0;
  const size_t n = render_tick_cycles.size();
  size_t j = 0;
  for (size_t i = 0; i < tick_cycles.size() && j < n; i++) {
    const long t = tick_cycles[i];
    while (j < n && render_tick_cycles[j] < t) j++;
    if (j < n && render_tick_cycles[j] == t + kStreams * kPairs + 1) ok++;
  }
  check.dec("[S] a render tick per media tick", n, tick_cycles.size());
  check.dec("[S] render tick = media tick + N_STREAMS x PAIRS + 1", ok, tick_cycles.size());
  check.dec("[S] stream 1 popped nothing while in prefill", pop_count[1], 0);
  long tuser_ok = 0;
  long shape_ok = 0;
  for (const Event& e : popped[0]) {
    if (e.stream == 0) tuser_ok++;
    if (e.beats == kPairs && e.tlast_on_last && e.pads_zero) shape_ok++;
  }
  check.dec("[S] every event carries tuser 0", tuser_ok, popped[0].size());
  check.dec("[S] every event is PAIRS beats, tlast last, pads zero", shape_ok, popped[0].size());
}

// ============================================================================
// [C] byte-exact beats for 8 (already popped above), 3, 1 and 12 wire
//     channels on stream 1, while stream 0's law keeps holding.
// ============================================================================
void RenderSetpointHarness::prove_beats_for_every_channel_count(long d0_ref) {
  printf("[C] beats for 3, 1 and 12 wire channels on stream 1\n");
  // 8 channels on stream 0: lanes byte-exact for every popped event so far
  long exact8 = 0;
  for (const Event& e : popped[0]) {
    bool ok = true;
    for (int c = 0; c < kCh; c++)
      if (e.lane[c] != sample_of(pdu_of(e.lane[0]), event_of(e.lane[0]), c)) ok = false;
    if (ok) exact8++;
  }
  check.dec("[C] 8 channels: every lane byte-exact", exact8, popped[0].size());

  struct Shape { int c; const char* name; };
  //! 12 channels FIRST: it writes every lane of stream 1's rows, so the two
  //! narrower shapes that follow read stale lanes unless the mask zeroes them
  const std::array<Shape, 3> shapes{{{12, "12 channels (virtual 8..11)"}, {3, "3 channels (straddle)"}, {1, "mono"}}};
  for (const Shape& sh : shapes) {
    dut->flush_i = 0x2; idle(1); dut->flush_i = 0;
    popped[1].clear();
    set_chans(1, sh.c);
    const int base = pdu_seq1;
    // stream 1 rides its own cadence 60 cycles behind stream 0's, and stream 0
    // keeps its cadence so the two are proved independent
    for (int i = 0; i < 6; i++) {
      run_to(slot_cycle(slot_seq)); push_pdu(0, static_cast<int>(pdu_seq)); pdu_seq++; slot_seq++;
      run_to(slot_cycle(slot_seq - 1) + 60); push_pdu(1, pdu_seq1); pdu_seq1++;
    }
    run_to(slot_cycle(slot_seq) + kTickPeriod);
    long exact = 0;
    long zero_beyond = 0;
    long consecutive = 0;
    int expect_pdu = -1;
    int expect_event = 0;
    const int lanes = (sh.c < kCh) ? sh.c : kCh;
    for (const Event& e : popped[1]) {
      bool ok = true;
      bool zeros = true;
      const int p = pdu_of(e.lane[0]);
      const int k = event_of(e.lane[0]);
      for (int c = 0; c < lanes; c++) if (e.lane[c] != sample_of(p, k, c)) ok = false;
      for (int c = lanes; c < kCh; c++) if (e.lane[c] != 0) zeros = false;
      if (ok && p >= base) exact++;
      if (zeros) zero_beyond++;
      if (expect_pdu < 0) { expect_pdu = p; expect_event = k; }
      if (p == expect_pdu && k == expect_event) consecutive++;
      expect_event++;
      if (expect_event == kPduEvents) { expect_event = 0; expect_pdu++; }
    }
    char w[96];
    snprintf(w, sizeof w, "[C] %s: events popped after release", sh.name);
    check.that(w, popped[1].size() >= static_cast<size_t>(2 * kPduEvents));
    snprintf(w, sizeof w, "[C] %s: lanes < C byte-exact", sh.name);
    check.dec(w, exact, popped[1].size());
    snprintf(w, sizeof w, "[C] %s: lanes >= C read zero", sh.name);
    check.dec(w, zero_beyond, popped[1].size());
    snprintf(w, sizeof w, "[C] %s: events in order, none lost or repeated", sh.name);
    check.dec(w, consecutive, popped[1].size());
  }
  // stream 0 was untouched by stream 1's shapes
  const long d = first_event_delay(0, static_cast<int>(pdu_seq) - 1, push_cycle[0]);
  const long d_prev = first_event_delay(0, static_cast<int>(pdu_seq) - 2,
                                        push_cycle[0] - kPduPeriod);
  check.dec("[C] stream 0's delay unchanged beside stream 1 (this PDU)", d_prev, d0_ref);
  check.that("[C] stream 0's last PDU still queued or popped in law", d < 0 || in_law_band(d));
  set_chans(1, kCh);
}

// ---- the stream-0 cadence, shared by the phases below ----------------------
// PDU pdu_seq goes out at slot_cycle(slot_seq) + cadence_phase (+ extra), and
// the law is judged on a PDU only after two more PDUs have followed it on the
// cadence, so the queue never drains while a measurement waits.
long RenderSetpointHarness::push_next(long extra) {
  run_to(slot_cycle(slot_seq) + cadence_phase + extra);
  push_pdu(0, static_cast<int>(pdu_seq));
  const long at = push_cycle[0];
  pdu_seq++; slot_seq++;
  return at;
}

void RenderSetpointHarness::pulse_recentre() {
  dut->recentre_p_i = 1; step(); dut->recentre_p_i = 0;
}

// ============================================================================
// [U] an underrun is one bounded gap: the queue drains, ONE underrun is
//     counted, prefill re-arms, and the cadence's return releases again.
// ============================================================================
void RenderSetpointHarness::prove_an_underrun_is_one_bounded_gap() {
  printf("[U] underrun: one bounded gap, then prefill\n");
  //! stream 1 parks in prefill (a flush) so the counter below is stream 0's
  dut->flush_i = 0x2; step(); dut->flush_i = 0;
  const long pops0 = pop_count[0];
  const int  queued = fill(0);
  check.that("[U] events queued before the cadence stops", queued > 0 && !prefill(0));
  const long gap_ticks = kTarget + 12;
  run_to(cycle + gap_ticks * kTickPeriod);
  check.dec("[U] the queue drained to zero", fill(0), 0);
  check.dec("[U] exactly one underrun counted", dut->underruns_o, 1);
  check.that("[U] prefill re-armed", prefill(0));
  check.dec("[U] pops stopped at the drained count", pop_count[0] - pops0, queued);
  run_to(cycle + 12 * kTickPeriod);
  check.dec("[U] no repeat storm: still one underrun", dut->underruns_o, 1);
  // resume on the next free slot: three PDUs release again and the law holds
  while (slot_cycle(slot_seq) + cadence_phase < cycle) slot_seq++;
  for (int i = 0; i < 3; i++) push_next(0);
  idle(2);
  check.that("[U] released after three PDUs", !prefill(0));
  check.dec("[U] fill at TARGET again", fill(0), kTarget);
  const int  pdu = static_cast<int>(pdu_seq);
  const long pushed = push_next(0);
  for (int i = 0; i < 2; i++) push_next(0);
  check.that("[U] the law holds after the gap", in_law_band(first_event_delay(0, pdu, pushed)));
  check.dec("[U] the gap left the underrun count at one", dut->underruns_o, 1);
}

// ============================================================================
// [R] the rails: a bunched burst snaps once at the high rail; a PDU exactly
//     one PDU late trips nothing; a PDU seven ticks late re-enters prefill.
// ============================================================================
void RenderSetpointHarness::prove_the_rails() {
  printf("[R] the reset rails (band +/-%d events at PDU ends)\n", kResetBand);
  // keep the cadence so the observer converges before the burst
  for (int i = 0; i < 20; i++) push_next(0);
  //! the burst is 72 beats, so it starts 26 cycles early to stay clear of
  //! the tick that would otherwise fall inside it
  run_to(slot_cycle(slot_seq) + cadence_phase - 26);
  check.that("[R] converged before the burst", converged(0));
  // a regular PDU then two bunched extras: fill ends at 14, 20 (dev +6, no
  // rail), 26 (dev +12, snap)
  push_pdu(0, static_cast<int>(pdu_seq)); pdu_seq++;
  push_pdu(0, static_cast<int>(pdu_seq)); pdu_seq++;
  idle(2);
  check.dec("[R] one PDU over: dev +6 trips no rail", dut->rails_o, 0);
  check.dec("[R] ...and the fill sits at TARGET + one PDU", fill(0), kTarget + kPduEvents);
  push_pdu(0, static_cast<int>(pdu_seq)); pdu_seq++;
  idle(2);
  check.dec("[R] two PDUs over: the high rail snapped once", dut->rails_o, 1);
  check.dec("[R] ...to TARGET", fill(0), kTarget);
  check.that("[R] the rail cleared converged", !converged(0));
  slot_seq++;
  // the cadence resumes: the law holds again from the next PDU
  int  pdu = static_cast<int>(pdu_seq);
  long pushed = push_next(0);
  for (int i = 0; i < 2; i++) push_next(0);
  check.that("[R] the law holds after the snap", in_law_band(first_event_delay(0, pdu, pushed)));
  check.dec("[R] no second snap", dut->rails_o, 1);
  // exactly one PDU late: PDU n arrives in PDU n+1's slot, followed at once
  // by PDU n+1 (dev -6 then 0): neither rail, no underrun
  slot_seq++;
  push_next(0);
  push_pdu(0, static_cast<int>(pdu_seq)); pdu_seq++;
  idle(2);
  check.dec("[R] a PDU one PDU late trips no rail", dut->rails_o, 1);
  check.dec("[R] ...and no underrun", dut->underruns_o, 1);
  check.dec("[R] ...fill back at TARGET", fill(0), kTarget);
  for (int i = 0; i < 2; i++) push_next(0);
  // seven ticks late (dev -7): the low rail re-enters prefill without an
  // underrun (one event was still queued); the cadence keeps that phase
  run_to(slot_cycle(slot_seq) + cadence_phase + 7 * kTickPeriod);
  check.dec("[R] seven ticks late: one event still queued", fill(0), kSetpoint - 7);
  cadence_phase += 7 * kTickPeriod;
  push_next(0);
  idle(2);
  check.dec("[R] the low rail counted", dut->rails_o, 2);
  check.that("[R] ...and re-entered prefill", prefill(0));
  check.dec("[R] ...with no underrun", dut->underruns_o, 1);
  for (int i = 0; i < 2; i++) push_next(0);
  idle(2);
  check.that("[R] released two PDUs later", !prefill(0));
  check.dec("[R] fill at TARGET", fill(0), kTarget);
  pdu = static_cast<int>(pdu_seq);
  pushed = push_next(0);
  for (int i = 0; i < 2; i++) push_next(0);
  check.that("[R] the law holds on the shifted cadence", in_law_band(first_event_delay(0, pdu, pushed)));
}

// ============================================================================
// [V] convergence holds between the bands; the recentre is one-shot and
//     counted once, two pulses in one PDU count once, prefill ignores it.
// ============================================================================
void RenderSetpointHarness::prove_convergence_and_the_one_shot_recentre() {
  printf("[V] convergence hold and the one-shot recentre\n");
  for (int i = 0; i < 22; i++) push_next(0);
  check.that("[V] converged again in lock", converged(0));
  // displace by 4 ticks (dev -4: outside CONV, inside RESET): the observer
  // HOLDS converged, the law shows the displaced delay
  cadence_phase += 4 * kTickPeriod;
  int  pdu = static_cast<int>(pdu_seq);
  long pushed = push_next(0);
  for (int i = 0; i < 4; i++) push_next(0);
  check.that("[V] between the bands: converged holds", converged(0));
  check.dec("[V] between the bands: no rail", dut->rails_o, 2);
  const long d_disp = first_event_delay(0, pdu, pushed);
  check.that("[V] displaced: the delay is four ticks short of the law", d_disp > 0 && !in_law_band(d_disp)
             && d_disp > (kSetpoint - 4) * kTickPeriod && d_disp <= (kSetpoint - 3) * kTickPeriod + 2);
  // ONE recentre pulse: the next PDU end finds 10 < TARGET, re-enters prefill,
  // the one after releases at TARGET; counted once
  pulse_recentre();
  push_next(0); idle(2);
  check.dec("[V] the pulse was consumed at the next PDU end", dut->recentres_o, 1);
  check.that("[V] a short queue re-enters prefill", prefill(0));
  push_next(0); idle(2);
  check.that("[V] ...and releases at the PDU end after", !prefill(0));
  check.dec("[V] fill at TARGET after the recentre", fill(0), kTarget);
  pdu = static_cast<int>(pdu_seq);
  pushed = push_next(0);
  for (int i = 0; i < 10; i++) push_next(0);
  check.that("[V] the law is restored on the displaced cadence", in_law_band(first_event_delay(0, pdu, pushed)));
  check.dec("[V] counted once, never again", dut->recentres_o, 1);
  // displace the other way: 3 ticks EARLY (dev +3, in band); two pulses in one
  // PDU count once and the snap drops the three excess events
  cadence_phase -= 3 * kTickPeriod;
  pdu = static_cast<int>(pdu_seq);
  pushed = push_next(0);
  for (int i = 0; i < 3; i++) push_next(0);
  const long d_early = first_event_delay(0, pdu, pushed);
  check.that("[V] early cadence: the delay is three ticks over the law", d_early > (kSetpoint + 3) * kTickPeriod
             && d_early <= (kSetpoint + 4) * kTickPeriod + 2);
  pulse_recentre();
  idle(3);
  pulse_recentre();
  push_next(0); idle(2);
  check.dec("[V] two pulses in one PDU: counted once", dut->recentres_o, 2);
  check.dec("[V] the snap dropped the excess to TARGET", fill(0), kTarget);
  check.that("[V] no prefill on a long queue", !prefill(0));
  pdu = static_cast<int>(pdu_seq);
  pushed = push_next(0);
  for (int i = 0; i < 3; i++) push_next(0);
  check.that("[V] the law is restored on the early cadence", in_law_band(first_event_delay(0, pdu, pushed)));
  check.dec("[V] still two recentres", dut->recentres_o, 2);
  check.dec("[V] no rail through both recentres", dut->rails_o, 2);
}

// ============================================================================
// [F] flush empties into prefill and a pulse there counts nothing; a tick
//     inside the schedule is queued; an event completing at a full queue is
//     dropped and counted; the flush leaves no stale event behind.
// ============================================================================
void RenderSetpointHarness::prove_flush_queued_tick_and_overrun() {
  printf("[F] flush, queued tick, overrun\n");
  dut->flush_i = 0x1; step(); dut->flush_i = 0;
  check.dec("[F] flush: fill 0", fill(0), 0);
  check.that("[F] flush: prefill", prefill(0));
  pulse_recentre();
  const int first_after = static_cast<int>(pdu_seq);
  popped[0].clear();
  for (int i = 0; i < 3; i++) push_next(0);
  idle(2);
  check.dec("[F] a pulse in prefill counted nothing", dut->recentres_o, 2);
  check.that("[F] released after three post-flush PDUs", !prefill(0));
  for (int i = 0; i < 2; i++) push_next(0);
  bool stale = false;
  for (const Event& e : popped[0]) if (pdu_of(e.lane[0]) < first_after) stale = true;
  check.that("[F] no pre-flush event was ever popped", !stale && !popped[0].empty());
  // a tick inside the schedule: both ticks are served
  ticks_on = false;
  idle(5);
  const long pops0 = pop_count[0];
  const size_t rt0 = render_tick_cycles.size();
  dut->tick_i = 1; dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); cycle++; dut->tick_i = 0; observe();
  idle(2);
  dut->tick_i = 1; dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); cycle++; dut->tick_i = 0; observe();
  idle(3 * kStreams * kPairs);
  check.dec("[F] a tick inside the schedule is queued: two pops", pop_count[0] - pops0, 2);
  check.dec("[F] ...and two render ticks", render_tick_cycles.size() - rt0, 2);
  ticks_on = true;
  // overrun on stream 1 (in prefill): one long PDU overfills the 32 rows
  dut->flush_i = 0x2; step(); dut->flush_i = 0;
  const uint32_t ovr0 = dut->overruns_o;
  push_pdu(1, pdu_seq1, kLongPduEvents); pdu_seq1++;
  idle(2);
  check.dec("[F] events beyond the depth were dropped", dut->overruns_o - ovr0, kLongPduEvents - kRows);
  check.dec("[F] the long PDU's end released stream 1 at TARGET", fill(1), kTarget);
  check.that("[F] stream 1 out of prefill", !prefill(1));
}

int RenderSetpointHarness::run() {
  printf("== KL_render_setpoint: %d streams x %d lanes, %d rows, PDU %d events, setpoint %d, bands %d/%d ==\n",
         kStreams, kCh, kRows, kPduEvents, kSetpoint, kConvBand, kResetBand);
  reset();
  long d0_ref = 0;
  prove_prefill_holds_then_releases_at_the_target();
  prove_the_law_pdu_after_pdu(d0_ref);
  prove_the_schedule_and_the_render_tick();
  prove_beats_for_every_channel_count(d0_ref);
  prove_an_underrun_is_one_bounded_gap();
  prove_the_rails();
  prove_convergence_and_the_one_shot_recentre();
  prove_flush_queued_tick_and_overrun();
  return check.report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  RenderSetpointHarness harness;
  return harness.run();
}

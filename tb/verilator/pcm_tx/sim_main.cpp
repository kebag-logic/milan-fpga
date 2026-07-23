// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_pcm_tx self-checking harness. Built shrunk (N_STREAMS_P=2, CHANS_P=4 =>
// 2 channel-pairs/stream => 4 pair slots; SAMPLE_DIV_C=32) so full playback
// episodes run in microseconds.
//
// A model host PCM ring is filled with distinct S32BE samples and its per-
// stream write pointer advanced; the harness models the module's word-fetch
// port (1-cycle-latency memory) and asserts:
//   * media cadence: exactly (enabled streams * pairs) pairs per sample tick,
//     none between ticks;
//   * EXACT de-interleaved sample sequence (S32BE byte order = the RX ring's),
//     including a negative control that a little-lane read would NOT match;
//   * ring wrap: reads continue correctly across the sub-ring wrap point;
//   * underrun: starve a stream -> the pair is still emitted on cadence, the
//     count grows, and the substitute is last-sample (repeat) or silence;
//   * overrun: lap the reader -> the count grows and the read pointer fast-
//     forwards one lap so the fill is bounded again.

#include "VKL_pcm_tx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_pcm_tx *dut;
static int pass = 0, fail = 0;

// ---- build-time config (must match the Makefile -G flags) ----------------
static const int      N       = 2;      // N_STREAMS_P
static const int      PAIRS   = 2;      // CHANS_P/2
static const int      SLOTS   = N * PAIRS;
static const uint32_t LEN     = 128;    // per-stream sub-ring bytes (16 words)
static const uint32_t STRIDE  = 4096;   // bytes between stream sub-ring bases
static const int      SAMPLE_DIV = 32;

// ---- model host ring (physical DRAM bytes) -------------------------------
static std::vector<uint8_t> dram(STRIDE * N + LEN + 64, 0);
static uint32_t wrv[N]       = {0, 0};   // per-stream absolute write pointer
static uint32_t committed[N] = {0, 0};   // words already written into dram

// distinct 24-bit samples per (stream, absolute word index)
static uint32_t modelL(int s, uint32_t j) { return 0x100000u | (s << 12) | (j & 0xFFF); }
static uint32_t modelR(int s, uint32_t j) { return 0x200000u | (s << 12) | (j & 0xFFF); }

static uint32_t stream_base(int s) { return (uint32_t)s * STRIDE; }

// write word j of stream s into dram at its wrapped offset, S32BE layout:
//   lane0=L[23:16] lane1=L[15:8] lane2=L[7:0] lane3=0
//   lane4=R[23:16] lane5=R[15:8] lane6=R[7:0] lane7=0
static void put_word(int s, uint32_t j, uint32_t L, uint32_t R) {
  uint32_t off = (j * 8) % LEN;
  uint32_t a   = stream_base(s) + off;
  dram[a + 0] = (L >> 16) & 0xFF; dram[a + 1] = (L >> 8) & 0xFF;
  dram[a + 2] = L & 0xFF;         dram[a + 3] = 0x00;
  dram[a + 4] = (R >> 16) & 0xFF; dram[a + 5] = (R >> 8) & 0xFF;
  dram[a + 6] = R & 0xFF;         dram[a + 7] = 0x00;
}

// commit words up to `target` for stream s (advances the host write pointer)
static void feed_to(int s, uint32_t target) {
  for (uint32_t j = committed[s]; j < target; j++)
    put_word(s, j, modelL(s, j), modelR(s, j));
  if (target > committed[s]) committed[s] = target;
  wrv[s] = committed[s] * 8;
}

static uint64_t mem_word(uint32_t a) {
  uint64_t w = 0;
  for (int j = 0; j < 8; j++) w |= (uint64_t)dram[a + j] << (8 * j);
  return w;
}

// ---- module accessors ----------------------------------------------------
static uint32_t rd_of(int s)    { return (uint32_t)((dut->rd_ptr_o  >> (32 * s)) & 0xFFFFFFFFu); }
static uint32_t under_of(int s) { return (dut->underrun_o >> (16 * s)) & 0xFFFF; }
static uint32_t over_of(int s)  { return (dut->overrun_o  >> (16 * s)) & 0xFFFF; }
static void push_wr() { dut->wr_ptr_i = (uint64_t)wrv[0] | ((uint64_t)wrv[1] << 32); }

// ---- fetch-port memory model + pair capture ------------------------------
static bool     mem_pend = false;
static uint32_t mem_addr = 0;

struct Pair { int slot; uint32_t l, r; };
static std::vector<Pair> caps;          // pairs captured this observation window
static bool auto_feed = false;
static int  LEAD = 8;                    // words kept ahead per stream when feeding

static void tick() {
  // present the response for a request captured on the previous cycle
  dut->mem_valid_i = mem_pend ? 1 : 0;
  if (mem_pend) dut->mem_data_i = mem_word(mem_addr);
  push_wr();
  dut->clk_i = 0; dut->eval();
  // capture the fetch request valid THIS cycle (Moore output off current state)
  bool req = dut->mem_rd_o; uint32_t a = dut->mem_addr_o;
  dut->clk_i = 1; dut->eval();          // posedge
  mem_pend = req; mem_addr = a;
  // record an emitted pair (registered: valid after the edge)
  if (dut->pair_valid_o)
    caps.push_back({(int)dut->pair_slot_o, (uint32_t)dut->pair_l_o, (uint32_t)dut->pair_r_o});
  // keep the enabled streams fed (top up to consumed + LEAD, no over/underrun)
  if (auto_feed)
    for (int s = 0; s < N; s++)
      if (dut->stream_en_i & (1 << s)) feed_to(s, rd_of(s) / 8 + LEAD);
}
static void run(int n) { for (int i = 0; i < n; i++) tick(); }

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        (unsigned long long)got, (unsigned long long)want); }
}
static void ck_true(const char *name, bool c) { ck(name, c ? 1 : 0, 1); }

// run exactly one sample: consume the tick, then let the walk drain
static void one_sample() {
  caps.clear();
  // advance to the next media tick edge
  int guard = 0;
  while (!dut->smp_tick_o && guard++ < 4 * SAMPLE_DIV) tick();
  if (!dut->smp_tick_o) { fail++; printf("[FAIL] no media tick within window\n"); }
  // let the walk complete (well within one sample period)
  run(SAMPLE_DIV - 2);
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_pcm_tx;

  dut->rst_n = 0;
  dut->enable_i = 0; dut->stream_en_i = 0; dut->underrun_silence_i = 0;
  dut->ring_base_i = 0; dut->ring_len_i = LEN; dut->ring_stride_i = STRIDE;
  dut->wr_ptr_i = 0; dut->smp_tick_i = 0; dut->mem_valid_i = 0; dut->mem_data_i = 0;
  run(4); dut->rst_n = 1; run(4);

  // ====================================================================
  //  Phase 1 - exact de-interleaved sample sequence + cadence + wrap
  // ====================================================================
  // fully feed both streams every cycle; run many samples so the ring wraps
  // (LEN = 16 words; > 16 consumed words per stream exercises the wrap).
  dut->enable_i = 1; dut->stream_en_i = 0x3;
  auto_feed = true;
  feed_to(0, LEAD); feed_to(1, LEAD);

  uint32_t exp_cw[N] = {0, 0};          // expected consumed words per stream
  bool seq_ok = true, slot_ok = true, cadence_ok = true, neg_ok = true;
  const int SAMPLES = 40;               // 40*PAIRS = 80 words/stream >> 16 = wraps
  for (int m = 0; m < SAMPLES; m++) {
    one_sample();
    // cadence: exactly SLOTS pairs this sample, none missing
    if ((int)caps.size() != SLOTS) cadence_ok = false;
    for (auto &p : caps) {
      int t = p.slot / PAIRS, pp = p.slot % PAIRS;
      if (t < 0 || t >= N || pp < 0 || pp >= PAIRS) { slot_ok = false; continue; }
      uint32_t j  = exp_cw[t]++;
      uint32_t eL = modelL(t, j), eR = modelR(t, j);
      if (p.l != eL || p.r != eR) seq_ok = false;
      // negative control: a little-lane (byte-reversed) read of L would be
      // 0xCCBBAA-shaped; assert the module did NOT produce that
      uint32_t wrongL = ((eL & 0xFF) << 16) | (eL & 0xFF00) | ((eL >> 16) & 0xFF);
      if (eL != wrongL && p.l == wrongL) neg_ok = false;
    }
  }
  ck_true("phase1 cadence: SLOTS pairs/sample", cadence_ok);
  ck_true("phase1 slot ownership t*PAIRS+p",    slot_ok);
  ck_true("phase1 exact S32BE sample sequence", seq_ok);
  ck_true("phase1 neg-control (not little-lane)", neg_ok);
  // both streams consumed >> one ring => wrap was exercised and stayed correct
  ck_true("phase1 wrap exercised (rd past LEN)", rd_of(0) > LEN && rd_of(1) > LEN);
  ck("phase1 s0 consumed words", rd_of(0) / 8, (uint64_t)exp_cw[0]);
  ck("phase1 s1 consumed words", rd_of(1) / 8, (uint64_t)exp_cw[1]);

  // no phantom underruns/overruns on the healthy path
  ck("phase1 s0 no underrun", under_of(0), 0);
  ck("phase1 s1 no underrun", under_of(1), 0);
  ck("phase1 s0 no overrun",  over_of(0), 0);
  ck("phase1 s1 no overrun",  over_of(1), 0);

  // ====================================================================
  //  Phase 2 - paced emission: SLOTS pair-cycles per period + an idle gap
  // ====================================================================
  {
    // align to a tick (start of a period; streams still fed => all data)
    int g = 0; while (!dut->smp_tick_o && g++ < 4 * SAMPLE_DIV) tick();
    // count pair-valid cycles over the rest of the period (tick cycle emits
    // none - the walk starts the cycle after). Exactly SLOTS pairs, and far
    // fewer than the period => emission is paced, not free-running.
    int pv = 0; bool crossed = false;
    for (int c = 0; c < SAMPLE_DIV - 1; c++) {
      tick();
      if (dut->pair_valid_o) pv++;
      if (dut->smp_tick_o) crossed = true;
    }
    ck("phase2 SLOTS pair-cycles per period", pv, SLOTS);
    ck_true("phase2 idle gap between ticks (paced)", pv < SAMPLE_DIV - 1);
    ck_true("phase2 exactly one tick per period", !crossed);
  }

  // ====================================================================
  //  Phase 3 - underrun: repeat-last policy, cadence preserved, counted
  // ====================================================================
  {
    auto_feed = false;                    // freeze the write pointers
    // resync the model to the reader (fill 0 on both streams), then give
    // stream 0 EXACTLY one clean sample's worth so both channel-pair slots
    // establish a known last-sample hold; stream 1 stays empty (underruns).
    for (int s = 0; s < N; s++) { committed[s] = rd_of(s) / 8; wrv[s] = committed[s] * 8; }
    feed_to(0, committed[0] + PAIRS);     // one sample = PAIRS words
    push_wr();
    one_sample();
    // record the last real sample per channel-pair slot of stream 0
    uint32_t lp[PAIRS][2] = {{0,0},{0,0}};
    for (auto &p : caps) if (p.slot / PAIRS == 0) { int pp = p.slot % PAIRS; lp[pp][0] = p.l; lp[pp][1] = p.r; }
    uint32_t u0 = under_of(0);
    // now fully starved: stream 0 must underrun and REPEAT its last sample
    dut->underrun_silence_i = 0;          // repeat-last policy
    one_sample();
    int s0pairs = 0; bool repeat_ok = true;
    for (auto &p : caps) if (p.slot / PAIRS == 0) {
      int pp = p.slot % PAIRS; s0pairs++;
      if (p.l != lp[pp][0] || p.r != lp[pp][1]) repeat_ok = false;
    }
    ck_true("phase3 underrun still emits s0 pairs", s0pairs == PAIRS);
    ck_true("phase3 underrun repeats last sample",  repeat_ok);
    ck_true("phase3 underrun count grew",           under_of(0) > u0);
    ck_true("phase3 cadence held under underrun",   (int)caps.size() == SLOTS);
    // policy switch: silence
    dut->underrun_silence_i = 1;
    one_sample();
    bool silence_ok = true; int s0p2 = 0;
    for (auto &p : caps) if (p.slot / PAIRS == 0) { s0p2++; if (p.l || p.r) silence_ok = false; }
    ck_true("phase3 silence policy emits zeros", silence_ok && s0p2 == PAIRS);
    // read pointer must NOT advance during underrun (nothing consumed)
    uint32_t rd_before = rd_of(0);
    one_sample();
    ck("phase3 rd_ptr frozen on underrun", rd_of(0), rd_before);
  }

  // ====================================================================
  //  Phase 4 - overrun: lap the reader, count + fast-forward one lap
  // ====================================================================
  {
    // stream 1 is currently frozen/drained. Set its write pointer a full
    // ring + a bit ahead of the read pointer while the engine is idle: the
    // idle overrun scan must drop exactly one lap and count it.
    uint32_t rd1 = rd_of(1);
    uint32_t o1  = over_of(1);
    committed[1] = rd1 / 8;               // resync the model to the reader
    feed_to(1, rd1 / 8 + LEN / 8 + 4);    // fill = LEN + 32 bytes > LEN => overrun
    wrv[1] = (rd1 / 8 + LEN / 8 + 4) * 8;
    push_wr();
    // step until the idle scan drops a lap (over increments); the lap-drop is
    // in PT_IDLE and does not consume, so rd is EXACTLY one lap on at that edge
    int gov = 0; while (over_of(1) == o1 && gov++ < 4 * SAMPLE_DIV) tick();
    ck("phase4 overrun counted once", over_of(1), (uint64_t)(o1 + 1));
    ck("phase4 rd fast-forwarded one lap", rd_of(1), (uint64_t)(rd1 + LEN));
    // fill is now bounded (<= LEN): no runaway repeated counting
    run(2 * SAMPLE_DIV);
    ck_true("phase4 overrun not double-counted", over_of(1) == o1 + 1);
    // engine still alive: stream 1 keeps emitting on the next samples
    caps.clear();
    // refeed to keep it healthy and confirm pairs resume
    committed[1] = rd_of(1) / 8; wrv[1] = committed[1] * 8;
    auto_feed = true;
    one_sample();
    int s1pairs = 0; for (auto &p : caps) if (p.slot / PAIRS == 1) s1pairs++;
    ck_true("phase4 stream resumes after overrun", s1pairs == PAIRS);
  }

  // ====================================================================
  //  Phase 5 - per-stream enable gating
  // ====================================================================
  {
    auto_feed = true;
    dut->stream_en_i = 0x1;               // only stream 0 emits
    caps.clear();
    one_sample();
    int s0 = 0, s1 = 0;
    for (auto &p : caps) { if (p.slot / PAIRS == 0) s0++; else s1++; }
    ck_true("phase5 disabled stream1 emits nothing", s1 == 0);
    ck_true("phase5 enabled  stream0 still emits",   s0 == PAIRS);
    ck_true("phase5 cadence = only enabled slots",   (int)caps.size() == PAIRS);
    dut->stream_en_i = 0x3;
  }

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  delete dut;
  return fail ? 1 : 0;
}

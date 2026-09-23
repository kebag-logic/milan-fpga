// Reviewer probe (R262-1, issue #74 item 2): drives the PR's own
// media_grid_align_wrap (real KL_media_grid_align + KL_media_nco +
// KL_chan_map_capture) with an independent physical-grid model and an
// independent marker-to-tick clearance measurement. Not part of the repo.
//
// usage: probe <mode> <lead> <dir> <jit> <seed> [settle_cyc] [win_cyc] [nwin]
//   mode : engage  - deselect, anchor, select so the next frame engages
//                    <lead> RTL edges after a sampled tick, then settle and
//                    count the real junction counters in windows
//          passage - deselected free-run from <lead>, count over settle_cyc
//   dir  : slow (the -10.64 ppm plan, frames slower than ticks)
//          fast (the mirrored +10.64 ppm feed)
//   jit  : each marker is delivered 0..jit edges late, uniform (0 = none)
//
// RTL pairing (verified against the wrap): at clock edge k the DUT samples
// frame_ev_i as driven before edge k and tick_i = the tick_o that edge k-1
// produced. So a tick_o observed after edge k is a tick SAMPLED at edge k+1.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <climits>
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"

static Vmedia_grid_align_wrap* dut;
static double frame_period = 0.0, frame_acc = 0.0;
static int jit = 0;
static uint32_t rng = 1;
static long edge = 0;                 // index of the edge the next cyc() drives
static std::deque<long> due;          // edges at which delayed markers fire
static long last_tick_edge = LONG_MIN / 2;   // RTL-sampled tick edges
static long pend_mark = -1;           // marker edge awaiting its next tick
static long clear_min = LONG_MAX, coincide = 0, last_mark_phase = -1;
static bool measuring = false;

static uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

static void cyc() {
  if (frame_period > 0.0) {
    frame_acc += 1.0;
    if (frame_acc >= frame_period) {
      frame_acc -= frame_period;
      long d = jit > 0 ? static_cast<long>(rnd() % static_cast<uint32_t>(jit + 1)) : 0;
      due.push_back(edge + d);
    }
  }
  bool fev = false;
  while (!due.empty() && due.front() <= edge) { fev = true; due.pop_front(); }
  dut->frame_ev_i = fev;
  dut->clk = 0; dut->eval();
  dut->clk = 1; dut->eval();
  // this edge (index `edge`) sampled fev; tick_i sampled here was produced
  // by the previous edge and was recorded as last_tick_edge == edge then.
  if (fev) {
    long after = edge - last_tick_edge;           // 0 = coincident
    last_mark_phase = after;
    if (measuring) {
      if (after == 0) coincide++;
      if (after < clear_min) clear_min = after;
    }
    pend_mark = edge;
  }
  if (dut->tick_o) {                              // sampled at edge+1
    long tick_edge = edge + 1;
    if (measuring && pend_mark >= 0 && pend_mark != tick_edge) {
      long before = tick_edge - pend_mark;
      if (before < clear_min) clear_min = before;
    }
    pend_mark = -1;
    last_tick_edge = tick_edge;
  }
  edge++;
}
static void run(long n) { for (long i = 0; i < n; i++) cyc(); }

int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char* mode = argv[1];
  long lead = atol(argv[2]);
  bool fast = strcmp(argv[3], "fast") == 0;
  jit = atoi(argv[4]);
  rng = static_cast<uint32_t>(strtoul(argv[5], nullptr, 0)); if (!rng) rng = 1;
  long settle = argc > 6 ? atol(argv[6]) : 100000000L;
  long win = argc > 7 ? atol(argv[7]) : 20000000L;
  int nwin = argc > 8 ? atoi(argv[8]) : 5;

#ifndef PROBE_CLK_HZ
#define PROBE_CLK_HZ 100e6   // must match the wrap's CLK_FREQ_HZ_P
#endif
  // the physical grid is the 391/1591 plan off the 100 MHz reference
  // whatever the datapath clock; only the cycle count per frame scales
  const double clk = PROBE_CLK_HZ, nominal = 48000.0;
  const double plan_hz = 100e6 * (391.0 / 1591.0) / 512.0;
  const double plan = plan_hz;
  const double plan_period = clk / plan;
  const double fast_period = plan_period * (plan / nominal) * (plan / nominal);
  const double period = fast ? fast_period : plan_period;

  Verilated::commandArgs(argc, argv);
  dut = new Vmedia_grid_align_wrap;
  dut->rst_n = 0; dut->sel_i = 0; dut->frame_ev_i = 0;
  for (int i = 0; i < 8; i++) { dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); edge++; }
  dut->rst_n = 1;

  // anchor: free-run, find a tick_o (sampled at the next edge), then place
  // the next undelayed frame `lead` edges after that sampled tick
  int saved_jit = jit; jit = 0;
  frame_period = period;
  run(20000);
  while (!dut->tick_o) cyc();
  // next cyc() drives edge E = the sampled-tick edge; a frame firing on the
  // (lead+1)-th cyc() lands on edge E + lead
  frame_acc = frame_period - 0.5 - static_cast<double>(lead);
  run(lead);
  if (strcmp(mode, "engage") == 0) dut->sel_i = 1;
  cyc();                                            // the anchored frame
  long anchored_phase = last_mark_phase;
  int engaged0 = dut->engaged_o;
  jit = saved_jit;

  long d0 = dut->tdm_dup_cnt_o, s0 = dut->tdm_skip_cnt_o;
  if (strcmp(mode, "passage") == 0) {
    run(settle);
    printf("mode=passage dir=%s lead=%ld jit=%d seed=%s anchored_phase=%ld dups=%ld skips=%ld net=%ld\n",
           fast ? "fast" : "slow", lead, jit, argv[5], anchored_phase,
           (long)dut->tdm_dup_cnt_o - d0, (long)dut->tdm_skip_cnt_o - s0,
           ((long)dut->tdm_dup_cnt_o - d0) - ((long)dut->tdm_skip_cnt_o - s0));
    delete dut; return 0;
  }
  run(settle);
  long acq_d = (long)dut->tdm_dup_cnt_o - d0, acq_s = (long)dut->tdm_skip_cnt_o - s0;
  measuring = true; clear_min = LONG_MAX; coincide = 0;
  long wd0 = dut->tdm_dup_cnt_o, ws0 = dut->tdm_skip_cnt_o;
  printf("mode=engage dir=%s lead=%ld jit=%d seed=%s anchored_phase=%ld engaged_on_frame=%d acq_dups=%ld acq_skips=%ld",
         fast ? "fast" : "slow", lead, jit, argv[5], anchored_phase, engaged0, acq_d, acq_s);
  printf(" win=");
  for (int w = 0; w < nwin; w++) {
    long a = dut->tdm_dup_cnt_o, b = dut->tdm_skip_cnt_o;
    run(win);
    printf("%s%ld/%ld", w ? "," : "", (long)dut->tdm_dup_cnt_o - a, (long)dut->tdm_skip_cnt_o - b);
  }
  printf(" lock_dups=%ld lock_skips=%ld clear_min=%ld coincidences=%ld err=%d u=%d engaged=%d",
         (long)dut->tdm_dup_cnt_o - wd0, (long)dut->tdm_skip_cnt_o - ws0, clear_min, coincide,
         (int)(int16_t)dut->err_cyc_o, (int)(int16_t)dut->u_o, (int)dut->engaged_o);
  if (argc > 9 && strcmp(argv[9], "inject") == 0) {
    // a held frame: the physical grid steps one whole period late
    long a = dut->tdm_dup_cnt_o, b = dut->tdm_skip_cnt_o;
    frame_acc -= frame_period;
    run(1000000);
    long hd = (long)dut->tdm_dup_cnt_o - a, hs = (long)dut->tdm_skip_cnt_o - b;
    // a surplus frame: one extra marker a quarter frame after a real one
    a = dut->tdm_dup_cnt_o; b = dut->tdm_skip_cnt_o;
    while (!dut->frame_ev_i) cyc();
    run(520);
    due.push_back(edge);
    run(1000000);
    long sd = (long)dut->tdm_dup_cnt_o - a, ss = (long)dut->tdm_skip_cnt_o - b;
    // a whole-period early step: the grid jumps one period ahead
    a = dut->tdm_dup_cnt_o; b = dut->tdm_skip_cnt_o;
    frame_acc += frame_period - 1.0;
    run(1000000);
    long ed = (long)dut->tdm_dup_cnt_o - a, es = (long)dut->tdm_skip_cnt_o - b;
    printf(" held=%ld/%ld surplus=%ld/%ld early_step=%ld/%ld engaged_after=%d",
           hd, hs, sd, ss, ed, es, (int)dut->engaged_o);
  }
  printf("\n");
  delete dut;
  return 0;
}

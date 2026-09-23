// Review probe P-LOOP: the real KL_media_grid_align + KL_media_nco +
// KL_chan_map_capture (tb/verilator/media_grid_align's wrap, unmodified),
// driven with sim_main.cpp's own grid model, marker-jitter model and
// clearance tracker (copied semantics), to test two doc claims beyond the
// suite's fixed arms:
//   passage <slow|fast> <lead> <jitter 0|1> <seed>
//     one free-running passage; prints dups, skips, net, and the dither
//     depth: how far a near-tick marker-to-nearest-tick offset ever falls
//     back behind the furthest offset already reached in the passage's
//     direction (1 = the marker dithers between two adjacent cycles)
//   acq <slow|fast> <lead> <jitter 0|1> <seed>
//     engage as `lock` does, run 2.5 s from engagement and report ticks the
//     NCO dropped (a tick-to-tick gap over 2100 edges), whether u reached
//     the +/-3200 rail, the net junction count, and the min clearance over
//     the last 0.5 s
//   lock <slow|fast> <lead> <seed>
//     engage with the frame `lead` edges after a tick, 1 edge of jitter,
//     settle 1 s, then 1 s at lock: dups, skips, min clearance
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <climits>
#include <algorithm>
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"
constexpr double kClkHz = 100e6, kNominalHz = 48000.0;
constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0;
constexpr double kPlanPeriod = kClkHz / PLAN_A;
constexpr double kFastPeriod = kPlanPeriod * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);
struct H {
  Vmedia_grid_align_wrap* dut;
  double frame_period = 0, frame_acc = 0;
  bool marker_jitter = false, late_frame = false, tick_q = false;
  uint32_t rng = 0x74A197u;
  long gap = 0, max_gap = 0, drops = 0;
  long edges_since_tick = 0, mark_phase = -1, last_phase = -1, clear_min = LONG_MAX;
  // signed-offset tracking for passages
  long pending_prev = -1;           // this period's marker distance after the previous tick
  bool slow_dir = true; long run_ext = 0; bool have_ext = false;
  long max_spread = 0; long n_near = 0;
  uint32_t next_rand() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }
  void note_offset(long o) {
    if (std::labs(o) <= 6) {
      n_near++;
      if (!have_ext) { run_ext = o; have_ext = true; }
      if (slow_dir) { run_ext = std::max(run_ext, o); max_spread = std::max(max_spread, run_ext - o); }
      else          { run_ext = std::min(run_ext, o); max_spread = std::max(max_spread, o - run_ext); }
    }
  }
  void cyc() {
    bool fev = late_frame; late_frame = false;
    if (frame_period > 0.0) {
      frame_acc += 1.0;
      if (frame_acc >= frame_period) {
        frame_acc -= frame_period;
        if (marker_jitter && (next_rand() & 1u)) late_frame = true; else fev = true;
      }
    }
    dut->frame_ev_i = fev;
    dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval();
    bool tk = dut->tick_o;
    gap++; if (tk) { if (gap > 2100) drops++; max_gap = std::max(max_gap, gap); gap = 0; }
    // sim_main.cpp track_clearance(), verbatim semantics
    if (tick_q) {
      if (mark_phase > 0) {
        long after = edges_since_tick + 1 - mark_phase;
        clear_min = std::min(clear_min, after);
        note_offset(mark_phase <= after ? mark_phase : -after);
      }
      edges_since_tick = 0; mark_phase = -1;
    } else edges_since_tick++;
    if (fev) {
      mark_phase = tick_q ? 0 : edges_since_tick;
      last_phase = mark_phase;
      clear_min = std::min(clear_min, mark_phase);
      if (mark_phase == 0) note_offset(0);
    }
    tick_q = tk;
  }
  void run(long n) { for (long i = 0; i < n; i++) cyc(); }
  void anchor_grid(double period, long lead) {   // sim_main.cpp anchor_grid()
    dut->sel_i = 0; marker_jitter = false; frame_period = period;
    run(10000);
    while (!dut->tick_o) cyc();
    frame_acc = frame_period - 0.5 - (double)lead;
    run(lead);
  }
};
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
  const bool passage = !strcmp(argv[1], "passage");
  const bool fast = !strcmp(argv[2], "fast");
  const long lead = atol(argv[3]);
  const double period = fast ? kFastPeriod : kPlanPeriod;
  H h; Vmedia_grid_align_wrap dut; h.dut = &dut;
  dut.rst_n = 0; dut.sel_i = 0; dut.frame_ev_i = 0;
  for (int i = 0; i < 8; i++) { dut.clk = 0; dut.eval(); dut.clk = 1; dut.eval(); }
  dut.rst_n = 1;
  if (passage) {
    const int jit = atoi(argv[4]);
    h.rng ^= (uint32_t)atol(argv[5]) * 2654435761u;
    h.frame_period = period; h.run(2000000);
    h.anchor_grid(period, lead);
    h.marker_jitter = jit != 0;
    long d0 = dut.tdm_dup_cnt_o, s0 = dut.tdm_skip_cnt_o;
    h.max_spread = 0; h.have_ext = false; h.n_near = 0; h.slow_dir = !fast;
    h.run(10000000);
    long d = dut.tdm_dup_cnt_o - d0, s = dut.tdm_skip_cnt_o - s0;
    printf("passage %s lead=%ld jitter=%d seed=%s: dups=%ld skips=%ld net=%+ld "
           "near-tick markers=%ld dither depth=%ld\n",
           fast ? "fast" : "slow", lead, jit, argv[5], d, s, d - s, h.n_near, h.max_spread);
    return 0;
  }
  if (!strcmp(argv[1], "acq")) {
    const int jit = atoi(argv[4]);
    h.rng ^= (uint32_t)atol(argv[5]) * 2654435761u;
    h.frame_period = period; h.run(2000000);
    h.anchor_grid(period, lead);
    dut.sel_i = 1; h.cyc();
    const long ph = h.last_phase;
    h.marker_jitter = jit != 0;
    h.drops = 0; h.max_gap = 0;
    long d0 = dut.tdm_dup_cnt_o, s0 = dut.tdm_skip_cnt_o; bool rail = false;
    for (long i = 0; i < 200000000; i++) { h.cyc(); if (std::abs((int)(int16_t)dut.u_o) == 3200) rail = true; }
    h.clear_min = LONG_MAX;
    long d1 = dut.tdm_dup_cnt_o, s1 = dut.tdm_skip_cnt_o;
    h.run(50000000);
    printf("acq %s lead=%ld jitter=%d seed=%s: phase=%ld dropped_ticks=%ld max_tick_gap=%ld u_rail=%d "
           "acq dups=%ld skips=%ld net=%+ld | last 0.5 s dups=%ld skips=%ld min clearance=%ld\n",
           fast ? "fast" : "slow", lead, jit, argv[5], ph, h.drops, h.max_gap, (int)rail,
           d1 - d0, s1 - s0, (d1 - d0) - (s1 - s0),
           (long)(dut.tdm_dup_cnt_o - d1), (long)(dut.tdm_skip_cnt_o - s1), h.clear_min);
    return 0;
  }
  h.rng ^= (uint32_t)atol(argv[4]) * 2654435761u;
  h.frame_period = period; h.run(2000000);
  h.anchor_grid(period, lead);
  dut.sel_i = 1; h.cyc();
  const long eng = dut.engaged_o, ph = h.last_phase;
  h.marker_jitter = true;
  h.run(100000000);                                  // settle 1 s
  h.clear_min = LONG_MAX;
  long d0 = dut.tdm_dup_cnt_o, s0 = dut.tdm_skip_cnt_o;
  h.run(100000000);                                  // 1 s at lock
  printf("lock %s lead=%ld seed=%s: engaged=%ld phase=%ld -> at lock dups=%ld skips=%ld "
         "min clearance=%ld err=%d engaged=%d\n", fast ? "fast" : "slow", lead, argv[4], eng, ph,
         (long)(dut.tdm_dup_cnt_o - d0), (long)(dut.tdm_skip_cnt_o - s0), h.clear_min,
         (int)(int16_t)dut.err_cyc_o, (int)dut.engaged_o);
  return 0;
}

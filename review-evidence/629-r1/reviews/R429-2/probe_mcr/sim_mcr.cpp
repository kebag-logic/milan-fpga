// Reviewer probe R429-2: does a second restart request d cycles after a
// source-change edge reach the wire as a second mr toggle?
// KL_media_clock_restart at head c554ae51, N_TALKERS_P=2:
//   talker 0 = an AAF output, one PDU every A cycles;
//   talker 1 = the CRF output, one PDU every 16*A cycles.
// Each trial: reset, run to steady state, change clk_src at a swept phase,
// optionally pulse restart_p_i d cycles later, count mr_o changes per talker
// over a window long enough for two 8-PDU holds on the CRF output.
#include "VKL_media_clock_restart.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>

static const int A = 100;          // AAF PDU period, cycles (125 us scaled)
static const int C = 16 * A;       // CRF PDU period
static vluint64_t cyc;

static void tick(VKL_media_clock_restart* m) {
  m->clk_i = 0; m->eval();
  m->clk_i = 1; m->eval();
  ++cyc;
}

// returns toggles per talker packed: t0 + 100*t1
static int trial(int phase, int d) {
  VKL_media_clock_restart* m = new VKL_media_clock_restart;
  cyc = 0;
  m->rst_n = 0; m->restart_p_i = 0; m->clk_src_i = 2; m->streaming_i = 3;
  m->frame_p_i = 0; m->frame_idx_i = 0; m->frame_mr_i = 0;
  for (int i = 0; i < 4; ++i) tick(m);
  m->rst_n = 1;
  const int settle = 20 * C;
  const int t0 = settle + phase;
  const int end = t0 + 24 * C;
  int prev0 = -1, prev1 = -1, n0 = 0, n1 = 0;
  for (int t = 0; t < end; ++t) {
    m->restart_p_i = 0; m->frame_p_i = 0;
    if (t == t0) m->clk_src_i = 3;                 // the switch
    if (d >= 0 && t == t0 + d) m->restart_p_i = 1; // the second request
    // feed reports: AAF at t % A == 7, CRF at t % C == 53 (never same cycle)
    if (t % A == 7) { m->frame_p_i = 1; m->frame_idx_i = 0; m->frame_mr_i = m->mr_o & 1; }
    else if (t % C == 53) { m->frame_p_i = 1; m->frame_idx_i = 1; m->frame_mr_i = (m->mr_o >> 1) & 1; }
    tick(m);
    int b0 = m->mr_o & 1, b1 = (m->mr_o >> 1) & 1;
    if (t >= t0) { if (prev0 >= 0 && b0 != prev0) ++n0; if (prev1 >= 0 && b1 != prev1) ++n1; }
    prev0 = b0; prev1 = b1;
  }
  delete m;
  return n0 + 100 * n1;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  // phases sweep one full CRF period in steps of 7 cycles
  struct Case { const char* name; int dmin; int dmax; } cases[] = {
    {"no second request (design)", -1, -1},
    {"second request 1..4 cycles after the edge (era-start lock-fall mutant)", 1, 4},
    {"second request 0..A cycles after the edge (new input's first PDU, no re-seed mutant)", 0, A},
  };
  for (auto& k : cases) {
    long trials = 0, aaf2 = 0, crf2 = 0, any2 = 0, aaf1 = 0, crf1 = 0;
    for (int ph = 0; ph < C; ph += 7) {
      int dlo = k.dmin, dhi = k.dmax;
      for (int d = dlo; d <= dhi; d += (dhi - dlo > 10 ? 9 : 1)) {
        int r = trial(ph, d);
        int a = r % 100, c = r / 100;
        ++trials;
        if (a == 1) ++aaf1; if (c == 1) ++crf1;
        if (a >= 2) ++aaf2; if (c >= 2) ++crf2;
        if (a >= 2 || c >= 2) ++any2;
        if (d < 0) break;
      }
    }
    printf("%s: trials %ld; AAF output 1 toggle %ld, >=2 toggles %ld; "
           "CRF output 1 toggle %ld, >=2 toggles %ld; any output >=2: %ld\n",
           k.name, trials, aaf1, aaf2, crf1, crf2, any2);
  }
  return 0;
}

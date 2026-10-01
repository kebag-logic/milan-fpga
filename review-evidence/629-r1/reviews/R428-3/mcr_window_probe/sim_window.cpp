// Reviewer probe (PR #631, head a463a1de): where does each output's merge
// window end after a media-clock source change? Drives the unmodified
// hdl/ieee1722/avtp/KL_media_clock_restart.sv (N_TALKERS_P = 2):
//   talker 0: an AAF-like output, a PDU launched every A cycles;
//   talker 1: a CRF-like output, a PDU launched every C = 16 A cycles,
//             offset OFF cycles;
// each PDU latches mr_o at launch and is reported LAT cycles later; an AAF
// report wins a same-cycle conflict and the CRF one waits a cycle.
// For every switch phase and every second-request delay d, the probe counts
// wire toggles per output and compares with the design page's statement
// (MEDIA_CLOCK_FOLLOWING.md:802-807): a second request merges while the
// output's first PDU launched after the switch has not been reported.
// Usage: sim_window A LAT OFF phase_step d_step d_max
#include "VKL_media_clock_restart.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>

static long A, C, LAT, OFF;

struct Out { int tog[2]; long first_rep[2]; };

static Out trial(long t0, long d) {
  VKL_media_clock_restart m;
  m.clk_i = 0; m.rst_n = 0; m.restart_p_i = 0; m.clk_src_i = 0;
  m.streaming_i = 3; m.frame_p_i = 0; m.frame_idx_i = 0; m.frame_mr_i = 0;
  for (int i = 0; i < 4; ++i) { m.clk_i = 0; m.eval(); m.clk_i = 1; m.eval(); }
  m.rst_n = 1;
  long due[2] = {-1, -1}, launch[2] = {-1, -1};
  int lvl[2] = {0, 0}, last[2] = {-1, -1}, pre[2] = {-1, -1};
  Out o = {{0, 0}, {-1, -1}};
  const long end = t0 + 24 * C;
  for (long t = 0; t < end; ++t) {
    if (t == t0) { pre[0] = m.mr_o & 1; pre[1] = (m.mr_o >> 1) & 1; }
    m.restart_p_i = (d >= 0 && t == t0 + d);
    m.clk_src_i = t >= t0 ? 2 : 0;
    m.frame_p_i = 0;
    int rep = -1;
    if (due[0] >= 0 && due[0] <= t) rep = 0;
    else if (due[1] >= 0 && due[1] <= t) rep = 1;
    if (rep >= 0) {
      m.frame_p_i = 1; m.frame_idx_i = rep; m.frame_mr_i = lvl[rep];
      if (t >= t0 && last[rep] >= 0 && lvl[rep] != last[rep]) ++o.tog[rep];
      // the RTL's own rule (KL_media_clock_restart.sv:236-246): the window
      // ends at the first PDU reported at the adopted (new) level
      if (o.first_rep[rep] < 0 && t >= t0 && lvl[rep] != pre[rep]) o.first_rep[rep] = t;
      last[rep] = lvl[rep]; due[rep] = -1;
    }
    if (t > 8 && t % A == 0) { lvl[0] = m.mr_o & 1; due[0] = t + LAT; launch[0] = t; }
    if (t > 8 && t % C == OFF) { lvl[1] = (m.mr_o >> 1) & 1; due[1] = t + LAT; launch[1] = t; }
    m.clk_i = 0; m.eval(); m.clk_i = 1; m.eval();
  }
  return o;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  A = atol(argv[1]); C = 16 * A; LAT = atol(argv[2]); OFF = atol(argv[3]);
  const long pstep = atol(argv[4]), dstep = atol(argv[5]), dmax = atol(argv[6]);
  long trials = 0, agree[2] = {0, 0}, near[2] = {0, 0}, far_bad[2] = {0, 0};
  long design_one = 0, design_n = 0;
  for (long ph = 0; ph < C; ph += pstep) {
    const long t0 = 4 * C + ph;
    Out base = trial(t0, -1);
    ++design_n;
    if (base.tog[0] == 1 && base.tog[1] == 1) ++design_one;
    for (long d = 0; d <= dmax; d += dstep) {
      Out o = trial(t0, d);
      ++trials;
      for (int k = 0; k < 2; ++k) {
        // statement: merges (one toggle) iff t0 + d is not after the report
        // of the first PDU at the adopted level (launched after the switch)
        const long edge = base.first_rep[k] - t0;
        const bool pred_one = d <= edge;
        const bool obs_one = o.tog[k] == 1;
        if (pred_one == obs_one) ++agree[k];
        else if (labs(d - edge) <= 3) ++near[k];
        else ++far_bad[k];
      }
    }
  }
  printf("A=%ld C=%ld LAT=%ld OFF=%ld: switch alone one toggle per output %ld/%ld; "
         "second-request trials %ld; agree AAF %ld CRF %ld; disagreements within "
         "3 cycles of the edge AAF %ld CRF %ld; elsewhere AAF %ld CRF %ld\n",
         A, C, LAT, OFF, design_one, design_n, trials, agree[0], agree[1],
         near[0], near[1], far_bad[0], far_bad[1]);
  return (far_bad[0] || far_bad[1] || design_one != design_n) ? 1 : 0;
}

// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (round R429-3) for #629: drives the UNMODIFIED
// hdl/ieee1722/avtp/KL_media_clock_restart.sv (N_TALKERS_P=2) with one AAF
// output (context 0, a PDU every A cycles) and one CRF output (context 1, a
// PDU every C cycles). Each output latches mr_o at launch and the PDU is
// reported LAT cycles later on frame_p_i/frame_idx_i/frame_mr_i (one report
// per cycle; a collision defers the later one by a cycle). Both outputs
// stream throughout. At cycle SW the clock-source index changes 2 -> 3 (an
// AAF-to-AAF switch). Written independently of the author's harness.
//
// Scenarios (argv[1]):
//   design      the source change only
//   era<d>      plus one restart pulse d cycles after the switch (the
//               "era-start lock clear on disrupt_p" mutant), d = 1..4
//   echo<us>    plus one restart pulse <us> microseconds after the switch
//               (the "no re-seed" mutant: a stale-seed echo at the new
//               talker's first accepted PDU)
// Usage: r429_mcr_switch <scenario> <A> <C> <LAT> <nphase> <obs_cycles>
// Prints, over nphase switch phases spread over one CRF period: trials,
// trials with exactly one wire toggle on both outputs, trials with >= 2 on
// the AAF output, >= 2 on the CRF output, and 0 on any output.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <string>
#include "VKL_media_clock_restart.h"
#include "verilated.h"

struct Rep { long long at; int idx; int mr; };

static void tick(VKL_media_clock_restart* m) {
  m->clk_i = 0; m->eval();
  m->clk_i = 1; m->eval();
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  std::string scen = argv[1];
  long long A = atoll(argv[2]), C = atoll(argv[3]), LAT = atoll(argv[4]);
  int nphase = atoi(argv[5]);
  long long OBS = atoll(argv[6]);
  long long extra = -1;               // restart pulse offset after SW, cycles
  if (scen.rfind("era", 0) == 0) extra = atoll(scen.c_str() + 3);
  else if (scen.rfind("echo", 0) == 0) extra = atoll(scen.c_str() + 4) * A / 125;
  else if (scen != "design") { fprintf(stderr, "bad scenario\n"); return 2; }
  int trials = 0, one_both = 0, aaf2 = 0, crf2 = 0, any0 = 0;
  for (int ph = 0; ph < nphase; ph++) {
    VKL_media_clock_restart* m = new VKL_media_clock_restart;
    m->clk_i = 0; m->rst_n = 0; m->restart_p_i = 0; m->clk_src_i = 2;
    m->streaming_i = 3; m->frame_p_i = 0; m->frame_idx_i = 0; m->frame_mr_i = 0;
    for (int i = 0; i < 4; i++) tick(m);
    m->rst_n = 1;
    // pre-roll: 40 CRF periods so every hold is satisfied, then the switch
    // lands at a phase spread over one CRF period
    long long SW = 40 * C + (C * ph) / nphase + 7;
    long long END = SW + OBS;
    std::deque<Rep> q;
    int last_mr[2] = {-1, -1}, tog[2] = {0, 0};
    // the source index had been 2 since reset; the restart module resets its
    // shadow to 0, so the 0 -> 2 change at reset is itself one request in
    // the pre-roll; it is settled long before SW.
    for (long long cyc = 0; cyc < END; cyc++) {
      // launches (latch the level presented by the module this cycle)
      for (int t = 0; t < 2; t++) {
        long long P = t == 0 ? A : C;
        if (cyc % P == 0) {
          int mr = (m->mr_o >> t) & 1;
          q.push_back({cyc + LAT, t, mr});
          if (cyc >= SW) {
            if (last_mr[t] >= 0 && mr != last_mr[t]) tog[t]++;
          }
          last_mr[t] = mr;
        }
      }
      m->clk_src_i = cyc >= SW ? 3 : 2;
      m->restart_p_i = (extra >= 0 && cyc == SW + extra) ? 1 : 0;
      m->frame_p_i = 0;
      if (!q.empty() && q.front().at <= cyc) {
        m->frame_p_i = 1; m->frame_idx_i = q.front().idx; m->frame_mr_i = q.front().mr;
        q.pop_front();
      }
      tick(m);
    }
    trials++;
    if (tog[0] == 1 && tog[1] == 1) one_both++;
    if (tog[0] >= 2) aaf2++;
    if (tog[1] >= 2) crf2++;
    if (tog[0] == 0 || tog[1] == 0) any0++;
    m->final();
    delete m;
  }
  printf("%-8s A=%lld C=%lld LAT=%lld obs=%lld: trials %d; one toggle on both %d; "
         "AAF>=2 %d; CRF>=2 %d; an output with 0 %d\n",
         scen.c_str(), A, C, LAT, OBS, trials, one_both, aaf2, crf2, any0);
  return 0;
}

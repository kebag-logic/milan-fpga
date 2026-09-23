// Review probe P-NCO: KL_media_nco alone (the shipping 100 MHz / 48 kHz
// shape), servo engaged, no loop, no frame model, no jitter. One
// servo_trim_i step U0 -> U1 is applied k edges after tick t (the tick
// counter keeps running through the pre-step edges, so a tick inside them
// is seen). A tick-to-tick gap over 2100 edges is a dropped tick.
//   probe_nco <U0> <U1> <ticks> <k_lo> <k_hi>
#include <cstdio>
#include <cstdlib>
#include <map>
#include "VKL_media_nco.h"
#include "verilated.h"
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const int U0 = atoi(argv[1]), U1 = atoi(argv[2]), NT = atoi(argv[3]);
  const int KLO = atoi(argv[4]), KHI = atoi(argv[5]);
  long trials = 0, drops = 0; std::map<long, long> by_k, by_gap;
  for (int t = 0; t < NT; t++) {
    for (int k = KLO; k <= KHI; k++) {
      VKL_media_nco d;
      d.rst_n = 0; d.trim_i = 0; d.servo_trim_i = U0; d.servo_en_i = 1;
      for (int i = 0; i < 4; i++) { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); }
      d.rst_n = 1;
      int ticks = 0;
      while (ticks <= t) { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); if (d.tick_o) ticks++; }
      long gap = 0, maxgap = 0;
      for (int i = 0; i < k + 9000; i++) {
        if (i == k) d.servo_trim_i = U1;
        d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); gap++;
        if (d.tick_o) { if (gap > maxgap) maxgap = gap; gap = 0; }
      }
      trials++;
      if (maxgap > 2100) { drops++; by_k[k]++; by_gap[maxgap]++; }
    }
  }
  printf("P-NCO step %d -> %d, ticks 0..%d, offsets %d..%d: %ld of %ld trials dropped ticks\n",
         U0, U1, NT - 1, KLO, KHI, drops, trials);
  for (auto& kv : by_k)   printf("  step applied %ld edges after the tick: %ld drops\n", kv.first, kv.second);
  for (auto& kv : by_gap) printf("  tick-to-tick gap %ld edges: %ld times\n", kv.first, kv.second);
  return 0;
}

// SPDX-License-Identifier: CERN-OHL-W-2.0
// Base-versus-head lockstep main (reviewer probe). usage: Vls_wrap <seed> <cycles>
// Compares every output port of the two copies at every cycle after the
// first reset, mid-run resets included. Unreset state starts random
// (+verilator+rand+reset+2), independently per variable, so the base's and
// the head's memories start with different contents.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include "Vls_wrap.h"
#include "verilated.h"
#include "drive.hpp"

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  uint64_t seed = std::strtoull(argv[1], nullptr, 0);
  uint64_t cycles = std::strtoull(argv[2], nullptr, 0);
  Vls_wrap* d = new Vls_wrap;
  Drv g(seed, N_CTX);
  bool armed = false;
  uint64_t mism = 0, resets = 0;
  std::vector<uint64_t> per(N_OUT, 0), act(N_OUT, 0);
  int shown = 0;
  bool was_reset = true;
  for (uint64_t c = 0; c < cycles; ++c) {
    g.begin_cycle();
    drive_inputs(d, g);
    d->clk_i = 0;
    d->eval();
    if (!g.in_reset() && was_reset) { armed = true; resets++; }
    was_reset = g.in_reset();
    if (armed) {
      uint64_t mm = d->mm_o;
      uint64_t ac = d->act_o;
      for (int i = 0; i < N_OUT; ++i) {
        if ((mm >> i) & 1) per[i]++;
        if ((ac >> i) & 1) act[i]++;
      }
      if (mm) {
        mism++;
        if (shown < 5) { shown++; printf("MISMATCH cycle %llu mask %llx\n", (unsigned long long)c, (unsigned long long)mm); }
      }
    }
    d->clk_i = 1;
    d->eval();
  }
  printf("seed %llu cycles %llu resets %llu mismatching_cycles %llu\n", (unsigned long long)seed,
         (unsigned long long)cycles, (unsigned long long)resets, (unsigned long long)mism);
  for (int i = 0; i < N_OUT; ++i)
    printf("  %-24s active %10llu mismatch %llu\n", OUT_NAMES[i], (unsigned long long)act[i], (unsigned long long)per[i]);
  delete d;
  return mism ? 1 : 0;
}

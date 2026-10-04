// SPDX-License-Identifier: CERN-OHL-W-2.0
#include <cstdio>
#include "Voor.h"
#include "verilated.h"
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Voor d;
  d.w64_i = 0x1122334455667788ULL; d.w48_i = 0xAABBCCDDEEFFULL;
  d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval();
  for (int i = 0; i < 2; ++i) {
    d.idx_i = i; d.eval();
    std::printf("idx %d: r64 %016llx r48 %012llx\n", i,
                (unsigned long long)d.r64_o, (unsigned long long)d.r48_o);
  }
  return 0;
}

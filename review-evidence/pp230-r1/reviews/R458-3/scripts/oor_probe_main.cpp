#include "Voor.h"
#include "verilated.h"
#include <cstdio>
int main(int c, char** v) { Verilated::commandArgs(c, v); Voor m; m.d_i = 0x1122334455667788ull;
  m.clk_i = 0; m.eval(); m.clk_i = 1; m.eval(); m.idx_i = 0; m.eval(); unsigned long long a = m.q_o;
  m.idx_i = 1; m.eval(); unsigned long long b = m.q_o;
  printf("idx0=%016llx idx1(out-of-range)=%016llx\n", a, b); return 0; }

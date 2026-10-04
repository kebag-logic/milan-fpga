// R458-2 disposable driver for oor_read.sv
#include <cstdio>
#include "Voor_read.h"
#include "verilated.h"
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Voor_read* d = new Voor_read;
  d->we_i = 1; d->d_i = 0x0123456789ABCDEFull; d->idx_i = 0;
  d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); d->we_i = 0; d->clk_i = 0; d->eval();
  for (int i = 0; i < 2; ++i) {
    d->idx_i = i; d->eval();
    std::printf("idx=%d q64=%016llx q48=%012llx q32=%08x q12=%03x q64r=%016llx\n", i,
                (unsigned long long)d->q64_o, (unsigned long long)d->q48_o, (unsigned)d->q32_o,
                (unsigned)d->q12_o, (unsigned long long)d->q64r_o);
  }
  delete d;
  return 0;
}

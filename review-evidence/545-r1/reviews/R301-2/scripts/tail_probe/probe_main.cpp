// Drives the engine outputs as registered signals (changed just after a
// rising edge) and grades each PHC sample the servo would stage: the sample
// taken at edge c+1 is ptp_now during cycle c; its flag is eff during cycle c.
// A sample whose last increment (ptp_now[c] - ptp_now[c-1]) is not the clean
// 8 ns must carry the flag. Slew addend = +8 ns/cycle for visibility.
#include "Vprobe_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
struct Ev { int cyc; int we; uint32_t addend; int level; };
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Vprobe_top* d = new Vprobe_top;
  const uint32_t S = 0x08000000u, C = 0u;
  // scenarios: rise before addend, completion clears with replacement pulse;
  // a repeated slew addend while high; a same-cycle rise+addend; mastership retire
  const Ev evs[] = {
    {40, 0, 0, 1}, {45, 1, S, 1}, {70, 1, S, 1}, {100, 1, C, 0},
    {160, 1, S, 1}, {200, 1, C, 0},
    {260, 0, 0, 1}, {262, 1, S, 1}, {263, 1, C, 0},
  };
  int ei = 0; const int N = sizeof(evs) / sizeof(evs[0]);
  d->axis_clk = 0; d->axis_resetn = 0; d->eng_we_i = 0; d->eng_addend_i = 0; d->eng_level_i = 0;
  uint64_t prev = 0; int errors = 0, slewed = 0, flagged = 0, over = 0;
  for (int cyc = 0; cyc < 320; ++cyc) {
    // cycle `cyc` begins just after rising edge `cyc`: registered engine outputs change here
    if (cyc == 5) d->axis_resetn = 1;
    d->eng_we_i = 0;
    if (ei < N && evs[ei].cyc == cyc) {
      d->eng_we_i = evs[ei].we; if (evs[ei].we) d->eng_addend_i = evs[ei].addend;
      d->eng_level_i = evs[ei].level; ++ei;
    }
    d->axis_clk = 0; d->eval();
    const uint64_t now = d->ptp_now_o; const int eff = d->eff_o;
    if (cyc > 20) {
      const uint64_t inc = now - prev;
      const bool dirty = inc != 8;
      slewed += dirty; flagged += eff; over += eff && !dirty;
      if (dirty && !eff) { ++errors; std::printf("  VIOLATION cyc=%d inc=%llu eff=%d\n", cyc, (unsigned long long)inc, eff); }
    }
    prev = now;
    d->axis_clk = 1; d->eval();
  }
  std::printf("  slewed samples=%d flagged samples=%d conservative extra=%d violations=%d\n",
              slewed, flagged, over, errors);
  std::printf(errors ? "  RESULT: FAIL\n" : "  RESULT: PASS\n");
  delete d;
  return errors ? 1 : 0;
}

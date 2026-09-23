// Review probe P-LAW: the REGISTER_MAP SLIP_TDM claim "from the first frame
// on and below the ceiling, dups minus skips follows ticks minus frame
// markers to within the one pending marker", checked cycle by cycle on the
// real RTL under random and near-grid stimulus with coincidences.
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <climits>
#include "Vprobe_law_wrap.h"
#include "verilated.h"
static uint32_t rng = 0x1234567u;
static uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  long bad = 0, total_cycles = 0, coin_pend = 0, coin_nopend = 0;
  for (int scen = 0; scen < 6; scen++) {
    rng = 0x9E3779B9u ^ (uint32_t)(scen * 7919 + 1);
    Vprobe_law_wrap* d = new Vprobe_law_wrap;
    d->rst_n = 0; d->frame_ev_i = 0; d->tick_i = 0;
    for (int i = 0; i < 8; i++) { d->clk = 0; d->eval(); d->clk = 1; d->eval(); }
    d->rst_n = 1;
    long T = 0, M = 0, pre_first_dups = -1; bool seen = false;
    long lo = LONG_MAX, hi = LONG_MIN;
    bool pend_model = false;       // only to classify coverage of the 2'b11 branch
    const long N = 3'000'000;
    double facc = 0, tacc = 0;
    // scenario: 0-1 random densities; 2-5 two near-equal grids with 0/1/2/3
    // edges of marker jitter (the passage regime, both directions)
    const double fper = (scen == 3 || scen == 5) ? 2083.30 : 2083.37, tper = 2083.3333;
    const int jit = (scen >= 2) ? scen - 2 : 0;
    long late[8] = {0};
    for (long c = 0; c < N; c++) {
      bool f = false, t = false;
      if (scen == 0) { f = (rnd() % 7) == 0; t = (rnd() % 7) == 0; }
      else if (scen == 1) { f = (rnd() % 3) == 0; t = (rnd() % 2) == 0; }
      else {
        facc += 1.0; if (facc >= fper) { facc -= fper; late[(c + (jit ? rnd() % (jit + 1) : 0)) & 7] ++; }
        if (late[c & 7]) { late[c & 7]--; f = true; }
        tacc += 1.0; if (tacc >= tper) { tacc -= tper; t = true; }
      }
      if (f && t) { if (pend_model) coin_pend++; else coin_nopend++; }
      d->frame_ev_i = f; d->tick_i = t;
      d->clk = 0; d->eval(); d->clk = 1; d->eval();
      // pend model mirrors the documented law, for coverage classification only
      if (f && !t) pend_model = true; else if (t && !f) pend_model = false;
      if (f) { seen = true; }
      if (!seen) { pre_first_dups = d->tdm_dup_cnt_o; continue; }
      if (f) M++;
      if (t) T++;
      if (d->tdm_dup_cnt_o == 0xFFFF || d->tdm_skip_cnt_o == 0xFFFF) break;
      long v = (long)d->tdm_dup_cnt_o - (long)d->tdm_skip_cnt_o - (T - M);
      if (v < lo) lo = v; if (v > hi) hi = v;
      total_cycles++;
    }
    printf("scenario %d (jitter %d): after first frame T=%ld M=%ld dups=%u skips=%u; "
           "(dups-skips)-(T-M) spans [%ld,%ld] (width %ld); dups before first frame=%ld\n",
           scen, jit, T, M, d->tdm_dup_cnt_o, d->tdm_skip_cnt_o, lo, hi, hi - lo, pre_first_dups);
    if (hi - lo > 1) bad++;
    if (pre_first_dups > 0) bad++;
    delete d;
  }
  printf("coincidences over a pending marker: %ld, over none: %ld\n", coin_pend, coin_nopend);
  printf("P-LAW %s (%ld cycles checked)\n", bad ? "FAIL" : "PASS", total_cycles);
  return bad ? 1 : 0;
}

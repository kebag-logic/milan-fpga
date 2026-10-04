// lockstep driver: identical random arms into both blocks, every output
// compared after each clock edge. argv: seed cycles mode
//   mode 0: protocol-shaped (sparse arms, bursts on random faces)
//   mode 1: fully random rates, frequent long saturation phases
#include "Vtb_top.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <random>

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1000000;
  int mode = argc > 3 ? atoi(argv[3]) : 0;
  std::mt19937_64 rng(seed);
  auto u = [&](double p) { return std::uniform_real_distribution<double>(0, 1)(rng) < p; };
  Vtb_top* t = new Vtb_top;
  double rate[8];
  auto new_phase = [&]() {
    for (int k = 0; k < 8; k++) {
      if (mode == 0) {
        rate[k] = u(0.75) ? 0.002 : (u(0.6) ? 0.05 : (u(0.5) ? 0.4 : 1.0));
      } else {
        static const double r[] = {0.0, 0.05, 0.2, 0.5, 0.8, 1.0};
        rate[k] = r[rng() % 6];
      }
    }
  };
  new_phase();
  uint64_t mism = 0, arms = 0, drops = 0, resets = 0, fullpop = 0, fullpush = 0;
  uint64_t maxcnt_hits[8] = {0};
  int rst_left = 3;
  uint64_t last_drop = 0;
  auto cmp = [&](uint64_t cyc, const char* ph) {
    bool bad = t->r_valid != t->d_valid || t->r_cancel != t->d_cancel ||
               t->r_slot != t->d_slot || t->r_owner != t->d_owner ||
               t->r_deadline != t->d_deadline || t->r_drop != t->d_drop;
    if (bad) {
      if (mism < 5)
        printf("MISMATCH cyc %llu %s: ref v%d c%d s%u o%u d%08x drop%u | dut v%d c%d s%u o%u d%08x drop%u\n",
               (unsigned long long)cyc, ph, t->r_valid, t->r_cancel, t->r_slot, t->r_owner, t->r_deadline,
               t->r_drop, t->d_valid, t->d_cancel, t->d_slot, t->d_owner, t->d_deadline, t->d_drop);
      mism++;
    }
  };
  for (uint64_t c = 0; c < cycles; c++) {
    if (rng() % (mode == 0 ? 3000 : 20000) == 0) new_phase();
    if (rst_left == 0 && rng() % (mode == 0 ? 200000 : 50000) == 0) { rst_left = 1 + rng() % 3; resets++; }
    t->rst_n = rst_left > 0 ? 0 : 1;
    if (rst_left > 0) rst_left--;
    uint8_t v = 0, cn = 0;
    for (int k = 0; k < 8; k++) { if (u(rate[k])) v |= 1u << k; if (u(0.3)) cn |= 1u << k; }
    t->vld_i = v;
    t->cancel_i = cn;
    uint64_t sl = rng();
    t->slot_i = sl;  // low 8*TMR_AW_C bits used (TMR_AW_C <= 8)
    t->owner_i = rng();
    for (int w = 0; w < 8; w++) t->deadline_i[w] = (uint32_t)rng();
    t->clk_i = 0;
    t->eval();
    cmp(c, "low");
    // coverage, read from the ref's state before the edge
    for (int k = 0; k < 8; k++) {
      unsigned cntk = (t->cnt_o >> (3 * k)) & 7u;
      if (cntk == 4) maxcnt_hits[k]++;
      bool pop = (t->pop_o >> k) & 1, push = (t->push_o >> k) & 1;
      if (t->rst_n && cntk == 4 && pop && push) fullpop++;
      if (t->rst_n && cntk == 4 && ((v >> k) & 1) && !push) fullpush++;
    }
    t->clk_i = 1;
    t->eval();
    cmp(c, "high");
    if (t->r_valid) arms++;
    if (t->r_drop != last_drop) { if (t->r_drop > last_drop) drops += t->r_drop - last_drop; last_drop = t->r_drop; }
  }
  printf("seed %llu mode %d cycles %llu: arms %llu drop-increments %llu resets %llu "
         "full+pop+push %llu push-at-full %llu full-cycles/face",
         (unsigned long long)seed, mode, (unsigned long long)cycles, (unsigned long long)arms,
         (unsigned long long)drops, (unsigned long long)resets, (unsigned long long)fullpop,
         (unsigned long long)fullpush);
  for (int k = 0; k < 8; k++) printf(" %llu", (unsigned long long)maxcnt_hits[k]);
  printf("\nMISMATCHES %llu\n", (unsigned long long)mism);
  delete t;
  return mism ? 1 : 0;
}

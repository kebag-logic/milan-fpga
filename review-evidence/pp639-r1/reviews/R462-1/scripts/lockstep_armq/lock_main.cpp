// Lockstep: main's arm-port block against the head's, identical random arms.
// usage: Vlock_top SEED CYCLES   (AW fixed at build time by -GAW=)
#include "Vlock_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <random>

template <typename T> static uint64_t field(const T& v) { return uint64_t(v); }

int main(int argc, char** argv) {
  const uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  const uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1000000;
  auto* ctx = new VerilatedContext;
  ctx->randReset(2);
  ctx->randSeed(static_cast<int>(seed * 7919 + 13));
  auto* d = new Vlock_top{ctx};
  std::mt19937_64 rng(seed);
  auto u = [&](uint32_t n) { return uint32_t(rng() % n); };
  const int AWB = 1 + AW_BITS + 8 + 32;
  const uint64_t amask = (AWB >= 64) ? ~0ULL : ((1ULL << AWB) - 1);
  uint64_t mism = 0, first = 0, arms = 0, drops_clk = 0, offers_full = 0, fullpoppush = 0,
           resets = 0, rst_offers = 0, multi_drop = 0, depth_hist[5] = {0, 0, 0, 0, 0},
           sat = 0, cnt_mism = 0;
  // rates per face, re-drawn per phase
  uint32_t rate[8];
  auto new_phase = [&]() {
    const uint32_t kind = u(4);
    for (int k = 0; k < 8; ++k) {
      if (kind == 0) rate[k] = u(1000);              // fully random
      else if (kind == 1) rate[k] = u(4) ? 50 : 980; // a few hot faces
      else if (kind == 2) rate[k] = 990;             // saturate every face
      else rate[k] = u(200);                         // light
    }
  };
  new_phase();
  int rst_hold = 5;
  bool force_sat = (seed % 8) == 7;  // one seed per eight drives the counter to saturation
  for (uint64_t t = 0; t < cycles; ++t) {
    if (u(20000) == 0) new_phase();
    if (rst_hold == 0 && u(30000) == 0) { rst_hold = 1 + u(4); ++resets; }
    d->rst_n = rst_hold > 0 ? 0 : 1;
    if (rst_hold > 0) --rst_hold;
    uint8_t v = 0;
    constexpr int WORDS = (8 * (1 + AW_BITS + 8 + 32) + 31) / 32;
    for (int w = 0; w < WORDS; ++w) d->in_arm_i[w] = 0;
    for (int k = 0; k < 8; ++k) {
      const uint32_t r = force_sat ? 995 : rate[k];
      if (u(1000) < r) v |= uint8_t(1u << k);
      uint64_t a = ((uint64_t(rng()) << 1) ^ rng()) & amask;
      for (int b = 0; b < AWB; ++b) {
        if ((a >> b) & 1ULL) {
          const int bit = k * AWB + b;
          d->in_arm_i[bit / 32] |= (1u << (bit % 32));
        }
      }
    }
    d->in_vld_i = v;
    // pre-edge observation (both designs' counts, which are equal while in lockstep)
    if (d->rst_n) {
      bool any_pop = false;
      int dropping = 0;
      for (int k = 0; k < 8; ++k) {
        const uint32_t c = (d->r_cnt_o >> (3 * k)) & 7u;
        depth_hist[c > 4 ? 4 : c]++;
        const bool pop = !any_pop && c != 0;
        if (c != 0) any_pop = true;
        if ((v >> k) & 1u) {
          if (c == 4 && !pop) { ++offers_full; ++dropping; }
          if (c == 4 && pop) ++fullpoppush;
        }
      }
      if (dropping) ++drops_clk;
      if (dropping > 1) ++multi_drop;
    } else if (v) {
      ++rst_offers;
    }
    d->clk_i = 0; d->eval();
    d->clk_i = 1; d->eval();
    const bool same = d->r_valid_o == d->d_valid_o
                      && field(d->r_arm_o) == field(d->d_arm_o)
                      && d->r_drop_o == d->d_drop_o;
    if (d->r_cnt_o != d->d_cnt_o) ++cnt_mism;
    if (d->r_valid_o) ++arms;
    if (d->r_drop_o == 0xFFFF) ++sat;
    if (!same) { if (!mism) first = t; ++mism; }
  }
  printf("seed %llu cycles %llu AW %d: mismatches %llu (first %llu) cnt_mismatches %llu | arms %llu "
         "offers_to_full_dropped %llu drop_clocks %llu multi_face_drop_clocks %llu "
         "full_pop_push %llu resets %llu offers_during_reset %llu sat_clocks %llu "
         "depth_hist %llu/%llu/%llu/%llu/%llu\n",
         (unsigned long long)seed, (unsigned long long)cycles, AW_BITS,
         (unsigned long long)mism, (unsigned long long)first, (unsigned long long)cnt_mism,
         (unsigned long long)arms, (unsigned long long)offers_full,
         (unsigned long long)drops_clk, (unsigned long long)multi_drop,
         (unsigned long long)fullpoppush, (unsigned long long)resets,
         (unsigned long long)rst_offers, (unsigned long long)sat,
         (unsigned long long)depth_hist[0], (unsigned long long)depth_hist[1],
         (unsigned long long)depth_hist[2], (unsigned long long)depth_hist[3],
         (unsigned long long)depth_hist[4]);
  delete d;
  delete ctx;
  return mism ? 1 : 0;
}

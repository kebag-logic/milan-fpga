// R298-2 reviewer probe: randomized declarations/withdrawals against an oracle
// written from architecture 10 section 6.3 (current-declaration grant, cross-source
// hold, publication = greedy walk, bounded latency), plus lockstep equality of
// two RTL variants (u_a vs u_b) when EQ_CHECK is set.
#include "Vfz_wrap.h"
#include "verilated.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <random>

static constexpr unsigned N = FZ_N;
static constexpr unsigned BOUND = N == 1 ? 4 : 3 * N;
static uint64_t slope(unsigned f, unsigned m) {
  return (std::max(f + 22u, 68u) + 20ull) * m * 64000ull;
}
struct Tally { uint64_t checks = 0, fails = 0; };
static Tally tally;
static std::array<uint64_t, 16> fail_by{};
static const char* names[16] = {"C1 grant only while requesting",
  "C2 grant carries exact current slope <= ceiling", "C3 unadmitted slope zero",
  "C4 live granted sum <= ceiling", "C5 publication == greedy over current declarations",
  "C5b publication only >= 4 clocks after every requesting source's change",
  "C6 between publications no grant rises / unchanged grants hold",
  "C6b aggregate holds between publications", "C7 publication within bound of last change",
  "C8 lockstep equality of the two variants", "C9 changed source low until next publication"};
static void chk(bool ok, int id) {
  ++tally.checks;
  if (!ok) { ++tally.fails; if (fail_by[id]++ < 3) std::printf("FAIL: %s\n", names[id]); }
}
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const unsigned seed = argc > 1 ? unsigned(std::atoi(argv[1])) : 1;
  const unsigned episodes = argc > 2 ? unsigned(std::atoi(argv[2])) : 200;
  std::mt19937 rng(seed);
  auto* d = new Vfz_wrap;
  const unsigned frames[] = {29, 224, 1051, 1520, 2000, 4645, 6208, 10000, 10895, 11395, 20000, 0xffff};
  const unsigned mifs[] = {1, 1, 1, 1, 2, 3, 0, 100, 0xffff};
  uint64_t publications = 0, holds_seen = 0, max_lat = 0;
  for (unsigned ep = 0; ep < episodes; ++ep) {
    const uint32_t rate = (ep % 5 == 4) ? 100000000u : 1000000000u;
    const uint64_t limit = (rate >> 1) + (rate >> 2);
    std::array<unsigned, 8> mfs{}, mif{}; unsigned req = 0;
    std::array<int64_t, 8> chg_at; chg_at.fill(-1000);
    std::array<bool, 8> await_pub{};
    int64_t last_change = -1000; bool pub_since = true;
    const unsigned pct = 1 + rng() % 40;           // change probability per clock, percent
    d->rst_n = 0; d->chg_i = 0; d->req_i = 0; d->rate_i = rate;
    for (int i = 0; i < 4; ++i) { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
    d->rst_n = 1;
    unsigned prev_adm = 0; uint32_t prev_sum = 0; bool prev_over = false;
    std::array<uint32_t, 8> prev_gs{};
    for (int64_t t = 0; t < 4000; ++t) {
      unsigned chg = 0;
      bool quiet = (t % 400) > 300;                  // regular quiet stretches for liveness
      if (!quiet && rng() % 100 < pct) {
        unsigned k = (rng() % 8 == 0) ? 2 : 1;
        for (unsigned j = 0; j < k; ++j) {
          unsigned s = rng() % N; chg |= 1u << s;
          unsigned r = rng() % 10;
          if (r == 0) { req &= ~(1u << s); }
          else if (r <= 2 && (req >> s & 1)) { /* identical re-declaration */ }
          else { req |= 1u << s; mfs[s] = frames[rng() % 12]; mif[s] = mifs[rng() % 9]; }
        }
      }
      d->chg_i = chg; d->req_i = req;
      for (unsigned w = 0; w < 4; ++w) { d->mfs_i[w] = 0; d->mif_i[w] = 0; }
      for (unsigned s = 0; s < 8; ++s) {
        d->mfs_i[s / 2] |= uint32_t(mfs[s] & 0xffff) << (16 * (s % 2));
        d->mif_i[s / 2] |= uint32_t(mif[s] & 0xffff) << (16 * (s % 2));
      }
      d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval();
      if (chg) {
        last_change = t; pub_since = false;
        for (unsigned s = 0; s < N; ++s) if (chg >> s & 1) { chg_at[s] = t; await_pub[s] = true; }
      }
      const unsigned adm = d->adm_a_o;
      uint64_t live = 0;
      for (unsigned s = 0; s < N; ++s) {
        const bool g = adm >> s & 1;
        const uint32_t gs = d->gs_a_o[s];
        live += gs;
        chk(!g || (req >> s & 1), 0);
        chk(!g || (gs == slope(mfs[s], mif[s]) && slope(mfs[s], mif[s]) <= limit), 1);
        chk(g || gs == 0, 2);
        chk(!g || !await_pub[s] || d->rnd_a_o, 10);
      }
      chk(live <= limit, 3);
      if (d->rnd_a_o) {
        ++publications;
        unsigned gg = 0; uint64_t sum = 0; bool over = false;
        for (unsigned s = 0; s < N; ++s) {
          if (!(req >> s & 1)) continue;
          uint64_t sl = slope(mfs[s], mif[s]);
          if (sum + sl <= limit) { gg |= 1u << s; sum += sl; } else over = true;
        }
        bool slopes = true;
        for (unsigned s = 0; s < N; ++s)
          slopes &= d->gs_a_o[s] == ((gg >> s & 1) ? slope(mfs[s], mif[s]) : 0);
        chk(adm == gg && slopes && d->sum_a_o == sum && bool(d->over_a_o) == over, 4);
        bool aged = true;
        for (unsigned s = 0; s < N; ++s) if (req >> s & 1) aged &= t - chg_at[s] >= 4;
        chk(aged, 5);
        if (!pub_since) { max_lat = std::max<uint64_t>(max_lat, uint64_t(t - last_change)); }
        pub_since = true; await_pub.fill(false);
      } else {
        chk((adm & ~prev_adm) == 0 && (adm & ~chg) == (prev_adm & ~chg), 6);
        bool gs_hold = true;
        for (unsigned s = 0; s < N; ++s) if (!(chg >> s & 1)) gs_hold &= d->gs_a_o[s] == prev_gs[s];
        chk(gs_hold, 6);
        chk(d->sum_a_o == prev_sum && bool(d->over_a_o) == prev_over, 7);
        if (!pub_since && t - last_change >= int64_t(BOUND)) { chk(false, 8); pub_since = true; }
        if (!pub_since) ++holds_seen;
      }
#ifdef EQ_CHECK
      bool eq = d->adm_a_o == d->adm_b_o && d->sum_a_o == d->sum_b_o &&
                d->over_a_o == d->over_b_o && d->rnd_a_o == d->rnd_b_o;
      for (unsigned s = 0; s < 8; ++s) eq &= d->gs_a_o[s] == d->gs_b_o[s];
      chk(eq, 9);
#endif
      prev_adm = adm; prev_sum = d->sum_a_o; prev_over = d->over_a_o;
      for (unsigned s = 0; s < 8; ++s) prev_gs[s] = d->gs_a_o[s];
    }
  }
  d->final(); delete d;
  std::printf("FUZZ N=%u seed=%u episodes=%u publications=%llu held_clocks=%llu max_latency=%llu bound=%u\n",
              N, seed, episodes, (unsigned long long)publications,
              (unsigned long long)holds_seen, (unsigned long long)max_lat, BOUND);
  for (int i = 0; i < 11; ++i) if (fail_by[i]) std::printf("FAILCOUNT %s: %llu\n", names[i], (unsigned long long)fail_by[i]);
  std::printf("%llu checks: %llu PASS, %llu FAIL\n", (unsigned long long)tally.checks,
              (unsigned long long)(tally.checks - tally.fails), (unsigned long long)tally.fails);
  return tally.fails ? 1 : 0;
}

// Reviewer probe: the engine's scaledLastGmFreqChange multiply (RTL lines
// copied verbatim into tlvmul.sv) against exact arithmetic, over the whole
// +-RATE_PPM_C trim envelope at 2, 100 and 125 MHz, extremes included.
#include <cstdint>
#include <cstdio>
#include <random>
#include "Vtlvtop.h"
#include "verilated.h"
static int64_t ilim(int64_t clk) { return (200LL * (1LL << 24) * 1000 + clk / 2) / clk; }
static int64_t floordiv(__int128 n, __int128 d) { __int128 q = n / d; if ((n % d) != 0 && ((n < 0) != (d < 0))) q--; return (int64_t)q; }
static uint32_t K_of(Vtlvtop &t, int i) { return i == 0 ? t.k2_o : i == 1 ? t.k50_o : i == 2 ? t.k100_o : t.k125_o; }
static int32_t F_of(Vtlvtop &t, int i) { return (int32_t)(i == 0 ? t.f2_o : i == 1 ? t.f50_o : i == 2 ? t.f100_o : t.f125_o); }
int main() {
  Vtlvtop t; const int64_t clks[4] = {2000000, 50000000, 100000000, 125000000};
  long bad = 0, n = 0; double worst[4] = {0, 0, 0, 0};
  std::mt19937_64 rng(100);
  auto step = [&](int32_t a, int32_t e) {
    t.a_i = (uint32_t)a; t.e_i = (uint32_t)e;
    for (int k = 0; k < 2; k++) { t.clk_i = 0; t.eval(); t.clk_i = 1; t.eval(); }
    const int32_t f[4] = {(int32_t)t.f2_o, (int32_t)t.f50_o, (int32_t)t.f100_o, (int32_t)t.f125_o};
    const uint32_t K[4] = {t.k2_o, t.k50_o, t.k100_o, t.k125_o};
    for (int i = 0; i < 4; i++) {
      const int64_t L = ilim(clks[i]);
      if (a < -L || a > L || e < -L || e > L) continue;
      const int64_t u = (int64_t)a - e; n++;
      const int64_t model = floordiv((__int128)u * K[i], 65536);
      // exact value: u * clk * 2^17 / 1e9
      const long double ex = (long double)u * clks[i] * 131072.0L / 1e9L;
      const long double err = (long double)f[i] - ex;
      const long double tol = 1.0L + (long double)(u < 0 ? -u : u) * 0.5L / 65536.0L;
      if ((long double)worst[i] < (err < 0 ? -err : err)) worst[i] = (double)(err < 0 ? -err : err);
      if (f[i] != model || err > tol || err < -tol - 1.0L || (u > 0 && f[i] <= 0) || (u < 0 && f[i] >= 0)) {
        if (bad++ < 10) printf("MISMATCH clk %lld a %d e %d u %lld f %d model %lld exact %.3Lf\n", (long long)clks[i], a, e, (long long)u, f[i], (long long)model, ex);
      }
    }
  };
  for (int i = 0; i < 4; i++) {
    const int32_t L = (int32_t)ilim(clks[i]);
    const int32_t v[] = {-L, -L + 1, -1, 0, 1, L - 1, L};
    for (int32_t a : v) for (int32_t e : v) step(a, e);
    printf("clk %lld: K=%u ilim=%d  extreme (L,-L) -> u=%d\n", (long long)clks[i], K_of(t, i), L, 2 * L);
  }
  for (int r = 0; r < 400000; r++) {
    const int64_t L = ilim(clks[r % 4]);
    step((int32_t)((int64_t)(rng() % (2 * L + 1)) - L), (int32_t)((int64_t)(rng() % (2 * L + 1)) - L));
  }
  // the corners at each clock, printed
  for (int i = 0; i < 4; i++) {
    const int32_t L = (int32_t)ilim(clks[i]);
    step(L, -L); const int32_t hi = F_of(t, i);
    step(-L, L); const int32_t lo = F_of(t, i);
    printf("clk %lld: +400 ppm -> %d (exact %.1f), -400 ppm -> %d; worst |err| %.3f\n", (long long)clks[i], hi, 400e-6 * 2199023255552.0, lo, worst[i]);
  }
  printf("%ld comparisons, %ld mismatches\n", n, bad);
  return bad ? 1 : 0;
}

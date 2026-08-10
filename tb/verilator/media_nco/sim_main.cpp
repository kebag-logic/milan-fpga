// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_media_nco - the steerable media sample grid.
//
// What this proves, and why each check exists:
//
//   1. INTERNAL IS UNCHANGED. With trim tied to 0 the DUT is tick-for-tick
//      identical to the inline Bresenham it replaced (transcribed from
//      milan_datapath.sv at VERSION 0x0040). clock_source = INTERNAL is the
//      shipping default and every bench number on record was measured
//      against that grid, so "bit-exact" is a release gate, not a nicety.
//
//   2. THE RATE IS EXACT, NOT MERELY CLOSE. Checked in integer arithmetic
//      (|E*FS - N*(CLK+trim)| < FS), so the accuracy verdict does not depend
//      on how long the harness happened to run. An averaged-ppm check at
//      this resolution would need a full second of audio per trim point.
//
//   3. THE PHASE NEVER RUNS AWAY. The elapsed clock count is never a whole
//      clock from N*period. This is what "zero long-term residual" means,
//      and an averaging check cannot see its absence.
//
//   4. THE GRID STAYS A GRID. Every instantaneous period is DIV-1, DIV or
//      DIV+1. A divider that hit the right average by alternating wildly
//      would pass 2 and 3 and be useless to a converter.
//
//   5. THE LSB IS 1/CLK_FREQ_HZ, NOT A 100 MHz COINCIDENCE. Two instances at
//      the two datapath clocks this project ships (AX7101 100 MHz, Arty
//      50 MHz) are graded against the same closed form.
//
//   6. THE SIGN IS THE ONE THE DATAPATH ASSUMES. trim > 0 SLOWS the grid.
//      KL_mmcm_drp_servo's u is the opposite ("u > 0 = speed up"), so
//      milan_datapath negates between them; a sign error here is a runaway
//      servo, so it is pinned explicitly rather than left to inference.
//
//   7. A WILD TRIM DEGRADES TO THE CLAMP. Beyond +/-TRIM_MAX_P the rate must
//      saturate, never wrap and never drop a sample.

#include "Vmedia_nco_wrap.h"
#include "verilated.h"
#include "nco_ref_model.h"

#include <cstdio>
#include <cmath>
#include <string>
#include <vector>

static long g_checks = 0;
static long g_fail   = 0;

static void ok(bool cond, const std::string& what) {
    ++g_checks;
    if (!cond) {
        ++g_fail;
        printf("  [FAIL] %s\n", what.c_str());
    }
}

static Vmedia_nco_wrap* dut = nullptr;
static uint64_t g_clock = 0;

// One clock. Returns the {A,B} tick pair observed on this edge.
struct Ticks { bool a, b; };
static Ticks tick_clock() {
    dut->clk_i = 0;
    dut->eval();
    dut->clk_i = 1;
    dut->eval();
    ++g_clock;
    return Ticks{ dut->a_tick_o != 0, dut->b_tick_o != 0 };
}

static void do_reset() {
    dut->rst_n = 0;
    dut->a_trim_i = 0;
    dut->b_trim_i = 0;
    for (int i = 0; i < 8; ++i) tick_clock();
    dut->rst_n = 1;
}

// ------------------------------------------------------------------------ //
// 1. Bit-exactness against the divider this module replaced                  //
// ------------------------------------------------------------------------ //
static void test_bit_exact(uint64_t clocks) {
    printf("\n-- 1. trim = 0 is bit-for-bit the VERSION 0x0040 divider --\n");
    do_reset();

    LegacyBresenham legacy_a(100000000ULL, 48000ULL);
    LegacyBresenham legacy_b( 50000000ULL, 48000ULL);

    uint64_t mismatch_a = 0, mismatch_b = 0, ta = 0, tb = 0;
    for (uint64_t c = 0; c < clocks; ++c) {
        const Ticks t = tick_clock();
        const bool la = legacy_a.step();
        const bool lb = legacy_b.step();
        if (t.a != la) ++mismatch_a;
        if (t.b != lb) ++mismatch_b;
        if (t.a) ++ta;
        if (t.b) ++tb;
    }
    printf("   A(100 MHz): %llu ticks in %llu clocks, %llu mismatches\n",
           (unsigned long long)ta, (unsigned long long)clocks,
           (unsigned long long)mismatch_a);
    printf("   B( 50 MHz): %llu ticks in %llu clocks, %llu mismatches\n",
           (unsigned long long)tb, (unsigned long long)clocks,
           (unsigned long long)mismatch_b);

    // Vacuity guard: a DUT stuck low would report zero mismatches against a
    // model that also never fired. Demand real ticks before believing it.
    ok(ta > 0, "A produced ticks at all (vacuity guard)");
    ok(tb > 0, "B produced ticks at all (vacuity guard)");
    ok(mismatch_a == 0, "A tick-for-tick identical to the legacy divider");
    ok(mismatch_b == 0, "B tick-for-tick identical to the legacy divider");
}

// ------------------------------------------------------------------------ //
// 2-4, 6-7. Rate, phase, period bounds and clamp across a trim sweep         //
// ------------------------------------------------------------------------ //
struct Shape {
    const char* name;
    NcoSpec     spec;
};

static void test_trim_point(const Shape& sh, int64_t trim, uint64_t want_ticks,
                            bool is_a, double* out_ppm) {
    do_reset();
    if (is_a) dut->a_trim_i = (int32_t)trim; else dut->b_trim_i = (int32_t)trim;

    NcoObserver obs(sh.spec);
    obs.reset(g_clock);

    // Discard the first tick for PERIOD purposes: it carries the reset phase,
    // not a period. The PHASE oracle counts from the very first tick.
    uint64_t seen = 0;
    uint64_t first_clock = 0, last_clock = 0;
    bool have_first = false;

    // The phase oracle. phase at tick k is exactly ((k*(REM+trim)) mod DEN),
    // taken into [0,DEN). This is a closed form, not the DUT's recurrence, and
    // it is what makes a sub-LSB remainder error visible in a handful of ticks
    // instead of the ~144,000 the tick pattern alone would need.
    const int64_t  clamped_t = sh.spec.clamp(trim);
    const int64_t  den       = int64_t(sh.spec.fs_hz);
    const int64_t  step      = int64_t(sh.spec.rem()) + clamped_t;
    uint64_t k = 0, phase_bad = 0;

    while (seen <= want_ticks) {
        const Ticks t = tick_clock();
        const bool hit = is_a ? t.a : t.b;
        if (!hit) continue;

        ++k;
        const int64_t want_phase = (((int64_t(k) * step) % den) + den) % den;
        const int64_t got_phase  = is_a ? int64_t(dut->a_phase_o)
                                        : int64_t(dut->b_phase_o);
        if (got_phase != want_phase) ++phase_bad;

        obs.on_tick(g_clock, trim);
        if (!have_first) { have_first = true; first_clock = g_clock; }
        else { last_clock = g_clock; ++seen; }
    }

    const int64_t  clamped = sh.spec.clamp(trim);
    const uint64_t N       = seen;
    const int64_t  E       = int64_t(last_clock - first_clock);

    // CHECK 2 - exact rate, in integers: |E*FS - N*(CLK+trim)| < FS
    const long double lhs =
        (long double)E * (long double)sh.spec.fs_hz
      - (long double)N * (long double)(int64_t(sh.spec.clk_hz) + clamped);
    const bool rate_exact = std::fabsl(lhs) < (long double)sh.spec.fs_hz;

    // CHECK 3 - phase never a whole clock adrift
    const bool phase_ok = obs.worst_drift() < 1.0;

    // CHECK 4 - period bounds
    const int64_t div = int64_t(sh.spec.div());
    const bool bounds_ok = obs.min_period() >= div - 1 && obs.max_period() <= div + 1;

    const double meas = obs.measured_ppm();
    const double want = sh.spec.ppm(trim);
    if (out_ppm) *out_ppm = meas;

    printf("   %s trim %+7lld -> %+10.4f ppm (spec %+10.4f, d %+7.4f)"
           "  periods [%lld..%lld]  drift %.4f\n",
           sh.name, (long long)trim, meas, want, meas - want,
           (long long)obs.min_period(), (long long)obs.max_period(),
           obs.worst_drift());

    ok(N > 0, std::string(sh.name) + " produced ticks (vacuity guard)");
    ok(phase_bad == 0, std::string(sh.name) + " phase accumulator matches (k*(REM+trim)) mod DEN at trim "
                       + std::to_string(trim) + " (" + std::to_string(phase_bad) + " bad)");
    ok(rate_exact, std::string(sh.name) + " exact rate at trim " + std::to_string(trim));
    ok(phase_ok,   std::string(sh.name) + " phase bounded at trim " + std::to_string(trim));
    ok(bounds_ok,  std::string(sh.name) + " period in {DIV-1,DIV,DIV+1} at trim " + std::to_string(trim));
}

static void test_sweep(const Shape& sh, bool is_a, uint64_t ticks_per_point) {
    printf("\n-- 2/3/4. %s: rate, phase and period across the trim range --\n", sh.name);
    //! shape-relative, so the 50 MHz build exercises ITS whole range rather
    //! than clamping halfway through a list sized for the 100 MHz one
    const int64_t tmax = sh.spec.trim_max;
    const std::vector<int64_t> trims = {
        0, 1, -1, 10, -10, 100, -100, 1000, -1000,
        tmax / 4, -tmax / 4, tmax / 2, -tmax / 2, tmax, -tmax
    };
    double ppm_at_0 = 0.0, ppm_at_p1000 = 0.0, ppm_at_m1000 = 0.0;
    double ppm_at_pmax = 0.0, ppm_at_mmax = 0.0;
    for (int64_t t : trims) {
        double p = 0.0;
        test_trim_point(sh, t, ticks_per_point, is_a, &p);
        if (t ==     0) ppm_at_0     = p;
        if (t ==  1000) ppm_at_p1000 = p;
        if (t == -1000) ppm_at_m1000 = p;
        if (t ==  tmax) ppm_at_pmax  = p;
        if (t == -tmax) ppm_at_mmax  = p;
    }

    // CHECK 6 - the sign the datapath depends on
    printf("\n-- 6. %s: sign convention (trim > 0 SLOWS the grid) --\n", sh.name);
    printf("   ppm(+1000) = %+.4f, ppm(0) = %+.4f, ppm(-1000) = %+.4f\n",
           ppm_at_p1000, ppm_at_0, ppm_at_m1000);
    ok(ppm_at_p1000 < ppm_at_0, std::string(sh.name) + " positive trim slows the grid");
    ok(ppm_at_m1000 > ppm_at_0, std::string(sh.name) + " negative trim speeds the grid");

    // CHECK 5 - the trim LSB.
    //
    // The EXACT proof is check 2 at trim +/-1: |E*FS - N*(CLK+trim)| < FS says
    // the average period is (CLK+trim)/FS clocks, i.e. one trim LSB moves the
    // period by exactly 1/FS clocks = 1/CLK relative. That is integer-exact
    // and needs no statistics.
    //
    // What follows is the human-readable confirmation, and it is deliberately
    // taken across the FULL +/-tmax span rather than +/-1000: the averaged-ppm
    // estimate carries ~480/N ppm of quantisation, which over a 2000-LSB span
    // is 1.6% of a 0.01 ppm LSB - a gate at 1% there would flake. Over the
    // full span the same noise is ~0.05%. The oracle is the spec's own secant
    // (the exact ppm curve is 1/(1+t/CLK), not a straight line, so comparing
    // a wide secant to the derivative at 0 would be wrong by design).
    const double span_lsb  = 2.0 * double(tmax);
    const double meas_lsb  = (ppm_at_mmax - ppm_at_pmax) / span_lsb;
    const double spec_lsb  = (sh.spec.ppm(-tmax) - sh.spec.ppm(tmax)) / span_lsb;
    printf("\n-- 5. %s: trim LSB calibration --\n", sh.name);
    printf("   measured %.7f ppm/LSB over +/-%lld, spec secant %.7f, nominal 1e6/%llu = %.7f\n",
           meas_lsb, (long long)tmax, spec_lsb,
           (unsigned long long)sh.spec.clk_hz, sh.spec.lsb_ppm());
    ok(std::fabs(meas_lsb - spec_lsb) < spec_lsb * 0.005,
       std::string(sh.name) + " trim LSB matches the spec secant within 0.5%");
    ok(std::fabs(spec_lsb - sh.spec.lsb_ppm()) < sh.spec.lsb_ppm() * 0.05,
       std::string(sh.name) + " LSB is 1e6/CLK_FREQ_HZ (secant within 5% of the derivative)");
}

// ------------------------------------------------------------------------ //
// 7. Clamp                                                                   //
// ------------------------------------------------------------------------ //
static void test_clamp(const Shape& sh, bool is_a, uint64_t ticks) {
    printf("\n-- 7. %s: trim beyond +/-TRIM_MAX_P saturates --\n", sh.name);
    const int64_t tmax = sh.spec.trim_max;
    double at_max = 0, beyond = 0, at_min = 0, below = 0;
    test_trim_point(sh,  tmax,       ticks, is_a, &at_max);
    test_trim_point(sh,  tmax * 2,   ticks, is_a, &beyond);   // 2x past the clamp
    test_trim_point(sh, -tmax,       ticks, is_a, &at_min);
    test_trim_point(sh, -tmax * 2,   ticks, is_a, &below);
    ok(std::fabs(beyond - at_max) < 1e-3,
       std::string(sh.name) + " trim above TRIM_MAX_P equals TRIM_MAX_P");
    ok(std::fabs(below - at_min) < 1e-3,
       std::string(sh.name) + " trim below -TRIM_MAX_P equals -TRIM_MAX_P");
    //! the clamp must land on the DERIVED authority, not on a literal: this
    //! is the check that catches a hand-written TRIM_MAX_P override
    ok(std::fabs(at_max - sh.spec.ppm(tmax)) < 0.05,
       std::string(sh.name) + " clamp lands on the derived authority");
    ok(std::fabs(std::fabs(at_max) - 319.9) < 1.0,
       std::string(sh.name) + " derived authority is +/-320 ppm (covers the servo's +/-200)");
}

// ------------------------------------------------------------------------ //
// 8. A trim change mid-flight neither loses nor duplicates a sample          //
// ------------------------------------------------------------------------ //
static void test_dynamic(const Shape& sh, bool is_a) {
    printf("\n-- 8. %s: live trim change keeps the grid continuous --\n", sh.name);
    do_reset();
    if (is_a) dut->a_trim_i = 0; else dut->b_trim_i = 0;

    const int64_t div = int64_t(sh.spec.div());
    uint64_t ticks = 0, last = 0;
    bool have_last = false;
    int64_t worst_lo = div + 99, worst_hi = 0;

    for (uint64_t c = 0; c < 3000000; ++c) {
        if (c == 1000000) { if (is_a) dut->a_trim_i = -5000; else dut->b_trim_i = -5000; }
        if (c == 2000000) { if (is_a) dut->a_trim_i =  5000; else dut->b_trim_i =  5000; }
        const Ticks t = tick_clock();
        const bool hit = is_a ? t.a : t.b;
        if (!hit) continue;
        if (have_last) {
            const int64_t p = int64_t(g_clock - last);
            if (p < worst_lo) worst_lo = p;
            if (p > worst_hi) worst_hi = p;
        }
        last = g_clock; have_last = true; ++ticks;
    }
    printf("   %llu ticks across two live trim steps, periods [%lld..%lld]\n",
           (unsigned long long)ticks, (long long)worst_lo, (long long)worst_hi);
    ok(ticks > 0, std::string(sh.name) + " ticked across the trim steps (vacuity guard)");
    ok(worst_lo >= div - 1 && worst_hi <= div + 1,
       std::string(sh.name) + " no period glitch when the trim moves");
}

// ------------------------------------------------------------------------ //
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmedia_nco_wrap;

    printf("======================================================================\n");
    printf("KL_media_nco - steerable media sample grid\n");
    printf("======================================================================\n");

    //! trim_max is stated INDEPENDENTLY here (48000 - CLK%48000) rather than
    //! read from the RTL, so a change to the module's derived default trips
    //! the clamp checks instead of silently moving with it
    const Shape A{ "A(100MHz)", NcoSpec{100000000ULL, 48000ULL, 32000} };
    const Shape B{ "B( 50MHz)", NcoSpec{ 50000000ULL, 48000ULL, 16000} };

    printf("   A: DIV %llu REM %llu, LSB %.4f ppm, authority +/-%.2f ppm\n",
           (unsigned long long)A.spec.div(), (unsigned long long)A.spec.rem(),
           A.spec.lsb_ppm(), std::fabs(A.spec.ppm(20000)));
    printf("   B: DIV %llu REM %llu, LSB %.4f ppm, authority +/-%.2f ppm\n",
           (unsigned long long)B.spec.div(), (unsigned long long)B.spec.rem(),
           B.spec.lsb_ppm(), std::fabs(B.spec.ppm(20000)));

    test_bit_exact(600000);

    test_sweep(A, true,  1500);
    test_sweep(B, false, 1500);

    test_clamp(A, true,  1500);
    test_clamp(B, false, 1500);

    test_dynamic(A, true);
    test_dynamic(B, false);

    dut->final();
    delete dut;

    printf("\n======================================================================\n");
    printf("media_nco: %ld checks: %ld PASS, %ld FAIL\n",
           g_checks, g_checks - g_fail, g_fail);
    printf("======================================================================\n");
    return g_fail == 0 ? 0 : 1;
}

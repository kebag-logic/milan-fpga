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
#include "../../common/verilator_harness.hpp"
#include "nco_ref_model.h"

#include <cstdio>
#include <cmath>
#include <string>
#include <vector>

namespace {

// One clock. Returns the {A,B} tick pair observed on this edge.
struct Ticks {
    bool a;
    bool b;
};

struct Shape {
    const char* name;
    NcoSpec     spec;
};

class MediaNcoHarness {
 public:
    int run();

 private:
    void ok(bool cond, const std::string& what);
    Ticks tick_clock();
    void do_reset();
    void test_bit_exact(uint64_t clocks);
    void test_trim_point(const Shape& sh, int64_t trim, uint64_t want_ticks,
                         bool is_a, double* out_ppm);
    void test_sweep(const Shape& sh, bool is_a, uint64_t ticks_per_point);
    void test_clamp(const Shape& sh, bool is_a, uint64_t ticks);
    void test_dynamic(const Shape& sh, bool is_a);
    void test_servo(const Shape& sh, bool is_a, long ppm_lsb, uint64_t ticks);

    long g_checks = 0;
    long g_fail   = 0;

    Vmedia_nco_wrap* dut = nullptr;
    uint64_t g_clock = 0;
};

void MediaNcoHarness::ok(bool cond, const std::string& what) {
    ++g_checks;
    if (!cond) {
        ++g_fail;
        printf("  [FAIL] %s\n", what.c_str());
    }
}

Ticks MediaNcoHarness::tick_clock() {
    dut->clk_i = 0;
    dut->eval();
    dut->clk_i = 1;
    dut->eval();
    ++g_clock;
    return Ticks{ dut->a_tick_o != 0, dut->b_tick_o != 0 };
}

//! Clocks rst_n is held low for before any stimulus, so both NCO instances
//! start every test from their reset counter and accumulator.
constexpr int kResetClocks = 8;

void MediaNcoHarness::do_reset() {
    dut->rst_n = 0;
    dut->a_trim_i = 0;
    dut->b_trim_i = 0;
    dut->a_servo_trim_i = 0;
    dut->b_servo_trim_i = 0;
    dut->a_servo_en_i = 0;
    dut->b_servo_en_i = 0;
    for (int i = 0; i < kResetClocks; ++i) tick_clock();
    dut->rst_n = 1;
}

// ------------------------------------------------------------------------ //
// 1. Bit-exactness against the divider this module replaced                  //
// ------------------------------------------------------------------------ //
void MediaNcoHarness::test_bit_exact(uint64_t clocks) {
    printf("\n-- 1. trim = 0 is bit-for-bit the VERSION 0x0040 divider --\n");
    do_reset();

    LegacyBresenham legacy_a(100000000ULL, 48000ULL);
    LegacyBresenham legacy_b( 50000000ULL, 48000ULL);

    uint64_t mismatch_a = 0;
    uint64_t mismatch_b = 0;
    uint64_t ta = 0;
    uint64_t tb = 0;
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
           static_cast<unsigned long long>(ta),
           static_cast<unsigned long long>(clocks),
           static_cast<unsigned long long>(mismatch_a));
    printf("   B( 50 MHz): %llu ticks in %llu clocks, %llu mismatches\n",
           static_cast<unsigned long long>(tb),
           static_cast<unsigned long long>(clocks),
           static_cast<unsigned long long>(mismatch_b));

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
void MediaNcoHarness::test_trim_point(const Shape& sh, int64_t trim, uint64_t want_ticks,
                                      bool is_a, double* out_ppm) {
    do_reset();
    if (is_a) dut->a_trim_i = static_cast<int32_t>(trim);
    else      dut->b_trim_i = static_cast<int32_t>(trim);

    NcoObserver obs(sh.spec);
    obs.reset(g_clock);

    // Discard the first tick for PERIOD purposes: it carries the reset phase,
    // not a period. The PHASE oracle counts from the very first tick.
    uint64_t seen = 0;
    uint64_t first_clock = 0;
    uint64_t last_clock = 0;
    bool have_first = false;

    // The phase oracle. phase at tick k is exactly ((k*(REM+trim)) mod DEN),
    // taken into [0,DEN). This is a closed form, not the DUT's recurrence, and
    // it is what makes a sub-LSB remainder error visible in a handful of ticks
    // instead of the ~144,000 the tick pattern alone would need.
    const int64_t  clamped_t = sh.spec.clamp(trim);
    const int64_t  den       = int64_t(sh.spec.fs_hz);
    const int64_t  step      = int64_t(sh.spec.rem()) + clamped_t;
    uint64_t k = 0;
    uint64_t phase_bad = 0;

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
        static_cast<long double>(E) * static_cast<long double>(sh.spec.fs_hz)
      - static_cast<long double>(N)
        * static_cast<long double>(int64_t(sh.spec.clk_hz) + clamped);
    const bool rate_exact =
        std::fabs(lhs) < static_cast<long double>(sh.spec.fs_hz);

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
           sh.name, static_cast<long long>(trim), meas, want, meas - want,
           static_cast<long long>(obs.min_period()),
           static_cast<long long>(obs.max_period()),
           obs.worst_drift());

    ok(N > 0, std::string(sh.name) + " produced ticks (vacuity guard)");
    ok(phase_bad == 0, std::string(sh.name) + " phase accumulator matches (k*(REM+trim)) mod DEN at trim "
                       + std::to_string(trim) + " (" + std::to_string(phase_bad) + " bad)");
    ok(rate_exact, std::string(sh.name) + " exact rate at trim " + std::to_string(trim));
    ok(phase_ok,   std::string(sh.name) + " phase bounded at trim " + std::to_string(trim));
    ok(bounds_ok,  std::string(sh.name) + " period in {DIV-1,DIV,DIV+1} at trim " + std::to_string(trim));
}

//! Gate on the measured ppm/LSB against the spec's own secant. The averaged
//! estimate carries ~0.05% of quantisation noise over the full +/-tmax span,
//! so this 0.5% gate sits ten times clear of the noise that would flake it.
constexpr double kSecantTol = 0.005;

//! Gate on the spec's secant against the derivative at trim 0. The exact ppm
//! curve is 1/(1+t/CLK), not a straight line, so a full-span secant is a few
//! percent off the tangent by construction; 5% admits that and no more.
constexpr double kDerivativeTol = 0.05;

void MediaNcoHarness::test_sweep(const Shape& sh, bool is_a, uint64_t ticks_per_point) {
    printf("\n-- 2/3/4. %s: rate, phase and period across the trim range --\n", sh.name);
    //! shape-relative, so the 50 MHz build exercises ITS whole range rather
    //! than clamping halfway through a list sized for the 100 MHz one
    const int64_t tmax = sh.spec.trim_max;
    const std::vector<int64_t> trims = {
        0, 1, -1, 10, -10, 100, -100, 1000, -1000,
        tmax / 4, -tmax / 4, tmax / 2, -tmax / 2, tmax, -tmax
    };
    double ppm_at_0 = 0.0;
    double ppm_at_p1000 = 0.0;
    double ppm_at_m1000 = 0.0;
    double ppm_at_pmax = 0.0;
    double ppm_at_mmax = 0.0;
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
           meas_lsb, static_cast<long long>(tmax), spec_lsb,
           static_cast<unsigned long long>(sh.spec.clk_hz), sh.spec.lsb_ppm());
    ok(std::fabs(meas_lsb - spec_lsb) < spec_lsb * kSecantTol,
       std::string(sh.name) + " trim LSB matches the spec secant within 0.5%");
    ok(std::fabs(spec_lsb - sh.spec.lsb_ppm()) < sh.spec.lsb_ppm() * kDerivativeTol,
       std::string(sh.name) + " LSB is 1e6/CLK_FREQ_HZ (secant within 5% of the derivative)");
}

// ------------------------------------------------------------------------ //
// 7. Clamp                                                                   //
// ------------------------------------------------------------------------ //
//! The rate the derived TRIM_MAX_P lands on, in ppm - the module's clamp is
//! 48000 - CLK%48000 LSB, which is +/-320 ppm at both shipping clocks.
constexpr double kAuthorityPpm = 319.9;

//! Tolerance on that authority. One ppm: wide enough for the averaged
//! estimate, far narrower than the 120 ppm of headroom over the servo's 200.
constexpr double kAuthorityTolPpm = 1.0;

void MediaNcoHarness::test_clamp(const Shape& sh, bool is_a, uint64_t ticks) {
    printf("\n-- 7. %s: trim beyond +/-TRIM_MAX_P saturates --\n", sh.name);
    const int64_t tmax = sh.spec.trim_max;
    double at_max = 0;
    double beyond = 0;
    double at_min = 0;
    double below = 0;
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
    ok(std::fabs(std::fabs(at_max) - kAuthorityPpm) < kAuthorityTolPpm,
       std::string(sh.name) + " derived authority is +/-320 ppm (covers the servo's +/-200)");
}

// ------------------------------------------------------------------------ //
// 8. A trim change mid-flight neither loses nor duplicates a sample          //
// ------------------------------------------------------------------------ //
//! The run this test observes: three equal thirds, so the grid is watched
//! free-running, then across a step down, then across a step back up.
constexpr uint64_t kDynamicClocks = 3000000;
constexpr uint64_t kDynamicStepDownAt = 1000000;
constexpr uint64_t kDynamicStepUpAt = 2000000;

//! The trim the run steps to. Well inside +/-TRIM_MAX_P at both clocks, so
//! what this test sees is the STEP, never the clamp that test 7 covers.
constexpr int32_t kDynamicTrimDown = -5000;
constexpr int32_t kDynamicTrimUp = 5000;

void MediaNcoHarness::test_dynamic(const Shape& sh, bool is_a) {
    printf("\n-- 8. %s: live trim change keeps the grid continuous --\n", sh.name);
    do_reset();
    if (is_a) dut->a_trim_i = 0; else dut->b_trim_i = 0;

    const int64_t div = int64_t(sh.spec.div());
    uint64_t ticks = 0;
    uint64_t last = 0;
    bool have_last = false;
    int64_t worst_lo = div + 99;
    int64_t worst_hi = 0;

    for (uint64_t c = 0; c < kDynamicClocks; ++c) {
        if (c == kDynamicStepDownAt) {
            if (is_a) dut->a_trim_i = kDynamicTrimDown;
            else      dut->b_trim_i = kDynamicTrimDown;
        }
        if (c == kDynamicStepUpAt) {
            if (is_a) dut->a_trim_i = kDynamicTrimUp;
            else      dut->b_trim_i = kDynamicTrimUp;
        }
        const Ticks t = tick_clock();
        const bool hit = is_a ? t.a : t.b;
        if (!hit) continue;
        if (have_last) {
            const int64_t p = int64_t(g_clock - last);
            if (p < worst_lo) worst_lo = p;
            if (p > worst_hi) worst_hi = p;
        }
        last = g_clock;
        have_last = true;
        ++ticks;
    }
    printf("   %llu ticks across two live trim steps, periods [%lld..%lld]\n",
           static_cast<unsigned long long>(ticks),
           static_cast<long long>(worst_lo), static_cast<long long>(worst_hi));
    ok(ticks > 0, std::string(sh.name) + " ticked across the trim steps (vacuity guard)");
    ok(worst_lo >= div - 1 && worst_hi <= div + 1,
       std::string(sh.name) + " no period glitch when the trim moves");
}

// ------------------------------------------------------------------------ //
// 9. The SERVO path: sign, scale, gating and clamp interaction.
//
//    This is the arithmetic that used to sit as four naked lines in
//    milan_datapath.sv with nothing able to exercise it. A sign error here is
//    a runaway servo, not a wrong number, so it is swept rather than argued.
//
//    Oracle, stated independently of the RTL:
//      servo u is signed, 1/16 ppm, and u > 0 means SPEED UP
//      one NCO LSB is 1/PPM_LSB ppm and POSITIVE trim SLOWS the grid
//      => trim = -(u * PPM_LSB) / 16, then clamped to +/-TRIM_MAX
//      => servo_en = 0 must ignore u entirely and use trim_i
// ------------------------------------------------------------------------ //
static long conv_oracle(const Shape& sh, long u, long ppm_lsb) {
    long t = -((u * ppm_lsb) >> 4);            // arithmetic shift, floors
    if (t >  sh.spec.trim_max) t =  sh.spec.trim_max;
    if (t < -sh.spec.trim_max) t = -sh.spec.trim_max;
    return t;
}

void MediaNcoHarness::test_servo(const Shape& sh, bool is_a, long ppm_lsb, uint64_t ticks) {
    printf("\n-- 9. %s: servo path (u in 1/16 ppm -> trim in LSB) --\n", sh.name);

    // The servo's own clamp is +-200 ppm = +-3200 in 1/16 ppm units. Sweep
    // past it on both sides so the NCO clamp interaction is covered too.
    const std::vector<long> us = { 0, 16, -16, 160, -160, 1600, -1600,
                                   3200, -3200, 8000, -8000, 32767, -32768 };

    for (long u : us) {
        // servo_en = 1: the grid must follow the converted command
        do_reset();
        if (is_a) { dut->a_servo_en_i = 1; dut->a_servo_trim_i = static_cast<int32_t>(u); }
        else      { dut->b_servo_en_i = 1; dut->b_servo_trim_i = static_cast<int32_t>(u); }

        const long  want_lsb = conv_oracle(sh, u, ppm_lsb);
        const double want_ppm = sh.spec.ppm(want_lsb);

        NcoObserver obs(sh.spec);
        obs.reset(g_clock);
        uint64_t seen = 0;
        uint64_t first = 0;
        uint64_t last = 0;
        bool have = false;
        while (seen <= ticks) {
            const Ticks t = tick_clock();
            const bool hit = is_a ? t.a : t.b;
            if (!hit) continue;
            obs.on_tick(g_clock, want_lsb);
            if (!have) { have = true; first = g_clock; } else { last = g_clock; ++seen; }
        }
        const long double lhs =
            static_cast<long double>(static_cast<int64_t>(last - first))
            * static_cast<long double>(sh.spec.fs_hz)
          - static_cast<long double>(seen)
            * static_cast<long double>(int64_t(sh.spec.clk_hz) + want_lsb);
        const bool exact =
            std::fabs(lhs) < static_cast<long double>(sh.spec.fs_hz);

        printf("   %s u %+7ld (1/16 ppm) -> trim %+7ld LSB, %+9.4f ppm "
               "(measured %+9.4f)\n",
               sh.name, u, want_lsb, want_ppm, obs.measured_ppm());
        ok(exact, std::string(sh.name) + " servo u=" + std::to_string(u)
                  + " lands on the converted rate exactly");
    }

    // SIGN, stated as its own check so a flipped negation cannot hide inside
    // a table of numbers: a POSITIVE u must make the grid FASTER.
    auto rate_at = [&](long u, bool en) {
        do_reset();
        if (is_a) { dut->a_servo_en_i = en; dut->a_servo_trim_i = static_cast<int32_t>(u); }
        else      { dut->b_servo_en_i = en; dut->b_servo_trim_i = static_cast<int32_t>(u); }
        NcoObserver o(sh.spec);
        o.reset(g_clock);
        uint64_t seen = 0;
        bool have = false;
        while (seen <= ticks) {
            const Ticks t = tick_clock();
            const bool hit = is_a ? t.a : t.b;
            if (!hit) continue;
            o.on_tick(g_clock, 0);
            if (!have) have = true; else ++seen;
        }
        return o.measured_ppm();
    };
    const double up = rate_at(1600, true);
    const double zero = rate_at(0, true);
    const double dn = rate_at(-1600, true);
    printf("   sign: u=+1600 -> %+.4f ppm, u=0 -> %+.4f, u=-1600 -> %+.4f\n", up, zero, dn);
    ok(up > zero, std::string(sh.name) + " servo u > 0 SPEEDS THE GRID UP");
    ok(dn < zero, std::string(sh.name) + " servo u < 0 slows the grid down");

    // GATING: servo_en = 0 must ignore u completely. This is the check that
    // was unfalsifiable at datapath level, because there the servo is idle at
    // u = 0 whenever the gate is closed - here u is forced non-zero.
    const double gated_off = rate_at(3200, false);
    const double gated_on  = rate_at(3200, true);
    printf("   gate: u=+3200 with servo_en=0 -> %+.4f ppm, servo_en=1 -> %+.4f\n",
           gated_off, gated_on);
    ok(std::fabs(gated_off) < 0.5,
       std::string(sh.name) + " servo_en=0 IGNORES a non-zero u (INTERNAL free-runs)");
    ok(std::fabs(gated_on - sh.spec.ppm(conv_oracle(sh, 3200, ppm_lsb))) < 0.5,
       std::string(sh.name) + " servo_en=1 follows that same u");
}

// ------------------------------------------------------------------------ //

//! Clocks the bit-exactness comparison runs for: 600 000 is 288 A ticks and
//! 576 B ticks, i.e. 6 ms and 12 ms of a 48 kHz grid, and every one of them
//! is compared against the legacy divider tick for tick.
constexpr uint64_t kBitExactClocks = 600000;

//! Ticks observed at each trim point. The rate verdict is integer-exact
//! (|E*FS - N*(CLK+trim)| < FS), so this only has to be enough ticks for the
//! period bounds and the printed ppm estimate to mean something.
constexpr uint64_t kTicksPerPoint = 1500;

//! PPM_LSB per shape, stated independently as CLK/1e6 rather than read from
//! the RTL, so a change to the module's derived default trips the servo
//! conversion checks instead of moving with them.
constexpr long kPpmLsbA = 100;
constexpr long kPpmLsbB = 50;

int MediaNcoHarness::run() {
    const milan::tb::Model<Vmedia_nco_wrap> model;
    dut = model.get();

    printf("======================================================================\n");
    printf("KL_media_nco - steerable media sample grid\n");
    printf("======================================================================\n");

    //! trim_max is stated INDEPENDENTLY here (48000 - CLK%48000) rather than
    //! read from the RTL, so a change to the module's derived default trips
    //! the clamp checks instead of silently moving with it
    const Shape A{ "A(100MHz)", NcoSpec{100000000ULL, 48000ULL, 32000} };
    const Shape B{ "B( 50MHz)", NcoSpec{ 50000000ULL, 48000ULL, 16000} };

    printf("   A: DIV %llu REM %llu, LSB %.4f ppm, authority +/-%.2f ppm\n",
           static_cast<unsigned long long>(A.spec.div()),
           static_cast<unsigned long long>(A.spec.rem()),
           A.spec.lsb_ppm(), std::fabs(A.spec.ppm(20000)));
    printf("   B: DIV %llu REM %llu, LSB %.4f ppm, authority +/-%.2f ppm\n",
           static_cast<unsigned long long>(B.spec.div()),
           static_cast<unsigned long long>(B.spec.rem()),
           B.spec.lsb_ppm(), std::fabs(B.spec.ppm(20000)));

    test_bit_exact(kBitExactClocks);

    test_sweep(A, true,  kTicksPerPoint);
    test_sweep(B, false, kTicksPerPoint);

    test_clamp(A, true,  kTicksPerPoint);
    test_clamp(B, false, kTicksPerPoint);

    test_dynamic(A, true);
    test_dynamic(B, false);

    //  PPM_LSB stated independently (CLK/1e6), so a change to the module's
    //  derived default trips the conversion checks instead of moving with them
    test_servo(A, true,  kPpmLsbA, kTicksPerPoint);
    test_servo(B, false, kPpmLsbB, kTicksPerPoint);

    printf("\n======================================================================\n");
    printf("media_nco: %ld checks: %ld PASS, %ld FAIL\n",
           g_checks, g_checks - g_fail, g_fail);
    printf("======================================================================\n");
    return g_fail == 0 ? 0 : 1;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    MediaNcoHarness harness;
    return harness.run();
}

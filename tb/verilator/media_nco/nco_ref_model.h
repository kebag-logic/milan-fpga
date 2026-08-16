// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Independent reference for KL_media_nco.
//
// This header deliberately does NOT re-implement the DUT's recurrence. It
// states the three DEFINING properties of a first-order fractional-N grid and
// checks the DUT against them, so a DUT that computes the right answer by a
// different route still passes and a DUT that copies its own bug does not.
//
//   P1  average period, exactly:  (CLK_FREQ_HZ + trim) / FS_HZ  clocks
//       (because DIV*DEN + REM == CLK_FREQ_HZ by construction, so the
//        remainder trim lands directly on the clock count - which is why the
//        LSB is 1/CLK_FREQ_HZ relative and independent of FS)
//   P2  bounded phase error: after N ticks the elapsed clock count is never
//       a whole clock away from N * P. This is what "zero long-term residual"
//       means and it is the property an averaging check alone cannot see.
//   P3  bounded instantaneous period: every period is in {DIV-1, DIV, DIV+1}.
//       A grid that hit the right average by alternating 2000 and 2166 would
//       satisfy P1 and P2-on-average and still be unusable.
//
// The exact ppm follows from P1 and is used as the accuracy oracle:
//       ppm(trim) = 1e6 * (CLK/(CLK+trim) - 1) = -1e6*trim/(CLK+trim)

#pragma once

#include <cstdint>
#include <cmath>
#include <algorithm>

struct NcoSpec {
    uint64_t clk_hz;
    uint64_t fs_hz;
    int64_t  trim_max;

    uint64_t div() const { return clk_hz / fs_hz; }
    uint64_t rem() const { return clk_hz % fs_hz; }

    int64_t clamp(int64_t trim) const {
        return std::max(-trim_max, std::min(trim_max, trim));
    }

    // P1: exact average period in clocks, as a double for reporting and as a
    // rational (num/den) for the drift check so no float error accumulates.
    double period(int64_t trim) const {
        return double(int64_t(clk_hz) + clamp(trim)) / double(fs_hz);
    }
    int64_t period_num(int64_t trim) const { return int64_t(clk_hz) + clamp(trim); }
    int64_t period_den() const              { return int64_t(fs_hz); }

    // The accuracy oracle: offset from the nominal FS, in ppm. Negative trim
    // speeds the grid up, which is the opposite of the servo's u convention -
    // the datapath negates between them and this sign is what pins it.
    double ppm(int64_t trim) const {
        const int64_t t = clamp(trim);
        return -1e6 * double(t) / double(int64_t(clk_hz) + t);
    }

    // The trim step, in ppm, at trim = 0. Exactly 1e6/clk_hz.
    double lsb_ppm() const { return 1e6 / double(clk_hz); }
};

// Accumulates observed ticks and grades them against the spec.
class NcoObserver {
public:
    explicit NcoObserver(const NcoSpec& s) : spec_(s) {}

    void reset(uint64_t at_clock) {
        ticks_ = 0;
        first_clock_ = at_clock;
        last_clock_  = at_clock;
        have_first_  = false;
        worst_drift_ = 0.0;
        min_period_  = INT64_MAX;
        max_period_  = 0;
    }

    // Call on every clock where tick_o is high. `trim` is the trim in force.
    void on_tick(uint64_t clock, int64_t trim) {
        trim_ = trim;
        if (!have_first_) {
            have_first_  = true;
            first_clock_ = clock;
            last_clock_  = clock;
            ticks_       = 0;
            return;
        }
        const int64_t p = int64_t(clock - last_clock_);
        min_period_ = std::min(min_period_, p);
        max_period_ = std::max(max_period_, p);
        last_clock_ = clock;
        ++ticks_;

        // P2: |elapsed - ticks*P| in clocks, kept in exact integer arithmetic.
        //   elapsed*den - ticks*num, scaled back by den
        const int64_t elapsed = int64_t(clock - first_clock_);
        const long double err =
            (long double)(elapsed * spec_.period_den()
                          - int64_t(ticks_) * spec_.period_num(trim_))
            / (long double)spec_.period_den();
        worst_drift_ = std::max(worst_drift_, (double)std::fabs(err));
    }

    uint64_t ticks()        const { return ticks_; }
    int64_t  min_period()   const { return min_period_; }
    int64_t  max_period()   const { return max_period_; }
    double   worst_drift()  const { return worst_drift_; }

    // Measured average period over the observation, in clocks.
    double avg_period() const {
        if (ticks_ == 0) return 0.0;
        return double(last_clock_ - first_clock_) / double(ticks_);
    }

    // Measured offset from nominal FS, in ppm.
    double measured_ppm() const {
        const double nominal = double(spec_.clk_hz) / double(spec_.fs_hz);
        const double p = avg_period();
        if (p <= 0.0) return 0.0;
        return 1e6 * (nominal / p - 1.0);
    }

private:
    NcoSpec  spec_;
    int64_t  trim_        = 0;
    uint64_t ticks_       = 0;
    uint64_t first_clock_ = 0;
    uint64_t last_clock_  = 0;
    bool     have_first_  = false;
    double   worst_drift_ = 0.0;
    int64_t  min_period_  = INT64_MAX;
    int64_t  max_period_  = 0;
};

// The divider KL_media_nco REPLACED, transcribed from milan_datapath.sv as it
// stood at VERSION 0x0040 (lines 479-502). It exists for exactly one check:
// that clock_source = INTERNAL (trim tied to 0) is bit-for-bit what shipped.
// It is NOT used as the oracle for anything else.
class LegacyBresenham {
public:
    LegacyBresenham(uint64_t clk_hz, uint64_t fs_hz)
        : div_(clk_hz / fs_hz), rem_(clk_hz % fs_hz), den_(fs_hz) {}

    // One clock. Returns true on the cycle the legacy block set media_tick_p.
    bool step() {
        const uint64_t sum = frac_ + rem_;
        const bool ov = (rem_ != 0) && (sum >= den_);
        const uint64_t end = div_ - 1 + (ov ? 1 : 0);
        if (cnt_ == end) {
            cnt_  = 0;
            frac_ = ov ? (sum - den_) : sum;
            return true;
        }
        ++cnt_;
        return false;
    }

private:
    uint64_t div_, rem_, den_;
    uint64_t cnt_ = 0, frac_ = 0;
};

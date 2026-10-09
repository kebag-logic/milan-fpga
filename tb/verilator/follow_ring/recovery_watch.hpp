// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once

#include <cmath>
#include <cstdio>
#include <vector>

//! Observe the implemented state, but derive quiet dwell independently of
//! its counter and threshold. The ruled band is +/-2 axis-clock cycles;
//! recovery requires 2048 consecutive media ticks within that band.
struct RecoveryWatch {
    struct Window { double start; double end; unsigned quiet_ticks; };
    std::vector<Window> windows;
    std::vector<double> arms;
    bool was_pending = false;
    bool was_recovering = false;
    unsigned quiet_ticks = 0;

    void sample(double now, int error, bool engaged, bool tick,
                bool pending, bool recovering) {
        if (pending && !was_pending) arms.push_back(now);
        if (recovering && !was_recovering) {
            windows.push_back({now, -1.0, 0});
            quiet_ticks = 0;
        } else if (was_recovering) {
            if (!engaged || std::abs(error) > 2) quiet_ticks = 0;
            else if (tick) ++quiet_ticks;
            if (!recovering) {
                windows.back().end = now;
                windows.back().quiet_ticks = quiet_ticks;
            }
        }
        was_pending = pending;
        was_recovering = recovering;
    }

    template <typename Checker>
    void check(Checker& ck, double start, double end) const {
        unsigned count = 0;
        for (const auto& w : windows) {
            if (w.start < start || w.start >= end) continue;
            ++count;
            std::printf("RECOVERY: action %.9f rearmed %.9f duration %.9f s quiet_ticks %u\n",
                        w.start, w.end, w.end - w.start, w.quiet_ticks);
            ck.that("[RECOVERY] re-arms after a full 2048-tick quiet dwell",
                    w.end > w.start && w.end < end && w.quiet_ticks >= 2048);
        }
        ck.that("[RECOVERY] observed an action and its recovery", count > 0);
    }
};

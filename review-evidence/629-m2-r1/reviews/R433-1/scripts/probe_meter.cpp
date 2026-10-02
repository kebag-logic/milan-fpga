// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Reviewer probes of KL_aaf_clock_meter (#629, round R433-1), independent of
// the lane's harness. Built against the head's own meter_wrap.sv and RTL by
// probe_meter.sh. Each probe prints PROBE <name> <measured> <expected> <verdict>.
// The design statements probed are in docs/design/MEDIA_CLOCK_FOLLOWING.md
// (Lost PDUs; The jump bound; The rate estimator).
#include "Vmeter_wrap.h"
#include "verilated.h"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <memory>
#include <random>
#include <string>
#include <vector>

namespace {
constexpr int kClk = CLK_HZ_TB;
constexpr int kSlot = kClk / 8000;
int g_fail = 0;

struct Tk {
    double ppm = 0;            // timestamp-spacing offset (the lane harness's convention)
    int64_t t0 = 1'000'000'000;
    std::function<int64_t(uint64_t)> err;
    int64_t stamp(uint64_t i) const {
        const long double sp = 125'000.0L * (1.0L + ppm * 1e-6L);
        int64_t v = t0 + static_cast<int64_t>(std::floor(static_cast<long double>(i) * sp));
        if (err) v += err(i);
        return v;
    }
};

struct Bench {
    std::unique_ptr<Vmeter_wrap> d{new Vmeter_wrap};
    uint64_t cyc = 0;
    uint64_t restarts = 0;
    uint8_t rq = 0;
    void tick() {
        d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); ++cyc;
        const auto r = static_cast<uint8_t>((d->status_o >> 8) & 0xFF);
        if (r != rq) { restarts += static_cast<uint8_t>(r - rq); rq = r; }
    }
    void reset(bool en = true) {
        d->rst_n = 0; d->en_i = 0; d->follow_idx_i = 0; d->bind_rise_i = 0;
        d->stopped_i = 0; d->match_p_i = 0; d->crf_p_i = 0;
        for (int i = 0; i < 4; ++i) tick();
        d->rst_n = 1; tick();
        d->en_i = en; tick();
        restarts = 0; rq = static_cast<uint8_t>((d->status_o >> 8) & 0xFF);
    }
    void pdu(const Tk& t, uint64_t i, bool tv = true) {
        d->match_p_i = 1; d->match_idx_i = 0; d->subtype_i = 2; d->tv_i = tv;
        d->tu_i = 0; d->mr_i = 0; d->seq_i = static_cast<uint8_t>(i & 0xFF);
        d->ts_i = static_cast<uint32_t>(static_cast<uint64_t>(t.stamp(i)));
        // INT_32BIT, 48 kHz, 8 channels, 6 samples: sdl 192
        d->fsh_i = (0x02ULL << 56) | (0x5ULL << 52) | (8ULL << 40) | (32ULL << 32) | (192ULL << 16);
        tick();
        d->match_p_i = 0;
    }
    void idle(int n) { for (int k = 0; k < n; ++k) tick(); }
};

void verdict(const char* name, const std::string& got, const std::string& want, bool ok) {
    std::printf("PROBE %-58s got=%-28s want=%-22s %s\n", name, got.c_str(), want.c_str(),
                ok ? "AGREE" : "DISAGREE");
    if (!ok) ++g_fail;
}

//! Run `pdus` slots of talker t, losing PDU i when lost(i); sample rate_valid
//! once per 512 ms of slots after `fill_s` seconds.
struct RunOut { uint64_t restarts; double valid_frac; int64_t first_valid_slot; };
RunOut run(Bench& b, const Tk& t, uint64_t pdus, const std::function<bool(uint64_t)>& lost,
           double fill_s = 0.0) {
    uint64_t samples = 0, valid = 0;
    int64_t first_valid = -1;
    for (uint64_t i = 0; i < pdus; ++i) {
        if (!lost || !lost(i)) b.pdu(t, i); else b.tick();
        b.idle(kSlot - 1);
        if (first_valid < 0 && b.d->rate_valid_o) first_valid = static_cast<int64_t>(i);
        if (i % 4096 == 4095 && static_cast<double>(i) * 125e-6 >= fill_s) {
            ++samples;
            if (b.d->rate_valid_o) ++valid;
        }
    }
    return {b.restarts, samples ? static_cast<double>(valid) / samples : 0.0, first_valid};
}

std::string s(double v, const char* f = "%.3f") { char x[64]; std::snprintf(x, sizeof x, f, v); return x; }
std::string u(uint64_t v) { return std::to_string(v); }

std::function<int64_t(uint64_t)> indep(int64_t j, uint64_t seed) {
    auto g = std::make_shared<std::mt19937_64>(seed);
    auto c = std::make_shared<std::vector<int64_t>>();
    return [g, c, j](uint64_t i) {
        while (c->size() <= i) c->push_back(static_cast<int64_t>((*g)() % (2 * j + 1)) - j);
        return (*c)[i];
    };
}
std::function<int64_t(uint64_t)> rsign(int64_t j, uint64_t seed) {
    auto g = std::make_shared<std::mt19937_64>(seed);
    auto c = std::make_shared<std::vector<int64_t>>();
    return [g, c, j](uint64_t i) {
        while (c->size() <= i / 16) c->push_back(((*g)() & 1U) ? j : -j);
        return (*c)[i / 16];
    };
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Bench b;

    // P1 random independent loss (Lost PDUs, "Random loss degrades the rate
    // gradually"): validity ~ e^(-4.096*500 q^2), restarts ~ 500 q^2 (1-q) per s.
    for (const double p : {1e-4, 1e-3, 2e-3}) {
        b.reset();
        Tk t; t.err = indep(1042, 0xA11 + static_cast<uint64_t>(p * 1e6));
        auto g = std::make_shared<std::mt19937_64>(0x1055 + static_cast<uint64_t>(p * 1e6));
        auto lost = [g, p](uint64_t) { return std::uniform_real_distribution<double>(0, 1)(*g) < p; };
        const double secs = 300.0;
        const RunOut r = run(b, t, static_cast<uint64_t>(secs * 8000), lost, 8.4);
        const double q = 1 - std::pow(1 - p, 16);
        const double rate = 500 * q * q * (1 - q);
        const double want_valid = std::exp(-4.096 * 500 * q * q);
        const double want_n = rate * secs;
        const bool ok = std::fabs(r.valid_frac - want_valid) < 0.12 &&
                        std::fabs(static_cast<double>(r.restarts) - want_n) <= 4 * std::sqrt(want_n) + 2;
        verdict(("P1 random loss p=" + s(p, "%.0e") + " 300 s").c_str(),
                "restarts " + u(r.restarts) + " valid " + s(r.valid_frac),
                "~" + s(want_n, "%.1f") + " / ~" + s(want_valid), ok);
    }

    // P2 aliasing runs (Lost PDUs rule 3): 255, 256, 257, 512 lost PDUs from a
    // group's PDU 0 or PDU 5 each restart the history exactly once.
    for (const uint64_t len : {255ULL, 256ULL, 257ULL, 512ULL}) {
        for (const uint64_t off : {0ULL, 5ULL}) {
            b.reset();
            Tk t; t.ppm = 100;
            const uint64_t at = 40 * 16 + off;
            const RunOut r = run(b, t, at + len + 2000, [at, len](uint64_t i) { return i >= at && i < at + len; });
            verdict(("P2 run of " + u(len) + " from PDU " + u(off)).c_str(), "restarts " + u(r.restarts), "1",
                    r.restarts == 1);
        }
    }
    // whole lost groups: 1 restarts nothing, 2..33 restart once
    for (uint64_t n = 1; n <= 33; ++n) {
        b.reset();
        Tk t; t.ppm = -100;
        const uint64_t at = 40 * 16;
        const RunOut r = run(b, t, at + n * 16 + 2000, [at, n](uint64_t i) { return i >= at && i < at + n * 16; });
        verdict(("P2 " + u(n) + " whole lost group(s)").c_str(), "restarts " + u(r.restarts),
                n == 1 ? "0" : "1", r.restarts == (n == 1 ? 0U : 1U));
    }

    // P3 tolerance (The jump bound): every shape to +/-1,748 ns at 300 ppm and
    // +/-2,048 ns at 0 ppm is accepted; 60 s each, both signs of the offset.
    struct Tol { const char* n; double ppm; int64_t j; bool ind; };
    for (const Tol& c : {Tol{"rsign 1,700 @+300", 300, 1700, false}, Tol{"rsign 1,700 @-300", -300, 1700, false},
                         Tol{"indep 1,740 @+300", 300, 1740, true}, Tol{"indep 1,740 @-300", -300, 1740, true},
                         Tol{"indep 2,000 @0", 0, 2000, true}, Tol{"rsign 2,000 @0", 0, 2000, false}}) {
        b.reset();
        Tk t; t.ppm = c.ppm; t.err = c.ind ? indep(c.j, 77) : rsign(c.j, 78);
        const RunOut r = run(b, t, 60 * 8000, nullptr, 4.2);
        verdict((std::string("P3 ") + c.n + ", 60 s").c_str(),
                "restarts " + u(r.restarts) + " valid " + s(r.valid_frac), "0 / 1.000",
                r.restarts == 0 && r.valid_frac > 0.999);
    }

    // P4 reorder and duplicate (Robustness): one swapped pair, or one duplicate
    // PDU, per second for 30 s: each voids one group and restarts nothing.
    for (int mode = 0; mode < 3; ++mode) {
        b.reset();
        Tk t; t.ppm = 50; t.err = indep(1000, 91);
        const uint64_t n = 30 * 8000;
        for (uint64_t i = 0; i < n; ++i) {
            const bool ev = (i % 8000) == 4003;
            if (mode == 0 && ev) {            // swap i and i+1
                b.pdu(t, i + 1); b.idle(kSlot / 2 - 1); b.pdu(t, i); b.idle(kSlot - kSlot / 2 - 1);
                b.pdu(t, i + 2); b.idle(kSlot - 1); i += 2; continue;
            }
            b.pdu(t, i, !(mode == 2 && ev));  // mode 2: tv clear on one PDU
            if (mode == 1 && ev) { b.idle(kSlot / 2 - 1); b.pdu(t, i); b.idle(kSlot - kSlot / 2 - 1); }
            else b.idle(kSlot - 1);
        }
        const char* nm[] = {"P4 swapped pair once a second, 30 s", "P4 duplicate PDU once a second, 30 s",
                            "P4 tv clear on one PDU a second, 30 s"};
        verdict(nm[mode], "restarts " + u(b.restarts) + " valid " + u(b.d->rate_valid_o), "0 / 1",
                b.restarts == 0 && b.d->rate_valid_o);
    }

    // P5 cold-start latency (The rate estimator): valid 2,048 groups after the
    // first complete group, i.e. at PDU ~32,783 + pipeline.
    {
        b.reset();
        Tk t;
        const RunOut r = run(b, t, 40000, nullptr);
        verdict("P5 first valid rate, ideal 0 ppm (PDU index)", u(static_cast<uint64_t>(r.first_valid_slot)),
                "32767..32800", r.first_valid_slot >= 32767 && r.first_valid_slot <= 32800);
    }

    std::printf("probe_meter: %d disagreement(s)\n", g_fail);
    return g_fail ? 1 : 0;
}

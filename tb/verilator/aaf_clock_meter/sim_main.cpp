// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_aaf_clock_meter, the meter rows of docs/design/MEDIA_CLOCK_FOLLOWING.md's
// test plan (#629). Each row is a named case; `Vmeter_sim CASE...` runs those
// cases only (mutants.py runs the case its mutant must fail), and no argument
// runs them all.
//
// THE TALKER MODEL. A synthetic AAF talker in Milan v1.2 6.2's 48 kHz Base
// format: 6 samples and one presentation timestamp per PDU, sequence_num
// incrementing modulo 256. Its "ppm" is the offset of its TIMESTAMP SPACING
// from nominal, the design's convention (a +300 ppm talker's 4 ms spans
// 4 ms + 1,200 ns): PDU i is stamped t0 + i * 125,000 * (1 + ppm 1e-6) ns,
// rounded down, plus the case's error shape and step. The planted rate in
// the meter's units (gPTP ns per 512 ms of the talker's media time, minus
// 512 ms) is therefore 512 * ppm.
//
// TIME. clk_i runs at CLK_HZ_TB (the Makefile's one value, which also sets
// the RTL's CLK_FREQ_HZ_P), and one PDU slot is CLK_HZ_TB / 8000 cycles,
// 125 us. Only the meter's 100 ms timeout reads cycles; every rate is the
// timestamps' own arithmetic, so the compression changes no rate.
//
// Random error shapes come from a pinned 64-bit generator mapped by a modulo
// (portable, unlike std::uniform_int_distribution), so every run of every
// build sees the same stimulus.

#include "../../common/verilator_harness.hpp"
#include "Vmeter_wrap.h"
#include "Vmeter_wrap___024root.h"
#include "verilated.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <memory>
#include <random>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int kClkHz = CLK_HZ_TB;
constexpr int kSlotCyc = kClkHz / 8000;          //! one 125 us PDU slot
constexpr int64_t kPduNs = 125'000;
constexpr int kGroupPdus = 16;
constexpr int kHistGroups = 2048;                 //! E8: 8 x 256 groups
constexpr int64_t kOneSampleNs = 20'833;          //! 1 / 48 kHz
constexpr int64_t kHalfSampleNs = 10'417;
constexpr int64_t kJ = 1'426;                     //! the design point
constexpr double kDesignPpm = 300.0;
constexpr uint64_t kSeed = 0x629'0000'4D33'7E42ULL;
constexpr double kPi = 3.14159265358979323846;

//! The AAF format-specific header word (IEEE 1722-2016 Figure 26) for a
//! stream of `samples` samples per PDU at `cpf` channels.
uint64_t aaf_fsh(int format, int nsr, int cpf, int samples, bool sparse) {
    const uint64_t sdl = static_cast<uint64_t>(samples) * 4 * static_cast<uint64_t>(cpf);
    return (static_cast<uint64_t>(format) << 56) | (static_cast<uint64_t>(nsr) << 52) |
           (static_cast<uint64_t>(cpf) << 40) | (32ULL << 32) | (sdl << 16) |
           (sparse ? (1ULL << 12) : 0ULL);
}

//! One synthetic talker: its clock, its error shape, its losses and steps.
struct Talker {
    double ppm = 0.0;
    int64_t t0 = 1'000'000'000;
    uint8_t subtype = 2;                          //! AAF
    bool tv = true;
    bool tu = false;
    bool mr = false;
    uint64_t fsh = aaf_fsh(0x02, 0x5, 8, 6, false);
    std::function<int64_t(uint64_t)> err;         //! per-PDU error, ns
    std::function<bool(uint64_t)> lost;           //! PDU i never arrives
    uint64_t step_at = UINT64_MAX;                //! first PDU of a step
    int64_t step_ns = 0;
    uint64_t n = 0;                               //! next PDU index

    int64_t ideal(uint64_t i) const {
        const long double spacing = 125'000.0L * (1.0L + ppm * 1e-6L);
        return t0 + static_cast<int64_t>(std::floor(static_cast<long double>(i) * spacing));
    }
    int64_t stamp(uint64_t i) const {
        int64_t v = ideal(i);
        if (err) v += err(i);
        if (i >= step_at) v += step_ns;
        return v;
    }
    uint8_t seq(uint64_t i) const { return static_cast<uint8_t>(i & 0xFF); }
};

//! What the bench saw while a run lasted.
struct Seen {
    uint64_t restarts = 0;                        //! data-caused, status[15:8]
    uint64_t disrupts = 0;
    uint64_t mr_toggles = 0;
    uint64_t rate_updates = 0;
    int64_t first_valid_cyc = -1;
    bool valid_fell = false;
    int64_t worst_rate_err = 0;                   //! |rate - planted|, max
    int64_t worst_crf_diff = 0;                   //! |rate - KL_crf_rx rate|, max
    std::vector<int32_t> rates;                   //! every published rate
    int64_t last_restart_cyc = -1;
    uint64_t lock_falls = 0;                      //! locked_o 1 -> 0 transitions
};

class MeterBench {
 public:
    explicit MeterBench(milan::tb::Checker& check) : check_(check) {}

    Vmeter_wrap* dut = nullptr;
    uint64_t cyc = 0;
    Seen seen;
    int64_t planted = 0;                          //! the rate the run expects
    bool track_crf = false;

    //! Reset, deselected, both listeners started and unbound-edge free.
    void reset() {
        dut->rst_n = 0;
        dut->en_i = 0;
        dut->follow_idx_i = 0;
        dut->bind_rise_i = 0;
        dut->stopped_i = 0;
        dut->match_p_i = 0;
        dut->crf_p_i = 0;
        for (int i = 0; i < 4; ++i) tick();
        dut->rst_n = 1;
        tick();
        seen = Seen{};
    }

    //! One clk_i cycle, then the observation of its outputs.
    void tick() {
        dut->clk_i = 0;
        dut->eval();
        dut->clk_i = 1;
        dut->eval();
        ++cyc;
        observe();
    }
    void idle(int64_t cycles) {
        for (int64_t i = 0; i < cycles; ++i) tick();
    }

    //! Deliver talker `t`'s next PDU on listener `idx` (unless it is lost),
    //! with the equivalent CRF PDU at each group's PDU 0 when `crf` is set,
    //! then spend the rest of the slot.
    void slot(Talker& t, int idx, bool crf = false) {
        const uint64_t i = t.n++;
        const bool deliver = !(t.lost && t.lost(i));
        if (deliver) drive_pdu(t, idx, i);
        if (crf && (i % kGroupPdus) == 0) {
            dut->crf_p_i = 1;
            dut->crf_seq_i = static_cast<uint8_t>((i / kGroupPdus) & 0xFF);
            dut->crf_ts_i = static_cast<uint64_t>(t.stamp(i));
        }
        tick();
        dut->match_p_i = 0;
        dut->crf_p_i = 0;
        idle(kSlotCyc - 1);
    }
    //! Two talkers on listeners 0 and 1, half a slot apart.
    void slot2(Talker& a, Talker& b, bool deliver_a = true, bool deliver_b = true) {
        const uint64_t ia = a.n++;
        if (deliver_a) drive_pdu(a, 0, ia);
        tick();
        dut->match_p_i = 0;
        idle(kSlotCyc / 2 - 1);
        const uint64_t ib = b.n++;
        if (deliver_b) drive_pdu(b, 1, ib);
        tick();
        dut->match_p_i = 0;
        idle(kSlotCyc - kSlotCyc / 2 - 1);
    }
    void run_seconds(Talker& t, double s, bool crf = false) {
        const auto slots = static_cast<uint64_t>(s * 8000.0);
        for (uint64_t k = 0; k < slots; ++k) slot(t, 0, crf);
    }

    bool locked() const { return dut->locked_o != 0; }
    bool rate_valid() const { return dut->rate_valid_o != 0; }
    double seconds() const { return static_cast<double>(cyc) / kClkHz; }

 private:
    milan::tb::Checker& check_;
    uint8_t restart_q_ = 0;
    bool valid_q_ = false;
    bool locked_q_ = false;
    bool rate_pending_ = false;

    void drive_pdu(const Talker& t, int idx, uint64_t i) {
        dut->match_p_i = 1;
        dut->match_idx_i = static_cast<uint8_t>(idx);
        dut->subtype_i = t.subtype;
        dut->tv_i = t.tv;
        dut->tu_i = t.tu;
        dut->mr_i = t.mr;
        dut->seq_i = t.seq(i);
        dut->ts_i = static_cast<uint32_t>(static_cast<uint64_t>(t.stamp(i)));
        dut->fsh_i = t.fsh;
    }

    void observe() {
        const auto restarts = static_cast<uint8_t>((dut->status_o >> 8) & 0xFF);
        if (restarts != restart_q_) {
            seen.restarts += static_cast<uint8_t>(restarts - restart_q_);
            seen.last_restart_cyc = static_cast<int64_t>(cyc);
            restart_q_ = restarts;
        }
        if (dut->disrupt_p_o) ++seen.disrupts;
        const bool lk = locked();
        if (!lk && locked_q_) ++seen.lock_falls;
        locked_q_ = lk;
        if (dut->mr_toggle_p_o) ++seen.mr_toggles;
        const bool valid = rate_valid();
        if (valid && seen.first_valid_cyc < 0) seen.first_valid_cyc = static_cast<int64_t>(cyc);
        if (!valid && valid_q_) seen.valid_fell = true;
        valid_q_ = valid;
        if (rate_pending_) {
            rate_pending_ = false;
            record_rate();
        }
        if (dut->rootp->meter_wrap__DOT__meter__DOT__g5_v_r) rate_pending_ = true;
    }

    void record_rate() {
        const int32_t r = dut->rate_o;
        ++seen.rate_updates;
        seen.rates.push_back(r);
        const int64_t e = std::llabs(static_cast<int64_t>(r) - planted);
        if (e > seen.worst_rate_err) seen.worst_rate_err = e;
        if (track_crf && dut->crf_rate_valid_o) {
            const int64_t d = std::llabs(static_cast<int64_t>(r) -
                                         static_cast<int32_t>(dut->crf_rate_o));
            if (d > seen.worst_crf_diff) seen.worst_crf_diff = d;
        }
    }
};

//! The planted rate of a talker whose timestamp spacing is off by `ppm`.
int64_t planted_rate(double ppm) {
    return static_cast<int64_t>(std::llround(512e6 * ppm * 1e-6));
}

//! Error shapes at amplitude `j` (design, The rate estimator).
std::function<int64_t(uint64_t)> independent(int64_t j, uint64_t seed) {
    auto gen = std::make_shared<std::mt19937_64>(seed);
    auto cache = std::make_shared<std::vector<int64_t>>();
    return [gen, cache, j](uint64_t i) {
        while (cache->size() <= i) {
            cache->push_back(static_cast<int64_t>((*gen)() % static_cast<uint64_t>(2 * j + 1)) - j);
        }
        return (*cache)[i];
    };
}
std::function<int64_t(uint64_t)> random_sign_group(int64_t j, uint64_t seed) {
    auto gen = std::make_shared<std::mt19937_64>(seed);
    auto cache = std::make_shared<std::vector<int64_t>>();
    return [gen, cache, j](uint64_t i) {
        const uint64_t g = i / kGroupPdus;
        while (cache->size() <= g) cache->push_back(((*gen)() & 1U) ? j : -j);
        return (*cache)[g];
    };
}
std::function<int64_t(uint64_t)> periodic(int64_t j, double period_s) {
    return [j, period_s](uint64_t i) {
        const double t = static_cast<double>(i) * 125e-6;
        return static_cast<int64_t>(std::llround(static_cast<double>(j) *
                                                 std::sin(2.0 * kPi * t / period_s)));
    };
}
//! +/-J held over each 512 ms block (256 groups), the sign flipping every 8
//! blocks: each E8 two-point difference then spans opposite signs, 2J / 8.
std::function<int64_t(uint64_t)> worst_case(int64_t j) {
    return [j](uint64_t i) {
        const uint64_t block = i / (static_cast<uint64_t>(kGroupPdus) * 256);
        return ((block / 8) % 2 == 0) ? j : -j;
    };
}


// ------------------------------------------------------------------------
//  Case helpers
// ------------------------------------------------------------------------
using milan::tb::Checker;

//! A labelled check whose label carries the case's own parameters.
bool named(Checker& ck, const std::string& what, bool ok) {
    return ck.that(what.c_str(), ok);
}

//! Reset and follow listener 0, the run expecting `ppm`'s planted rate.
void follow(MeterBench& b, double ppm) {
    b.reset();
    b.planted = planted_rate(ppm);
    b.track_crf = false;
    b.dut->en_i = 1;
    b.dut->follow_idx_i = 0;
    //! entry is an era start, and an era start wins over a PDU in its own
    //! cycle: let it land before the stream's first PDU
    b.tick();
}

//! The rate validated within 4.2 s of the stream's start (2048 groups,
//! 4.096 s, plus the first group and the pipeline) and never fell after.
bool valid_by_42_and_held(const MeterBench& b, int64_t start_cyc) {
    const auto by = static_cast<int64_t>(4.2 * kClkHz);
    return b.seen.first_valid_cyc >= 0 && b.seen.first_valid_cyc - start_cyc <= by &&
           !b.seen.valid_fell;
}

//! Run `seconds` of talker `t` on listener 0 and return the cycle at which
//! its PDU `mark` was driven (-1 when the run never reached it).
int64_t run_marking(MeterBench& b, Talker& t, double seconds, uint64_t mark) {
    int64_t at = -1;
    const auto slots = static_cast<uint64_t>(seconds * 8000.0);
    for (uint64_t k = 0; k < slots; ++k) {
        if (t.n == mark) at = static_cast<int64_t>(b.cyc);
        b.slot(t, 0);
    }
    return at;
}

//! The design's "a deviation above the jump bound restarts the history at
//! once": the one restart lands inside the slot of the PDU that carried the
//! step, so a verdict deferred to the group's PDU 15 (round 4's rule) or to
//! the spacing check at the group's end fails it.
bool restart_at_pdu(const MeterBench& b, int64_t pdu_cyc) {
    return pdu_cyc >= 0 && b.seen.restarts == 1 && b.seen.last_restart_cyc > pdu_cyc &&
           b.seen.last_restart_cyc - pdu_cyc <= kSlotCyc;
}

std::string fmt(const char* pattern, double v) {
    std::array<char, 160> buf{};
    std::snprintf(buf.data(), buf.size(), pattern, v);
    return buf.data();
}

// ------------------------------------------------------------------------
//  M1, the largest deviation's level (max_dev_ns_o, AAFM_STAT[31:16]): every
//  era start clears it and it reads zero while not following, a data
//  restart keeps it, a PDU after a sequence gap is no deviation, and it
//  saturates at 65,535 ns. follow() resets before each M1 rate, so only a
//  run across an era start can see a stale maximum. Run by case_rates.
//  Mutants (the PR #634 round-2 reviews' probes): the era-start clear
//  removed; the saturation removed; the PDU after a gap measured.
// ------------------------------------------------------------------------
uint64_t max_dev(const MeterBench& b) { return b.dut->status_o >> 16; }

//! The era `event` ends follows a +100 ppm talker on listener 0, whose
//! largest deviation is the offset over 15 spacings, 187.5 ns; the era it
//! starts follows a 0 ppm talker (on listener 1 when `two`), whose ideal
//! timestamps deviate by nothing.
void max_dev_era(MeterBench& b, Checker& ck, const char* name, bool two,
                 const std::function<void()>& event) {
    follow(b, 100.0);
    Talker old_era;
    old_era.ppm = 100.0;
    Talker new_era;
    new_era.t0 = 7'000'000'000;
    for (int k = 0; k < 800; ++k) {
        if (two) b.slot2(old_era, new_era); else b.slot(old_era, 0);
    }
    const std::string tag = std::string("[M1 max_dev, ") + name + "] ";
    const uint64_t before = max_dev(b);
    named(ck, tag + "the old era's largest deviation is the offset over 15 spacings",
          before >= 187 && before <= 189);
    event();
    for (int k = 0; k < 800; ++k) {
        if (two) b.slot2(old_era, new_era); else b.slot(new_era, 0);
    }
    ck.dec((tag + "the new era's largest deviation reads 0").c_str(), max_dev(b), 0);
}

void max_dev_levels(MeterBench& b, Checker& ck) {
    max_dev_era(b, ck, "listener change", true, [&b] { b.dut->follow_idx_i = 1; });
    max_dev_era(b, ck, "entry", false, [&b, &ck] {
        b.dut->en_i = 0;
        b.idle(kSlotCyc);
        ck.dec("[M1 max_dev, exit] reads 0 while not following", max_dev(b), 0);
        b.dut->en_i = 1;
    });
    max_dev_era(b, ck, "bind edge", false, [&b] {
        b.dut->bind_rise_i = 1;
        b.tick();
        b.dut->bind_rise_i = 0;
    });
    max_dev_era(b, ck, "timeout", false, [&b, &ck] {
        b.idle(static_cast<int64_t>(0.15 * 8000) * kSlotCyc);
        ck.dec("[M1 max_dev, timeout] reads 0 once the timeout starts an era", max_dev(b), 0);
    });
    // one lost PDU inside a group: the PDU after the gap is not compared
    // with the group's PDU 0, so it is no deviation
    follow(b, 0.0);
    Talker lossy;
    lossy.lost = [](uint64_t i) { return i == 30 * kGroupPdus + 5; };
    b.run_seconds(lossy, 0.12);
    ck.dec("[M1 max_dev, a lost PDU] the PDU after the gap is no deviation", max_dev(b), 0);
    // a step at PDU 5 is that PDU's deviation, the history restarts at it,
    // and the restart keeps the reading
    for (const int64_t step : {int64_t{65'535}, int64_t{65'536}, int64_t{100'000},
                               int64_t{-100'000}}) {
        follow(b, 0.0);
        Talker t;
        t.step_at = 30 * kGroupPdus + 5;
        t.step_ns = step;
        b.run_seconds(t, 0.12);
        std::array<char, 112> label{};
        std::snprintf(label.data(), label.size(),
                      "[M1 max_dev, step %+lld @5] restarts the history once",
                      static_cast<long long>(step));
        ck.dec(label.data(), b.seen.restarts, 1);
        std::snprintf(label.data(), label.size(),
                      "[M1 max_dev, step %+lld @5] reads min(|step|, 65,535) after it",
                      static_cast<long long>(step));
        ck.dec(label.data(), max_dev(b),
               static_cast<uint64_t>(std::min<int64_t>(std::llabs(step), 65'535)));
    }
}

// ------------------------------------------------------------------------
//  M1: synthetic streams at seven rates, ideal timestamps, against
//  KL_crf_rx on the equivalent CRF stimulus, and the largest deviation the
//  meter reports (max_dev_ns_o, the wrapper's status_o[31:16]), then that
//  value's level (max_dev_levels). Mutants: decimation by 1; the largest
//  deviation not tracked; and max_dev_levels' three.
// ------------------------------------------------------------------------
void case_rates(MeterBench& b, Checker& ck) {
    for (const double ppm : {0.0, 10.64, -10.64, 50.0, -50.0, 100.0, -100.0}) {
        follow(b, ppm);
        b.track_crf = true;
        Talker t;
        t.ppm = ppm;
        const auto start = static_cast<int64_t>(b.cyc);
        b.run_seconds(t, 6.2, true);
        named(ck, fmt("[M1 %+.2f ppm] rate_valid rises within 4.2 s and holds", ppm),
              valid_by_42_and_held(b, start));
        named(ck, fmt("[M1 %+.2f ppm] at least three rate updates", ppm),
              b.seen.rate_updates >= 3);
        named(ck, fmt("[M1 %+.2f ppm] rate equals KL_crf_rx's within 1 LSB", ppm),
              b.seen.worst_crf_diff <= 1);
        named(ck, fmt("[M1 %+.2f ppm] rate equals the planted rate within 1 LSB", ppm),
              b.seen.worst_rate_err <= 1);
        //! ideal timestamps deviate from PDU 0 only by the offset, which
        //! accumulates over a group's 15 spacings; the floors add up to 1 ns
        const double dev = 15.0 * static_cast<double>(kPduNs) * std::fabs(ppm) * 1e-6;
        const auto max_dev = static_cast<double>(b.dut->status_o >> 16);
        named(ck, fmt("[M1 %+.2f ppm] the largest deviation is the offset over 15 spacings", ppm),
              std::fabs(max_dev - dev) <= 1.5);
        std::printf("  info: M1 %+.2f ppm: %llu updates, worst |rate - planted| %lld, "
                    "|rate - crf| %lld\n", ppm,
                    static_cast<unsigned long long>(b.seen.rate_updates),
                    static_cast<long long>(b.seen.worst_rate_err),
                    static_cast<long long>(b.seen.worst_crf_diff));
    }
    max_dev_levels(b, ck);
}

// ------------------------------------------------------------------------
//  M2: the design point in four error shapes, 120 s each, +300 ppm.
//  Mutants: E1, B1 (2048 ns bound), P1 (first-PDU pick).
// ------------------------------------------------------------------------
void case_shapes(MeterBench& b, Checker& ck) {
    struct Shape {
        const char* name;
        std::function<int64_t(uint64_t)> err;
        int64_t bound;
    };
    const std::array<Shape, 4> shapes = {{
        {"indep", independent(kJ, kSeed), 256},
        {"rsign", random_sign_group(kJ, kSeed + 1), 360},
        {"p10ms", periodic(kJ, 0.010), 360},
        {"worst", worst_case(kJ), 360},
    }};
    for (const Shape& sh : shapes) {
        follow(b, kDesignPpm);
        Talker t;
        t.ppm = kDesignPpm;
        t.err = sh.err;
        const auto start = static_cast<int64_t>(b.cyc);
        b.run_seconds(t, 120.0);
        const std::string tag = std::string("[M2 ") + sh.name + "] ";
        named(ck, tag + "no history restart", b.seen.restarts == 0);
        named(ck, tag + "rate_valid rises within 4.2 s and holds", valid_by_42_and_held(b, start));
        named(ck, tag + "every rate within 360 ns of the planted rate",
              b.seen.worst_rate_err <= 360 && b.seen.rate_updates > 200);
        if (sh.bound < 360) {
            named(ck, tag + "every rate within 256 ns of the planted rate",
                  b.seen.worst_rate_err <= sh.bound);
        }
        std::printf("  info: M2 %s: %llu restarts, %llu rates, worst %lld ns\n", sh.name,
                    static_cast<unsigned long long>(b.seen.restarts),
                    static_cast<unsigned long long>(b.seen.rate_updates),
                    static_cast<long long>(b.seen.worst_rate_err));
    }
}

// ------------------------------------------------------------------------
//  M3: beyond the tolerance, and real steps. Mutants: B3 (16384 ns),
//  the within-group void removed.
// ------------------------------------------------------------------------
void beyond_one(MeterBench& b, Checker& ck, const char* name, double ppm,
                std::function<int64_t(uint64_t)> shape) {
    follow(b, ppm);
    Talker t;
    t.ppm = ppm;
    const uint64_t stop = 12 * 8000;
    t.err = [shape, stop](uint64_t i) { return i < stop ? shape(i) : 0; };
    b.run_seconds(t, 12.0);
    const std::string tag = std::string("[M3 ") + name + "] ";
    named(ck, tag + "the error restarts the history", b.seen.restarts > 0);
    named(ck, tag + "rate_valid stays low while the error lasts", b.seen.first_valid_cyc < 0);
    b.run_seconds(t, 6.0);
    const int64_t hist = static_cast<int64_t>(kHistGroups) * kGroupPdus * kSlotCyc;
    const int64_t gap = b.seen.first_valid_cyc - b.seen.last_restart_cyc;
    named(ck, tag + "rate_valid returns 2048 picks after the last restart",
          b.seen.first_valid_cyc > 0 && gap >= hist - kSlotCyc &&
              gap <= hist + 2 * kGroupPdus * kSlotCyc);
    std::printf("  info: M3 %s: %llu restarts; valid %lld cycles after the last\n", name,
                static_cast<unsigned long long>(b.seen.restarts), static_cast<long long>(gap));
}

void case_beyond(MeterBench& b, Checker& ck) {
    beyond_one(b, ck, "rsign1800", kDesignPpm, random_sign_group(1'800, kSeed + 2));
    beyond_one(b, ck, "indep2100", 0.0, independent(2'100, kSeed + 3));
    for (const int64_t step : {kOneSampleNs, -kOneSampleNs, kHalfSampleNs, -kHalfSampleNs}) {
        for (int pos = 0; pos < kGroupPdus; ++pos) {
            follow(b, 0.0);
            Talker t;
            t.step_at = 30 * kGroupPdus + static_cast<uint64_t>(pos);
            t.step_ns = step;
            const int64_t at = run_marking(b, t, 0.12, t.step_at);
            std::array<char, 112> label{};
            std::snprintf(label.data(), label.size(),
                          "[M3 step %+lld @%d] restarts the history once",
                          static_cast<long long>(step), pos);
            ck.dec(label.data(), b.seen.restarts, 1);
            //! a step at PDU 0 moves the group's own reference, so only the
            //! spacing check at the group's end can see it
            if (pos == 0) continue;
            std::snprintf(label.data(), label.size(),
                          "[M3 step %+lld @%d] the restart lands at the step's PDU",
                          static_cast<long long>(step), pos);
            named(ck, label.data(), restart_at_pdu(b, at));
        }
    }
}

// ------------------------------------------------------------------------
//  M4: only the 48 kHz Base format with 6 samples per PDU is consumed.
//  Mutants: the stream_data_length check removed; channels_per_frame 0
//  accepted (its stream_data_length, 0, matches 24 x 0).
// ------------------------------------------------------------------------
void case_format(MeterBench& b, Checker& ck) {
    struct Fmt {
        const char* name;
        uint64_t fsh;
        bool locks;
    };
    const std::array<Fmt, 7> fmts = {{
        {"6-sample INT_32BIT 48k", aaf_fsh(0x02, 0x5, 8, 6, false), true},
        {"12-sample", aaf_fsh(0x02, 0x5, 8, 12, false), false},
        {"8-sample", aaf_fsh(0x02, 0x5, 8, 8, false), false},
        {"sparse", aaf_fsh(0x02, 0x5, 8, 6, true), false},
        {"nsr 96 kHz", aaf_fsh(0x02, 0x7, 8, 6, false), false},
        {"INT_24BIT", aaf_fsh(0x03, 0x5, 8, 6, false), false},
        {"0 channels", aaf_fsh(0x02, 0x5, 0, 6, false), false},
    }};
    for (const Fmt& f : fmts) {
        follow(b, 0.0);
        Talker t;
        t.fsh = f.fsh;
        b.run_seconds(t, 0.05);
        named(ck, std::string("[M4 ") + f.name + "] " + (f.locks ? "locks" : "does not lock"),
              b.locked() == f.locks);
    }
}

// ------------------------------------------------------------------------
//  M5: 10 s across 312 sequence_num wraps. Mutant: continuity compared
//  without the 8-bit wrap.
// ------------------------------------------------------------------------
void case_wrap(MeterBench& b, Checker& ck) {
    follow(b, 100.0);
    Talker t;
    t.ppm = 100.0;
    const auto start = static_cast<int64_t>(b.cyc);
    b.run_seconds(t, 10.0);
    std::printf("  info: M5: %llu sequence wraps\n", static_cast<unsigned long long>(t.n / 256));
    named(ck, "[M5] zero restarts across the sequence wraps", b.seen.restarts == 0);
    named(ck, "[M5] rate_valid from 4.1 s on and held", valid_by_42_and_held(b, start));
}

// ------------------------------------------------------------------------
//  M6: lock after 8 consumed PDUs, unlock 100 ms after the last; a sequence
//  gap before lock restarts the settle run. Mutants: the timeout disabled; a
//  gap that does not break the settle run.
// ------------------------------------------------------------------------
void case_lock(MeterBench& b, Checker& ck) {
    follow(b, 0.0);
    Talker t;
    for (int k = 0; k < 7; ++k) b.slot(t, 0);
    named(ck, "[M6] not locked after 7 PDUs", !b.locked());
    b.slot(t, 0);
    named(ck, "[M6] locked after the 8th PDU", b.locked());
    for (int k = 0; k < 40; ++k) b.slot(t, 0);
    const uint64_t last = b.cyc - static_cast<uint64_t>(kSlotCyc);
    const uint64_t tout = static_cast<uint64_t>(kClkHz) / 10;
    while (b.locked() && b.cyc < last + 2 * tout) b.tick();
    const uint64_t after = b.cyc - last;
    named(ck, "[M6] unlocks 100 ms after the last PDU", !b.locked() && after >= tout &&
              after <= tout + 8);
    named(ck, "[M6] the unlock is one disruption pulse", b.seen.disrupts == 1);
    // five clean PDUs, PDU 5 lost: the PDU after the gap counts nothing, so
    // the lock needs eight clean PDUs after it
    follow(b, 0.0);
    Talker g;
    g.lost = [](uint64_t i) { return i == 5; };
    for (int k = 0; k < 6; ++k) b.slot(g, 0);
    for (int k = 0; k < 8; ++k) b.slot(g, 0);
    named(ck, "[M6 gap before lock] not locked at the gap PDU and 7 clean PDUs after it",
          !b.locked());
    b.slot(g, 0);
    named(ck, "[M6 gap before lock] locked at the 8th clean PDU after the gap", b.locked());
}

// ------------------------------------------------------------------------
//  M7: the history restarts, and what each does to a held lock: a tu edge
//  and the bind edge keep it, a change of the followed listener and entry
//  clear it, silently. Mutants: no restart on the tu edge; a listener change
//  keeping the lock; the bind edge clearing it. The meter takes tu as a
//  port, so the design's "tu taken from the tv net" is a wiring mutant and
//  runs at the root (tb/verilator/milan_dp_mclk, mutant 15).
// ------------------------------------------------------------------------
void restart_event(MeterBench& b, Checker& ck, const char* name,
                   const std::function<void(Talker&, Talker&)>& event, bool two,
                   uint64_t lock_falls) {
    follow(b, 100.0);
    Talker a;
    a.ppm = 100.0;
    Talker c;
    c.ppm = 100.0;
    c.t0 = 7'000'000'000;
    for (int k = 0; k < static_cast<int>(4.3 * 8000); ++k) {
        if (two) b.slot2(a, c); else b.slot(a, 0);
    }
    const std::string tag = std::string("[M7 ") + name + "] ";
    named(ck, tag + "rate valid before the event", b.rate_valid());
    named(ck, tag + "locked before the event", b.locked());
    b.seen.valid_fell = false;
    b.seen.first_valid_cyc = -1;
    const uint64_t lf0 = b.seen.lock_falls;
    const uint64_t d0 = b.seen.disrupts;
    event(a, c);
    for (int k = 0; k < 800; ++k) {
        if (two) b.slot2(a, c); else b.slot(a, 0);
    }
    named(ck, tag + "rate_valid falls at the event", b.seen.valid_fell || !b.rate_valid());
    ck.dec((tag + (lock_falls ? "the held lock clears at the event"
                              : "the held lock is kept through the event")).c_str(),
           b.seen.lock_falls - lf0, lock_falls);
    ck.dec((tag + "no disrupt_p pulse").c_str(), b.seen.disrupts - d0, 0);
    for (int k = 0; k < static_cast<int>(4.2 * 8000); ++k) {
        if (two) b.slot2(a, c); else b.slot(a, 0);
    }
    named(ck, tag + "rate_valid returns 2048 intervals later", b.rate_valid());
}

void case_restarts(MeterBench& b, Checker& ck) {
    restart_event(b, ck, "tu edge", [](Talker& a, Talker&) { a.tu = true; }, false, 0);
    named(ck, "[M7 tu edge] counted as a data restart", b.seen.restarts == 1);
    restart_event(b, ck, "listener change",
                  [&b](Talker&, Talker&) { b.dut->follow_idx_i = 1; }, true, 1);
    restart_event(b, ck, "entry", [&b](Talker&, Talker&) {
        b.dut->en_i = 0;
        b.idle(kSlotCyc);
        b.dut->en_i = 1;
    }, false, 1);
    restart_event(b, ck, "bind edge", [&b](Talker&, Talker&) {
        b.dut->bind_rise_i = 1;
        b.tick();
        b.dut->bind_rise_i = 0;
    }, false, 0);
    // the 32-bit timestamp wrap is not a discontinuity
    follow(b, 100.0);
    Talker t;
    t.ppm = 100.0;
    t.t0 = (1LL << 32) - 2'000'000'000;
    const auto start = static_cast<int64_t>(b.cyc);
    b.run_seconds(t, 8.0);
    named(ck, "[M7 ts wrap] no restart across the 32-bit timestamp wrap", b.seen.restarts == 0);
    named(ck, "[M7 ts wrap] rate_valid from 4.1 s on and held", valid_by_42_and_held(b, start));
}

// ------------------------------------------------------------------------
//  M8: periodic single-PDU loss at the design point, rule (b). Mutant:
//  restart on any loss (round 3's rule).
// ------------------------------------------------------------------------
void case_loss_periodic(MeterBench& b, Checker& ck) {
    struct Leg {
        const char* name;
        std::function<int64_t(uint64_t)> err;
        uint64_t every;
    };
    const std::array<Leg, 4> legs = {{
        {"indep 1 s", independent(kJ, kSeed + 4), 8000},
        {"indep 0.3 s", independent(kJ, kSeed + 5), 2400},
        {"rsign 1 s", random_sign_group(kJ, kSeed + 6), 8000},
        {"rsign 0.3 s", random_sign_group(kJ, kSeed + 7), 2400},
    }};
    for (const Leg& leg : legs) {
        follow(b, kDesignPpm);
        Talker t;
        t.ppm = kDesignPpm;
        t.err = leg.err;
        const uint64_t every = leg.every;
        t.lost = [every](uint64_t i) { return i % every == every / 2; };
        const auto start = static_cast<int64_t>(b.cyc);
        b.run_seconds(t, 120.0);
        const std::string tag = std::string("[M8 ") + leg.name + "] ";
        named(ck, tag + "no history restart", b.seen.restarts == 0);
        named(ck, tag + "rate_valid from 4.1 s on and never falls", valid_by_42_and_held(b, start));
        named(ck, tag + "every rate within 360 ns of the planted rate",
              b.seen.worst_rate_err <= 360 && b.seen.rate_updates > 200);
        std::printf("  info: M8 %s: worst %lld ns\n", leg.name,
                    static_cast<long long>(b.seen.worst_rate_err));
    }
}

// ------------------------------------------------------------------------
//  M9: a lost PDU in a snapshot group (the group at 3 x 512 ms) is filled
//  by the midpoint. Mutants: the snapshot from the next pick less 2 ms; a
//  voided snapshot group restarting the history.
// ------------------------------------------------------------------------
void case_loss_snapshot(MeterBench& b, Checker& ck) {
    follow(b, 100.0);
    Talker clean;
    clean.ppm = 100.0;
    b.run_seconds(clean, 7.0);
    const std::vector<int32_t> want = b.seen.rates;
    follow(b, 100.0);
    Talker t;
    t.ppm = 100.0;
    const uint64_t victim = 3ULL * 256 * kGroupPdus + 5;
    t.lost = [victim](uint64_t i) { return i == victim; };
    b.run_seconds(t, 7.0);
    named(ck, "[M9] no history restart", b.seen.restarts == 0);
    bool same = want.size() == b.seen.rates.size() && want.size() >= 4;
    for (size_t k = 0; same && k < want.size(); ++k) {
        same = std::llabs(static_cast<int64_t>(want[k]) - b.seen.rates[k]) <= 1;
    }
    named(ck, "[M9] every rate equals the no-loss run within 1 LSB", same);
}

// ------------------------------------------------------------------------
//  M10: the loss rule's bound. Mutant: a gap of more than one voided group
//  accepted.
// ------------------------------------------------------------------------
void case_bound(MeterBench& b, Checker& ck) {
    struct Pat {
        const char* name;
        std::function<bool(uint64_t)> lost;
        double seconds;
        uint64_t restarts;
    };
    const uint64_t g = 40ULL * kGroupPdus;
    const std::array<Pat, 5> pats = {{
        {"two losses in adjacent groups", [g](uint64_t i) { return i == g + 7 || i == g + 16 + 3; },
         0.6, 1},
        {"a run of 17", [g](uint64_t i) { return i >= g + 3 && i < g + 20; }, 0.6, 1},
        {"a run of 2 across a group boundary",
         [g](uint64_t i) { return i == g + 15 || i == g + 16; }, 0.6, 1},
        {"a run of 2 inside a group", [g](uint64_t i) { return i == g + 5 || i == g + 6; }, 0.6, 0},
        {"single losses 32 PDUs apart for 10 s", [](uint64_t i) { return i % 32 == 7; }, 10.0, 0},
    }};
    for (const Pat& p : pats) {
        follow(b, 100.0);
        Talker t;
        t.ppm = 100.0;
        t.lost = p.lost;
        b.run_seconds(t, p.seconds);
        const std::string label = std::string("[M10 ") + p.name + "] restarts " +
                                  (p.restarts ? "once" : "nothing");
        ck.dec(label.c_str(), b.seen.restarts, p.restarts);
    }
}

// ------------------------------------------------------------------------
//  M11: the 5,120 ns gap bound graded at both edges, the step at the lost
//  PDU 0 of group 50. Mutants: the gap bound at 4,096 ns; the bound scaled
//  with k (8,192 ns).
// ------------------------------------------------------------------------
void case_gap_value(MeterBench& b, Checker& ck) {
    const uint64_t at = 50ULL * kGroupPdus;
    follow(b, kDesignPpm);
    Talker a;
    a.ppm = kDesignPpm;
    a.step_at = at;
    a.step_ns = 3'900;
    a.lost = [at](uint64_t i) { return i == at; };
    b.run_seconds(a, 0.5);
    ck.dec("[M11 a] +3,900 ns at +300 ppm, 5,100 ns from 4 ms: no restart", b.seen.restarts, 0);
    follow(b, -kDesignPpm);
    Talker c;
    c.ppm = -kDesignPpm;
    c.err = [at](uint64_t i) { return i < at ? kJ : -kJ; };
    c.step_at = at;
    c.step_ns = kHalfSampleNs;
    c.lost = [at](uint64_t i) { return i == at; };
    b.run_seconds(c, 0.5);
    ck.dec("[M11 b] half sample at -300 ppm against +/-J, 6,365 ns off: one restart",
           b.seen.restarts, 1);
}

// ------------------------------------------------------------------------
//  M12: a step inside a loss-voided group, at the design point. Mutant: no
//  check across a gap.
// ------------------------------------------------------------------------
void case_step_in_gap(MeterBench& b, Checker& ck) {
    const uint64_t g = 20ULL * kGroupPdus;
    uint64_t salt = 0;
    for (const int64_t step : {kOneSampleNs, -kOneSampleNs, kHalfSampleNs, -kHalfSampleNs}) {
        for (int lose15 = 0; lose15 <= 1; ++lose15) {
            for (int pos = lose15 ? 0 : 1; pos <= (lose15 ? 14 : 15); ++pos) {
                follow(b, kDesignPpm);
                Talker t;
                t.ppm = kDesignPpm;
                t.err = independent(kJ, kSeed + 100 + salt++);
                const uint64_t lost_pdu = g + (lose15 ? 15 : 0);
                t.lost = [lost_pdu](uint64_t i) { return i == lost_pdu; };
                t.step_at = g + static_cast<uint64_t>(pos);
                t.step_ns = step;
                const int64_t at = run_marking(b, t, 0.1, t.step_at);
                std::array<char, 128> label{};
                std::snprintf(label.data(), label.size(),
                              "[M12 %s, step %+lld @%d] restarts the history once",
                              lose15 ? "PDU 15 lost" : "PDU 0 lost",
                              static_cast<long long>(step), pos);
                ck.dec(label.data(), b.seen.restarts, 1);
                //! rule 1, the deviation check up to the gap: a group that
                //! keeps its PDU 0 and loses its PDU 15 is checked at each
                //! PDU as it arrives, so the restart comes at the step's PDU,
                //! before the gap. A group that loses its PDU 0 has no
                //! reference, and a step at PDU 0 moves it: those 64 cases
                //! are the check across the gap's, graded by the count alone
                if (!lose15 || pos == 0) continue;
                std::snprintf(label.data(), label.size(),
                              "[M12 PDU 15 lost, step %+lld @%d] the deviation check restarts "
                              "it at the step's PDU, before the gap",
                              static_cast<long long>(step), pos);
                named(ck, label.data(), restart_at_pdu(b, at));
            }
        }
    }
}

// ------------------------------------------------------------------------
//  M13: what is not measured. Mutant: the listener compare ignored.
// ------------------------------------------------------------------------
void case_selection(MeterBench& b, Checker& ck) {
    follow(b, 0.0);
    Talker other;
    for (int k = 0; k < 400; ++k) b.slot(other, 1);
    named(ck, "[M13 another listener] not measured", !b.locked());
    follow(b, 0.0);
    Talker crf;
    crf.subtype = 4;
    b.run_seconds(crf, 0.05);
    named(ck, "[M13 wrong subtype] not measured", !b.locked());
    follow(b, 0.0);
    Talker untimed;
    untimed.tv = false;
    b.run_seconds(untimed, 0.05);
    named(ck, "[M13 tv clear] not measured", !b.locked());
    follow(b, 0.0);
    b.dut->stopped_i = 1;
    Talker stopped;
    b.run_seconds(stopped, 0.05);
    named(ck, "[M13 STOPPED input] not measured", !b.locked());
    b.dut->stopped_i = 0;
}

// ------------------------------------------------------------------------
//  M14: the meter's two pulses, counted at its ports. Mutants: no re-seed
//  at an era start; an era-start lock clear reported on disrupt_p;
//  disrupt_p tied low; the enable tied high.
// ------------------------------------------------------------------------
struct PulsePhase {
    MeterBench& b;
    Checker& ck;
    Talker& a;
    Talker& c;

    //! Run `seconds` of both streams (A optionally silent) and require the
    //! phase's own pulse counts.
    void run(const char* name, double seconds, uint64_t disrupts, uint64_t toggles,
             bool deliver_a = true, double toggle_a_every_s = 0.0) {
        const uint64_t d0 = b.seen.disrupts;
        const uint64_t m0 = b.seen.mr_toggles;
        const auto slots = static_cast<uint64_t>(seconds * 8000.0);
        const auto every = static_cast<uint64_t>(toggle_a_every_s * 8000.0);
        for (uint64_t k = 0; k < slots; ++k) {
            if (every != 0 && k % every == every - 1) a.mr = !a.mr;
            b.slot2(a, c, deliver_a, true);
        }
        const std::string tag = std::string("[M14 ") + name + "] ";
        ck.dec((tag + "disrupt_p pulses").c_str(), b.seen.disrupts - d0, disrupts);
        ck.dec((tag + "mr_toggle_p pulses").c_str(), b.seen.mr_toggles - m0, toggles);
    }
};

void case_pulses(MeterBench& b, Checker& ck) {
    b.reset();
    Talker a;
    a.mr = true;
    Talker c;
    c.t0 = 5'000'000'000;
    PulsePhase ph{b, ck, a, c};
    ph.run("INTERNAL dwell", 0.05, 0, 0);
    b.dut->en_i = 1;
    b.dut->follow_idx_i = 0;
    ph.run("entry onto a talker at mr 1", 0.05, 0, 0);
    named(ck, "[M14 entry] locked on listener 0", b.locked());
    b.dut->follow_idx_i = 1;
    ph.run("listener change to the opposite mr level", 0.05, 0, 0);
    named(ck, "[M14 listener change] locked on listener 1", b.locked());
    b.dut->en_i = 0;
    ph.run("exit", 0.05, 0, 0);
    b.dut->follow_idx_i = 0;
    ph.run("enable low, talker 0 toggling its mr", 0.1, 0, 0, true, 0.005);
    b.dut->en_i = 1;
    ph.run("re-entry", 0.05, 0, 0);
    a.mr = !a.mr;
    ph.run("a toggle of the followed talker's mr", 0.05, 0, 1);
    ph.run("100 ms of silence", 0.15, 1, 0, false);
    a.mr = !a.mr;
    ph.run("the stream resumes", 0.05, 0, 0);
    ph.run("an unbind", 0.15, 1, 0, false);
    a.mr = !a.mr;
    b.dut->bind_rise_i = 1;
    b.tick();
    b.dut->bind_rise_i = 0;
    ph.run("the rebind", 0.05, 0, 0);
    named(ck, "[M14 rebind] locked again", b.locked());
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vmeter_wrap> model;
    Checker check{"aaf_clock_meter"};
    MeterBench bench{check};
    bench.dut = model.get();
    struct Case {
        const char* name;
        void (*fn)(MeterBench&, Checker&);
    };
    const std::array<Case, 14> cases = {{
        {"rates", case_rates},           {"shapes", case_shapes},
        {"beyond", case_beyond},         {"format", case_format},
        {"wrap", case_wrap},             {"lock", case_lock},
        {"restarts", case_restarts},     {"loss_periodic", case_loss_periodic},
        {"loss_snapshot", case_loss_snapshot}, {"bound", case_bound},
        {"gap_value", case_gap_value},   {"step_in_gap", case_step_in_gap},
        {"selection", case_selection},   {"pulses", case_pulses},
    }};
    std::set<std::string> want;
    for (int k = 1; k < argc; ++k) {
        if (argv[k][0] != '+') want.insert(argv[k]);
    }
    for (const Case& c : cases) {
        if (!want.empty() && want.count(c.name) == 0) continue;
        std::printf("---- %s ----\n", c.name);
        c.fn(bench, check);
    }
    return check.report();
}

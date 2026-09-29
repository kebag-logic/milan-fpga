// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// coherence_bench.hpp - what both capture_coherence legs share (#617): the
// oscillator that makes the axis and TDM clocks, the SoC transmitter on the
// TDM pins, and the bench that grades every AAF sample column the talker
// emits. sim_main.cpp drives them against the junction wrapper and
// sim_dp.cpp against the whole milan_datapath; one statement of each keeps
// the two legs' oracles one oracle (Rule 3).
//
// THE PATTERN. The #451 page's: slot s of TDM frame n carries the 24-bit
// sample ((s + 1) << 16) | (n & 0xFFFF), in bits 31:8 of a 32-bit slot with
// bits 7:0 zero. The talker's AAF word for channel c is that sample in bits
// 31:8 of an S32BE word (IEEE 1722-2016 7.3.5), so a column is valid when
// channel c carries tag c + 1 and a zero pad byte, and COHERENT when all its
// channels carry one frame ordinal.

#ifndef MILAN_TB_CAPTURE_COHERENCE_BENCH_HPP
#define MILAN_TB_CAPTURE_COHERENCE_BENCH_HPP

#include "../../common/verilator_harness.hpp"

#include <algorithm>
#include <array>
#include <climits>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string>
#include <utility>
#include <vector>

namespace coherence {

//! the elaborated shape, stated once in the Makefile (-G and -D together)
constexpr int kChans = WIRE_CHANS_TB;
constexpr int kPairs = kChans / 2;
constexpr int kTdmSlots = TDM_SLOTS_TB;
constexpr long kAxisHz = CLK_HZ_TB;

//! one simulation step is 5 ns: both edges of the 100 MHz oscillator
constexpr std::uint64_t kStepHz = 200'000'000;
constexpr long kStepsPerAxisHalf = static_cast<long>(kStepHz) / (2 * kAxisHz);
//! the TDM word and frame, in bit clocks
constexpr int kWordBits = 32;
constexpr int kFrameBits = kTdmSlots * kWordBits;
//! one media tick in axis cycles
constexpr double kTickCycles = static_cast<double>(kAxisHz) / 48000.0;
//! the AAF PDU: Ethernet + C-TAG + AAF header, then 6 events x C x 4 octets
constexpr int kEvents = 6;
constexpr int kPayloadOffset = 42;
constexpr int kFrameBytes = kPayloadOffset + kEvents * kChans * 4;
//! columns closer than this belong to one slip cluster
constexpr long kClusterGap = 64;
//! CRF: the columns in which an engagement landing on the walk's crossing may
//! repeat and skip a frame, one of each, net zero. The aligner's split puts
//! such an engagement's lock target a keep-off to one side, and its
//! proportional term pulls the close there at u = keep-off << KP_LOG2_P, in
//! 1/16 ppm: 64 ppm at milan_datapath's 256 cycles (the wrapper's
//! engage_u_o). A relative rate |r| against the pull leaves (64 - |r|) ppm,
//! (64 - |r|) x 1e-6 x 1041.7 cycles a frame, and the close stops dithering
//! across the crossing once that has carried it a cycle, its jitter, clear.
//! At the Milan v1.2 7.4 +/-50 ppm bound that is 0.0146 cycles a frame, 68
//! frames, and the talker's first column comes about four frames after the
//! engagement: 64 columns. Measured at every sub-cycle phase of the crossing
//! (CRF-fine-50, -50 ppm): the last slip at column 57. Below the bound the
//! departure is faster and the bound's window holds (last slips at columns
//! 19, 23 and 31 at -10.64, -25 and -40 ppm); beyond it, engage_columns().
constexpr long kEngageColumns = 64;
//! Milan v1.2 7.4: a media clock source within +/-50 ppm of nominal
constexpr double kMilanPpm = 50.0;
//! no column window: at or past the pull an engagement is carried across the
//! crossing and back while its lock settles (above nominal), or dwells on it
//! ever longer with the rate (below), so only the lock is graded
constexpr long kUnbounded = LONG_MAX;

//! The engagement window at relative rate `ppm` against a pull of `pull_ppm`
//! (the aligner's u at one keep-off of error): kEngageColumns within the
//! Milan bound; beyond it stretched as the departure (pull - |r|) slows, since
//! the time to clear a cycle is its inverse (224 columns at 60 ppm, where the
//! last slip measures column 181); unbounded at or past the pull. Above
//! nominal that is the on-crossing engagement limit (measured: net zero by
//! column 8 at +66 ppm, carried across from about +67); below nominal there
//! is no sharp limit, the single net-zero pair only coming later with the
//! rate (column 426 at -63 ppm, 1,323 at -66, 2,918 at -70; review probes
//! R394-3 and R395-3), and an unbounded window grades only the lock.
inline long engage_columns(double ppm, double pull_ppm) {
    const double rate = std::fabs(ppm);
    if (rate <= kMilanPpm) return kEngageColumns;
    if (rate >= pull_ppm) return kUnbounded;
    return static_cast<long>(
        std::ceil(static_cast<double>(kEngageColumns) * (pull_ppm - kMilanPpm) / (pull_ppm - rate)));
}

//! Where a CRF run's lock tail starts: its second half, and never inside its
//! engagement window - a slip the window admits is acquisition, not the lock.
inline long tail_start(long frames, long window) {
    return window == kUnbounded ? frames / 2 : std::max(frames / 2, window);
}

//! A TDM clock as a fractional-N divider of the 200 MHz step rate: the clock
//! toggles on every step at which `num` accumulated into `den` wraps.
struct ClockPlan {
    std::string name;
    std::uint64_t num = 0;
    std::uint64_t den = 1;
    double ppm = 0.0;  //! the TDM frame's offset against the 48 kHz grid
};

//! the shipping divider plan (sw/litex/milan_soc.py PLAN A): 100 MHz x
//! 391/1591, toggling at 200 MHz x 391/1591, is 24,575,738.53 Hz
inline ClockPlan true_plan() {
    const double hz = 100e6 * 391.0 / 1591.0;
    return {"true 391/1591 plan", 391, 1591, (hz / 512.0 / 48000.0 - 1.0) * 1e6};
}

//! 24.576 MHz x (1 + ppm/1e6) exactly: 0.24576 of the step rate is
//! 245,760,000 / 1e9, and 245.76 per ppm is an integer for any multiple of 25
inline ClockPlan ppm_plan(int ppm) {
    const auto num = static_cast<std::uint64_t>(245'760'000 + (24'576 * ppm) / 100);
    char label[48];
    std::snprintf(label, sizeof label, "%+d ppm plan", ppm);
    return {label, num, 1'000'000'000ULL, static_cast<double>(ppm)};
}

//! Which clock edges one oscillator step produced.
struct Edges {
    bool axis = false;
    bool tdm = false;
};

//! Sub-step phases of the TDM clock: its fractional-N accumulator can start
//! at k / kSubPhases of the plan's denominator, which moves every TDM edge
//! by up to one oscillator step - finer than a held step, a quarter cycle.
constexpr long kSubPhases = 64;

//! The oscillator: the axis clock at a fixed division, the TDM clock as the
//! plan's fractional-N divider, held for a number of steps after a restart
//! and started at a sub-step phase, so a scenario can place the TDM frame
//! against the packet grid finer than an axis cycle.
class Oscillator {
 public:
    void restart(const ClockPlan& plan, long hold_steps, long sub_phase = 0) {
        plan_ = plan;
        acc_ = 0;
        hold_ = hold_steps;
        if (sub_phase > 0) acc_ = plan.den * static_cast<std::uint64_t>(sub_phase) / kSubPhases;
    }

    Edges step() {
        Edges e;
        ++step_;
        e.axis = (step_ % kStepsPerAxisHalf) == 0;
        if (hold_ > 0) {
            --hold_;
        } else {
            acc_ += plan_.num;
            if (acc_ >= plan_.den) {
                acc_ -= plan_.den;
                e.tdm = true;
            }
        }
        if (e.axis) axis_ ^= 1;
        if (e.tdm) tdm_ ^= 1;
        return e;
    }

    int axis() const { return axis_; }
    int tdm() const { return tdm_; }
    const ClockPlan& plan() const { return plan_; }

 private:
    ClockPlan plan_{};
    std::uint64_t acc_ = 0;
    long hold_ = 0;
    long step_ = 0;
    int axis_ = 0;
    int tdm_ = 0;
};

//! the SoC's 32-bit word for slot s of frame n: the 24-bit sample in 31:8
inline std::uint32_t pattern_word(int slot, std::uint32_t frame) {
    const std::uint32_t smp = (static_cast<std::uint32_t>(slot + 1) << 16) | (frame & 0xFFFFu);
    return smp << 8;
}

//! The SoC transmitter, a McASP in dsp_a as the bus slave: fsync high across
//! a bclk rise marks the frame, the next fall launches slot 0's MSB (a
//! one-bit data delay), every fall launches the next bit, and the line idles
//! high outside a frame. Call it after every TDM-clock rising edge; it
//! returns the data pin's level from then on.
class SocTransmitter {
 public:
    void restart(std::uint32_t first_frame, int bclk_now) {
        next_ = first_frame;
        bitpos_ = -1;
        bclk_prev_ = bclk_now;
        data_ = 1;
    }

    int on_tdm_edge(int bclk, int fsync) {
        if (bclk && !bclk_prev_ && fsync) {
            frame_ = next_++;
            bitpos_ = 0;
        } else if (!bclk && bclk_prev_) {
            if (bitpos_ >= 0 && bitpos_ < kFrameBits) {
                const std::uint32_t word = pattern_word(bitpos_ / kWordBits, frame_);
                data_ = static_cast<int>((word >> (kWordBits - 1 - bitpos_ % kWordBits)) & 1u);
                ++bitpos_;
            } else {
                data_ = 1;
            }
        }
        bclk_prev_ = bclk;
        return data_;
    }

    //! frames launched so far
    std::uint32_t frames_sent() const { return next_; }

 private:
    std::uint32_t next_ = 0;
    std::uint32_t frame_ = 0;
    int bitpos_ = -1;
    int bclk_prev_ = 0;
    int data_ = 1;
};

// ---- PLACED CRF ENGAGEMENTS ------------------------------------------------ //
// A CRF scenario engages the aligner on the first frame close it sees.
// Holding the TDM clock D oscillator steps moves every TDM event, that close
// included, D steps later against the packet grid, which the hold does not
// touch. So a leg measures once, per plan, where that close lands with the
// clock unheld (its CALIBRATION), and delay_for() then places an engagement
// any chosen number of cycles from the walk's crossing (0 = the close on the
// tick cycle, positive = after it).

//! oscillator steps per axis cycle: a held TDM clock moves the frame by one
//! cycle every this many steps
constexpr long kStepsPerCycle = static_cast<long>(kStepHz) / kAxisHz;
//! no placed engagement: the scenario keeps its held-clock offset
constexpr long kUnplaced = LONG_MIN;
//! a placed engagement lands 0 to 2 cycles before its linear placement: the
//! front end's clock crossing and the tick grid's whole-cycle steps
//! (measured over every placed scenario of both legs)
constexpr long kPlaceTolerance = 2;

//! A placed sweep: one CRF scenario per offset from `lo` to `hi` cycles from
//! the crossing, `step` apart, each `frames` columns long - and, for a
//! sub-cycle sweep, per offset `holds` placements a quarter cycle (one held
//! step) apart, each at `phases` sub-step phases.
struct Sweep {
    std::string tag;
    ClockPlan plan;
    long lo = 0;
    long hi = 0;
    long step = 1;
    long frames = 0;
    long holds = 1;
    long phases = 1;
};

//! a cycle offset wrapped into one frame about zero, (-P/2, P/2]
inline long wrap_offset(double cycles) {
    double w = std::fmod(cycles, kTickCycles);
    if (w > kTickCycles / 2) w -= kTickCycles;
    if (w <= -kTickCycles / 2) w += kTickCycles;
    return std::lround(w);
}

//! The held-clock steps that land the engagement close `offset` cycles from
//! the crossing, given where it lands with the clock unheld.
inline long delay_for(long unheld, long offset) {
    const double frame_steps = kTickCycles * static_cast<double>(kStepsPerCycle);
    double d = std::fmod(static_cast<double>(offset - unheld) * static_cast<double>(kStepsPerCycle), frame_steps);
    if (d < 0) d += frame_steps;
    return std::lround(d);
}

//! A sweep's engagements, sorted, must span its window with no gap wider
//! than its step plus the placement tolerance: otherwise a band narrower
//! than the gap could sit between two of them unseen.
inline void grade_window(milan::tb::Checker& check, const Sweep& sw, std::vector<long> landed) {
    std::sort(landed.begin(), landed.end());
    long gap = landed.empty() ? LONG_MAX : 0;
    for (size_t i = 1; i < landed.size(); i++) gap = std::max(gap, landed[i] - landed[i - 1]);
    const long slack = sw.step + kPlaceTolerance;
    const bool spans = !landed.empty() && landed.front() <= sw.lo + slack && landed.back() >= sw.hi - slack;
    std::printf("  [i]  %s: %zu engagements landed from %+ld to %+ld, widest gap %ld cycles\n", sw.tag.c_str(),
                landed.size(), landed.empty() ? 0 : landed.front(), landed.empty() ? 0 : landed.back(), gap);
    check.that(("[" + sw.tag + "] [V] the engagements covered the window, no gap wider than its step").c_str(),
               spans && gap <= slack);
}

//! Pair offsets of one column against pair 0: the #451 state key.
using StateKey = std::array<int, kPairs - 1>;

//! What the column bench measured.
struct ColumnTally {
    long pdus = 0;              //! AAF PDUs decoded
    long bad_pdus = 0;          //! PDUs not the 8-channel AAF shape
    long columns = 0;           //! columns after the first valid one
    long invalid = 0;           //! columns with a word not its own channel's
    long pair_split = 0;        //! L and R of one pair from two frames
    long torn = 0;              //! columns mixing two TDM frames
    long dups = 0;              //! column repeats
    long skips = 0;             //! column skips
    long bad_steps = 0;         //! any other continuity step
    long clusters = 0;          //! slip clusters
    long bad_clusters = 0;      //! clusters not netting one slip
    long tail_slips = 0;        //! slips while the caller's tail flag is set
    long last_slip_col = -1;    //! the column of the last slip
    std::map<StateKey, long> states;
};

//! The column bench: AXIS beats of the talker's frames in, every AAF sample
//! column graded. Frames that are not AAF (subtype 0x02 behind the 0x22F0
//! ethertype and a C-TAG) are not the talker's and are ignored.
class ColumnBench {
 public:
    void restart() {
        t_ = ColumnTally{};
        pdu_.clear();
        live_ = false;
        tail_ = false;
        prev_frame_ = 0;
        last_slip_col_ = -1;
        cluster_net_ = 0;
        in_cluster_ = false;
    }

    //! one accepted AXIS beat, byte lane j = frame byte 8k + j
    void beat(std::uint64_t tdata, unsigned tkeep, bool tlast) {
        for (int b = 0; b < 8; b++) {
            if ((tkeep >> b) & 1u) pdu_.push_back(static_cast<std::uint8_t>((tdata >> (8 * b)) & 0xFFu));
        }
        if (!tlast) return;
        decode_pdu();
        pdu_.clear();
    }

    //! slips counted while the tail flag is set are the CRF lock's
    void set_tail(bool tail) { tail_ = tail; }
    void finish() {
        if (in_cluster_) end_cluster();
    }
    bool live() const { return live_; }
    const ColumnTally& tally() const { return t_; }

    //! The column checks, prefixed with the scenario's name. With `drift`
    //! (INTERNAL) `ppm` is the TDM frame's offset against the grid and every
    //! slip cluster must net one frame in its direction. Without it (CRF) the
    //! grids are held together and there is no drift to net: a slip may come
    //! only while the engagement acquires - on the walk's crossing, inside
    //! its `window` columns (engage_columns()), or, at or past the pull,
    //! anywhere before the lock's tail - and it nets zero: the
    //! aligner's loop returns the close to the side it engaged on.
    void grade(milan::tb::Checker& check, const std::string& n, long min_columns, double ppm, bool drift,
               long window) const {
        check.dec((n + "[A] PDUs not the 8-channel AAF shape").c_str(), static_cast<std::uint64_t>(t_.bad_pdus), 0);
        check.that((n + "[V] every requested column was decoded").c_str(), t_.columns >= min_columns);
        check.dec((n + "[A] words not carrying their own channel tag").c_str(),
                  static_cast<std::uint64_t>(t_.invalid), 0);
        check.dec((n + "[A] pairs whose L and R come from two frames").c_str(),
                  static_cast<std::uint64_t>(t_.pair_split), 0);
        check.dec((n + "[A] AAF columns mixing two TDM frames").c_str(), static_cast<std::uint64_t>(t_.torn), 0);
        check.dec((n + "[C] continuity steps other than +1, one repeat or one skip").c_str(),
                  static_cast<std::uint64_t>(t_.bad_steps), 0);
        if (!drift) {
            check.that((n + "[C] CRF slips net zero").c_str(), t_.skips == t_.dups);
            check.that((n + "[C] CRF slips only inside the engagement's first columns").c_str(),
                       t_.last_slip_col < std::min(window, tail_start(min_columns, window)));
            return;
        }
        check.dec((n + "[C] slip clusters not netting exactly one frame").c_str(),
                  static_cast<std::uint64_t>(t_.bad_clusters), 0);
        const long sign = ppm < 0 ? -1 : 1;
        check.that((n + "[C] every slip cluster nets one frame in the drift's direction").c_str(),
                   t_.skips - t_.dups == sign * t_.clusters);
    }

    //! The #451 page's table: the frame offset of pairs 1, 2, 3 against pair 0.
    void print_table() const {
        const double cols = t_.columns ? static_cast<double>(t_.columns) : 1.0;
        std::printf("  [i]  %ld columns in %ld PDUs, %ld torn (%.1f%%), %ld repeats, %ld skips, %ld slip clusters\n",
                    t_.columns, t_.pdus, t_.torn, 100.0 * static_cast<double>(t_.torn) / cols, t_.dups,
                    t_.skips, t_.clusters);
        std::vector<std::pair<long, StateKey>> rows;
        for (const auto& [key, count] : t_.states) rows.emplace_back(count, key);
        std::sort(rows.begin(), rows.end(), [](const auto& a, const auto& b) { return a.first > b.first; });
        for (const auto& [count, key] : rows) {
            const bool torn = std::any_of(key.begin(), key.end(), [](int k) { return k != 0; });
            std::printf("  [i]    pairs 1..3 vs pair 0: %+d %+d %+d  %9ld columns  %5.1f%%  %s\n", key[0],
                        key[1], key[2], count, 100.0 * static_cast<double>(count) / cols,
                        torn ? "torn" : "coherent");
        }
    }

 private:
    ColumnTally t_{};
    std::vector<std::uint8_t> pdu_;
    bool live_ = false;
    bool tail_ = false;
    long prev_frame_ = 0;
    long last_slip_col_ = -1;
    int cluster_net_ = 0;
    bool in_cluster_ = false;

    //! the unwrapped frame of a 16-bit ordinal, nearest the previous column's
    long unwrap(std::uint32_t ord16) const {
        if (!live_) return static_cast<long>(ord16);
        const long delta = static_cast<long>((ord16 - static_cast<std::uint32_t>(prev_frame_)) & 0xFFFFu);
        return prev_frame_ + (delta >= 0x8000 ? delta - 0x10000 : delta);
    }

    void decode_pdu() {
        const bool aaf = pdu_.size() >= 19 && pdu_[16] == 0x22 && pdu_[17] == 0xF0 && pdu_[18] == 0x02;
        if (!aaf) return;
        t_.pdus++;
        if (static_cast<int>(pdu_.size()) != kFrameBytes) {
            t_.bad_pdus++;
            return;
        }
        for (int e = 0; e < kEvents; e++) {
            decode_column(&pdu_[static_cast<size_t>(kPayloadOffset + e * kChans * 4)]);
        }
    }

    //! One AAF sample column: eight S32BE words, the 24-bit sample in 31:8.
    void decode_column(const std::uint8_t* col) {
        std::array<long, kChans> frame{};
        bool valid = true;
        for (int c = 0; c < kChans; c++) {
            const std::uint8_t* w = col + 4 * c;
            const std::uint32_t ord = (static_cast<std::uint32_t>(w[1]) << 8) | w[2];
            valid = valid && w[3] == 0 && w[0] == static_cast<std::uint8_t>(c + 1);
            frame[static_cast<size_t>(c)] = unwrap(ord);
        }
        if (!live_) {
            if (!valid) return;
            live_ = true;
            prev_frame_ = frame[0] - 1;
        }
        const long col_idx = t_.columns++;
        if (!valid) {
            t_.invalid++;
            return;
        }
        StateKey key{};
        for (int p = 0; p < kPairs; p++) {
            if (frame[static_cast<size_t>(2 * p)] != frame[static_cast<size_t>(2 * p + 1)]) t_.pair_split++;
            if (p > 0) key[static_cast<size_t>(p - 1)] = static_cast<int>(frame[static_cast<size_t>(2 * p)] - frame[0]);
        }
        t_.states[key]++;
        if (std::any_of(key.begin(), key.end(), [](int k) { return k != 0; })) t_.torn++;
        slip(static_cast<int>(frame[0] - prev_frame_), col_idx);
        prev_frame_ = frame[0];
    }

    //! Continuity of pair 0's frame between consecutive columns.
    void slip(int step, long col) {
        if (in_cluster_ && col - last_slip_col_ > kClusterGap) end_cluster();
        if (step == 1) return;
        if (step == 0) {
            t_.dups++;
        } else if (step == 2) {
            t_.skips++;
        } else {
            t_.bad_steps++;
            return;
        }
        if (tail_) t_.tail_slips++;
        t_.last_slip_col = col;
        in_cluster_ = true;
        cluster_net_ += step - 1;
        last_slip_col_ = col;
    }

    //! A cluster of repeats and skips must net exactly one slip.
    void end_cluster() {
        t_.clusters++;
        if (cluster_net_ != 1 && cluster_net_ != -1) t_.bad_clusters++;
        cluster_net_ = 0;
        in_cluster_ = false;
    }
};

}  // namespace coherence

#endif  // MILAN_TB_CAPTURE_COHERENCE_BENCH_HPP

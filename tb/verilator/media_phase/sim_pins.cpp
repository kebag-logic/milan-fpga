// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Two media interfaces on one clock domain, graded at their pins (#632): the
// synthetic shape of pin_wrap.sv (TDM8 owner A, TDM4 B, real
// KL_tdm_capture_master instances on one 24.576 MHz audio clock, a 50 MHz
// datapath clock, the PHC the true time).
//
// A slot-MSB pin decoder per interface reads only that interface's bclk and
// fsync pins: the rise that reads fsync high is the frame's sync instant, and
// slot k's MSB is sampled (k x 32 + d) rises later, d the interface's data
// delay. The harness derives each slot's offset itself, independently of the
// RTL's KL_media_if_latency_pkg, and requires:
//   [pins A|B] every frame instant the interface stamps (A: the domain event,
//              B: its own back-dated marker) is the frame's slot-k MSB pin
//              instant less slot k's offset, for every slot, inside IEEE
//              1722-2016 10.8's +/-5 % of Ps and inside the derivation (two
//              datapath cycles);
//   [pins]     every CRF timing point the domain emits (its timestamp less the
//              2 ms Eq. 14 offset) is a frame instant of BOTH interfaces' pins
//              to +/-5 % of Ps: every interface's pin instants fall on the same
//              CRF timing points;
//   [pins]     the two interfaces' constants differ by more than the
//              derivation band, so swapping them cannot pass.
// phase_mutants.py drops B's constant and swaps the two, each a named failure.

#include "Vpin_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <deque>

namespace {

constexpr double kPsNs = 1e9 / 48000.0;
constexpr double kBandNs = 0.05 * kPsNs;
constexpr double kAxisHz = 50e6;
//! the audio clock 10.64 ppm under 24.576 MHz, the shipping MMCM plan, so the
//! two clocks never line up on a small period
constexpr double kAudHz = 24.576e6 * (1.0 - 10.64e-6);
constexpr double kHalfIFs = 0.5 * 1e15 / kAxisHz;
constexpr double kHalfAFs = 0.5 * 1e15 / kAudHz;
//! the stamp's derivation band: the read side rounds half a datapath cycle
//! and the PHC is the time of the datapath edge that latched it
constexpr double kDerivNs = 2.0 * 1e9 / kAxisHz;
constexpr double kMttNs = 2e6;

//! one interface's pin decoder and its graded stamps
struct Interface {
    const char* name;
    int slots;
    int data_delay;
    double bit_hz;
    int prev_bclk = 0;
    long rise = -1;                       //!< rises since the latest sync
    //! the latest frames' sync instants and slot-MSB instants, ns
    struct Frame {
        double sync = 0;
        std::array<double, 8> msb{};
        int got = 0;
    };
    std::deque<Frame> frames;
    long stamps = 0, slot_grades = 0;
    double max_err = 0;

    double slot_offset(int k) const { return (k * 32.0 + data_delay) * 1e9 / bit_hz; }

    void on_audio_edge(int bclk, int fsync, double t_ns) {
        const bool r = bclk && !prev_bclk;
        prev_bclk = bclk;
        if (!r) return;
        if (fsync) {
            frames.push_back(Frame{t_ns, {}, 0});
            if (frames.size() > 64) frames.pop_front();
            rise = 0;
        } else if (rise >= 0) {
            ++rise;
        }
        if (rise < 0 || frames.empty()) return;
        if (rise >= data_delay && (rise - data_delay) % 32 == 0) {
            const long k = (rise - data_delay) / 32;
            if (k < slots) {
                frames.back().msb[static_cast<size_t>(k)] = t_ns;
                frames.back().got++;
            }
        }
    }

    //! one stamped frame instant, against the frame it belongs to by the
    //! physics, not by its value: the marker of frame f arrives about one
    //! frame after f's sync, so f is the latest frame synced at least half a
    //! frame before the stamp arrived. Each slot's MSB less its offset.
    void grade(double stamp_ns, double arrival_ns) {
        const Frame* best = nullptr;
        for (const Frame& f : frames)
            if (f.sync <= arrival_ns - kPsNs / 2) best = &f;
        if (!best || best->got != slots) return;
        stamps++;
        for (int k = 0; k < slots; k++) {
            const double inst = best->msb[static_cast<size_t>(k)] - slot_offset(k);
            max_err = std::max(max_err, std::fabs(stamp_ns - inst));
            slot_grades++;
        }
    }

    //! is t on this interface's frame grid, mod Ps, within the band?
    double grid_dist(double t_ns) const {
        double best = 1e18;
        for (const Frame& f : frames) {
            double r = std::fmod(t_ns - f.sync, kPsNs);
            if (r < 0) r += kPsNs;
            if (r >= kPsNs / 2) r -= kPsNs;
            best = std::min(best, std::fabs(r));
        }
        return best;
    }
};

class PinHarness {
 public:
    PinHarness(Vpin_wrap* dut, milan::tb::Checker& check) : dut_(dut), check_(check) {}

    int run() {
        dut_->rst_n = 0;
        run_ns(2000);
        dut_->rst_n = 1;
        run_ns(30e6);                   // 30 ms: 1,440 frames on each interface
        report_interface(a_);
        report_interface(b_);
        char what[200];
        std::snprintf(what, sizeof what,
                      "[pins] every CRF timing point is a frame instant of BOTH interfaces' pins, inside "
                      "+/-5 %% of Ps (%ld points, max A %.1f ns, B %.1f ns)", crf_points_, crf_max_a_, crf_max_b_);
        check_.that(what, crf_points_ >= 12 && crf_max_a_ < kBandNs && crf_max_b_ < kBandNs);
        //! the two marker latencies, derived here from each interface's own
        //! geometry: one frame (less a bit at data delay 0), one audio cycle to
        //! the FIFO write, 4.5 datapath cycles of read side
        const double lat_a = kPsNs - (a_.data_delay ? 0.0 : 1e9 / a_.bit_hz) + 1e9 / 24.576e6 + 4.5e9 / kAxisHz;
        const double lat_b = kPsNs - (b_.data_delay ? 0.0 : 1e9 / b_.bit_hz) + 1e9 / 24.576e6 + 4.5e9 / kAxisHz;
        std::snprintf(what, sizeof what,
                      "[pins] the interfaces' constants differ (A %.1f ns, B %.1f ns): %.1f ns, beyond the "
                      "derivation band, so a swap cannot pass", lat_a, lat_b, lat_a - lat_b);
        check_.that(what, std::fabs(lat_a - lat_b) > 2 * kDerivNs);
        return check_.report();
    }

 private:
    void report_interface(const Interface& i) {
        char what[200];
        std::printf("  info: [pins %s] %ld stamps, %ld slot grades, max |stamp - (slot MSB - offset)| %.1f ns\n",
                    i.name, i.stamps, i.slot_grades, i.max_err);
        std::snprintf(what, sizeof what, "[pins %s] stamps graded at every slot (%ld)", i.name, i.slot_grades);
        check_.that(what, i.stamps >= 1400 && i.slot_grades == i.stamps * i.slots);
        std::snprintf(what, sizeof what,
                      "[pins %s] every stamped frame instant is each slot's MSB pin instant less its offset, "
                      "inside +/-5 %% of Ps (max %.1f ns)", i.name, i.max_err);
        check_.that(what, i.stamps > 0 && i.max_err < kBandNs);
        std::snprintf(what, sizeof what,
                      "[pins %s] ...and inside the derivation, +/-%.0f ns (max %.1f ns)", i.name, kDerivNs, i.max_err);
        check_.that(what, i.stamps > 0 && i.max_err <= kDerivNs);
    }

    void tick_one() {
        if (next_i_ <= next_a_) {
            t_fs_ = next_i_;
            next_i_ += kHalfIFs;
            dut_->clk_i ^= 1;
            if (dut_->clk_i) dut_->ptp_now_i = static_cast<uint64_t>(t_fs_ / 1e6);
            dut_->eval();
            if (dut_->clk_i) observe_clk();
        } else {
            t_fs_ = next_a_;
            next_a_ += kHalfAFs;
            dut_->clk_audio_i ^= 1;
            dut_->eval();
            const double t_ns = t_fs_ / 1e6;
            a_.on_audio_edge(dut_->a_bclk_o, dut_->a_fsync_o, t_ns);
            b_.on_audio_edge(dut_->b_bclk_o, dut_->b_fsync_o, t_ns);
        }
    }
    void run_ns(double ns) {
        const double te = t_fs_ + ns * 1e6;
        while (t_fs_ < te) tick_one();
    }

    void observe_clk() {
        // the stamps; the first few frames after reset are not yet complete
        if (dut_->a_ev_p_o) {
            const double s = static_cast<double>(dut_->a_ns_o);
            if (++a_events_ > 4) a_.grade(s, t_fs_ / 1e6);
        }
        if (dut_->b_ev_p_o) {
            const double s = static_cast<double>(dut_->b_ns_o);
            if (++b_events_ > 4) b_.grade(s, t_fs_ / 1e6);
        }
        // the CRF output: its timing points against both interfaces' pins
        if (dut_->crft_tvalid_o) {
            const uint64_t d = dut_->crft_tdata_o;
            for (int l = 0; l < 8; l++) crf_bytes_.push_back(static_cast<uint8_t>(d >> (8 * l)));
            if (dut_->crft_tlast_o) {
                if (crf_bytes_.size() >= 42) {
                    uint64_t ts = 0;
                    for (int k = 34; k < 42; k++) ts = (ts << 8) | crf_bytes_[static_cast<size_t>(k)];
                    const double inst = static_cast<double>(ts) - kMttNs;
                    crf_points_++;
                    crf_max_a_ = std::max(crf_max_a_, a_.grid_dist(inst));
                    crf_max_b_ = std::max(crf_max_b_, b_.grid_dist(inst));
                }
                crf_bytes_.clear();
            }
        }
    }

    Vpin_wrap* dut_;
    milan::tb::Checker& check_;
    double t_fs_ = 0, next_i_ = kHalfIFs, next_a_ = kHalfAFs;
    Interface a_{"A", 8, 1, 8 * 32 * 48000.0};
    Interface b_{"B", 4, 0, 4 * 32 * 48000.0};
    long a_events_ = 0, b_events_ = 0;
    std::deque<uint8_t> crf_bytes_;
    long crf_points_ = 0;
    double crf_max_a_ = 0, crf_max_b_ = 0;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vpin_wrap> model;
    milan::tb::Checker check{"media_phase pins"};
    check.echo_passes();
    std::printf("[pins] two interfaces on one clock domain: A TDM8 owner, B TDM4, graded at their pins\n");
    PinHarness harness(model.get(), check);
    return harness.run();
}

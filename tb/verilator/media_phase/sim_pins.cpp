// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Three media interfaces on one clock domain, graded at their pins (#632):
// the synthetic shape of pin_wrap.sv (TDM8 owner A and TDM4 B on one
// 24.576 MHz audio clock, TDM32 C on its 98.304 MHz clock off the same VCO,
// all real KL_tdm_capture_master instances, a 50 MHz datapath clock, the PHC
// the true time). C is the shipping 8x8 front end, whose frame the capture
// crossbar closes on an inner pair, a quarter of a frame in.
//
// A slot-MSB pin decoder per interface reads only that interface's bclk and
// fsync pins: the rise that reads fsync high is the frame's sync instant, and
// slot k's MSB is sampled (k x 32 + d) rises later, d the interface's data
// delay. The harness derives each slot's offset and each interface's constant
// itself, independently of the RTL's KL_media_if_latency_pkg, and requires:
//   [pins A|B|C] every frame instant the interface stamps (A: the domain
//              event, B and C: their own back-dated markers) is the frame's
//              slot-k MSB pin instant less slot k's offset, for every slot,
//              inside IEEE 1722-2016 10.8's +/-5 % of Ps and inside the
//              derivation (two datapath cycles);
//   [pins]     every CRF timing point the domain emits (its timestamp less the
//              2 ms Eq. 14 offset) is a frame instant of ALL three interfaces'
//              pins to +/-5 % of Ps: every interface's pin instants fall on
//              the same CRF timing points;
//   [pins]     the interfaces' constants differ pairwise by more than the
//              derivation band, so swapping two cannot pass.
// phase_mutants.py drops B's constant, swaps A's and B's, and derives C's at
// the frame's last pair instead of its closing pair, each a named failure.

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
//! the audio VCO 10.64 ppm under nominal, the shipping MMCM plan, so the
//! clocks never line up on a small period; C's clock is four times A's
constexpr double kPlan = 1.0 - 10.64e-6;
constexpr double kAudHz = 24.576e6 * kPlan;
constexpr double kTdm32Hz = 98.304e6 * kPlan;
constexpr double kHalfIFs = 0.5 * 1e15 / kAxisHz;
constexpr double kHalfAFs = 0.5 * 1e15 / kAudHz;
constexpr double kHalfCFs = 0.5 * 1e15 / kTdm32Hz;
//! the stamp's derivation band: the read side rounds half a datapath cycle
//! and the PHC is the time of the datapath edge that latched it
constexpr double kDerivNs = 2.0 * 1e9 / kAxisHz;
constexpr double kMttNs = 2e6;
//! the capture crossbar keeps four pairs and closes a frame on the last
constexpr int kKeptPairs = 4;

//! one interface's pin decoder and its graded stamps
struct Interface {
    Interface(const char* n, int s, int dd, double hz, double wr_hz)
        : name(n), slots(s), data_delay(dd), bit_hz(hz), write_hz(wr_hz) {}
    const char* name;
    int slots;
    int data_delay;
    double bit_hz;
    double write_hz;       //!< its FIFO write clock
    int prev_bclk = 0;
    long rise = -1;        //!< rises since the latest sync
    //! the latest frames' sync instants and slot-MSB instants, ns
    struct Frame {
        double sync = 0;
        std::array<double, 32> msb{};
        int got = 0;
    };
    std::deque<Frame> frames;
    long stamps = 0;
    long slot_grades = 0;
    double max_err = 0;

    double slot_offset(int k) const { return (k * 32.0 + data_delay) * 1e9 / bit_hz; }

    //! the marker latency, derived here: to the last bit of the pair that
    //! closes the frame (slot 2c+1's LSB, c the last kept pair), one write
    //! clock cycle to the FIFO, 4.5 datapath cycles of read side
    double latency() const {
        const int close = std::min(slots / 2, kKeptPairs) - 1;
        const double bits = 2.0 * (close + 1) * 32 + data_delay - 1;
        return bits * 1e9 / bit_hz + 1e9 / write_hz + 4.5e9 / kAxisHz;
    }

    void on_edge(int bclk, int fsync, double t_ns) {
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
    //! physics, not by its value: the marker of frame f arrives one latency
    //! after f's sync, so f is the latest frame synced at least half that
    //! before the stamp arrived. The stamp waits for that frame's last slot
    //! (C's marker comes a quarter of a frame in), then each slot's MSB less
    //! its offset grades it.
    void stamp(double stamp_ns, double arrival_ns) {
        const Frame* best = nullptr;
        for (const Frame& f : frames)
            if (f.sync <= arrival_ns - latency() / 2) best = &f;
        if (best) pending.push_back({stamp_ns, best->sync});
        grade_pending();
    }
    void grade_pending() {
        while (!pending.empty()) {
            const Frame* f = nullptr;
            for (const Frame& g : frames)
                if (g.sync == pending.front().sync) f = &g;
            if (f && f->got < slots && f == &frames.back()) return;   // still arriving
            if (f && f->got == slots) {
                stamps++;
                for (int k = 0; k < slots; k++) {
                    const double inst = f->msb[static_cast<size_t>(k)] - slot_offset(k);
                    max_err = std::max(max_err, std::fabs(pending.front().stamp - inst));
                    slot_grades++;
                }
            }
            pending.pop_front();
        }
    }
    struct Pending {
        double stamp;
        double sync;
    };
    std::deque<Pending> pending;

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
        for (const Interface* i : {&a_, &b_, &c_}) report_interface(*i);
        char what[220];
        std::snprintf(what, sizeof what,
                      "[pins] every CRF timing point is a frame instant of ALL three interfaces' pins, inside "
                      "+/-5 %% of Ps (%ld points, max A %.1f ns, B %.1f ns, C %.1f ns)",
                      crf_points_, crf_max_[0], crf_max_[1], crf_max_[2]);
        check_.that(what, crf_points_ >= 12 && crf_max_[0] < kBandNs && crf_max_[1] < kBandNs &&
                              crf_max_[2] < kBandNs);
        const double la = a_.latency(), lb = b_.latency(), lc = c_.latency();
        const double gap = std::min({std::fabs(la - lb), std::fabs(la - lc), std::fabs(lb - lc)});
        std::snprintf(what, sizeof what,
                      "[pins] the interfaces' constants differ (A %.1f ns, B %.1f ns, C %.1f ns): at least %.1f ns "
                      "apart, beyond the derivation band, so a swap cannot pass", la, lb, lc, gap);
        check_.that(what, gap > 2 * kDerivNs);
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
        const double next = std::min({next_i_, next_a_, next_c_});
        t_fs_ = next;
        const double t_ns = t_fs_ / 1e6;
        if (next == next_i_) {
            next_i_ += kHalfIFs;
            dut_->clk_i ^= 1;
            if (dut_->clk_i) dut_->ptp_now_i = static_cast<uint64_t>(t_ns);
            dut_->eval();
            if (dut_->clk_i) observe_clk();
        } else if (next == next_a_) {
            next_a_ += kHalfAFs;
            dut_->clk_audio_i ^= 1;
            dut_->eval();
            a_.on_edge(dut_->a_bclk_o, dut_->a_fsync_o, t_ns);
            b_.on_edge(dut_->b_bclk_o, dut_->b_fsync_o, t_ns);
        } else {
            next_c_ += kHalfCFs;
            dut_->clk_tdm32_i ^= 1;
            dut_->eval();
            c_.on_edge(dut_->c_bclk_o, dut_->c_fsync_o, t_ns);
        }
    }
    void run_ns(double ns) {
        const double te = t_fs_ + ns * 1e6;
        while (t_fs_ < te) tick_one();
    }

    void observe_clk() {
        // the stamps; the first few frames after reset are not yet complete
        const double now = t_fs_ / 1e6;
        if (dut_->a_ev_p_o && ++a_events_ > 4) a_.stamp(static_cast<double>(dut_->a_ns_o), now);
        if (dut_->b_ev_p_o && ++b_events_ > 4) b_.stamp(static_cast<double>(dut_->b_ns_o), now);
        if (dut_->c_ev_p_o && ++c_events_ > 4) c_.stamp(static_cast<double>(dut_->c_ns_o), now);
        // the CRF output: its timing points against every interface's pins
        if (dut_->crft_tvalid_o) {
            const uint64_t d = dut_->crft_tdata_o;
            for (int l = 0; l < 8; l++) crf_bytes_.push_back(static_cast<uint8_t>(d >> (8 * l)));
            if (dut_->crft_tlast_o) {
                if (crf_bytes_.size() >= 42) {
                    uint64_t ts = 0;
                    for (int k = 34; k < 42; k++) ts = (ts << 8) | crf_bytes_[static_cast<size_t>(k)];
                    const double inst = static_cast<double>(ts) - kMttNs;
                    crf_points_++;
                    const std::array<const Interface*, 3> all = {&a_, &b_, &c_};
                    for (size_t i = 0; i < all.size(); i++)
                        crf_max_[i] = std::max(crf_max_[i], all[i]->grid_dist(inst));
                }
                crf_bytes_.clear();
            }
        }
    }

    Vpin_wrap* dut_;
    milan::tb::Checker& check_;
    double t_fs_ = 0;
    double next_i_ = kHalfIFs;
    double next_a_ = kHalfAFs;
    double next_c_ = kHalfCFs;
    Interface a_{"A", 8, 1, 8 * 32 * 48000.0, 24.576e6};
    Interface b_{"B", 4, 0, 4 * 32 * 48000.0, 24.576e6};
    Interface c_{"C", 32, 1, 32 * 32 * 48000.0, 98.304e6};
    long a_events_ = 0;
    long b_events_ = 0;
    long c_events_ = 0;
    std::deque<uint8_t> crf_bytes_;
    long crf_points_ = 0;
    std::array<double, 3> crf_max_{};
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vpin_wrap> model;
    milan::tb::Checker check{"media_phase pins"};
    check.echo_passes();
    std::printf("[pins] three interfaces on one clock domain: A TDM8 owner, B TDM4, C TDM32, graded at their pins\n");
    PinHarness harness(model.get(), check);
    return harness.run();
}

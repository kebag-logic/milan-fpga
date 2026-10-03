// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The servo with the AAF clock meter in front of it (#629, the design's
// "servo-with-meter" row, tb/verilator/aaf_clock_meter/meter_servo_wrap.sv).
//
// A synthetic AAF talker at +20 ppm, its presentation times carrying
// +/-1,426 ns (the design point): 60 s in the worst-case shape for the loop,
// then 60 s with a random sign per group, then 60 s of independent error with
// one PDU lost in every 0.3 s and the talker stepped to +24 ppm at the leg's
// start. Pass: LOCKED within 10 s of the first PDU and never left; every
// window's |e| under 1,024 ns after the first LOCKED; by the end of the loss
// leg the trim has followed the 4 ppm step within 0.5 ppm (the mean trim over
// each leg's last 10 s, which the error shapes leave wandering by about that).
//
// TALKER PPM here is the servo suites' convention (sim_phc_step's): a
// +20 ppm talker's media clock runs 20 ppm FAST, so its 125 us of samples
// span 125,000 / (1 + 20e-6) ns of gPTP time.
//
// THE CLOCKS (one femtosecond wheel):
//   audio  the shipping 24.576 MHz plan (-10.64 ppm) divided by 32, shifted
//          by the behavioral MMCM's fine phase steps (1 ns each, GAIN 1);
//   ps_clk 2 MHz, the fine phase-shift runner (13 PSCLK per step);
//   clk_i  1 MHz, and 25 MHz from three audio cycles before each servo tick
//          to six after it: the servo's window span is sampled at the clk_i
//          edge after its tick crosses, so that edge carries silicon-like
//          quantisation (40 ns, against 10 ns at 100 MHz) while the rest of
//          the loop, which only counts, runs coarse. The meter's PDUs arrive
//          at the next clk_i edge after their wire time; nothing it computes
//          reads arrival time but its 100 ms timeout.
//
// THE WORST-CASE SHAPE. +/-J held over each 512 ms block of the meter's
// snapshot grid, with the signs of the loop's impulse response: the linear
// model below (the servo's PI shifts, a plant of gain 1 one window late,
// E8's two-point difference) gives the response h[k] of e to a snapshot
// error k windows back, and x[m] = J sign(h[(P - 1 - m) mod P]) puts the
// largest |e| the model allows at the end of every P-block period.

#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include "Vmeter_servo_wrap.h"
#include "Vmeter_servo_wrap___024root.h"
#include "verilated.h"

#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <memory>
#include <random>
#include <string>
#include <vector>

namespace {

constexpr double kBasePpm = -10.64;               //! the MMCM plan
constexpr int kTickCyc = TICK_CYC_TB;             //! audio cycles per 1 ms tick
constexpr double kAudioHz = 24.576e6 / 32.0;
constexpr double kHalfAudio0 = 0.5e15 / kAudioHz * (1.0 - kBasePpm * 1e-6);
constexpr double kHalfCoarse = 0.5e15 / 1e6;      //! clk_i 1 MHz
constexpr double kHalfFine = 0.5e15 / 25e6;       //! clk_i 25 MHz near a tick
constexpr double kHalfPs = 0.5e15 / 2e6;          //! ps_clk 2 MHz
constexpr double kPduFs = 125e9;                  //! 125 us
constexpr int kGroupPdus = 16;
constexpr int kSnapGroups = 256;
constexpr int64_t kJ = 1'426;
constexpr int32_t kLockThr = 1'024;
constexpr int kStateLocked = 4;
constexpr int kPeriodBlocks = 48;                 //! worst-case pattern period
constexpr uint64_t kSeed = 0x629'5E7C'0000'0001ULL;

//! The loop's response of e to a unit snapshot error k windows back.
std::array<double, kPeriodBlocks> impulse_response() {
    std::array<double, kPeriodBlocks + 8> g{};
    double integ = 0.0;
    double d = 0.0;                               //! (our - talker) x 512, this window
    for (size_t n = 0; n < g.size(); ++n) {
        const double eps = (n == 0) ? 1.0 : 0.0;
        const double e = -d - eps;
        g[n] = e;
        integ += e / 2.0;
        d = integ + e / 4.0;
    }
    std::array<double, kPeriodBlocks> h{};
    for (size_t k = 0; k < h.size(); ++k) h[k] = (g[k] - (k >= 8 ? g[k - 8] : 0.0)) / 8.0;
    return h;
}

class ServoMeterBench {
 public:
    explicit ServoMeterBench(milan::tb::Checker& check) : check_(check) {}

    Vmeter_servo_wrap* dut = nullptr;
    MmcmModel mm{};

    //! A frequency step that keeps the talker's phase: from the next PDU on
    //! its spacing changes, and its timeline continues from where it is.
    void step_talker_ppm(double ppm) {
        base_ts_ = ideal(pdu_n_);
        base_pdu_ = pdu_n_;
        talker_ppm_ = ppm;
    }
    std::function<int64_t(uint64_t)> err;
    std::function<bool(uint64_t)> lost;

    void reset() {
        mm.regs[0x08] = 0x0595;
        mm.regs[0x09] = 0x0080;
        mm.step_fs = 1e6;                         //! 1 ns per fine phase step
        dut->rst_n = 0;
        dut->mmcm_locked_i = 1;
        run_until(t_fs_ + 20e9);
        dut->rst_n = 1;
        next_pdu_fs_ = t_fs_ + 1e9;
        first_pdu_fs_ = next_pdu_fs_;
    }

    //! Run to absolute femtosecond time `until`.
    void run_until(double until) {
        while (t_fs_ < until) step();
    }
    double seconds_since_first_pdu() const { return (t_fs_ - first_pdu_fs_) * 1e-15; }

    int state() const { return static_cast<int>(dut->status_o & 7); }
    int16_t trim() const { return static_cast<int16_t>(dut->status_o >> 16); }

    // what the run saw
    double first_locked_s = -1.0;
    bool left_locked = false;
    int32_t worst_e = 0;
    uint64_t windows_after_lock = 0;
    std::vector<int16_t> trims;                   //! the trim at each window close

    //! the mean trim, in ppm, over the last `n` windows
    double mean_trim_ppm(size_t n) const {
        if (trims.size() < n) return 0.0;
        double sum = 0.0;
        for (size_t k = trims.size() - n; k < trims.size(); ++k) sum += trims[k];
        return sum / static_cast<double>(n) / 16.0;
    }

 private:
    milan::tb::Checker& check_;
    double t_fs_ = 0.0;
    double next_clk_ = kHalfCoarse;
    double next_ps_ = kHalfPs;
    double base_audio_ = kHalfAudio0;
    double next_audio_ = kHalfAudio0;
    double next_pdu_fs_ = 0.0;
    double first_pdu_fs_ = 0.0;
    uint64_t pdu_n_ = 0;
    double talker_ppm_ = 20.0;                    //! the header's +20 ppm talker
    long double base_ts_ = 1e9L;                  //! the timeline's anchor, ns
    uint64_t base_pdu_ = 0;
    bool pdu_pending_ = false;
    uint8_t pp_seq_q_ = 0;

    bool near_tick() const {
        const auto div = dut->rootp->meter_servo_wrap__DOT__servo__DOT__tick_div_r;
        return div >= static_cast<uint32_t>(kTickCyc - 3) || div <= 6;
    }

    long double ideal(uint64_t i) const {
        const long double spacing = 125'000.0L / (1.0L + talker_ppm_ * 1e-6L);
        return base_ts_ + static_cast<long double>(i - base_pdu_) * spacing;
    }
    int64_t stamp(uint64_t i) const {
        int64_t v = static_cast<int64_t>(std::floor(ideal(i)));
        if (err) v += err(i);
        return v;
    }

    void step() {
        if (next_clk_ <= next_ps_ && next_clk_ <= next_audio_) {
            t_fs_ = next_clk_;
            next_clk_ += near_tick() ? kHalfFine : kHalfCoarse;
            dut->clk_i ^= 1;
            if (dut->clk_i) on_clk_rise();
            dut->eval();
            if (dut->clk_i) after_clk_rise();
        } else if (next_ps_ <= next_audio_) {
            t_fs_ = next_ps_;
            next_ps_ += kHalfPs;
            dut->ps_clk_i ^= 1;
            dut->eval();
            if (dut->ps_clk_i) {
                mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
                dut->ps_done_i = mm.psdone;
            }
        } else {
            t_fs_ = next_audio_;
            base_audio_ += kHalfAudio0;
            next_audio_ = base_audio_ + mm.audio_adj_fs;
            if (next_audio_ <= t_fs_) next_audio_ = t_fs_ + 1e3;
            dut->clk_audio_i ^= 1;
            dut->eval();
        }
    }

    void on_clk_rise() {
        dut->ptp_now_i = static_cast<uint64_t>(t_fs_ / 1e6);
        dut->match_p_i = 0;
        if (!pdu_pending_ && t_fs_ >= next_pdu_fs_) {
            const uint64_t i = pdu_n_++;
            next_pdu_fs_ += kPduFs;
            if (!(lost && lost(i))) {
                dut->match_p_i = 1;
                dut->seq_i = static_cast<uint8_t>(i & 0xFF);
                dut->ts_i = static_cast<uint32_t>(static_cast<uint64_t>(stamp(i)));
            }
        }
    }

    void after_clk_rise() {
        mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o, dut->drp_di_o,
                     dut->mmcm_rst_o);
        dut->drp_do_i = mm.dout;
        dut->drp_rdy_i = mm.drdy;
        dut->mmcm_locked_i = mm.locked;
        const int st = state();
        if (st == kStateLocked && first_locked_s < 0.0) first_locked_s = seconds_since_first_pdu();
        if (first_locked_s >= 0.0 && st != kStateLocked) left_locked = true;
        //! the window error lands at the PI micro-sequence's S3 (pp_seq 3 -> 4)
        const uint8_t seq = dut->rootp->meter_servo_wrap__DOT__servo__DOT__pp_seq_r;
        if (seq == 4 && pp_seq_q_ == 3 && first_locked_s >= 0.0 &&
            dut->rootp->meter_servo_wrap__DOT__servo__DOT__pp_run_r) {
            const int32_t e = dut->rootp->meter_servo_wrap__DOT__servo__DOT__ew_r;
            ++windows_after_lock;
            if (std::abs(e) > worst_e) worst_e = std::abs(e);
            trims.push_back(trim());
        }
        pp_seq_q_ = seq;
    }
};

//! the worst-case snapshot-error sign pattern of the header
std::function<int64_t(uint64_t)> worst_case_shape() {
    const auto h = impulse_response();
    return [h](uint64_t i) {
        const uint64_t block = i / (static_cast<uint64_t>(kGroupPdus) * kSnapGroups);
        const size_t k = static_cast<size_t>(kPeriodBlocks - 1 - (block % kPeriodBlocks));
        return h[k] >= 0.0 ? kJ : -kJ;
    };
}

std::function<int64_t(uint64_t)> random_sign_group(uint64_t seed) {
    auto gen = std::make_shared<std::mt19937_64>(seed);
    auto cache = std::make_shared<std::vector<int64_t>>();
    return [gen, cache](uint64_t i) {
        const uint64_t g = i / kGroupPdus;
        while (cache->size() <= g) cache->push_back(((*gen)() & 1U) ? kJ : -kJ);
        return (*cache)[g];
    };
}

std::function<int64_t(uint64_t)> independent(uint64_t seed) {
    auto gen = std::make_shared<std::mt19937_64>(seed);
    auto cache = std::make_shared<std::vector<int64_t>>();
    return [gen, cache](uint64_t i) {
        while (cache->size() <= i) {
            cache->push_back(static_cast<int64_t>((*gen)() % static_cast<uint64_t>(2 * kJ + 1)) - kJ);
        }
        return (*cache)[i];
    };
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vmeter_servo_wrap> model;
    milan::tb::Checker ck{"aaf_clock_meter servo"};
    ServoMeterBench b{ck};
    b.dut = model.get();
    constexpr double kLegFs = 60e15;
    b.err = worst_case_shape();
    b.reset();
    const double first_pdu = 21e9;                //! reset's 20 us plus 1 us
    b.run_until(first_pdu + kLegFs);
    std::printf("  info: S2 worst: first LOCKED %.2f s, worst |e| %d ns over %llu windows\n",
                b.first_locked_s, b.worst_e, static_cast<unsigned long long>(b.windows_after_lock));
    ck.that("[S2] LOCKED within 10 s of the first PDU",
            b.first_locked_s >= 0.0 && b.first_locked_s <= 10.0);
    ck.that("[S2 worst] every window's |e| under 1,024 ns after the first LOCKED",
            b.worst_e < kLockThr && b.windows_after_lock > 80);
    b.worst_e = 0;
    b.err = random_sign_group(kSeed);
    b.run_until(first_pdu + 2 * kLegFs);
    std::printf("  info: S2 rsign: worst |e| %d ns\n", b.worst_e);
    ck.that("[S2 rsign] every window's |e| under 1,024 ns", b.worst_e < kLockThr);
    //! 20 windows, the last 10 s of each leg: the trim wanders with the
    //! leg's error shape, so a single sample would grade that wander
    constexpr size_t kMeanWindows = 20;
    const double trim_before = b.mean_trim_ppm(kMeanWindows);
    b.worst_e = 0;
    b.step_talker_ppm(24.0);
    b.err = independent(kSeed + 1);
    b.lost = [](uint64_t i) { return i % 2400 == 1200; };
    b.run_until(first_pdu + 3 * kLegFs);
    const double trim_after = b.mean_trim_ppm(kMeanWindows);
    const double moved_ppm = trim_after - trim_before;
    std::printf("  info: S2 loss: worst |e| %d ns; mean trim %+.3f -> %+.3f ppm (moved %+.3f)\n",
                b.worst_e, trim_before, trim_after, moved_ppm);
    ck.that("[S2 loss] every window's |e| under 1,024 ns", b.worst_e < kLockThr);
    ck.that("[S2 loss] the trim followed the 4 ppm step within 0.5 ppm",
            std::fabs(moved_ppm - 4.0) <= 0.5);
    ck.that("[S2] LOCKED never left after the first LOCKED", !b.left_locked);
    return ck.report();
}

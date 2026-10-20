// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The in-tree two-interface shape graded at its pins (#632, R677-1-F1):
// blend_wrap.sv, the Arty I2S + TDM8 capture bound as milan_datapath binds
// it. Two codec models drive the pins: the I2S ADC writes every bit of frame
// m with a word naming m, the TDM codec every slot of its frame m likewise,
// each recording the instant its frame started at the pins (the I2S LRCK
// fall, the instant the I2S marker latency is derived to; the TDM frame sync
// sampled at a bit-clock rise, slot k's MSB (32k + 1) bit periods later).
// Each frame the capture crossbar banks is then read with the instant it
// banked: the I2S pair and every TDM pair of it must have started at their
// pins within +/-5 % of Ps of that one instant, unfolded, so no whole sample
// apart (IEEE 1722-2016 4.3.5, 10.8). Closing the frame on a TDM pair, as
// before #632's R677-1-F1, banked the I2S pair of an earlier frame. Six reset
// phases of the audio clock against the datapath clock. Planted controls:
// phase_mutants.py.

#include "Vblend_wrap.h"
#include "Vblend_wrap___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string>

namespace {

constexpr double kPsNs = 1e9 / 48000.0;
constexpr double kBandNs = 0.05 * kPsNs;
constexpr double kHalfClkNs = 10.0;                      //!< 50 MHz
constexpr double kHalfAudNs = 1e9 / 24.576e6 / 2.0;
constexpr uint32_t kI2sTag = 0xA00000;
constexpr uint32_t kTdmTag = 0x500000;
constexpr double kWarmNs = 1e6;                          //!< graded after 1 ms
constexpr double kEndNs = 4e6;

//! the spread of one quantity over the banked frames
struct Spread {
    double lo = 1e18;
    double hi = -1e18;
    long bad = 0;
    void add(double e) {
        lo = std::fmin(lo, e);
        hi = std::fmax(hi, e);
        if (std::fabs(e) >= kBandNs) bad++;
    }
    double worst() const { return std::fmax(std::fabs(lo), std::fabs(hi)); }
};

//! one reset phase: the two codec models, the bank reader and its tallies
class BlendPhase {
 public:
    BlendPhase(Vblend_wrap* d, int k) : d_(d), na_(kHalfAudNs + k * 7.3), reset_at_(2000.0 + k * 1013.0) {}

    void run() {
        d_->clk_i = 0;
        d_->clk_audio_i = 0;
        d_->rst_n = 0;
        d_->ptp_now_i = 0;
        d_->i2s_sdout_i = 0;
        d_->tdm_data_i = 0;
        d_->eval();
        while (t_ < kEndNs) {
            if (ni_ <= na_) clk_edge();
            else audio_edge();
        }
    }

    long banked = 0;
    long bad_tag = 0;
    Spread i2s;
    Spread tdm;
    double worst_pair = 0;

 private:
    void clk_edge() {
        t_ = ni_;
        ni_ += kHalfClkNs;
        d_->clk_i ^= 1;
        if (d_->clk_i) {
            d_->ptp_now_i = static_cast<uint64_t>(std::llround(t_));
            d_->rst_n = t_ > reset_at_;
        }
        d_->eval();
        if (d_->clk_i) read_bank();
    }

    void audio_edge() {
        t_ = na_;
        na_ += kHalfAudNs;
        d_->clk_audio_i ^= 1;
        d_->eval();
        i2s_codec();
        tdm_codec();
    }

    //! the I2S ADC: a frame starts at the LRCK fall; the bit for each SCLK
    //! rise is driven on the fall before it (Philips: one-bit delay, the
    //! word's MSB at the second rise, 24 bits in 32)
    void i2s_codec() {
        if (lrck_prev_ && !d_->i2s_lrck_o) {
            i2s_m_++;
            i2s_start_[i2s_m_] = t_;
            i2s_rises_ = 0;
        }
        lrck_prev_ = d_->i2s_lrck_o;
        if (!sclk_prev_ && d_->i2s_sclk_o && i2s_m_ >= 0) i2s_rises_++;
        if (sclk_prev_ && !d_->i2s_sclk_o && i2s_m_ >= 0) {
            const long idx = i2s_rises_ % 32;
            const uint32_t w = kI2sTag | static_cast<uint32_t>(i2s_m_ & 0x0FFFFF);
            d_->i2s_sdout_i = (idx >= 1 && idx <= 24) ? ((w >> (24 - idx)) & 1) : 0;
        }
        sclk_prev_ = d_->i2s_sclk_o;
    }

    //! the TDM codec: the rise that samples the frame sync high is bit period
    //! 0 of a frame; slot k's bit b is sampled at period 1 + 32k + b
    void tdm_codec() {
        if (!bclk_prev_ && d_->tdm_bclk_o) {
            if (d_->tdm_fsync_o) {
                tdm_m_++;
                tdm_start_[tdm_m_] = t_;
                tdm_rises_ = 0;
            }
            tdm_rises_++;
        }
        if (bclk_prev_ && !d_->tdm_bclk_o && tdm_m_ >= 0) {
            const long pos = tdm_rises_ % 256;
            const long b = (pos - 1) % 32;
            const uint32_t w = kTdmTag | static_cast<uint32_t>(tdm_m_ & 0x0FFFFF);
            d_->tdm_data_i = (pos >= 1 && b < 24) ? ((w >> (23 - b)) & 1) : 0;
        }
        bclk_prev_ = d_->tdm_bclk_o;
    }

    //! a frame banked: grade each of its pairs against the instant banked
    void read_bank() {
        auto* r = d_->rootp;
        const uint32_t ns = r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_ns_r;
        if (have_last_ && ns != last_ns_ && t_ > kWarmNs) {
            banked++;
            const double x = static_cast<double>(ns);
            double first_i2s = -1;
            double first_tdm = -1;
            for (int p = 0; p < 4; p++) {
                const double start = pair_start(r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_r[p], p);
                if (start < 0) continue;
                if (p == 0) { i2s.add(start - x); first_i2s = start; }
                else { tdm.add(start - x); if (first_tdm < 0) first_tdm = start; }
            }
            if (first_i2s >= 0 && first_tdm >= 0)
                worst_pair = std::fmax(worst_pair, std::fabs(first_i2s - first_tdm));
        }
        last_ns_ = ns;
        have_last_ = true;
    }

    //! the pins instant the banked pair's frame started at, or -1 for a pair
    //! that names no frame its codec sent
    double pair_start(uint64_t v, int p) {
        const uint32_t lv = static_cast<uint32_t>(v >> 24) & 0xFFFFFF;
        const uint32_t rv = static_cast<uint32_t>(v) & 0xFFFFFF;
        const uint32_t tag = lv & 0xF00000;
        const long m = static_cast<long>(lv & 0x0FFFFF);
        const auto& starts = (p == 0) ? i2s_start_ : tdm_start_;
        const auto it = starts.find(m);
        if (lv != rv || tag != (p == 0 ? kI2sTag : kTdmTag) || it == starts.end()) {
            bad_tag++;
            return -1;
        }
        return it->second;
    }

    Vblend_wrap* d_;
    double t_ = 0;
    double ni_ = kHalfClkNs;
    double na_;
    double reset_at_;
    int lrck_prev_ = 0;
    int sclk_prev_ = 0;
    int bclk_prev_ = 0;
    long i2s_m_ = -1;
    long i2s_rises_ = 0;
    long tdm_m_ = -1;
    long tdm_rises_ = 0;
    uint32_t last_ns_ = 0;
    bool have_last_ = false;
    std::map<long, double> i2s_start_;
    std::map<long, double> tdm_start_;
};

void grade(milan::tb::Checker& c, int k, const BlendPhase& g) {
    std::printf("  info: [blend %d] %ld banked frames; I2S frame start - banked instant %.1f .. %.1f ns, "
                "TDM frame start - banked instant %.1f .. %.1f ns, I2S against TDM of one bank max %.1f ns\n",
                k, g.banked, g.i2s.lo, g.i2s.hi, g.tdm.lo, g.tdm.hi, g.worst_pair);
    char what[240];
    std::snprintf(what, sizeof what, "[blend %d] every banked pair names a frame its codec sent (%ld banked)", k, g.banked);
    c.that(what, g.bad_tag == 0 && g.banked > 100);
    std::snprintf(what, sizeof what,
                  "[blend %d] the I2S pair of every banked frame started at its pins inside +/-5 %% of Ps of the "
                  "banked instant, unfolded (max %.1f ns)", k, g.i2s.worst());
    c.that(what, g.i2s.bad == 0 && g.banked > 100);
    std::snprintf(what, sizeof what,
                  "[blend %d] every TDM pair of every banked frame started at its pins inside +/-5 %% of Ps of the "
                  "banked instant, unfolded (max %.1f ns)", k, g.tdm.worst());
    c.that(what, g.tdm.bad == 0 && g.banked > 100);
    std::snprintf(what, sizeof what,
                  "[blend %d] ...the I2S pair inside the I2S marker latency's derivation, +/-40 ns (%.1f .. %.1f ns)",
                  k, g.i2s.lo, g.i2s.hi);
    c.that(what, g.i2s.lo > -40.0 && g.i2s.hi < 40.0);
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"media_phase blend"};
    check.echo_passes();
    std::printf("[blend] the Arty I2S + TDM8 capture of one domain, graded at its pins\n");
    for (int k = 0; k < 6; k++) {
        const milan::tb::Model<Vblend_wrap> model;
        BlendPhase phase(model.get(), k);
        phase.run();
        grade(check, k, phase);
    }
    return check.report();
}

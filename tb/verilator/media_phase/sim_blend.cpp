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
// before #632's R677-1-F1, banked the I2S pair of the frame before: a whole
// period older than its stamp. Six reset phases of the audio clock against
// the datapath clock. Planted controls: phase_mutants.py.

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

class BlendHarness {
 public:
    BlendHarness(milan::tb::Checker& c) : c_(c) {}

    void run_phase(int k) {
        Vblend_wrap* d = new Vblend_wrap;
        d_ = d;
        double t = 0, ni = kHalfClkNs, na = kHalfAudNs + k * 7.3;
        d->clk_i = 0; d->clk_audio_i = 0; d->rst_n = 0; d->ptp_now_i = 0;
        d->i2s_sdout_i = 0; d->tdm_data_i = 0;
        d->eval();
        const double reset_at = 2000.0 + k * 1013.0;
        int lrck_prev = 0, sclk_prev = 0, bclk_prev = 0;
        long i2s_m = -1, i2s_rises = 0, tdm_m = -1, tdm_rises = 0;
        uint32_t last_ns = 0;
        bool have_last = false;
        double worst_i2s = 0, worst_tdm = 0, worst_pair = 0;
        double lo_i2s = 1e18, hi_i2s = -1e18, lo_tdm = 1e18, hi_tdm = -1e18;
        long banked = 0, bad_i2s = 0, bad_tdm = 0, bad_tag = 0;
        while (t < 4e6) {
            if (ni <= na) {
                t = ni; ni += kHalfClkNs; d->clk_i ^= 1;
                if (d->clk_i) {
                    d->ptp_now_i = static_cast<uint64_t>(std::llround(t));
                    d->rst_n = t > reset_at;
                }
                d->eval();
                if (!d->clk_i) continue;
                // a frame banked: its pairs and its instant
                auto* r = d->rootp;
                const uint32_t ns = r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_ns_r;
                if (have_last && ns != last_ns && t > 1e6) {
                    banked++;
                    const double x = static_cast<double>(ns);
                    for (int p = 0; p < 4; p++) {
                        const uint64_t v = r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_r[p];
                        const uint32_t lv = static_cast<uint32_t>(v >> 24) & 0xFFFFFF;
                        const uint32_t rv = static_cast<uint32_t>(v) & 0xFFFFFF;
                        const uint32_t tag = lv & 0xF00000;
                        const long m = static_cast<long>(lv & 0x0FFFFF);
                        if (lv != rv || (p == 0 && tag != kI2sTag) || (p > 0 && tag != kTdmTag)) { bad_tag++; continue; }
                        const auto& starts = (p == 0) ? i2s_start_ : tdm_start_;
                        auto it = starts.find(m);
                        if (it == starts.end()) { bad_tag++; continue; }
                        const double e = it->second - x;      // unfolded
                        if (p == 0) {
                            worst_i2s = std::fmax(worst_i2s, std::fabs(e));
                            lo_i2s = std::fmin(lo_i2s, e); hi_i2s = std::fmax(hi_i2s, e);
                            if (std::fabs(e) >= kBandNs) bad_i2s++;
                        } else {
                            worst_tdm = std::fmax(worst_tdm, std::fabs(e));
                            lo_tdm = std::fmin(lo_tdm, e); hi_tdm = std::fmax(hi_tdm, e);
                            if (std::fabs(e) >= kBandNs) bad_tdm++;
                        }
                    }
                    // the two interfaces of one banked frame: one frame instant
                    const uint64_t v0 = r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_r[0];
                    const uint64_t v1 = r->blend_wrap__DOT__u_cmap__DOT__tdm_frame_r[1];
                    const long m0 = static_cast<long>((v0 >> 24) & 0x0FFFFF);
                    const long m1 = static_cast<long>((v1 >> 24) & 0x0FFFFF);
                    if (i2s_start_.count(m0) && tdm_start_.count(m1))
                        worst_pair = std::fmax(worst_pair, std::fabs(i2s_start_[m0] - tdm_start_[m1]));
                }
                last_ns = ns;
                have_last = true;
            } else {
                t = na; na += kHalfAudNs; d->clk_audio_i ^= 1;
                d->eval();
                // I2S: a frame starts at the LRCK fall; the bit for each SCLK
                // rise is driven on the fall before it (Philips: one-bit delay,
                // the word's MSB at the second rise, 24 bits in 32)
                if (lrck_prev && !d->i2s_lrck_o) {
                    i2s_m++;
                    i2s_start_[i2s_m] = t;
                    i2s_rises = 0;
                }
                lrck_prev = d->i2s_lrck_o;
                if (!sclk_prev && d->i2s_sclk_o && i2s_m >= 0) i2s_rises++;
                if (sclk_prev && !d->i2s_sclk_o && i2s_m >= 0) {
                    const long idx = i2s_rises % 32;      // bit index the next rise samples
                    const uint32_t w = kI2sTag | static_cast<uint32_t>(i2s_m & 0x0FFFFF);
                    d->i2s_sdout_i = (idx >= 1 && idx <= 24) ? ((w >> (24 - idx)) & 1) : 0;
                }
                sclk_prev = d->i2s_sclk_o;
                // TDM: the rise that samples the frame sync high is bit period
                // 0 of a frame; slot k's bit b is sampled at period 1 + 32k + b
                if (!bclk_prev && d->tdm_bclk_o) {
                    if (d->tdm_fsync_o) {
                        tdm_m++;
                        tdm_start_[tdm_m] = t;
                        tdm_rises = 0;
                    }
                    tdm_rises++;
                }
                if (bclk_prev && !d->tdm_bclk_o && tdm_m >= 0) {
                    const long pos = tdm_rises % 256;     // the period the next rise samples
                    const long b = (pos - 1) % 32;
                    const uint32_t w = kTdmTag | static_cast<uint32_t>(tdm_m & 0x0FFFFF);
                    d->tdm_data_i = (pos >= 1 && b < 24) ? ((w >> (23 - b)) & 1) : 0;
                }
                bclk_prev = d->tdm_bclk_o;
            }
        }
        std::printf("  info: [blend %d] %ld banked frames; I2S frame start - banked instant %.1f .. %.1f ns, "
                    "TDM frame start - banked instant %.1f .. %.1f ns, I2S against TDM of one bank max %.1f ns\n",
                    k, banked, lo_i2s, hi_i2s, lo_tdm, hi_tdm, worst_pair);
        char what[240];
        std::snprintf(what, sizeof what, "[blend %d] every banked pair names a frame its codec sent (%ld banked)", k, banked);
        c_.that(what, bad_tag == 0 && banked > 100);
        std::snprintf(what, sizeof what,
                      "[blend %d] the I2S pair of every banked frame started at its pins inside +/-5 %% of Ps of the "
                      "banked instant, unfolded (max %.1f ns)", k, worst_i2s);
        c_.that(what, bad_i2s == 0 && banked > 100);
        std::snprintf(what, sizeof what,
                      "[blend %d] every TDM pair of every banked frame started at its pins inside +/-5 %% of Ps of the "
                      "banked instant, unfolded (max %.1f ns)", k, worst_tdm);
        c_.that(what, bad_tdm == 0 && banked > 100);
        std::snprintf(what, sizeof what,
                      "[blend %d] ...the I2S pair inside the I2S marker latency's derivation, +/-40 ns (%.1f .. %.1f ns)",
                      k, lo_i2s, hi_i2s);
        c_.that(what, lo_i2s > -40.0 && hi_i2s < 40.0);
        d->final();
        delete d;
        i2s_start_.clear();
        tdm_start_.clear();
    }

 private:
    milan::tb::Checker& c_;
    Vblend_wrap* d_ = nullptr;
    std::map<long, double> i2s_start_;
    std::map<long, double> tdm_start_;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"media_phase blend"};
    check.echo_passes();
    std::printf("[blend] the Arty I2S + TDM8 capture of one domain, graded at its pins\n");
    BlendHarness harness(check);
    for (int k = 0; k < 6; k++) harness.run_phase(k);
    return check.report();
}

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The phase detector of KL_mmcm_drp_servo on its own (#632, #764): every
// boundary the closed loop of sim_main.cpp reaches only by chance, placed
// exactly. The servo's tick divider runs at 32 audio cycles (the audio clock
// is clk_i here), so a 512-tick window is 16,384 cycles holding 256 PDUs, one
// every 64 cycles, two cycles after a domain event. The harness holds the
// rate side still: the state is kept LOCKED and each window boundary is given
// exactly the nominal 512 ms span against a zero reference rate, so the
// window error is zero and the integrator moves by the phase term alone. No
// plant, no physical claim: the loop's dynamics are sim_main.cpp's. Each
// PDU's phase d = domain event - CRF timestamp is chosen per sample:
//
//   inband     +/-100 ns alternating: engaged, settled first at the close of
//              the fourth full in-band window, and not before
//   events     the same, then an mr restart mid-window and phase samples
//              moved out of the band: settled (phase_o[21], MCSRV_STAT[9])
//              reads 0 at once and only rises again after four clean
//              in-band windows; it falls at the first window with a sample
//              out of the band and stays low while they are
//   meanin     +/-1,500 ns alternating: the mean is inside the band, no
//              sample is, so settled never asserts
//   balanced   +/-10,416 ns alternating, either side of +/-Ps/2: the window
//              phase reads the half-period phase it is and pulls at the
//              slew limit; settled never asserts
//   unbal129   the same, 129 samples on one side and 127 on the other
//   unbal160   the same, 160 against 96
//   jitter     Ps/2 - 20 ns with +/-60 ns of uniform jitter: straddling
//   cross      Ps/2 - 100 ns for three windows, then past +Ps/2 by 100 ns:
//              the window phase re-folds to the short way
//   range      d = +/-(2^25 - 1) ns is sampled, d = +/-2^25 ns is not
//   snap       a steady +500 ns phase; each hold condition (mr, the term
//              disabled, a broken history, a state other than LOCKED, a
//              local PHC step, the slew level) placed on the window's
//              closing edge, one cycle before and one after: the committed
//              phase contribution is zero for the first two and the closed
//              window's whole correction for the third
//
// Mutants: phase_mutants.py plants one defect per detector behaviour and
// requires the named check to fail.

#include "Vdet_servo.h"
#include "Vdet_servo___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <functional>
#include <string>

#define R(n) d_->rootp->KL_mmcm_drp_servo__DOT__##n

namespace {

constexpr double kPsNs = 1e9 / 48000.0;
constexpr int kPsU = 62500;                  //!< Ps in 1/3 ns
constexpr int kHalfU = kPsU / 2;
constexpr int kBandU = kPsU / 20;            //!< 10.8 Eq. 15, in 1/3 ns
constexpr int kClampU = 16384;               //!< PH_SLEW_NS_P = 256 at PH_GAIN_LSH_P = 1
constexpr uint32_t kDomNs = 1000000000u;     //!< the domain event's instant
constexpr int kPduCyc = 64;
constexpr int kWinCyc = 512 * 32;

class DetHarness {
 public:
    DetHarness(Vdet_servo* d, milan::tb::Checker& c) : d_(d), c_(c) {}

    int run(const std::string& name);

 private:
    //! one clk_i edge; the inputs of this cycle are set by the caller
    void edge() {
        d_->clk_i = 0; d_->clk_audio_i = 0; d_->ps_clk_i = 0;
        d_->eval();
        d_->clk_i = 1; d_->clk_audio_i = 1; d_->ps_clk_i = 1;
        d_->ptp_now_i += 20 + ptp_step_;
        ptp_step_ = 0;
        d_->eval();
        cyc_++;
    }

    void reset() {
        d_->sel_i = 1; d_->ref_locked_i = 1; d_->ref_rate_valid_i = 1; d_->ph_en_i = 1;
        d_->mmcm_locked_i = 1; d_->ref_rate_ns_i = 0; d_->phc_slew_active_i = 0;
        d_->ref_restart_p_i = 0; d_->dom_ev_p_i = 0; d_->ref_ts_p_i = 0;
        d_->auto_repair_i = 0; d_->ps_invert_i = 0;
        d_->ptp_now_i = 5000000000ULL;
        d_->rst_n = 0;
        for (int i = 0; i < 8; i++) edge();
        d_->rst_n = 1;
        cyc_ = 0;
        pdu_ = 0;
        windows_ = 0;
        full_run_ = 0;
        settle_rise_full_ = -1;
        bad_mirror_ = false;
    }

    //! one cycle: the PDU schedule, the forced LOCKED state, the nominal
    //! window span at each boundary, then the edge. `t0` reports whether this
    //! edge closed a window
    bool step_cycle() {
        d_->dom_ev_p_i = (cyc_ % kPduCyc) == 0;
        d_->dom_ns_i = kDomNs;
        d_->ref_ts_p_i = (cyc_ % kPduCyc) == 2;
        if (d_->ref_ts_p_i) d_->ref_ts_ns_i = kDomNs - static_cast<uint32_t>(static_cast<int32_t>(sample_(pdu_++)));
        if (!acquire_now_) R(state_r) = 4;
        else R(state_r) = 3;
        R(lock_cnt_r) = 4;
        const bool t0 = R(tick_p_w) && R(win_valid_r) && R(tick_cnt_r) == 511;
        if (t0) {
            R(win_start_r) = R(ptp_q_r) - 512000000ULL;
            const unsigned cnt = R(ph_cnt_r);
            closing_full_ = cnt >= 255 && R(ph_wok_r);
        }
        edge();
        if (((d_->status_o >> 9) & 1) != ((d_->phase_o >> 21) & 1)) bad_mirror_ = true;
        if (t0) {
            windows_++;
            full_run_ = closing_full_ ? full_run_ + 1 : 0;
        }
        return t0;
    }
    //! run until `n` more windows have closed
    void windows(int n) {
        const unsigned w = windows_ + n;
        while (windows_ < w) step_cycle();
    }

    int theta() const { return static_cast<int16_t>(R(ph_theta_r)); }
    bool settled() const { return (d_->phase_o >> 21) & 1; }
    bool engaged() const { return (d_->phase_o >> 20) & 1; }
    unsigned wcount() const { return (d_->phase_o >> 23) & 0x1FF; }
    int64_t integ() const {
        const int32_t i = static_cast<int32_t>(R(integ_r) << 8) >> 8;
        return static_cast<int64_t>(i) * 256 + R(integ_frac_r);
    }

    //! a sample source and a few windows of it from reset; settled is
    //! watched on every cycle, and the full window it first rises after
    void run_samples(std::function<int64_t(long)> f, int n, bool* ever_settled) {
        sample_ = std::move(f);
        reset();
        *ever_settled = false;
        while (windows_ < static_cast<unsigned>(n)) {
            const bool was = settled();
            step_cycle();
            if (settled()) *ever_settled = true;
            if (settled() && !was && settle_rise_full_ < 0) settle_rise_full_ = full_run_;
        }
    }

    // ----------------------------------------------------------------- cases
    void case_inband() {
        bool ever = false;
        run_samples([](long k) { return (k & 1) ? -100 : 100; }, 8, &ever);
        char what[200];
        std::snprintf(what, sizeof what, "[det inband] engaged, the window phase inside the band (theta %d)", theta());
        c_.that(what, engaged() && std::abs(theta()) < kBandU);
        std::snprintf(what, sizeof what,
                      "[det inband] settled first reads 1 at the close of the fourth full in-band window (at %d)",
                      settle_rise_full_);
        c_.that(what, settle_rise_full_ == 4);
        c_.that("[det inband] MCSRV_STAT[9] mirrors phase_o[21] on every cycle", !bad_mirror_);
    }

    void case_events() {
        bool ever = false;
        bool out = false;
        run_samples([&out](long k) -> int64_t { return out ? 5000 : ((k & 1) ? -100 : 100); }, 8, &ever);
        c_.that("[det events] settled before the restart", settled());
        // an mr restart in the middle of a window
        for (int i = 0; i < kWinCyc / 2; i++) step_cycle();
        d_->ref_restart_p_i = 1;
        step_cycle();
        d_->ref_restart_p_i = 0;
        c_.that("[det events] settled reads 0 on the cycle after an mr restart", !settled());
        // count the clean full windows after the one the restart spoiled
        while (!(R(tick_p_w) && R(win_valid_r) && R(tick_cnt_r) == 511)) step_cycle();
        step_cycle();   // the spoiled window closes
        int clean = 0;
        int rise_at = -1;
        bool low_before = true;
        while (clean < 6) {
            const bool t0 = step_cycle();
            if (t0) clean++;
            if (settled() && rise_at < 0) rise_at = clean;
            if (settled() && clean < 4) low_before = false;
        }
        char what[200];
        std::snprintf(what, sizeof what,
                      "[det events] after the restart settled rises only at the close of the fourth clean window (at %d)",
                      rise_at);
        c_.that(what, low_before && rise_at == 4);
        // phase samples out of the band from this window boundary on: the
        // window that closes next is the first to hold them
        out = true;
        bool high_after = false;
        int t0s = 0;
        while (t0s < 6) {
            if (step_cycle()) t0s++;
            if (t0s >= 1 && settled()) high_after = true;
        }
        c_.that("[det events] settled falls at the first window with a sample out of the band and stays low",
                !high_after && !settled());
        c_.that("[det events] MCSRV_STAT[9] mirrors phase_o[21] on every cycle", !bad_mirror_);
    }

    void case_meanin() {
        bool ever = false;
        run_samples([](long k) { return (k & 1) ? -1500 : 1500; }, 9, &ever);
        char what[200];
        std::snprintf(what, sizeof what, "[det meanin] the window phase is the samples' mean, inside the band (theta %d)",
                      theta());
        c_.that(what, engaged() && std::abs(theta()) < kBandU);
        c_.that("[det meanin] settled never asserts with every sample outside the band", !ever);
    }

    //! the half-period cases: the window phase must read about Ps/2 and pull
    //! at the slew limit, and settled must never assert
    void half_period(const char* tag, std::function<int64_t(long)> f) {
        bool ever = false;
        run_samples(std::move(f), 6, &ever);
        // the next committed correction: past the one the last boundary
        // started, then the whole of the next
        for (int i = 0; i < 16; i++) step_cycle();
        const int64_t i0 = integ();
        windows(1);
        for (int i = 0; i < 16; i++) step_cycle();
        const int64_t di = integ() - i0 - static_cast<int64_t>(static_cast<int32_t>(R(ew_r))) * 128;
        char what[200];
        std::snprintf(what, sizeof what, "[det %s] the window phase reads the half-period phase (theta %d, |theta| >= %d)",
                      tag, theta(), kHalfU - kBandU);
        c_.that(what, engaged() && std::abs(theta()) >= kHalfU - kBandU);
        std::snprintf(what, sizeof what, "[det %s] the committed correction is the slew limit's (%lld/256)",
                      tag, static_cast<long long>(di));
        c_.that(what, std::llabs(di) == 2LL * kClampU);
        std::snprintf(what, sizeof what, "[det %s] settled never asserts", tag);
        c_.that(what, !ever);
    }

    void case_cross() {
        bool ever = false;
        bool crossed = false;
        run_samples([&crossed](long) { return crossed ? -10317 : 10317; }, 4, &ever);
        const int before = theta();
        crossed = true;               // from this window boundary on
        windows(2);
        const int after = theta();
        char what[200];
        std::snprintf(what, sizeof what, "[det cross] before the crossing the window phase reads +Ps/2 - 100 ns (%d)", before);
        c_.that(what, std::abs(before - 30951) < 10);
        std::snprintf(what, sizeof what,
                      "[det cross] past +Ps/2 the window phase re-folds to the short way, -Ps/2 + 100 ns (%d)", after);
        c_.that(what, std::abs(after + 30951) < 10);
    }

    void case_range() {
        const struct { int64_t d; bool sampled; } pts[] = {
            {33554431, true}, {-33554431, true}, {33554432, false}, {-33554432, false}};
        for (const auto& p : pts) {
            unsigned most = 0;
            bool eng = false;
            sample_ = [p](long) { return p.d; };
            reset();
            while (windows_ < 4) {
                step_cycle();
                if (wcount() > most) most = wcount();
                if (engaged()) eng = true;
            }
            char what[200];
            if (p.sampled) {
                std::snprintf(what, sizeof what, "[det range] d = %lld ns, inside +/-2^25 ns, is sampled (%u a window)",
                              static_cast<long long>(p.d), most);
                c_.that(what, most >= 255 && eng);
            } else {
                std::snprintf(what, sizeof what,
                              "[det range] a timestamp 2^25 ns from the domain event is not sampled (d = %lld ns: %u a window)",
                              static_cast<long long>(p.d), most);
                c_.that(what, most == 0 && !eng);
            }
        }
    }

    //! one hold condition, raised so that ph_hold_w is high on the edge `off`
    //! cycles after the window's closing edge (T0); returns the committed
    //! phase contribution of the correction that boundary starts
    enum class Hold { mr, disabled, history, state, step, slew };
    void raise(Hold h, bool on) {
        switch (h) {
            case Hold::mr: d_->ref_restart_p_i = on; break;
            case Hold::disabled: d_->ph_en_i = !on; break;
            case Hold::history: d_->ref_rate_valid_i = !on; break;
            case Hold::state: acquire_now_ = on; break;
            case Hold::step: if (on) ptp_step_ = 10000; break;
            case Hold::slew: d_->phc_slew_active_i = on; break;
        }
    }
    //! the cycles from raising a hold to ph_hold_w reading it
    int lead(Hold h) {
        sample_ = [](long) { return 500; };
        reset();
        windows(3);
        for (int i = 0; i < 100; i++) step_cycle();
        int n = 0;
        raise(h, true);
        // the hold is judged before the edge: ph_hold_w as the edge sees it,
        // the inputs of this cycle settled first
        while (n < 16) {
            if (h == Hold::state) R(state_r) = acquire_now_ ? 3 : 4;
            d_->eval();
            const bool held = R(ph_hold_w);
            if (held) break;
            step_cycle();
            raise(h, false);
            n++;
        }
        raise(h, false);
        return n;
    }
    int64_t snap_one(Hold h, int off, int ld) {
        sample_ = [](long) { return 500; };
        reset();
        windows(5);
        // find the next closing edge: tick_cnt_r reaches 511 one tick before it
        while (!(R(tick_p_w) && R(win_valid_r) && R(tick_cnt_r) == 510)) step_cycle();
        step_cycle();
        const uint64_t t0 = cyc_ + 31;            // the tick period is 32 cycles
        const uint64_t at = t0 + off - ld;
        while (cyc_ < at) step_cycle();
        const int64_t i0 = integ();
        raise(h, true);
        step_cycle();
        raise(h, false);
        int32_t ew = 0;
        bool committed = false;
        uint8_t seq_prev = R(pp_seq_r);
        for (int i = 0; i < 40; i++) {
            step_cycle();
            const uint8_t sq = R(pp_seq_r);
            if (sq == 0 && seq_prev == 7 && R(pp_run_r) && !committed) {
                committed = true;
                ew = static_cast<int32_t>(R(ew_r));
            }
            seq_prev = sq;
        }
        if (!committed) return integ() - i0;
        return integ() - i0 - static_cast<int64_t>(ew) * 128;
    }
    void case_snap() {
        const struct { Hold h; const char* name; } holds[] = {
            {Hold::mr, "mr"}, {Hold::disabled, "term disabled"}, {Hold::history, "broken history"},
            {Hold::state, "not LOCKED"}, {Hold::step, "PHC step"}, {Hold::slew, "slew level"}};
        // the steady correction: 1,500 units of phase, under the clamp, times 2
        const int64_t full = 2 * 1500;
        for (const auto& hd : holds) {
            const int ld = lead(hd.h);
            for (int off = -1; off <= 1; off++) {
                const int64_t got = snap_one(hd.h, off, ld);
                const int64_t want = (off < 1) ? 0 : full;
                char what[220];
                std::snprintf(what, sizeof what,
                              "[det snap] %s %s the closing edge: committed phase contribution %lld/256 (want %lld)",
                              hd.name, off < 0 ? "one cycle before" : off == 0 ? "on" : "one cycle after",
                              static_cast<long long>(got), static_cast<long long>(want));
                c_.that(what, got == want);
            }
        }
    }

    Vdet_servo* d_;
    milan::tb::Checker& c_;
    std::function<int64_t(long)> sample_ = [](long) { return 0; };
    uint64_t cyc_ = 0;
    long pdu_ = 0;
    unsigned windows_ = 0;
    int full_run_ = 0;
    bool closing_full_ = false;
    int settle_rise_full_ = -1;
    bool bad_mirror_ = false;
    bool acquire_now_ = false;
    uint64_t ptp_step_ = 0;
    uint64_t lcg_ = 0x632764ULL;
};

int DetHarness::run(const std::string& name) {
    std::printf("[det %s] the phase detector alone, 256 PDUs a window\n", name.c_str());
    if (name == "inband") case_inband();
    else if (name == "events") case_events();
    else if (name == "meanin") case_meanin();
    else if (name == "balanced") half_period("balanced", [](long k) { return (k & 1) ? -10416 : 10416; });
    else if (name == "unbal129") half_period("unbal129", [](long k) { return (k % 256) < 129 ? 10416 : -10416; });
    else if (name == "unbal160") half_period("unbal160", [](long k) { return (k % 256) < 160 ? 10416 : -10416; });
    else if (name == "jitter") {
        half_period("jitter", [this](long) {
            lcg_ = lcg_ * 6364136223846793005ULL + 1442695040888963407ULL;
            const int64_t j = static_cast<int64_t>((lcg_ >> 33) % 121) - 60;
            return static_cast<int64_t>(std::llround(kPsNs / 2 - 20.0)) + j;
        });
    } else if (name == "cross") case_cross();
    else if (name == "range") case_range();
    else if (name == "snap") case_snap();
    else c_.fail("unknown case");
    return c_.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    std::string name = "inband";
    for (int i = 1; i < argc; i++)
        if (std::strncmp(argv[i], "+case=", 6) == 0) name = argv[i] + 6;
    const milan::tb::Model<Vdet_servo> model;
    milan::tb::Checker check{("media_phase det " + name).c_str()};
    check.echo_passes();
    DetHarness harness(model.get(), check);
    return harness.run(name);
}

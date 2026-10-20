// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The media-clock phase loop, closed at the silicon 512 ms window (#632,
// #764): media_phase_wrap.sv (the real KL_crf_rx, KL_mmcm_drp_servo,
// KL_media_domain_event and the phased KL_crf_tx) against the behavioural
// MMCM of tb/verilator/mmcm_servo (16.9 ps fine-phase steps, the silicon
// plant gain), a free-running local oscillator under the audio clock, and a
// CRF talker on an exact 2 ms grid of gPTP time, as at the bench.
//
// The grade is the PHYSICS, not the servo's own view: the harness knows the
// instant of every frame of the DUT's frame grid (the audio edge that starts
// it) and every timing point of the followed stream, so the phase it grades
// is fold(frame instant - CRF timing point) in [-Ps/2, Ps/2), Ps = 1e9/48000
// ns, against IEEE 1722-2016 10.8 Eq. 15's +/-5 % of Ps. The frame instant is
// read in the DUT's own gPTP timescale (its PHC), the one its timestamps are
// in; only the slew case moves that off the harness's time. The DUT's own CRF
// output is graded the same way, and against its own frame instants (4.3.5:
// whole periods). One case per process (+case=<name>):
//
//   engage    an arbitrary engagement phase, 0.47 Ps (near the fold), pulled
//             the short way into +/-5 % and held; the pull is slew-limited
//   engage2   the same from -0.33 Ps
//   step      a reference phase step of 0.37 Ps (a CRF timestamp jump),
//             re-acquired and held
//   ramp      a local-oscillator ramp of 4 ppm over 80 s, held throughout
//   holdover  a 15 s holdover (the reference silent, the oscillator moving),
//             re-acquired after the return and held
//   internal  re-engagement through INTERNAL (servo IDLE for 15 s),
//             re-acquired and held
//   mr        the followed stream toggles mr with a 1.8 us jump (inside the
//             receiver's jump bound), re-acquired and held
//   slew      the local PHC slews 27 us at 200 ppm under the #545 slew level:
//             re-acquired the short way (6.2 us, not the 27 us the slew
//             moved) and held
//   burst     the talker sends 4 % faster than its declared interval for
//             one window, its timestamps still on its grid: the window keeps
//             264 samples, the cap, so its phase cannot wrap, and the phase
//             is held
//
// Each event case also requires the phase term to let go at the event (the
// engaged bit, phase_o[20], low on some datapath cycle shortly after it):
// the hold conditions are graded one by one.
//   carry     the phase term off: the integrator carries every odd error
//             exactly (#764's floor leak), and the phase does not walk
//
// Mutants: phase_mutants.py plants one defect per loop term and requires the
// named check to fail.

#include "Vmedia_phase_wrap.h"
#include "Vmedia_phase_wrap___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr double kPsNs = 1e9 / 48000.0;           //!< the sample period
constexpr double kBandNs = 0.05 * kPsNs;           //!< 10.8 Eq. 15
constexpr double kClkHz = 3.125e6;                 //!< media_phase_wrap default
constexpr double kAudHz = 768e3;
//! a local crystal 3.7 ppm slow under clk_i, so PHC samples land on every
//! nanosecond phase (the integrator carry needs odd errors to exist)
constexpr double kHalfIFs = 0.5 * 1e15 / kClkHz * (1.0 + 3.7e-6);
constexpr double kHalfANomFs = 0.5 * 1e15 / kAudHz;
constexpr double kWindowS = 0.512;
constexpr double kMttNs = 2e6;                     //!< 96 periods exactly

//! fold into [-Ps/2, Ps/2)
double fold(double x) {
    double r = std::fmod(x, kPsNs);
    if (r < 0) r += kPsNs;
    if (r >= kPsNs / 2) r -= kPsNs;
    return r;
}

struct Scenario {
    const char* name = "";
    double phi0_ps = 0.0;        //!< the reference's phase against the DUT grid, Ps
    double lo_ppm = 8.0;         //!< the free-running audio clock, + = fast
    bool ph_en = true;
    double end_s = 60.0;
};

class MediaPhaseHarness {
 public:
    MediaPhaseHarness(Vmedia_phase_wrap* dut, milan::tb::Checker& check)
        : dut_(dut), check_(check) {}

    int run(const std::string& name);

 private:
    // ---------------------------------------------------------------- clocks
    void tick_one() {
        if (next_i_ <= next_a_) {
            t_fs_ = next_i_;
            next_i_ += kHalfIFs;
            dut_->clk_i ^= 1;
            if (dut_->clk_i) {
                dut_->ptp_now_i = static_cast<uint64_t>(t_fs_ / 1e6 + phc_offset_ns());
                dut_->phc_slew_i = now_s() >= slew_t0_ && now_s() <= slew_t1_;
                drive_reference();
            }
            dut_->eval();
            if (dut_->clk_i) {
                mm_.dclk_edge(dut_->drp_addr_o, dut_->drp_en_o, dut_->drp_we_o,
                              dut_->drp_di_o, dut_->mmcm_rst_o);
                dut_->drp_do_i = mm_.dout;
                dut_->drp_rdy_i = mm_.drdy;
                dut_->mmcm_locked_i = mm_.locked;
                mm_.psclk_edge(dut_->ps_en_o, dut_->ps_incdec_o, dut_->mmcm_rst_o);
                dut_->ps_done_i = mm_.psdone;
                observe_clk();
            }
        } else {
            t_fs_ = next_a_;
            const double half = kHalfANomFs / (1.0 + lo_ppm_now() * 1e-6);
            base_a_ += half;
            next_a_ = base_a_ + mm_.audio_adj_fs;
            if (next_a_ <= t_fs_) next_a_ = t_fs_ + 1e3;
            dut_->clk_audio_i ^= 1;
            const bool was = dut_->frame_a_o;
            dut_->eval();
            if (dut_->clk_audio_i && dut_->frame_a_o && !was) frame_edge();
        }
    }
    void run_to(double s) {
        const double te = s * 1e15;
        while (t_fs_ < te) tick_one();
    }
    double now_s() const { return t_fs_ * 1e-15; }
    //! the local PHC against the harness's time: a linear slew between two
    //! instants (#545), zero before it
    double phc_offset_ns() const {
        const double t = now_s();
        if (t <= slew_t0_) return 0.0;
        if (t >= slew_t1_) return slew_ns_;
        return slew_ns_ * (t - slew_t0_) / (slew_t1_ - slew_t0_);
    }

    //! the oscillator: base offset plus a linear ramp between two instants
    double lo_ppm_now() const {
        const double t = now_s();
        if (t <= ramp_t0_) return lo_ppm_;
        if (t >= ramp_t1_) return lo_ppm_ + ramp_ppm_;
        return lo_ppm_ + ramp_ppm_ * (t - ramp_t0_) / (ramp_t1_ - ramp_t0_);
    }

    // ------------------------------------------------------- the reference
    //! PDU j: source instant ref_t0 + j * 2 ms of gPTP time, timestamp that
    //! plus the 2 ms Max Transit Time (96 periods, Eq. 14), arriving 30 us
    //! after its source instant plus up to 4 us of jitter
    void drive_reference() {
        dut_->frame_p_i = 0;
        const double t_ns = t_fs_ / 1e6;
        if (t_ns < ref_next_send_ns_) return;
        const double src = ref_t0_ns_ + static_cast<double>(ref_j_) * 2e6;
        ref_j_++;
        ref_next_send_ns_ = ref_t0_ns_ + static_cast<double>(ref_j_) * 2e6 + 30e3 + jitter_ns();
        //! a burst sends the next PDU 1.92 ms after this one whatever its
        //! timestamp; afterwards the talker waits for its grid again
        if (now_s() >= burst_t0_ && now_s() < burst_t1_) {
            ref_next_send_ns_ = t_ns + 1.92e6;
            burst_sent_.push_back(now_s());
        }
        if (!ref_on_) return;
        dut_->frame_p_i = 1;
        dut_->ts_ns_i = static_cast<uint64_t>(std::llround(src + kMttNs));
        dut_->seq_i = static_cast<uint8_t>(ref_seq_++);
        dut_->mr_i = ref_mr_;
    }
    double jitter_ns() {
        lcg_ = lcg_ * 6364136223846793005ULL + 1442695040888963407ULL;
        return static_cast<double>((lcg_ >> 33) % 4000);
    }
    //! the reference's phase step: its grid moves by d ns from the next PDU
    void step_reference(double d_ns) {
        ref_t0_ns_ += d_ns;
        ref_next_send_ns_ += d_ns;
    }

    // ------------------------------------------------------- observation
    void frame_edge() {
        last_frame_ns_ = t_fs_ / 1e6 + phc_offset_ns();
        frame_ns_.push_back(last_frame_ns_);
        if (frame_ns_.size() > 4096) frame_ns_.erase(frame_ns_.begin(), frame_ns_.begin() + 2048);
    }
    //! the true phase: the latest frame instant against the reference grid
    double true_phase() const { return fold(last_frame_ns_ - ref_t0_ns_); }

    void observe_clk() {
        // the hold: the phase term must let go at each event that holds it
        if (now_s() >= letgo_from_ && now_s() <= letgo_until_ && !engaged()) letgo_seen_ = true;
        // the most samples any window kept (phase_o[31:23])
        const unsigned wcnt = (dut_->phase_o >> 23) & 0x1FF;
        if (wcnt > max_wcnt_) max_wcnt_ = wcnt;
        // the DUT's CRF output frames: 8 beats, timestamp at frame bytes 34..41
        if (dut_->crft_tvalid_o) {
            const uint64_t d = dut_->crft_tdata_o;
            for (int l = 0; l < 8; l++) crf_bytes_.push_back(static_cast<uint8_t>(d >> (8 * l)));
            if (dut_->crft_tlast_o) {
                if (crf_bytes_.size() >= 42) {
                    uint64_t ts = 0;
                    for (int k = 34; k < 42; k++) ts = (ts << 8) | crf_bytes_[k];
                    crf_out(ts);
                }
                crf_bytes_.clear();
            }
        }
        // a window boundary: sample the true phase once per servo window
        if (now_s() >= next_win_s_) {
            next_win_s_ += kWindowS;
            window_sample();
        }
    }

    //! one DUT CRF output timestamp: its instant (minus the 2 ms offset) must
    //! be one of the DUT's own frame instants (4.3.5) to the marker's
    //! back-dating, and, while the case grades, on the reference's grid
    void crf_out(uint64_t ts) {
        const double inst = static_cast<double>(ts) - kMttNs;
        double best = 1e18;
        for (auto it = frame_ns_.rbegin(); it != frame_ns_.rend() && it - frame_ns_.rbegin() < 200; ++it)
            best = std::min(best, std::fabs(inst - *it));
        crf_n_++;
        if (crf_n_ > 4 && best > max_crf_vs_frame_ns_) max_crf_vs_frame_ns_ = best;
        if (grading_) {
            const double p = std::fabs(fold(inst - ref_t0_ns_));
            if (p > max_crf_vs_ref_ns_) max_crf_vs_ref_ns_ = p;
        }
    }

    void window_sample() {
        const double p = true_phase();
        locked_windows_ = locked() ? locked_windows_ + 1 : 0;
        //! the slew limit is graded once the rate loop's own tail has gone
        //! (its pole is 0.71 a window): what moves the phase then is the term
        if (have_prev_ && locked_windows_ >= 6 && pull_watch_) {
            const double dp = std::fabs(fold(p - prev_phase_));
            if (dp > max_pull_ns_) max_pull_ns_ = dp;
        }
        //! the engagement phase, and the short way from it
        const bool engaged = (dut_->phase_o >> 20) & 1;
        if (engaged && !have_eng_) {
            have_eng_ = true;
            eng_phase_ = p;
        }
        if (have_eng_ && pull_watch_ && std::fabs(p) > max_after_eng_) max_after_eng_ = std::fabs(p);
        prev_phase_ = p;
        have_prev_ = true;
        if (grading_) {
            if (std::fabs(p) > max_held_ns_) max_held_ns_ = std::fabs(p);
        }
        if (verbose_)
            std::printf("  t=%7.2f s state=%d phase=%9.1f ns (%+.4f Ps) dut=%9.1f ns eng=%d set=%d trim=%+.3f ppm\n",
                        now_s(), state(), p, p / kPsNs, dut_phase_ns(),
                        static_cast<int>((dut_->phase_o >> 20) & 1),
                        static_cast<int>((dut_->phase_o >> 21) & 1),
                        static_cast<int16_t>(dut_->status_o >> 16) / 16.0);
    }

    int state() const { return static_cast<int>(dut_->status_o & 7); }
    bool engaged() const { return ((dut_->phase_o >> 20) & 1) != 0; }
    //! watch the engaged bit from now for `within_s`: an event that holds the
    //! phase term must make it let go, observed on every datapath cycle
    void watch_letgo(double within_s) {
        letgo_from_ = now_s();
        letgo_until_ = now_s() + within_s;
        letgo_seen_ = false;
        engaged_before_ = engaged();
    }
    void check_letgo(const char* tag, const char* event) {
        char what[160];
        std::snprintf(what, sizeof what, "[%s] the phase term let go at %s (within %.0f ms)", tag, event,
                      (letgo_until_ - letgo_from_) * 1e3);
        check_.that(what, engaged_before_ && letgo_seen_);
    }
    bool locked() const { return state() == 4; }
    double dut_phase_ns() const {
        int32_t v = static_cast<int32_t>(dut_->phase_o & 0xFFFFF);
        if (v & 0x80000) v -= 0x100000;
        return v / 3.0;
    }

    //! run until the true phase has been inside the band for `hold_s`
    //! running, or `bound_s` has passed; return the instant it entered
    double settle(double bound_s, double hold_s) {
        double in_since = -1;
        const double te = now_s() + bound_s;
        while (now_s() < te) {
            run_to(now_s() + 0.064);
            const bool in = std::fabs(true_phase()) < kBandNs;
            if (in && in_since < 0) in_since = now_s();
            if (!in) in_since = -1;
            if (in_since >= 0 && now_s() - in_since >= hold_s) return in_since;
        }
        return -1;
    }

    //! the common grade after an event at `t_event`: inside the band within
    //! `bound_s`, then held to the case's end with the DUT's CRF output on
    //! the reference's grid too
    void grade_reacquired(const char* tag, double t_event, double bound_s, double end_s) {
        const double t_in = settle(bound_s, 4.0);
        char what[160];
        std::snprintf(what, sizeof what, "[%s] phase inside +/-5 %% of Ps within %.0f s of the event", tag, bound_s);
        check_.that(what, t_in >= 0);
        if (t_in >= 0)
            std::printf("  info: [%s] inside the band %.2f s after the event\n", tag, t_in - t_event);
        grading_ = true;
        max_held_ns_ = 0;
        max_crf_vs_ref_ns_ = 0;
        run_to(end_s);
        grading_ = false;
        std::snprintf(what, sizeof what, "[%s] phase held inside +/-5 %% of Ps to the end (max %.1f ns)", tag, max_held_ns_);
        check_.that(what, max_held_ns_ < kBandNs);
        std::snprintf(what, sizeof what, "[%s] the DUT's CRF output on the reference's grid (max %.1f ns)", tag, max_crf_vs_ref_ns_);
        check_.that(what, max_crf_vs_ref_ns_ < kBandNs && crf_n_ > 0);
        std::snprintf(what, sizeof what, "[%s] the servo reports settled at the end", tag);
        check_.that(what, (dut_->phase_o >> 21) & 1);
        std::snprintf(what, sizeof what, "[%s] still LOCKED at the end", tag);
        check_.that(what, locked());
    }

    void common_checks(const char* tag) {
        char what[160];
        std::snprintf(what, sizeof what,
                      "[%s] every DUT CRF timestamp is a frame instant of its own grid (max %.1f ns)",
                      tag, max_crf_vs_frame_ns_);
        check_.that(what, crf_n_ > 10 && max_crf_vs_frame_ns_ < 0.01 * kPsNs);
        std::snprintf(what, sizeof what, "[%s] fine-PS protocol clean", tag);
        check_.that(what, mm_.ps_viol == 0 && mm_.ps_during_drp_rst == 0);
    }

    //! the reference's grid is placed against the DUT's first frame, so the
    //! true phase starts at phi0 (the reference sends from 100 periods on)
    void start(const Scenario& s) {
        lo_ppm_ = s.lo_ppm;
        ref_t0_ns_ = 1e18;
        ref_next_send_ns_ = 1e18;
        mm_.regs[0x08] = 0x0595;
        mm_.regs[0x09] = 0x0080;
        mm_.ps_lat = 2;
        dut_->rst_n = 0;
        dut_->sel_i = 0;
        dut_->ph_en_i = s.ph_en;
        dut_->phc_slew_i = 0;
        dut_->mmcm_locked_i = 1;
        run_to(0.001);
        dut_->rst_n = 1;
        while (frame_ns_.empty()) tick_one();
        ref_t0_ns_ = frame_ns_.front() - s.phi0_ps * kPsNs + 100.0 * kPsNs;
        ref_next_send_ns_ = ref_t0_ns_ + 30e3;
        run_to(0.2);
        dut_->sel_i = 1;
    }

    // ---------------------------------------------------------------- cases
    //! a small oscillator offset, so the engagement lands near phi0 and the
    //! case controls where in the period it starts
    void case_engage(double phi0, const char* tag) {
        Scenario s; s.phi0_ps = phi0; s.lo_ppm = 0.3;
        start(s);
        pull_watch_ = true;
        verbose_ = true;
        grade_reacquired(tag, 0.2, 45.0, 60.0);
        char what[160];
        std::snprintf(what, sizeof what, "[%s] engaged %+.4f Ps from the reference's grid", tag, eng_phase_ / kPsNs);
        check_.that(what, have_eng_ && std::fabs(eng_phase_) > 0.3 * kPsNs);
        //! the clamp's 256 ns per window, plus the rate loop's own window noise
        //! at this harness's 320 ns PHC sampling (about 80 ns); the unclamped
        //! term pulls Theta / 64 ns, 488 ns per window from Ps/2
        std::snprintf(what, sizeof what, "[%s] the pull is slew-limited: <= 400 ns of phase per window (max %.1f)", tag, max_pull_ns_);
        check_.that(what, max_pull_ns_ <= 400.0);
        std::snprintf(what, sizeof what, "[%s] the pull went the short way (max |phase| %.4f Ps after engaging)", tag, max_after_eng_ / kPsNs);
        check_.that(what, max_after_eng_ <= std::fabs(eng_phase_) + kBandNs);
        common_checks(tag);
    }

    //! the event cases start engaged: a small offset and a phase already
    //! inside the band, so the event at 15 s finds the loop settled
    void start_settled() {
        Scenario s; s.phi0_ps = 0.02; s.lo_ppm = 0.3;
        start(s);
        verbose_ = true;
        grade_reacquired("pre", 0.2, 14.0, 15.0);
    }

    void case_step() {
        start_settled();
        watch_letgo(0.010);
        step_reference(0.37 * kPsNs);
        std::printf("  info: [step] the reference stepped by 0.37 Ps at %.2f s\n", now_s());
        grade_reacquired("step", now_s(), 35.0, 60.0);
        check_letgo("step", "the reference's history restart");
        common_checks("step");
    }

    void case_ramp() {
        start_settled();
        ramp_t0_ = 15.0; ramp_t1_ = 95.0; ramp_ppm_ = 4.0;
        grading_ = true;
        max_held_ns_ = 0;
        max_crf_vs_ref_ns_ = 0;
        run_to(100.0);
        grading_ = false;
        char what[160];
        std::snprintf(what, sizeof what, "[ramp] phase held inside +/-5 %% of Ps through a 4 ppm ramp (max %.1f ns)", max_held_ns_);
        check_.that(what, max_held_ns_ < kBandNs);
        std::snprintf(what, sizeof what, "[ramp] the DUT's CRF output on the reference's grid (max %.1f ns)", max_crf_vs_ref_ns_);
        check_.that(what, max_crf_vs_ref_ns_ < kBandNs);
        check_.that("[ramp] still LOCKED", locked());
        common_checks("ramp");
    }

    void case_holdover() {
        start_settled();
        watch_letgo(0.200);
        ref_on_ = false;
        lo_ppm_ += 0.5;                  // the oscillator moves while held
        run_to(16.0);
        check_.that("[holdover] the servo holds over while the reference is silent", state() == 5);
        run_to(30.0);
        ref_on_ = true;
        std::printf("  info: [holdover] the reference returns at %.2f s, phase %+.4f Ps\n",
                    now_s(), true_phase() / kPsNs);
        grade_reacquired("holdover", now_s(), 40.0, 80.0);
        check_letgo("holdover", "HOLDOVER");
        common_checks("holdover");
    }

    //! INTERNAL clears the trim, so the audio clock free-runs at the
    //! oscillator's 8 ppm for 15 s (5.8 periods) and re-engages anywhere
    void case_internal() {
        start_settled();
        watch_letgo(0.005);
        dut_->sel_i = 0;
        lo_ppm_ = 8.0;
        run_to(16.0);
        check_.that("[internal] INTERNAL idles the servo", state() == 0);
        run_to(30.0);
        dut_->sel_i = 1;
        std::printf("  info: [internal] CRF selected again at %.2f s, phase %+.4f Ps\n",
                    now_s(), true_phase() / kPsNs);
        grade_reacquired("internal", now_s(), 45.0, 85.0);
        check_letgo("internal", "INTERNAL");
        common_checks("internal");
    }

    void case_mr() {
        start_settled();
        watch_letgo(0.005);
        ref_mr_ = !ref_mr_;
        step_reference(1800.0);
        std::printf("  info: [mr] mr toggled with a 1.8 us jump at %.2f s\n", now_s());
        grade_reacquired("mr", now_s(), 30.0, 55.0);
        check_letgo("mr", "the mr toggle");
        common_checks("mr");
    }

    //! a policy slew of the local PHC (#545): the DUT's timescale moves 27 us
    //! under the reference, so its frames must move 27 us mod Ps = 6.2 us.
    //! The term lets go while the slew level is up and re-acquires the short
    //! way from the folded phase
    void case_slew() {
        start_settled();
        slew_ns_ = 27000.0;
        slew_t0_ = now_s();
        slew_t1_ = slew_t0_ + slew_ns_ * 1e-9 / 200e-6;
        watch_letgo(0.005);
        std::printf("  info: [slew] the local PHC slews +27 us at 200 ppm from %.2f s\n", now_s());
        run_to(slew_t1_ + 0.002);
        have_eng_ = true;
        eng_phase_ = true_phase();
        max_after_eng_ = 0;
        pull_watch_ = true;
        std::printf("  info: [slew] phase %+.4f Ps when the slew ends\n", eng_phase_ / kPsNs);
        grade_reacquired("slew", slew_t0_, 40.0, 70.0);
        char what[160];
        std::snprintf(what, sizeof what, "[slew] the pull went the short way (max |phase| %.4f Ps after the slew)",
                      max_after_eng_ / kPsNs);
        check_.that(what, max_after_eng_ <= std::fabs(eng_phase_) + kBandNs);
        check_letgo("slew", "the slew level");
        common_checks("slew");
    }

    //! a talker sending 4 % faster than its declared timestamp_interval, its
    //! timestamps still 2 ms apart on its grid (so the phase each sample
    //! reads is unchanged): about 266 PDUs land in a 512 ms window.
    //! The window keeps at most 264 (the nominal 256 plus 1/32), so its
    //! phase, the sum over 256, stays inside 33/32 of Ps/2 and cannot wrap
    void case_burst() {
        start_settled();
        //! from a servo window boundary for 0.6 s, so one whole window lies
        //! inside the burst while its timestamps (80 us further ahead each
        //! PDU) stay inside the detector's 33.5 ms fold range
        auto* r = dut_->rootp;
        const uint64_t w0 = r->media_phase_wrap__DOT__servo__DOT__win_start_r;
        while (r->media_phase_wrap__DOT__servo__DOT__win_start_r == w0) tick_one();
        burst_t0_ = now_s();
        burst_t1_ = burst_t0_ + 0.6;
        max_wcnt_ = 0;
        std::printf("  info: [burst] the talker sends every 1.92 ms from %.2f s for 0.6 s\n", now_s());
        grade_reacquired("burst", now_s(), 30.0, 45.0);
        size_t most = 0;
        for (size_t i = 0, j = 0; j < burst_sent_.size(); j++) {
            while (burst_sent_[j] - burst_sent_[i] >= kWindowS) i++;
            most = std::max(most, j - i + 1);
        }
        char what[160];
        std::snprintf(what, sizeof what, "[burst] the burst put more than 264 PDUs in some 512 ms (%zu)", most);
        check_.that(what, most > 264);
        std::snprintf(what, sizeof what, "[burst] the window the burst filled kept exactly 264 samples, the cap (max %u)",
                      max_wcnt_);
        check_.that(what, max_wcnt_ == 264);
        common_checks("burst");
    }

    //! the phase term off (AAF following leaves it off): the integrator must
    //! carry every odd error exactly, so over N committed windows it moves by
    //! exactly sum(e) / 2^KI_SHIFT_P; the floored form drops every odd LSB
    void case_carry() {
        Scenario s; s.phi0_ps = 0.25; s.ph_en = false; s.lo_ppm = 0.3;
        start(s);
        verbose_ = false;
        run_to(10.0);
        check_.that("[carry] LOCKED on rate alone", locked());
        auto* r = dut_->rootp;
        const auto ix = [r]() -> int64_t {
            int32_t i = static_cast<int32_t>(r->media_phase_wrap__DOT__servo__DOT__integ_r << 8) >> 8;
            return static_cast<int64_t>(i) * 256 + r->media_phase_wrap__DOT__servo__DOT__integ_frac_r;
        };
        const int64_t ix0 = ix();
        int64_t sum_e = 0;
        int odd = 0;
        int windows = 0;
        const double te = now_s() + 40 * kWindowS;
        uint8_t seq_prev = r->media_phase_wrap__DOT__servo__DOT__pp_seq_r;
        while (now_s() < te) {
            tick_one();
            const uint8_t sq = r->media_phase_wrap__DOT__servo__DOT__pp_seq_r;
            if (sq == 0 && seq_prev == 7 && r->media_phase_wrap__DOT__servo__DOT__pp_run_r) {
                const int32_t e = static_cast<int32_t>(r->media_phase_wrap__DOT__servo__DOT__ew_r);
                sum_e += e;
                if (e & 1) odd++;
                windows++;
            }
            seq_prev = sq;
        }
        const int64_t ix1 = ix();
        std::printf("  info: [carry] %d windows, %d odd errors, sum(e) %lld, integrator moved %lld/256\n",
                    windows, odd, static_cast<long long>(sum_e), static_cast<long long>(ix1 - ix0));
        check_.that("[carry] the window sample is wide enough to grade (odd errors seen)", odd >= 5);
        check_.that("[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)",
                    ix1 - ix0 == sum_e * 128);
        check_.that("[carry] the phase term stayed off (never engaged)",
                    !((dut_->phase_o >> 20) & 1));
        common_checks("carry");
    }

    Vmedia_phase_wrap* dut_;
    milan::tb::Checker& check_;
    MmcmModel mm_{};
    double t_fs_ = 0;
    double next_i_ = kHalfIFs;
    double next_a_ = kHalfANomFs;
    double base_a_ = kHalfANomFs;
    double slew_t0_ = 1e9;
    double slew_t1_ = 1e9;
    double slew_ns_ = 0;
    double burst_t0_ = 1e9;
    double burst_t1_ = 1e9;
    std::vector<double> burst_sent_;
    unsigned max_wcnt_ = 0;
    double lo_ppm_ = 8.0;
    double ramp_t0_ = 1e9;
    double ramp_t1_ = 2e9;
    double ramp_ppm_ = 0;
    double ref_t0_ns_ = 0;
    double ref_next_send_ns_ = 0;
    long ref_j_ = 0;
    unsigned ref_seq_ = 0;
    bool ref_on_ = true;
    bool ref_mr_ = false;
    uint64_t lcg_ = 0x632764ULL;
    double last_frame_ns_ = 0;
    std::vector<double> frame_ns_;
    std::vector<uint8_t> crf_bytes_;
    long crf_n_ = 0;
    double max_crf_vs_frame_ns_ = 0;
    double max_crf_vs_ref_ns_ = 0;
    double max_held_ns_ = 0;
    double max_pull_ns_ = 0;
    double next_win_s_ = kWindowS;
    double prev_phase_ = 0;
    bool have_prev_ = false;
    bool grading_ = false;
    bool pull_watch_ = false;
    bool verbose_ = false;
    bool have_eng_ = false;
    double letgo_from_ = 1e9;
    double letgo_until_ = 0;
    bool letgo_seen_ = false;
    bool engaged_before_ = false;
    double eng_phase_ = 0;
    double max_after_eng_ = 0;
    int locked_windows_ = 0;
};

int MediaPhaseHarness::run(const std::string& name) {
    std::printf("[%s] media-clock phase loop, silicon window, clk %.3f MHz, audio %.0f kHz\n",
                name.c_str(), kClkHz / 1e6, kAudHz / 1e3);
    if (name == "engage") case_engage(0.47, "engage");
    else if (name == "engage2") case_engage(-0.33, "engage2");
    else if (name == "step") case_step();
    else if (name == "ramp") case_ramp();
    else if (name == "holdover") case_holdover();
    else if (name == "internal") case_internal();
    else if (name == "mr") case_mr();
    else if (name == "slew") case_slew();
    else if (name == "burst") case_burst();
    else if (name == "carry") case_carry();
    else check_.fail("unknown case");
    return check_.report();
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    std::string name = "engage";
    for (int i = 1; i < argc; i++)
        if (std::strncmp(argv[i], "+case=", 6) == 0) name = argv[i] + 6;
    const milan::tb::Model<Vmedia_phase_wrap> model;
    milan::tb::Checker check{("media_phase " + name).c_str()};
    check.echo_passes();
    MediaPhaseHarness harness(model.get(), check);
    return harness.run(name);
}

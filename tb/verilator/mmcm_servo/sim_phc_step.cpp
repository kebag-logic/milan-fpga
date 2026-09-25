// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_mmcm_drp_servo against a PHC step, at the SILICON window scale (#539).
//
// The unit harness (sim_main.cpp) compresses the window to 4 ms and scales the
// error back up by NORM_SHIFT_P = 7, so a step there is amplified 128 times and
// the 2^19 guard sits near a 4 us step. This harness runs the servo with its
// DEFAULT parameters, the ones the datapath elaborates: a 1 ms tick of 24576
// audio cycles, a 512-tick window, NOM_WIN_NS_P = 512 ms and NORM_SHIFT_P = 0.
// A PHC step of S ns inside one window is then exactly S units of window error
// (1 ppm = 512 units), which is the arithmetic #539 reads.
//
// Cases (no argument):
//   P0  lock at the silicon scale against a +20 ppm talker
//   P1  a step at mid-window, 21 us to 1 s, both signs: counted once, the next
//       window commits clean, integrator and written rate held, LOCKED held
//   P2  the step staged on the boundary sample (that window is squashed), one
//       edge after it (the closed window commits, the new one is abandoned),
//       one edge before it (the window is re-based instead of closing); each
//       arm first asserts it landed where it claims
//   P3  a guard discard and a step on ONE cycle: both counted
//   P4  the rate path: a real talker rate change still reaches the integrator
//
// +slew_suite grades the #545 level and the 100 us / 200 ppm trajectory,
// both signs, a short within-window correction, a shared boundary sample,
// a clean pre-slew close, an indefinitely held correction, and PI resumption.
// +slew_control selects P0 and the +100 us case for the named mutants.
//
// Trace modes (the #539 records; lock, then one disturbance at mid-window,
// printed window by window):
//   +trace_step_ns=<n>        a PHC step of n ns (signed)
//   +trace_slew_ns=<n>        the plane's slew of n ns at 200 ppm
//   +trace_talker_step_ns=<n> the TALKER's step: KL_crf_rx rate_o carries n ns
//                             for its 256-PDU (512 ms) ring
//
// The integrator and the written rate are read through --public-flat-rw
// (integ_r, u_cmd_r, ew_r, pp_seq_r, pp_run_r, win_valid_r, ptp_jump_r and
// the tick synchroniser); nothing is written through it.

#include "VKL_mmcm_drp_servo.h"
#include "VKL_mmcm_drp_servo___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "mmcm_model.h"
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

namespace {

//! Silicon servo constants the checks are written against (the RTL defaults).
constexpr int kWinTicks = 512;           //! 2^WIN_LOG2_P
constexpr int32_t kLockThr = 1024;       //! LOCK_THR_P: 2 ppm in x512 units
constexpr int32_t kGuardThr = 1 << 19;   //! GUARD_THR_C: 1024 ppm
constexpr int kStateLocked = 4;
constexpr double kTalkerPpm = 20.0;
//! audio base: 24.576 MHz - 10.64 ppm (the integer two-stage MMCM plan)
constexpr double kBasePpm = -10.64;
//! P1: the #539 range, 100 us to 1 s, both signs, plus the 20 us link-up
//! step of the #387 policy and the 108 us edge of the legitimate envelope
constexpr std::array<int64_t, 11> kSweepNs = {
    21'000, 100'000, -100'000, 108'000, 150'000, -150'000,
    300'000, 524'000, 1'000'000, 1'000'000'000, -1'000'000'000};

//! One window, as the PI micro-sequence closed it.
struct WindowClose {
    int32_t ew;         //! normalized window error (ns per 512 ms)
    int32_t integ;      //! integrator after the writeback
    int32_t ucmd;       //! written rate command after the writeback
    bool committed;     //! pp_run_r at the writeback (false = discarded)
};

//! The loop state a step must leave alone.
struct Snapshot {
    int32_t integ;
    int32_t ucmd;
    int disc;
};

enum class Disturbance { phc_step, phc_slew, talker_step };

class PhcStepHarness {
 public:
    //! ps_half_fs: half the PSCLK period. The suite runs PSCLK at 50 MHz (its
    //! command stays under 56 ppm, the runner's ceiling there); the trace modes
    //! run the SoC's 200 MHz so a pre-fix record is never actuator-limited.
    explicit PhcStepHarness(double ps_half_fs) : half_p_(ps_half_fs) {
        check_.echo_passes();
    }

    int suite() {
        prove_lock_at_the_silicon_scale();
        std::printf("[P1] one PHC step at mid-window, per size\n");
        for (const int64_t s : kSweepNs) prove_step_leaves_the_loop_untouched(s);
        prove_step_on_the_boundary_sample_is_squashed();
        prove_step_after_the_boundary_commits_the_closed_window();
        prove_step_before_the_boundary_rebases_the_window();
        prove_coincident_discards_both_count();
        prove_rate_path_still_integrates();
        return check_.report();
    }

    int slew_control() {
        prove_lock_at_the_silicon_scale();
        prove_slew_holds(100'000);
        return check_.report();
    }

    int slew_suite() {
        prove_lock_at_the_silicon_scale();
        prove_slew_holds(100'000);
        prove_slew_holds(-100'000);
        prove_slew_holds(100);
        prove_slew_boundary();
        prove_clean_close_before_slew();
        prove_slew_stays_active();
        prove_rate_path_still_integrates();
        return check_.report();
    }

    int trace(Disturbance kind, int64_t amount_ns) {
        bring_up_and_lock();
        static constexpr std::array<const char*, 3> kNames = {
            "PHC step", "PHC slew at 200 ppm", "talker step (crf rate_o, 512 ms)"};
        std::printf("[TRACE] %s of %lld ns at mid-window, talker %+.1f ppm\n",
                    kNames.at(static_cast<size_t>(kind)),
                    static_cast<long long>(amount_ns), kTalkerPpm);
        print_row("locked", last_);
        run_to_tick(kWinTicks / 2);
        const int disc0 = disc_cnt();
        if (kind == Disturbance::phc_step) ptp_step_ns += static_cast<double>(amount_ns);
        if (kind == Disturbance::phc_slew) slew_left_ns_ = static_cast<double>(amount_ns);
        if (kind == Disturbance::talker_step) {
            dut->crf_rate_i = talker_rate_ + static_cast<int32_t>(amount_ns);
            talker_bias_until_fs_ = t_fs + 512e12;
        }
        std::printf("  applied at t=%.3f ms (tick %d of the window)\n",
                    t_fs * 1e-12, tick_cnt());
        for (int w = 1; w <= 5; w++) {
            const WindowClose c = run_to_window_close();
            char tag[32];
            std::snprintf(tag, sizeof tag, "close +%d", w);
            print_row(tag, c);
        }
        std::printf("  discards counted across the trace: %d\n", disc_cnt() - disc0);
        return 0;
    }

 private:
    // ---- observation --------------------------------------------------------
    //! Verilator keeps a 24-bit signed flop in a zero-extended 32-bit word.
    static int32_t sext24(uint32_t v) {
        return static_cast<int32_t>(v << 8) >> 8;
    }
    VKL_mmcm_drp_servo___024root* root() const { return dut->rootp; }
    int32_t integ() const { return sext24(root()->KL_mmcm_drp_servo__DOT__integ_r); }
    int32_t ucmd() const { return sext24(root()->KL_mmcm_drp_servo__DOT__u_cmd_r); }
    int32_t ew() const { return static_cast<int32_t>(root()->KL_mmcm_drp_servo__DOT__ew_r); }
    int pp_seq() const { return root()->KL_mmcm_drp_servo__DOT__pp_seq_r; }
    bool pp_run() const { return root()->KL_mmcm_drp_servo__DOT__pp_run_r != 0; }
    bool win_valid() const { return root()->KL_mmcm_drp_servo__DOT__win_valid_r != 0; }
    bool ptp_jump() const { return root()->KL_mmcm_drp_servo__DOT__ptp_jump_r != 0; }
    int tick_cnt() const { return root()->KL_mmcm_drp_servo__DOT__tick_cnt_r; }
    int state() const { return static_cast<int>(dut->status_o & 7); }
    int disc_cnt() const { return static_cast<int>((dut->status_o >> 10) & 0x3F); }
    int16_t trim() const { return static_cast<int16_t>(dut->status_o >> 16); }
    Snapshot snapshot() const { return Snapshot{integ(), ucmd(), disc_cnt()}; }

    //! clk_i edges until the next window boundary (T0), read off the tick
    //! synchroniser, where tick_p_w = sync[2] ^ sync[1]. 0 = not within two.
    //! (Three is never observable here: sync[0] captures the audio-side level
    //! on the very edge this harness observes after.)
    unsigned tick_sync() const {
        return root()->KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync;
    }
    bool tick_pending() const { return ((tick_sync() >> 2) ^ (tick_sync() >> 1)) & 1u; }
    int edges_to_t0() const {
        if (tick_cnt() != kWinTicks - 1 || !win_valid()) return 0;
        if (tick_pending()) return 1;
        if (((tick_sync() >> 1) ^ tick_sync()) & 1u) return 2;
        return 0;
    }

    void print_row(const char* tag, const WindowClose& c) const {
        std::printf("  %-9s ew=%+8d (%+8.2f ppm) integ=%+7d (%+7.2f ppm) "
                    "u_cmd=%+7d (%+7.2f ppm) trim=%+5d %s state=%d\n",
                    tag, c.ew, c.ew / 512.0, c.integ, c.integ / 512.0, c.ucmd,
                    c.ucmd / 512.0, trim(), c.committed ? "COMMIT " : "discard",
                    state());
    }

    void within(const char* what, long long got, long long lo, long long hi) {
        char msg[200];
        std::snprintf(msg, sizeof msg, "%s = %lld in [%lld, %lld]", what, got, lo, hi);
        check_.that(msg, got >= lo && got <= hi);
    }

    // ---- stimulus -----------------------------------------------------------
    //! One event off the femtosecond wheel; true on a clk_i rising edge.
    bool tick_one() {
        if (next_i <= next_p && next_i <= next_a) {
            t_fs = next_i; next_i += kHalfI;
            dut->clk_i ^= 1;
            if (dut->clk_i) {
                dut->phc_slew_active_i = held_slew_ || slew_left_ns_ != 0.0;
                if (slew_left_ns_ != 0.0) apply_slew_for_one_cycle();
                dut->ptp_now_i = static_cast<uint64_t>(std::llround(t_fs / 1e6 + ptp_step_ns));
            }
            dut->eval();
            if (dut->clk_i) {
                mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o,
                             dut->drp_di_o, dut->mmcm_rst_o);
                dut->drp_do_i      = mm.dout;
                dut->drp_rdy_i     = mm.drdy;
                dut->mmcm_locked_i = mm.locked;
            }
            return dut->clk_i != 0;
        }
        if (next_p <= next_a) {
            t_fs = next_p; next_p += half_p_;
            dut->ps_clk_i ^= 1;
            dut->eval();
            if (dut->ps_clk_i) {
                mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
                dut->ps_done_i = mm.psdone;
            }
            return false;
        }
        t_fs = next_a;
        base_a += kHalfA0;
        next_a = base_a + mm.audio_adj_fs;
        if (next_a <= t_fs) next_a = t_fs + 1e3;
        dut->clk_audio_i ^= 1;
        dut->eval();
        return false;
    }
    //! the plane's slew: the PHC runs 200 ppm off until the offset is paid
    void apply_slew_for_one_cycle() {
        const double d = 200e-6 * 2.0 * kHalfI * 1e-6;
        const double inc = (std::fabs(slew_left_ns_) < d) ? slew_left_ns_
                         : std::copysign(d, slew_left_ns_);
        ptp_step_ns += inc;
        slew_left_ns_ -= inc;
    }

    //! Advance to the next clk_i rising edge. A PI writeback closing on that
    //! edge is recorded in last_ and reported by the return value; an edge that
    //! leaves the servo out of LOCKED is remembered in left_locked_.
    bool clk_edge() {
        const bool closing = (pp_seq() == 7);
        const bool run = pp_run();
        while (!tick_one()) {}
        if (closing) last_ = WindowClose{ew(), integ(), ucmd(), run};
        if (state() != kStateLocked) left_locked_ = true;
        if (talker_bias_until_fs_ > 0.0 && t_fs >= talker_bias_until_fs_) {
            dut->crf_rate_i = talker_rate_;
            talker_bias_until_fs_ = 0.0;
        }
        return closing;
    }
    void run_ms(double ms) {
        const double te = t_fs + ms * 1e12;
        while (t_fs < te) clk_edge();
    }
    WindowClose run_to_window_close() {
        while (!clk_edge()) {}
        return last_;
    }
    void run_to_tick(int tick) {
        while (tick_cnt() != tick) clk_edge();
    }
    //! run until the boundary is exactly `edges` clk_i edges away
    void run_to_edges_before_t0(int edges) {
        while (edges_to_t0() != edges) clk_edge();
    }

    static int32_t rate_for_ppm(double ppm) {   // KL_crf_rx rate_o for a talker offset
        return static_cast<int32_t>(std::llround(512e6 * (1.0 / (1.0 + ppm * 1e-6) - 1.0)));
    }

    //! Reset, select CRF against the talker and run until LOCKED, then two more
    //! committed windows so the integrator is settled.
    void bring_up_and_lock() {
        mm.regs[0x08] = 0x0595;
        mm.regs[0x09] = 0x0080;
        dut->rst_n = 0;
        dut->clk_src_i = 0;
        dut->crf_src_idx_i = 1;
        dut->crf_locked_i = 0;
        dut->crf_rate_valid_i = 1; // synthetic rate input is valid
        dut->phc_slew_active_i = 0;
        dut->crf_rate_i = 0;
        dut->auto_repair_i = 0;
        dut->ps_invert_i = 0;
        dut->mmcm_locked_i = 1;
        run_ms(0.01);
        dut->rst_n = 1;
        run_ms(0.1);
        talker_rate_ = rate_for_ppm(kTalkerPpm);
        dut->crf_rate_i = talker_rate_;
        dut->crf_locked_i = 1;
        dut->clk_src_i = 1;
        int windows = 0;
        while (state() != kStateLocked && windows < 40) {
            run_to_window_close();
            windows++;
        }
        lock_windows_ = windows;
        run_to_window_close();
        run_to_window_close();
    }

    // ---- cases --------------------------------------------------------------
    void prove_lock_at_the_silicon_scale() {
        std::printf("[P0] lock at the silicon window scale (talker %+.0f ppm)\n",
                    kTalkerPpm);
        bring_up_and_lock();
        check_.dec("[P0] state LOCKED", static_cast<uint64_t>(state()), kStateLocked);
        within("[P0] windows to LOCKED", lock_windows_, 1, 39);
        check_.that("[P0] the last window committed", last_.committed);
        within("[P0] last window error (x512 ppm)", last_.ew, -kLockThr + 1, kLockThr - 1);
        const long long want = std::llround((kTalkerPpm - kBasePpm) * 512.0);
        within("[P0] integrator ~ talker - base (x512 ppm)", integ(),
               want - kLockThr, want + kLockThr);
    }

    //! The shared verdict: the step was counted once, the loop state held, the
    //! servo never left LOCKED, and the close that followed was clean. A close
    //! that zeroes lock_cnt drops LOCKED two edges after its writeback, so the
    //! LOCKED verdict is read four edges past the close.
    void expect_untouched(const char* tag, const Snapshot& s0, const WindowClose& next,
                          int disc_delta) {
        for (int e = 0; e < 4; e++) clk_edge();
        char what[96];
        std::snprintf(what, sizeof what, "%s discards counted", tag);
        within(what, disc_cnt() - s0.disc, disc_delta, disc_delta);
        std::snprintf(what, sizeof what, "%s next window committed", tag);
        check_.that(what, next.committed);
        std::snprintf(what, sizeof what, "%s next window error", tag);
        within(what, next.ew, -kLockThr + 1, kLockThr - 1);
        std::snprintf(what, sizeof what, "%s integrator moved", tag);
        within(what, next.integ - s0.integ, -kLockThr / 2, kLockThr / 2);
        std::snprintf(what, sizeof what, "%s written rate moved", tag);
        within(what, next.ucmd - s0.ucmd, -kLockThr, kLockThr);
        std::snprintf(what, sizeof what, "%s LOCKED on every edge", tag);
        check_.that(what, !left_locked_);
    }

    void prove_step_leaves_the_loop_untouched(int64_t step_ns) {
        char tag[40];
        std::snprintf(tag, sizeof tag, "[P1 %+lld ns]", static_cast<long long>(step_ns));
        run_to_tick(kWinTicks / 2);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        ptp_step_ns += static_cast<double>(step_ns);
        const WindowClose next = run_to_window_close();
        expect_untouched(tag, s0, next, 1);
    }

    //! The stepped sample is the one the boundary snapshots: that window is
    //! squashed, not committed, and the one after it is clean.
    void prove_step_on_the_boundary_sample_is_squashed() {
        std::printf("[P2a] step staged on the boundary sample\n");
        run_to_edges_before_t0(2);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        ptp_step_ns += 150'000.0;
        clk_edge();
        check_.that("[P2a] arm: the stepped sample is staged, T0 next edge",
                    ptp_jump() && edges_to_t0() == 1);
        clk_edge();
        check_.that("[P2a] arm: the boundary fired on it", pp_seq() == 1);
        const WindowClose squashed = run_to_window_close();
        check_.that("[P2a] the boundary window is NOT committed", !squashed.committed);
        within("[P2a] integrator at the squashed close", squashed.integ - s0.integ, 0, 0);
        within("[P2a] written rate at the squashed close", squashed.ucmd - s0.ucmd, 0, 0);
        expect_untouched("[P2a]", s0, run_to_window_close(), 1);
    }

    //! One edge later the boundary snapshotted the pre-step sample: that window
    //! is clean and commits; the new one straddles the step and is abandoned.
    void prove_step_after_the_boundary_commits_the_closed_window() {
        std::printf("[P2b] step staged one edge after the boundary\n");
        run_to_edges_before_t0(1);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        ptp_step_ns += 150'000.0;
        check_.that("[P2b] arm: no stepped sample staged before T0", !ptp_jump());
        clk_edge();
        check_.that("[P2b] arm: T0 fired as the stepped sample was staged",
                    pp_seq() == 1 && ptp_jump());
        const WindowClose closed = run_to_window_close();
        check_.that("[P2b] the closed (pre-step) window commits", closed.committed);
        within("[P2b] its window error", closed.ew, -kLockThr + 1, kLockThr - 1);
        expect_untouched("[P2b]", s0, run_to_window_close(), 1);
    }

    //! Earlier still, inside the window's last tick, the window is abandoned
    //! before its boundary: the boundary tick re-bases instead of closing, and
    //! the next close is clean.
    void prove_step_before_the_boundary_rebases_the_window() {
        std::printf("[P2c] step inside the last tick before the boundary\n");
        run_to_tick(kWinTicks - 1);
        run_ms(0.5);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        ptp_step_ns += 150'000.0;
        clk_edge();
        clk_edge();
        check_.that("[P2c] arm: window abandoned inside its last tick",
                    !win_valid() && tick_cnt() == kWinTicks - 1 && pp_seq() == 0);
        while (!tick_pending()) clk_edge();
        clk_edge();
        check_.that("[P2c] arm: the boundary tick re-based instead of closing",
                    pp_seq() == 0 && win_valid() && tick_cnt() == 0);
        expect_untouched("[P2c]", s0, run_to_window_close(), 1);
    }

    //! The 1024 ppm guard discards a window (an implausible CRF rate) in its S4
    //! cycle while a PHC step lands in the window that just opened: two
    //! discards on one cycle, and both are counted.
    void prove_coincident_discards_both_count() {
        std::printf("[P3] guard discard and PHC step on one cycle\n");
        run_to_tick(kWinTicks / 2);
        dut->crf_rate_i = talker_rate_ + 2'000'000;
        run_to_edges_before_t0(1);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        clk_edge();
        dut->crf_rate_i = talker_rate_;
        while (pp_seq() != 3) clk_edge();
        ptp_step_ns += 150'000.0;
        clk_edge();
        check_.that("[P3] arm: S4 of a guard window with a step staged",
                    pp_seq() == 4 && pp_run() && ptp_jump() && std::abs(ew()) > kGuardThr);
        const WindowClose guarded = run_to_window_close();
        check_.that("[P3] the implausible window is NOT committed", !guarded.committed);
        expect_untouched("[P3]", s0, run_to_window_close(), 2);
    }

    //! Same 100 us / 200 ppm trajectory as the #539 record. The two
    //! overlapping windows include the partial tail after the level falls.
    void prove_slew_holds(int64_t ns) {
        std::printf("[S1] policy slew %+lld ns at 200 ppm\n", static_cast<long long>(ns));
        run_to_tick(kWinTicks / 2);
        const Snapshot s0 = snapshot();
        const double start_fs = t_fs;
        left_locked_ = false;
        slew_left_ns_ = static_cast<double>(ns);
        const int affected = std::abs(ns) == 100'000 ? 2 : 1;
        for (int w = 0; w < affected; ++w) {
            const WindowClose c = run_to_window_close();
            print_row("slew", c);
            check_.that("[S1] overlapped window is discarded", !c.committed);
            within("[S1] integrator held exactly", c.integ - s0.integ, 0, 0);
            within("[S1] written rate held exactly", c.ucmd - s0.ucmd, 0, 0);
        }
        check_.that("[S1] tail window closes after deassertion", !dut->phc_slew_active_i);
        const WindowClose clean = run_to_window_close();
        expect_untouched("[S1]", s0, clean, affected);
        check_.that("[S1] first clean close within 1.536 seconds of start",
                    t_fs - start_fs < 1.536e15);
    }

    //! Assert on the staged boundary sample, then remove the level before
    //! the next sample. That shared endpoint taints both adjacent windows.
    void prove_slew_boundary() {
        run_to_edges_before_t0(2);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        held_slew_ = true;
        clk_edge();
        check_.that("[S2] arm: boundary next edge", edges_to_t0() == 1);
        held_slew_ = false;
        check_.that("[S2] boundary sample is discarded", !run_to_window_close().committed);
        check_.that("[S2] shared endpoint taints next window", !run_to_window_close().committed);
        expect_untouched("[S2]", s0, run_to_window_close(), 2);
    }

    //! A level staged on T0 itself is newer than the closed sample. A
    //! completed clean measurement must still commit through the PI stages.
    void prove_clean_close_before_slew() {
        run_to_edges_before_t0(1);
        left_locked_ = false;
        held_slew_ = true;
        const WindowClose closed = run_to_window_close();
        check_.that("[S3] clean pre-slew window commits", closed.committed);
        const Snapshot s0 = snapshot();
        held_slew_ = false;
        check_.that("[S3] partial window is discarded", !run_to_window_close().committed);
        expect_untouched("[S3]", s0, run_to_window_close(), 1);
    }

    //! The producer can hold correction through missing measurements. No
    //! 0.5 s timer may silently release the consumer while it stays high.
    void prove_slew_stays_active() {
        run_to_tick(kWinTicks / 2);
        const Snapshot s0 = snapshot();
        left_locked_ = false;
        held_slew_ = true;
        for (int w = 0; w < 7; ++w) {
            const WindowClose c = run_to_window_close();
            check_.that("[S4] held level discards every window", !c.committed);
            within("[S4] integrator held exactly", c.integ - s0.integ, 0, 0);
        }
        held_slew_ = false;
        check_.that("[S4] final partial window discarded", !run_to_window_close().committed);
        expect_untouched("[S4]", s0, run_to_window_close(), 8);
    }

    //! A real talker rate change is not a step: it is integrated and the servo
    //! re-locks on the new rate, with nothing discarded.
    void prove_rate_path_still_integrates() {
        std::printf("[P4] rate path: talker %+.0f -> -20 ppm, no step\n", kTalkerPpm);
        const int disc0 = disc_cnt();
        talker_rate_ = rate_for_ppm(-20.0);
        dut->crf_rate_i = talker_rate_;
        const WindowClose first = run_to_window_close();
        check_.that("[P4] the first window after the change commits", first.committed);
        within("[P4] its error carries the rate change (x512 ppm)", first.ew,
               std::llround(-45.0 * 512), std::llround(-5.0 * 512));
        int windows = 0;
        while ((state() != kStateLocked || windows < 2) && windows < 40) {
            run_to_window_close();
            windows++;
        }
        check_.dec("[P4] re-LOCKED on the new rate", static_cast<uint64_t>(state()),
                   kStateLocked);
        const long long want = std::llround((-20.0 - kBasePpm) * 512.0);
        within("[P4] integrator ~ new talker - base (x512 ppm)", integ(),
               want - kLockThr, want + kLockThr);
        within("[P4] nothing discarded", disc_cnt() - disc0, 0, 0);
    }

    const milan::tb::Model<VKL_mmcm_drp_servo> model_{};
    VKL_mmcm_drp_servo* dut = model_.get();
    MmcmModel mm{};
    milan::tb::Checker check_{"mmcm_servo phc_step"};
    WindowClose last_{0, 0, 0, false};
    int lock_windows_ = 0;
    bool left_locked_ = false;
    int32_t talker_rate_ = 0;
    double talker_bias_until_fs_ = 0.0;
    double slew_left_ns_ = 0.0;
    bool held_slew_ = false;

    // ---- clocks (femtosecond wheel, as sim_main.cpp) --------------------------
    double half_p_;
    double t_fs = 0;
    double ptp_step_ns = 0;
    double next_i = 10000e3;
    double next_p = 2500e3;
    double next_a = 12345e3;
    static constexpr double kHalfI = 10000e3;      // clk_i 50 MHz
    static constexpr double kHalfA0 = 0.5 * (1e15 / 24.576e6) * (1.0 - kBasePpm * 1e-6);
    double base_a = 12345e3;
};

//! +name=<n> as a signed integer, or false when the plusarg is absent
bool plusarg_ns(const char* name, int64_t& out) {
    const char* arg = Verilated::commandArgsPlusMatch(name);
    if (arg == nullptr || arg[0] == '\0') return false;
    const char* eq = std::strchr(arg, '=');
    if (eq == nullptr) return false;
    out = std::strtoll(eq + 1, nullptr, 10);
    return true;
}

constexpr double kHalfPsSuite = 10000e3;   //! PSCLK 50 MHz
constexpr double kHalfPsTrace = 2500e3;    //! PSCLK 200 MHz, the SoC's

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    int64_t ns = 0;
    if (plusarg_ns("trace_step_ns=", ns)) {
        return PhcStepHarness(kHalfPsTrace).trace(Disturbance::phc_step, ns);
    }
    if (plusarg_ns("trace_slew_ns=", ns)) {
        return PhcStepHarness(kHalfPsTrace).trace(Disturbance::phc_slew, ns);
    }
    if (plusarg_ns("trace_talker_step_ns=", ns)) {
        return PhcStepHarness(kHalfPsTrace).trace(Disturbance::talker_step, ns);
    }
    if (Verilated::commandArgsPlusMatch("slew_control")[0] != '\0') {
        return PhcStepHarness(kHalfPsSuite).slew_control();
    }
    if (Verilated::commandArgsPlusMatch("slew_suite")[0] != '\0') {
        return PhcStepHarness(kHalfPsSuite).slew_suite();
    }
    return PhcStepHarness(kHalfPsSuite).suite();
}

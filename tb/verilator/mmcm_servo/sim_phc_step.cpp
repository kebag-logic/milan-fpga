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
// Modes:
//   (no argument)          the self-checking cases below
//   +trace_step_ns=<n>     the reproduction record: lock, then one step of n ns
//                          (signed) at mid-window, traced window by window
//
// The integrator and the written rate are read through --public-flat-rw
// (integ_r, u_cmd_r, ew_r, pp_seq_r, pp_run_r); nothing is written through it.

#include "VKL_mmcm_drp_servo.h"
#include "VKL_mmcm_drp_servo___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "mmcm_model.h"
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cmath>

namespace {

//! Silicon servo constants the checks are written against (the RTL defaults).
constexpr int kWinTicks = 512;          //! 2^WIN_LOG2_P
constexpr int32_t kLockThr = 1024;      //! LOCK_THR_P: 2 ppm in x512 units
constexpr int kStateLocked = 4;
constexpr int kStateAcquire = 3;

//! One clean window, as the PI micro-sequence closed it.
struct WindowClose {
    int32_t ew;         //! normalized window error (ns per 512 ms)
    int32_t integ;      //! integrator after the writeback
    int32_t ucmd;       //! written rate command after the writeback
    bool committed;     //! pp_run_r at the writeback (false = discarded)
};

class PhcStepHarness {
 public:
    int trace(int64_t step_ns) {
        bring_up_and_lock();
        std::printf("[TRACE] step %lld ns at mid-window, talker %+.1f ppm\n",
                    static_cast<long long>(step_ns), kTalkerPpm);
        print_row("locked", last_);
        run_to_tick(kWinTicks / 2);
        const int disc0 = disc_cnt();
        apply_step_at_next_edge(static_cast<double>(step_ns));
        std::printf("  step applied at t=%.3f ms (tick %d of the window)\n",
                    t_fs * 1e-12, tick_cnt());
        for (int w = 1; w <= 4; w++) {
            const WindowClose c = run_to_window_close();
            char tag[32];
            std::snprintf(tag, sizeof tag, "window +%d", w);
            print_row(tag, c);
        }
        std::printf("  guard discards counted across the trace: %d\n",
                    disc_cnt() - disc0);
        return 0;
    }

 private:
    //! Signed readers for the traced registers (Verilator keeps a 24-bit
    //! signed flop in a 32-bit word, zero-extended).
    static int32_t sext24(uint32_t v) {
        return static_cast<int32_t>(v << 8) >> 8;
    }
    int32_t integ() const { return sext24(root()->KL_mmcm_drp_servo__DOT__integ_r); }
    int32_t ucmd() const { return sext24(root()->KL_mmcm_drp_servo__DOT__u_cmd_r); }
    int32_t ew() const { return static_cast<int32_t>(root()->KL_mmcm_drp_servo__DOT__ew_r); }
    int pp_seq() const { return root()->KL_mmcm_drp_servo__DOT__pp_seq_r; }
    bool pp_run() const { return root()->KL_mmcm_drp_servo__DOT__pp_run_r != 0; }
    int tick_cnt() const { return root()->KL_mmcm_drp_servo__DOT__tick_cnt_r; }
    int state() const { return static_cast<int>(dut->status_o & 7); }
    int disc_cnt() const { return static_cast<int>((dut->status_o >> 10) & 0x3F); }
    int16_t trim() const { return static_cast<int16_t>(dut->status_o >> 16); }
    VKL_mmcm_drp_servo___024root* root() const { return dut->rootp; }

    void print_row(const char* tag, const WindowClose& c) const {
        std::printf("  %-10s ew=%+8d (%+8.2f ppm) integ=%+7d (%+7.2f ppm) "
                    "u_cmd=%+7d (%+7.2f ppm) trim=%+5d %s state=%d\n",
                    tag, c.ew, c.ew / 512.0, c.integ, c.integ / 512.0, c.ucmd,
                    c.ucmd / 512.0, trim(), c.committed ? "COMMIT " : "discard",
                    state());
    }

    //! One event off the femtosecond wheel; returns true on a clk_i rising
    //! edge (the servo's own edge).
    bool tick_one() {
        if (next_i <= next_p && next_i <= next_a) {
            t_fs = next_i; next_i += kHalfI;
            dut->clk_i ^= 1;
            if (dut->clk_i) {
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
            t_fs = next_p; next_p += kHalfP;
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

    //! Advance to the next clk_i rising edge. A PI writeback closing on that
    //! edge is recorded in last_ and reported by the return value.
    bool clk_edge() {
        const bool closing = (pp_seq() == 7);
        const bool run = pp_run();
        while (!tick_one()) {}
        if (closing) {
            last_ = WindowClose{ew(), integ(), ucmd(), run};
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
    //! The PHC step lands on the next clk_i edge's ptp_now_i sample.
    void apply_step_at_next_edge(double ns) { ptp_step_ns += ns; }

    static int32_t rate_for_ppm(double ppm) {   // KL_crf_rx rate_o for a talker offset
        return static_cast<int32_t>(std::llround(512e6 * (1.0 / (1.0 + ppm * 1e-6) - 1.0)));
    }

    //! Reset, select CRF against a +20 ppm talker and run until LOCKED, then
    //! two more committed windows so the integrator is settled.
    void bring_up_and_lock() {
        mm.regs[0x08] = 0x0595;
        mm.regs[0x09] = 0x0080;
        dut->rst_n = 0;
        dut->clk_src_i = 0;
        dut->crf_src_idx_i = 1;
        dut->crf_locked_i = 0;
        dut->crf_rate_i = 0;
        dut->auto_repair_i = 0;
        dut->ps_invert_i = 0;
        dut->mmcm_locked_i = 1;
        run_ms(0.01);
        dut->rst_n = 1;
        run_ms(0.1);
        dut->crf_rate_i = rate_for_ppm(kTalkerPpm);
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

    const milan::tb::Model<VKL_mmcm_drp_servo> model_{};
    VKL_mmcm_drp_servo* dut = model_.get();
    MmcmModel mm{};
    WindowClose last_{0, 0, 0, false};
    int lock_windows_ = 0;

    static constexpr double kTalkerPpm = 20.0;

    // ---- clocks (femtosecond wheel, as sim_main.cpp) --------------------------
    double t_fs = 0;
    double ptp_step_ns = 0;
    double next_i = 10000e3;
    double next_p = 2500e3;
    double next_a = 12345e3;
    static constexpr double kHalfI = 10000e3;      // clk_i 50 MHz
    static constexpr double kHalfP = 2500e3;       // ps_clk 200 MHz
    // audio base: 24.576 MHz - 10.64 ppm (the integer two-stage MMCM plan)
    static constexpr double kBasePpm = -10.64;
    static constexpr double kHalfA0 = 0.5 * (1e15 / 24.576e6) * (1.0 - kBasePpm * 1e-6);
    double base_a = 12345e3;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const char* arg = Verilated::commandArgsPlusMatch("trace_step_ns=");
    PhcStepHarness harness;
    if (arg != nullptr && arg[0] != '\0') {
        const char* eq = std::strchr(arg, '=');
        return harness.trace(std::strtoll(eq + 1, nullptr, 10));
    }
    std::printf("usage: +trace_step_ns=<n>\n");
    return 1;
}

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R302-1, #546): receiver-to-servo GM-change variants the
// shipped talker_step harness does not run. Same event model and wrapper
// as tb/verilator/crf_rx/sim_talker_step.cpp; scenario selected by argv[1].
#include "Vcrf_talker_wrap.h"
#include "Vcrf_talker_wrap___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>

namespace {
class LoopProbe {
 public:
    int run(const std::string& scenario) {
        mm.regs[0x08] = 0x0595; mm.regs[0x09] = 0x0080;
        dut->rst_n = 0; dut->clk_src_i = 1; dut->crf_src_idx_i = 1;
        dut->auto_repair_i = 0; dut->ps_invert_i = 0;
        dut->mmcm_locked_i = 1; run_ms(0.01); dut->rst_n = 1;
        run_ms(8500);
        check.that("loop locked before scenario", state() == 4);
        if (scenario == "tu_only") {
            // legitimate tu: no step anywhere
            begin(); dut->tu_i = 1; run_ms(250); dut->tu_i = 0; run_ms(1100);
            end("tu_only", 0, true);
        } else if (scenario == "step_inside_tu") {
            // tu rises first; the talker steps 100 ms later (no tu edge on
            // that PDU); tu stays high 600 ms (> one 512 ms ring)
            begin(); dut->tu_i = 1; run_ms(100);
            remote_step_ns += 150000; run_ms(100);
            local_step_ns += 150000; run_ms(400);
            dut->tu_i = 0; run_ms(1100);
            end("step_inside_tu", 1, true);
        } else if (scenario == "step20us") {
            for (const int64_t s : {20000LL, -20000LL}) {
                begin(); remote_step_ns += s; run_ms(100);
                local_step_ns += s; run_ms(1250);
                end("step20us", 1, true);
            }
        } else if (scenario == "local_first") {
            begin(); local_step_ns -= 150000; run_ms(100);
            remote_step_ns -= 150000; run_ms(1250);
            end("local_first", 1, true);
        } else if (scenario == "repeated") {
            // five GM changes 300 ms apart: each lands inside the previous
            // refill; tu marks alternate events only
            begin();
            for (int k = 0; k < 5; ++k) {
                const int64_t s = (k % 2) ? -150000 : 150000;
                if (k % 2 == 0) dut->tu_i = !dut->tu_i;
                remote_step_ns += s; run_ms(100);
                local_step_ns += s; run_ms(200);
            }
            dut->tu_i = 0; run_ms(1300);
            end("repeated", 5, true);
        } else if (scenario == "subthreshold") {
            // informative: an unmarked talker step below the 2048 ns backstop
            // is by construction NOT detected; quantify its servo footprint
            begin(); remote_step_ns += 2000; run_ms(1500);
            std::printf("subthreshold 2000 ns: integrator range %.3f..%.3f ppm"
                        " (before %.3f), invalid seen %d\n",
                        min_integ / 512.0, max_integ / 512.0, before / 512.0,
                        saw_invalid);
            check.that("subthreshold: stays LOCKED", stayed_locked);
        } else if (scenario == "quiet") {
            // no event at all: the shipped sampling still reports invalid
            begin(); run_ms(1100); monitor = false;
            check.that("quiet: shipped post-edge sampling reports invalid (artifact)",
                       raw_invalid);
            check.that("quiet: registered view stays valid", !saw_invalid);
            check.that("quiet: LOCKED", stayed_locked);
        } else if (scenario == "talker_only_neg") {
            // unmarked talker step, no listener step: nothing else can hide it
            begin(); remote_step_ns -= 150000; run_ms(1500);
            end("talker_only_neg", 0, true);
        } else if (scenario == "talker_only_pos") {
            begin(); dut->tu_i = 1; remote_step_ns += 150000; run_ms(250);
            dut->tu_i = 0; run_ms(1250);
            end("talker_only_pos", 0, true);
        } else if (scenario == "lag_sweep") {
            // GM change with steps at both ends; the listener step lags the
            // talker's by 100..500 ms and the event phase walks the window
            int k = 0;
            for (const double lag : {100.0, 200.0, 300.0, 400.0, 500.0}) {
                begin();
                const int64_t s = (k++ % 2) ? -150000 : 150000;
                remote_step_ns += s; run_ms(lag);
                local_step_ns += s; run_ms(1300 + 37.0 * k);
                end("lag_sweep", 1, true);
            }
        } else {
            check.fail("unknown scenario");
        }
        return check.report();
    }
 private:
    milan::tb::Model<Vcrf_talker_wrap> dut;
    milan::tb::Checker check{"r302 loop probe"};
    MmcmModel mm;
    double now_fs = 0, next_i = 10e6, next_p = 10e6, next_a = 12345e3;
    double base_a = 12345e3, next_pdu_ns = 100000;
    int64_t local_step_ns = 0, remote_step_ns = 0;
    uint64_t remote_ts_ns = 10'000'000'000ULL;
    bool monitor = false, stayed_locked = true, saw_invalid = false;
    bool raw_invalid = false;
    int min_integ = 0, max_integ = 0, before = 0, disc_before = 0;
    uint32_t unlocks_before = 0;

    int state() const { return dut->status_o & 7; }
    int integ() const {
        return static_cast<int32_t>(
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__integ_r << 8) >> 8;
    }
    void observe() {
        if (!monitor) return;
        const int v = integ();
        stayed_locked &= state() == 4;
        // After the accepting edge the harness still holds frame_p_i high,
        // so the combinational rate_valid_o reflects a post-update view the
        // DUT never samples. raw_invalid reproduces the shipped harness's
        // sampling; saw_invalid only counts clocks with frame_p_i low.
        raw_invalid |= !dut->rate_valid_o;
        if (!dut->frame_p_i) saw_invalid |= !dut->rate_valid_o;
        min_integ = std::min(min_integ, v);
        max_integ = std::max(max_integ, v);
    }
    void event() {
        if (next_i <= next_p && next_i <= next_a) {
            now_fs = next_i; next_i += 10e6; dut->clk_i ^= 1;
            if (dut->clk_i) {
                dut->ptp_now_i = static_cast<uint64_t>(
                    10'000'000'000LL + std::llround(now_fs / 1e6) + local_step_ns);
                dut->frame_p_i = 0;
                if (dut->rst_n && now_fs / 1e6 >= next_pdu_ns) {
                    next_pdu_ns += 1'999'960;
                    remote_ts_ns += 1'999'960;
                    dut->ts_ns_i = remote_ts_ns + static_cast<uint64_t>(remote_step_ns);
                    dut->seq_i = static_cast<uint8_t>(dut->seq_i + 1);
                    dut->frame_p_i = 1;
                }
            }
            dut->eval();
            if (dut->clk_i) {
                mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o,
                             dut->drp_di_o, dut->mmcm_rst_o);
                dut->drp_do_i = mm.dout; dut->drp_rdy_i = mm.drdy;
                dut->mmcm_locked_i = mm.locked;
                observe();
            }
        } else if (next_p <= next_a) {
            now_fs = next_p; next_p += 10e6; dut->ps_clk_i ^= 1;
            dut->eval();
            if (dut->ps_clk_i) {
                mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
                dut->ps_done_i = mm.psdone;
            }
        } else {
            now_fs = next_a;
            base_a += 0.5 * (1e15 / 24.576e6) * (1.0 + 10.64e-6);
            next_a = std::max(base_a + mm.audio_adj_fs, now_fs + 1e3);
            dut->clk_audio_i ^= 1; dut->eval();
        }
    }
    void run_ms(double ms) {
        const auto until = now_fs + ms * 1e12;
        while (now_fs < until) event();
    }
    void begin() {
        before = integ(); disc_before = (dut->status_o >> 10) & 63;
        unlocks_before = dut->rx_unlocks_o;
        stayed_locked = true; saw_invalid = false; raw_invalid = false;
        min_integ = before; max_integ = before; monitor = true;
    }
    void end(const char* name, int local_steps, bool expect_invalid) {
        monitor = false;
        std::string p(name);
        check.that((p + ": receiver withheld samples").c_str(),
                   saw_invalid == expect_invalid);
        check.that((p + ": servo LOCKED on every clock").c_str(), stayed_locked);
        check.dec((p + ": no counted receiver unlock").c_str(),
                  dut->rx_unlocks_o, unlocks_before);
        check.that((p + ": integrator within 1 ppm").c_str(),
                   min_integ >= before - 512 && max_integ <= before + 512);
        check.that((p + ": rate valid again").c_str(), dut->rate_valid_o);
        check.dec((p + ": recovered rate excludes steps").c_str(),
                  static_cast<uint32_t>(static_cast<int32_t>(dut->rate_o)),
                  static_cast<uint32_t>(-40 * 256));
        check.dec((p + ": local PHC steps counted").c_str(),
                  ((dut->status_o >> 10) & 63) - disc_before,
                  static_cast<uint64_t>(local_steps));
        std::printf("%s: integrator %.3f..%.3f ppm (before %.3f), state %d\n",
                    name, min_integ / 512.0, max_integ / 512.0, before / 512.0,
                    state());
    }
};
}  // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    LoopProbe probe;
    return probe.run(argc > 1 ? argv[1] : "");
}

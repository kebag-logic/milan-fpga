// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// GM-change integration: independent PHC timelines step at both ends.
// Real CRF timestamps enter the receiver; its rate and valid outputs feed
// the production servo. Audio frequency responds through the MMCM model.
#include "Vcrf_talker_wrap.h"
#include "Vcrf_talker_wrap___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "../mmcm_servo/mmcm_model.h"
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>

namespace {
class TalkerStepHarness {
 public:
    int run() {
        check.echo_passes();
        mm.regs[0x08] = 0x0595; mm.regs[0x09] = 0x0080;
        dut->rst_n = 0; dut->clk_src_i = 1; dut->crf_src_idx_i = 1;
        dut->auto_repair_i = 0; dut->ps_invert_i = 0;
        dut->mmcm_locked_i = 1; run_ms(0.01); dut->rst_n = 1;
        run_ms(8500);
        check.that("receiver-to-servo loop locks at production scale", state() == 4);
        check.that("steady receiver rate is valid", dut->rate_valid_o);
        check.that("steady rate matches the source interval sum",
                   static_cast<int32_t>(dut->rate_o) == -40 * 256);
        std::printf("steady integrator %.3f ppm\n", integ() / 512.0);
        gm_change(150000, true);
        gm_change(-150000, false); // same tu: the timestamp backstop alone
        return check.report();
    }
 private:
    milan::tb::Model<Vcrf_talker_wrap> dut;
    milan::tb::Checker check{"crf_rx talker_step"};
    MmcmModel mm;
    double now_fs = 0;
    double next_i = 10e6;
    double next_p = 10e6;
    double next_a = 12345e3;
    double base_a = 12345e3;
    double next_pdu_ns = 100000;
    int64_t local_step_ns = 0;
    uint64_t remote_ts_ns = 10'000'000'000ULL;
    int64_t remote_step_ns = 0;
    bool monitor = false;
    bool stayed_locked = true;
    bool saw_invalid = false;
    int min_integ = 0;
    int max_integ = 0;
    int held_updates = 0;
    int previous_integ = 0;
    bool previous_valid = true;

    int state() const { return dut->status_o & 7; }
    int integ() const {
        return static_cast<int32_t>(
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__integ_r << 8) >> 8;
    }
    void observe() {
        if (!monitor) return;
        const int value = integ();
        stayed_locked &= state() == 4;
        saw_invalid |= !dut->rate_valid_o;
        min_integ = std::min(min_integ, value);
        max_integ = std::max(max_integ, value);
        // Allow a clean pre-event PI sequence to finish (eight cycles).
        if (!previous_valid && !dut->rate_valid_o &&
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__pp_seq_r == 0 &&
            value != previous_integ) ++held_updates;
        previous_integ = value;
        previous_valid = dut->rate_valid_o;
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
    void gm_change(int64_t step_ns, bool marker) {
        const int before = integ();
        const int disc_before = (dut->status_o >> 10) & 63;
        const auto unlocks_before = dut->rx_unlocks_o;
        stayed_locked = true; saw_invalid = false; held_updates = 0;
        min_integ = before; max_integ = before;
        previous_integ = before; previous_valid = true; monitor = true;
        remote_step_ns += step_ns;
        if (marker) dut->tu_i = 1;
        run_ms(100); // talker changes first; local guard cannot hide it
        local_step_ns += step_ns;
        run_ms(150);
        if (marker) dut->tu_i = 0;
        run_ms(1100); // includes refill and a clean servo window
        monitor = false;
        check.that("GM change: receiver withholds crossing rate samples", saw_invalid);
        check.that("GM change: servo stays LOCKED on every clock", stayed_locked);
        check.dec("GM change: no counted receiver re-lock", dut->rx_unlocks_o, unlocks_before);
        check.that("GM change: integrator stays within 1 ppm",
                   min_integ >= before - 512 && max_integ <= before + 512);
        check.dec("invalid sample cannot update the integrator", held_updates, 0);
        check.that("GM change: receiver returns to clean valid rate", dut->rate_valid_o);
        check.that("GM change: recovered rate excludes talker step",
                   static_cast<int32_t>(dut->rate_o) == -40 * 256);
        check.dec("GM change: local PHC step counted exactly once",
                  ((dut->status_o >> 10) & 63) - disc_before, 1);
        std::printf("step %lld ns: integrator range %.3f..%.3f ppm, state %d\n",
                    static_cast<long long>(step_ns), min_integ / 512.0,
                    max_integ / 512.0, state());
    }
};
} // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    TalkerStepHarness harness;
    return harness.run();
}

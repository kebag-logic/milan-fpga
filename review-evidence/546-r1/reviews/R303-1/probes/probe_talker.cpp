// Reviewer probe for PR #554 / issue #546 (not part of the tree).
// Built against the head's crf_talker_wrap.sv (real KL_crf_rx + real
// KL_mmcm_drp_servo). Same clocking and MMCM model as sim_talker_step.cpp.
// Phases after lock:
//   B  legitimate tu pulse (300 ms) with no step at either end, from LOCKED
//   D  source timestamp jitter +/-1200 ns from LOCKED (spacing can exceed 2048 ns)
//   E  clean recovery
//   C  source timestamp jitter +/-500 ns (uniform, deterministic LCG)
// Every phase prints what it observed; checks are the false-positive claims.
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
class Probe {
 public:
    int run() {
        mm.regs[0x08] = 0x0595; mm.regs[0x09] = 0x0080;
        dut->rst_n = 0; dut->clk_src_i = 1; dut->crf_src_idx_i = 1;
        dut->auto_repair_i = 0; dut->ps_invert_i = 0;
        dut->mmcm_locked_i = 1; run_ms(0.01); dut->rst_n = 1;
        run_ms(8500);
        check.that("probe: loop locks", state() == 4);
        // B: tu pulse, no step anywhere
        phase("B tu pulse no step", [&] {
            dut->tu_i = 1; run_ms(300); dut->tu_i = 0; run_ms(1500);
        });
        check.that("B: servo LOCKED throughout", locked_all);
        check.that("B: integrator within 0.1 ppm", max_i - min_i <= 51);
        check.that("B: rate valid again", dut->rate_valid_o);
        // the falling edge lands inside the rising edge's refill: one fall,
        // invalid for 300 ms + 256 intervals (~812 ms at 50 MHz clk_i)
        check.dec("B: one registered invalidation episode", breaks, 1);
        check.that("B: invalid for tu hold plus one 256-interval refill",
                   invalid_clk > 40'000'000 && invalid_clk < 41'500'000);
        // D: +/-1200 ns jitter from LOCKED: deviation up to 2400 ns > 2048 ns
        jitter = 1200;
        phase("D jitter 1200", [&] { run_ms(6000); });
        jitter = 0;
        phase("E clean recovery", [&] { run_ms(4000); });
        // C: +/-500 ns jitter: spacing deviation < 1000 + 20 ns drift
        jitter = 500;
        phase("C jitter 500", [&] { run_ms(4000); });
        check.dec("C: jitter 500 ns never invalidates (registered)", invalid_clk, 0);
        return check.report();
    }
 private:
    milan::tb::Model<Vcrf_talker_wrap> dut;
    milan::tb::Checker check{"reviewer probe talker"};
    MmcmModel mm;
    double now_fs = 0, next_i = 10e6, next_p = 10e6;
    double next_a = 12345e3, base_a = 12345e3, next_pdu_ns = 100000;
    uint64_t remote_ts_ns = 10'000'000'000ULL;
    uint32_t lcg = 12345u;
    int jitter = 0;
    bool monitor = false, locked_all = true;
    long invalid_clk = 0, clk_count = 0, pdus = 0, breaks = 0;
    int min_i = 0, max_i = 0;
    bool prev_valid = true;

    int state() const { return dut->status_o & 7; }
    int integ() const {
        return static_cast<int32_t>(
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__integ_r << 8) >> 8;
    }
    int jit() {
        lcg = lcg * 1664525u + 1013904223u;
        if (!jitter) return 0;
        return static_cast<int>((lcg >> 8) % (2u * jitter + 1u)) - jitter;
    }
    template <class F> void phase(const char* name, F body) {
        const int disc0 = (dut->status_o >> 10) & 63;
        locked_all = true; invalid_clk = 0; clk_count = 0; breaks = 0;
        min_i = max_i = integ();
        prev_valid = dut->rootp->crf_talker_wrap__DOT__rx__DOT__rate_valid_r;
        monitor = true;
        body();
        monitor = false;
        std::printf("[probe] %-20s state=%d locked_all=%d invalid_clk=%ld/%ld "
                    "valid_falls=%ld integ=%.3f..%.3f ppm now_valid=%d disc_delta=%d\n",
                    name, state(), locked_all ? 1 : 0, invalid_clk, clk_count, breaks,
                    min_i / 512.0, max_i / 512.0, dut->rate_valid_o ? 1 : 0,
                    ((dut->status_o >> 10) & 63) - disc0);
    }
    void observe() {
        if (!monitor) return;
        ++clk_count;
        locked_all &= state() == 4;
        // registered validity: the combinational port also reads low for
        // the one clock this harness holds frame_p_i past its accepting edge
        const bool v = dut->rootp->crf_talker_wrap__DOT__rx__DOT__rate_valid_r;
        if (!v) ++invalid_clk;
        if (prev_valid && !v) ++breaks;
        prev_valid = v;
        min_i = std::min(min_i, integ()); max_i = std::max(max_i, integ());
    }
    void event() {
        if (next_i <= next_p && next_i <= next_a) {
            now_fs = next_i; next_i += 10e6; dut->clk_i ^= 1;
            if (dut->clk_i) {
                dut->ptp_now_i = static_cast<uint64_t>(
                    10'000'000'000LL + std::llround(now_fs / 1e6));
                dut->frame_p_i = 0;
                if (dut->rst_n && now_fs / 1e6 >= next_pdu_ns) {
                    next_pdu_ns += 1'999'960;
                    remote_ts_ns += 1'999'960;
                    dut->ts_ns_i = remote_ts_ns + static_cast<int64_t>(jit());
                    dut->seq_i = static_cast<uint8_t>(dut->seq_i + 1);
                    dut->frame_p_i = 1; ++pdus;
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
};
} // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Probe probe;
    return probe.run();
}

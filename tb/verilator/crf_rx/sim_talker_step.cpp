// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// GM-change integration: talker-only and independently stepped PHC timelines.
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
        quiet();
        // No local guard can mask the two talker-only events.
        gm_change("talker_only_pos", 150000, true, 0);
        gm_change("talker_only_neg", -150000, false, 0);
        // Preserve the original short-lag ordering as guard interaction evidence.
        gm_change("both_short_pos", 150000, true, 100);
        gm_change("both_short_neg", -150000, false, 100);
        // The listener steps after a full window; receiver isolation is required.
        gm_change("both_long_pos", 150000, true, 600);
        gm_change("both_long_neg", -150000, false, 600);
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
    bool invalid_window = false;
    bool step_pending = false;
    unsigned crossing_intervals = 0;
    unsigned exposed_boundaries = 0;
    unsigned invalid_boundaries = 0;
    unsigned post_edge_artifacts = 0;

    int state() const { return dut->status_o & 7; }
    int integ() const {
        return static_cast<int32_t>(
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__integ_r << 8) >> 8;
    }
    void observe(bool sampled_valid, bool boundary, bool writeback, int old_integ) {
        if (!monitor) return;
        const int value = integ();
        stayed_locked &= state() == 4;
        saw_invalid |= !sampled_valid;
        min_integ = std::min(min_integ, value);
        max_integ = std::max(max_integ, value);
        // The same observer serves quiet and step cases. Post-edge validity
        // is deliberately counted separately: it is not the servo's input.
        if (sampled_valid && !dut->rate_valid_o) ++post_edge_artifacts;
        if (writeback && invalid_window && value != old_integ) ++held_updates;
        if (boundary) {
            invalid_window = !sampled_valid;
            if (crossing_intervals > 0) ++exposed_boundaries;
            if (!sampled_valid) {
                ++invalid_boundaries;
                // Reject even a numerically idle PI run on invalid history.
                if (dut->rootp->crf_talker_wrap__DOT__servo__DOT__pp_run_r)
                    ++held_updates;
            }
        }
    }
    void event() {
        if (next_i <= next_p && next_i <= next_a) {
            now_fs = next_i; next_i += 10e6;
            const bool rising = !dut->clk_i;
            bool sampled_valid = true;
            bool boundary = false;
            bool writeback = false;
            const int old_integ = integ();
            if (rising) {
                dut->ptp_now_i = static_cast<uint64_t>(
                    10'000'000'000LL + std::llround(now_fs / 1e6) + local_step_ns);
                dut->frame_p_i = 0;
                if (dut->rst_n && now_fs / 1e6 >= next_pdu_ns) {
                    next_pdu_ns += 1'999'960;
                    remote_ts_ns += 1'999'960;
                    dut->ts_ns_i = remote_ts_ns + static_cast<uint64_t>(remote_step_ns);
                    dut->seq_i = static_cast<uint8_t>(dut->seq_i + 1);
                    dut->frame_p_i = 1;
                    // Count source intervals independently of receiver state.
                    if (step_pending) {
                        crossing_intervals = 256;
                        step_pending = false;
                    } else if (crossing_intervals > 0) {
                        --crossing_intervals;
                    }
                }
                // Settle inputs with clk_i LOW, then capture exactly what
                // the servo samples on this edge, including accept-edge vetoes.
                dut->eval();
                sampled_valid = dut->rate_valid_o;
                const auto* root = dut->rootp;
                boundary = root->crf_talker_wrap__DOT__servo__DOT__tick_p_w &&
                    root->crf_talker_wrap__DOT__servo__DOT__win_valid_r &&
                    root->crf_talker_wrap__DOT__servo__DOT__tick_cnt_r == 511;
                writeback = root->crf_talker_wrap__DOT__servo__DOT__pp_seq_r == 7;
            }
            dut->clk_i = rising;
            dut->eval();
            if (dut->clk_i) {
                mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o,
                             dut->drp_di_o, dut->mmcm_rst_o);
                dut->drp_do_i = mm.dout; dut->drp_rdy_i = mm.drdy;
                dut->mmcm_locked_i = mm.locked;
                // A coincident local PHC step squashes the closing boundary.
                boundary &= dut->rootp->crf_talker_wrap__DOT__servo__DOT__pp_seq_r == 1;
                observe(sampled_valid, boundary, writeback, old_integ);
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
    void align_event() {
        // Land 100 ms after a real boundary: the next one must close about
        // 412 ms later, strictly inside the 256 * 1.999960 ms crossing span.
        const auto deadline = now_fs + 600e12;
        do { event(); } while (
            dut->rootp->crf_talker_wrap__DOT__servo__DOT__pp_seq_r != 1 &&
            now_fs < deadline);
        check.that("event alignment reaches a servo boundary", now_fs < deadline);
        run_ms(100);
    }
    void begin() {
        stayed_locked = true; saw_invalid = false; held_updates = 0;
        exposed_boundaries = 0; invalid_boundaries = 0; post_edge_artifacts = 0;
        invalid_window = false;
        min_integ = integ(); max_integ = integ(); monitor = true;
    }
    void quiet() {
        begin(); run_ms(1100); monitor = false;
        check.that("quiet: post-edge artifact was exercised", post_edge_artifacts > 0);
        check.that("quiet: sampled validity never satisfies withhold check", !saw_invalid);
        check.dec("quiet: no invalid servo boundaries", invalid_boundaries, 0);
        check.that("quiet: servo stays LOCKED", stayed_locked);
        std::printf("quiet: post-edge artifacts %u, sampled invalid %d\n",
                    post_edge_artifacts, saw_invalid);
    }
    void gm_change(const char* name, int64_t step_ns, bool marker, double lag_ms) {
        align_event();
        const int before = integ();
        const int disc_before = (dut->status_o >> 10) & 63;
        const auto unlocks_before = dut->rx_unlocks_o;
        begin();
        std::printf("scenario %s: step %lld ns, listener lag %.0f ms\n",
                    name, static_cast<long long>(step_ns), lag_ms);
        remote_step_ns += step_ns; step_pending = true;
        if (marker) dut->tu_i = 1;
        // A marked event holds tu for 250 ms in every ordering. An unmarked
        // negative event has no tu edge: it specifically needs the backstop.
        if (lag_ms > 0 && lag_ms < 250) {
            run_ms(lag_ms); local_step_ns += step_ns;
            run_ms(250 - lag_ms);
        } else {
            run_ms(250);
        }
        if (marker) dut->tu_i = 0;
        if (lag_ms >= 250) {
            run_ms(lag_ms - 250); local_step_ns += step_ns;
        }
        run_ms(1100); // complete refill and at least one clean servo window
        monitor = false;
        if (lag_ms == 0 || lag_ms >= 512) {
            check.that("crossing history reaches a servo boundary", exposed_boundaries > 0);
            check.that("servo samples invalid history at a boundary", invalid_boundaries > 0);
        }
        check.that("GM change: receiver withholds crossing rate samples", saw_invalid);
        check.that("GM change: servo stays LOCKED on every clock", stayed_locked);
        check.dec("GM change: no counted receiver re-lock", dut->rx_unlocks_o, unlocks_before);
        check.that("GM change: integrator stays within 1 ppm",
                   min_integ >= before - 512 && max_integ <= before + 512);
        check.dec("invalid sample cannot update the integrator", held_updates, 0);
        check.that("GM change: receiver returns to clean valid rate", dut->rate_valid_o);
        check.that("GM change: recovered rate excludes talker step",
                   static_cast<int32_t>(dut->rate_o) == -40 * 256);
        check.dec("GM change: local PHC steps counted",
                  ((dut->status_o >> 10) & 63) - disc_before, lag_ms > 0 ? 1 : 0);
        std::printf("%s: integrator range %.3f..%.3f ppm, state %d, "
                    "crossing boundaries %u, invalid boundaries %u\n",
                    name, min_integ / 512.0, max_integ / 512.0, state(),
                    exposed_boundaries, invalid_boundaries);
    }
};
} // namespace
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    TalkerStepHarness harness;
    return harness.run();
}

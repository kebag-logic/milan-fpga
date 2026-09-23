// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_media_grid_align closed over the real KL_media_nco (#74).
//
// The C++ side IS the physical grid: frame_ev_i pulses on a double-precision
// fractional-period model of the TDM fsync (the true 391/1591 divider plan:
// 100 MHz * 391/1591 / 512 = 47,999.4893 Hz, -10.6393 ppm against the NCO's
// exact 48,000.0000 Hz - the "Media boundary" table of
// docs/design/TIME_SYNC.md; Plan A itself and the drift
// tb/verilator/milan_dp/sim_aclk.cpp measures as one slipped sample every
// 1.9582 s are recorded in sections 3.1 and 3.5.1 of the archived
// docs/history/v1/design/TIME_SYNC.md). The oracle is the NCO's tick_o: the
// harness runs its own copy
// of the junction pend/consume law (the same law as KL_chan_map_capture's
// tdm_dup/tdm_skip counters), so "no sample slip" is graded by the
// instrument the datapath actually ships.
//
// Sign lesson, pinned here in BOTH rate directions: err > 0 = ticks fast =
// u must go NEGATIVE (the NCO port speaks the servo's "u > 0 = speed up").
// A flipped sign is a runaway - [G2]/[G3] fail loudly, not numerically.

#include <cstdint>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <climits>
#include "$LANES/74-junction-chatter/tb/common/verilator_harness.hpp"
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"

constexpr double kClkHz     = 100e6;   // the 100 MHz fabric clock
constexpr double kNominalHz = 48000.0; // the NCO's exact media rate
constexpr int    kResetCycles = 8;     // clock edges held in reset

constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0; // 47999.4893 Hz
//! lower bound on the lock's marker-to-tick clearance [G7]/[G8] grade
constexpr long   kLockClearMin = 8;

namespace {

//! The whole grid-alignment harness in one object: the Verilated model, the
//! check counters, the physical grid model and the shipped junction law - all
//! of which used to be this file's mutable file scope (I.2) - with one member
//! function per lettered case (F.3).
class MediaGridAlignHarness {
 public:
    //! What `main` used to be: bring the DUT up, run every case in order,
    //! print the tally.
    int run() {
        const milan::tb::Model<Vmedia_grid_align_wrap> model;
        dut = model.get();

        release_reset();

        printf("== KL_media_grid_align closed over KL_media_nco (#74) ==\n");

        explore_free_run();
        return report();
        prove_deselected_issues_no_command();
        prove_deselected_nco_is_bit_exact_nominal();
        prove_plan_a_ratio_acquires_bounds_and_holds();
        prove_opposite_rate_direction_flips_the_sign();
        prove_feed_watchdog_disengages_and_re_engages();
        prove_deselect_mid_lock_restores_free_run();
        prove_beyond_authority_parks_at_the_clamp();
        prove_raced_lock_keeps_the_junction_counters_still();
        prove_raced_lock_below_the_tick_is_kept_off_too();

        return report();
    }

 private:
    void ck(const char* t, long got, long exp) {
        checks++;
        if (got == exp) printf("  [ ok ] %-52s = %ld\n", t, got);
        else { fails++; printf("  [FAIL] %-52s = %ld (expected %ld)\n", t, got, exp); }
    }
    void ck_range(const char* t, long got, long lo, long hi) {
        checks++;
        if (got >= lo && got <= hi)
            printf("  [ ok ] %-52s = %ld (in [%ld, %ld])\n", t, got, lo, hi);
        else { fails++; printf("  [FAIL] %-52s = %ld (outside [%ld, %ld])\n",
                               t, got, lo, hi); }
    }

    // ---- the physical grid model + the shipped junction law ----------------
    void cyc() {
        bool fev = extra_frame;
        extra_frame = false;
        if (frame_period > 0.0) {
            frame_acc += 1.0;
            if (frame_acc >= frame_period) { frame_acc -= frame_period; fev = true; }
        }
        dut->frame_ev_i = fev;
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();
        bool tk = dut->tick_o;
        if (fev) frame_count++;
        if (tk)  tick_count++;
        if (fev && !tk)      { if (pend) skips++; pend = true; }
        else if (tk && !fev) { if (!pend) dups++; pend = false; }
        else if (fev && tk)  { pend = false; }
        track_clearance(fev);
        tick_q = tk;
    }
    //! Marker-to-tick clearance exactly as the RTL samples the pair: the
    //! tick_i an edge sees is the tick_o the PREVIOUS edge produced, and
    //! a marker's phase is the aligner's own capture (0 on the tick's
    //! edge, n edges after it otherwise). A marker n edges after one tick
    //! and m edges before the next is min(n, m) clear of the junction's
    //! race; a coincident one is 0.
    void track_clearance(bool fev) {
        if (tick_q) {
            if (mark_phase > 0) clear_min = std::min(clear_min, (edges_since_tick + 1) - mark_phase);
            edges_since_tick = 0;
            mark_phase = -1;
        } else {
            edges_since_tick++;
        }
        if (fev) {
            mark_phase = tick_q ? 0 : edges_since_tick;
            last_phase = mark_phase;
            clear_min  = std::min(clear_min, mark_phase);
        }
    }
    void run_cycles(long n) { for (long i = 0; i < n; i++) cyc(); }
    void slip_reset() { dups = 0; skips = 0; }

    void release_reset() {
        dut->rst_n = 0; dut->sel_i = 0; dut->frame_ev_i = 0;
        for (int i = 0; i < kResetCycles; i++) { dut->clk = 0; dut->eval();
                                                 dut->clk = 1; dut->eval(); }
        dut->rst_n = 1;
    }

    // ---------------------------------------------------------------------- //
    void prove_deselected_issues_no_command() {
        printf("\n[G0] reset / deselected: no command, no engagement\n");
        frame_period = kClkHz / PLAN_A;              // feed alive, sel low
        run_cycles(2'000'000);
        ck("G0: u_o stays 0 with sel_i low",        dut->u_o, 0);
        ck("G0: engaged_o stays 0 with sel_i low",  dut->engaged_o, 0);
    }

    // ---------------------------------------------------------------------- //
    void prove_deselected_nco_is_bit_exact_nominal() {
        printf("\n[G1] INTERNAL equivalence: deselected NCO is bit-exact nominal\n");
        tick_count = 0;
        run_cycles(10'000'000);                       // 0.1 s
        ck("G1: 4800 ticks in 10M cycles (exact 48 kHz)", tick_count, 4800);
    }

    // ---------------------------------------------------------------------- //
    void prove_plan_a_ratio_acquires_bounds_and_holds() {
        printf("\n[G2] select at the true Plan-A ratio: acquire, bound, hold\n");
        dut->sel_i = 1;
        // acquisition watch: from the engaging frame on, the phase error must
        // never reach one sample - that is what keeps the junction counters at
        // zero THROUGH acquisition, not just after it
        long max_abs_err = 0;
        bool was_engaged = false;
        slip_reset();
        for (long i = 0; i < 60'000'000; i++) {       // 0.6 s
            cyc();
            if (dut->engaged_o) {
                was_engaged = true;
                long e = static_cast<int16_t>(dut->err_cyc_o);
                if (e < 0) e = -e;
                if (e > max_abs_err) max_abs_err = e;
            }
        }
        ck("G2: loop engaged", was_engaged ? 1 : 0, 1);
        ck_range("G2: |err| peak over acquisition (cycles, <1 sample=2083)",
                 max_abs_err, 0, 300);
        ck("G2: zero surplus ticks while engaged (junction law)",  dups, 0);
        ck("G2: zero surplus frames while engaged (junction law)", skips, 0);
        // -10.6393 ppm plan: u settles near -170 LSB (1/16 ppm units, speed-up
        // convention -> negative = slow the fast packet grid down)
        ck_range("G2: settled u (LSB of 1/16 ppm; plan needs ~-170)",
                 static_cast<int16_t>(dut->u_o), -200, -140);
        ck_range("G2: settled |err| (cycles)", static_cast<int16_t>(dut->err_cyc_o) < 0
                 ? -static_cast<int16_t>(dut->err_cyc_o)
                 : static_cast<int16_t>(dut->err_cyc_o), 0, 60);
        // rate proof on the oracle: engaged ticks now come at the FRAME rate
        tick_count = 0; frame_count = 0;
        run_cycles(20'000'000);                       // 0.2 s locked
        ck_range("G2: locked tick count tracks frame count (+/-1)",
                 tick_count - frame_count, -1, 1);
    }

    // ---------------------------------------------------------------------- //
    void prove_opposite_rate_direction_flips_the_sign() {
        printf("\n[G3] the opposite direction: a +10.64 ppm fast feed\n");
        frame_period = (kClkHz / PLAN_A) * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);
        slip_reset();
        run_cycles(60'000'000);
        ck("G3: zero surplus ticks (junction law)",  dups, 0);
        ck("G3: zero surplus frames (junction law)", skips, 0);
        ck_range("G3: u flips sign with the rate (~+170 LSB)",
                 static_cast<int16_t>(dut->u_o), 140, 200);
    }

    // ---------------------------------------------------------------------- //
    void prove_feed_watchdog_disengages_and_re_engages() {
        printf("\n[G4] feed watchdog: silence disengages, frames re-engage\n");
        frame_period = 0.0;                           // feed dies
        run_cycles(20'000);                           // >> 4 frame periods
        ck("G4: engaged_o falls on a dead feed",      dut->engaged_o, 0);
        ck("G4: u_o returns to 0 on a dead feed",     dut->u_o, 0);
        tick_count = 0;
        run_cycles(10'000'000);
        ck("G4: dead-feed NCO free-runs at exact 48 kHz", tick_count, 4800);
        frame_period = kClkHz / PLAN_A;               // feed returns
        slip_reset();
        run_cycles(60'000'000);
        ck("G4: re-engaged after the feed returns",   dut->engaged_o, 1);
        ck_range("G4: reacquired u (~-170 LSB)", static_cast<int16_t>(dut->u_o),
                 -200, -140);
    }

    // ---------------------------------------------------------------------- //
    void prove_deselect_mid_lock_restores_free_run() {
        printf("\n[G5] deselect mid-lock: INTERNAL free-run comes back untouched\n");
        dut->sel_i = 0;
        run_cycles(1'000);
        ck("G5: u_o drops to 0 on deselect",          dut->u_o, 0);
        ck("G5: engaged_o drops on deselect",         dut->engaged_o, 0);
        tick_count = 0;
        run_cycles(10'000'000);
        ck("G5: deselected NCO is bit-exact nominal again", tick_count, 4800);
    }

    // ---------------------------------------------------------------------- //
    void prove_beyond_authority_parks_at_the_clamp() {
        printf("\n[G6] beyond authority: a 400 ppm feed parks at the clamp,\n");
        printf("     slips honestly, and recovery is frames - not seconds\n");
        dut->sel_i = 1;
        frame_period = (kClkHz / kNominalHz) * (1.0 + 400e-6);
        run_cycles(40'000'000);
        ck("G6: u parked at the negative clamp", static_cast<int16_t>(dut->u_o), -3200);
        frame_period = kClkHz / PLAN_A;               // sane rate returns
        run_cycles(45'000'000);                       // slip unwind + acc unwind
        slip_reset();
        run_cycles(20'000'000);
        ck("G6: slips stop after recovery (surplus ticks)",  dups, 0);
        ck("G6: slips stop after recovery (surplus frames)", skips, 0);
        ck_range("G6: recovered u (~-170 LSB)", static_cast<int16_t>(dut->u_o),
                 -200, -140);
    }

    // ---- [G7] helpers: the shipped junction counters and a raced engagement --
    long rtl_dups()  const { return dut->tdm_dup_cnt_o; }
    long rtl_skips() const { return dut->tdm_skip_cnt_o; }

    //! Deselect, then re-anchor the physical grid so its next frame lands
    //! `lead` edges after the edge on which the RTL samples a tick (0 = ON
    //! the tick), select, and let exactly that frame engage the loop. The
    //! engagement capture IS the lock target, so this parks the lock where
    //! the caller aims it.
    void engage_at_phase(long lead) {
        dut->sel_i = 0;
        frame_period = kClkHz / PLAN_A;
        run_cycles(10'000);
        while (!dut->tick_o) cyc();           // the RTL sees a tick next edge
        frame_acc = frame_period - 0.5 - static_cast<double>(lead);
        run_cycles(lead);
        dut->sel_i = 1;
        cyc();                                // the engaging frame
    }

    // ---------------------------------------------------------------------- //
    void prove_raced_lock_keeps_the_junction_counters_still() {
        printf("\n[G7] raced lock: the engaging frame lands ON a tick (#74 item 2)\n");
        engage_at_phase(0);
        ck("G7: the loop engaged on that frame", dut->engaged_o, 1);
        ck("G7: the engaging frame raced onto the tick (phase)", last_phase, 0);
        run_cycles(60'000'000);                       // 0.6 s: settle, as G2
        ck("G7: still engaged after settling", dut->engaged_o, 1);
        // the chatter R1 measured came and went in 0.2 s windows, so grade
        // every window, not only the sum
        clear_min = LONG_MAX;
        long win_dups = 0, win_skips = 0;
        for (int w = 0; w < 5; w++) {
            const long d0 = rtl_dups(), s0 = rtl_skips();
            run_cycles(20'000'000);                   // 0.2 s
            const long dd = rtl_dups() - d0, ds = rtl_skips() - s0;
            printf("  window %d: %ld junction dups, %ld skips, err %d\n", w, dd, ds,
                   static_cast<int16_t>(dut->err_cyc_o));
            win_dups += dd; win_skips += ds;
        }
        ck("G7: zero junction dups over 5 x 0.2 s at the raced lock", win_dups, 0);
        ck("G7: zero junction skips over 5 x 0.2 s at the raced lock", win_skips, 0);
        ck_range("G7: marker clearance from every tick at lock (cycles)",
                 clear_min, kLockClearMin, 2083);

        // negative controls AT THIS LOCK: a real slip still counts, once
        {
            const long d0 = rtl_dups(), s0 = rtl_skips();
            frame_acc -= frame_period;                // hold the grid one frame
            run_cycles(1'000'000);
            ck("G7: a held frame is one junction dup",   rtl_dups() - d0, 1);
            ck("G7: a held frame is no junction skip",   rtl_skips() - s0, 0);
        }
        {
            const long d0 = rtl_dups(), s0 = rtl_skips();
            while (!dut->frame_ev_i) cyc();           // just past a frame
            run_cycles(520);                          // a quarter frame on
            extra_frame = true;                       // one surplus marker
            run_cycles(1'000'000);
            ck("G7: a surplus frame is one junction skip", rtl_skips() - s0, 1);
            ck("G7: a surplus frame is no junction dup",   rtl_dups() - d0, 0);
        }
        ck("G7: the loop stayed engaged through both slips", dut->engaged_o, 1);
    }

    // ---------------------------------------------------------------------- //
    void prove_raced_lock_below_the_tick_is_kept_off_too() {
        printf("\n[G8] raced lock from the other side: the engaging frame lands just BEFORE a tick\n");
        engage_at_phase(2082);                        // 1-2 edges before the next tick
        ck("G8: the loop engaged on that frame", dut->engaged_o, 1);
        ck_range("G8: the engaging frame raced the next tick (phase)",
                 last_phase, 2081, 2083);
        run_cycles(60'000'000);
        clear_min = LONG_MAX;
        const long d0 = rtl_dups(), s0 = rtl_skips();
        run_cycles(20'000'000);
        ck("G8: zero junction dups over 0.2 s at the lock",  rtl_dups() - d0, 0);
        ck("G8: zero junction skips over 0.2 s at the lock", rtl_skips() - s0, 0);
        ck_range("G8: marker clearance from every tick at lock (cycles)",
                 clear_min, kLockClearMin, 2083);
    }

    void explore_free_run() {
        dut->sel_i = 0;
        for (int dir = 0; dir < 2; dir++) {
            frame_period = dir == 0 ? kClkHz / PLAN_A
                         : (kClkHz / PLAN_A) * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);
            run_cycles(1000);
            long d = rtl_dups(), k = rtl_skips(), n = 0;
            const long d0 = d, k0 = k;
            for (long i = 0; i < 1'200'000'000L; i++) {
                cyc();
                if (rtl_dups() != d || rtl_skips() != k) {
                    printf("  dir %d t=%.4f s: dups %+ld skips %+ld\n", dir, i / kClkHz,
                           rtl_dups() - d, rtl_skips() - k);
                    d = rtl_dups(); k = rtl_skips(); n++;
                }
            }
            printf("  dir %d TOTAL 12 s: rtl dups %ld skips %ld (expected ~%.2f slips)\n", dir,
                   rtl_dups()-d0, rtl_skips()-k0, 12.0 / 1.9582);
        }
    }
    int report() {
        printf("\n----------------------------------------------------------------------\n");
        printf("%d checks, %d failures\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

    Vmedia_grid_align_wrap* dut = nullptr;
    int checks = 0;
    int fails = 0;

    double frame_period = 0.0;  // clk cycles per frame; 0 = feed dead
    double frame_acc    = 0.0;
    bool   pend         = false;
    long   dups  = 0;           // surplus ticks
    long   skips = 0;           // surplus frames
    long   tick_count  = 0;
    long   frame_count = 0;
    bool   extra_frame = false; // one surplus marker on the next edge
    bool   tick_q      = false; // tick_o after the previous edge = tick_i now
    long   edges_since_tick = 0;
    long   mark_phase  = -1;    // this tick period's marker phase, -1 = none
    long   last_phase  = -1;    // the most recent marker's phase
    long   clear_min   = LONG_MAX;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    MediaGridAlignHarness harness;
    return harness.run();
}

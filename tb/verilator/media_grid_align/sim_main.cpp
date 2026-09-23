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
// instrument the datapath actually ships. Its coincidence line follows the
// #74 item 2 law: pend carries over.
//
// [G7]-[G9] (#74 item 2) do not trust that copy: they read the counters of
// the REAL KL_chan_map_capture the wrap instantiates on the same marker and
// tick. [G7]/[G8] engage with the marker raced onto the tick and hold the
// counters at zero through the lock, with one edge of marker delivery
// jitter (the root's capture FIFO); a held and a surplus frame there still
// count once each. [G9] drives one slow free-running passage each way.
//
// Sign lesson, pinned here in BOTH rate directions: err > 0 = ticks fast =
// u must go NEGATIVE (the NCO port speaks the servo's "u > 0 = speed up").
// A flipped sign is a runaway - [G2]/[G3] fail loudly, not numerically.

#include <cstdint>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <climits>
#include "../../common/verilator_harness.hpp"
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"

constexpr double kClkHz     = 100e6;   // the 100 MHz fabric clock
constexpr double kNominalHz = 48000.0; // the NCO's exact media rate
constexpr int    kResetCycles = 8;     // clock edges held in reset

constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0; // 47999.4893 Hz
constexpr double kPlanPeriod = kClkHz / PLAN_A;                 // cycles/frame
//! the mirrored feed: +10.64 ppm, as [G3] drives it
constexpr double kFastPeriod = kPlanPeriod * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);
//! [G7]/[G8] clearance floor: the keep-off (2083/128 = 16 cycles) less the
//! lock's own dither and the delivery jitter
constexpr long   kLockClearMin = 12;

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

        prove_deselected_issues_no_command();
        prove_deselected_nco_is_bit_exact_nominal();
        prove_plan_a_ratio_acquires_bounds_and_holds();
        prove_opposite_rate_direction_flips_the_sign();
        prove_feed_watchdog_disengages_and_re_engages();
        prove_deselect_mid_lock_restores_free_run();
        prove_beyond_authority_parks_at_the_clamp();
        prove_a_lock_raced_onto_the_tick_counts_nothing();
        prove_a_lock_raced_before_the_tick_counts_nothing();
        prove_a_free_running_passage_counts_one_slip();

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
        bool fev = surplus_frame || late_frame;
        surplus_frame = false;
        late_frame    = false;
        if (frame_period > 0.0) {
            frame_acc += 1.0;
            if (frame_acc >= frame_period) {
                frame_acc -= frame_period;
                if (marker_jitter && (next_rand() & 1u)) late_frame = true;
                else fev = true;
            }
        }
        dut->frame_ev_i = fev;
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();
        bool tk = dut->tick_o;
        if (fev) frame_count++;
        if (tk)  tick_count++;
        if (fev && !tk)      { if (pend) skips++; pend = true; }
        else if (tk && !fev) { if (!pend) dups++; pend = false; }
        // fev && tk: the tick takes the pending frame, the new one pends
        track_clearance(fev);
        tick_q = tk;
    }
    //! Marker-to-tick clearance as the RTL pairs them: the tick_i an edge
    //! samples is the tick_o the PREVIOUS edge produced, and a marker's
    //! phase is the aligner's own capture (0 on the tick's edge, n edges
    //! after it otherwise). A marker n edges after one tick and m before
    //! the next is min(n, m) clear of the junction's race.
    void track_clearance(bool fev) {
        if (tick_q) {
            if (mark_phase > 0)
                clear_min = std::min(clear_min, edges_since_tick + 1 - mark_phase);
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
    uint32_t next_rand() {                 // xorshift32: a fixed, repeatable draw
        rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5;
        return rng;
    }
    long rtl_dups()  const { return dut->tdm_dup_cnt_o; }
    long rtl_skips() const { return dut->tdm_skip_cnt_o; }
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

    // ---------------------------------------------------------------------- //
    //! Deselect, then re-anchor the physical grid so its next frame lands
    //! `lead` edges after the edge on which the RTL samples a tick (0 = ON
    //! the tick). The frame after this call's return is that frame.
    void anchor_grid(double period, long lead) {
        dut->sel_i = 0;
        marker_jitter = false;
        frame_period = period;
        run_cycles(10'000);
        while (!dut->tick_o) cyc();           // the RTL samples a tick next edge
        frame_acc = frame_period - 0.5 - static_cast<double>(lead);
        run_cycles(lead);
    }
    //! ...and let exactly that frame engage the loop: the engagement
    //! capture is the lock target, so the lock lands where the caller aims
    void engage_at_phase(long lead) {
        anchor_grid(kPlanPeriod, lead);
        dut->sel_i = 1;
        cyc();
    }

    // ---------------------------------------------------------------------- //
    void prove_a_lock_raced_onto_the_tick_counts_nothing() {
        printf("\n[G7] raced lock: the engaging frame lands ON a tick (#74 item 2)\n");
        engage_at_phase(0);
        ck("G7: the loop engaged on that frame", dut->engaged_o, 1);
        ck("G7: the engaging frame raced onto the tick (phase)", last_phase, 0);
        marker_jitter = true;                         // the root's FIFO pop
        long d0 = rtl_dups(), s0 = rtl_skips();
        run_cycles(60'000'000);                       // 0.6 s: settle, as G2
        printf("  acquisition: %ld junction dups, %ld skips\n",
               rtl_dups() - d0, rtl_skips() - s0);
        ck("G7: still engaged after settling", dut->engaged_o, 1);
        // PR #323's [R1] saw the chatter come and go in 0.2 s windows, and
        // it starts only once the integrator has walked the marker onto the
        // tick (~1.4 s after engaging), so eight windows are printed and
        // their sum is graded
        clear_min = LONG_MAX;
        d0 = rtl_dups(); s0 = rtl_skips();
        for (int w = 0; w < 8; w++) {
            const long wd = rtl_dups(), ws = rtl_skips();
            run_cycles(20'000'000);
            printf("  window %d: %ld junction dups, %ld skips, err %d cycles\n", w,
                   rtl_dups() - wd, rtl_skips() - ws,
                   static_cast<int16_t>(dut->err_cyc_o));
        }
        ck("G7: zero junction dups over 8 x 0.2 s at the raced lock",  rtl_dups() - d0, 0);
        ck("G7: zero junction skips over 8 x 0.2 s at the raced lock", rtl_skips() - s0, 0);
        ck_range("G7: marker clearance from every tick at lock (cycles)",
                 clear_min, kLockClearMin, 2083);

        // the negative controls, AT this lock: a real slip still counts once
        d0 = rtl_dups(); s0 = rtl_skips();
        frame_acc -= frame_period;                    // hold the grid one frame
        run_cycles(1'000'000);
        ck("G7: a held frame is one junction dup",   rtl_dups() - d0, 1);
        ck("G7: a held frame is no junction skip",   rtl_skips() - s0, 0);
        d0 = rtl_dups(); s0 = rtl_skips();
        while (!dut->frame_ev_i) cyc();               // just past a frame
        run_cycles(520);                              // a quarter frame on
        surplus_frame = true;
        run_cycles(1'000'000);
        ck("G7: a surplus frame is one junction skip", rtl_skips() - s0, 1);
        ck("G7: a surplus frame is no junction dup",   rtl_dups() - d0, 0);
        ck("G7: the loop stayed engaged through both slips", dut->engaged_o, 1);
    }

    // ---------------------------------------------------------------------- //
    void prove_a_lock_raced_before_the_tick_counts_nothing() {
        printf("\n[G8] raced lock from below: the engaging frame lands just BEFORE a tick\n");
        engage_at_phase(2082);                        // 1-2 edges before the next
        ck("G8: the loop engaged on that frame", dut->engaged_o, 1);
        ck_range("G8: the engaging frame raced the next tick (phase)",
                 last_phase, 2081, 2083);
        marker_jitter = true;
        long d0 = rtl_dups(), s0 = rtl_skips();
        run_cycles(100'000'000);                      // 1 s: this side settles last
        printf("  acquisition: %ld junction dups, %ld skips\n",
               rtl_dups() - d0, rtl_skips() - s0);
        clear_min = LONG_MAX;
        d0 = rtl_dups(); s0 = rtl_skips();
        run_cycles(20'000'000);
        ck("G8: zero junction dups over 0.2 s at the lock",  rtl_dups() - d0, 0);
        ck("G8: zero junction skips over 0.2 s at the lock", rtl_skips() - s0, 0);
        ck_range("G8: marker clearance from every tick at lock (cycles)",
                 clear_min, kLockClearMin, 2083);
    }

    // ---------------------------------------------------------------------- //
    void prove_a_free_running_passage_counts_one_slip() {
        printf("\n[G9] free-running: one slow passage across a tick is ONE slip, its way\n");
        // the plan's slow grid: the marker drifts ~1064 cycles/s later and
        // crosses the tick it starts 20 edges before, once in 0.1 s
        anchor_grid(kPlanPeriod, 2063);
        long d0 = rtl_dups(), s0 = rtl_skips();
        run_cycles(10'000'000);
        ck("G9: a slow grid's passage is one junction dup",   rtl_dups() - d0, 1);
        ck("G9: a slow grid's passage is no junction skip",   rtl_skips() - s0, 0);
        // the mirrored fast grid crosses the tick it starts 20 edges after
        anchor_grid(kFastPeriod, 20);
        d0 = rtl_dups(); s0 = rtl_skips();
        run_cycles(10'000'000);
        ck("G9: a fast grid's passage is one junction skip",  rtl_skips() - s0, 1);
        ck("G9: a fast grid's passage is no junction dup",    rtl_dups() - d0, 0);
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

    // ---- [G7]-[G9]: marker placement and the clearance it keeps --------------
    bool     surplus_frame = false; // one extra marker on the next edge
    bool     late_frame    = false; // a marker the delivery jitter held one edge
    bool     marker_jitter = false; // [G7]/[G8]: each marker 0 or 1 edge late
    uint32_t rng           = 0x74A197u;
    bool     tick_q        = false; // tick_o after the previous edge = tick_i now
    long     edges_since_tick = 0;
    long     mark_phase    = -1;    // this tick period's marker, -1 = none
    long     last_phase    = -1;    // the most recent marker's phase
    long     clear_min     = LONG_MAX;
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    MediaGridAlignHarness harness;
    return harness.run();
}

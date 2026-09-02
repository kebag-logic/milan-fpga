// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_media_grid_align closed over the real KL_media_nco (#74).
//
// The C++ side IS the physical grid: frame_ev_i pulses on a double-precision
// fractional-period model of the TDM fsync (the true 391/1591 divider plan:
// 100 MHz * 391/1591 / 512 = 47,999.4893 Hz, -10.6393 ppm against the NCO's
// exact 48,000.0000 Hz - docs/design/TIME_SYNC.md Plan A, the drift
// tb/verilator/milan_dp/sim_aclk.cpp measures as one slipped sample every
// 1.9582 s). The oracle is the NCO's tick_o: the harness runs its own copy
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
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"

static Vmedia_grid_align_wrap* dut;
static int checks = 0, fails = 0;

static void ck(const char* t, long got, long exp) {
  checks++;
  if (got == exp) printf("  [ ok ] %-52s = %ld\n", t, got);
  else { fails++; printf("  [FAIL] %-52s = %ld (expected %ld)\n", t, got, exp); }
}
static void ck_range(const char* t, long got, long lo, long hi) {
  checks++;
  if (got >= lo && got <= hi)
    printf("  [ ok ] %-52s = %ld (in [%ld, %ld])\n", t, got, lo, hi);
  else { fails++; printf("  [FAIL] %-52s = %ld (outside [%ld, %ld])\n",
                         t, got, lo, hi); }
}

// ---- the physical grid model + the shipped junction law ------------------
static double frame_period = 0.0;  // clk cycles per frame; 0 = feed dead
static double frame_acc    = 0.0;
static bool   pend         = false;
static long   dups = 0, skips = 0; // surplus ticks / surplus frames
static long   tick_count = 0, frame_count = 0;

static void cyc() {
  bool fev = false;
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
}
static void run(long n) { for (long i = 0; i < n; i++) cyc(); }
static void slip_reset() { dups = 0; skips = 0; }

static const double PLAN_A = 100e6 * (391.0 / 1591.0) / 512.0; // 47999.4893 Hz

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vmedia_grid_align_wrap;

  dut->rst_n = 0; dut->sel_i = 0; dut->frame_ev_i = 0;
  for (int i = 0; i < 8; i++) { dut->clk = 0; dut->eval();
                                dut->clk = 1; dut->eval(); }
  dut->rst_n = 1;

  printf("== KL_media_grid_align closed over KL_media_nco (#74) ==\n");

  // -------------------------------------------------------------------- //
  printf("\n[G0] reset / deselected: no command, no engagement\n");
  frame_period = 100e6 / PLAN_A;               // feed alive, sel low
  run(2'000'000);
  ck("G0: u_o stays 0 with sel_i low",        dut->u_o, 0);
  ck("G0: engaged_o stays 0 with sel_i low",  dut->engaged_o, 0);

  // -------------------------------------------------------------------- //
  printf("\n[G1] INTERNAL equivalence: deselected NCO is bit-exact nominal\n");
  tick_count = 0;
  run(10'000'000);                              // 0.1 s
  ck("G1: 4800 ticks in 10M cycles (exact 48 kHz)", tick_count, 4800);

  // -------------------------------------------------------------------- //
  printf("\n[G2] select at the true Plan-A ratio: acquire, bound, hold\n");
  dut->sel_i = 1;
  // acquisition watch: from the engaging frame on, the phase error must
  // never reach one sample - that is what keeps the junction counters at
  // zero THROUGH acquisition, not just after it
  long max_abs_err = 0; bool was_engaged = false;
  slip_reset();
  for (long i = 0; i < 60'000'000; i++) {       // 0.6 s
    cyc();
    if (dut->engaged_o) {
      was_engaged = true;
      long e = (int16_t)dut->err_cyc_o; if (e < 0) e = -e;
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
           (int16_t)dut->u_o, -200, -140);
  ck_range("G2: settled |err| (cycles)", (int16_t)dut->err_cyc_o < 0
           ? -(int16_t)dut->err_cyc_o : (int16_t)dut->err_cyc_o, 0, 60);
  // rate proof on the oracle: engaged ticks now come at the FRAME rate
  tick_count = 0; frame_count = 0;
  run(20'000'000);                              // 0.2 s locked
  ck_range("G2: locked tick count tracks frame count (+/-1)",
           tick_count - frame_count, -1, 1);

  // -------------------------------------------------------------------- //
  printf("\n[G3] the opposite direction: a +10.64 ppm fast feed\n");
  frame_period = (100e6 / PLAN_A) * (PLAN_A / 48000.0) * (PLAN_A / 48000.0);
  slip_reset();
  run(60'000'000);
  ck("G3: zero surplus ticks (junction law)",  dups, 0);
  ck("G3: zero surplus frames (junction law)", skips, 0);
  ck_range("G3: u flips sign with the rate (~+170 LSB)",
           (int16_t)dut->u_o, 140, 200);

  // -------------------------------------------------------------------- //
  printf("\n[G4] feed watchdog: silence disengages, frames re-engage\n");
  frame_period = 0.0;                           // feed dies
  run(20'000);                                  // >> 4 frame periods
  ck("G4: engaged_o falls on a dead feed",      dut->engaged_o, 0);
  ck("G4: u_o returns to 0 on a dead feed",     dut->u_o, 0);
  tick_count = 0;
  run(10'000'000);
  ck("G4: dead-feed NCO free-runs at exact 48 kHz", tick_count, 4800);
  frame_period = 100e6 / PLAN_A;                // feed returns
  slip_reset();
  run(60'000'000);
  ck("G4: re-engaged after the feed returns",   dut->engaged_o, 1);
  ck_range("G4: reacquired u (~-170 LSB)", (int16_t)dut->u_o, -200, -140);

  // -------------------------------------------------------------------- //
  printf("\n[G5] deselect mid-lock: INTERNAL free-run comes back untouched\n");
  dut->sel_i = 0;
  run(1'000);
  ck("G5: u_o drops to 0 on deselect",          dut->u_o, 0);
  ck("G5: engaged_o drops on deselect",         dut->engaged_o, 0);
  tick_count = 0;
  run(10'000'000);
  ck("G5: deselected NCO is bit-exact nominal again", tick_count, 4800);

  // -------------------------------------------------------------------- //
  printf("\n[G6] beyond authority: a 400 ppm feed parks at the clamp,\n");
  printf("     slips honestly, and recovery is frames - not seconds\n");
  dut->sel_i = 1;
  frame_period = (100e6 / 48000.0) * (1.0 + 400e-6);
  run(40'000'000);
  ck("G6: u parked at the negative clamp", (int16_t)dut->u_o, -3200);
  frame_period = 100e6 / PLAN_A;                // sane rate returns
  run(45'000'000);                              // slip unwind + acc unwind
  slip_reset();
  run(20'000'000);
  ck("G6: slips stop after recovery (surplus ticks)",  dups, 0);
  ck("G6: slips stop after recovery (surplus frames)", skips, 0);
  ck_range("G6: recovered u (~-170 LSB)", (int16_t)dut->u_o, -200, -140);

  printf("\n----------------------------------------------------------------------\n");
  printf("%d checks, %d failures\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  delete dut;
  return fails ? 1 : 0;
}

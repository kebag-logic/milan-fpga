// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_aclk - the media-grid ALIGNMENT measurement, at the TRUE clock ratio.
//
// WHY THIS IS ITS OWN BINARY. Every other milan_dp leg toggles clk_audio_i
// (and, since 2026-08-10, clk_tdm_i) 1:1 with axis_clk. That is fine for the
// 380-odd functional checks those legs run - none of them care about the audio
// clock's RATE - but it means the one property the media clock actually has to
// hold cannot be observed anywhere in the tree:
//
//     the TDM word clock and the AAF packet grid must stay ALIGNED
//
// On the shipping board they do not, and the amount by which they do not is a
// compile-time constant, not a tolerance:
//
//   clk_audio = 100 MHz * 23/2 /37 * 34/43 = 100e6 * 391/1591
//             = 24,575,738.5292 Hz            (PLAN A, milan_soc.py:363)
//   clk_tdm   = clk_audio                     (milan_soc.py:5012 nulls
//                                              audio_tdm_hz at 24.576 MHz,
//                                              :5224 binds ClockSignal("audio"))
//   fsync     = clk_tdm / (2*8*32) = /512     = 47,999.4893 Hz
//   media_tick_p                              = 48,000.0000 Hz exactly
//                                              (KL_media_nco off axis_clk)
//   => -10.6393 ppm, one whole sample of slip every 1.9582 s
//
// 391/1591 is exact and reduced (23*34 / (2*37*43)), and BOTH clocks come off
// the same 100 MHz oscillator, so this is a pure divider-plan constant with no
// oscillator noise in it. That is exactly why an integer-ratio model is
// faithful rather than an approximation - there is nothing stochastic to miss.
//
// WHAT IT DOES NOT DO. It does not wait for a whole sample of slip: that is
// 195,815,385 axis cycles, minutes of wall clock on this design. It measures
// the DRIFT RATE from the two periods and reports ppm, which needs ~1e7 cycles
// for 0.1 ppm resolution. The silicon counterpart is AX7101 J11.8 (tdm_fsync_o)
// against J11.9 (media_lrclk_o) on a two-channel probe.

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"

#include <cstdio>
#include <cstdint>
#include <cmath>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, unsigned long got, unsigned long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%lu exp=%lu\n", what, got, exp); }
    else            { printf("  [ok]   %-52s = %lu\n", what, got); }
}

// ---------------------------------------------------------------------- //
//  The fractional-N audio clock.
//
//  Advance the audio phase by 391 on every axis HALF cycle and toggle on
//  wrap against 1591: that is 2*391/1591 toggles per axis cycle = 391/1591
//  audio cycles per axis cycle, exactly. No rounding, no drift of its own -
//  the only error is the one clk_audio edge of quantisation any digital
//  model of a slower clock has, and it does not accumulate.
// ---------------------------------------------------------------------- //
static const long AUD_NUM = 391;    // clk_audio = axis * AUD_NUM / AUD_DEN
static const long AUD_DEN = 1591;

static long acc = 0;
static int  aud = 0;
static long axis_cycle = 0;

static void half() {
    acc += AUD_NUM;
    if (acc >= AUD_DEN) { acc -= AUD_DEN; aud ^= 1; }
    dut->clk_audio_i = aud;
    dut->clk_tdm_i   = aud;
}

static void step() {
    dut->axis_clk = 0; dut->gtx_clk = 0; half(); dut->eval();
    dut->axis_clk = 1; dut->gtx_clk = 1; half(); dut->eval();
    axis_cycle++;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("======================================================================\n");
    printf("media-grid alignment at the TRUE ratio: clk_audio = axis * %ld/%ld\n",
           AUD_NUM, AUD_DEN);
    printf("======================================================================\n");

    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    for (int i = 0; i < 64; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 512; i++) step();

    // ---- measure -------------------------------------------------------
    // Record the first and last edge of each grid and count them; the period
    // is (last-first)/(n-1), which is exact to one axis cycle regardless of
    // where the window happened to start.
    const long RUN = 10000000;          // ~0.1 s of board time, ~4800 grid ticks

    long m_first = -1, m_last = -1, m_n = 0;
    long f_first = -1, f_last = -1, f_n = 0;
    int  f_prev = dut->tdm_fsync_o;

    for (long i = 0; i < RUN; i++) {
        step();
        if (dut->rootp->milan_datapath__DOT__media_tick_p) {
            if (m_first < 0) m_first = axis_cycle;
            m_last = axis_cycle; m_n++;
        }
        const int f = dut->tdm_fsync_o;
        if (f && !f_prev) {                      // rising edge of the frame sync
            if (f_first < 0) f_first = axis_cycle;
            f_last = axis_cycle; f_n++;
        }
        f_prev = f;
    }

    printf("\n  media_tick_p : %ld ticks, first %ld last %ld\n", m_n, m_first, m_last);
    printf("  tdm_fsync_o  : %ld frames, first %ld last %ld\n", f_n, f_first, f_last);

    ck("media grid ticked", m_n > 2, 1);
    ck("TDM master framed", f_n > 2, 1);
    if (m_n <= 2 || f_n <= 2) {                  // vacuity guard: no rate to report
        printf("\n  [FAIL] nothing to measure - the ratio test needs both grids live\n");
        printf("media_aclk: %ld checks, %ld failures\n", checks, fails + 1);
        delete dut; return 1;
    }

    const double t_media = double(m_last - m_first) / double(m_n - 1);
    const double t_fsync = double(f_last - f_first) / double(f_n - 1);
    // fsync rate relative to the media grid, in ppm. NEGATIVE = fsync slower.
    const double ppm = (t_media / t_fsync - 1.0) * 1e6;

    // The closed form this is graded against, from the divider plan alone.
    const double t_media_exp = 100e6 / 48000.0;                       // 2083.3333
    const double t_fsync_exp = 512.0 * double(AUD_DEN) / double(AUD_NUM);
    const double ppm_exp = (t_media_exp / t_fsync_exp - 1.0) * 1e6;   // -10.6393

    printf("\n  media period : %10.4f axis cycles (exact %10.4f)\n", t_media, t_media_exp);
    printf("  fsync period : %10.4f axis cycles (exact %10.4f)\n", t_fsync, t_fsync_exp);
    printf("  MEASURED     : %+9.4f ppm   (closed form %+9.4f ppm)\n", ppm, ppm_exp);
    printf("  one sample of slip every %.4f s\n", 1.0 / (48000.0 * std::fabs(ppm) * 1e-6));

    // Resolution: one axis cycle of quantisation on each period over ~4800
    // ticks is about 1e6/(4800*2083) = 0.10 ppm, so a 0.5 ppm gate is four
    // sigma of the measurement and still far tighter than the 10.64 it must
    // distinguish from zero.
    ck("fsync is SLOWER than the media grid (the sign of the defect)",
       ppm < 0.0, 1);
    ck("drift rate matches the divider plan within 0.5 ppm",
       std::fabs(ppm - ppm_exp) < 0.5, 1);
    ck("the two grids are NOT aligned (this is the open finding)",
       std::fabs(ppm) > 1.0, 1);

    printf("\n----------------------------------------------------------------------\n");
    printf("media_aclk: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}

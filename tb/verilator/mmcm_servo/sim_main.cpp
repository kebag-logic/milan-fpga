// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_mmcm_drp_servo unit harness against the behavioral MMCME2 model
// (mmcm_model.h: DRDY latency, 12-PSCLK PSDONE, step physics 16.9 ps =
// 1/(56*F_VCO) at the silicon VCO 1056.7568 MHz).
//
// Cases:
//   U0  clock_source != 2  -> ZERO DRP and ZERO PS activity
//   U1  activation         -> DRP read-VERIFY only (2 reads, 0 writes)
//   U2  lock from +100 ppm -> LOCKED, effective clock within 3 ppm of talker
//   U3  bounded step       -> per-window trim delta <= SLEW_MAX, PS protocol clean
//   U4  step response      -> talker step re-locks per the PI constants
//   U5  holdover           -> CRF unlock freezes trim, keeps the held rate
//   U6  lock from -100 ppm (fresh engage, opposite sign)
//   U7  auto_repair OFF    -> mismatch flagged, 0 writes, still locks
//   U8  auto_repair ON     -> XAPP888 sequence: PS quiesced, RST held around
//       power+RMW writes, reserved bits preserved, relock waited
//
// Sim-compressed servo params (-G): 125 us tick, 4 ms window; the ns/512ms
// CSR unit scale is preserved by NORM_SHIFT so crf_rate_i uses REAL units.

#include "VKL_mmcm_drp_servo.h"
#include "verilated.h"
#include "mmcm_model.h"
#include <cstdio>
#include <cstdint>
#include <cmath>

static VKL_mmcm_drp_servo* dut;
static MmcmModel mm;
static long checks = 0, fails = 0;
static void ck(const char* w, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", w, got, exp); }
    else            printf("  [ ok ] %-52s = %ld\n", w, got);
}
static void ckr(const char* w, double got, double lo, double hi) {
    checks++;
    if (got < lo || got > hi) { fails++; printf("  [FAIL] %-52s got=%.3f exp=[%.3f,%.3f]\n", w, got, lo, hi); }
    else            printf("  [ ok ] %-52s = %.3f\n", w, got);
}

// ---- clocks (femtosecond wheel) ------------------------------------------
static double t_fs = 0;
static double next_i = 10000e3, next_p = 2500e3, next_a = 12345e3;
static const double HALF_I = 10000e3;         // clk_i 50 MHz
static const double HALF_P = 2500e3;          // ps_clk 200 MHz
// audio base: 24.576 MHz - 10.64 ppm (the integer two-stage MMCM plan)
static const double BASE_PPM = -10.64;
static const double HALF_A0 = 0.5 * (1e15 / 24.576e6) * (1.0 - BASE_PPM * 1e-6);
static double base_a = 12345e3;               // un-shifted audio edge grid

static int state()  { return (int)(dut->status_o & 7); }
static int16_t trim(){ return (int16_t)(dut->status_o >> 16); }

static void tick_one() {
    if (next_i <= next_p && next_i <= next_a) {
        t_fs = next_i; next_i += HALF_I;
        dut->clk_i ^= 1;
        if (dut->clk_i) dut->ptp_now_i = (uint64_t)(t_fs / 1e6);
        dut->eval();
        if (dut->clk_i) {   // registered model side of the DRP/reset
            mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o,
                         dut->drp_di_o, dut->mmcm_rst_o);
            dut->drp_do_i      = mm.dout;
            dut->drp_rdy_i     = mm.drdy;
            dut->mmcm_locked_i = mm.locked;
        }
    } else if (next_p <= next_a) {
        t_fs = next_p; next_p += HALF_P;
        dut->ps_clk_i ^= 1;
        dut->eval();
        if (dut->ps_clk_i) {
            mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
            dut->ps_done_i = mm.psdone;
        }
    } else {
        t_fs = next_a;
        base_a += HALF_A0;
        next_a = base_a + mm.audio_adj_fs;    // PS steps shift every edge
        if (next_a <= t_fs) next_a = t_fs + 1e3;
        dut->clk_audio_i ^= 1;
        dut->eval();
    }
}
static void run_ms(double ms) {
    double te = t_fs + ms * 1e12;
    while (t_fs < te) tick_one();
}
static int32_t rate_for_ppm(double ppm) {   // KL_crf_rx rate_o for a talker offset
    return (int32_t)llround(512e6 * (1.0 / (1.0 + ppm * 1e-6) - 1.0));
}
// effective audio clock offset vs nominal, measured from the model physics
static double eff_ppm_meas(double ms) {
    double a0 = mm.audio_adj_fs, t0 = t_fs;
    run_ms(ms);
    return BASE_PPM - 1e6 * (mm.audio_adj_fs - a0) / (t_fs - t0);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_mmcm_drp_servo;

    // expected CLKOUT0 config in the model (matches the servo defaults)
    mm.regs[0x08] = 0x0595;
    mm.regs[0x09] = 0x0080;

    dut->rst_n = 0; dut->clk_src_i = 0; dut->crf_locked_i = 0;
    dut->crf_rate_i = 0; dut->auto_repair_i = 0;
    dut->mmcm_locked_i = 1;
    run_ms(0.01);
    dut->rst_n = 1;

    printf("[U0] clock_source != 2: fully inert\n");
    run_ms(10);
    ck("[U0] state IDLE", state(), 0);
    ck("[U0] zero DRP accesses", mm.drp_reads + mm.drp_writes, 0);
    ck("[U0] zero PS operations", mm.ps_ops, 0);
    ck("[U0] trim 0", trim(), 0);

    printf("[U1] activation: DRP read-verify only\n");
    dut->clk_src_i = 2; dut->crf_locked_i = 1;
    dut->crf_rate_i = rate_for_ppm(+100.0);      // talker +100 ppm
    run_ms(1);
    ck("[U1] verify reads = 2", mm.drp_reads, 2);
    ck("[U1] verify writes = 0", mm.drp_writes, 0);
    ck("[U1] verified flag", (dut->status_o >> 3) & 1, 1);
    ck("[U1] no mismatch", (dut->status_o >> 4) & 1, 0);

    printf("[U2] lock from +100 ppm talker\n");
    {
        // track per-window trim slew while acquiring (U3 evidence)
        int16_t tprev = trim(); long max_dtrim = 0; double tmark = t_fs;
        long guard = 0;
        while (state() != 4 && guard < 200) {   // LOCKED
            run_ms(1);
            if (t_fs - tmark >= 4e12) {         // once per 4 ms window
                long d = labs((long)trim() - (long)tprev);
                if (d > max_dtrim) max_dtrim = d;
                tprev = trim(); tmark = t_fs;
            }
            guard++;
        }
        ck("[U2] reached LOCKED", state(), 4);
        double eff = eff_ppm_meas(20.0);
        ckr("[U2] effective clock ppm ~ talker (+100)", eff, 97.0, 103.0);
        ckr("[U2] trim readout ~ +110.6 ppm (x16)", trim(), 1600.0, 1950.0);
        printf("[U3] bounded step + PS protocol\n");
        ck("[U3] per-window trim step <= SLEW (100 ppm x16)", max_dtrim <= 1600 + 64, 1);
        ck("[U3] no PSEN while shift in flight", mm.ps_viol, 0);
        ck("[U3] no PS during DRP reset", mm.ps_during_drp_rst, 0);
    }

    printf("[U4] step response: talker +100 -> +80 ppm\n");
    dut->crf_rate_i = rate_for_ppm(+80.0);
    {
        long guard = 0;
        run_ms(8);                               // leave the settled point
        while (state() != 4 && guard < 100) { run_ms(1); guard++; }
        ck("[U4] re-locked after step", state(), 4);
        ck("[U4] re-lock within PI budget (<48 ms = 12 windows)", guard < 48, 1);
        double eff = eff_ppm_meas(20.0);
        ckr("[U4] effective clock ppm ~ talker (+80)", eff, 77.0, 83.0);
    }

    printf("[U5] holdover on CRF unlock\n");
    {
        dut->crf_locked_i = 0;
        run_ms(6);
        ck("[U5] state HOLDOVER", state(), 5);
        int16_t t0 = trim();
        double eff = eff_ppm_meas(20.0);
        ck("[U5] trim frozen across holdover", trim(), t0);
        ckr("[U5] held rate ~ last talker (+80)", eff, 76.0, 84.0);
        dut->crf_locked_i = 1;
        long guard = 0;
        while (state() != 4 && guard < 100) { run_ms(1); guard++; }
        ck("[U5] relock after CRF returns", state(), 4);
    }

    printf("[U6] deselect + fresh lock from -100 ppm\n");
    {
        dut->clk_src_i = 0;
        run_ms(3);
        ck("[U6] back to IDLE", state(), 0);
        ck("[U6] trim 0 in IDLE", trim(), 0);
        long ops0 = mm.ps_ops;
        run_ms(5);
        ck("[U6] PS silent in IDLE", mm.ps_ops - ops0, 0);
        dut->crf_rate_i = rate_for_ppm(-100.0);
        dut->clk_src_i = 2;
        long guard = 0;
        while (state() != 4 && guard < 200) { run_ms(1); guard++; }
        ck("[U6] locked from -100 ppm", state(), 4);
        double eff = eff_ppm_meas(20.0);
        ckr("[U6] effective clock ppm ~ talker (-100)", eff, -103.0, -97.0);
        ckr("[U6] trim ~ -89.4 ppm (x16)", trim(), -1600.0, -1250.0);
    }

    printf("[U7] config mismatch, auto_repair OFF: informative only\n");
    {
        dut->clk_src_i = 0; run_ms(3);
        mm.regs[0x08] = 0x1234;                  // corrupt HIGH/LOW cone
        long w0 = mm.drp_writes;
        dut->clk_src_i = 2;
        run_ms(2);
        ck("[U7] mismatch flagged", (dut->status_o >> 4) & 1, 1);
        ck("[U7] verified NOT set", (dut->status_o >> 3) & 1, 0);
        ck("[U7] zero DRP writes", mm.drp_writes - w0, 0);
        long guard = 0;
        while (state() != 4 && guard < 200) { run_ms(1); guard++; }
        ck("[U7] PS servo still locks on the live config", state(), 4);
    }

    printf("[U8] auto_repair ON: full XAPP888 safe sequence\n");
    {
        dut->clk_src_i = 0; run_ms(3);
        // corrupt the fields AND plant junk in the RESERVED bits that the
        // RMW must preserve (ClkReg1 [12], ClkReg2 [15] - XAPP888 Tables 1/2)
        mm.regs[0x08] = 0x1234 | 0x1000;
        mm.regs[0x09] = 0x0700 | 0x8000;
        mm.regs[0x28] = 0x0000;
        long w0 = mm.drp_writes, ops0 = mm.ps_ops;
        dut->auto_repair_i = 1;
        dut->clk_src_i = 2;
        long guard = 0;
        while (state() != 3 && state() != 4 && guard < 400) { run_ms(1); guard++; }
        ck("[U8] repair completed (ACQUIRE/LOCKED)", state() == 3 || state() == 4, 1);
        ck("[U8] power reg written 0xFFFF (XAPP888 T14)", mm.regs[0x28], 0xFFFF);
        ck("[U8] ClkReg1 repaired, RESERVED[12] preserved", mm.regs[0x08], 0x0595 | 0x1000);
        ck("[U8] ClkReg2 repaired, RESERVED[15] preserved", mm.regs[0x09], 0x0080 | 0x8000);
        ck("[U8] writes under reset only (safe seq)", mm.writes_wo_rst, 0);
        ck("[U8] no PS during reconfiguration", mm.ps_during_drp_rst, 0);
        ck("[U8] mmcm reset released", dut->mmcm_rst_o, 0);
        ck("[U8] relock seen (LOCKED synced)", (dut->status_o >> 5) & 1, 1);
        (void)w0; (void)ops0;
        while (state() != 4 && guard < 600) { run_ms(1); guard++; }
        ck("[U8] locks after repair", state(), 4);
    }

    printf("======================================================================\n");
    printf("KL_mmcm_drp_servo: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}

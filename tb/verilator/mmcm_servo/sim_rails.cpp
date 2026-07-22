// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Rails-cease proof: KL_i2s_playback + KL_mmcm_drp_servo closed loop
// (rails_wrap.sv) against the behavioral MMCM model.
//
//   R0 (control, clock_source = 0): talker +1000 ppm vs the free-running
//      audio clock -> the historical drift-lottery: the 16-pair FIFO pins
//      full and sheds pairs (overrun rail events accumulate). Servo inert.
//   R1 (servo, clock_source = 2): identical stimulus; the servo pulls the
//      audio clock onto the talker rate -> ZERO rail events after settle.
//
// The model uses 10x-sized PS steps (169 ps) with the wrapper's matching
// gain/authority overrides so seconds of media time simulate quickly; the
// loop math (units, PI, window normalization) is the silicon math.

#include "Vrails_wrap.h"
#include "verilated.h"
#include "mmcm_model.h"
#include <cstdio>
#include <cstdint>
#include <cmath>

static Vrails_wrap* dut;
static MmcmModel mm;
static long checks = 0, fails = 0;
static void ck(const char* w, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", w, got, exp); }
    else            printf("  [ ok ] %-52s = %ld\n", w, got);
}

static const double TALKER_PPM = 1000.0;      // within the modeled authority
static const double BASE_PPM   = -10.64;      // integer two-stage MMCM plan

static double t_fs = 0;
static double next_i = 10000e3, next_p = 5000e3, next_a = 12345e3;
static const double HALF_I = 10000e3;         // clk_i 50 MHz
static const double HALF_P = 5000e3;          // ps_clk 100 MHz (model)
static const double HALF_A0 = 0.5 * (1e15 / 24.576e6) * (1.0 - BASE_PPM * 1e-6);
static double base_a = 12345e3;

// talker feed: 6-sample PDU bursts on the talker's own +1000 ppm grid
static double next_pdu_fs = 3e9;              // first PDU at 3 us
static const double PDU_FS = 6.0 * (1e15 / 48000.0) / (1.0 + TALKER_PPM * 1e-6);
static int burst_left = 0;

static void tick_one() {
    if (next_i <= next_p && next_i <= next_a) {
        t_fs = next_i; next_i += HALF_I;
        dut->clk_i ^= 1;
        if (dut->clk_i) {
            dut->ptp_now_i = (uint64_t)(t_fs / 1e6);
            // feeder (one beat per clk_i cycle while a burst is open)
            if (burst_left == 0 && t_fs >= next_pdu_fs) {
                burst_left = 6; next_pdu_fs += PDU_FS;
            }
            if (burst_left > 0 && !dut->pcm_tvalid_i) {
                dut->pcm_tdata_i  = 0x0011223300445566ull;
                dut->pcm_tvalid_i = 1;
                dut->pcm_tlast_i  = (burst_left == 1);
                burst_left--;
            } else {
                dut->pcm_tvalid_i = 0;
                dut->pcm_tlast_i  = 0;
            }
        }
        dut->eval();
        if (dut->clk_i) {
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
        next_a = base_a + mm.audio_adj_fs;
        if (next_a <= t_fs) next_a = t_fs + 1e3;
        dut->clk_audio_i ^= 1;
        dut->eval();
    }
}
static void run_ms(double ms) {
    double te = t_fs + ms * 1e12;
    while (t_fs < te) tick_one();
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vrails_wrap;
    mm.step_fs = 169000.0;                    // 10x model step (see header)
    mm.regs[0x08] = 0x0595; mm.regs[0x09] = 0x0080;

    const int32_t rate = (int32_t)llround(512e6 * (1.0/(1.0 + TALKER_PPM*1e-6) - 1.0));

    auto reset_dut = [&](int clk_src) {
        dut->rst_n = 0; dut->clk_src_i = 0; dut->crf_locked_i = 0;
        dut->pcm_tvalid_i = 0; dut->pcm_tlast_i = 0;
        dut->wire_chans_i = 2; dut->crf_rate_i = rate;
        dut->mmcm_locked_i = 1;
        run_ms(0.05);
        dut->rst_n = 1;
        dut->clk_src_i = (uint16_t)clk_src;
        dut->crf_locked_i = 1;
        burst_left = 0; next_pdu_fs = t_fs + 3e9;
    };

    // ---- R0: control (servo deselected) --------------------------------
    printf("[R0] control run: free-running clock, talker %+.0f ppm\n", TALKER_PPM);
    reset_dut(0);
    run_ms(150);                               // boot prefill + pin to a rail
    long over0 = dut->overruns_o, under0 = dut->underruns_o;
    long ps0 = mm.ps_ops, drp0 = mm.drp_reads + mm.drp_writes;
    run_ms(500);
    long over_ctrl  = (long)dut->overruns_o  - over0;
    long under_ctrl = (long)dut->underruns_o - under0;
    printf("  control window: +%ld overruns, +%ld underruns\n", over_ctrl, under_ctrl);
    ck("[R0] drift-lottery rail events occur (>= 2)", (over_ctrl + under_ctrl) >= 2, 1);
    ck("[R0] servo inert: zero PS ops", mm.ps_ops - ps0, 0);
    ck("[R0] servo inert: zero DRP accesses", (mm.drp_reads + mm.drp_writes) - drp0, 0);

    // ---- R1: servo in loop ---------------------------------------------
    printf("[R1] servo run: clock_source = 2 (CRF), same stimulus\n");
    reset_dut(2);
    run_ms(150);                               // verify + acquire + settle
    ck("[R1] servo LOCKED", (long)(dut->status_o & 7), 4);
    {
        int16_t tr = (int16_t)(dut->status_o >> 16);
        // u carries the STEP command, so with the 10x model step and
        // GAIN_NUM=1 (true per-tick gain 0.74 steps/u<<9) the converged
        // u = required_steps_per_tick * 512 = (1010.64e-6/1.69e-10 /8000)
        //   * 512 = 382.7k -> trim = u>>5 ~ 11960. (On silicon GAIN_NUM=59
        //   is within 0.3% so the trim readout IS the applied ppm x16.)
        ck("[R1] trim tracks the +1010.6 ppm correction (model gain)",
           tr > 11200 && tr < 12700, 1);
    }
    long over1 = dut->overruns_o, under1 = dut->underruns_o;
    run_ms(700);
    long over_srv  = (long)dut->overruns_o  - over1;
    long under_srv = (long)dut->underruns_o - under1;
    printf("  servo window: +%ld overruns, +%ld underruns\n", over_srv, under_srv);
    ck("[R1] rail events CEASE (zero overruns)", over_srv, 0);
    ck("[R1] rail events CEASE (zero underruns)", under_srv, 0);
    ck("[R1] still LOCKED at end", (long)(dut->status_o & 7), 4);

    printf("======================================================================\n");
    printf("mmcm_servo rails: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}

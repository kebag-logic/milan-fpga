/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_talker_diag_ctx - Milan v1.2 Table 5.4, per
 * Stream Output, with the clause's exact semantics:
 *
 *  - STREAM_START/STOP count edges of ONE level, so START == STOP or
 *    STOP+1 always (the clause's stated invariant);
 *  - MEDIA_RESET / TIMESTAMP_UNCERTAIN / FRAMES_TX are per-OBSERVATION-
 *    INTERVAL counts: eight PDUs inside one interval move FRAMES_TX by
 *    EXACTLY ONE (a raw frame total here would read 8000x off at the real
 *    frame rate - the pre-2026-07-28 behaviour);
 *  - TIMESTAMP_UNCERTAIN counts intervals in which tu was set ON A
 *    TRANSMITTED PDU - tu high with nothing sent counts nothing (the
 *    difference from the free-running CLKV_TUCNT);
 *  - all three interval counters reset to 0 each time the talker starts
 *    streaming.
 *
 * TICK_CYC_P is 64 in this build; a "period" below is 64 clk cycles.
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vtkdiag_tb_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vtkdiag_tb_top* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-56s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ok]   %-56s = 0x%llx\n", what, (unsigned long long)got);
    }
}

static void step() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void cyc(int n) { for (int i = 0; i < n; i++) step(); }
// one full observation interval, with margin for the divider phase
static void interval() { cyc(70); }

static void frame(int idx, int tu) {
    dut->tu_i = tu; dut->frame_p_i = 1; dut->frame_idx_i = idx;
    step();
    dut->frame_p_i = 0;
}
static void rd(int idx) { dut->rd_idx_i = idx; dut->eval(); }

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vtkdiag_tb_top;
    dut->rst_n = 0; dut->streaming_i = 0; dut->frame_p_i = 0;
    dut->tu_i = 0; dut->mr_p_i = 0; dut->mr_idx_i = 0; dut->rd_idx_i = 0;
    cyc(4); dut->rst_n = 1; cyc(4);

    printf("[T1] reset state + the START/STOP invariant at zero\n");
    rd(0);
    ck("T1 all five zero", dut->rd_start_o | dut->rd_stop_o | dut->rd_mreset_o
                         | dut->rd_tu_o | dut->rd_ftx_o, 0);

    printf("[T2] START/STOP edge counting (one level, invariant holds)\n");
    dut->streaming_i = 0b001; cyc(3); rd(0);
    ck("T2 rise -> START 1", dut->rd_start_o, 1);
    ck("T2 ... STOP still 0 (START == STOP+1 while streaming)",
       dut->rd_stop_o, 0);
    dut->streaming_i = 0b000; cyc(3); rd(0);
    ck("T2 fall -> STOP 1 (START == STOP while stopped)", dut->rd_stop_o, 1);

    printf("[T3] FRAMES_TX is an INTERVAL count, not a frame total\n");
    dut->streaming_i = 0b001; cyc(3);        // start (resets the three)
    for (int f = 0; f < 8; f++) frame(0, 0); // 8 PDUs, ONE interval
    interval(); rd(0);
    ck("T3 8 PDUs in one interval -> FRAMES_TX 1 (not 8)", dut->rd_ftx_o, 1);
    frame(0, 0); interval();
    frame(0, 0); interval(); rd(0);
    ck("T3 two more active intervals -> 3", dut->rd_ftx_o, 3);
    interval(); interval(); rd(0);
    ck("T3 idle intervals do not count", dut->rd_ftx_o, 3);

    printf("[T4] TIMESTAMP_UNCERTAIN qualifies tu BY TRANSMISSION\n");
    dut->tu_i = 1; interval(); interval(); rd(0);
    ck("T4 tu high, nothing sent -> no count", dut->rd_tu_o, 0);
    frame(0, 1); interval(); rd(0);
    ck("T4 tu on a TRANSMITTED PDU -> 1", dut->rd_tu_o, 1);
    dut->tu_i = 0;
    frame(0, 0); interval(); rd(0);
    ck("T4 clean interval leaves it", dut->rd_tu_o, 1);

    printf("[T5] reset-on-start zeroes the three interval counters\n");
    rd(0);
    { uint64_t s0 = dut->rd_start_o;
      dut->streaming_i = 0b000; cyc(3);
      dut->streaming_i = 0b001; cyc(3); rd(0);
      ck("T5 START advanced", dut->rd_start_o, s0 + 1); }
    ck("T5 FRAMES_TX reset on start (Table 5.4)", dut->rd_ftx_o, 0);
    ck("T5 TIMESTAMP_UNCERTAIN reset on start", dut->rd_tu_o, 0);
    ck("T5 MEDIA_RESET reset on start", dut->rd_mreset_o, 0);

    printf("[T6] per-context isolation + the CRF context (index 2)\n");
    frame(2, 0); interval();
    rd(0);
    ck("T6 ctx0 unmoved by ctx2 frames", dut->rd_ftx_o, 0);
    rd(2);
    ck("T6 ctx2 counted its own interval", dut->rd_ftx_o, 1);
    ck("T6 ctx2 never started (level low) -> START 0", dut->rd_start_o, 0);

    printf("[T7] the read port is combinational per index\n");
    rd(0); uint64_t a = dut->rd_start_o;
    rd(2); uint64_t b = dut->rd_start_o;
    ck("T7 idx swap changes the view same-eval", (a != b) ? 1 : 0, 1);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}

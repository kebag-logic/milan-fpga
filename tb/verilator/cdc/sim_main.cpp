/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for the open CDC primitives cdc_pulse.sv and
 * cdc_handshake.sv (Track 1.4 — replacing xpm_cdc_pulse / xpm_cdc_handshake).
 *
 * Drives two INDEPENDENT clocks (src half-period 2, dest half-period 3 => async)
 * and checks: every source pulse produces exactly one destination pulse; each
 * value handed to the handshake arrives byte-exact in the destination domain with
 * a dest_req pulse and the src_rcv acknowledge returns to the source.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vcdc_tb_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vcdc_tb_top* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-28s got=0x%llx exp=0x%llx\n", what,
                                       (unsigned long long)got, (unsigned long long)exp); }
}

// two asynchronous clocks: src toggles every SRC_HP ticks, dest every DST_HP
static const int SRC_HP = 2, DST_HP = 3;
static uint64_t T = 0;
static bool src_rose = false, dest_rose = false;

static void step() {
    bool sp = dut->src_clk, dp = dut->dest_clk;
    T++;
    if (T % SRC_HP == 0) dut->src_clk = !dut->src_clk;
    if (T % DST_HP == 0) dut->dest_clk = !dut->dest_clk;
    dut->eval();
    src_rose  = (!sp && dut->src_clk);
    dest_rose = (!dp && dut->dest_clk);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vcdc_tb_top;

    dut->src_clk = 0; dut->dest_clk = 0;
    dut->src_rst_n = 0; dut->dest_rst_n = 0;
    dut->p_src_pulse = 0; dut->h_src_in = 0; dut->h_src_send = 0;
    for (int i = 0; i < 40; i++) step();
    dut->src_rst_n = 1; dut->dest_rst_n = 1;
    for (int i = 0; i < 20; i++) step();

    printf("== cdc_pulse + cdc_handshake harness (async 2:3 clocks) ==\n");

    // ---- pulse CDC: N source pulses -> N destination pulses ----
    const int N = 12;
    int dest_pulses = 0;
    for (int n = 0; n < N; n++) {
        dut->p_src_pulse = 1;
        do { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; } while (!src_rose);
        dut->p_src_pulse = 0;                       // exactly one src-cycle pulse
        for (int g = 0; g < 12 * SRC_HP; g++) { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; }
    }
    for (int g = 0; g < 60; g++) { step(); if (dest_rose && dut->p_dest_pulse) dest_pulses++; }
    ck("dest pulse count == src", dest_pulses, N);
    printf("  [%s] pulse CDC: %d/%d pulses crossed\n", dest_pulses == N ? "PASS" : "FAIL", dest_pulses, N);

    // ---- value CDC: each value crosses byte-exact with req + rcv ----
    const uint64_t vals[] = { 0x1122334455667788ULL, 0xDEADBEEFCAFEF00DULL,
                              0x0000000000000001ULL, 0xFFFFFFFFFFFFFFFFULL,
                              0x0102030405060708ULL };
    for (uint64_t v : vals) {
        dut->h_src_in = v;
        dut->h_src_send = 1;                        // rising edge starts the transfer
        bool got_req = false, got_rcv = false; uint64_t out = 0;
        for (int c = 0; c < 400 && !(got_req && got_rcv); c++) {
            step();
            if (dest_rose && dut->h_dest_req) { got_req = true; out = dut->h_dest_out; }
            if (src_rose  && dut->h_src_rcv)  got_rcv = true;
        }
        ck("handshake dest_req", got_req ? 1 : 0, 1);
        ck("handshake value",    out, v);
        ck("handshake src_rcv",  got_rcv ? 1 : 0, 1);
        dut->h_src_send = 0;                         // drop send; gap before next
        for (int g = 0; g < 12; g++) step();
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}

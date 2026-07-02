/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for ptp_csr_sync.sv — the CSR<->PHC clock-
 * domain crossing (REQ-CSR-03). Guards the settime/adjtime payload-alignment
 * fix: when the synchronised command pulse (t_cmd_load / t_cmd_adjust) reaches
 * the counter, the accompanying payload (t_tod_wr / t_offset) must already hold
 * the value software wrote — never a stale/zero capture.
 *
 * Both clocks are driven together (functional check of the alignment, not async
 * metastability). Also checks: exactly one command pulse per software command,
 * and the snapshot return path (t_tod_snapshot -> a_tod_rd + a_tod_rd_valid).
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vptp_csr_sync.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static Vptp_csr_sync* dut;
static long fails = 0, checks = 0;

static void step() {           // advance both domains one (shared) cycle
    dut->aclk = 0; dut->ts_clk = 0; dut->eval();
    dut->aclk = 1; dut->ts_clk = 1; dut->eval();
}
static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-28s got=0x%llx exp=0x%llx\n", what,
                                      (unsigned long long)got, (unsigned long long)exp); }
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vptp_csr_sync;

    dut->aresetn = 0; dut->ts_resetn = 0;
    dut->a_enable = 1; dut->a_incr = 0x08000000; dut->a_adj = 0;
    dut->a_tod_wr = 0; dut->a_offset = 0;
    dut->a_cmd_load = 0; dut->a_cmd_adjust = 0; dut->a_cmd_snapshot = 0;
    dut->t_tod_snapshot = 0; dut->t_tod_snapshot_valid = 0;
    for (int i = 0; i < 6; i++) step();
    dut->aresetn = 1; dut->ts_resetn = 1;
    for (int i = 0; i < 6; i++) step();

    printf("== ptp_csr_sync CDC harness ==\n");

    // ---- settime: payload must be aligned with the command pulse ----
    {
        const uint64_t T = 0x1122334455667788ULL;
        dut->a_tod_wr = T;                 // software holds the payload stable
        dut->a_cmd_load = 1; step(); dut->a_cmd_load = 0;
        int pulses = 0; uint64_t seen_payload = 0; bool aligned = true;
        for (int i = 0; i < 40; i++) {
            step();
            if (dut->t_cmd_load & 1) {
                pulses++;
                seen_payload = dut->t_tod_wr;
                if (dut->t_tod_wr != T) aligned = false;   // <-- the bug this guards
            }
        }
        ck("settime pulse count", pulses, 1);
        ck("settime payload aligned", aligned ? 1 : 0, 1);
        printf("  [%s] settime: %d pulse(s), payload=0x%llx (expect 0x%llx)\n",
               (pulses==1 && aligned) ? "PASS" : "FAIL", pulses,
               (unsigned long long)seen_payload, (unsigned long long)T);
    }

    // ---- adjtime: signed offset payload aligned with the command pulse ----
    {
        const uint64_t OFF = 0xFFFFFFFFFFFF0000ULL;  // -65536
        dut->a_offset = OFF;
        dut->a_cmd_adjust = 1; step(); dut->a_cmd_adjust = 0;
        int pulses = 0; bool aligned = true; uint64_t seen = 0;
        for (int i = 0; i < 40; i++) {
            step();
            if (dut->t_cmd_adjust & 1) { pulses++; seen = dut->t_offset; if (dut->t_offset != OFF) aligned = false; }
        }
        ck("adjtime pulse count", pulses, 1);
        ck("adjtime payload aligned", aligned ? 1 : 0, 1);
        printf("  [%s] adjtime: %d pulse(s), offset=0x%llx\n",
               (pulses==1 && aligned) ? "PASS" : "FAIL", pulses, (unsigned long long)seen);
    }

    // ---- back-to-back settime with different payloads (no stale carry-over) ----
    {
        bool ok = true;
        for (uint64_t T : { 0x00000000DEADBEEFULL, 0x0000000012345678ULL, 0xCAFEF00DBAADF00DULL }) {
            dut->a_tod_wr = T; dut->a_cmd_load = 1; step(); dut->a_cmd_load = 0;
            uint64_t seen = 0; int pulses = 0;
            for (int i = 0; i < 40; i++) { step(); if (dut->t_cmd_load & 1) { pulses++; seen = dut->t_tod_wr; } }
            if (pulses != 1 || seen != T) { ok = false; printf("  [FAIL] back2back settime T=0x%llx seen=0x%llx pulses=%d\n",
                                                              (unsigned long long)T,(unsigned long long)seen,pulses); }
        }
        ck("back-to-back settime", ok ? 1 : 0, 1);
        printf("  [%s] back-to-back settime loads the current payload each time\n", ok?"PASS":"FAIL");
    }

    // ---- rate config passes through (enable/incr/adj) ----
    {
        dut->a_enable = 1; dut->a_incr = 0x04000000; dut->a_adj = 0x00000010;
        for (int i = 0; i < 8; i++) step();
        ck("t_enable", dut->t_enable & 1, 1);
        ck("t_incr",   dut->t_incr, 0x04000000);
        ck("t_adj",    dut->t_adj,  0x00000010);
        printf("  [%s] rate config (enable/incr/adj) synchronised through\n",
               (fails==0) ? "PASS" : "FAIL");
    }

    // ---- snapshot return path: ts_clk value -> aclk a_tod_rd + valid pulse ----
    {
        const uint64_t SNAP = 0x0102030405060708ULL;
        dut->t_tod_snapshot = SNAP;
        dut->t_tod_snapshot_valid = 1; step(); dut->t_tod_snapshot_valid = 0;
        int vpulses = 0; uint64_t rd = 0;
        for (int i = 0; i < 40; i++) { step(); if (dut->a_tod_rd_valid & 1) { vpulses++; rd = dut->a_tod_rd; } }
        ck("snapshot return valid pulses", vpulses, 1);
        ck("snapshot return value", rd, SNAP);
        printf("  [%s] gettime snapshot returns 0x%llx to aclk with one valid pulse\n",
               (vpulses==1 && rd==SNAP) ? "PASS" : "FAIL", (unsigned long long)rd);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}

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
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>

// Shared-clock cycle budgets. Both domains are stepped together, so a command
// needs only the synchroniser depth to cross; the windows below are generous
// guards, not timing measurements.
constexpr int kResetCycles = 6;      // cycles held in, then released from, reset
constexpr int kObserveCycles = 40;   // window watched for the synchronised pulse
constexpr int kSettleCycles = 8;     // cycles for level config to cross
// The PPS live-target return publishes on a free-running 2^8 ts_clk beat, so
// its window is a whole beat plus the synchroniser depth, not kObserveCycles.
constexpr int kPpsPublishCycles = 600;

// Whether THIS build elaborated the PPS crossing. The ports exist either way
// (the OFF arm parks them), so one harness covers both: the Makefile's obj_pps
// leg passes -GPPS_P=1 to the RTL and -DPTP_SYNC_PPS_P=1 here from one
// variable. The default build is then the negative control - the parked arm
// must hold a structural zero while the CSR-side inputs are driven hard.
#ifndef PTP_SYNC_PPS_P
#define PTP_SYNC_PPS_P 0
#endif
constexpr bool kPpsBuilt = PTP_SYNC_PPS_P != 0;

namespace {
// The model handle and the tally were file-scope statics; they are the state
// of one run of this harness, so they belong to the object that performs it.
class PtpCsrSyncHarness {
 public:
    int run();

 private:
    void pps_alarm_crossing();
    void step() {              // advance both domains one (shared) cycle
        dut->aclk = 0; dut->ts_clk = 0; dut->eval();
        dut->aclk = 1; dut->ts_clk = 1; dut->eval();
    }
    void ck(const char* what, uint64_t got, uint64_t exp) {
        checks++;
        if (got != exp) { fails++; printf("  [FAIL] %-28s got=0x%llx exp=0x%llx\n", what,
                                          static_cast<unsigned long long>(got),
                                          static_cast<unsigned long long>(exp)); }
    }

    Vptp_csr_sync* dut = nullptr;
    long fails = 0;
    long checks = 0;
};

//! PPS alarm crossing (#260): enable, armed target, live readback.
//!
//! Three shapes, the same three the command path uses, and the same bug
//! class: the arm strobe crosses as a toggle and the target it arms is a
//! separate 64-bit payload, so a capture that does not land with the pulse
//! arms the comparator at a stale (or zero) second boundary - which on this
//! path is a pulse at the WRONG TIME, not a visibly dead output. With PPS_P
//! off the generate block is parked, and every one of these must read a
//! structural zero under exactly the same stimulus.
void PtpCsrSyncHarness::pps_alarm_crossing() {
    constexpr uint64_t TGT = 0x0000000B'2D05E000ULL;   // 48e9 ns
    dut->a_pps_enable = 1;
    for (int i = 0; i < kSettleCycles; i++) step();
    ck("t_pps_enable crosses", dut->t_pps_enable & 1, kPpsBuilt ? 1 : 0);

    dut->a_pps_target_ns = TGT;            // software holds the target stable
    dut->a_pps_arm = 1; step(); dut->a_pps_arm = 0;
    int pulses = 0; uint64_t seen = 0; bool aligned = true;
    for (int i = 0; i < kObserveCycles; i++) {
        step();
        if (dut->t_pps_arm & 1) {
            pulses++;
            seen = dut->t_pps_target_ns;
            if (dut->t_pps_target_ns != TGT) aligned = false;
        }
    }
    ck("pps arm pulse count", pulses, kPpsBuilt ? 1 : 0);
    ck("pps target aligned with the arm", aligned ? 1 : 0, 1);
    ck("pps target held after the pulse", dut->t_pps_target_ns, kPpsBuilt ? TGT : 0);
    printf("  [%s] pps arm: %d pulse(s), target=0x%llx\n",
           (pulses == (kPpsBuilt ? 1 : 0) && aligned) ? "PASS" : "FAIL",
           pulses, static_cast<unsigned long long>(seen));

    // The return path is a free-running publish beat, so the live target
    // reaches aclk whatever the PHC is doing to it.
    constexpr uint64_t LIVE = 0x0000000C'3C9C3800ULL;
    dut->t_pps_target_live_ns = LIVE;
    for (int i = 0; i < kPpsPublishCycles; i++) step();
    ck("live pps target published to aclk", dut->a_pps_target_rd_ns,
       kPpsBuilt ? LIVE : 0);
    printf("  [%s] live pps target readback = 0x%llx (PPS_P=%d)\n",
           (dut->a_pps_target_rd_ns == (kPpsBuilt ? LIVE : 0)) ? "PASS" : "FAIL",
           static_cast<unsigned long long>(dut->a_pps_target_rd_ns),
           kPpsBuilt ? 1 : 0);
}

int PtpCsrSyncHarness::run() {
    const milan::tb::Model<Vptp_csr_sync> model;
    dut = model.get();

    dut->aresetn = 0; dut->ts_resetn = 0;
    dut->a_enable = 1; dut->a_incr = 0x08000000; dut->a_adj = 0;
    dut->a_tod_wr = 0; dut->a_offset = 0;
    dut->a_cmd_load = 0; dut->a_cmd_adjust = 0; dut->a_cmd_snapshot = 0;
    dut->t_tod_snapshot = 0; dut->t_tod_snapshot_valid = 0;
    dut->a_pps_enable = 0; dut->a_pps_target_ns = 0; dut->a_pps_arm = 0;
    dut->t_pps_target_live_ns = 0;
    for (int i = 0; i < kResetCycles; i++) step();
    dut->aresetn = 1; dut->ts_resetn = 1;
    for (int i = 0; i < kResetCycles; i++) step();

    printf("== ptp_csr_sync CDC harness ==\n");

    // ---- settime: payload must be aligned with the command pulse ----
    {
        constexpr uint64_t T = 0x1122334455667788ULL;
        dut->a_tod_wr = T;                 // software holds the payload stable
        dut->a_cmd_load = 1; step(); dut->a_cmd_load = 0;
        int pulses = 0; uint64_t seen_payload = 0; bool aligned = true;
        for (int i = 0; i < kObserveCycles; i++) {
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
               static_cast<unsigned long long>(seen_payload), static_cast<unsigned long long>(T));
    }

    // ---- adjtime: signed offset payload aligned with the command pulse ----
    {
        constexpr uint64_t OFF = 0xFFFFFFFFFFFF0000ULL;  // -65536
        dut->a_offset = OFF;
        dut->a_cmd_adjust = 1; step(); dut->a_cmd_adjust = 0;
        int pulses = 0; bool aligned = true; uint64_t seen = 0;
        for (int i = 0; i < kObserveCycles; i++) {
            step();
            if (dut->t_cmd_adjust & 1) { pulses++; seen = dut->t_offset; if (dut->t_offset != OFF) aligned = false; }
        }
        ck("adjtime pulse count", pulses, 1);
        ck("adjtime payload aligned", aligned ? 1 : 0, 1);
        printf("  [%s] adjtime: %d pulse(s), offset=0x%llx\n",
               (pulses==1 && aligned) ? "PASS" : "FAIL", pulses, static_cast<unsigned long long>(seen));
    }

    // ---- back-to-back settime with different payloads (no stale carry-over) ----
    {
        bool ok = true;
        for (uint64_t T : { 0x00000000DEADBEEFULL, 0x0000000012345678ULL, 0xCAFEF00DBAADF00DULL }) {
            dut->a_tod_wr = T; dut->a_cmd_load = 1; step(); dut->a_cmd_load = 0;
            uint64_t seen = 0; int pulses = 0;
            for (int i = 0; i < kObserveCycles; i++) { step(); if (dut->t_cmd_load & 1) { pulses++; seen = dut->t_tod_wr; } }
            if (pulses != 1 || seen != T) { ok = false; printf("  [FAIL] back2back settime T=0x%llx seen=0x%llx pulses=%d\n",
                                                              static_cast<unsigned long long>(T),
                                                              static_cast<unsigned long long>(seen), pulses); }
        }
        ck("back-to-back settime", ok ? 1 : 0, 1);
        printf("  [%s] back-to-back settime loads the current payload each time\n", ok?"PASS":"FAIL");
    }

    // ---- rate config passes through (enable/incr/adj) ----
    {
        dut->a_enable = 1; dut->a_incr = 0x04000000; dut->a_adj = 0x00000010;
        for (int i = 0; i < kSettleCycles; i++) step();
        ck("t_enable", dut->t_enable & 1, 1);
        ck("t_incr",   dut->t_incr, 0x04000000);
        ck("t_adj",    dut->t_adj,  0x00000010);
        printf("  [%s] rate config (enable/incr/adj) synchronised through\n",
               (fails==0) ? "PASS" : "FAIL");
    }

    // ---- snapshot return path: ts_clk value -> aclk a_tod_rd + valid pulse ----
    {
        constexpr uint64_t SNAP = 0x0102030405060708ULL;
        dut->t_tod_snapshot = SNAP;
        dut->t_tod_snapshot_valid = 1; step(); dut->t_tod_snapshot_valid = 0;
        int vpulses = 0; uint64_t rd = 0;
        for (int i = 0; i < kObserveCycles; i++) { step(); if (dut->a_tod_rd_valid & 1) { vpulses++; rd = dut->a_tod_rd; } }
        ck("snapshot return valid pulses", vpulses, 1);
        ck("snapshot return value", rd, SNAP);
        printf("  [%s] gettime snapshot returns 0x%llx to aclk with one valid pulse\n",
               (vpulses==1 && rd==SNAP) ? "PASS" : "FAIL", static_cast<unsigned long long>(rd));
    }

    pps_alarm_crossing();

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    PtpCsrSyncHarness harness;
    return harness.run();
}

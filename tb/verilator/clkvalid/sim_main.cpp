// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_ptp_clock_validity harness - the AVTP "tu" verdict.
//
// WHAT THIS PROVES, and why each check exists.  On 2026-07-27 our Arty
// streamed 31 M AAF frames whose presentation times came from a PHC 60 h out
// of the domain, at full rate, with tu = 0 the whole time.  The receiving
// Milan device counted 99.4 % of them LATE or EARLY and could not tell,
// because the one field that exists to warn it said the timestamps were fine
// (docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md).
//
// The FIRST check below is the mutation anchor: RESET STATE IS tu = 1.  Tie
// ts_uncertain_o to 0 - the pre-fix behaviour - and it fails immediately.
// Every "unknown means uncertain" check has the same property. The fabric
// shape also proves that a real engine-owned sync verdict can clear tu; the
// option-off shape deliberately has no owner and therefore cannot clear it.
//
// Argv[1] = QTICK_CYC_P the model was elaborated with.  Two shapes run: a
// fast one (8) that exercises every behaviour, and the real 100 MHz value
// (25_000_000) so the divider arithmetic is proved at the shipping number
// and not only at a toy one.

#include "VKL_ptp_clock_validity.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>

static VKL_ptp_clock_validity* dut;
static long checks = 0, fails = 0;
static long qtick = 8;

static void ck(const char* what, long got, long exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-52s got=%ld exp=%ld\n", ok ? "ok" : "FAIL", what, got, exp);
}
static void ck_range(const char* what, long got, long lo, long hi) {
    checks++;
    bool ok = (got >= lo && got <= hi);
    if (!ok) fails++;
    printf("  [%s] %-52s got=%ld exp=%ld..%ld\n", ok ? "ok" : "FAIL", what, got, lo, hi);
}

static void tick(long n = 1) {
    for (long i = 0; i < n; i++) {
        dut->clk_i = 0; dut->eval();
        dut->clk_i = 1; dut->eval();
    }
}

//! Drive every CLKV compatibility pin as one maximal write. They must have no
//! effect in either shape.
static void clkv_write(bool sync_ok, unsigned wdog_q, bool disc = false,
                       bool as_cap = false) {
    dut->sw_sync_ok_i = sync_ok;
    dut->sw_wdog_q_i  = wdog_q;
    dut->sw_disc_p_i  = disc;
    dut->sw_as_cap_i  = as_cap;
    dut->sw_wr_p_i    = 1;
    tick();
    dut->sw_wr_p_i   = 0;
    dut->sw_disc_p_i = 0;
    tick();
}

//! run until tu clears, or give up. Returns cycles waited.
static long wait_tu(int want, long limit) {
    long n = 0;
    while (dut->ts_uncertain_o != want && n < limit) { tick(); n++; }
    return n;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc > 1) qtick = atol(argv[1]);
    const bool fabric = argc > 2 && strcmp(argv[2], "fabric") == 0;
    const bool full = (qtick <= 1000);   //! interval-counter checks only in the fast shape

    dut = new VKL_ptp_clock_validity;
    dut->rst_n = 0;
    dut->sw_wr_p_i = 0; dut->sw_sync_ok_i = 0; dut->sw_disc_p_i = 0;
    dut->sw_as_cap_i = 0;
    dut->sw_wdog_q_i = 0;
    dut->fabric_sync_ok_i = 0; dut->fabric_as_cap_i = 0;
    dut->fabric_disc_p_i = 0;
    dut->phc_load_p_i = 0; dut->phc_adj_p_i = 0;
    dut->gm_id_i = 0;
    tick(4);
    dut->rst_n = 1;
    tick(2);

    printf("== KL_ptp_clock_validity (QTICK_CYC_P=%ld) ==\n", qtick);

    if (fabric) {
        printf("-- fabric publication bank owns validity (#116) --\n");
        ck("reset: fabric has not synchronised, tu = 1",
           dut->ts_uncertain_o, 1);
        ck("fabric mode keeps retired no-lease field zero",
           (dut->stat_o >> 2) & 1, 0);

        clkv_write(true, 8, false, true);
        ck("software sync lease ignored", (dut->stat_o >> 1) & 1, 0);
        ck("software asCapable ignored", dut->as_capable_o, 0);
        ck("retired lease count is zero", (dut->stat_o >> 4) & 0xFFF, 0);

        dut->gm_id_i = 0x1122334455667788ull;
        dut->fabric_sync_ok_i = 1;
        dut->fabric_as_cap_i = 1;
        dut->eval();
        ck("GM adoption raises tu before the sampling edge",
           dut->ts_uncertain_o, 1);
        tick(2);
        long cleared = wait_tu(0, qtick * 8);
        ck_range("fabric sync clears tu after holdover (cycles)",
                 cleared, qtick, qtick * 4);
        ck("fabric sync is the STAT claim", (dut->stat_o >> 1) & 1, 1);
        ck("fabric asCapable is live", dut->as_capable_o, 1);
        ck("fabric asCapable is STAT[16]", (dut->stat_o >> 16) & 1, 1);
        tick(qtick * 10);
        ck("fabric sync stays valid without software", dut->ts_uncertain_o, 0);

        dut->fabric_disc_p_i = 1; dut->eval();
        ck("fabric discontinuity raises tu before the sampling edge",
           dut->ts_uncertain_o, 1);
        tick(); dut->fabric_disc_p_i = 0; tick();
        wait_tu(0, qtick * 8);

        dut->fabric_sync_ok_i = 0;
        dut->fabric_as_cap_i = 0;
        dut->eval();
        ck("fabric sync loss asserts tu immediately", dut->ts_uncertain_o, 1);
        tick();
        ck("fabric asCapable loss is immediate", dut->as_capable_o, 0);

        printf("== clkvalid: checks: %ld  failures: %ld ==\n", checks, fails);
        delete dut;
        return fails ? 1 : 0;
    }

    // -----------------------------------------------------------------
    // 1. OWNERLESS OPTION-OFF INVARIANT. With no fabric gPTP engine there
    //    is no authority that can assert sync or asCapable. The honest AVTP
    //    verdict is tu=1 forever.
    // -----------------------------------------------------------------
    printf("-- option-off is permanently ownerless (#116) --\n");
    ck("reset: tu = 1", dut->ts_uncertain_o, 1);
    ck("reset: STAT[0] tu", dut->stat_o & 1, 1);
    ck("reset: STAT[1] sync_ok", (dut->stat_o >> 1) & 1, 0);
    ck("reset: retired no-lease bit is zero", (dut->stat_o >> 2) & 1, 0);
    ck("reset: STAT[3] holdover", (dut->stat_o >> 3) & 1, 0);
    ck("reset: retired lease count is zero", (dut->stat_o >> 4) & 0xFFF, 0);
    ck("reset: asCapable = 0", dut->as_capable_o, 0);
    ck("reset: STAT[16] asCapable", (dut->stat_o >> 16) & 1, 0);
    ck("reset: TUCNT = 0", dut->tu_ivals_o, 0);

    // Drive every inert compatibility input at once. This is the mutation
    // anchor: reconnecting them makes sync/asCapable rise and tu clear.
    clkv_write(/*sync_ok=*/true, /*wdog_q=*/0xFFF,
               /*disc=*/true, /*as_cap=*/true);
    ck("software write cannot clear tu", dut->ts_uncertain_o, 1);
    ck("software write cannot assert sync", (dut->stat_o >> 1) & 1, 0);
    ck("software write cannot assert asCapable", dut->as_capable_o, 0);
    ck("software write cannot create a lease", (dut->stat_o >> 4) & 0xFFF, 0);
    ck("software discontinuity input is inert", (dut->stat_o >> 3) & 1, 0);

    for (int n = 0; n < 8; ++n)
        clkv_write((n & 1) != 0, 1u << n, (n & 2) != 0, (n & 4) != 0);
    ck("repeated writes still cannot clear tu", dut->ts_uncertain_o, 1);
    ck("repeated writes leave owner fields zero",
       dut->stat_o & 0x0001FFF6u, 0);

    // Fabric publication pins are also irrelevant in the option-off
    // elaboration; only FABRIC_GPTP_P=1 may consume them.
    dut->fabric_sync_ok_i = 1;
    dut->fabric_as_cap_i = 1;
    dut->fabric_disc_p_i = 1;
    dut->eval();
    ck("fabric sync pin ignored when option is off", (dut->stat_o >> 1) & 1, 0);
    ck("fabric asCapable pin ignored when option is off", dut->as_capable_o, 0);
    ck("fabric discontinuity pin ignored when option is off",
       (dut->stat_o >> 3) & 1, 0);
    ck("fabric pins cannot clear tu", dut->ts_uncertain_o, 1);
    tick();
    dut->fabric_disc_p_i = 0;

    // A stray identity on the retained module port is not an owner either.
    dut->gm_id_i = 0x1122334455667788ull;
    dut->eval();
    ck("GM input is ignored without a fabric owner", (dut->stat_o >> 3) & 1, 0);
    tick(2);
    ck("GM input cannot clear tu", dut->ts_uncertain_o, 1);

    // PHC steps remain observable diagnostics and arm holdover, but an
    // ownerless clock is already uncertain before, during, and after it.
    if (full) {
        dut->phc_load_p_i = 1; dut->eval();
        ck("PHC step keeps tu asserted", dut->ts_uncertain_o, 1);
        tick(); dut->phc_load_p_i = 0; tick();
        ck("PHC step arms holdover", (dut->stat_o >> 3) & 1, 1);
        tick(qtick * 3);
        ck("holdover expires while tu remains asserted", dut->ts_uncertain_o, 1);
        ck("expired holdover bit clears", (dut->stat_o >> 3) & 1, 0);

        uint32_t base = dut->tu_ivals_o;
        tick(qtick * 17);
        long delta = (long)(dut->tu_ivals_o - base);
        ck_range("permanent tu counts one-second intervals, not cycles",
                 delta, 4, 5);
    } else {
        // The real-divider shape proves the wide counter arithmetic without
        // simulating a full quarter second.
        tick(32);
        ck("shipping divider: writes still cannot clear tu",
           dut->ts_uncertain_o, 1);
        ck("shipping divider: owner fields remain zero",
           dut->stat_o & 0x0001FFF6u, 0);
    }
    printf("== clkvalid: checks: %ld  failures: %ld ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}

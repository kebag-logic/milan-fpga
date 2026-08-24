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
// Every "unknown means uncertain" check has the same property; the checks
// that tu can be CLEARED exist so the fix cannot be "assert tu forever",
// which would fail Milan validation 11.x (TIMESTAMP_UNCERTAIN must read 0
// on a healthy stream) just as loudly in the other direction.
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

//! one CSR write to CLKV_CTRL. The stored fields persist afterwards, exactly
//! as milan_csr's clkv_ctrl register does; only sw_wr_p_i is a pulse.
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

//! run until as_capable_o reaches want, or give up. Returns cycles waited.
static long wait_ascap(int want, long limit) {
    long n = 0;
    while (dut->as_capable_o != want && n < limit) { tick(); n++; }
    return n;
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
        ck("fabric mode reports no software lease",
           (dut->stat_o >> 2) & 1, 0);

        clkv_write(true, 8, false, true);
        ck("software sync lease ignored", (dut->stat_o >> 1) & 1, 0);
        ck("software asCapable ignored", dut->as_capable_o, 0);
        ck("software lease count hidden", (dut->stat_o >> 4) & 0xFFF, 0);

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
        ck("no daemon lease expiry in fabric mode", dut->ts_uncertain_o, 0);

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
    // 1. FAIL-SAFE DEFAULT. This is the whole defect in one check: with
    //    nothing published, the device must NOT claim its timestamps are
    //    good. Reverting the RTL to a hard tu=0 fails here first.
    // -----------------------------------------------------------------
    printf("-- fail-safe default (the 2026-07-27 defect) --\n");
    ck("reset: tu = 1 (unknown clock is NOT valid)", dut->ts_uncertain_o, 1);
    ck("reset: STAT[0] tu",        dut->stat_o & 1, 1);
    ck("reset: STAT[1] sync_ok",  (dut->stat_o >> 1) & 1, 0);
    ck("reset: STAT[2] no lease", (dut->stat_o >> 2) & 1, 1);
    ck("reset: STAT[3] holdover", (dut->stat_o >> 3) & 1, 0);
    ck("reset: TUCNT = 0",         dut->tu_ivals_o, 0);
    //! gh #64 J3: same fail-safe for asCapable. IEEE 802.1AS-2020 10.2.5.1
    //! is a per-port determination that the neighbour can interoperate via
    //! the protocol - unknown must read FALSE, never "probably".
    ck("reset: asCapable = 0 (unknown neighbour is NOT capable)",
       dut->as_capable_o, 0);
    ck("reset: STAT[16] asCapable", (dut->stat_o >> 16) & 1, 0);
    tick(qtick * 3);
    ck("no software at all: still tu = 1 after 3 ticks", dut->ts_uncertain_o, 1);

    // -----------------------------------------------------------------
    // 2. A software lease clears tu, and only a lease does.
    // -----------------------------------------------------------------
    printf("-- the software lease --\n");
    clkv_write(true, 0);                 //! sync_ok with a ZERO lease
    ck("sync_ok + lease 0 = never trust: tu stays 1", dut->ts_uncertain_o, 1);
    ck("lease 0: STAT[1] sync_ok not latched", (dut->stat_o >> 1) & 1, 0);

    clkv_write(false, 8);                //! a lease, but sync_ok = 0
    ck("lease without sync_ok: tu stays 1", dut->ts_uncertain_o, 1);

    clkv_write(true, 8);                 //! the real thing
    ck("sync_ok + lease 8: tu clears", dut->ts_uncertain_o, 0);
    ck("STAT[1] sync_ok set",   (dut->stat_o >> 1) & 1, 1);
    ck("STAT[2] no_lease clear",(dut->stat_o >> 2) & 1, 0);
    //! the prescaler free-runs, so a quarter-tick may already have eaten one
    //! of the 8 before this read - the honest expectation is 7 or 8, not 8
    ck_range("STAT[15:4] lease left after arming 8", (dut->stat_o >> 4) & 0xFFF, 7, 8);

    // -----------------------------------------------------------------
    // 3. The lease EXPIRES. A boolean written once at boot is the defect;
    //    a claim that is never refreshed must lapse.
    // -----------------------------------------------------------------
    printf("-- the lease expires (a claim nobody renews is not a claim) --\n");
    clkv_write(true, 2);
    ck("relet with lease 2: tu clear", dut->ts_uncertain_o, 0);
    long waited = wait_tu(1, qtick * 6);
    ck_range("tu re-asserts on lease expiry (cycles)", waited, qtick, qtick * 3);
    ck("expired: tu = 1", dut->ts_uncertain_o, 1);
    ck("expired: STAT[1] sync_ok cleared", (dut->stat_o >> 1) & 1, 0);
    ck("expired: STAT[2] no_lease set",    (dut->stat_o >> 2) & 1, 1);

    //! a daemon that keeps writing keeps the claim alive
    clkv_write(true, 2);
    for (int r = 0; r < 6; r++) { tick(qtick); clkv_write(true, 2); }
    ck("refreshed lease: tu stays clear across 6 renewals", dut->ts_uncertain_o, 0);

    // -----------------------------------------------------------------
    // 3b. asCapable RIDES THE SAME LEASE (gh #64 J3). IEEE 802.1AS-2020
    //     10.2.5.1: asCapable is the per-port determination that this
    //     time-aware system and its neighbour can interoperate via the
    //     802.1AS protocol - a pdelay-exchange verdict only the daemon
    //     computes. The old consumer proxied it as "some propagation
    //     delay was once written", which stays TRUE forever after the
    //     daemon dies. Here the claim is a LEASED level: latched only
    //     with a live lease, and cleared by the SAME branch that clears
    //     the synchronised flag, so a dead daemon answers asCapable = 0
    //     by construction. Milan v1.2 Table 5.22 makes it a GET_AVB_INFO
    //     push trigger, so this edge is the one the wire will carry.
    // -----------------------------------------------------------------
    printf("-- asCapable rides the lease (gh #64 J3) --\n");
    {
        //! a claim with NO lease is not a claim - same law as sync_ok
        clkv_write(/*sync_ok=*/true, /*wdog=*/0, /*disc=*/false, /*as_cap=*/true);
        ck("asCapable + lease 0: not latched", dut->as_capable_o, 0);
        ck("asCapable + lease 0: STAT[16] clear", (dut->stat_o >> 16) & 1, 0);

        //! the daemon publishes asCapable TRUE on a renewing write
        clkv_write(true, 2, false, true);
        ck("asCapable claimed with a live lease", dut->as_capable_o, 1);
        ck("STAT[16] asCapable set", (dut->stat_o >> 16) & 1, 1);
        ck("...and the sync claim stands with it", (dut->stat_o >> 1) & 1, 1);

        //! THE DEADMAN. Stop writing and run past expiry: the claim must
        //! fall, and fall WITH the synchronised flag - one lease, one
        //! lapse, no way for a stale asCapable to outlive the daemon.
        long lapsed = wait_ascap(0, qtick * 6);
        ck_range("asCapable falls on lease expiry (cycles)", lapsed, qtick, qtick * 3);
        ck("expired: asCapable = 0", dut->as_capable_o, 0);
        ck("expired: STAT[16] cleared", (dut->stat_o >> 16) & 1, 0);
        ck("expired: sync claim fell in the SAME branch", (dut->stat_o >> 1) & 1, 0);
        ck("expired: no live lease", (dut->stat_o >> 2) & 1, 1);
        ck("expired: tu asserted", dut->ts_uncertain_o, 1);

        //! a renewal that CLEARS bit 2 is a report of asCapable false, not
        //! silence: the level follows every write, it is not sticky
        clkv_write(true, 4000, false, true);
        ck("re-armed: asCapable back", dut->as_capable_o, 1);
        clkv_write(true, 4000, false, false);
        ck("renewed with the claim dropped: asCapable = 0", dut->as_capable_o, 0);
        ck("...while the sync claim is untouched", (dut->stat_o >> 1) & 1, 1);
        ck("...and tu stays clear (the two are independent)",
           dut->ts_uncertain_o, 0);

        //! asCapable is orthogonal to the discontinuity holdover: a PHC
        //! step raises tu but says nothing about the neighbour
        clkv_write(true, 4000, false, true);
        dut->phc_load_p_i = 1; tick(); dut->phc_load_p_i = 0; tick();
        ck("PHC step raises tu", dut->ts_uncertain_o, 1);
        ck("...and leaves asCapable alone", dut->as_capable_o, 1);
        wait_tu(0, qtick * 8);
    }

    // -----------------------------------------------------------------
    // 4. Fabric-observed discontinuities: a PHC step is a gPTP time
    //    discontinuity by construction (IEEE 1722-2016 4.4.4.7) and needs
    //    no software cooperation at all.
    // -----------------------------------------------------------------
    printf("-- PHC steps: the discontinuity fabric can see for itself --\n");
    clkv_write(true, 4000);              //! a long lease so only the step matters
    ck("long lease: tu clear before the step", dut->ts_uncertain_o, 0);

    dut->phc_load_p_i = 1; dut->eval();
    ck("settime pulse raises tu before the sampling edge",
       dut->ts_uncertain_o, 1);
    tick(); dut->phc_load_p_i = 0; tick();
    ck("settime (PTP_CMD[0]): tu asserts", dut->ts_uncertain_o, 1);
    ck("STAT[3] holdover active", (dut->stat_o >> 3) & 1, 1);
    ck("STAT[1] sync_ok survives the step", (dut->stat_o >> 1) & 1, 1);
    long held = wait_tu(0, qtick * 8);
    //! Milan v1.2 Annex B.1.1: at least 0.25 s == at least one quarter-tick.
    ck_range("holdover length (cycles) >= 0.25 s, <= 0.5 s + slop",
             held, qtick, qtick * 2 + 4);
    ck("after the holdover: tu clears again", dut->ts_uncertain_o, 0);

    dut->phc_adj_p_i = 1; dut->eval();
    ck("adjtime pulse raises tu before the sampling edge",
       dut->ts_uncertain_o, 1);
    tick(); dut->phc_adj_p_i = 0; tick();
    ck("adjtime (PTP_CMD[1]): tu asserts", dut->ts_uncertain_o, 1);
    wait_tu(0, qtick * 8);
    ck("adjtime holdover ends", dut->ts_uncertain_o, 0);

    // -----------------------------------------------------------------
    // 5. Grandmaster change - Milan v1.2 Annex B.1.1, for free, off the
    //    gptp_grandmaster_id the daemon already publishes for ADP.
    // -----------------------------------------------------------------
    printf("-- grandmaster change (Milan v1.2 Annex B.1.1) --\n");
    dut->gm_id_i = 0x020000FFFE000001ULL; dut->eval();
    ck("GM change raises tu before the sampling edge",
       dut->ts_uncertain_o, 1);
    tick(2);
    ck("new GM id: tu asserts", dut->ts_uncertain_o, 1);
    held = wait_tu(0, qtick * 8);
    ck_range("GM-change holdover >= 0.25 s", held, qtick, qtick * 2 + 4);

    dut->gm_id_i = 0x020000FFFE000001ULL; tick(qtick * 3);
    ck("same GM id held: no holdover", dut->ts_uncertain_o, 0);

    dut->gm_id_i = 0x3CC0C6FFFE010203ULL; tick(2);
    ck("GM id changes again: tu asserts", dut->ts_uncertain_o, 1);
    wait_tu(0, qtick * 8);

    // -----------------------------------------------------------------
    // 6. Software-reported discontinuity (CLKV_CTRL[1] W1S) - the daemon
    //    knows things fabric never will (servo reset, GM timing-source
    //    change with an unchanged GM id).
    // -----------------------------------------------------------------
    printf("-- software-reported discontinuity --\n");
    ck("clear before the report", dut->ts_uncertain_o, 0);
    clkv_write(true, 4000, /*disc=*/true);
    ck("CLKV_CTRL[1]: tu asserts", dut->ts_uncertain_o, 1);
    held = wait_tu(0, qtick * 8);
    ck_range("software-report holdover >= 0.25 s", held, qtick, qtick * 2 + 4);

    // -----------------------------------------------------------------
    // 7. Milan Table 5.4 / 5.6 TIMESTAMP_UNCERTAIN: ONE increment per
    //    one-second observation interval in which tu was set - NOT one per
    //    frame, and NOT one per tu edge (that is the 1722.1 Table 7-159
    //    reading, which Milan overrides for a PAAD).
    // -----------------------------------------------------------------
    if (full) {
        printf("-- TIMESTAMP_UNCERTAIN counts observation intervals (Milan Table 5.4) --\n");
        //! park in a clean state and let the counter settle on a boundary
        clkv_write(true, 4000);
        tick(qtick * 12);
        uint32_t base = dut->tu_ivals_o;
        tick(qtick * 12);
        ck("healthy clock: TUCNT frozen", (long)(dut->tu_ivals_o - base), 0);

        //! now hold tu for a bit over 4 observation intervals (16 quarter-ticks)
        clkv_write(false, 4000);
        ck("sync dropped: tu = 1", dut->ts_uncertain_o, 1);
        base = dut->tu_ivals_o;
        tick(qtick * 17);
        long d = (long)(dut->tu_ivals_o - base);
        ck_range("tu held ~4.25 s: TUCNT +4..+5 (never per-frame)", d, 4, 5);

        clkv_write(true, 4000);
        tick(qtick * 12);
        base = dut->tu_ivals_o;
        tick(qtick * 12);
        ck("clock healthy again: TUCNT frozen", (long)(dut->tu_ivals_o - base), 0);
    }

    printf("== clkvalid: checks: %ld  failures: %ld ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}

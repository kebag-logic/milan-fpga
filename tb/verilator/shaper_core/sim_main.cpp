/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for traffic_shaping_core.sv — the 802.1Qav
 * multi-queue arbiter with per-queue CBS (REQ-VER-02).
 *
 * The per-queue credit arithmetic is proven bit-exact by tb/verilator/cbs; here
 * we verify the *arbitration*: an independent C++ model of the grant FSM must
 * predict grant_queue_o exactly, every cycle, and directed scenarios assert the
 * 802.1Q intent (grant exclusivity, tlast-held grants, strict-priority order,
 * the shaped/unshaped bypass, and credit depletion during transmission).
 *
 * Exit code 0 = pass, non-zero = failure (CI friendly).
 */

#include "Vshaper_core_wrap.h"
#include "verilated.h"

#include <cstdio>
#include <cmath>
#include <cstdint>
#include <random>

static const int NQ = 6;   // 802.1Q order: q5 = highest priority, q0 = lowest

static int64_t sx48(uint64_t v) {
    v &= (((uint64_t)1 << 48) - 1);
    if (v & ((uint64_t)1 << 47)) v |= ~((((uint64_t)1 << 48) - 1));
    return (int64_t)v;
}
static int popcountq(uint32_t x) { int n = 0; for (int i = 0; i < NQ; i++) n += (x >> i) & 1; return n; }
// priority encoder: HIGHEST set bit index, or -1. Mirrors
// ethernet_packet_pkg::priority_encode, which scans from the top index down
// since the 6-queue map put SR class A on q5 (802.1Q order).
static int penc(uint32_t req) { for (int i = NQ - 1; i >= 0; i--) if (req & (1u << i)) return i; return -1; }
// one-hot index (grant is always one-hot or zero, so direction is irrelevant)
static int onehot_idx(uint32_t v) { for (int i = 0; i < NQ; i++) if (v & (1u << i)) return i; return -1; }

// milan_csr CBS reset defaults for the 6-queue map, INDEXED BY QUEUE:
// q0 BE / q1 spare / q2 control / q3 gPTP / q4 SR class B / q5 SR class A.
struct Cfg {
    uint32_t idle[NQ] = {25000000, 25000000, 50000000, 50000000, 150000000, 450000000};
    int32_t  hi[NQ]   = {38, 38, 76, 76, 228, 684};
    int32_t  lo[NQ]   = {-1483, -1483, -1445, -1445, -1293, -837};
    uint32_t shaped   = 0x3F; // all shaped by default (this harness, NOT the reset word)
};

struct Harness {
    Vshaper_core_wrap* dut;
    long checks = 0, fails = 0;

    // reference grant FSM (mirrors traffic_shaping_core)
    bool hold = false;
    int  active = 0;

    explicit Harness(Vshaper_core_wrap* d) : dut(d) {}

    void apply_cfg(const Cfg& c) {
        // Verilator packs <=64-bit wide ports as scalars, wider as arrays; the
        // 128-bit CBS vectors are VlWide — assign per 32-bit lane.
        for (int i = 0; i < NQ; i++) {
            dut->cbs_idle_slope_i.at(i) = c.idle[i];
            dut->cbs_hi_credit_i.at(i)  = (uint32_t)c.hi[i];
            dut->cbs_lo_credit_i.at(i)  = (uint32_t)c.lo[i];
        }
        dut->cbs_shaped_i = c.shaped;
    }

    // Drive one cycle. Returns after the posedge with outputs settled.
    void cycle(uint32_t has_data, bool s_tvalid, bool s_tlast, bool m_tready,
               const char* tag) {
        dut->queue_has_data_i = has_data;
        dut->s_tvalid = s_tvalid;
        dut->s_tlast  = s_tlast;
        dut->m_tready = m_tready;
        dut->s_tkeep  = 0xFF;              // 8 bytes/beat when transmitting
        dut->s_tdata  = 0xDEADBEEF;
        dut->eval();                       // settle comb (allow, grant) pre-edge

        // sample registered allow_transmit and compute the arbiter's next state
        uint32_t allow = dut->dbg_allow;
        int sel = penc(allow & has_data);
        bool m_fire_last = s_tvalid && m_tready && s_tlast;

        bool n_hold = hold; int n_active = active;
        if (hold) {
            if (m_fire_last) n_hold = false;
        } else if (sel >= 0) {
            n_active = sel; n_hold = true;
        }
        if (!dut->resetn) { n_hold = false; n_active = 0; }  // synchronous reset

        // posedge
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();
        hold = n_hold; active = n_active;

        // check grant_o matches the reference exactly
        uint32_t exp_grant = hold ? (1u << active) : 0u;
        if (dut->grant_o != exp_grant)
            fail(tag, "grant", dut->grant_o, exp_grant);
        // invariant: grant is one-hot or zero
        if (popcountq(dut->grant_o) > 1)
            fail(tag, "grant_onehot", dut->grant_o, 0);
        checks++;
    }

    void fail(const char* tag, const char* what, uint32_t got, uint32_t exp) {
        if (fails < 20)
            printf("  [FAIL] %-16s %-14s got=0x%X exp=0x%X\n", tag, what, got, exp);
        fails++;
    }

    void reset(int n) {
        dut->resetn = 0;
        for (int i = 0; i < n; i++) cycle(0, false, false, false, "reset");
        dut->resetn = 1;
    }

    int64_t credit(int q) {
        switch (q) {
            case 0: return sx48(dut->dbg_credit0);
            case 1: return sx48(dut->dbg_credit1);
            case 2: return sx48(dut->dbg_credit2);
            case 3: return sx48(dut->dbg_credit3);
            case 4: return sx48(dut->dbg_credit4);
            default:return sx48(dut->dbg_credit5);
        }
    }
    int grant_index() { return onehot_idx(dut->grant_o); }
};


// ---------------------------------------------------------------------------
//  REQ-CBS-07 helper: run a single shaped queue flat out for `cycles` and
//  return the bytes actually ACCEPTED at the egress. `ready_period` paces the
//  sink: 1 = accept every cycle (the datapath can drain 8 B/cycle = 6.4 Gb/s at
//  100 MHz, far above any wire), 8 = one beat per 8 cycles (~0.8 Gb/s, about
//  line rate). The long-run average must come out the same either way - the
//  credit math is rate-correct because credit accrues per CYCLE and is debited
//  per BYTE, so the fixed point is bytes/s == idleSlope/8 regardless of how
//  bursty the drain is. If bytes_sent/is_transmitting counted anything other
//  than accepted beats, the two regimes would disagree.
// ---------------------------------------------------------------------------
static long run_rate(Harness& h, uint32_t idle_slope, int ready_period,
                     int cycles, int frame_beats, const char* tag) {
    Cfg c;
    c.idle[0] = idle_slope;
    c.hi[0]   = 456; c.lo[0] = -1065;
    c.shaped  = 0x3F;
    h.apply_cfg(c);
    h.reset(4);
    // let the slope engine commit (2 passes = 200 cycles) before measuring
    for (int i = 0; i < 400; i++) h.cycle(0x1, false, false, true, tag);

    long beats = 0;
    int  beat_in_frame = 0;
    for (int i = 0; i < cycles; i++) {
        bool rdy   = (i % ready_period) == 0;
        bool tlast = (beat_in_frame == frame_beats - 1);
        // count the beat if it is actually accepted at the egress
        h.dut->eval();
        bool granted = (h.dut->grant_o != 0);
        h.cycle(0x1, /*s_tvalid=*/true, tlast, rdy, tag);
        if (granted && rdy) {
            beats++;
            beat_in_frame = tlast ? 0 : beat_in_frame + 1;
        }
    }
    return beats * 8;   // 8 bytes per beat (tkeep = 0xFF)
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vshaper_core_wrap* dut = new Vshaper_core_wrap;
    Harness h(dut);
    Cfg cfg;

    dut->is_1g_i = 1;
    dut->resetn = 0;
    h.apply_cfg(cfg);
    h.reset(4);

    printf("== traffic_shaping_core arbitration harness (NQ=%d, all shaped) ==\n", NQ);

    // ---- Scenario 1: single queue q2 wins its own grant ----
    {
        long f0 = h.fails;
        // let q2 build credit while idle-waiting (has_data, no transmit)
        for (int i = 0; i < 400; i++) h.cycle(0x4, false, false, false, "q2_build");
        // now q2 transmits a 10-beat packet
        int granted_q2 = -1;
        for (int i = 0; i < 10; i++) {
            bool last = (i == 9);
            h.cycle(0x4, true, last, true, "q2_tx");
            if (h.grant_index() >= 0) granted_q2 = h.grant_index();
        }
        bool ok = (granted_q2 == 2) && (h.fails == f0);
        printf("  [%s] lone queue q2 is granted (idx=%d)\n", ok ? "PASS" : "FAIL", granted_q2);
        if (!ok) h.fails++;
    }

    // ---- Scenario 2: 802.1Q ORDER - the HIGHEST index wins ----
    // q5 (SR class A) must beat q4 (class B) must beat q3 (gPTP) ... down to q0.
    // This is the arbitration half of the queue-map directive: the CBS-shaped
    // classes sit at the TOP of the strict-priority order, which is what
    // 802.1Q-2018 8.6.8.2 credit-based shaping assumes. If the encoder ever
    // scans upward again (q0 winning), every one of these fails.
    {
        long f0 = h.fails;
        for (int lo = 0; lo < NQ - 1; lo++) {
            for (int hi = lo + 1; hi < NQ; hi++) {
                h.reset(4);
                uint32_t pair = (1u << lo) | (1u << hi);
                for (int i = 0; i < 400; i++) h.cycle(pair, false, false, false, "pair_build");
                h.cycle(pair, true, false, true, "pair_arb");
                int g = h.grant_index();
                if (g != hi) {
                    printf("  [FAIL] q%d vs q%d: grant idx=%d (the HIGHER index must win)\n",
                           lo, hi, g);
                    h.fails++;
                }
            }
        }
        // and all six at once: q5 takes it
        h.reset(4);
        for (int i = 0; i < 400; i++) h.cycle(0x3F, false, false, false, "all_build");
        h.cycle(0x3F, true, false, true, "all_arb");
        int gall = h.grant_index();
        if (gall != NQ - 1) {
            printf("  [FAIL] all queues eligible: grant idx=%d (want q%d = SR class A)\n",
                   gall, NQ - 1);
            h.fails++;
        }
        printf("  [%s] 802.1Q order: the higher queue index always wins "
               "(%d pairs + the all-six case, q5 = SR class A on top)\n",
               (h.fails == f0) ? "PASS" : "FAIL", NQ * (NQ - 1) / 2);
    }

    // ---- Scenario 3: a depleted q5 yields to q4 ----
    // Drain q5 (SR class A) negative by transmitting many beats, then offer
    // q5+q4: q4 (allowed) must win because q5's credit is negative (allow=0).
    // THE point of CBS - the top-priority shaped queue does not starve the one
    // below it once it has spent its credit.
    {
        h.reset(4);
        long f0 = h.fails;
        const uint32_t Q5 = 1u << 5, Q4 = 1u << 4;
        // q5 transmits a long burst to drive its credit negative
        for (int i = 0; i < 300; i++) {
            bool last = (i % 30 == 29);
            h.cycle(Q5, true, last, true, "q5_drain");
        }
        // brief settle with no data so allow registers update
        for (int i = 0; i < 4; i++) h.cycle(0x0, false, false, false, "settle");
        bool q5_neg = h.credit(5) < 0;
        // build q4 credit while q5 stays negative & idle-empty
        for (int i = 0; i < 400; i++) h.cycle(Q4, false, false, false, "q4_build");
        h.cycle(Q5 | Q4, true, false, true, "q54_after_drain");
        int g = h.grant_index();
        bool ok = q5_neg && (g == 4) && (h.fails == f0);
        printf("  [%s] depleted q5 drove credit negative, then yields to q4: grant idx=%d\n",
               ok ? "PASS" : "FAIL", g);
        if (!ok) h.fails++;
    }

    // ---- Scenario 4: unshaped strict-priority queue always eligible ----
    // q0 unshaped: even with zero/negative credit it must be grantable immediately.
    {
        h.reset(4);
        Cfg c2 = cfg; c2.shaped = 0x3E;  // q0 unshaped (the reset posture for BE), rest shaped
        h.apply_cfg(c2);
        for (int i = 0; i < 4; i++) h.cycle(0, false, false, false, "reconf");
        long f0 = h.fails;
        // q0 offered immediately with no credit build-up
        h.cycle(0x1, true, false, true, "q0_strict");
        int g = h.grant_index();
        bool ok = (g == 0) && (h.dut->dbg_allow & 0x1) && (h.fails == f0);
        printf("  [%s] unshaped q0 grantable with no credit: allow=0x%X grant idx=%d\n",
               ok ? "PASS" : "FAIL", h.dut->dbg_allow, g);
        if (!ok) h.fails++;
        h.apply_cfg(cfg);
    }

    // ---- Scenario 5: randomized traffic; reference must match every cycle ----
    {
        h.reset(4);
        long f0 = h.fails;
        std::mt19937 rng(0x5EED);
        std::uniform_int_distribution<int> b(0, 1);
        std::uniform_int_distribution<int> q(0, (1 << NQ) - 1);
        for (int i = 0; i < 60000; i++) {
            uint32_t has = q(rng);
            bool tv = b(rng);
            bool tl = b(rng) && b(rng);       // ~25% tlast
            bool tr = b(rng);
            h.cycle(has, tv, tl, tr, "random");
        }
        printf("  [%s] randomized 60000 cycles: grant matches arbiter reference exactly\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- REQ-CBS-07: egress pacing / real occupancy, MEASURED ----
    // 802.1Qav assumes a transmitting queue occupies the port for the frame's
    // real wire time. Ours does not: the shaper hands 8 B per cycle to a MAC
    // FIFO, so at 100 MHz a beat leaves in 10 ns while 8 B on a 1 Gb/s wire take
    // 64 ns. `is_transmitting` is asserted only on ACCEPTED beats (real
    // occupancy of the AXIS port - confirmed below, both drain regimes agree),
    // so the debit is exact per byte; but the queue then ACCRUES idleSlope
    // during the 5.4 cycles per beat that the wire would still be busy.
    //
    // Steady state with accrual on every non-transmitting cycle and an exact
    // per-byte debit:
    //     (CLK - r/8)*S/(8*CLK) + r*(S - link)/link = 0
    //  => r = (S/8) / [ S/(64*CLK) + (link - S)/link ]     bytes/s
    // versus the 802.1Qav ideal r_ideal = S/8. The test asserts the ACCOUNTING
    // model (so any change to the credit arithmetic fails here) and REPORTS the
    // over-delivery against the standard, which is the REQ-CBS-07 finding.
    {
        long f0 = h.fails;
        const int    CYCLES = 200000;
        const int    FBEATS = 8;                 // 64-byte frames
        const double CLK    = 100000000.0;       // wrapper CLK_FREQ_HZ
        const double LINK   = 1000000000.0;      // is_1g_i = 1 in the wrapper

        struct { uint32_t slope; int period; const char* name; } runs[] = {
            { 100000000, 1, "fast drain  (8 B/cycle sink)" },
            { 100000000, 8, "paced drain (1 beat / 8 cyc)" },
            { 200000000, 8, "paced drain, 2x idleSlope   " },
        };
        double bpc[3];
        for (int r = 0; r < 3; r++) {
            long   bytes = run_rate(h, runs[r].slope, runs[r].period, CYCLES, FBEATS, "cbs07");
            double S     = (double)runs[r].slope;
            bpc[r]       = (double)bytes / (double)CYCLES;
            double model = (S / 8.0) / (S / (64.0 * CLK) + (LINK - S) / LINK) / CLK;
            double ideal = S / 8.0 / CLK;
            double merr  = std::fabs(bpc[r] - model) / model * 100.0;
            printf("  [INFO] REQ-CBS-07 %s  %.6f B/cyc | accounting model %.6f (%.2f%%) "
                   "| 802.1Qav ideal %.6f -> OVER-DELIVERS %.1f%%\n",
                   runs[r].name, bpc[r], model, merr, ideal,
                   (bpc[r] / ideal - 1.0) * 100.0);
            // pin the accounting: the startup hiCredit burst and frame
            // quantisation account for well under 1.5% over 200k cycles
            if (merr > 1.5) {
                printf("  [FAIL] cbs07: %s is %.2f%% off the accounting model\n",
                       runs[r].name, merr);
                h.fails++;
            }
        }
        // Both drain regimes must give the SAME rate. This is the real-occupancy
        // check: if bytes_sent/is_transmitting counted anything but accepted
        // beats, throttling the sink 8x would move the answer.
        double disagree = std::fabs(bpc[0] - bpc[1]) / bpc[1] * 100.0;
        if (disagree > 0.5) {
            printf("  [FAIL] cbs07: fast vs paced drain disagree by %.2f%% - "
                   "bytes_sent/is_transmitting are not counting accepted beats\n", disagree);
            h.fails++;
        }
        // non-vacuity: the measurement must track idleSlope, not the harness
        double ratio = bpc[2] / bpc[1];
        if (ratio < 1.5 || ratio > 2.5) {
            printf("  [FAIL] cbs07: 2x idleSlope gave %.3fx the rate (measurement is pinned)\n", ratio);
            h.fails++;
        }
        printf("  [%s] REQ-CBS-07 bytes_sent/is_transmitting track accepted beats "
               "(regimes differ %.2f%%); over-delivery vs 802.1Qav is the UNPACED-EGRESS gap\n",
               (h.fails == f0) ? "PASS" : "FAIL", disagree);
    }

    printf("--------------------------------------------------------------\n");
    printf("cycle checks: %ld   mismatches: %ld\n", h.checks, h.fails);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}

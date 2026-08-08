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

static const int NQ = 5;   // 802.1Q order: q4 = highest priority, q0 = lowest

static int64_t sx48(uint64_t v) {
    v &= (((uint64_t)1 << 48) - 1);
    if (v & ((uint64_t)1 << 47)) v |= ~((((uint64_t)1 << 48) - 1));
    return (int64_t)v;
}
static int popcountq(uint32_t x) { int n = 0; for (int i = 0; i < NQ; i++) n += (x >> i) & 1; return n; }
// priority encoder: HIGHEST set bit index, or -1. Mirrors
// ethernet_packet_pkg::priority_encode, which scans from the top index down
// since the 802.1Q-order map put SR class A on the TOP queue (q4 at N=5).
static int penc(uint32_t req) { for (int i = NQ - 1; i >= 0; i--) if (req & (1u << i)) return i; return -1; }
// one-hot index (grant is always one-hot or zero, so direction is irrelevant)
static int onehot_idx(uint32_t v) { for (int i = 0; i < NQ; i++) if (v & (1u << i)) return i; return -1; }

// milan_csr CBS reset defaults for the 5-queue map, INDEXED BY QUEUE:
// q0 BE / q1 control / q2 gPTP / q3 SR class B / q4 SR class A.
struct Cfg {
    uint32_t idle[NQ] = {25000000, 50000000, 50000000, 150000000, 450000000};
    int32_t  hi[NQ]   = {38, 76, 76, 228, 684};
    int32_t  lo[NQ]   = {-1483, -1445, -1445, -1293, -837};
    uint32_t shaped   = 0x1F; // all shaped by default (this harness, NOT the reset word)
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
            default:return sx48(dut->dbg_credit4);
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

// ---------------------------------------------------------------------------
//  FQTSS helper (802.1Q-2018 clause 34 / 8.6.8.2): offer SEVERAL queues at once,
//  permanently backlogged, and record which queue each ACCEPTED beat went to.
//  That is the only way to see the thing FQTSS actually promises - how the port
//  is SHARED - because a lone-queue rate test can never show a shaped class
//  starving (or being starved by) the traffic underneath it.
//
//  `wait_q`, if >= 0, additionally records the longest run of consecutive
//  ACCEPTED beats during which that queue was NOT the granted one, i.e. its
//  worst-case service gap in port slots.
// ---------------------------------------------------------------------------
static void run_share(Harness& h, const Cfg& c, uint32_t has_data,
                      int ready_period, int cycles, int frame_beats,
                      long beats_q[NQ], int wait_q, long* worst_wait,
                      const char* tag) {
    h.apply_cfg(c);
    h.reset(4);
    for (int i = 0; i < NQ; i++) beats_q[i] = 0;
    long gap = 0;
    if (worst_wait) *worst_wait = 0;
    // let the sequential slope engine commit (2 passes = 200 cycles) first
    for (int i = 0; i < 400; i++) h.cycle(has_data, false, false, true, tag);

    int beat_in_frame = 0;
    for (int i = 0; i < cycles; i++) {
        bool rdy   = (i % ready_period) == 0;
        bool tlast = (beat_in_frame == frame_beats - 1);
        h.dut->eval();                       // pre-edge: the grant in force NOW
        int g = h.grant_index();
        h.cycle(has_data, /*s_tvalid=*/true, tlast, rdy, tag);
        if (g >= 0 && rdy) {
            beats_q[g]++;
            beat_in_frame = tlast ? 0 : beat_in_frame + 1;
            if (wait_q >= 0) {
                if (g == wait_q) gap = 0;
                else if (worst_wait && ++gap > *worst_wait) *worst_wait = gap;
            }
        }
    }
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

    // ---- Scenario 1: single queue q2 (gPTP) wins its own grant ----
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
    // q4 (SR class A) must beat q3 (class B) must beat q2 (gPTP) ... down to q0.
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
        // and all five at once: q4 takes it
        h.reset(4);
        for (int i = 0; i < 400; i++) h.cycle(0x1F, false, false, false, "all_build");
        h.cycle(0x1F, true, false, true, "all_arb");
        int gall = h.grant_index();
        if (gall != NQ - 1) {
            printf("  [FAIL] all queues eligible: grant idx=%d (want q%d = SR class A)\n",
                   gall, NQ - 1);
            h.fails++;
        }
        printf("  [%s] 802.1Q order: the higher queue index always wins "
               "(%d pairs + the all-five case, q4 = SR class A on top)\n",
               (h.fails == f0) ? "PASS" : "FAIL", NQ * (NQ - 1) / 2);
    }

    // ---- Scenario 3: a depleted q4 yields to q3 ----
    // Drain q4 (SR class A) negative by transmitting many beats, then offer
    // q4+q3: q3 (allowed) must win because q4's credit is negative (allow=0).
    // THE point of CBS - the top-priority shaped queue does not starve the one
    // below it once it has spent its credit.
    {
        h.reset(4);
        long f0 = h.fails;
        const uint32_t QA = 1u << 4, QB = 1u << 3;
        // q4 transmits a long burst to drive its credit negative
        for (int i = 0; i < 300; i++) {
            bool last = (i % 30 == 29);
            h.cycle(QA, true, last, true, "q4_drain");
        }
        // brief settle with no data so allow registers update
        for (int i = 0; i < 4; i++) h.cycle(0x0, false, false, false, "settle");
        bool qa_neg = h.credit(4) < 0;
        // build q3 credit while q4 stays negative & idle-empty
        for (int i = 0; i < 400; i++) h.cycle(QB, false, false, false, "q3_build");
        h.cycle(QA | QB, true, false, true, "q43_after_drain");
        int g = h.grant_index();
        bool ok = qa_neg && (g == 3) && (h.fails == f0);
        printf("  [%s] depleted q4 drove credit negative, then yields to q3: grant idx=%d\n",
               ok ? "PASS" : "FAIL", g);
        if (!ok) h.fails++;
    }

    // ---- Scenario 4: unshaped strict-priority queue always eligible ----
    // q0 unshaped: even with zero/negative credit it must be grantable immediately.
    {
        h.reset(4);
        Cfg c2 = cfg; c2.shaped = 0x1E;  // q0 unshaped (the reset posture for BE), rest shaped
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

    // ---- REQ-CBS-07: egress pacing under the WIRE-TIME DEBT law --------
    // 802.1Q-2018 8.6.8.2 (d)/(e): idleSlope accrues only while `transmit`
    // is FALSE, and transmit covers the frame's real wire occupation. The
    // shaper hands 8 B per cycle to a MAC FIFO (10 ns/beat at 100 MHz vs
    // 64 ns of 1 Gb/s wire), and the OLD law accrued on every
    // non-transmitting cycle - measured 9.6 / 20.5 percent over-delivery at
    // idleSlope 100 / 200 Mb/s. credit_based_shaper now carries a per-queue
    // Q16 wire-time debt (bytes per accepted beat + the 24-octet per-frame
    // overhead + min-frame pad at tlast, drained at the port byte rate) and
    // accrues only at debt == 0.
    //
    // Steady state of the debt law (frame of L client bytes, per-frame
    // overhead V = 24 + max(0, 60 - L)):
    //     accrual time * S/8 = debit  with the wire busy L+V octets/frame
    //  => r = (S/8) * L*link / (L*link + V*S)          client bytes/s
    // i.e. the reservation's own per-frame overhead now comes out of the
    // shaped rate. NOTE the deliberate deviation from a bare "r = S/8":
    // with V charged to the debt but the per-byte debit unchanged, exact
    // S/8 is unreachable - the law under-delivers by the V*S/(L*link) term
    // (3.6 percent at 100 Mb/s / 64 B frames) instead of OVER-delivering
    // 9.6/20.5 percent. Both the law's own fixed point AND the
    // over-delivery-is-dead bound are asserted.
    {
        long f0 = h.fails;
        const int    CYCLES = 200000;
        const int    FBEATS = 8;                 // 64-byte frames
        const double CLK    = 100000000.0;       // wrapper CLK_FREQ_HZ
        const double LINK   = 1000000000.0;      // is_1g_i = 1 in the wrapper
        const double LBYTES = 8.0 * FBEATS;      // client bytes per frame
        const double OVH    = 24.0;              // >= 60 B frames: no pad

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
            double model = (S / 8.0) * (LBYTES * LINK)
                           / (LBYTES * LINK + OVH * S) / CLK;
            double ideal = S / 8.0 / CLK;
            double merr  = std::fabs(bpc[r] - model) / model * 100.0;
            printf("  [INFO] REQ-CBS-07 %s  %.6f B/cyc | debt-law model %.6f (%.2f%%) "
                   "| 802.1Qav S/8 %.6f -> delivers %.1f%%\n",
                   runs[r].name, bpc[r], model, merr, ideal,
                   (bpc[r] / ideal - 1.0) * 100.0);
            // (a) the LAW: measured egress = the debt-law fixed point. The
            // closed form assumes wire-continuous frames; a sink SLOWER than
            // the wire (RDYP=8 = 0.8 Gb/s here) opens mid-frame debt gaps
            // that shave up to ~1.5% more (measured 0.1/0.7/1.5% across the
            // three regimes), so the bound is 2% - the OLD law read 13/28%
            // off this model, so the check keeps its teeth.
            if (merr > 2.0) {
                printf("  [FAIL] cbs07: %s is %.2f%% off the debt-law model\n",
                       runs[r].name, merr);
                h.fails++;
            }
            // (b) OVER-DELIVERY IS DEAD: the old law delivered ideal*1.096 /
            // *1.205 here; the debt law may never exceed the reservation
            if (bpc[r] > ideal * 1.005) {
                printf("  [FAIL] cbs07: %s delivers %.2f%% ABOVE S/8 - the "
                       "8.6.8.2 accrual gap is back\n",
                       runs[r].name, (bpc[r] / ideal - 1.0) * 100.0);
                h.fails++;
            }
        }
        // The two drain regimes must agree closely. Under the debt law they
        // are no longer IDENTICAL - a sink slower than the wire (paced leg)
        // opens mid-frame debt gaps the fast leg does not have, worth ~0.8%
        // here - but a bytes_sent/is_transmitting miscount moves this by
        // the full 8x pacing ratio, so 2% still catches that whole class.
        double disagree = std::fabs(bpc[0] - bpc[1]) / bpc[1] * 100.0;
        if (disagree > 2.0) {
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
        printf("  [%s] REQ-CBS-07 debt law: egress = (S/8)*L*link/(L*link+24*S) "
               "at 100 AND 200 Mb/s, never above S/8; regimes differ %.2f%%\n",
               (h.fails == f0) ? "PASS" : "FAIL", disagree);
    }

    // =======================================================================
    //  FQTSS - IEEE 802.1Q-2018 clause 34, "Forwarding and Queuing Enhancements
    //  for Time-Sensitive Streams", as an END STATION must meet it.
    //
    //  Everything above proves the credit ARITHMETIC (tb/verilator/cbs, bit-exact)
    //  and the ARBITER (the per-cycle reference model). FQTSS is the layer above
    //  both: what the port actually does when a shaped SR class and unshaped
    //  traffic contend for it. None of that is visible from a lone-queue rate
    //  test, and with the 6-queue map it is the property the whole ordering
    //  argument rests on - so measure it.
    // =======================================================================
    printf("== FQTSS (802.1Q-2018 clause 34) ==\n");

    // ---- FQTSS-1: 34.3.1 bandwidth availability ------------------------
    // deltaBandwidth: the sum of the SR classes' idleSlope must not exceed the
    // configured maximum (75 % of portTransmitRate is the standard's default and
    // REQ-CBS-03). Read out of ethernet_packet_pkg itself via the wrapper, so
    // this fails if anyone edits the reset slope table past the ceiling.
    {
        long f0 = h.fails;
        const double LINK_1G = 1000000000.0, LINK_100M = 100000000.0;
        uint32_t nq   = dut->cap_nq;
        double sum1g  = (double)dut->cap_sum_1g;
        double sum100 = (double)dut->cap_sum_100m;
        double sumsr  = (double)dut->cap_sum_sr_1g;
        if (nq != (uint32_t)NQ) {
            printf("  [FAIL] NUMBER_OF_QUEUES is %u, harness compiled for %d\n", nq, NQ);
            h.fails++;
        }
        // (a) the SR classes alone - the quantity 34.3.1 actually constrains
        if (sumsr > 0.75 * LINK_1G) {
            printf("  [FAIL] 34.3.1: SR class A+B idleSlope %.0f > 75%% of 1 Gb/s\n", sumsr);
            h.fails++;
        }
        // (b) every queue together, at both link rates (REQ-CBS-03 house rule)
        if (sum1g > 0.75 * LINK_1G) {
            printf("  [FAIL] REQ-CBS-03: sum(IDLE_SLOPE_1G) %.0f > 75%% of 1 Gb/s\n", sum1g);
            h.fails++;
        }
        if (sum100 > 0.75 * LINK_100M) {
            printf("  [FAIL] REQ-CBS-03: sum(IDLE_SLOPE_100M) %.0f > 75%% of 100 Mb/s\n", sum100);
            h.fails++;
        }
        // (c) class A must outrank class B in bandwidth as well as in priority -
        // a Milan talker's audio lives on A, and an A-below-B table would be a
        // silent misprovision that no ordering check can see.
        if (!(dut->cap_slope_sra > dut->cap_slope_srb)) {
            printf("  [FAIL] 34.3.1: class A slope %u must exceed class B %u\n",
                   dut->cap_slope_sra, dut->cap_slope_srb);
            h.fails++;
        }
        printf("  [%s] 34.3.1 bandwidth availability: SR A+B = %.0f Mb/s (%.1f%% of 1G, "
               "ceiling 75%%); all %u queues = %.0f Mb/s (%.1f%%) at 1G and %.1f%% at 100M\n",
               (h.fails == f0) ? "PASS" : "FAIL", sumsr / 1e6, sumsr / LINK_1G * 100.0,
               nq, sum1g / 1e6, sum1g / LINK_1G * 100.0, sum100 / LINK_100M * 100.0);
    }

    // ---- FQTSS-2: the shaped class and best effort SHARE the port ------
    // 8.6.8.2 transmission selection with a credit-based shaper. q4 (SR class A)
    // is shaped and permanently backlogged; q0 (best effort, unshaped) is too.
    // q4 outranks q0 absolutely, so ONLY the credit gate can stop it - and it
    // must, or a talker with one stream would black-hole every other frame the
    // station has to send. Symmetrically q0 must never squeeze q4 out, since q4
    // wins outright whenever its credit is non-negative.
    //
    // Measured against the REQ-CBS-07 debt-law model (the shaped class now
    // delivers its wire-honest rate - slightly UNDER S/link by the per-frame
    // overhead term - and best effort takes the rest).
    {
        long f0 = h.fails;
        const int    CYCLES = 200000, FBEATS = 8, RDYP = 8;
        const double CLK = 100000000.0, LINK = 1000000000.0;
        const double LBYTES = 8.0 * FBEATS, OVH = 24.0;
        // RDYP = 8 -> the sink takes 8 B every 8 cycles = 100 MB/s of port
        const double PORT_BPC = 8.0 / (double)RDYP;

        struct { uint32_t slope; const char* name; } runs[] = {
            { 100000000, "q4 @ 100 Mb/s" },
            { 200000000, "q4 @ 200 Mb/s" },
            { 450000000, "q4 @ 450 Mb/s (the class-A RESET slope)" },
        };
        double share5[3];
        for (int r = 0; r < 3; r++) {
            Cfg c;                                  // reset slopes, then override q4
            c.idle[4] = runs[r].slope;
            c.shaped  = 1u << 4;                    // ONLY q4 shaped; q0 strict/unshaped
            long bq[NQ]; long dummy;
            run_share(h, c, (1u << 4) | (1u << 0), RDYP, CYCLES, FBEATS,
                      bq, -1, &dummy, "fqtss_share");
            long total = 0; for (int i = 0; i < NQ; i++) total += bq[i];
            share5[r]  = total ? (double)bq[4] / (double)total : 0.0;
            double sh0 = total ? (double)bq[0] / (double)total : 0.0;

            double S     = (double)runs[r].slope;
            double model = (S / 8.0) * (LBYTES * LINK)
                           / (LBYTES * LINK + OVH * S) / CLK / PORT_BPC;
            double ideal = S / LINK;

            // (a) NEITHER queue is starved - the FQTSS guarantee, both ways
            if (!(share5[r] > 0.01)) {
                printf("  [FAIL] FQTSS: shaped q4 starved by best effort (%.3f%% of the port)\n",
                       share5[r] * 100.0);
                h.fails++;
            }
            if (!(sh0 > 0.01)) {
                printf("  [FAIL] FQTSS: shaped q4 MONOPOLISED the port - q0 got %.3f%%, "
                       "so the credit gate is not stopping the top-priority queue\n",
                       sh0 * 100.0);
                h.fails++;
            }
            // (b) every accepted beat belongs to exactly one of the two offered
            // queues (no beat attributed to a queue with no data)
            long stray = total - bq[4] - bq[0];
            if (stray != 0) {
                printf("  [FAIL] FQTSS: %ld beats granted to a queue with no data\n", stray);
                h.fails++;
            }
            // (c) the split is the credit accounting's, not the harness's.
            // Frame-grain arbitration against the contending queue costs up
            // to ~2.3% relative at the 450 Mb/s point (measured 0.7/1.5/2.3
            // across the sweep); 3.5% keeps the old law's 9-20% miss red.
            double merr = std::fabs(share5[r] - model) / model * 100.0;
            if (merr > 3.5) {
                printf("  [FAIL] FQTSS: %s took %.2f%% of the port, accounting model says "
                       "%.2f%% (%.2f%% off)\n", runs[r].name, share5[r]*100.0, model*100.0, merr);
                h.fails++;
            }
            printf("  [INFO] FQTSS share  %-38s q4 %6.2f%% | q0 %6.2f%% | model %6.2f%% "
                   "| 802.1Qav reservation %5.2f%%\n",
                   runs[r].name, share5[r]*100.0, sh0*100.0, model*100.0, ideal*100.0);
        }
        // (d) non-vacuity: the split must MOVE with idleSlope, monotonically
        if (!(share5[0] < share5[1] && share5[1] < share5[2])) {
            printf("  [FAIL] FQTSS: q4's share is not monotone in idleSlope "
                   "(%.3f, %.3f, %.3f) - the measurement is not tracking the reservation\n",
                   share5[0], share5[1], share5[2]);
            h.fails++;
        }
        printf("  [%s] 8.6.8.2: a shaped SR class and unshaped best effort SHARE the port - "
               "neither starves the other, and the split tracks idleSlope monotonically\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    // ---- FQTSS-3: NON-VACUITY - unshape q4 and it takes everything -----
    // The partition above must come from the CREDIT GATE, not from the arbiter
    // or the harness. Same stimulus, same priorities, `shaped` cleared: q4 now
    // outranks q0 with nothing to stop it and must take essentially the whole
    // port. If this scenario ALSO showed a split, FQTSS-2 would prove nothing.
    {
        long f0 = h.fails;
        Cfg c; c.idle[4] = 100000000; c.shaped = 0;      // nothing shaped
        long bq[NQ], dummy;
        run_share(h, c, (1u << 4) | (1u << 0), 8, 50000, 8, bq, -1, &dummy, "fqtss_novac");
        long total = 0; for (int i = 0; i < NQ; i++) total += bq[i];
        double sh5 = total ? (double)bq[4] / (double)total : 0.0;
        if (sh5 < 0.99) {
            printf("  [FAIL] FQTSS non-vacuity: UNSHAPED q4 took only %.2f%% of the port - "
                   "the split in FQTSS-2 is not the credit gate's doing\n", sh5 * 100.0);
            h.fails++;
        }
        printf("  [%s] non-vacuity: with CBS off, q4 takes %.2f%% (strict priority, "
               "no credit gate) - so the FQTSS split above IS the shaper\n",
               (h.fails == f0) ? "PASS" : "FAIL", sh5 * 100.0);
    }

    // ---- FQTSS-4: gPTP is not starved by a saturating shaped class -----
    // The 802.1Q-order map puts gPTP on q2, BELOW the CBS-shaped q4/q3. That is
    // a correctness requirement (a strict queue above the shaped classes voids
    // the credit accounting that bounds class-A latency), and the argument for
    // it being harmless is that a credit-shaped q4 MUST yield periodically by
    // construction. This measures that claim instead of asserting it: q4 shaped
    // at its class-A reset slope and permanently backlogged, q2 offered
    // continuously, and we record q2's worst service gap in port slots.
    {
        long f0 = h.fails;
        const int RDYP = 8, FBEATS = 8, CYCLES = 200000;
        Cfg c;                                        // reset slopes (q4 = 450 Mb/s)
        c.shaped = 1u << 4;                           // q4 shaped, q2 strict/unshaped
        long bq[NQ], worst = 0;
        run_share(h, c, (1u << 4) | (1u << 2), RDYP, CYCLES, FBEATS,
                  bq, /*wait_q=*/2, &worst, "fqtss_gptp");
        long total = 0; for (int i = 0; i < NQ; i++) total += bq[i];
        double sh3 = total ? (double)bq[2] / (double)total : 0.0;
        if (bq[2] == 0) {
            printf("  [FAIL] FQTSS: gPTP q2 got ZERO service under a saturating shaped q4\n");
            h.fails++;
        }
        // A Milan class-A stream is 8000 frames/s; gPTP is 8-16 frames/s, i.e.
        // ~0.2 % of the port at 64-90 B. Demand at least an order of magnitude
        // more headroom than gPTP can consume, so a regression that merely
        // *narrows* the gap still fails here rather than passing on a trickle.
        if (sh3 < 0.02) {
            printf("  [FAIL] FQTSS: gPTP q2 got only %.3f%% of the port under a saturating "
                   "shaped q4 - less than 10x what 802.1AS needs\n", sh3 * 100.0);
            h.fails++;
        }
        // worst gap, in accepted 8-byte port slots -> wire time at 1 Gb/s
        double gap_us = (double)worst * 8.0 * 8.0 / 1000.0;
        printf("  [%s] gPTP q2 under a saturating class-A q4: %.2f%% of the port, worst "
               "service gap %ld slots = %.2f us of 1 Gb/s wire time (802.1AS needs "
               "8-16 frames/s)\n", (h.fails == f0) ? "PASS" : "FAIL",
               sh3 * 100.0, worst, gap_us);
    }

    // ---- Scenario: CBS_QUEUES_MASK_P equivalence oracle (2026-07-28) ----
    // The wrap carries a SECOND core with mask 5'b11000 (the builder's
    // derivation: SR class A q4 + class B q3 keep their CBS instance, q0-q2
    // are strict-priority only) on the SAME stimulus. Two properties, both
    // per cycle across everything driven below:
    //   (a) masked-out queues report allow_transmit == 1 ALWAYS - even while
    //       the reference core's same queue is credit-blocked;
    //   (b) the two KEPT queues' allow bits equal the reference core's
    //       bit-for-bit, so the mask provably does not touch them.
    {
        long f0 = h.fails;
        bool saw_ref_block = false;   // the reference q0 must actually block
        bool saw_q4_shape  = false;   // ...and q4 must actually shape (drop+return)
        h.apply_cfg(cfg);
        h.reset(4);
        // the sequential slope engine needs ~2 passes before any queue has a
        // non-zero sendSlope (same warmup run_rate does); without this the
        // whole scenario is vacuous - credit never moves, nothing ever blocks
        for (int i = 0; i < 400; i++) h.cycle(0x11, false, false, true, "mask_warm");
        auto scan = [&](const char* tag) {
            uint32_t ref = dut->dbg_allow, msk = dut->dbg_allow_masked;
            for (int q = 0; q < 3; q++)
                if (!((msk >> q) & 1)) {
                    h.fail(tag, "mask_allow_const1", msk, ref);
                    break;
                }
            if (((msk >> 3) & 3) != ((ref >> 3) & 3))
                h.fail(tag, "mask_kept_equiv", msk, ref);
            if (!((ref >> 0) & 1)) saw_ref_block = true;
            if (!((ref >> 4) & 1)) saw_q4_shape = true;
            h.checks++;
        };
        // deplete q0 in the reference core: continuous transmission burns
        // credit at sendSlope; with q0's small hiCredit it goes negative and
        // the reference blocks - the masked core must not care
        for (int i = 0; i < 600; i++) {
            h.cycle(0x01, true, (i % 10) == 9, true, "mask_q0");
            scan("mask_q0");
            if (getenv("MASK_DBG") && i % 50 == 0)
                printf("    dbg i=%d credit0=%lld allow=0x%X grant=0x%X\n",
                       i, (long long)h.credit(0), dut->dbg_allow, dut->grant_o);
        }
        // now the kept queue: saturate q4 so BOTH cores shape it identically
        for (int i = 0; i < 600; i++) {
            h.cycle(0x10, true, (i % 10) == 9, true, "mask_q4");
            scan("mask_q4");
        }
        if (!saw_ref_block) {
            printf("  [FAIL] mask oracle vacuous: reference q0 never credit-blocked\n");
            h.fails++;
        }
        if (!saw_q4_shape) {
            printf("  [FAIL] mask oracle vacuous: q4 never actually shaped\n");
            h.fails++;
        }
        printf("  [%s] CBS_QUEUES_MASK_P=11000 sibling: q0-q2 allow==1 always "
               "(ref q0 did block), kept q3/q4 bit-equal to the all-CBS core "
               "(q4 did shape)\n", (h.fails == f0) ? "PASS" : "FAIL");
    }

    printf("--------------------------------------------------------------\n");
    printf("cycle checks: %ld   mismatches: %ld\n", h.checks, h.fails);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}

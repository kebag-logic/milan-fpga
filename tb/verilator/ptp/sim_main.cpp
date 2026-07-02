/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for timestamp_counter.sv — the PTP hardware
 * clock (PHC) phase accumulator (REQ-PTP-01..03).
 *
 * A 128-bit software model of the {ns, frac} accumulator (INT=64, FRAC=24)
 * tracks the DUT bit-exactly through: nominal ticking, adjfine rate changes,
 * settime (absolute load), adjtime (signed offset), and gettime (snapshot),
 * including fractional-ns carry into the integer field. Directed checks assert
 * the intended time behaviour; a randomized command stream asserts equivalence.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vtimestamp_counter.h"
#include "verilated.h"

#include <cstdio>
#include <cstdint>
#include <random>

static const int FRAC = 24;   // PTP_INCR is Q8.24 (matches milan_csr reset 0x08000000 = 8.0 ns)
// 8.0 ns nominal per tick @125MHz, in Q8.24 -> 8 << 24
static const uint32_t INCR_8NS = (uint32_t)8u << FRAC;

// 128-bit accumulator model (only need <= 92 bits, use unsigned __int128).
struct Model {
    __int128 acc = 0;                    // {ns:64, frac:24}
    uint64_t snap = 0;
    bool snap_valid = false;

    uint64_t ns() const { return (uint64_t)((unsigned __int128)acc >> FRAC); }

    void step(bool resetn, bool en, uint32_t incr, int32_t adj,
              uint64_t tod_wr, bool load, int64_t offset, bool adjust, bool snapshot) {
        // snapshot latch (registered off the *current* acc, like the RTL)
        bool n_snap_valid = snapshot;
        uint64_t n_snap = snap;
        if (snapshot) n_snap = ns();

        __int128 n_acc;
        if (!resetn) {
            n_acc = 0;
        } else if (load) {
            n_acc = ((__int128)(unsigned __int128)tod_wr) << FRAC;
        } else {
            __int128 next = acc;
            if (en)     next += (__int128)((int64_t)incr) + (__int128)adj;   // Q8.24 step
            if (adjust) next += ((__int128)offset) << FRAC;
            n_acc = next;
        }

        if (!resetn) { snap = 0; snap_valid = false; }
        else { snap = n_snap; snap_valid = n_snap_valid; }
        acc = n_acc;
    }
};

struct Harness {
    Vtimestamp_counter* dut;
    Model m;
    long checks = 0, fails = 0;
    explicit Harness(Vtimestamp_counter* d) : dut(d) {}

    void cycle(bool resetn, bool en, uint32_t incr, int32_t adj,
               uint64_t tod_wr, bool load, int64_t offset, bool adjust, bool snapshot,
               const char* tag) {
        dut->resetn = resetn;
        dut->enable_i = en;
        dut->incr_i = incr;
        dut->adj_i = (uint32_t)adj;
        dut->tod_wr_i = tod_wr;
        dut->cmd_load_i = load;
        dut->offset_i = (uint64_t)offset;
        dut->cmd_adjust_i = adjust;
        dut->cmd_snapshot_i = snapshot;
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();

        m.step(resetn, en, incr, adj, tod_wr, load, offset, adjust, snapshot);

        expect(dut->timestamp_out, m.ns(), tag, "timestamp");
        expect(dut->tod_snapshot_o, m.snap, tag, "snapshot");
        expect(dut->tod_snapshot_valid_o & 1, m.snap_valid ? 1 : 0, tag, "snap_valid");
        checks++;
    }

    // convenience: free-run a nominal tick
    void run(int n, uint32_t incr, int32_t adj, const char* tag) {
        for (int i = 0; i < n; i++) cycle(true, true, incr, adj, 0, false, 0, false, false, tag);
    }

    void expect(uint64_t got, uint64_t exp, const char* tag, const char* what) {
        if (got != exp) {
            if (fails < 20)
                printf("  [FAIL] %-14s %-11s got=%llu exp=%llu\n", tag, what,
                       (unsigned long long)got, (unsigned long long)exp);
            fails++;
        }
    }
    void reset(int n) { for (int i = 0; i < n; i++) cycle(false,false,0,0,0,false,0,false,false,"reset"); }
};

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vtimestamp_counter* dut = new Vtimestamp_counter;
    Harness h(dut);

    printf("== timestamp_counter PHC harness (INT=64, FRAC=%d; nominal 8ns/tick) ==\n", FRAC);

    h.reset(4);

    // ---- Scenario 1: nominal rate -> exactly 8 ns per tick ----
    {
        long f0 = h.fails;
        h.run(1000, INCR_8NS, 0, "nominal");
        bool ok = (dut->timestamp_out == 8ull * 1000) && (h.fails == f0);
        printf("  [%s] nominal 8ns/tick: t=%llu ns after 1000 ticks (expect 8000)\n",
               ok ? "PASS" : "FAIL", (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 2: settime absolute load ----
    {
        long f0 = h.fails;
        uint64_t T = 1234567890123ull;
        h.cycle(true,true,INCR_8NS,0, T, /*load=*/true, 0,false,false, "settime");
        h.run(10, INCR_8NS, 0, "post_settime");
        bool ok = (dut->timestamp_out == T + 8ull*10) && (h.fails == f0);
        printf("  [%s] settime load %llu then +10 ticks -> %llu\n",
               ok ? "PASS" : "FAIL", (unsigned long long)T, (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 3: adjtime signed offset (forward and back) ----
    {
        long f0 = h.fails;
        uint64_t before = dut->timestamp_out;
        h.cycle(true,true,INCR_8NS,0, 0,false, /*offset=*/+1000, /*adjust=*/true,false, "adj_fwd");
        // +offset AND the normal +8 tick both apply
        bool ok1 = (dut->timestamp_out == before + 1000 + 8);
        uint64_t mid = dut->timestamp_out;
        h.cycle(true,true,INCR_8NS,0, 0,false, /*offset=*/-500, true,false, "adj_back");
        bool ok2 = (dut->timestamp_out == mid - 500 + 8);
        bool ok = ok1 && ok2 && (h.fails == f0);
        printf("  [%s] adjtime +1000/-500 ns applied on top of ticks\n", ok ? "PASS" : "FAIL");
        if (!ok) h.fails++;
    }

    // ---- Scenario 4: adjfine fractional rate accumulates carry ----
    // Set adj so that the sub-ns fraction accrues and eventually carries a full
    // ns. With incr=0 and adj=2^(FRAC-2) (=0.25 ns/tick), 4 ticks = 1 ns.
    {
        h.reset(4);
        long f0 = h.fails;
        int32_t quarter = 1 << (FRAC - 2);           // 0.25 ns per tick
        h.run(4, 0, quarter, "adjfine_frac");        // 4 * 0.25 = 1.0 ns
        bool ok = (dut->timestamp_out == 1) && (h.fails == f0);
        printf("  [%s] adjfine 0.25ns/tick x4 -> %llu ns (expect 1, fractional carry)\n",
               ok ? "PASS" : "FAIL", (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 5: negative adjfine slows the clock ----
    {
        h.reset(4);
        long f0 = h.fails;
        // incr = 8ns, adj = -0.5ns -> effective 7.5 ns/tick; after 8 ticks = 60 ns
        int32_t half = 1 << (FRAC - 1);
        h.run(8, INCR_8NS, -half, "adjfine_neg");
        bool ok = (dut->timestamp_out == 60) && (h.fails == f0);
        printf("  [%s] incr8 + adj -0.5ns/tick x8 -> %llu ns (expect 60)\n",
               ok ? "PASS" : "FAIL", (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 6: gettime snapshot latches a stable value ----
    {
        h.reset(4);
        long f0 = h.fails;
        h.run(100, INCR_8NS, 0, "pre_snap");
        uint64_t live = dut->timestamp_out;
        h.cycle(true,true,INCR_8NS,0,0,false,0,false, /*snapshot=*/true, "snap");
        uint64_t snapped = dut->tod_snapshot_o;
        bool vpulse = dut->tod_snapshot_valid_o & 1;
        // keep running; snapshot must stay frozen
        h.run(50, INCR_8NS, 0, "post_snap");
        bool ok = (snapped == live) && vpulse && (dut->tod_snapshot_o == snapped) && (h.fails == f0);
        printf("  [%s] gettime snapshot=%llu frozen while clock advances to %llu\n",
               ok ? "PASS" : "FAIL", (unsigned long long)snapped, (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 7: disable holds the clock ----
    {
        h.reset(4);
        long f0 = h.fails;
        h.run(20, INCR_8NS, 0, "pre_dis");
        uint64_t held = dut->timestamp_out;
        for (int i = 0; i < 30; i++) h.cycle(true,false,INCR_8NS,0,0,false,0,false,false,"disabled");
        bool ok = (dut->timestamp_out == held) && (h.fails == f0);
        printf("  [%s] enable=0 holds time at %llu\n", ok ? "PASS" : "FAIL",
               (unsigned long long)dut->timestamp_out);
        if (!ok) h.fails++;
    }

    // ---- Scenario 8: randomized command stream must track model exactly ----
    {
        h.reset(4);
        long f0 = h.fails;
        std::mt19937_64 rng(0x71337);
        std::uniform_int_distribution<int> b(0, 1);
        std::uniform_int_distribution<int> rare(0, 20);
        std::uniform_int_distribution<int32_t> adjd(-(1 << (FRAC-1)), (1 << (FRAC-1)));
        std::uniform_int_distribution<int64_t> offd(-100000, 100000);
        std::uniform_int_distribution<uint64_t> todd(0, (1ull<<48));
        for (int i = 0; i < 200000; i++) {
            bool en = b(rng);
            uint32_t incr = b(rng) ? INCR_8NS : ((uint32_t)4u << FRAC);
            int32_t adj = adjd(rng);
            bool load = (rare(rng) == 0);
            bool adjust = (rare(rng) == 0);
            bool snap = (rare(rng) == 0);
            h.cycle(true, en, incr, adj, todd(rng), load, offd(rng), adjust, snap, "random");
        }
        printf("  [%s] randomized 200000 command cycles track model exactly\n",
               (h.fails == f0) ? "PASS" : "FAIL");
    }

    printf("--------------------------------------------------------------\n");
    printf("cycle checks: %ld   mismatches: %ld\n", h.checks, h.fails);
    printf("RESULT: %s\n", (h.fails == 0) ? "PASS" : "FAIL");

    dut->final();
    delete dut;
    return (h.fails == 0) ? 0 : 1;
}

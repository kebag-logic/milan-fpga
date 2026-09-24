// SPDX-License-Identifier: CERN-OHL-W-2.0
// R276-5 reviewer probe: randomized property check of KL_media_clock_restart
// against the #387 rulings, graded ONLY on the transmitted-PDU feed (the
// engine's own definition of "on the wire", ruling 5819379503 item 1).
//
// Per talker, a reference reads the feed and the request stream:
//   * a request (restart_p_i, or a clk_src_i change) on a streaming talker
//     sets `pending`;
//   * a reported PDU whose mr differs from the previous reported PDU of the
//     same continuous stream is a TOGGLE. A toggle with no pending request is
//     SPURIOUS (a double toggle / an unmerged request). A toggle clears
//     pending (the merge: every request up to and including that report's
//     cycle is served by it, ruling 5818091077 read at the feed);
//   * HOLD: at least 8 PDUs at a level before the next toggle (4.4.4.3);
//   * LIVENESS: after a quiet tail with many PDUs, no request is still
//     pending (never a cancellation, ruling 5802264260 item 2).
// Within one cycle the request is applied before the report, matching the
// engine (a request in the report's own cycle still sees hold_r == 0).
//
// It also measures the documented residue: requests landing after the
// LAUNCH of a stream's first PDU at a new level and at/before its REPORT.
//
// Usage: Vmcr_prop <seed> <cycles> <mode>   mode 0 = continuous streams,
// mode 1 = random stream stop/start as well. Exit 0 = every property held.
#include "Vmcr_prop_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <random>
#include <vector>

static constexpr int kN = 3;
static constexpr int kHold = 8;

struct Pdu { uint64_t due; int mr; uint64_t launch; };

struct Talker {
    int period = 0;              // launch spacing (cycles)
    uint64_t next_launch = 0;
    std::deque<Pdu> inflight;    // launched, not yet reported (in order)
    // reference state, on the feed
    bool have_level = false;
    int level = 0;
    int at_level = 0;            // PDUs reported at `level` since it began
    bool pending = false;
    uint64_t pending_since = 0;
    long toggles = 0;
    // residue measurement (launch side)
    int launched_level = -1;
    uint64_t first_new_launch = 0;
    bool first_new_unreported = false;
};

int main(int argc, char** argv) {
    const uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
    const uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 200000;
    const int mode = argc > 3 ? atoi(argv[3]) : 0;
    //! optional: print every request and report before this cycle
    const uint64_t trace_to = argc > 4 ? strtoull(argv[4], nullptr, 0) : 0;
    Verilated::commandArgs(argc, argv);
    std::mt19937_64 rng(seed);
    auto rnd = [&](uint64_t n) { return static_cast<uint64_t>(rng() % n); };

    Vmcr_prop_top* dut = new Vmcr_prop_top;
    uint64_t cyc = 0;
    auto tick = [&]() {
        dut->clk_i = 0; dut->eval();
        dut->clk_i = 1; dut->eval();
        ++cyc;
    };

    dut->rst_n = 0; dut->restart_p_i = 0; dut->clk_src_i = 0;
    dut->streaming_i = 0; dut->frame_p_i = 0; dut->frame_idx_i = 0;
    dut->frame_mr_i = 0;
    for (int i = 0; i < 4; i++) tick();
    dut->rst_n = 1;

    Talker t[kN];
    // AAF-like fast talkers and a CRF-like slow one; spacing varies by seed
    t[0].period = 12 + static_cast<int>(rnd(20));
    t[1].period = 16 + static_cast<int>(rnd(40));
    t[2].period = 150 + static_cast<int>(rnd(250));
    unsigned streaming = (1u << kN) - 1;
    uint16_t clk_src = 0;
    // request density: mean gap between requests, varied by seed
    const uint64_t req_gap = 20 + rnd(600);
    const uint64_t quiet_from = cycles;           // tail with no requests
    const uint64_t end = cycles + 40000;

    long fails = 0, requests = 0, residue_hits = 0, merges_seen = 0;
    long spurious = 0, hold_viol = 0, total_toggles = 0;
    auto fail = [&](const char* what, int k) {
        if (fails < 20)
            printf("[FAIL] seed=%llu cyc=%llu talker=%d %s\n",
                   (unsigned long long)seed, (unsigned long long)cyc, k, what);
        ++fails;
    };

    for (; cyc < end;) {
        // ---- inputs for this cycle ----
        const bool req_window = cyc < quiet_from;
        bool rq = req_window && rnd(req_gap) == 0;
        bool src_ch = req_window && rnd(req_gap * 4) == 0;
        dut->restart_p_i = rq;
        if (src_ch) clk_src = static_cast<uint16_t>(clk_src ^ (1 + rnd(3)));
        dut->clk_src_i = clk_src;
        // the engine sees a source change as clk_src_q_r != clk_src_i, i.e.
        // in the cycle the value first differs
        static uint16_t prev_src = 0;
        const bool src_edge = clk_src != prev_src;
        prev_src = clk_src;
        const bool request = rq || src_edge;

        if (mode == 1 && req_window && rnd(5000) == 0) {
            const int k = static_cast<int>(rnd(kN));
            streaming ^= 1u << k;
            if (!((streaming >> k) & 1)) {
                // a stopped stream: its continuity ends; drop the reference
                t[k].inflight.clear();
                t[k].have_level = false; t[k].pending = false;
                t[k].at_level = 0; t[k].launched_level = -1;
                t[k].first_new_unreported = false;
            } else {
                t[k].next_launch = cyc + 1 + rnd(t[k].period);
            }
        }
        dut->streaming_i = streaming;

        // the packetizers: launch latches the level granted NOW (mr_o before
        // this edge); the report follows 0-3 cycles later on the shared feed
        const unsigned mr_now = dut->mr_o;
        for (int k = 0; k < kN; k++) {
            if (!((streaming >> k) & 1)) continue;
            if (cyc >= t[k].next_launch) {
                const int mr = (mr_now >> k) & 1;
                t[k].inflight.push_back({cyc + rnd(4), mr, cyc});
                if (t[k].launched_level >= 0 && mr != t[k].launched_level) {
                    t[k].first_new_launch = cyc;
                    t[k].first_new_unreported = true;
                }
                t[k].launched_level = mr;
                t[k].next_launch = cyc + t[k].period + rnd(3);
            }
        }
        // one report per cycle; the earliest due wins, others defer
        int rep = -1;
        uint64_t best = UINT64_MAX;
        for (int k = 0; k < kN; k++)
            if (!t[k].inflight.empty() && t[k].inflight.front().due <= cyc &&
                t[k].inflight.front().due < best) {
                best = t[k].inflight.front().due; rep = k;
            }
        Pdu rp{};
        if (rep >= 0) { rp = t[rep].inflight.front(); t[rep].inflight.pop_front(); }
        dut->frame_p_i = rep >= 0;
        dut->frame_idx_i = rep >= 0 ? rep : 0;
        dut->frame_mr_i = rep >= 0 ? rp.mr : 0;

        if (trace_to && cyc < trace_to) {
            if (request) printf("TRACE cyc=%llu REQUEST rq=%d src_edge=%d mr_o=%u\n",
                                (unsigned long long)cyc, rq, src_edge, mr_now);
            if (rep >= 0) printf("TRACE cyc=%llu REPORT talker=%d mr=%d launched=%llu mr_o=%u\n",
                                 (unsigned long long)cyc, rep, rp.mr,
                                 (unsigned long long)rp.launch, mr_now);
        }
        // ---- reference, request first, then the report ----
        if (request) {
            ++requests;
            for (int k = 0; k < kN; k++) {
                if (!((streaming >> k) & 1)) continue;
                if (t[k].first_new_unreported) ++residue_hits;
                if (t[k].pending) ++merges_seen;
                if (!t[k].pending) t[k].pending_since = cyc;
                t[k].pending = true;
            }
        }
        // BOUNDED SERVICE: a pending request is on the wire within the rest
        // of one hold plus one PDU (a cancellation that a LATER request
        // happens to repair is caught here, not only at the tail)
        for (int k = 0; k < kN; k++) {
            if (!((streaming >> k) & 1) || !t[k].pending) continue;
            const uint64_t bound =
                static_cast<uint64_t>(kHold + 3) * (t[k].period + 3) + 16;
            if (cyc - t[k].pending_since > bound) {
                fail("STARVED: a pending request is not on the wire within one hold + one PDU", k);
                t[k].pending_since = cyc;   // report once per bound
            }
        }
        if (rep >= 0) {
            Talker& r = t[rep];
            if (!r.have_level) {
                // first PDU of a continuous stream: a baseline, not a toggle;
                // it carries whatever was requested before it
                // (no toggle happened in this stream yet, so the 4.4.4.3
                // hold, which follows a toggle, does not constrain it)
                // It serves a request only if it LAUNCHED after that request:
                // a first PDU already in flight carries the old truth.
                r.have_level = true; r.level = rp.mr; r.at_level = kHold;
                // A request at cycle c is registered at c's edge and granted
                // (mr_o) from c + 2, so only a launch at c + 2 or later can
                // carry it.
                if (r.pending && r.pending_since + 2 <= rp.launch) r.pending = false;
            } else if (rp.mr != r.level) {
                ++r.toggles; ++total_toggles;
                if (!r.pending) { ++spurious; fail("SPURIOUS toggle (no pending request)", rep); }
                if (r.at_level < kHold) { ++hold_viol; fail("HOLD violated (< 8 PDUs at the level)", rep); }
                r.pending = false;
                r.level = rp.mr; r.at_level = 1;
                r.first_new_unreported = false;
            } else {
                ++r.at_level;
            }
        }
        tick();
    }
    long left_pending = 0;
    for (int k = 0; k < kN; k++)
        if (((streaming >> k) & 1) && t[k].pending) {
            ++left_pending;
            fail("CANCELLED: a request is still pending after the quiet tail", k);
        }
    printf("seed=%llu mode=%d periods=%d/%d/%d req_gap=%llu requests=%ld "
           "toggles=%ld merged_requests=%ld residue_requests=%ld spurious=%ld "
           "hold_viol=%ld left_pending=%ld fails=%ld\n",
           (unsigned long long)seed, mode, t[0].period, t[1].period, t[2].period,
           (unsigned long long)req_gap, requests, total_toggles, merges_seen,
           residue_hits, spurious, hold_viol, left_pending, fails);
    delete dut;
    return fails ? 1 : 0;
}

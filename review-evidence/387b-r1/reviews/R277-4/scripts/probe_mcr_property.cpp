// SPDX-License-Identifier: CERN-OHL-W-2.0
// R277-4 reviewer probe: randomized property check of KL_media_clock_restart
// (with KL_talker_diag_ctx, through the committed tb/verilator/tkdiag top).
//
// Model (ruling 5802264260 item 2, boundary 5818091077, report = launched per
// decision 5819379503 item 1): per stream, a request opens a restart need
// unless one is already pending; a need stays pending until the transmitted-
// PDU feed REPORTS a PDU whose mr differs from the last reported PDU. A
// request and a report in the same cycle: the request is taken first (the
// engine reads pre-edge state).
//
// Properties, per stream, all streams streaming throughout:
//   P1 no spurious toggle: every level change on the reported wire closes a
//      pending need;
//   P2 no lost restart: after quiescence, toggles == needs and nothing pends;
//   P3 hold: a level that is itself a toggle is carried by >= 8 reported PDUs
//      before the next toggle;
//   P4 MEDIA_RESET (Table 5.4, per-interval) == toggles (toggles are spaced
//      further apart than one 64-cycle interval, recorded as min spacing).
// Talkers latch mr_o at launch and are reported 0..maxlat cycles later on one
// shared feed (one report per cycle, as the datapath's muxed feed).
#include "Vtkdiag_tb_top.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <random>

namespace {
constexpr int kK = 3;
struct Rep { uint64_t due; int idx; int mr; };
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const unsigned seed = argc > 1 ? static_cast<unsigned>(atoi(argv[1])) : 1u;
    const uint64_t ncyc = argc > 2 ? strtoull(argv[2], nullptr, 10) : 1000000ull;
    const int maxlat = argc > 3 ? atoi(argv[3]) : 3;
    const int req_div = argc > 4 ? atoi(argv[4]) : 150;
    std::mt19937_64 rng(seed);
    auto* d = new Vtkdiag_tb_top;
    uint64_t cyc = 0;
    auto tick = [&] { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); ++cyc; };

    d->rst_n = 0; d->streaming_i = 0; d->mcr_streaming_i = 0; d->frame_p_i = 0;
    d->frame_idx_i = 0; d->frame_mr_i = 0; d->tu_i = 0; d->mcr_restart_p_i = 0;
    d->mcr_clk_src_i = 0; d->rd_idx_i = 0;
    for (int i = 0; i < 8; ++i) tick();
    d->rst_n = 1;
    d->streaming_i = 7; d->mcr_streaming_i = 7;
    for (int i = 0; i < 4; ++i) tick();

    const int period[kK] = {19, 23, 311};
    uint64_t next_launch[kK] = {5, 11, 17};
    int W[kK] = {0, 0, 0};          // last reported level
    bool Pd[kK] = {false, false, false};
    long N[kK] = {0, 0, 0}, T[kK] = {0, 0, 0}, hold[kK] = {0, 0, 0};
    long viol_spurious[kK] = {0, 0, 0}, viol_hold[kK] = {0, 0, 0};
    uint64_t last_toggle[kK] = {0, 0, 0};
    uint64_t min_spacing = UINT64_MAX;
    long reqs = 0, merged = 0, srcchg = 0;
    std::deque<Rep> q;
    uint16_t src = 0;
    const uint64_t warm = 5000, quiet_after = ncyc;
    const uint64_t end = ncyc + 40000;
    long burst_left = 0;

    while (cyc < end) {
        // 1. requests (restart pulse or a clock-source change), none in the
        //    warm-up or the drain; bursts put a second request close behind
        bool req = false;
        d->mcr_restart_p_i = 0;
        if (cyc >= warm && cyc < quiet_after) {
            if (burst_left > 0 && --burst_left == 0) req = true;
            else if (rng() % static_cast<uint64_t>(req_div) == 0) {
                req = true;
                if (rng() % 3 == 0) burst_left = 1 + static_cast<long>(rng() % 400);
            }
            if (req) {
                if (rng() % 8 == 0) { src ^= static_cast<uint16_t>(1 + rng() % 3); d->mcr_clk_src_i = src; ++srcchg; }
                else d->mcr_restart_p_i = 1;
            }
        }
        // 2. launches: latch the pre-edge mr_o
        for (int t = 0; t < kK; ++t) {
            if (cyc >= next_launch[t]) {
                const int m = (d->mcr_mr_o >> t) & 1;
                const uint64_t lat = maxlat > 0 ? rng() % static_cast<uint64_t>(maxlat + 1) : 0;
                q.push_back({cyc + lat, t, m});
                next_launch[t] = cyc + static_cast<uint64_t>(period[t]) + rng() % 3;
            }
        }
        // 3. one report per cycle: the earliest due
        d->frame_p_i = 0;
        int rep_idx = -1, rep_mr = 0;
        for (auto it = q.begin(); it != q.end(); ++it) {
            if (it->due <= cyc) {
                rep_idx = it->idx; rep_mr = it->mr; q.erase(it); break;
            }
        }
        if (rep_idx >= 0) { d->frame_p_i = 1; d->frame_idx_i = rep_idx; d->frame_mr_i = rep_mr; }
        // 4. model: request first, then the report
        if (req) {
            ++reqs;
            for (int t = 0; t < kK; ++t) { if (!Pd[t]) { Pd[t] = true; ++N[t]; } else ++merged; }
        }
        if (rep_idx >= 0) {
            const int t = rep_idx;
            if (rep_mr != W[t]) {
                if (!Pd[t]) ++viol_spurious[t];
                if (T[t] > 0 && hold[t] < 8) ++viol_hold[t];
                if (T[t] > 0 && cyc - last_toggle[t] < min_spacing) min_spacing = cyc - last_toggle[t];
                ++T[t]; W[t] = rep_mr; hold[t] = 1; Pd[t] = false; last_toggle[t] = cyc;
            } else {
                ++hold[t];
            }
        }
        tick();
    }
    // let every interval close
    d->frame_p_i = 0;
    for (int i = 0; i < 400; ++i) tick();
    long bad = 0;
    for (int t = 0; t < kK; ++t) {
        d->rd_idx_i = t; d->eval();
        const long mres = static_cast<long>(d->rd_mreset_o);
        const bool p2 = (T[t] == N[t]) && !Pd[t];
        const bool p4 = (mres == T[t]);
        printf("seed %u ctx %d: needs %ld toggles %ld pending %d spurious %ld holdviol %ld mreset %ld | P1 %s P2 %s P3 %s P4 %s\n",
               seed, t, N[t], T[t], Pd[t] ? 1 : 0, viol_spurious[t], viol_hold[t], mres,
               viol_spurious[t] ? "FAIL" : "ok", p2 ? "ok" : "FAIL",
               viol_hold[t] ? "FAIL" : "ok", p4 ? "ok" : "FAIL");
        bad += (viol_spurious[t] != 0) + (!p2) + (viol_hold[t] != 0) + (!p4);
    }
    printf("seed %u: requests %ld (src changes %ld), merged per-stream %ld, min toggle spacing %llu cycles, maxlat %d\n",
           seed, reqs, srcchg, merged, static_cast<unsigned long long>(min_spacing), maxlat);
    printf("PROBE %s seed %u\n", bad ? "FAIL" : "PASS", seed);
    delete d;
    return bad ? 1 : 0;
}

// Reviewer property probe for KL_media_clock_restart (#387 merge rule).
// Random restart requests against two streaming talkers whose packetizers
// latch the granted level at launch and report it LAT cycles later. Checks:
//  P1 no lost request: after every request each talker launches a PDU whose
//     level differs from the level of its last launch at or before the request
//  P2 hold: two wire toggles of one talker are >= 8 launches apart
//  P3 no stray toggle: wire toggles per talker <= requests
//  P4 settle: once requests stop, every talker settles with no pending restart
//  D1 directed: requests inside one pending window yield exactly one toggle
//  D2 directed: a request on the adoption edge itself merges
//  D3 directed (informational): a request after adoption but before the first
//     launch at the new level is a NEW restart (two toggles)
#include "VKL_media_clock_restart.h"
#include "VKL_media_clock_restart___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <vector>
#include <memory>
#include <unistd.h>

static std::unique_ptr<VKL_media_clock_restart> d;
static long cyc_n = 0, fails = 0, checks = 0;
static void ck(const char* w, long got, long exp) {
  checks++; bool ok = got == exp; if (!ok) fails++;
  printf("  [%s] %s got=%ld exp=%ld\n", ok ? "ok" : "FAIL", w, got, exp);
}
struct Pdu { int t; int mr; long done; };
static const int NT = 2, LAT = 3;
static int period[NT] = {5, 37};
static std::deque<Pdu> inflight;
static std::vector<int> launches[NT];      // levels launched, in order
static std::vector<long> launch_cyc[NT];
static long requests = 0;
static bool auto_launch = true;

static void tick(int req) {
  d->restart_p_i = req;
  // completion feed: at most one per cycle
  d->frame_p_i = 0;
  for (auto it = inflight.begin(); it != inflight.end(); ++it)
    if (it->done <= cyc_n) { d->frame_p_i = 1; d->frame_idx_i = it->t;
      d->frame_mr_i = it->mr; inflight.erase(it); break; }
  // launches latch the granted level before the edge
  if (auto_launch) for (int t = 0; t < NT; t++) if (cyc_n % period[t] == 0) {
    int mr = (d->mr_o >> t) & 1;
    launches[t].push_back(mr); launch_cyc[t].push_back(cyc_n);
    inflight.push_back({t, mr, cyc_n + LAT});
  }
  d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval();
  if (req) requests++;
  cyc_n++;
}
static void launch_now(int t) {
  int mr = (d->mr_o >> t) & 1;
  launches[t].push_back(mr); launch_cyc[t].push_back(cyc_n);
  inflight.push_back({t, mr, cyc_n + LAT});
}
static void reset() {
  inflight.clear(); for (int t = 0; t < NT; t++) { launches[t].clear(); launch_cyc[t].clear(); }
  d->rst_n = 0; d->clk_src_i = 0; d->streaming_i = 0; d->restart_p_i = 0;
  for (int i = 0; i < 4; i++) tick(0);
  d->rst_n = 1; d->streaming_i = 3; requests = 0;
  // forget what the reset cycles launched: those carried the previous run's level
  inflight.clear(); for (int t = 0; t < NT; t++) { launches[t].clear(); launch_cyc[t].clear(); }
}
static int toggles(int t, size_t from = 0) {
  int n = 0; for (size_t i = from + 1; i < launches[t].size(); i++) n += launches[t][i] != launches[t][i-1];
  return n;
}
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = std::make_unique<VKL_media_clock_restart>();
  setvbuf(stdout, nullptr, _IONBF, 0);
  unsigned seed = argc > 1 ? atoi(argv[1]) : 1; srand(seed);
  long lost = 0, holdbad = 0, stray = 0, unsettled = 0, runs = 40;
  for (long r = 0; r < runs; r++) {
    if (getenv("PROBE_TRACE")) printf("run %ld cyc %ld\n", r, cyc_n);
    reset();
    for (int i = 0; i < 400; i++) tick(0);
    std::vector<long> reqc;
    int density = 20 + rand() % 400;
    for (int i = 0; i < 20000; i++) { int q = (rand() % density) == 0; if (q) reqc.push_back(cyc_n); tick(q); }
    for (int i = 0; i < 20000; i++) tick(0);  // quiet: everything drains
    for (int t = 0; t < NT; t++) {
      // P1
      for (long c : reqc) {
        int before = -1; size_t k = 0;
        for (; k < launch_cyc[t].size() && launch_cyc[t][k] <= c; k++) before = launches[t][k];
        bool served = false;
        for (; k < launches[t].size(); k++) if (launches[t][k] != before) { served = true; break; }
        if (!served && before >= 0) lost++;
      }
      // P2
      long last = -1000;
      for (size_t i = 1; i < launches[t].size(); i++) if (launches[t][i] != launches[t][i-1]) {
        if ((long)i - last < 8) holdbad++;
        last = i;
      }
      // P3
      if (toggles(t) > (long)reqc.size()) stray++;
      // P4
      auto* root = d->rootp;
      if (((root->KL_media_clock_restart__DOT__tgt_r >> t) & 1) != ((d->mr_o >> t) & 1)) unsettled++;
    }
  }
  printf("random: %ld runs seed %u\n", runs, seed);
  ck("P1 no request lost on any talker", lost, 0);
  ck("P2 no toggle held fewer than 8 launches", holdbad, 0);
  ck("P3 no talker toggles more often than it was asked", stray, 0);
  ck("P4 every talker settles with no pending restart", unsettled, 0);

  // D1: three requests inside talker 1's pending window -> exactly one toggle
  reset(); for (int i = 0; i < 400; i++) tick(0);
  size_t f0 = launches[1].size();
  tick(1); for (int i = 0; i < 3 * period[1]; i++) tick(0);    // first toggle, now holding
  size_t f1 = launches[1].size();
  tick(1); for (int i = 0; i < 40; i++) tick(0); tick(1); for (int i = 0; i < 40; i++) tick(0); tick(1);
  for (int i = 0; i < 20 * period[1]; i++) tick(0);
  ck("D1 four requests, two restarts: two toggles in all", toggles(1, f0 - 1), 2);
  ck("D1 three requests in one pending window: one more toggle", toggles(1, f1 - 1), 1);

  // D2 / D3: manual launches on talker 1 to place requests exactly
  auto_launch = false; reset(); for (int i = 0; i < 10; i++) tick(0);
  tick(1); tick(0); launch_now(1);                          // level 1 adopted and launched
  for (int k = 0; k < 7; k++) { tick(0); launch_now(1); }    // 8 launches at level 1
  for (int i = 0; i < LAT + 2; i++) tick(0);                 // hold complete
  tick(1);                                                   // new request: adopt next edge
  // adoption happens on the next edge; put a request ON that edge
  int pre = (d->mr_o >> 1) & 1; tick(1); int post = (d->mr_o >> 1) & 1;
  tick(0); tick(0);
  ck("D2 adoption edge seen (level changed)", pre != post, 1);
  ck("D2 a request on the adoption edge merges (no pending after)",
     ((d->rootp->KL_media_clock_restart__DOT__tgt_r >> 1) & 1) == ((d->mr_o >> 1) & 1), 1);
  // D3: now level adopted but nothing launched at it yet; request again
  tick(1); tick(0);
  printf("  [info] D3 request after adoption, before first launch at the new level: pending=%d (1 = a new restart, two wire toggles)\n",
     (int)(((d->rootp->KL_media_clock_restart__DOT__tgt_r >> 1) & 1) != ((d->mr_o >> 1) & 1)));
  // D4 (informational): what the wire carries for the two requests above,
  // D2's (merged into the grant it landed on) and D3's (after the grant,
  // before any PDU at the granted level was launched)
  {
    size_t base = launches[1].size() - 1;   // last launch before either request
    for (int k = 0; k < 24; k++) { launch_now(1); for (int i = 0; i < LAT + 2; i++) tick(0); }
    printf("  [info] D4 wire toggles on talker 1 after the grant-window request: %d "
           "(1 = merged as not yet on the wire, 2 = a second restart)\n", toggles(1, base));
  }
  printf("checks: %ld   failures: %ld\n", checks, fails);
  fflush(stdout);
  d->final();
  _exit(fails ? 1 : 0);   // skip static teardown
}

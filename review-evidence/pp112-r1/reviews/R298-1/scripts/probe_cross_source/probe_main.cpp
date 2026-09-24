// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R298-1): cross-source effects of the #112 invalidation.
// Drives the head's own tb/srp_admission/srp_admission_wrap.sv (same capture
// edge as KL_srp_top). Oracle: Milan 4.3.3.2 slope + greedy source-order
// admission against 75 % of 1 Gb/s, computed over the CURRENT declarations.
// A source that the current-declaration oracle refuses must never show
// sr_admitted; the live sum of per-source granted slopes must never exceed
// the ceiling.
#include "Vsrp_admission_wrap.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <algorithm>

static constexpr unsigned N = TB_SOURCES;
static constexpr uint64_t LIMIT = 750000000ull;
static Vsrp_admission_wrap* d;
static unsigned req = 0, frame[8] = {}, ivl[8] = {};
static unsigned long cyc = 0;
static unsigned fails = 0, checks = 0;

static uint64_t slope(unsigned f, unsigned i) {
  return (std::max(f + 22u, 68u) + 20ull) * i * 64000ull;
}
static unsigned oracle_grants() {
  uint64_t acc = 0; unsigned g = 0;
  for (unsigned s = 0; s < N; ++s) {
    if (!(req >> s & 1)) continue;
    uint64_t sl = slope(frame[s], ivl[s]);
    if (acc + sl <= LIMIT) { acc += sl; g |= 1u << s; }
  }
  return g;
}
static void set_tspec(unsigned s, unsigned f, unsigned i) {
  unsigned sh = 16 * (s % 2);
  d->max_frame_i[s / 2] = (d->max_frame_i[s / 2] & ~(0xffffu << sh)) | (f << sh);
  d->interval_frames_i[s / 2] = (d->interval_frames_i[s / 2] & ~(0xffffu << sh)) | (i << sh);
}
// per-cycle observation
static unsigned pulses_refused[8];
static void tick(const char* tag, bool log) {
  d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); ++cyc;
  unsigned g = d->admitted_o & ((1u << N) - 1);
  unsigned o = oracle_grants();
  uint64_t live = 0;
  for (unsigned s = 0; s < N; ++s) live += d->granted_o[s];
  ++checks;
  if (live > LIMIT) { ++fails; std::printf("FAIL %s cyc=%lu live-sum %llu > ceiling\n", tag, cyc, (unsigned long long)live); }
  for (unsigned s = 0; s < N; ++s) {
    bool grant = g >> s & 1, allowed = o >> s & 1;
    ++checks;
    if (grant && !allowed) {
      ++fails; ++pulses_refused[s];
      if (log) std::printf("FAIL %s cyc=%lu source %u granted (slope %u) but REFUSED by current declarations (oracle grants 0x%02x, dut 0x%02x)\n",
                           tag, cyc, s, d->granted_o[s], o, g);
    }
  }
}
static void change(unsigned s, bool r, unsigned f, unsigned i, const char* tag) {
  req = (req & ~(1u << s)) | (unsigned(r) << s); frame[s] = f; ivl[s] = i;
  set_tspec(s, f, i); d->req_i = req; d->change_i = 1u << s;
  tick(tag, true); d->change_i = 0;
}
static void idle(unsigned n, const char* tag) { while (n--) tick(tag, true); }
static void reset() {
  d->rst_n = 0; d->change_i = 0; d->req_i = 0; d->port_rate_bps_i = 1000000000u;
  for (int k = 0; k < 4; ++k) { d->max_frame_i[k] = 0; d->interval_frames_i[k] = 0; }
  req = 0; std::fill(frame, frame + 8, 0u); std::fill(ivl, ivl + 8, 0u);
  for (int k = 0; k < 4; ++k) tick("reset", false);
  d->rst_n = 1;
}
static void phase(unsigned p) { for (unsigned n = 0; n < N && d->sample_index_o != p; ++n) tick("align", true); }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = new Vsrp_admission_wrap;
  const unsigned BIG = 7770;   // slope 499,968,000 bps: one fits, two do not
  unsigned case_fail[4] = {};
  for (unsigned p = 0; p < N; ++p) {
    // Case A: identical re-declaration of lower-index source 0 while the
    // higher-index source N-1 stands refused behind it.
    unsigned f0 = fails;
    reset(); phase(p);
    change(0, true, BIG, 1, "A-setup"); idle(4 * N, "A-setup");
    change(N - 1, true, BIG, 1, "A-setup"); idle(4 * N, "A-setup");
    phase(p);
    change(0, true, BIG, 1, "A-identical-redeclare-src0"); idle(4 * N, "A-after");
    case_fail[0] += fails - f0;
    // Case B: lower-index source 0 re-declares with a DIFFERENT TSpec that
    // still dominates (grow) while source N-1 stands refused.
    f0 = fails;
    reset(); phase(p);
    change(0, true, BIG, 1, "B-setup"); idle(4 * N, "B-setup");
    change(N - 1, true, BIG, 1, "B-setup"); idle(4 * N, "B-setup");
    phase(p);
    change(0, true, BIG + 500, 1, "B-grow-src0"); idle(4 * N, "B-after");
    case_fail[1] += fails - f0;
    // Case C (control, legitimate): source 0 shrinks so N-1 may be admitted.
    f0 = fails;
    reset(); phase(p);
    change(0, true, BIG, 1, "C-setup"); idle(4 * N, "C-setup");
    change(N - 1, true, BIG, 1, "C-setup"); idle(4 * N, "C-setup");
    phase(p);
    change(0, true, 224, 1, "C-shrink-src0"); idle(4 * N, "C-after");
    case_fail[2] += fails - f0;
    // Case D: same as A but source 0 re-declares twice, 5 cycles apart.
    f0 = fails;
    reset(); phase(p);
    change(0, true, BIG, 1, "D-setup"); idle(4 * N, "D-setup");
    change(N - 1, true, BIG, 1, "D-setup"); idle(4 * N, "D-setup");
    phase(p);
    change(0, true, BIG, 1, "D-redeclare"); idle(5, "D-mid");
    change(0, true, BIG, 1, "D-redeclare"); idle(4 * N, "D-after");
    case_fail[3] += fails - f0;
  }
  std::printf("SUMMARY N=%u caseA_identical=%u caseB_grow=%u caseC_shrink_control=%u caseD_double=%u refused-grant-cycles-per-source:",
              N, case_fail[0], case_fail[1], case_fail[2], case_fail[3]);
  for (unsigned s = 0; s < N; ++s) std::printf(" %u", pulses_refused[s]);
  std::printf("\n%u checks: %u PASS, %u FAIL\n", checks, checks - fails, fails);
  delete d;
  return fails ? 1 : 0;
}

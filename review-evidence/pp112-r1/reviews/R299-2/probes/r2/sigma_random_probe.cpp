// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R299-2, issue #112 / PR #114 round 2). Drives
// KL_srp_admission through the suite's capture wrapper
// (tb/srp_admission/srp_admission_wrap.sv) with seeded random traffic:
// declarations, identical re-declarations, shrinks, grows, withdrawals,
// bursts shorter than a round, and (in MULTI mode) several sources changed
// on the same edge. Written independently of the DUT's pipeline: the model
// knows only the current declarations and the clock of the last change.
//
// Judged on EVERY clock:
//  R1 admitted subset of requesting; granted slope is 0 unless admitted and
//     equals the exact Milan 4.3.3.2 slope of the CURRENT TSpec if admitted.
//  R2 live sum of granted slopes <= 75 % ceiling and <= published sum.
//  R3 a publication (round strobe) equals the greedy index-order walk over
//     every current declaration (grants, slopes, sum, over_limit).
//  R4 no publication earlier than one full round after the last change.
//  R5 between publications: no grant rises; a grant falls only on its own
//     source's change edge (or its request falling); slopes, sum and
//     over_limit hold.
//  R6 liveness: after the last change, a publication arrives within
//     3*N clocks (4 at N = 1).
//  R7 cross-source: a source refused by the last publication whose own
//     declaration has not changed since never grants before the next
//     publication, whatever other sources declare or withdraw (implied by
//     R5; counted separately so the exercised hold clocks are visible).
#include VTOP_H
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

namespace {
constexpr unsigned N = TB_SOURCES;
constexpr uint64_t RATE = 1000000000ull;
constexpr uint64_t LIMIT = RATE / 2 + RATE / 4;
constexpr unsigned MAX_LAT = N == 1 ? 4 : 3 * N;
uint64_t slope(unsigned f, unsigned i) {
  return (std::max(f + 22u, 68u) + 20ull) * i * 64000ull;
}
uint64_t sat(uint64_t v) { return v > 0xFFFFFFFFull ? 0xFFFFFFFFull : v; }
struct Rng {
  uint64_t s;
  uint32_t next() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return uint32_t(s); }
  unsigned pick(unsigned n) { return next() % n; }
};
// frames chosen so that 1..4 of them compete for the 750 Mb/s ceiling
constexpr std::array<unsigned, 10> FRAMES = {224, 1520, 2000, 4645, 6208,
                                             10000, 10895, 11395, 20000, 29};
struct Probe {
  VTOP* d;
  std::array<unsigned, 8> fr{}, iv{};
  unsigned req = 0;
  long now = 0, last_change = -1000000, last_pub = -1;
  unsigned checks = 0, fails = 0;
  unsigned pubs = 0, changes = 0, held_clocks = 0, max_lat = 0, r7_watch = 0,
           r7_clocks = 0;
  unsigned watch = 0;  // R7: refused at the last publication, unchanged since
  bool await = false;
  void check(bool ok, const char* what) {
    ++checks;
    if (!ok) {
      ++fails;
      if (fails <= 40) std::printf("FAIL: %s N=%u clock=%ld\n", what, N, now);
    }
  }
  unsigned greedy(uint64_t* sum_out, bool* over_out) const {
    uint64_t sum = 0; unsigned g = 0; bool over = false;
    for (unsigned s = 0; s < N; ++s) {
      if (!(req & (1u << s))) continue;
      uint64_t sl = slope(fr[s], iv[s]);
      if (sum + sl <= LIMIT) { g |= 1u << s; sum += sl; } else over = true;
    }
    if (sum_out) *sum_out = sum;
    if (over_out) *over_out = over;
    return g;
  }
  void reset() {
    d->rst_n = 0; d->change_i = 0; d->req_i = 0;
    d->port_rate_bps_i = uint32_t(RATE);
    req = 0; fr.fill(0); iv.fill(0);
    for (int k = 0; k < 4; ++k) { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
    d->rst_n = 1;
    now = 0; last_change = -1000000; last_pub = -1; await = false; watch = 0;
  }
  // one clock; `chg` is the set of sources whose declaration this edge captures
  void tick(unsigned chg) {
    const unsigned g0 = d->admitted_o;
    const uint32_t sum0 = d->sum_o;
    const bool over0 = d->over_o;
    std::array<uint32_t, 8> sl0{};
    for (unsigned s = 0; s < N; ++s) sl0[s] = d->granted_o[s];
    d->change_i = chg;
    d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval();
    d->change_i = 0;
    ++now;
    if (chg) { last_change = now; await = true; ++changes; }
    // R1, R2
    uint64_t live = 0;
    for (unsigned s = 0; s < N; ++s) {
      bool g = (d->admitted_o >> s) & 1u;
      check(!g || ((req >> s) & 1u), "R1 admitted implies requesting");
      check(g ? d->granted_o[s] == sat(slope(fr[s], iv[s])) : d->granted_o[s] == 0,
            "R1 granted slope is the current TSpec's slope, else 0");
      live += d->granted_o[s];
    }
    check(live <= LIMIT, "R2 live sum within ceiling");
    check(live <= d->sum_o, "R2 live sum never exceeds the published sum");
    if (d->round_o) {
      ++pubs;
      uint64_t gs; bool go;
      unsigned g = greedy(&gs, &go);
      bool slopes = true;
      for (unsigned s = 0; s < N; ++s)
        slopes &= d->granted_o[s] == (((g >> s) & 1u) ? slope(fr[s], iv[s]) : 0);
      check(d->admitted_o == g && slopes && d->sum_o == gs && bool(d->over_o) == go,
            "R3 publication equals greedy walk over current declarations");
      check(now - last_change >= long(N), "R4 no publication within a round of a change");
      if (await) {
        max_lat = std::max<unsigned>(max_lat, unsigned(now - last_change));
        await = false;
      }
      last_pub = now;
      watch = req & ~d->admitted_o;
    } else {
      bool ok = (d->admitted_o & ~g0) == 0;
      check(ok, "R5 no grant rises between publications");
      unsigned fell = g0 & ~d->admitted_o;
      check((fell & ~(chg | ~req)) == 0, "R5 a grant falls only with its own change");
      for (unsigned s = 0; s < N; ++s)
        if (!((chg >> s) & 1u) && ((d->admitted_o >> s) & 1u))
          check(d->granted_o[s] == sl0[s], "R5 unchanged granted slope holds");
      check(d->sum_o == sum0 && bool(d->over_o) == over0, "R5 aggregate holds");
      if (await) ++held_clocks;
    }
    if (await) check(now - last_change <= long(MAX_LAT), "R6 publication within bound");
    watch &= ~chg;
    if (!d->round_o && watch) {
      r7_clocks += await;
      check((d->admitted_o & watch) == 0, "R7 refused unchanged source never licensed");
    }
  }
  void change(unsigned mask, bool withdraw_allowed, Rng& r) {
    for (unsigned s = 0; s < N; ++s) {
      if (!((mask >> s) & 1u)) continue;
      unsigned k = r.pick(10);
      bool on = !(withdraw_allowed && k == 0);
      unsigned f = fr[s], i = iv[s];
      if (k >= 2 || i == 0) {  // new TSpec (k==1 keeps an identical one)
        f = FRAMES[r.pick(FRAMES.size())];
        i = r.pick(16) == 0 ? 2 + r.pick(3) : 1;
        if (r.pick(64) == 0) { f = 0xffff; i = 0xffff; }
      }
      unsigned sh = 16 * (s % 2);
      d->max_frame_i[s / 2] = (d->max_frame_i[s / 2] & ~(0xffffu << sh)) | (f << sh);
      d->interval_frames_i[s / 2] = (d->interval_frames_i[s / 2] & ~(0xffffu << sh)) | (i << sh);
      req = (req & ~(1u << s)) | (unsigned(on) << s);
      fr[s] = f; iv[s] = i;
    }
    d->req_i = req;
    tick(mask);
    r7_watch += (watch & ~mask) != 0;
  }
};
}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const bool multi = argc > 1 && argv[1][0] == 'm';
  const unsigned seeds = argc > 2 ? unsigned(std::atoi(argv[2])) : 200;
  VTOP top;
  Probe p{&top};
  for (unsigned seed = 1; seed <= seeds; ++seed) {
    Rng r{0x9E3779B97F4A7C15ull * seed + N};
    p.reset();
    for (unsigned ev = 0; ev < 400; ++ev) {
      unsigned mask = 1u << r.pick(N);
      if (multi && r.pick(3) == 0) mask |= 1u << r.pick(N);
      p.change(mask, true, r);
      // gap: burst (< a round), mid, or quiet (> the latency bound)
      unsigned kind = r.pick(8);
      unsigned gap = kind < 3 ? r.pick(N + 1) : kind < 5 ? r.pick(3 * N + 2) : 3 * N + 4 + r.pick(2 * N);
      for (unsigned c = 0; c < gap; ++c) p.tick(0);
    }
    for (unsigned c = 0; c < 4 * N + 8; ++c) p.tick(0);
  }
  std::printf("SUMMARY N=%u mode=%s seeds=%u changes=%u publications=%u held_clocks=%u "
              "r7_hold_events=%u r7_refused_watched_clocks=%u max_latency=%u bound=%u\n",
              N, multi ? "multi" : "single", seeds, p.changes, p.pubs, p.held_clocks,
              p.r7_watch, p.r7_clocks, p.max_lat, MAX_LAT);
  std::printf("%u checks: %u PASS, %u FAIL\n", p.checks, p.checks - p.fails, p.fails);
  top.final();
  return p.fails ? 1 : 0;
}

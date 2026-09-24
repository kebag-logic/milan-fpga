// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R299-1, issue #112 / PR #114). Drives KL_srp_admission
// through the suite's capture wrapper (head) or a copy without the
// invalidate_i connection (base). Two things are measured on EVERY clock:
//
//  P1 stale-grant (the parent-review idea, re-run at processor level with
//     two concurrently requesting sources): a source whose CURRENT TSpec
//     cannot fit even alone (20000 bytes after 224 bytes) must never grant.
//  P2 cross-source licence: while a lower-index source L stays admitted
//     through an identical or shrinking re-declaration, a higher-index
//     source H that the greedy walk refuses BEFORE and AFTER the change
//     (its own TSpec never changes) must never grant.
//
// Oracle: exact Milan 4.3.3.2 slope and greedy index-order admission at the
// 75% ceiling of 1 Gb/s, written independently of the DUT.
#include VTOP_H
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <string>

namespace {
constexpr unsigned N = TB_SOURCES;
constexpr uint64_t LIMIT = 750000000ull;
uint64_t slope(unsigned f, unsigned i) {
  return (std::max(f + 22u, 68u) + 20ull) * i * 64000ull;
}
struct Bench {
  VTOP* d;
  std::array<unsigned, 8> fr{}, iv{};
  unsigned req = 0;
  unsigned checks = 0, fails = 0;
  void tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
  void reset() {
    d->rst_n = 0; d->change_i = 0; d->req_i = 0; d->port_rate_bps_i = 1000000000u;
    req = 0; fr.fill(0); iv.fill(0);
    for (int k = 0; k < 4; ++k) tick();
    d->rst_n = 1;
  }
  void set(unsigned s, bool r, unsigned f, unsigned i) {
    unsigned sh = 16 * (s % 2);
    d->max_frame_i[s / 2] = (d->max_frame_i[s / 2] & ~(0xffffu << sh)) | (f << sh);
    d->interval_frames_i[s / 2] = (d->interval_frames_i[s / 2] & ~(0xffffu << sh)) | (i << sh);
    req = (req & ~(1u << s)) | (unsigned(r) << s);
    fr[s] = f; iv[s] = i;
    d->req_i = req; d->change_i = 1u << s;
    tick();
    d->change_i = 0;
  }
  unsigned greedy() const {
    uint64_t sum = 0; unsigned g = 0;
    for (unsigned s = 0; s < N; ++s) {
      if (!(req & (1u << s))) continue;
      uint64_t sl = slope(fr[s], iv[s]);
      if (sum + sl <= LIMIT) { g |= 1u << s; sum += sl; }
    }
    return g;
  }
  void phase(unsigned p) { for (unsigned n = 0; d->sample_index_o != p && n < N; ++n) tick(); }
  void check(bool ok, const char* what, unsigned p) {
    ++checks;
    if (!ok) { ++fails; if (fails <= 40) std::printf("FAIL: %s phase=%u\n", what, p); }
  }
};
}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  VTOP top;
  Bench b{&top};
  const unsigned lo = 0, hi = N - 1;
  const unsigned F700 = 10895, F643 = 10000, F131 = 2000;  // 699.968M, 642.688M, 130.688M
  unsigned p1_pulses = 0, p2_pulses_identical = 0, p2_pulses_shrink = 0;
  unsigned p2_max_len = 0;
  for (unsigned p = 0; p < N; ++p) {
    // ---- P1: two sources hold 224 B; re-declare `hi` then `lo` at 20000 B
    for (unsigned victim : {hi, lo}) {
      b.reset();
      b.set(lo, true, 224, 1); b.set(hi, true, 224, 1);
      for (unsigned k = 0; k < 4 * N + 8; ++k) b.tick();
      b.check((top.admitted_o & ((1u << lo) | (1u << hi))) == ((1u << lo) | (1u << hi)),
              "P1 precondition: both 224-byte sources granted", p);
      b.phase(p);
      b.set(victim, true, 20000, 1);
      bool pulse = false;
      for (unsigned k = 0; k < 6 * N + 8; ++k) {
        pulse |= (top.admitted_o >> victim) & 1u;
        b.tick();
      }
      pulse |= (top.admitted_o >> victim) & 1u;
      p1_pulses += pulse;
      b.check(!pulse, "P1 refused 20000-byte re-declaration never grants", p);
      unsigned other = victim == hi ? lo : hi;
      b.check(((top.admitted_o >> other) & 1u) == 1u, "P1 other 224-byte source stays granted", p);
    }
    // ---- P2: lo ~700M admitted, hi ~131M refused (sum 830.7M > 750M)
    for (int mode = 0; mode < 2; ++mode) {
      b.reset();
      b.set(lo, true, F700, 1); b.set(hi, true, F131, 1);
      for (unsigned k = 0; k < 4 * N + 8; ++k) b.tick();
      unsigned before = b.greedy();
      b.check(((top.admitted_o >> lo) & 1u) && !((top.admitted_o >> hi) & 1u),
              "P2 precondition: lo granted, hi refused", p);
      b.phase(p);
      b.set(lo, true, mode == 0 ? F700 : F643, 1);  // identical / shrink
      unsigned after = b.greedy();
      bool hi_refused_both = !((before >> hi) & 1u) && !((after >> hi) & 1u);
      b.check(hi_refused_both, "P2 oracle: hi refused before and after", p);
      unsigned run = 0, longest = 0; bool pulse = false;
      for (unsigned k = 0; k < 6 * N + 8; ++k) {
        bool g = (top.admitted_o >> hi) & 1u;
        pulse |= g; run = g ? run + 1 : 0; longest = std::max(longest, run);
        b.tick();
      }
      p2_max_len = std::max(p2_max_len, longest);
      if (mode == 0) p2_pulses_identical += pulse; else p2_pulses_shrink += pulse;
      b.check(!pulse, mode == 0
                  ? "P2 identical re-declaration of lo never licenses refused hi"
                  : "P2 shrink of lo (still admitted) never licenses refused hi", p);
      b.check(((top.admitted_o >> lo) & 1u) && !((top.admitted_o >> hi) & 1u),
              "P2 settles: lo granted, hi refused", p);
    }
  }
  std::printf("SUMMARY N=%u P1_stale_pulses=%u/%u P2_identical_pulses=%u/%u "
              "P2_shrink_pulses=%u/%u P2_longest_hi_grant_cycles=%u\n",
              N, p1_pulses, 2 * N, p2_pulses_identical, N, p2_pulses_shrink, N, p2_max_len);
  std::printf("%u checks: %u PASS, %u FAIL\n", b.checks, b.checks - b.fails, b.fails);
  top.final();
  return b.fails ? 1 : 0;
}

#!/usr/bin/env python3
"""Insert R421-3's seeded random-press probe into a scratch copy's
tb/pp_top/notify_phases.hpp (reviewer-owned; never part of the reviewed tree).

After section ID's own arms, the probe drives identify_button_i with a seeded
random sequence of presses and releases (1 ms to 2.5 s each, with a random
clock offset), optionally with random MAC tx_ready stalls, and grades the wire
alone against invariants read from IEEE 1722.1-2021 7.5.1 / Figure 7-142 and
the head's own contract (integrator guide 6, 06 section 7):

  R421R1 frames come in bursts of three, each byte-exact, one sequence_id per
         burst, +1 per burst;
  R421R2 every gap between two consecutive identify frames >= T-IDENT-BURST;
  R421R3 every press edge is answered: a burst's first frame leaves after it,
         within 3 x T-IDENT-BURST + 4 x SLACK (plus the stalled time that
         overlaps, in stall mode);
  R421R4 no burst is unexplained: each one after the first answers at least one
         press edge made since the previous burst's first frame, or is the
         re-arm of a button held throughout, at least T-IDENT-REARM after the
         previous first frame (at most SLACK more without stalls);
  R421R5 (no stalls) a button held for T-IDENT-REARM + SLACK past a burst's
         first frame re-arms.

Environment of the run: R421_SEED (hex/dec), R421_STEPS, R421_STALL (0/1).
Usage: r421_3_random.py TREE
"""
import sys
from pathlib import Path

PROBE = r'''
  // ---- R421-3 random-press probe (reviewer-owned, never committed) ----
  struct R421Stall {
    uint64_t a, b;
  };
  uint64_t r421_x = 0;
  uint64_t r421_rand() {
    r421_x ^= r421_x << 13;
    r421_x ^= r421_x >> 7;
    r421_x ^= r421_x << 17;
    return r421_x;
  }
  uint64_t r421_uni(uint64_t lo, uint64_t hi) { return lo + r421_rand() % (hi - lo + 1); }
  std::vector<R421Stall> r421_stalls;
  void r421_adv(uint64_t n) {
    for (uint64_t i = 0; i < n; ++i) {
      bool stalled = false;
      for (const R421Stall& s : r421_stalls)
        if (io.t >= s.a && io.t < s.b) stalled = true;
      if (!r421_stalls.empty()) io.mac_tx_ready = !stalled;
      tick();
    }
  }
  uint64_t r421_stalled_in(uint64_t a, uint64_t b) const {
    uint64_t n = 0;
    for (const R421Stall& s : r421_stalls) {
      const uint64_t lo = std::max(a, s.a);
      const uint64_t hi = std::min(b, s.b);
      if (hi > lo) n += hi - lo;
    }
    return n;
  }
  void r421_random_presses() {
    const char* e_seed = getenv("R421_SEED");
    const char* e_steps = getenv("R421_STEPS");
    const char* e_stall = getenv("R421_STALL");
    r421_x = e_seed ? strtoull(e_seed, nullptr, 0) : 0xC6A4213ull;
    if (r421_x == 0) r421_x = 1;
    const long steps = e_steps ? strtol(e_steps, nullptr, 0) : 120;
    const bool stall = e_stall && atoi(e_stall) != 0;
    press(false);
    io.mac_tx_ready = true;
    run_ms(2500);
    const size_t from = seen.size();
    const uint64_t t_begin = io.t;
    // the press plan: (level, clocks) pairs
    std::vector<std::pair<bool, uint64_t>> plan;
    uint64_t total = 0;
    for (long s = 0; s < steps; ++s) {
      const uint64_t r1 = r421_rand() % 10;
      const uint64_t on_ms = r1 < 4 ? r421_uni(1, 40) : r1 < 7 ? r421_uni(41, 300) : r421_uni(301, 2500);
      const uint64_t r2 = r421_rand() % 10;
      const uint64_t off_ms = r2 < 4 ? r421_uni(1, 40) : r2 < 8 ? r421_uni(41, 400) : r421_uni(401, 1500);
      const uint64_t on = on_ms * MS_CYC + r421_rand() % MS_CYC;
      const uint64_t off = off_ms * MS_CYC + r421_rand() % MS_CYC;
      plan.push_back({true, on});
      plan.push_back({false, off});
      total += on + off;
    }
    r421_stalls.clear();
    if (stall) {
      uint64_t t = t_begin;
      while (t < t_begin + total) {
        t += r421_uni(200, 2000) * MS_CYC + r421_rand() % MS_CYC;
        const uint64_t len = r421_uni(1, 300) * MS_CYC + r421_rand() % MS_CYC;
        r421_stalls.push_back({t, t + len});
        t += len;
      }
    }
    // drive it; record each press edge and each level interval
    std::vector<uint64_t> edges;
    std::vector<std::pair<uint64_t, uint64_t>> highs;  // [press, release)
    for (const auto& st : plan) {
      if (st.first) edges.push_back(io.t);
      press(st.first);
      const uint64_t t0 = io.t;
      r421_adv(st.second);
      if (st.first) highs.push_back({t0, io.t});
    }
    press(false);
    r421_adv(3000L * MS_CYC);
    const size_t n_stalls = r421_stalls.size();
    io.mac_tx_ready = true;
    const auto v = idents(from);
    if (const char* dump = getenv("R421_DUMP")) {
      // every event for offline analysis: E edge, H high, S stall, F frame
      if (FILE* df = fopen(dump, "w")) {
        for (const uint64_t e : edges) fprintf(df, "E %llu\n", (unsigned long long)e);
        for (const auto& hv : highs) fprintf(df, "H %llu %llu\n", (unsigned long long)hv.first, (unsigned long long)hv.second);
        for (const R421Stall& s : r421_stalls) fprintf(df, "S %llu %llu\n", (unsigned long long)s.a, (unsigned long long)s.b);
        for (const Seen& f : v) fprintf(df, "F %llu %u\n", (unsigned long long)f.t, seq_of(f.f));
        for (size_t i = from; i < seen.size(); ++i)
          if (da_of(seen[i].f) != IDENT_MAC) fprintf(df, "O %llu\n", (unsigned long long)seen[i].t);
        fclose(df);
      }
    }
    // R421R1: bursts of three, one sequence_id each, +1 per burst
    bool r1 = (v.size() % 3) == 0 && !v.empty();
    std::vector<uint64_t> first;
    for (size_t i = 0; i + 2 < v.size() && r1; i += 3) {
      const unsigned s = seq_of(v[i].f);
      if (!(v[i].f == ident(uint16_t(s)) && v[i + 1].f == ident(uint16_t(s))
            && v[i + 2].f == ident(uint16_t(s)))) r1 = false;
      if (i >= 3 && s != ((seq_of(v[i - 3].f) + 1) & 0xFFFFu)) r1 = false;
      first.push_back(v[i].t);
    }
    CHECK(r1, "R421R1: seed 0x%llx stall %d: %zu identify frames in bursts of "
          "three, byte-exact, one sequence_id per burst, +1 per burst",
          (unsigned long long)strtoull(e_seed ? e_seed : "0", nullptr, 0), int(stall), v.size());
    // R421R2: every gap >= T-IDENT-BURST
    long min_gap = 1L << 40;
    for (size_t i = 1; i < v.size(); ++i) min_gap = std::min(min_gap, long(v[i].t - v[i - 1].t));
    CHECK(v.size() < 2 || min_gap >= BURST, "R421R2: smallest gap between two identify "
          "frames %ld clocks, want >= %ld", min_gap, BURST);
    // R421R3: each edge answered by the first burst whose first frame leaves
    // at least 150 clocks after it (a press's own start takes ~166)
    const long live = 3 * BURST + 4 * SLACK;
    long worst = 0;
    long min_start = 1L << 40;
    size_t lost = 0;
    std::vector<int> answered(first.size(), 0);
    std::vector<int> alt(first.size(), 0);
    for (const uint64_t tp : edges) {
      size_t k = 0;
      while (k < first.size() && first[k] < tp + 150) ++k;
      if (k == first.size()) { ++lost; printf("  [r] edge at %llu: no burst after it\n", (unsigned long long)tp); continue; }
      ++answered[k];
      // stall mode: a burst may have started before the edge while its first
      // frame was held in the MAC; then the edge is a new press inside that
      // burst and the next burst is its answer. Such an edge may explain
      // either (R421R4), its latency is bounded against the later one
      if (r421_stalled_in(tp, first[k]) > 0 && k + 1 < first.size()) {
        ++alt[k + 1];
        const long lat2 = long(first[k + 1] - tp);
        if (lat2 > live + long(r421_stalled_in(tp, first[k + 1]))) --alt[k + 1];
      }
      const long lat = long(first[k] - tp);
      const long allow = live + long(r421_stalled_in(tp, first[k]));
      min_start = std::min(min_start, lat);
      worst = std::max(worst, lat - long(r421_stalled_in(tp, first[k])));
      if (lat > allow) {
        ++lost;
        printf("  [r] edge at %llu answered %ld clocks later (allow %ld)\n",
               (unsigned long long)tp, lat, allow);
      }
    }
    CHECK(lost == 0, "R421R3: every one of %zu press edges answered by a burst within "
          "%ld clocks (+ stalled time): %zu not", edges.size(), live, lost);
    // R421R4/R5: every burst explained; a held button re-arms
    auto held = [&](uint64_t a, uint64_t b) {
      for (const auto& hv : highs) if (hv.first <= a && hv.second >= b) return true;
      return false;
    };
    size_t unexplained = 0, rearms = 0, missed_rearm = 0;
    for (size_t k = 0; k < first.size(); ++k) {
      if (answered[k] > 0 || alt[k] > 0) continue;
      const long d = k > 0 ? long(first[k] - first[k - 1]) : -1;
      // stall mode: the re-arm is decided at the timeout; a stall may then
      // hold its first frame in the MAC past the release
      const uint64_t until = stall ? first[k - (k > 0)] + REARM : first[k] - 200;
      const bool ok = k > 0 && held(first[k - 1] - 150, until) && d >= REARM
                      && (stall || d <= REARM + SLACK);
      if (ok) { ++rearms; continue; }
      ++unexplained;
      printf("  [r] burst %zu at %llu unexplained (prev first %lld)\n", k,
             (unsigned long long)first[k], k > 0 ? (long long)first[k - 1] : -1LL);
    }
    CHECK(unexplained == 0, "R421R4: %zu bursts, each answers a press edge or is the "
          "re-arm of a held button: %zu unexplained", first.size(), unexplained);
    if (!stall) {
      for (size_t k = 0; k < first.size(); ++k) {
        if (!held(first[k] - 150, first[k] + REARM + SLACK)) continue;
        const bool next = k + 1 < first.size() && long(first[k + 1] - first[k]) <= REARM + SLACK;
        if (!next) { ++missed_rearm; printf("  [r] burst %zu held but not re-armed\n", k); }
      }
      CHECK(missed_rearm == 0, "R421R5: a button held T-IDENT-REARM + SLACK past a "
            "burst's first frame re-arms: %zu missed", missed_rearm);
    }
    printf("  [i] R421R: seed %s stall %d: %ld steps, %zu edges, %zu bursts (%zu re-arms), "
           "%zu stalls, smallest gap %ld, press-to-first-frame %ld..%ld clocks (stall-free)\n",
           e_seed ? e_seed : "default", int(stall), steps, edges.size(), first.size(), rearms,
           n_stalls, min_gap, min_start, worst);
    r421_stalls.clear();
  }

  void run() {
    boot_to_idle(true);
'''


def main() -> int:
    path = Path(sys.argv[1]) / "tb/pp_top/notify_phases.hpp"
    text = path.read_text()
    old = "  void run() {\n    boot_to_idle(true);\n    one_press_sends_one_burst();\n"
    assert text.count(old) == 1, "anchor"
    text = text.replace(old, PROBE + "    one_press_sends_one_burst();\n", 1)
    old2 = "    a_tx_stall_mid_burst_never_bunches_it();\n  }\n"
    assert text.count(old2) == 1, "anchor2"
    text = text.replace(old2, "    a_tx_stall_mid_burst_never_bunches_it();\n"
                        "    r421_random_presses();\n  }\n", 1)
    if "#include <cstdlib>" not in text:
        text = "#include <cstdlib>\n" + text
    path.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

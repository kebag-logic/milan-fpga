// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes R420-3 (disposable; never part of the suite). Included into a
// private copy of tb/pp_top/notify_phases.hpp just before run_identify(), and
// run in place of IdentifyPhase in the third build (P-EN-IDENTIFY-NOTIFICATION
// = 1). Every arm boots its own fresh processor, so identifySequenceID starts
// at 0 in each, and grades only what the wire shows: frame count, byte-exact
// frames at a per-burst sequence_id counted from 0, and every inter-frame gap
// (last byte to last byte) at least T-IDENT-BURST.
struct R420Probe : IdentifyPhase {
  using IdentifyPhase::IdentifyPhase;
  long min_gap_all = 1L << 40;

  //! grade frames v: exactly `bursts` bursts of three, byte-exact at
  //! sequence_id 0, 1, ...; every gap >= T-IDENT-BURST
  void grade(const std::vector<Seen>& v, size_t bursts, const char* tag) {
    CHECK(v.size() == 3 * bursts, "%s: %zu frames, want %zu (%zu bursts)", tag,
          v.size(), 3 * bursts, bursts);
    for (size_t i = 0; i < v.size(); ++i) {
      const uint16_t seq = uint16_t(i / 3);
      CHECK(v[i].f == ident(seq), "%s: frame %zu byte-exact at sequence_id %u",
            tag, i + 1, unsigned(seq));
    }
    long mg = 1L << 40;
    for (size_t k = 0; k + 1 < v.size(); ++k) mg = std::min(mg, gap_of(v, k));
    if (v.size() > 1) {
      min_gap_all = std::min(min_gap_all, mg);
      CHECK(mg >= BURST, "%s: smallest inter-frame gap %ld clocks, want >= %ld",
            tag, mg, BURST);
    }
    printf("  [p] %s: %zu frames, smallest gap %ld clocks\n", tag, v.size(),
           v.size() > 1 ? mg : -1L);
  }
  void fresh() {
    seen.clear();
    gap_arms.clear();
    gap_ends.clear();
    boot_to_idle(true);
  }
  //! a 30 ms press and its burst; returns the third frame's clock (0: none)
  uint64_t lead(bool hold_through) {
    press(true);
    if (!hold_through) {
      run_ms(30);
      press(false);
    }
    wait_idents(0, 3);
    const auto v = idents(0);
    return v.size() >= 3 ? v[2].t : 0;
  }
  void until(uint64_t t) {
    while (io.t < t) tick();
  }
  void pulse_clocks(long n) {
    press(true);
    for (long c = 0; c < n; ++c) tick();
    press(false);
  }

  //! RP3a: held through the whole burst (no release inside it), let go 2 ms
  //! after the third frame, pressed again at 10 ms for 30 ms: HOLD -> WAITING
  //! -> the WAITING latch. One more burst, never sooner than T-IDENT-BURST.
  void rp3a() {
    fresh();
    const uint64_t t3 = lead(true);
    until(t3 + 2 * MS_CYC);
    press(false);
    until(t3 + 10 * MS_CYC);
    press(true);
    run_ms(30);
    press(false);
    run_ms(1500);
    grade(idents(0), 2, "RP3a held-through, release+press in gap");
  }
  //! RP3b: three 10 ms presses inside one gap: one burst, not three
  void rp3b() {
    fresh();
    const uint64_t t3 = lead(false);
    for (long at : {5L, 40L, 90L}) {
      until(t3 + uint64_t(at * MS_CYC));
      press(true);
      run_ms(10);
      press(false);
    }
    run_ms(1500);
    grade(idents(0), 2, "RP3b three presses in one gap");
  }
  //! RP3c: two release/press cycles inside one burst (between frames 1-2 and
  //! 2-3), each let go at once: exactly one owed burst
  void rp3c() {
    fresh();
    press(true);
    wait_idents(0, 1);
    press(false);
    run_ms(20);
    press(true);
    run_ms(10);
    press(false);
    wait_idents(0, 2);
    run_ms(20);
    press(true);
    run_ms(10);
    press(false);
    run_ms(2000);
    grade(idents(0), 2, "RP3c two re-presses inside one burst");
  }
  //! RP3d: a release inside a burst with no new press: no extra burst
  void rp3d() {
    fresh();
    press(true);
    wait_idents(0, 1);
    press(false);
    run_ms(2000);
    grade(idents(0), 1, "RP3d release only");
  }
  //! RP3e: a 1-clock press (after the integrator's debounce) 20 ms into the
  //! gap; and a 1-clock press inside the burst after a release
  void rp3e() {
    fresh();
    const uint64_t t3 = lead(false);
    until(t3 + 20 * MS_CYC);
    pulse_clocks(1);
    run_ms(1500);
    grade(idents(0), 2, "RP3e 1-clock press in gap");
    fresh();
    press(true);
    run_ms(5);
    press(false);
    wait_idents(0, 1);
    run_ms(30);
    pulse_clocks(1);
    run_ms(1500);
    grade(idents(0), 2, "RP3e' 1-clock press between frames 1 and 2");
  }
  //! RP3f: a chain: the latched burst starts with the button up, and a new
  //! press during that latched burst is owed one more; 3 bursts in all
  void rp3f() {
    fresh();
    const uint64_t t3 = lead(false);
    until(t3 + 20 * MS_CYC);
    press(true);
    run_ms(10);
    press(false);
    wait_idents(0, 4);
    run_ms(30);
    press(true);
    run_ms(10);
    press(false);
    run_ms(2000);
    grade(idents(0), 3, "RP3f press inside a latched burst");
  }
  //! RP3g: frame 3's last byte held 300 ms by the MAC; meanwhile the button
  //! (released after frame 1) is pressed again for 10 ms: one owed burst,
  //! T-IDENT-BURST after frame 3 actually left
  void rp3g() {
    fresh();
    press(true);
    run_ms(10);
    press(false);
    wait_idents(0, 2);
    for (long c = 0; c < 300L * MS_CYC && !mid_ident_frame(); ++c) tick();
    io.tx_eof_stalled = false;
    io.stall_tx_at_eof = true;
    for (long c = 0; c < 1000 && !io.tx_eof_stalled; ++c) tick();
    const bool stalled = io.tx_eof_stalled;
    run_ms(100);
    press(true);
    run_ms(10);
    press(false);
    run_ms(190);
    io.stall_tx_at_eof = false;
    io.mac_tx_ready = true;
    io.tx_eof_stalled = false;
    run_ms(1500);
    CHECK(stalled, "RP3g premise: frame 3's last byte was held");
    grade(idents(0), 2, "RP3g press while frame 3's last byte is held");
  }
  //! RP3h: a 3-clock press placed at clock offset k from the gap's end
  //! (IDENT-BURST expiry after frame 3, predicted from a calibration run):
  //! every placement sends exactly one more burst, never two, never none
  void rp3h() { rp3_boundary(3, -12, 6, "RP3h"); }
  //! RP3j: the same with a 1-clock press, so that for one k the press is
  //! sampled by the sequencer only on the edge that also samples the expiry
  void rp3j() { rp3_boundary(1, -6, 4, "RP3j"); }
  void rp3_boundary(long width, long k_lo, long k_hi, const char* name) {
    // calibration: where the expiry falls against its arm's deadline ms
    fresh();
    uint64_t t3 = lead(false);
    for (long c = 0; c < 10L * MS_CYC && gap_deadline_after(t3) == 0; ++c) tick();
    uint32_t dl = gap_deadline_after(t3);
    run_ms(200);
    const uint64_t e = gap_end_after(t3);
    const long sweep = long(int64_t(e) - clock_of_ms(dl));
    printf("  [p] %s calibration: expiry %ld clocks into its deadline ms\n", name, sweep);
    for (long k = k_lo; k <= k_hi; ++k) {
      fresh();
      t3 = lead(false);
      for (long c = 0; c < 10L * MS_CYC && gap_deadline_after(t3) == 0; ++c) tick();
      dl = gap_deadline_after(t3);
      const int64_t ge = clock_of_ms(dl) + sweep;
      while (int64_t(io.t) < ge + k) tick();
      pulse_clocks(width);
      run_ms(1500);
      const uint64_t got = gap_end_after(t3);
      char tag[96];
      snprintf(tag, sizeof tag, "%s w=%ld k=%ld (expiry %s)", name, width, k,
               int64_t(got) == ge ? "as predicted" : "MISPREDICTED");
      CHECK(int64_t(got) == ge, "%s: premise", tag);
      grade(idents(0), 2, tag);
    }
  }
  //! RP3i: a 5 ms press every 7 ms offset across the whole gap and past it
  //! (2 to 170 ms after frame 3): one more burst each time
  void rp3i() {
    for (long d = 2; d <= 170; d += 7) {
      fresh();
      const uint64_t t3 = lead(false);
      until(t3 + uint64_t(d * MS_CYC));
      press(true);
      run_ms(5);
      press(false);
      run_ms(1300);
      char tag[64];
      snprintf(tag, sizeof tag, "RP3i press at +%ld ms", d);
      grade(idents(0), 2, tag);
    }
  }
  void run() {
    rp3a();
    rp3b();
    rp3c();
    rp3d();
    rp3e();
    rp3f();
    rp3g();
    rp3h();
    rp3j();
    rp3i();
    printf("  [p] smallest inter-frame gap over every probe: %ld clocks\n", min_gap_all);
  }
};

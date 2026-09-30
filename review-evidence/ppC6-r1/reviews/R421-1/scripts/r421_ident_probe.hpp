// R421-1 reviewer probe (disposable; never part of the reviewed tree).
// Grades the gap between IDENTIFY_NOTIFICATION frames 2 and 3 when frame 2
// meets contention or TX backpressure, which sections ID1..ID6 never create
// (ID5 contends only with frame 1, ID6 holds only before frame 1).
struct R421IdentProbe : IdentifyPhase {
  using IdentifyPhase::IdentifyPhase;
  long min12 = 1L << 40, min23 = 1L << 40;
  //! press, wait for frame 1 on the wire, release, then run `hook` at
  //! t1 + offset clocks; returns the burst's gaps (or -1 if not 3 frames)
  std::pair<long, long> burst_with(long offset, const std::function<void()>& hook) {
    const size_t from = seen.size();
    press(true);
    for (long c = 0; c < 50L * MS_CYC && idents(from).empty(); ++c) tick();
    press(false);
    if (idents(from).empty()) return {-1, -1};
    const uint64_t t1 = idents(from)[0].t;
    while (io.t < t1 + uint64_t(offset)) tick();
    hook();
    run_ms(1500);
    const auto v = idents(from);
    if (v.size() != 3) { printf("  [p] offset %ld: %zu identify frames\n", offset, v.size()); return {-1, -1}; }
    return {long(v[1].t - v[0].t), long(v[2].t - v[1].t)};
  }
  void run_probe() {
    boot_to_idle(true);
    int ok = 0;
    for (unsigned k = 0; k < 15; ++k)
      ok += register_controller(FAN_MAC + k, FAN_EID + k, uint16_t(0x5B00 + k)) ? 1 : 0;
    printf("  [p] P0 registered %d of 15\n", ok);
    // P1: a 15-row SET_NAME fan-out timed around frame 2's deadline
    unsigned n = 0;
    for (long off = BURST - 1200; off <= BURST + 300; off += 50) {
      char text[32];
      snprintf(text, sizeof text, "R421 probe %u", n);
      const auto body = clock_domain_name(text);
      const uint16_t s = uint16_t(0x5C00 + n++);
      const auto g = burst_with(off, [&] {
        feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, s, AEM_SET_NAME, body));
      });
      if (g.first < 0) continue;
      printf("  [p] P1 fan-out at frame1+%ld clocks: gaps %ld and %ld\n", off, g.first, g.second);
      min12 = std::min(min12, g.first);
      min23 = std::min(min23, g.second);
    }
    printf("  [p] P1 min gap1->2 %ld, min gap2->3 %ld clocks (T-IDENT-BURST %ld)\n", min12, min23, BURST);
    // P2: MAC TX backpressure after frame 1, of several lengths
    for (long stall_ms : {100L, 200L, 250L, 320L}) {
      const auto g = burst_with(1000, [&] {
        io.mac_tx_ready = false;
        run_ms(stall_ms);
        io.mac_tx_ready = true;
      });
      printf("  [p] P2 TX stalled %ld ms from frame1+10 ms: gaps %ld and %ld clocks\n", stall_ms, g.first, g.second);
    }
    for (unsigned k = 0; k < 15; ++k) (void)deregister_controller(FAN_MAC + k, FAN_EID + k, uint16_t(0x5D00 + k));
  }
};
[[maybe_unused]] static void run_r421_probe(H& h) {
  R421IdentProbe{h}.run_probe();
}

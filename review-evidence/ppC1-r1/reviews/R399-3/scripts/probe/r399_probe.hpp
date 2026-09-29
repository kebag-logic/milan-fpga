// R399-3 composition probe (disposable; included by a scratch copy of tb/pp_top/sim_main.cpp).
// At the full processor top it runs C1's peer-LeaveAll restart (802.1Q-2014 Table 10-5
// rLA!) while #132's D3 writer holds AECP (no restore started), and again after the boot
// restore released AECP, each with an AECP command flood. It prints one line per case
// and grades: no own MSRP LeaveAll while a peer's arrives every second, the next own one
// 10-15 s after the last peer's, and the AECP hold state (held: no response, drops
// counted in snapshot word 37; booted: answered).
struct R399Probe {
  H& h;
  static std::vector<uint8_t> peer_la_msrp() {
    Vec v; v.la = true; v.nov = 1; v.fv = fv_domain(6, 3, 2); v.ev = {1};   // Domain JoinIn, LeaveAll
    return mrpdu_frame(true, 0x02000000B1B1ULL, {Msg{4, 4, false, {v}}});
  }
  static std::vector<uint8_t> read_entity(uint16_t seq) {
    return aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, seq, 0x0004,
                      std::vector<uint8_t>(8, 0));
  }
  std::vector<long> own_la;   // ms of every own MSRP LeaveAll MRPDU
  int aecp_rsp = 0;
  void drain() {
    while (!h.q_msrp.empty()) {
      auto p = parse_mrpdu(h.q_msrp.front());
      h.q_msrp.pop_front();
      for (auto& v : p.vecs) if (v.la) { own_la.push_back(long(h.now_ms())); break; }
    }
    aecp_rsp += int(h.q_aecp.size()); h.q_aecp.clear();
    h.q_mvrp.clear(); h.q_adp.clear(); h.q_acmp.clear(); h.q_maap.clear();
  }
  void run_case(const char* name, bool boot, bool flood, int peers) {
    own_la.clear(); aecp_rsp = 0;
    Suite setup(h);
    setup.load_descriptor_image();
    h.reset();
    if (boot) {
      setup.boot_restore_over_blank_nvm();
      long g = 4000000;
      while (h.d->dbg_d3_own_o && g-- > 0) h.step();
    }
    h.d->link_up_i = 1;
    h.d->entity_enable_i = 1;
    const long t0 = long(h.now_ms());
    long t_last = -1; uint16_t seq = 1; int sent = 0;
    for (long ms = 0; ms < 2000 + 1000L * peers + 16500; ++ms) {
      const long rel = ms - 2000;
      if (rel >= 0 && rel % 1000 == 0 && rel / 1000 < peers) {
        h.feed(peer_la_msrp()); t_last = long(h.now_ms()); ++sent;
      } else if (flood && rel >= 0 && rel < 1000L * peers && (ms % 100) == 50) {
        h.feed(read_entity(seq++));
      }
      h.idle(MS_CYC);
      drain();
    }
    const long t_first_peer = t0 + 2000;
    int in_peer = 0; long next_after = -1;
    for (long t : own_la) {
      if (t >= t_first_peer && t <= t_last) ++in_peer;
      if (t > t_last && next_after < 0) next_after = t - t_last;
    }
    printf("R399P %s: t0=%ld first_peer=%ld last_peer=%ld own_la_ms=", name, t0, t_first_peer, t_last);
    for (long t : own_la) printf("%ld ", t);
    printf("\n");
    const bool held = h.d->dbg_d3_own_o != 0;
    const uint32_t w37 = h.snap(37) & 0xFFFFu;
    printf("R399P %s: boot=%d flood=%d peers=%d own_la_total=%zu own_la_in_peer_window=%d "
           "next_own_after_last_peer_ms=%ld aecp_held_at_end=%d aecp_responses=%d word37_drops=%u\n",
           name, int(boot), int(flood), sent, own_la.size(), in_peer, next_after, int(held),
           aecp_rsp, unsigned(w37));
    CHECK(in_peer == 0, "R399P %s: %d own MSRP LeaveAll inside the peer window", name, in_peer);
    CHECK(next_after >= 10000 && next_after <= 15400,
          "R399P %s: next own MSRP LeaveAll %ld ms after the last peer", name, next_after);
    if (boot) {
      CHECK(!held, "R399P %s: AECP released by the boot restore", name);
      if (flood) CHECK(aecp_rsp > 0, "R399P %s: AECP answered after the release", name);
    } else {
      CHECK(held, "R399P %s: AECP still held (no restore started)", name);
      if (flood) CHECK(aecp_rsp == 0 && w37 > 0, "R399P %s: AECP unanswered, drops counted", name);
    }
  }
  void run() {
    const int c0 = h.checks, f0 = h.fails;
    run_case("held+flood", false, true, 30);
    run_case("booted+flood", true, true, 30);
    printf("R399P: %d checks, %d failures\n", h.checks - c0, h.fails - f0);
  }
};

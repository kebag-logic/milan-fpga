// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes, round 2 (not part of the suite). Appended to a disposable
// copy of tb/pp_top/d3_phases.hpp; run with --probe-r2. Everything printed,
// nothing graded here: the reviewer reads the lines against the rulings.
//
// A: the DR3a aggregate (ruling: 1,000 ms from the accepted PP_CTRL[1],
//    enforced, the per-wait terminal path on expiry).
//   A0 every grant withheld TMO - 12 cycles: the edge. At the head the
//      binding walk's first wait reaches its per-wait bound (that walk fails,
//      release at about TMO), while each D3 wait ends inside its deadline
//      (longest 20,000 of 20,001), so the D3 walk ends at the aggregate.
//   A1 every grant withheld TMO - 13 cycles, one cycle inside the per-wait
//      deadline, erased device (the bound falls in pass 1).
//   A2 the same with every record framed, restore_go_i held as a LEVEL for
//      the whole boot (firmware leaves PP_CTRL[1] set).
//   A3 the same, with a second restore_go_i pulse at half the bound: does a
//      repeated PP_CTRL[1] restart or extend the bound?
//   A4 after an aggregate DEFAULTS: ADP enabled, a queued AECP command
//      answered, a new one answered.
// B: the AECP hold admission (ruling: one AECP record while held, the rest
//    dropped at the slot gate and counted, non-AECP latency unchanged).
//   B1 CLOSED, six AECP commands back to back with NO inter-frame idle,
//      then a GET_RX_STATE at once: its latency against idle; word 37.
//   B2 CLOSED, eight (AECP, GET_RX_STATE) pairs back to back with no idle:
//      how many GET_RX_STATE are answered.
//   B3 slowed restore (grant held 15,000 cycles), six AECP back to back
//      and a GET: latency; at COMPLETE the held one answered; then after
//      the terminal two AECP back to back: both answered, word 37 unchanged.
struct ProbeR2 {
  H& h;
  const std::vector<uint8_t>& image;
  const std::vector<ImgEnt>& ents;
  ProbeR2(H& tally, const std::vector<uint8_t>& img, const std::vector<ImgEnt>& e)
      : h(tally), image(img), ents(e) {}

  static constexpr long TMO = D3RestorePhase::RS_TMO;
  static constexpr long AGG = D3RestorePhase::AGG;

  struct Obs { long release = -1, done = -1, closed = -1; };
  //! boot with a go pattern: go(c) says whether restore_go_i is 1 at clock c
  template <class Go>
  Obs boot_go(D3RestorePhase& r, long cycles, Go go) {
    Obs o;
    long maxwd = 0, maxbw = 0;
    for (long c = 0; c < cycles; ++c) {
      r.x.d->restore_go_i = go(c) ? 1 : 0;
      r.x.step();
      maxwd = std::max(maxwd, long(r.x.d->dbg_d3_wd_o));
      maxbw = std::max(maxbw, long(r.x.d->dbg_bind_wd_o));
      if (o.release < 0 && r.x.d->dbg_lsn_released_o) o.release = c;
      if (o.done < 0 && r.x.d->restore_done_o) o.done = c;
      if (o.closed < 0 && r.x.d->restore_closed_o) o.closed = c;
      if ((o.done >= 0 || o.closed >= 0) && c > std::max(o.done, o.closed) + 100) break;
    }
    r.x.d->restore_go_i = 0;
    printf("        longest D3 wait %ld, longest binding wait %ld, per-wait bound %ld\n",
           maxwd, maxbw, TMO);
    return o;
  }
  void report(const char* tag, D3RestorePhase& r, const Obs& o) {
    const auto* d = r.x.d;
    printf("PROBE %s: release %ld, done at clock %ld, closed at clock %ld "
           "(aggregate %ld); fail %u cause %u rb %u closed %u applied %u\n",
           tag, o.release, o.done >= 0 ? o.done + 1 : -1,
           o.closed >= 0 ? o.closed + 1 : -1, AGG, unsigned(d->restore_fail_o),
           unsigned(d->rs_cause_o), unsigned(d->restore_rb_o),
           unsigned(d->restore_closed_o), unsigned(d->dbg_d3_applied_o));
  }

  static constexpr int IN = static_cast<int>(TMO - 13);   // one cycle inside
  void a0() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed_every_record();
    r.x.nv_gnt_every = IN + 1;
    const Obs o = boot_go(r, AGG + 4 * TMO, [](long c) { return c < 5; });
    r.x.nv_gnt_every = 0;
    report("A0 framed, at the per-wait edge", r, o);
  }
  void a1() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.x.nv_gnt_every = IN;
    const Obs o = boot_go(r, AGG + 4 * TMO, [](long c) { return c < 5; });
    r.x.nv_gnt_every = 0;
    report("A1 erased, one cycle inside", r, o);
  }
  void a2() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed_every_record();
    r.x.nv_gnt_every = IN;
    const Obs o = boot_go(r, AGG + 4 * TMO, [](long) { return true; });
    r.x.nv_gnt_every = 0;
    report("A2 framed, go held as a level", r, o);
  }
  void a3() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed_every_record();
    r.x.nv_gnt_every = IN;
    const Obs o = boot_go(r, 2 * AGG, [](long c) {
      return c < 5 || (c >= AGG / 2 && c < AGG / 2 + 5);
    });
    r.x.nv_gnt_every = 0;
    report("A3 framed, go pulsed again at AGG/2", r, o);
  }
  void a4() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed_every_record();
    r.x.d->entity_enable_i = 1;
    r.x.d->link_up_i = 1;
    r.x.nv_gnt_every = static_cast<int>(TMO - 200);
    r.x.feed(d3_read_entity_cmd(0xA401));        // held from reset
    const Obs o = boot_go(r, AGG + 4 * TMO, [](long c) { return c < 5; });
    r.x.nv_gnt_every = 0;
    report("A4 framed, a command held from reset", r, o);
    const auto held = r.x.wait_any(r.x.q_aecp, 50);
    r.x.q_aecp.clear();
    r.x.feed(d3_read_entity_cmd(0xA402));
    const auto fresh_rsp = r.x.wait_any(r.x.q_aecp, 50);
    printf("PROBE A4: adp enable %u, the held command answered byte-exact %d, a "
           "new command answered byte-exact %d, own %u\n",
           unsigned(r.x.d->dbg_adp_enable_o), held == d3_read_entity_rsp(0xA401) ? 1 : 0,
           fresh_rsp == d3_read_entity_rsp(0xA402) ? 1 : 0, unsigned(r.x.d->dbg_d3_own_o));
    r.x.d->entity_enable_i = 0;
  }

  // ---- B ----------------------------------------------------------------------
  //! feed with no inter-frame idle at all
  static void feed_tight(H& x, const std::vector<uint8_t>& f) {
    for (size_t i = 0; i < f.size(); i++) {
      x.d->rx_valid_i = 1;
      x.d->rx_data_i = f[i];
      x.d->rx_last_i = (i + 1 == f.size()) ? 1 : 0;
      x.step();
    }
    x.d->rx_valid_i = 0;
    x.d->rx_last_i = 0;
  }
  static std::vector<uint8_t> getrx(uint16_t seq) {
    return acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, seq, 0, 0);
  }
  static bool is_getrx(const std::vector<uint8_t>& f, uint16_t seq) {
    return f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == seq;
  }
  static int count_aecp(const H& x, uint16_t seq) {
    int n = 0;
    for (const auto& r : x.q_aecp) n += (r.size() >= 38 && fv_u64(r, 34, 2) == seq) ? 1 : 0;
    return n;
  }
  long latency(H& x, uint16_t seq) {
    x.q_acmp.clear();
    x.feed(getrx(seq));
    const long t0 = long(x.t);
    const auto g = x.wait_frame(x.q_acmp, 50, [seq](const std::vector<uint8_t>& f) {
      return is_getrx(f, seq);
    });
    return g.empty() ? -1 : long(x.t) - t0;
  }
  void closed_boot(D3OwnershipPhase& o) {
    std::vector<uint8_t> bad = image;
    bad[0] ^= 0xFF;
    o.power_up(bad, false);
    o.boot_for(12000);
  }
  void b1() {
    D3OwnershipPhase o{h, image};
    closed_boot(o);
    const long idle = latency(o.x, 0xB100);
    o.x.q_acmp.clear();
    feed_tight(o.x, getrx(0xB102));
    const long ti0 = long(o.x.t);
    const auto gi = o.x.wait_frame(o.x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
      return is_getrx(f, 0xB102);
    });
    const long idle_tight = gi.empty() ? -1 : long(o.x.t) - ti0;
    for (int k = 0; k < 6; ++k) feed_tight(o.x, d3_read_entity_cmd(uint16_t(0xB110 + k)));
    o.x.q_acmp.clear();
    feed_tight(o.x, getrx(0xB101));
    const long t0 = long(o.x.t);
    const auto g = o.x.wait_frame(o.x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
      return is_getrx(f, 0xB101);
    });
    const long lat = g.empty() ? -1 : long(o.x.t) - t0;
    printf("PROBE B1 CLOSED: closed %u; idle GET latency %ld (fed with idle), %ld "
           "(fed tight); after six tight AECP a tight GET answered in %ld; word 37 = "
           "%u; head %u\n",
           unsigned(o.x.d->dbg_d3_closed_o), idle, idle_tight, lat, o.x.snap(37),
           unsigned(o.x.d->dbg_aecp_head_o));
  }
  void b2() {
    D3OwnershipPhase o{h, image};
    closed_boot(o);
    o.x.q_acmp.clear();
    for (int k = 0; k < 8; ++k) {
      feed_tight(o.x, d3_read_entity_cmd(uint16_t(0xB210 + k)));
      feed_tight(o.x, getrx(uint16_t(0xB200 + k)));
    }
    o.x.run_ms(50);
    int ans = 0;
    for (int k = 0; k < 8; ++k) {
      bool got = false;
      for (const auto& f : o.x.q_acmp) got = got || is_getrx(f, uint16_t(0xB200 + k));
      ans += got ? 1 : 0;
    }
    printf("PROBE B2 CLOSED: eight tight (AECP, GET_RX_STATE) pairs: %d of 8 GET "
           "answered; word 37 = %u; rx slot drops (snapshot) see receipt\n",
           ans, o.x.snap(37));
  }
  void b3() {
    D3OwnershipPhase o{h, image};
    o.power_up(image, false);
    o.x.d->restore_go_i = 1;
    for (long c = 0; c < 20000 && !o.x.d->dbg_lsn_released_o; ++c) {
      if (c == 5) o.x.d->restore_go_i = 0;
      o.x.step();
    }
    o.x.d->restore_go_i = 0;
    o.x.nv_gnt_hold = 15000;
    for (int k = 0; k < 6; ++k) feed_tight(o.x, d3_read_entity_cmd(uint16_t(0xB310 + k)));
    o.x.q_acmp.clear();
    feed_tight(o.x, getrx(0xB301));
    const long t0 = long(o.x.t);
    const auto g = o.x.wait_frame(o.x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
      return is_getrx(f, 0xB301);
    });
    const long lat = g.empty() ? -1 : long(o.x.t) - t0;
    const bool walking = !o.x.d->dbg_d3_done_o;
    for (long c = 0; c < 40000 && !o.x.d->dbg_d3_done_o; ++c) o.x.step();
    o.x.idle(3000);
    int held = count_aecp(o.x, 0xB310), dropped = 0;
    for (int k = 1; k < 6; ++k) dropped += count_aecp(o.x, uint16_t(0xB310 + k));
    const uint32_t w37 = o.x.snap(37);
    o.x.q_aecp.clear();
    feed_tight(o.x, d3_read_entity_cmd(0xB3F0));
    feed_tight(o.x, d3_read_entity_cmd(0xB3F1));
    o.x.run_ms(50);
    printf("PROBE B3 slowed restore: GET behind six tight AECP answered in %ld (walking "
           "%d); at the terminal held answered %d, dropped answered %d, word 37 = %u; "
           "after the terminal two tight AECP answered %d+%d, word 37 = %u\n",
           lat, walking ? 1 : 0, held, dropped, w37, count_aecp(o.x, 0xB3F0),
           count_aecp(o.x, 0xB3F1), o.x.snap(37));
  }
  void run() { a0(); a1(); a2(); a3(); a4(); b1(); b2(); b3(); }
};

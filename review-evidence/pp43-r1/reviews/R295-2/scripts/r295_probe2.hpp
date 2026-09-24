// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe, round 2 (disposable). Compiled into a scratch copy of
// tb/pp_top only, beside the unchanged round-1 probe.
// R4: a changed FailureInformation under a registered Talker Failed must not
//     make the processor declare the Listener attribute again, with ANY event
//     (New, JoinIn, In, JoinMt, Mt, Lv), compared with an unchanged refresh,
//     in the first 250 ms and over 1500 ms; it must push exactly one
//     unsolicited GET_STREAM_INFO carrying the new code and full bridge, and
//     move nothing on the ACMP wire.
// R6: the stated residual - an Advertise refresh that changes only the
//     accumulated latency. Observed (count of unsolicited responses), graded
//     only as "no more than one".
// R7: a settled, started sink re-bound to another talker with STREAMING_WAIT:
//     pbsta COMPLETED->ACTIVE and started 1->0 land in the same record write;
//     exactly one unsolicited response, carrying ACTIVE/0.
struct R295Probe2 {
  H& h;
  const milan::tb::Model<Vpp_top_wrap> model;
  H io;
  uint16_t sequence = 0x5300;
  explicit R295Probe2(H& tally) : h(tally), io(model.get()) {}

  static uint64_t sid(unsigned s) { return 0x123456789ABC0100ull + s; }
  static uint64_t da(unsigned s) { return 0x91E0F0000100ull + s; }

  void boot() {
    for (auto& region : io.nv_mem) std::fill(region.begin(), region.end(), 0xFF);
    io.nv_st = H::NvState::NV_IDLE;
    io.nv_done_lag = 0;
    io.reset();
    io.d->restore_go_i = 1;
    io.idle(5);
    io.d->restore_go_i = 0;
    unsigned budget = 400000;
    while (!io.d->restore_done_o && budget-- != 0) io.step();
    io.d->link_up_i = 1;
    io.d->entity_enable_i = 1;
    io.run_ms(30);
    io.q_aecp.clear();
    io.q_acmp.clear();
  }
  void register_controller() {
    const auto seq = sequence++;
    io.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, seq,
                      0x0024, std::vector<uint8_t>(4, 0)));
    (void)io.wait_any(io.q_aecp, 500);
    io.q_aecp.clear();
  }
  bool bind(unsigned sink, uint64_t talker, uint16_t flags) {
    const auto seq = sequence++;
    io.feed(acmp_frame(CTLR_MAC, 6, 0, 0, CTLR_EID, talker, EID, T1_UID,
                      sink, 0, 0, seq, flags, 0));
    auto f = io.wait_frame(io.q_acmp, 500, [seq](const std::vector<uint8_t>& r) {
      return r.size() == 70 && fv_u64(r, 62, 2) == seq && (r[15] & 15) == 7;
    });
    return !f.empty() && ((f[16] >> 3) & 31) == 0;
  }
  // unsolicited GET_STREAM_INFO frames for STREAM_INPUT `sink` seen in `ms`;
  // other AECP frames are dropped, ACMP frames counted into *acmp
  int count_uns(unsigned sink, int ms, std::vector<uint8_t>* last = nullptr,
                int* acmp = nullptr) {
    int n = 0;
    for (int t = 0; t < ms; ++t) {
      io.run_ms(1);
      while (!io.q_aecp.empty()) {
        auto f = io.q_aecp.front();
        io.q_aecp.pop_front();
        if (f.size() == 94 && (f[36] & 0x80) && fv_u64(f, 38, 2) == 0x0005
            && fv_u64(f, 40, 2) == sink) {
          ++n;
          if (last) *last = f;
        }
      }
      if (acmp) *acmp += int(io.q_acmp.size());
      io.q_acmp.clear();
    }
    return n;
  }
  std::vector<uint8_t> probe(unsigned sink, int wait_ms = 1600) {
    return io.wait_frame(io.q_acmp, wait_ms, [sink](const std::vector<uint8_t>& r) {
      return r.size() == 70 && (r[15] & 15) == 0 && fv_u64(r, 52, 2) == sink;
    });
  }
  bool settle(unsigned sink, uint64_t talker) {
    io.feed(adp_frame(0, T1_MAC + sink, talker, 31, 0, GM0, DOM0,
                      0xBBB0000000000001ull + sink, 8, TKCAP, 0, 0,
                      0x0000C588u, 0, 0));
    auto p = probe(sink);
    io.run_ms(5);
    if (p.size() != 70) return false;
    io.feed(acmp_frame(T1_MAC + sink, 1, 0, sid(sink), CTLR_EID, talker, EID,
                      T1_UID, sink, da(sink), 0, fv_u64(p, 62, 2), 0, 2));
    io.run_ms(50);
    return true;
  }
  void attribute(unsigned sink, uint8_t code, uint64_t bridge, bool failed,
                 uint32_t lat = 0x12345) {
    auto fv = fv_talker(sid(sink), da(sink), 2, 256, 1, 3, 1, lat);
    if (failed) {
      const auto n = fv.size();
      fv.resize(n + 9);
      putbe(&fv[n], bridge, 8);
      fv[n + 8] = code;
    }
    io.feed(mrpdu_frame(true, T1_MAC + sink,
        {Msg{failed ? 2 : 1, failed ? 34 : 25, false,
             {Vec{false, 1, fv, {EV_JOININ}, {}}}}}));
  }
  // Listener-attribute vectors for sid(sink) the processor sends, by event,
  // over `ms`; also the count in the first `early` ms
  struct Decl { int any = 0, early = 0, by_ev[6] = {0, 0, 0, 0, 0, 0}; };
  Decl listener_decl(unsigned sink, int ms, int early) {
    Decl d;
    for (int t = 0; t < ms; ++t) {
      io.run_ms(1);
      while (!io.q_msrp.empty()) {
        auto f = io.q_msrp.front();
        io.q_msrp.pop_front();
        for (int ev = 0; ev < 6; ++ev) {
          if (frame_has(f, true, 3, sid(sink), ev)) {
            ++d.any;
            ++d.by_ev[ev];
            if (t < early) ++d.early;
          }
        }
      }
    }
    return d;
  }
  static void print_decl(const char* tag, const Decl& d) {
    printf("R295-OBS %s listener_decl any=%d first250ms=%d New=%d JoinIn=%d In=%d JoinMt=%d Mt=%d Lv=%d\n",
           tag, d.any, d.early, d.by_ev[0], d.by_ev[1], d.by_ev[2], d.by_ev[3],
           d.by_ev[4], d.by_ev[5]);
  }

  void run() {
    std::vector<ImgEnt> entries{
        {CFGIX, 0x0000, 1, 312, 0, 312, 0},
        {CFGIX, 0x0005, 2, 140, 1, 144, 0}};
    io.dram = build_image(entries,
        {entity_descriptor(), stream_descriptor(0x0005, 0),
         stream_descriptor(0x0005, 1)}, {"Entity", "Input 0", "Input 1"}, 1);
    boot();
    register_controller();

    // ---- R4 -----------------------------------------------------------
    CHECK(bind(1, T1_EID + 1, 0), "R295 R4: bind sink 1");
    CHECK(settle(1, T1_EID + 1), "R295 R4: sink 1 probed and settled");
    io.q_msrp.clear();
    attribute(1, 7, 0xB17D23456789ABCDull, true);
    auto d_first = listener_decl(1, 1500, 250);
    io.q_aecp.clear();
    attribute(1, 7, 0xB17D23456789ABCDull, true);
    std::vector<uint8_t> f_same;
    int acmp_same = 0;
    auto d_same = listener_decl(1, 1500, 250);
    const int n_same = count_uns(1, 5, &f_same, &acmp_same);
    attribute(1, 9, 0x117D23456789ABCDull, true);
    std::vector<uint8_t> f_chg;
    int acmp_chg = 0;
    const int n_chg_early = count_uns(1, 20, &f_chg, &acmp_chg);
    auto d_chg = listener_decl(1, 1480, 230);
    const int n_chg = n_chg_early + count_uns(1, 5, &f_chg, &acmp_chg);
    print_decl("R4 first-failed", d_first);
    print_decl("R4 unchanged-refresh", d_same);
    print_decl("R4 changed-refresh", d_chg);
    printf("R295-OBS R4 uns_unchanged=%d uns_changed=%d code=%u bridge=%016llx pb=0x%02x acmp_frames_unchanged=%d acmp_frames_changed=%d\n",
           n_same, n_chg, f_chg.size() == 94 ? f_chg[72] : 999u,
           f_chg.size() == 94 ? (unsigned long long)fv_u64(f_chg, 74, 8) : 0ull,
           f_chg.size() == 94 ? f_chg[90] : 0xFFu, acmp_same, acmp_chg);
    CHECK(d_first.by_ev[0] >= 1, "R295 R4: control - a fresh Failed registration declares New");
    CHECK(d_chg.by_ev[0] == 0, "R295 R4: no Listener New after a changed FailureInformation");
    CHECK(d_chg.early <= d_same.early,
          "R295 R4: no extra early Listener declaration after a changed FailureInformation");
    CHECK(d_chg.any <= d_same.any + 1,
          "R295 R4: Listener declarations after a change match an unchanged refresh (+-1 periodic)");
    CHECK(n_same == 0, "R295 R4: an unchanged refresh pushes nothing");
    CHECK(n_chg == 1 && f_chg.size() == 94 && f_chg[72] == 9
          && fv_u64(f_chg, 74, 8) == 0x117D23456789ABCDull && f_chg[90] == 0x60,
          "R295 R4: exactly one push carrying the new code, full bridge, COMPLETED/0");
    CHECK(acmp_chg == 0, "R295 R4: the change moves nothing on the ACMP wire");

    // ---- R6 (residual, observed) -------------------------------------
    attribute(1, 0, 0, false, 0x12345);
    std::vector<uint8_t> f_adv;
    const int n_adv = count_uns(1, 300, &f_adv);
    attribute(1, 0, 0, false, 0x54321);
    const int n_lat = count_uns(1, 300);
    printf("R295-OBS R6 uns_failed_to_advertise=%d adv_code=%u adv_bridge=%016llx uns_latency_only_refresh=%d\n",
           n_adv, f_adv.size() == 94 ? f_adv[72] : 999u,
           f_adv.size() == 94 ? (unsigned long long)fv_u64(f_adv, 74, 8) : 0ull, n_lat);
    CHECK(n_adv == 1 && f_adv.size() == 94 && f_adv[72] == 0
          && fv_u64(f_adv, 74, 8) == 0,
          "R295 R6: Failed->Advertise pushes once with code and bridge cleared");
    CHECK(n_lat <= 1, "R295 R6: a latency-only refresh pushes at most once");

    // ---- R7 -----------------------------------------------------------
    CHECK(bind(0, T1_EID, 0), "R295 R7: bind sink 0 (started)");
    CHECK(settle(0, T1_EID), "R295 R7: sink 0 settled");
    (void)count_uns(0, 100);
    const unsigned st0 = io.d->aecp_strm_started_o & 1u;
    CHECK(bind(0, T1_EID + 0x66, 0x0008), "R295 R7: re-bind sink 0 to another talker, STREAMING_WAIT");
    std::vector<uint8_t> f7;
    const int n7 = count_uns(0, 60, &f7);
    const unsigned st1 = io.d->aecp_strm_started_o & 1u;
    printf("R295-OBS R7 started_before=%u started_after=%u uns=%d pb=0x%02x flags=%08llx\n",
           st0, st1, n7, f7.size() == 94 ? f7[90] : 0xFFu,
           f7.size() == 94 ? (unsigned long long)fv_u64(f7, 42, 4) : 0ull);
    CHECK(st0 == 1 && st1 == 0, "R295 R7: the re-bind stopped the settled sink");
    CHECK(n7 == 1 && f7.size() == 94 && f7[90] == 0x40,
          "R295 R7: pbsta and started/stopped moving in one write push exactly one ACTIVE/0 frame");
  }
};

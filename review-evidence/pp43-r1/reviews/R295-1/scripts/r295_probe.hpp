// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (disposable). Compiled into a scratch copy of tb/pp_top only.
// R1: a BIND_RX naming a DIFFERENT talker while the sink is ACTIVE/acmpsta 0,
//     with STREAMING_WAIT flipping the started state (Milan Table 5.22
//     started/stopped). Counts unsolicited GET_STREAM_INFO frames for the sink.
// R2: a changed FailureInformation while Talker Failed stays registered.
//     Counts Listener-attribute New events the processor transmits for the
//     stream afterwards, versus an unchanged refresh.
// R3: a refused/aborted gather (integrator stalls selector 0) followed by a
//     good query on another sink: internal fields must not leak across sinks.
struct R295Probe {
  H& h;
  const milan::tb::Model<Vpp_top_wrap> model;
  H io;
  uint16_t sequence = 0x5100;
  explicit R295Probe(H& tally) : h(tally), io(model.get()) {}

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
  // unsolicited GET_STREAM_INFO frames for STREAM_INPUT `sink` seen in `ms`
  int count_uns(unsigned sink, int ms, uint8_t* last_pb = nullptr) {
    int n = 0;
    for (int t = 0; t < ms; ++t) {
      io.run_ms(1);
      while (!io.q_aecp.empty()) {
        auto f = io.q_aecp.front();
        io.q_aecp.pop_front();
        if (f.size() == 94 && (f[36] & 0x80) && fv_u64(f, 38, 2) == 0x0005
            && fv_u64(f, 40, 2) == sink) {
          ++n;
          if (last_pb) *last_pb = f[90];
        }
      }
    }
    return n;
  }
  std::vector<uint8_t> query(unsigned sink) {
    std::vector<uint8_t> body(4, 0);
    putbe(&body[0], 0x0005, 2);
    putbe(&body[2], sink, 2);
    const auto seq = sequence++;
    io.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, seq, 0x000F, body));
    auto f = io.wait_frame(io.q_aecp, 1500, [seq](const std::vector<uint8_t>& r) {
      return r.size() >= 38 && !(r[36] & 0x80) && fv_u64(r, 34, 2) == seq;
    });
    return f;
  }
  std::vector<uint8_t> probe(unsigned sink, int wait_ms = 1600) {
    return io.wait_frame(io.q_acmp, wait_ms, [sink](const std::vector<uint8_t>& r) {
      return r.size() == 70 && (r[15] & 15) == 0 && fv_u64(r, 52, 2) == sink;
    });
  }
  void attribute(unsigned sink, uint8_t code, uint64_t bridge, bool failed) {
    auto fv = fv_talker(sid(sink), da(sink), 2, 256, 1, 3, 1, 0x12345);
    if (failed) {
      const auto n = fv.size();
      fv.resize(n + 9);
      putbe(&fv[n], bridge, 8);
      fv[n + 8] = code;
    }
    io.feed(mrpdu_frame(true, T1_MAC + sink,
        {Msg{failed ? 2 : 1, failed ? 34 : 25, false,
             {Vec{false, 1, fv, {EV_NEW}, {}}}}}));
  }
  int listener_new(unsigned sink, int ms) {
    int n = 0;
    for (int t = 0; t < ms; ++t) {
      io.run_ms(1);
      while (!io.q_msrp.empty()) {
        auto f = io.q_msrp.front();
        io.q_msrp.pop_front();
        if (frame_has(f, true, 3, sid(sink), EV_NEW)) ++n;
      }
    }
    return n;
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

    // ---- R1 -----------------------------------------------------------
    CHECK(bind(0, T1_EID, 0), "R295 R1: first bind accepted");
    const int n_bind = count_uns(0, 60);
    const unsigned started0 = io.d->aecp_strm_started_o & 1u;
    // still inside T-ACMP-CMD (200 ms): the sink is ACTIVE, acmpsta 0
    CHECK(bind(0, T1_EID + 0x55, 0x0008), "R295 R1: rebind to a different talker accepted");
    uint8_t pb = 0xFF;
    const int n_rebind = count_uns(0, 60, &pb);
    const unsigned started1 = io.d->aecp_strm_started_o & 1u;
    printf("R295-OBS R1 bind_notifications=%d started_before=%u rebind_notifications=%d started_after=%u\n",
           n_bind, started0, n_rebind, started1);
    CHECK(started0 == 1 && started1 == 0,
          "R295 R1: rebind flipped the published started state (STREAMING_WAIT)");
    CHECK(n_rebind >= 1,
          "R295 R1: rebind that changes started/stopped raises a GET_STREAM_INFO notification");
    // without STREAMING_WAIT change: rebind back to the first talker, SW set
    CHECK(bind(0, T1_EID, 0x0008), "R295 R1b: rebind again (SW unchanged)");
    const int n_rebind2 = count_uns(0, 60);
    printf("R295-OBS R1b rebind_same_sw_notifications=%d\n", n_rebind2);
    // unbind to leave sink 0 quiet
    {
      const auto seq = sequence++;
      io.feed(acmp_frame(CTLR_MAC, 8, 0, 0, CTLR_EID, T1_EID, EID, T1_UID,
                        0, 0, 0, seq, 0, 0));
      (void)io.wait_frame(io.q_acmp, 500, [seq](const std::vector<uint8_t>& r) {
        return r.size() == 70 && fv_u64(r, 62, 2) == seq; });
      io.run_ms(50);
      io.q_aecp.clear();
    }

    // ---- R2 -----------------------------------------------------------
    CHECK(bind(1, T1_EID + 1, 0), "R295 R2: bind sink 1");
    io.feed(adp_frame(0, T1_MAC + 1, T1_EID + 1, 31, 0, GM0, DOM0,
                      0xBBB0000000000001ull, 8, TKCAP, 0, 0, 0x0000C588u, 0, 0));
    auto p = probe(1);
    // a probe may be the one from bind; take the latest one for the seq
    io.run_ms(5);
    if (p.size() == 70) {
      io.feed(acmp_frame(T1_MAC + 1, 1, 0, sid(1), CTLR_EID, T1_EID + 1, EID,
                        T1_UID, 1, da(1), 0, fv_u64(p, 62, 2), 0, 2));
    }
    io.run_ms(50);
    attribute(1, 7, 0xB17D23456789ABCDull, true);
    const int n_first = listener_new(1, 1500);
    attribute(1, 7, 0xB17D23456789ABCDull, true);
    const int n_same = listener_new(1, 1500);
    attribute(1, 9, 0x117D23456789ABCDull, true);
    const int n_changed = listener_new(1, 1500);
    auto q = query(1);
    printf("R295-OBS R2 settle_probe=%zu first_failed_new=%d unchanged_refresh_new=%d changed_refresh_new=%d q_code=%u q_pb=0x%02x\n",
           p.size(), n_first, n_same, n_changed,
           q.size() == 94 ? q[72] : 999u, q.size() == 94 ? q[90] : 0xFFu);
    CHECK(n_changed == 0,
          "R295 R2: a changed FailureInformation does not re-declare the Listener with New");

    // ---- R3 -----------------------------------------------------------
    // sink 1 now holds code 9 + bridge; stall sink 0's selector 0 until the
    // gather watchdog voids that response, then read sink 0 again cleanly.
    io.q_aecp.clear();
    auto q1 = query(1);
    io.gsi_stuck = true;
    auto qs = query(0);
    io.gsi_stuck = false;
    auto q0 = query(0);
    printf("R295-OBS R3 q1=%zu stuck_resp=%zu stuck_status=%u q0=%zu q0_code=%u q0_bridge=%016llx\n",
           q1.size(), qs.size(), qs.size() > 16 ? unsigned(qs[16] >> 3) : 999u,
           q0.size(), q0.size() == 94 ? q0[72] : 999u,
           q0.size() == 94 ? (unsigned long long)fv_u64(q0, 74, 8) : 0ull);
    bool leak = false;
    if (qs.size() == 94) leak = leak || qs[72] != 0 || fv_u64(qs, 74, 8) != 0;
    if (q0.size() == 94) leak = leak || q0[72] != 0 || fv_u64(q0, 74, 8) != 0;
    CHECK(!leak, "R295 R3: no cross-sink failure data after a voided gather");
  }
};

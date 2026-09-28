  // ===================== reviewer probes (R375-1), disposable =====================
  // Inserted into a scratch copy of tb/srp_top/sim_main.cpp by r375_run.py.
  // Observes only wrapper debug outputs and the wire; no DUT state is forced.
  static long first_after(const std::vector<uint64_t>& v, long after) {
    for (auto c : v) if (long(c) > after) return long(c);
    return -1;
  }
  long first_la_fin(long after) {
    for (size_t i = 0; i < h.archive.size() && i < h.fin_cycles.size(); i++) {
      if (long(h.fin_cycles[i]) <= after) continue;
      auto p = parse_frame(h.archive[i]);
      bool la = false;
      for (const auto& v : p.vecs) la |= v.la;
      if (p.ok && p.msrp && la) return long(h.fin_cycles[i]);
    }
    return -1;
  }
  // feed one body byte-per-accepted-cycle starting now; returns start cycle
  void feed_raw(const std::vector<uint8_t>& bytes, bool msrp, int extra) {
    size_t i = 0;
    while (i < bytes.size()) {
      d->mrp_valid_i = 1; d->mrp_data_i = bytes[i];
      d->mrp_last_i = i + 1 == bytes.size(); d->mrp_msrp_i = msrp;
      if (h.step()) i++;
    }
    d->mrp_valid_i = 0; d->mrp_last_i = 0;
    h.idle(extra);
  }

  // R1/R2: Listener Lv anchored on the OBSERVED expiry strobe and on the first
  // join opportunity after it; residual window from that opportunity to the
  // first LeaveAll-flagged MSRP frame on the wire.
  void r375_early_window() {
    for (int fp : {DECL_READY, DECL_READYFAIL}) for (int target : {0, 7}) {
      uint32_t deadline = leaveall_setup(fp);
      until_ms(deadline - 2); long m = long(h.t);
      h.run_ms(300);
      long E = first_after(h.expiry_cycles, m);
      long J = first_after(h.join_cycles, E);
      long A = first_after(h.la_cycles, m);
      long W = first_la_fin(J);
      printf("R375_CAL fp=%d target=%d expiry=%ld join=%ld action=%ld wire_done=%ld "
             "(cycles from mark; 40 cycles = 1 tb ms)\n", fp, target, E - m, J - m,
             A < 0 ? -1 : A - m, W < 0 ? -1 : W - m);
      CHECK(E > 0 && J > E, "R1a: calibration observes expiry and the following join opportunity");
      CHECK(A == J, "R1b: own registrar action coincides with the first join opportunity after expiry");
      CHECK(W > J, "R2a: own LeaveAll reaches the wire after the action");
      printf("R375_RESIDUAL fp=%d action_to_wire_done_cycles=%ld\n", fp, W - J);
      // decode latency of the Listener Lv (throwaway run)
      deadline = leaveall_setup(fp); until_ms(deadline - 2); long m2 = long(h.t);
      h.idle(int(E - m) + 60); long s0 = long(h.t);
      listener_event(target, EV_LV, fp);
      long L = first_after(h.rx_cycles, s0 - 1) - s0;
      CHECK(L > 0, "R1c: Lv decode latency measured");
      (void)m2;
      long rel_e = E - m, rel_j = J - m;
      for (long want : {rel_e + 1, rel_e + 40, (rel_e + rel_j) / 2, rel_j - 2, rel_j, rel_j + 2}) {
        deadline = leaveall_setup(fp); until_ms(deadline - 2); long mm = long(h.t);
        long wait = want - L;
        if (wait > 0) h.idle(int(wait));
        long st = long(h.t);
        listener_event(target, EV_LV, fp);
        long r = first_after(h.rx_cycles, st - 1);
        long e = first_after(h.expiry_cycles, mm);
        // run on to see the join opportunity (it may be after r)
        bool held = true;
        long j = -1;
        bool pre = false, decided = false;
        for (int i = 0; i < 2000 * MS_CYC; i++) {
          h.cycle();
          if (!decided) {
            j = first_after(h.join_cycles, e);
            if (j >= 0) { pre = r <= j; decided = true; }
          }
          if (decided) held &= h.active(target) == !pre;
        }
        CHECK(decided && e >= 0 && r > e, "R1d: Lv decoded after the observed expiry");
        CHECK(held && source_reg(target) == (pre ? 0 : 2),
              "R1e: Lv at expiry%+ld/opportunity%+ld cycles follows IN/LV policy (pre=%d)",
              r - e, r - j, int(pre));
        printf("R375_WINDOW fp=%d target=%d rx_minus_expiry=%ld rx_minus_opportunity=%ld "
               "expect_stop=%d active_after_hold=%d reg=%d\n", fp, target, r - e, r - j,
               int(pre), int(h.active(target)), source_reg(target));
      }
    }
  }

  // R3: MVRP responsiveness while an empty canceled MSRP reservation is parked.
  void r375_parked_mvrp() {
    long lat[2] = {-1, -1};
    for (int cancel = 0; cancel <= 1; cancel++) {
      h.reset(); d->link_up_i = 1; h.idle(10);
      h.op(OP_DECL_TK, 0, own_sid(0), 0x91e0f0010100ULL, 2, 29, 1);
      h.run_ms(700);
      uint32_t deadline = d->dbg_la_deadline_o;
      until_ms(deadline - 20); d->block_alloc_i = 1; until_ms(deadline + 250);
      int waiting = d->dbg_la_wait_o;
      if (cancel) h.feed(mrpdu_body(true, {la_only(3, 8, true)}), true);
      d->block_alloc_i = 0; h.run_ms(5);
      int st = d->dbg_enc_state_o, cnt = d->dbg_enc_count_o;
      size_t base = h.archive.size();
      uint32_t t0 = d->now_ms_o;
      h.feed(mrpdu_body(false, {la_only(1, 2, false)}), false);
      long got = -1; size_t scanned = base;
      long park_end = -1;
      for (int i = 0; i < 3000 * MS_CYC && got < 0; i++) {
        h.cycle();
        if (park_end < 0 && d->dbg_enc_state_o != 16) park_end = d->now_ms_o;
        for (; scanned < h.archive.size(); scanned++) {
          auto p = parse_frame(h.archive[scanned]);
          if (p.ok && !p.msrp) { got = long(d->now_ms_o) - long(t0); break; }
        }
      }
      lat[cancel] = got;
      printf("R375_MVRP cancel=%d waiting=%d enc_state_after_release=%d msrp_pending=%d "
             "park_ends_ms=%ld mvrp_response_ms=%ld\n", cancel, waiting, st, cnt,
             park_end < 0 ? -1 : park_end - long(t0), got);
      CHECK(waiting == 1, "R3a: own preparation was waiting on allocation");
    }
    CHECK(lat[0] >= 0 && lat[0] <= 250, "R3b: control MVRP response within one join period");
    CHECK(lat[1] >= 0 && lat[1] <= 250,
          "R3c: MVRP response with an empty canceled MSRP reservation parked (%ld ms)", lat[1]);
  }

  // R4: peer LeaveAll decoded around the join opportunity that would start
  // preparation (the join-start guard), and the cycles just after.
  void r375_peer_at_join_start() {
    auto peer = mrpdu_body(true, {la_only(4, 4, false)});
    uint32_t deadline = leaveall_setup(DECL_READY);
    until_ms(deadline - 2); long m = long(h.t);
    h.run_ms(300);
    long E = first_after(h.expiry_cycles, m) - m;
    long Wt = first_after(h.wait_cycles, m) - m;   // first cycle la_wait is visible
    long P = first_after(h.prep_cycles, m) - m;
    CHECK(E > 0 && Wt > E && P >= Wt, "R4a: calibration sees expiry, wait and acceptance");
    long due = Wt - 1;                               // cycle of the join opportunity
    deadline = leaveall_setup(DECL_READY); until_ms(deadline - 2);
    long s0 = long(h.t) + 200; h.idle(200);
    feed_raw(peer, true, 8);
    long Lp = first_after(h.peer_la_cycles, s0 - 1) - s0;
    CHECK(Lp > 0, "R4b: peer decode latency measured");
    unsigned seen = 0;
    for (long delta = -2; delta <= 3; delta++) {
      deadline = leaveall_setup(DECL_READY); until_ms(deadline - 2); long mm = long(h.t);
      h.idle(int(due + delta - Lp));
      size_t base = h.archive.size();
      feed_raw(peer, true, 8);
      h.run_ms(700);
      long p = first_after(h.peer_la_cycles, mm) - mm;
      long e = first_after(h.expiry_cycles, mm) - mm;
      long acc = first_after(h.prep_cycles, mm);
      bool own = acc >= 0 && (acc - mm) < p;
      long d_obs = p - due;
      if (e == E && d_obs >= -1 && d_obs <= 1) seen |= 1u << (d_obs + 1);
      CHECK(e == E, "R4c: deterministic expiry phase");
      CHECK(h.la_cycles.size() == size_t(own) && leaveall_frames(h, base) == int(own),
            "R4d: peer at join-start delta=%ld supersedes unless acceptance preceded it", d_obs);
      CHECK(source_reg(0) == (own ? 2 : 1) && sink_reg(7) == (own ? 2 : 1),
            "R4e: registrar planes agree with the action outcome delta=%ld", d_obs);
      printf("R375_JOINSTART peer_minus_opportunity=%ld accepted_before_peer=%d actions=%zu\n",
             d_obs, int(own), h.la_cycles.size());
    }
    CHECK(seen == 7, "R4f: sweep covers -1, 0, +1 around the join opportunity");
  }

  // R5: sink plane (listener FSM registrar) at the exact acceptance edge.
  void r375_sink_edge() {
    for (int fp : {DECL_READY, DECL_READYFAIL}) {
      unsigned seen = 0;
      for (int release = 4; release <= 60; release++) {
        uint32_t deadline = leaveall_setup(fp);
        until_ms(deadline - 20); d->block_alloc_i = 1; until_ms(deadline + 250);
        h.rx_cycles.clear(); h.la_cycles.clear();
        auto bytes = mrpdu_body(true, {Msg{1, 25, false,
          {Vec{false, 1, fv_talker(peer_sid(0), peer_da(0), 2, 29, 1, 3, 1, 500), {EV_LV}, {}}}}});
        size_t i = 0;
        for (int clk = 0; clk < 120; clk++) {
          if (clk == release) d->block_alloc_i = 0;
          d->mrp_valid_i = i < bytes.size(); d->mrp_data_i = i < bytes.size() ? bytes[i] : 0;
          d->mrp_last_i = i + 1 == bytes.size(); d->mrp_msrp_i = 1;
          if (h.step() && i < bytes.size()) i++;
        }
        d->mrp_valid_i = 0; d->mrp_last_i = 0;
        if (h.la_cycles.size() != 1 || h.rx_cycles.size() != 1) {
          CHECK(false, "R5a: one sLA and one decoded talker Lv (release=%d)", release);
          continue;
        }
        long delta = long(h.rx_cycles[0]) - long(h.la_cycles[0]);
        if (delta < -1 || delta > 1) continue;
        seen |= 1u << (delta + 1);
        bool retain = delta > 0;
        h.run_ms(50);
        CHECK(sink_reg(0) == (retain ? 2 : 0) && h.tk_reg(0) == (retain ? 1 : 0),
              "R5b: sink-plane Lv at acceptance delta=%ld fp=%d", delta, fp);
        printf("R375_SINKEDGE fp=%d release=%d rx_minus_sLA=%ld sink_reg=%d\n",
               fp, release, delta, sink_reg(0));
      }
      CHECK(seen == 7, "R5c: sink sweep covers -1, 0, +1");
    }
  }

  // R6: peer LeaveAll while preparation waits behind a busy encoder (TX held).
  void r375_cancel_while_encoder_busy() {
    h.reset(); d->link_up_i = 1; h.run_ms(700);
    uint32_t deadline = d->dbg_la_deadline_o;
    until_ms(deadline - 300); h.pause_tx = true;
    until_ms(deadline + 250);
    int waiting = d->dbg_la_wait_o, st = d->dbg_enc_state_o;
    printf("R375_BUSY waiting=%d enc_state=%d\n", waiting, st);
    CHECK(waiting == 1 && st == 15, "R6a: preparation waits while encoder holds a TX request");
    size_t base = h.archive.size();
    h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);
    h.pause_tx = false; h.run_ms(800);
    CHECK(h.la_cycles.empty() && leaveall_frames(h, base) == 0 && !d->dbg_la_wait_o,
          "R6b: peer cancels a preparation not yet started in the encoder");
  }

  // R7: a new own expiry while a canceled preparation is still blocked.
  void r375_new_intent_during_canceled_prep() {
    h.reset(); d->link_up_i = 1; h.run_ms(700);
    uint32_t deadline = d->dbg_la_deadline_o;
    until_ms(deadline - 20); d->block_alloc_i = 1; until_ms(deadline + 250);
    h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);
    uint32_t next = d->dbg_la_deadline_o;
    CHECK(next > deadline + 1000, "R7a: next own deadline drawn");
    until_ms(next + 50);
    CHECK(d->dbg_la_pending_o && d->dbg_la_wait_o && h.la_cycles.empty(),
          "R7b: new intent pending while canceled preparation still blocked");
    size_t base = h.archive.size();
    d->block_alloc_i = 0; h.run_ms(800);
    CHECK(h.la_cycles.size() == 1 && leaveall_frames(h, base) == 1,
          "R7c: newer intent survives the canceled acceptance and is sent once");
    printf("R375_NEWINTENT actions=%zu flagged=%d\n", h.la_cycles.size(), leaveall_frames(h, base));
  }

  void r375_all(bool base_rtl) {
    r375_early_window();
    if (base_rtl) return;
    r375_parked_mvrp();
    r375_peer_at_join_start();
    r375_sink_edge();
    r375_cancel_while_encoder_busy();
    r375_new_intent_during_canceled_prep();
  }
  // =================== end reviewer probes ===================

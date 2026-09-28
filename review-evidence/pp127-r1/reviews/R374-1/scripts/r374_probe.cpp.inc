  // ---- R374 reviewer probes (independent of the author's K/L/M/N groups) ----
  // R1: parent-scenario reconstruction. Listener Leave for source 0 at
  //     deadline+off; does the licence stay down for the 2 s hold?
  // R2: canceled empty reservation; MVRP re-join delay after an MVRP rLA.
  // R3: cancel, then a newer timer expiry while allocation is still blocked.
  // R4: peer MSRP LeaveAll on the same clock as the join cadence tick.
  void r374_probe(const char* which) {
    if (!strcmp(which, "r374r1")) {
      for (int off = -3; off <= 200; off += (off < 5 || off > 75 ? 1 : 5)) {
        uint32_t dl = leaveall_setup(DECL_READY);
        until_ms(dl + off);
        size_t acts = h.la_cycles.size();
        uint32_t la_t = acts ? h.la_times[0] : 0;
        int regb = source_reg(0);
        listener_event(0, EV_LV, DECL_READY);
        int rega = source_reg(0);
        bool stopped = true;
        for (int i = 0; i < 2000 * MS_CYC; i++) { h.cycle(); if (h.active(0)) stopped = false; }
        printf("R374_R1 off=%d deadline=%u reg_before=%d reg_after=%d actions_before=%zu first_action_ms=%u stopped_2s=%d\n",
               off, dl, regb, rega, acts, la_t, stopped);
      }
    }
    if (!strcmp(which, "r374r2")) {
      // scenario 0: listener sink 0 declared (VID held), peer Talker Failed-only LA
      // scenario 1: nothing declared but the Domain, peer Listener-only LA
      for (int sc = 0; sc <= 1; sc++) for (int canceled = 0; canceled <= 1; canceled++) {
        h.reset(); d->link_up_i = 1; h.idle(10);
        if (sc == 0) { h.op(OP_DECL_LS, 0, peer_sid(0), peer_da(0), 2, 0, 0, DECL_READY); talker_event(0, EV_NEW); }
        h.run_ms(700);
        uint32_t dl = d->dbg_la_deadline_o;
        until_ms(dl - 20); d->block_alloc_i = 1; until_ms(dl + 250);
        if (canceled) h.feed(mrpdu_body(true, {sc == 0 ? la_only(2, 34, false) : la_only(3, 8, true)}), true);
        d->block_alloc_i = 0;
        uint32_t rel = d->now_ms_o;
        int guard = 50 * MS_CYC; while (d->dbg_enc_state_o != 16 && guard--) h.cycle();
        uint32_t enter = d->now_ms_o;
        size_t base = h.archive.size();
        h.feed(mrpdu_body(false, {la_only(1, 2, false)}), false);
        uint32_t tl = d->now_ms_o, tj = 0, leave = 0;
        size_t seen = base;
        for (int i = 0; i < 3000 * MS_CYC && !(tj && leave); i++) {
          h.cycle();
          if (!leave && d->dbg_enc_state_o != 16) leave = d->now_ms_o;
          while (seen < h.archive.size()) {
            auto p = parse_frame(h.archive[seen++]);
            if (!p.msrp && p.ok && !tj) tj = d->now_ms_o;
          }
        }
        printf("R374_R2 scenario=%d canceled=%d own_actions=%zu release_ms=%u collect_enter_ms=%u collect_leave_ms=%u collect_dwell_ms=%d mvrp_rLA_ms=%u first_mvrp_frame_ms=%u mvrp_delay_ms=%d\n",
               sc, canceled, h.la_cycles.size(), rel, enter, leave, leave ? int(leave - enter) : -1, tl, tj, tj ? int(tj - tl) : -1);
      }
    }
    if (!strcmp(which, "r374r3")) {
      uint32_t dl = leaveall_setup(DECL_READY);
      until_ms(dl - 20); d->block_alloc_i = 1; until_ms(dl + 250);
      h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);   // peer cancels
      uint32_t second = d->dbg_la_deadline_o;
      until_ms(second + 50);                                     // newer intent
      int pend = d->dbg_la_pending_o;
      d->block_alloc_i = 0; h.run_ms(700);
      printf("R374_R3 first=%u second=%u pending_after_second=%d actions=%zu\n", dl, second, pend, h.la_cycles.size());
      CHECK(pend == 1 && h.la_cycles.size() == 1,
            "R3: a newer expiry after a canceled preparation still yields one own sLA");
    }
    if (!strcmp(which, "r374r4")) {
      // Find the join cadence clock that would start the prepared round,
      // then land the peer LeaveAll lane exactly on it (and +-1).
      for (int delta : {-1, 0, 1}) {
        uint32_t dl = leaveall_setup(DECL_READY);
        until_ms(dl + 1);
        uint64_t mark = h.t; int guard = 400 * MS_CYC;
        while (!d->dbg_la_wait_o && guard--) h.cycle();
        uint64_t wait_clk = h.t;      // la_wait_r visible: the join tick was wait_clk-1
        int dist = int(wait_clk - mark);
        // replay with the peer lane on that join tick
        dl = leaveall_setup(DECL_READY);
        until_ms(dl + 1);
        mark = h.t;
        h.idle(dist - 1 - 7 + delta);
        h.peer_la_cycles.clear();
        size_t base = h.archive.size();
        h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);
        h.run_ms(600);
        long rel = h.peer_la_cycles.empty() ? -999 : long(h.peer_la_cycles[0]) - long(mark + dist - 1);
        printf("R374_R4 delta=%d peer_minus_joinclk=%ld actions=%zu la_frames=%d\n",
               delta, rel, h.la_cycles.size(), leaveall_frames(h, base));
        if (rel >= 0) CHECK(h.la_cycles.size() == 0, "R4: peer on/after the join clock but before sLA supersedes rel=%ld", rel);
      }
    }
    if (!strcmp(which, "r374r5")) {
      // R5: a canceled empty reservation (link down, as in M12) is reused by
      // the next own action; land a peer MSRP LeaveAll on the clocks around
      // that reuse acceptance. Own flags on the wire must match sLA strobes.
      auto setup = [&](uint32_t& later) {
        h.reset(); d->link_up_i = 1; h.run_ms(700);
        uint32_t qd = d->dbg_la_deadline_o;
        until_ms(qd - 20); d->block_alloc_i = 1; d->link_up_i = 0;
        until_ms(qd + 250);
        later = d->dbg_la_deadline_o;
        h.feed(mrpdu_body(true, {la_only(3, 8, true)}), true);
        d->block_alloc_i = 0;
        until_ms(later + 1);
        h.la_cycles.clear();   // the canceled round has no own action
      };
      uint32_t later = 0;
      setup(later);
      uint64_t mark = h.t; int guard = 400 * MS_CYC;
      int st_before = d->dbg_enc_state_o;
      while (!d->dbg_la_wait_o && guard--) h.cycle();
      int dist = int(h.t - mark);
      for (int delta : {-1, 0, 1, 2}) {
        setup(later); mark = h.t;
        h.idle(dist - 1 - 7 + delta);
        h.peer_la_cycles.clear(); h.prep_cycles.clear();
        size_t base = h.archive.size();
        h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);
        h.run_ms(700);
        long rel = h.peer_la_cycles.empty() ? -999 : long(h.peer_la_cycles[0]) - long(mark + dist - 1);
        long prel = h.prep_cycles.empty() ? -999 : long(h.prep_cycles[0]) - long(mark + dist - 1);
        int laf = leaveall_frames(h, base);
        for (auto c : h.la_cycles) printf("R374_R5dbg delta=%d later=%u dist=%d sLA_minus_joinclk=%ld\n", delta, later, dist, long(c) - long(mark + dist - 1));
        for (size_t j = 0; j < h.archive.size(); j++) { auto pf = parse_frame(h.archive[j]); bool la = false; for (auto& v : pf.vecs) la |= v.la; if (pf.msrp && la) printf("R374_R5dbg delta=%d la_frame_index=%zu base=%zu\n", delta, j, base); }
        printf("R374_R5 enc_state_before=%d delta=%d peer_minus_joinclk=%ld prep_minus_joinclk=%ld actions=%zu la_frames=%d\n",
               st_before, delta, rel, prel, h.la_cycles.size(), laf);
        CHECK(int(h.la_cycles.size()) == laf, "R5: own LeaveAll flags on the wire only with an sLA strobe delta=%d", delta);
        if (rel >= 0 && prel >= rel) CHECK(h.la_cycles.empty(), "R5: peer on or before reuse acceptance supersedes delta=%d", delta);
      }
    }
  }


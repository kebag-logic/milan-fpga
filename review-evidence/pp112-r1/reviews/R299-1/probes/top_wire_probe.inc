  // ==== R299-1 reviewer probe 2: can the cross-source licence reach the
  // wire? Same shape as probe 1 (source 0 ~70 Mb/s admitted, source 7
  // ~15.5 Mb/s refused before and after an identical re-declaration of
  // source 0), but the re-declaration is placed k clocks before a T-MRP-JOIN
  // tick (the talker FSM's transmit opportunity), k = 1..40. Every MSRP frame
  // from just before that tick through two further join periods is parsed
  // for a Talker Advertise (type 1) carrying source 7's stream ID.
  void probe_wire() {
    const int lo = 0, hi = 7;
    const unsigned F_LO = 1051, F_HI = 200;
    const uint64_t sid_lo = (OWN_MAC << 16) | 0x500, sid_hi = (OWN_MAC << 16) | 0x507;
    const uint64_t da_lo = DA0 + 0x40, da_hi = DA0 + 0x47;
    unsigned hits = 0, tried = 0;
    for (int k = 1; k <= 40; ++k) {
      h.reset(); d->link_up_i = 1; h.idle(40);
      h.op(OP_DECL_TK, lo, sid_lo, da_lo, 2, F_LO, 1);
      h.op(OP_DECL_TK, hi, sid_hi, da_hi, 2, F_HI, 1);
      h.idle(64);
      h.feed(mrpdu_body(true, {Msg{3, 8, true,
        {Vec{false, 1, fv_sid(sid_lo), {EV_NEW}, {DECL_READY}},
         Vec{false, 1, fv_sid(sid_hi), {EV_NEW}, {DECL_READY}}}}}), true);
      h.run_ms(450);
      CHECK(!(d->sr_admitted_o & 0x80u) && h.tk_decl(hi) == 2,
            "WIRE precondition k=%d: source 7 refused and Failed", k);
      // measure the join period from two ticks, then land k clocks early
      auto next_tick = [&]() {
        long n = 0;
        while (d->dbg_join_o) { h.cycle(); ++n; }
        while (!d->dbg_join_o) { h.cycle(); ++n; }
        return n;
      };
      next_tick();
      long period = next_tick();
      h.idle(int(period) - k - 3);  // the op() below accepts ~3 clocks after its call
      size_t wire0 = h.archive.size();
      h.samples.clear(); h.recording = true;
      h.op(OP_DECL_TK, lo, sid_lo, da_lo, 2, F_LO, 1);
      h.idle(96); h.recording = false;
      unsigned grant = 0, adv = 0;
      for (const auto& x : h.samples) {
        grant += (x.grants >> hi) & 1u;
        adv += ((x.tk_decl >> (2 * hi)) & 3u) == 1u;
      }
      h.run_ms(450);
      unsigned wire_adv = 0;
      for (size_t i = wire0; i < h.archive.size(); ++i) {
        auto p = parse_frame(h.archive[i]);
        if (!p.msrp) continue;
        for (auto& v : p.vecs)
          if (v.type == 1 && fv_u64(v.fv, 0, 8) == sid_hi) ++wire_adv;
      }
      ++tried; hits += wire_adv != 0;
      printf("WIRE k=%d join_period=%ld src7_grant_cycles=%u src7_declared_advertise_cycles=%u "
             "src7_wire_talker_advertise_vectors=%u\n", k, period, grant, adv, wire_adv);
      CHECK(wire_adv == 0, "WIRE refused source 7 never sends Talker Advertise (k=%d)", k);
    }
    printf("WIRE SUMMARY tried=%u with_wire_talker_advertise=%u\n", tried, hits);
  }

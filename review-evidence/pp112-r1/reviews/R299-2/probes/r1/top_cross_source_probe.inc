  // ==== R299-1 reviewer probe: cross-source licence through the real service
  // port. Source 0 (~70 Mb/s) is admitted; source 7 (~15.5 Mb/s) is refused by
  // the 75 Mb/s ceiling. Both have a real Listener Ready. Source 0 is then
  // re-declared identically (mode 0) or shrunk to ~60.3 Mb/s (mode 1); source 7
  // stays refused before and after under the independent greedy model.
  // Observed every clock: source 7 grant, ACTIVE, ACTIVE AND grant, declared
  // Advertise; and the wire (Talker Advertise for source 7's stream).
  void probe_cross_source() {
    const int lo = 0, hi = 7;
    const unsigned F_LO = 1051, F_LO_SHRINK = 900, F_HI = 200;
    const uint64_t sid_lo = (OWN_MAC << 16) | 0x500, sid_hi = (OWN_MAC << 16) | 0x507;
    const uint64_t da_lo = DA0 + 0x40, da_hi = DA0 + 0x47;
    unsigned tot_grant = 0, tot_conf = 0, tot_adv = 0, tot_wire_adv = 0, runs = 0;
    unsigned longest = 0;
    for (int mode = 0; mode < 2; ++mode) {
      for (unsigned phase = 0; phase < 8; ++phase) {
        h.reset(); d->link_up_i = 1; h.idle(40);
        auto rl = h.op(OP_DECL_TK, lo, sid_lo, da_lo, 2, F_LO, 1);
        auto rh = h.op(OP_DECL_TK, hi, sid_hi, da_hi, 2, F_HI, 1);
        h.idle(64);
        h.feed(mrpdu_body(true, {Msg{3, 8, true,
          {Vec{false, 1, fv_sid(sid_lo), {EV_NEW}, {DECL_READY}},
           Vec{false, 1, fv_sid(sid_hi), {EV_NEW}, {DECL_READY}}}}}), true);
        h.idle(64);
        AdmModel before; before.req[lo] = before.req[hi] = true;
        before.mfs[lo] = F_LO; before.mfs[hi] = F_HI; before.mif[lo] = before.mif[hi] = 1;
        before.walk();
        AdmModel after = before; after.mfs[lo] = mode ? F_LO_SHRINK : F_LO; after.walk();
        CHECK(rl.got && rh.got && before.grant[lo] && !before.grant[hi] &&
              after.grant[lo] && !after.grant[hi],
              "PROBE model: 0 admitted, 7 refused before and after (mode %d)", mode);
        CHECK(h.active(lo) && (d->sr_admitted_o & 1u) && !(d->sr_admitted_o & 0x80u) &&
              h.tk_decl(hi) == 2 && !h.active(hi) && h.lstn_reg(hi) == DECL_READY,
              "PROBE precondition phase %u mode %d: 0 active+granted, 7 Failed with Listener Ready",
              phase, mode);
        // run past the next join tick so the precondition wire is flushed
        h.run_ms(450);
        size_t wire0 = h.archive.size();
        for (unsigned n = 0; d->dbg_sample_index_o != phase && n < 8; ++n) h.cycle();
        h.samples.clear(); h.recording = true;
        h.op(OP_DECL_TK, lo, sid_lo, da_lo, 2, mode ? F_LO_SHRINK : F_LO, 1);
        h.idle(96);
        h.recording = false;
        unsigned grant = 0, conf = 0, adv = 0, run = 0, lng = 0;
        for (const auto& x : h.samples) {
          bool g = (x.grants >> hi) & 1u;
          bool a = (x.active >> hi) & 1u;
          grant += g; conf += (g && a);
          adv += ((x.tk_decl >> (2 * hi)) & 3u) == 1u;
          run = g ? run + 1 : 0; lng = std::max(lng, run);
        }
        // wire: two join periods after the re-declaration
        h.run_ms(450);
        unsigned wire_adv = 0;
        for (size_t i = wire0; i < h.archive.size(); ++i)
          if (frame_has(h.archive[i], true, 1, sid_hi, EV_NEW) ||
              frame_has(h.archive[i], true, 1, sid_hi, EV_JOININ) ||
              frame_has(h.archive[i], true, 1, sid_hi, EV_JOINMT)) ++wire_adv;
        printf("PROBE mode=%s phase=%u src7_grant_cycles=%u src7_active_and_grant_cycles=%u "
               "src7_declared_advertise_cycles=%u longest_grant=%u wire_talker_advertise_frames=%u "
               "settled_src7_grant=%u settled_src7_decl=%d\n",
               mode ? "shrink" : "identical", phase, grant, conf, adv, lng, wire_adv,
               unsigned((d->sr_admitted_o >> hi) & 1u), h.tk_decl(hi));
        CHECK(grant == 0, "PROBE refused source 7 never grants (mode %d phase %u)", mode, phase);
        CHECK(conf == 0, "PROBE refused source 7 never ACTIVE AND granted (mode %d phase %u)", mode, phase);
        CHECK(adv == 0 && wire_adv == 0,
              "PROBE refused source 7 never declares Advertise (mode %d phase %u)", mode, phase);
        tot_grant += grant != 0; tot_conf += conf != 0; tot_adv += adv != 0;
        tot_wire_adv += wire_adv != 0; longest = std::max(longest, lng); ++runs;
      }
    }
    printf("PROBE SUMMARY runs=%u with_grant=%u with_active_and_grant=%u with_declared_advertise=%u "
           "with_wire_advertise=%u longest_grant_cycles=%u\n",
           runs, tot_grant, tot_conf, tot_adv, tot_wire_adv, longest);
  }

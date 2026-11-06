// Reviewer probes (round 3), inserted into a scratch copy of
// tb/srp_stream_fsms/sim_main.cpp by scripts/make_probe_tree.sh.
// Each CHECK is prefixed XP. XP1 and XP4-XP6 are the round 2 probes
// unchanged; XP2 and XP3 are the round 2 info probes, now CHECKs;
// XP7-XP13 are new and target the link-change claims of this head.
void SrpStreamFsmsSuite::r770_probes() {
  const int sL = app_msg(LA, false, false);
  const int sN = app_msg(VN, false, false);
  // XP1: 13-bit leave deadline, wrap-safe, exact T-MRP-LEAVE (Milan Table 4.3)
  const uint32_t t0s[] = {100000u, 8192u - 3000u, 8191u, 8192u, 3191u, 3192u,
                          16384u * 3u + 4999u, 0xFFFFFFFFu - 2500u, 0xFFFFFFFFu, 0u};
  const uint32_t offs[] = {0u, 1u, 2000u, 3191u, 3192u, 4999u, 5000u, 5001u, 8191u};
  for (uint32_t t0 : t0s) {
    for (uint32_t off : offs) {
      h.reset();
      h.now = t0;
      h.idle(2);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      h.la_rx_lanes(kLaTalkerAdv);                 // LV, deadline t0 + 5000
      h.now = t0 + off;
      h.idle(2);
      h.clear_logs();
      h.ctl(true, 0, SID0, DA0, VID0);
      bool ok;
      if (off < LEAVE_MS) {
        ok = h.l_reg[0] == 1 && h.l_regst(0) == R_LV && h.l_arm.size() == 1
             && !h.l_arm[0].cancel && h.l_arm[0].deadline == t0 + LEAVE_MS;
      } else {
        ok = h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT && h.l_arm.empty();
      }
      CHECK(ok, "XP1: t0 %u settle at +%u: %s (reg %d, state %d, %zu ops, deadline %u want %u)",
            t0, off, off < LEAVE_MS ? "seeded LV, deadline t0+5000" : "expired, nothing",
            h.l_reg[0], h.l_regst(0), h.l_arm.size(),
            h.l_arm.empty() ? 0u : h.l_arm[0].deadline, t0 + LEAVE_MS);
    }
  }
  // XP2: a sink settled through a link change, then A8 and A15 on the same
  // triple (round 2 F1's path): ended at the fall, nothing kept after
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    const bool reg_before = h.l_tkreg(0) == 1;
    h.clear_logs();
    d->link_up_i = 0; h.idle(3);
    const int unreg_dn = h.l_unreg[0];
    const int tk_dn = h.l_tkreg(0);
    d->link_up_i = 1; h.idle(3);
    const int unreg_all = h.l_unreg[0];
    h.ctl(false, 0, SID0, DA0, VID0);
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    printf("XPINFO XP2: settled through link down/up: before %d, unreg at down %d, tk at down %d, "
           "unreg total %d, after A8+A15 same: reg %d tk %d state %d\n", reg_before, unreg_dn,
           tk_dn, unreg_all, h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
    CHECK(reg_before && unreg_dn == 1 && tk_dn == 0 && unreg_all == 1 && h.l_reg[0] == 0
          && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT,
          "XP2: settled through a link change, A8 and A15 on the same triple keep nothing "
          "(before %d, unreg dn %d, tk dn %d, unreg %d, reg %d tk %d state %d)", reg_before,
          unreg_dn, tk_dn, unreg_all, h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
  }
  // XP3: A8 on the clock the link goes down, link up, A15 on the same triple
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    h.clear_logs();
    d->ctl_valid_i = 1; d->ctl_settle_i = 0; d->ctl_sink_i = 0;
    d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
    d->link_up_i = 0;
    h.step(); h.idle(3);
    const int unreg_dn = h.l_unreg[0];
    d->link_up_i = 1; h.idle(3);
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    printf("XPINFO XP3: A8 on the link-down clock (unreg there %d), link up, A15 same: "
           "reg %d tk %d state %d\n", unreg_dn, h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
    CHECK(h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT,
          "XP3: A8 on the link-down clock, link up, A15 same: nothing (reg %d tk %d state %d)",
          h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
  }
  // XP4: no stale registration survives a re-bind to a different stream
  h.reset();
  fill_port_registrars();
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.ctl(false, 0, SID0, DA0, VID0);
  h.tick();
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);                 // another, unregistered value
  const bool other_quiet = h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT;
  h.ctl(false, 0, SIDF, DAF, VID0);
  h.tick();
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);                 // back to the first value
  CHECK(other_quiet && nothing_applied(),
        "XP4: a re-bind to another stream ends the kept registration; binding back "
        "to the first stream takes nothing (other %d, reg %d, tk %d)", other_quiet,
        h.l_reg[0], h.l_tkreg(0));
  // XP5: a kept LV registration keeps its own leave slot and ends at its deadline
  {
    h.reset();
    fill_port_registrars();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    h.clear_logs();
    h.la_rx_lanes(kLaTalkerAdv);
    const bool armed = h.l_arm.size() == 1 && !h.l_arm[0].cancel
                       && h.l_arm[0].deadline == NOW + LEAVE_MS;
    h.ctl(false, 0, SID0, DA0, VID0);
    h.tick();
    h.now = NOW + 2000;
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    const bool kept = h.l_reg[0] == 1 && h.l_tkreg(0) == 1 && h.l_regst(0) == R_LV
                      && h.l_arm.empty();
    h.now = NOW + LEAVE_MS;
    h.clear_logs();
    h.expire(kLsSlot);
    CHECK(armed && kept && h.l_unreg[0] == 1 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT,
          "XP5: an LV registration kept through A8 and a same-stream A15 keeps its own "
          "leave slot and ends at its deadline (armed %d, kept %d, unreg %d, tk %d, state %d)",
          armed, kept, h.l_unreg[0], h.l_tkreg(0), h.l_regst(0));
  }
  // XP6: an LV registrar unbound, re-bound to another unheld stream: its slot is cancelled
  h.reset();
  fill_port_registrars();
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);
  h.ctl(false, 0, SID0, DA0, VID0);
  h.tick();
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);
  CHECK(h.l_arm.size() == 1 && h.l_arm[0].cancel && h.l_arm[0].slot == kLsSlot
        && h.l_regst(0) == R_MT && h.l_reg[0] == 0,
        "XP6: an LV registration unbound and re-bound to another stream cancels its "
        "leave slot and starts MT (%zu ops, cancel %d, state %d)", h.l_arm.size(),
        h.l_arm.empty() ? -1 : (int)h.l_arm[0].cancel, h.l_regst(0));

  // XP7: a seeded LV settle, the link down on the very next clock (the seeded
  // arm is issuing): the arm then a cancel of the same slot, one
  // EVT_TK_UNREGISTERED, MT; a stale expiry of that slot later does nothing;
  // the talker's next declaration registers again
  {
    h.reset();
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);   // port registers
    h.la_rx_lanes(kLaTalkerAdv);                                 // port entry LV
    h.now = NOW + 1000; h.idle(2);
    h.clear_logs();
    d->ctl_valid_i = 1; d->ctl_settle_i = 1; d->ctl_sink_i = 0;
    d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
    h.step();                                                    // settle: seeded LV
    d->link_up_i = 0;
    h.step();                                                    // seeded arm + link
    h.idle(4);
    const bool ops = h.l_arm.size() == 2 && !h.l_arm[0].cancel && h.l_arm[0].slot == kLsSlot
                     && h.l_arm[0].deadline == NOW + LEAVE_MS && h.l_arm[1].cancel
                     && h.l_arm[1].slot == kLsSlot;
    const bool down = h.l_reg[0] == 1 && h.l_unreg[0] == 1 && h.l_regst(0) == R_MT
                      && h.l_tkreg(0) == 0;
    std::string opw;
    for (const auto& a : h.l_arm) {
      char b[48]; snprintf(b, sizeof b, "%s%s@%u:%u", opw.empty() ? "" : " ",
                           a.cancel ? "cancel" : "arm", unsigned(a.slot), a.deadline);
      opw += b;
    }
    d->link_up_i = 1; h.idle(3);
    h.now = NOW + LEAVE_MS;
    h.clear_logs();
    h.expire(kLsSlot);                                           // stale expiry
    const bool stale_quiet = h.l_unreg[0] == 0 && h.l_reg[0] == 0 && h.l_regst(0) == R_MT;
    h.clear_logs();
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    const bool again = h.l_reg[0] == 1 && h.l_tkreg(0) == 1 && h.l_regst(0) == R_IN;
    CHECK(ops && down && stale_quiet && again,
          "XP7: seeded LV, link down on the next clock: arm then cancel, one unregistered, "
          "MT; a stale expiry later is quiet; the next declaration registers (ops %d [%s], "
          "down %d, stale quiet %d, again %d)", ops, opw.c_str(), down, stale_quiet, again);
  }
  // XP8: a Talker registered while the link is down (no edge), then LINK_UP
  // (Begin!): the settled sink's registration ends, published (10 §6.4:
  // "ends it the same way"); the port registrars hold nothing for a settle
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    d->link_up_i = 0; h.idle(3);
    h.clear_logs();
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);   // while down
    h.inject(true, 1, SIDF, DAF, VID0, 1 /*JoinIn*/, 0, 555);   // port only
    const bool reg_down = h.l_reg[0] == 1 && h.l_tkreg(0) == 1;
    h.clear_logs();
    d->link_up_i = 1; h.idle(3);
    const bool up = h.l_unreg[0] == 1 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT;
    h.clear_logs();
    h.ctl(true, 1, SIDF, DAF, VID0);                            // settle on the port value
    const bool none = h.l_reg[1] == 0 && h.l_tkreg(1) == 0 && h.l_regst(1) == R_MT;
    printf("XPINFO XP8: registered while down %d; at LINK_UP unreg %d tk %d; port value "
           "after LINK_UP seeds: reg %d tk %d\n", reg_down, up, h.l_tkreg(0), h.l_reg[1],
           h.l_tkreg(1));
    CHECK(reg_down && up && none,
          "XP8: a registration made while the link was down ends at LINK_UP, published; "
          "a port value from then seeds nothing (reg_down %d, up %d, none %d)", reg_down,
          up, none);
  }
  // XP9: a re-bind to another stream the port holds, its old Lv parked, then a
  // link change before the walk: the seeded registration ends, published; the
  // walk sends only the owed Lv of the old stream, no New for the new one
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    for (int k = 0; k < 3; ++k) h.tick();                       // declared Ready
    const bool declared = h.l_decl(0) == 2;
    inject_failed(1 /*JoinIn*/);                                // port holds SIDF
    h.ctl(false, 0, SID0, DA0, VID0);
    h.clear_logs();
    h.ctl(true, 0, SIDF, DAF, VID0);                            // seeded FAILED, parked
    const bool seeded = failed_at_once();
    h.clear_logs();
    d->link_up_i = 0; h.idle(3);
    d->link_up_i = 1; h.idle(3);
    const bool ended = h.l_unreg[0] == 1 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT;
    h.clear_logs();
    h.tick();
    const std::string w1 = push_words(h.l_push);
    const bool first = listener_pushes(h.l_push, {{sL, 2, SID0}});
    h.clear_logs();
    h.tick();
    const std::string w2 = push_words(h.l_push);
    CHECK(declared && seeded && ended && first && h.l_push.empty() && h.l_decl(0) == 0,
          "XP9: parked re-bind seeded on a held Failed, link down and up before the walk: "
          "ended and published, the walk sends only the owed Lv (declared %d, seeded %d, "
          "ended %d, first [%s], second [%s], decl %d)", declared, seeded, ended,
          w1.c_str(), w2.c_str(), h.l_decl(0));
  }
  // XP10: two sinks settled on one stream (one group applicant), link change:
  // both withdrawals published, the group's Lv once; the next declaration
  // registers both and one New Ready goes out
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.ctl(true, 1, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    for (int k = 0; k < 3; ++k) h.tick();
    const bool both = h.l_tkreg(0) == 1 && h.l_tkreg(1) == 1;
    h.clear_logs();
    d->link_up_i = 0; h.idle(3);
    d->link_up_i = 1; h.idle(3);
    const bool ended = h.l_unreg[0] == 1 && h.l_unreg[1] == 1 && h.l_tkreg(0) == 0
                       && h.l_tkreg(1) == 0;
    h.clear_logs();
    h.tick();
    const std::string w1 = push_words(h.l_push);
    const bool lv = listener_pushes(h.l_push, {{sL, 2, SID0}});
    h.clear_logs();
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    const bool again = h.l_reg[0] == 1 && h.l_reg[1] == 1 && h.l_tkreg(0) == 1
                       && h.l_tkreg(1) == 1;
    h.clear_logs();
    h.tick();
    const std::string w2 = push_words(h.l_push);
    CHECK(both && ended && lv && again && listener_pushes(h.l_push, {{sN, 2, SID0}}),
          "XP10: two sinks on one stream through a link change: both published, one Lv; "
          "the next declaration registers both, one New (both %d, ended %d, lv [%s], "
          "again %d, new [%s])", both, ended, w1.c_str(), again, w2.c_str());
  }
  // XP11: a settled Talker Failed through a link change: FAILED ends, the
  // failure code reads 0, nothing kept at a same-triple re-bind; latency info
  {
    h.reset();
    h.ctl(true, 0, SIDF, DAF, VID0);
    inject_failed(1 /*JoinIn*/);
    const bool failed = h.l_tkreg(0) == 2 && h.l_fcode(0) == FCODE;
    h.clear_logs();
    d->link_up_i = 0; h.idle(3);
    const bool ended = h.l_unreg[0] == 1 && h.l_tkreg(0) == 0 && h.l_fcode(0) == 0;
    const uint32_t lat_link = h.l_lat(0);
    d->link_up_i = 1; h.idle(3);
    h.ctl(false, 0, SIDF, DAF, VID0);
    h.clear_logs();
    h.ctl(true, 0, SIDF, DAF, VID0);
    const bool quiet = h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT
                       && h.l_fcode(0) == 0;
    // the same registration ended by its leavetimer! instead, for comparison
    h.reset();
    h.ctl(true, 0, SIDF, DAF, VID0);
    inject_failed(1 /*JoinIn*/);
    h.la_rx_lanes(1u << 1);                                      // Talker Failed lane
    h.now = NOW + LEAVE_MS;
    h.expire(kLsSlot);
    const uint32_t lat_lt = h.l_lat(0);
    printf("XPINFO XP11: acc_latency of a settled sink after the registration ends: link "
           "change %u, leavetimer! %u (tk %d)\n", lat_link, lat_lt, h.l_tkreg(0));
    CHECK(failed && ended && quiet && lat_link == lat_lt,
          "XP11: a settled Talker Failed through a link change ends as at its leavetimer!, "
          "and a same-triple re-bind keeps nothing (failed %d, ended %d, quiet %d, lat %u/%u)",
          failed, ended, quiet, lat_link, lat_lt);
  }
  // XP12: a LeaveAll and the link fall on the same clock: Flush! first, MT,
  // published, and no leave arm left behind (only cancels, if any)
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    h.clear_logs();
    d->leaveall_rx_i = kLaTalkerAdv; d->link_up_i = 0;
    h.step(); h.idle(4);
    bool no_arm = true;
    for (const auto& a : h.l_arm) no_arm = no_arm && a.cancel;
    CHECK(no_arm && h.l_unreg[0] == 1 && h.l_regst(0) == R_MT && h.l_tkreg(0) == 0,
          "XP12: LeaveAll on the link-fall clock: MT, published, no arm (%zu ops, unreg %d, "
          "state %d)", h.l_arm.size(), h.l_unreg[0], h.l_regst(0));
  }
  // XP13: a LeaveAll, then the link fall on the next clock (its arm issuing):
  // the last leave op of the slot is a cancel
  {
    h.reset();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    h.clear_logs();
    d->leaveall_rx_i = kLaTalkerAdv;
    h.step();
    d->link_up_i = 0;
    h.step(); h.idle(4);
    const bool last_cancel = !h.l_arm.empty() && h.l_arm.back().cancel
                             && h.l_arm.back().slot == kLsSlot;
    CHECK(last_cancel && h.l_unreg[0] == 1 && h.l_regst(0) == R_MT,
          "XP13: LeaveAll then the link fall next clock: the last op cancels the slot, MT, "
          "published (%zu ops, last cancel %d, unreg %d)", h.l_arm.size(), last_cancel,
          h.l_unreg[0]);
  }
}

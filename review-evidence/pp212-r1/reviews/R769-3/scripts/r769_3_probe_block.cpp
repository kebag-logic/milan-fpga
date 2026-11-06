  // ---- R769-3 reviewer probes (disposable; inserted before the tally) ----
  {
    const int qL = app_msg(LA, false, false);
    // Q1: P1 again, with the exact expectation PS24 states: after the link
    // change and the same-triple re-bind nothing is registered, published or
    // declared, and the only push is the owed Lv (before the old Lv) or none
    for (const bool lv_out : {false, true}) {
      h.reset();
      fill_port_registrars();
      h.ctl(true, 0, SID0, DA0, VID0);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      h.clear_logs();
      d->link_up_i = 0; h.idle(3);
      d->link_up_i = 1; h.idle(3);
      const int unreg = h.l_unreg[0];
      h.ctl(false, 0, SID0, DA0, VID0);
      if (lv_out) h.tick();
      h.clear_logs();
      h.ctl(true, 0, SID0, DA0, VID0);
      const bool quiet = h.l_reg[0] == 0 && h.l_unreg[0] == 0 && h.l_tkreg(0) == 0
                         && h.l_regst(0) == R_MT && h.l_arm.empty();
      h.clear_logs(); h.tick();
      const bool push_ok = lv_out ? h.l_push.empty()
                                  : listener_pushes(h.l_push, {{qL, 2, SID0}});
      const std::string w = push_words(h.l_push);
      h.clear_logs(); h.tick();
      CHECK(unreg == 1 && quiet && push_ok && h.l_push.empty() && h.l_decl(0) == 0,
            "PROBE Q1 (lv_out %d): link down/up unreg %d, A8, A15 same: quiet %d, "
            "first tx! %s, decl %d", lv_out, unreg, quiet, w.c_str(), h.l_decl(0));
    }
    // Q2: the Talker Failed variant: Asking Failed withdrawn at the link change,
    // FAILED ends, and a same-triple re-bind applies nothing
    for (const bool lv_out : {false, true}) {
      h.reset();
      fill_port_registrars();
      h.ctl(true, 0, SIDF, DAF, VID0);
      inject_failed(1 /*JoinIn*/);
      for (int k = 0; k < 3; ++k) h.tick();
      const bool failed = h.l_tkreg(0) == 2 && h.l_decl(0) == 1;
      h.clear_logs();
      d->link_up_i = 0; h.idle(3);
      const int unreg = h.l_unreg[0];
      const int tk_dn = h.l_tkreg(0), decl_dn = h.l_decl(0);
      d->link_up_i = 1; h.idle(3);
      h.ctl(false, 0, SIDF, DAF, VID0);
      if (lv_out) h.tick();
      h.clear_logs();
      h.ctl(true, 0, SIDF, DAF, VID0);
      const bool quiet = h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT;
      h.clear_logs(); h.tick(); h.tick();
      CHECK(failed && unreg == 1 && tk_dn == 0 && decl_dn == 0 && quiet && h.l_decl(0) == 0,
            "PROBE Q2 (lv_out %d): Failed settled (%d), link down: unreg %d tk %d decl %d; "
            "re-bind same: quiet %d decl %d fcode %u", lv_out, failed, unreg, tk_dn,
            decl_dn, quiet, h.l_decl(0), h.l_fcode(0));
    }
    // Q3: an A15 on the same triple on the LINK_UP clock (PS23 grades the fall)
    {
      h.reset();
      h.ctl(true, 0, SID0, DA0, VID0);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      d->link_up_i = 0; h.idle(3);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);   // while down
      const int tk_in_down = h.l_tkreg(0);
      h.ctl(false, 0, SID0, DA0, VID0);
      h.tick();
      h.clear_logs();
      d->ctl_valid_i = 1; d->ctl_settle_i = 1; d->ctl_sink_i = 0;
      d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
      d->link_up_i = 1;
      h.step(); h.idle(2);
      const bool none = nothing_applied();
      CHECK(none, "PROBE Q3: registered while the link was down (tk %d), A8, A15 same on "
            "the LINK_UP clock: nothing applied (decl %d)", tk_in_down, h.l_decl(0));
    }
    // Q4: a settle seeded LV, the link goes down on the very next clock (the
    // seeded arm issues there): the slot is armed then cancelled, MT, one
    // unregistration; the old deadline's expiry later changes nothing
    {
      h.reset();
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      h.la_own();                                      // port entry LV
      h.clear_logs();
      d->ctl_valid_i = 1; d->ctl_settle_i = 1; d->ctl_sink_i = 0;
      d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
      h.step();                                        // settle, seeded LV
      d->link_up_i = 0;
      h.step(); h.idle(3);
      const int reg = h.l_reg[0], unreg = h.l_unreg[0], st = h.l_regst(0);
      const size_t ops = h.l_arm.size();
      const bool seq = ops == 2 && !h.l_arm[0].cancel && h.l_arm[1].cancel
                       && h.l_arm[0].slot == kLsSlot && h.l_arm[1].slot == kLsSlot;
      d->link_up_i = 1; h.idle(3);
      h.now += 6000; h.idle(1);
      h.clear_logs();
      h.expire(kLsSlot);
      const bool late = h.l_unreg[0] == 0 && h.l_reg[0] == 0 && h.l_regst(0) == R_MT;
      CHECK(reg == 1 && unreg == 1 && st == R_MT && seq && late,
            "PROBE Q4: seeded LV then link down next clock: reg %d unreg %d state %d "
            "%zu ops (arm then cancel %d), late expiry quiet %d", reg, unreg, st, ops,
            seq, late);
      h.now = NOW;
    }
    // Q5: a value received while the link is down registers the settled sink;
    // LINK_UP ends it the same way (10 §6.4's LINK_UP sentence)
    {
      h.reset();
      h.ctl(true, 0, SID0, DA0, VID0);
      d->link_up_i = 0; h.idle(3);
      h.clear_logs();
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      const int reg_dn = h.l_reg[0], tk_dn = h.l_tkreg(0);
      h.clear_logs();
      d->link_up_i = 1; h.idle(3);
      CHECK(reg_dn == 1 && tk_dn == 1 && h.l_unreg[0] == 1 && h.l_tkreg(0) == 0
            && h.l_regst(0) == R_MT,
            "PROBE Q5: registered while down (reg %d tk %d), LINK_UP: unreg %d tk %d "
            "state %d", reg_dn, tk_dn, h.l_unreg[0], h.l_tkreg(0), h.l_regst(0));
    }
    // Q6: the link change on the clock of the settled LV sink's own leavetimer!:
    // one unregistration, not two, MT
    {
      h.reset();
      h.ctl(true, 0, SID0, DA0, VID0);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      h.la_rx_lanes(kLaTalkerAdv);
      const bool lv = h.l_regst(0) == R_LV;
      h.clear_logs();
      d->exp_valid_i = 1; d->exp_slot_i = kLsSlot; d->link_up_i = 0;
      h.step(); h.idle(3);
      CHECK(lv && h.l_unreg[0] == 1 && h.l_regst(0) == R_MT && h.l_tkreg(0) == 0,
            "PROBE Q6: link down on the leavetimer! clock: LV %d unreg %d state %d "
            "(%zu ops)", lv, h.l_unreg[0], h.l_regst(0), h.l_arm.size());
      d->link_up_i = 1; h.idle(3);
    }
    // Q7: two sinks settled on one stream, both registered: each publishes its
    // own withdrawal at the link change
    {
      h.reset();
      h.ctl(true, 0, SID0, DA0, VID0);
      h.ctl(true, 1, SID0, DA0, VID0);
      h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
      const bool both = h.l_tkreg(0) == 1 && h.l_tkreg(1) == 1;
      h.clear_logs();
      d->link_up_i = 0; h.idle(3);
      d->link_up_i = 1; h.idle(3);
      CHECK(both && h.l_unreg[0] == 1 && h.l_unreg[1] == 1 && h.l_regst(0) == R_MT
            && h.l_regst(1) == R_MT,
            "PROBE Q7: two settled sinks on one stream: unreg %d/%d state %d/%d", h.l_unreg[0],
            h.l_unreg[1], h.l_regst(0), h.l_regst(1));
    }
  }

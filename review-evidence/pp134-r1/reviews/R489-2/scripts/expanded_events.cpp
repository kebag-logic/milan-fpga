// Independent extension: all slot indices, matching and unrelated receive events,
// both initial and renewed attribute variants, both LeaveAll causes.
void SrpStreamFsmsSuite::review_expanded_events() {
  int cases = 0;
  for (bool listener : {false, true}) for (bool own : {false, true})
    for (int slot = 0; slot < 8; ++slot) for (int initial = 0; initial < 2; ++initial)
      for (int replacement = 0; replacement < 2; ++replacement)
        for (bool match : {false, true}) for (int ev = 0; ev < 6; ++ev) {
          h.reset();
          const int old_type = listener ? 1 + initial : 3;
          const int new_type = listener ? 1 + replacement : 3;
          if (listener) h.ctl(true, slot, SID0, DA0, VID0);
          else h.gate(true, slot, SID0, DA0, VID0);
          h.inject(true, old_type, SID0, DA0, VID0, 0, 2 + initial, 500, 0x1234, 1);
          if (own) h.la_own(); else h.la_rx();
          h.idle(12);
          const bool aged = (listener ? h.l_regst(slot) : h.t_reg(slot)) == 2;
          h.clear_logs();
          d->exp_valid_i = 1;
          d->exp_slot_i = (listener ? 24 : 16) + slot;
          h.inject(true, new_type, SID0 + (match ? 0 : 1), DA0, VID0,
                   ev, 2 + replacement, 501, 0x5678, 2);
          h.idle(12);
          const bool renew = match && (ev == 0 || ev == 1 || ev == 3);
          const int state = listener ? h.l_regst(slot) : h.t_reg(slot);
          const bool published = listener
            ? h.l_tkreg(slot) == (renew ? new_type : 0)
            : h.t_lstn(slot) == (renew ? 2 + replacement : 0)
              && bool((d->t_active_o >> slot) & 1) == renew;
          const bool events = listener
            ? h.l_unreg[slot] == int(!renew)
              && h.l_reg[slot] == int(renew && initial != replacement)
              && h.l_fchg[slot] == int(renew && initial == 1 && replacement == 1)
            : h.t_chg[slot] == int(!renew || initial != replacement);
          const auto& timer = listener ? h.l_arm : h.t_arm;
          const bool timer_ok = renew ? timer.size() == 1 && timer[0].cancel : timer.empty();
          const bool payload = !listener || !renew ||
            (h.l_lat(slot) == 501 && h.l_fcode(slot) == (replacement ? 2 : 0)
             && (!replacement || h.l_fbridge(slot) == 0x5678));
          bool isolated = true;
          for (int s = 0; s < 8; ++s) if (s != slot)
            isolated &= h.t_reg(s) == 0 && h.l_regst(s) == 0 && h.t_chg[s] == 0
                        && h.l_unreg[s] == 0 && h.l_reg[s] == 0 && h.l_fchg[s] == 0;
          CHECK(aged && state == int(renew) && published && events && timer_ok
                && payload && isolated,
                "REVIEW_EVENT plane=%d own=%d slot=%d old=%d new=%d match=%d ev=%d "
                "state=%d published=%d events=%d timer=%d payload=%d isolated=%d",
                listener, own, slot, initial, replacement, match, ev, state,
                published, events, timer_ok, payload, isolated);
          ++cases;
        }
  printf("REVIEW_EVENT_CASES %d\n", cases);
}

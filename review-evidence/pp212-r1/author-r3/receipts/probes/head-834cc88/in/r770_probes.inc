// Reviewer probes, inserted into a scratch copy of tb/srp_stream_fsms/sim_main.cpp
// by scripts/make_probe_tree.sh. Each CHECK is prefixed XP.
void SrpStreamFsmsSuite::r770_probes() {
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
  // XP2: a sink settled through a link change, then A8 and A15 on the same triple
  h.reset();
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  const bool reg_before = h.l_tkreg(0) == 1;
  d->link_up_i = 0; h.idle(3); d->link_up_i = 1; h.idle(3);
  const bool kept_settled = h.l_tkreg(0) == 1;
  h.ctl(false, 0, SID0, DA0, VID0);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  printf("XPINFO XP2: settled through link down/up: before %d, kept while settled %d, "
         "after A8+A15 same: reg %d tk %d state %d\n", reg_before, kept_settled,
         h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
  // XP3: A8 on the clock the link goes down, link up, A15 on the same triple
  h.reset();
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  d->ctl_valid_i = 1; d->ctl_settle_i = 0; d->ctl_sink_i = 0;
  d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
  d->link_up_i = 0;
  h.step(); h.idle(3);
  d->link_up_i = 1; h.idle(3);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  printf("XPINFO XP3: A8 on the link-down clock, link up, A15 same: reg %d tk %d state %d\n",
         h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
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
}

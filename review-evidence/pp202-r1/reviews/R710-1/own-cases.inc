  // Independent dense provisioned collisions: the first eight candidates
  // include the withdrawn ID and every other configured/current ID.
  {
    Hn h;
    for (int s = 0; s < N_SRC; ++s) h.sid_cfg[s] = SidChecks::UP | uint64_t(8+s);
    h.configure_the_talker_and_release_reset(); h.run(400);
    for (int s = 0; s < N_SRC; ++s) h.da[s] = da_pool(s);
    for (int s = 0; s < N_SRC; ++s)
      CHECK(h.sid_pub(s) == h.sid_cfg[s], "OWN reset publishes arbitrary slot %d", s);
    const auto moved = sid.move_once(h, 0, "OWN dense collision");
    CHECK(moved == (SidChecks::UP | 16) && h.sid_pub(0) == moved
          && sid.all_distinct(h), "OWN dense collision skips all eight occupied IDs");
    printf("OWN collision: old=%016llx new=%016llx expected=%016llx\n",
           (unsigned long long)h.sid_cfg[0], (unsigned long long)moved,
           (unsigned long long)(SidChecks::UP | 16));
  }
  // A dynamic PCP change after a listener-driven withdrawal must still
  // protect the same ID when demand returns before two LeaveAllTime.
  for (int moved_case = 0; moved_case < 2; ++moved_case) {
    Hn h; h.configure_the_talker_and_release_reset(); h.run(400);
    h.d->now_ms_i = 1000;
    h.set_lsn(0, LSN_READY);
    CHECK(h.decl_mask() == 1, "OWN PCP setup declares source zero");
    if (moved_case) {
      h.d->maap_conflict_valid_i=1; h.d->maap_conflict_src_i=0;
      h.tick(); h.run(200);
      CHECK(h.sid_pub(0) == (SidChecks::UP|8) && h.decl_mask()==1,
            "OWN PCP setup moved ID after conflict");
    }
    const uint64_t withdrawn_sid=h.sid_pub(0);
    h.d->now_ms_i = 1010;
    h.set_lsn(0, LSN_NONE);
    CHECK(h.decl_mask() == 0, "OWN PCP setup withdraws source zero");
    h.gates.clear(); h.arms.clear();
    h.d->now_ms_i = 1011;
    h.d->srp_pcp_change_i = 1; h.tick(); h.run(80);
    h.d->now_ms_i = 1012;
    h.set_lsn(0, LSN_READY);
    bool early_same = false;
    for (const auto& g : h.gates) if (g.open && g.src == 0) {
      printf("OWN PCP: withdrawn_ms=1010 opened_ms=%u sid=%016llx original=%016llx arms=%zu\n",
             g.ms, (unsigned long long)g.sid, (unsigned long long)withdrawn_sid, h.arms.size());
      if (g.sid == withdrawn_sid && g.ms - 1010 < 20000) early_same = true;
    }
    CHECK(!early_same, "OWN PCP after withdrawal preserves same-ID two-LeaveAll gap");
  }

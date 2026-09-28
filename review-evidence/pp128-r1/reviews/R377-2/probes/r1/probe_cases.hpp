// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe cases for processor issue #128. Appended to a DISPOSABLE
// copy of tb/acmp_talker (included after retry_cases.hpp); never committed.
// Checks are tagged "P" so they are distinguishable from the suite's own.
struct ReviewerProbes {
  int& checks;
  int& fails;
  // P1: an ACCEPTED, never-answered allocation with another source's retry
  // pending. Solicited commands must keep being served back to back within
  // the retry-induced command bound (P-MAAP-ACCEPT-CYC + 64), not only once.
  void silent_accept_back_to_back_commands() {
    Hn h; h.auto_grant = false;
    h.configure_the_talker_and_release_reset();
    h.d->cfg_src_en_i = 0x03; h.run(60);
    CHECK(h.mreqs.size() == 1, "P1 src0 alloc accepted and silent (%zu)", h.mreqs.size());
    for (int i = 0; i < 6; ++i) {
      h.resps.clear();
      bool ok = h.send(MT_PROBE, 1, C1, 0x700 + i, L1, 8, FL_FC);
      CHECK(ok && h.last_send_cyc <= MAAP_TMO + 64,
            "P1 command %d consumed within bound (ok=%d cyc=%d)", i, ok, h.last_send_cyc);
      CHECK(h.resps.size() == 1 && h.resps[0].status == ST_DMAC_FAIL,
            "P1 command %d honest DEST_MAC_FAILED", i);
    }
  }
  // P2: 05 says a conflict starts a new acquisition lifetime. A source that
  // acquired its DA in the CURRENT round and is then conflicted from DA_OK
  // re-allocates without waiting for the next round (pre-#128 behaviour).
  void conflict_restarts_lifetime_in_round() {
    Hn h;
    h.configure_the_talker_and_release_reset();
    h.run(400);
    CHECK(h.mreqs.size() == N_SRC, "P2 boot walk (%zu)", h.mreqs.size());
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 3; h.tick();
    h.run(60);   // same millisecond: no retry round boundary
    CHECK(h.mreqs.size() == N_SRC + 1 && h.mreqs.back().src == 3 && !h.mreqs.back().rel,
          "P2 conflicted DA_OK source re-allocates inside the round (%zu)", h.mreqs.size());
  }
  // P3: continuous solicited commands with a refusing allocator and every
  // source in NO_DA: the maximum command gap stays within the documented
  // bound while retries proceed, one attempt per source per round.
  void refusing_allocator_under_command_load() {
    Hn h; h.grant_ok = false;
    h.configure_the_talker_and_release_reset(); h.run(400);
    const auto boot = h.mreqs.size();
    int max_cyc = 0;
    for (int round = 1; round <= 3; ++round) {
      h.d->now_ms_i = 100 + round * 100;
      for (int i = 0; i < 8; ++i) {
        h.resps.clear();
        bool ok = h.send(MT_PROBE, i, C1, 0x800 + i, L1, 8, FL_FC);
        if (h.last_send_cyc > max_cyc) max_cyc = h.last_send_cyc;
        CHECK(ok && h.resps.size() == 1 && h.resps[0].status == ST_DMAC_FAIL,
              "P3 round %d probe %d honest failure", round, i);
      }
      h.run(200);
      CHECK(h.mreqs.size() == boot + size_t(round) * N_SRC,
            "P3 round %d exactly one attempt per source (%zu)", round, h.mreqs.size());
    }
    CHECK(max_cyc <= MAAP_TMO + 64, "P3 command wait bound (max %d)", max_cyc);
  }
  // P4: backoff expiry with the DA invalid re-enters NO_DA + ALLOC_DA at
  // once (F05.12 arc), not at the next retry round. Expiry fired mid-round.
  void backoff_exit_reallocates_mid_round() {
    Hn h; h.configure_the_talker_and_release_reset(); h.d->cfg_src_en_i = 1;
    h.run(100);
    h.resps.clear();
    CHECK(h.send(MT_PROBE, 0, C1, 0x900, L1, 8, FL_FC) && h.decl_mask() == 1, "P4 declaring");
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 0; h.tick(); h.run(60);
    const auto before = h.mreqs.size();
    h.d->now_ms_i = 150; h.fire_expiry(0); h.run(60);   // round boundary is 200
    CHECK(h.mreqs.size() == before + 1 && !h.mreqs.back().rel,
          "P4 backoff exit re-allocates inside the round (%zu -> %zu)", before, h.mreqs.size());
  }
  // P5/P6: after a conflict clears a refused source's pacing bit inside a
  // round, a probe (P5) or a listener change (P6) asks again immediately.
  void demand_after_conflict_window(bool listener) {
    Hn h; h.grant_ok = false; h.configure_the_talker_and_release_reset(); h.run(400);
    const auto before = h.mreqs.size();
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 3; h.tick(); h.run(40);
    if (listener) h.set_lsn(3, LSN_READY);
    else { h.resps.clear(); h.send(MT_PROBE, 3, C1, 0x910, L1, 8, FL_FC); }
    h.run(60);
    CHECK(h.mreqs.size() == before + 1 && h.mreqs.back().src == 3,
          "P%d %s re-asks inside the round after a conflict (%zu -> %zu)", listener ? 6 : 5,
          listener ? "listener change" : "probe", before, h.mreqs.size());
  }
};

void run_reviewer_probes(int& checks, int& fails) {
  ReviewerProbes p{checks, fails};
  p.silent_accept_back_to_back_commands();
  p.conflict_restarts_lifetime_in_round();
  p.refusing_allocator_under_command_load();
  p.backoff_exit_reallocates_mid_round();
  p.demand_after_conflict_window(false);
  p.demand_after_conflict_window(true);
}

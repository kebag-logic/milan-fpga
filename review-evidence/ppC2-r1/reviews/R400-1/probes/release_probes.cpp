// R400-1 disposable probes, appended to a scratch copy of tb/maap/sim_main.cpp
// by probes/insert_probes.py. Each CHECK states what docs/architecture/
// 11_maap_engine.md section 6 (Release! row) and IEEE 1722-2016 Table B.7
// footnote c say; a FAIL line is a measured divergence, not a harness error.

// ---- P1: 11 s6 "seed re-armed for the next engage" on the W_ADDR Release! arc
// A provisioned seed is consumed, a PROBE-state rAnnounce! yields (the seed is
// then deliberately not reused inside the engagement), the redraw loop is
// held by overhanging kind-7 draws, and the link drops mid-redraw. The next
// engage is a new engagement: section 6 says its first PROBE is the seed.
// P1c is the control: the same, but the Release! lands after the yield-walk
// already sent its first PROBE (the W_IDLE arc).
void MaapAnnexBSuite::p1_release_mid_redraw_rearms_the_seed() {
  for (int variant = 0; variant < 2; ++variant) {
    const char* tag = variant ? "P1c" : "P1";
    d->link_up_i = 0; h.idle(30);
    h.addr_script.clear();
    d->cfg_count_i = COUNT;
    d->cfg_seed_offset_i = 0x2000;
    d->cfg_seed_valid_i = 1;
    size_t n0 = h.tx.size();
    d->link_up_i = 1;
    CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs) && (d->addr_o & 0xFFFF) == 0x2000,
          "%s: premise, the seed 0x2000 is probed first", tag);
    // the seed is contested: PROBE/rAnnounce! yields with no tie-break
    if (variant == 0) h.addr_script = {uint16_t(POOL_SIZE - 1)};  // hold the redraw loop
    h.addr_draws = 0;
    const size_t n1 = h.tx.size();
    h.rx(3, 0xF2FFEEDDCCFFull, POOL_HI | 0x2000, COUNT);
    if (variant == 0) {
      for (int g = 0; g < 2000 && h.addr_draws < 3; ++g) h.step();
      CHECK(h.addr_draws >= 3 && h.tx.size() == n1 && d->state_o == 0,
            "%s: premise, the walker is redrawing (draws %zu)", tag, h.addr_draws);
    } else {
      CHECK(h.wait_frames(n1 + 1, kProbeBudgetMs) && (d->addr_o & 0xFFFF) != 0x2000,
            "%s: premise, the yield-walk probes a fresh range", tag);
    }
    d->link_up_i = 0; h.idle(30);                        // Release!
    h.addr_script.clear();
    const size_t n2 = h.tx.size();
    d->link_up_i = 1;                                    // PortOperational!
    CHECK(h.wait_frames(n2 + 1, kProbeBudgetMs), "%s: the next engagement probes", tag);
    const unsigned got = unsigned(d->addr_o & 0xFFFF);
    printf("  %s: first PROBE of the next engagement at offset 0x%04x\n", tag, got);
    CHECK(got == 0x2000,
          "%s: 11 s6 Release! re-arms the seed: next engagement probes 0x2000 (got 0x%04x)",
          tag, got);
  }
  d->cfg_seed_valid_i = 0;
  d->link_up_i = 0; h.idle(30);
  d->link_up_i = 1;
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
}

// ---- P2: Release! while the 4th PROBE / 1st ANNOUNCE are in the TX path ------
// Footnote c: Release! sends no PDU; section 6: INITIAL. Sweep the drop over
// 160 consecutive cycles after the 4th PROBE's lane grant and count lane
// grants after the drop and claims (addr_valid_o) that RISE after the drop.
void MaapAnnexBSuite::p2_release_inside_the_tx_path() {
  int k_with_pdu = 0, k_with_claim = 0, k_first_pdu = -1, k_first_claim = -1;
  int max_valid_run = 0;
  for (int k = 0; k < 160; ++k) {
    d->link_up_i = 0; h.idle(30);
    h.addr_script.clear();
    d->cfg_count_i = COUNT;
    d->link_up_i = 1;
    int grants = 0;
    for (long c = 0; c < 6L * kProbeBudgetMs * kClkPerMs && grants < 4; ++c) {
      if (!h.ser_busy && d->txreq_valid_o) ++grants;
      h.step();
    }
    for (int i = 0; i < k; ++i) h.step();
    const bool valid_at_drop = d->addr_valid_o;
    d->link_up_i = 0;                                    // Release!
    int after = 0;
    bool rose = false;
    bool prev = valid_at_drop;
    for (int c = 0; c < 50 * kClkPerMs; ++c) {
      if (!h.ser_busy && d->txreq_valid_o) ++after;
      h.step();
      if (d->addr_valid_o && !prev) rose = true;
      if (rose && d->addr_valid_o) { static int run; run = prev ? run + 1 : 1;
        if (run > max_valid_run) max_valid_run = run; }
      prev = d->addr_valid_o;
    }
    if (after) { ++k_with_pdu; if (k_first_pdu < 0) k_first_pdu = k; }
    if (rose)  { ++k_with_claim; if (k_first_claim < 0) k_first_claim = k; }
  }
  printf("  P2: of 160 drop offsets, %d put a PDU on the lane after Release! (first k=%d),"
         " %d raised addr_valid_o after Release! (first k=%d)\n",
         k_with_pdu, k_first_pdu, k_with_claim, k_first_claim);
  printf("  P2: longest post-Release! addr_valid_o run: %d cycles\n", max_valid_run);
  CHECK(k_with_pdu == 0, "P2: footnote c, no PDU after Release! (%d of 160 offsets sent one)",
        k_with_pdu);
  CHECK(k_with_claim == 0, "P2: no claim published after Release! (%d of 160 offsets)",
        k_with_claim);
  d->link_up_i = 1;
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
}

// ---- P3: a short link bounce while a DEFEND is being built -------------------
// Release! then PortOperational! (Table B.7): INITIAL, then a fresh walk. The
// bounce lands inside the sDefend TX path of a DEFEND-state claim.
void MaapAnnexBSuite::p3_bounce_inside_the_defend_path() {
  CHECK(d->addr_valid_o && d->state_o == 2, "P3: premise, DEFEND state");
  const uint64_t b = d->addr_o;
  const unsigned c0 = d->conflicts_o;
  // rProbe! -> sDefend, driven by hand so the bounce lands inside the TX path
  d->txn_msg_i = 1; d->txn_status_i = 1; d->txn_src_mac_i = 0x0A2233445566ull;
  d->txn_req_i = ((b + 2) << 16) | 2; d->txn_conf_i = 0; d->txn_valid_i = 1;
  int acc = 0;
  for (int g = 0; g < kRxAcceptCycles && !acc; ++g) {
    d->clk_i = 0; d->eval();
    acc = d->txn_ready_o;
    h.step_body();
  }
  d->txn_valid_i = 0;
  h.idle(3);                                             // W_RX -> W_ALLOC -> ...
  const size_t nb = h.tx.size();
  d->link_up_i = 0; h.idle(5);                           // Release!
  bool dropped = !d->addr_valid_o;
  d->link_up_i = 1;                                      // PortOperational!
  int min_state = d->state_o;
  for (int c = 0; c < 50 * kClkPerMs; ++c) {
    h.step();
    if (!d->addr_valid_o) dropped = true;
    if (int(d->state_o) < min_state) min_state = d->state_o;
  }
  printf("  P3: accepted=%d; after a 5-cycle bounce inside sDefend: state_o=%u addr_valid_o=%u "
         "claim ever dropped=%d min state=%d conflicts %u->%u frames sent after the bounce=%zu\n",
         acc, unsigned(d->state_o), unsigned(d->addr_valid_o), int(dropped), min_state, c0,
         unsigned(d->conflicts_o), h.tx.size() - nb);
  CHECK(dropped && d->state_o != 2,
        "P3: Release!+PortOperational! restart the walk (claim kept through the bounce)");
}

// ---- P4: Release! while a FITTING kind-7 draw is in flight --------------------
// The fixed W_ADDR arc abandons the draw: no PDU may follow a Release! that
// lands before the kind-7 answer is consumed (footnote c), and the next
// engage must still probe. U17b only drops the link while every draw
// overhangs, so it cannot tell "abandon" from "wait for the answer, then
// leave". The drop is swept over the first 8 cycles after the rise; offsets
// where the draw had already completed (the walker is past W_ADDR, the
// disclosed W_IVAL/TX corner of F1) are reported separately, not checked.
void MaapAnnexBSuite::p4_release_during_a_fitting_draw() {
  int pdu_in_draw = 0, pdu_after_draw = 0, n_in_draw = 0, k_stuck = 0;
  for (int k = 0; k < 8; ++k) {
    d->link_up_i = 0; h.idle(30);
    d->cfg_count_i = COUNT;
    h.addr_script = {uint16_t(0x1000)};                  // every draw fits
    h.addr_draws = 0;
    d->link_up_i = 1;
    for (int i = 0; i < k; ++i) h.step();
    const bool in_draw = (h.addr_draws == 0);
    d->link_up_i = 0;                                    // Release!
    int after = 0;
    for (int c = 0; c < 50 * kClkPerMs; ++c) {
      if (!h.ser_busy && d->txreq_valid_o) ++after;
      h.step();
    }
    printf("  P4: k=%d draw_done_at_drop=%d pdus_after_release=%d\n", k, int(!in_draw), after);
    if (in_draw) { ++n_in_draw; if (after) ++pdu_in_draw; }
    else if (after) ++pdu_after_draw;
    const size_t n0 = h.tx.size();
    d->link_up_i = 1;                                    // PortOperational!
    if (!h.wait_frames(n0 + 1, kProbeBudgetMs)) ++k_stuck;
  }
  h.addr_script.clear();
  printf("  P4: %d offsets before the draw completed (%d sent a PDU); %d PDUs from "
         "offsets after it (F1 corner); %d never probed again\n",
         n_in_draw, pdu_in_draw, pdu_after_draw, k_stuck);
  CHECK(pdu_in_draw == 0,
        "P4: a Release! before the kind-7 answer sends nothing (%d offsets)", pdu_in_draw);
  CHECK(k_stuck == 0, "P4: the next engage probes (%d offsets stuck)", k_stuck);
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
}

// ---- P5: a 100 ms link outage while the MAAP lane is not granting ------------
// W_LANE holds txreq until the lane grants. If the egress does not drain while
// the link is down (a stalled serializer, modelled here by holding the
// harness's lane busy), the walker never visits W_IDLE during the outage, so
// the Release!/PortOperational! pair is never seen. Table B.7: INITIAL, then a
// fresh walk. Conditional on the lane stall; the engine behaviour is measured.
void MaapAnnexBSuite::p5_outage_while_the_lane_is_stalled() {
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
  CHECK(d->addr_valid_o && d->state_o == 2, "P5: premise, DEFEND state");
  const uint64_t b = d->addr_o;
  h.ser_busy = true;                                    // the lane stops granting
  d->txn_msg_i = 1; d->txn_status_i = 1; d->txn_src_mac_i = 0x0A2233445566ull;
  d->txn_req_i = ((b + 2) << 16) | 2; d->txn_conf_i = 0; d->txn_valid_i = 1;
  for (int g = 0; g < kRxAcceptCycles; ++g) {
    d->clk_i = 0; d->eval();
    const bool acc = d->txn_ready_o;
    h.step_body();
    if (acc) break;
  }
  d->txn_valid_i = 0;
  h.idle(80);                                           // sDefend built, waiting in the lane
  d->link_up_i = 0;                                     // Release!
  bool dropped = false;
  for (int c = 0; c < 100 * kClkPerMs; ++c) { h.step(); if (!d->addr_valid_o) dropped = true; }
  d->link_up_i = 1;                                     // PortOperational!
  h.idle(5);
  h.ser_busy = false; h.ser_cur.clear();               // the lane drains again
  for (int c = 0; c < 50 * kClkPerMs; ++c) { h.step(); if (!d->addr_valid_o) dropped = true; }
  printf("  P5: after a 100 ms outage with the lane stalled: state_o=%u addr_valid_o=%u "
         "claim ever dropped=%d addr unchanged=%d\n", unsigned(d->state_o),
         unsigned(d->addr_valid_o), int(dropped), int(d->addr_o == b));
  CHECK(dropped && d->state_o != 2,
        "P5: the outage restarts the walk (claim kept through a 100 ms Release!)");
}

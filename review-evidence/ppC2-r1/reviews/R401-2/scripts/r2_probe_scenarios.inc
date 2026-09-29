// ===== R401-2 reviewer probes (appended to a scratch copy of tb/maap) =====
// Tags start with "Q" so they never collide with the suite's U-numbers or the
// round-1 P-probes. Expectations come from the manager's ruling on #66
// (comment 5890772857) and 11 section 6, never from RTL text.

// Q1/Q2: U28's sweep, with the fall driven by cfg_en_i (Q1) or cfg_count_i -> 0
// (Q2) instead of link_up_i. Same ruling points per walker state.
void MaapAnnexBSuite::r401_fall_sweep(int source) {
  const char* tag = source == 1 ? "Q1" : "Q2";
  const char* how = source == 1 ? "cfg_en_i" : "cfg_count_i=0";
  constexpr int kWatchCycles = kAnnounceBudgetMs * kClkPerMs;
  constexpr int kPoints = static_cast<int>(std::size(kFallPoints));
  int missed = 0, requested = 0, overdrained = 0, started = 0, expired = 0, claimed = 0;
  unsigned covered = 0;
  h.confl_auto = true;
  for (int p = 0; p < kPoints; ++p) {
    const FallPoint& f = kFallPoints[p];
    if (f.how == Poise::kBounce) continue;              // those bounce the link itself
    if (!poise_a_fall(p)) { ++missed; continue; }
    covered |= 1u << f.walker;
    if (source == 1) d->cfg_en_i = 0; else d->cfg_count_i = 0;   // Release!
    h.step();                                          // the first cycle it is seen
    const size_t reqs = h.slot_reqs, grants = h.grants;
    const size_t starts = h.tmr_starts, expiries = h.tmr_expiries;
    const size_t owed = reqs - grants;
    bool valid_after = d->addr_valid_o;
    for (int c = 1; c < kWatchCycles; ++c) { h.step(); if (d->addr_valid_o) valid_after = true; }
    printf("OBS: %s %s fall in %s (%s): owed %zu, drained %zu, reqs after %zu, starts %zu, "
           "expiries %zu\n", tag, how, kWalkerName[f.walker], f.what, owed, h.grants - grants,
           h.slot_reqs - reqs, h.tmr_starts - starts, h.tmr_expiries - expiries);
    if (h.slot_reqs != reqs) ++requested;
    if (owed > 1 || h.grants - grants != owed) ++overdrained;
    if (h.tmr_starts != starts) ++started;
    if (h.tmr_expiries != expiries) ++expired;
    if (valid_after || d->state_o != 0) ++claimed;
    d->cfg_en_i = 1; d->cfg_count_i = COUNT;           // restore for the next poise
  }
  CHECK(missed == 0, "%s: premise, every fall point reached (%d missed)", tag, missed);
  CHECK(requested == 0, "%s: no TX slot request after a %s fall (%d)", tag, how, requested);
  CHECK(overdrained == 0, "%s: at most the one pre-fall frame drains (%d)", tag, overdrained);
  CHECK(started == 0, "%s: no timer started after the fall (%d)", tag, started);
  CHECK(expired == 0, "%s: no timer expiry after the fall (%d)", tag, expired);
  CHECK(claimed == 0, "%s: no claim after the fall, INITIAL (%d)", tag, claimed);
  printf("OBS: %s covered walker-state mask 0x%03x\n", tag, covered);
  h.confl_auto = false;
  h.confl_srcs.clear();
}

void MaapAnnexBSuite::r401_probes() {
  h.addr_script.clear();
  d->cfg_count_i = COUNT; d->cfg_en_i = 1; d->cfg_seed_valid_i = 0;
  h.confl_auto = true;

  // Q3/Q4: a Release! behind a frame stalled in the lane for longer than a
  // probe interval. The frame (the first PROBE) was requested before the fall;
  // the ruling lets it drain. 11 section 6 states that the timers stop once the
  // lane has the frame and that an expiry meanwhile meets INITIAL (-x-).
  // Graded: no slot request and no timer start after the fall, no claim,
  // INITIAL; Q3: exactly one frame drains when the lane resumes and nothing
  // more for 33 s; Q4: the link rises inside the stalled drain. Both: the next
  // engagement walks afresh with byte-exact PROBEs spaced inside (500, 600) ms.
  for (int rise_in_stall = 0; rise_in_stall < 2; ++rise_in_stall) {
    const char* tag = rise_in_stall ? "Q4" : "Q3";
    d->link_up_i = 0; h.idle(30);
    h.lane_hold = true;                                // the egress stops granting
    d->link_up_i = 1;                                  // PortOperational!
    const bool at_lane = run_to_walker(WK_LANE, 200L * kClkPerMs);
    CHECK(at_lane, "%s: premise, the first PROBE waits in the lane", tag);
    const size_t n0 = h.tx.size(), r0 = h.slot_reqs, s0 = h.tmr_starts, e0 = h.tmr_expiries;
    d->link_up_i = 0;                                  // Release!
    h.step();
    bool valid = false;
    for (int c = 0; c < 700 * kClkPerMs; ++c) { h.step(); if (d->addr_valid_o) valid = true; }
    const size_t exp_in_stall = h.tmr_expiries - e0;
    printf("OBS: %s expiries of the engine's timers during the 700 ms stalled drain: %zu "
           "(11 section 6: an expiry meanwhile meets INITIAL)\n", tag, exp_in_stall);
    CHECK(h.slot_reqs == r0 && h.tmr_starts == s0 && !valid && d->state_o == 0,
          "%s: during the stalled drain no slot request, no timer start, no claim, INITIAL "
          "(reqs %zu, starts %zu, state %u)", tag, h.slot_reqs - r0, h.tmr_starts - s0,
          unsigned(d->state_o));
    if (rise_in_stall) {
      d->link_up_i = 1;                                // PortOperational! inside the drain
      h.idle(5);
    }
    h.lane_hold = false;                               // the egress resumes
    if (!rise_in_stall) {
      for (int c = 0; c < kAnnounceBudgetMs * kClkPerMs; ++c) {
        h.step();
        if (d->addr_valid_o) valid = true;
      }
      CHECK(h.tx.size() == n0 + 1 && h.slot_reqs == r0 && h.tmr_starts == s0 && !valid,
            "Q3: exactly the one pre-fall frame drains, then nothing for 33 s "
            "(%zu frames, %zu reqs, %zu starts)", h.tx.size() - n0, h.slot_reqs - r0,
            h.tmr_starts - s0);
      if (h.tx.size() > n0) {
        CHECK(h.tx[n0].b.size() > 15 && h.tx[n0].b[14] == 0xFE && (h.tx[n0].b[15] & 0x0F) == 1,
              "Q3: the drained frame is the pre-fall PROBE");
      }
      d->link_up_i = 1;                                // PortOperational!
    }
    // Q3: the fresh walk's first two PROBEs. Q4: the drained PROBE, then the
    // fresh walk's first two.
    const size_t m0 = h.tx.size();
    const size_t first = rise_in_stall ? m0 + 1 : m0;
    const bool walked = h.wait_frames(first + 2, 3 * kProbeBudgetMs);
    CHECK(walked, "%s: the next engagement walks afresh (%zu frames)", tag, h.tx.size() - m0);
    if (walked) {
      const uint32_t gap = h.tx[first + 1].ms - h.tx[first].ms;
      printf("OBS: %s fresh walk PROBE spacing %u ms\n", tag, gap);
      CHECK(h.tx[first].b == maap_frame(MAAP_DA, OWN_MAC, 1, d->addr_o, COUNT, 0, 0)
                && gap > 500 && gap < 600,
            "%s: the fresh walk's PROBEs are byte-exact and spaced inside (500, 600) ms "
            "(gap %u ms): no stale expiry survives the Release!", tag, gap);
    }
    for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
  }

  r401_fall_sweep(1);
  r401_fall_sweep(2);
  h.confl_auto = false;
}

// Issue #202, REQ-ACMP-010: historical StreamID reuse must keep the gap.
// Drive only public inputs. The external allocator selects among held
// addresses after a release; no MAAP conflict or internal force is used.
int probe_disable_lap() {
  Hn h;
  h.configure_the_talker_and_release_reset(); h.run(400);
  h.review_clock = true;
  h.d->now_ms_i = 1000;
  h.send(MT_PROBE, 0, C1, 0x700, L1, 8, FL_FC);
  uint64_t active_sid = h.sid_pub(0), active_da = da_pool(0);
  std::vector<uint64_t> withdrawn_da(65536, 0);
  std::vector<uint32_t> withdrawn_ms(65536, 0);
  int opens = 0, closes = 0, repeats = 0, violations = 0;
  const bool slow = std::getenv("PROBE_SLOW") != nullptr;
  bool setup = h.decl_mask() == 1;
  uint64_t& cycles = h.review_ticks;
  uint32_t& origin_ms = h.review_origin;
  auto step = [&](int n) { h.run(n); }; // tick counts every core clock, commands included
  h.gates.clear();
  for (int iteration = 0; iteration < 66000 && repeats == 0 && setup; ++iteration) {
    h.d->cfg_src_en_i = 0xFE;
    step(200);
    bool closed = false;
    for (const auto& g : h.gates) if (g.src == 0 && !g.open) {
      withdrawn_da[unsigned(active_sid & 0xffff)] = active_da;
      withdrawn_ms[unsigned(active_sid & 0xffff)] = g.ms;
      ++closes; closed = true;
    }
    if (!closed || (h.decl_mask() & 1)) { setup = false; break; }
    h.gates.clear();
    // Three pre-allocated valid multicast destinations. A released source
    // may be assigned a different held address without a fresh claim walk.
    h.block_count = N_SRC;
    h.block_base = da_pool((iteration % 3) * 256);
    h.d->cfg_src_en_i = 0xFF;
    step(400);
    // Demand comes from an ordinary PROBE_TX; no stale Listener READY is
    // kept across a withdrawal or across a StreamID change.
    if (!h.send(MT_PROBE, 0, C1, uint16_t(iteration), L1, 8, FL_FC)) setup = false;
    bool opened = false;
    for (const auto& g : h.gates) if (g.src == 0 && g.open) {
      ++opens; opened = true;
      const unsigned uid = unsigned(g.sid & 0xffff);
      if (withdrawn_da[uid] && withdrawn_da[uid] != g.da) {
        ++repeats;
        const unsigned gap = g.ms - withdrawn_ms[uid];
        printf("REUSED sid=%016llx old_da=%012llx new_da=%012llx withdrawal_ms=%u reopen_ms=%u gap_ms=%u minimum_ms=20000 moves=%d cycles=%llu\n",
          (unsigned long long)g.sid, (unsigned long long)withdrawn_da[uid],
          (unsigned long long)g.da, withdrawn_ms[uid], g.ms, gap, opens,
          (unsigned long long)cycles);
        if (gap < 20000) {
          ++violations;
          printf("FAIL historical ID reused with changed FirstValue before two LeaveAllTime\n");
        }
      }
      active_sid = g.sid; active_da = g.da;
    }
    if (!opened || h.sid_pub(0) != active_sid || !(h.decl_mask() & 1)) setup = false;
    // Keep the first moved ID declared for 500 ms: ample time for its
    // normal Join transmission before its withdrawal. Only time advances.
    if (iteration == 0) origin_ms += 500;
    if (slow) origin_ms += 1;
    h.gates.clear(); h.arms.clear(); h.mreqs.clear(); h.resps.clear();
    h.offered.clear(); h.decl_edges.clear();
  }
  printf("setup=%s opens=%d closes=%d historical_repeats=%d gap_violations=%d no_conflict_inputs=1 cfg_stream_id_unchanged=1 listener_ready=0 demand=PROBE_TX slow_control=%d\n",
         setup ? "PASS" : "FAIL", opens, closes, repeats, violations, int(slow));
  return !setup || !repeats ? 2 : violations ? 1 : 0;
}

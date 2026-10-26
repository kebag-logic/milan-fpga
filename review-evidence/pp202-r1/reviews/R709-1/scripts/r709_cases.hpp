// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes for issue #202 (round R709-1). Included after sid_cases.hpp
// in a disposable copy of tb/acmp_talker/sim_main.cpp; never committed.
// Expectations come from 05 F05.12 and IEEE 802.1Q-2018 35.2.2.8, not from
// the DUT.
struct R709 {
  int& checks;
  int& fails;
  static constexpr uint64_t UP  = 0xAB00000000000000ull;
  static constexpr uint64_t UP2 = 0xCD00000000000000ull;
  uint64_t rng = 0x9E3779B97F4A7C15ull;
  uint64_t next() { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

  // the last gate-open strobe for src in h.gates, or nullptr
  static const GateEv* last_open(const Hn& h, int src) {
    const GateEv* g = nullptr;
    for (const auto& e : h.gates) if (e.open && e.src == src) g = &e;
    return g;
  }

  // RP1: a declared source is disabled and re-enabled; the allocator (the
  // bench's default model, a fresh address per ALLOC_DA, legal on the 02
  // section 4.2 face after a RELEASE_DA) grants another DA. 35.2.2.8: the
  // same StreamID with a different FirstValue needs two LeaveAllTime after
  // the withdrawal. 05 F05.12: "a declared ID is not declared again with
  // another address".
  void disable_reenable(bool block_alloc) {
    Hn h;
    if (block_alloc) { h.block_count = N_SRC; h.block_base = da_pool(0); }
    h.configure_the_talker_and_release_reset(); h.run(400);
    h.d->now_ms_i = 1000;
    h.gates.clear(); h.resps.clear();
    CHECK(h.send(MT_PROBE, 3, C1, 0x900, L1, 8, FL_FC), "RP1 probe consumed");
    const GateEv* g0 = last_open(h, 3);
    CHECK(g0 != nullptr, "RP1 src3 declares on the probe");
    const uint64_t sid0 = g0 ? g0->sid : 0, da0 = g0 ? g0->da : 0;
    h.gates.clear(); h.resps.clear();
    h.d->cfg_src_en_i = 0xF7; h.run(200);
    CHECK(h.decl_mask() == 0 && !h.gates.empty() && !h.gates[0].open,
          "RP1 the disable withdraws src3");
    const uint32_t t_wd = h.d->now_ms_i;
    h.gates.clear();
    h.d->cfg_src_en_i = 0xFF; h.run(400);
    h.d->now_ms_i = 1500;                       // 0.5 s after the withdrawal
    h.resps.clear();
    CHECK(h.send(MT_PROBE, 3, C1, 0x901, L1, 8, FL_FC), "RP1 re-probe consumed");
    const GateEv* g1 = last_open(h, 3);
    printf("RP1[%s]: first decl sid %016llx da %012llx; after re-enable decl %s sid %016llx da %012llx at +%u ms\n",
           block_alloc ? "block" : "fresh",
           (unsigned long long)sid0, (unsigned long long)da0, g1 ? "yes" : "no",
           (unsigned long long)(g1 ? g1->sid : 0), (unsigned long long)(g1 ? g1->da : 0),
           g1 ? g1->ms - t_wd : 0u);
    const bool same_id_new_fv = g1 && g1->sid == sid0 && g1->da != da0
                                && (g1->ms - t_wd) < 20000u;
    CHECK(!same_id_new_fv,
          "RP1[%s] a declared Stream ID is not re-declared with another DA inside "
          "two LeaveAllTime of its withdrawal", block_alloc ? "block" : "fresh");
  }

  // RP2: the mover's OWN provisioned ID is the first candidate {UP, 8}: the
  // move must not take the withdrawn ID back.
  void own_id_is_first_candidate() {
    Hn h; h.sid_cfg[0] = UP | 0x0008u;
    h.configure_the_talker_and_release_reset(); h.run(400);
    h.set_lsn(0, LSN_READY);
    CHECK((h.decl_mask() & 1u) == 1u, "RP2 src0 declares");
    h.gates.clear();
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 0;
    h.tick(); h.run(200);
    const GateEv* g = last_open(h, 0);
    CHECK(g && g->sid != (UP | 0x0008u) && h.sid_pub(0) == g->sid,
          "RP2 a move never takes the withdrawn ID back (got %016llx)",
          (unsigned long long)(g ? g->sid : 0));
    CHECK(g && g->sid == (UP | 0x0009u), "RP2 the rule gives {UP, 9}");
  }

  // RP3: random provisioning with many collisions against the candidates,
  // two upper-48 values, every source declaring on a registered Listener;
  // random conflicts. After each move: the new ID differs from the withdrawn
  // one and from every other source's current ID, keeps the slot's upper 48
  // bits, src_stream_id_o names it, nobody else's ID changed, and PROBE_TX /
  // GET_TX_STATE answer it.
  void fuzz(int seeds, int moves) {
    int bad_distinct = 0, bad_withdrawn = 0, bad_upper = 0, bad_pub = 0,
        bad_others = 0, bad_answer = 0, no_decl = 0, total = 0;
    for (int seed = 1; seed <= seeds; ++seed) {
      rng = 0x9E3779B97F4A7C15ull * uint64_t(seed) + 1;
      Hn h;
      uint64_t cfg[N_SRC];
      for (;;) {
        for (int s = 0; s < N_SRC; ++s) {
          const uint64_t up = (next() % 4 == 0) ? UP2 : UP;
          const uint64_t r = next() % 10;
          const uint64_t lo = r < 7 ? 8 + next() % 24          // the first candidates
                            : r < 9 ? next() % 8               // the default {MAC, s}
                            : 0xFFF8 + next() % 8;             // near the wrap
          cfg[s] = up | lo;
        }
        bool dup = false;
        for (int a = 0; a < N_SRC; ++a)
          for (int b = a + 1; b < N_SRC; ++b) if (cfg[a] == cfg[b]) dup = true;
        if (!dup) break;
      }
      for (int s = 0; s < N_SRC; ++s) h.sid_cfg[s] = cfg[s];
      h.configure_the_talker_and_release_reset(); h.run(400);
      for (int s = 0; s < N_SRC; ++s) h.set_lsn(s, LSN_READY);
      h.run(100);
      for (int k = 0; k < moves; ++k) {
        const int s = int(next() % N_SRC);
        uint64_t before[N_SRC];
        for (int j = 0; j < N_SRC; ++j) before[j] = h.sid_pub(j);
        h.gates.clear();
        h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = s;
        h.tick();
        const GateEv* g = nullptr;
        for (int i = 0; i < 400 && !g; ++i) { h.tick(); g = last_open(h, s); }
        ++total;
        if (!g) { ++no_decl; continue; }
        const uint64_t nsid = g->sid;
        if (nsid == before[s]) ++bad_withdrawn;
        for (int j = 0; j < N_SRC; ++j)
          if (j != s && (nsid == before[j] || nsid == h.sid_pub(j))) ++bad_distinct;
        if ((nsid >> 16) != (cfg[s] >> 16)) ++bad_upper;
        if (h.sid_pub(s) != nsid) ++bad_pub;
        for (int j = 0; j < N_SRC; ++j)
          if (j != s && h.sid_pub(j) != before[j]) ++bad_others;
        if (k % 16 == 0) {
          h.resps.clear();
          h.send(MT_PROBE, uint16_t(s), C1, uint16_t(0xA00 + k), L1, 8, FL_FC);
          const bool p_ok = h.resps.size() == 1 && h.resps[0].status == ST_OK
                            && h.resps[0].sid == nsid && h.resps[0].da == g->da;
          h.resps.clear();
          h.send(MT_GTXS, uint16_t(s), C1, uint16_t(0xB00 + k), 0, 0, 0);
          const bool t_ok = h.resps.size() == 1 && h.resps[0].sid == nsid
                            && h.resps[0].da == g->da;
          h.resps.clear();
          if (!p_ok || !t_ok) ++bad_answer;
        }
      }
    }
    printf("RP3: %d seeds, %d moves: no_decl %d withdrawn %d distinct %d upper %d pub %d others %d answer %d\n",
           seeds, total, no_decl, bad_withdrawn, bad_distinct, bad_upper, bad_pub,
           bad_others, bad_answer);
    CHECK(no_decl == 0, "RP3 every conflict re-declares at its grant (%d)", no_decl);
    CHECK(bad_withdrawn == 0, "RP3 no move keeps the withdrawn ID (%d)", bad_withdrawn);
    CHECK(bad_distinct == 0, "RP3 every move differs from every other current ID (%d)", bad_distinct);
    CHECK(bad_upper == 0, "RP3 every move keeps the slot's upper 48 bits (%d)", bad_upper);
    CHECK(bad_pub == 0, "RP3 src_stream_id_o names the declared ID (%d)", bad_pub);
    CHECK(bad_others == 0, "RP3 no other source's ID moves (%d)", bad_others);
    CHECK(bad_answer == 0, "RP3 PROBE_TX and GET_TX_STATE answer the new ID and DA (%d)", bad_answer);
  }
};

void r709_run(Hn& base) {
  R709 r{base.checks, base.fails};
  r.disable_reenable(false);
  r.disable_reenable(true);
  r.own_id_is_first_candidate();
  r.fuzz(40, 300);
}

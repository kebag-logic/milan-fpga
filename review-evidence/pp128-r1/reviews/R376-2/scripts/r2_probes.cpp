// SPDX-License-Identifier: CERN-OHL-W-2.0
// R376-2 reviewer probes for processor #128 at head cc7c911e. Builds against
// the donor's own talker bench (same BFM, documented ports only) and prints
// one verdict per probe plus a per-seed port-trace digest for differential
// comparison of candidate-equivalent mutants against the head RTL.
#define main upstream_suite_main_unused
#include "acmp_talker/sim_main.cpp"
#undef main
#include <cstdlib>
#include <map>
#include <string>

static int probe_fail = 0;
static void verdict(bool ok, const char* name, const char* what) {
  printf("%s %s: %s\n", ok ? "PROBE-PASS" : "PROBE-FAIL", name, what);
  if (!ok) ++probe_fail;
}

// ---- R376-1 probes, unchanged semantics --------------------------------
static void p1() {
  Hn h; h.configure_the_talker_and_release_reset(); h.run(400);
  const size_t n0 = h.mreqs.size();
  h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 3; h.tick();
  h.run(60);
  verdict(h.mreqs.size() == n0 + 1 && h.mreqs.back().src == 3
          && !h.mreqs.back().rel, "P1",
          "DA_OK conflict reallocates without waiting for the next round");
}
static void p2() {
  Hn h; h.grant_ok = false; h.configure_the_talker_and_release_reset();
  h.run(8 * (MAAP_TMO + 64));
  const size_t n0 = h.mreqs.size();
  h.grant_ok = true;
  h.d->cfg_src_en_i = 0xFF & ~(1u << 5); h.run(40);
  h.d->cfg_src_en_i = 0xFF; h.run(60);
  verdict(h.mreqs.size() == n0 + 1 && h.mreqs.back().src == 5,
          "P2", "re-enabled source allocates without waiting for the next round");
}
static void p3() {
  Hn h; h.configure_the_talker_and_release_reset(); h.run(400);
  h.auto_grant = false;
  h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 0; h.tick();
  h.run(60);
  h.d->cfg_src_en_i = 0xFF & ~(1u << 1); h.run(60);
  const int rel_before = h.offers_rel;
  h.resps.clear();
  verdict(h.send(MT_GTXS, 2, C1, 0x77, 0, 0, 0), "P3-seed", "seed command consumed");
  h.d->txn_valid_i = 1;
  h.inject_rsp(true, da_pool(40));
  const size_t r0 = h.resps.size();
  for (int i = 0; i < 4 * (MAAP_TMO + 64); ++i) h.tick();
  h.d->txn_valid_i = 0;
  verdict(h.resps.size() > r0 + 20, "P3a", "commands kept being answered");
  verdict(h.offers_rel == rel_before + 1, "P3b",
          "the owed release is offered while commands are continuous");
}
static void p5() {
  Hn h; h.auto_grant = false; h.configure_the_talker_and_release_reset();
  h.run(200);
  bool ok = h.mreqs.size() == 1;
  for (int k = 0; k < 3; ++k) {
    h.resps.clear();
    const bool took = h.send(MT_GTXS, 1 + k, C1, 0x90 + k, 0, 0, 0);
    ok = ok && took && h.last_send_cyc <= MAAP_TMO + 64 && h.resps.size() == 1;
  }
  verdict(ok, "P5", "three consecutive commands served while an accepted "
          "allocation is unanswered and retries are pending");
}
static void p4_behavior() {
  Hn h; h.grant_ok = false; h.configure_the_talker_and_release_reset();
  h.run(8 * (MAAP_TMO + 64));
  const size_t n0 = h.mreqs.size();
  h.resps.clear();
  const bool took = h.send(MT_PROBE, 0, C1, 0x44, L1, 8, FL_FC);
  h.run(4000);
  printf("BEHAVIOR P4: probe consumed=%d status=%d; ALLOC_DA requests caused "
         "within 4000 cycles of the same round = %zu\n", int(took),
         h.resps.empty() ? -1 : int(h.resps[0].status), h.mreqs.size() - n0);
  h.d->now_ms_i += 100; h.run(8 * (MAAP_TMO + 64));
  printf("BEHAVIOR P4: after one T-ACMP-DA-RETRY round, total new ALLOC_DA "
         "requests = %zu\n", h.mreqs.size() - n0);
}

// ---- new in R376-2 -------------------------------------------------------
// P7: absent allocator (ready tied low), the millisecond input held inside
// one round. 05 6bis: "One attempt per source per round"; tb README J: "a
// later retry round re-offers". Count offers (rising maap_req_valid_o).
static void p7() {
  Hn h; h.configure_the_talker_and_release_reset();
  h.d->maap_req_ready_i = 0;
  h.run(12 * (MAAP_TMO + 64));
  const int first = h.offers;
  h.run(12 * (MAAP_TMO + 64));
  const int same_round = h.offers - first;
  h.d->now_ms_i += 100; h.run(12 * (MAAP_TMO + 64));
  const int next_round = h.offers - first - same_round;
  printf("BEHAVIOR P7: offers in first window=%d, further offers in the same "
         "round=%d, offers in the next round=%d\n", first, same_round, next_round);
  verdict(first == N_SRC && same_round == 0 && next_round == N_SRC, "P7",
          "absent allocator: one offer per enabled source per round");
}

// P9: absent allocator (ready tied low) and repeated listener demand inside
// one round. 05 6bis: "One attempt per source per round is allowed,
// including probe/listener-triggered requests"; RTL S_EV_MAAP comment: an
// abandoned offer is revisited by "the next paced retry round ... exactly as
// it does after a refused allocation". Count offers the probes cause.
static void p9() {
  Hn h; h.configure_the_talker_and_release_reset();
  h.d->maap_req_ready_i = 0;
  h.run(12 * (MAAP_TMO + 64));
  const int first = h.offers;
  for (int k = 0; k < 3; ++k) {
    h.resps.clear();
    (void)h.send(MT_PROBE, 0, C1, uint16_t(0x60 + k), L1, 8, FL_FC);
    h.run(2 * (MAAP_TMO + 64));
  }
  printf("BEHAVIOR P9: offers in first window=%d; offers caused by 3 same-round "
         "probes to src0 = %d\n", first, h.offers - first);
  verdict(first == N_SRC && h.offers == first, "P9",
          "absent allocator: same-round probes do not re-offer an abandoned source");
}

// P8: a PROBE_TX for one source must not create an allocation attempt for a
// different source (demand is per source).
static void p8() {
  Hn h; h.auto_grant = false; h.configure_the_talker_and_release_reset();
  h.d->cfg_src_en_i = 3; h.run(60);                  // src0 ALLOC accepted
  h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 0; h.tick();
  h.run(20);
  h.inject_rsp(true, 0x91e0f000beefULL); h.run(40);  // obsolete grant -> release
  h.inject_rsp(true, 0, true); h.run(40);            // release answered
  h.inject_rsp(false, 0); h.run(40);                 // src1 ALLOC refused
  const size_t n0 = h.mreqs.size();
  std::string before;
  for (auto& m : h.mreqs) before += std::to_string(m.src) + (m.rel ? "R " : "A ");
  (void)h.send(MT_PROBE, 1, C1, 0x55, L1, 8, FL_FC);  // demand for src1 only
  h.run(200);
  int src0_new = 0;
  for (size_t i = n0; i < h.mreqs.size(); ++i)
    if (h.mreqs[i].src == 0 && !h.mreqs[i].rel) ++src0_new;
  printf("BEHAVIOR P8: requests before the src1 probe: %s; new src0 ALLOC "
         "caused by a src1 probe inside the round = %d\n", before.c_str(), src0_new);
}

// ---- randomized differential run ----------------------------------------
// Drives every documented input at random (seeded), including exact-edge
// disable pulses and conflicts around accepts, variable response latency,
// silent accepts, ready stalls, probes, listener changes, PCP, expiries and
// time jumps across rounds. Prints a digest of every port output on every
// cycle, plus two safety invariants graded here:
//  I1 no SUCCESS PROBE/GET_TX_STATE answer and no gate-open ever carries a
//     DA that the allocator granted to a DIFFERENT source index;
//  I2 every presented command is consumed within P-MAAP-ACCEPT-CYC + 64.
struct Rng { uint64_t s; uint32_t next() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return uint32_t(s); } };

static void rand_run(uint64_t seed, int steps) {
  Hn h; h.auto_grant = false; Rng r{seed * 0x9E3779B97F4A7C15ULL + 1};
  h.configure_the_talker_and_release_reset();
  std::map<uint64_t, int> da_owner;       // granted DA -> source it was granted to
  struct Acc { int src; bool rel; uint32_t t0; };
  std::vector<Acc> fifo;                  // accepted requests awaiting an answer
  size_t seen_m = 0, seen_r = 0, seen_g = 0;
  int lat = 0; bool late = false;
  uint64_t digest = 1469598103934665603ULL;
  auto mix = [&](uint64_t v) { digest ^= v; digest *= 1099511628211ULL; };
  int i1 = 0, i2 = 0, cmds = 0, grants = 0, lates = 0;
  uint64_t next_da = 0x91e0f0100000ULL;
  auto drain = [&]() {
    for (; seen_m < h.mreqs.size(); ++seen_m) {
      fifo.push_back({h.mreqs[seen_m].src, h.mreqs[seen_m].rel, uint32_t(h.d->now_ms_i)});
      mix(0xA000u | unsigned(h.mreqs[seen_m].src) << 1 | unsigned(h.mreqs[seen_m].rel));
    }
    for (; seen_r < h.resps.size(); ++seen_r) {
      const Resp& p = h.resps[seen_r];
      if (p.status == ST_OK && p.da != 0) {
        auto it = da_owner.find(p.da);
        if (it == da_owner.end() || it->second != p.tuid) ++i1;
      }
      mix(p.mt); mix(p.status); mix(p.da); mix(p.tuid); mix(p.sid); mix(p.seq);
    }
    for (; seen_g < h.gates.size(); ++seen_g) {
      const GateEv& g = h.gates[seen_g];
      if (g.open) {
        auto it = da_owner.find(g.da);
        if (it == da_owner.end() || it->second != g.src) ++i1;
      }
      mix(g.open); mix(g.src); mix(g.da);
    }
  };
  auto tickd = [&]() {
    h.tick();
    drain();
    mix(h.d->txn_ready_o); mix(h.d->maap_req_valid_o); mix(h.d->maap_req_src_o);
    mix(h.d->maap_req_release_o); mix(h.d->declaring_o); mix(h.d->tmr_arm_valid_o);
    mix(h.d->tmr_arm_deadline_ms_o); mix(h.d->prng_draw_req_o);
    // allocator model: FIFO answers after 1..6 cycles; occasionally LATE,
    // i.e. only after P-MAAP-RSP-MS has elapsed since its accept
    if (!fifo.empty() && h.mrsp_cnt == 0) {
      if (lat == 0) { lat = 1 + int(r.next() % 6); late = (r.next() % 23) == 0; }
      const bool due = late ? (uint32_t(h.d->now_ms_i) - fifo.front().t0 > MAAP_RSP_MS)
                            : (--lat <= 0);
      if (due) {
        Acc q = fifo.front(); fifo.erase(fifo.begin());
        const bool ok = !q.rel && (r.next() % 3) != 0;
        uint64_t da = 0;
        if (ok) { da = next_da++; da_owner[da] = q.src; ++grants; }
        if (late) ++lates;
        h.inject_rsp(ok, da, q.rel);
        lat = 0; late = false;
      }
    }
  };
  for (int step = 0; step < steps; ++step) {
    const uint32_t a = r.next() % 100;
    if (a < 8) {                       // single-cycle disable pulse, or a hold
      const int s = int(r.next() % N_SRC);
      h.d->cfg_src_en_i ^= (1u << s);
      if (r.next() & 1) { tickd(); h.d->cfg_src_en_i ^= (1u << s); }
    } else if (a < 14) {
      h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = r.next() % N_SRC;
    } else if (a < 16) {
      h.d->srp_pcp_change_i = 1;
    } else if (a < 22) {
      const int s = int(r.next() % N_SRC);
      uint16_t v = h.d->srp_lsn_reg_state_i;
      v = uint16_t((v & ~(3u << (2 * s))) | ((r.next() & 3u) << (2 * s)));
      h.d->srp_lsn_reg_state_i = v;
    } else if (a < 26) {
      const int s = int(r.next() % N_SRC);
      h.d->tmr_exp_valid_i = 1; h.d->tmr_exp_slot_i = TMR_BASE + s;
      h.d->tmr_exp_owner_i = OWNER_BASE + s;
    } else if (a < 36) {
      h.d->now_ms_i += r.next() % 160;
    } else if (a < 40) {
      h.d->maap_req_ready_i = (r.next() % 4) != 0;
    } else if (a < 52) {
      const int s = int(r.next() % N_SRC);
      const int mt = (r.next() & 1) ? MT_PROBE : MT_GTXS;
      // send() drives the BFM's own tick; the allocator model resumes after
      // it (answers are only delayed). Accepts seen inside are folded in.
      const bool took = h.send(mt, uint16_t(s), C1, uint16_t(step), L1, 8, FL_FC);
      drain();
      ++cmds; if (!took || h.last_send_cyc > MAAP_TMO + 64) ++i2;
      mix(uint64_t(h.last_send_cyc));
    }
    const int n = 1 + int(r.next() % 12);
    for (int k = 0; k < n; ++k) tickd();
  }
  printf("TRACE seed=%llu digest=%016llx cmds=%d grants=%d late=%d I1_alias=%d I2_budget=%d\n",
         (unsigned long long)seed, (unsigned long long)digest, cmds, grants, lates, i1, i2);
  if (i1 || i2) ++probe_fail;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  p1(); p2(); p3(); p5(); p4_behavior(); p7(); p8(); p9();
  const int seeds = argc > 1 ? atoi(argv[1]) : 40;
  for (int s = 1; s <= seeds; ++s) rand_run(uint64_t(s), 3000);
  printf("%s: %d probe failures\n", probe_fail ? "PROBES-FAILED" : "PROBES-OK", probe_fail);
  return probe_fail ? 1 : 0;
}

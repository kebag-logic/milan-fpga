// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes for the #128 talker change. Builds against the donor's own
// talker bench (same BFM, same documented ports); prints one verdict per probe.
#define main upstream_suite_main_unused
#include "acmp_talker/sim_main.cpp"
#undef main

static int probe_fail = 0;
static void verdict(bool ok, const char* name, const char* what) {
  printf("%s %s: %s\n", ok ? "PROBE-PASS" : "PROBE-FAIL", name, what);
  if (!ok) ++probe_fail;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  {
    // P1: a conflict in the same retry round as the source's last attempt
    // starts a new acquisition at once (05 6bis "conflict start[s] a new
    // acquisition lifetime"; base behavior: DA_OK conflict reallocates now).
    Hn h; h.configure_the_talker_and_release_reset(); h.run(400);
    const size_t n0 = h.mreqs.size();
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 3; h.tick();
    h.run(60);
    verdict(h.mreqs.size() == n0 + 1 && h.mreqs.back().src == 3
            && !h.mreqs.back().rel, "P1",
            "DA_OK conflict reallocates without waiting for the next round");
  }
  {
    // P2: disable/re-enable in the same round as a refused attempt starts a
    // new acquisition at once (05 6bis "Initial enable ... start a new
    // acquisition lifetime"; base behavior: the enable edge allocates now).
    Hn h; h.grant_ok = false; h.configure_the_talker_and_release_reset();
    h.run(8 * (MAAP_TMO + 64));
    const size_t n0 = h.mreqs.size();
    h.grant_ok = true;
    h.d->cfg_src_en_i = 0xFF & ~(1u << 5); h.run(40);
    h.d->cfg_src_en_i = 0xFF; h.run(60);
    verdict(h.mreqs.size() == n0 + 1 && h.mreqs.back().src == 5,
            "P2", "re-enabled source allocates without waiting for the next round");
  }
  {
    // P3: an owed RELEASE_DA is served under continuous solicited commands
    // (05 6bis "Commands and pending events alternate when both are present").
    Hn h; h.configure_the_talker_and_release_reset(); h.run(400);
    h.auto_grant = false;
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 0; h.tick();
    h.run(60);                                   // src0 re-ALLOC accepted, unanswered
    h.d->cfg_src_en_i = 0xFF & ~(1u << 1); h.run(60);  // src1 owes a release
    const int rel_before = h.offers_rel;
    h.resps.clear();
    verdict(h.send(MT_GTXS, 2, C1, 0x77, 0, 0, 0), "P3-seed", "seed command consumed");
    h.d->txn_valid_i = 1;                         // continuous GET_TX_STATE
    h.inject_rsp(true, da_pool(40));
    const size_t r0 = h.resps.size();
    for (int i = 0; i < 4 * (MAAP_TMO + 64); ++i) h.tick();
    h.d->txn_valid_i = 0;
    verdict(h.resps.size() > r0 + 20, "P3a", "commands kept being answered");
    verdict(h.offers_rel == rel_before + 1, "P3b",
            "the owed release is offered while commands are continuous");
  }
  {
    // P5: an accepted ALLOC_DA sits unanswered (tracker busy) while other
    // sources have retry work pending. Consecutive solicited commands must
    // each be consumed within the documented P-MAAP-ACCEPT-CYC + 64 bound.
    Hn h; h.auto_grant = false; h.configure_the_talker_and_release_reset();
    h.run(200);                                  // src0 ALLOC accepted, unanswered
    bool ok = h.mreqs.size() == 1;
    for (int k = 0; k < 3; ++k) {
      h.resps.clear();
      const bool took = h.send(MT_GTXS, 1 + k, C1, 0x90 + k, 0, 0, 0);
      ok = ok && took && h.last_send_cyc <= MAAP_TMO + 64 && h.resps.size() == 1;
    }
    verdict(ok, "P5", "three consecutive commands served while an accepted "
            "allocation is unanswered and retries are pending");
  }
  {
    // P4 (behavior record, not graded): the parent pp_shadow [H] shape. The
    // allocator refuses (no block), a PROBE_TX arrives in the same retry
    // round as the refused startup attempt, and 4000 cycles pass with the
    // millisecond input unchanged. Count the ALLOC_DA requests the probe
    // causes. Base: the probe re-asks at once. Head: paced to the next round.
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
  printf("%s: %d probe failures\n", probe_fail ? "PROBES-FAILED" : "PROBES-OK", probe_fail);
  return probe_fail ? 1 : 0;
}

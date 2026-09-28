// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R377-2 P7): every pending-event class keeps its turn while
// commands are presented continuously (05 section 6bis: "Commands and pending
// events alternate when both are present"). Each effect is sampled BEFORE the
// command stream is released, so an event served only in an idle gap fails.
// Included after retry_cases.hpp in a scratch copy of sim_main.cpp.
struct R377EventClasses {
  int& checks;
  int& fails;
  void run_all();
  void one(int kind);
};

void R377EventClasses::one(int kind) {
  static const char* const names[4] = {"conflict", "pcp", "freshness", "listener"};
  Hn h; h.configure_the_talker_and_release_reset(); h.run(400);   // boot walk: 8 DAs
  h.resps.clear();
  CHECK(h.send(MT_PROBE, 1, C1, 0x501, L1, 8, FL_FC), "P7 %s seed probe", names[kind]);
  CHECK(h.decl_mask() == 0x02, "P7 %s src1 declaring before stimulus (0x%02x)",
        names[kind], h.decl_mask());
  if (kind == 2) {                       // move past the freshness window, drain the round
    h.d->now_ms_i = 100 + T_DAFRESH + 1; h.run(400);   // seed ping was at 100
    CHECK(h.decl_mask() == 0x02, "P7 freshness gate still open before expiry");
  }
  // seed a GET_TX_STATE record for src3, then hold it valid continuously
  CHECK(h.send(MT_GTXS, 3, C1, 0x777, 0, 0, 0), "P7 %s command seed", names[kind]);
  h.resps.clear();
  h.d->txn_valid_i = 1;
  h.run(8);
  switch (kind) {
    case 0: h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = 1; h.tick(); break;
    case 1: h.d->srp_pcp_change_i = 1; h.tick(); break;
    case 2: h.fire_expiry(1); break;
    default: {
      uint16_t v = h.d->srp_lsn_reg_state_i;
      v = uint16_t((v & ~(3u << 4)) | (unsigned(LSN_READY) << 4));   // src2 listener
      h.d->srp_lsn_reg_state_i = v; h.tick();
    }
  }
  h.run(4 * (MAAP_TMO + 64));
  const uint32_t mask = h.decl_mask();   // sampled with commands still presented
  const size_t served = h.resps.size();
  h.d->txn_valid_i = 0;
  const uint32_t want = (kind == 3) ? 0x06u : 0x00u;
  CHECK(served > 100, "P7 %s commands keep flowing (%zu)", names[kind], served);
  CHECK(mask == want, "P7 %s event served under continuous commands (gates 0x%02x want 0x%02x)",
        names[kind], mask, want);
}

void R377EventClasses::run_all() {
  for (int kind = 0; kind < 4; ++kind) one(kind);
}

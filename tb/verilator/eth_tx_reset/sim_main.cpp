// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_eth_tx_reset_model self-checking harness (AX42: extend the KL_link_guard
// sequenced eth reset to cover the PHY-side eth_tx/gtx path).
//
// Two identical DUTs share one TB-controlled eth_tx clock, one frame_start
// (the true system boundary) and one payload byte:
//   g = GUARDED  - receives the extended eth_rst (models ext_reset=self.eth_rst)
//   c = CONTROL  - eth_rst tied 0 (models the pre-fix build: eth_rst never
//                  reaches the PHY CRG). This is the negative control.
//
// The proof, in order:
//   1. both re-init clean on power-on (async reset while establishing state)
//   2. both frame in lockstep, tx_data latches, tx_en tracks the pointer
//   3. STOP the eth_tx clock mid-frame: both pointers freeze, both reset_less
//      tx_data registers HOLD their last value (no clock, no update)
//   4. assert the extended eth_rst on the GUARDED DUT WHILE THE CLOCK IS
//      STOPPED: its framing pointer re-inits to the boundary asynchronously
//      (the AX42 property); the reset_less tx_data is untouched; the CONTROL
//      pointer stays stale
//   5. restart the clock: guarded holds through the async-assert/sync-release,
//      then free-runs from the boundary; control resumes from its stale phase
//   6. drive several TRUE frame boundaries: the guarded (re-synced) framer
//      stays in sync forever (desync_err == 0); the control framer, offset by
//      the un-reset stop, latches a persistent misframe (desync_err == 1) and
//      never recovers = the silicon TX wedge the fix removes.

#include "VKL_eth_tx_reset_model.h"
#include "verilated.h"
#include <cstdio>

static VKL_eth_tx_reset_model *g;   // guarded (fix present)
static VKL_eth_tx_reset_model *c;   // control  (fix absent)
static int pass = 0, fail = 0;

// full eth_tx clock cycle for BOTH DUTs (0 -> 1). frame_start/data/por/ext are
// set by the caller before the tick and are common except ext_rst.
static void tick() {
  g->eth_tx_clk_i = 0; c->eth_tx_clk_i = 0; g->eval(); c->eval();
  g->eth_tx_clk_i = 1; c->eth_tx_clk_i = 1; g->eval(); c->eval();
}

// settle combinational + async-reset logic WITHOUT a clock edge (the clock
// stays parked at its last level - this is the "clock dead" evaluation path
// that must still propagate an async reset assertion).
static void settle() { g->eval(); c->eval(); g->eval(); c->eval(); }

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        (unsigned long long)got, (unsigned long long)want); }
}

// tick until the guarded pointer sits at the frame boundary (bp == 0), with
// frame_start deasserted so no boundary is consumed on the way there.
static void advance_g_to_boundary() {
  g->frame_start_i = 0; c->frame_start_i = 0;
  for (int i = 0; i < 64 && g->beat_ptr_o != 0; i++) tick();
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  g = new VKL_eth_tx_reset_model;
  c = new VKL_eth_tx_reset_model;

  // common defaults
  g->por_rst_i = 0; c->por_rst_i = 0;
  g->ext_rst_i = 0; c->ext_rst_i = 0;
  g->frame_start_i = 0; c->frame_start_i = 0;
  g->data_i = 0x00; c->data_i = 0x00;
  g->eth_tx_clk_i = 1; c->eth_tx_clk_i = 1;

  // -- 1. power-on: async-assert por, sync-release, land at boundary --------
  g->por_rst_i = 1; c->por_rst_i = 1; settle();
  ck("por async-assert g bp0", g->beat_ptr_o, 0);
  ck("por async-assert c bp0", c->beat_ptr_o, 0);
  tick(); tick();                       // hold reset a couple of clocks
  g->por_rst_i = 0; c->por_rst_i = 0;
  tick(); tick();                       // sync-release
  advance_g_to_boundary();
  ck("post-por g idle",  g->idle_o, 1);
  ck("post-por c idle",  c->idle_o, 1);
  ck("post-por g in-sync", g->desync_err_o, 0);
  ck("post-por c in-sync", c->desync_err_o, 0);

  // -- 2. frame in lockstep; latch a known payload -------------------------
  g->data_i = 0xA5; c->data_i = 0xA5;
  tick();                               // bp 0 -> 1, tx_data <- 0xA5
  tick();                               // bp 1 -> 2
  tick();                               // bp 2 -> 3  (mid-frame)
  ck("lockstep g bp3", g->beat_ptr_o, 3);
  ck("lockstep c bp3", c->beat_ptr_o, 3);
  ck("mid-frame g tx_en", g->tx_en_o, 1);
  ck("mid-frame c tx_en", c->tx_en_o, 1);
  ck("g tx_data latched", g->tx_data_o, 0xA5);
  ck("c tx_data latched", c->tx_data_o, 0xA5);

  // -- 3. STOP the eth_tx clock mid-frame ----------------------------------
  // (no tick() past here until step 5). Change data_i to prove the reset_less
  // register cannot follow a stopped clock.
  g->data_i = 0x5A; c->data_i = 0x5A;
  settle();
  ck("stopped g bp frozen", g->beat_ptr_o, 3);
  ck("stopped c bp frozen", c->beat_ptr_o, 3);
  ck("stopped g tx_data held", g->tx_data_o, 0xA5);   // reset_less holds, no clock
  ck("stopped c tx_data held", c->tx_data_o, 0xA5);

  // -- 4. assert the extended eth_rst on the GUARDED DUT, clock STILL dead --
  g->ext_rst_i = 1;                     // c->ext_rst_i stays 0 (negative control)
  settle();
  ck("AX42 async-assert with clock stopped: g bp re-init", g->beat_ptr_o, 0);
  ck("AX42 guarded now idle",            g->idle_o, 1);
  ck("control NOT reset: c bp stale",    c->beat_ptr_o, 3);
  ck("control still mid-frame",          c->idle_o, 0);
  // the eth reset must NOT disturb the reset_less data registers on either DUT
  ck("reset leaves g tx_data (reset_less)", g->tx_data_o, 0xA5);
  ck("reset leaves c tx_data (reset_less)", c->tx_data_o, 0xA5);

  // -- 5. restart the clock: hold ext_rst 2 clks, then sync-release --------
  tick();                               // ext still 1 -> g held at boundary
  tick();                               // ext still 1 -> g held at boundary
  ck("guarded held at boundary during hold", g->beat_ptr_o, 0);
  g->ext_rst_i = 0;                     // release
  tick(); tick();                       // 2-stage sync-release
  ck("guarded re-synced idle after release", g->idle_o, 1);
  // control advanced through the whole episode from its stale phase
  ck("control free-ran through episode (off-boundary phase)",
     (uint64_t)(c->beat_ptr_o != g->beat_ptr_o), 1);

  // -- 6. drive TRUE system boundaries; guard stays synced, control wedges --
  // frame_start is pulsed exactly when the GUARDED (re-synced) pointer is at
  // the boundary - that IS the system frame phase after the reinit sequence.
  for (int f = 0; f < 5; f++) {
    advance_g_to_boundary();
    g->frame_start_i = 1; c->frame_start_i = 1;
    // at this posedge: g.bp == 0 (in sync), c.bp != 0 (misframe latches)
    tick();
    g->frame_start_i = 0; c->frame_start_i = 0;
    ck("guarded in-sync at boundary", g->desync_err_o, 0);
  }
  ck("GUARDED never desynced (fix works)", g->desync_err_o, 0);
  ck("CONTROL latched persistent misframe (bug reproduced)", c->desync_err_o, 1);

  // control stays wedged for every subsequent boundary (sticky) ------------
  for (int f = 0; f < 3; f++) {
    advance_g_to_boundary();
    g->frame_start_i = 1; c->frame_start_i = 1;
    tick();
    g->frame_start_i = 0; c->frame_start_i = 0;
  }
  ck("guarded still clean",  g->desync_err_o, 0);
  ck("control still wedged",  c->desync_err_o, 1);

  // -- 7. recovery proof: apply the extended eth_rst (the fix) to BOTH DUTs -
  // as one sequenced episode - it clears the control wedge AND re-syncs both
  // pointers to a common boundary, so the previously-wedged control now frames
  // cleanly forever. (Resetting the control alone would clear the wedge but
  // land it on its own phase, not the system's - the reinit sequence holds
  // both sides for exactly this reason; here g defines the system phase.)
  ck("pre-recovery control still wedged", c->desync_err_o, 1);
  g->ext_rst_i = 1; c->ext_rst_i = 1; settle();
  ck("fix clears control pointer",   c->beat_ptr_o, 0);
  ck("fix clears control desync",    c->desync_err_o, 0);
  ck("guarded re-synced to boundary", g->beat_ptr_o, 0);
  tick(); tick();                       // hold both
  g->ext_rst_i = 0; c->ext_rst_i = 0;
  tick(); tick();                       // shared sync-release -> common phase
  for (int f = 0; f < 4; f++) {
    advance_g_to_boundary();            // g.bp == 0; c shares g's phase now
    g->frame_start_i = 1; c->frame_start_i = 1;
    tick();
    g->frame_start_i = 0; c->frame_start_i = 0;
  }
  ck("control recovered - in sync after the fix", c->desync_err_o, 0);
  ck("guarded still clean",                       g->desync_err_o, 0);

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  int rc = fail ? 1 : 0;
  delete g; delete c;
  return rc;
}

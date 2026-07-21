// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_link_guard self-checking harness. Built with shrunken timing
// (-GDEAD_CYC_C=64 -GSETTLE_CYC_C=256) so full bounce episodes run in
// microseconds of sim time.
//
// Covers: arm-on-first-transition inertness, rx and tx death detection,
// automatic reinit hold + clean-clock settle, mid-settle re-death (one
// episode = one bounce count), repeat bounces, manual reinit OR-path,
// freeze test hook, disable semantics, activity flag, status packing.

#include "VKL_link_guard.h"
#include "verilated.h"
#include <cstdio>

static VKL_link_guard *dut;
static int pass = 0, fail = 0;
static vluint64_t tcyc = 0;

// eth-clock models: toggle flips every N sys cycles (0 = frozen)
static int rx_period = 0, tx_period = 0;

static void tick() {
  if (rx_period && (tcyc % rx_period) == 0) dut->rx_tgl_i ^= 1;
  if (tx_period && (tcyc % tx_period) == 0) dut->tx_tgl_i ^= 1;
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  tcyc++;
}

static void run(int n) { for (int i = 0; i < n; i++) tick(); }

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        (unsigned long long)got, (unsigned long long)want); }
}

static const int DEAD = 64, SETTLE = 256;

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_link_guard;

  dut->rst_n = 0; dut->rx_tgl_i = 0; dut->tx_tgl_i = 0; dut->act_tgl_i = 0;
  dut->dis_i = 0; dut->freeze_i = 0; dut->man_reinit_i = 0;
  run(4); dut->rst_n = 1; run(4);

  // -- unarmed = inert (TB/no-PHY tops): alive, no reinit, link up ------
  run(3 * DEAD);
  ck("unarmed alive stat", dut->stat_o, 0x0003);
  ck("unarmed reinit",     dut->reinit_o, 0);
  ck("unarmed link_est",   dut->link_est_o, 1);

  // -- arm both clocks, stay RUN ---------------------------------------
  rx_period = 2; tx_period = 3;
  run(4 * DEAD);
  ck("armed RUN reinit",   dut->reinit_o, 0);
  ck("armed RUN alive",    dut->stat_o & 0x3F, 0x03);   // state 0, alive 11
  ck("armed link_est",     dut->link_est_o, 1);

  // -- rx death -> HOLD + reinit + bounce 1 ----------------------------
  rx_period = 0;
  run(DEAD + 8);
  ck("rx-death reinit",    dut->reinit_o, 1);
  ck("rx-death link_est",  dut->link_est_o, 0);
  ck("rx-death state",     (dut->stat_o >> 4) & 3, 1);  // HOLD_S
  ck("rx-death bounce",    dut->stat_o >> 16, 1);

  // -- clock back -> SETTLE holds, then releases -----------------------
  rx_period = 2;
  run(DEAD / 2);
  ck("settle still held",  dut->reinit_o, 1);
  ck("settle state",       (dut->stat_o >> 4) & 3, 2);  // SETTLE_S
  // mid-settle re-death: back to HOLD, same episode (no extra bounce)
  rx_period = 0;
  run(DEAD + 8);
  ck("re-death state",     (dut->stat_o >> 4) & 3, 1);
  ck("re-death bounce",    dut->stat_o >> 16, 1);
  rx_period = 2;
  run(SETTLE + DEAD + 16);
  ck("recovered reinit",   dut->reinit_o, 0);
  ck("recovered state",    (dut->stat_o >> 4) & 3, 0);
  ck("recovered link_est", dut->link_est_o, 1);

  // -- tx death is also a trigger; second episode counts ---------------
  tx_period = 0;
  run(DEAD + 8);
  ck("tx-death reinit",    dut->reinit_o, 1);
  ck("tx-death bounce",    dut->stat_o >> 16, 2);
  tx_period = 3;
  run(SETTLE + DEAD + 16);
  ck("tx-recover reinit",  dut->reinit_o, 0);

  // -- manual reinit OR-path -------------------------------------------
  dut->man_reinit_i = 1; run(2);
  ck("manual reinit",      dut->reinit_o, 1);
  dut->man_reinit_i = 0; run(2);
  ck("manual release",     dut->reinit_o, 0);

  // -- freeze test hook: fakes death, full sequence --------------------
  dut->freeze_i = 1;
  run(DEAD + 8);
  ck("freeze reinit",      dut->reinit_o, 1);
  ck("freeze flag",        (dut->stat_o >> 9) & 1, 1);
  ck("freeze bounce",      dut->stat_o >> 16, 3);
  dut->freeze_i = 0;
  run(SETTLE + DEAD + 16);
  ck("unfreeze recover",   dut->reinit_o, 0);

  // -- disable: drops the guard reset immediately ----------------------
  rx_period = 0;
  run(DEAD + 8);
  ck("pre-disable reinit", dut->reinit_o, 1);
  dut->dis_i = 1; run(2);
  ck("disabled reinit",    dut->reinit_o, 0);
  ck("disabled flag",      (dut->stat_o >> 8) & 1, 1);
  dut->dis_i = 0; rx_period = 2;
  run(SETTLE + 2 * DEAD + 16);
  ck("re-enable recover",  dut->reinit_o, 0);

  // -- activity flag ----------------------------------------------------
  ck("act idle",           (dut->stat_o >> 7) & 1, 0);
  dut->act_tgl_i ^= 1; run(4);
  ck("act recent",         (dut->stat_o >> 7) & 1, 1);

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  delete dut;
  return fail ? 1 : 0;
}

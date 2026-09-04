// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_aaf_latency_tap_bank pruned-build arm (ENABLE_P = 0).
//
// The pruned bank presents a STRUCTURAL zero: every LTAP word and the status
// rail read 0 whatever the observation points do. That is not a latency of
// zero, and the distinction is the reason this arm exists - a reader who
// cannot tell the two apart reports 0 ns end to end. The builder gate refuses
// to prune the taps in a configuration that keeps its probes; this arm proves
// the pruned shape is unambiguous rather than accidentally alive.
//
// It also anchors the anti-vacuity direction: the SAME stimulus drives real,
// non-zero deltas in the ENABLE_P = 1 build (sim_main.cpp), so a zero here is
// the parameter's doing and not a dead harness.

#include "VKL_aaf_latency_tap_bank.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>

// every one of the sixteen words plus the status rail must be zero
constexpr int kLtapWords = 16;      // the LTAP RO window; kLtapWords marks the status rail

namespace {

class TapBankPruneHarness {
 public:
  int run();

 private:
  void ck(const char *name, uint64_t got, uint64_t want);
  void quiet();
  void tick();
  void idle(int n);
  void aaf_tx_beat(bool last);
  void mac_rx_beat(bool last);
  int all_zero();

  void release_reset();
  void prove_tx_activity_leaves_the_window_zero();
  void prove_rx_activity_leaves_the_window_zero();
  void prove_min_rails_are_zero_not_railed_high();
  void prove_clear_and_enable_are_inert();

  VKL_aaf_latency_tap_bank *dut = nullptr;
  int pass = 0;
  int fail = 0;
};

void TapBankPruneHarness::ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        static_cast<unsigned long long>(got),
                        static_cast<unsigned long long>(want)); }
}

void TapBankPruneHarness::quiet() {
  dut->cap_pair_p_i = 0; dut->avtp_accept_p_i = 0;
  dut->aaf_tx_tvalid_i = 0; dut->aaf_tx_tready_i = 0; dut->aaf_tx_tlast_i = 0;
  dut->mac_tx_tvalid_i = 0; dut->mac_tx_tready_i = 0; dut->mac_tx_tlast_i = 0;
  dut->mac_rx_tvalid_i = 0; dut->mac_rx_tready_i = 0; dut->mac_rx_tlast_i = 0;
  dut->dpkt_tvalid_i = 0; dut->dpkt_tready_i = 0; dut->dpkt_tlast_i = 0;
  dut->render_tvalid_i = 0; dut->render_tready_i = 0; dut->render_tlast_i = 0;
}

void TapBankPruneHarness::tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  quiet();
}
void TapBankPruneHarness::idle(int n) { for (int i = 0; i < n; i++) tick(); }

void TapBankPruneHarness::aaf_tx_beat(bool last) {
  dut->aaf_tx_tvalid_i = 1; dut->aaf_tx_tready_i = 1; dut->aaf_tx_tlast_i = last;
  tick();
}
void TapBankPruneHarness::mac_rx_beat(bool last) {
  dut->mac_rx_tvalid_i = 1; dut->mac_rx_tready_i = 1; dut->mac_rx_tlast_i = last;
  tick();
}

int TapBankPruneHarness::all_zero() {
  for (int k = 0; k < kLtapWords; k++) if (dut->regs_o[k] != 0) return k;
  return dut->status_o == 0 ? -1 : kLtapWords;
}

void TapBankPruneHarness::release_reset() {
  quiet();
  dut->rst_n = 0; dut->en_i = 1; dut->clr_i = 0; dut->now_i = 0;
  idle(4);
  dut->rst_n = 1; idle(4);

  ck("pruned: zero out of reset", all_zero() == -1, 1);
}

// the same shape sim_main.cpp measures with: a TX chain and an RX chain
void TapBankPruneHarness::prove_tx_activity_leaves_the_window_zero() {
  dut->now_i = 0x1111;
  dut->cap_pair_p_i = 1; tick();
  idle(4);
  aaf_tx_beat(false); aaf_tx_beat(false); aaf_tx_beat(true);
  idle(5);
  dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 1; dut->mac_tx_tlast_i = 1; tick();
  idle(4);
  ck("pruned: TX activity leaves zero", all_zero() == -1, 1);
}

void TapBankPruneHarness::prove_rx_activity_leaves_the_window_zero() {
  dut->now_i = 0x3333;
  mac_rx_beat(false);
  idle(3);
  dut->avtp_accept_p_i = 1; tick();
  idle(6);
  dut->dpkt_tvalid_i = 1; dut->dpkt_tready_i = 1; dut->dpkt_tlast_i = 1; tick();
  idle(1);
  dut->render_tvalid_i = 1; dut->render_tready_i = 1; dut->render_tlast_i = 1; tick();
  idle(4);
  ck("pruned: RX activity leaves zero", all_zero() == -1, 1);
}

// the min rails are the sharpest tell: the measuring build rails them high
// out of reset, the pruned build must NOT
void TapBankPruneHarness::prove_min_rails_are_zero_not_railed_high() {
  ck("pruned: tx min d0 is zero, not 0xFFFF", dut->regs_o[3] & 0xFFFFu, 0u);
  ck("pruned: rx min d2 is zero, not 0xFFFF", dut->regs_o[15] & 0xFFFFu, 0u);
}

// clear and enable are inert in a pruned build
void TapBankPruneHarness::prove_clear_and_enable_are_inert() {
  dut->clr_i = 1; tick(); dut->clr_i = 0; idle(2);
  ck("pruned: clear leaves zero", all_zero() == -1, 1);
  dut->en_i = 0; idle(4);
  ck("pruned: disabled leaves zero", all_zero() == -1, 1);
}

int TapBankPruneHarness::run() {
  const milan::tb::Model<VKL_aaf_latency_tap_bank> model;
  dut = model.get();

  release_reset();
  prove_tx_activity_leaves_the_window_zero();
  prove_rx_activity_leaves_the_window_zero();
  prove_min_rails_are_zero_not_railed_high();
  prove_clear_and_enable_are_inert();

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  return fail ? 1 : 0;
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  TapBankPruneHarness harness;
  return harness.run();
}

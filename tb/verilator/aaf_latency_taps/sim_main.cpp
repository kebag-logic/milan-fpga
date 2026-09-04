// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_aaf_latency_taps self-checking harness (roadmap item-11). Built with a
// shrunken per-stage timeout (-GTIMEOUT_C=64) so the token-abort leg runs in
// microseconds of sim time.
//
// The module measures inter-stage deltas in free-running cycles: driving a
// stage-k pulse D cycles after stage-(k-1) makes the recorded delta EXACTLY D
// (cyc_r increments once per posedge, both pulses sample cyc on their edge).
// The module's last/min/max/samples/timeouts/epoch/status outputs are the
// values milan_datapath packs 1:1 into the LTAP CSR words (0x870..0x8B0).
//
// Covers: known-delta capture (TX + RX), min/max accumulation over samples,
// gPTP epoch latch at arm, TX/RX chain independence, in-flight status
// (active + awaited stage), stage-0-while-active ignored (single in-flight),
// per-stage timeout abort + re-arm, enable gating, and W1S stats clear.

#include "../../common/verilator_harness.hpp"
#include "VKL_aaf_latency_taps.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

// status_o packs {16'd0, rx_stage[2:0], rx_active, tx_stage[2:0], tx_active, 8'd0}.
constexpr int kStatusTxActiveBit = 8;
constexpr int kStatusTxStageLsb = 9;
constexpr int kStatusRxActiveBit = 12;
constexpr uint32_t kStageMask = 7;

// last/min/max each pack the three inter-stage deltas as 16-bit lanes.
constexpr int kDeltaBits = 16;
constexpr uint64_t kDeltaMask = 0xFFFF;

// Cycles reset is held, and the same span to settle after releasing it.
constexpr int kResetCycles = 4;
// Idle span past the per-stage guard the Makefile shrinks to -GTIMEOUT_C=64.
constexpr int kTimeoutIdleCycles = 80;
// All four stage-pulse bits asserted in a single cycle.
constexpr uint32_t kAllStagesMask = 0xF;

namespace {

// 16-bit slice out of a packed delta bus
uint64_t seg(uint64_t bus, int idx) { return (bus >> (kDeltaBits * idx)) & kDeltaMask; }

class LatencyTapsHarness {
 public:
  int run();

 private:
  void tick();
  void ck(const char *name, uint64_t got, uint64_t want);
  void idle(int n);
  void tx_pulse(int s);
  void rx_pulse(int s);
  void frame_tx(int d0, int d1, int d2, uint32_t nowv);
  void frame_rx(int d0, int d1, int d2, uint32_t nowv);

  void reset_and_check_fresh_rails();
  void measure_known_tx_deltas();
  void accumulate_min_max_over_second_tx_frame();
  void prove_rx_chain_independent_of_tx();
  void report_in_flight_status_and_awaited_stage();
  void ignore_stage0_edge_while_in_flight();
  void abort_and_rearm_on_per_stage_timeout();
  void freeze_measurement_while_disabled();
  void clear_stats_and_resume_measuring();
  void walk_same_cycle_stage_cascade();
  void complete_chain_from_all_stages_in_one_cycle();

  VKL_aaf_latency_taps *dut = nullptr;
  int pass = 0;
  int fail = 0;
};

void LatencyTapsHarness::tick() {
  dut->clk_i = 0;
  dut->eval();
  dut->clk_i = 1;
  dut->eval();
}

void LatencyTapsHarness::ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) {
    pass++;
    printf("[PASS] %s\n", name);
  } else {
    fail++;
    printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
           static_cast<unsigned long long>(got),
           static_cast<unsigned long long>(want));
  }
}

// one idle cycle with no stage edges
void LatencyTapsHarness::idle(int n) {
  dut->tx_stage_p_i = 0;
  dut->rx_stage_p_i = 0;
  for (int i = 0; i < n; i++) tick();
}
// pulse one TX / RX stage bit for exactly one cycle
void LatencyTapsHarness::tx_pulse(int s) {
  dut->tx_stage_p_i = 1u << s;
  tick();
  dut->tx_stage_p_i = 0;
}
void LatencyTapsHarness::rx_pulse(int s) {
  dut->rx_stage_p_i = 1u << s;
  tick();
  dut->rx_stage_p_i = 0;
}

// a full 4-stage TX frame with the three inter-stage deltas d0,d1,d2
void LatencyTapsHarness::frame_tx(int d0, int d1, int d2, uint32_t nowv) {
  dut->now_i = nowv;
  tx_pulse(0);
  idle(d0 - 1); tx_pulse(1);
  idle(d1 - 1); tx_pulse(2);
  idle(d2 - 1); tx_pulse(3);
}
void LatencyTapsHarness::frame_rx(int d0, int d1, int d2, uint32_t nowv) {
  dut->now_i = nowv;
  rx_pulse(0);
  idle(d0 - 1); rx_pulse(1);
  idle(d1 - 1); rx_pulse(2);
  idle(d2 - 1); rx_pulse(3);
}

void LatencyTapsHarness::reset_and_check_fresh_rails() {
  dut->rst_n = 0; dut->en_i = 1; dut->clr_i = 0;
  dut->now_i = 0; dut->tx_stage_p_i = 0; dut->rx_stage_p_i = 0;
  for (int i = 0; i < kResetCycles; i++) tick();
  dut->rst_n = 1; idle(kResetCycles);

  // -- fresh state: no samples, min rails read all-ones --------------------
  ck("init tx_samples",  dut->tx_samples_o, 0);
  ck("init tx_timeouts", dut->tx_timeouts_o, 0);
  ck("init tx_min d0",   seg(dut->tx_min_o, 0), 0xFFFF);
  ck("init tx_active",   (dut->status_o >> kStatusTxActiveBit) & 1, 0);
}

// -- TX frame A: known deltas (5,7,9), epoch 0x1111 ----------------------
void LatencyTapsHarness::measure_known_tx_deltas() {
  frame_tx(5, 7, 9, 0x1111);
  ck("A tx_last d0", seg(dut->tx_last_o, 0), 5);
  ck("A tx_last d1", seg(dut->tx_last_o, 1), 7);
  ck("A tx_last d2", seg(dut->tx_last_o, 2), 9);
  ck("A tx_min d0",  seg(dut->tx_min_o, 0), 5);
  ck("A tx_max d2",  seg(dut->tx_max_o, 2), 9);
  ck("A tx_samples", dut->tx_samples_o, 1);
  ck("A tx_epoch",   dut->tx_epoch_o, 0x1111);
  ck("A tx idle",    (dut->status_o >> kStatusTxActiveBit) & 1, 0);
}

// -- TX frame B: (3,11,4) -> last=B, min=elementwise-min, max=max --------
void LatencyTapsHarness::accumulate_min_max_over_second_tx_frame() {
  idle(3);
  frame_tx(3, 11, 4, 0x2222);
  ck("B tx_last d0", seg(dut->tx_last_o, 0), 3);
  ck("B tx_last d1", seg(dut->tx_last_o, 1), 11);
  ck("B tx_last d2", seg(dut->tx_last_o, 2), 4);
  ck("B tx_min d0",  seg(dut->tx_min_o, 0), 3);   // min(5,3)
  ck("B tx_min d1",  seg(dut->tx_min_o, 1), 7);   // min(7,11)
  ck("B tx_min d2",  seg(dut->tx_min_o, 2), 4);   // min(9,4)
  ck("B tx_max d0",  seg(dut->tx_max_o, 0), 5);   // max(5,3)
  ck("B tx_max d1",  seg(dut->tx_max_o, 1), 11);  // max(7,11)
  ck("B tx_max d2",  seg(dut->tx_max_o, 2), 9);   // max(9,4)
  ck("B tx_samples", dut->tx_samples_o, 2);
  ck("B tx_epoch",   dut->tx_epoch_o, 0x2222);
}

// -- RX chain is fully independent of TX ---------------------------------
void LatencyTapsHarness::prove_rx_chain_independent_of_tx() {
  idle(3);
  frame_rx(2, 4, 6, 0x3333);
  ck("RX rx_last d0", seg(dut->rx_last_o, 0), 2);
  ck("RX rx_last d1", seg(dut->rx_last_o, 1), 4);
  ck("RX rx_last d2", seg(dut->rx_last_o, 2), 6);
  ck("RX rx_samples", dut->rx_samples_o, 1);
  ck("RX rx_epoch",   dut->rx_epoch_o, 0x3333);
  ck("RX tx untouched", dut->tx_samples_o, 2);   // TX counters unchanged
}

// -- in-flight status: active + awaited stage index ----------------------
void LatencyTapsHarness::report_in_flight_status_and_awaited_stage() {
  idle(3);
  dut->now_i = 0x4444;
  tx_pulse(0);
  ck("flight active",  (dut->status_o >> kStatusTxActiveBit) & 1, 1);
  ck("flight stage=1", (dut->status_o >> kStatusTxStageLsb) & kStageMask, 1);
  idle(3); tx_pulse(1);
  ck("flight stage=2", (dut->status_o >> kStatusTxStageLsb) & kStageMask, 2);
  idle(3); tx_pulse(2);
  ck("flight stage=3", (dut->status_o >> kStatusTxStageLsb) & kStageMask, 3);
  idle(3); tx_pulse(3);
  ck("flight complete active", (dut->status_o >> kStatusTxActiveBit) & 1, 0);
  ck("flight samples", dut->tx_samples_o, 3);
  ck("flight last d0", seg(dut->tx_last_o, 0), 4);   // 1 + idle(3)
}

// -- single in-flight: a stage-0 edge mid-measurement is ignored ---------
void LatencyTapsHarness::ignore_stage0_edge_while_in_flight() {
  idle(3);
  dut->now_i = 0x5555;
  tx_pulse(0);                       // arm (epoch latches 0x5555 here)
  dut->now_i = 0xDEAD;               // if a re-arm wrongly took, epoch->0xDEAD
  idle(1); tx_pulse(0);              // spurious re-arm edge: must be ignored
  idle(1); tx_pulse(1);              // d0 = (2+1)+... measured from FIRST arm
  idle(5); tx_pulse(2);
  idle(5); tx_pulse(3);
  ck("ignore-rearm samples", dut->tx_samples_o, 4);
  ck("ignore-rearm epoch",   dut->tx_epoch_o, 0x5555);   // first arm's now, not re-arm
  ck("ignore-rearm last d0", seg(dut->tx_last_o, 0), 4); // 1+1+1+1 cycles to stage1
}

// -- per-stage timeout: token aborts, re-arms, no false sample -----------
void LatencyTapsHarness::abort_and_rearm_on_per_stage_timeout() {
  idle(3);
  uint32_t smp_before = dut->tx_samples_o;
  tx_pulse(0);
  idle(kTimeoutIdleCycles);          // > TIMEOUT_C(64): guard fires
  ck("timeout counted",  dut->tx_timeouts_o, 1);
  ck("timeout not sampled", dut->tx_samples_o, smp_before);
  ck("timeout re-armed inactive", (dut->status_o >> kStatusTxActiveBit) & 1, 0);
  // a clean frame after the abort still measures
  frame_tx(6, 6, 6, 0x6666);
  ck("post-timeout samples", dut->tx_samples_o, smp_before + 1);
  ck("post-timeout last d1", seg(dut->tx_last_o, 1), 6);
}

// -- enable gating: en=0 freezes measurement (stats preserved) -----------
void LatencyTapsHarness::freeze_measurement_while_disabled() {
  idle(3);
  uint32_t smp_en = dut->tx_samples_o;
  dut->en_i = 0;
  frame_tx(4, 4, 4, 0x7777);         // fully ignored while disabled
  ck("disabled no sample", dut->tx_samples_o, smp_en);
  ck("disabled inactive",  (dut->status_o >> kStatusTxActiveBit) & 1, 0);
  dut->en_i = 1;
  frame_tx(8, 8, 8, 0x8888);
  ck("re-enabled samples", dut->tx_samples_o, smp_en + 1);
  ck("re-enabled last d0", seg(dut->tx_last_o, 0), 8);
}

// -- W1C stats clear: everything zeroed, min rails back to all-ones ------
void LatencyTapsHarness::clear_stats_and_resume_measuring() {
  dut->clr_i = 1; idle(1); dut->clr_i = 0; idle(1);
  ck("clr tx_samples",  dut->tx_samples_o, 0);
  ck("clr tx_timeouts", dut->tx_timeouts_o, 0);
  ck("clr rx_samples",  dut->rx_samples_o, 0);
  ck("clr tx_last d1",  seg(dut->tx_last_o, 1), 0);
  ck("clr tx_max d1",   seg(dut->tx_max_o, 1), 0);
  ck("clr tx_min d1",   seg(dut->tx_min_o, 1), 0xFFFF);
  ck("clr tx_epoch",    dut->tx_epoch_o, 0);
  // measurement resumes cleanly after a clear
  frame_tx(10, 12, 14, 0x9999);
  ck("post-clr last d0", seg(dut->tx_last_o, 0), 10);
  ck("post-clr min d2",  seg(dut->tx_min_o, 2), 14);
  ck("post-clr samples", dut->tx_samples_o, 1);
}

// -- same-cycle cascade (2026-07-26 silicon find): a combinational hop ---
// (KL_pcm_route DEPKT->FABRIC_RENDER) pulses two stages in ONE cycle. The walk must
// consume both: measured delta on the first hop, 0-cycle on the second,
// sample completes, no timeout.
void LatencyTapsHarness::walk_same_cycle_stage_cascade() {
  idle(3);
  uint32_t smp_cas = dut->rx_samples_o;
  uint32_t tmo_cas = dut->rx_timeouts_o;
  dut->now_i = 0xAAAA;
  rx_pulse(0);
  idle(4); rx_pulse(1);                       // d0 = 5
  idle(2);
  dut->rx_stage_p_i = (1u << 2) | (1u << 3);  // DEPKT + FABRIC_RENDER same cycle
  tick();
  dut->rx_stage_p_i = 0;
  ck("cascade samples",   dut->rx_samples_o, smp_cas + 1);
  ck("cascade timeouts",  dut->rx_timeouts_o, tmo_cas);
  ck("cascade last d0",   seg(dut->rx_last_o, 0), 5);
  ck("cascade last d1",   seg(dut->rx_last_o, 1), 3);   // idle(2)+1
  ck("cascade last d2",   seg(dut->rx_last_o, 2), 0);   // same-cycle hop
  ck("cascade min d2",    seg(dut->rx_min_o, 2), 0);
  ck("cascade inactive",  (dut->status_o >> kStatusRxActiveBit) & 1, 0);
  // a normal spaced frame afterwards still measures cleanly
  frame_rx(3, 3, 3, 0xBBBB);
  ck("post-cascade samples", dut->rx_samples_o, smp_cas + 2);
  ck("post-cascade last d2", seg(dut->rx_last_o, 2), 3);
  ck("post-cascade max d2 kept", seg(dut->rx_max_o, 2) >= 3, 1);
}

// -- all-stages-one-cycle (arm cascade): chain completes instantly -------
void LatencyTapsHarness::complete_chain_from_all_stages_in_one_cycle() {
  idle(3);
  uint32_t smp_all = dut->tx_samples_o;
  dut->now_i = 0xCCCC;
  dut->tx_stage_p_i = kAllStagesMask;         // stages 0..3 in one cycle
  tick();
  dut->tx_stage_p_i = 0;
  ck("armcascade samples", dut->tx_samples_o, smp_all + 1);
  ck("armcascade epoch",   dut->tx_epoch_o, 0xCCCC);
  ck("armcascade last d0", seg(dut->tx_last_o, 0), 0);
  ck("armcascade last d2", seg(dut->tx_last_o, 2), 0);
  ck("armcascade inactive", (dut->status_o >> kStatusTxActiveBit) & 1, 0);
}

int LatencyTapsHarness::run() {
  const milan::tb::Model<VKL_aaf_latency_taps> model;
  dut = model.get();

  reset_and_check_fresh_rails();
  measure_known_tx_deltas();
  accumulate_min_max_over_second_tx_frame();
  prove_rx_chain_independent_of_tx();
  report_in_flight_status_and_awaited_stage();
  ignore_stage0_edge_while_in_flight();
  abort_and_rearm_on_per_stage_timeout();
  freeze_measurement_while_disabled();
  clear_stats_and_resume_measuring();
  walk_same_cycle_stage_cascade();
  complete_chain_from_all_stages_in_one_cycle();

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  return fail ? 1 : 0;
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  LatencyTapsHarness harness;
  return harness.run();
}

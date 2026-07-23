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

#include "VKL_aaf_latency_taps.h"
#include "verilated.h"
#include <cstdio>

static VKL_aaf_latency_taps *dut;
static int pass = 0, fail = 0;

static void tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
}

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        (unsigned long long)got, (unsigned long long)want); }
}

// one idle cycle with no stage edges
static void idle(int n) {
  dut->tx_stage_p_i = 0; dut->rx_stage_p_i = 0;
  for (int i = 0; i < n; i++) tick();
}
// pulse one TX / RX stage bit for exactly one cycle
static void tx_pulse(int s) { dut->tx_stage_p_i = 1u << s; tick(); dut->tx_stage_p_i = 0; }
static void rx_pulse(int s) { dut->rx_stage_p_i = 1u << s; tick(); dut->rx_stage_p_i = 0; }

// a full 4-stage TX frame with the three inter-stage deltas d0,d1,d2
static void frame_tx(int d0, int d1, int d2, uint32_t nowv) {
  dut->now_i = nowv;
  tx_pulse(0);
  idle(d0 - 1); tx_pulse(1);
  idle(d1 - 1); tx_pulse(2);
  idle(d2 - 1); tx_pulse(3);
}
static void frame_rx(int d0, int d1, int d2, uint32_t nowv) {
  dut->now_i = nowv;
  rx_pulse(0);
  idle(d0 - 1); rx_pulse(1);
  idle(d1 - 1); rx_pulse(2);
  idle(d2 - 1); rx_pulse(3);
}

// 16-bit slice out of a packed delta bus
static uint64_t seg(uint64_t bus, int idx) { return (bus >> (16 * idx)) & 0xFFFF; }

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_aaf_latency_taps;

  dut->rst_n = 0; dut->en_i = 1; dut->clr_i = 0;
  dut->now_i = 0; dut->tx_stage_p_i = 0; dut->rx_stage_p_i = 0;
  for (int i = 0; i < 4; i++) tick();
  dut->rst_n = 1; idle(4);

  // -- fresh state: no samples, min rails read all-ones --------------------
  ck("init tx_samples",  dut->tx_samples_o, 0);
  ck("init tx_timeouts", dut->tx_timeouts_o, 0);
  ck("init tx_min d0",   seg(dut->tx_min_o, 0), 0xFFFF);
  ck("init tx_active",   (dut->status_o >> 8) & 1, 0);

  // -- TX frame A: known deltas (5,7,9), epoch 0x1111 ----------------------
  frame_tx(5, 7, 9, 0x1111);
  ck("A tx_last d0", seg(dut->tx_last_o, 0), 5);
  ck("A tx_last d1", seg(dut->tx_last_o, 1), 7);
  ck("A tx_last d2", seg(dut->tx_last_o, 2), 9);
  ck("A tx_min d0",  seg(dut->tx_min_o, 0), 5);
  ck("A tx_max d2",  seg(dut->tx_max_o, 2), 9);
  ck("A tx_samples", dut->tx_samples_o, 1);
  ck("A tx_epoch",   dut->tx_epoch_o, 0x1111);
  ck("A tx idle",    (dut->status_o >> 8) & 1, 0);

  // -- TX frame B: (3,11,4) -> last=B, min=elementwise-min, max=max --------
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

  // -- RX chain is fully independent of TX ---------------------------------
  idle(3);
  frame_rx(2, 4, 6, 0x3333);
  ck("RX rx_last d0", seg(dut->rx_last_o, 0), 2);
  ck("RX rx_last d1", seg(dut->rx_last_o, 1), 4);
  ck("RX rx_last d2", seg(dut->rx_last_o, 2), 6);
  ck("RX rx_samples", dut->rx_samples_o, 1);
  ck("RX rx_epoch",   dut->rx_epoch_o, 0x3333);
  ck("RX tx untouched", dut->tx_samples_o, 2);   // TX counters unchanged

  // -- in-flight status: active + awaited stage index ----------------------
  idle(3);
  dut->now_i = 0x4444;
  tx_pulse(0);
  ck("flight active",  (dut->status_o >> 8) & 1, 1);
  ck("flight stage=1", (dut->status_o >> 9) & 7, 1);
  idle(3); tx_pulse(1);
  ck("flight stage=2", (dut->status_o >> 9) & 7, 2);
  idle(3); tx_pulse(2);
  ck("flight stage=3", (dut->status_o >> 9) & 7, 3);
  idle(3); tx_pulse(3);
  ck("flight complete active", (dut->status_o >> 8) & 1, 0);
  ck("flight samples", dut->tx_samples_o, 3);
  ck("flight last d0", seg(dut->tx_last_o, 0), 4);   // 1 + idle(3)

  // -- single in-flight: a stage-0 edge mid-measurement is ignored ---------
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

  // -- per-stage timeout: token aborts, re-arms, no false sample -----------
  idle(3);
  uint32_t smp_before = dut->tx_samples_o;
  tx_pulse(0);
  idle(80);                          // > TIMEOUT_C(64): guard fires
  ck("timeout counted",  dut->tx_timeouts_o, 1);
  ck("timeout not sampled", dut->tx_samples_o, smp_before);
  ck("timeout re-armed inactive", (dut->status_o >> 8) & 1, 0);
  // a clean frame after the abort still measures
  frame_tx(6, 6, 6, 0x6666);
  ck("post-timeout samples", dut->tx_samples_o, smp_before + 1);
  ck("post-timeout last d1", seg(dut->tx_last_o, 1), 6);

  // -- enable gating: en=0 freezes measurement (stats preserved) -----------
  idle(3);
  uint32_t smp_en = dut->tx_samples_o;
  dut->en_i = 0;
  frame_tx(4, 4, 4, 0x7777);         // fully ignored while disabled
  ck("disabled no sample", dut->tx_samples_o, smp_en);
  ck("disabled inactive",  (dut->status_o >> 8) & 1, 0);
  dut->en_i = 1;
  frame_tx(8, 8, 8, 0x8888);
  ck("re-enabled samples", dut->tx_samples_o, smp_en + 1);
  ck("re-enabled last d0", seg(dut->tx_last_o, 0), 8);

  // -- W1C stats clear: everything zeroed, min rails back to all-ones ------
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

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  delete dut;
  return fail ? 1 : 0;
}

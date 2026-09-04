// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_aaf_latency_tap_bank self-checking harness.
//
// The bank is the seam Rule 1 (Issue #249) cut out of milan_datapath: the
// datapath used to own the AXIS-to-stage-edge derivation, the uniform
// one-cycle stage-pulse delay and the LTAP CSR word order inline, next to
// twenty-one unrelated state groups. This harness grades that seam through
// the OBSERVATION POINTS - AXIS handshakes and pulses - not through the
// pre-derived stage vector the measurement core takes, which is graded by
// tb/verilator/aaf_latency_taps.
//
// The expectations are an INDEPENDENT ORACLE. Every word offset, field split
// and reserved half below is read from the LTAP register map (base 0x870,
// docs/reference/REGISTER_MAP.md), not from the packing expression in the
// RTL. Importing the DUT's own word order would make the test agree with any
// permutation of it.
//
// Three properties belong to this module and to nothing else, so each one
// carries an arm that fails if the responsibility is re-coupled into the
// parent:
//
//   RECOUPLE-1  in-frame tracking. SOF is the FIRST accepted beat of a frame,
//               not every accepted beat. A parent that re-derives the edge as
//               a bare tvalid&tready sees a start of frame on every beat.
//   RECOUPLE-2  uniform one-cycle stage-pulse delay. Every stage pulse is
//               registered once, so the core latches the epoch one cycle
//               after the observed edge. Dropping the register (or applying
//               it to only one chain) moves the epoch and the deltas.
//   RECOUPLE-3  CSR word order. Reserved halves stay zero and min/last/max
//               keep their documented positions; a swap is invisible to any
//               test that reads the words back through the same expression.
//
// Built with -GTIMEOUT_C=64 so the per-stage re-arm guard runs in
// microseconds of simulated time.

#include "VKL_aaf_latency_tap_bank.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>

// ---------------------------------------------------------------------------
// LTAP register map (base 0x870) - the independent oracle.
// 0x870 is LTAP_STATUS; the sixteen RO words start at 0x874 and read:
//   +0  tx_epoch                      +8  rx_epoch
//   +1  {tx_timeouts, tx_samples}     +9  {rx_timeouts, rx_samples}
//   +2  {tx_max d0,  tx_last d0}     +10  {rx_max d0,  rx_last d0}
//   +3  {reserved,   tx_min  d0}     +11  {reserved,   rx_min  d0}
//   +4/+5, +6/+7 repeat for d1, d2   +12..+15 repeat for d1, d2
// ---------------------------------------------------------------------------
constexpr int kWordsPerChain = 8;   // TX occupies +0..+7, RX +8..+15
constexpr int W_TX_EPOCH = 0;
constexpr int W_TX_COUNTS = 1;
constexpr int W_RX_EPOCH = 8;
constexpr int W_RX_COUNTS = 9;

constexpr int TX = 0;
constexpr int RX = 1;

namespace {

class TapBankHarness {
 public:
  int run();

 private:
  static int w_last_max(int chain, int d) { return chain * kWordsPerChain + 2 + 2 * d; }
  static int w_min(int chain, int d)      { return chain * kWordsPerChain + 3 + 2 * d; }

  static uint32_t lo(uint32_t v)  { return v & 0xFFFFu; }
  static uint32_t hi(uint32_t v)  { return (v >> 16) & 0xFFFFu; }

  void ck(const char *name, uint64_t got, uint64_t want);

  uint32_t word(int k)     { return dut->regs_o[k]; }

  uint32_t last_of(int chain, int d) { return lo(word(w_last_max(chain, d))); }
  uint32_t max_of(int chain, int d)  { return hi(word(w_last_max(chain, d))); }
  uint32_t min_of(int chain, int d)  { return lo(word(w_min(chain, d))); }
  uint32_t samples_of(int chain) { return lo(word(chain ? W_RX_COUNTS : W_TX_COUNTS)); }
  uint32_t epoch_of(int chain)   { return word(chain ? W_RX_EPOCH : W_TX_EPOCH); }

  // -------------------------------------------------------------------------
  // stimulus helpers - every one drives OBSERVATION POINTS only
  // -------------------------------------------------------------------------
  void quiet();
  void tick();
  void idle(int n);
  void aaf_tx_beat(bool last);
  void mac_rx_beat(bool last);
  void mac_tx_last();
  void dpkt_last();
  void render_last();
  void cap_pulse();
  void avtp_accept();
  void tx_frame(int gap_cap_sof, int beats, int gap_eof_mac);

  void release_reset();
  void read_fresh_state_in_documented_shape();
  void measure_tx_chain_through_observation_points();
  void measure_single_beat_frame();
  void prove_mid_frame_beat_is_not_a_start_of_frame();
  void prove_epoch_is_latched_after_the_observed_cap();
  void measure_rx_chain_in_the_upper_eight_words();
  void prove_min_last_max_keep_their_documented_halves();
  void prove_disabled_bank_advances_nothing();

  VKL_aaf_latency_tap_bank *dut = nullptr;
  int pass = 0;
  int fail = 0;
};

void TapBankHarness::ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        static_cast<unsigned long long>(got),
                        static_cast<unsigned long long>(want)); }
}

void TapBankHarness::quiet() {
  dut->cap_pair_p_i = 0; dut->avtp_accept_p_i = 0;
  dut->aaf_tx_tvalid_i = 0; dut->aaf_tx_tready_i = 0; dut->aaf_tx_tlast_i = 0;
  dut->mac_tx_tvalid_i = 0; dut->mac_tx_tready_i = 0; dut->mac_tx_tlast_i = 0;
  dut->mac_rx_tvalid_i = 0; dut->mac_rx_tready_i = 0; dut->mac_rx_tlast_i = 0;
  dut->dpkt_tvalid_i = 0; dut->dpkt_tready_i = 0; dut->dpkt_tlast_i = 0;
  dut->render_tvalid_i = 0; dut->render_tready_i = 0; dut->render_tlast_i = 0;
}

void TapBankHarness::tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  quiet();                       // every stimulus is a single-cycle event
}

void TapBankHarness::idle(int n) { for (int i = 0; i < n; i++) tick(); }

// one accepted beat on the AAF talker stream
void TapBankHarness::aaf_tx_beat(bool last) {
  dut->aaf_tx_tvalid_i = 1; dut->aaf_tx_tready_i = 1; dut->aaf_tx_tlast_i = last;
  tick();
}
// one accepted beat on the MAC RX stream
void TapBankHarness::mac_rx_beat(bool last) {
  dut->mac_rx_tvalid_i = 1; dut->mac_rx_tready_i = 1; dut->mac_rx_tlast_i = last;
  tick();
}
void TapBankHarness::mac_tx_last() {
  dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 1; dut->mac_tx_tlast_i = 1;
  tick();
}
void TapBankHarness::dpkt_last() {
  dut->dpkt_tvalid_i = 1; dut->dpkt_tready_i = 1; dut->dpkt_tlast_i = 1;
  tick();
}
void TapBankHarness::render_last() {
  dut->render_tvalid_i = 1; dut->render_tready_i = 1; dut->render_tlast_i = 1;
  tick();
}
void TapBankHarness::cap_pulse()  { dut->cap_pair_p_i = 1;    tick(); }
void TapBankHarness::avtp_accept(){ dut->avtp_accept_p_i = 1; tick(); }

// a complete TX measurement: cap, then an n-beat AAF frame, then MAC egress.
// gaps are chosen by the caller so the recorded deltas are known.
void TapBankHarness::tx_frame(int gap_cap_sof, int beats, int gap_eof_mac) {
  cap_pulse();
  idle(gap_cap_sof - 1);
  for (int b = 0; b < beats; b++) aaf_tx_beat(b == beats - 1);
  idle(gap_eof_mac - 1);
  mac_tx_last();
}

void TapBankHarness::release_reset() {
  quiet();
  dut->rst_n = 0; dut->en_i = 1; dut->clr_i = 0; dut->now_i = 0;
  idle(4);
  dut->rst_n = 1; idle(4);
}

// -- RECOUPLE-3: fresh state reads the documented shape -------------------
void TapBankHarness::read_fresh_state_in_documented_shape() {
  ck("init tx samples", samples_of(TX), 0);
  ck("init tx min d0 rails high", min_of(TX, 0), 0xFFFF);
  ck("init rx min d2 rails high", min_of(RX, 2), 0xFFFF);
  ck("init tx epoch", epoch_of(TX), 0u);
  for (int d = 0; d < 3; d++) {
    ck("init reserved half tx", hi(word(w_min(TX, d))), 0u);
    ck("init reserved half rx", hi(word(w_min(RX, d))), 0u);
  }
}

// -- TX chain through the observation points -----------------------------
// cap at t, SOF 5 cycles later, 4-beat frame (EOF at SOF+3), MAC 6 after.
// The bank delays every stage pulse one cycle, uniformly, so the deltas the
// core records are the OBSERVED gaps.
void TapBankHarness::measure_tx_chain_through_observation_points() {
  dut->now_i = 0x1111;
  tx_frame(/*gap_cap_sof=*/5, /*beats=*/4, /*gap_eof_mac=*/6);
  idle(2);
  ck("TX last d0 (cap->sof)",  last_of(TX, 0), 5);
  ck("TX last d1 (sof->eof)",  last_of(TX, 1), 3);
  ck("TX last d2 (eof->mac)",  last_of(TX, 2), 6);
  ck("TX samples", samples_of(TX), 1);
  ck("TX min d0 tracks", min_of(TX, 0), 5);
  ck("TX max d2 tracks", max_of(TX, 2), 6);
  ck("TX reserved half stays zero", hi(word(w_min(TX, 0))), 0u);
}

// -- single-beat frame: SOF and EOF are the SAME accepted beat -----------
void TapBankHarness::measure_single_beat_frame() {
  dut->now_i = 0x2222;
  tx_frame(/*gap_cap_sof=*/4, /*beats=*/1, /*gap_eof_mac=*/3);
  idle(2);
  ck("TX 1-beat last d0", last_of(TX, 0), 4);
  ck("TX 1-beat last d1 is zero", last_of(TX, 1), 0);
  ck("TX 1-beat last d2", last_of(TX, 2), 3);
  ck("TX samples after 2", samples_of(TX), 2);
  ck("TX min d1 now zero", min_of(TX, 1), 0);
  ck("TX max d1 keeps 3", max_of(TX, 1), 3);
}

// -- RECOUPLE-1: a mid-frame beat is NOT a start of frame ----------------
// Arm the chain in the middle of a frame. The next SOF the bank may report
// is the FIRST beat of the NEXT frame, so delta d0 spans to that frame.
// A parent that re-derives SOF as bare tvalid&tready reports the very next
// beat instead and records d0 = 1 rather than the nine cycles to frame Y.
void TapBankHarness::prove_mid_frame_beat_is_not_a_start_of_frame() {
  idle(8);
  uint32_t smp_before = samples_of(TX);
  dut->aaf_tx_tvalid_i = 1; dut->aaf_tx_tready_i = 1; dut->aaf_tx_tlast_i = 0;
  tick();                                   // beat 1 of frame X: a real SOF
  cap_pulse();                              // arm mid-frame (t = +1)
  aaf_tx_beat(false);                       // beat 2 - must NOT be a SOF
  aaf_tx_beat(false);                       // beat 3 - must NOT be a SOF
  aaf_tx_beat(true);                        // beat 4, tlast - closes frame X
  idle(5);                                  // gap before frame Y
  aaf_tx_beat(false);                       // frame Y beat 1 - the real SOF
  aaf_tx_beat(true);
  idle(2);
  mac_tx_last();
  idle(2);
  ck("RECOUPLE-1 mid-frame beats are not SOF", last_of(TX, 0), 9);
  ck("RECOUPLE-1 sample completed", samples_of(TX), smp_before + 1);
}

// -- RECOUPLE-2: the epoch is latched one cycle AFTER the observed cap ----
// now_i holds a decoy during the cap cycle and the real value on the next.
// With the uniform stage-pulse register the core arms on the second value.
void TapBankHarness::prove_epoch_is_latched_after_the_observed_cap() {
  idle(6);
  dut->now_i = 0xDEAD;                      // decoy, visible only at cap time
  cap_pulse();
  dut->now_i = 0xBEEF;                      // what a one-cycle delay latches
  idle(4);
  aaf_tx_beat(true);
  idle(3);
  mac_tx_last();
  idle(2);
  ck("RECOUPLE-2 epoch is the post-pulse value", epoch_of(TX), 0xBEEFu);
}

// -- RX chain is independent and packs into the upper eight words --------
void TapBankHarness::measure_rx_chain_in_the_upper_eight_words() {
  uint32_t tx_smp_guard = samples_of(TX);
  dut->now_i = 0x3333;
  mac_rx_beat(false);                       // RX SOF
  mac_rx_beat(true);                        // closes the frame; NOT a SOF
  idle(2);
  avtp_accept();                            // +4
  idle(6);
  dpkt_last();                              // +11, so d1 = 7
  idle(1);
  render_last();                            // +13, so d2 = 2
  idle(2);
  ck("RX last d0 (sof->accept)", last_of(RX, 0), 4);
  ck("RX last d1 (accept->depkt)", last_of(RX, 1), 7);
  ck("RX last d2 (depkt->fabric render)", last_of(RX, 2), 2);
  ck("RX samples", samples_of(RX), 1);
  ck("RX epoch", epoch_of(RX), 0x3333u);
  ck("RX traffic left TX samples alone", samples_of(TX), tx_smp_guard);
  ck("RX reserved half stays zero", hi(word(w_min(RX, 1))), 0u);
}

// -- RECOUPLE-3: min/last/max keep their documented halves ---------------
// A second, longer RX measurement must move last and max but not min.
void TapBankHarness::prove_min_last_max_keep_their_documented_halves() {
  uint32_t rx_min_d0 = min_of(RX, 0);
  dut->now_i = 0x4444;
  mac_rx_beat(false);                       // the closing tlast above re-armed
  mac_rx_beat(true);                        // this SOF, so d0 can span further
  idle(7);
  avtp_accept();                            // +9
  idle(1);
  dpkt_last();                              // +11
  idle(1);
  render_last();                            // +13
  idle(2);
  ck("RECOUPLE-3 last d0 moved", last_of(RX, 0), 9);
  ck("RECOUPLE-3 max d0 took the larger", max_of(RX, 0), 9);
  ck("RECOUPLE-3 min d0 kept the smaller", min_of(RX, 0), rx_min_d0);
  ck("RECOUPLE-3 reserved half still zero", hi(word(w_min(RX, 0))), 0u);
}

// -- enable gate: with en_i low nothing advances -------------------------
void TapBankHarness::prove_disabled_bank_advances_nothing() {
  uint32_t frozen_smp = samples_of(TX);
  uint32_t frozen_last = last_of(TX, 0);
  dut->en_i = 0;
  tx_frame(3, 2, 3);
  idle(4);
  ck("disabled: samples frozen", samples_of(TX), frozen_smp);
  ck("disabled: last frozen", last_of(TX, 0), frozen_last);
  dut->en_i = 1;
}

int TapBankHarness::run() {
  const milan::tb::Model<VKL_aaf_latency_tap_bank> model;
  dut = model.get();

  release_reset();

  read_fresh_state_in_documented_shape();
  measure_tx_chain_through_observation_points();
  measure_single_beat_frame();
  prove_mid_frame_beat_is_not_a_start_of_frame();
  prove_epoch_is_latched_after_the_observed_cap();
  measure_rx_chain_in_the_upper_eight_words();
  prove_min_last_max_keep_their_documented_halves();
  prove_disabled_bank_advances_nothing();

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  return fail ? 1 : 0;
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  TapBankHarness harness;
  return harness.run();
}

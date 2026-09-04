// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_mac_rmon_events - the missing link between "the MAC knows" and "the RMON
// counter counts". Proves, per lane:
//   * a supported lane emits EXACTLY one 1-cycle pulse per frame/error, in the
//     datapath clock domain, across an asynchronous clock ratio;
//   * a structurally unsupported lane is silent AND says so in cap_o;
//   * attached_i = 0 (no MAC at the boundary) zeroes BOTH events and cap, so a
//     stub build cannot be mistaken for a clean link;
//   * a MAC error counter that RESETS (link-guard reinit) emits nothing.
//
// Two shapes: default (MAC checks everything) and --nochk (the -G build with
// HAS_FCS_CHECK_P/HAS_ALIGN_CHECK_P/HAS_RX_ERR_FLAG_P = 0).
#include "VKL_mac_rmon_events.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstring>

// ethernet_events_t lane indices (the CSR 0x210 + 4n ABI). Plain integers,
// not an enum class: every use is a shift count or an array index.
constexpr int TX_ERROR_UNDERFLOW = 0;
constexpr int TX_FIFO_OVERFLOW   = 1;
constexpr int TX_FIFO_BAD_FRAME  = 2;
constexpr int TX_FIFO_GOOD_FRAME = 3;
constexpr int RX_ERROR_BAD_FRAME = 4;
constexpr int RX_ERROR_BAD_FCS   = 5;
constexpr int RX_FIFO_OVERFLOW   = 6;
constexpr int RX_FIFO_BAD_FRAME  = 7;
constexpr int RX_FIFO_GOOD_FRAME = 8;
constexpr int N_LANE             = 9;
constexpr const char* LANE[] = {"TX_ERROR_UNDERFLOW", "TX_FIFO_OVERFLOW",
  "TX_FIFO_BAD_FRAME", "TX_FIFO_GOOD_FRAME", "RX_ERROR_BAD_FRAME",
  "RX_ERROR_BAD_FCS", "RX_FIFO_OVERFLOW", "RX_FIFO_BAD_FRAME",
  "RX_FIFO_GOOD_FRAME"};

// ---- two asynchronous clocks: mac period 4 units, dp period 6 units --------
constexpr int kMacPeriodUnits = 4;   // mac clock period, in time units
constexpr int kMacFallUnit    = 2;   // the mac falling edge inside that period
constexpr int kDpPeriodUnits  = 6;   // dp clock period, in time units
constexpr int kDpFallUnit     = 3;   // the dp falling edge inside that period
constexpr int kSettleCycles   = 12;  // mac cycles for every CDC toggle to land

namespace {

//! The whole run: the two clocks, the dp-domain pulse tally, and the nine
//! phases that judge one build shape of KL_mac_rmon_events.
class MacRmonEventsHarness {
 public:
  explicit MacRmonEventsHarness(bool nochk_in) : nochk(nochk_in) {}

  int run();

 private:
  void ck(const char* w, long g, long e) {
    checks++;
    if (g != e) { fails++; printf("  [FAIL] %s got=%ld exp=%ld\n", w, g, e); }
    else        { printf("  [ ok ] %s=%ld\n", w, g); }
  }

  void unit() {
    t_units++;
    if (t_units % kMacPeriodUnits == 0)            dut->mac_clk_i = 1;
    if (t_units % kMacPeriodUnits == kMacFallUnit) dut->mac_clk_i = 0;
    if (t_units % kDpPeriodUnits  == 0)            dut->dp_clk_i  = 1;
    if (t_units % kDpPeriodUnits  == kDpFallUnit)  dut->dp_clk_i  = 0;
    dut->eval();
    if (dut->dp_clk_i && !prev_dp) {          // dp rising edge: sample events
      uint32_t ev = dut->events_o;
      for (int i = 0; i < N_LANE; i++) {
        int hi = (ev >> i) & 1;
        if (hi) { pulses[i]++; if (last_hi[i]) wide[i]++; }
        last_hi[i] = hi;
      }
    }
    prev_dp = dut->dp_clk_i;
  }
  //! advance exactly one mac clock period (one mac posedge, inputs pre-applied)
  void mac_cycle(int n = 1) { for (int k = 0; k < n * kMacPeriodUnits; k++) unit(); }

  void clear_tally() { memset(pulses, 0, sizeof(pulses)); memset(wide, 0, sizeof(wide)); }
  //! let every in-flight toggle synchroniser land in the dp domain
  void settle() { mac_cycle(kSettleCycles); }

  // ---- stimulus helpers (mac domain) ----------------------------------------
  void idle() {
    dut->mac_tx_tvalid_i = 0; dut->mac_tx_tready_i = 0; dut->mac_tx_tlast_i = 0;
    dut->mac_rx_tvalid_i = 0; dut->mac_rx_tready_i = 0; dut->mac_rx_tlast_i = 0;
    dut->mac_rx_err_i    = 0;
  }
  //! one TX frame of `beats` beats accepted at the MAC boundary
  void tx_frame(int beats) {
    for (int b = 0; b < beats; b++) {
      dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 1;
      dut->mac_tx_tlast_i  = (b == beats - 1);
      mac_cycle();
    }
    idle(); mac_cycle();
  }
  //! one RX frame of `beats` beats delivered, `err` = the MAC's bad-frame verdict
  void rx_frame(int beats, int err) {
    for (int b = 0; b < beats; b++) {
      dut->mac_rx_tvalid_i = 1; dut->mac_rx_tready_i = 1;
      dut->mac_rx_tlast_i  = (b == beats - 1);
      dut->mac_rx_err_i    = (b == beats - 1) ? err : 0;
      mac_cycle();
    }
    idle(); mac_cycle();
  }

  void hold_boundary_in_reset();
  void prove_unattached_boundary_is_silent();
  void prove_capability_mask_is_the_build();
  void prove_tx_good_frame_pulses_once_per_frame();
  void prove_unaccepted_beats_do_not_count();
  void prove_rx_good_and_bad_are_exclusive();
  void prove_error_counters_become_pulses();
  void prove_counter_reset_is_not_an_error();
  void prove_unsupported_lanes_stayed_silent();
  void prove_detach_stops_events_and_cap();

  bool nochk;                         // the --nochk build shape is under test
  VKL_mac_rmon_events* dut = nullptr;
  long checks = 0;
  long fails = 0;

  long t_units = 0;
  int  prev_dp = 0;
  long pulses[N_LANE] = {};           // dp-domain pulse tally per lane
  long wide[N_LANE] = {};             // lanes seen high on two consecutive dp edges
  int  last_hi[N_LANE] = {};
};

void MacRmonEventsHarness::hold_boundary_in_reset() {
  dut->mac_clk_i = 0; dut->dp_clk_i = 0;
  dut->mac_rst_n = 0; dut->dp_rst_n = 0;
  dut->attached_i = 0; dut->fcs_err_cnt_i = 0; dut->align_err_cnt_i = 0;
  idle();
  mac_cycle(6);
}

// ---- 1. stub boundary: no MAC attached -> cap 0 and no events ------------
void MacRmonEventsHarness::prove_unattached_boundary_is_silent() {
  dut->mac_rst_n = 1; dut->dp_rst_n = 1; mac_cycle(4);
  ck("[1a] cap_o = 0 while unattached", dut->cap_o, 0);
  clear_tally();
  tx_frame(4); rx_frame(4, 0); rx_frame(4, 1);
  dut->fcs_err_cnt_i = 3; dut->align_err_cnt_i = 5; settle();
  long any = 0; for (int i = 0; i < N_LANE; i++) any += pulses[i];
  ck("[1b] unattached: zero events on every lane", any, 0);
}

// ---- 2. attach: the capability mask is the parameters, not a wish -------
void MacRmonEventsHarness::prove_capability_mask_is_the_build() {
  dut->attached_i = 1;
  dut->fcs_err_cnt_i = 0; dut->align_err_cnt_i = 0;
  dut->mac_rst_n = 0; dut->dp_rst_n = 0; mac_cycle(4);
  dut->mac_rst_n = 1; dut->dp_rst_n = 1; mac_cycle(4);
  long exp_cap = (1 << TX_FIFO_GOOD_FRAME) | (1 << RX_FIFO_GOOD_FRAME);
  if (!nochk) exp_cap |= (1 << RX_ERROR_BAD_FCS) | (1 << RX_ERROR_BAD_FRAME)
                       | (1 << RX_FIFO_BAD_FRAME);
  ck("[2a] cap_o matches the build's real sources", dut->cap_o, exp_cap);
  // the four MAC-internal lanes are NEVER claimed, in either shape
  for (int l : {TX_ERROR_UNDERFLOW, TX_FIFO_OVERFLOW, TX_FIFO_BAD_FRAME, RX_FIFO_OVERFLOW}) {
    char b[96]; snprintf(b, sizeof b, "[2b] %s declared unsupported", LANE[l]);
    ck(b, (dut->cap_o >> l) & 1, 0);
  }
}

// ---- 3. TX good frame: one pulse per accepted tlast ----------------------
void MacRmonEventsHarness::prove_tx_good_frame_pulses_once_per_frame() {
  clear_tally();
  tx_frame(8); settle();
  ck("[3a] TX_FIFO_GOOD_FRAME = 1 per frame", pulses[TX_FIFO_GOOD_FRAME], 1);
  ck("[3b] the pulse is 1 dp cycle wide",      wide[TX_FIFO_GOOD_FRAME], 0);
  clear_tally();
  tx_frame(8); tx_frame(8); tx_frame(8); settle();
  ck("[3c] three frames -> three pulses", pulses[TX_FIFO_GOOD_FRAME], 3);
}

// ---- 4. no tlast / no tready must NOT count -----------------------------
void MacRmonEventsHarness::prove_unaccepted_beats_do_not_count() {
  clear_tally();
  for (int b = 0; b < 6; b++) {           // beats without tlast
    dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 1; dut->mac_tx_tlast_i = 0;
    mac_cycle();
  }
  idle();
  // tlast held with valid but NEVER accepted (ready low) - a stalled frame
  for (int b = 0; b < 6; b++) {
    dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 0; dut->mac_tx_tlast_i = 1;
    dut->mac_rx_tvalid_i = 1; dut->mac_rx_tready_i = 0; dut->mac_rx_tlast_i = 1;
    mac_cycle();
  }
  idle(); settle();
  ck("[4a] mid-frame beats do not count",     pulses[TX_FIFO_GOOD_FRAME], 0);
  ck("[4b] backpressured tlast does not count (TX)", pulses[TX_FIFO_GOOD_FRAME], 0);
  ck("[4c] backpressured tlast does not count (RX)", pulses[RX_FIFO_GOOD_FRAME], 0);
  ck("[4d] RX backpressure is NOT reported as overflow", pulses[RX_FIFO_OVERFLOW], 0);
}

// ---- 5. RX good vs RX bad frame are mutually exclusive -------------------
void MacRmonEventsHarness::prove_rx_good_and_bad_are_exclusive() {
  clear_tally();
  rx_frame(9, 0); settle();
  ck("[5a] clean RX frame -> GOOD_FRAME 1", pulses[RX_FIFO_GOOD_FRAME], 1);
  ck("[5b] clean RX frame -> BAD_FRAME 0",  pulses[RX_FIFO_BAD_FRAME], 0);
  clear_tally();
  rx_frame(9, 1); settle();
  if (nochk) {
    // no bad-frame flag on this MAC: the frame can only be reported delivered
    ck("[5c] flag-less MAC counts it good", pulses[RX_FIFO_GOOD_FRAME], 1);
    ck("[5d] flag-less MAC never claims BAD_FRAME", pulses[RX_FIFO_BAD_FRAME], 0);
  } else {
    ck("[5c] flagged RX frame -> BAD_FRAME 1", pulses[RX_FIFO_BAD_FRAME], 1);
    ck("[5d] flagged RX frame is NOT also good", pulses[RX_FIFO_GOOD_FRAME], 0);
  }
}

// ---- 6. MAC error counters -> pulses ------------------------------------
void MacRmonEventsHarness::prove_error_counters_become_pulses() {
  clear_tally();
  dut->fcs_err_cnt_i = 1; mac_cycle(2);
  dut->fcs_err_cnt_i = 2; mac_cycle(2);
  dut->align_err_cnt_i = 1; settle();
  ck("[6a] FCS counter +2 -> 2 BAD_FCS pulses",
     pulses[RX_ERROR_BAD_FCS], nochk ? 0 : 2);
  ck("[6b] preamble counter +1 -> 1 BAD_FRAME pulse",
     pulses[RX_ERROR_BAD_FRAME], nochk ? 0 : 1);
}

// ---- 7. a counter RESET (MAC reinit) is not an error --------------------
void MacRmonEventsHarness::prove_counter_reset_is_not_an_error() {
  clear_tally();
  dut->fcs_err_cnt_i = 0; dut->align_err_cnt_i = 0; settle();
  ck("[7a] FCS counter reset emits nothing",      pulses[RX_ERROR_BAD_FCS], 0);
  ck("[7b] preamble counter reset emits nothing", pulses[RX_ERROR_BAD_FRAME], 0);
}

// ---- 8. the unsupported lanes stayed silent for the whole run -----------
void MacRmonEventsHarness::prove_unsupported_lanes_stayed_silent() {
  clear_tally();
  tx_frame(4); rx_frame(4, 1); dut->fcs_err_cnt_i = 9; settle();
  for (int l : {TX_ERROR_UNDERFLOW, TX_FIFO_OVERFLOW, TX_FIFO_BAD_FRAME, RX_FIFO_OVERFLOW}) {
    char b[96]; snprintf(b, sizeof b, "[8] %s structurally silent", LANE[l]);
    ck(b, pulses[l], 0);
  }
}

// ---- 9. detach at runtime: events stop, cap drops ------------------------
void MacRmonEventsHarness::prove_detach_stops_events_and_cap() {
  dut->attached_i = 0; mac_cycle(2);
  ck("[9a] cap_o returns to 0 on detach", dut->cap_o, 0);
  clear_tally();
  tx_frame(4); rx_frame(4, 0); settle();
  long any2 = 0; for (int i = 0; i < N_LANE; i++) any2 += pulses[i];
  ck("[9b] detached boundary emits nothing", any2, 0);
}

int MacRmonEventsHarness::run() {
  printf("== KL_mac_rmon_events (%s) ==\n", nochk ? "no MAC checks" : "full MAC");

  const milan::tb::Model<VKL_mac_rmon_events> model;
  dut = model.get();                    // the file's observing pointer
  hold_boundary_in_reset();

  prove_unattached_boundary_is_silent();
  prove_capability_mask_is_the_build();
  prove_tx_good_frame_pulses_once_per_frame();
  prove_unaccepted_beats_do_not_count();
  prove_rx_good_and_bad_are_exclusive();
  prove_error_counters_become_pulses();
  prove_counter_reset_is_not_an_error();
  prove_unsupported_lanes_stayed_silent();
  prove_detach_stops_events_and_cap();

  printf("mac_rmon(%s): %ld checks, %ld failures\n",
         nochk ? "nochk" : "full", checks, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  bool nochk = false;
  for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "--nochk")) nochk = true;

  MacRmonEventsHarness harness(nochk);
  return harness.run();
}

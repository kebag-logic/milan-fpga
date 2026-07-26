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
#include <cstdio>
#include <cstring>

// ethernet_events_t lane indices (the CSR 0x210 + 4n ABI)
enum {
  TX_ERROR_UNDERFLOW = 0, TX_FIFO_OVERFLOW, TX_FIFO_BAD_FRAME, TX_FIFO_GOOD_FRAME,
  RX_ERROR_BAD_FRAME, RX_ERROR_BAD_FCS, RX_FIFO_OVERFLOW, RX_FIFO_BAD_FRAME,
  RX_FIFO_GOOD_FRAME, N_LANE
};
static const char* LANE[] = {"TX_ERROR_UNDERFLOW", "TX_FIFO_OVERFLOW",
  "TX_FIFO_BAD_FRAME", "TX_FIFO_GOOD_FRAME", "RX_ERROR_BAD_FRAME",
  "RX_ERROR_BAD_FCS", "RX_FIFO_OVERFLOW", "RX_FIFO_BAD_FRAME",
  "RX_FIFO_GOOD_FRAME"};

static VKL_mac_rmon_events* dut;
static long checks = 0, fails = 0;
static void ck(const char* w, long g, long e) {
  checks++;
  if (g != e) { fails++; printf("  [FAIL] %s got=%ld exp=%ld\n", w, g, e); }
  else        { printf("  [ ok ] %s=%ld\n", w, g); }
}

// ---- two asynchronous clocks: mac period 4 units, dp period 6 units --------
static long  t_units = 0;
static int   prev_dp = 0;
static long  pulses[N_LANE];        // dp-domain pulse tally per lane
static long  wide[N_LANE];          // lanes seen high on two consecutive dp edges
static int   last_hi[N_LANE];

static void unit() {
  t_units++;
  if (t_units % 4 == 0) dut->mac_clk_i = 1;
  if (t_units % 4 == 2) dut->mac_clk_i = 0;
  if (t_units % 6 == 0) dut->dp_clk_i  = 1;
  if (t_units % 6 == 3) dut->dp_clk_i  = 0;
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
static void mac_cycle(int n = 1) { for (int k = 0; k < n * 4; k++) unit(); }

static void clear_tally() { memset(pulses, 0, sizeof(pulses)); memset(wide, 0, sizeof(wide)); }
//! let every in-flight toggle synchroniser land in the dp domain
static void settle() { mac_cycle(12); }

// ---- stimulus helpers (mac domain) ----------------------------------------
static void idle() {
  dut->mac_tx_tvalid_i = 0; dut->mac_tx_tready_i = 0; dut->mac_tx_tlast_i = 0;
  dut->mac_rx_tvalid_i = 0; dut->mac_rx_tready_i = 0; dut->mac_rx_tlast_i = 0;
  dut->mac_rx_err_i    = 0;
}
//! one TX frame of `beats` beats accepted at the MAC boundary
static void tx_frame(int beats) {
  for (int b = 0; b < beats; b++) {
    dut->mac_tx_tvalid_i = 1; dut->mac_tx_tready_i = 1;
    dut->mac_tx_tlast_i  = (b == beats - 1);
    mac_cycle();
  }
  idle(); mac_cycle();
}
//! one RX frame of `beats` beats delivered, `err` = the MAC's bad-frame verdict
static void rx_frame(int beats, int err) {
  for (int b = 0; b < beats; b++) {
    dut->mac_rx_tvalid_i = 1; dut->mac_rx_tready_i = 1;
    dut->mac_rx_tlast_i  = (b == beats - 1);
    dut->mac_rx_err_i    = (b == beats - 1) ? err : 0;
    mac_cycle();
  }
  idle(); mac_cycle();
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  bool nochk = false;
  for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "--nochk")) nochk = true;
  printf("== KL_mac_rmon_events (%s) ==\n", nochk ? "no MAC checks" : "full MAC");

  dut = new VKL_mac_rmon_events;
  dut->mac_clk_i = 0; dut->dp_clk_i = 0;
  dut->mac_rst_n = 0; dut->dp_rst_n = 0;
  dut->attached_i = 0; dut->fcs_err_cnt_i = 0; dut->align_err_cnt_i = 0;
  idle();
  mac_cycle(6);

  // ---- 1. stub boundary: no MAC attached -> cap 0 and no events ------------
  dut->mac_rst_n = 1; dut->dp_rst_n = 1; mac_cycle(4);
  ck("[1a] cap_o = 0 while unattached", dut->cap_o, 0);
  clear_tally();
  tx_frame(4); rx_frame(4, 0); rx_frame(4, 1);
  dut->fcs_err_cnt_i = 3; dut->align_err_cnt_i = 5; settle();
  long any = 0; for (int i = 0; i < N_LANE; i++) any += pulses[i];
  ck("[1b] unattached: zero events on every lane", any, 0);

  // ---- 2. attach: the capability mask is the parameters, not a wish -------
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

  // ---- 3. TX good frame: one pulse per accepted tlast ----------------------
  clear_tally();
  tx_frame(8); settle();
  ck("[3a] TX_FIFO_GOOD_FRAME = 1 per frame", pulses[TX_FIFO_GOOD_FRAME], 1);
  ck("[3b] the pulse is 1 dp cycle wide",      wide[TX_FIFO_GOOD_FRAME], 0);
  clear_tally();
  tx_frame(8); tx_frame(8); tx_frame(8); settle();
  ck("[3c] three frames -> three pulses", pulses[TX_FIFO_GOOD_FRAME], 3);

  // ---- 4. no tlast / no tready must NOT count -----------------------------
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

  // ---- 5. RX good vs RX bad frame are mutually exclusive -------------------
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

  // ---- 6. MAC error counters -> pulses ------------------------------------
  clear_tally();
  dut->fcs_err_cnt_i = 1; mac_cycle(2);
  dut->fcs_err_cnt_i = 2; mac_cycle(2);
  dut->align_err_cnt_i = 1; settle();
  ck("[6a] FCS counter +2 -> 2 BAD_FCS pulses",
     pulses[RX_ERROR_BAD_FCS], nochk ? 0 : 2);
  ck("[6b] preamble counter +1 -> 1 BAD_FRAME pulse",
     pulses[RX_ERROR_BAD_FRAME], nochk ? 0 : 1);

  // ---- 7. a counter RESET (MAC reinit) is not an error --------------------
  clear_tally();
  dut->fcs_err_cnt_i = 0; dut->align_err_cnt_i = 0; settle();
  ck("[7a] FCS counter reset emits nothing",      pulses[RX_ERROR_BAD_FCS], 0);
  ck("[7b] preamble counter reset emits nothing", pulses[RX_ERROR_BAD_FRAME], 0);

  // ---- 8. the unsupported lanes stayed silent for the whole run -----------
  clear_tally();
  tx_frame(4); rx_frame(4, 1); dut->fcs_err_cnt_i = 9; settle();
  for (int l : {TX_ERROR_UNDERFLOW, TX_FIFO_OVERFLOW, TX_FIFO_BAD_FRAME, RX_FIFO_OVERFLOW}) {
    char b[96]; snprintf(b, sizeof b, "[8] %s structurally silent", LANE[l]);
    ck(b, pulses[l], 0);
  }

  // ---- 9. detach at runtime: events stop, cap drops ------------------------
  dut->attached_i = 0; mac_cycle(2);
  ck("[9a] cap_o returns to 0 on detach", dut->cap_o, 0);
  clear_tally();
  tx_frame(4); rx_frame(4, 0); settle();
  long any2 = 0; for (int i = 0; i < N_LANE; i++) any2 += pulses[i];
  ck("[9b] detached boundary emits nothing", any2, 0);

  printf("mac_rmon(%s): %ld checks, %ld failures\n",
         nochk ? "nochk" : "full", checks, fails);
  return fails ? 1 : 0;
}

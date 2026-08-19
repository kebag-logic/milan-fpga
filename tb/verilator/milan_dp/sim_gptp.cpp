// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The GPTP_PLANE_EN_P=1 elaboration smoke (issue #114): the option-ON
// datapath builds, and the plane's boot Pdelay_Req emerges at the REAL
// MAC boundary through the real merge chain (gptp_ctl_mux -> adp_tx_mux)
// with NOTHING driven but clocks and resets -- the plane's own timer
// cadence is the stimulus. The deep protocol behavior lives in
// tb/verilator/gptp_shadow (the fabric slice) and the donor's own
// suites; THIS leg pins that the splice is real fabric in the real
// datapath, and that an option-OFF build stays byte-identical
// elsewhere (the other nine legs).
//
// MILAN_CLK_FREQ_HZ=2 MHz for this leg so the 1200 ms boot cadence
// fires within a runnable window; the ucode hex is generated for the
// same clock (see the Makefile rule).

#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "Vmilan_datapath.h"

static int checks = 0, fails = 0;
static void expect(const char *what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("FAIL %-30s got %016llx exp %016llx\n", what,
           (unsigned long long)got, (unsigned long long)exp);
  }
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  Vmilan_datapath *dut = new Vmilan_datapath;

  dut->axis_resetn = 0;
  dut->gtx_resetn = 0;
  dut->m_axis_mac_tx_tready = 1;
  for (int i = 0; i < 16; i++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
  }
  dut->axis_resetn = 1;
  dut->gtx_resetn = 1;

  // scan the MAC boundary for the plane's boot Pdelay_Req: an 0x88F7
  // frame whose transportSpecific|msgType byte is 0x12
  bool seen_pdreq = false;
  bool seen_ann = false;
  int beat = 0;
  std::vector<uint8_t> frame;
  for (uint64_t n = 0; n < 12000000ull; n++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
      uint64_t d = dut->m_axis_mac_tx_tdata;
      for (int i = 0; i < 8; i++)
        if ((dut->m_axis_mac_tx_tkeep >> i) & 1)
          frame.push_back((d >> (8 * i)) & 0xFF);
      beat++;
      if (dut->m_axis_mac_tx_tlast) {
        if (frame.size() > 14 && frame[12] == 0x88 && frame[13] == 0xF7) {
          if (frame[14] == 0x12) seen_pdreq = true;
          if (frame[14] == 0x1B) seen_ann = true;
        }
        frame.clear();
        beat = 0;
      }
    }
  }
  expect("the plane's Pdelay_Req reaches the MAC", seen_pdreq, 1);
  // no peer ever answers, so asCapable never rises: the announce
  // receipt timeout expires inside the scan window but the becgate
  // must HOLD -- an Announce here would mean an ungated become-master
  expect("no Announce without asCapable", seen_ann, 0);

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

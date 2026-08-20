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

static void tick(Vmilan_datapath *dut) {
  dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
  dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
}

static void axi_write(Vmilan_datapath *dut, uint16_t addr, uint32_t data) {
  dut->s_axi_awaddr = addr; dut->s_axi_awvalid = 1;
  dut->s_axi_wdata = data; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
  dut->s_axi_bready = 1;
  for (int n = 0; n < 2048; n++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    bool accepted = dut->s_axi_awready && dut->s_axi_wready;
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
    if (accepted) break;
  }
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
  for (int n = 0; n < 2048; n++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    bool valid = dut->s_axi_bvalid;
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
    if (valid) break;
  }
  dut->s_axi_bready = 0;
}

static uint32_t axi_read(Vmilan_datapath *dut, uint16_t addr) {
  dut->s_axi_araddr = addr; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
  for (int n = 0; n < 2048; n++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    bool accepted = dut->s_axi_arready;
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
    if (accepted) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t data = 0;
  for (int n = 0; n < 2048; n++) {
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval();
    bool valid = dut->s_axi_rvalid;
    if (valid) data = dut->s_axi_rdata;
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
    if (valid) break;
  }
  dut->s_axi_rready = 0;
  return data;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  Vmilan_datapath *dut = new Vmilan_datapath;

  dut->axis_resetn = 0;
  dut->gtx_resetn = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
  dut->s_axi_bready = dut->s_axi_rready = 0;
  dut->m_axis_mac_tx_tready = 1;
  for (int i = 0; i < 16; i++) tick(dut);
  dut->axis_resetn = 1;
  dut->gtx_resetn = 1;

  // The option is omitted from this elaboration: these are assertions about
  // the RTL default.  Before any peer answers, the engine's committed bank is
  // zero. Writes to the old software mirror remain accepted for ABI safety but
  // cannot change any live read or manufacture a healthy CLKV claim.
  expect("default-on VERSION", axi_read(dut, 0x004), 0x00020055);
  axi_write(dut, 0x624, 0x55667788); axi_write(dut, 0x628, 0x11223344);
  axi_write(dut, 0x6E4, 1234);
  axi_write(dut, 0x730, 0xDDEEFF00); axi_write(dut, 0x734, 0x99AABBCC);
  axi_write(dut, 0x778, 0x00000085); // sync + asCapable + live SW lease
  expect("fabric GM low overrides SW", axi_read(dut, 0x624), 0);
  expect("fabric GM high overrides SW", axi_read(dut, 0x628), 0);
  expect("fabric pdelay overrides SW", axi_read(dut, 0x6E4), 0);
  expect("fabric parent low overrides SW", axi_read(dut, 0x730), 0);
  expect("fabric parent high overrides SW", axi_read(dut, 0x734), 0);
  uint32_t clkv = axi_read(dut, 0x77C);
  expect("software lease cannot clear tu", clkv & 1, 1);
  expect("software sync claim hidden", (clkv >> 1) & 1, 0);
  expect("software lease fields hidden", (clkv >> 2) & 0x3FFF, 0);
  expect("software asCapable hidden", (clkv >> 16) & 1, 0);

  // scan the MAC boundary for the plane's boot Pdelay_Req: an 0x88F7
  // frame whose transportSpecific|msgType byte is 0x12
  bool seen_pdreq = false;
  bool seen_ann = false;
  int beat = 0;
  std::vector<uint8_t> frame;
  for (uint64_t n = 0; n < 12000000ull; n++) {
    tick(dut);
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

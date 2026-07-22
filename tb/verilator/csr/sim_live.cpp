/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * P11 indexed window against LIVE context engines (csr_win_live.sv):
 *   - lwSRP: window SEL/SID/CTRL commits provision REAL KL_lwsrp_ctx rows
 *     through the ctx req/gnt port (listener idx1 -> row 1, talker idx1 ->
 *     row 2); 0x85C reads the live row status {valid,dir,...} back through
 *     the grant path; CTRL.en=0 withdraws the row.
 *   - ACMP: a fast-connect CONNECT_RX binds KL_acmp_lstn_ctx context 1
 *     (record + explicit-sid policy); the window SID/DMAC words and the
 *     snap-latched STATE read the binding back through the tbl port.
 *   - index-0 SRP word = live hard alias of the flat 0x694 status.
 */

#include "Vcsr_win_live.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vcsr_win_live* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("  [FAIL] %-44s got=0x%llx exp=0x%llx\n", what,
           (unsigned long long)got, (unsigned long long)exp);
  } else {
    printf("  [ok]   %-44s = 0x%llx\n", what, (unsigned long long)got);
  }
}

static void posedge() {
  dut->clk_i = 1; dut->eval();
  dut->clk_i = 0; dut->eval();
}
static void run(int n) { for (int i = 0; i < n; i++) posedge(); }

static void axi_write(uint32_t a, uint32_t d) {
  dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
  dut->s_axi_wdata  = d; dut->s_axi_wvalid  = 1; dut->s_axi_wstrb = 0xF;
  dut->s_axi_bready = 1;
  for (int g = 0; g < 2048; ++g) {
    dut->eval();
    bool acc = dut->s_axi_awready && dut->s_axi_wready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
  for (int g = 0; g < 2048; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; posedge(); }
  posedge();
  dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint32_t a) {
  dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
  for (int g = 0; g < 2048; ++g) {
    dut->eval();
    bool acc = dut->s_axi_arready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t v = 0;
  for (int g = 0; g < 2048; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } posedge(); }
  posedge();
  dut->s_axi_rready = 0;
  return v;
}

// --------------------------------------------------------------- ACMP frames
static const uint64_t US_EID = 0x020000FFFE000003ULL;
static const uint64_t CT_EID = 0x680500FFFE0000AAULL;
static const uint64_t T1_EID = 0x020000FFFE000001ULL;

static void put_be(std::vector<uint8_t>& v, uint64_t x, int n) {
  for (int i = n-1; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}

// CONNECT_RX_COMMAND (msg 6) — explicit fast-connect sid + dmac for ctx1
static std::vector<uint8_t> acmp_connect(uint64_t sid, uint64_t talker,
                                         uint16_t luid, const uint8_t* dmac,
                                         uint16_t seq) {
  std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                            0xAA,0xBB,0xCC,0x00,0x00,0x01,
                            0x22,0xF0, 0xFC};
  f.push_back(6);                 // CONNECT_RX_COMMAND
  f.push_back(0);                 // status/cdl
  f.push_back(44);
  put_be(f, sid, 8);
  put_be(f, CT_EID, 8);
  put_be(f, talker, 8);
  put_be(f, US_EID, 8);
  put_be(f, 0, 2);                // talker_unique_id
  put_be(f, luid, 2);
  for (int i = 0; i < 6; i++) f.push_back(dmac ? dmac[i] : 0);
  put_be(f, 0, 2);                // connection_count
  put_be(f, seq, 2);
  put_be(f, 0, 2);                // flags
  put_be(f, 0, 2);                // vlan
  put_be(f, 0, 2);
  return f;
}

static void feed(const std::vector<uint8_t>& f) {
  int n = (int)f.size();
  for (int off = 0; off < n; off += 8) {
    uint64_t d = 0; uint8_t keep = 0;
    for (int l = 0; l < 8; l++)
      if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1u << l); }
    dut->rx_tvalid_i = 1;
    dut->rx_tdata_i  = d;
    dut->rx_tkeep_i  = keep;
    dut->rx_tlast_i  = (off + 8 >= n);
    posedge();
  }
  dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
  run(2);
}

enum {
  A_STRM_SEL=0x800, A_STRM_SNAP=0x804, A_SW_CTRL=0x810,
  A_SW_SID_LO=0x814, A_SW_SID_HI=0x818, A_SW_DMAC_LO=0x81C,
  A_SW_DMAC_HI=0x820, A_SW_STATE=0x82C, A_SW_CNT0=0x830,
  A_SW_PDUS=0x858, A_SW_SRP=0x85C,
};

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vcsr_win_live;

  dut->rst_n = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_bready = 0;
  dut->s_axi_arvalid = dut->s_axi_rready = 0;
  dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
  run(8);
  dut->rst_n = 1;
  run(8);

  printf("== P11 window vs LIVE KL_lwsrp_ctx + KL_acmp_lstn_ctx ==\n");

  printf("-- lwSRP row provisioning through the window --\n");
  axi_write(0x680, 0x0D);                 // LWSRP_CTRL: enable (qidx 3 kept)
  run(4);
  // listener stream 1 -> ctx row 1: stage sid, commit with CTRL.en
  axi_write(A_STRM_SEL, 0x001);           // dir=0 (listener), idx=1
  axi_write(A_SW_SID_LO, 0x0000BB80);
  axi_write(A_SW_SID_HI, 0x04106001);
  axi_write(A_SW_CTRL, 1);
  run(20);                                // write grant + status re-poll
  uint32_t srp = axi_read(A_SW_SRP);
  ck("live row1 valid (ctx_gnt path)", (srp >> 15) & 1, 1);
  ck("live row1 dir = listener",       (srp >> 14) & 1, 1);
  // the engine's row identity took the staged sid: read it back via the
  // ctx snapshot on the talker view is n/a for listeners — the valid/dir
  // status IS the grant-path proof; withdraw next
  axi_write(A_SW_CTRL, 0);
  run(20);
  srp = axi_read(A_SW_SRP);
  ck("live row1 withdrawn", (srp >> 15) & 1, 0);
  // talker stream 1 -> ctx row 2 (N_LISTENERS-1+idx): sid readback live
  axi_write(A_STRM_SEL, 0x101);           // dir=1 (talker), idx=1
  axi_write(A_SW_SID_LO, 0x0000000A);
  axi_write(A_SW_SID_HI, 0x02000000);
  axi_write(A_SW_DMAC_LO, 0xF000FE0A);
  axi_write(A_SW_DMAC_HI, 0x000091E0);
  axi_write(A_SW_CTRL, 1);
  run(20);
  srp = axi_read(A_SW_SRP);
  ck("live row2 valid",        (srp >> 15) & 1, 1);
  ck("live row2 dir = talker", (srp >> 14) & 1, 0);
  ck("live row2 sid readback LO", axi_read(A_SW_SID_LO), 0x0000000A);
  ck("live row2 sid readback HI", axi_read(A_SW_SID_HI), 0x02000000);

  printf("-- ACMP fast-connect bind read back via the window --\n");
  static const uint8_t DM1[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x07};
  const uint64_t SID1 = 0x9876543210ABCDEFULL;
  feed(acmp_connect(SID1, T1_EID, /*luid*/1, DM1, 0x101));
  run(60);                                // bind + response + tbl re-poll
  ck("ctx1 bound (compat view)", dut->acmp1_bound_o, 1);
  axi_write(A_STRM_SEL, 0x001);           // dir=0, idx=1 -> acmp ctx 1
  run(20);                                // tbl grant refresh
  ck("window SID_LO = bound sid", axi_read(A_SW_SID_LO), (uint32_t)SID1);
  ck("window SID_HI = bound sid", axi_read(A_SW_SID_HI), (uint32_t)(SID1 >> 32));
  ck("window DMAC_LO = bound dmac", axi_read(A_SW_DMAC_LO), 0xF0002A07);
  ck("window DMAC_HI = bound dmac", axi_read(A_SW_DMAC_HI), 0x91E0);
  axi_write(A_STRM_SNAP, 1);
  for (int g = 0; g < 64; ++g) if (axi_read(A_STRM_SNAP) == 0) break;
  uint32_t st = axi_read(A_SW_STATE);
  ck("STATE.state bound (!= UNBOUND)", (st & 7) != 0, 1);
  ck("CNT block zero (LCTX tied)", axi_read(A_SW_CNT0), 0);

  printf("-- E1 bind-restore inject + E2 readback (live engine) --\n");
  // ctx0 (probe-SM media sink) is UNBOUND: stage + commit the saved bind
  axi_write(0x7A0, 0xFE000001);           // talker lo (T1)
  axi_write(0x7A4, 0x02000000);           // talker hi
  axi_write(0x7A8, 0x00020007);           // vlan 2 (informational), tuid 7
  axi_write(0x7AC, (uint32_t)CT_EID);
  axi_write(0x7B0, (uint32_t)(CT_EID >> 32));
  axi_write(0x7B4, 0x80000000u | (0x0008u << 8) | 0);  // commit idx0, SW flag
  uint32_t rc = 0;
  for (int g = 0; g < 100; ++g) { rc = axi_read(0x7B4); if (!(rc >> 31)) break; }
  ck("restore commit completed", rc >> 31, 0);
  ck("restore done", (rc >> 30) & 1, 1);
  ck("restore status 0 (injected)", (rc >> 8) & 3, 0);
  // E2 readback of the injected record through the window (ctx0)
  axi_write(A_STRM_SEL, 0x000);           // dir=0 idx=0 -> acmp ctx0
  run(30);                                // tbl grant refresh
  ck("E2 CTLR_LO = restored ctlr", axi_read(0x860), (uint32_t)CT_EID);
  ck("E2 CTLR_HI = restored ctlr", axi_read(0x864), (uint32_t)(CT_EID >> 32));
  ck("E2 BIND {SW flag, tuid}", axi_read(0x868), 0x00080007);
  ck("injected sid CLEARED (5.5.2.6 step 1)", axi_read(A_SW_SID_LO), 0);
  ck("injected dmac CLEARED", axi_read(A_SW_DMAC_LO), 0);
  // ctx0 now occupied (PRB_W_AVAIL): a re-commit is refused with status 1
  axi_write(0x7B4, 0x80000000u);
  for (int g = 0; g < 100; ++g) { rc = axi_read(0x7B4); if (!(rc >> 31)) break; }
  ck("occupied re-commit refused (1)", (rc >> 8) & 3, 1);
  // ctx1 is a record-only context: refused with status 2
  axi_write(0x7B4, 0x80000000u | 1);
  for (int g = 0; g < 100; ++g) { rc = axi_read(0x7B4); if (!(rc >> 31)) break; }
  ck("record-only ctx refused (2)", (rc >> 8) & 3, 2);
  // ctx1's earlier fast-connect bind is untouched by the refusals
  ck("ctx1 bind survives refusals", dut->acmp1_bound_o, 1);
  axi_write(A_STRM_SEL, 0x001);
  run(30);
  ck("ctx1 E2 tuid still 0", axi_read(0x868) & 0xFFFF, 0);
  ck("ctx1 sid intact", axi_read(A_SW_SID_LO), (uint32_t)SID1);

  printf("-- index 0 SRP word = live 0x694 alias --\n");
  axi_write(A_STRM_SEL, 0x000);
  ck("win SRP idx0 == flat 0x694", axi_read(A_SW_SRP), axi_read(0x694));

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  dut->final();
  delete dut;
  return fails ? 1 : 0;
}

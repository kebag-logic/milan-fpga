/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * P11 indexed per-stream CSR window at N_LISTENERS_P=4 / N_TALKERS_P=4
 * (NXN_ARCHITECTURE.md §1.5) against MODELED lane-K engines:
 *   - LCTX/TCTX context-RAM port-B model (2-stage registered pipeline, the
 *     T2 contract) serving the slow window reads (CTRL/FMT listener side,
 *     CTRL/DMAC extra talker contexts)
 *   - SNAP atomicity: a free-running event pump increments ALL counter words
 *     of the model every cycle and freezes ONLY while snap_req && snap_ok
 *     (the engine-arbitrated burst). The latched {STATE, CNT0..9, PDUS}
 *     block must be ONE coherent epoch while events keep flowing before,
 *     between and after snaps.
 *   - lwSRP ctx master protocol: poll row map (dir=0 -> idx, dir=1 ->
 *     N_LISTENERS_P-1+idx), one-deep provisioning write (CTRL commit carries
 *     the staged SID/DMAC), hold-until-gnt, status readback into 0x85C
 *   - ACMP tbl master protocol: continuous poll, 317-bit ctx latch on gnt,
 *     SID/DMAC/STATE field extraction (offsets locked against acmp_pkg)
 *   - LCTX/TCTX CFG write bundles (window word -> engine word address map)
 *   - out-of-range index rule at N=4 (idx >= 4: reads 0, writes ignored)
 */

#include "Vmilan_csr.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>

static Vmilan_csr* dut;
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

// ----------------------------------------------------------------- models
static uint32_t lctx[8][32];        // {s[2:0], word[4:0]}
static uint32_t tctx[8][16];        // {t[2:0], word[3:0]}
static uint32_t l_q1, l_q2, t_q1, t_q2;   // port-B registered pipelines
static int      l_ev1, l_ev2, t_ev1, t_ev2; // rd_valid pipelines (P12 contract)
static int      l_ok_cnt, t_ok_cnt;       // snap_ok grant delay counters
static bool     pump_on;
static uint32_t evt;                       // coherent event epoch

// lwSRP ctx port model (grant one cycle after req, KL_lwsrp_ctx style) +
// sticky capture of the last WRITE command's payload
static int      srp_gnt_next;
static bool     srp_saw_wr;
static uint32_t srp_wr_idx, srp_wr_valid, srp_wr_dir;
static uint64_t srp_wr_sid, srp_wr_dmac;
static uint32_t srp_seen_idx_rd;           // last polled (we=0) row index

// ACMP tbl model
static int      acmp_gnt_next;

static void set_ctx_bits(int lo, int width, uint64_t v) {
  for (int i = 0; i < width; i++) {
    int b = lo + i;
    if ((v >> i) & 1) dut->i_acmp_tbl_ctx[b >> 5] |=  (1u << (b & 31));
    else              dut->i_acmp_tbl_ctx[b >> 5] &= ~(1u << (b & 31));
  }
}

static void model_pre_edge() {
  dut->eval();
  // event pump: every counter word of every stream carries the SAME epoch
  // value; frozen only while the engine has granted a coherent burst
  bool l_frozen = dut->o_lctx_snap_req && dut->i_lctx_snap_ok;
  bool t_frozen = dut->o_tctx_snap_req && dut->i_tctx_snap_ok;
  if (pump_on && !l_frozen && !t_frozen) {
    evt++;
    for (int s = 0; s < 8; s++) {
      for (int w = 16; w <= 25; w++) lctx[s][w] = evt;   // CNT0..9
      lctx[s][11] = evt;                                 // PDUS
      lctx[s][8]  = ((evt & 0xFF) << 14) | (1u << 12);   // wire_chans, locked
      tctx[s][5]  = evt;                                 // talker FRAMES
    }
  }
  // port-B pipelines: present q2, then shift (data valid 2 edges after addr).
  // P12 contract: rd_valid mirrors the data pipeline (valid = rd_en two
  // edges ago) — an always-idle engine model, the P11 timing exactly.
  uint32_t la = dut->o_lctx_rd_addr, ta = dut->o_tctx_rd_addr;
  dut->i_lctx_rd_data = l_q2;
  l_q2 = l_q1; l_q1 = lctx[(la >> 5) & 7][la & 31];
  dut->i_lctx_rd_valid = l_ev2;
  l_ev2 = l_ev1; l_ev1 = dut->o_lctx_rd_en & 1;
  dut->i_tctx_rd_data = t_q2;
  t_q2 = t_q1; t_q1 = tctx[(ta >> 4) & 7][ta & 15];
  dut->i_tctx_rd_valid = t_ev2;
  t_ev2 = t_ev1; t_ev1 = dut->o_tctx_rd_en & 1;
  // snap_ok: granted 3 cycles into a held request
  l_ok_cnt = dut->o_lctx_snap_req ? l_ok_cnt + 1 : 0;
  t_ok_cnt = dut->o_tctx_snap_req ? t_ok_cnt + 1 : 0;
  dut->i_lctx_snap_ok = (l_ok_cnt >= 3);
  dut->i_tctx_snap_ok = (t_ok_cnt >= 3);
  // lwSRP ctx port: capture the command at its service beat (req && !gnt),
  // grant one cycle later
  dut->i_srp_ctx_gnt = srp_gnt_next;
  dut->eval();
  if (dut->o_srp_ctx_req && !dut->i_srp_ctx_gnt) {
    if (dut->o_srp_ctx_we) {
      srp_saw_wr   = true;
      srp_wr_idx   = dut->o_srp_ctx_idx;
      srp_wr_valid = dut->o_srp_ctx_valid;
      srp_wr_dir   = dut->o_srp_ctx_dir;
      srp_wr_sid   = dut->o_srp_ctx_sid;
      srp_wr_dmac  = dut->o_srp_ctx_dmac;
    } else {
      srp_seen_idx_rd = dut->o_srp_ctx_idx;
    }
    srp_gnt_next = 1;
  } else {
    srp_gnt_next = 0;
  }
  // ACMP tbl port: same grant shape; ctx word is preloaded by the test
  dut->i_acmp_tbl_gnt = acmp_gnt_next;
  dut->eval();
  acmp_gnt_next = (dut->o_acmp_tbl_req && !dut->i_acmp_tbl_gnt) ? 1 : 0;
}

// sticky captures of the CFG write bundles
static bool     seen_lctx_wr, seen_tctx_wr;
static uint32_t lctx_wr_addr, lctx_wr_data, tctx_wr_addr, tctx_wr_data;

static void posedge() {
  model_pre_edge();
  dut->aclk = 1; dut->eval();
  if (dut->o_lctx_wr_p) {
    seen_lctx_wr = true;
    lctx_wr_addr = dut->o_lctx_wr_addr; lctx_wr_data = dut->o_lctx_wr_data;
  }
  if (dut->o_tctx_wr_p) {
    seen_tctx_wr = true;
    tctx_wr_addr = dut->o_tctx_wr_addr; tctx_wr_data = dut->o_tctx_wr_data;
  }
  dut->aclk = 0; dut->eval();
}

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

enum {
  A_STRM_SEL=0x800, A_STRM_SNAP=0x804, A_SW_CTRL=0x810,
  A_SW_SID_LO=0x814, A_SW_SID_HI=0x818, A_SW_DMAC_LO=0x81C,
  A_SW_DMAC_HI=0x820, A_SW_FMT_LO=0x824, A_SW_FMT_HI=0x828,
  A_SW_STATE=0x82C, A_SW_CNT0=0x830, A_SW_PDUS=0x858, A_SW_SRP=0x85C,
};

static void snap_and_wait() {
  axi_write(A_STRM_SNAP, 1);
  for (int g = 0; g < 64; ++g)
    if (axi_read(A_STRM_SNAP) == 0) return;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vmilan_csr;
  memset(lctx, 0, sizeof lctx); memset(tctx, 0, sizeof tctx);
  // P12: CFG-word writes are held until the engine's wr_rdy; the model
  // accepts every cycle (arbitration under load is the milan_dp NxN TB's job)
  dut->i_lctx_wr_rdy = 1; dut->i_tctx_wr_rdy = 1;

  dut->aresetn = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_bready = 0;
  dut->s_axi_arvalid = dut->s_axi_rready = 0;
  for (int i = 0; i < 5; ++i) posedge();
  dut->aresetn = 1; posedge();

  printf("== milan_csr P11 window, N=4x4, modeled lane-K engines ==\n");

  printf("-- slow window reads from the LCTX port-B model --\n");
  lctx[2][4] = 0xC0DE0004;   // CTRL
  lctx[2][2] = 0xC0DE0002;   // FMT_LO
  lctx[2][3] = 0xC0DE0003;   // FMT_HI
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  ck("LCTX CTRL (w4) via port B",  axi_read(A_SW_CTRL),   0xC0DE0004);
  ck("LCTX FMT_LO (w2) via port B", axi_read(A_SW_FMT_LO), 0xC0DE0002);
  ck("LCTX FMT_HI (w3) via port B", axi_read(A_SW_FMT_HI), 0xC0DE0003);
  tctx[3][0] = 0xBEEF0000; tctx[3][1] = 0xBEEF0001; tctx[3][2] = 0xBEEF0002;
  axi_write(A_STRM_SEL, 0x103);              // dir=1 idx=3
  ck("TCTX CTRL (w0) via port B",    axi_read(A_SW_CTRL),    0xBEEF0000);
  ck("TCTX DMAC_LO (w1) via port B", axi_read(A_SW_DMAC_LO), 0xBEEF0001);
  ck("TCTX DMAC_HI (w2) via port B", axi_read(A_SW_DMAC_HI), 0xBEEF0002);

  printf("-- CFG write bundles: window word -> engine word map --\n");
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  seen_lctx_wr = false;
  axi_write(A_SW_FMT_LO, 0xAB01);
  ck("FMT_LO write pulsed LCTX", seen_lctx_wr, 1);
  ck("LCTX wr addr {s=2,w=2}", lctx_wr_addr, (2u << 5) | 2u);
  ck("LCTX wr data", lctx_wr_data, 0xAB01);
  seen_lctx_wr = false;
  axi_write(A_SW_SID_LO, 0x5511);
  ck("SID_LO write -> LCTX w0", lctx_wr_addr, (2u << 5) | 0u);
  axi_write(A_STRM_SEL, 0x103);              // dir=1 idx=3
  seen_tctx_wr = false;
  axi_write(A_SW_DMAC_HI, 0x91E0);
  ck("DMAC_HI write pulsed TCTX", seen_tctx_wr, 1);
  ck("TCTX wr addr {t=3,w=2}", tctx_wr_addr, (3u << 4) | 2u);
  ck("TCTX wr data", tctx_wr_data, 0x91E0);

  printf("-- SNAP atomicity: coherent block while events keep flowing --\n");
  pump_on = true;
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  for (int i = 0; i < 20; ++i) posedge();    // let events flow
  axi_write(A_STRM_SNAP, 1);
  ck("SNAP busy while bursting", axi_read(A_STRM_SNAP) & 1, 1);
  for (int g = 0; g < 64; ++g) if (axi_read(A_STRM_SNAP) == 0) break;
  uint32_t v1 = axi_read(A_SW_CNT0);
  ck("snap epoch nonzero", v1 != 0, 1);
  bool coh = true;
  for (int k = 0; k < 10; ++k)
    if (axi_read(A_SW_CNT0 + 4*k) != v1) coh = false;
  if (axi_read(A_SW_PDUS) != v1) coh = false;
  ck("CNT0..9 + PDUS one epoch", coh, 1);
  uint32_t st1 = axi_read(A_SW_STATE);
  ck("STATE wire_chans same epoch", (st1 >> 11) & 0xFF, v1 & 0xFF);
  ck("STATE media_locked (m8[12])", (st1 >> 10) & 1, 1);
  // events kept flowing: a later snap latches a LARGER, again-coherent epoch
  for (int i = 0; i < 30; ++i) posedge();
  snap_and_wait();
  uint32_t v2 = axi_read(A_SW_CNT0);
  ck("second snap advanced", v2 > v1, 1);
  coh = true;
  for (int k = 0; k < 10; ++k)
    if (axi_read(A_SW_CNT0 + 4*k) != v2) coh = false;
  if (axi_read(A_SW_PDUS) != v2) coh = false;
  ck("second snap coherent", coh, 1);
  // talker snap: TCTX w5 -> PDUS, CNT block zero
  axi_write(A_STRM_SEL, 0x101);              // dir=1 idx=1
  snap_and_wait();
  uint32_t vt = axi_read(A_SW_PDUS);
  ck("talker PDUS = TCTX w5 epoch", vt != 0 && vt >= v2, 1);
  ck("talker CNT0 zero", axi_read(A_SW_CNT0), 0);
  pump_on = false;

  printf("-- lwSRP ctx master: row map, provisioning, status readback --\n");
  axi_write(A_STRM_SEL, 0x003);              // dir=0 idx=3 -> poll row 3
  dut->i_srp_ctx_rd_stat = 0x8123;           // engine-held snapshot
  dut->i_srp_ctx_rd_sid  = 0x1122334455667788ULL;
  for (int i = 0; i < 10; ++i) posedge();    // let a poll grant land
  ck("poll row = idx (dir=0)", srp_seen_idx_rd, 3);
  ck("SRP word = {16'0, rd_stat}", axi_read(A_SW_SRP), 0x8123);
  axi_write(A_STRM_SEL, 0x102);              // dir=1 idx=2 -> row 4-1+2 = 5
  for (int i = 0; i < 10; ++i) posedge();
  ck("poll row = N_L-1+idx (dir=1)", srp_seen_idx_rd, 5);
  ck("talker SID_LO = ctx rd_sid", axi_read(A_SW_SID_LO), 0x55667788);
  ck("talker SID_HI = ctx rd_sid", axi_read(A_SW_SID_HI), 0x11223344);
  // provisioning: stage SID/DMAC, commit with CTRL.en=1
  srp_saw_wr = false;
  axi_write(A_SW_SID_LO, 0x0000AAAA);
  axi_write(A_SW_SID_HI, 0x02000000);
  axi_write(A_SW_DMAC_LO, 0xF000FE05);
  axi_write(A_SW_DMAC_HI, 0x000091E0);
  axi_write(A_SW_CTRL, 1);
  for (int i = 0; i < 10; ++i) posedge();
  ck("provision write granted", srp_saw_wr, 1);
  ck("provision row", srp_wr_idx, 5);
  ck("provision valid", srp_wr_valid, 1);
  ck("provision dir (ctx enc: talker=0)", srp_wr_dir, 0);
  ck("provision sid staged", srp_wr_sid, 0x020000000000AAAAULL);
  ck("provision dmac staged", srp_wr_dmac, 0x91E0F000FE05ULL);
  // withdraw: CTRL.en=0 -> valid=0 write to the same row
  srp_saw_wr = false;
  axi_write(A_SW_CTRL, 0);
  for (int i = 0; i < 10; ++i) posedge();
  ck("withdraw granted", srp_saw_wr, 1);
  ck("withdraw valid=0", srp_wr_valid, 0);
  // listener provisioning carries ctx dir=1
  axi_write(A_STRM_SEL, 0x001);              // dir=0 idx=1 -> row 1
  srp_saw_wr = false;
  axi_write(A_SW_CTRL, 1);
  for (int i = 0; i < 10; ++i) posedge();
  ck("listener provision row", srp_wr_idx, 1);
  ck("listener provision dir=1", srp_wr_dir, 1);

  printf("-- ACMP tbl master: 317-bit ctx latch + field extraction --\n");
  set_ctx_bits(128, 64, 0xAABBCCDD00112233ULL);  // sid
  set_ctx_bits(192, 48, 0x91E0F0004455ULL);      // dmac
  set_ctx_bits(305, 5, 21);                      // status
  set_ctx_bits(310, 2, 1);                       // probing
  set_ctx_bits(314, 3, 7);                       // state
  axi_write(A_STRM_SEL, 0x001);              // dir=0 idx=1 (re-latch fresh)
  for (int i = 0; i < 10; ++i) posedge();
  ck("acmp SID_LO",  axi_read(A_SW_SID_LO),  0x00112233);
  ck("acmp SID_HI",  axi_read(A_SW_SID_HI),  0xAABBCCDD);
  ck("acmp DMAC_LO", axi_read(A_SW_DMAC_LO), 0xF0004455);
  ck("acmp DMAC_HI", axi_read(A_SW_DMAC_HI), 0x91E0);
  dut->i_srp_ctx_rd_stat = 0;                // keep the STATE srp9 field 0
  pump_on = true;
  snap_and_wait();
  pump_on = false;
  uint32_t st = axi_read(A_SW_STATE);
  ck("STATE acmp state",   st & 7, 7);
  ck("STATE acmp probing", (st >> 3) & 3, 1);
  ck("STATE acmp status",  (st >> 5) & 31, 21);

  printf("-- out-of-range at N=4: idx 4+ reads 0 / writes ignored --\n");
  axi_write(A_STRM_SEL, 0x004);              // dir=0 idx=4: OUT of range
  seen_lctx_wr = false; srp_saw_wr = false;
  axi_write(A_SW_CTRL, 0xFF);
  axi_write(A_SW_SID_LO, 0x1234);
  for (int i = 0; i < 10; ++i) posedge();
  ck("oor CTRL reads 0",   axi_read(A_SW_CTRL), 0);
  ck("oor SID_LO reads 0", axi_read(A_SW_SID_LO), 0);
  ck("oor SRP reads 0",    axi_read(A_SW_SRP), 0);
  ck("oor no LCTX write",  seen_lctx_wr, 0);
  ck("oor no SRP provision", srp_saw_wr, 0);
  ck("oor SEL readback intact", axi_read(A_STRM_SEL), 0x004);

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  dut->final();
  delete dut;
  return fails ? 1 : 0;
}

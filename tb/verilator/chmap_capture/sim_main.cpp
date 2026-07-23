// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_chan_map_capture harness: the per-pair-slot TX source mux feeding the
// shared KL_aaf_packetizer.
//   Lane A: chmap(32) -> packetizer(N=2, t0=2ch slot0 / t1=8ch slots1..4).
//     - per-slot source routing (I2S / TDM / RING / TONE), payload-exact;
//     - mid-run remap (RING->ZERO, TONE->RING1);
//     - disabled slot = absence (drop t0 by disabling its only slot);
//     - map RAM readback port.
//   Lane B: chmap(32) -> packetizer(N=8, ALL 8ch = 32 pair slots). Exercises
//     the widened pair_slot: talker 7 owns slots 28..31, so slot 31 = t7's
//     4th pair - its payload proves the >15 slot path end to end.
#include "Vchmap_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vchmap_wrap* dut;
static long checks = 0, fails = 0;
static void ck(const char* t, long got, long exp) {
  checks++;
  if (got != exp) { fails++; printf("  [FAIL] %-46s got=0x%lx exp=0x%lx\n", t, got, exp); }
  else            printf("  [ ok ] %-46s = 0x%lx\n", t, got);
}

using Frame = std::vector<uint8_t>;
static std::vector<Frame> afr, bfr;
static Frame acur, bcur;

static void sample() {
  if (dut->a_tvalid_o && dut->a_tready_i) {
    for (int i = 0; i < 8; i++) if ((dut->a_tkeep_o >> i) & 1)
      acur.push_back((dut->a_tdata_o >> (8 * i)) & 0xFF);
    if (dut->a_tlast_o) { afr.push_back(acur); acur.clear(); }
  }
  if (dut->b_tvalid_o && dut->b_tready_i) {
    for (int i = 0; i < 8; i++) if ((dut->b_tkeep_o >> i) & 1)
      bcur.push_back((dut->b_tdata_o >> (8 * i)) & 0xFF);
    if (dut->b_tlast_o) { bfr.push_back(bcur); bcur.clear(); }
  }
}
static void step() { dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); sample(); }
static void cyc(int n = 1) { for (int i = 0; i < n; i++) step(); }

static unsigned long be(const Frame& b, int o, int n) {
  unsigned long v = 0; for (int i = 0; i < n; i++) v = (v << 8) | b[o + i]; return v; }
static int find_len(std::vector<Frame>& v, size_t len) {
  for (size_t i = 0; i < v.size(); i++) if (v[i].size() == len) return (int)i; return -1; }
static uint8_t ent(int en, int src, int idx) {
  return (uint8_t)(((en & 1) << 7) | ((src & 7) << 4) | (idx & 0xF)); }

// ---- map RAM write / read ------------------------------------------------
static void a_map_wr(int slot, uint8_t d) {
  dut->a_map_wr_en_i = 1; dut->a_map_wr_addr_i = slot; dut->a_map_wr_data_i = d;
  cyc(); dut->a_map_wr_en_i = 0; cyc(); }
static void b_map_wr(int slot, uint8_t d) {
  dut->b_map_wr_en_i = 1; dut->b_map_wr_addr_i = slot; dut->b_map_wr_data_i = d;
  cyc(); dut->b_map_wr_en_i = 0; cyc(); }
static uint8_t a_map_rd(int slot) {
  dut->a_map_rd_en_i = 1; dut->a_map_rd_addr_i = slot; cyc();
  uint8_t v = dut->a_map_rd_data_o; bool ok = dut->a_map_rd_valid_o;
  dut->a_map_rd_en_i = 0; cyc();
  if (!ok) { printf("  [FAIL] a_map_rd(%d) no valid\n", slot); fails++; checks++; }
  return v; }

// ---- TCTX window writes (poll wr_rdy, like the NxN harness) ---------------
static void a_tctx_wr(int t, int w, uint32_t v) {
  dut->a_tctx_wr_en_i = 1; dut->a_tctx_wr_addr_i = (uint8_t)((t << 4) | w);
  dut->a_tctx_wr_data_i = v;
  for (int i = 0; i < 48; i++) {
    dut->clk = 0; dut->eval(); bool rdy = dut->a_tctx_wr_rdy_o;
    dut->clk = 1; dut->eval(); sample();
    if (rdy) { dut->a_tctx_wr_en_i = 0; cyc(); return; } }
  dut->a_tctx_wr_en_i = 0; printf("  [FAIL] a_tctx_wr timeout\n"); fails++; checks++; }
static void b_tctx_wr(int t, int w, uint32_t v) {
  dut->b_tctx_wr_en_i = 1; dut->b_tctx_wr_addr_i = (uint8_t)((t << 4) | w);
  dut->b_tctx_wr_data_i = v;
  for (int i = 0; i < 48; i++) {
    dut->clk = 0; dut->eval(); bool rdy = dut->b_tctx_wr_rdy_o;
    dut->clk = 1; dut->eval(); sample();
    if (rdy) { dut->b_tctx_wr_en_i = 0; cyc(); return; } }
  dut->b_tctx_wr_en_i = 0; printf("  [FAIL] b_tctx_wr timeout\n"); fails++; checks++; }

// ---- source-pair drivers (latched free-running by both chmaps) -----------
static void drv_i2s(uint32_t l, uint32_t r) {
  dut->i2s_pair_valid_i = 1; dut->i2s_l_i = l & 0xFFFFFF; dut->i2s_r_i = r & 0xFFFFFF;
  cyc(); dut->i2s_pair_valid_i = 0; cyc(); }
static void drv_tdm(int slot, uint32_t l, uint32_t r) {
  dut->tdm_pair_valid_i = 1; dut->tdm_pair_slot_i = slot;
  dut->tdm_l_i = l & 0xFFFFFF; dut->tdm_r_i = r & 0xFFFFFF;
  cyc(); dut->tdm_pair_valid_i = 0; cyc(); }
static void drv_ring(int slot, uint32_t l, uint32_t r) {
  dut->ring_pair_valid_i = 1; dut->ring_pair_slot_i = slot;
  dut->ring_l_i = l & 0xFFFFFF; dut->ring_r_i = r & 0xFFFFFF;
  cyc(); dut->ring_pair_valid_i = 0; cyc(); }

// ---- media ticks (one full slot walk per tick; drain-friendly spacing) ---
static void a_tick() { dut->a_tick_i = 1; cyc(); dut->a_tick_i = 0; cyc(300); }
static void b_tick() { dut->b_tick_i = 1; cyc(); dut->b_tick_i = 0; cyc(340); }

static const uint32_t I2S_L = 0x1A1111, I2S_R = 0x1A2222;
static const uint32_t TONE  = 0x7A7A7A;
static uint32_t TDM_L(int p) { return 0x2B0000 | (p << 4); }
static uint32_t TDM_R(int p) { return 0x2BB000 | (p << 4); }
static uint32_t RNG_L(int r) { return 0x3C0000 | (r << 4); }
static uint32_t RNG_R(int r) { return 0x3CC000 | (r << 4); }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vchmap_wrap;

  dut->rst_n = 0;
  dut->a_tready_i = 1; dut->b_tready_i = 1;
  dut->dest_mac_i = 0x91E0F000FE01ULL; dut->station_mac_i = 0x020000000002ULL;
  dut->vlan_vid_i = 2; dut->ptp_ns_i = 0x11223344; dut->transit_ns_i = 2000000;
  dut->i2s_pair_valid_i = 0; dut->tdm_pair_valid_i = 0; dut->ring_pair_valid_i = 0;
  dut->tone_smp_i = 0;
  dut->a_map_wr_en_i = 0; dut->a_map_rd_en_i = 0; dut->a_tick_i = 0; dut->a_en_i = 0;
  dut->a_tctx_wr_en_i = 0; dut->a_tctx_rd_en_i = 0;
  dut->b_map_wr_en_i = 0; dut->b_map_rd_en_i = 0; dut->b_tick_i = 0; dut->b_en_i = 0;
  dut->b_tctx_wr_en_i = 0; dut->b_tctx_rd_en_i = 0;
  cyc(8); dut->rst_n = 1; cyc(4);

  printf("== KL_chan_map_capture (per-pair-slot TX source mux) ==\n");

  // ====================================================================== //
  printf("\n[A] per-slot routing: I2S / TDM / RING / TONE across t0(2ch)+t1(8ch)\n");
  // t1 CFG via the TCTX window (chans=8 so t1 owns pair slots 1..4)
  a_tctx_wr(1, 1, 0xF000FE02u);            // DMAC_LO (wire bytes 2..5) = base+1
  a_tctx_wr(1, 2, (1u << 16) | 0x91E0u);   // {UID=1, DMAC_HI}
  a_tctx_wr(1, 0, (2u << 5) | (8u << 1) | 1u); // CTRL {en, chans=8, vid=2}
  dut->a_en_i = 3;

  a_map_wr(0, ent(1, 1, 0));   // slot0 (t0 pair0) = I2S
  a_map_wr(1, ent(1, 2, 0));   // slot1 (t1 pair0) = TDM idx0
  a_map_wr(2, ent(1, 2, 1));   // slot2 (t1 pair1) = TDM idx1
  a_map_wr(3, ent(1, 3, 0));   // slot3 (t1 pair2) = RING idx0
  a_map_wr(4, ent(1, 4, 0));   // slot4 (t1 pair3) = TONE

  dut->tone_smp_i = TONE;
  drv_i2s(I2S_L, I2S_R);
  drv_tdm(0, TDM_L(0), TDM_R(0));
  drv_tdm(1, TDM_L(1), TDM_R(1));
  drv_ring(0, RNG_L(0), RNG_R(0));
  drv_ring(1, RNG_L(1), RNG_R(1));   // preloaded for the remap phase
  cyc(4);

  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);

  ck("A: two frames (t0 + t1)", (long)afr.size(), 2);
  int ia0 = find_len(afr, 90), ia1 = find_len(afr, 234);
  ck("A: t0 90-byte frame present", ia0 >= 0, 1);
  ck("A: t1 234-byte frame present", ia1 >= 0, 1);
  if (ia0 >= 0 && ia1 >= 0) {
    ck("A: t0 channels_per_frame = 2", afr[ia0][36], 2);
    ck("A: t1 channels_per_frame = 8", afr[ia1][36], 8);
    ck("A: t0 uid 0", be(afr[ia0], 22, 8) & 0xFFFF, 0);
    ck("A: t1 uid 1", be(afr[ia1], 22, 8) & 0xFFFF, 1);
    ck("A: t1 DMAC = base+1 (TCTX)", be(afr[ia1], 0, 6), 0x91E0F000FE02UL);
    ck("A: t0 slot0 = I2S L", be(afr[ia0], 42, 3), I2S_L);
    ck("A: t0 slot0 = I2S R", be(afr[ia0], 46, 3), I2S_R);
    ck("A: t1 pair0 slot1 = TDM0 L", be(afr[ia1], 42, 3), TDM_L(0));
    ck("A: t1 pair0 slot1 = TDM0 R", be(afr[ia1], 46, 3), TDM_R(0));
    ck("A: t1 pair1 slot2 = TDM1 L", be(afr[ia1], 50, 3), TDM_L(1));
    ck("A: t1 pair2 slot3 = RING0 L", be(afr[ia1], 58, 3), RNG_L(0));
    ck("A: t1 pair2 slot3 = RING0 R", be(afr[ia1], 62, 3), RNG_R(0));
    ck("A: t1 pair3 slot4 = TONE L", be(afr[ia1], 66, 3), TONE);
    ck("A: t1 pair3 slot4 = TONE R", be(afr[ia1], 70, 3), TONE);
    ck("A: t0 seq 0", afr[ia0][20], 0);
    ck("A: t1 seq 0", afr[ia1][20], 0);
  } else { for (int k = 0; k < 15; k++) ck("A content (skipped: frames missing)", 0, 1); }

  // ====================================================================== //
  printf("\n[A2] mid-run remap: slot3 RING0->ZERO(silence), slot4 TONE->RING1\n");
  a_map_wr(3, ent(1, 0, 0));   // slot3 -> ZERO source (silence, en=1)
  a_map_wr(4, ent(1, 3, 1));   // slot4 -> RING idx1
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  ck("A2: two frames again", (long)afr.size(), 2);
  int j1 = find_len(afr, 234), j0 = find_len(afr, 90);
  if (j1 >= 0) {
    ck("A2: t1 pair2 slot3 now silence L", be(afr[j1], 58, 3), 0);
    ck("A2: t1 pair2 slot3 now silence R", be(afr[j1], 62, 3), 0);
    ck("A2: t1 pair3 slot4 now RING1 L", be(afr[j1], 66, 3), RNG_L(1));
    ck("A2: t1 pair3 slot4 now RING1 R", be(afr[j1], 70, 3), RNG_R(1));
    ck("A2: t1 seq advanced to 1", afr[j1][20], 1);
  } else { for (int k = 0; k < 5; k++) ck("A2 content (skipped)", 0, 1); }
  if (j0 >= 0) ck("A2: t0 seq advanced to 1", afr[j0][20], 1);
  else         ck("A2: t0 frame (skipped)", 0, 1);

  // ====================================================================== //
  printf("\n[A3] disabled slot = absence: disable slot0 drops t0 entirely\n");
  a_map_wr(0, ent(0, 1, 0));   // slot0 disabled (en=0)
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  ck("A3: only one frame (t0 absent)", (long)afr.size(), 1);
  if (afr.size() == 1) {
    ck("A3: surviving frame is 8ch (t1)", afr[0][36], 8);
    ck("A3: t1 seq advanced to 2", afr[0][20], 2);
  } else { ck("A3 content (skipped)", 0, 1); ck("A3 content (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[RB] map RAM readback port\n");
  ck("RB: slot1 = {en,TDM,0}",  a_map_rd(1), ent(1, 2, 0));
  ck("RB: slot3 = {en,ZERO,0}", a_map_rd(3), ent(1, 0, 0));
  ck("RB: slot4 = {en,RING,1}", a_map_rd(4), ent(1, 3, 1));
  ck("RB: slot0 = disabled",    a_map_rd(0), ent(0, 1, 0));

  // ====================================================================== //
  printf("\n[B] widened slot: N=8 all-8ch, talker 7 owns slots 28..31 (slot 31)\n");
  // ALL 8 talkers must be 8ch so the prefix sum gives pbase[7]=28 (t7 pair p =
  // slot 28+p; slot 31 = t7 pair 3)
  for (int t = 0; t < 8; t++)
    b_tctx_wr(t, 0, (2u << 5) | (8u << 1) | (t == 7 ? 1u : 0u)); // CTRL chans=8
  b_tctx_wr(7, 1, 0xF000FE08u);            // t7 DMAC_LO = base+7
  b_tctx_wr(7, 2, (7u << 16) | 0x91E0u);   // {UID=7, DMAC_HI}
  dut->b_en_i = 0x80;                        // enable talker 7 only

  b_map_wr(28, ent(1, 1, 0));  // slot28 (t7 pair0) = I2S
  b_map_wr(29, ent(1, 2, 0));  // slot29 (t7 pair1) = TDM idx0
  b_map_wr(30, ent(1, 3, 0));  // slot30 (t7 pair2) = RING idx0
  b_map_wr(31, ent(1, 4, 0));  // slot31 (t7 pair3) = TONE  <-- widened slot

  // refresh the shared source holds for lane B
  dut->tone_smp_i = TONE;
  drv_i2s(I2S_L, I2S_R);
  drv_tdm(0, TDM_L(0), TDM_R(0));
  drv_ring(0, RNG_L(0), RNG_R(0));
  cyc(4);

  bfr.clear();
  for (int i = 0; i < 6; i++) b_tick();
  cyc(600);

  ck("B: one frame emitted (t7)", (long)bfr.size(), 1);
  if (bfr.size() == 1) {
    ck("B: t7 frame is 234 bytes (8ch)", (long)bfr[0].size(), 234);
    ck("B: t7 channels_per_frame = 8", bfr[0][36], 8);
    ck("B: t7 uid 7", be(bfr[0], 22, 8) & 0xFFFF, 7);
    ck("B: t7 DMAC = base+7", be(bfr[0], 0, 6), 0x91E0F000FE08UL);
    ck("B: slot28 pair0 = I2S L", be(bfr[0], 42, 3), I2S_L);
    ck("B: slot29 pair1 = TDM0 L", be(bfr[0], 50, 3), TDM_L(0));
    ck("B: slot30 pair2 = RING0 L", be(bfr[0], 58, 3), RNG_L(0));
    ck("B: slot31 pair3 = TONE L (widened >15 slot)", be(bfr[0], 66, 3), TONE);
    ck("B: slot31 pair3 = TONE R (widened >15 slot)", be(bfr[0], 70, 3), TONE);
  } else { for (int k = 0; k < 9; k++) ck("B content (skipped: count wrong)", 0, 1); }

  printf("\n======================================================================\n");
  printf("KL_chan_map_capture: %ld checks, %ld failures\nRESULT: %s\n",
         checks, fails, fails ? "FAIL" : "PASS");
  delete dut;
  return fails ? 1 : 0;
}

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_chan_map_capture harness: the per-pair-slot TX source mux feeding the
// shared KL_aaf_packetizer.
//
// LEVELS AND ORACLES (docs/testing/methodology.md):
//   L0  the mux against its clause-derived expectation (7.3.3 / 7.3.5).
//   L2  every payload assertion below reads the AVTPDU bytes emitted by the
//       REAL KL_aaf_packetizer on its AXIS port - the oracle is the frame on
//       the wire-facing port, never an internal signal. That is why the
//       expected values are byte offsets into a 234-byte frame.
//   L1  [R5] section only: the mapped-vs-fed capability mask, whose oracle is
//       the fabric's own accepted-beat strobe. It is the one thing here that
//       can distinguish an UNWIRED integration from a quiet one.
//   R4  every RX channel carries a DISTINCT value throughout: a harness that
//       drove the same value on two channels could not detect a swap, and a
//       swap is the defect this whole lane exists to make visible.
//   R2  negative controls (run by hand, recorded in the lane report): a
//       single-parity inversion of the L/R store yields 11 failures, a full
//       L/R swap yields 17 with every value perfectly transposed. Note that
//       the "L != R" checks survive a pure swap - distinctness catches
//       DUPLICATION, only the exact-value checks catch CROSSING. Both kept.
//   Lane A: chmap(32) -> packetizer(N=2, t0=2ch slot0 / t1=8ch slots1..4).
//     - per-slot source routing (I2S / TDM / RING / TONE), payload-exact;
//     - mid-run remap (RING->ZERO, TONE->RING1);
//     - disabled slot = absence (drop t0 by disabling its only slot);
//     - map RAM readback port;
//     - LOOPBACK source (src 5): a RECEIVED stream's channel pair feeding a
//       talker pair slot. Every RX channel carries a DISTINCT value, so the
//       payload bytes prove L and R are neither crossed nor duplicated -
//       which no other source on this board can prove (the tone is the same
//       sample on both channels and the AX7101 has no audio input at all).
//   Lane B: chmap(32) -> packetizer(N=8, ALL 8ch = 32 pair slots). Exercises
//     the widened pair_slot: talker 7 owns slots 28..31, so slot 31 = t7's
//     4th pair - its payload proves the >15 slot path end to end.
//   [G] tone ONE-GRID contract (task #59): clk_audio drifts against clk at
//     an incommensurate ratio; both tone shapes are sampled at the media-
//     tick instants exactly as the crossbar's TONE bucket reads them. The
//     legacy clk_audio/512 shape MUST slip in BOTH drift directions (drops
//     when audio is fast, repeats when slow) - the negative control that
//     proves the check has teeth against the pre-fix wiring - while the
//     USE_EXT_ADV_P media-grid shape advances EXACTLY one table step per
//     tick over every tick of both phases.
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
// map entry {half[13:12], idxh[11:8], en[7], src[6:4], idx[3:0]}: idxh is
// read by the LOOP source only and half defaults to BOTH, so ent() is the
// pre-loopback 8-bit word verbatim with 0b11 above it - every legacy check
// below still writes exactly the byte it used to, meaning exactly what it
// used to mean.
static const uint16_t HALF_BOTH = 0x3000, HALF_L = 0x2000, HALF_R = 0x1000;
static const uint16_t SWAP_BOTH = 0xC000, SWAP_L = 0x8000, SWAP_R = 0x4000;
static uint16_t ent(int en, int src, int idx) {
  return (uint16_t)(HALF_BOTH | ((en & 1) << 7) | ((src & 7) << 4)
                    | (idx & 0xF)); }
//! the same entry with only ONE of the slot's two stream channels armed
static uint16_t ent_half(int half, int en, int src, int idx) {
  return (uint16_t)((ent(en, src, idx) & 0x0FFF) | half); }
// LOOP entry: RX stream s (idxh) + channel pair p (idx) -> wire ch {2p, 2p+1}
static const int SRC_LOOP = 5;
static uint16_t ent_lb(int en, int s, int p) {
  return (uint16_t)((((s) & 0xF) << 8) | ent(en, SRC_LOOP, p)); }

// ---- map RAM write / read ------------------------------------------------
static void a_map_wr(int slot, uint16_t d) {
  dut->a_map_wr_en_i = 1; dut->a_map_wr_addr_i = slot; dut->a_map_wr_data_i = d;
  cyc(); dut->a_map_wr_en_i = 0; cyc(); }
static void b_map_wr(int slot, uint16_t d) {
  dut->b_map_wr_en_i = 1; dut->b_map_wr_addr_i = slot; dut->b_map_wr_data_i = d;
  cyc(); dut->b_map_wr_en_i = 0; cyc(); }
static uint16_t a_map_rd(int slot) {
  dut->a_map_rd_en_i = 1; dut->a_map_rd_addr_i = slot; cyc();
  uint16_t v = dut->a_map_rd_data_o; bool ok = dut->a_map_rd_valid_o;
  dut->a_map_rd_en_i = 0; cyc();
  if (!ok) { printf("  [FAIL] a_map_rd(%d) no valid\n", slot); fails++; checks++; }
  return v; }
// the addressed entry (readback [13:0] - [13:12] is the per-half enable,
// which used to be reserved zeros; [11:0] keeps its exact legacy meaning)
static uint16_t a_map_ent(int slot) { return a_map_rd(slot) & 0x3FFF; }
// the LOOP capability mask (readback [15:14]): bit0 = mapped, bit1 = fed
static uint16_t a_map_mask(int slot) { return (a_map_rd(slot) >> 14) & 3; }

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

// ---- LOOPBACK payload stimulus: a synthetic KL_aaf_rx_depacketizer clone --
// One 64-bit beat = 2 consecutive S32BE samples in WIRE order (byte lane j =
// wire byte j; the top 24 bits are the audio, lanes 3/7 are the S32 pad), one
// AXIS frame per AAF PDU, tuser = stream index - the depacketizer's m_axis
// contract, which is also what KL_chan_map_render consumes.
static uint64_t lb_beat(uint32_t a, uint32_t b) {
  uint64_t d = 0;
  d |= (uint64_t)((a >> 16) & 0xFF) << 0;
  d |= (uint64_t)((a >>  8) & 0xFF) << 8;
  d |= (uint64_t)( a        & 0xFF) << 16;
  d |= (uint64_t)((b >> 16) & 0xFF) << 32;
  d |= (uint64_t)((b >>  8) & 0xFF) << 40;
  d |= (uint64_t)( b        & 0xFF) << 48;
  return d; }
// DISTINCT per (stream, wire channel, sample event) - the whole point: with a
// unique value in every channel, a crossed or duplicated L/R is visible in the
// emitted payload bytes rather than hidden behind two equal samples.
static uint32_t LBV(int s, int c, int e) {
  return 0x400000u | ((s & 7) << 12) | ((c & 0xF) << 4) | (e & 0xF); }

static uint32_t lb_chans_word = 0;
static void lb_set_chans(int s, int chans) {          // RX monitors' wire_chans
  lb_chans_word = (lb_chans_word & ~(0xFu << (s * 4)))
                | ((uint32_t)(chans & 0xF) << (s * 4));
  dut->lb_wire_chans_i = lb_chans_word; }

// one PDU: `events` sample events x `chans` channels, chronologically
// interleaved (IEEE 1722-2016 7.3.5). events*chans must be even (2 samples
// per beat, as the depacketizer emits full 8-byte beats).
static void drv_lb_pdu(int s, int chans, int events, int e0) {
  std::vector<uint32_t> smp;
  for (int e = 0; e < events; e++)
    for (int c = 0; c < chans; c++) smp.push_back(LBV(s, c, e0 + e));
  if (smp.size() & 1) { printf("  [FAIL] drv_lb_pdu odd sample count\n");
                        fails++; checks++; return; }
  dut->lb_tuser_i = s;
  for (size_t i = 0; i < smp.size(); i += 2) {
    dut->lb_tdata_i  = lb_beat(smp[i], smp[i + 1]);
    dut->lb_tvalid_i = 1;
    dut->lb_tlast_i  = (i + 2 >= smp.size());
    cyc(); }
  dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0; dut->lb_tdata_i = 0; cyc(2); }

// ---- media ticks (one full slot walk per tick; drain-friendly spacing) ---
//! Both wrappers elaborate N_SLOTS_P = 32 with GAP_CYC_P = 24, and EVERY slot
//! now injects (an unmapped one carries silence - Milan v1.2 5.3.7.3), so a
//! walk is 1 + 32*26 = 833 cycles whatever the map holds. The old 300/340
//! spacing only ever fitted because the sparsely mapped phases below skipped
//! 27 of the 32 slots in one cycle each; it was never the real grid, which is
//! MILAN_CLK_FREQ_HZ/48000 = 2083 cycles at 100 MHz (1041 at 50 MHz). WALK_C
//! is checked against that budget in [A4] rather than being restated there.
static const int WALK_C = 1 + 32 * (24 + 2);
static void a_tick() { dut->a_tick_i = 1; cyc(); dut->a_tick_i = 0; cyc(WALK_C + 60); }
static void b_tick() { dut->b_tick_i = 1; cyc(); dut->b_tick_i = 0; cyc(WALK_C + 100); }

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
  dut->clk_audio = 0; dut->tg_en_i = 0; dut->tg_tick_i = 0;
  dut->a_tready_i = 1; dut->b_tready_i = 1;
  dut->dest_mac_i = 0x91E0F000FE01ULL; dut->station_mac_i = 0x020000000002ULL;
  dut->vlan_vid_i = 2; dut->ptp_ns_i = 0x11223344; dut->transit_ns_i = 2000000;
  dut->i2s_pair_valid_i = 0; dut->tdm_pair_valid_i = 0; dut->ring_pair_valid_i = 0;
  dut->tone_smp_i = 0;
  dut->lb_tdata_i = 0; dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0;
  dut->lb_tuser_i = 0; dut->lb_wire_chans_i = 0;
  dut->a_map_wr_en_i = 0; dut->a_map_rd_en_i = 0; dut->a_tick_i = 0; dut->a_en_i = 0;
  dut->a_tctx_wr_en_i = 0; dut->a_tctx_rd_en_i = 0;
  dut->b_map_wr_en_i = 0; dut->b_map_rd_en_i = 0; dut->b_tick_i = 0; dut->b_en_i = 0;
  dut->b_tctx_wr_en_i = 0; dut->b_tctx_rd_en_i = 0;
  cyc(8); dut->rst_n = 1; cyc(4);

  printf("== KL_chan_map_capture (per-pair-slot TX source mux) ==\n");

  // ====================================================================== //
  // [R5] LEVEL L1 (binding) / oracle: the fabric's own accepted-beat strobe.
  // A loopback slot that is MAPPED but has never been FED emits 24'd0 - the
  // same bytes a working, quiet slot emits. On the AX7101 that is the whole
  // product's audio (the board routes no audio pins in either direction), so
  // "not connected" reading identically to "connected and silent" would make
  // an unwired integration indistinguishable from a quiet room. This section
  // must run FIRST, while the loopback AXIS has genuinely never been driven.
  printf("\n[R5] capability mask: mapped-but-UNFED != silence\n");
  ck("R5: at reset nothing is mapped and nothing has been fed",
     a_map_mask(0), 0);
  a_map_wr(31, ent_lb(1, 0, 0));       // slot 31: outside lane A's talkers
  ck("R5: a LOOP entry declares MAPPED while still UNFED",
     a_map_mask(0), 1);
  ck("R5: mask is global, readable at any entry address", a_map_mask(7), 1);
  a_map_wr(31, ent(0, 0, 0));          // clear it again
  ck("R5: removing the entry clears MAPPED (it is live, not sticky)",
     a_map_mask(0), 0);

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
  // An UNMAPPED slot is a SILENT channel, never a missing stream.            //
  //                                                                          //
  // Milan v1.2 5.3.9.1 says each channel of a Stream Output is "either not   //
  // mapped or mapped to a channel of an Audio Cluster", so leaving slot0     //
  // unmapped is a legal configuration. 5.3.7.3 says the PAAD "shall be       //
  // streaming AVTP packets" for as long as it is declaring Talker Advertise  //
  // and seeing a Listener Ready - with no STREAMING_WAIT to hide behind.     //
  // Those two together mean an unmapped channel owes the wire silence, and   //
  // owes it INSIDE a frame that still goes out.                              //
  //                                                                          //
  // The crossbar used to skip an unmapped slot with no pulse, and the        //
  // packetizer advances a talker's sample count per slot it is fed - so one  //
  // unmapped channel stalled the whole talker and t0 vanished from the wire. //
  // KL_pair_zero_fill exists to catch exactly that, but milan_datapath muxes //
  // it out of the packetizer's input whenever this crossbar is armed         //
  // (the pkt_pv_w bypass), so while CHMAP owns slot coverage nothing else    //
  // was covering it. This phase is the wire-level proof that it does now.    //
  // ====================================================================== //
  printf("\n[A3] unmapped slot = SILENCE, not absence: t0 keeps framing\n");
  a_map_wr(0, ent(0, 1, 0));   // slot0 unmapped (en=0), was I2S
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  ck("A3: BOTH talkers still frame", (long)afr.size(), 2);
  int k0 = find_len(afr, 90), k1 = find_len(afr, 234);
  ck("A3: t0 is still on the wire", k0 >= 0, 1);
  if (k0 >= 0) {
    ck("A3: t0 is still 2ch", afr[k0][36], 2);
    ck("A3: t0 unmapped pair0 is silence L", be(afr[k0], 42, 3), 0);
    ck("A3: t0 unmapped pair0 is silence R", be(afr[k0], 46, 3), 0);
    ck("A3: t0 seq advanced to 2 (it never stalled)", afr[k0][20], 2);
  } else { for (int k = 0; k < 4; k++) ck("A3 t0 content (skipped)", 0, 1); }
  if (k1 >= 0) {
    ck("A3: t1 is unaffected by t0's unmapped slot", afr[k1][36], 8);
    ck("A3: t1 seq advanced to 2", afr[k1][20], 2);
    ck("A3: t1 pair3 slot4 still RING1 L", be(afr[k1], 66, 3), RNG_L(1));
  } else { for (int k = 0; k < 3; k++) ck("A3 t1 content (skipped)", 0, 1); }
  //! slot0 is deliberately LEFT unmapped - [RB] below reads it back

  // ====================================================================== //
  // The walk got LONGER when unmapped slots stopped being free, so the      //
  // budget it has to fit in is now load-bearing: one whole walk must still  //
  // finish inside one media tick or a talker loses samples. Measured here   //
  // against the WORST map (every slot unmapped = every slot injected), then //
  // compared to the tightest real grid, MILAN_CLK_FREQ_HZ/48000 at 50 MHz.  //
  // ====================================================================== //
  printf("\n[A4] the full-coverage walk still fits one media tick\n");
  {
    std::vector<uint16_t> saved(32);
    for (int s = 0; s < 32; s++) { saved[s] = a_map_ent(s);
                                   a_map_wr(s, ent(0, 0, 0)); }
    cyc(4);
    afr.clear();
    //! count the injects of ONE walk and time it, then complete the 6-sample
    //! frame so the phases below stay on the frame boundary they expect
    long pulses = 0, span = 0;
    dut->a_tick_i = 1; cyc(); dut->a_tick_i = 0;
    for (int c = 0; c < WALK_C + 60; c++) {
      cyc();
      if (dut->a_pv_o) { pulses++; span = c + 1; }
    }
    ck("A4: an all-unmapped map injects every slot", pulses, 32);
    ck("A4: the walk finishes inside the declared WALK_C", span <= WALK_C, 1);
    //! 50 MHz is the tighter of the two shipping media grids; 100 MHz has
    //! twice the room. Derived from the divider, not restated: 50e6/48000.
    ck("A4: WALK_C fits the 50 MHz media tick", WALK_C < (50000000 / 48000), 1);
    for (int i = 0; i < 5; i++) a_tick();
    cyc(400);
    //! the whole point, at the wire: a board with NOTHING mapped still
    //! streams - every channel silent, no channel missing
    ck("A4: an all-unmapped board still frames BOTH talkers",
       (long)afr.size(), 2);
    int z0 = find_len(afr, 90), z1 = find_len(afr, 234);
    ck("A4: t0 still framed", z0 >= 0, 1);
    ck("A4: t1 still framed", z1 >= 0, 1);
    long nz = 0;
    for (auto& f : afr) for (size_t i = 42; i < f.size(); i++) if (f[i]) nz++;
    ck("A4: and every payload octet is silence", nz, 0);
    for (int s = 0; s < 32; s++) a_map_wr(s, saved[s]);
    cyc(4);
  }

  // ====================================================================== //
  // A Stream Output mapping is per STREAM CHANNEL (1722.1-2021 7.4.45 /     //
  // Milan v1.2 5.4.2.26 "at most one dynamic mapping per Stream Output's    //
  // channel") while this store is per PAIR SLOT, so "channel 2p+1 mapped,   //
  // channel 2p not" is a state a conformant controller can ask for with a   //
  // single-mapping ADD. en alone cannot express it: it either armed the     //
  // unmapped channel with the source's other half (audio on a channel       //
  // GET_AUDIO_MAP does not report) or silenced the mapped one. That is why  //
  // the entry carries half[13:12], and this is its wire-level proof.        //
  // ====================================================================== //
  printf("\n[A5] per-half enable: one channel of a slot mapped, one silent\n");
  {
    uint16_t save1 = a_map_ent(1);
    //! t1 pair0 = wire channels 0/1, payload offsets 42 (L) and 46 (R)
    a_map_wr(1, ent_half(HALF_L, 1, 2, 0));   // TDM idx0, L only
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    int h1 = find_len(afr, 234);
    ck("A5: t1 still frames with a half-armed slot", h1 >= 0, 1);
    if (h1 >= 0) {
      ck("A5: L half carries its source",   be(afr[h1], 42, 3), TDM_L(0));
      ck("A5: R half is DIGITAL SILENCE",   be(afr[h1], 46, 3), 0);
      ck("A5: the rest of the talker is untouched (pair1 L)",
         be(afr[h1], 50, 3), TDM_L(1));
    } else { for (int k = 0; k < 3; k++) ck("A5 L-only (skipped)", 0, 1); }
    ck("A5: readback shows half = L only", a_map_ent(1) >> 12, 2);

    a_map_wr(1, ent_half(HALF_R, 1, 2, 0));   // TDM idx0, R only
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    h1 = find_len(afr, 234);
    if (h1 >= 0) {
      ck("A5: L half is DIGITAL SILENCE",  be(afr[h1], 42, 3), 0);
      ck("A5: R half carries its source",  be(afr[h1], 46, 3), TDM_R(0));
    } else { for (int k = 0; k < 2; k++) ck("A5 R-only (skipped)", 0, 1); }
    ck("A5: readback shows half = R only", a_map_ent(1) >> 12, 1);

    //! the legacy meaning is preserved exactly: a writer that says nothing
    //! about halves (ent(), i.e. 0b11) still arms both
    a_map_wr(1, save1);
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    h1 = find_len(afr, 234);
    if (h1 >= 0) {
      ck("A5: restored entry carries BOTH halves L", be(afr[h1], 42, 3), TDM_L(0));
      ck("A5: restored entry carries BOTH halves R", be(afr[h1], 46, 3), TDM_R(0));
    } else { for (int k = 0; k < 2; k++) ck("A5 restore (skipped)", 0, 1); }
  }

  // ====================================================================== //
  printf("\n[A7] half-swap mux (USER 08-06): any half onto any parity\n");
  {
    uint16_t save1 = a_map_ent(1);
    //! full crisscross: both channels take the OTHER half of TDM pair 0
    a_map_wr(1, (uint16_t)(ent_half(HALF_BOTH, 1, 2, 0) | SWAP_BOTH));
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    int h1 = find_len(afr, 234);
    ck("A7: frames with a swapped slot", h1 >= 0, 1);
    if (h1 >= 0) {
      ck("A7: L position carries the R source", be(afr[h1], 42, 3), TDM_R(0));
      ck("A7: R position carries the L source", be(afr[h1], 46, 3), TDM_L(0));
    } else { for (int k = 0; k < 2; k++) ck("A7 crisscross (skipped)", 0, 1); }

    //! single-lane swap: L takes the R half, R stays natural = the
    //! "R-half cluster onto an even channel" ATDECC route
    a_map_wr(1, (uint16_t)(ent_half(HALF_BOTH, 1, 2, 0) | SWAP_L));
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    h1 = find_len(afr, 234);
    if (h1 >= 0) {
      ck("A7: swapped L lane = R source",  be(afr[h1], 42, 3), TDM_R(0));
      ck("A7: natural R lane = R source",  be(afr[h1], 46, 3), TDM_R(0));
    } else { for (int k = 0; k < 2; k++) ck("A7 single-swap (skipped)", 0, 1); }

    //! legacy writers (swap bits absent) keep the natural route bit-for-bit
    a_map_wr(1, save1);
    cyc(4);
    afr.clear();
    for (int i = 0; i < 6; i++) a_tick();
    cyc(400);
    h1 = find_len(afr, 234);
    if (h1 >= 0) {
      ck("A7: restored natural L", be(afr[h1], 42, 3), TDM_L(0));
      ck("A7: restored natural R", be(afr[h1], 46, 3), TDM_R(0));
    } else { for (int k = 0; k < 2; k++) ck("A7 restore (skipped)", 0, 1); }
  }

  // ====================================================================== //
  printf("\n[RB] map RAM readback port\n");
  ck("RB: slot1 = {en,TDM,0}",  a_map_ent(1), ent(1, 2, 0));
  ck("RB: slot3 = {en,ZERO,0}", a_map_ent(3), ent(1, 0, 0));
  ck("RB: slot4 = {en,RING,1}", a_map_ent(4), ent(1, 3, 1));
  ck("RB: slot0 = disabled",    a_map_ent(0), ent(0, 1, 0));

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

  // ====================================================================== //
  printf("\n[LB] rx -> talker LOOPBACK (src 5): a received stream's channel\n"
         "     pair feeds a talker pair slot, every RX channel DISTINCT\n");
  // wire channels_per_frame (7.3.3) as the RX monitors report them:
  //   s3, s5 = 8ch;  s2 = 3ch (ODD: sample events straddle the 2-sample
  //   beats, so the de-interleave cannot be beat-aligned by luck);
  //   s0 left at 0 = the pre-first-accept field, which must mean 2.
  lb_set_chans(3, 8); lb_set_chans(5, 8); lb_set_chans(2, 3);
  drv_lb_pdu(3, 8, 2, 1);    // stream 3: sample events e=1,2 -> latest e=2
  drv_lb_pdu(5, 8, 2, 3);    // stream 5: e=3,4              -> latest e=4
  drv_lb_pdu(0, 2, 6, 5);    // stream 0 (chans field 0 = 2) -> latest e=10
  drv_lb_pdu(2, 3, 4, 1);    // stream 2, 3 channels         -> latest e=4

  a_map_wr(0, ent_lb(1, 0, 0));   // t0 pair0 <- s0 ch0/ch1 (chans 0 -> 2)
  a_map_wr(1, ent_lb(1, 3, 0));   // t1 pair0 <- s3 ch0/ch1
  a_map_wr(2, ent_lb(1, 3, 1));   // t1 pair1 <- s3 ch2/ch3
  a_map_wr(3, ent_lb(1, 5, 3));   // t1 pair2 <- s5 ch6/ch7
  a_map_wr(4, ent_lb(1, 9, 0));   // t1 pair3 <- stream 9: out of range
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);

  // the other half of the R5 pair: once payload has actually arrived the mask
  // reads MAPPED+FED, so a zero sample from here on is real silence
  ck("LB: mask now reads MAPPED and FED", a_map_mask(0), 3);
  ck("LB: two frames (t0 + t1)", (long)afr.size(), 2);
  int l0 = find_len(afr, 90), l1 = find_len(afr, 234);
  if (l1 >= 0) {
    // pair p of the entry = wire channels {2p, 2p+1} = {L, R}, and the
    // packetizer emits pair p into the same two channels - identity round trip
    ck("LB: t1 ch0 = s3 ch0 (pair0 L)", be(afr[l1], 42, 3), LBV(3, 0, 2));
    ck("LB: t1 ch1 = s3 ch1 (pair0 R)", be(afr[l1], 46, 3), LBV(3, 1, 2));
    ck("LB: t1 ch2 = s3 ch2 (pair1 L)", be(afr[l1], 50, 3), LBV(3, 2, 2));
    ck("LB: t1 ch3 = s3 ch3 (pair1 R)", be(afr[l1], 54, 3), LBV(3, 3, 2));
    ck("LB: t1 ch4 = s5 ch6 (pair3 L)", be(afr[l1], 58, 3), LBV(5, 6, 4));
    ck("LB: t1 ch5 = s5 ch7 (pair3 R)", be(afr[l1], 62, 3), LBV(5, 7, 4));
    ck("LB: out-of-range stream = silence L", be(afr[l1], 66, 3), 0);
    ck("LB: out-of-range stream = silence R", be(afr[l1], 70, 3), 0);
    // the crossing/duplication oracle: four values from one PDU, all live,
    // all different - a swapped or duplicated half shows up here
    ck("LB: pair0 L != R (not duplicated)",
       be(afr[l1], 42, 3) != be(afr[l1], 46, 3), 1);
    ck("LB: pair1 L != R (not duplicated)",
       be(afr[l1], 50, 3) != be(afr[l1], 54, 3), 1);
    ck("LB: pair0 L != pair1 L (pair idx selects)",
       be(afr[l1], 42, 3) != be(afr[l1], 50, 3), 1);
    ck("LB: pair0 R != pair1 R (pair idx selects)",
       be(afr[l1], 46, 3) != be(afr[l1], 54, 3), 1);
    ck("LB: s5 pair L != R (not duplicated)",
       be(afr[l1], 58, 3) != be(afr[l1], 62, 3), 1);
  } else { for (int k = 0; k < 13; k++) ck("LB content (skipped)", 0, 1); }
  if (l0 >= 0) {
    ck("LB: t0 ch0 = s0 ch0 (chans field 0 -> 2)", be(afr[l0], 42, 3),
       LBV(0, 0, 10));
    ck("LB: t0 ch1 = s0 ch1 (chans field 0 -> 2)", be(afr[l0], 46, 3),
       LBV(0, 1, 10));
    ck("LB: t0 L != R", be(afr[l0], 42, 3) != be(afr[l0], 46, 3), 1);
  } else { for (int k = 0; k < 3; k++) ck("LB t0 (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[LB2] loopback remap + odd-channel de-interleave + a NEWER PDU\n");
  a_map_wr(1, ent_lb(1, 3, 3));   // t1 pair0 <- s3 ch6/ch7 (remap)
  a_map_wr(4, ent_lb(1, 2, 0));   // t1 pair3 <- s2 ch0/ch1 (3-channel stream)
  drv_lb_pdu(3, 8, 2, 5);         // stream 3 again: e=5,6 -> latest e=6
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int m1 = find_len(afr, 234);
  if (m1 >= 0) {
    ck("LB2: remapped pair0 L = s3 ch6", be(afr[m1], 42, 3), LBV(3, 6, 6));
    ck("LB2: remapped pair0 R = s3 ch7", be(afr[m1], 46, 3), LBV(3, 7, 6));
    ck("LB2: pair1 follows the NEWER PDU L", be(afr[m1], 50, 3), LBV(3, 2, 6));
    ck("LB2: pair1 follows the NEWER PDU R", be(afr[m1], 54, 3), LBV(3, 3, 6));
    ck("LB2: untouched stream 5 holds L", be(afr[m1], 58, 3), LBV(5, 6, 4));
    ck("LB2: untouched stream 5 holds R", be(afr[m1], 62, 3), LBV(5, 7, 4));
    ck("LB2: 3-ch stream ch0 (beats straddle events)", be(afr[m1], 66, 3),
       LBV(2, 0, 4));
    ck("LB2: 3-ch stream ch1 (beats straddle events)", be(afr[m1], 70, 3),
       LBV(2, 1, 4));
    ck("LB2: 3-ch pair L != R", be(afr[m1], 66, 3) != be(afr[m1], 70, 3), 1);
  } else { for (int k = 0; k < 9; k++) ck("LB2 content (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[LB3] a LOOP slot naming a stream nothing has sent = silence;\n"
         "      an UNMAPPED loop slot = silence too, never absence\n");
  a_map_wr(4, ent_lb(1, 7, 0));   // stream 7: in range, never fed
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int n1 = find_len(afr, 234);
  ck("LB3: t1 still emitted", n1 >= 0, 1);
  if (n1 >= 0) {
    ck("LB3: unfed stream = silence L", be(afr[n1], 66, 3), 0);
    ck("LB3: unfed stream = silence R", be(afr[n1], 70, 3), 0);
    ck("LB3: the other loop pairs still live", be(afr[n1], 42, 3),
       LBV(3, 6, 6));
  } else { for (int k = 0; k < 3; k++) ck("LB3 content (skipped)", 0, 1); }

  //! The unmapped LOOP slot is the same clause as [A3], reached down the
  //! loopback bucket instead of a physical one: 5.3.9.1 lets the channel be
  //! unmapped, 5.3.7.3 still owes the Stream Output its packets. Both
  //! talkers must survive, and t1's now-unmapped pair3 must read silence.
  a_map_wr(4, ent_lb(0, 3, 0));   // unmapped LOOP slot (en=0)
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  ck("LB3: unmapping a loop slot keeps BOTH talkers", (long)afr.size(), 2);
  int u1 = find_len(afr, 234), u0 = find_len(afr, 90);
  ck("LB3: t0 (2ch) survived", u0 >= 0 ? afr[u0][36] : -1, 2);
  ck("LB3: t1 (8ch) survived it too", u1 >= 0, 1);
  if (u1 >= 0) {
    ck("LB3: t1 unmapped pair3 is silence L", be(afr[u1], 66, 3), 0);
    ck("LB3: t1 unmapped pair3 is silence R", be(afr[u1], 70, 3), 0);
    ck("LB3: t1 mapped pair0 still carries loop audio",
       be(afr[u1], 42, 3), LBV(3, 6, 6));
  } else { for (int k = 0; k < 3; k++) ck("LB3 unmapped content (skipped)", 0, 1); }
  ck("LB3: readback carries the loop stream nibble", a_map_ent(2),
     ent_lb(1, 3, 1));
  ck("LB3: readback of the disabled loop slot", a_map_ent(4), ent_lb(0, 3, 0));

  // ====================================================================== //
  printf("\n[LB4] boundaries: last bank entry (s7 p3), a wire WIDER than the\n"
         "      kept channels (10ch: virtual channels are walked, not kept),\n"
         "      out-of-range pair index, and a no-duplicate scan\n");
  lb_set_chans(7, 8);
  drv_lb_pdu(7, 8, 2, 1);                 // stream 7 (max stream) -> e=2
  lb_set_chans(6, 10);                    // 7.3.3 says 10 channels on the wire
  drv_lb_pdu(6, 10, 2, 1);                // ch8/ch9 are VIRTUAL (N_LB_CH_P=8)
  a_map_wr(1, ent_lb(1, 6, 0));   // t1 pair0 <- s6 ch0/ch1 (10ch wire)
  a_map_wr(2, ent_lb(1, 6, 3));   // t1 pair1 <- s6 ch6/ch7 (last KEPT pair)
  a_map_wr(3, ent_lb(1, 7, 3));   // t1 pair2 <- s7 ch6/ch7 = bank entry 31
  a_map_wr(4, ent_lb(1, 3, 0));   // t1 pair3 <- s3 ch0/ch1
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int q1 = find_len(afr, 234);
  if (q1 >= 0) {
    ck("LB4: 10ch wire, ch0 kept", be(afr[q1], 42, 3), LBV(6, 0, 2));
    ck("LB4: 10ch wire, ch1 kept", be(afr[q1], 46, 3), LBV(6, 1, 2));
    ck("LB4: 10ch wire, ch6 (alignment survived ch8/ch9)",
       be(afr[q1], 50, 3), LBV(6, 6, 2));
    ck("LB4: 10ch wire, ch7 (alignment survived ch8/ch9)",
       be(afr[q1], 54, 3), LBV(6, 7, 2));
    ck("LB4: last bank entry s7 p3 L", be(afr[q1], 58, 3), LBV(7, 6, 2));
    ck("LB4: last bank entry s7 p3 R", be(afr[q1], 62, 3), LBV(7, 7, 2));
    ck("LB4: s3 pair0 L", be(afr[q1], 66, 3), LBV(3, 0, 6));
    ck("LB4: s3 pair0 R", be(afr[q1], 70, 3), LBV(3, 1, 6));
    // NO-DUPLICATION SCAN: eight live channels from four different (stream,
    // pair) sources - every one must be a different value. A slot that
    // duplicated its neighbour, or a bank read that ignored part of the
    // address, collapses two of these onto each other.
    long dup = 0;
    for (int a = 0; a < 8; a++)
      for (int b = a + 1; b < 8; b++)
        if (be(afr[q1], 42 + 4 * a, 3) == be(afr[q1], 42 + 4 * b, 3)) dup++;
    ck("LB4: all 8 emitted channels distinct (dup count)", dup, 0);
  } else { for (int k = 0; k < 9; k++) ck("LB4 content (skipped)", 0, 1); }

  // out-of-range PAIR index (kept channels = 8 -> pairs 0..3; 5 is not one)
  a_map_wr(3, ent_lb(1, 7, 5));
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int q2 = find_len(afr, 234);
  if (q2 >= 0) {
    ck("LB4: out-of-range pair = silence L", be(afr[q2], 58, 3), 0);
    ck("LB4: out-of-range pair = silence R", be(afr[q2], 62, 3), 0);
    ck("LB4: its neighbours are untouched L", be(afr[q2], 42, 3),
       LBV(6, 0, 2));
    ck("LB4: its neighbours are untouched R", be(afr[q2], 70, 3),
       LBV(3, 1, 6));
  } else { for (int k = 0; k < 4; k++) ck("LB4 range (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[LB6] WIRE TRUTH: the de-interleave follows the WIRE's\n"
         "      channels_per_frame (7.3.3), never the PDU's length. Stream 1\n"
         "      is left at the pre-first-accept field 0 = 2 channels, so a\n"
         "      PDU carrying 8 channels' worth of samples fills PAIR 0 ONLY\n");
  // (this check exists because the first draft of [LB4] forgot to set the
  // wire count for stream 7 and the DUT was RIGHT: it filled pair 0 and left
  // pairs 1..3 silent. Making that an assertion keeps the rule pinned.)
  drv_lb_pdu(1, 8, 2, 3);          // 16 samples, wire says 2 channels
  a_map_wr(1, ent_lb(1, 1, 0));    // t1 pair0 <- s1 pair0 (the only live one)
  a_map_wr(2, ent_lb(1, 1, 1));    // t1 pair1 <- s1 pair1 (never written)
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int w1 = find_len(afr, 234);
  if (w1 >= 0) {
    // with 2 wire channels the 16 samples land ch0,ch1,ch0,ch1... so the
    // LAST pair of samples in the PDU (values built for "channel 6/7") is
    // what pair 0 holds - position, not label, decides the channel
    ck("LB6: 2ch wire, pair0 L = last even sample", be(afr[w1], 42, 3),
       LBV(1, 6, 4));
    ck("LB6: 2ch wire, pair0 R = last odd sample", be(afr[w1], 46, 3),
       LBV(1, 7, 4));
    ck("LB6: pair0 L != R", be(afr[w1], 42, 3) != be(afr[w1], 46, 3), 1);
    ck("LB6: pair1 beyond the wire's channels = silence L",
       be(afr[w1], 50, 3), 0);
    ck("LB6: pair1 beyond the wire's channels = silence R",
       be(afr[w1], 54, 3), 0);
  } else { for (int k = 0; k < 5; k++) ck("LB6 (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[LB5] QUARANTINE: with NO loop entry in the map, loopback traffic\n"
         "      must not perturb one byte of the payload (the unselected-\n"
         "      source axiom - the feature off is the feature absent)\n");
  a_map_wr(0, ent(1, 1, 0));   // back to the [A] map exactly
  a_map_wr(1, ent(1, 2, 0));
  a_map_wr(2, ent(1, 2, 1));
  a_map_wr(3, ent(1, 3, 0));
  a_map_wr(4, ent(1, 4, 0));
  dut->tone_smp_i = TONE;
  drv_i2s(I2S_L, I2S_R);
  drv_tdm(0, TDM_L(0), TDM_R(0));
  drv_tdm(1, TDM_L(1), TDM_R(1));
  drv_ring(0, RNG_L(0), RNG_R(0));
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();     // loopback AXIS IDLE
  cyc(400);
  int r1 = find_len(afr, 234), r0 = find_len(afr, 90);
  Frame quiet1, quiet0;
  if (r1 >= 0) quiet1 = Frame(afr[r1].begin() + 42, afr[r1].end());
  if (r0 >= 0) quiet0 = Frame(afr[r0].begin() + 42, afr[r0].end());
  ck("LB5: quiet-run frames present", (r1 >= 0 && r0 >= 0), 1);

  for (int s = 0; s < 8; s++) {             // now hammer EVERY RX stream
    lb_set_chans(s, 8);
    drv_lb_pdu(s, 8, 2, 11);
  }
  cyc(4);
  afr.clear();
  for (int i = 0; i < 6; i++) a_tick();
  cyc(400);
  int r3 = find_len(afr, 234), r2 = find_len(afr, 90);
  if (r3 >= 0 && r2 >= 0) {
    Frame busy1(afr[r3].begin() + 42, afr[r3].end());
    Frame busy0(afr[r2].begin() + 42, afr[r2].end());
    ck("LB5: t1 payload byte-identical under loopback traffic",
       busy1 == quiet1, 1);
    ck("LB5: t0 payload byte-identical under loopback traffic",
       busy0 == quiet0, 1);
    ck("LB5: t1 payload is the [A] source set (TDM0 L still there)",
       be(afr[r3], 42, 3), TDM_L(0));
  } else { for (int k = 0; k < 3; k++) ck("LB5 (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[LBB] lane B: the loopback into the WIDENED slot 31 (t7 pair 3)\n");
  b_map_wr(31, ent_lb(1, 3, 2));   // t7 pair3 <- s3 ch4/ch5
  cyc(4);
  bfr.clear();
  for (int i = 0; i < 6; i++) b_tick();
  cyc(600);
  ck("LBB: one frame emitted (t7)", (long)bfr.size(), 1);
  if (bfr.size() == 1) {
    ck("LBB: slot31 loop L = s3 ch4", be(bfr[0], 66, 3), LBV(3, 4, 12));
    ck("LBB: slot31 loop R = s3 ch5", be(bfr[0], 70, 3), LBV(3, 5, 12));
    ck("LBB: slot31 loop L != R", be(bfr[0], 66, 3) != be(bfr[0], 70, 3), 1);
    ck("LBB: slot28 still I2S L (untouched)", be(bfr[0], 42, 3), I2S_L);
    ck("LBB: slot30 still RING0 L (untouched)", be(bfr[0], 58, 3), RNG_L(0));
  } else { for (int k = 0; k < 5; k++) ck("LBB content (skipped)", 0, 1); }

  // ====================================================================== //
  printf("\n[G] tone ONE-GRID contract: media-tick pacing vs clk_audio/512\n");
  // The 48-entry table, verbatim from KL_tone_gen (att = 0).
  static const uint32_t TAB[48] = {
      0x000000,0x10B515,0x2120FB,0x30FBC5,0x3FFFFF,0x4DEBE4,
      0x5A8279,0x658C99,0x6ED9EB,0x7641AE,0x7BA374,0x7EE7A9,
      0x7FFFFF,0x7EE7A9,0x7BA374,0x7641AE,0x6ED9EB,0x658C99,
      0x5A8279,0x4DEBE4,0x3FFFFF,0x30FBC5,0x2120FB,0x10B515,
      0x000000,0xEF4AEB,0xDEDF05,0xCF043B,0xC00001,0xB2141C,
      0xA57D87,0x9A7367,0x912615,0x89BE52,0x845C8C,0x811857,
      0x800001,0x811857,0x845C8C,0x89BE52,0x912615,0x9A7367,
      0xA57D87,0xB2141C,0xC00000,0xCF043B,0xDEDF05,0xEF4AEB };
  // Fractional-accumulator clock driver: one clk cycle per call, clk_audio
  // toggled whenever its (non-integer) half-period elapses - the two clocks
  // are INCOMMENSURATE, the real-silicon regime the lockstep harnesses
  // never model (and exactly why this defect escaped them).
  static double aud_acc = 0.0;
  auto gstep = [&](double aud_half) {
    dut->clk = 0; dut->eval();
    aud_acc += 0.5;
    while (aud_acc >= aud_half) {
      dut->clk_audio ^= 1; dut->eval(); aud_acc -= aud_half; }
    dut->clk = 1; dut->eval();
    aud_acc += 0.5;
    while (aud_acc >= aud_half) {
      dut->clk_audio ^= 1; dut->eval(); aud_acc -= aud_half; }
  };
  // media tick every TICKDIV clk; the legacy tone period is 512 audio
  // cycles = 1024 * aud_half clk, so aud_half = TICKDIV*(1 -+ eps)/1024
  // puts the legacy grid eps FASTER (phase 1: drops) then eps SLOWER
  // (phase 2: repeats) than the tick grid - the bench's 4-12 slips/s,
  // compressed to one slip every ~1/eps ticks.
  const int    TICKDIV = 520;
  const double EPS     = 0.004;
  const int    NTICK   = 3000;                 // per phase: ~12 slips
  dut->tg_en_i = 1;
  long med_mism = 0, med_ticks = 0, leg_offtab = 0;
  long leg_slip[2] = {0, 0}, leg_rep[2] = {0, 0}, leg_drop[2] = {0, 0};
  int  leg_idx = -1;
  for (int ph = 0; ph < 2; ph++) {
    const double aud_half =
        TICKDIV * (ph == 0 ? 1.0 - EPS : 1.0 + EPS) / 1024.0;
    for (int t = 0; t < NTICK; t++) {
      dut->tg_tick_i = 1; gstep(aud_half);
      dut->tg_tick_i = 0;
      for (int c = 0; c < TICKDIV - 1; c++) {
        gstep(aud_half);
        if (c == 3) {                          // sample well after the tick
          // media grid: EXACTLY one step per tick, no exceptions
          uint32_t vm = dut->tone_media_o;
          if (vm != TAB[med_ticks % 48]) med_mism++;
          med_ticks++;
          // legacy grid: track the walk, count slips (the crossbar's read)
          uint32_t vl = dut->tone_legacy_o;
          int f = -1;
          for (int k = 0; k < 48; k++) if (TAB[k] == vl) { f = k; break; }
          if (f < 0) { leg_offtab++; }
          else if (leg_idx < 0) { leg_idx = f; }
          else if (vl == TAB[(leg_idx + 1) % 48]) { leg_idx = (leg_idx + 1) % 48; }
          else {
            leg_slip[ph]++;
            if      (vl == TAB[leg_idx])            leg_rep[ph]++;
            else if (vl == TAB[(leg_idx + 2) % 48]) { leg_drop[ph]++;
                                                      leg_idx = (leg_idx + 2) % 48; }
            else                                    leg_idx = f;
          }
        }
      }
    }
  }
  printf("  [info] legacy grid, audio fast: %ld slips (%ld drops, %ld repeats)\n",
         leg_slip[0], leg_drop[0], leg_rep[0]);
  printf("  [info] legacy grid, audio slow: %ld slips (%ld drops, %ld repeats)\n",
         leg_slip[1], leg_drop[1], leg_rep[1]);
  ck("G: media grid = N table steps over N ticks", med_mism, 0);
  ck("G: media grid saw both drift phases", med_ticks, 2L * NTICK);
  ck("G: legacy tone never leaves the table", leg_offtab, 0);
  ck("G: NEG CONTROL fast audio grid slips (drops)", leg_slip[0] > 0, 1);
  ck("G: NEG CONTROL slow audio grid slips (repeats)", leg_slip[1] > 0, 1);

  printf("\n======================================================================\n");
  printf("KL_chan_map_capture: %ld checks, %ld failures\nRESULT: %s\n",
         checks, fails, fails ? "FAIL" : "PASS");
  delete dut;
  return fails ? 1 : 0;
}

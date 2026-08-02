// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_pcm_tx WIDE-SHAPE harness: the 8x8x8 ship shape (N_STREAMS_P=8,
// CHANS_P=8 => 4 pair slots per stream => 32 pair slots). Before the
// pair-slot bus was widened to 5 bits, slots 16..31 TRUNCATED onto 0..15:
// stream 4's pairs landed on stream 0's slot ids (and its hold state), so a
// high-stream playback silently corrupted a low one. This harness pins the
// widened space:
//   * a high stream (7) emits its own slots 28..31 - ids that cannot exist
//     on a 4-bit bus;
//   * streams 0 and 7 play CONCURRENTLY with distinct sample models and
//     neither sequence bleeds into the other's slots;
//   * a starved high stream repeats ITS OWN hold, not slot id mod 16's.
//
// Port shapes at this width: wr_ptr_i/rd_ptr_o are 256-bit (VlWide<8>,
// word s = stream s's 32-bit slice), underrun_o/overrun_o 128-bit
// (VlWide<4>, stream s at word s/2, half s&1).

#include "VKL_pcm_tx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_pcm_tx *dut;
static int pass = 0, fail = 0;

static const int      N          = 8;     // N_STREAMS_P
static const int      PAIRS      = 4;     // CHANS_P/2
static const uint32_t LEN        = 256;   // per-stream sub-ring bytes (32 words)
static const uint32_t STRIDE     = 4096;
static const int      SAMPLE_DIV = 64;    // room for the 32-slot walk

static std::vector<uint8_t> dram(STRIDE * N + LEN + 64, 0);
static uint32_t wrv[N]       = {0};
static uint32_t committed[N] = {0};

static uint32_t modelL(int s, uint32_t j) { return 0x400000u | (s << 16) | (j & 0xFFF); }
static uint32_t modelR(int s, uint32_t j) { return 0x500000u | (s << 16) | (j & 0xFFF); }

static void put_word(int s, uint32_t j, uint32_t L, uint32_t R) {
  uint32_t a = (uint32_t)s * STRIDE + (j * 8) % LEN;
  dram[a + 0] = (L >> 16) & 0xFF; dram[a + 1] = (L >> 8) & 0xFF;
  dram[a + 2] = L & 0xFF;         dram[a + 3] = 0x00;
  dram[a + 4] = (R >> 16) & 0xFF; dram[a + 5] = (R >> 8) & 0xFF;
  dram[a + 6] = R & 0xFF;         dram[a + 7] = 0x00;
}

static void feed_to(int s, uint32_t target) {
  for (uint32_t j = committed[s]; j < target; j++)
    put_word(s, j, modelL(s, j), modelR(s, j));
  if (target > committed[s]) committed[s] = target;
  wrv[s] = committed[s] * 8;
}

static uint64_t mem_word(uint32_t a) {
  uint64_t w = 0;
  for (int j = 0; j < 8; j++) w |= (uint64_t)dram[a + j] << (8 * j);
  return w;
}

// ---- wide-port accessors -------------------------------------------------
static uint32_t rd_of(int s)    { return dut->rd_ptr_o[s]; }
static uint32_t under_of(int s) { return (dut->underrun_o[s / 2] >> (16 * (s & 1))) & 0xFFFF; }
static void push_wr() { for (int s = 0; s < N; s++) dut->wr_ptr_i[s] = wrv[s]; }

static bool     mem_pend = false;
static uint32_t mem_addr = 0;
struct Pair { int slot; uint32_t l, r; };
static std::vector<Pair> caps;
static bool auto_feed = false;
static const int LEAD = 12;

static void tick() {
  dut->mem_valid_i = mem_pend ? 1 : 0;
  if (mem_pend) dut->mem_data_i = mem_word(mem_addr);
  push_wr();
  dut->clk_i = 0; dut->eval();
  bool req = dut->mem_rd_o; uint32_t a = dut->mem_addr_o;
  dut->clk_i = 1; dut->eval();
  mem_pend = req; mem_addr = a;
  if (dut->pair_valid_o)
    caps.push_back({(int)dut->pair_slot_o, (uint32_t)dut->pair_l_o, (uint32_t)dut->pair_r_o});
  if (auto_feed)
    for (int s = 0; s < N; s++)
      if (dut->stream_en_i & (1u << s)) feed_to(s, rd_of(s) / 8 + LEAD);
}
static void run(int n) { for (int i = 0; i < n; i++) tick(); }

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass++; printf("[PASS] %s\n", name); }
  else { fail++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                        (unsigned long long)got, (unsigned long long)want); }
}
static void ck_true(const char *name, bool c) { ck(name, c ? 1 : 0, 1); }

static void one_sample() {
  caps.clear();
  int guard = 0;
  while (!dut->smp_tick_o && guard++ < 4 * SAMPLE_DIV) tick();
  if (!dut->smp_tick_o) { fail++; printf("[FAIL] no media tick within window\n"); }
  run(SAMPLE_DIV - 2);
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_pcm_tx;

  dut->rst_n = 0;
  dut->enable_i = 0; dut->stream_en_i = 0; dut->underrun_silence_i = 0;
  dut->ring_base_i = 0; dut->ring_len_i = LEN; dut->ring_stride_i = STRIDE;
  dut->smp_tick_i = 0; dut->mem_valid_i = 0; dut->mem_data_i = 0;
  for (int s = 0; s < N; s++) dut->wr_ptr_i[s] = 0;
  run(4); dut->rst_n = 1; run(4);

  // ---- W1: stream 7 alone emits slot ids 28..31 (impossible on 4 bits) ---
  dut->enable_i = 1; dut->stream_en_i = 0x80;
  auto_feed = true;
  feed_to(7, LEAD);
  run(2);            // stream_en edge settles (clean-restart gate)
  one_sample();
  {
    bool ids_ok = ((int)caps.size() == PAIRS);
    bool high_ok = true;
    for (int p = 0; p < (int)caps.size(); p++) {
      if (caps[p].slot != 7 * PAIRS + p) ids_ok = false;
      if (caps[p].slot < 16) high_ok = false;
    }
    ck_true("W1 stream7 emits exactly its 4 pairs", (int)caps.size() == PAIRS);
    ck_true("W1 slot ids are 28..31 in order",      ids_ok);
    ck_true("W1 no id truncated below 16",          high_ok);
  }

  // ---- W2: streams 0 and 7 concurrent - sequences never cross ------------
  dut->stream_en_i = 0x81;
  feed_to(0, LEAD);
  run(2);
  uint32_t cw0 = 0, cw7 = rd_of(7) / 8;
  bool seq_ok = true, sets_ok = true;
  for (int m = 0; m < 20; m++) {
    one_sample();
    if ((int)caps.size() != 2 * PAIRS) sets_ok = false;
    for (auto &c : caps) {
      int t = c.slot / PAIRS;
      if (t != 0 && t != 7) { sets_ok = false; continue; }
      uint32_t j = (t == 0) ? cw0++ : cw7++;
      if (c.l != modelL(t, j) || c.r != modelR(t, j)) seq_ok = false;
    }
  }
  ck_true("W2 cadence: 8 pairs/sample over 2 streams", sets_ok);
  ck_true("W2 both sequences exact and un-crossed",    seq_ok);
  ck_true("W2 wrap exercised on both",  rd_of(0) > LEN && rd_of(7) > 2 * LEN);

  // ---- W3: starved stream 7 repeats ITS hold (index un-aliased) ----------
  {
    auto_feed = false;
    // drain: freeze the host pointers and let it catch up, note the last
    // real pair per stream-7 slot from a final fed sample
    for (int s : {0, 7}) { committed[s] = rd_of(s) / 8; wrv[s] = committed[s] * 8; }
    feed_to(7, committed[7] + PAIRS);      // one clean sample for stream 7
    push_wr();
    one_sample();
    uint32_t lp[PAIRS][2];
    for (auto &c : caps) if (c.slot / PAIRS == 7) {
      lp[c.slot % PAIRS][0] = c.l; lp[c.slot % PAIRS][1] = c.r;
    }
    uint32_t u7 = under_of(7);
    dut->underrun_silence_i = 0;           // repeat policy
    one_sample();
    bool rep_ok = true; int s7 = 0; bool tags_ok = true;
    for (auto &c : caps) {
      int t = c.slot / PAIRS;
      if (t == 7) {
        s7++;
        if (c.l != lp[c.slot % PAIRS][0] || c.r != lp[c.slot % PAIRS][1]) rep_ok = false;
      }
      // hold cross-contamination oracle: every repeated L carries its own
      // stream's model tag (modelL bits [19:16] = stream id) - a 4-bit
      // slot bus would have parked stream 7's samples in stream 0's holds
      if ((c.l >> 16) != (uint32_t)(0x40 + t)) tags_ok = false;
    }
    ck_true("W3 starved stream7 still emits its 4 slots", s7 == PAIRS);
    ck_true("W3 repeat uses stream7's own hold",          rep_ok);
    ck_true("W3 stream7 underruns counted",               under_of(7) > u7);
    ck_true("W3 holds carry their own stream's tag",      tags_ok);
  }

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  delete dut;
  return fail ? 1 : 0;
}

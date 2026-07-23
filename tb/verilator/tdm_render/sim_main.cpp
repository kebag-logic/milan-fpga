// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_tdm_render — the TDM8 OUTPUT serializer (item-4
// audio front-end family, output side; the symmetric twin of KL_tdm_capture).
//
// Strategy: the TB is the TDM bus MASTER. It drives bclk/fsync at the frame
// geometry (SLOTS x SLOT_BITS bclk/frame, one-bclk fsync pulse at slot 0),
// writes known per-slot samples on clk_i, then de-serializes tdm_dout_o with a
// GOLDEN model that samples exactly like KL_tdm_capture — rising-edge sample,
// edge-armed fsync, Philips-heritage DATA_DELAY_P=1 — and asserts the recovered
// slots bit-exact. A render(delay-1) driving a capture(delay-1) is a
// bit-transparent loopback, so the golden IS the acceptance oracle.
//
// Coverage: bit-exact slots (all 8), frame alignment after fsync, double-buffer
// latching (new tick vs mid-frame stability), pad bits zero, 24-bit sign
// preservation, a multi-frame run (9 data frames) and a stale/no-update frame
// that must repeat the last sample (underrun), plus the clk_i status counters.
#include "VKL_tdm_render.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <array>
#include <deque>
#include <vector>

static const int SLOTS        = 8;
static const int SLOT_BITS    = 32;
static const int FRAME_PERIODS= SLOTS * SLOT_BITS;   // 256 bclk / frame
static const int CPB          = 2;                   // clk_i cycles / bclk half

static VKL_tdm_render* dut;
static long checks = 0, fails = 0;
static void ck(const char* t, long got, long exp) {
  checks++;
  if (got != exp) { fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n", t, got, exp); }
  else            printf("  [ ok ] %-46s = %ld\n", t, got);
}
static void ckx(const char* t, unsigned long got, unsigned long exp) {
  checks++;
  if (got != exp) { fails++; printf("  [FAIL] %-46s got=0x%06lX exp=0x%06lX\n", t, got, exp); }
  else            printf("  [ ok ] %-46s = 0x%06lX\n", t, got);
}

// ---------------------------------------------------------------------------
// Golden de-serializer: a 1:1 model of KL_tdm_capture's rising-edge sampler
// (edge-armed fsync, startp pipeline = DATA_DELAY_P=1, MSB-first, top-24-of-32
// left-justified). last_word[] holds the full 32-bit slot words per frame.
// ---------------------------------------------------------------------------
static int      gv_fsync_q = 0, gv_armed = 0, gv_startp = 0, gv_run = 0;
static int      gv_slot = 0, gv_bit = 0;
static uint64_t gv_shift = 0;
static uint32_t rec_word[SLOTS];
static uint32_t last_word[SLOTS];
static long     golden_frames = 0;
static bool     golden_en = false;

static void golden_reset() {
  gv_fsync_q = gv_armed = gv_startp = gv_run = 0;
  gv_slot = gv_bit = 0; gv_shift = 0; golden_frames = 0;
  memset(rec_word, 0, sizeof(rec_word));
  memset(last_word, 0, sizeof(last_word));
}

static void golden_rising(int f, int d) {
  int start = (f && !gv_fsync_q && gv_armed) ? 1 : 0;
  int sol   = gv_startp;                 // DATA_DELAY_P=1: previous edge's start
  int eslot = sol ? 0 : gv_slot;
  int ebit  = sol ? 0 : gv_bit;
  if (gv_run || sol) {
    gv_run   = 1;
    gv_shift = (gv_shift << 1) | (uint64_t)(d & 1);
    if (ebit == SLOT_BITS - 1) {
      rec_word[eslot] = (uint32_t)(gv_shift & 0xFFFFFFFFULL);  // {sample,8'b0}
      if (eslot == SLOTS - 1) {
        memcpy(last_word, rec_word, sizeof(rec_word));
        golden_frames++;
      }
      gv_bit  = 0;
      gv_slot = (eslot == SLOTS - 1) ? 0 : eslot + 1;
    } else {
      gv_bit  = ebit + 1;
      gv_slot = eslot;
    }
  }
  gv_fsync_q = f;
  if (!f) gv_armed = 1;
  gv_startp = start;
}

// ---------------------------------------------------------------------------
// Clock drivers. clk_i and tdm_bclk_i are toggled independently so the
// gray-pointer cdc_pair_fifo crossing is exercised for real.
// ---------------------------------------------------------------------------
static void clk_tick() { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }

// one bclk period; the render drives data on the FALLING edge, so tdm_dout_o
// sampled just after the RISING-edge eval is the bit for this period (exactly
// how KL_tdm_capture reads it).
static void bperiod(int fsync_level) {
  dut->tdm_fsync_i = fsync_level;
  dut->tdm_bclk_i = 1; dut->eval();
  if (golden_en) golden_rising(fsync_level, dut->tdm_dout_o & 1);
  for (int i = 0; i < CPB; i++) clk_tick();
  dut->tdm_bclk_i = 0; dut->eval();
  for (int i = 0; i < CPB; i++) clk_tick();
}

// slot-indexed writes then a one-cycle tick_i commit (bclk held static).
static void write_frame(const uint32_t s[SLOTS]) {
  for (int i = 0; i < SLOTS; i++) {
    dut->smp_wr_slot_i = i; dut->smp_wr_data_i = s[i] & 0xFFFFFF;
    dut->smp_wr_en_i = 1; clk_tick();
  }
  dut->smp_wr_en_i = 0; clk_tick();
  dut->tick_i = 1; clk_tick(); dut->tick_i = 0; clk_tick();
}

// ---------------------------------------------------------------------------
struct Entry { uint32_t s[SLOTS]; bool underrun; bool detailed; const char* name; };

static uint32_t samp(int slot, int seq) {
  uint32_t v = ((uint32_t)(seq * 8 + slot) * 2654435u) & 0x7FFFFFu;  // 23-bit spread
  if ((slot ^ seq) & 1) v |= 0x800000u;                              // sign variety
  return v & 0xFFFFFFu;
}

static std::deque<Entry> exq;

static void check_frame(const Entry& e) {
  bool all_ok = true, pad_ok = true;
  for (int s = 0; s < SLOTS; s++) {
    uint32_t rec = (last_word[s] >> 8) & 0xFFFFFF;
    if (rec != (e.s[s] & 0xFFFFFF)) all_ok = false;
    if ((last_word[s] & 0xFF) != 0)  pad_ok = false;
  }
  if (e.detailed) {
    for (int s = 0; s < SLOTS; s++) {
      char buf[80]; snprintf(buf, sizeof(buf), "%s slot%d bit-exact", e.name, s);
      ckx(buf, (last_word[s] >> 8) & 0xFFFFFF, e.s[s] & 0xFFFFFF);
    }
    ck("EDGE: all pad bits zero (24-in-32)", pad_ok ? 1 : 0, 1);
    ckx("EDGE: sign preserved slot0 0x800000", (last_word[0] >> 8) & 0xFFFFFF, 0x800000);
    ckx("EDGE: sign preserved slot2 0xFFFFFF", (last_word[2] >> 8) & 0xFFFFFF, 0xFFFFFF);
  } else {
    char buf[80]; snprintf(buf, sizeof(buf), "%s: 8 slots bit-exact", e.name);
    ck(buf, all_ok ? 1 : 0, 1);
    snprintf(buf, sizeof(buf), "%s: pad bits zero", e.name);
    ck(buf, pad_ok ? 1 : 0, 1);
    if (e.underrun) {
      ck("stale frame REPEATS last sample (bit-exact)", all_ok ? 1 : 0, 1);
      ck("underruns_o incremented", dut->underruns_o, 1);
    }
  }
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_tdm_render;

  dut->clk_i = 0; dut->rst_n = 0;
  dut->smp_wr_en_i = 0; dut->smp_wr_slot_i = 0; dut->smp_wr_data_i = 0;
  dut->tick_i = 0; dut->tdm_bclk_i = 0; dut->tdm_fsync_i = 0;
  dut->eval();

  printf("== KL_tdm_render harness (TDM8 out: %d slots x %d bclk, 48 kHz frame) ==\n",
         SLOTS, SLOT_BITS);

  // reset both domains (golden idle)
  golden_en = false;
  for (int i = 0; i < 8; i++) bperiod(0);
  dut->rst_n = 1;
  for (int i = 0; i < 4; i++) bperiod(0);
  golden_reset(); golden_en = true;

  // ---- build the frame program -------------------------------------------
  std::vector<Entry> entries;
  { Entry e{{0x800000,0x7FFFFF,0xFFFFFF,0x000001,0xABCDEF,0x123456,0x000000,0xA5A5A5},
            false, true, "EDGE"}; entries.push_back(e); }
  int seqs[] = {1, 2};                       // idx1, idx2
  for (int q : seqs) { Entry e{}; for (int s = 0; s < SLOTS; s++) e.s[s] = samp(s, q);
    e.underrun = false; e.detailed = false; e.name = (q == 1) ? "F1(mid-frame-stable)" : "F2";
    entries.push_back(e); }
  { Entry e = entries.back(); e.underrun = true; e.detailed = false; e.name = "UNDERRUN(=F2)";
    entries.push_back(e); }                  // idx3: repeats F2 (its .s already = F2)
  int seqs2[] = {4, 5, 6, 7, 8, 9};          // idx4..idx9  (multi-frame run)
  for (int q : seqs2) { Entry e{}; for (int s = 0; s < SLOTS; s++) e.s[s] = samp(s, q);
    e.underrun = false; e.detailed = false;
    static char nm[6][8]; snprintf(nm[q-4], 8, "F%d", q); e.name = nm[q-4];
    entries.push_back(e); }
  { Entry e{}; for (int s = 0; s < SLOTS; s++) e.s[s] = 0x0F0F00u + s;
    e.underrun = false; e.detailed = false; e.name = "SENTINEL"; entries.push_back(e); }
  const int N = (int)entries.size();

  // ---- preload entry 0, arm + cross into the bclk domain -----------------
  write_frame(entries[0].s);
  exq.push_back(entries[0]);
  for (int i = 0; i < 12; i++) bperiod(0);          // fsync low: arm + prefetch

  printf("\n[align] nothing serialized before the first fsync\n");
  ck("no golden frame before fsync", golden_frames, 0);
  ck("line idle (dout=0) before fsync", dut->tdm_dout_o & 1, 0);

  printf("\n[run] fsync-aligned frames; golden recovers each after its boundary\n");
  long prev_gf = 0;
  int  calls = 0;
  for (int i = 0; i < N; i++) {
    for (int p = 0; p < FRAME_PERIODS; p++) {
      bperiod(p == 0 ? 1 : 0);                       // one-bclk fsync at slot 0
      if (p == 4 && i + 1 < N) {                     // commit the NEXT frame mid-frame
        if (!entries[i + 1].underrun) write_frame(entries[i + 1].s);
        exq.push_back(entries[i + 1]);               // (underrun: repeat, no commit)
      }
    }
    calls++;
    if (golden_frames > prev_gf) {                   // one frame completes per call
      prev_gf = golden_frames;
      Entry e = exq.front(); exq.pop_front();
      check_frame(e);
    }
  }

  printf("\n[status] clk_i-domain plain counters\n");
  ck("frames_o == fsync frames issued", dut->frames_o, calls);
  ck("underruns_o == 1 (single stale frame)", dut->underruns_o, 1);
  ck("overruns_o == 0 (consumer kept up)", dut->overruns_o, 0);
  ck("golden completed >= 9 frames", golden_frames >= 9 ? 1 : 0, 1);

  printf("\n======================================================================\n");
  printf("KL_tdm_render: %ld checks, %ld failures\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  delete dut;
  return fails ? 1 : 0;
}

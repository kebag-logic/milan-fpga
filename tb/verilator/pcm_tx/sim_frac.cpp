// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_pcm_tx FRACTIONAL media-clock leg — the SHIPPING ratio, not a toy one.
//
// WHY THIS LEG EXISTS (bench 2026-08-03): the playback sample tick was a
// FLOORED integer divider, SAMPLE_DIV_C = clk_hz / f_s. At the 100 MHz
// shipping datapath 100e6/48000 = 2083.333..., floored to 2083, so the media
// clock ran at 100e6/2083 = 48,007.6812 Hz — +160 ppm FAST. That is 3.2x over
// the +/-50 ppm bound Milan v1.2 §7.4 places on a media clock domain's
// oscillator, and it was measured on the wire as avtp_timestamp deltas of
// 124,980 ns instead of 125,000 (274,535 frames, sd 0.1 ns — dead steady, so
// unmistakably a ratio error and not jitter).
//
// Nothing in the suite elaborated a divider whose ratio was NOT a whole
// number, which is exactly why a truncation survived: every existing leg uses
// SAMPLE_DIV_C 32 or 64, where the remainder is 0 and the bug is invisible.
//
// THE CHECK IS EXACTNESS, NOT CLOSENESS. 100e6/48000 = 6250 clocks per 3
// samples with zero remainder, so over any whole number of 6250-clock groups
// the tick count must be EXACT. 10,000,000 clocks = 1600 groups = 4800 ticks.
// A floored divider yields 4801 over the same window (+160 ppm) — one extra
// tick is the entire defect, and this harness fails on it.

#include "VKL_pcm_tx.h"
#include "verilated.h"
#include <cstdio>
#include <map>

static VKL_pcm_tx *dut;
static vluint64_t  main_time = 0;

static void tick_clk() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  main_time++;
}

static int fails = 0;
static void check(bool ok, const char *msg) {
  printf("[%s] %s\n", ok ? "PASS" : "FAIL", msg);
  if (!ok) fails++;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_pcm_tx;

  // the pace divider is independent of the ring: hold every ring input quiet
  dut->enable_i = 0;
  dut->stream_en_i = 0;
  dut->underrun_silence_i = 0;
  dut->ring_base_i = 0;
  dut->ring_len_i = 0;
  dut->ring_stride_i = 0;
  dut->wr_ptr_i = 0;
  dut->smp_tick_i = 0;
  dut->mem_data_i = 0;
  dut->mem_valid_i = 0;

  dut->rst_n = 0;
  for (int i = 0; i < 8; i++) tick_clk();
  dut->rst_n = 1;

  // settle out of reset so the first measured period is a full one
  while (!dut->smp_tick_o) tick_clk();

  const long CLOCKS = 10000000L;          // 1600 groups of 6250
  const long EXPECT = 4800L;              // 48000 Hz * 0.1 s
  long ticks = 0, last = 0;
  std::map<long, long> hist;
  for (long c = 0; c < CLOCKS; c++) {
    tick_clk();
    if (dut->smp_tick_o) {
      if (ticks > 0) hist[(long)main_time - last]++;
      last = (long)main_time;
      ticks++;
    }
  }

  printf("  %ld clocks -> %ld ticks (expected exactly %ld)\n", CLOCKS, ticks, EXPECT);
  printf("  implied rate = %.4f Hz at 100 MHz (nominal 48000)\n",
         100e6 * (double)ticks / (double)CLOCKS);
  for (auto &kv : hist)
    printf("  period %ld clocks x %ld\n", kv.first, kv.second);

  check(ticks == EXPECT,
        "fractional divider emits EXACTLY 48 kHz over a whole ratio period");

  // only the two adjacent periods may appear, and 2084 exactly one third
  bool only_two = true;
  long n2083 = 0, n2084 = 0;
  for (auto &kv : hist) {
    if (kv.first == 2083) n2083 = kv.second;
    else if (kv.first == 2084) n2084 = kv.second;
    else only_two = false;
  }
  check(only_two, "period is only ever 2083 or 2084 clocks (no long tick)");
  check(n2084 > 0 && n2083 > 0, "both periods are actually exercised");
  // 100e6 = 2083*2 + 2084 per 3 samples -> 2084 is exactly 1 in 3
  check(n2084 * 2 == n2083 || n2084 * 2 == n2083 + 1 || n2084 * 2 + 1 == n2083,
        "2084 lands exactly one sample in three (Bresenham ratio held)");

  printf("\n%d checks: %d PASS, %d FAIL\n", 4, 4 - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

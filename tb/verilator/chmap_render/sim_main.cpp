// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_chan_map_render harness: drive a depacketizer-clone AXIS (64-bit beats =
// 2 consecutive S32BE samples, wire-interleaved payload, tuser = stream, tlast
// per PDU) with recognizable per-sample ramps whose 24-bit value encodes
// {s[3:0], c[3:0], seq[15:0]}. Program identity / permuted / cross-stream /
// unmapped maps and assert BYTE-EXACT routing on the phys outputs at each
// 48 kHz tick. Also proves the glitch-free contract: both the map RAM AND the
// free-running cur_r latch are only ever sampled onto the outputs at a tick
// (old value until tick, new after), plus tlast beat-realignment across
// back-to-back PDUs of different (even/odd) channel counts, and pad-byte drop.
#include "VKL_chan_map_render.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static VKL_chan_map_render* dut;
static long checks = 0, fails = 0;

static void ck(const char* w, uint32_t got, uint32_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("  [FAIL] %-34s got=0x%06x exp=0x%06x\n", w, got, exp);
  }
}

static void step() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
}

// 24-bit sample payload = {s[3:0], c[3:0], seq[15:0]}
static uint32_t value(int s, int c, int seq) {
  return (((uint32_t)(s & 0xF)) << 20) | (((uint32_t)(c & 0xF)) << 16) |
         ((uint32_t)(seq & 0xFFFF));
}

// pack two 24-bit samples (+ their pad bytes) into a wire-order S32BE beat:
// lane j = wire byte j; sample byte 0 = MSB; lane 3/7 = pad (must be dropped).
static uint64_t beat(uint32_t v0, uint8_t p0, uint32_t v1, uint8_t p1) {
  uint64_t b = 0;
  b |= (uint64_t)((v0 >> 16) & 0xFF) << 0;
  b |= (uint64_t)((v0 >> 8) & 0xFF) << 8;
  b |= (uint64_t)(v0 & 0xFF) << 16;
  b |= (uint64_t)p0 << 24;
  b |= (uint64_t)((v1 >> 16) & 0xFF) << 32;
  b |= (uint64_t)((v1 >> 8) & 0xFF) << 40;
  b |= (uint64_t)(v1 & 0xFF) << 48;
  b |= (uint64_t)p1 << 56;
  return b;
}

static void set_chans(const int c[8]) {
  uint32_t v = 0;
  for (int s = 0; s < 8; s++) v |= ((uint32_t)(c[s] & 0xF)) << (s * 4);
  dut->wire_chans_i = v;
}

// drive one AAF PDU: C channels, 6 samples/channel (Milan 48k), 2 samples/beat.
// sample k -> channel k%C, within-channel seq k/C (0..5); tag offsets seq so
// each frame's latched values (seq 5 -> tag+5) are distinguishable.
static void drive_frame(int s, int C, int tag, bool deassert = true) {
  int nbeats = (6 * C) / 2;  // = 3*C, always whole (6*C even)
  for (int b = 0; b < nbeats; b++) {
    int k0 = 2 * b, k1 = 2 * b + 1;
    uint32_t v0 = value(s, k0 % C, tag + k0 / C);
    uint32_t v1 = value(s, k1 % C, tag + k1 / C);
    dut->s_tdata_i  = beat(v0, 0xAA, v1, 0x55);  // nonzero pad -> must drop
    dut->s_tvalid_i = 1;
    dut->s_tuser_i  = s;
    dut->s_tlast_i  = (b == nbeats - 1) ? 1 : 0;
    step();
  }
  if (deassert) { dut->s_tvalid_i = 0; dut->s_tlast_i = 0; }
}

static void wr_map(int p, int en, int s, int c) {
  dut->map_wr_en_i   = 1;
  dut->map_wr_addr_i = p;
  dut->map_wr_data_i = ((en & 1) << 7) | ((s & 7) << 3) | (c & 7);
  step();
  dut->map_wr_en_i = 0;
}

static void do_tick() {
  dut->s_tvalid_i = 0;   // cur_r frozen while we sample it onto the outputs
  dut->tick_i = 1; step();
  dut->tick_i = 0;       // phys_smp_o / phys_valid_o now hold this frame
}

static uint32_t phys(int p) {
  int lo = p * 24, wi = lo >> 5, off = lo & 31;
  uint64_t w = (uint64_t)dut->phys_smp_o[wi] |
               ((uint64_t)dut->phys_smp_o[wi + 1] << 32);
  return (uint32_t)((w >> off) & 0xFFFFFF);
}

static uint8_t rd_map(int p) {
  dut->map_rd_addr_i = p; dut->eval();
  return dut->map_rd_data_o;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_chan_map_render;

  // ---- reset ----
  dut->rst_n = 0; dut->s_tvalid_i = 0; dut->s_tlast_i = 0; dut->s_tuser_i = 0;
  dut->tick_i = 0; dut->map_wr_en_i = 0; dut->map_wr_addr_i = 0;
  dut->map_wr_data_i = 0; dut->map_rd_addr_i = 0; dut->s_tdata_i = 0;
  int chans[8] = {2, 8, 2, 3, 2, 2, 2, 2};
  set_chans(chans);
  for (int i = 0; i < 6; i++) step();
  dut->rst_n = 1;

  printf("== KL_chan_map_render ==\n");

  // ================================================================
  // Phase 1: latch 4 streams, program the default identity map
  //   (I2S L/R = phys0/1 <- stream0; TDM8 slots = phys2..9 <- stream1)
  // ================================================================
  drive_frame(0, 2, 0x100);   // cur[0][c] = value(0,c,0x105)
  drive_frame(1, 8, 0x200);   // cur[1][c] = value(1,c,0x205)
  drive_frame(2, 2, 0x300);   // cur[2][c] = value(2,c,0x305)
  drive_frame(3, 3, 0x400);   // cur[3][c] = value(3,c,0x405)  (odd straddle)

  wr_map(0, 1, 0, 0); wr_map(1, 1, 0, 1);
  for (int p = 2; p < 10; p++) wr_map(p, 1, 1, p - 2);   // stream1 ch0..7
  do_tick();
  ck("id.phys_valid", dut->phys_valid_o, 1);
  ck("id.mask", dut->mapped_mask_o, 0x3FF);
  ck("id.phys0 s0c0", phys(0), value(0, 0, 0x105));
  ck("id.phys1 s0c1", phys(1), value(0, 1, 0x105));
  for (int c = 0; c < 8; c++)
    ck("id.phys s1", phys(2 + c), value(1, c, 0x205));
  ck("id.rdmap0", rd_map(0), (1 << 7) | (0 << 3) | 0);
  ck("id.rdmap9", rd_map(9), (1 << 7) | (1 << 3) | 7);
  // phys_valid is a one-cycle pulse
  dut->tick_i = 0; step();
  ck("id.valid_pulse_clears", dut->phys_valid_o, 0);

  // ================================================================
  // Phase 2: permuted (reverse stream1) + cross to stream2
  // ================================================================
  wr_map(0, 1, 2, 0); wr_map(1, 1, 2, 1);
  for (int p = 2; p < 10; p++) wr_map(p, 1, 1, 9 - p);   // ch7..0 reversed
  do_tick();
  ck("perm.phys0 s2c0", phys(0), value(2, 0, 0x305));
  ck("perm.phys1 s2c1", phys(1), value(2, 1, 0x305));
  for (int p = 2; p < 10; p++)
    ck("perm.phys s1rev", phys(p), value(1, 9 - p, 0x205));

  // ================================================================
  // Phase 3: full cross-stream incl. odd stream3, and a duplicated source
  //          (phys0 and phys9 both point at stream3 ch0)
  // ================================================================
  int ms[10] = {3, 3, 3, 0, 0, 1, 2, 2, 1, 3};
  int mc[10] = {0, 1, 2, 0, 1, 3, 0, 1, 0, 0};
  int mtag[10] = {0x405, 0x405, 0x405, 0x105, 0x105,
                  0x205, 0x305, 0x305, 0x205, 0x405};
  for (int p = 0; p < 10; p++) wr_map(p, 1, ms[p], mc[p]);
  do_tick();
  for (int p = 0; p < 10; p++)
    ck("cross.phys", phys(p), value(ms[p], mc[p], mtag[p]));

  // ================================================================
  // Phase 4: unmapped (en=0) channels render 0; mask tracks live en bits
  // ================================================================
  for (int p = 3; p < 10; p++) wr_map(p, 0, 0, 0);
  do_tick();
  ck("unmap.mask", dut->mapped_mask_o, 0x007);
  ck("unmap.phys0", phys(0), value(3, 0, 0x405));
  ck("unmap.phys1", phys(1), value(3, 1, 0x405));
  ck("unmap.phys2", phys(2), value(3, 2, 0x405));
  for (int p = 3; p < 10; p++) ck("unmap.zero", phys(p), 0);

  // ================================================================
  // Phase 5a: cur_r free-runs, but a mapped output only changes at a tick
  // ================================================================
  wr_map(0, 1, 0, 0); do_tick();
  ck("free.baseline", phys(0), value(0, 0, 0x105));
  drive_frame(0, 2, 0x700);          // cur[0][0] now value(0,0,0x705), NO tick
  ck("free.frozen_no_tick", phys(0), value(0, 0, 0x105));  // still old
  do_tick();
  ck("free.after_tick", phys(0), value(0, 0, 0x705));      // now new

  // ================================================================
  // Phase 5b: a map rewrite is likewise frozen until the next tick
  // ================================================================
  wr_map(1, 1, 1, 0); do_tick();
  ck("remap.baseline", phys(1), value(1, 0, 0x205));
  wr_map(1, 1, 2, 1);                 // repoint phys1, NO tick
  ck("remap.frozen_no_tick", phys(1), value(1, 0, 0x205));  // still old route
  do_tick();
  ck("remap.after_tick", phys(1), value(2, 1, 0x305));      // new route

  // ================================================================
  // Phase 6: tlast beat-realignment across back-to-back PDUs of different
  //          channel counts (8 -> 3 odd -> 2) with tvalid never dropping.
  //          If the tlast reset failed, the odd 3ch frame would drag chpos
  //          into the following frames and corrupt the embedded ch field.
  // ================================================================
  drive_frame(1, 8, 0xA00, /*deassert=*/false);
  drive_frame(3, 3, 0xB00, /*deassert=*/false);
  drive_frame(0, 2, 0xC00, /*deassert=*/true);
  wr_map(0, 1, 1, 7); wr_map(1, 1, 3, 0); wr_map(2, 1, 3, 1);
  wr_map(3, 1, 3, 2); wr_map(4, 1, 0, 0); wr_map(5, 1, 0, 1);
  for (int p = 6; p < 10; p++) wr_map(p, 0, 0, 0);
  do_tick();
  ck("b2b.s1c7", phys(0), value(1, 7, 0xA05));
  ck("b2b.s3c0", phys(1), value(3, 0, 0xB05));
  ck("b2b.s3c1", phys(2), value(3, 1, 0xB05));
  ck("b2b.s3c2", phys(3), value(3, 2, 0xB05));
  ck("b2b.s0c0", phys(4), value(0, 0, 0xC05));
  ck("b2b.s0c1", phys(5), value(0, 1, 0xC05));

  printf("%ld checks, %ld failures, RESULT: %s\n", checks, fails,
         fails ? "FAIL" : "PASS");
  delete dut;
  return fails ? 1 : 0;
}

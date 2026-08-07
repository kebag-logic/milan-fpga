// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// END-TO-END item-7 PLAYBACK harness - the mirror of the proven record path.
//
// Host PCM ring words go IN through the word-fetch port (a C++ DRAM model),
// and the serialized DAC output is decoded OUT at the far end and compared
// BIT-EXACTLY against the words that were written. Chain under test:
//
//   host ring -> KL_pcm_tx -> KL_chan_map_render (playback source, map
//   src=1) -> KL_i2s_feed_mux -> KL_i2s_playback -> i2s_sdin_o
//
// The I2S receiver below is derived from the IEEE/Philips I2S bus spec, NOT
// from the DUT's serializer or from the existing chip models (a double
// Philips delay once made silicon playback sign-squared while every TB model
// carried the same double delay and agreed with the bug):
//
//   * SCK: the transmitter changes SD on the FALLING edge, the receiver
//     samples SD on the RISING edge.
//   * WS (LRCK) changes one SCK period BEFORE the MSB of the new word;
//     WS low = left channel, WS high = right.
//   * therefore, at the first RISING edge where WS differs from the previous
//     rising edge's WS, the line still carries the tail of the PREVIOUS word.
//     The MSB lands on the NEXT rising edge. A 24-bit word is the 24 rising
//     edges following the WS-change edge, MSB first.
//
// Clocks are event-scheduled in picoseconds: clk 50 MHz, clk_audio 25 MHz
// with a deliberate phase offset (independent MMCM outputs on silicon). With
// TICK_DIV_P = 1024 the media grid is 50e6/1024 = 48828.125 Hz and the DAC
// frame rate is 25e6/512 = 48828.125 Hz - the SAME rate, so a mismatch in
// the chain shows as a data error and never as an unavoidable rate slip.

#include "Vpcm_playback_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vpcm_playback_wrap *dut;
static long pass_n = 0, fail_n = 0;

static void ck(const char *name, uint64_t got, uint64_t want) {
  if (got == want) { pass_n++; printf("[PASS] %s\n", name); }
  else { fail_n++; printf("[FAIL] %s: got 0x%llx want 0x%llx\n", name,
                         (unsigned long long)got, (unsigned long long)want); }
}
static void ck_true(const char *name, bool c) { ck(name, c ? 1 : 0, 1); }

// ---- build-time config (must match the Makefile -G flags) ----------------
static const int      N        = 2;        // N_STREAMS_P
static const uint32_t LEN      = 256;      // per-stream sub-ring bytes (32 wd)
static const uint32_t STRIDE   = 4096;     // bytes between sub-ring bases
static const int      TICK_DIV = 1024;     // clk cycles per media frame

// ---- host ring model (physical bytes the SoC read shim would fetch) ------
static std::vector<uint8_t> dram(STRIDE * N + LEN + 64, 0);
static uint32_t wrv[N]       = {0, 0};     // per-stream absolute write pointer
static uint32_t committed[N] = {0, 0};     // words already written

// distinct 24-bit samples per (stream, absolute word index)
static uint32_t modelL(int s, uint32_t j) { return 0x100000u | (s << 12) | (j & 0xFFF); }
static uint32_t modelR(int s, uint32_t j) { return 0x200000u | (s << 12) | (j & 0xFFF); }

// S32BE ring word: lane0..2 = L MSB..LSB, lane3 = pad, lane4..6 = R, lane7 pad
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
static void push_wr() {
  dut->pb_wr_ptr_i = (uint64_t)wrv[0] | ((uint64_t)wrv[1] << 32);
}

static uint32_t rd_of(int s)    { return (uint32_t)((dut->pb_rd_ptr_o >> (32 * s)) & 0xFFFFFFFFu); }
static uint32_t under_of(int s) { return (dut->pb_underrun_o >> (16 * s)) & 0xFFFF; }
static uint32_t over_of(int s)  { return (dut->pb_overrun_o  >> (16 * s)) & 0xFFFF; }

// ---- decoded DAC words ---------------------------------------------------
struct Word { int left; uint32_t v; };
static std::vector<Word> dacw;
static int      d_ws_q = 1, d_sclk_q = 0, d_bit = -1;
static uint32_t d_acc = 0;
static bool     d_left = false;

static void i2s_rx_sample() {
  int sclk = dut->i2s_sclk_o, ws = dut->i2s_lrck_o;
  if (sclk && !d_sclk_q) {                    // receiver samples on SCK rise
    if (ws != d_ws_q) {                       // WS changed: this edge is the
      d_bit = 0; d_acc = 0;                   // delay slot, MSB is the NEXT
      d_left = (ws == 0);                     // WS low = LEFT channel
    } else if (d_bit >= 0 && d_bit < 24) {
      d_acc = (d_acc << 1) | (uint32_t)(dut->i2s_sdin_o & 1);
      if (++d_bit == 24) dacw.push_back({d_left ? 1 : 0, d_acc});
    }
    d_ws_q = ws;
  }
  d_sclk_q = sclk;
}

// ---- event-scheduled clocking -------------------------------------------
static uint64_t t_ps = 0, next_clk = 0, next_aud = 3000;
static bool     mem_pend = false;
static uint32_t mem_addr = 0;
static long     ticks_seen = 0;              // media ticks (phys_valid pulses)

static void edge() {
  if (next_clk <= next_aud) {
    t_ps = next_clk; next_clk += 10000;      // 50 MHz: 10 ns half period
    if (!dut->clk) {                          // about to go HIGH: pre-edge
      dut->mem_valid_i = mem_pend ? 1 : 0;
      if (mem_pend) dut->mem_data_i = mem_word(mem_addr);
      push_wr();
      dut->eval();
      bool req = dut->mem_rd_o; uint32_t a = dut->mem_addr_o;
      dut->clk = 1; dut->eval();
      mem_pend = req; mem_addr = a;
      if (dut->phys_valid_o) ticks_seen++;
    } else {
      dut->clk = 0; dut->eval();
    }
  } else {
    t_ps = next_aud; next_aud += 20000;      // 25 MHz: 20 ns half period
    dut->clk_audio ^= 1; dut->eval();
  }
  i2s_rx_sample();
}

static void run_ps(uint64_t dur) { uint64_t e = t_ps + dur; while (t_ps < e) edge(); }
// one media frame = TICK_DIV clk cycles = TICK_DIV * 20 ns
static void run_frames(int n) { run_ps((uint64_t)n * TICK_DIV * 20000ull); }

static void wr_map(int p, int en, int src, int idx) {
  // map writes are clk-domain single-cycle strobes
  dut->map_wr_en_i = 1; dut->map_wr_addr_i = p;
  dut->map_wr_data_i = ((en & 1) << 7) | ((src & 1) << 6) | (idx & 0x3F);
  // hold for one full clk period, then drop
  run_ps(20000);
  dut->map_wr_en_i = 0;
  run_ps(20000);
}

// keep both streams fed ahead of the reader (no under/overrun)
static const int LEAD = 12;
static void top_up() { for (int s = 0; s < N; s++) feed_to(s, rd_of(s) / 8 + LEAD); }
static void run_frames_fed(int n) {
  for (int i = 0; i < n; i++) { top_up(); run_frames(1); }
  top_up();
}

// collect the decoded stereo frames as {L,R} pairs (drop a leading orphan R)
struct Frm { uint32_t l, r; };
static std::vector<Frm> frames_from(size_t from) {
  std::vector<Frm> out;
  for (size_t i = from; i + 1 < dacw.size(); i++)
    if (dacw[i].left && !dacw[i + 1].left) { out.push_back({dacw[i].v, dacw[i + 1].v}); i++; }
  return out;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vpcm_playback_wrap;

  dut->clk = 0; dut->clk_audio = 0; dut->rst_n = 0;
  dut->pb_enable_i = 0; dut->pb_stream_en_i = 0; dut->pb_underrun_silence_i = 0;
  dut->pb_ring_len_i = LEN; dut->pb_ring_stride_i = STRIDE; dut->pb_wr_ptr_i = 0;
  dut->mem_data_i = 0; dut->mem_valid_i = 0;
  dut->chmap_enable_i = 0; dut->map_wr_en_i = 0; dut->map_wr_addr_i = 0;
  dut->map_wr_data_i = 0;
  dut->tap_tdata_i = 0; dut->tap_tvalid_i = 0; dut->tap_tready_i = 1;
  dut->tap_tlast_i = 0; dut->tap_chans_i = 2; dut->lpf_active_i = 0;
  run_ps(400000);
  dut->rst_n = 1;
  run_ps(200000);

  printf("== item-7 playback chain: host ring -> KL_pcm_tx -> render -> I2S ==\n");

  // ==================================================================
  // A. BIT-EXACT end to end. The listener side is SILENT for the whole
  //    run (the wrapper ties the depacketizer clone off and tap_tvalid
  //    stays 0) and lpf_active_i is held 1 - the shipped default, which
  //    used to win the DAC walker outright. Anything that reaches the
  //    pin therefore came from the host ring through the crossbar.
  // ==================================================================
  wr_map(0, 1, 1, 0);          // phys0 <- playback channel 0 (slot0 L)
  wr_map(1, 1, 1, 1);          // phys1 <- playback channel 1 (slot0 R)
  ck("A map armed (en&src=PB on phys0/1)", dut->pb_mask_o & 3, 3);

  dut->chmap_enable_i = 1;
  dut->lpf_active_i   = 1;     // defect-2 regression: must NOT win here
  dut->pb_stream_en_i = 0x3;
  dut->pb_enable_i    = 1;
  run_ps(40000);
  ck("A feed source = render crossbar", dut->src_render_o, 1);
  ck("A LPF override MASKED in render mode", dut->feed_lpf_active_o, 0);
  ck("A crossbar frame is always a stereo pair", dut->feed_chans_o, 2);

  feed_to(0, LEAD); feed_to(1, LEAD);
  long feeds0 = dut->feeds_o; long ticks0 = ticks_seen;
  size_t dac0 = dacw.size();
  run_frames_fed(48);

  ck_true("A engine walked (pb_playing seen / rd_ptr advanced)", rd_of(0) > 0);
  ck("A feeds == media ticks (one frame per tick, no stall)",
     (long)dut->feeds_o - feeds0, ticks_seen - ticks0);
  ck("A no disarmed-render frames", dut->unarmed_o, 0);
  ck("A KL_pcm_tx underruns", under_of(0), 0);
  ck("A KL_pcm_tx overruns",  over_of(0),  0);

  std::vector<Frm> fr = frames_from(dac0);
  ck_true("A enough DAC frames decoded", fr.size() >= 24);

  // find the longest run that matches the model ring sequence of stream 0
  int best = 0, cur = 0; uint32_t startj = 0, bestj = 0;
  for (size_t i = 0; i + 1 < fr.size(); i++) {
    // a frame matches model word j when both L and R match
    bool linked = false;
    for (uint32_t j = 0; j < 64 && !linked; j++)
      if (fr[i].l == modelL(0, j) && fr[i].r == modelR(0, j)) { startj = j; linked = true; }
    if (!linked) { cur = 0; continue; }
    cur = 1;
    uint32_t j = startj;
    size_t k = i;
    while (k + 1 < fr.size() &&
           fr[k + 1].l == modelL(0, j + 1) && fr[k + 1].r == modelR(0, j + 1)) {
      cur++; k++; j++;
    }
    if (cur > best) { best = cur; bestj = startj; }
  }
  printf("  decoded %zu DAC frames, longest model-consecutive run = %d (from j=%u)\n",
         fr.size(), best, bestj);
  for (size_t i = 0; i < 6 && i < fr.size(); i++)
    printf("    dac[%zu] L=0x%06X R=0x%06X\n", i, fr[i].l, fr[i].r);
  ck_true("A BIT-EXACT: DAC replays the host ring words in order (>=16)",
          best >= 16);

  // negative control: the SAME bytes read little-lane-first would decode to
  // a different value, so a byte-order slip anywhere cannot pass leg A
  uint32_t swapped = ((modelL(0, bestj) & 0xFF) << 16) |
                     (modelL(0, bestj) & 0xFF00) |
                     ((modelL(0, bestj) >> 16) & 0xFF);
  bool sawswap = false;
  for (auto &f : fr) if (f.l == swapped && swapped != modelL(0, bestj)) sawswap = true;
  ck("A neg-control: no little-lane byte order on the pin", sawswap, 0);

  // ==================================================================
  // B. Mid-stream channel-count change on the LISTENER tap. In render
  //    mode the crossbar frame is ALWAYS a stereo pair, so a listener
  //    going 2ch -> 8ch must not re-stride the DAC walker (the 4:1
  //    overfeed) nor disturb the playback audio.
  // ==================================================================
  long fb0 = dut->feeds_o; long tb0 = ticks_seen;
  long ov0 = dut->i2s_overruns_o;
  size_t dacB = dacw.size();
  dut->tap_chans_i = 8;
  run_frames_fed(16);
  ck("B crossbar stride stays 2 at listener chans=8", dut->feed_chans_o, 2);
  dut->tap_chans_i = 3;                     // odd count too
  run_frames_fed(16);
  ck("B crossbar stride stays 2 at listener chans=3", dut->feed_chans_o, 2);
  ck("B feeds still 1 per media tick under chans 2->8->3",
     (long)dut->feeds_o - fb0, ticks_seen - tb0);
  ck("B DAC overrun rail did not move (no re-strided overfeed)",
     (long)dut->i2s_overruns_o - ov0, 0);
  std::vector<Frm> frB = frames_from(dacB);
  int okB = 0;
  for (auto &f : frB)
    for (uint32_t j = 0; j < 200; j++)
      if (f.l == modelL(0, j) && f.r == modelR(0, j)) { okB++; break; }
  printf("  B: %d of %zu frames still exact ring words\n", okB, frB.size());
  ck_true("B playback audio unaffected by the listener channel count",
          frB.size() >= 8 && okB >= (int)frB.size() - 2);
  dut->tap_chans_i = 2;

  // ==================================================================
  // C. Mid-stream map repoint: phys{0,1} move from playback stream 0's
  //    pair to stream 1's pair. Must land whole (never a half-old /
  //    half-new frame) and be bit-exact to stream 1 afterwards.
  // ==================================================================
  size_t dacC = dacw.size();
  wr_map(0, 1, 1, 2);          // phys0 <- playback channel 2 (slot1 L)
  wr_map(1, 1, 1, 3);          // phys1 <- playback channel 3 (slot1 R)
  run_frames_fed(24);
  std::vector<Frm> frC = frames_from(dacC);
  int s1_exact = 0, mixed = 0;
  for (auto &f : frC) {
    bool s0 = false, s1 = false;
    for (uint32_t j = 0; j < 400; j++) {
      if (f.l == modelL(0, j) && f.r == modelR(0, j)) s0 = true;
      if (f.l == modelL(1, j) && f.r == modelR(1, j)) s1 = true;
    }
    if (s1) s1_exact++;
    if (!s0 && !s1) mixed++;
  }
  printf("  C: %d stream-1 exact frames, %d unexplained frames of %zu\n",
         s1_exact, mixed, frC.size());
  ck_true("C repoint lands on stream 1 bit-exactly", s1_exact >= 8);
  ck("C no half-old / half-new frame ever reaches the pin", mixed, 0);
  wr_map(0, 1, 1, 0); wr_map(1, 1, 1, 1);   // back to stream 0
  run_frames_fed(8);

  // ==================================================================
  // D. NEGATIVE - ring UNDER-RUN. Stop the host write pointer: the media
  //    cadence must NOT skew (a skew silently swaps L/R forever), the
  //    engine must count it, and the substitute must be the documented
  //    one - repeat-last, then digital silence when asked.
  // ==================================================================
  long u0 = under_of(0); long fd0 = dut->feeds_o; long td0 = ticks_seen;
  size_t dacD = dacw.size();
  run_frames(40);                            // NO top_up: the ring drains
  ck_true("D KL_pcm_tx underrun counted", under_of(0) > u0);
  ck("D cadence held through the under-run (feeds == ticks)",
     (long)dut->feeds_o - fd0, ticks_seen - td0);
  std::vector<Frm> frD = frames_from(dacD);
  ck_true("D DAC still framed during under-run", frD.size() >= 8);
  uint32_t lastl = frD.empty() ? 0 : frD.back().l, lastr = frD.empty() ? 0 : frD.back().r;
  int reps = 0;
  for (size_t i = 1; i < frD.size(); i++)
    if (frD[i].l == frD[i - 1].l && frD[i].r == frD[i - 1].r) reps++;
  printf("  D: %d repeated frames of %zu (repeat-last policy)\n", reps, frD.size());
  ck_true("D under-run substitutes REPEAT the last sample", reps > 0);
  ck_true("D repeat value is a real ring word, not garbage",
          [&]{ for (uint32_t j = 0; j < 500; j++)
                 if (lastl == modelL(0, j) && lastr == modelR(0, j)) return true;
               return false; }());

  // silence policy
  dut->pb_underrun_silence_i = 1;
  size_t dacDs = dacw.size();
  run_frames(24);
  std::vector<Frm> frDs = frames_from(dacDs);
  int zeros = 0;
  for (auto &f : frDs) if (f.l == 0 && f.r == 0) zeros++;
  printf("  D: %d silent frames of %zu under silence policy\n", zeros, frDs.size());
  ck_true("D silence policy renders digital zero", frDs.size() >= 4 && zeros >= 4);
  dut->pb_underrun_silence_i = 0;

  // ==================================================================
  // E. NEGATIVE - ring OVER-RUN. The host laps the reader by more than a
  //    whole sub-ring: the engine must count it, fast-forward one lap so
  //    the fill is bounded again, and resume on FRESH words - not on the
  //    torn lap it was reading.
  // ==================================================================
  long o0 = over_of(0);
  // write two full laps of new content, then jump the write pointer past
  // the reader by more than LEN (the definition of a lap-drop)
  uint32_t base = committed[0];
  for (uint32_t j = base; j < base + 2 * (LEN / 8) + 8; j++)
    put_word(0, j, modelL(0, j), modelR(0, j));
  committed[0] = base + 2 * (LEN / 8) + 8;
  wrv[0] = committed[0] * 8;
  push_wr();
  run_frames(4);
  ck_true("E KL_pcm_tx overrun counted", over_of(0) > o0);
  uint32_t fill = wrv[0] - rd_of(0);
  printf("  E: fill after lap-drop = %u bytes (ring len %u)\n", fill, LEN);
  ck_true("E read pointer fast-forwarded: fill bounded by the ring", fill <= LEN);
  size_t dacE = dacw.size();
  run_frames_fed(24);
  // the DAC pipeline (producer FIFO prefill + the CDC FIFO) holds a BOUNDED
  // number of already-queued frames from the previous phase; PIPE_C skips
  // exactly those, and every frame after them must be an intact ring word.
  const size_t PIPE_C = 8;
  std::vector<Frm> frE = frames_from(dacE);
  int fresh = 0, tail = 0;
  for (size_t i = PIPE_C; i < frE.size(); i++) {
    tail++;
    for (uint32_t j = 0; j < 1000; j++)
      if (frE[i].l == modelL(0, j) && frE[i].r == modelR(0, j)) { fresh++; break; }
  }
  printf("  E: %d of %d post-pipeline frames are real ring words after the lap-drop\n",
         fresh, tail);
  ck_true("E resumes on intact ring words (no torn/garbage samples)",
          tail >= 8 && fresh == tail);

  // ==================================================================
  // F. NEGATIVE - chmap DISARMED. Two distinct disarmed states, both of
  //    which must REPORT rather than quietly emit noise:
  //      F1 crossbar selected but no map entry backs phys{0,1}
  //         -> guaranteed silence + the unarmed_o rail counts it.
  //      F2 CHMAP_CTRL[0] = 0 -> the feed falls back to the listener tap,
  //         which is silent here, so the delivered-frame count FREEZES -
  //         that freeze IS the honest report (and the DAC under-run rail
  //         confirms it from the far end).
  // ==================================================================
  wr_map(0, 0, 1, 0); wr_map(1, 0, 1, 1);
  ck("F1 map disarmed (pb_mask clear)", dut->pb_mask_o & 3, 0);
  long un0 = dut->unarmed_o; long fe0 = dut->feeds_o;
  size_t dacF = dacw.size();
  run_frames_fed(32);
  ck_true("F1 disarmed-render frames counted", (long)dut->unarmed_o > un0);
  ck_true("F1 frames still delivered on cadence", (long)dut->feeds_o > fe0);
  std::vector<Frm> frF = frames_from(dacF);
  int nz = 0, ftail = 0;                    // same bounded-pipeline skip as E
  for (size_t i = PIPE_C; i < frF.size(); i++) {
    ftail++;
    if (frF[i].l || frF[i].r) nz++;
  }
  printf("  F1: %d nonzero of %d post-pipeline frames after disarm\n", nz, ftail);
  ck_true("F1 enough post-pipeline frames observed", ftail >= 8);
  ck("F1 disarmed render is SILENCE, never garbage", nz, 0);

  dut->chmap_enable_i = 0;                  // F2
  long fe1 = dut->feeds_o; long du0 = dut->i2s_underruns_o;
  run_frames(24);
  ck("F2 feed count FREEZES with the tap silent", (long)dut->feeds_o - fe1, 0);
  ck("F2 feed source reports legacy tap", dut->src_render_o, 0);
  ck_true("F2 DAC under-run rail reports the starve",
          (long)dut->i2s_underruns_o > du0);

  // ==================================================================
  // G. The CERT path is UNCHANGED: with the crossbar deselected the
  //    listener tap passes through the feed mux bit-identically and the
  //    LPF override is forwarded (not masked).
  // ==================================================================
  dut->lpf_active_i = 1;
  run_ps(40000);
  ck("G lpf override FORWARDED on the legacy path", dut->feed_lpf_active_o, 1);
  dut->tap_chans_i = 6;
  run_ps(40000);
  ck("G legacy stride follows the listener wire truth", dut->feed_chans_o, 6);
  dut->tap_chans_i = 2;
  dut->lpf_active_i = 0;
  size_t dacG = dacw.size();
  long fg0 = dut->feeds_o;
  // drive the tap with known S32BE beats (2ch: one {L,R} pair per beat)
  const uint32_t GL[6] = {0x303132, 0x404142, 0x505152, 0x606162, 0x707172, 0x111213};
  const uint32_t GR[6] = {0x0A0B0C, 0x1A1B1C, 0x2A2B2C, 0x3A3B3C, 0x4A4B4C, 0x5A5B5C};
  for (int rep = 0; rep < 40; rep++) {
    for (int k = 0; k < 6; k++) {
      uint32_t L = GL[k], R = GR[k];
      uint64_t d = 0;
      d |= (uint64_t)((L >> 16) & 0xFF) << 0;  d |= (uint64_t)((L >> 8) & 0xFF) << 8;
      d |= (uint64_t)(L & 0xFF) << 16;
      d |= (uint64_t)((R >> 16) & 0xFF) << 32; d |= (uint64_t)((R >> 8) & 0xFF) << 40;
      d |= (uint64_t)(R & 0xFF) << 48;
      dut->tap_tdata_i = d; dut->tap_tvalid_i = 1; dut->tap_tlast_i = (k == 5);
      run_ps(20000);                          // one clk period = one accepted beat
      dut->tap_tvalid_i = 0; dut->tap_tlast_i = 0;
      run_ps(20000 * 20);                     // pace ~ the media rate
    }
  }
  run_frames(8);
  ck_true("G legacy tap feeds the DAC again", (long)dut->feeds_o > fg0);
  std::vector<Frm> frG = frames_from(dacG);
  int gok = 0;
  for (auto &f : frG)
    for (int k = 0; k < 6; k++)
      if (f.l == GL[k] && f.r == GR[k]) { gok++; break; }
  printf("  G: %d of %zu frames are exact legacy-tap pairs\n", gok, frG.size());
  ck_true("G CERT path still serializes the tap BIT-EXACTLY",
          frG.size() >= 6 && gok >= (int)frG.size() - 2);

  // -----------------------------------------------------------------------
  //  H: GM/PHC-step recenter (task #22). A grandmaster change may step the
  //  presentation timebase by SECONDS; without this pin the playback FIFO
  //  walked back into its convergence band at the residual ppm - measured
  //  ~2 minutes on silicon (08-06). One pulse must snap fill to MID and
  //  raise the honest media_reset event.
  // -----------------------------------------------------------------------
  printf("\n[H] GM-step recenter snaps the FIFO to MID\n");
  {
    const long MID = 1L << (9 - 1);            // FIFO_LOG2 default 9
    long f0 = (long)dut->i2s_fill_o;
    ck_true("H precondition: fill is OFF mid", f0 != MID);
    bool mr_seen = false;
    dut->recenter_p_i = 1;
    for (int e = 0; e < 8; e++) {              // >= 3 full clk_i periods
      run_ps(10000);
      if (dut->media_reset_p_o) mr_seen = true;
    }
    dut->recenter_p_i = 0;
    for (int e = 0; e < 16; e++) {
      run_ps(10000);
      if (dut->media_reset_p_o) mr_seen = true;
    }
    long f1 = (long)dut->i2s_fill_o;
    printf("  H: fill %ld -> %ld (MID %ld)\n", f0, f1, MID);
    ck_true("H fill snapped to MID (+/- the in-flight beat)",
            f1 >= MID - 2 && f1 <= MID + 2);
    ck_true("H media_reset pulsed (the honest discontinuity)", mr_seen);
  }

  printf("--------------------------------------------------------------\n");
  printf("pcm_playback: %ld checks: %ld PASS, %ld FAIL\n",
         pass_n + fail_n, pass_n, fail_n);
  printf("RESULT: %s\n", fail_n ? "FAIL" : "PASS");
  delete dut;
  return fail_n ? 1 : 0;
}

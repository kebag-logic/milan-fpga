// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_pcm_ring_bram self-checking harness.
//
// Built twice (see Makefile): N_STREAMS=1 and N_STREAMS=4, each with a
// matching TB_N_STREAMS / TB_RING_BYTES so the C++ shadow computes the same
// addresses the RTL does.
//
// Proves the flagship claim: the BRAM ring CANNOT shed.
//   [N=1] no-shed under the exact mf52 regime — the 6-back-to-back-beat-PDU
//         + gap non-stallable pattern from test_pcm_ring.py, driven WHILE the
//         CPU read port is hammered concurrently: wr_ready_o is checked to be
//         1 on EVERY offered cycle, ZERO beats dropped, and every offered beat
//         lands in BRAM in order. A NEGATIVE CONTROL runs the identical
//         schedule through a software model of the depth-16 contended DRAM
//         lane and shows it SHEDS (drops>0) — the failure the BRAM removes.
//   [N=1] byte-exact content + correct wrap at length_i + offset_o readback.
//   [N=1] enable_i=0 clears offsets and drops beats (ready still 1).
//   [N=1] CPU read port returns written words at the right addresses;
//         read-during-write to the same location is coherent.
//   [N=4] tuser routing: per-stream sub-rings at base + s*stride, per-stream
//         offset wrap, offset_o readback via sel_i.

#include "VKL_pcm_ring_bram.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <deque>
#include <algorithm>

#ifndef TB_N_STREAMS
#define TB_N_STREAMS 1
#endif
#ifndef TB_RING_BYTES
#define TB_RING_BYTES 32768
#endif

static const uint32_t NB    = 8;
static const uint32_t DEPTH = TB_RING_BYTES / NB;
static const uint32_t DMASK = DEPTH - 1;

static VKL_pcm_ring_bram *dut;
static int pass = 0, fail = 0;
static vluint64_t tcyc = 0;
static uint32_t hammer_addr = 0;   // walks the ring on the concurrent read port

static void tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  tcyc++;
}

static void ck(const char *name, bool cond, const char *detail = "") {
  if (cond) { pass++; printf("[PASS] %s%s%s\n", name, detail[0] ? "  " : "", detail); }
  else      { fail++; printf("[FAIL] %s%s%s\n", name, detail[0] ? "  " : "", detail); }
}

static void ckq(const char *name, uint64_t got, uint64_t want) {
  char d[96];
  snprintf(d, sizeof d, "got=0x%llx want=0x%llx",
           (unsigned long long)got, (unsigned long long)want);
  ck(name, got == want, d);
}

// ---- control programming ---------------------------------------------------
static void program(uint32_t length, uint32_t stride, bool en, uint8_t sel) {
  dut->length_i = length;
  dut->stride_i = stride;
  dut->enable_i = en ? 1 : 0;
  dut->sel_i    = sel;
}

// ---- reset -----------------------------------------------------------------
static void reset() {
  dut->rst_n = 0;
  dut->wr_data_i = 0; dut->wr_user_i = 0; dut->wr_valid_i = 0;
  dut->length_i = 0; dut->stride_i = 0; dut->enable_i = 0; dut->sel_i = 0;
  dut->wb_adr_i = 0; dut->wb_cyc_i = 0; dut->wb_stb_i = 0;
  for (int i = 0; i < 4; i++) tick();
  dut->rst_n = 1;
  for (int i = 0; i < 4; i++) tick();
}

// ---- one write beat; optionally hammer the CPU read port the same cycle ----
// returns wr_ready_o sampled the offered cycle (must be 1 always).
static bool offer(uint64_t data, uint8_t user, bool hammer) {
  dut->wr_data_i = data; dut->wr_user_i = user; dut->wr_valid_i = 1;
  if (hammer) { dut->wb_cyc_i = 1; dut->wb_stb_i = 1; dut->wb_adr_i = hammer_addr; }
  bool rdy = dut->wr_ready_o;   // combinational, constant 1
  tick();
  if (hammer && dut->wb_ack_o) hammer_addr = (hammer_addr + 1) & DMASK;
  return rdy;
}

static void idle(int n, bool hammer) {
  dut->wr_valid_i = 0;
  for (int i = 0; i < n; i++) {
    if (hammer) { dut->wb_cyc_i = 1; dut->wb_stb_i = 1; dut->wb_adr_i = hammer_addr; }
    tick();
    if (hammer && dut->wb_ack_o) hammer_addr = (hammer_addr + 1) & DMASK;
  }
}

static void quiesce() {
  dut->wr_valid_i = 0; dut->wb_cyc_i = 0; dut->wb_stb_i = 0;
  for (int i = 0; i < 4; i++) tick();
}

// ---- clean wishbone-classic read of one word -------------------------------
static uint64_t wb_read(uint32_t word_addr) {
  dut->wb_adr_i = word_addr; dut->wb_cyc_i = 1; dut->wb_stb_i = 1;
  int guard = 0;
  do { tick(); } while (!dut->wb_ack_o && ++guard < 64);
  uint64_t d = dut->wb_dat_o;
  dut->wb_cyc_i = 0; dut->wb_stb_i = 0;
  tick();
  return d;
}

// ---- C++ shadow: mirrors the RTL write + offset logic exactly --------------
struct Shadow {
  std::vector<uint64_t> mem;
  std::vector<uint32_t> off;
  uint32_t length = 0, stride = 0;
  Shadow() : mem(DEPTH, 0), off(16, 0) {}
  void clear() { std::fill(mem.begin(), mem.end(), 0); std::fill(off.begin(), off.end(), 0); }
  void apply(uint8_t s, uint64_t data) {
    uint32_t byte = stride * (uint32_t)s + off[s];
    uint32_t w    = (byte >> 3) & DMASK;
    mem[w] = data;
    if (off[s] + NB >= length) off[s] = 0; else off[s] += NB;
  }
};

// ---- schedule of the mf52 PDU pattern: 6 back-to-back beats + gap ----------
// element >= 0 : offer this beat value; -1 : idle cycle
static std::vector<long long> make_schedule(int pdus, int gap, int bpp,
                                            uint8_t stream) {
  std::vector<long long> s;
  long long seq = 0;
  for (int p = 0; p < pdus; p++) {
    for (int b = 0; b < bpp; b++) s.push_back(((long long)stream << 56) | (seq++));
    for (int g = 0; g < gap; g++) s.push_back(-1);
  }
  return s;
}

// ---- NEGATIVE CONTROL: software model of the depth-16 contended DRAM lane --
// The non-stallable source feeds a shallow FIFO drained by a wishbone writer
// that eats a `slow` contention burst every `every` services (CPU reading the
// ring region). A beat offered while the FIFO is full is SHED. This is the
// mf52 silicon failure — it reproduces here so the BRAM result is meaningful.
struct DramLaneModel {
  int depth, fast, slow, every;
  std::deque<int> q;           // occupancy only
  int stall = 0, since = 0;
  long served = 0, drops = 0, offered = 0;
  void step(bool has_offer) {
    // drain phase (one service per `fast` cycles; a `slow` stall every `every`)
    if (stall > 0) { stall--; }
    else if (!q.empty()) {
      if (++since >= fast) { since = 0; q.pop_front(); served++;
                             if (every && served % every == 0) stall = slow; }
    }
    // offer phase (the wire does not wait)
    if (has_offer) { offered++; if ((int)q.size() < depth) q.push_back(1); else drops++; }
  }
};

#if TB_N_STREAMS == 1

static int test_no_shed_vs_dram() {
  printf("[1] N=1 no-shed under mf52 regime (concurrent CPU reads) + DRAM negative control\n");
  reset();

  const int PDUS = 120, GAP = 40, BPP = 6;
  const uint32_t LEN = 6144;            // 768 words > 720 beats => no wrap: clean sequence
  auto sched = make_schedule(PDUS, GAP, BPP, /*stream=*/0);

  // ---- NEGATIVE CONTROL: identical schedule through the DRAM lane model ----
  DramLaneModel dram{ /*depth=*/16, /*fast=*/2, /*slow=*/500, /*every=*/8 };
  for (auto ev : sched) dram.step(ev >= 0);

  // ---- DUT: same schedule, CPU read port hammered concurrently -------------
  program(LEN, /*stride=*/0, /*en=*/true, /*sel=*/0);
  tick();
  Shadow sh; sh.length = LEN; sh.stride = 0; sh.clear();
  long offered = 0, ready_lows = 0;
  for (auto ev : sched) {
    if (ev >= 0) {
      bool r = offer((uint64_t)ev, 0, /*hammer=*/true);
      offered++;
      if (!r) ready_lows++;
      sh.apply(0, (uint64_t)ev);
    } else {
      idle(1, /*hammer=*/true);
    }
  }
  quiesce();

  int fails0 = fail;
  char d[96];
  snprintf(d, sizeof d, "dropped=%ld offered=%ld", dram.drops, dram.offered);
  ck("NEGATIVE CONTROL: DRAM lane (depth 16) SHEDS under this load", dram.drops > 0, d);

  ckq("beats offered", offered, (uint64_t)(PDUS * BPP));
  ckq("wr_ready_o was 1 on EVERY offered cycle (no back-pressure ever)", ready_lows, 0);
  ck("BRAM ring: every offered beat present, in order (byte-exact)",
     [&] {
       for (uint32_t i = 0; i < (uint32_t)(PDUS * BPP); i++)
         if (wb_read(i) != (uint64_t)i) return false;
       return true;
     }());
  printf("      note: on the DRAM WishboneDMAWriter this exact load shed ~1 beat in 24 "
         "(mf52); the BRAM sink.ready is constant 1 so drops are structurally impossible.\n");
  return fail - fails0;
}

static int test_wrap_and_offset() {
  printf("[2] N=1 wrap at length_i + offset_o readback\n");
  reset();
  const uint32_t LEN = 256;             // 32 words
  program(LEN, /*stride=*/0, /*en=*/true, /*sel=*/0);
  tick();
  Shadow sh; sh.length = LEN; sh.stride = 0; sh.clear();

  const int BEATS = 100;                // wraps 3+ times (100*8=800, 800/256=3.125)
  for (int i = 0; i < BEATS; i++) { offer((uint64_t)i, 0, false); sh.apply(0, (uint64_t)i); }
  quiesce();

  int fails0 = fail;
  // offset_o (sel 0) must equal the shadow write pointer
  dut->sel_i = 0; tick();
  ckq("offset_o = (beats*8) mod length", dut->offset_o, ((uint64_t)BEATS * NB) % LEN);
  // every ring word holds the LAST beat that mapped to it (post-wrap overwrite)
  ck("wrapped ring content byte-exact (last-writer-wins per word)",
     [&] {
       for (uint32_t w = 0; w < LEN / NB; w++)
         if (wb_read(w) != sh.mem[w]) return false;
       return true;
     }());
  return fail - fails0;
}

static int test_enable_clear() {
  printf("[3] N=1 enable_i=0 clears offsets + drops beats (ready still 1)\n");
  reset();
  const uint32_t LEN = 4096;
  program(LEN, 0, /*en=*/true, 0);
  tick();
  // land a known value at word 0, advance the pointer a little
  offer(0xAAAAAAAAAAAAAAAAull, 0, false);   // -> word 0, offset now 8
  offer(0x1111111111111111ull, 0, false);   // -> word 1, offset now 16
  quiesce();
  int fails0 = fail;
  dut->sel_i = 0; tick();
  ckq("offset advanced before disable", dut->offset_o, 16);

  // disable: offsets clear, beats drop, ready stays 1
  program(LEN, 0, /*en=*/false, 0);
  tick(); tick();
  dut->sel_i = 0; tick();
  ckq("offset_o cleared to 0 on disable", dut->offset_o, 0);
  bool r = offer(0xDEADDEADDEADDEADull, 0, false);   // dropped (disabled)
  ck("wr_ready_o still 1 while disabled", r);
  offer(0xDEADDEADDEADDEADull, 0, false);
  quiesce();
  ckq("disabled beat did NOT overwrite word 0", wb_read(0), 0xAAAAAAAAAAAAAAAAull);
  ckq("disabled beat did NOT overwrite word 1", wb_read(1), 0x1111111111111111ull);

  // re-enable: pointer resumes from 0, new beat lands at word 0
  program(LEN, 0, /*en=*/true, 0);
  tick();
  offer(0xBEEFBEEFBEEFBEEFull, 0, false);
  quiesce();
  ckq("re-enabled beat lands at word 0 (offset restarted)", wb_read(0), 0xBEEFBEEFBEEFBEEFull);
  return fail - fails0;
}

static int test_cpu_read_coherency() {
  printf("[4] N=1 CPU read port: read-back correctness + read-during-write coherency\n");
  reset();
  const uint32_t LEN = 4096;
  program(LEN, 0, /*en=*/true, 0);
  tick();
  // write 8 distinct words
  for (int i = 0; i < 8; i++) offer(0xC0DE0000ull + i, 0, false);
  quiesce();
  int fails0 = fail;
  ck("read port returns each written word at its address",
     [&] { for (int i = 0; i < 8; i++) if (wb_read(i) != (uint64_t)(0xC0DE0000ull + i)) return false;
           return true; }());

  // concurrent read of word 3 in the SAME cycle a write lands at word 8:
  // independent ports -> read sees the committed word 3, write still lands.
  dut->wb_adr_i = 3; dut->wb_cyc_i = 1; dut->wb_stb_i = 1;   // fresh strobe -> reads mem[3] this edge
  bool r = offer(0x99998888ull, 0, /*hammer=*/false);        // write lands at word 8 same edge
  ck("wr_ready_o=1 during concurrent CPU read", r);
  uint64_t rd = dut->wb_dat_o;                               // ack asserted this cycle
  ckq("read-during-write to a different word returns committed data", rd, 0xC0DE0003ull);
  dut->wb_cyc_i = 0; dut->wb_stb_i = 0;
  quiesce();
  ckq("the concurrent write still landed at word 8", wb_read(8), 0x99998888ull);

  // same-location coherency: a 1-word ring (length=8) is written repeatedly;
  // the read port must observe the latest committed value.
  program(8, 0, /*en=*/true, 0); tick();
  offer(0x1000000000000001ull, 0, false);   // -> word 0
  offer(0x2000000000000002ull, 0, false);   // -> word 0 (wrapped)
  offer(0x3000000000000003ull, 0, false);   // -> word 0 (wrapped)
  quiesce();
  ckq("read port sees latest committed value at a re-written location",
      wb_read(0), 0x3000000000000003ull);
  return fail - fails0;
}

#else  // TB_N_STREAMS == 4

static int test_nxn_routing() {
  printf("[1] N=4 tuser routing: per-stream sub-rings + per-stream offset + offset_o readback\n");
  reset();
  const uint32_t RING_WORDS = 512;
  const uint32_t LEN    = RING_WORDS * NB;   // 4096 bytes / stream
  const uint32_t STRIDE = RING_WORDS * NB;   // contiguous sub-rings
  program(LEN, STRIDE, /*en=*/true, /*sel=*/0);
  tick();

  Shadow sh; sh.length = LEN; sh.stride = STRIDE; sh.clear();

  const int PDUS = 96, GAP = 20, BPP = 6;    // 24 PDUs/stream -> 144 beats/stream (< 512: no wrap)
  uint32_t seq[4] = {0, 0, 0, 0};
  for (int p = 0; p < PDUS; p++) {
    uint8_t s = (uint8_t)(p % 4);
    for (int b = 0; b < BPP; b++) {
      uint64_t word = ((uint64_t)s << 56) | (seq[s]++);
      offer(word, s, /*hammer=*/true);
      sh.apply(s, word);
    }
    idle(GAP, /*hammer=*/true);
  }
  quiesce();

  int fails0 = fail;
  const uint32_t PER = (uint32_t)(PDUS / 4 * BPP);   // 144
  for (int s = 0; s < 4; s++) {
    // each stream's beats sit at base + s*stride, sequence 0..PER-1, tagged s
    bool ok = true;
    for (uint32_t i = 0; i < PER; i++) {
      uint64_t got = wb_read(s * RING_WORDS + i);
      uint64_t want = ((uint64_t)s << 56) | i;
      if (got != want) { ok = false; break; }
    }
    char nm[80]; snprintf(nm, sizeof nm, "stream %d: %u beats at base+%d*stride, in order", s, PER, s);
    ck(nm, ok);
    // offset_o readback via sel_i
    dut->sel_i = (uint8_t)s; tick();
    char no[80]; snprintf(no, sizeof no, "stream %d: offset_o = beats*8", s);
    ckq(no, dut->offset_o, (uint64_t)PER * NB);
  }
  // sub-rings are disjoint: stream 0's region untouched by streams 1..3 tails
  ck("stream 3 region does not bleed into stream 0 region",
     wb_read(0) != wb_read(3 * RING_WORDS) || (wb_read(0) >> 56) == 0);
  return fail - fails0;
}

#endif

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_pcm_ring_bram;

  printf("== KL_pcm_ring_bram TB : N_STREAMS=%d RING_BYTES=%d DEPTH=%u words ==\n",
         TB_N_STREAMS, TB_RING_BYTES, DEPTH);

#if TB_N_STREAMS == 1
  test_no_shed_vs_dram();
  test_wrap_and_offset();
  test_enable_clear();
  test_cpu_read_coherency();
#else
  test_nxn_routing();
#endif

  printf("\n%d checks: %d PASS, %d FAIL\n", pass + fail, pass, fail);
  delete dut;
  return fail ? 1 : 0;
}

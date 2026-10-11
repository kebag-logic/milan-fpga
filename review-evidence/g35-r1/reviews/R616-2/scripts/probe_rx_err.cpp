// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe for FPGA-gPTP #35 / PR #80 (independent of the PR's bench).
//
// Drives KL_gptp_rx_parser directly. For every frame shape below and every
// byte position p, a reference clean run records the per-edge write log; the
// flagged run (rx_err_i on byte p only) must then give: drops +1, no event,
// no bank write on any edge after byte p's own edge, and the writes up to and
// including p's edge equal the clean run's prefix (address and data).
// Further probes: random multi-byte flag sets, a flag on a one-byte frame,
// a flagged stray byte outside any frame, a flag stacked on another refusal,
// zero-gap refused/clean pairs (incl. Announce with PathTrace and the
// stale-tail case), and a refusal adjacent to a runt.
#include <cstdint>
#include <cstdio>
#include <map>
#include <random>
#include <string>
#include <vector>
#include <verilated.h>
#include "VKL_gptp_rx_parser.h"

static VKL_gptp_rx_parser *dut;
static int checks = 0, fails = 0;
static void expect(const std::string &what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("FAIL %s got %llu exp %llu\n", what.c_str(),
           (unsigned long long)got, (unsigned long long)exp);
  }
}

struct Wr { int edge; unsigned addr; uint64_t data; };
static std::vector<Wr> wlog;
static int edge_no = 0;      // index of the byte whose edge just happened (-1 idle)
static int ev_count = 0;
static uint8_t ev_code = 0;
static uint16_t ev_seq = 0;
static std::map<unsigned, uint64_t> bank, ev_bank;

static void tick(int edge_tag) {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  // outputs are registered: what is visible now was decided on this edge
  if (dut->bank_we_o) {
    wlog.push_back({edge_tag, dut->bank_addr_o, dut->bank_wdata_o});
    bank[dut->bank_addr_o] = dut->bank_wdata_o;
  }
  if (dut->ev_valid_o) {
    ev_count++; ev_code = dut->ev_code_o; ev_seq = dut->ev_seq_o;
    ev_bank = bank;
  }
}
static void idle(int n) {
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0; dut->rx_err_i = 0;
  for (int i = 0; i < n; i++) tick(1000000 + i);
}

struct F { std::vector<uint8_t> b;
  void u8(unsigned v) { b.push_back(v & 0xFF); }
  void u16(unsigned v) { u8(v >> 8); u8(v); }
  void u32(uint32_t v) { u16(v >> 16); u16(v); }
  void u48(uint64_t v) { u16(v >> 32); u32((uint32_t)v); }
  void u64(uint64_t v) { u32(v >> 32); u32((uint32_t)v); }
};

static const uint64_t LOCAL = 0x0A0B0CFFFE0D0E0Full;
static const uint64_t GM = 0x1111111111111111ull;

static F hdr(unsigned mt, unsigned body, unsigned salt) {
  F f;
  for (int i = 0; i < 6; i++) f.u8(0x01);
  for (int i = 0; i < 6; i++) f.u8(0x30 + salt);
  f.u16(0x88F7);
  f.u8(0x10 | mt); f.u8(0x02); f.u16(34 + body); f.u8(0); f.u8(0);
  f.u16(0x0200 | salt);
  f.u64(0x0102030405060700ull | salt);
  f.u32(0);
  f.u64(0xA0A0A0FFFE000000ull | (uint64_t)salt << 8 | salt);
  f.u16(0x100 + salt);
  f.u16(0x4400 + salt);
  f.u8(0); f.u8(0xF0 + (salt & 0xF));
  return f;
}
static F make(const std::string &kind, unsigned salt) {
  if (kind == "sync") { F f = hdr(0x0, 10, salt); f.u48(0x1234500 + salt); f.u32(0x100 + salt); return f; }
  if (kind == "fu") {
    F f = hdr(0x8, 42, salt); f.u48(0x5550 + salt); f.u32(0x7770 + salt);
    f.u16(3); f.u16(28); f.u8(0x00); f.u8(0x80); f.u8(0xC2); f.u8(0); f.u8(0); f.u8(1);
    f.u32(0xABC00000 + salt); f.u16(0x0700 + salt);
    for (int i = 0; i < 12; i++) f.u8(i); f.u32(0x123); return f; }
  if (kind == "pdreq") { F f = hdr(0x2, 20, salt); for (int i = 0; i < 20; i++) f.u8(0); return f; }
  if (kind == "pdresp" || kind == "pdrfu") {
    F f = hdr(kind == "pdresp" ? 0x3 : 0xA, 20, salt);
    f.u48(0x99900 + salt); f.u32(0x888 + salt);
    f.u64(0xBEEF0000CAFE0000ull + salt); f.u16(0x300 + salt); return f; }
  if (kind == "sig") { F f = hdr(0xC, 10, salt); f.u64(0x77); f.u16(1); return f; }
  if (kind == "ann" || kind == "ann_pt3" || kind == "ann_pt9" || kind == "ann_pad") {
    unsigned hops = kind == "ann_pt3" ? 3 : kind == "ann_pt9" ? 9 : 0;
    unsigned steps = hops ? hops - 1 : 0;
    unsigned suffix = hops ? 4 + 8 * hops : 0;
    F f = hdr(0xB, 30 + suffix, salt);
    for (int i = 0; i < 10; i++) f.u8(0);
    f.u16(37); f.u8(0); f.u8(128); f.u32(0xF8FE436A); f.u8(128);
    f.u64(GM); f.u16(steps); f.u8(0xA0);
    if (hops) { f.u16(8); f.u16(8 * hops);
      for (unsigned h = 0; h < hops; h++) f.u64(h == 0 ? GM : 0x2222000000000000ull + h * 0x101 + salt); }
    if (kind == "ann_pad") for (int i = 0; i < 6; i++) f.u8(0xEE);   // physical padding after the declared end
    return f; }
  fprintf(stderr, "unknown kind %s\n", kind.c_str()); exit(2);
}
static unsigned code_of(const std::string &k) {
  if (k == "sync") return 1; if (k == "fu") return 2; if (k.rfind("ann", 0) == 0) return 3;
  if (k == "pdreq") return 4; if (k == "pdresp") return 5; if (k == "pdrfu") return 6;
  if (k == "sig") return 7; return 0;
}

// stream frames back to back (no idle between) with per-frame flag masks
static void stream(const std::vector<std::pair<const F *, std::vector<bool>>> &fs, int base_tag = 0) {
  int tag = base_tag;
  for (auto &[f, m] : fs) {
    for (size_t i = 0; i < f->b.size(); i++) {
      dut->rx_valid_i = 1; dut->rx_data_i = f->b[i];
      dut->rx_sof_i = i == 0; dut->rx_eof_i = i + 1 == f->b.size();
      dut->rx_err_i = m.empty() ? 0 : (bool)m[i];
      tick(tag++);
    }
  }
  idle(4);
}
static void reset() {
  dut->rst_n = 0; dut->rx_valid_i = 0; dut->rx_err_i = 0;
  dut->local_clock_id_i = LOCAL; dut->local_clock_valid_i = 1;
  for (int i = 0; i < 4; i++) tick(-1);
  dut->rst_n = 1; idle(2);
}
static void clear() { wlog.clear(); ev_count = 0; ev_code = 0; bank.clear(); ev_bank.clear(); }

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new VKL_gptp_rx_parser;
  reset();
  const std::vector<std::string> kinds = {"sync", "fu", "pdreq", "pdresp", "pdrfu",
                                          "sig", "ann", "ann_pt3", "ann_pt9", "ann_pad"};
  // ---- 1. every byte, every kind: drop, no event, no write after, prefix equal
  for (const auto &k : kinds) {
    F f = make(k, 5);
    clear(); uint16_t d0 = dut->drop_cnt_o;
    stream({{&f, {}}});
    expect(k + " clean control event", ev_count == 1 ? ev_code : 0, code_of(k));
    expect(k + " clean control no drop", dut->drop_cnt_o, d0);
    const std::vector<Wr> ref = wlog;
    size_t bad = 0;
    int max_before = 0, max_after = 0;
    for (size_t p = 0; p < f.b.size(); p++) {
      std::vector<bool> m(f.b.size(), false); m[p] = true;
      clear(); d0 = dut->drop_cnt_o;
      stream({{&f, m}});
      int after = 0; size_t pre = 0; bool prefix_ok = true;
      for (auto &w : wlog) { if (w.edge > (int)p) after++; else pre++; }
      std::vector<Wr> refpre; for (auto &w : ref) if (w.edge <= (int)p) refpre.push_back(w);
      if (refpre.size() != pre) prefix_ok = false;
      else for (size_t i = 0; i < pre; i++)
        if (refpre[i].edge != wlog[i].edge || refpre[i].addr != wlog[i].addr || refpre[i].data != wlog[i].data) prefix_ok = false;
      bool ok = (uint16_t)(dut->drop_cnt_o - d0) == 1 && ev_count == 0 && after == 0 && prefix_ok;
      if (!ok) { bad++; printf("  %s p=%zu drops+%d ev=%d after=%d prefix_ok=%d\n", k.c_str(), p,
                                (int)(uint16_t)(dut->drop_cnt_o - d0), ev_count, after, prefix_ok); }
      if ((int)pre > max_before) max_before = pre;
      if (after > max_after) max_after = after;
    }
    expect(k + " every byte refused cleanly (bytes failing)", bad, 0);
    printf("INFO %s len=%zu clean writes=%zu max writes up to flag=%d max after=%d\n",
           k.c_str(), f.b.size(), ref.size(), max_before, max_after);
  }
  // ---- 2. random multi-byte flag sets: exactly one drop, no event, no write after first flag
  std::mt19937 rng(35);
  for (const auto &k : kinds) {
    F f = make(k, 6); size_t bad = 0;
    for (int t = 0; t < 200; t++) {
      std::vector<bool> m(f.b.size(), false); int first = -1;
      int n = 1 + rng() % 6;
      for (int j = 0; j < n; j++) m[rng() % f.b.size()] = true;
      for (size_t i = 0; i < m.size(); i++) if (m[i]) { first = (int)i; break; }
      clear(); uint16_t d0 = dut->drop_cnt_o; stream({{&f, m}});
      int after = 0; for (auto &w : wlog) if (w.edge > first) after++;
      if ((uint16_t)(dut->drop_cnt_o - d0) != 1 || ev_count || after) bad++;
    }
    expect(k + " random multi-flag sets refused once (bad trials)", bad, 0);
  }
  // ---- 3. one-byte frame with the flag: one drop only
  { F one; one.u8(0x01); clear(); uint16_t d0 = dut->drop_cnt_o;
    stream({{&one, {true}}});
    expect("flagged one-byte frame: one drop", (uint16_t)(dut->drop_cnt_o - d0), 1);
    expect("flagged one-byte frame: no event", ev_count, 0);
    F s = make("sync", 7); clear(); d0 = dut->drop_cnt_o; stream({{&s, {}}});
    expect("sync after flagged runt: event", ev_count == 1 ? ev_code : 0, 1);
    expect("sync after flagged runt: no drop", (uint16_t)(dut->drop_cnt_o - d0), 0); }
  // ---- 4. flagged stray valid byte outside any frame: no drop, next frame fine
  { clear(); uint16_t d0 = dut->drop_cnt_o;
    dut->rx_valid_i = 1; dut->rx_data_i = 0x55; dut->rx_sof_i = 0; dut->rx_eof_i = 0; dut->rx_err_i = 1; tick(0);
    idle(2);
    F s = make("sync", 8); stream({{&s, {}}});
    expect("stray flagged byte then sync: event", ev_count == 1 ? ev_code : 0, 1);
    expect("stray flagged byte then sync: no drop", (uint16_t)(dut->drop_cnt_o - d0), 0); }
  // ---- 5. flag stacked on another refusal (bad EtherType / foreign domain): one drop
  for (int which = 0; which < 2; which++) {
    F f = make("sync", 9);
    if (which == 0) f.b[12] = 0x86; else f.b[18] = 7;
    for (size_t p : {size_t(0), size_t(13), size_t(30), f.b.size() - 1}) {
      std::vector<bool> m(f.b.size(), false); m[p] = true;
      clear(); uint16_t d0 = dut->drop_cnt_o; stream({{&f, m}});
      expect(std::string(which ? "foreign domain" : "bad ethertype") + " + flag at " + std::to_string(p) + ": one drop",
             (uint16_t)(dut->drop_cnt_o - d0), 1);
      expect(std::string(which ? "foreign domain" : "bad ethertype") + " + flag at " + std::to_string(p) + ": no event", ev_count, 0);
    }
  }
  // ---- 6. zero-gap refused (flag on eof, so it leaves every word) -> clean, all kind pairs;
  //         the clean event must see each word the clean clean-run wrote, with its value
  for (const auto &kr : kinds) for (const auto &kc : kinds) {
    F r = make(kr, 0x21), c = make(kc, 0x42);
    clear(); stream({{&c, {}}});                      // reference: what c writes
    std::map<unsigned, uint64_t> cw; for (auto &w : wlog) cw[w.addr] = w.data;
    clear(); uint16_t d0 = dut->drop_cnt_o;
    std::vector<bool> m(r.b.size(), false); m.back() = true;
    stream({{&r, m}, {&c, {}}});
    std::string n = kc + " after refused " + kr;
    expect(n + ": one drop", (uint16_t)(dut->drop_cnt_o - d0), 1);
    expect(n + ": one event of its code", ev_count == 1 ? ev_code : 0, code_of(kc));
    size_t wrong = 0;
    for (auto &[a, v] : cw) if (!ev_bank.count(a) || ev_bank[a] != v) wrong++;
    expect(n + ": every word it writes is its own at the event", wrong, 0);
    // also flagged mid-frame (byte 30) instead of at eof
    clear(); d0 = dut->drop_cnt_o;
    std::vector<bool> m2(r.b.size(), false); m2[30] = true;
    stream({{&r, m2}, {&c, {}}});
    expect(n + " (flag at 30): one drop", (uint16_t)(dut->drop_cnt_o - d0), 1);
    expect(n + " (flag at 30): one event", ev_count == 1 ? ev_code : 0, code_of(kc));
  }
  // ---- 7. a flagged frame whose eof edge coincides with a following runt's drop
  { F r = make("sync", 0x31); F one; one.u8(1);
    std::vector<bool> m(r.b.size(), false); m[20] = true;
    clear(); uint16_t d0 = dut->drop_cnt_o; stream({{&r, m}, {&one, {false}}});
    expect("flagged sync then zero-gap runt: two drops", (uint16_t)(dut->drop_cnt_o - d0), 2);
    clear(); d0 = dut->drop_cnt_o; stream({{&r, m}, {&one, {true}}});
    expect("flagged sync then zero-gap flagged runt: two drops", (uint16_t)(dut->drop_cnt_o - d0), 2);
    expect("flagged sync then zero-gap flagged runt: no event", ev_count, 0); }
  // ---- 8. clean frame, then a zero-gap frame flagged on its FIRST byte: first dispatches
  { F a = make("pdresp", 0x51), b = make("sync", 0x52);
    std::vector<bool> m(b.b.size(), false); m[0] = true;
    clear(); uint16_t d0 = dut->drop_cnt_o; stream({{&a, {}}, {&b, m}});
    expect("clean pdresp then sof-flagged sync: pdresp event", ev_count == 1 ? ev_code : 0, 5);
    expect("clean pdresp then sof-flagged sync: one drop", (uint16_t)(dut->drop_cnt_o - d0), 1);
    expect("sof-flagged successor: no write from it", wlog.empty() ? 0 : (wlog.back().edge >= (int)a.b.size()), 0); }
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

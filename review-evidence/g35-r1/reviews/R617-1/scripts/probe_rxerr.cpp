// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer-owned, independent rx_err_i probe for KL_gptp_rx_parser.
// Frame builders and checks are written from the module header and the
// 802.1AS layouts, not taken from the project's parser bench. Built against
// any parser RTL (base or head); prints one TSV row per measurement and a
// tally of the head contract checks ("CHECK" lines). Exit 0 always: the
// caller compares base and head output.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include "VKL_gptp_rx_parser.h"
#include "verilated.h"

using Bytes = std::vector<uint8_t>;
static VKL_gptp_rx_parser *d;
static long writes = 0, events = 0;
static int last_code = 0;
static long checks = 0, fails = 0;

static void tick() {
  d->clk_i = 0; d->eval();
  d->clk_i = 1; d->eval();
  if (d->bank_we_o) writes++;
  if (d->ev_valid_o) { events++; last_code = d->ev_code_o; }
}
static void idle(int n, bool err = false) {
  d->rx_valid_i = 0; d->rx_sof_i = 0; d->rx_eof_i = 0; d->rx_err_i = err;
  for (int i = 0; i < n; i++) tick();
  d->rx_err_i = 0;
}
static void put(uint8_t b, bool sof, bool eof, bool err) {
  d->rx_valid_i = 1; d->rx_data_i = b; d->rx_sof_i = sof; d->rx_eof_i = eof;
  d->rx_err_i = err; tick();
}

static void be(Bytes &f, uint64_t v, int n) {
  for (int i = n - 1; i >= 0; i--) f.push_back((v >> (8 * i)) & 0xFF);
}
static const uint64_t GM = 0x0011223344556677ull;
// Ethernet II header + 34-octet PTP common header; body appended by caller.
static Bytes hdr(int mtype, int msglen, uint16_t seq) {
  Bytes f;
  be(f, 0x0180C200000Eull, 6); be(f, 0x020000000001ull, 6); be(f, 0x88F7, 2);
  f.push_back(0x10 | mtype);       // transportSpecific 1, messageType
  f.push_back(0x02);               // versionPTP 2
  be(f, msglen, 2);
  f.push_back(0x00);               // domainNumber 0
  f.push_back(0x00);
  be(f, 0x0208, 2);                // flags
  be(f, 0, 8);                     // correctionField
  be(f, 0, 4);
  be(f, 0xAABBCCFFFE001122ull, 8); be(f, 1, 2);   // sourcePortIdentity
  be(f, seq, 2);
  f.push_back(0x00); f.push_back(0xFD);
  return f;
}
static Bytes mk(const std::string &t) {
  Bytes f;
  if (t == "sync") { f = hdr(0x0, 44, 0x100); be(f, 0x12345678, 6); be(f, 0x1DCD6500, 4); }
  else if (t == "fu") {
    f = hdr(0x8, 76, 0x101); be(f, 0x12345678, 6); be(f, 0x1000, 4);
    be(f, 0x0003, 2); be(f, 28, 2); be(f, 0x0080C2, 3); be(f, 1, 3);
    be(f, 0, 4); be(f, 0, 2); be(f, 0, 8); be(f, 0, 4); be(f, 0, 4);
  } else if (t == "pdreq") { f = hdr(0x2, 54, 0x102); be(f, 0, 10); be(f, 0, 10); }
  else if (t == "pdresp") { f = hdr(0x3, 54, 0x103); be(f, 0xABCD, 6); be(f, 7, 4); be(f, 0x00220FFFFE334455ull, 8); be(f, 2, 2); }
  else if (t == "pdrfu") { f = hdr(0xA, 54, 0x104); be(f, 0xABCE, 6); be(f, 9, 4); be(f, 0x00220FFFFE334455ull, 8); be(f, 2, 2); }
  else if (t == "signal") { f = hdr(0xC, 44, 0x105); be(f, 0x00220FFFFE334455ull, 8); be(f, 2, 2); }
  else if (t == "announce") {
    // fixed 64-octet body + PATH_TRACE with stepsRemoved+1 = 1 identity (GM)
    f = hdr(0xB, 76, 0x106); be(f, 0, 10);
    be(f, 37, 2); f.push_back(0); f.push_back(246); be(f, 0xF8FE436A, 4);
    f.push_back(248); be(f, GM, 8); be(f, 0, 2); f.push_back(0xA0);
    be(f, 0x0008, 2); be(f, 8, 2); be(f, GM, 8);
  } else if (t == "sync_pad") { f = mk("sync"); f.push_back(0); f.push_back(0); }
  return f;
}

struct R { long drops, evs, code, own, later; };
// Stream f with rx_err_i on the bytes where err[i]; returns deltas.
static R run(const Bytes &f, const std::vector<bool> &err) {
  long d0 = d->drop_cnt_o, w0 = writes, e0 = events;
  long first = -1, own = 0;
  last_code = 0;
  for (size_t i = 0; i < f.size(); i++) {
    long wb = writes;
    put(f[i], i == 0, i + 1 == f.size(), err[i]);
    if (err[i] && first < 0) { first = (long)i; own = writes - wb; w0 = writes; }
  }
  idle(4);
  R r{(long)(uint16_t)(d->drop_cnt_o - d0), events - e0, last_code,
      own, first < 0 ? 0 : writes - w0};
  return r;
}
static void check(bool ok, const std::string &what) {
  checks++;
  if (!ok) { fails++; printf("CHECK FAIL %s\n", what.c_str()); }
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  d = new VKL_gptp_rx_parser;
  d->local_clock_id_i = 0x0102030405060708ull; d->local_clock_valid_i = 1;
  d->rst_n = 0; idle(4); d->rst_n = 1; idle(2);
  const char *types[] = {"sync", "fu", "pdreq", "pdresp", "pdrfu", "signal",
                         "announce", "sync_pad"};
  const int codes[] = {1, 2, 4, 5, 6, 7, 3, 1};
  printf("type\tlen\tcase\tpos\tdrops\tevents\town_write\tlater_writes\n");
  for (int k = 0; k < 8; k++) {
    std::string t = types[k];
    Bytes f = mk(t);
    size_t n = f.size();
    R c = run(f, std::vector<bool>(n, false));
    printf("%s\t%zu\tclean\t-\t%ld\t%ld\t-\t-\n", t.c_str(), n, c.drops, c.evs);
    check(c.drops == 0 && c.evs == 1 && c.code == codes[k], t + " clean control dispatches");
    long ok1 = 0, ownw = 0;
    for (size_t p = 0; p < n; p++) {
      std::vector<bool> e(n, false); e[p] = true;
      R r = run(f, e);
      printf("%s\t%zu\tpulse\t%zu\t%ld\t%ld\t%ld\t%ld\n", t.c_str(), n, p, r.drops, r.evs, r.own, r.later);
      ok1 += (r.drops == 1 && r.evs == 0 && r.later == 0);
      ownw += r.own;
    }
    check(ok1 == (long)n, t + " single pulse at every byte: one drop, no event, no later write");
    printf("%s\t%zu\tpulse_own_writes_total\t-\t-\t-\t%ld\t-\n", t.c_str(), n, ownw);
    long okh = 0;
    for (size_t p = 0; p < n; p++) {
      std::vector<bool> e(n, false);
      for (size_t i = p; i < n; i++) e[i] = true;
      R r = run(f, e);
      okh += (r.drops == 1 && r.evs == 0);
    }
    check(okh == (long)n, t + " held from every byte to eof: one drop, no event");
    printf("%s\t%zu\theld_ok\t-\t%ld/%zu\t-\t-\t-\n", t.c_str(), n, okh, n);
    // pseudo-random multi-pulse patterns
    uint32_t s = 0x35u + k; long okm = 0;
    for (int it = 0; it < 64; it++) {
      std::vector<bool> e(n, false);
      for (size_t i = 0; i < n; i++) { s = s * 1103515245u + 12345u; e[i] = ((s >> 16) & 7) == 0; }
      e[(s >> 8) % n] = true;
      R r = run(f, e);
      okm += (r.drops == 1 && r.evs == 0 && r.later == 0);
    }
    check(okm == 64, t + " 64 multi-pulse patterns: one drop, no event, no later write");
    R a = run(f, std::vector<bool>(n, true));
    check(a.drops == 1 && a.evs == 0 && a.own == 0 && a.later == 0, t + " every byte flagged: one drop, nothing written");
    R c2 = run(f, std::vector<bool>(n, false));
    check(c2.drops == 0 && c2.evs == 1, t + " clean after the sweeps dispatches");
  }
  Bytes sync = mk("sync"); size_t n = sync.size();
  // one-byte frame with the flag: one drop (runt arm), not two
  { long d0 = d->drop_cnt_o; put(0x01, true, true, true); idle(4);
    check((uint16_t)(d->drop_cnt_o - d0) == 1, "one-byte frame with rx_err: one drop");
    R c = run(sync, std::vector<bool>(n, false)); check(c.evs == 1 && c.drops == 0, "clean after flagged runt"); }
  // zero gap: clean A, then B whose sof byte is flagged (B's sof lands on A's fin cycle)
  { long d0 = d->drop_cnt_o, e0 = events;
    for (size_t i = 0; i < n; i++) put(sync[i], i == 0, i + 1 == n, false);
    for (size_t i = 0; i < n; i++) put(sync[i], i == 0, i + 1 == n, i == 0);
    idle(4);
    check(events - e0 == 1 && (uint16_t)(d->drop_cnt_o - d0) == 1, "zero gap: clean then sof-flagged: one event, one drop"); }
  // zero gap: eof-flagged A then clean B
  { long d0 = d->drop_cnt_o, e0 = events;
    for (size_t i = 0; i < n; i++) put(sync[i], i == 0, i + 1 == n, i + 1 == n);
    for (size_t i = 0; i < n; i++) put(sync[i], i == 0, i + 1 == n, false);
    idle(4);
    check(events - e0 == 1 && (uint16_t)(d->drop_cnt_o - d0) == 1, "zero gap: eof-flagged then clean: one event, one drop"); }
  // zero gap: mid-flagged A then flagged-sof one-byte runt, same edge as A's fin
  { long d0 = d->drop_cnt_o, e0 = events;
    for (size_t i = 0; i < n; i++) put(sync[i], i == 0, i + 1 == n, i == 30);
    put(0x01, true, true, true); idle(4);
    check(events - e0 == 0 && (uint16_t)(d->drop_cnt_o - d0) == 2, "zero gap: mid-flagged then flagged runt: two drops"); }
  // stray valid bytes outside any frame carrying the flag, then a clean frame
  { long d0 = d->drop_cnt_o;
    for (int i = 0; i < 5; i++) put(0xEE, false, false, true);
    R c = run(sync, std::vector<bool>(n, false));
    check(c.evs == 1 && (uint16_t)(d->drop_cnt_o - d0) == 0, "flagged stray bytes outside a frame do not poison the next frame"); }
  // a frame abandoned without eof after a flag, then a clean frame
  { long d0 = d->drop_cnt_o;
    for (size_t i = 0; i < 30; i++) put(sync[i], i == 0, false, i == 10);
    R c = run(sync, std::vector<bool>(n, false));
    check(c.evs == 1 && (uint16_t)(d->drop_cnt_o - d0) == 0, "abandoned flagged frame then clean frame dispatches"); }
  // flag in every idle gap (rx_valid_i low) is ignored
  { long d0 = d->drop_cnt_o, e0 = events;
    for (size_t i = 0; i < n; i++) { if (i) idle(1, true); put(sync[i], i == 0, i + 1 == n, false); }
    idle(4);
    check(events - e0 == 1 && (uint16_t)(d->drop_cnt_o - d0) == 0, "flag only in valid-low gaps: dispatches"); }
  // another refusal arm plus the flag still counts once
  { Bytes bad = sync; bad[13] = 0xF8; std::vector<bool> e(n, false); e[40] = true;
    R r = run(bad, e); check(r.drops == 1 && r.evs == 0, "ethertype refusal plus rx_err: one drop"); }
  printf("%ld checks: %ld PASS, %ld FAIL\n", checks, checks - fails, fails);
  delete d;
  return 0;
}

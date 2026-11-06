// Constrained-random check of KL_srp_encoder against an independent reference
// of the merge table in docs/architecture/10_srp_engine.md section 3.
// Every committed MRPDU is parsed, each VectorAttribute range is expanded, and
// the list of (type, value, event, declaration) must equal the reference table
// entry for entry. That covers a doubled value, a lost value and a wrong merge.
#include "VKL_srp_encoder.h"
#include "verilated.h"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <vector>
using Val = std::array<uint8_t, 34>;
struct Ent { int type; int ev; int fp; Val v; };
static VKL_srp_encoder* d;
static std::mt19937_64 rng;
static uint32_t R(uint32_t n) { return static_cast<uint32_t>(rng() % n); }
static bool same_key(bool mvrp, const Ent& a, int t, const Val& v) {
  if (mvrp) return a.v[0] == v[0] && a.v[1] == v[1];
  return a.type == t && !std::memcmp(a.v.data(), v.data(), 8);
}
static int merged(int o, int n) {
  const bool oS = o == 2 || o == 4;
  const bool nS = n == 2 || n == 4;
  if (n == 0 || n == 5) return n;
  if (!nS) return o == 0 ? 0 : n;
  return oS ? n : o;
}
static void set_value(const Val& v) {
  for (int w = 0; w < 9; w++) d->ev_value_i[w] = 0;
  for (int b = 0; b < 34; b++) {
    const int pos = 264 - 8 * b;
    d->ev_value_i[pos / 32] |= static_cast<uint32_t>(v[b]) << (pos % 32);
  }
}
struct Offer { bool on; bool app; int type; int ev; int fp; Val v; };
static Offer mk() {
  Offer o{}; o.on = true; o.app = R(3) == 0; o.v.fill(0);
  static const int evs[] = {0, 1, 2, 3, 4, 5};
  o.ev = evs[R(6)]; o.fp = o.app ? 0 : static_cast<int>(R(4));
  if (o.app) { o.type = 1; o.v[1] = static_cast<uint8_t>(2 + R(7)); return o; }
  o.type = 1 + static_cast<int>(R(4));
  if (R(64) == 0) o.type = R(2) ? 0 : 9;        // an unknown type is dropped
  if (o.type == 4) {
    const int c = 5 + static_cast<int>(R(3));
    o.v[0] = static_cast<uint8_t>(c); o.v[1] = static_cast<uint8_t>(c - 3); o.v[3] = 2;
  } else {
    // a few StreamIDs that differ in the Unique ID, and a few in the MAC only
    const int u = static_cast<int>(R(6));
    o.v[0] = static_cast<uint8_t>(R(4) == 0 ? 0x91 : 0x90);
    o.v[5] = 0x11; o.v[7] = static_cast<uint8_t>(u);
    if (o.type == 1 || o.type == 2) {
      o.v[13] = static_cast<uint8_t>(0x20 + u);   // the DA moves with the StreamID
      o.v[15] = 2; o.v[21] = static_cast<uint8_t>(R(8) == 0 ? 7 : 6);  // payload
    }
  }
  return o;
}
static long frames, pushes, hits, drops, mism, doubled, la_frames, maxstall;
static std::vector<Ent> tbl[2];
static uint8_t buf[2048];
static void fail(const char* m, long t) { mism++; if (mism < 6) printf("MISMATCH t=%ld: %s\n", t, m); }
static void check_frame(int len, long t) {
  const bool mvrp = buf[12] == 0x88;
  std::vector<Ent> got;
  int p = 15;
  bool la = false;
  while (p + 1 < len && !(buf[p] == 0 && buf[p + 1] == 0)) {
    const int type = buf[p]; const int alen = buf[p + 1];
    int q = p + (mvrp ? 2 : 4);
    int vectors = 0;
    while (!(buf[q] == 0 && buf[q + 1] == 0)) {
      const int la3 = buf[q] >> 5; la |= la3 != 0;
      const int nov = ((buf[q] & 0x1F) << 8) | buf[q + 1];
      q += 2; Val fv; fv.fill(0); std::memcpy(fv.data(), buf + q, alen); q += alen;
      const int n3 = (nov + 2) / 3; const int n4 = (!mvrp && type == 3) ? (nov + 3) / 4 : 0;
      for (int k = 0; k < nov; k++) {
        const int by = buf[q + k / 3]; const int ev = k % 3 == 0 ? by / 36 : k % 3 == 1 ? (by / 6) % 6 : by % 6;
        int fp = 0;
        if (n4) { const int b4 = buf[q + n3 + k / 4]; fp = (b4 >> (6 - 2 * (k % 4))) & 3; }
        Val v = fv;
        if (mvrp) v[1] = static_cast<uint8_t>(v[1] + k);
        else if (type == 4) { v[0] = static_cast<uint8_t>(v[0] + k); v[1] = static_cast<uint8_t>(v[1] + k); }
        else { v[7] = static_cast<uint8_t>(v[7] + k); if (type != 3) v[13] = static_cast<uint8_t>(v[13] + k); }
        got.push_back(Ent{type, ev, fp, v});
      }
      q += n3 + n4; vectors++;
      if (q >= len) { fail("vector overrun", t); return; }
    }
    p = q + 2;
  }
  if (la) la_frames++;
  std::vector<Ent>& e = tbl[mvrp];
  for (size_t i = 0; i < got.size(); i++)
    for (size_t j = i + 1; j < got.size(); j++)
      if (same_key(mvrp, got[i], got[j].type, got[j].v)) { doubled++; fail("value twice in one MRPDU", t); }
  bool ok = got.size() == e.size();
  for (size_t i = 0; ok && i < e.size(); i++)
    ok = got[i].type == e[i].type && got[i].ev == e[i].ev && (got[i].type != 3 || mvrp || got[i].fp == e[i].fp)
      && !std::memcmp(got[i].v.data(), e[i].v.data(), 34);
  if (!ok) {
    char m[200]; std::snprintf(m, sizeof m, "%s frame: %zu values, reference %zu", mvrp ? "MVRP" : "MSRP", got.size(), e.size());
    fail(m, t);
    for (auto& x : got) printf("  got t%d ev%d fp%d id%02x%02x\n", x.type, x.ev, x.fp, x.v[0], x.v[7]);
    for (auto& x : e) printf("  ref t%d ev%d fp%d id%02x%02x\n", x.type, x.ev, x.fp, x.v[0], x.v[7]);
  }
  e.clear(); frames++;
}
static void tick() { d->clk_i = 1; d->eval(); d->clk_i = 0; d->eval(); }
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const uint64_t seed = argc > 1 ? std::strtoull(argv[1], nullptr, 0) : 1;
  const long cycles = argc > 2 ? std::atol(argv[2]) : 2000000;
  const int density = argc > 3 ? std::atoi(argv[3]) : 3;
  rng.seed(seed);
  d = new VKL_srp_encoder;
  d->rst_n = 0; d->clk_i = 0; d->ev_valid_i = 0; d->join_tick_i = 0; d->leaveall_i = 0;
  d->la_prepare_i = 0; d->la_cancel_i = 0; d->alloc_gnt_i = 0; d->txreq_ready_i = 0; d->own_mac_i = 0x0250C2000001ull;
  for (int i = 0; i < 4; i++) tick();
  d->rst_n = 1;
  Offer o{}; bool prep = false; long stall = 0; int gnt_wait = -1; int hold_tx = 0; int after_prep = -1;
  for (long t = 0; t < cycles; t++) {
    if (!o.on && R(density) == 0) o = mk();
    else if (o.on && R(16) == 0) { if (R(4) == 0) o.on = false; else o = mk(); }  // re-arbitrate or withdraw
    d->ev_valid_i = o.on; d->ev_app_i = o.app; d->ev_attr_type_i = o.type; d->ev_event_i = o.ev;
    d->ev_fourpack_i = o.fp; set_value(o.v);
    d->join_tick_i = (R(120) == 0 ? 1 : 0) | (R(120) == 0 ? 2 : 0);
    d->leaveall_i = (R(700) == 0 ? 1 : 0) | (R(700) == 0 ? 2 : 0);
    if (!prep && after_prep < 0 && R(900) == 0) prep = true;
    d->la_prepare_i = prep; d->la_cancel_i = prep && R(12) == 0;
    if (after_prep > 0 && --after_prep == 0) { d->join_tick_i = d->join_tick_i | 1; after_prep = -1; }
    d->alloc_gnt_i = 0;
    if (gnt_wait == 0) { d->alloc_gnt_i = 1; d->alloc_slot_i = R(4); gnt_wait = -1; }
    else if (gnt_wait > 0) gnt_wait--;
    if (hold_tx > 0) { hold_tx--; d->txreq_ready_i = 0; }
    else { d->txreq_ready_i = R(3) == 0; if (R(300) == 0) hold_tx = 400; }
    d->eval();
    if (d->alloc_req_o && gnt_wait < 0 && !d->alloc_gnt_i) gnt_wait = static_cast<int>(R(6));
    const bool acc = o.on && d->ev_ready_o;
    const bool done = d->la_prepare_done_o;
    if (d->wr_valid_o) buf[d->wr_addr_o] = d->wr_data_o;
    const bool commit = d->wr_commit_o; const int len = d->wr_len_o;
    if (acc) {
      pushes++;
      const bool known = o.app ? o.type == 1 : (o.type >= 1 && o.type <= 4);
      if (!known) drops++;
      else {
        auto& e = tbl[o.app];
        bool hit = false;
        for (Ent& x : e) if (same_key(o.app, x, o.type, o.v)) {
          const int m = merged(x.ev, o.ev);
          const bool nS = o.ev == 2 || o.ev == 4; const bool oS = x.ev == 2 || x.ev == 4;
          x.fp = (nS && !oS) ? x.fp : o.fp; x.ev = m; x.v = o.v; x.type = o.type; hit = true; hits++; break;
        }
        if (!hit) {
          Val v = o.v;
          e.push_back(Ent{o.type, o.ev, o.fp, v});
        }
      }
      o.on = false; stall = 0;
    } else if (o.on) { if (++stall > maxstall) maxstall = stall; }
    tick();
    if (commit) check_frame(len, t);
    if (done) { prep = false; after_prep = 1 + static_cast<int>(R(24)); }
  }
  printf("seed=%llu cycles=%ld frames=%ld la_frames=%ld pushes=%ld merged=%ld dropped=%ld doubled=%ld mismatches=%ld max_stall=%ld left={%zu,%zu}\n",
         static_cast<unsigned long long>(seed), cycles, frames, la_frames, pushes, hits, drops, doubled, mism, maxstall, tbl[0].size(), tbl[1].size());
  d->final(); delete d;
  return mism != 0 ? 1 : 0;
}

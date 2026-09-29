// SPDX-License-Identifier: CERN-OHL-W-2.0
// R400-2 reviewer probe for KL_pp_maap's Release! handling, built against the
// head's tb/maap/maap_wrap.sv (replace sim_main.cpp with this file).
//
// Expectations come from IEEE 1722-2016 Annex B as ruled on #66 (comment
// 5890772857): Table B.7 Release! (stop the running timer, INITIAL, no
// sProbe/sAnnounce/sDefend), B.3.1 c)/e) (a stopped timer does not expire),
// B.3.2 (a frame whose TX slot the entry requested before the fall may drain),
// B.3.5.2 (the claim ends at the fall), then PortOperational! -> a fresh walk.
//
//  PA  one-cycle falls first seen in each TX-path walker state (and W_IVAL,
//      W_POST), in three entries: a PROBE retransmit, a DEFEND re-announce and
//      an sDefend. Required: INITIAL is reached, no claim is valid from the
//      cycle after the fall, and the next claim is preceded by a FRESH 4-PROBE
//      walk (a Release! is never absorbed).
//  PB  long falls (held 33 s) swept cycle by cycle from four anchors: a probe
//      expiry, an announce expiry, an sDefend record, a yielding rAnnounce!.
//      Required from the cycle after the fall is first seen: no TX slot
//      request, no timer start, no timer expiry, no valid claim, INITIAL at
//      the end, and at most the one frame requested by then drains, of the
//      entry's own message type, on the lane within 63 cycles of the fall.
//
// The walker state (walker_o) is read only to land a fall; never an oracle.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "Vmaap_wrap.h"
#include "verilated.h"

typedef std::vector<uint8_t> Bytes;
static int checks = 0, fails = 0;
#define CHECK(c, ...) do { ++checks; if (!(c)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } } while (0)

constexpr uint64_t OWN_MAC = 0x02AABBCCDDEEull;
constexpr uint64_t LOSE_MAC = 0xF21122334401ull;   // reversed-lower: we lose
constexpr int CLK_PER_MS = 10;
enum { WK_OFF, WK_IDLE, WK_ADDR, WK_IVAL, WK_ALLOC, WK_GWAIT, WK_WRITE, WK_COMMIT,
       WK_LANE, WK_POST, WK_RX, WK_TEARDOWN };
static const char* WN[] = {"W_OFF", "W_IDLE", "W_ADDR", "W_IVAL", "W_ALLOC", "W_GWAIT",
                           "W_WRITE", "W_COMMIT", "W_LANE", "W_POST", "W_RX", "W_TEARDOWN"};

struct Frame { Bytes b; uint64_t cyc; };

struct H {
  Vmaap_wrap* d;
  uint64_t cyc = 0;
  bool ser_busy = false;
  Bytes cur;
  uint64_t cur_cyc = 0;
  std::vector<Frame> tx;
  uint64_t grants = 0, slot_reqs = 0, starts = 0, expiries = 0;
  uint64_t last_grant_cyc = 0;
  explicit H(Vmaap_wrap* dd) : d(dd) {}
  void step() {
    d->clk_i = 0; d->eval();
    d->txreq_ready_i = 0; d->ser_ready_i = 1; d->conflict_ack_i = d->conflict_valid_o;
    if (!ser_busy && d->txreq_valid_o) {
      d->txreq_ready_i = 1; d->ser_req_i = 1; d->ser_slot_i = d->txreq_slot_o;
      ser_busy = true; cur.clear(); cur_cyc = cyc; ++grants; last_grant_cyc = cyc;
    }
    if (ser_busy && d->ser_valid_o) {
      d->ser_req_i = 0; cur.push_back(d->ser_data_o);
      if (d->ser_last_o) { tx.push_back({cur, cur_cyc}); ser_busy = false; }
    }
    d->eval();
    if (d->slot_req_o) ++slot_reqs;
    if (d->tmr_start_o) ++starts;
    if (d->tmr_exp_o) ++expiries;
    d->clk_i = 1; d->eval();
    ++cyc;
  }
  void idle(long n) { for (long i = 0; i < n; ++i) step(); }
  bool wait_frames(size_t n, long ms) { long c = ms * CLK_PER_MS; while (tx.size() < n && c-- > 0) step(); return tx.size() >= n; }
  bool run_to(unsigned st, long budget) { for (long c = 0; c < budget && d->walker_o != st; ++c) step(); return d->walker_o == st; }
  bool wait_expiry(long ms) { uint64_t e = expiries; long c = ms * CLK_PER_MS; while (expiries == e && c-- > 0) step(); return expiries > e; }
  bool accept(int msg, uint64_t sa, uint64_t start, uint16_t cnt) {
    d->txn_msg_i = msg; d->txn_status_i = 1; d->txn_src_mac_i = sa;
    d->txn_req_i = (start << 16) | cnt; d->txn_conf_i = 0; d->txn_valid_i = 1;
    bool taken = false;
    for (int g = 0; g < 200 && !taken; ++g) {
      d->clk_i = 0; d->eval(); taken = d->txn_ready_o; step();
    }
    d->txn_valid_i = 0;
    return taken;
  }
};

static int msg_of(const Bytes& b) { return b.size() > 15 ? (b[15] & 0x0F) : -1; }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Vmaap_wrap* d = new Vmaap_wrap;
  H h(d);
  d->rst_n = 0; d->cfg_en_i = 1; d->cfg_count_i = 8; d->cfg_seed_valid_i = 0; d->cfg_seed_offset_i = 0;
  d->own_mac_i = OWN_MAC; d->entity_id_i = 0x001BC5FFFE000042ull; d->link_up_i = 0;
  d->txn_valid_i = 0; d->alloc_req_valid_i = 0; d->addr_stub_en_i = 0; d->ser_ready_i = 1;
  h.idle(20); d->rst_n = 1; h.idle(10);

  auto release = [&]() { d->link_up_i = 0; h.idle(30); };
  auto engage_to_probe = [&]() -> bool { release(); size_t n = h.tx.size(); d->link_up_i = 1; return h.wait_frames(n + 1, 700); };
  auto engage_to_defend = [&]() -> bool {
    if (!engage_to_probe()) return false;
    for (int g = 0; g < 10 && !d->addr_valid_o; ++g) h.idle(700L * CLK_PER_MS);
    return d->addr_valid_o;
  };

  // ------------------------------------------------------------------ PA
  enum Ctx { PROBE_RETX, DEFEND_ANN, DEFEND_SDEF, N_CTX };
  const char* ctxn[] = {"PROBE retransmit", "DEFEND re-announce", "sDefend"};
  const unsigned pa_states[] = {WK_IVAL, WK_ALLOC, WK_GWAIT, WK_WRITE, WK_COMMIT, WK_LANE, WK_POST};
  int pa_absorbed = 0, pa_claim = 0, pa_poise = 0, pa_total = 0;
  for (int c = 0; c < N_CTX; ++c) {
    for (unsigned st : pa_states) {
      if (c == DEFEND_SDEF && st == WK_IVAL) continue;          // sDefend draws no interval
      ++pa_total;
      bool ok = (c == PROBE_RETX) ? engage_to_probe() : engage_to_defend();
      if (ok && c == PROBE_RETX) ok = h.wait_expiry(700);        // 2nd PROBE entry starts
      if (ok && c == DEFEND_ANN) ok = h.wait_expiry(33000);      // re-announce entry starts
      if (ok && c == DEFEND_SDEF) ok = h.accept(1, 0x0A2233445566ull, d->addr_o + 2, 2);
      const uint64_t r_anchor = h.slot_reqs, g_anchor = h.grants;
      if (ok) ok = h.run_to(st, 2000);
      if (!ok) { ++pa_poise; printf("  PA %s %s: could not poise (walker %s)\n", ctxn[c], WN[st], WN[d->walker_o & 15]); continue; }
      d->link_up_i = 0; h.step();                                // the one cycle it is seen
      const uint64_t fall_cyc = h.cyc - 1;
      d->link_up_i = 1;
      // the entry's slot requests (up to and including the fall cycle) not yet on the lane
      const uint64_t owed = (h.slot_reqs - r_anchor) - (h.grants - g_anchor);
      bool initial = (d->state_o == 0), valid_after = false;
      for (long k = 0; k < 10L * 700 * CLK_PER_MS && (k < 100 || !d->addr_valid_o); ++k) {
        h.step();
        if (d->state_o == 0) initial = true;
        if (d->addr_valid_o && k < 50L * CLK_PER_MS) valid_after = true;
      }
      h.idle(200);                                               // the claim's ANNOUNCE serializes
      // frames the lane took after the fall; the first is the drained one if owed
      std::vector<int> seq;
      for (const Frame& f : h.tx) if (f.cyc > fall_cyc) seq.push_back(msg_of(f.b));
      const size_t i0 = (owed == 1 && !seq.empty()) ? 1 : 0;
      int fresh_probes = 0;
      bool saw_ann = false;
      for (size_t i = i0; i < seq.size(); ++i) {
        if (seq[i] == 3) { saw_ann = true; break; }
        if (seq[i] == 1) ++fresh_probes;
      }
      const bool fresh = initial && saw_ann && fresh_probes == 4;
      if (!fresh) ++pa_absorbed;
      if (valid_after && c != PROBE_RETX) ++pa_claim;
      printf("  PA %s, 1-cycle fall in %s: owed=%d INITIAL=%d frames=", ctxn[c], WN[st], int(owed), int(initial));
      if (owed > 1) ++pa_absorbed;
      for (int m : seq) printf("%d", m);
      printf(" fresh=%d%s\n", fresh_probes, fresh ? "" : "  <-- Release! absorbed");
    }
  }
  CHECK(pa_poise == 0, "PA: premise, every short fall is poised (%d of %d missed)", pa_poise, pa_total);
  CHECK(pa_absorbed == 0, "PA: a one-cycle Release! in a TX-path state gives INITIAL and a fresh 4-PROBE walk (%d of %d absorbed)", pa_absorbed, pa_total);
  CHECK(pa_claim == 0, "PA: no claim is valid within 50 ms of a one-cycle Release! (%d of %d)", pa_claim, pa_total);

  // ------------------------------------------------------------------ PB
  enum Anchor { A_PROBE_EXP, A_ANN_EXP, A_SDEFEND, A_YIELD, N_ANCH };
  const char* an[] = {"probe expiry", "announce expiry", "sDefend record", "yielding rAnnounce!"};
  const int want_msg[] = {1, 3, 2, 1};
  const int offsets = 100;
  const long watch = 33000L * CLK_PER_MS;
  for (int a = 0; a < N_ANCH; ++a) {
    int poise = 0, req = 0, st = 0, ex = 0, claim = 0, over = 0, wrong = 0, late = 0, drained = 0, dropped = 0;
    long lat_max = -1;
    for (int k = 0; k < offsets; ++k) {
      bool ok = (a == A_PROBE_EXP) ? engage_to_probe() : engage_to_defend();
      if (ok && a == A_PROBE_EXP) ok = h.wait_expiry(700);
      if (ok && a == A_ANN_EXP) ok = h.wait_expiry(33000);
      if (ok && a == A_SDEFEND) ok = h.accept(1, 0x0A2233445566ull, d->addr_o + 2, 2);
      if (ok && a == A_YIELD) ok = h.accept(3, LOSE_MAC, d->addr_o, 8);
      if (!ok) { ++poise; continue; }
      const uint64_t r_anchor = h.slot_reqs, g_anchor = h.grants;
      const size_t n_anchor = h.tx.size();
      h.idle(k);
      d->link_up_i = 0;
      h.step();                                                  // first cycle the fall is seen
      const uint64_t fall_cyc = h.cyc - 1;
      const uint64_t r0 = h.slot_reqs, s0 = h.starts, e0 = h.expiries, g0 = h.grants;
      const uint64_t owed = (h.slot_reqs - r_anchor) - (h.grants - g_anchor);
      bool valid_after = false;
      for (long c = 1; c < watch; ++c) { h.step(); if (d->addr_valid_o) valid_after = true; }
      if (h.slot_reqs != r0) ++req;
      if (h.starts != s0) ++st;
      if (h.expiries != e0) ++ex;
      if (valid_after || d->state_o != 0) ++claim;
      const uint64_t after = h.grants - g0;
      if (owed > 1 || after != owed) ++over;
      if (after == 1) {
        ++drained;
        const Frame& f = h.tx.back();
        if (msg_of(f.b) != want_msg[a] || h.tx.size() - n_anchor != 1) ++wrong;
        const long lat = long(h.last_grant_cyc - fall_cyc);
        if (lat > lat_max) lat_max = lat;
        if (lat > 63) ++late;
      } else if (after == 0) {
        ++dropped;
      }
    }
    printf("  PB %s: %d offsets, %d dropped, %d drained (max lane latency %ld cycles after the fall)\n",
           an[a], offsets, dropped, drained, lat_max);
    CHECK(poise == 0, "PB %s: premise, every anchor reached (%d missed)", an[a], poise);
    CHECK(dropped > 0 && drained > 0, "PB %s: premise, the sweep spans the slot request (%d/%d)", an[a], dropped, drained);
    CHECK(req == 0, "PB %s: no TX slot request after the fall (%d offsets)", an[a], req);
    CHECK(st == 0, "PB %s: no timer started after the fall (%d offsets)", an[a], st);
    CHECK(ex == 0, "PB %s: no timer expiry for 33 s after the fall (%d offsets)", an[a], ex);
    CHECK(claim == 0, "PB %s: no claim after the fall, INITIAL at the end (%d offsets)", an[a], claim);
    CHECK(over == 0, "PB %s: at most the one frame requested by the fall drains (%d offsets)", an[a], over);
    CHECK(wrong == 0, "PB %s: the drained frame is the entry's own message type (%d offsets)", an[a], wrong);
    CHECK(late == 0, "PB %s: the drained frame reaches the lane within 63 cycles of the fall (%d late)", an[a], late);
  }

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete d;
  return fails ? 1 : 0;
}

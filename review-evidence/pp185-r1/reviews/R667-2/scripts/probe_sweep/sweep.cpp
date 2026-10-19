// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (#185/#186 round 2): every LOCK_ENTITY notification carries one
// cause. Drives KL_aecp_notify with a cycle-level engine model that loads a
// presented LOCK job, reads the holder through the rgy face `gap` cycles later,
// runs `run` more cycles and then raises a ONE-CYCLE done strobe, as
// KL_aecp_engine's uns_done_o does. A solicited LOCK/UNLOCK is issued only while
// the engine model is idle, as the single-threaded engine would. Lock expiries
// are injected at clock offsets swept over every round. Checks per run:
//   A  each frame is the pair of one cause: a LOCK that took the lock (its
//      flags, its eid), an UNLOCK that released it (its flags, 0) or an expiry
//      (UNLOCK = 1, 0)
//   B  no frame carries a change to that change's own requester
//   C  each registered controller's LAST frame is the final state's pair (the
//      final change's requester exempt); after a final expiry every controller,
//      the former owner included, last saw (1, 0)
//   D  every done strobe lands while the job it retires is presented
//   E  the holder read is answered within 3 request cycles
//   F  each destination's sequence_id advances by exactly 1 per frame
// Exit 0 when every run passes.
#include <cstdint>
#include <cstdio>
#include <map>
#include <memory>
#include <string>
#include <vector>
#include "VKL_aecp_notify.h"
#include "verilated.h"

// main before #186 has no rgy_flags_i port: build with -DNO_FLAGS there
#ifdef NO_FLAGS
#define SET_FLAGS(d, v) ((void)(v))
#else
#define SET_FLAGS(d, v) ((d)->rgy_flags_i = (v))
#endif
static constexpr uint8_t KIND_LOCK = 1;
static constexpr uint8_t OWN_LOCK = 0xB0;
static constexpr uint8_t LOCK_SLOT = 61;
static constexpr uint32_t UNLOCK = 1;

struct Frame { uint64_t mac; uint16_t seq; uint32_t flags; uint64_t lid; };
struct Op { int t; bool unlock; uint64_t eid; uint32_t flags; };
struct Cause { uint32_t flags; uint64_t lid; uint64_t req; bool has_req; };
struct Row { uint64_t eid; uint64_t mac; };

struct Sim {
  std::unique_ptr<VerilatedContext> ctx{new VerilatedContext};
  std::unique_ptr<VKL_aecp_notify> d{new VKL_aecp_notify{ctx.get()}};
  void tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
  void reset() {
    d->now_ms_i = 40000; d->prng_draw_busy_i = 1; d->ca_ready_i = 1; d->uns_done_i = 0;
    d->rst_n = 0; for (int i = 0; i < 4; ++i) tick(); d->rst_n = 1; for (int i = 0; i < 2; ++i) tick();
  }
  bool reg(uint64_t eid, uint64_t mac) {
    d->rgy_state_i = 0; d->rgy_op_i = 0; d->rgy_eid_i = eid; d->rgy_mac_i = mac;
    d->rgy_tl_i = 0; d->rgy_req_i = 1;
    uint64_t r = ~0ull;
    for (int g = 0; g < 40; ++g) { d->clk_i = 0; d->eval(); if (!d->rgy_wait_o) { r = d->rgy_data_o; break; } tick(); }
    tick(); d->rgy_req_i = 0; tick(); tick();
    return r == 0;
  }
};

struct Params { int gap; int run; };
static int g_runs = 0, g_fails = 0;
static int g_ident_sent = 0;
static int g_press_at = -1;

static bool run_case(const std::string& name, const std::vector<Row>& rows,
                     std::vector<Op> ops, const std::vector<int>& exps, Params p) {
  ++g_runs;
  Sim s; s.reset();
  for (const Row& r : rows) if (!s.reg(r.eid, r.mac)) { printf("FAIL %s: register refused\n", name.c_str()); ++g_fails; return false; }
  std::vector<Frame> frames; std::vector<Cause> causes; std::vector<std::string> errs;
  enum { IDLE, LOADED, READ, RUN, OPS } st = IDLE;
#ifdef IDENT
  bool cur_ident = false; g_ident_sent = 0;
  s.d->uns_tx_busy_i = 0; s.d->identify_index_i = 0; s.d->identify_button_i = 0;
#endif
  Frame cur{}; Op cur_op{}; size_t next_op = 0; int op_gap = 0;
  int cnt = 0, read_cycles = 0, quiet = 0, t = 0;
  bool prev_held = s.d->lock_held_o;
  int last_fall = -1, last_unlock_fall = -2; Cause last_unlock{};
  for (; t < 8000; ++t) {
    s.d->uns_done_i = (st == RUN && cnt == 0);
#ifdef IDENT
    s.d->identify_button_i = (g_press_at >= 0 && t >= g_press_at && t < g_press_at + 40);
#endif
    s.d->tmr_exp_valid_i = 0;
    for (int e : exps) if (e == t) { s.d->tmr_exp_valid_i = 1; s.d->tmr_exp_slot_i = LOCK_SLOT; s.d->tmr_exp_owner_i = OWN_LOCK; }
    if (op_gap > 0) --op_gap;
    if (st == IDLE && op_gap == 0 && next_op < ops.size() && ops[next_op].t <= t) {
      cur_op = ops[next_op++]; st = OPS;
      s.d->rgy_state_i = 0; s.d->rgy_op_i = cur_op.unlock ? 3 : 2; s.d->rgy_eid_i = cur_op.eid;
      s.d->rgy_mac_i = 0; SET_FLAGS(s.d, cur_op.flags); s.d->rgy_req_i = 1;
    }
    if (st == READ) { s.d->rgy_state_i = 1; s.d->rgy_op_i = 0; s.d->rgy_eid_i = 0; s.d->rgy_req_i = 1; }
    s.d->clk_i = 0; s.d->eval();
    const bool held = s.d->lock_held_o;
    if (prev_held && !held) last_fall = t;
    prev_held = held;
    bool take = false, answered = false;
    if (st == IDLE && s.d->uns_valid_o) {
#ifdef IDENT
      if (s.d->uns_kind_o != KIND_LOCK && s.d->uns_kind_o != 15) errs.push_back("unexpected job kind");
#else
      if (s.d->uns_kind_o != KIND_LOCK) errs.push_back("non-LOCK job presented");
#endif
      take = true;
      cur = {static_cast<uint64_t>(s.d->uns_mac_o), static_cast<uint16_t>(s.d->uns_seq_o),
             (uint32_t(s.d->uns_arg1_o) << 16) | s.d->uns_arg0_o, 0};
#ifdef IDENT
      cur_ident = s.d->uns_kind_o == 15;
#endif
    } else if (st == READ) {
      ++read_cycles;
      if (!s.d->rgy_wait_o) {
        answered = true; cur.lid = s.d->rgy_data_o;
        if (read_cycles > 3) errs.push_back("E: holder read answered late");
      }
    } else if (st == RUN && cnt == 0) {
#ifdef IDENT
      if (cur_ident) {
        if (!(s.d->uns_valid_o && s.d->uns_kind_o == 15)) errs.push_back("D: IDENTIFY done while the IDENTIFY job is not presented");
        ++g_ident_sent;
      } else
#endif
      if (true) {
      const bool ok = s.d->uns_valid_o && s.d->uns_kind_o == KIND_LOCK
                      && static_cast<uint64_t>(s.d->uns_mac_o) == cur.mac && s.d->uns_seq_o == cur.seq;
      if (!ok) { char b[128]; snprintf(b, sizeof b, "D: done at t=%d while the job to %012llx seq %u is not presented", t, (unsigned long long)cur.mac, unsigned(cur.seq)); errs.push_back(b); }
      frames.push_back(cur);
      }
    } else if (st == OPS && !s.d->rgy_wait_o) {
      answered = true;
      const uint64_t r = s.d->rgy_data_o;
      if (!(r & 1) && (r & 2)) {
        Cause c{cur_op.flags, cur_op.unlock ? 0 : cur_op.eid, cur_op.eid, true};
        causes.push_back(c);
        if (cur_op.unlock) { last_unlock_fall = t; last_unlock = c; }
      }
    }
    s.d->clk_i = 1; s.d->eval();
#ifdef IDENT
    if (take && cur_ident) { st = RUN; cnt = p.run; }
    else
#endif
    if (take) { st = LOADED; cnt = p.gap; }
    else if (st == LOADED) { if (--cnt <= 0) { st = READ; read_cycles = 0; } }
    else if (st == READ && answered) { s.d->rgy_req_i = 0; s.d->rgy_state_i = 0; st = RUN; cnt = p.run; op_gap = 2; }
    else if (st == RUN) { if (cnt == 0) { st = IDLE; s.d->uns_done_i = 0; op_gap = 2; } else --cnt; }
    else if (st == OPS && answered) { s.d->rgy_req_i = 0; SET_FLAGS(s.d, 0); st = IDLE; op_gap = 2; }
    bool exp_left = false; for (int e : exps) if (e >= t) exp_left = true;
    const bool busy = st != IDLE || next_op < ops.size() || exp_left;
    quiet = busy ? 0 : quiet + 1;
    if (quiet > 300) break;
  }
  if (t >= 8000) errs.push_back("did not quiesce");
  const bool any_exp = !exps.empty();
  std::map<uint64_t, uint64_t> mac_of; for (const Row& r : rows) mac_of[r.eid] = r.mac;
  for (const Frame& f : frames) {
    bool legit = any_exp && f.flags == UNLOCK && f.lid == 0, to_req = false;
    for (const Cause& c : causes)
      if (c.flags == f.flags && c.lid == f.lid) {
        legit = true;
        if (mac_of.count(c.req) && mac_of[c.req] == f.mac && !(any_exp && f.flags == UNLOCK && f.lid == 0)) to_req = true;
      }
    char b[200];
    if (!legit) { snprintf(b, sizeof b, "A: frame to %012llx seq %u: flags %08x locked_id %016llx is no cause's pair", (unsigned long long)f.mac, unsigned(f.seq), f.flags, (unsigned long long)f.lid); errs.push_back(b); }
    if (to_req) { snprintf(b, sizeof b, "B: frame to %012llx seq %u carries its own change", (unsigned long long)f.mac, unsigned(f.seq)); errs.push_back(b); }
  }
  // the final state's pair and its requester
  const bool held = s.d->lock_held_o; const uint64_t holder = s.d->lock_ctlr_o;
  Cause fin{UNLOCK, 0, 0, false};
  if (held) {
    bool found = false;
    for (auto it = causes.rbegin(); it != causes.rend(); ++it) if (it->lid == holder) { fin = *it; found = true; break; }
    if (!found) errs.push_back("C: the final holder took the lock with no recorded change");
  } else if (last_fall == last_unlock_fall) {
    fin = last_unlock;                     // the lock fell with the last UNLOCK
  }                                        // else it fell by the expiry: (1, 0)
  for (const Row& r : rows) {
    if (fin.has_req && r.eid == fin.req) continue;
    const Frame* last = nullptr;
    for (const Frame& f : frames) if (f.mac == r.mac) last = &f;
    if (!last || last->flags != fin.flags || last->lid != fin.lid) {
      char b[220]; snprintf(b, sizeof b, "C: %012llx's last frame %s%08x/%016llx, the final state %08x/%016llx",
                            (unsigned long long)r.mac, last ? "" : "(none) ", last ? last->flags : 0u,
                            last ? (unsigned long long)last->lid : 0ull, fin.flags, (unsigned long long)fin.lid);
      errs.push_back(b);
    }
  }
  std::map<uint64_t, int> lastseq;
  for (const Frame& f : frames) {
    if (lastseq.count(f.mac) && f.seq != lastseq[f.mac] + 1) errs.push_back("F: sequence_id not +1 (a frame repeated or skipped)");
    lastseq[f.mac] = f.seq;
  }
  if (!errs.empty()) {
    ++g_fails;
    printf("FAIL %s\n", name.c_str());
    for (auto& e : errs) printf("    %s\n", e.c_str());
    for (const Frame& f : frames) printf("    frame %012llx seq %u flags %08x locked_id %016llx\n", (unsigned long long)f.mac, unsigned(f.seq), f.flags, (unsigned long long)f.lid);
    return false;
  }
  return true;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const Row C{0x1111000000000001ull, 0x020000000001ull}, X{0x8888000000000008ull, 0x020000000008ull},
            Y{0x9999000000000009ull, 0x020000000009ull}, D{0x4444000000000004ull, 0x020000000004ull};
#ifdef IDENT
  char nmi[160];
  int lost = 0;
  for (const Params& p : {Params{1, 8}, Params{2, 12}, Params{3, 20}})
    for (int k = 0; k <= 80; ++k) {
      g_press_at = k;
      snprintf(nmi, sizeof nmi, "S7 gap=%d run=%d press@%d", p.gap, p.run, k);
      run_case(nmi, {C, X, D}, {{0, false, X.eid, 0x00010000u}}, {}, p);
      if (g_ident_sent < 1) { ++lost; printf("LOST %s: no IDENTIFY frame built\n", nmi); }
    }
  printf("S7: %d runs, %d FAIL, %d without an IDENTIFY frame\n", g_runs, g_fails, lost);
  return (g_fails || lost) ? 1 : 0;
#endif
  char nm[160];
  const std::vector<Params> ps = {{1, 8}, {1, 12}, {2, 9}, {3, 20}};
  // S1: X locks with W; the timeout expires at every offset over the round and the next
  for (uint32_t W : {0x00000000u, 0x00010000u})
    for (const Params& p : ps)
      for (int k = 0; k <= 140; ++k) {
        snprintf(nm, sizeof nm, "S1 W=%08x gap=%d run=%d expiry@%d", W, p.gap, p.run, k);
        run_case(nm, {C, X, D}, {{0, false, X.eid, W}}, {k}, p);
      }
  // S2: X locks, then unlocks with reserved bits; Y locks at every offset after the UNLOCK
  for (const Params& p : ps)
    for (int u : {0, 6, 60})
      for (int k = 0; k <= 120; ++k) {
        snprintf(nm, sizeof nm, "S2 gap=%d run=%d unlock@%d ylock@+%d", p.gap, p.run, u, k);
        run_case(nm, {C, X, Y, D}, {{0, false, X.eid, 0}, {u, true, X.eid, 0x80020001u}, {u + k, false, Y.eid, 0x00030000u}}, {}, p);
      }
  // S3: X locks, then unlocks at every offset during its LOCK round
  for (const Params& p : ps)
    for (int k = 0; k <= 120; ++k) {
      snprintf(nm, sizeof nm, "S3 gap=%d run=%d unlock@%d", p.gap, p.run, k);
      run_case(nm, {C, X, D}, {{0, false, X.eid, 0x00010000u}, {k, true, X.eid, 0x80020001u}}, {}, p);
    }
  // S4: X locks; the timeout expires at k1 and Y locks at k2 (denied while X still holds)
  for (const Params& p : {Params{1, 8}, Params{2, 12}})
    for (int k1 = 0; k1 <= 60; ++k1)
      for (int k2 = 0; k2 <= 80; k2 += 1) {
        snprintf(nm, sizeof nm, "S4 gap=%d run=%d expiry@%d ylock@%d", p.gap, p.run, k1, k2);
        run_case(nm, {C, X, Y, D}, {{0, false, X.eid, 0x00010000u}, {k2, false, Y.eid, 0x00030000u}}, {k1}, p);
      }
  // S5: X locks; the timeout expires at k1 and X re-locks at k2
  for (const Params& p : {Params{1, 8}, Params{2, 12}})
    for (int k1 = 0; k1 <= 60; ++k1)
      for (int k2 = 0; k2 <= 80; k2 += 1) {
        snprintf(nm, sizeof nm, "S5 gap=%d run=%d expiry@%d xrelock@%d", p.gap, p.run, k1, k2);
        run_case(nm, {C, X, D}, {{0, false, X.eid, 0x00010000u}, {k2, false, X.eid, 0x00040000u}}, {k1}, p);
      }
  // S6 (margin, reported apart): engine tails 2..7 after the read, an expiry at every offset
  int m_runs = g_runs, m_fails = g_fails;
  for (int run = 2; run <= 7; ++run)
    for (int k = -1; k <= 60; ++k) {
      snprintf(nm, sizeof nm, "S6 gap=1 run=%d expiry@%d", run, k);
      std::vector<int> e; if (k >= 0) e.push_back(k);
      run_case(nm, {C, X, D}, {{0, false, X.eid, 0x00010000u}}, e, Params{1, run});
    }
  printf("S6 margin runs: %d, FAIL %d\n", g_runs - m_runs, g_fails - m_fails);
  g_runs = m_runs; g_fails = m_fails;
  printf("%d runs: %d PASS, %d FAIL\n", g_runs, g_runs - g_fails, g_fails);
  return g_fails ? 1 : 0;
}

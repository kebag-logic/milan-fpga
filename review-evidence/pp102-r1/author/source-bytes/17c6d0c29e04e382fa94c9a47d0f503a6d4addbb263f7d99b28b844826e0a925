// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_scoreboard suite — independent expectations, never DUT logic.
//
// The C++ model is an independent transcription of the F03.7 hazard matrix
// (03 §6) as a LITERAL 9x9 table of {NEVER, SAMEKEY, ALWAYS} — a different
// formulation from the RTL's rule chain, so a divergence in either fails the
// run. On top of the matrix the model mirrors only the port CONTRACT: a
// MAX_HOLDS_P-deep hold set with opaque ids (no allocation-policy assumption
// beyond id uniqueness), the registered barrier-drain flag (a refused
// CFG_BARRIER blocks all non-barrier admission until the barrier grants on
// an empty table), and the rule (e) gate (a deadline-kill is honored only
// with the response-queued flag). Combinational outputs (gnt, id, kill_ack)
// are sampled pre-edge; registered outputs (holds, full, barrier_pend) are
// compared post-edge.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include "VKL_pp_scoreboard.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// pp_pkg::pp_hazard_e encodings (F03.7 row order). Plain integers, not an
// `enum class`: they index M9/CN and are passed as the `int` class argument,
// so a scoped enum would only add a cast at every use.
constexpr int RO  = 0;
constexpr int CFG = 1;
constexpr int STR = 2;
constexpr int MAP = 3;
constexpr int CLK = 4;
constexpr int NAM = 5;
constexpr int LCK = 6;
constexpr int REG = 7;
constexpr int IDF = 8;

//! Hazard classes, RO..IDF — the order and the rank of the F03.7 matrix.
constexpr int kClasses = 9;

constexpr const char* CN[kClasses] = {"RO", "CFG", "STR", "MAP", "CLK", "NAME",
                                      "LOCK", "REG", "IDF"};

// conflict kinds
enum Kind { NV = 0, SK = 1, AL = 2 };  // never / same-key / always

// Independent literal transcription of F03.7 (docs/architecture/03 §6):
//  - CFG_BARRIER row/col: ALWAYS (global drain, itself included)
//  - RO row/col: NEVER vs RO, else SAMEKEY (blocked only vs same-key write)
//  - LOCK row/col: ALWAYS vs lock-protected members (CFG STR MAP CLK NAME
//    IDF, per F06.14) + itself; NEVER vs REG (not lock-protected)
//  - same class: REG, IDF single-resource (ALWAYS); STR MAP CLK NAME SAMEKEY
//  - STR x MAP: ALWAYS (format<->mapping cross-lock, class-wide)
//  - all other cross pairs: NEVER
constexpr Kind M9[kClasses][kClasses] = {
  //         RO   CFG  STR  MAP  CLK  NAM  LCK  REG  IDF
  /* RO  */ {NV,  AL,  SK,  SK,  SK,  SK,  SK,  SK,  SK},
  /* CFG */ {AL,  AL,  AL,  AL,  AL,  AL,  AL,  AL,  AL},
  /* STR */ {SK,  AL,  SK,  AL,  NV,  NV,  AL,  NV,  NV},
  /* MAP */ {SK,  AL,  AL,  SK,  NV,  NV,  AL,  NV,  NV},
  /* CLK */ {SK,  AL,  NV,  NV,  SK,  NV,  AL,  NV,  NV},
  /* NAM */ {SK,  AL,  NV,  NV,  NV,  SK,  AL,  NV,  NV},
  /* LCK */ {SK,  AL,  AL,  AL,  AL,  AL,  AL,  NV,  AL},
  /* REG */ {SK,  AL,  NV,  NV,  NV,  NV,  NV,  AL,  NV},
  /* IDF */ {SK,  AL,  NV,  NV,  NV,  NV,  AL,  NV,  AL},
};

constexpr int MAXH = 8;  // must match MAX_HOLDS_P

struct Model {
  bool v[MAXH] = {};
  int  c[MAXH] = {};
  int  k[MAXH] = {};
  bool pend = false;

  static bool conflict(int ac, int ak, int bc, int bk) {
    Kind kk = M9[ac][bc];
    if (kk == AL) return true;
    if (kk == SK) return ak == bk;
    return false;
  }
  bool fullT() const { for (bool b : v) if (!b) return false; return true; }
  bool admissible(int cls, int key) const {
    if (fullT()) return false;
    if (pend && cls != CFG) return false;
    for (int i = 0; i < MAXH; i++)
      if (v[i] && conflict(cls, key, c[i], k[i])) return false;
    return true;
  }
  uint32_t mask() const {
    uint32_t m = 0;
    for (int i = 0; i < MAXH; i++) if (v[i]) m |= 1u << i;
    return m;
  }
};

// ---- the suite ----------------------------------------------------------
// One object owns the model, the port BFM, the independent Model mirror and
// the tally, so every phase below is a named member function rather than
// another stretch of a `main` nobody can scope (Core Guidelines I.2, F.3).
namespace {
class ScoreboardSuite {
 public:
  ScoreboardSuite() { idle(); }
  int run();

 private:
  void idle();
  void settle();
  void edge();
  void cycle();
  int request(int cls, int key, const char* tag);
  void release(int id);
  bool kill(int id, bool respq, const char* tag);
  void check_state(const char* tag);
  void drain(const char* tag);
  void reset_leaves_the_table_empty();
  void same_key_serializes_and_release_reopens();
  void distinct_keys_run_parallel_and_so_does_read_only();
  void the_whole_hazard_matrix_agrees_with_the_rtl();
  void a_kill_is_refused_until_the_response_is_queued();
  void a_grant_sees_the_pre_release_state();
  void a_full_holds_table_refuses_a_conflict_free_request();
  void the_barrier_drains_the_table_then_excludes_all();
  void randomized_traffic_tracks_the_model();

  const milan::tb::Model<VKL_pp_scoreboard> model;
  VKL_pp_scoreboard* const d = model.get();
  Model m;
  int checks = 0;
  int fails = 0;
};
}  // namespace

void ScoreboardSuite::idle() {
  d->adm_req_i = 0; d->rel_valid_i = 0;
  d->kill_valid_i = 0; d->kill_resp_queued_i = 0;
}

void ScoreboardSuite::settle() { d->clk_i = 0; d->eval(); }

void ScoreboardSuite::edge()   { d->clk_i = 1; d->eval(); }

void ScoreboardSuite::cycle()  { settle(); edge(); }

// One request cycle. Checks gnt against the model and id uniqueness;
// returns the granted id or -1. Model bookkeeping included.
int ScoreboardSuite::request(int cls, int key, const char* tag) {
  bool exp = m.admissible(cls, key);
  d->adm_req_i = 1; d->adm_class_i = cls; d->adm_key_i = key;
  settle();
  bool g = d->adm_gnt_o;
  int  id = d->adm_id_o;
  CHECK(g == exp, "%s: req %s key=%d gnt=%d expected=%d",
        tag, CN[cls], key, static_cast<int>(g), static_cast<int>(exp));
  if (g) {
    bool ok_id = (id >= 0 && id < MAXH && !m.v[id]);
    CHECK(ok_id, "%s: grant id %d out of range or duplicated", tag, id);
    if (id >= 0 && id < MAXH) { m.v[id] = true; m.c[id] = cls; m.k[id] = key; }
    if (cls == CFG) m.pend = false;
  } else if (cls == CFG) {
    m.pend = true;  // refused barrier latches the drain
  }
  edge();
  idle();
  return g ? id : -1;
}

void ScoreboardSuite::release(int id) {
  d->rel_valid_i = 1; d->rel_id_i = id;
  cycle();
  idle();
  if (id >= 0 && id < MAXH) m.v[id] = false;
}

bool ScoreboardSuite::kill(int id, bool respq, const char* tag) {
  bool exp = respq && id >= 0 && id < MAXH && m.v[id];
  d->kill_valid_i = 1; d->kill_id_i = id; d->kill_resp_queued_i = respq;
  settle();
  bool a = d->kill_ack_o;
  CHECK(a == exp, "%s: kill id=%d respq=%d ack=%d expected=%d",
        tag, id, static_cast<int>(respq), static_cast<int>(a),
        static_cast<int>(exp));
  edge();
  idle();
  if (a && id >= 0 && id < MAXH) m.v[id] = false;
  return a;
}

void ScoreboardSuite::check_state(const char* tag) {
  CHECK(static_cast<uint32_t>(d->holds_o) == m.mask(),
        "%s: holds %02x expected %02x", tag,
        static_cast<unsigned>(d->holds_o), static_cast<unsigned>(m.mask()));
  CHECK(static_cast<bool>(d->full_o) == m.fullT(),
        "%s: full_o mismatch", tag);
  CHECK(static_cast<bool>(d->barrier_pend_o) == m.pend,
        "%s: barrier_pend mismatch", tag);
}

// Release everything; clear a latched barrier drain by granting it.
void ScoreboardSuite::drain(const char* tag) {
  for (int i = 0; i < MAXH; i++) if (m.v[i]) release(i);
  if (m.pend) {
    int id = request(CFG, 0, tag);
    if (id >= 0) release(id);
  }
}

void ScoreboardSuite::reset_leaves_the_table_empty() {
  d->rst_n = 0;
  for (int i = 0; i < 4; ++i) cycle();
  d->rst_n = 1;
  cycle();

  // ---- T0: reset state -------------------------------------------------
  CHECK(d->holds_o == 0, "T0 no holds after reset");
  CHECK(d->full_o == 0, "T0 not full after reset");
  CHECK(d->barrier_pend_o == 0, "T0 no barrier pending after reset");
}

// ---- T1: same-key serializes; release reopens ------------------------
void ScoreboardSuite::same_key_serializes_and_release_reopens() {
  int a = request(STR, 5, "T1 first");
  CHECK(a >= 0, "T1 first STR key5 granted");
  int b = request(STR, 5, "T1 second");           // model: refused
  CHECK(b < 0, "T1 same-key refused while held");
  release(a);
  int c = request(STR, 5, "T1 after release");    // model: granted
  CHECK(c >= 0, "T1 granted after release");
  release(c);
  check_state("T1 end");
}

// ---- T2: distinct keys parallel; RO parallel on the SAME key ---------
void ScoreboardSuite::distinct_keys_run_parallel_and_so_does_read_only() {
  int a = request(STR, 1, "T2 k1");
  int b = request(STR, 2, "T2 k2");
  CHECK(a >= 0 && b >= 0 && a != b, "T2 distinct keys both granted, ids differ");
  int r1 = request(RO, 9, "T2 ro1");
  int r2 = request(RO, 9, "T2 ro2");               // same key: still parallel
  CHECK(r1 >= 0 && r2 >= 0, "T2 RO same-key admits concurrently");
  release(a); release(b); release(r1); release(r2);
  check_state("T2 end");
}

// ---- T3: systematic 9x9 x {same,diff} sweep vs the literal matrix ----
void ScoreboardSuite::the_whole_hazard_matrix_agrees_with_the_rtl() {
  for (int a = 0; a < kClasses; a++) {
    for (int b = 0; b < kClasses; b++) {
      for (int same = 0; same < 2; same++) {
        char tag[64];
        snprintf(tag, sizeof tag, "T3 %s->%s %s",
                 CN[a], CN[b], same ? "same-key" : "diff-key");
        int ka = 0x42;
        int kb = same ? 0x42 : 0x41;
        int ida = request(a, ka, tag);
        CHECK(ida >= 0, "%s: A admitted on empty table", tag);
        int idb = request(b, kb, tag);   // expectation checked inside
        if (idb >= 0) release(idb);
        if (ida >= 0) release(ida);
        drain(tag);
        CHECK(d->holds_o == 0, "%s: drained", tag);
      }
    }
  }
}

// ---- T4: rule (e) — kill refused before response-queued --------------
void ScoreboardSuite::a_kill_is_refused_until_the_response_is_queued() {
  int a = request(STR, 7, "T4 acquire");
  CHECK(a >= 0, "T4 STR key7 granted");
  bool ack0 = kill(a, false, "T4 kill-early");     // model: refused
  CHECK(!ack0, "T4 kill refused before response queued");
  int b = request(STR, 7, "T4 still-held");        // model: refused
  CHECK(b < 0, "T4 key still serialized after refused kill");
  bool ack1 = kill(a, true, "T4 kill-queued");     // model: honored
  CHECK(ack1, "T4 kill honored once response queued");
  int c = request(STR, 7, "T4 freed");
  CHECK(c >= 0, "T4 key free after honored kill");
  release(c);
  bool ack2 = kill(a, true, "T4 kill-stale");      // id no longer held
  CHECK(!ack2, "T4 kill of a non-held id refused");
  check_state("T4 end");
}

// ---- T5: grant/release ordering ---------------------------------------
void ScoreboardSuite::a_grant_sees_the_pre_release_state() {
  int a = request(STR, 3, "T5 acquire");
  CHECK(a >= 0, "T5 granted");
  // same-cycle release + conflicting request: grant sees PRE-release state
  d->rel_valid_i = 1; d->rel_id_i = a;
  d->adm_req_i = 1; d->adm_class_i = STR; d->adm_key_i = 3;
  settle();
  CHECK(d->adm_gnt_o == 0, "T5 same-cycle release does not admit");
  edge();
  idle();
  m.v[a] = false;                       // release landed on the edge
  int b = request(STR, 3, "T5 next-cycle");
  CHECK(b >= 0, "T5 admitted the cycle after the release");
  // release of a non-held id is a no-op (MAXH > 1, so (b+1)%MAXH != b)
  release((b + 1) % MAXH);
  check_state("T5 no-op release");
  release(b);
  check_state("T5 end");
}

// ---- T6: holds-table full ---------------------------------------------
void ScoreboardSuite::a_full_holds_table_refuses_a_conflict_free_request() {
  int ids[MAXH];
  for (int i = 0; i < MAXH; i++) {
    ids[i] = request(RO, 100 + i, "T6 fill");      // RO: all parallel
    CHECK(ids[i] >= 0, "T6 fill %d granted", i);
  }
  CHECK(d->full_o == 1, "T6 table full");
  int x = request(RO, 999, "T6 overflow");         // no conflict, no room
  CHECK(x < 0, "T6 refused when full despite no conflict");
  release(ids[0]);
  CHECK(d->full_o == 0, "T6 not full after a release");
  int y = request(RO, 999, "T6 after-release");
  CHECK(y >= 0, "T6 granted after a release");
  release(y);
  for (int i = 1; i < MAXH; i++) release(ids[i]);
  check_state("T6 end");
}

// ---- T7: CFG_BARRIER drain --------------------------------------------
void ScoreboardSuite::the_barrier_drains_the_table_then_excludes_all() {
  int s = request(STR, 1, "T7 str");
  int c = request(CLK, 2, "T7 clk");
  CHECK(s >= 0 && c >= 0, "T7 two writers in flight");
  int b0 = request(CFG, 0, "T7 barrier-1");        // refused, latches pend
  CHECK(b0 < 0, "T7 barrier refused while holders live");
  CHECK(d->barrier_pend_o == 1, "T7 drain latched");
  int n = request(NAM, 5, "T7 blocked");           // admissible w/o pend
  CHECK(n < 0, "T7 non-barrier admission blocked during drain");
  release(s);
  int b1 = request(CFG, 0, "T7 barrier-2");        // one holder left
  CHECK(b1 < 0, "T7 barrier still refused with one holder");
  release(c);
  int b2 = request(CFG, 0, "T7 barrier-3");        // table empty
  CHECK(b2 >= 0, "T7 barrier granted on empty table");
  CHECK(d->barrier_pend_o == 0, "T7 drain cleared by the grant");
  int r = request(RO, 0x33, "T7 excluded");        // barrier held
  CHECK(r < 0, "T7 everything excluded while barrier held");
  release(b2);
  int r2 = request(RO, 0x33, "T7 resumed");
  CHECK(r2 >= 0, "T7 normal admission after barrier release");
  release(r2);
  check_state("T7 end");
}

// ---- T8: randomized traffic, >= 2k ops vs the model -------------------
void ScoreboardSuite::randomized_traffic_tracks_the_model() {
  srand(7);
  constexpr int OPS = 2600;
  int reqs = 0;
  int grants = 0;
  int rels = 0;
  int kills = 0;
  for (int op = 0; op < OPS; op++) {
    int r = rand() % 100;
    if (m.pend && r < 30) {
      int id = request(CFG, 0, "T8 cfg");
      ++reqs; if (id >= 0) ++grants;
    } else if (r < 55) {
      constexpr int wcls[12] = {RO, RO, RO, STR, STR, MAP, CLK,
                                NAM, LCK, REG, IDF, CFG};
      int cls = wcls[rand() % 12];
      int key = rand() % 6;
      int id = request(cls, key, "T8 req");
      ++reqs; if (id >= 0) ++grants;
    } else if (r < 85) {
      // release a random active hold (or a random id if none: no-op)
      int live[MAXH];
      int n = 0;
      for (int i = 0; i < MAXH; i++) if (m.v[i]) live[n++] = i;
      release(n ? live[rand() % n] : rand() % MAXH);
      ++rels;
    } else {
      int live[MAXH];
      int n = 0;
      for (int i = 0; i < MAXH; i++) if (m.v[i]) live[n++] = i;
      int id = n ? live[rand() % n] : rand() % MAXH;
      kill(id, (rand() & 1) != 0, "T8 kill");
      ++kills;
    }
    if ((op & 63) == 0) check_state("T8 mask");
  }
  printf("T8: %d ops (%d req / %d granted, %d rel, %d kill)\n",
         OPS, reqs, grants, rels, kills);
  CHECK(reqs + rels + kills == OPS, "T8 op accounting");
  drain("T8 drain");
  check_state("T8 end");
  CHECK(d->holds_o == 0, "T8 all holds returned");
}

int ScoreboardSuite::run() {
  reset_leaves_the_table_empty();
  same_key_serializes_and_release_reopens();
  distinct_keys_run_parallel_and_so_does_read_only();
  the_whole_hazard_matrix_agrees_with_the_rtl();
  a_kill_is_refused_until_the_response_is_queued();
  a_grant_sees_the_pre_release_state();
  a_full_holds_table_refuses_a_conflict_free_request();
  the_barrier_drains_the_table_then_excludes_all();
  randomized_traffic_tracks_the_model();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  ScoreboardSuite suite;
  return suite.run();
}

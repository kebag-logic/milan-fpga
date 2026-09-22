// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_tx_arbiter suite — independent expectations, never DUT logic.
//
// Proves the 03 §8 TX-arbitration contract over the REAL KL_pp_tx_slots
// pool (harness wires the ser_* contract directly): strict priority when
// fresh (ACMP > AECP-sol/self > unsol/SRP > ADP, lowest index on ties);
// frame-atomic grant — a higher-priority arrival mid-frame waits for
// ser_last and the byte stream is verified byte-exact and uninterrupted
// against the model's own frame images; T-TX-AGING starvation promotion
// (compressed tick_ms bursts) — an aged ADP outranks a fresh native ACMP;
// pacing — after a non-solicited grant a pending solicited requester is
// served before any further non-solicited frame, and pacing outranks
// aging; per-requester grant counters exact; a PP_SLOT_NULL_C handle is
// never granted; randomized contention >= 1000 frames with every grant
// matched to the model's decision.
//
// The reference model re-implements the arbitration POLICY from the doc
// (priority map, solicited mask, aging rule, pacing rule) — it shares no
// FSM, no serializer and no memory with the RTL.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Vtx_arbiter_harness.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

namespace {

// ---- independent arbitration model ----------------------------------------
struct RefArb {
  static constexpr int N = 6;
  // doc F03.5 classes, 0 = doc priority 1:
  //  0 AECP-sol=1, 1 AECP-unsol=2, 2 ACMP=0, 3 ADP=3, 4 SRP=2, 5 self/CA=1
  static constexpr std::array<int, N> PRIO = {{1, 2, 0, 3, 2, 1}};
  static constexpr uint32_t SOL = 0b100101;   // ACMP, AECP-sol, self/CA
  static constexpr int  AGE_SAT = 10;         // T-TX-AGING in ms ticks

  int      age[N] = {0};
  bool     pace_nonsol = false;               // last granted frame non-solicited
  uint16_t cnt[N] = {0};

  // the decision the arbiter must make with this pending set, now
  int decide(uint32_t pend) const {
    bool solp = (pend & SOL) != 0;
    uint32_t elig = (pace_nonsol && solp) ? (pend & SOL) : pend;
    int best = -1;
    int bkey = 99;
    for (int i = 0; i < N; ++i) {
      if (!((elig >> i) & 1)) continue;
      int key = ((age[i] >= AGE_SAT) ? 0 : 4) + PRIO[i];
      if (key < bkey) { bkey = key; best = i; }
    }
    return best;
  }
  // one clock edge: winner (-1 = none), pre-edge pending set, pre-edge tick
  void edge(int w, uint32_t pend, bool tick) {
    for (int i = 0; i < N; ++i) {
      if (i == w)                    age[i] = 0;
      else if (!((pend >> i) & 1))   age[i] = 0;
      else if (tick && age[i] < AGE_SAT) age[i]++;
    }
    if (w >= 0) { cnt[w]++; pace_nonsol = !((SOL >> w) & 1); }
  }
};

// ---- harness / engine ------------------------------------------------------
struct Eng {
  Vtx_arbiter_harness* dut;
  RefArb ref;
  uint32_t rng = 0xA5B7C901u;

  // requester drive state
  uint32_t req_mask = 0;
  std::array<int, 6> slot_field = {{0, 0, 0, 0, 0, 0}};

  // tick + ready policy
  bool tick_every = false;
  int  tick_burst = 0;       // forced ticks remaining
  int  tick_div   = 0;       // 0 = off, else 1-in-N random ticks
  int  ready_pct  = 100;
  bool start_abort = false;

  // TB pool bookkeeping + frame images (per slot)
  std::array<bool, 5> slot_free = {{true, true, true, true, true}};
  uint8_t img[5][1600];
  int     len_of[5] = {0};
  int     epoch = 0;

  // frame in service
  bool in_service = false;
  int  srv_req = -1;
  int  srv_slot = -1;
  int  srv_pos = 0;
  std::vector<uint8_t> srv_exp;

  // logs + error counters (every grant / byte in every phase runs these)
  std::vector<int> grant_log;
  long frames_done = 0;
  long e_gnt_mismatch = 0;
  long e_byte = 0;
  long e_sof = 0;
  long e_eof = 0;
  long e_spur = 0;
  long e_onehot = 0;
  long e_pulse = 0;
  long e_gnt_midframe = 0;
  long e_stall = 0;
  long e_alloc = 0;
  // cycles a pending request may go ungranted, with the serializer idle,
  // before the wait counts as an arbitration stall
  static constexpr int kStallLimitCycles = 80;
  int  idle_wait = 0;
  bool prev_gnt = false;
  // The DUT registers its slot-side qualification (stage-0 pipeline: the
  // != NULL compare on the far-traveling slot buses lands in pend_r before
  // the selection loop sees it). Selection uses that registered set AND the
  // current valid set so a withdrawn request cannot survive for one stale
  // cycle. The model mirrors that intersection.
  uint32_t pend_q = 0;
  bool     select_pending = false;
  int      selected_req = -1;

  explicit Eng(Vtx_arbiter_harness* d) : dut(d) { memset(img, 0, sizeof img); }

  uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

  uint32_t pend_now() const {
    uint32_t p = 0;
    for (int i = 0; i < 6; ++i)
      if (((req_mask >> i) & 1) && slot_field[i] != 7) p |= 1u << i;
    return p;
  }

  uint16_t cnt_field(int i) const {
    uint32_t w = dut->gnt_count_o[i / 2];
    return uint16_t((w >> ((i % 2) * 16)) & 0xFFFFu);
  }

  void step() {
    // drive this cycle's requester/tick/ready intents
    dut->req_valid_i = uint8_t(req_mask);
    uint32_t packed = 0;
    for (int r = 0; r < 6; ++r)
      packed |= uint32_t(slot_field[r] & 7) << (3 * r);
    dut->tx_slot_i = packed;
    bool tick = tick_every || (tick_burst > 0);
    if (tick_burst > 0) tick_burst--;
    if (!tick && tick_div > 0) tick = (rnd() % uint32_t(tick_div)) == 0;
    dut->tick_ms_i = tick;
    dut->tx_ready_i = (rnd() % 100u) < uint32_t(ready_pct);
    dut->start_abort_i = start_abort;

    // settle + pre-edge observation (what the registers will see)
    dut->clk_i = 0; dut->eval();
    uint32_t pend_pre = pend_now();
    uint32_t arb_pend_pre = pend_q & pend_pre;
    bool had_selection = select_pending;
    int selected_pre = selected_req;
    bool was_in_service = in_service;
    int next_selection = (!was_in_service && !had_selection)
                           ? ref.decide(arb_pend_pre) : -1;
    int  s_valid = dut->tx_valid_o;
    int  s_sof = dut->tx_sof_o;
    int  s_eof = dut->tx_eof_o;
    int  s_ready = dut->tx_ready_i;
    uint8_t s_data = dut->tx_data_o;
    bool tick_pre = dut->tick_ms_i;

    // rising edge
    dut->clk_i = 1; dut->eval();

    // ---- byte lane: consumed at this edge -------------------------------
    if (s_valid && s_ready) {
      if (!in_service) {
        e_spur++;
      } else {
        if (srv_pos < int(srv_exp.size()) && s_data != srv_exp[srv_pos]) e_byte++;
        if ((s_sof != 0) != (srv_pos == 0)) e_sof++;
        bool exp_eof = (srv_pos == int(srv_exp.size()) - 1);
        if ((s_eof != 0) != exp_eof) e_eof++;
        srv_pos++;
        if (s_eof) {
          slot_free[srv_slot] = true;      // pool auto-frees on eof
          in_service = false;
          frames_done++;
        }
      }
    }

    // ---- grant pulse (registered: set at this edge) ----------------------
    uint8_t g = dut->gnt_o;
    if (g) {
      if (g & (g - 1)) e_onehot++;
      if (prev_gnt)    e_pulse++;
      int w = __builtin_ctz(g);
      if (in_service)  e_gnt_midframe++;
      int exp = had_selection ? selected_pre : -1;
      if (exp != w) {
        e_gnt_mismatch++;
        printf("  gnt mismatch: dut=%d model=%d pend=%02x pace=%d\n",
               w, exp, arb_pend_pre, int(ref.pace_nonsol));
      }
      ref.edge(w, arb_pend_pre, tick_pre); // DUT-history bookkeeping
      // frame capture from the model's own image of the presented slot
      srv_req  = w;
      srv_slot = slot_field[w];
      srv_exp.assign(img[srv_slot], img[srv_slot] + len_of[srv_slot]);
      srv_pos  = 0;
      in_service = true;
      grant_log.push_back(w);
      req_mask &= ~(1u << w);              // requester drops after grant
      idle_wait = 0;
    } else {
      if (had_selection && !start_abort) {
        e_gnt_mismatch++;
        printf("  missing gnt: model=%d pend=%02x pace=%d\n",
               selected_pre, arb_pend_pre, int(ref.pace_nonsol));
      }
      ref.edge(-1, arb_pend_pre, tick_pre);
      if (pend_pre != 0 && !in_service) {
        if (++idle_wait > kStallLimitCycles) { e_stall++; idle_wait = 0; }
      } else {
        idle_wait = 0;
      }
    }
    if (had_selection) {
      select_pending = false;
      selected_req = -1;
    } else if (!was_in_service && !g && next_selection >= 0) {
      select_pending = true;
      selected_req = next_selection;
    }
    prev_gnt = (g != 0);
    pend_q = pend_pre;
  }

  void run(int n) { for (int i = 0; i < n; ++i) step(); }

  // ---- builder-side helpers (TB = response builders) ---------------------
  int expected_alloc(bool ov) const {
    if (ov) return slot_free[4] ? 4 : -1;
    for (int i = 0; i < 4; ++i) if (slot_free[i]) return i;
    return -1;
  }
  int alloc(bool ov) {
    int exp = expected_alloc(ov);
    for (int t = 0; t < 6; ++t) {
      dut->alloc_req_i = 1; dut->oversize_i = ov;
      step();
      dut->alloc_req_i = 0; dut->oversize_i = 0;
      if (dut->alloc_gnt_o) {
        int got = dut->alloc_slot_o;
        if (got != exp) {
          e_alloc++;
          printf("  alloc mismatch: got %d exp %d free=%d%d%d%d%d\n", got, exp,
                 slot_free[0], slot_free[1], slot_free[2], slot_free[3],
                 slot_free[4]);
        }
        if (got >= 0 && got < 5) slot_free[got] = false;
        step();
        return got;
      }
      step();
    }
    e_alloc++;
    printf("  alloc DENIED (ov=%d) free=%d%d%d%d%d\n", int(ov), slot_free[0],
           slot_free[1], slot_free[2], slot_free[3], slot_free[4]);
    return -1;
  }
  void wr(int s, int a, uint8_t d) {
    dut->wr_slot_i = uint8_t(s); dut->wr_addr_i = uint16_t(a);
    dut->wr_data_i = d; dut->wr_valid_i = 1;
    step();
    dut->wr_valid_i = 0;
    img[s][a] = d;
  }
  void commit(int s, int l) {
    dut->wr_slot_i = uint8_t(s); dut->wr_len_i = uint16_t(l);
    dut->wr_commit_i = 1;
    step();
    dut->wr_commit_i = 0;
    len_of[s] = l;
  }
  static uint8_t pat(int s, int a, int e) {
    return uint8_t(0x35 * s + 7 * a + 0x11 + 0x4D * e);
  }
  // alloc + fill + commit one frame; returns the slot (no request raised)
  int prep(int len, bool ov = false) {
    int s = alloc(ov);
    if (s < 0) return -1;
    ++epoch;
    for (int a = 0; a < len; ++a) wr(s, a, pat(s, a, epoch));
    commit(s, len);
    return s;
  }
  void raise(int r, int s) { slot_field[r] = s; req_mask |= 1u << r; }
  int  arm(int r, int len, bool ov = false) {
    int s = prep(len, ov);
    if (s >= 0) raise(r, s);
    return s;
  }

  // ---- wait helpers -------------------------------------------------------
  int wait_grant(int maxcyc) {
    size_t n0 = grant_log.size();
    for (int c = 0; c < maxcyc; ++c) {
      step();
      if (grant_log.size() > n0) return grant_log.back();
    }
    return -1;
  }
  bool wait_frames(long upto, int maxcyc) {
    for (int c = 0; c < maxcyc; ++c) {
      if (frames_done >= upto) return true;
      step();
    }
    return frames_done >= upto;
  }

  // ---- aggregated clean check --------------------------------------------
  struct Snap { long a, b, c, d, e, f, g, h, i, j; };
  Snap snap() const {
    return {e_gnt_mismatch, e_byte, e_sof, e_eof, e_spur,
            e_onehot, e_pulse, e_gnt_midframe, e_stall, e_alloc};
  }
  bool clean_since(const Snap& s) const {
    Snap n = snap();
    return n.a == s.a && n.b == s.b && n.c == s.c && n.d == s.d &&
           n.e == s.e && n.f == s.f && n.g == s.g && n.h == s.h &&
           n.i == s.i && n.j == s.j;
  }
  void print_errs() const {
    printf("  errs: mism=%ld byte=%ld sof=%ld eof=%ld spur=%ld onehot=%ld "
           "pulse=%ld midfrm=%ld stall=%ld alloc=%ld\n",
           e_gnt_mismatch, e_byte, e_sof, e_eof, e_spur, e_onehot, e_pulse,
           e_gnt_midframe, e_stall, e_alloc);
  }
};

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- the suite: the engine above, driven one lettered phase at a time -------
class TxArbiterSuite {
 public:
  explicit TxArbiterSuite(Vtx_arbiter_harness* model) : dut(model), h(model) {}

  int run();

 private:
  void reset_leaves_the_arbiter_quiescent();
  void strict_priority_when_every_requester_is_fresh();
  void a_frame_is_atomic_against_a_higher_priority_arrival();
  void aging_promotes_a_starved_requester();
  void pacing_outranks_aging();
  void a_null_slot_handle_is_never_granted();
  void randomized_contention_matches_the_model();
  void a_cancelled_selection_produces_no_grant();

  Vtx_arbiter_harness* const dut;
  Eng h;
  int checks = 0;
  int fails = 0;
};

// ---- A: reset --------------------------------------------------------
void TxArbiterSuite::reset_leaves_the_arbiter_quiescent() {
  dut->rst_n = 0;
  for (int i = 0; i < 4; ++i) h.step();
  dut->rst_n = 1;
  h.run(10);
  {
    bool cnt0 = true;
    for (int i = 0; i < 6; ++i) cnt0 &= (h.cnt_field(i) == 0);
    CHECK(cnt0, "A grant counters zero after reset");
    CHECK(h.grant_log.empty() && h.frames_done == 0,
          "A no grants or frames while idle");
    CHECK(dut->tx_valid_o == 0 && dut->gnt_o == 0, "A quiescent outputs");

    // Populate the registered qualifier, then withdraw before arbitration.
    // No pool slot is needed because the request must never be granted.
    h.slot_field[5] = 0;
    h.req_mask |= 1u << 5;
    h.step();
    h.req_mask &= ~(1u << 5);
    h.run(4);
    CHECK(h.grant_log.empty() && !h.in_service,
          "A withdrawn registered request is never granted");
  }
}

// ---- B: strict priority when fresh ----------------------------------
void TxArbiterSuite::strict_priority_when_every_requester_is_fresh() {
  // round 1: five simultaneous requesters -> 2 (ACMP), 0 (AECP-sol),
  // 5 (self/CA), 1 (unsol), 4 (SRP, oversize slot); index breaks ties
  {
    auto s0 = h.snap();
    h.ready_pct = 70;
    int sl2 = h.prep(56);
    int sl0 = h.prep(90);
    int sl5 = h.prep(70);
    int sl1 = h.prep(40);
    int sl4 = h.prep(100, true);
    h.raise(2, sl2); h.raise(0, sl0); h.raise(5, sl5); h.raise(1, sl1);
    h.raise(4, sl4);
    static constexpr std::array<int, 5> expseq = {{2, 0, 5, 1, 4}};
    for (int k = 0; k < 5; ++k) {
      int g = h.wait_grant(4000);
      CHECK(g == expseq[k], "B1 grant #%d is %d exp %d", k, g, expseq[k]);
    }
    CHECK(h.wait_frames(5, 4000), "B1 all five frames drain");
    CHECK(h.clean_since(s0), "B1 stream byte-exact, no model mismatch");
    if (!h.clean_since(s0)) h.print_errs();
  }
  // round 2: lone lowest-priority requester is served
  {
    auto s0 = h.snap();
    h.arm(3, 33);
    int g = h.wait_grant(2000);
    CHECK(g == 3, "B2 lone ADP served (got %d)", g);
    CHECK(h.wait_frames(6, 2000) && h.clean_since(s0), "B2 clean");
  }
  // round 3: {0,3,4} -> 0, then 4 (class 2 < class 3), then 3
  {
    auto s0 = h.snap();
    int a = h.prep(48);
    int b = h.prep(30);
    int c = h.prep(64);
    h.raise(0, a); h.raise(3, b); h.raise(4, c);
    static constexpr std::array<int, 3> expseq = {{0, 4, 3}};
    for (int k = 0; k < 3; ++k) {
      int g = h.wait_grant(2000);
      CHECK(g == expseq[k], "B3 grant #%d is %d exp %d", k, g, expseq[k]);
    }
    CHECK(h.wait_frames(9, 2000) && h.clean_since(s0), "B3 clean");
  }
  // counters after B: 9 grants total, per-lane exact
  for (int i = 0; i < 6; ++i)
    CHECK(h.cnt_field(i) == h.ref.cnt[i],
          "B counter[%d] dut %u model %u", i, h.cnt_field(i), h.ref.cnt[i]);
}

// ---- C: frame atomicity ----------------------------------------------
void TxArbiterSuite::a_frame_is_atomic_against_a_higher_priority_arrival() {
  // ACMP arrives mid-ADP-frame: the ADP frame streams to ser_last intact,
  // no grant fires mid-frame, ACMP wins the next arbitration
  {
    auto s0 = h.snap();
    h.ready_pct = 60;
    h.arm(3, 200);
    int g = h.wait_grant(200);
    CHECK(g == 3, "C ADP frame granted (got %d)", g);
    size_t nglog = h.grant_log.size();
    while (h.in_service && h.srv_pos < 60) h.step();   // mid-frame
    h.ready_pct = 0;                                   // freeze the stream
    h.arm(2, 30);                                      // ACMP arrives now
    h.ready_pct = 60;
    while (h.in_service) h.step();                     // to ser_last
    CHECK(h.grant_log.size() == nglog,
          "C no grant fires mid-frame (higher prio waits for ser_last)");
    g = h.wait_grant(200);
    CHECK(g == 2, "C ACMP wins the next arbitration (got %d)", g);
    CHECK(h.wait_frames(11, 2000) && h.clean_since(s0),
          "C both frames byte-exact and uninterrupted");
    if (!h.clean_since(s0)) h.print_errs();
  }
}

// ---- D: aging promotion (compressed ticks) ---------------------------
void TxArbiterSuite::aging_promotes_a_starved_requester() {
  // ADP starves behind back-to-back ACMP while un-aged; a 12-tick burst
  // (>= T-TX-AGING = 10) flips the next arbitration to ADP
  {
    auto s0 = h.snap();
    h.ready_pct = 60;
    h.arm(2, 120);
    int g = h.wait_grant(300);
    CHECK(g == 2, "D ACMP #0 granted (got %d)", g);
    h.ready_pct = 0;                 // freeze so the preps can never slip
    h.arm(3, 60);                    // the starving ADP request, armed
    h.arm(2, 120);                   //   while the arbiter is mid-frame
    h.ready_pct = 60;
    while (h.in_service) h.step();
    g = h.wait_grant(300);
    CHECK(g == 2, "D ACMP #1 outranks un-aged ADP (got %d)", g);
    h.ready_pct = 0; h.arm(2, 120); h.ready_pct = 60;
    while (h.in_service) h.step();
    g = h.wait_grant(300);
    CHECK(g == 2, "D ACMP #2 still outranks un-aged ADP (got %d)", g);
    h.ready_pct = 0;                 // freeze mid-frame
    h.tick_burst = 12;               // age the pending ADP past T-TX-AGING
    h.run(12);
    h.arm(2, 120);                   // fresh ACMP, armed with ticks OFF
    h.ready_pct = 60;
    while (h.in_service) h.step();
    g = h.wait_grant(300);
    CHECK(g == 3, "D aged ADP outranks fresh native ACMP (got %d)", g);
    g = h.wait_grant(2000);
    CHECK(g == 2, "D ACMP resumes after the aged frame (got %d)", g);
    CHECK(h.wait_frames(16, 4000) && h.clean_since(s0), "D clean");
    if (!h.clean_since(s0)) h.print_errs();
  }
}

// ---- E: pacing outranks aging ----------------------------------------
void TxArbiterSuite::pacing_outranks_aging() {
  // three aged non-solicited requesters vs a continuously re-armed ACMP:
  // grants must alternate non-sol / solicited — never two non-sol in a row
  // while solicited traffic waits: [1, 2, 4, 2, 3, 2]
  {
    auto s0 = h.snap();
    h.ready_pct = 60;
    h.arm(2, 240);
    int g = h.wait_grant(300);
    CHECK(g == 2, "E lead-in ACMP granted (got %d)", g);
    h.ready_pct = 0;                 // freeze the lead-in frame mid-stream
    h.arm(1, 120); h.arm(4, 120);    // std slots
    h.arm(3, 120, true);             // oversize slot: keeps one std free
    h.tick_burst = 15;               // age 1, 4, 3 past T-TX-AGING
    h.run(15);
    h.arm(2, 80);                    // fresh solicited, ticks OFF again
    h.ready_pct = 60;
    while (h.in_service) h.step();
    static constexpr std::array<int, 6> expseq = {{1, 2, 4, 2, 3, 2}};
    for (int k = 0; k < 6; ++k) {
      g = h.wait_grant(3000);
      CHECK(g == expseq[k], "E grant #%d is %d exp %d", k, g, expseq[k]);
      if (g == 2 && k < 4) {         // keep solicited pressure up
        h.ready_pct = 0;
        h.arm(2, 80);
        h.ready_pct = 60;
      }
      while (h.in_service) h.step();
    }
    CHECK(h.clean_since(s0), "E pacing rounds byte-exact and model-matched");
    if (!h.clean_since(s0)) h.print_errs();
  }
}

// ---- F: a PP_SLOT_NULL_C handle is never granted ---------------------
void TxArbiterSuite::a_null_slot_handle_is_never_granted() {
  {
    auto s0 = h.snap();
    size_t nglog = h.grant_log.size();
    h.slot_field[3] = 7; h.req_mask |= 1u << 3;   // null-handle "request"
    h.run(40);
    CHECK(h.grant_log.size() == nglog, "F null handle never granted");
    h.arm(1, 24);
    int g = h.wait_grant(300);
    CHECK(g == 1, "F real requester wins past the null one (got %d)", g);
    h.req_mask &= ~(1u << 3);
    while (h.in_service) h.step();
    CHECK(h.clean_since(s0), "F clean");
  }
}

// ---- G: randomized contention, >= 1000 frames ------------------------
void TxArbiterSuite::randomized_contention_matches_the_model() {
  {
    constexpr long kRandomFrames = 1000;           // the phase's frame target
    constexpr long kRandomGuardCycles = 3000000;   // cap on cycles spent here
    constexpr int  kDrainCycles = 30000;           // cap on the closing drain
    long target = h.frames_done + kRandomFrames;
    h.tick_div = 50;                 // sparse ms ticks
    long guard = 0;
    while (h.frames_done < target && guard < kRandomGuardCycles) {
      // keep contention up: arm any idle requester when a slot is free
      uint32_t busy = h.req_mask;
      int idle[6];
      int ni = 0;
      for (int r = 0; r < 6; ++r) if (!((busy >> r) & 1)) idle[ni++] = r;
      if (ni > 0 && (h.rnd() % 4u) != 0) {
        int r = idle[h.rnd() % uint32_t(ni)];
        bool ov = h.slot_free[4] && (h.rnd() % 10u) == 0;
        if (ov || h.expected_alloc(false) >= 0) {
          int len = 1 + int(h.rnd() % 64u);
          h.arm(r, len, ov);
        }
      }
      h.ready_pct = 40 + int(h.rnd() % 61u);
      int n = 1 + int(h.rnd() % 12u);
      h.run(n);
      guard += n;
    }
    h.tick_div = 0;
    // drain everything still pending
    h.ready_pct = 100;
    for (int c = 0; c < kDrainCycles && (h.pend_now() || h.in_service); ++c)
      h.step();
    CHECK(h.frames_done >= target, "G >= 1000 randomized frames (%ld)",
          h.frames_done - (target - kRandomFrames));
    CHECK(h.e_gnt_mismatch == 0, "G every grant matched to the model (%ld off)",
          h.e_gnt_mismatch);
    CHECK(h.e_byte == 0, "G merged stream byte-exact (%ld off)", h.e_byte);
    CHECK(h.e_sof == 0 && h.e_eof == 0, "G sof/eof exact (%ld/%ld off)",
          h.e_sof, h.e_eof);
    CHECK(h.e_spur == 0, "G no bytes outside a granted frame (%ld)", h.e_spur);
    CHECK(h.e_onehot == 0 && h.e_pulse == 0,
          "G grants one-hot single-cycle (%ld/%ld)", h.e_onehot, h.e_pulse);
    CHECK(h.e_gnt_midframe == 0, "G no mid-frame grant ever (%ld)",
          h.e_gnt_midframe);
    CHECK(h.e_stall == 0, "G no arbitration stall with work pending (%ld)",
          h.e_stall);
    CHECK(h.e_alloc == 0, "G pool allocation bookkeeping exact (%ld)",
          h.e_alloc);
    CHECK(dut->slots_free_o == 5 && dut->slots_ready_o == 0,
          "G pool fully drained");
    for (int i = 0; i < 6; ++i)
      CHECK(h.cnt_field(i) == h.ref.cnt[i],
            "G counter[%d] dut %u model %u", i, h.cnt_field(i), h.ref.cnt[i]);
    long total = 0;
    for (int i = 0; i < 6; ++i) total += h.ref.cnt[i];
    CHECK(total == long(h.grant_log.size()),
          "G counter sum equals grant count (%ld vs %zu)",
          total, h.grant_log.size());
  }
}

// ---- H: cancellation between selection and serializer acceptance ----
void TxArbiterSuite::a_cancelled_selection_produces_no_grant() {
  {
    auto s0 = h.snap();
    int slot = h.prep(17);
    h.raise(5, slot);
    for (int i = 0; i < 8 && !h.select_pending; ++i) h.step();
    CHECK(h.select_pending && h.selected_req == 5,
          "H originator request reaches the pre-start selection stage");
    size_t g0 = h.grant_log.size();
    long f0 = h.frames_done;
    h.req_mask &= ~(1u << 5);
    h.start_abort = true;
    h.step();
    h.start_abort = false;
    h.run(4);
    CHECK(h.grant_log.size() == g0 && h.frames_done == f0,
          "H withdrawn selection produces no grant or frame");
    CHECK((dut->slots_ready_o & (1u << slot)) != 0
              && dut->slots_free_o == 4,
          "H aborted start leaves the committed slot untouched");
    h.raise(5, slot);
    CHECK(h.wait_grant(100) == 5,
          "H the same slot remains serviceable after the abort");
    CHECK(h.wait_frames(f0 + 1, 1000) && dut->slots_free_o == 5
              && h.clean_since(s0),
          "H accepted retry is byte-exact and frees the pool");
  }
}

int TxArbiterSuite::run() {
  dut->alloc_req_i = 0; dut->oversize_i = 0;
  dut->wr_slot_i = 0; dut->wr_addr_i = 0; dut->wr_data_i = 0;
  dut->wr_valid_i = 0; dut->wr_commit_i = 0; dut->wr_len_i = 0;
  dut->req_valid_i = 0; dut->tx_slot_i = 0; dut->tx_ready_i = 0;
  dut->start_abort_i = 0;
  dut->tick_ms_i = 0;

  reset_leaves_the_arbiter_quiescent();
  strict_priority_when_every_requester_is_fresh();
  a_frame_is_atomic_against_a_higher_priority_arrival();
  aging_promotes_a_starved_requester();
  pacing_outranks_aging();
  a_null_slot_handle_is_never_granted();
  randomized_contention_matches_the_model();
  a_cancelled_selection_produces_no_grant();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  if (fails) h.print_errs();
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vtx_arbiter_harness> model;
  TxArbiterSuite suite(model.get());
  return suite.run();
}

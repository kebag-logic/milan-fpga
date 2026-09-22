// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_prng suite — independent expectations, never DUT logic.
//
// The reference model is written from the documented contract (08 §3 F08.2 +
// IEEE 1722.1-2021 §6.2.4.2.2 practice), not from the RTL: the primitive
// polynomial x^64+x^63+x^61+x^60+1 in right-shift Galois form, seed =
// entity_id XOR cycles-since-reset latched at the FIRST link-up rise only
// (zero seed replaced by a nonzero substitute), and rejection-sampled range
// draws whose attempts ride the free-running stream one state per cycle.
// Bit-exactness against that model IS the requirement — an LFSR is its
// polynomial. The suite cross-checks the raw stream for 10k steps, every
// range draw value/accept-cycle against model prediction, endpoint
// reachability, once-only seeding across link flaps, entity_id divergence,
// the zero-seed guard, and that rejection genuinely occurs at the expected
// rate for the 5001-wide span against its 8192 mask (~39 %).
#include <array>
#include <cinttypes>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include "VKL_pp_prng.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- independent model (from 08 §3 F08.2, not from the RTL) --------------
constexpr uint64_t POLY = 0xD800000000000000ull;  // x^64+x^63+x^61+x^60+1
constexpr uint64_t NONZ = 1;                      // never-zero substitute
constexpr int DECIMATION = 16;                    // LFSR steps per clock edge

struct Model {
  uint64_t lfsr = NONZ;
  uint64_t ctr = 0;
  bool seeded = false;
  bool linkq = false;
  static uint64_t step1(uint64_t s) { return (s >> 1) ^ ((s & 1) ? POLY : 0); }
  // per-cycle advance = decimation by 16 (fresh 16-bit draw window each
  // cycle; still maximal because gcd(16, 2^64-1) = 1)
  static uint64_t next(uint64_t s) {
    for (int i = 0; i < DECIMATION; ++i) s = step1(s);
    return s;
  }
  void edge(bool rstn, bool link, uint64_t eid) {
    if (!rstn) { lfsr = NONZ; ctr = 0; seeded = false; linkq = false; return; }
    const bool rise = link && !linkq;
    if (rise && !seeded) {
      const uint64_t s = eid ^ ctr;  // pre-edge counter value
      lfsr = s ? s : NONZ;
      seeded = true;
    } else {
      lfsr = next(lfsr);
    }
    ++ctr;
    linkq = link;
  }
};

// F08.2 ranges (F08.1 rows: T-ACMP-DELAY, T-ADP-DELAY-START, T-ADP-DELAY,
// T-MRP-LEAVEALL, T-NOTIF-MONITOR; then the MAAP kinds of 11 — probe_timer
// strictly inside (500, 600) ms and announce_timer strictly inside
// (30, 32) s per IEEE 1722-2016 B.3.4, and the kind-7 pool-offset draw
// uniform over the whole Table B.9 pool 0..0xFDFF). MASK = next power of
// two above the span.
constexpr std::array<uint16_t, 8> MASK  = {0x03FF, 0x07FF, 0x0FFF, 0x1FFF, 0x7FFF,
                                           0x007F, 0x07FF, 0xFFFF};
constexpr std::array<uint16_t, 8> LIMIT = {1000, 2000, 4000, 5000, 30000,
                                           98, 1998, 0xFDFF};
constexpr std::array<uint16_t, 8> BASE  = {0, 0, 0, 10000, 30000, 501, 30001, 0};

struct Tb {
  VKL_pp_prng* dut;
  Model m;
  bool compare = false;
  long stream_mismatch = 0;
  long zeros = 0;
  long consec_same = 0;
  long valid_pulses = 0;
  uint64_t prev_lfsr = 0;

  explicit Tb(VKL_pp_prng* d) : dut(d) {}

  void tick() {
    dut->clk_i = 0; dut->eval();   // pre-edge: settle this cycle's inputs
    dut->clk_i = 1; dut->eval();   // rising edge: registers update
    m.edge(dut->rst_n, dut->link_up_i, dut->entity_id_i);
    if (compare && dut->rst_n) {
      if (dut->dbg_lfsr_o != m.lfsr) ++stream_mismatch;
      if (dut->dbg_lfsr_o == 0) ++zeros;
      if (dut->dbg_lfsr_o == prev_lfsr) ++consec_same;
    }
    prev_lfsr = dut->dbg_lfsr_o;
    if (dut->draw_valid_o) ++valid_pulses;
  }
};

struct DrawRes {
  bool done;            // DUT produced a valid
  uint16_t ms;          // DUT value
  int lat;              // cycles after the request tick until valid observed
  bool model_ok;        // model prediction resolved
  uint16_t model_ms;    // model-predicted value
  int model_lat;        // model-predicted latency
  int rejects;          // model-counted rejected attempts
};

// Cycles a pending draw is tracked for before the harness gives up on it.
constexpr int DRAW_TIMEOUT_CYCLES = 600;

// One draw: request for one cycle, then track DUT valid against the model's
// independent replay of the attempt discipline (attempt j uses the stream
// state j+1 edges after the request edge; accept iff masked value <= limit).
static DrawRes draw(Tb& tb, int kind, bool interfere = false) {
  VKL_pp_prng* d = tb.dut;
  d->draw_req_i = 1; d->draw_kind_i = kind;
  tb.tick();
  d->draw_req_i = 0;
  bool mdone = false;
  uint16_t mms = 0;
  int mlat = -1;
  int rej = 0;
  for (int t = 1; t <= DRAW_TIMEOUT_CYCLES; ++t) {
    if (!mdone) {  // model attempt uses the state BEFORE this edge
      const uint16_t a = static_cast<uint16_t>(tb.m.lfsr) & MASK[kind];
      if (a <= LIMIT[kind]) {
        mdone = true;
        mms = static_cast<uint16_t>(a + BASE[kind]);
        mlat = t;
      } else {
        ++rej;
      }
    }
    if (interfere && t == 1) { d->draw_req_i = 1; d->draw_kind_i = 0; }
    tb.tick();
    if (interfere && t == 1) d->draw_req_i = 0;
    if (d->draw_valid_o)
      return {true, static_cast<uint16_t>(d->draw_ms_o), t,
              mdone, mms, mlat, rej};
  }
  return {false, 0, 0, mdone, mms, mlat, rej};
}

namespace {

constexpr uint64_t EID_A = 0x001B92FFFE0170ADull;
constexpr uint64_t EID_B = 0xA5A5A5A55A5A5A5Aull;

//! Owns the model, the tick loop's shadow state and the tally, so every phase
//! below reads the same counters the summary line prints.
class PrngSuite {
 public:
  PrngSuite() : dut(model.get()), tb(dut) {}

  int run();

 private:
  void reset_state_is_the_nonzero_constant();
  void first_link_up_rise_latches_the_seed();
  void raw_stream_is_bit_exact();
  void later_rises_do_not_reseed();
  void range_draws_match_the_model();
  void rejection_occurs_where_the_mask_overshoots();
  void busy_tracks_the_pending_draw();
  void zero_seed_is_replaced();
  void two_entity_ids_diverge();

  const milan::tb::Model<VKL_pp_prng> model;
  VKL_pp_prng* const dut;
  Tb tb;
  int checks = 0;
  int fails = 0;
  long cyc_since_rst = 0;  // independent mirror of the seed counter
  long total_reqs = 0;
  std::array<long, 8> rej_frac_pct = {0, 0, 0, 0, 0, 0, 0, 0};
};

// ---- A: reset state --------------------------------------------------
void PrngSuite::reset_state_is_the_nonzero_constant() {
  dut->rst_n = 0; dut->link_up_i = 0;
  dut->draw_req_i = 0; dut->draw_kind_i = 0;
  dut->entity_id_i = EID_A;
  for (int i = 0; i < 4; ++i) tb.tick();
  CHECK(dut->dbg_seeded_o == 0, "A: not seeded in reset");
  CHECK(dut->draw_valid_o == 0, "A: no valid in reset");
  CHECK(dut->dbg_lfsr_o == NONZ,
        "A: reset state is the nonzero constant, got %016" PRIx64,
        static_cast<uint64_t>(dut->dbg_lfsr_o));

  dut->rst_n = 1;
  tb.compare = true;
  for (int i = 0; i < 5; ++i) { tb.tick(); ++cyc_since_rst; }
  CHECK(tb.stream_mismatch == 0, "A: pre-seed free-run matches model");
}

// ---- B: FIRST link-up rise latches the seed --------------------------
void PrngSuite::first_link_up_rise_latches_the_seed() {
  const uint64_t exp_ctr = static_cast<uint64_t>(cyc_since_rst);  // pre-edge ctr at rise
  dut->link_up_i = 1;
  tb.tick(); ++cyc_since_rst;
  CHECK(dut->dbg_seeded_o == 1, "B: seeded after first rise");
  CHECK(dut->dbg_lfsr_o == (EID_A ^ exp_ctr),
        "B: seed = entity_id XOR free-running counter, got %016" PRIx64,
        static_cast<uint64_t>(dut->dbg_lfsr_o));
  CHECK(tb.stream_mismatch == 0, "B: model seeded identically");
}

// ---- C: raw stream bit-exact for 10k steps ---------------------------
void PrngSuite::raw_stream_is_bit_exact() {
  for (int i = 0; i < 10000; ++i) tb.tick();
  CHECK(tb.stream_mismatch == 0, "C: 10k steps bit-exact, %ld mismatches",
        tb.stream_mismatch);
  CHECK(tb.zeros == 0, "C: state never zero");
  CHECK(tb.consec_same == 0, "C: advances every cycle");
}

// ---- D: re-seeding on later rises is forbidden -----------------------
void PrngSuite::later_rises_do_not_reseed() {
  dut->link_up_i = 0;
  for (int i = 0; i < 8; ++i) tb.tick();
  dut->entity_id_i = EID_B;  // a re-seed would visibly take this value
  const uint64_t pre_rise = tb.m.lfsr;
  dut->link_up_i = 1;
  tb.tick();
  CHECK(dut->dbg_lfsr_o == Model::next(pre_rise),
        "D: second rise advances the stream, does not reseed");
  CHECK(dut->dbg_seeded_o == 1, "D: seeded flag persists");
  for (int i = 0; i < 200; ++i) tb.tick();
  CHECK(tb.stream_mismatch == 0, "D: stream bit-exact across the link flap");
}

// ---- E: range draws --------------------------------------------------
void PrngSuite::range_draws_match_the_model() {
  constexpr std::array<int, 8> NDRAW = {6000, 9000, 12000, 2200, 2200, 4000, 6000, 2200};
  for (int k = 0; k < 8; ++k) {
    long bad_bounds = 0;
    long bad_val = 0;
    long bad_lat = 0;
    long rejected_draws = 0;
    uint32_t mn = 0xFFFFFFFFu;
    uint32_t mx = 0;
    double sum = 0.0;
    for (int i = 0; i < NDRAW[k]; ++i) {
      DrawRes r = draw(tb, k);
      ++total_reqs;
      if (!r.done) { ++bad_val; continue; }
      if (r.ms < BASE[k] ||
          r.ms > static_cast<uint32_t>(BASE[k]) + LIMIT[k]) ++bad_bounds;
      if (!r.model_ok || r.ms != r.model_ms) ++bad_val;
      if (r.lat != r.model_lat) ++bad_lat;
      if (r.rejects > 0) ++rejected_draws;
      if (r.ms < mn) mn = r.ms;
      if (r.ms > mx) mx = r.ms;
      sum += r.ms;
      for (int g = i % 3; g > 0; --g) tb.tick();  // vary alignment
    }
    rej_frac_pct[k] = rejected_draws * 100 / NDRAW[k];
    CHECK(bad_bounds == 0, "E k%d: %ld draws out of bounds", k, bad_bounds);
    CHECK(bad_val == 0, "E k%d: %ld draws mismatch model value", k, bad_val);
    CHECK(bad_lat == 0, "E k%d: %ld draws accept on the wrong cycle", k, bad_lat);
    const double mid = BASE[k] + LIMIT[k] / 2.0;
    const double mean = sum / NDRAW[k];
    CHECK(std::fabs(mean - mid) < LIMIT[k] * 0.05,
          "E k%d: mean %.1f vs midpoint %.1f", k, mean, mid);
    if (k <= 2 || k == 5) {  // small ranges: both endpoints must be drawn
      CHECK(mn == BASE[k], "E k%d: min endpoint %u never drawn, min %u",
            k, BASE[k], mn);
      CHECK(mx == static_cast<uint32_t>(BASE[k]) + LIMIT[k],
            "E k%d: max endpoint %u never drawn, max %u",
            k, BASE[k] + LIMIT[k], mx);
    } else {       // wide ranges: min/max proximity (2 % of the span)
      CHECK(mn <= BASE[k] + LIMIT[k] / 50u,
            "E k%d: min %u not near base %u", k, mn, BASE[k]);
      CHECK(mx >= static_cast<uint32_t>(BASE[k]) + LIMIT[k] - LIMIT[k] / 50u,
            "E k%d: max %u not near top %u", k, mx, BASE[k] + LIMIT[k]);
    }
    printf("  kind %d: n=%d min=%u max=%u mean=%.1f rejected-draw-frac=%ld%%\n",
           k, NDRAW[k], mn, mx, mean, rej_frac_pct[k]);
  }
}

void PrngSuite::rejection_occurs_where_the_mask_overshoots() {
  // rejection genuinely occurs where the mask overshoots the span:
  // kind 3 span 5001 vs mask 8192 -> per-attempt reject p = 3191/8192 = 39 %
  CHECK(rej_frac_pct[3] > 20, "E: kind3 rejection fraction %ld%% <= 20%%",
        rej_frac_pct[3]);
  CHECK(rej_frac_pct[3] < 60, "E: kind3 rejection fraction %ld%% >= 60%%",
        rej_frac_pct[3]);
  // ...and mostly does not where the mask is tight (kind 0: 23/1024 = 2.2 %)
  CHECK(rej_frac_pct[0] < 10, "E: kind0 rejection fraction %ld%% >= 10%%",
        rej_frac_pct[0]);
  // kind 5 span 99 vs mask 128 -> per-attempt reject p = 29/128 = 23 %:
  // the B.3.4.2 bounds are EXCLUSIVE, so a draw of exactly 500 or 600 ms
  // must be structurally impossible (the bounds check above already graded
  // every draw against 501..599)
  CHECK(rej_frac_pct[5] > 5, "E: kind5 rejection fraction %ld%% <= 5%%",
        rej_frac_pct[5]);
}

void PrngSuite::busy_tracks_the_pending_draw() {
  // busy visible during a pending draw, clears with valid
  dut->draw_req_i = 1; dut->draw_kind_i = 3;
  tb.tick();
  dut->draw_req_i = 0;
  ++total_reqs;
  CHECK(dut->draw_busy_o == 1, "E: busy during a pending draw");
  int guard = 0;
  while (!dut->draw_valid_o && ++guard < DRAW_TIMEOUT_CYCLES) tb.tick();
  CHECK(guard < DRAW_TIMEOUT_CYCLES && dut->draw_busy_o == 0,
        "E: busy clears on valid");

  // a request while busy is ignored (not queued)
  DrawRes ri = draw(tb, 3, true);
  ++total_reqs;  // the interfering request must NOT count: it is dropped
  CHECK(ri.done && ri.ms >= 10000 && ri.ms <= 15000,
        "E: mid-draw request ignored, kind3 bounds hold, got %u", ri.ms);
  CHECK(ri.model_ok && ri.ms == ri.model_ms && ri.lat == ri.model_lat,
        "E: mid-draw request ignored, prediction holds");
  const long vp = tb.valid_pulses;
  for (int i = 0; i < 8; ++i) tb.tick();
  CHECK(tb.valid_pulses == vp, "E: ignored request produced an extra valid");
  CHECK(tb.valid_pulses == total_reqs,
        "E: one valid per accepted request, %ld valids vs %ld requests",
        tb.valid_pulses, total_reqs);
}

// ---- F: zero-seed guard ----------------------------------------------
void PrngSuite::zero_seed_is_replaced() {
  dut->rst_n = 0; dut->link_up_i = 0;
  for (int i = 0; i < 4; ++i) tb.tick();
  dut->rst_n = 1;
  long cs = 0;
  for (int i = 0; i < 7; ++i) { tb.tick(); ++cs; }
  dut->entity_id_i = static_cast<uint64_t>(cs);  // entity_id XOR ctr == 0 at the rise
  dut->link_up_i = 1;
  tb.tick();
  CHECK(dut->dbg_lfsr_o == NONZ,
        "F: zero seed replaced by the nonzero substitute, got %016" PRIx64,
        static_cast<uint64_t>(dut->dbg_lfsr_o));
  CHECK(dut->dbg_lfsr_o == tb.m.lfsr, "F: model substitutes identically");
}

// ---- G: two entity_ids diverge ---------------------------------------
void PrngSuite::two_entity_ids_diverge() {
  constexpr int DIVERGE_STEPS = 64;  // states compared after each seed edge
  auto run_seed = [&](uint64_t eid, uint64_t states[DIVERGE_STEPS]) {
    dut->link_up_i = 0; dut->rst_n = 0;
    for (int i = 0; i < 4; ++i) tb.tick();
    dut->rst_n = 1; dut->entity_id_i = eid;
    for (int i = 0; i < 6; ++i) tb.tick();
    dut->link_up_i = 1;
    tb.tick();  // seed edge
    for (int i = 0; i < DIVERGE_STEPS; ++i) {
      states[i] = dut->dbg_lfsr_o;
      tb.tick();
    }
  };
  uint64_t sa[DIVERGE_STEPS];
  uint64_t sb[DIVERGE_STEPS];
  run_seed(0x0000000000000001ull, sa);
  run_seed(0x0000000000000002ull, sb);
  int diff = 0;
  for (int i = 0; i < DIVERGE_STEPS; ++i) if (sa[i] != sb[i]) ++diff;
  CHECK(diff > 0, "G: different entity_ids diverge within 64 steps");
  CHECK(diff == DIVERGE_STEPS,
        "G: XOR of the two streams is itself a never-zero LFSR stream -> "
        "all 64 states differ, got %d", diff);
  CHECK(tb.stream_mismatch == 0, "G: zero stream mismatches over the whole run");
}

int PrngSuite::run() {
  reset_state_is_the_nonzero_constant();
  first_link_up_rise_latches_the_seed();
  raw_stream_is_bit_exact();
  later_rises_do_not_reseed();
  range_draws_match_the_model();
  rejection_occurs_where_the_mask_overshoots();
  busy_tracks_the_pending_draw();
  zero_seed_is_replaced();
  two_entity_ids_diverge();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  PrngSuite suite;
  return suite.run();
}

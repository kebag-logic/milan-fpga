// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_event_router suite — independent expectations, never DUT logic.
//
// The C++ model independently implements the documented policy (02 §5
// class-C sticky events + the 03 §2/§5 router): per-source sticky latch
// holding the FIRST payload until ack, re-fire before ack = coalesced flag
// + one saturating lost tick, ack+re-fire on the same cycle = a NEW event
// (nothing lost), and a round-robin presentation whose base advances past
// each delivered source. Every cycle the DUT outputs are compared against
// the model pre-edge (lockstep), every delivery is matched, the lost-count
// read port is spot-read on a rotating index every cycle, and the phase-J
// conservation law strobes = delivered + lost + pending is closed per
// source — the "never silently dropped" contract as arithmetic.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include "VKL_pp_event_router.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// shipping shape — must match the DUT parameter defaults (no -G overrides)
constexpr int N  = 16;
constexpr int PW = 16;

// the per-source lost counter saturates here instead of wrapping
constexpr uint8_t kLostCountMax = 0xFF;
// drain() is bounded: a router that never empties ends the run, not hangs
constexpr int kDrainMaxCycles = 100;

struct Delivery { int src; uint16_t payload; bool lost; };

// ------------------------------------------------------------------ model
struct Model {
  bool     pending[N]   = {};
  bool     coalesced[N] = {};
  uint16_t payload[N]   = {};
  uint8_t  lost_sat[N]  = {};   // what the DUT counter must read
  uint64_t lost_true[N] = {};   // unbounded, for the conservation law
  uint64_t strobes[N]   = {};
  uint64_t delivered[N] = {};
  bool     valid = false;
  int      sel = 0;
  int      ptr = 0;

  bool any_pending() const {
    for (int s = 0; s < N; ++s) if (pending[s]) return true;
    return false;
  }

  // one clock edge: this cycle's strobes/payloads/ack, pre-edge state read
  void step(uint32_t strobe_mask, const uint16_t* pl, bool ack) {
    const bool deliver = valid && ack;
    const int  dsrc    = deliver ? sel : -1;

    // grant from the registered pending set minus the delivered event
    bool pa[N];
    for (int s = 0; s < N; ++s) pa[s] = pending[s];
    if (deliver) pa[dsrc] = false;
    const int base = deliver ? (sel + 1) % N : ptr;
    int gnt = -1;
    for (int k = 0; k < N; ++k) {
      const int idx = (base + k) % N;
      if (pa[idx]) { gnt = idx; break; }
    }

    // per-source sticky latch
    for (int s = 0; s < N; ++s) {
      if (strobe_mask & (1u << s)) {
        ++strobes[s];
        if (!pending[s] || s == dsrc) {          // a NEW event
          pending[s] = true; payload[s] = pl[s]; coalesced[s] = false;
        } else {                                 // re-fire before ack
          coalesced[s] = true;
          ++lost_true[s];
          if (lost_sat[s] != kLostCountMax) ++lost_sat[s];
        }
      } else if (s == dsrc) {
        pending[s] = false; coalesced[s] = false;
      }
    }

    if (deliver) { ++delivered[dsrc]; ptr = (dsrc + 1) % N; }
    if (deliver || !valid) { valid = (gnt >= 0); if (gnt >= 0) sel = gnt; }
  }
};

namespace {

// ---------------------------------------------------------------- harness
//! The router, the reference model, the delivery log and the tally in one
//! object. `checks`/`fails` were file-scope mutables (I.2) and the lettered
//! phases below were one 252-line `main` (F.3); the BFM half of this struct
//! is unchanged.
struct Harness {
  const milan::tb::Model<VKL_pp_event_router> model;
  VKL_pp_event_router* const dut = model.get();
  Model    m;
  uint64_t cycle = 0;
  uint16_t pl[N] = {};
  uint64_t out_mm = 0;
  uint64_t lost_rd_mm = 0;
  uint64_t first_mm_cycle = 0;
  std::string first_mm_what;
  std::vector<Delivery> dl;
  int checks = 0;
  int fails = 0;

  void mm(const char* what) {
    if (!out_mm && !lost_rd_mm) { first_mm_cycle = cycle; first_mm_what = what; }
  }

  void set_pl(int s, uint16_t v) {
    pl[s] = v;
    const int w  = (s * PW) / 32;
    const int sh = (s * PW) % 32;
    const uint32_t msk = 0xFFFFu << sh;
    dut->src_payload_i[w] = (dut->src_payload_i[w] & ~msk)
                          | (static_cast<uint32_t>(v) << sh);
  }

  void tick(uint32_t strobe_mask, bool ack) {
    dut->src_strobe_i = static_cast<uint16_t>(strobe_mask);
    dut->evt_ack_i    = ack;
    const int ls = static_cast<int>(cycle % N);
    dut->lost_src_i = static_cast<uint8_t>(ls);

    // settle combinational logic with this cycle's inputs
    dut->clk_i = 0; dut->eval();

    // observe PRE-EDGE: registered outputs vs the model's registered state
    if (static_cast<bool>(dut->evt_valid_o) != m.valid) { mm("valid"); ++out_mm; }
    if (m.valid && dut->evt_valid_o) {
      if (static_cast<int>(dut->evt_src_o) != m.sel)    { mm("src");     ++out_mm; }
      if (static_cast<uint16_t>(dut->evt_payload_o)
          != m.payload[m.sel])                          { mm("payload"); ++out_mm; }
      if (static_cast<bool>(dut->evt_lost_o) != m.coalesced[m.sel]) { mm("lost"); ++out_mm; }
    } else if (!m.valid && dut->evt_lost_o) { mm("lost@idle"); ++out_mm; }
    if (static_cast<uint8_t>(dut->lost_count_o) != m.lost_sat[ls]) {
      mm("lost_rd"); ++lost_rd_mm;
    }

    if (m.valid && ack) dl.push_back({m.sel, m.payload[m.sel], m.coalesced[m.sel]});

    m.step(strobe_mask, pl, ack);

    // rising edge: registers update
    dut->clk_i = 1; dut->eval();
    ++cycle;
  }

  // combinational read of one lost counter (no clock edge)
  uint8_t read_lost(int s) {
    dut->lost_src_i = static_cast<uint8_t>(s);
    dut->clk_i = 0; dut->eval();
    return dut->lost_count_o;
  }

  // ack until the router is empty (bounded)
  int drain() {
    int n = 0;
    while ((m.valid || m.any_pending()) && n < kDrainMaxCycles) {
      tick(0, true); ++n;
    }
    return n;
  }

  int run();

  void reset_and_check_the_router_is_idle();
  void check_a_single_event_is_delivered_exactly_once();
  void check_a_restrobe_before_ack_holds_the_first_payload();
  void check_a_queued_source_coalesces_too();
  void check_ack_and_strobe_on_one_cycle_is_a_new_event();
  void check_sixteen_simultaneous_deliver_once_in_round_robin();
  void check_the_round_robin_pointer_wraps();
  void check_the_lost_counter_is_exact_then_saturates();
  void check_an_ack_while_idle_is_a_no_op();
  void check_full_saturation_rotates_one_per_cycle();
  void check_the_randomized_soak_closes_the_conservation_law();
  int report();
};

// ---- reset ----------------------------------------------------------
void Harness::reset_and_check_the_router_is_idle() {
  dut->rst_n = 0; dut->src_strobe_i = 0; dut->evt_ack_i = 0;
  dut->lost_src_i = 0;
  for (int w = 0; w < (N * PW) / 32; ++w) dut->src_payload_i[w] = 0;
  constexpr int kResetCycles = 4;
  for (int i = 0; i < kResetCycles; ++i) {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
  }
  dut->rst_n = 1;

  CHECK(dut->evt_valid_o == 0, "R1 idle after reset");
  {
    bool allz = true;
    for (int s = 0; s < N; ++s) allz &= (read_lost(s) == 0);
    CHECK(allz, "R2 all lost counters zero after reset");
  }
}

// ---- A: single event delivered exactly once -------------------------
void Harness::check_a_single_event_is_delivered_exactly_once() {
  set_pl(3, 0xABCD);
  tick(1u << 3, false);
  tick(0, false);
  CHECK(dut->evt_valid_o == 1, "A1 valid two cycles after the strobe");
  CHECK(dut->evt_src_o == 3, "A2 src 3 got %d", static_cast<int>(dut->evt_src_o));
  CHECK(dut->evt_payload_o == 0xABCD, "A3 payload got %04x",
        static_cast<int>(dut->evt_payload_o));
  CHECK(dut->evt_lost_o == 0, "A4 no loss flag");
  {
    bool sticky = true;
    for (int i = 0; i < 5; ++i) {
      tick(0, false);
      sticky &= dut->evt_valid_o && dut->evt_src_o == 3
             && dut->evt_payload_o == 0xABCD;
    }
    CHECK(sticky, "A5 event + payload held over 5 un-acked cycles");
  }
  tick(0, true);
  CHECK(dut->evt_valid_o == 0, "A6 valid drops after ack");
  CHECK(dl.size() == 1 && dl[0].src == 3 && dl[0].payload == 0xABCD
        && !dl[0].lost, "A7 delivered exactly once, clean");
  {
    for (int i = 0; i < 8; ++i) tick(0, false);
    CHECK(dl.size() == 1 && dut->evt_valid_o == 0, "A8 no re-delivery");
  }
  CHECK(read_lost(3) == 0, "A9 nothing lost");
}

// ---- B: re-strobe before ack — FIRST payload holds, counter ticks ---
void Harness::check_a_restrobe_before_ack_holds_the_first_payload() {
  set_pl(5, 0xAAAA);
  tick(1u << 5, false);
  tick(0, false);
  set_pl(5, 0xBBBB);
  tick(1u << 5, false);
  CHECK(dut->evt_payload_o == 0xAAAA, "B1 payload stays the FIRST got %04x",
        static_cast<int>(dut->evt_payload_o));
  CHECK(dut->evt_lost_o == 1, "B2 evt_lost set on coalesce");
  CHECK(read_lost(5) == 1, "B3 lost count 1 got %d", read_lost(5));
  set_pl(5, 0xCCCC);
  tick(1u << 5, false);
  CHECK(read_lost(5) == 2, "B4 lost count 2 got %d", read_lost(5));
  CHECK(dut->evt_payload_o == 0xAAAA, "B5 payload still the FIRST");
  tick(0, true);
  CHECK(dl.back().src == 5 && dl.back().payload == 0xAAAA
        && dl.back().lost, "B6 delivery carries FIRST payload + lost flag");
  set_pl(5, 0xDDDD);
  tick(1u << 5, false);
  tick(0, false);
  CHECK(dut->evt_valid_o && dut->evt_src_o == 5
        && dut->evt_payload_o == 0xDDDD, "B7 next event carries NEW payload");
  CHECK(dut->evt_lost_o == 0, "B8 fresh event has no loss flag");
  CHECK(read_lost(5) == 2, "B9 counter cumulative, not cleared by ack");
  drain();
}

// ---- C: coalesce on a queued-but-not-presented source ---------------
void Harness::check_a_queued_source_coalesces_too() {
  set_pl(1, 0x1111); set_pl(2, 0x2222);
  tick((1u << 1) | (1u << 2), false);
  tick(0, false);
  CHECK(dut->evt_valid_o && dut->evt_src_o == 1, "C1 src 1 presented first");
  set_pl(2, 0x2299);
  tick(1u << 2, false);
  CHECK(read_lost(2) == 1, "C2 queued source coalesces too");
  tick(0, true);                      // delivers 1, loads 2
  tick(0, true);                      // delivers 2
  CHECK(dl.back().src == 2 && dl.back().payload == 0x2222
        && dl.back().lost, "C3 queued source delivers FIRST payload + flag");
}

// ---- D: ack + strobe on the same cycle = a NEW event, nothing lost --
void Harness::check_ack_and_strobe_on_one_cycle_is_a_new_event() {
  set_pl(9, 0x9001);
  tick(1u << 9, false);
  tick(0, false);
  set_pl(9, 0x9002);
  tick(1u << 9, true);                // ack the old, latch the new
  CHECK(dl.back().src == 9 && dl.back().payload == 0x9001
        && !dl.back().lost, "D1 ack cycle delivers the OLD event");
  CHECK(dut->evt_valid_o == 0, "D2 one-cycle bubble through empty");
  tick(0, false);
  CHECK(dut->evt_valid_o && dut->evt_src_o == 9
        && dut->evt_payload_o == 0x9002 && dut->evt_lost_o == 0,
        "D3 NEW event presents with the new payload, clean");
  CHECK(read_lost(9) == 0, "D4 no lost tick on the ack+strobe race");
  drain();
}

// ---- E: N simultaneous — all delivered exactly once, RR order -------
void Harness::check_sixteen_simultaneous_deliver_once_in_round_robin() {
  {
    for (int s = 0; s < N; ++s) set_pl(s, static_cast<uint16_t>(0xE000 | s));
    const int p0 = m.ptr;
    const size_t d0 = dl.size();
    tick(0xFFFF, false);
    const int cyc = drain();
    CHECK(dl.size() - d0 == N, "E1 all %d delivered got %zu", N,
          dl.size() - d0);
    CHECK(cyc == N + 1, "E2 one event per cycle (%d cycles for %d + load)",
          cyc, N);
    bool order = true;
    bool pay   = true;
    bool clean = true;
    bool once[N] = {};
    for (size_t i = d0; i < dl.size(); ++i) {
      const int exp = (p0 + static_cast<int>(i - d0)) % N;
      order &= (dl[i].src == exp);
      pay   &= (dl[i].payload == (0xE000 | dl[i].src));
      clean &= !dl[i].lost;
      if (dl[i].src >= 0 && dl[i].src < N) once[dl[i].src] = true;
    }
    bool all = true;
    for (int s = 0; s < N; ++s) all &= once[s];
    CHECK(order, "E3 round-robin order from the pointer");
    CHECK(all, "E4 every source delivered");
    CHECK(pay, "E5 every payload matches its source");
    CHECK(clean, "E6 no loss flags on a single burst");
  }
}

// ---- F: RR pointer wrap, directed -----------------------------------
void Harness::check_the_round_robin_pointer_wraps() {
  set_pl(11, 0x0B0B);
  tick(1u << 11, false); tick(0, false); tick(0, true);  // ptr -> 12
  {
    const size_t d0 = dl.size();
    set_pl(1, 0x0101); set_pl(13, 0x0D0D);
    tick((1u << 1) | (1u << 13), false);
    drain();
    CHECK(dl.size() - d0 == 2 && dl[d0].src == 13
          && dl[d0 + 1].src == 1,
          "F1 wrap order 13 then 1 (ptr at 12) got %d,%d",
          dl.size() - d0 > 0 ? dl[d0].src : -1,
          dl.size() - d0 > 1 ? dl[d0 + 1].src : -1);
  }
}

// ---- H: lost counter exact then saturating (fresh source 4) ---------
void Harness::check_the_lost_counter_is_exact_then_saturates() {
  CHECK(read_lost(4) == 0, "H0 source 4 pristine");
  set_pl(4, 0x4441);
  tick(1u << 4, false);               // the event
  for (int i = 0; i < 100; ++i) tick(1u << 4, false);
  CHECK(read_lost(4) == 100, "H1 exact count got %d", read_lost(4));
  for (int i = 0; i < 155; ++i) tick(1u << 4, false);
  CHECK(read_lost(4) == kLostCountMax, "H2 saturates at 255 got %d",
        read_lost(4));
  for (int i = 0; i < 60; ++i) tick(1u << 4, false);
  CHECK(read_lost(4) == kLostCountMax,
        "H3 315 re-fires: pegged, no wrap got %d",
        read_lost(4));
  tick(0, true);
  CHECK(dl.back().src == 4 && dl.back().payload == 0x4441
        && dl.back().lost, "H4 still delivers the FIRST payload");
}

// ---- I: ack while idle is a no-op -----------------------------------
void Harness::check_an_ack_while_idle_is_a_no_op() {
  {
    const size_t d0 = dl.size();
    for (int i = 0; i < 3; ++i) tick(0, true);
    CHECK(dut->evt_valid_o == 0 && dl.size() == d0, "I1 idle ack ignored");
    set_pl(7, 0x0777);
    tick(1u << 7, false); tick(0, false);
    CHECK(dut->evt_valid_o && dut->evt_src_o == 7, "I2 router alive after");
    drain();
  }
}

// ---- G: full saturation — one delivery per cycle, rotating ----------
void Harness::check_full_saturation_rotates_one_per_cycle() {
  {
    for (int s = 0; s < N; ++s) set_pl(s, static_cast<uint16_t>(0x7000 | s));
    const size_t d0 = dl.size();
    for (int i = 0; i < 80; ++i) tick(0xFFFF, true);
    const size_t nd = dl.size() - d0;
    CHECK(nd >= 78, "G1 %zu deliveries in 80 saturated cycles", nd);
    bool rot = true;
    for (size_t i = d0 + 1; i < dl.size(); ++i)
      rot &= (dl[i].src == (dl[i - 1].src + 1) % N);
    CHECK(rot, "G2 saturated order rotates by one every cycle");
    tick(0, true); drain();
    bool sat_ok = true;
    for (int s = 0; s < N; ++s) sat_ok &= (read_lost(s) == m.lost_sat[s]);
    CHECK(sat_ok, "G3 all 16 climbing counters read back exactly");
  }
}

// ---- J: randomized soak, >= 2000 deliveries, model lockstep ---------
void Harness::check_the_randomized_soak_closes_the_conservation_law() {
  {
    const size_t d0 = dl.size();
    constexpr size_t   kSoakDeliveries = 2200;   // the soak's delivery floor
    constexpr uint64_t kSoakMaxCycles  = 60000;  // and its runtime guard
    uint32_t rng = 0xC0FFEE01u;
    auto rnd = [&rng]() {
      rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng;
    };
    uint64_t cycles = 0;
    while (dl.size() - d0 < kSoakDeliveries && cycles < kSoakMaxCycles) {
      uint32_t mask = 0;
      for (int s = 0; s < N; ++s) {
        if ((rnd() & 7u) == 0) {               // ~1/8 strobe probability
          mask |= 1u << s;
          set_pl(s, static_cast<uint16_t>(rnd()));
        }
      }
      const bool ack = (rnd() & 3u) != 0;      // ~3/4 ack probability
      tick(mask, ack);
      ++cycles;
    }
    drain();
    CHECK(dl.size() - d0 >= kSoakDeliveries, "J1 %zu random deliveries",
          dl.size() - d0);
    CHECK(out_mm == 0,
          "J2 per-cycle lockstep clean (%llu mismatches, first '%s' @%llu)",
          static_cast<unsigned long long>(out_mm), first_mm_what.c_str(),
          static_cast<unsigned long long>(first_mm_cycle));
    CHECK(lost_rd_mm == 0,
          "J3 rotating lost-port reads clean (%llu mismatches)",
          static_cast<unsigned long long>(lost_rd_mm));
    bool every = true;
    for (int s = 0; s < N; ++s) every &= (m.delivered[s] > 0);
    CHECK(every, "J4 no source starved");
    CHECK(!m.valid && !m.any_pending(), "J5 fully drained");
    // conservation: every strobe is a delivery or a counted loss — the
    // "never silently dropped" contract, closed per source
    for (int s = 0; s < N; ++s) {
      CHECK(m.strobes[s] == m.delivered[s] + m.lost_true[s],
            "J6.%d conservation: %llu strobes = %llu delivered + %llu lost",
            s, static_cast<unsigned long long>(m.strobes[s]),
            static_cast<unsigned long long>(m.delivered[s]),
            static_cast<unsigned long long>(m.lost_true[s]));
    }
    for (int s = 0; s < N; ++s) {
      CHECK(read_lost(s) == m.lost_sat[s],
            "J7.%d final counter got %d want %d", s, read_lost(s),
            static_cast<int>(m.lost_sat[s]));
    }
  }
}

int Harness::report() {
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int Harness::run() {
  reset_and_check_the_router_is_idle();
  check_a_single_event_is_delivered_exactly_once();
  check_a_restrobe_before_ack_holds_the_first_payload();
  check_a_queued_source_coalesces_too();
  check_ack_and_strobe_on_one_cycle_is_a_new_event();
  check_sixteen_simultaneous_deliver_once_in_round_robin();
  check_the_round_robin_pointer_wraps();
  check_the_lost_counter_is_exact_then_saturates();
  check_an_ack_while_idle_is_a_no_op();
  check_full_saturation_rotates_one_per_cycle();
  check_the_randomized_soak_closes_the_conservation_law();
  return report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Harness h;
  return h.run();
}

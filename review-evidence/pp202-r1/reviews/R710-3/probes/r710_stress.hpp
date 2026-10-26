// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (issue #202): randomized falsification of the Stream ID
// quarantine and distinctness claims of KL_acmp_talker. Included into a
// disposable copy of tb/acmp_talker/sim_main.cpp just before main().
//
// Oracle, independent of the suite's SidHistory:
//  * per 64-bit Stream ID: the last close strobe (withdrawal) time and the
//    FirstValue it was declared with {DA, VLAN, PCP epoch};
//  * C20: an open of an ID with another FirstValue less than 20 s
//    (2 x LeaveAllTime, IEEE 802.1Q-2018 35.2.2.8 / Table 10-7) after the
//    ID's last withdrawal  -> conformance violation;
//  * C30: an open that MOVES a source (its ID differs from its previous
//    declared one) onto an ID withdrawn less than 30 s before -> violation of
//    the documented quarantine claim (05 F05.12 "no move takes an ID declared
//    within Q");
//  * DIST: two sources publish the same 64-bit ID;
//  * DUP: an open whose ID equals another source's currently open ID.
// Timer service: every arm on a talker slot is honoured at its deadline.
#include <map>
#include <random>
#include <cstdlib>

namespace r710 {

struct Fv { uint64_t da; int vlan; int pcp; };
struct Last { bool seen; bool open; uint32_t wd_ms; Fv fv; int src; };

struct Stress {
  Hn& h;
  std::mt19937_64 rng;
  std::map<uint64_t, Last> ids;
  uint64_t open_sid[N_SRC] = {};
  bool open_v[N_SRC] = {};
  uint64_t prev_decl[N_SRC] = {};   // last ID each source declared
  bool prev_v[N_SRC] = {};
  int pcp_epoch = 0;
  int pcp_at_open[N_SRC] = {};
  // timer model: slot -> {deadline, owner}
  struct T { bool v; uint32_t dl; int owner; };
  std::map<int, T> tm;
  long c20 = 0, c30 = 0, dist = 0, dup = 0, opens = 0, moves = 0, keeps = 0;
  long same_reopen = 0;
  uint32_t min_move_gap = 0xFFFFFFFFu, min_fv_gap = 0xFFFFFFFFu;
  char first[256] = {0};

  explicit Stress(Hn& hh, uint64_t seed) : h(hh), rng(seed) {}

  uint32_t now() const { return h.d->now_ms_i; }
  uint64_t rnd(uint64_t n) { return n ? rng() % n : 0; }

  void note(const char* what, uint64_t sid, uint32_t gap, int src) {
    if (!first[0])
      snprintf(first, sizeof first, "%s sid=%016llx gap=%u ms src=%d at %u ms",
               what, static_cast<unsigned long long>(sid), gap, src, now());
  }

  void drain() {
    for (const auto& a : h.arms) {
      if (a.cancel) tm[a.slot].v = false;
      else tm[a.slot] = T{true, a.dl, a.owner};
    }
    h.arms.clear();
    for (const auto& g : h.gates) see(g);
    h.gates.clear();
    h.mreqs.clear(); h.resps.clear(); h.draws.clear();
    // distinctness of the published IDs
    for (int a = 0; a < N_SRC; ++a)
      for (int b = a + 1; b < N_SRC; ++b)
        if (h.sid_pub(a) == h.sid_pub(b)) { ++dist; note("DIST", h.sid_pub(a), 0, a); }
  }

  void see(const GateEv& g) {
    if (g.open) {
      ++opens;
      Fv fv{g.da, g.vlan, pcp_epoch};
      for (int s = 0; s < N_SRC; ++s)
        if (s != g.src && open_v[s] && open_sid[s] == g.sid) { ++dup; note("DUP", g.sid, 0, g.src); }
      auto it = ids.find(g.sid);
      const bool is_move = prev_v[g.src] && prev_decl[g.src] != g.sid;
      if (is_move) ++moves;
      if (it != ids.end() && it->second.seen && !it->second.open) {
        const Last& l = it->second;
        const uint32_t gap = g.ms - l.wd_ms;
        const bool other_fv = l.fv.da != fv.da || l.fv.vlan != fv.vlan || l.fv.pcp != fv.pcp
                              || l.src != g.src;
        if (other_fv) {
          if (gap < min_fv_gap) min_fv_gap = gap;
          if (gap < 20000u) { ++c20; note("C20", g.sid, gap, g.src); }
        } else {
          ++same_reopen;
        }
        if (is_move) {
          if (gap < min_move_gap) min_move_gap = gap;
          if (gap < 30000u) { ++c30; note("C30", g.sid, gap, g.src); }
        }
      }
      ids[g.sid] = Last{true, true, 0, fv, g.src};
      open_sid[g.src] = g.sid; open_v[g.src] = true;
      prev_decl[g.src] = g.sid; prev_v[g.src] = true;
    } else if (open_v[g.src]) {
      Last& l = ids[open_sid[g.src]];
      l.open = false; l.wd_ms = g.ms;
      open_v[g.src] = false;
    }
  }

  void tick() {
    h.tick();
    // honour due timers, one per clock
    for (auto& kv : tm) {
      if (kv.second.v && int32_t(now() - kv.second.dl) >= 0) {
        kv.second.v = false;
        h.d->tmr_exp_valid_i = 1;
        h.d->tmr_exp_slot_i = kv.first;
        h.d->tmr_exp_owner_i = kv.second.owner;
        h.tick();
        break;
      }
    }
    drain();
  }

  void run(int n) { for (int i = 0; i < n; ++i) tick(); }

  // advance the millisecond timebase by dt, at most `step` ms per clock
  void advance(uint32_t dt, uint32_t step) {
    const uint32_t end = now() + dt;
    while (int32_t(end - now()) > 0) {
      const uint32_t left = end - now();
      h.d->now_ms_i = now() + (left > step ? step : left);
      tick();
    }
  }

  void disable_return(int src, uint32_t off_ms) {
    const uint32_t all = 0xFFu;
    h.d->cfg_src_en_i = all & ~(1u << src);
    run(30);
    if (off_ms) advance(off_ms, 50);
    h.d->cfg_src_en_i = all;
    run(30);
  }

  void conflict(int src) {
    h.d->maap_conflict_valid_i = 1; h.d->maap_conflict_src_i = src;
    tick(); run(30);
  }

  void pcp() {
    h.d->srp_pcp_change_i = 1; ++pcp_epoch; tick(); run(30);
  }

  void listener(int src, bool up) { h.set_lsn(src, up ? LSN_READY : LSN_NONE); drain(); }

  // The adversarial case of the proof: source a leaves its ID Y (optionally
  // twice in a row, so its record stays on the older ID), then source b's
  // moves drive the cursor up to just below Y, and after a chosen delay
  // (around Q = 30 s, or anywhere in 0..45 s) b moves once more, which lands
  // on Y unless the record or the cursor guard refuses it.
  long ambushes = 0, landed = 0;
  void ambush(int a) {
    int b = int(rnd(N_SRC - 1)); if (b >= a) ++b;
    const bool twice = rnd(3) == 0;
    const uint64_t y_first = h.sid_pub(a);
    if (rnd(2)) conflict(a); else disable_return(a, 0);
    const uint64_t y_second = h.sid_pub(a);
    if (twice) {
      if (rnd(2)) conflict(a); else disable_return(a, 0);
    }
    const uint64_t y = (twice && rnd(2)) ? y_second : y_first;
    ++ambushes;
    // drive b until its published unique ID is just below y, moves fast
    for (int k = 0; k < 70000; ++k) {
      const unsigned cur = unsigned(h.sid_pub(b) & 0xFFFF);
      const unsigned dist = (unsigned(y & 0xFFFF) - cur) & 0xFFFF;
      if (dist <= 1 + rnd(3)) break;
      const uint64_t before = h.sid_pub(b);
      disable_return(b, 0);
      if ((k & 4095) == 4095) h.d->now_ms_i = now() + 1;
      if (h.sid_pub(b) == before) return;     // the guard keeps b's ID
    }
    const uint64_t t = rnd(4);
    uint32_t dly = t == 0 ? uint32_t(rnd(45000))
                 : t == 1 ? uint32_t(29000 + rnd(2001))
                 : t == 2 ? uint32_t(29990 + rnd(21))
                 : uint32_t(rnd(200));
    advance(dly, rnd(2) ? 1 : 1000);
    for (int k = 0; k < 4; ++k) {
      disable_return(b, 0);
      if (h.sid_pub(b) == y) { ++landed; break; }
    }
  }

  int go(long steps) {
    h.configure_the_talker_and_release_reset();
    h.run(400);
    for (int s = 0; s < N_SRC; ++s) h.set_lsn(s, LSN_READY);
    drain();
    for (long i = 0; i < steps; ++i) {
      h.draw_val = uint16_t(10000 + rnd(5001));       // T-MRP-LEAVEALL draw
      const int src = int(rnd(N_SRC));
      const uint64_t r = rnd(1000);
      if (r < 400) disable_return(src, rnd(4) == 0 ? uint32_t(rnd(3000)) : 0);
      else if (r < 600) conflict(src);
      else if (r < 620) pcp();
      else if (r < 700) listener(src, rnd(2));
      else if (r < 730) {
        // a burst: one or two sources cycle thousands of times, which walks
        // the cursor across halves and engages the guard; in the slow
        // variant the timebase moves inside the burst, so records and the
        // guard age while the cursor travels and it re-enters halves right
        // after the guard opens
        const bool slow = rnd(2);
        const int other = int(rnd(N_SRC));
        const long n = long(rnd(70000));
        const long chunk = long(1 + rnd(16384));
        for (long k = 0; k < n; ++k) {
          disable_return((k & 1) && rnd(4) == 0 ? other : src, 0);
          if ((k % chunk) == 0) {
            if (slow) advance(uint32_t(rnd(35000)), 1000);
            else h.d->now_ms_i = now() + 1;
          }
        }
      }
      else if (r < 800) ambush(src);
      // time: mostly small, sometimes across epoch boundaries
      const uint64_t t = rnd(100);
      if (t < 60) advance(uint32_t(rnd(6)), 1);
      else if (t < 90) advance(uint32_t(100 + rnd(3000)), 50);
      else advance(uint32_t(5000 + rnd(40000)), 1000);
    }
    // let every pending gap complete
    advance(70000, 1000);
    printf("R710-STRESS opens=%ld moves=%ld same_fv_reopens=%ld C20=%ld C30=%ld DIST=%ld DUP=%ld "
           "min_move_gap=%u min_otherfv_gap=%u ambushes=%ld landed=%ld now=%u\n",
           opens, moves, same_reopen, c20, c30, dist, dup, min_move_gap, min_fv_gap,
           ambushes, landed, now());
    if (first[0]) printf("R710-STRESS first violation: %s\n", first);
    return (c20 || c30 || dist || dup) ? 1 : 0;
  }
};

}  // namespace r710

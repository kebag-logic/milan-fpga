// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-2 P6 (disposable): the DR3a aggregate expiry swept
// across every state of the D3 walk. The probe copy of the wrap overrides
// NVM_RS_AGG_CYC_P with R391_AGG (a few thousand clocks) and taps the
// writer's state, pass and aggregate strobe (dbg_r391_*). Shifting the
// first device grant by h cycles moves the whole walk against the fixed
// bound, so the expiry falls, run by run, in every state the walk passes
// through. Each run is graded against the one path the writer banner and
// the ratification state, and the device face is proven unwedged after it.
#include <map>
#include <string>
static constexpr long R391_AGG = R391_AGG_VALUE;

struct R391Sweep {
  D3RestorePhase& r;
  H& x;
  long runs = 0, bad = 0, fired_n = 0, worst_late = 0;
  std::map<std::string, long> by_state;
  explicit R391Sweep(D3RestorePhase& rp) : r(rp), x(rp.x) {}

  static const char* wname(unsigned w) {
    static const char* n[] = {"WAITGO", "IMG", "IMGLOC", "RQ", "RD", "RULE", "NCFG", "LOC",
                              "LANE", "JUDGE", "APPLY", "NEXT", "RB", "RELOC", "DONE", "CLOSED"};
    return w < 16 ? n[w] : "?";
  }

  //! scenario 0: nine records saved; 1: 0x50 erased after pass 0 read it
  //! whole (pass 1 disagrees and rolls back, cause 5)
  void one(int scen, long h, int dram_lat, bool persist) {
    r.fresh();
    x.dram_lat = dram_lat;
    r.seed_every_record();
    x.nv_gnt_hold = int(h);
    const size_t ops0 = x.nvm_ops.size();
    bool erased = false;
    long fire_c = -1, fires = 0;
    unsigned fire_ws = 0, fire_pass = 0, prev_ws = 0, prev_pass = 0;
    bool prev_fired = false;
    long c = 0;
    const auto b = r.boot_with(R391_AGG + 3 * D3RestorePhase::RS_TMO, [&] {
      if (scen == 1 && !erased && r.reads_of(ops0, 0x50) == 2) {
        std::fill(x.nv_mem[0x50].begin(), x.nv_mem[0x50].begin() + 256, 0xFF);
        erased = true;
      }
      //! the registered agg_fired_r rises on the edge that takes the
      //! expiry; the state and pass sampled one clock earlier are the
      //! state the expiry was taken in (both are registers)
      const bool fired = x.d->dbg_r391_fired_o;
      if (fired && !prev_fired) {
        ++fires;
        if (fire_c < 0) {
          fire_c = c;
          fire_ws = prev_ws;
          fire_pass = prev_pass;
        }
      }
      if (!fired && prev_fired) ++fires;   // never falls before a reset
      prev_fired = fired;
      prev_ws = x.d->dbg_r391_ws_o;
      prev_pass = x.d->dbg_r391_pass_o;
      ++c;
    });
    const auto* d = x.d;
    const bool done = b.done >= 0, closed = b.closed >= 0;
    const long term = done ? b.done : (closed ? b.closed : -1);
    const unsigned cause = d->rs_cause_o;
    // the expected path
    std::string why;
    if (term < 0) why += " no-terminal";
    if (fires > 1) why += " fired-twice";
    if (fire_c >= 0) {
      ++fired_n;
      const std::string key = std::string(wname(fire_ws)) + (fire_pass ? "/p1" : "/p0");
      by_state[key]++;
      if (fire_c + 1 < R391_AGG) why += " fired-early";
      if (fire_c + 1 > R391_AGG + 64) why += " fired-late";
      worst_late = std::max(worst_late, fire_c + 1 - R391_AGG);
      const bool closed_path = fire_ws <= 2 || fire_ws == 12 || fire_ws == 13;
      if (closed_path) {
        if (!closed || d->dbg_d3_done_o || !d->dbg_d3_own_o) why += " expected-CLOSED";
      } else if (!fire_pass) {
        if (!done || d->restore_rb_o || closed || cause != 3 || !r.rows_cleared())
          why += " expected-DEFAULTS-p0-cause3";
        if (done && b.done - fire_c > 1) why += " p0-terminal-late";
      } else {
        // pass 1: roll-back, DEFAULTS with rb, or CLOSED if the re-LOCATE fails
        if (!(done && d->restore_rb_o && r.rows_cleared()) && !closed) why += " expected-RB";
        if (term - fire_c > 2 * D3RestorePhase::RS_TMO) why += " rb-unbounded";
        if (cause != 3 && !(scen == 1 && cause == 5)) why += " cause";
      }
    } else if (term >= 0) {
      if (term + 1 > R391_AGG) why += " terminal-past-bound-unfired";
      if (scen == 0 && (!done || d->restore_fail_o)) why += " expected-COMPLETE";
    }
    if (done && d->dbg_d3_own_o) {
      x.idle(200);
      if (d->dbg_d3_own_o) why += " own-after-done";
    }
    // the device face after it: a later SET persists (DEFAULTS/COMPLETE)
    bool set_ok = true;
    if (persist && done) {
      x.nv_gnt_hold = 0;
      x.idle(D3RestorePhase::RS_TMO);
      const size_t o1 = x.nvm_ops.size();
      const uint32_t v = 4000000u + uint32_t(h);
      const bool set = r.ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, v));
      for (long k = 0; k < 2 * D3RestorePhase::WINDOW; ++k) x.step();
      int writes = 0;
      for (size_t i = o1; i < x.nvm_ops.size(); i++)
        writes += x.nvm_ops[i].op == 1 && x.nvm_ops[i].region == 0x50;
      set_ok = set && writes == 1
               && std::equal(x.nv_mem[0x50].begin(), x.nv_mem[0x50].begin() + 12,
                             d3_record(0x50, v, 4).begin());
      if (!set_ok) why += " set-not-persisted";
    }
    if (closed) {
      // the listener still answers in CLOSED
      x.q_acmp.clear();
      x.feed(acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, 0x7777, 0, 0));
      const auto g = x.wait_frame(x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
        return f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == 0x7777;
      });
      if (g.empty()) why += " closed-acmp-silent";
    }
    ++runs;
    if (!why.empty()) ++bad;
    if (!why.empty() || (h % 50) == 0)
      std::printf("R391-P6 scen %d lat %d h %4ld: fire %ld (ws %s pass %u) term %ld %s "
                  "cause %u rb %u own %u%s%s\n",
                  scen, dram_lat, h, fire_c + 1, fire_c >= 0 ? wname(fire_ws) : "-",
                  fire_pass, term + 1, done ? "DONE" : (closed ? "CLOSED" : "NONE"), cause,
                  unsigned(d->restore_rb_o), unsigned(d->dbg_d3_own_o),
                  why.empty() ? "" : " BAD:", why.c_str());
  }
};

static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  D3RestorePhase r{h, image, setup.image_ents};
  R391Sweep s{r};
  for (long hh = 0; hh <= R391_AGG + 100; hh += 1) s.one(0, hh, 31, (hh % 7) == 0);
  for (long hh = 0; hh <= R391_AGG + 100; hh += 1) s.one(1, hh, 143, (hh % 7) == 0);
  std::printf("R391-P6 AGG %ld: %ld runs, %ld fired, %ld BAD; the expiry edge at most %ld "
              "clocks after the bound\n", R391_AGG, s.runs, s.fired_n, s.bad, s.worst_late);
  for (const auto& kv : s.by_state)
    std::printf("R391-P6 fired in %-10s %ld runs\n", kv.first.c_str(), kv.second);
}

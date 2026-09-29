// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-3 P6/P9, strengthened for R391-4 (disposable): the DR3a aggregate expiry swept
// across every state of both walks, graded against the round-3 rule (an
// aggregate expiry never closes a provable image). The probe copy of the wrap
// overrides NVM_RS_AGG_CYC_P with R391_AGG (a few thousand clocks) and taps
// the writer's state and pass and the binding manager's state (dbg_r391_*).
// Shifting the device's first grant by h cycles moves the whole boot against
// the fixed bound, so run by run the expiry lands on every clock of the walks:
// a binding byte in hand, the image proof's own clock, a grant in hand, the
// roll-back. Scenarios:
//   0 every D3 record saved, erased binding records
//   1 as 0, 0x50 erased after pass 0 read it whole (pass 1 aborts, cause 5)
//   2 every binding saved, the device slow per byte (both walks)
//   3 as 2, no image at reset: the writer's own LOCATE proves it
//   4 as 2, the image refused (magic flipped): the LOCATE errs, cause 7
//   5 as 0, the rate rule's AUDIO_UNIT fetch 15,000 clocks late (store
//     watchdog abort, cause 6, a burst owed across the roll-back)
// R391-4 adds to EVERY run: the port must come idle after the terminal (no
// drain, not busy, no owner) within one per-wait deadline of a fast device
// ("port-wedged" otherwise), a count of binding READ strobes that carry the
// abort in their issue clock (the 014e679 case; every such run also grades
// a later SET persisting), and a count of clocks in
// which the D3 writer presents its request and its abort together (claimed 0).
#include <map>
#include <string>
static constexpr long R391_AGG = R391_AGG_VALUE;

struct R391Sweep {
  D3RestorePhase& r;
  H& x;
  long runs = 0, bad = 0, fired_n = 0, worst_late = 0, proof_at_bound = 0;
  long bind_in_hand = 0, bind_failed_by_agg = 0, worst_bind_lat = 0, worst_term_after = 0;
  long set_checks = 0, acmp_checks = 0;
  long port_checks = 0, issue_aborts = 0, issue_abort_runs = 0, m1_both = 0, worst_idle = 0;
  std::map<std::string, long> by_state;
  explicit R391Sweep(D3RestorePhase& rp) : r(rp), x(rp.x) {}

  static const char* wname(unsigned w) {
    static const char* n[] = {"WAITGO", "IMG", "IMGLOC", "RQ", "RD", "RULE", "NCFG", "LOC",
                              "LANE", "JUDGE", "APPLY", "NEXT", "RB", "RELOC", "DONE", "CLOSED"};
    return w < 16 ? n[w] : "?";
  }
  static const char* hname(unsigned s) {
    static const char* n[] = {"INIT", "WAIT", "RS_REQ", "RS_STREAM", "RS_STORE", "RP_RD",
                              "RP_LATCH", "RP_DRIVE", "FIN", "RUN"};
    return s < 10 ? n[s] : "FL";
  }

  void one(int scen, long h, bool deep) {
    const long TMO = D3RestorePhase::RS_TMO;
    x.dram = r.image;
    if (scen == 4) x.dram[0] ^= 0xFF;
    if (scen == 3) x.dram.clear();
    x.dram_silent = false;
    x.dram_lat = (scen == 1) ? 143 : 31;
    x.erase_nvm();
    r.power_cycle();
    if (scen == 3) {
      x.idle(2000);
      x.dram = r.image;
    }
    r.seed_every_record();
    if (scen >= 2 && scen <= 4) {
      r.seed_every_binding();
      x.nv_hdr_every = 2;
      x.nv_byte_every = 5;
    }
    if (scen == 5) {
      x.dram_late_at = r.au_addr;
      x.dram_late_cycles = 15000;
    }
    x.nv_gnt_hold = int(h);
    const size_t ops0 = x.nvm_ops.size();
    bool erased = false;
    long fire_c = -1, fires = 0, agg_rise = -1, bind_end = -1, must_fail_c = -1;
    unsigned fire_ws = 0, fire_pass = 0, prev_ws = 0, prev_pass = 0, rise_hs = 0;
    unsigned ws_at_bound = 99;
    bool prev_fired = false, rise_in_hand = false, bind_failed = false;
    long c = 0;
    long iss_ab = 0;
    const auto b = r.boot_with(R391_AGG + 3 * TMO, [&] {
      const auto* d = x.d;
      if (scen == 1 && !erased && r.reads_of(ops0, 0x50) == 2) {
        std::fill(x.nv_mem[0x50].begin(), x.nv_mem[0x50].begin() + 256, 0xFF);
        erased = true;
      }
      // agg_fired_r rises on the edge that takes the expiry; state and pass
      // sampled one clock earlier are the state the expiry was taken in
      const bool fired = d->dbg_r391_aggf_o;   // the writer's agg_fired_r
      // the binding walk owes the aggregate's path in the first clock after
      // the expiry in which its read phase waits: H_RS_REQ, or H_RS_STREAM
      // with no byte, done or err (the RTL banner's rule)
      const unsigned hs = d->dbg_r391_hs_o;
      if (must_fail_c < 0 && bind_end < 0 && fired
          && (hs == 2 || (hs == 3 && d->dbg_r391_bstall_o)))
        must_fail_c = c;
      if (fired && !prev_fired) {
        ++fires;
        if (fire_c < 0) {
          fire_c = c;
          fire_ws = prev_ws;
          fire_pass = prev_pass;
          agg_rise = c;
          rise_hs = d->dbg_r391_hs_o;
          rise_in_hand = d->dbg_r391_brvalid_o;
        }
      }
      if (!fired && prev_fired) ++fires;
      if (d->dbg_bind_req_o && d->dbg_bind_abort_o) ++iss_ab;
      if (d->dbg_r391_m1both_o) ++m1_both;
      prev_fired = fired;
      if (c + 1 == R391_AGG) ws_at_bound = d->dbg_r391_ws_o;
      prev_ws = d->dbg_r391_ws_o;
      prev_pass = d->dbg_r391_pass_o;
      if (bind_end < 0 && d->dbg_r391_bdone_o) {
        bind_end = c;
        bind_failed = d->dbg_r391_bfail_o;
      }
      ++c;
    });
    x.dram_late_at = 0;
    x.nv_hdr_every = 0;
    x.nv_byte_every = 0;
    const auto* d = x.d;
    const bool done = b.done >= 0, closed = b.closed >= 0;
    const long term = done ? b.done : (closed ? b.closed : -1);
    const unsigned cause = d->rs_cause_o;
    int d3_reads = 0;
    for (size_t i = ops0; i < x.nvm_ops.size(); i++) {
      const auto& o = x.nvm_ops[i];
      d3_reads += (o.op == 0 || o.op == 4) && (o.region < 0x20 || o.region > 0x27);
    }
    const bool provable = scen != 4;
    std::string why;
    if (term < 0) why += " no-terminal";
    if (fires > 1) why += " fired-twice";
    if (term >= 0 && term + 1 > R391_AGG)
      worst_term_after = std::max(worst_term_after, term + 1 - R391_AGG);
    if (fire_c >= 0) {
      ++fired_n;
      const bool pre = fire_ws <= 2;
      std::string key = std::string(wname(fire_ws)) + (fire_pass ? "/p1" : "/p0");
      if (pre) key += std::string(" bind ") + hname(rise_hs) + (rise_in_hand ? "+byte" : "");
      by_state[key]++;
      if (fire_c + 1 < R391_AGG) why += " fired-early";
      if (fire_c + 1 > R391_AGG + 64) why += " fired-late";
      worst_late = std::max(worst_late, fire_c + 1 - R391_AGG);
      if (pre) {
        if (must_fail_c >= 0) {
          ++bind_failed_by_agg;
          if (rise_in_hand && rise_hs == 3) ++bind_in_hand;
          if (bind_end < 0 || !bind_failed || d->restore_cause_o != 3) why += " bind-not-failed";
          if (bind_end >= 0) worst_bind_lat = std::max(worst_bind_lat, bind_end - must_fail_c);
          if (bind_end >= 0 && bind_end - must_fail_c > 2) why += " bind-late";
        }
        if (provable) {
          if (!done || closed || !d->restore_fail_o || cause != 3 || d->restore_rb_o
              || d3_reads != 0 || !r.rows_cleared() || d->dbg_d3_own_o)
            why += " expected-DEFAULTS-proof-cause3";
          if (done && b.done - fire_c > TMO) why += " proof-terminal-late";
        } else if (!closed || done || cause != 7) {
          why += " expected-CLOSED-cause7";
        }
      } else if (fire_ws == 12 || fire_ws == 13) {
        if (!closed || done || !d->dbg_d3_own_o || cause == 3) why += " expected-CLOSED-rb";
      } else if (!fire_pass) {
        if (!done || d->restore_rb_o || closed || cause != 3 || !r.rows_cleared())
          why += " expected-DEFAULTS-p0-cause3";
        if (done && b.done - fire_c > 1) why += " p0-terminal-late";
      } else {
        if (!(done && d->restore_rb_o && r.rows_cleared()) && !closed) why += " expected-RB";
        if (term - fire_c > 2 * TMO) why += " rb-unbounded";
        if (cause != 3) why += " cause";
      }
    } else if (term >= 0 && term + 1 >= R391_AGG) {
      // unfired past the bound: only the proof landing on the bound's own
      // clock (its answer in hand) may end there, DEFAULTS with no record READ
      if (provable && done && cause == 3 && d3_reads == 0 && !d->restore_rb_o
          && (ws_at_bound == 1 || ws_at_bound == 2 || ws_at_bound == 14)) {
        ++proof_at_bound;
        by_state[std::string("unfired proof on the bound clock in ") + wname(ws_at_bound)]++;
      } else if (!provable && closed && cause == 7 && d3_reads == 0) {
        ++proof_at_bound;             // the LOCATE's err on the bound's own clock
        by_state["unfired image refusal on the bound clock"]++;
      } else {
        why += " terminal-past-bound-unfired";
      }
    } else if (term >= 0) {
      const bool ok_early =
          (scen == 4) ? (closed && cause == 7)
        : (scen == 1) ? (done && d->restore_rb_o && cause == 5)
        : (scen == 5) ? ((done && d->restore_rb_o && cause == 6) || (closed && cause == 6))
        : (done && !d->restore_fail_o);
      if (!ok_early) why += " early-terminal";
    }
    if (done) {
      x.idle(200);
      if (x.d->dbg_d3_own_o) why += " own-after-done";
    }
    {
      x.nv_gnt_hold = 0;
      long k = 0;
      for (; k < TMO && (x.d->dbg_nvm_drain_o || x.d->dbg_nvm_busy_o || x.d->dbg_nvm_own_o != 0); ++k)
        x.step();
      ++port_checks;
      worst_idle = std::max(worst_idle, k);
      if (k >= TMO) why += " port-wedged";
      issue_aborts += iss_ab;
      if (iss_ab) ++issue_abort_runs;
    }
    if ((deep || iss_ab) && done) {
      ++set_checks;
      x.nv_gnt_hold = 0;
      x.idle(TMO);
      const size_t o1 = x.nvm_ops.size();
      const uint32_t v = 4000000u + uint32_t(h);
      const bool set = r.ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, v));
      for (long k = 0; k < 2 * D3RestorePhase::WINDOW; ++k) x.step();
      int writes = 0;
      for (size_t i = o1; i < x.nvm_ops.size(); i++)
        writes += x.nvm_ops[i].op == 1 && x.nvm_ops[i].region == 0x50;
      if (!(set && writes == 1
            && std::equal(x.nv_mem[0x50].begin(), x.nv_mem[0x50].begin() + 12,
                          d3_record(0x50, v, 4).begin())))
        why += " set-not-persisted";
    }
    if (deep && closed) {
      ++acmp_checks;
      x.q_acmp.clear();
      x.feed(acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, 0x7777, 0, 0));
      const auto g = x.wait_frame(x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
        return f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == 0x7777;
      });
      if (g.empty()) why += " closed-acmp-silent";
    }
    ++runs;
    if (!why.empty()) ++bad;
    if (!why.empty() || (h % 100) == 0 || iss_ab)
      std::printf("R391-P9 scen %d h %4ld: fire %ld (ws %s pass %u bind %s%s) bind end %ld "
                  "fail %u rcause %u; term %ld %s cause %u rb %u own %u D3 READs %d%s%s%s\n",
                  scen, h, fire_c + 1, fire_c >= 0 ? wname(fire_ws) : "-", fire_pass,
                  hname(rise_hs), rise_in_hand ? "+byte" : "", bind_end + 1,
                  unsigned(bind_failed), unsigned(d->restore_cause_o), term + 1,
                  done ? "DONE" : (closed ? "CLOSED" : "NONE"), cause,
                  unsigned(d->restore_rb_o), unsigned(d->dbg_d3_own_o), d3_reads,
                  iss_ab ? " [issue-cycle abort]" : "", why.empty() ? "" : " BAD:", why.c_str());
  }
};

static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  D3RestorePhase r{h, image, setup.image_ents};
  R391Sweep s{r};
  const long step = R391_STEP;
  for (int scen : {R391_SCENS})
    for (long hh = 0; hh <= R391_AGG + 100; hh += step)
      s.one(scen, hh, (hh % 97) == 0);
  std::printf("R391-P9 AGG %ld scen {%s} step %ld: %ld runs, %ld fired, %ld BAD; expiry edge at "
              "most %ld clocks after the bound; terminal at most %ld clocks after it; %ld proofs "
              "unfired on the bound clock; binding walks failed by the aggregate %ld (%ld with a "
              "byte in hand at agg_o's rise), latest binding end %ld clocks after its first waiting clock under the fired aggregate; %ld later "
              "SETs and %ld CLOSED GET_RX_STATE graded\n",
              R391_AGG, "R391_SCENS_STR", step, s.runs, s.fired_n, s.bad, s.worst_late,
              s.worst_term_after, s.proof_at_bound, s.bind_failed_by_agg, s.bind_in_hand,
              s.worst_bind_lat, s.set_checks, s.acmp_checks);
  std::printf("R391-P9 R391-4 port: %ld runs graded idle after the terminal (longest %ld clocks); "
              "%ld binding READ strobes carried the abort in their issue clock (%ld runs); "
              "%ld clocks with the D3 writer's request and abort together\n",
              s.port_checks, s.worst_idle, s.issue_aborts, s.issue_abort_runs, s.m1_both);
  for (const auto& kv : s.by_state)
    std::printf("R391-P9 fired in %-40s %ld runs\n", kv.first.c_str(), kv.second);
}

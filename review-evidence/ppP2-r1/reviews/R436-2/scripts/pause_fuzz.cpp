// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer-owned randomized probe of KL_pp_nvm_port's deadline count (R436-2).
// Independent of tb/nvm_port: its own device model, its own manager, and its
// own owed-cycle oracle written from the port banner (02 sec. 8), not from owe_w.
//
// Modes (argv[1]):
//   legal  - every device event comes within the bound (a grant at most TMO
//            cycles after the request first shows; a byte or a terminal at
//            most TMO + 1 cycles after the device's previous event, a terminal
//            possibly riding the final byte or an ERASE's grant), strays only
//            where nothing is owned, device errs now and then, manager strobes
//            dropped at random, periodically, or for long stretches. Required:
//            never a DEADLINE, every op answered once, data byte-exact.
//   silent - the device withholds one owed event of the op for ever while the
//            manager drops its strobe at random (never for ever). Required: one
//            err, cause DEADLINE, never done, and the oracle's owed cycles
//            between the device's last event and the pulse equal TMO + 1.
//   resume - a READ, ERASE or WRITE abandoned by a deadline (silent at a byte or
//            at its terminal); the next op starts at once and the device ends
//            the abandoned command r cycles into that op's first owed cycle,
//            then keeps legal pace. Required: served if r <= TMO, one err
//            DEADLINE if r > TMO.
//   babble - an abandoned READ whose device keeps presenting bytes past the
//            command's length, one every TMO / 2 cycles, and never ends it.
//            Reports whether the waiting request is ever answered.
// argv[2] seed, argv[3] ops.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <vector>
#include "VKL_pp_nvm_port.h"
#include "verilated.h"

#ifndef TMO
#error "build with -DTMO=<MEM_TIMEOUT_CYC_P>"
#endif

static int fails = 0;
static long checks = 0;
#define REQUIRE(c, ...) do { ++checks; if (!(c)) { ++fails; if (fails < 40) { \
  printf("FAIL: " __VA_ARGS__); printf("\n"); } } } while (0)

static uint16_t crc16(const std::vector<uint8_t>& b) {
  uint16_t c = 0xFFFF;
  for (uint8_t x : b) {
    c ^= uint16_t(x << 8);
    for (int i = 0; i < 8; ++i) c = (c & 0x8000) ? uint16_t((c << 1) ^ 0x1021) : uint16_t(c << 1);
  }
  return c;
}
static std::vector<uint8_t> frame(uint8_t rec, const std::vector<uint8_t>& pl) {
  std::vector<uint8_t> f = {0x17, 0x22, 0x01, rec, uint8_t(pl.size() >> 8), uint8_t(pl.size())};
  std::vector<uint8_t> cb(f);
  cb.insert(cb.end(), pl.begin(), pl.end());
  uint16_t c = crc16(cb);
  f.push_back(uint8_t(c >> 8)); f.push_back(uint8_t(c));
  f.insert(f.end(), pl.begin(), pl.end());
  return f;
}

enum Obl { O_NONE, O_GNT, O_BYTE, O_TERM };

struct Sim {
  VKL_pp_nvm_port* d;
  std::mt19937_64 rng;
  long cyc = 0;
  std::string mode;
  // ---- device ----
  uint8_t mem[8][2048];
  bool cmd = false; int op = 0, reg = 0, off = 0, len = 0, moved = 0; bool dphase = false;
  long req_at = -1; int req_wait = 0;
  long next_at = 0;       // earliest cycle of the next byte / terminal
  long last_evt = -1;     // cycle of the device's last event
  bool err_next = false;  // the next event is an err instead
  // silence: withhold the n-th obligation of this op (counted 0..), or never
  int sil_n = -1, obl_n = 0; bool silent = false;
  bool babble = false; int babble_every = 0;
  bool hold_dev = false;  // resume mode: device holds every event until released
  long stray_block = 0;
  // ---- manager ----
  int m = 0;              // 0 idle, 1 commit, 2 restore
  std::vector<uint8_t> w, r; size_t wi = 0;
  int pat = 0; double p = 0; int per = 1; long hold_until = 0;
  // ---- capture ----
  int dones = 0, errs = 0, cause = -1; bool busy_at_pulse = false; long pulse_at = -1;
  long owed_since_evt = 0; bool owed_last = false; long owed_at_pulse = -1;
  long deadlines = 0, held = 0;
  bool trace = false;

  int rnd(int lo, int hi) { return std::uniform_int_distribution<int>(lo, hi)(rng); }
  double u() { return std::uniform_real_distribution<double>(0, 1)(rng); }
  int pick_wait(int maxw) {   // biased to the edges
    double x = u();
    if (x < 0.35) return maxw;
    if (x < 0.5) return 0;
    return rnd(0, maxw);
  }

  explicit Sim(VKL_pp_nvm_port* dut, uint64_t seed, const std::string& md)
      : d(dut), rng(seed), mode(md) { memset(mem, 0xFF, sizeof mem); }

  bool strobe() {
    if (cyc < hold_until) return false;
    switch (pat) {
      case 0: return true;
      case 1: return u() >= p;
      case 2: return (cyc % per) != 0;
      default:
        if (u() < 0.01) { hold_until = cyc + rnd(1, 5 * TMO + 3); return false; }
        return u() >= p;
    }
  }
  void new_pattern(bool may_hold) {
    pat = rnd(0, may_hold ? 3 : 2);
    double ps[] = {0.1, 0.5, 0.9};
    p = ps[rnd(0, 2)];
    per = rnd(2, 2 * TMO + 3);
  }

  // the oracle: does the device owe the port an event this cycle? Written from
  // the banner: a grant while a request is up; while it carries a command, a
  // byte the port presents (WRITE) or is ready for (READ), or the terminal of a
  // command whose data phase is over. Only while an operation is in flight.
  bool oracle_owed() const {
    if (!d->nvm_busy_o) return false;
    if (d->dev_req_o) return true;
    if (!cmd) return false;
    if (dphase) return op == 1 ? bool(d->dev_wvalid_o) : bool(d->dev_rready_o);
    return true;
  }

  void tick() {
    // manager drive
    bool s = strobe();
    if (m == 1) {
      bool v = wi < w.size() && s;
      d->nvm_wvalid_i = v; d->nvm_wdata_i = v ? w[wi] : 0; d->nvm_rready_i = 0;
      if (!v && wi < w.size()) ++held;
    } else if (m == 2) {
      d->nvm_wvalid_i = 0; d->nvm_rready_i = s;
      if (!s) ++held;
    } else {
      d->nvm_wvalid_i = 0; d->nvm_rready_i = 0;
    }
    d->dev_gnt_i = 0; d->dev_done_i = 0; d->dev_err_i = 0; d->dev_wready_i = 0;
    d->dev_rvalid_i = 0; d->dev_rdata_i = 0; d->dev_busy_i = cmd;
    d->clk_i = 0; d->eval();

    // device decides on what the port shows now
    bool gnt = false, done = false, err = false, wr = false, rv = false, took = false;
    bool owed_now = oracle_owed();
    bool stray = false;
    bool this_obl_silent = false;
    if (!cmd) {
      if (d->dev_req_o) {
        if (req_at < 0) { req_at = cyc; req_wait = pick_wait(TMO); }
        this_obl_silent = silent || (sil_n >= 0 && obl_n == sil_n);
        if (!this_obl_silent && !hold_dev && cyc - req_at >= req_wait) {
          if (err_next) { err = true; err_next = false; }
          else gnt = true;
        }
      } else {
        req_at = -1;
      }
      // a done that belongs to nobody, never near a real event
      if (!gnt && !err && cyc > stray_block && !babble && u() < 0.02) stray = true;
    } else if (dphase) {
      this_obl_silent = silent || (sil_n >= 0 && obl_n == sil_n);
      bool ready = !this_obl_silent && !hold_dev && cyc >= next_at;
      if (ready && err_next) { err = true; }
      else if (op == 1) wr = ready;
      else if (ready || (babble && cyc >= next_at)) rv = true;
    } else {
      this_obl_silent = silent || (sil_n >= 0 && obl_n == sil_n);
      if (!babble && !this_obl_silent && !hold_dev && cyc >= next_at) {
        if (err_next) err = true; else done = true;
      }
      if (babble && cyc >= next_at) rv = true;   // bytes past the command's length
    }
    d->dev_gnt_i = gnt; d->dev_err_i = err; d->dev_wready_i = wr; d->dev_rvalid_i = rv;
    if (rv) d->dev_rdata_i = (babble && !dphase) ? 0x5A : mem[reg][(off + moved) % 2048];
    d->eval();
    // a terminal riding the final byte or an ERASE's grant, decided once the
    // handshake shows, never where the terminal is the withheld obligation
    const bool term_free = !(sil_n >= 0 && obl_n + 1 == sil_n) && !hold_dev && !babble
                           && !err_next && !silent;
    bool wx = wr && d->dev_wvalid_o, rx = rv && d->dev_rready_o;
    bool cdone = false;
    if (cmd && dphase && (wx || rx) && moved + 1 == len && !err && term_free && u() < 0.5) {
      done = true; cdone = true;
    }
    bool gdone = false;
    if (gnt && int(d->dev_op_o) == 2 && term_free && u() < 0.4) { done = true; gdone = true; }
    if (stray) done = true;
    d->dev_done_i = done;
    d->eval();

    // pre-edge sampling
    bool evt = gnt || err || wx || rx || (done && !stray);
    if (d->nvm_done_o || d->nvm_err_o) {
      if (d->nvm_done_o) ++dones;
      if (d->nvm_err_o) { ++errs; cause = d->nvm_err_cause_o; if (cause == 3) ++deadlines; }
      busy_at_pulse = d->nvm_busy_o; if (pulse_at < 0) { pulse_at = cyc; owed_at_pulse = owed_since_evt; }
    }
    if (owed_now && !evt) ++owed_since_evt;
    if (evt) owed_since_evt = 0;
    owed_last = owed_now;
    // manager transfers
    if (m == 1 && d->nvm_wvalid_i && d->nvm_wready_o) ++wi;
    if (m == 2 && d->nvm_rvalid_o && d->nvm_rready_i) r.push_back(d->nvm_rdata_o);
    const bool req_was_up = d->nvm_req_i;

    // device state after the edge
    if (gnt) {
      cmd = true; op = d->dev_op_o; reg = d->dev_region_o % 8; off = d->dev_offset_o;
      len = d->dev_len_o; moved = 0; req_at = -1; ++obl_n;
      if (op == 2) { memset(mem[reg], 0xFF, 2048); dphase = false; }
      else dphase = len > 0;
      next_at = cyc + 1 + pick_wait(TMO);
      if (gdone) { cmd = false; ++obl_n; }
      stray_block = cyc + 2;
    }
    if (wx) { mem[reg][(off + moved) % 2048] = d->dev_wdata_o; }
    if (wx || (rx && dphase)) {
      ++moved; ++obl_n;
      if (moved == len) { dphase = false; if (cdone) { cmd = false; ++obl_n; } }
      next_at = cyc + 1 + (babble ? babble_every : pick_wait(TMO));
      stray_block = cyc + 2;
    } else if (rx && babble) {
      next_at = cyc + 1 + babble_every;
    }
    if ((done && !stray && !gdone && !cdone && cmd && !dphase) || err) {
      cmd = false; dphase = false; ++obl_n; stray_block = cyc + 2;
      if (err) err_next = false;
    }
    if (evt) last_evt = cyc;
    if (trace) printf("c%ld req%d gnt%d op%d len%d wv%d wr%d rv%d rr%d done%d err%d | nreq%d we%d busy%d nwv%d nwr%d nrv%d nrr%d nd%d ne%d cause%d | cmd%d dph%d moved%d obl%d owed%d o%ld\n",
        cyc, d->dev_req_o, gnt, d->dev_op_o, d->dev_len_o, d->dev_wvalid_o, wr, rv, d->dev_rready_o, done, err,
        d->nvm_req_i, d->nvm_we_i, d->nvm_busy_o, d->nvm_wvalid_i, d->nvm_wready_o, d->nvm_rvalid_o, d->nvm_rready_i,
        d->nvm_done_o, d->nvm_err_o, d->nvm_err_cause_o, cmd, dphase, moved, obl_n, owed_now, owed_since_evt);
    d->clk_i = 1; d->eval();
    if (req_was_up) d->nvm_req_i = 0;   // one cycle, sampled at this edge
    ++cyc;
  }

  void reset_all() {
    d->rst_n = 0; d->nvm_req_i = 0;
    for (int i = 0; i < 4; ++i) tick();
    d->rst_n = 1;
    cmd = false; dphase = false; req_at = -1; silent = false; sil_n = -1; babble = false;
    hold_dev = false; err_next = false; m = 0;
    tick();
  }

  void start(bool we, uint8_t rec, const std::vector<uint8_t>& f) {
    while (d->nvm_busy_o || d->nvm_done_o || d->nvm_err_o) tick();
    dones = errs = 0; cause = -1; pulse_at = -1; owed_at_pulse = -1; owed_since_evt = 0;
    held = 0; obl_n = 0;
    m = we ? 1 : 2; w = f; wi = 0; r.clear();
    d->nvm_req_i = 1; d->nvm_we_i = we; d->nvm_record_id_i = rec;
  }
  // run to the pulse (plus a drain); false if no pulse within the guard
  bool finish(long guard) {
    for (long i = 0; i < guard; ++i) {
      tick();
      if (pulse_at >= 0) { for (int k = 0; k < 3; ++k) tick(); m = 0; return true; }
    }
    m = 0;
    return false;
  }
};

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  std::string mode = argc > 1 ? argv[1] : "legal";
  uint64_t seed = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1;
  int nops = argc > 3 ? atoi(argv[3]) : 2000;
  auto* dut = new VKL_pp_nvm_port;
  Sim s(dut, seed, mode);
  s.reset_all();
  std::vector<std::vector<uint8_t>> good(8);   // the record each region holds, if known
  const long guard = 200L * (TMO + 10) * 80;
  int served = 0, dl_branch = 0, babble_answered = 0;

  const char* tr = getenv("FUZZ_TRACE_OP");
  for (int n = 0; n < nops; ++n) {
    s.trace = tr && atoi(tr) == n;
    uint8_t rec = uint8_t(s.rnd(0, 7));
    bool we = good[rec].empty() || s.u() < 0.5;
    std::vector<uint8_t> pl(size_t(s.rnd(0, 24)));
    for (auto& b : pl) b = uint8_t(s.rnd(0, 255));
    std::vector<uint8_t> f = we ? frame(rec, pl) : good[rec];

    if (mode == "legal") {
      s.new_pattern(true);
      s.err_next = s.u() < 0.04;
      bool will_err = s.err_next;
      s.start(we, rec, f);
      bool ok = s.finish(guard);
      REQUIRE(ok, "legal op %d (%s rec %d) never answered", n, we ? "commit" : "restore", rec);
      REQUIRE(s.dones + s.errs == 1, "legal op %d answered %d times", n, s.dones + s.errs);
      REQUIRE(!s.busy_at_pulse, "legal op %d busy at the pulse", n);
      REQUIRE(!(s.errs && s.cause == 3), "legal op %d refused DEADLINE (%s, %zu bytes, pattern %d)",
              n, we ? "commit" : "restore", f.size(), s.pat);
      if (s.errs) {
        REQUIRE(s.cause == 1, "legal op %d err cause %d, want DEVICE", n, s.cause);
        REQUIRE(will_err, "legal op %d err with no device err armed", n);
        if (we) good[rec].clear();
        s.err_next = false;
        // a device err mid-command may leave it carried: start clean
        if (s.cmd) s.reset_all();
      } else {
        REQUIRE(!will_err || !s.err_next, "legal op %d done although an err was armed and given", n);
        s.err_next = false;
        if (we) {
          bool eq = true;
          for (size_t i = 0; i < f.size(); ++i) eq = eq && s.mem[rec][i] == f[i];
          REQUIRE(eq, "legal op %d commit not byte-exact", n);
          good[rec] = f;
        } else {
          REQUIRE(s.r == f, "legal op %d restore not byte-exact (%zu of %zu)", n, s.r.size(), f.size());
        }
      }
      if (s.cmd) s.reset_all();
    } else if (mode == "silent") {
      s.new_pattern(false);
      // obligations of an op: commit = gnt(E) term(E) gnt(W) 8+plen bytes term(W);
      // restore = gnt term? no: gnt(H) 8 bytes term(H) gnt(P) plen bytes term(P)
      int nobl = we ? (2 + 1 + int(f.size()) + 1) : (1 + 8 + 1 + (f.size() > 8 ? 1 + int(f.size()) - 8 + 1 : 0));
      s.sil_n = s.rnd(0, nobl - 1);
      s.start(we, rec, f);
      bool ok = s.finish(guard);
      REQUIRE(ok, "silent op %d (%s, silent at obligation %d of %d, pattern %d) never answered",
              n, we ? "commit" : "restore", s.sil_n, nobl, s.pat);
      REQUIRE(s.dones == 0 && s.errs == 1 && s.cause == 3,
              "silent op %d: %d done %d err cause %d, want one err DEADLINE (obl %d of %d)",
              n, s.dones, s.errs, s.cause, s.sil_n, nobl);
      REQUIRE(s.owed_at_pulse == TMO + 1,
              "silent op %d: %ld owed cycles between the device's last event and the pulse, "
              "want %d (obl %d of %d, %s, pattern %d, held %ld)",
              n, s.owed_at_pulse, TMO + 1, s.sil_n, nobl, we ? "commit" : "restore", s.pat, s.held);
      good[rec].clear();
      s.reset_all();
      // re-commit a record so restores stay possible, on a prompt device
      s.sil_n = -1; s.pat = 0;
      std::vector<uint8_t> g = frame(rec, pl);
      s.start(true, rec, g);
      bool gok = s.finish(guard);
      REQUIRE(gok && s.dones == 1, "silent refill %d not served", n);
      if (gok && s.dones == 1) good[rec] = g;
      if (s.cmd) s.reset_all();
    } else if (mode == "resume" || mode == "babble") {
      // abandon a command: silent at a byte or a terminal of a restore or commit
      if (good[rec].empty()) {
        s.pat = 0; s.start(true, rec, frame(rec, pl)); s.finish(guard); good[rec] = frame(rec, pl);
        continue;
      }
      bool ab_we = mode == "babble" ? false : (s.u() < 0.4);
      std::vector<uint8_t> af = ab_we ? frame(rec, pl) : good[rec];
      int nobl = ab_we ? (2 + 1 + int(af.size()) + 1)
                       : (1 + 8 + 1 + (af.size() > 8 ? 1 + int(af.size()) - 8 + 1 : 0));
      // choose an obligation that leaves a command carried: not a grant
      int pick;
      for (;;) {
        pick = s.rnd(0, nobl - 1);
        bool is_gnt = ab_we ? (pick == 0 || pick == 2)
                            : (pick == 0 || (af.size() > 8 && pick == 10));
        // a WRITE abandoned mid-data is contained, not resumable: keep its terminal only
        bool wr_data = ab_we && pick >= 3 && pick < 3 + int(af.size());
        if (!is_gnt && !wr_data) break;
      }
      if (mode == "babble") {
        // a payload byte of the READ, so bytes are still to come
        if (af.size() <= 9) { continue; }
        pick = 11 + s.rnd(0, int(af.size()) - 10);
      }
      s.pat = 0;
      s.sil_n = pick;
      s.start(ab_we, rec, af);
      bool ok = s.finish(guard);
      REQUIRE(ok && s.errs == 1 && s.cause == 3, "resume setup %d: no DEADLINE", n);
      if (!s.cmd) { s.reset_all(); continue; }      // nothing carried after all
      s.sil_n = -1;
      // the next op, at once; the device holds until that op's first owed cycle
      uint8_t rec2 = uint8_t((rec + 1 + s.rnd(0, 6)) % 8);
      bool we2 = good[rec2].empty() || s.u() < 0.5;
      std::vector<uint8_t> pl2(size_t(s.rnd(0, 24)));
      for (auto& b : pl2) b = uint8_t(s.rnd(0, 255));
      std::vector<uint8_t> f2 = we2 ? frame(rec2, pl2) : good[rec2];
      s.new_pattern(false);
      s.hold_dev = true;
      s.start(we2, rec2, f2);
      // first owed cycle of the new op: a restore's first busy cycle; a commit's
      // first cycle after its 8 header bytes
      long first = -1;
      for (long i = 0; i < guard && first < 0; ++i) {
        s.tick();
        if (s.d->nvm_busy_o && (!we2 || s.wi >= 8)) first = s.cyc;
      }
      int rr;
      if (mode == "babble") {
        rr = 0; s.babble = true; s.babble_every = TMO / 2;
      } else {
        rr = s.pick_wait(2 * TMO + 2);
      }
      // release the device rr cycles into the first owed cycle (rr = 0: on it)
      for (long i = 0; i < rr - 1 && s.pulse_at < 0; ++i) s.tick();
      s.next_at = s.cyc + (rr > 0 ? 1 : 0);
      s.hold_dev = false;
      if (mode == "babble") {
        bool answered = s.finish(400L * TMO);
        if (answered) ++babble_answered;
        s.babble = false;
        s.reset_all();
        good[rec2].clear(); good[rec].clear();
        continue;
      }
      ok = s.finish(guard);
      REQUIRE(ok, "resume op %d never answered (r %d)", n, rr);
      if (rr <= TMO) {
        REQUIRE(s.errs == 0 && s.dones == 1, "resume op %d: the device ended the abandoned command "
                "%d cycles into the wait (bound %d), yet the op was not served (%d err, cause %d)",
                n, rr, TMO, s.errs, s.cause);
        if (s.dones == 1) {
          ++served;
          if (we2) good[rec2] = f2; else REQUIRE(s.r == f2, "resume op %d restore not byte-exact", n);
        }
      } else {
        REQUIRE(s.errs == 1 && s.cause == 3 && s.dones == 0,
                "resume op %d: %d cycles into the wait (bound %d), want one err DEADLINE "
                "(%d done, %d err, cause %d)", n, rr, TMO, s.dones, s.errs, s.cause);
        if (s.errs == 1) ++dl_branch;
      }
      if (we2 && s.errs) good[rec2].clear();
      if (ab_we) good[rec].clear();
      s.reset_all();
    }
  }
  printf("pause_fuzz TMO=%d mode=%s seed=%llu ops=%d cycles=%ld deadlines=%ld served=%d "
         "dl_branch=%d babble_answered=%d\n",
         TMO, mode.c_str(), (unsigned long long)seed, nops, s.cyc, s.deadlines, served, dl_branch,
         babble_answered);
  printf("%ld checks: %ld PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

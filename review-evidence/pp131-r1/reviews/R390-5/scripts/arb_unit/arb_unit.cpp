// Reviewer unit probe (R390-4) of KL_pp_nvm_mgr_arb alone: every way an abort
// can meet a strobe in the arbiter's issue cycle, and the owned-READ path.
// The port is modelled here: it takes a request only when idle, a READ
// offers NB bytes (each moves on rready) then a one-cycle done; a WRITE takes
// NB bytes (each on wvalid) then a one-cycle done; after the done it is idle
// in the next cycle, as KL_pp_nvm_port's S_IDLE follows its pulse.
#include "Varb.h"
#include "verilated.h"
#include <cstdio>
#include <string>

static Varb* d;
static long cyc = 0;
static int checks = 0, fails = 0;

// port model
static int p_state = 0;   // 0 idle, 1 read, 2 write, 3 done pulse
static int p_left = 0;
static const int NB = 5;

struct Obs {
  int m0_rv = 0, m1_rv = 0, m0_done = 0, m1_done = 0, m0_wr = 0, m1_wr = 0;
  int drain_cycles = 0, issued = 0, issue_we = -1, first_drain = -1, issue_cyc = -1;
  long ended = -1;
  int m1_gnt = 0;
};

static void check(bool ok, const std::string& what) {
  ++checks;
  if (!ok) ++fails;
  printf("%s: %s\n", ok ? "PASS" : "FAIL", what.c_str());
}

// one clock: drive the port model's outputs from its state, settle, sample,
// then advance state on the edge
static void tick(Obs& o, bool m0_req, bool m0_we, bool m0_abort, bool m1_req, bool m1_we,
                 bool m1_abort, bool m0_rr, bool m1_rr) {
  d->m0_req_i = m0_req; d->m0_we_i = m0_we; d->m0_abort_i = m0_abort;
  d->m1_req_i = m1_req; d->m1_we_i = m1_we; d->m1_abort_i = m1_abort;
  d->m0_rready_i = m0_rr; d->m1_rready_i = m1_rr;
  d->m0_wvalid_i = 1; d->m1_wvalid_i = 1; d->m0_wdata_i = 0xA0; d->m1_wdata_i = 0xB0;
  d->m0_rid_i = 0x20; d->m1_rid_i = 0x50;
  d->p_busy_i = (p_state == 1 || p_state == 2);
  d->p_rvalid_i = (p_state == 1 && p_left > 0);
  d->p_rdata_i = 0x5A;
  d->p_wready_i = (p_state == 2 && p_left > 0);
  d->p_done_i = (p_state == 3);
  d->p_err_i = 0; d->p_err_cause_i = 0;
  d->clk_i = 0; d->eval();
  // sample
  if (d->m1_gnt_o) ++o.m1_gnt;
  if (d->m0_rvalid_o && d->m0_rready_i) ++o.m0_rv;
  if (d->m1_rvalid_o && d->m1_rready_i) ++o.m1_rv;
  if (d->m0_done_o) ++o.m0_done;
  if (d->m1_done_o) ++o.m1_done;
  if (d->m0_wready_o) ++o.m0_wr;
  if (d->m1_wready_o) ++o.m1_wr;
  if (d->dbg_drain_o) { ++o.drain_cycles; if (o.first_drain < 0) o.first_drain = cyc; }
  if (d->p_done_i && o.ended < 0 && o.issued) o.ended = cyc;
  // port state advance
  int nxt = p_state;
  if (p_state == 0 && d->p_req_o) {
    ++o.issued; o.issue_we = d->p_we_o; o.issue_cyc = cyc;
    nxt = d->p_we_o ? 2 : 1; p_left = NB;
  } else if (p_state == 1) {
    if (p_left > 0 && d->p_rready_o) --p_left;
    if (p_left == 0) nxt = 3;
  } else if (p_state == 2) {
    if (p_left > 0 && d->p_wvalid_o) --p_left;
    if (p_left == 0) nxt = 3;
  } else if (p_state == 3) {
    nxt = 0;                     // S_IDLE follows the pulse
  }
  d->clk_i = 1; d->eval();
  p_state = nxt;
  ++cyc;
}

static void reset() {
  p_state = 0; p_left = 0;
  Obs o;
  d->rst_n = 0;
  for (int i = 0; i < 3; i++) tick(o, 0, 0, 0, 0, 0, 0, 0, 0);
  d->rst_n = 1;
}

// run a case: one issue-cycle presentation, then `cycles` more with the
// managers' later behaviour given by the flags
struct Case {
  const char* name;
  bool m0_req, m0_we, m0_abort, m1_req, m1_we, m1_abort;  // in the issue cycle
  bool m0_rr_after, m1_rr_after;                           // rready from the next cycle
  bool m1_holds_req;                                       // manager 1 holds until granted
};

static Obs run_case(const Case& c, int cycles = 40) {
  reset();
  Obs o;
  tick(o, c.m0_req, c.m0_we, c.m0_abort, c.m1_req, c.m1_we, c.m1_abort, 0, 0);
  for (int i = 0; i < cycles; i++) {
    const bool m1r = c.m1_holds_req && c.m1_req && o.m1_gnt == 0;
    tick(o, 0, 0, 0, m1r, c.m1_we, 0, c.m0_rr_after, c.m1_rr_after);
  }
  return o;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = new Varb;
  char b[512];
  // A. manager 0 READ strobe with its own abort, in the issue cycle: drained
  {
    Obs o = run_case({"A", 1, 0, 1, 0, 0, 0, false, false, false});
    snprintf(b, sizeof b, "A m0 READ strobe + m0 abort in the issue cycle: issued %d, drain from issue+%ld, "
             "%d drain cycles, m0 took %d bytes %d dones, port ended %d, idle after %d",
             o.issued, (o.first_drain < 0 ? -1L : o.first_drain - o.issue_cyc), o.drain_cycles, o.m0_rv, o.m0_done,
             o.ended >= 0, p_state == 0);
    check(o.issued == 1 && o.issue_we == 0 && o.first_drain == o.issue_cyc + 1 && o.m0_rv == 0
              && o.m0_done == 0 && o.ended >= 0 && p_state == 0 && !d->dbg_drain_o, b);
  }
  // B. manager 0 WRITE strobe with an abort: an abort never cuts a write
  {
    Obs o = run_case({"B", 1, 1, 1, 0, 0, 0, false, false, false});
    snprintf(b, sizeof b, "B m0 WRITE strobe + m0 abort: issued we %d, %d drain cycles, m0 wready %d, "
             "m0 done %d", o.issue_we, o.drain_cycles, o.m0_wr, o.m0_done);
    check(o.issued == 1 && o.issue_we == 1 && o.drain_cycles == 0 && o.m0_wr == NB && o.m0_done == 1, b);
  }
  // C. manager 1 READ granted with its own abort in the grant cycle: drained
  {
    Obs o = run_case({"C", 0, 0, 0, 1, 0, 1, false, false, true});
    snprintf(b, sizeof b, "C m1 READ grant + m1 abort in the issue cycle: drain from issue+%ld, %d drain "
             "cycles, m1 took %d bytes %d dones, idle after %d", (o.first_drain < 0 ? -1L : o.first_drain - o.issue_cyc),
             o.drain_cycles, o.m1_rv, o.m1_done, p_state == 0);
    check(o.issued == 1 && o.issue_we == 0 && o.first_drain == o.issue_cyc + 1 && o.m1_rv == 0
              && o.m1_done == 0 && p_state == 0 && !d->dbg_drain_o, b);
  }
  // D. manager 1 WRITE granted with an abort: not cut
  {
    Obs o = run_case({"D", 0, 0, 0, 1, 1, 1, false, false, true});
    snprintf(b, sizeof b, "D m1 WRITE grant + m1 abort: %d drain cycles, m1 wready %d, m1 done %d",
             o.drain_cycles, o.m1_wr, o.m1_done);
    check(o.issued == 1 && o.issue_we == 1 && o.drain_cycles == 0 && o.m1_wr == NB && o.m1_done == 1, b);
  }
  // E. manager 0 READ strobe while manager 1 presents an abort (a different
  // intent): manager 0's READ is served, never drained
  {
    Obs o = run_case({"E", 1, 0, 0, 0, 0, 1, true, false, false});
    snprintf(b, sizeof b, "E m0 READ strobe + m1 abort only: %d drain cycles, m0 took %d bytes %d dones",
             o.drain_cycles, o.m0_rv, o.m0_done);
    check(o.issued == 1 && o.drain_cycles == 0 && o.m0_rv == NB && o.m0_done == 1, b);
  }
  // F. manager 1 READ grant while manager 0 presents an abort without a strobe
  {
    Obs o = run_case({"F", 0, 0, 1, 1, 0, 0, false, true, true});
    snprintf(b, sizeof b, "F m1 READ grant + m0 abort only: %d drain cycles, m1 took %d bytes %d dones",
             o.drain_cycles, o.m1_rv, o.m1_done);
    check(o.issued == 1 && o.drain_cycles == 0 && o.m1_rv == NB && o.m1_done == 1, b);
  }
  // G. a tie at an idle port, manager 1 presenting its abort: manager 0 wins
  // and its READ is served; manager 1 is granted later with no abort and served
  {
    Obs o = run_case({"G", 1, 0, 0, 1, 0, 1, true, true, true}, 60);
    snprintf(b, sizeof b, "G tie, m0 READ strobe, m1 READ req + m1 abort: %d issued, %d drain cycles, "
             "m0 %d bytes %d dones, m1 %d bytes %d dones", o.issued, o.drain_cycles, o.m0_rv,
             o.m0_done, o.m1_rv, o.m1_done);
    check(o.issued == 2 && o.drain_cycles == 0 && o.m0_rv == NB && o.m0_done == 1 && o.m1_rv == NB
              && o.m1_done == 1, b);
  }
  // H. a manager 0 READ served normally, abort in its third owned cycle
  // (the head's owned path, unchanged): drained from the next clock
  {
    reset();
    Obs o;
    tick(o, 1, 0, 0, 0, 0, 0, 0, 0);
    tick(o, 0, 0, 0, 0, 0, 0, 1, 0);
    tick(o, 0, 0, 1, 0, 0, 0, 1, 0);
    long ab = cyc - 1;
    for (int i = 0; i < 40; i++) tick(o, 0, 0, 0, 0, 0, 0, 0, 0);
    snprintf(b, sizeof b, "H m0 READ, abort while owned: drain from abort+%ld, m0 took %d bytes %d dones, "
             "idle after %d", (o.first_drain < 0 ? -1L : o.first_drain - ab), o.m0_rv, o.m0_done, p_state == 0);
    check(o.first_drain == ab + 1 && o.m0_done == 0 && p_state == 0 && !d->dbg_drain_o, b);
  }
  // I. no strobe, no owner: an abort alone arms nothing
  {
    reset();
    Obs o;
    tick(o, 0, 0, 1, 0, 0, 1, 0, 0);
    for (int i = 0; i < 5; i++) tick(o, 0, 0, 0, 0, 0, 0, 0, 0);
    snprintf(b, sizeof b, "I both aborts with no strobe and no owner: %d drain cycles, issued %d",
             o.drain_cycles, o.issued);
    check(o.drain_cycles == 0 && o.issued == 0, b);
  }
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete d;
  return fails ? 1 : 0;
}

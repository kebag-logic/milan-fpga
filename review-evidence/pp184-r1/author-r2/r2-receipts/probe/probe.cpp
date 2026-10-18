// Standalone KL_srp_domain probe: the re-join encoding boundary documented in
// docs/architecture/10_srp_engine.md section 6.1 (snapshot at enqueue, kept until the
// encoder accepts it, enqueue-edge receive, no fixed drain bound). Expected values
// come from that text, not from the RTL.
#include "VKL_srp_domain.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>

static VKL_srp_domain* d;
static int fails = 0, passes = 0;
static void check(bool ok, const char* what) {
  std::printf("%s: %s\n", ok ? "PASS" : "FAIL", what);
  ok ? ++passes : ++fails;
}
static void clear_strobes() {
  d->rxdom_valid_i = 0; d->rxdom_lv_i = 0;
  d->periodic_tick_i = 0; d->leaveall_tick_i = 0; d->tx_tick_i = 0;
}
static void tick() {  // one core clock: inputs as set, then strobes cleared
  d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); clear_strobes();
}
static void rx(bool lv, unsigned prio, unsigned vid) {  // a received {6, prio, vid} vector
  d->rxdom_class_id_i = 6; d->rxdom_prio_i = prio; d->rxdom_vid_i = vid; d->rxdom_nov_i = 1;
  if (lv) d->rxdom_lv_i = 1; else d->rxdom_valid_i = 1;
}
static void reset_up() {
  clear_strobes(); d->rst_n = 0; d->link_up_i = 0; d->dom_ev_ready_i = 1;
  for (int i = 0; i < 4; ++i) tick();
  d->rst_n = 1; tick(); d->link_up_i = 1;
  for (int i = 0; i < 4; ++i) tick();  // New queued at link rise and accepted
}
static int queued_event() { return d->dom_ev_valid_o ? d->dom_ev_event_o : -1; }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = new VKL_srp_domain;
  const int JOININ = 1, JOINMT = 3;

  // B1: the queued code is the previously registered state; it survives a peer Lv
  // received while the encoder holds ready low, and the next fresh re-join is JoinMt.
  reset_up(); rx(false, 3, 2); tick();               // peer JoinIn {6,3,2}: IN
  d->dom_ev_ready_i = 0; d->periodic_tick_i = 1; tick(); tick();
  check(queued_event() == JOININ, "B1a registered: the queued re-join is JoinIn");
  rx(true, 3, 2); tick();
  for (int i = 0; i < 8; ++i) tick();
  check(queued_event() == JOININ, "B1b a peer Lv while it waits leaves the queued JoinIn");
  d->dom_ev_ready_i = 1; tick();
  check(queued_event() == -1, "B1c the encoder accepts the queued event");
  d->periodic_tick_i = 1; d->dom_ev_ready_i = 0; tick(); tick();
  check(queued_event() == JOINMT, "B1d the next fresh re-join after the Lv is JoinMt");
  d->dom_ev_ready_i = 1; tick();

  // B2: the inverse: a queued JoinMt survives a registering peer event while it waits.
  reset_up();
  d->dom_ev_ready_i = 0; d->periodic_tick_i = 1; tick(); tick();
  check(queued_event() == JOINMT, "B2a no registration: the queued re-join is JoinMt");
  rx(false, 3, 2); tick();
  for (int i = 0; i < 8; ++i) tick();
  check(queued_event() == JOINMT, "B2b a peer JoinIn while it waits leaves the queued JoinMt");
  d->dom_ev_ready_i = 1; tick();
  d->periodic_tick_i = 1; d->dom_ev_ready_i = 0; tick(); tick();
  check(queued_event() == JOININ, "B2c the next fresh re-join after the JoinIn is JoinIn");
  d->dom_ev_ready_i = 1; tick();

  // B3: a peer Lv on the enqueue edge: the enqueue uses the previous registered state,
  // and the registrar is updated for the subsequent re-join.
  reset_up(); rx(false, 3, 2); tick();
  d->dom_ev_ready_i = 0; d->periodic_tick_i = 1; tick();   // pending; enqueue on next edge
  check(queued_event() == -1, "B3a the re-join is pending, not yet queued");
  rx(true, 3, 2); tick();                                  // the enqueue edge
  check(queued_event() == JOININ, "B3b an Lv on the enqueue edge: queued JoinIn");
  d->dom_ev_ready_i = 1; tick();
  d->periodic_tick_i = 1; d->dom_ev_ready_i = 0; tick(); tick();
  check(queued_event() == JOINMT, "B3c the subsequent re-join is JoinMt");
  d->dom_ev_ready_i = 1; tick();

  // B4: backpressure extends the wait: no fixed drain bound while ready stays low.
  reset_up(); d->dom_ev_ready_i = 0; d->periodic_tick_i = 1; tick(); tick();
  int held = 0;
  for (int i = 0; i < 200000; ++i) { tick(); if (queued_event() == JOINMT) ++held; }
  check(held == 200000, "B4 the queued re-join waits 200000 clocks while ready stays low");
  d->dom_ev_ready_i = 1; tick();
  check(queued_event() == -1, "B4b and is accepted once ready rises");

  std::printf("probe: %d PASS, %d FAIL\n", passes, fails);
  delete d;
  return fails ? 1 : 0;
}

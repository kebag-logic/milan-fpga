// Independent reviewer bench for KL_srp_domain (issue #184 review).
// Expected encodings are taken from IEEE 802.1Q-2018 10.7.6.3 (sJ: JoinIn
// while the Registrar is IN, JoinMt in MT or LV), Table 10-4 (rNew/rJoinIn/
// rJoinMt register; rLA!/txLA! IN -> LV) and Milan v1.2 4.2.7.2.2 (rLv!:
// IN -> MT at once), not from the RTL. "OBS" lines record design behaviour in
// timing races the clauses do not grade; they never fail the bench.
#include "VKL_srp_domain.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <utility>

static VKL_srp_domain* d;
static std::vector<std::pair<int, uint32_t>> evs;
static int checks = 0, fails = 0;

static void tick() {
  d->clk_i = 0; d->eval();
  if (d->dom_ev_valid_o && d->dom_ev_ready_i) evs.push_back({d->dom_ev_event_o, d->dom_ev_value_o});
  d->clk_i = 1; d->eval();
}
static void run(int n) { for (int i = 0; i < n; i++) tick(); }
static void check(bool ok, const char* name) {
  checks++; if (!ok) fails++;
  printf("%s: %s\n", ok ? "PASS" : "FAIL", name);
}
static void dump(const char* tag) {
  printf("  %s events:", tag);
  for (auto& e : evs) printf(" (%d,%08x)", e.first, e.second);
  printf("\n");
}
// one received Domain value: registering event, or Lv
static void rx(int cid, int prio, int vid, int nov, bool lv) {
  d->rxdom_class_id_i = cid; d->rxdom_prio_i = prio; d->rxdom_vid_i = vid; d->rxdom_nov_i = nov;
  if (lv) d->rxdom_lv_i = 1; else d->rxdom_valid_i = 1;
  tick();
  d->rxdom_lv_i = 0; d->rxdom_valid_i = 0;
}
static void periodic_then_tx() {
  d->periodic_tick_i = 1; tick(); d->periodic_tick_i = 0;
  run(3); d->tx_tick_i = 1; tick(); d->tx_tick_i = 0; run(10);
}
static void rx_leaveall() { d->leaveall_tick_i = 1; tick(); d->leaveall_tick_i = 0; }
static void tx() { d->tx_tick_i = 1; tick(); d->tx_tick_i = 0; }

constexpr int NEW = 0, JIN = 1, JMT = 3, LV = 5;
constexpr uint32_t DEF = 0x06030002u;
using V = std::vector<std::pair<int, uint32_t>>;

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  d = new VKL_srp_domain;
  d->rst_n = 0; d->link_up_i = 0; d->dom_ev_ready_i = 1;
  d->rxdom_valid_i = 0; d->rxdom_lv_i = 0; d->periodic_tick_i = 0;
  d->leaveall_tick_i = 0; d->tx_tick_i = 0;
  run(5); d->rst_n = 1; run(5);

  evs.clear(); d->link_up_i = 1; run(10);
  check(evs == V{{NEW, DEF}}, "P1 link rise: one New of the default Domain {6,3,2}");

  evs.clear(); periodic_then_tx();
  check(evs == V{{JMT, DEF}}, "P2 no peer: periodic re-join JoinMt"); dump("P2");

  evs.clear(); rx(6, 3, 2, 1, false); run(3); periodic_then_tx();
  check(evs == V{{JIN, DEF}}, "P3 peer declares {6,3,2}: periodic re-join JoinIn"); dump("P3");

  evs.clear(); rx(6, 3, 2, 1, true); periodic_then_tx();
  check(evs == V{{JMT, DEF}}, "P4 peer Lv {6,3,2}: IN -> MT at once, next re-join JoinMt"); dump("P4");

  // received LeaveAll on the Domain lane with no re-declaration: IN -> LV
  rx(6, 3, 2, 1, false); run(3);
  evs.clear(); rx_leaveall(); run(5); tx(); run(10);
  check(evs == V{{JMT, DEF}}, "P5 received LeaveAll, peer silent: LA re-join JoinMt (LV)"); dump("P5");
  evs.clear(); periodic_then_tx();
  check(evs == V{{JMT, DEF}}, "P5b still LV: periodic re-join JoinMt"); dump("P5b");

  evs.clear(); rx(6, 3, 2, 1, false); run(3); periodic_then_tx();
  check(evs == V{{JIN, DEF}}, "P6 peer re-declares: JoinIn"); dump("P6");

  evs.clear(); rx(6, 3, 9, 1, true); periodic_then_tx();
  check(evs == V{{JIN, DEF}}, "P7 Lv of {6,3,9} (same prio, other VID) leaves IN"); dump("P7");

  evs.clear(); rx(6, 4, 2, 1, true); periodic_then_tx();
  check(evs == V{{JIN, DEF}}, "P8 Lv of {6,4,2} (other prio, same VID) leaves IN"); dump("P8");

  evs.clear(); rx(5, 2, 2, 2, true); periodic_then_tx();
  check(evs == V{{JMT, DEF}}, "P9 Lv of the two-class vector {5,2,2} NoV 2 (surfaces {6,3,2}): JoinMt"); dump("P9");

  evs.clear(); rx(5, 2, 2, 2, false); run(3); periodic_then_tx();
  check(evs == V{{JIN, DEF}} && d->adopted_o == 0,
        "P10 two-class vector {5,2,2} NoV 2 registers {6,3,2}, no adoption: JoinIn"); dump("P10");

  evs.clear(); rx(5, 2, 2, 1, false); run(3); periodic_then_tx();
  check(evs == V{{JIN, DEF}} && d->adopted_o == 0,
        "P11 class-B-only vector {5,2,2} NoV 1 is not Class A: nothing changes"); dump("P11");

  // own LeaveAll: sLA on the round's tx!: txLA! IN -> LV, re-join JoinMt
  evs.clear(); d->leaveall_tick_i = 1; d->tx_tick_i = 1; tick(); d->leaveall_tick_i = 0; d->tx_tick_i = 0; run(10);
  check(evs == V{{JMT, DEF}}, "P12 own LeaveAll: re-join JoinMt"); dump("P12");

  // adoption: SR class priority and VID update (Milan 4.2.7.2.1)
  evs.clear(); int chg = 0;
  d->rxdom_class_id_i = 6; d->rxdom_prio_i = 5; d->rxdom_vid_i = 7; d->rxdom_nov_i = 1; d->rxdom_valid_i = 1;
  tick(); d->rxdom_valid_i = 0;
  for (int i = 0; i < 10; i++) { tick(); chg += d->evt_domain_change_o; }
  check(evs == V{{LV, DEF}, {NEW, 0x06050007u}} && d->class_a_prio_o == 5 && d->class_a_vid_o == 7
        && d->adopted_o == 1 && chg == 1,
        "P13 differing Domain {6,5,7}: Lv old, New adopted, prio 5 VID 7, one DOMAIN_CHANGE"); dump("P13");
  evs.clear(); periodic_then_tx();
  check(evs == V{{JIN, 0x06050007u}}, "P14 adopted value registered by its declaration: JoinIn"); dump("P14");
  evs.clear(); rx(6, 5, 7, 1, true); periodic_then_tx();
  check(evs == V{{JMT, 0x06050007u}} && d->adopted_o == 1 && d->class_a_prio_o == 5,
        "P15 Lv of the adopted value: JoinMt, adoption kept until LINK_DOWN"); dump("P15");

  // link down/up: revert, New, nothing registered
  rx(6, 5, 7, 1, false); run(3);
  evs.clear(); d->link_up_i = 0; run(10); d->link_up_i = 1; run(10); periodic_then_tx();
  check(evs == V{{NEW, DEF}, {JMT, DEF}} && d->adopted_o == 0 && d->class_a_prio_o == 3 && d->class_a_vid_o == 2,
        "P16 LINK_DOWN/LINK_UP: revert to defaults, New, then JoinMt"); dump("P16");

  // ---- OBS: timing races the clauses do not grade --------------------------
  // (a) a tx! between a received LeaveAll and the peer's Domain value later in
  //     the same MRPDU
  rx(6, 3, 2, 1, false); run(3);
  evs.clear(); rx_leaveall(); tick(); tx(); run(2); rx(6, 3, 2, 1, false); run(10);
  printf("OBS-a tx! inside the peer LeaveAll MRPDU before its Domain value: ");
  for (auto& e : evs) printf("(%d,%08x) ", e.first, e.second); printf("\n");
  // (b) a received LeaveAll in the very clock of a tx!
  run(3); evs.clear();
  d->leaveall_tick_i = 1; d->tx_tick_i = 1; tick(); d->leaveall_tick_i = 0; d->tx_tick_i = 0;
  run(3); rx(6, 3, 2, 1, false); run(10);
  printf("OBS-b received LeaveAll on a tx! clock, Domain value 4 clocks later: ");
  for (auto& e : evs) printf("(%d,%08x) ", e.first, e.second); printf("\n");

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete d;
  return fails ? 1 : 0;
}

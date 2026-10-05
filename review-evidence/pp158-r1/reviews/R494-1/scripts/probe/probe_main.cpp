// Reviewer probe (disposable): tb/aecp_notify-style harness at N_CTRL_P=3,
// rows C(0) D(1) E(2). Grades the issue #158 acceptance beyond the committed
// two-row bench: a longer hold, a drain of a not-yet-served row, two drains in
// one round, re-registration during the hold, and the #148 stamp follow.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "../common/verilator_harness.hpp"
#include "VKL_aecp_notify.h"
#include "verilated.h"

#define CHECK(cond, ...) do { ++checks; if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } else { printf("ok:   " __VA_ARGS__); printf("\n"); } } while (0)

static constexpr uint8_t OWN_TL = 0xA0;
static constexpr uint8_t REGMON_BASE = 25;
static constexpr uint8_t KIND_DEREG = 0, KIND_CTRS = 6, KIND_NAME = 8;
static constexpr uint16_t DT_AVB = 0x0009;
static constexpr uint32_t WALK = 8;
static constexpr uint64_t EID[3] = {0x3333000000000003ull, 0x4444000000000004ull, 0x5555000000000005ull};
static constexpr uint64_t MAC[3] = {0x020000000003ull, 0x020000000004ull, 0x020000000005ull};

struct Job { uint32_t ms = 0; uint8_t kind = 0; uint16_t dt = 0, di = 0, a0 = 0, a1 = 0, seq = 0; uint64_t mac = 0; };

struct H {
  VKL_aecp_notify* d = nullptr; uint32_t now = 1000; int checks = 0, fails = 0;
  void tick() { d->now_ms_i = now; d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
  void idle(int n = 1) { for (int i = 0; i < n; ++i) tick(); }
  void reg(uint64_t eid, uint64_t mac, bool tl) {
    d->rgy_state_i = 0; d->rgy_op_i = 0; d->rgy_eid_i = eid; d->rgy_mac_i = mac; d->rgy_tl_i = tl; d->rgy_req_i = 1;
    int g = 0; while (g++ < 24) { d->clk_i = 0; d->eval(); if (!d->rgy_wait_o) break; tick(); }
    tick(); d->rgy_req_i = 0; idle(2);
  }
  void expire(int row) { d->tmr_exp_slot_i = REGMON_BASE + row; d->tmr_exp_owner_i = OWN_TL | row; d->tmr_exp_valid_i = 1; tick(); d->tmr_exp_valid_i = 0; }
  void warm() { d->rst_n = 0; idle(2); d->rst_n = 1; idle(2); }
  void ctr() { d->ev_ctr_type_i = DT_AVB; d->ev_ctr_index_i = 0; d->ev_ctr_i = 1; tick(); d->ev_ctr_i = 0; ++now; }
  Job presented(uint32_t last) {
    while (now <= last) { d->clk_i = 0; d->eval();
      if (d->uns_valid_o) return {now, (uint8_t)d->uns_kind_o, (uint16_t)d->uns_desc_type_o, (uint16_t)d->uns_desc_index_o, (uint16_t)d->uns_arg0_o, (uint16_t)d->uns_arg1_o, (uint16_t)d->uns_seq_o, (uint64_t)d->uns_mac_o};
      tick(); ++now; }
    return {};
  }
  uint32_t retire() { uint32_t s = now; d->uns_done_i = 1; tick(); d->uns_done_i = 0; ++now; return s; }
  void hold_until(uint32_t ms) { while (now < ms) { tick(); ++now; } }
  std::vector<Job> drain_all(uint32_t last) { std::vector<Job> v; for (Job j = presented(last); j.ms; j = presented(last)) { v.push_back(j); retire(); } return v; }
  void pr(const char* id, const std::vector<Job>& v) { for (auto& j : v) printf("  [i] %s: ms %u kind %u %04x:%u args %u/%u seq %u to %012llx\n", id, j.ms, j.kind, j.dt, j.di, j.a0, j.a1, j.seq, (unsigned long long)j.mac); }
  int count(const std::vector<Job>& v, uint64_t mac, uint8_t kind, uint16_t dt, uint16_t di, int seq = -1) {
    int n = 0; for (auto& j : v) if (j.mac == mac && j.kind == kind && j.dt == dt && j.di == di && (seq < 0 || j.seq == seq)) ++n; return n; }
  int to(const std::vector<Job>& v, uint64_t mac) { int n = 0; for (auto& j : v) if (j.mac == mac) ++n; return n; }

  // P1: C expires after its own job in a 3-row GET_COUNTERS round: D and E keep the round's notification
  void p1() {
    warm(); d->uns_done_i = 0; now = 20000;
    reg(EID[0], MAC[0], true); reg(EID[1], MAC[1], false); reg(EID[2], MAC[2], false);
    ctr(); Job c = presented(now + WALK); expire(0); retire();
    auto v = drain_all(now + 6 * WALK); v.insert(v.begin(), c); pr("P1", v);
    CHECK(count(v, MAC[1], KIND_CTRS, DT_AVB, 0) == 1 && count(v, MAC[2], KIND_CTRS, DT_AVB, 0) == 1,
          "P1: 3 rows, C expires after its job: D and E each receive the round's GET_COUNTERS once");
    CHECK(count(v, MAC[0], KIND_DEREG, 0, 0, 1) == 1 && to(v, MAC[0]) == 2,
          "P1: C receives its GET_COUNTERS and one DEREGISTER (0000:0, seq 1)");
  }
  // P2: E (row 2, not yet served) expires while C's job waits: E gets only its DEREGISTER; D keeps the round
  void p2() {
    warm(); d->uns_done_i = 0; now = 40000;
    reg(EID[0], MAC[0], false); reg(EID[1], MAC[1], false); reg(EID[2], MAC[2], true);
    ctr(); Job c = presented(now + WALK); expire(2); retire();
    auto v = drain_all(now + 6 * WALK); v.insert(v.begin(), c); pr("P2", v);
    CHECK(count(v, MAC[0], KIND_CTRS, DT_AVB, 0) == 1 && count(v, MAC[1], KIND_CTRS, DT_AVB, 0) == 1,
          "P2: a not-yet-served row E drains: C and D each receive the round's GET_COUNTERS");
    CHECK(to(v, MAC[2]) == 1 && count(v, MAC[2], KIND_DEREG, 0, 0, 0) == 1,
          "P2: E receives exactly one job, its own DEREGISTER (seq 0)");
  }
  // P3: SET_NAME round, C and D both TIME_LIMITED; C expires during C's job, D during D's job
  void p3() {
    warm(); d->uns_done_i = 0; now = 50000;
    reg(EID[0], MAC[0], true); reg(EID[1], MAC[1], true); reg(EID[2], MAC[2], false);
    d->ev_cmd_class_i = 7; d->ev_cmd_type_i = 5; d->ev_cmd_index_i = 1; d->ev_cmd_arg0_i = 2; d->ev_cmd_arg1_i = 3;
    d->ev_cmd_excl_eid_i = 0x7777000000000007ull; d->ev_cmd_i = 1; tick(); d->ev_cmd_i = 0; ++now;
    std::vector<Job> v;
    Job j = presented(now + WALK); v.push_back(j); expire(0); retire();
    for (int k = 0; k < 6; ++k) { Job n = presented(now + 2 * WALK); if (!n.ms) break; v.push_back(n); if (n.mac == MAC[1] && n.kind == KIND_NAME) expire(1); retire(); }
    pr("P3", v);
    CHECK(count(v, MAC[1], KIND_NAME, 5, 1) == 1 && count(v, MAC[2], KIND_NAME, 5, 1) == 1,
          "P3: two drains in one SET_NAME round: D (expiring during its own job) and E keep the round");
    CHECK(count(v, MAC[0], KIND_DEREG, 0, 0, 1) == 1 && count(v, MAC[1], KIND_DEREG, 0, 0, 1) == 1,
          "P3: C and D each receive one DEREGISTER with their own sequence_id 1");
    bool args = true; for (auto& x : v) if (x.kind == KIND_NAME && (x.a0 != 2 || x.a1 != 3)) args = false;
    CHECK(args, "P3: every SET_NAME job keeps arguments 2/3");
  }
  // P4: C re-registers while the drained DEREGISTER is held behind the round (disclosed ordering residual)
  void p4() {
    warm(); d->uns_done_i = 0; now = 60000;
    reg(EID[0], MAC[0], true); reg(EID[1], MAC[1], false); reg(EID[2], MAC[2], false);
    ctr(); std::vector<Job> v; Job c = presented(now + WALK); v.push_back(c); expire(0); retire();
    Job dj = presented(now + WALK); v.push_back(dj);
    hold_until(now + 200);                      // D's job waits for the TX slot
    uint32_t rereg = now; reg(EID[0], MAC[0], false);   // C re-registers meanwhile (withdraws D's job)
    auto rest = drain_all(now + 8 * WALK); v.insert(v.end(), rest.begin(), rest.end()); pr("P4", v);
    printf("  [i] P4: C re-registered at ms %u; registered rows now %u\n", rereg, unsigned(d->dbg_reg_cnt_o));
    CHECK(count(v, MAC[1], KIND_CTRS, DT_AVB, 0) >= 1 && count(v, MAC[2], KIND_CTRS, DT_AVB, 0) == 1,
          "P4: D and E keep the round's GET_COUNTERS across the re-registration");
    uint32_t dereg_ms = 0; for (auto& x : v) if (x.mac == MAC[0] && x.kind == KIND_DEREG) dereg_ms = x.ms;
    printf("  [i] P4: C's DEREGISTER sent at ms %u (%s its re-registration at ms %u)\n", dereg_ms, dereg_ms > rereg ? "AFTER" : "before", rereg);
  }
  // P5: #148 follow through the drain, 3 rows: the next round's first GET_COUNTERS to each row waits
  // a second from that row's own send in the round, with the last job waiting 1.5 s for the TX slot
  void p5() {
    warm(); d->uns_done_i = 0; now = 70000;
    reg(EID[0], MAC[0], true); reg(EID[1], MAC[1], false); reg(EID[2], MAC[2], false);
    ctr(); std::vector<Job> v; Job c = presented(now + WALK); expire(0); c.ms = retire(); v.push_back(c);
    Job dj = presented(now + WALK); dj.ms = retire(); v.push_back(dj);
    Job ej = presented(now + WALK); uint32_t s0 = now; hold_until(s0 + 100); ctr(); hold_until(s0 + 1500); ej.ms = retire(); v.push_back(ej);
    auto rest = drain_all(ej.ms + 1000 + 3 * WALK); v.insert(v.end(), rest.begin(), rest.end()); pr("P5", v);
    uint32_t e1 = 0, e2 = 0, d2 = 0;
    for (auto& x : v) { if (x.mac == MAC[2] && x.kind == KIND_CTRS) { if (!e1) e1 = x.ms; else if (!e2) e2 = x.ms; }
                        if (x.mac == MAC[1] && x.kind == KIND_CTRS && x.ms > dj.ms && !d2) d2 = x.ms; }
    printf("  [i] P5: round's last send (E) %u; next round: D at %u, E at %u\n", e1, d2, e2);
    CHECK(e1 && d2 >= e1 + 1000 && d2 <= e1 + 1000 + 3 * WALK,
          "P5: the next GET_COUNTERS round waits a second from the round's last send (stamp follows E's wait through the drain)");
  }
};

int main(int argc, char** argv) {
  const milan::tb::Model<VKL_aecp_notify> model; H h; h.d = model.get(); auto* d = h.d;
  d->rgy_req_i = 0; d->ev_stri_in_i = 0; d->ev_stri_out_i = 0; d->ev_avb_i = 0; d->ev_asp_i = 0; d->ev_amap_i = 0;
  d->ev_ctr_i = 0; d->ev_cmd_i = 0; d->rx_cmd_valid_i = 0; d->prng_draw_busy_i = 1; d->prng_draw_valid_i = 0;
  d->ca_ready_i = 1; d->ca_rsp_valid_i = 0; d->ca_fail_valid_i = 0; d->uns_done_i = 1; d->tmr_exp_valid_i = 0;
  d->rst_n = 0; h.idle(4); d->rst_n = 1; h.idle(2);
  h.p1(); h.p2(); h.p3(); h.p4(); h.p5();
  printf("[probe N_CTRL_P=3] %d checks, %d failures\n", h.checks, h.fails);
  return h.fails ? 1 : 0;
}

// Lockstep differential bench: reference vs candidate KL_aecp_notify, same inputs.
#include "Vlockstep_top.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <string>
#include <fstream>

static uint64_t s;
static uint64_t rnd() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
static bool pct(int p) { return (int)(rnd() % 1000) < p * 10; }
static bool pmil(int p) { return (int)(rnd() % 1000) < p; }

struct Key { uint64_t eid; uint64_t mac; };

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  long cycles = argc > 2 ? strtol(argv[2], nullptr, 0) : 200000;
  int nctrl = argc > 3 ? atoi(argv[3]) : 16;
  int chaos = argc > 4 ? atoi(argv[4]) : 0;      // 1 = every input random each cycle
  s = seed * 0x9E3779B97F4A7C15ull + 1;
  std::vector<std::string> outs;
  { std::ifstream f("outputs.txt"); std::string l; while (std::getline(f, l)) outs.push_back(l); }
  Vlockstep_top* t = new Vlockstep_top;
  // key pool: base keys plus near-collisions (one chunk, one bit, eid-only, mac-only)
  std::vector<Key> pool;
  for (int k = 0; k < 10; k++) pool.push_back({rnd(), rnd() & 0xFFFFFFFFFFFFull});
  int nb = pool.size();
  for (int k = 0; k < nb; k++) {
    Key b = pool[k];
    pool.push_back({b.eid ^ (1ull << (rnd() % 64)), b.mac});            // one eid bit
    pool.push_back({b.eid, b.mac ^ (1ull << (rnd() % 48))});            // one mac bit
    pool.push_back({b.eid ^ (0x3Full << (6 * (rnd() % 10))), b.mac});    // one 6-bit chunk
  }
  pool.push_back({0, 0});
  pool.push_back({~0ull, 0xFFFFFFFFFFFFull});
  int np = pool.size();
  auto pick = [&]() -> Key { return pool[rnd() % np]; };
  long mism = 0, hits = 0, busy_rx = 0, busy_hit = 0, regs_max = 0, uns = 0, ca = 0, cancels = 0, draws = 0;
  int req_hold = 0; bool req = false;
  uint32_t now = 0;
  t->clk_i = 0; t->rst_n = 0;
  auto drive = [&](long cyc) {
    if (chaos) {
      t->rgy_req_i = rnd() & 1; t->rgy_state_i = pct(10); t->rgy_op_i = rnd() & 3;
      Key k = pick(); t->rgy_eid_i = k.eid; t->rgy_mac_i = k.mac; t->rgy_tl_i = rnd() & 1;
    } else {
      // registry/lock op face: hold the request until the beat is released, then drop
      if (!req && pct(8)) {
        req = true; req_hold = rnd() % 3;
        t->rgy_state_i = pct(8);
        int r = rnd() % 100; t->rgy_op_i = r < 55 ? 0 : r < 80 ? 1 : r < 90 ? 2 : 3;
        Key k = pick(); t->rgy_eid_i = k.eid; t->rgy_mac_i = k.mac; t->rgy_tl_i = rnd() & 1;
      } else if (req && !t->rgy_wait_o) {
        if (req_hold-- <= 0) req = false;
      }
      t->rgy_req_i = req;
    }
    t->ev_stri_in_i = pmil(5) ? (rnd() & 0xFF) : 0;
    t->ev_stri_out_i = pmil(5) ? (rnd() & 0xFF) : 0;
    t->ev_avb_i = pmil(3); t->ev_asp_i = pmil(3);
    t->ev_amap_i = pmil(3); t->ev_amap_remove_i = rnd() & 1;
    t->ev_amap_type_i = rnd(); t->ev_amap_index_i = rnd(); t->ev_amap_count_i = rnd();
    t->ev_amap_excl_eid_i = pick().eid;
    t->ev_ctr_i = pmil(10);
    { int r = rnd() % 5; t->ev_ctr_type_i = r == 0 ? 5 : r == 1 ? 6 : r == 2 ? 9 : r == 3 ? 0x24 : rnd();
      t->ev_ctr_index_i = pct(80) ? rnd() % 3 : rnd(); }
    t->ev_cmd_i = pmil(10); t->ev_cmd_class_i = rnd() & 15; t->ev_cmd_type_i = rnd();
    t->ev_cmd_index_i = rnd(); t->ev_cmd_arg0_i = rnd(); t->ev_cmd_arg1_i = rnd();
    t->ev_cmd_excl_eid_i = pick().eid;
    t->identify_button_i = (cyc / 5000) & 1 ? pct(90) : pct(2);
    t->identify_index_i = rnd() & 3;
    t->rx_cmd_valid_i = chaos ? (rnd() & 1) : pct(25);
    { Key k = pick(); t->rx_cmd_eid_i = k.eid; t->rx_cmd_mac_i = k.mac; }
    t->prng_draw_busy_i = pct(30); t->prng_draw_valid_i = pct(20); t->prng_draw_ms_i = rnd();
    t->ca_ready_i = pct(50);
    t->ca_rsp_valid_i = pct(3); t->ca_rsp_owner_i = rnd() & 15;
    t->ca_fail_valid_i = pct(3); t->ca_fail_owner_i = rnd() & 15;
    t->uns_done_i = chaos ? (rnd() & 1) : (t->uns_valid_o && pct(30));
    t->uns_tx_busy_i = pct(40);
    if (pct(2)) now += 1; if (pmil(1)) now += rnd() % 5000; if (pmil(1)) now = rnd();
    t->now_ms_i = now;
    // timer expiries aimed at this block's owners and slots
    t->tmr_exp_valid_i = pct(4);
    { int r = rnd() % 6; int i = rnd() % (nctrl + 1);
      if (r == 0) { t->tmr_exp_owner_i = 0xA0 + i; t->tmr_exp_slot_i = 25 + i; }
      else if (r == 1) { t->tmr_exp_owner_i = 0xD0 + i; t->tmr_exp_slot_i = 25 + nctrl + i; }
      else if (r == 2) { t->tmr_exp_owner_i = 0xB0; t->tmr_exp_slot_i = 61; }
      else if (r == 3) { t->tmr_exp_owner_i = 0xB1 + (rnd() % 3); t->tmr_exp_slot_i = 62 + (rnd() & 1); }
      else { t->tmr_exp_owner_i = rnd(); t->tmr_exp_slot_i = rnd() % 89; } }
  };
  for (long cyc = 0; cyc < cycles; cyc++) {
    t->rst_n = (cyc < 4 || pmil(chaos ? 2 : 0) || ((cyc % 50000) == 49999)) ? 0 : 1;
    drive(cyc);
    t->clk_i = 0; t->eval();
    if (t->mism_o) {
      mism++;
      if (mism <= 5) {
        unsigned ix = t->mism_ix_o;
        printf("MISMATCH cycle %ld output %s hits r=%x c=%x busy=%d\n", cyc,
               ix == 999 ? "rx_cmd_hit_w" : (ix ? outs[ix - 1].c_str() : "?"),
               (unsigned)t->hit_r_o, (unsigned)t->hit_c_o, t->busy_o);
      }
    }
    if (t->hit_r_o) hits++;
    if (t->busy_o && t->rx_cmd_valid_i) busy_rx++;
    if (t->busy_o && t->hit_r_o) busy_hit++;
    if (t->dbg_reg_cnt_o > regs_max) regs_max = t->dbg_reg_cnt_o;
    if (t->uns_valid_o && t->uns_done_i) uns++;
    if (t->ca_valid_o && t->ca_ready_i) ca++;
    if (t->ca_cancel_valid_o) cancels++;
    if (t->prng_draw_req_o) draws++;
    t->clk_i = 1; t->eval();
    if (t->mism_o) {
      mism++;
      if (mism <= 5) printf("MISMATCH after edge cycle %ld ix %u\n", cyc, (unsigned)t->mism_ix_o);
    }
  }
  printf("seed %llu cycles %ld nctrl %d chaos %d: mismatches %ld | hit cycles %ld, rx during reindex %ld, "
         "hit during reindex %ld, max regs %ld, uns jobs %ld, ca issued %ld, cancels %ld, draws %ld\n",
         (unsigned long long)seed, cycles, nctrl, chaos, mism, hits, busy_rx, busy_hit, regs_max, uns, ca, cancels, draws);
  delete t;
  return mism ? 1 : 0;
}

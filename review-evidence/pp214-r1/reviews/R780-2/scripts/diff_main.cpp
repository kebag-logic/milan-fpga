// Random lockstep of head and arm; stops a seed at the first output difference.
#include "Vdiff_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <random>
#include <cstdlib>
int main(int argc, char** argv) {
  const int seeds = argc > 1 ? atoi(argv[1]) : 200;
  const int cycles = argc > 2 ? atoi(argv[2]) : 40000;
  int diffs = 0, outside = 0, ready_only = 0; long corner_clocks = 0, hit_cycles = 0;
  for (int s = 1; s <= seeds; ++s) {
    VerilatedContext ctx; Vdiff_top t(&ctx);
    std::mt19937 r(s);
    auto chance = [&](int pct) { return int(r() % 100) < pct; };
    auto tick = [&]() { t.clk_i = 0; t.eval(); t.clk_i = 1; t.eval(); };
    t.rst_n = 0; for (int i = 0; i < 8; ++i) tick(); t.rst_n = 1;
    bool offering = false, prepare = false, draining = false; int ser_wait = 0;
    bool corner_this_offer = false;
    const int tick_pct = 1 + s % 12, prep_pct = 1 + s % 7, offer_pct = 20 + s % 70;
    for (int c = 0; c < cycles; ++c) {
      if (!offering && chance(offer_pct)) {
        offering = true; corner_this_offer = false;
        const bool mvrp = chance(35);
        t.ev_app_i = mvrp; t.ev_type_i = mvrp ? 1 : 1 + r() % 4;
        t.ev_event_i = r() % 6; t.ev_fp_i = r() % 4;
        for (auto& w : t.ev_value_i.m_storage) w = 0;
        t.ev_value_i.m_storage[8] = uint32_t(r() % 6) << 8 | 0x06000000u;  // bits 287..256 top word
      }
      t.ev_valid_i = offering;
      t.join_i = (chance(tick_pct) ? 1 : 0) | (chance(tick_pct) ? 2 : 0);
      t.la_i = chance(2) ? 1 + r() % 2 : 0;
      if (!prepare && chance(prep_pct)) prepare = true;
      t.prepare_i = prepare;
      t.txreq_ready_i = t.h_txv_o && chance(60);
      t.ser_req_i = 0;
      if (t.txreq_ready_i) { t.ser_slot_i = t.h_txs_o; ser_wait = 1; }
      else if (ser_wait == 1) { t.ser_req_i = 1; t.ser_ready_i = 1; ser_wait = 2; draining = true; }
      t.clk_i = 0; t.eval();
      if (t.h_st_o == 16 && t.h_go0_o && t.prepare_i && offering) { corner_this_offer = true; ++corner_clocks; }
      const bool rdy_diff = t.h_ready_o != t.a_ready_o;
      const bool vec_diff = t.h_vec_o != t.a_vec_o;
      if (rdy_diff || vec_diff) {
        ++diffs; if (!corner_this_offer) ++outside;
        if (rdy_diff && !vec_diff) ++ready_only;
        printf("seed %d cycle %d st %d head_ready %d arm_ready %d vec_diff %d corner_seen %d\n", s, c,
               int(t.h_st_o), int(t.h_ready_o), int(t.a_ready_o), int(vec_diff), int(corner_this_offer));
        break;
      }
      const bool taken = offering && t.h_ready_o;
      const bool done = t.h_done_o;
      t.clk_i = 1; t.eval();
      ++hit_cycles;
      if (taken) offering = false;
      if (done) prepare = false;
      if (draining && t.h_serv_o && t.h_serl_o) { draining = false; t.ser_ready_i = 0; ser_wait = 0; }
    }
  }
  printf("seeds %d cycles_run %ld corner_clocks %ld first_differences %d outside_corner %d ready_only %d\n",
         seeds, hit_cycles, corner_clocks, diffs, outside, ready_only);
  return 0;
}

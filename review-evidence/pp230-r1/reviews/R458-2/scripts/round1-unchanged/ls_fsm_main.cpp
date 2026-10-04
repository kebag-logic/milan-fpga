// SPDX-License-Identifier: CERN-OHL-W-2.0
// R458-1 review probe: drives ls_fsm with random words, random time steps and
// random mid-run resets; prints mismatch and coverage counters. Exit 1 on any
// mismatch. usage: Vls_fsm <cycles> <seed>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include "Vls_fsm.h"
#include "verilated.h"

static uint64_t s_state;
static uint64_t rnd() {
  s_state ^= s_state << 13; s_state ^= s_state >> 7; s_state ^= s_state << 17;
  return s_state;
}

int main(int argc, char** argv) {
  const uint64_t cycles = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 1000000;
  const uint64_t seed = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 1;
  s_state = 0x9E3779B97F4A7C15ull ^ (seed * 0x100000001B3ull);
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->randReset(2);
  ctx->randSeed(static_cast<int>(seed));
  const auto m = std::make_unique<Vls_fsm>(ctx.get());
  uint32_t now = 0; uint32_t step = 8; uint64_t resets = 0; int rst_hold = 4;
  uint64_t first_mis = 0;
  for (uint64_t c = 0; c < cycles; ++c) {
    if (rst_hold == 0 && (rnd() % 40000) == 0) { rst_hold = 1 + rnd() % 5; ++resets; }
    m->rst_n = rst_hold > 0 ? 0 : 1;
    if (rst_hold > 0) --rst_hold;
    m->r0 = rnd(); m->r1 = rnd(); m->r2 = rnd(); m->r3 = rnd();
    m->r4 = rnd(); m->r5 = rnd(); m->r6 = rnd();
    if (--step == 0) { ++now; step = 8 + rnd() % 40; }
    m->now_ms_i = now;
    m->clk_i = 0; m->eval();
    m->clk_i = 1; m->eval();
    if (!first_mis && (m->mis_tk_o || m->mis_ls_o || m->mis_ad_o)) first_mis = c;
  }
  m->final();
  std::printf("LS-FSM seed=%llu cycles=%llu resets=%llu mis_tk=%llu mis_ls=%llu mis_ad=%llu first_mis_cycle=%llu "
              "tk_push=%llu ls_push=%llu redeclare=%llu resettle=%llu adm_rounds=%llu walk_push_ram_arm=%llu "
              "lstn_reg_change=%llu tk_registered=%llu\n",
              (unsigned long long)seed, (unsigned long long)cycles, (unsigned long long)resets,
              (unsigned long long)m->mis_tk_o, (unsigned long long)m->mis_ls_o, (unsigned long long)m->mis_ad_o,
              (unsigned long long)first_mis, (unsigned long long)m->cov_tk_push_o,
              (unsigned long long)m->cov_ls_push_o, (unsigned long long)m->cov_redecl_o,
              (unsigned long long)m->cov_resettle_o, (unsigned long long)m->cov_round_o,
              (unsigned long long)m->cov_walk_ram_o, (unsigned long long)m->cov_tk_reg_o,
              (unsigned long long)m->cov_ls_reg_o);
  return (m->mis_tk_o || m->mis_ls_o || m->mis_ad_o) ? 1 : 0;
}

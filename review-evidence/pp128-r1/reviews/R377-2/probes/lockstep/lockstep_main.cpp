// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R377-2): randomized, contract-conforming stimulus for the
// lockstep wrapper. Exit 0 = no output divergence; exit 3 = divergence.
// Usage: Vlockstep <seed> <cycles>
#include "Vlockstep.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <memory>
#include <random>

namespace {
struct Rsp { uint64_t due_cyc; uint32_t due_ms; bool by_ms; bool ok; uint64_t da; };
}

int main(int argc, char** argv) {
  const uint64_t seed = argc > 1 ? std::strtoull(argv[1], nullptr, 0) : 1;
  const uint64_t cycles = argc > 2 ? std::strtoull(argv[2], nullptr, 0) : 1000000;
  auto ctx = std::make_unique<VerilatedContext>();
  auto d = std::make_unique<Vlockstep>(ctx.get());
  std::mt19937_64 rng(seed);
  auto chance = [&](uint32_t den) { return den && (rng() % den) == 0; };
  auto rnd = [&](uint32_t n) { return static_cast<uint32_t>(rng() % n); };

  uint32_t now = chance(3) ? 0xffffff00u + rnd(0x80) : rnd(1u << 20);
  uint32_t en = 0xff;
  uint64_t lsn = 0;
  int mode = 0;            // allocator episode mode
  int txn_mode = 0;        // 0 sparse, 1 continuous
  int ready_wait = 0;
  std::deque<Rsp> owed;
  int prng_busy = 0;
  bool prng_pending = false;
  int glitch_bit = -1;
  int reset_left = 5;
  bool txn_hold = false;
  uint64_t n_acc = 0, n_ok = 0, n_ref = 0, n_conf = 0, n_resp = 0, n_succ = 0,
           n_decl = 0, n_rel = 0, n_draw = 0, n_rst = 0;
  uint32_t decl_prev = 0;
  int focus = 0;           // cycles of boosted churn around a request/response
  int focus_src = 0;
  const bool focused = (seed % 4) != 0;   // 3 of 4 seeds use focused churn

  for (uint64_t cyc = 0; cyc < cycles; ++cyc) {
    if (cyc % 20000 == 0) { mode = rnd(6); txn_mode = rnd(3) == 0; }
    // ---- time
    if (chance(8)) now += 1;
    if (chance(5000)) now += 100;
    if (chance(60000)) now += 10000;
    d->now_ms_i = now;
    // ---- reset
    if (reset_left == 0 && chance(300000)) { reset_left = 3; ++n_rst; }
    d->rst_n = reset_left > 0 ? 0 : 1;
    if (reset_left > 0) { --reset_left; owed.clear(); ready_wait = 0; txn_hold = false;
                          prng_busy = 0; prng_pending = false; }
    // ---- configuration churn
    if (glitch_bit >= 0) { en ^= 1u << glitch_bit; glitch_bit = -1; }
    if (chance(4000)) en ^= 1u << rnd(8);
    if (chance(20000)) { glitch_bit = static_cast<int>(rnd(8)); en ^= 1u << glitch_bit; }
    if (focused && focus > 0 && glitch_bit < 0 && chance(24)) {
      glitch_bit = chance(4) ? static_cast<int>(rnd(8)) : focus_src;
      en ^= 1u << glitch_bit;
      if (chance(3)) glitch_bit = -1;       // sometimes a lasting disable
    }
    if (en == 0 && chance(2)) en = 0xff;
    d->cfg_src_en_i = en;
    d->cfg_src_iface_i = 0;
    if (chance(3000)) {
      const int s = static_cast<int>(rnd(8));
      lsn = (lsn & ~(3ull << (2 * s))) | (uint64_t(rnd(4)) << (2 * s));
    }
    d->srp_lsn_reg_state_i = static_cast<uint16_t>(lsn);
    d->srp_pcp_change_i = chance(20000);
    // ---- timer expiries (matching slot/owner, occasionally foreign)
    d->tmr_exp_valid_i = 0;
    if (chance(2000)) {
      const int s = static_cast<int>(rnd(8));
      d->tmr_exp_valid_i = 1; d->tmr_exp_slot_i = 17 + s; d->tmr_exp_owner_i = 0x50 + s;
    } else if (chance(20000)) {
      d->tmr_exp_valid_i = 1; d->tmr_exp_slot_i = rnd(91); d->tmr_exp_owner_i = rnd(256);
    }
    // ---- prng
    d->prng_draw_valid_i = 0;
    if (prng_pending) {
      if (prng_busy > 0) --prng_busy;
      else { d->prng_draw_valid_i = 1; d->prng_draw_ms_i = rnd(40); prng_pending = false; }
    }
    d->prng_draw_busy_i = prng_pending ? 1 : 0;
    // ---- conflicts
    d->maap_conflict_valid_i = chance(3000);
    d->maap_conflict_src_i = rnd(8);
    if (focused && focus > 0 && chance(12)) {
      d->maap_conflict_valid_i = 1;
      d->maap_conflict_src_i = chance(4) ? rnd(8) : focus_src;
    }
    if (focus > 0) --focus;
    if (d->maap_conflict_valid_i) ++n_conf;
    // ---- allocator responses (FIFO, contract: one per accepted request)
    d->maap_rsp_valid_i = 0; d->maap_rsp_ok_i = 0; d->maap_rsp_da_i = 0;
    if (!owed.empty()) {
      const Rsp& r = owed.front();
      const bool due = r.by_ms ? (int32_t(now - r.due_ms) >= 0) : cyc >= r.due_cyc;
      if (due && !(mode == 3 && chance(1) && r.by_ms && rnd(4) != 0)) {
        d->maap_rsp_valid_i = 1; d->maap_rsp_ok_i = r.ok; d->maap_rsp_da_i = r.da;
        owed.pop_front();
        if (chance(2)) focus = 8;
      }
    }
    // ---- allocator request acceptance (never while an answer is owed)
    d->maap_req_ready_i = 0;
    // ---- transactions
    if (!txn_hold) {
      if (txn_mode ? true : chance(60)) {
        txn_hold = true;
        const uint32_t m = rnd(10);
        d->t_msg_i = m < 6 ? 0 : (m < 7 ? 1 : (m < 9 ? 2 : 3));
        d->t_uid_i = rnd(10);
        d->t_if_i = chance(10) ? 1 : 0;
        d->t_slot_i = rnd(5);
        d->t_tgt_i = chance(20) ? 0 : 1;
        d->t_seq_i = rnd(65536);
        d->rxs_slot_len_i = rnd(577);
      }
    }
    d->txn_valid_i = txn_hold ? 1 : 0;
    d->rxs_rd_data_i = rnd(256);

    d->clk_i = 0; d->eval();
    // request face reacts to the reference copy's offer
    if (d->a_maap_req_valid_o && owed.empty() && mode != 2) {
      if (ready_wait <= 0) ready_wait = 1 + static_cast<int>(rnd(mode == 5 ? 1500 : 6));
      if (--ready_wait == 0) d->maap_req_ready_i = 1;
    }
    d->eval();
    if (d->diff_o) {
      std::printf("DIVERGE seed=%llu cycle=%llu\n", (unsigned long long)seed,
                  (unsigned long long)cyc);
      return 3;
    }
    // sample handshakes on this edge
    const bool acc = d->a_maap_req_valid_o && d->maap_req_ready_i;
    const bool rel = d->a_maap_req_release_o;
    const bool txn_take = d->txn_valid_i && d->a_txn_ready_o;
    if (d->a_resp_valid_o) { ++n_resp; if (d->a_resp_status_o == 0) ++n_succ; }
    if (d->a_prng_draw_req_o) { prng_pending = true; prng_busy = static_cast<int>(rnd(3)); ++n_draw; }
    d->clk_i = 1; d->eval();
    if (d->a_maap_req_valid_o) focus_src = d->a_maap_req_src_o;
    if (acc && chance(3)) focus = 8;
    if (acc) {
      ++n_acc; if (rel) ++n_rel;
      Rsp r{};
      const int src = d->a_maap_req_src_o;
      bool ok = true;
      if (mode == 1) ok = false;
      if (mode == 4) ok = rnd(3) != 0;
      if (mode == 0 || mode == 5) ok = src < 6;
      r.ok = ok && !rel;
      r.da = r.ok ? (0x91e0f0000000ull + (uint64_t(rnd(4)) << 8) + src) : 0;
      if (mode == 3) { r.by_ms = true; r.due_ms = now + 5000 + rnd(12000); }
      else { r.by_ms = false; r.due_cyc = cyc + 1 + rnd(40); }
      if (r.ok) ++n_ok; else if (!rel) ++n_ref;
      owed.push_back(r);
    }
    if (txn_take) txn_hold = false;
    const uint32_t decl = d->a_declaring_o;
    n_decl += __builtin_popcount(decl & ~decl_prev);
    decl_prev = decl;
  }
  std::printf("NODIFF seed=%llu cycles=%llu accepts=%llu releases=%llu grants_ok=%llu "
              "refusals=%llu conflicts=%llu responses=%llu successes=%llu "
              "declare_edges=%llu draws=%llu resets=%llu\n",
              (unsigned long long)seed, (unsigned long long)cycles,
              (unsigned long long)n_acc, (unsigned long long)n_rel,
              (unsigned long long)n_ok, (unsigned long long)n_ref,
              (unsigned long long)n_conf, (unsigned long long)n_resp,
              (unsigned long long)n_succ, (unsigned long long)n_decl,
              (unsigned long long)n_draw, (unsigned long long)n_rst);
  return 0;
}

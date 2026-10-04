// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer lockstep bench: main's KL_aecp_notify (u_r) beside the candidate
// (u_d), the same inputs every cycle; every output and rx_cmd_hit_w compared
// after the input change (clock low) and after the rising edge.
//
// Usage: Vlk_top SEED CYCLES MODE [N_CTRL]
//   MODE 0 protocol-shaped, 1 fully random, 2 rewrite-focused (resets aimed at
//   the two re-index cycles, commands aimed at the written row's old/new identity),
//   3 registry-filling (REGISTER-heavy, timers rarely fire early).
// Exit 0 = no mismatch, 1 = mismatch, 2 = usage.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <random>
#include <string>
#include <vector>
#include "Vlk_top.h"
#include "verilated.h"

namespace {

struct Id { uint64_t eid; uint64_t mac; };

struct Arm { bool on = false; uint8_t owner = 0; uint32_t deadline = 0; };

}  // namespace

int main(int argc, char** argv) {
  if (argc < 4) { fprintf(stderr, "usage: Vlk_top SEED CYCLES MODE [N_CTRL]\n"); return 2; }
  const uint64_t seed = strtoull(argv[1], nullptr, 0);
  const uint64_t cycles = strtoull(argv[2], nullptr, 0);
  const int mode = atoi(argv[3]);
  const int n_ctrl_arg = argc > 4 ? atoi(argv[4]) : 16;
  std::mt19937_64 rng(seed);
  auto rnd = [&](uint64_t n) { return n ? rng() % n : 0; };
  auto pct = [&](double p) { return std::uniform_real_distribution<double>(0, 1)(rng) < p; };

  std::vector<std::string> names;
  {
    std::ifstream f("lk_top.sv.outputs");
    std::string s;
    while (std::getline(f, s)) names.push_back(s);
  }

  auto ctx = std::make_unique<VerilatedContext>();
  ctx->randReset(0);
  auto t = std::make_unique<Vlk_top>(ctx.get());

  // identity pool: chunk-sharing neighbours, one-bit neighbours, zero, all-ones
  std::vector<Id> pool;
  const uint64_t M48 = (1ull << 48) - 1;
  pool.push_back({0, 0});
  pool.push_back({~0ull, M48});
  for (int i = 0; i < 10; ++i) pool.push_back({rng(), rng() & M48});
  for (int i = 0; i < 6; ++i) {  // differ from pool[2] in exactly one 6-bit chunk
    Id b = pool[2];
    const int c = static_cast<int>(rnd(19));
    const int lo = c * 6;  // bit position in the 112-bit {eid, mac}
    for (int k = lo; k < lo + 6 && k < 112; ++k) {
      if (!pct(0.5) && k != lo) continue;
      if (k < 48) b.mac ^= 1ull << k; else b.eid ^= 1ull << (k - 48);
    }
    pool.push_back(b);
  }
  for (int i = 0; i < 6; ++i) {  // one-bit neighbours of pool[3]
    Id b = pool[3];
    const int k = static_cast<int>(rnd(112));
    if (k < 48) b.mac ^= 1ull << k; else b.eid ^= 1ull << (k - 48);
    pool.push_back(b);
  }
  // last chunk (bits 108..111 = eid bits 60..63) neighbour
  pool.push_back({pool[4].eid ^ (1ull << 62), pool[4].mac});

  auto pick_id = [&]() -> Id {
    const uint64_t r = rnd(100);
    if (r < 80) return pool[rnd(pool.size())];
    if (r < 90) { Id b = pool[rnd(pool.size())]; const int k = static_cast<int>(rnd(112));
                  if (k < 48) b.mac ^= 1ull << k; else b.eid ^= 1ull << (k - 48); return b; }
    return {rng(), rng() & M48};
  };

  Arm arms[128];
  uint32_t now = static_cast<uint32_t>(mode == 1 ? rng() : 1000);
  const uint64_t ms_period = 1 + rnd(4) * (mode == 0 ? 7 : 2);
  int rgy_phase = 0;        // 0 idle, 1 requesting, 2 answered (hold a little)
  int rgy_hold = 0;
  int uns_wait = -1, prng_wait = -1;
  int rst_left = 0;
  int ident_hold = 0;

  uint64_t mism_total = 0, mism_cycles = 0, printed = 0;
  std::vector<uint64_t> by_out(names.size(), 0);
  uint64_t hit_mism = 0;
  // coverage
  uint64_t c_hits = 0, c_cmd_clr = 0, c_cmd_set = 0, c_hit_wr_clr = 0, c_hit_wr_set = 0,
           c_oldhit_clr = 0, c_idchg_clr = 0, c_rst_clr = 0, c_rst_set = 0, c_rst = 0,
           c_walk_coll = 0, c_ca_coll = 0, c_full = 0, c_emit_wb = 0, c_rst_ctr = 0,
           c_reg_ops = 0, c_exp = 0, c_cancel = 0, c_uns = 0;

  auto compare = [&](uint64_t cyc, const char* phase) {
    const uint64_t m = t->mism_o;
    const bool hm = t->hit_dut_o != t->hit_ref_o;
    if (m || hm) {
      ++mism_cycles;
      for (size_t k = 0; k < names.size(); ++k)
        if ((m >> k) & 1) { ++by_out[k]; ++mism_total; }
      if (hm) { ++hit_mism; ++mism_total; }
      if (printed++ < 8)
        printf("MISMATCH cycle %llu %s mism=0x%llx hit d=0x%llx r=0x%llx\n",
               static_cast<unsigned long long>(cyc), phase,
               static_cast<unsigned long long>(m),
               static_cast<unsigned long long>(t->hit_dut_o),
               static_cast<unsigned long long>(t->hit_ref_o));
    }
  };

  // reset at start
  t->rst_n = 0;
  for (int i = 0; i < 3; ++i) { t->clk_i = 0; t->eval(); t->clk_i = 1; t->eval(); }
  t->rst_n = 1;

  for (uint64_t cyc = 0; cyc < cycles; ++cyc) {
    // ---- drive inputs (clock low) -----------------------------------------
    t->clk_i = 0;
    if (cyc % ms_period == 0) now += 1;
    if (mode == 1 && pct(0.001)) now = static_cast<uint32_t>(rng());
    if (mode == 1 && pct(0.0005)) now = 0xFFFFFFFFu - static_cast<uint32_t>(rnd(3000));
    t->now_ms_i = now;

    // reset: rare, plus aimed at the re-index cycles in mode 2
    if (rst_left > 0) { --rst_left; }
    else if (pct(mode == 1 ? 1.0 / 5000 : 1.0 / 40000)) rst_left = 1 + static_cast<int>(rnd(3));
    else if ((mode == 2 || mode == 3) && (t->cov_clr_o || t->cov_set_o) && pct(mode == 2 ? 0.03 : 0.002))
      rst_left = 1;
    t->rst_n = rst_left > 0 ? 0 : 1;
    if (!t->rst_n) { ++c_rst; if (t->cov_clr_o) ++c_rst_clr; if (t->cov_set_o) ++c_rst_set;
                     if (t->cov_ctr_sent_any_o) ++c_rst_ctr;
                     rgy_phase = 0; uns_wait = -1; prng_wait = -1;
                     for (auto& a : arms) a.on = false; }

    // registry op face
    if (mode == 1) {
      t->rgy_req_i = pct(0.3);
      t->rgy_state_i = pct(0.1);
      t->rgy_op_i = static_cast<uint8_t>(rnd(4));
      const Id id = pick_id();
      t->rgy_eid_i = id.eid; t->rgy_mac_i = id.mac; t->rgy_tl_i = pct(0.5);
    } else {
      t->eval();  // rgy_wait_o for the current state
      if (rgy_phase == 0 && pct(0.02)) {
        rgy_phase = 1; ++c_reg_ops;
        const uint64_t r = rnd(100);
        t->rgy_state_i = r < 4;
        t->rgy_op_i = mode == 3 ? (r < 92 ? 0 : r < 95 ? 1 : r < 98 ? 2 : 3)
                                : (r < 64 ? 0 : r < 84 ? 1 : r < 94 ? 2 : 3);
        const Id id = pool[rnd(pool.size())];
        t->rgy_eid_i = id.eid; t->rgy_mac_i = id.mac; t->rgy_tl_i = pct(0.6);
        t->rgy_req_i = 1;
      } else if (rgy_phase == 1 && !t->rgy_wait_o) {
        rgy_phase = 2; rgy_hold = static_cast<int>(rnd(3));
      } else if (rgy_phase == 2) {
        if (rgy_hold-- <= 0) { t->rgy_req_i = 0; rgy_phase = 0; }
      }
    }

    // availability monitor input
    t->rx_cmd_valid_i = pct(mode == 1 ? 0.5 : 0.3);
    {
      Id id = pick_id();
      if ((mode == 2 || mode == 3) && (t->cov_clr_o || t->cov_set_o || t->cov_wr_en_o) && pct(0.7)) {
        // aim at the written row: the identity rows_r holds there now, or the
        // one being written
        const uint64_t r = rnd(3);
        if (r == 0) id = {t->cov_old_eid_o, t->cov_old_mac_o};
        else if (r == 1) id = {t->cov_new_eid_o, t->cov_new_mac_o};
        else id = pool[rnd(pool.size())];
      }
      t->rx_cmd_eid_i = id.eid; t->rx_cmd_mac_i = id.mac;
    }

    // probe face
    t->ca_ready_i = pct(0.5);
    t->ca_rsp_valid_i = pct(0.04); t->ca_rsp_owner_i = static_cast<uint8_t>(rnd(16));
    t->ca_fail_valid_i = pct(mode == 3 ? 0.0005 : 0.04); t->ca_fail_owner_i = static_cast<uint8_t>(rnd(16));
    if (t->ca_valid_o && pct(0.3)) {
      if (pct(mode == 3 ? 0.98 : 0.5)) { t->ca_rsp_valid_i = 1; t->ca_rsp_owner_i = t->ca_owner_o; }
      else { t->ca_fail_valid_i = 1; t->ca_fail_owner_i = t->ca_owner_o; }
    }

    // PRNG
    t->prng_draw_busy_i = pct(0.2);
    t->prng_draw_valid_i = 0;
    if (mode == 1) { t->prng_draw_valid_i = pct(0.1); t->prng_draw_ms_i = static_cast<uint16_t>(rng()); }
    else {
      if (t->prng_draw_req_o && prng_wait < 0) prng_wait = static_cast<int>(rnd(6));
      if (prng_wait == 0) { t->prng_draw_valid_i = 1;
                            t->prng_draw_ms_i = static_cast<uint16_t>(rnd(pct(0.5) ? 4 : 3000)); }
      if (prng_wait >= 0) --prng_wait;
    }

    // engine job face
    t->uns_done_i = 0;
    if (mode == 1) { t->uns_done_i = pct(0.2); }
    else {
      if (t->uns_valid_o && uns_wait < 0) uns_wait = static_cast<int>(rnd(8));
      if (uns_wait == 0) t->uns_done_i = 1;
      if (uns_wait >= 0) --uns_wait;
    }
    t->uns_tx_busy_i = pct(0.2);

    // events
    t->ev_stri_in_i = pct(0.02) ? static_cast<uint32_t>(rng()) : 0;
    t->ev_stri_out_i = pct(0.02) ? static_cast<uint32_t>(rng()) : 0;
    t->ev_avb_i = pct(0.01); t->ev_asp_i = pct(0.01);
    t->ev_amap_i = pct(0.01); t->ev_amap_remove_i = pct(0.5);
    t->ev_amap_type_i = static_cast<uint16_t>(rnd(8)); t->ev_amap_index_i = static_cast<uint16_t>(rnd(4));
    t->ev_amap_count_i = static_cast<uint16_t>(rnd(8));
    t->ev_amap_excl_eid_i = pool[rnd(pool.size())].eid;
    t->ev_ctr_i = pct(mode == 1 ? 0.2 : 0.05);
    { static const uint16_t types[] = {0x0005, 0x0006, 0x0009, 0x0024, 0x0000, 0x0007};
      t->ev_ctr_type_i = types[rnd(6)]; t->ev_ctr_index_i = static_cast<uint16_t>(rnd(pct(0.9) ? 9 : 65536)); }
    t->ev_cmd_i = pct(0.02); t->ev_cmd_class_i = static_cast<uint8_t>(rnd(16));
    t->ev_cmd_type_i = static_cast<uint16_t>(rng()); t->ev_cmd_index_i = static_cast<uint16_t>(rng());
    t->ev_cmd_arg0_i = static_cast<uint16_t>(rng()); t->ev_cmd_arg1_i = static_cast<uint16_t>(rng());
    t->ev_cmd_excl_eid_i = pool[rnd(pool.size())].eid;
    if (ident_hold-- <= 0) { t->identify_button_i = pct(0.3); ident_hold = static_cast<int>(rnd(2000)); }
    t->identify_index_i = static_cast<uint16_t>(rnd(4));

    // timer expiry: armed slots fire at or after their deadline, sometimes early
    t->tmr_exp_valid_i = 0;
    if (mode == 1 && pct(0.05)) {
      t->tmr_exp_valid_i = 1; t->tmr_exp_slot_i = static_cast<uint8_t>(rnd(128));
      static const uint8_t own[] = {0xA0, 0xB0, 0xB1, 0xB2, 0xD0};
      t->tmr_exp_owner_i = static_cast<uint8_t>(own[rnd(5)] + ((own[0] == 0) ? 0 : rnd(16)));
    } else if (pct(0.3)) {
      const int s0 = static_cast<int>(rnd(128));
      for (int k = 0; k < 128; ++k) {
        Arm& a = arms[(s0 + k) % 128];
        if (a.on && (static_cast<int32_t>(now - a.deadline) >= 0 || pct(mode == 3 ? 0.0002 : 0.01))) {
          t->tmr_exp_valid_i = 1; t->tmr_exp_slot_i = static_cast<uint8_t>((s0 + k) % 128);
          t->tmr_exp_owner_i = a.owner; a.on = false; ++c_exp; break;
        }
      }
    }

    t->eval();
    compare(cyc, "low");

    // coverage at the decision point (before the edge)
    if (t->rx_cmd_valid_i && t->rst_n) {
      const uint64_t h = t->hit_ref_o;
      if (h) ++c_hits;
      if (t->cov_clr_o) { ++c_cmd_clr; if ((h >> t->cov_wr_ix_o) & 1) { ++c_hit_wr_clr;
                                         if (t->cov_idchg_o) ++c_oldhit_clr; } }
      if (t->cov_set_o) { ++c_cmd_set; if ((h >> t->cov_wr_ix_o) & 1) ++c_hit_wr_set; }
    }
    if (t->cov_clr_o && t->cov_idchg_o) ++c_idchg_clr;
    if (t->cov_wr_en_o && t->cov_rd_ix_o == t->cov_wr_ix_o) ++c_walk_coll;
    if (t->cov_wr_en_o && t->ca_valid_o && t->ca_owner_o == t->cov_wr_ix_o) ++c_ca_coll;
    if (t->cov_st_o == 7) ++c_emit_wb;
    if (t->uns_valid_o && t->uns_done_i && t->rst_n) ++c_uns;

    // ---- rising edge --------------------------------------------------------
    t->clk_i = 1;
    t->eval();
    compare(cyc, "high");

    // record arms issued by this edge (registered outputs)
    if (t->tmr_arm_valid_o) {
      Arm& a = arms[t->tmr_arm_slot_o & 127];
      if (t->tmr_arm_cancel_o) { a.on = false; ++c_cancel; }
      else { a.on = true; a.owner = t->tmr_arm_owner_o; a.deadline = t->tmr_arm_deadline_ms_o; }
    }
    if (t->mon_arm_valid_o) {
      Arm& a = arms[t->mon_arm_slot_o & 127];
      if (t->mon_arm_cancel_o) { a.on = false; ++c_cancel; }
      else { a.on = true; a.owner = t->mon_arm_owner_o; a.deadline = t->mon_arm_deadline_ms_o; }
    }
    if (t->dbg_reg_cnt_o >= n_ctrl_arg) ++c_full;
  }

  printf("seed %llu mode %d cycles %llu ms_period %llu\n", static_cast<unsigned long long>(seed),
         mode, static_cast<unsigned long long>(cycles), static_cast<unsigned long long>(ms_period));
  printf("coverage: reg_ops %llu cmd_hits %llu cmd_in_clr %llu cmd_in_set %llu "
         "hit_on_written_row_clr %llu (old_identity %llu) hit_on_written_row_set %llu "
         "identity_changing_clr %llu resets %llu reset_in_clr %llu reset_in_set %llu "
         "reset_with_stamp_valid %llu walk_read_eq_write %llu probe_pick_eq_write %llu "
         "full_cycles %llu emit_wb %llu expiries %llu cancels %llu uns_jobs %llu\n",
         (unsigned long long)c_reg_ops, (unsigned long long)c_hits, (unsigned long long)c_cmd_clr,
         (unsigned long long)c_cmd_set, (unsigned long long)c_hit_wr_clr,
         (unsigned long long)c_oldhit_clr, (unsigned long long)c_hit_wr_set,
         (unsigned long long)c_idchg_clr, (unsigned long long)c_rst, (unsigned long long)c_rst_clr,
         (unsigned long long)c_rst_set, (unsigned long long)c_rst_ctr,
         (unsigned long long)c_walk_coll, (unsigned long long)c_ca_coll,
         (unsigned long long)c_full, (unsigned long long)c_emit_wb, (unsigned long long)c_exp,
         (unsigned long long)c_cancel, (unsigned long long)c_uns);
  printf("mismatches %llu in %llu compare points; rx_cmd_hit_w %llu\n",
         (unsigned long long)mism_total, (unsigned long long)mism_cycles, (unsigned long long)hit_mism);
  for (size_t k = 0; k < names.size(); ++k)
    if (by_out[k]) printf("  %s %llu\n", names[k].c_str(), (unsigned long long)by_out[k]);
  printf("RESULT %s\n", mism_total ? "MISMATCH" : "MATCH");
  return mism_total ? 1 : 0;
}

// Reviewer lockstep driver for lockstep_top.sv (main's KL_aecp_notify beside
// the candidate's). Usage: Vlockstep SEED CYCLES MODE
//   MODE 0: protocol-shaped (registry handshakes, done after valid, ms ticks)
//   MODE 1: every input random each cycle (identities still from a small pool)
// Exit 0: no mismatch. Exit 1: mismatch (first one printed). Exit 2: usage.
// Verdict: mismatch_o (every output + rx_cmd_hit_w) at both clock phases.
#include "Vlockstep_top.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

#ifndef N_CTRL
#error "N_CTRL must be defined"
#endif

struct Id { uint64_t eid; uint64_t mac; };
static bool operator==(const Id& a, const Id& b) { return a.eid == b.eid && a.mac == b.mac; }

// bit b of the 112-bit {eid, mac} (mac is bits 0..47)
static Id flip_bit(Id x, int b) {
  if (b < 48) x.mac ^= (1ull << b); else x.eid ^= (1ull << (b - 48));
  return x;
}
// overwrite 6-bit chunk j (bits 6j..6j+5, clipped at bit 111) with v
static Id set_chunk(Id x, int j, unsigned v) {
  for (int k = 0; k < 6; ++k) {
    int b = 6 * j + k;
    if (b >= 112) break;
    bool want = (v >> k) & 1u;
    bool have = b < 48 ? ((x.mac >> b) & 1u) : ((x.eid >> (b - 48)) & 1u);
    if (want != have) x = flip_bit(x, b);
  }
  return x;
}
template <typename W> static Id id_from_wide(const W& w) {   // 112-bit output, 4 words
  Id r;
  uint64_t lo = (uint64_t)w[0] | ((uint64_t)w[1] << 32);
  uint64_t hi = (uint64_t)w[2] | ((uint64_t)w[3] << 32);
  r.mac = lo & 0xFFFFFFFFFFFFull;
  r.eid = (lo >> 48) | (hi << 16);
  return r;
}

int main(int argc, char** argv) {
  if (argc < 4) { fprintf(stderr, "usage: %s SEED CYCLES MODE\n", argv[0]); return 2; }
  const uint64_t seed = strtoull(argv[1], nullptr, 0);
  const uint64_t cycles = strtoull(argv[2], nullptr, 0);
  const int mode = atoi(argv[3]);
  Verilated::commandArgs(1, argv);
  std::mt19937_64 rng(seed * 0x9E3779B97F4A7C15ull + 12345);
  auto U = [&](uint64_t n) { return n ? rng() % n : 0; };
  auto P = [&](double p) { return std::uniform_real_distribution<double>(0, 1)(rng) < p; };

  // identity pool: chunk-sharing families so a stale or doubled index row
  // would mix chunks into a false match
  std::vector<Id> pool;
  Id a{rng(), rng() & 0xFFFFFFFFFFFFull};
  int k1 = (int)U(19), k2 = (int)((k1 + 1 + U(18)) % 19);
  Id a1 = set_chunk(a, k1, (unsigned)(rng() & 63)), a2 = set_chunk(a, k2, (unsigned)(rng() & 63));
  Id a12;
  { // a12 takes a1's k1 chunk and a2's k2 chunk: a doubled index row would match it
    Id t = a1; for (int b = 6 * k2; b < 6 * k2 + 6 && b < 112; ++b) {
      bool v2 = b < 48 ? ((a2.mac >> b) & 1u) : ((a2.eid >> (b - 48)) & 1u);
      bool vt = b < 48 ? ((t.mac >> b) & 1u) : ((t.eid >> (b - 48)) & 1u);
      if (v2 != vt) t = flip_bit(t, b);
    }
    a12 = t;
  }
  Id b{rng(), rng() & 0xFFFFFFFFFFFFull};
  Id b18 = set_chunk(b, 18, (unsigned)(((b.eid >> 60) ^ 0x5) & 0xF));
  Id z{0, 0};
  pool = {a, a1, a2, a12, b, b18, z};
  for (int i = 0; i < 12; ++i) pool.push_back(Id{rng(), rng() & 0xFFFFFFFFFFFFull});
  const size_t hot = 7;   // the first seven are drawn most often

  auto pick_id = [&]() -> Id {
    uint64_t r = U(100);
    if (r < 70) return pool[U(hot)];
    if (r < 85) return flip_bit(pool[U(hot)], (int)U(112));
    if (r < 95) return pool[U(pool.size())];
    return Id{rng(), rng() & 0xFFFFFFFFFFFFull};
  };

  Vlockstep_top* t = new Vlockstep_top;
  const int N = N_CTRL;
  const uint8_t own_ntfy = 0xA0, own_lock = 0xB0, own_cmon = 0xD0, own_ident = 0xB1;

  // protocol state
  int rgy_phase = 0, rgy_hold = 0;
  int done_delay = -1;
  uint32_t now = (uint32_t)rng();
  if (P(0.3)) now = 0xFFFFFFFFu - (uint32_t)U(200000);   // wrap inside the run
  const int ms_period = 2 + (int)U(19);
  int ms_count = 0;
  int rst_left = 3;
  bool button = false;

  // coverage
  uint64_t cov_claim_change = 0, cov_reg_same = 0, cov_cmd_clr = 0, cov_cmd_set = 0;
  uint64_t cov_hit_clr = 0, cov_hit_set = 0, cov_old_id_clr = 0, cov_old_hit_clr = 0;
  uint64_t cov_new_id_set = 0, cov_rst_clr = 0, cov_rst_set = 0, cov_hits = 0;
  uint64_t cov_rst = 0, cov_wb_win = 0, cov_ca_valid = 0, cov_drain_like = 0;
  uint64_t mismatches = 0, first_mm = 0;

  auto compare = [&](uint64_t cyc, const char* ph) {
    if (!t->mismatch_o) return;
    if (mismatches == 0) {
      first_mm = cyc;
      fprintf(stderr, "MISMATCH seed %llu cycle %llu phase %s\n",
              (unsigned long long)seed, (unsigned long long)cyc, ph);
      fprintf(stderr, "  ref_hit %llx dut_hit %llx\n",
              (unsigned long long)t->ref_hit_o, (unsigned long long)t->dut_hit_o);
      const int words = (int)(sizeof(t->ref_out_o) / sizeof(uint32_t));
      for (int w = words - 1; w >= 0; --w)
        if (t->ref_out_o[w] != t->dut_out_o[w])
          fprintf(stderr, "  out word %d ref %08x dut %08x\n", w, t->ref_out_o[w], t->dut_out_o[w]);
    }
    ++mismatches;
  };

  for (uint64_t cyc = 0; cyc < cycles; ++cyc) {
    // ---- reset: rare, and biased into the candidate's re-index window ----
    bool in_clr = t->dut_ix_clr_o, in_set = t->dut_ix_set_o;
    if (rst_left == 0) {
      if (P(1.0 / 20000)) rst_left = 1 + (int)U(3);
      else if ((in_clr || in_set) && P(1.0 / 40)) rst_left = 1 + (int)U(2);
    }
    t->rst_n = rst_left ? 0 : 1;
    if (rst_left) { ++cov_rst; if (in_clr) ++cov_rst_clr; if (in_set) ++cov_rst_set; --rst_left; }

    // ---- registry face ----
    if (mode == 0) {
      if (rgy_phase == 0) {
        t->rgy_req_i = 0;
        if (P(0.02)) {
          rgy_phase = 1;
          t->rgy_req_i = 1;
          uint64_t r = U(100);
          t->rgy_state_i = r < 5;
          t->rgy_op_i = r < 55 ? 0 : (r < 80 ? 1 : (r < 90 ? 2 : 3));
          Id x = pick_id();
          t->rgy_eid_i = x.eid; t->rgy_mac_i = x.mac;
          t->rgy_tl_i = P(0.3);
        }
      } else if (rgy_phase == 2) {
        if (rgy_hold-- <= 0) { t->rgy_req_i = 0; rgy_phase = 0; }
      }
    } else {
      t->rgy_req_i = P(0.1);
      t->rgy_state_i = P(0.1);
      t->rgy_op_i = (uint8_t)U(4);
      Id x = pick_id();
      t->rgy_eid_i = x.eid; t->rgy_mac_i = x.mac;
      t->rgy_tl_i = P(0.5);
    }

    // ---- events ----
    t->ev_stri_in_i  = P(0.002) ? (uint32_t)rng() : 0;
    t->ev_stri_out_i = P(0.002) ? (uint32_t)rng() : 0;
    t->ev_avb_i = P(0.002); t->ev_asp_i = P(0.002);
    t->ev_amap_i = P(0.002); t->ev_amap_remove_i = P(0.5);
    t->ev_amap_type_i = (uint16_t)rng(); t->ev_amap_index_i = (uint16_t)rng();
    t->ev_amap_count_i = (uint16_t)rng();
    t->ev_amap_excl_eid_i = P(0.5) ? pool[U(hot)].eid : rng();
    t->ev_ctr_i = P(mode == 0 ? 0.01 : 0.05);
    { static const uint16_t types[4] = {0x0005, 0x0006, 0x0009, 0x0024};
      t->ev_ctr_type_i = P(0.9) ? types[U(4)] : (uint16_t)rng();
      t->ev_ctr_index_i = (uint16_t)(P(0.85) ? U(10) : rng()); }
    t->ev_cmd_i = P(0.003); t->ev_cmd_class_i = (uint8_t)U(16);
    t->ev_cmd_type_i = (uint16_t)rng(); t->ev_cmd_index_i = (uint16_t)rng();
    t->ev_cmd_arg0_i = (uint16_t)rng(); t->ev_cmd_arg1_i = (uint16_t)rng();
    t->ev_cmd_excl_eid_i = P(0.5) ? pool[U(hot)].eid : rng();
    if (P(0.0005)) button = !button;
    t->identify_button_i = mode == 0 ? button : P(0.5);
    t->identify_index_i = (uint16_t)U(4);

    // ---- availability monitor ----
    t->rx_cmd_valid_i = P(mode == 0 ? 0.3 : 0.5);
    { Id x = pick_id(); t->rx_cmd_eid_i = x.eid; t->rx_cmd_mac_i = x.mac; }
    // bias: during the window, often present the row's old or new identity
    if ((in_clr || in_set) && P(0.6)) {
      Id oldid = id_from_wide(t->dut_wr_row_id_o);
      Id newid = id_from_wide(t->dut_wr_new_id_o);
      Id x = P(0.5) ? oldid : newid;
      t->rx_cmd_eid_i = x.eid; t->rx_cmd_mac_i = x.mac; t->rx_cmd_valid_i = 1;
    }
    t->prng_draw_busy_i = P(0.2);
    t->prng_draw_valid_i = P(0.1);
    t->prng_draw_ms_i = (uint16_t)(30000 + U(30001));
    t->ca_ready_i = P(0.5);
    auto owner = [&]() { return (uint8_t)(P(0.9) ? U((uint64_t)N) : U(16)); };
    t->ca_rsp_valid_i = P(0.01); t->ca_rsp_owner_i = owner();
    t->ca_fail_valid_i = P(0.01); t->ca_fail_owner_i = owner();
    if ((in_clr || in_set) && P(0.2)) { t->ca_fail_valid_i = 1; t->ca_fail_owner_i = t->dut_wr_ix_o; }

    // ---- unsolicited face ----
    if (mode == 0) {
      t->uns_done_i = 0;
      if (t->uns_valid_ref_o) {
        if (done_delay < 0) done_delay = (int)U(9);
        else if (done_delay-- == 0) { t->uns_done_i = 1; done_delay = -1; }
      } else done_delay = -1;
    } else {
      t->uns_done_i = P(0.2);
    }
    t->uns_tx_busy_i = P(0.2);

    // ---- time and timer expiries ----
    if (mode == 0) {
      if (++ms_count >= ms_period) { ms_count = 0; ++now; }
      if (P(0.0002)) now = (uint32_t)rng();
    } else {
      if (P(0.3)) now += (uint32_t)U(3);
      if (P(0.001)) now = (uint32_t)rng();
    }
    t->now_ms_i = now;
    t->tmr_exp_valid_i = P(mode == 0 ? 0.01 : 0.05);
    { uint64_t r = U(100); uint8_t ix = (uint8_t)U((uint64_t)N);
      if (r < 35)      { t->tmr_exp_owner_i = own_ntfy | ix; t->tmr_exp_slot_i = 25 + ix; }
      else if (r < 70) { t->tmr_exp_owner_i = own_cmon | ix; t->tmr_exp_slot_i = 25 + N + ix; }
      else if (r < 80) { t->tmr_exp_owner_i = own_lock; t->tmr_exp_slot_i = 61; }
      else if (r < 90) { uint8_t k = (uint8_t)U(2); t->tmr_exp_owner_i = own_ident + k; t->tmr_exp_slot_i = 62 + k; }
      else             { t->tmr_exp_owner_i = (uint8_t)rng(); t->tmr_exp_slot_i = (uint8_t)U(128); } }

    // ---- evaluate, compare, coverage (pre-edge) ----
    t->clk_i = 0;
    t->eval();
    compare(cyc, "pre");
    if (t->rx_cmd_valid_i) {
      int wix = t->dut_wr_ix_o;
      Id cmd{t->rx_cmd_eid_i, t->rx_cmd_mac_i};
      Id oldid = id_from_wide(t->dut_wr_row_id_o);
      Id newid = id_from_wide(t->dut_wr_new_id_o);
      bool hitw = (t->ref_hit_o >> wix) & 1u;
      if (t->dut_ix_clr_o) {
        ++cov_cmd_clr; if (hitw) ++cov_hit_clr;
        if (cmd == oldid && !(oldid == newid)) { ++cov_old_id_clr; if (hitw) ++cov_old_hit_clr; }
      }
      if (t->dut_ix_set_o) { ++cov_cmd_set; if (hitw) ++cov_hit_set; if (cmd == newid) ++cov_new_id_set; }
      if (t->ref_hit_o) ++cov_hits;
    }
    if (t->dut_ix_clr_o) {
      Id oldid = id_from_wide(t->dut_wr_row_id_o), newid = id_from_wide(t->dut_wr_new_id_o);
      if (oldid == newid) ++cov_reg_same; else ++cov_claim_change;
    }
    if (t->dut_wr_en_o && !t->dut_ix_clr_o && (in_clr || in_set)) ++cov_wb_win;
    if (mode == 0 && rgy_phase == 1 && t->rgy_wait_ref_o == 0) {
      rgy_phase = 2; rgy_hold = (int)U(3);
    }
    // ---- clock edge, compare again ----
    t->clk_i = 1;
    t->eval();
    compare(cyc, "post");
  }
  t->final();
  printf("seed %llu mode %d N_CTRL %d cycles %llu mismatches %llu first %llu | "
         "re-index id-change %llu same-id %llu | cmd in clear %llu (row hit %llu, old id %llu, old-id hit %llu) | "
         "cmd in set %llu (row hit %llu, new id %llu) | resets %llu (in clear %llu, in set %llu) | "
         "hits %llu | other writes in window %llu\n",
         (unsigned long long)seed, mode, N, (unsigned long long)cycles,
         (unsigned long long)mismatches, (unsigned long long)first_mm,
         (unsigned long long)cov_claim_change, (unsigned long long)cov_reg_same,
         (unsigned long long)cov_cmd_clr, (unsigned long long)cov_hit_clr,
         (unsigned long long)cov_old_id_clr, (unsigned long long)cov_old_hit_clr,
         (unsigned long long)cov_cmd_set, (unsigned long long)cov_hit_set,
         (unsigned long long)cov_new_id_set, (unsigned long long)cov_rst,
         (unsigned long long)cov_rst_clr, (unsigned long long)cov_rst_set,
         (unsigned long long)cov_hits, (unsigned long long)cov_wb_win);
  (void)cov_ca_valid; (void)cov_drain_like;
  delete t;
  return mismatches ? 1 : 0;
}

// Scratch (never committed): lockstep bench for issue #230.
// KL_srp_top_ref (base RTL) and KL_srp_top (RTL under test) share every input
// every cycle; lockstep_top raises diff_o (top outputs) and idiff_o (internal
// faces) on any difference. The environment is driven from the ref's faces:
// a timer-service model (arm/cancel/expire, plus spurious expiries), a PRNG
// model, a TX-slot pool model, the class-B service port and a generator of
// MRPDUs drawn from shared value pools so that declarations and received
// attributes match. Resets land at random mid-run.
//
// usage: Vlockstep <seed> <cycles> [mode]   mode 0 = protocol-shaped, 1 = noisy, 2 = frequent resets
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <map>
#include <random>
#include <string>
#include <vector>

#include "Vlockstep_top.h"
#include "verilated.h"

#ifndef N_SRC
#error N_SRC
#endif
#ifndef N_SNK
#error N_SNK
#endif
#ifndef SLOT_AW
#error SLOT_AW
#endif

static std::mt19937_64 rng;
static uint64_t rnd(uint64_t n) { return n ? rng() % n : 0; }
static bool chance(double p) { return std::uniform_real_distribution<double>(0, 1)(rng) < p; }

// ---- value pools (shared by declarations and received attributes) --------
static const uint64_t SIDS[] = {0x0011223344550000ull, 0x0011223344550001ull,
                                0x0011223344550002ull, 0x0011223344550003ull,
                                0x00AABBCCDDEE0007ull, 0x0011223344550005ull};
static const uint64_t DAS[] = {0x91E0F0000E00ull, 0x91E0F0000E01ull,
                               0x91E0F0000E02ull, 0x91E0F000FE80ull};
static const uint16_t VIDS[] = {2, 3, 2, 0x123, 5};
static const uint64_t SYSIDS[] = {0x0000001122334455ull, 0x8000AABBCCDDEEFFull, 0};
static uint64_t pick_sid() { return SIDS[rnd(6)]; }
static uint64_t pick_da() { return DAS[rnd(4)]; }
static uint16_t pick_vid() { return VIDS[rnd(5)]; }
static uint16_t pick_mfs() {
  switch (rnd(6)) {
    case 0: return static_cast<uint16_t>(rnd(64));
    case 1: return 224;
    case 2: return static_cast<uint16_t>(rnd(1600));
    case 3: return 0xFFFF;
    case 4: return 72;
    default: return static_cast<uint16_t>(rng());
  }
}

static void put16(std::vector<uint8_t>& b, uint16_t v) { b.push_back(v >> 8); b.push_back(v & 0xFF); }
static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
  for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

struct Triple { uint64_t sid; uint64_t da; uint16_t vid; };
static std::vector<Triple> recent_tk, recent_ls;   // declared talkers, settled listeners
static void remember(std::vector<Triple>& v, Triple x) { if (v.size() >= 8) v.erase(v.begin()); v.push_back(x); }

struct Vec { bool la; int nov; std::vector<uint8_t> fv; std::vector<int> ev; std::vector<int> fp; };

static std::vector<uint8_t> fv_for(bool msrp, int type) {
  std::vector<uint8_t> b;
  if (!msrp) { put16(b, chance(0.8) ? pick_vid() : static_cast<uint16_t>(rnd(4096))); return b; }
  if (type == 1 || type == 2) {
    if (!recent_ls.empty() && chance(0.6)) {
      const Triple& x = recent_ls[rnd(recent_ls.size())];
      put_be(b, x.sid, 8); put_be(b, x.da, 6); put16(b, x.vid);
    } else {
      put_be(b, pick_sid(), 8); put_be(b, pick_da(), 6);
      put16(b, chance(0.9) ? pick_vid() : static_cast<uint16_t>(rng()));
    }
    put16(b, pick_mfs()); put16(b, chance(0.8) ? 1 : static_cast<uint16_t>(rnd(4)));
    b.push_back(static_cast<uint8_t>((rnd(8) << 5) | (rnd(2) << 4)));
    static const uint32_t LATS[] = {0, 1000, 125000, 0xFFFFFFFFu};
    put_be(b, chance(0.7) ? LATS[rnd(4)] : static_cast<uint32_t>(rng()), 4);
    if (type == 2) { put_be(b, SYSIDS[rnd(3)], 8); b.push_back(static_cast<uint8_t>(rnd(4) ? 1 + rnd(3) : rng())); }
  } else if (type == 3) {
    put_be(b, !recent_tk.empty() && chance(0.6) ? recent_tk[rnd(recent_tk.size())].sid : pick_sid(), 8);
  } else {  // Domain
    b.push_back(chance(0.8) ? 6 : static_cast<uint8_t>(rnd(8)));
    b.push_back(static_cast<uint8_t>(chance(0.7) ? 3 : rnd(8)));
    put16(b, chance(0.8) ? pick_vid() : static_cast<uint16_t>(rnd(4096)));
  }
  return b;
}

static std::vector<uint8_t> make_pdu(bool msrp, bool noisy) {
  static const int ALEN[5] = {0, 25, 34, 8, 4};
  std::vector<uint8_t> b;
  b.push_back(0x00);
  int nmsg = 1 + static_cast<int>(rnd(3));
  for (int m = 0; m < nmsg; m++) {
    int type = msrp ? 1 + static_cast<int>(rnd(4)) : 1;
    int alen = msrp ? ALEN[type] : 2;
    bool listener = msrp && type == 3;
    b.push_back(static_cast<uint8_t>(type));
    b.push_back(static_cast<uint8_t>(alen));
    std::vector<uint8_t> body;
    int nvec = 1 + static_cast<int>(rnd(2));
    for (int v = 0; v < nvec; v++) {
      Vec x;
      x.la = chance(0.08);
      x.nov = x.la && chance(0.3) ? 0 : 1 + static_cast<int>(rnd(chance(0.8) ? 2 : 5));
      x.fv = fv_for(msrp, type);
      for (int i = 0; i < x.nov; i++) {
        x.ev.push_back(noisy && chance(0.02) ? 6 : static_cast<int>(rnd(6)));
        x.fp.push_back(static_cast<int>(rnd(4)));
      }
      body.push_back((x.la ? 0x20 : 0x00) | ((x.nov >> 8) & 0x1F));
      body.push_back(x.nov & 0xFF);
      body.insert(body.end(), x.fv.begin(), x.fv.end());
      for (int i = 0; i < x.nov; i += 3) {
        int e[3] = {0, 0, 0};
        for (int j = 0; j < 3 && i + j < x.nov; j++) e[j] = x.ev[i + j];
        body.push_back(static_cast<uint8_t>(((e[0] * 6) + e[1]) * 6 + e[2]));
      }
      if (listener) {
        for (int i = 0; i < x.nov; i += 4) {
          int p[4] = {0, 0, 0, 0};
          for (int j = 0; j < 4 && i + j < x.nov; j++) p[j] = x.fp[i + j];
          body.push_back(static_cast<uint8_t>(p[0] * 64 + p[1] * 16 + p[2] * 4 + p[3]));
        }
      }
    }
    if (msrp) put16(b, static_cast<uint16_t>(body.size() + 2));
    b.insert(b.end(), body.begin(), body.end());
    put16(b, 0x0000);
  }
  put16(b, 0x0000);
  if (noisy && chance(0.05)) b[rnd(b.size())] = static_cast<uint8_t>(rng());
  if (noisy && chance(0.03)) b.resize(1 + rnd(b.size()));
  return b;
}

int main(int argc, char** argv) {
  if (argc < 3) { std::fprintf(stderr, "usage: %s seed cycles [mode]\n", argv[0]); return 2; }
  uint64_t seed = std::strtoull(argv[1], nullptr, 0);
  uint64_t cycles = std::strtoull(argv[2], nullptr, 0);
  int mode = argc > 3 ? std::atoi(argv[3]) : 0;
  rng.seed(seed);
  Verilated::randReset(2);
  Verilated::randSeed(static_cast<int>(seed & 0x7FFFFFFF));
  auto* t = new Vlockstep_top;

  const uint32_t ms_cyc = 8 + static_cast<uint32_t>(rnd(40));
  const double p_pdu = mode ? 0.02 : 0.004 + 0.01 * (rnd(100) / 100.0);
  const double p_req = 0.002 + 0.02 * (rnd(100) / 100.0);
  const double p_rst = mode == 2 ? 3e-5 : 3e-6;   // mode 2: frequent mid-run resets
  t->own_mac_i = 0x001B21AABBCCull ^ (rng() & 0xFFFF);
  t->p2p_i = chance(0.85);
  t->cfg_rank_i = chance(0.5);
  t->cfg_acc_lat_ns_i = static_cast<uint32_t>(chance(0.5) ? 500 : rng());
  static const uint32_t RATES[] = {1000000000u, 100000000u, 10000000u, 0xFFFFFFFCu};
  t->port_rate_bps_i = RATES[rnd(4)];
  t->link_up_i = 1;

  // environment state
  std::deque<std::pair<uint8_t, bool>> mrpq;  // (byte, last)
  bool mrp_msrp = true;
  uint32_t now_ms = static_cast<uint32_t>(chance(0.5) ? rng() : 0);
  uint32_t ms_div = 0;
  std::map<uint32_t, uint32_t> armed;  // slot -> deadline
  int gnt_wait = -1;
  int draw_wait = -1;
  bool req_active = false;
  int rst_hold = 6;
  uint64_t first_bad = 0, bad = 0, ibad = 0;
  uint64_t diff_or = 0, idiff_or = 0;
  uint64_t n_rst = 0, n_regarm = 0, n_arm = 0, n_exp = 0, n_rsp = 0, n_commit = 0, n_pdu = 0, n_tkreg = 0, n_gnt = 0, n_txacc = 0, n_active = 0, n_wr = 0;

  for (uint64_t cyc = 0; cyc < cycles; cyc++) {
    // ---------------- inputs for this cycle ----------------
    if (rst_hold == 0 && chance(p_rst)) { rst_hold = 2 + static_cast<int>(rnd(8)); n_rst++; }
    bool in_rst = rst_hold > 0;
    if (rst_hold > 0) rst_hold--;
    t->rst_n = !in_rst;
    if (in_rst) { armed.clear(); gnt_wait = -1; draw_wait = -1; req_active = false; }
    if (chance(2e-6)) t->link_up_i = !t->link_up_i;
    if (chance(1e-6)) t->p2p_i = !t->p2p_i;
    if (chance(1e-6)) t->port_rate_bps_i = RATES[rnd(4)];
    if (chance(1e-6)) t->cfg_acc_lat_ns_i = static_cast<uint32_t>(rng());

    if (++ms_div >= ms_cyc) { ms_div = 0; now_ms++; }
    t->now_ms_i = now_ms;

    // MRP byte stream
    if (mrpq.empty() && chance(p_pdu)) {
      mrp_msrp = chance(0.75);
      auto pdu = make_pdu(mrp_msrp, mode == 1 || chance(0.1));
      for (size_t i = 0; i < pdu.size(); i++) mrpq.emplace_back(pdu[i], i + 1 == pdu.size());
      n_pdu++;
    }
    bool mrp_v = !mrpq.empty() && !chance(0.05);
    t->mrp_valid_i = mrp_v;
    t->mrp_data_i = mrp_v ? mrpq.front().first : static_cast<uint8_t>(rng());
    t->mrp_last_i = mrp_v ? mrpq.front().second : chance(0.5);
    t->mrp_msrp_i = mrp_msrp;

    // class-B service port: offer one request, hold until accepted
    if (!req_active && chance(p_req)) {
      req_active = true;
      int r = static_cast<int>(rnd(100));
      t->req_op_i = r < 35 ? 0 : r < 50 ? 1 : r < 80 ? 2 : r < 92 ? 3 : r < 97 ? 4 : 5 + static_cast<int>(rnd(3));
      t->req_index_i = chance(0.9) ? static_cast<uint8_t>(rnd(t->req_op_i >= 2 ? N_SNK : N_SRC))
                                   : static_cast<uint8_t>(chance(0.5) ? 6 : rng());
      t->req_stream_id_i = pick_sid();
      t->req_da_i = pick_da();
      t->req_vid_i = pick_vid() & 0xFFF;
      t->req_max_frame_i = pick_mfs();
      t->req_max_interval_i = chance(0.8) ? 1 : static_cast<uint16_t>(rnd(5));
      t->req_lstn_state_i = static_cast<uint8_t>(chance(0.7) ? 2 : rnd(4));
      Triple x{t->req_stream_id_i, t->req_da_i, static_cast<uint16_t>(t->req_vid_i)};
      if (t->req_op_i == 0) remember(recent_tk, x);
      if (t->req_op_i == 2) remember(recent_ls, x);
    }
    t->req_valid_i = req_active;

    // TX-slot pool and arbiter
    t->alloc_gnt_i = 0;
    if (gnt_wait > 0) gnt_wait--;
    if (gnt_wait == 0) { t->alloc_gnt_i = 1; t->alloc_slot_i = static_cast<uint8_t>(rnd(7)); gnt_wait = -1; }
    t->txreq_ready_i = chance(0.3);

    // timer service: expire the lowest due slot, else a spurious expiry
    t->exp_valid_i = 0;
    for (auto it = armed.begin(); it != armed.end(); ++it) {
      if (static_cast<int32_t>(now_ms - it->second) >= 0 && chance(0.5)) {
        t->exp_valid_i = 1; t->exp_slot_i = it->first; armed.erase(it); n_exp++; break;
      }
    }
    if (!t->exp_valid_i && chance(mode ? 1e-3 : 1e-4)) {
      t->exp_valid_i = 1; t->exp_slot_i = static_cast<uint8_t>(rnd(1u << SLOT_AW));
    }
    // PRNG
    t->draw_valid_i = 0;
    t->draw_busy_i = draw_wait >= 0;
    if (draw_wait > 0) draw_wait--;
    else if (draw_wait == 0) {
      t->draw_valid_i = 1;
      t->draw_ms_i = static_cast<uint16_t>(chance(0.85) ? 3 + rnd(120) : 10000 + rnd(5001));
      draw_wait = -1;
    }

    // ---------------- settle and compare ----------------
    t->clk_i = 0;
    t->eval();
    if (cyc > 0 && (t->diff_o || t->idiff_o)) {
      if (!bad && !ibad) first_bad = cyc;
      if (t->diff_o) bad++;
      if (t->idiff_o) ibad++;
      diff_or |= t->diff_o;
      idiff_or |= t->idiff_o;
    }

    // sample the ref's handshakes before the edge
    bool mrp_pop = t->mrp_valid_i && t->mrp_ready_o;
    bool req_acc = t->req_valid_i && t->req_ready_o;
    bool alloc_req = t->alloc_req_o;
    bool draw_req = t->draw_req_o;
    bool armv = t->arm_valid_o;
    bool arm_cancel = t->arm_cancel_o;
    uint32_t arm_slot = t->arm_slot_o, arm_dl = t->arm_deadline_ms_o;
    if (t->txreq_valid_o && t->txreq_ready_i) n_txacc++;
    if (t->wr_valid_o) n_wr++;

    t->clk_i = 1;
    t->eval();

    if (mrp_pop) mrpq.pop_front();
    if (req_acc) req_active = false;
    if (!in_rst) {
      if (alloc_req && gnt_wait < 0 && !t->alloc_gnt_i) gnt_wait = 1 + static_cast<int>(rnd(6));
      if (draw_req && draw_wait < 0) draw_wait = 2 + static_cast<int>(rnd(12));
      if (armv) {
        n_arm++;
        if (arm_slot >= 8) n_regarm++;
        if (arm_cancel) armed.erase(arm_slot);
        else armed[arm_slot] = arm_dl;
      }
      if (t->rsp_valid_o) n_rsp++;
      if (t->wr_commit_o) n_commit++;
      if (t->evt_tk_registered_o) n_tkreg++;
      if (t->alloc_gnt_i) n_gnt++;
      if (t->active_o) n_active++;
    }
  }
  std::printf("seed=%llu cycles=%llu N=%d/%d mode=%d ms_cyc=%u pdus=%llu arms=%llu expiries=%llu rsps=%llu commits=%llu tkreg=%llu "
              "resets=%llu regarms=%llu gnts=%llu txacc=%llu wrbytes=%llu active_cycles=%llu mismatch_cycles=%llu internal_mismatch_cycles=%llu first=%lld diff_mask=0x%llx idiff_mask=0x%llx\n",
              (unsigned long long)seed, (unsigned long long)cycles, N_SRC, N_SNK, mode, ms_cyc,
              (unsigned long long)n_pdu, (unsigned long long)n_arm, (unsigned long long)n_exp,
              (unsigned long long)n_rsp, (unsigned long long)n_commit, (unsigned long long)n_tkreg,
              (unsigned long long)n_rst, (unsigned long long)n_regarm, (unsigned long long)n_gnt, (unsigned long long)n_txacc, (unsigned long long)n_wr, (unsigned long long)n_active,
              (unsigned long long)bad, (unsigned long long)ibad, (bad || ibad) ? (long long)first_bad : -1LL,
              (unsigned long long)diff_or, (unsigned long long)idiff_or);
  delete t;
  return (bad || ibad) ? 1 : 0;
}

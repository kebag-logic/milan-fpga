// SPDX-License-Identifier: CERN-OHL-W-2.0
// Random-stimulus driver for the base-vs-head KL_srp_top lockstep.
// The model is the head KL_srp_top with lockstep_chk bound into it (the
// checker holds the base engine, KL_srp_top_ref, on the same inputs and
// compares 51 outputs and 40 internal signals every clock).
//
// usage: Vtop +seed=N +cycles=N [+compressed] [+ls_count]
//        [+verilator+rand+reset+2 +verilator+seed+N]
// Environment: MRPDUs (MSRP Talker Advertise/Failed, Listener, Domain;
// MVRP VID) built per 802.1Q 10.8.1.2 from value pools shared with the
// class-B requests, LeaveAll flags, NumberOfValues 0..5, out-of-alphabet
// events, corrupted/truncated PDUs; class-B requests with every op and
// out-of-range indices; a slot-pool grant model; a timer-service model fed
// by the arm face plus spurious expiries; a PRNG draw model; now_ms
// advancing every 8..47 clocks; link/p2p/rate/config changes; random
// mid-run resets.
#include <verilated.h>
#include "Vtop.h"
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <map>
#include <memory>
#include <random>
#include <string>
#include <vector>

static std::mt19937_64 rng;
static uint64_t rnd(uint64_t n) { return n ? rng() % n : 0; }
static bool chance(uint64_t n) { return rnd(n) == 0; }

static const uint64_t SID_BASE = 0x0011223344550000ULL;
static const uint64_t DA_BASE = 0x91E0F000FE00ULL;
static const uint16_t VIDS[3] = {2, 3, 0x7FF};
static unsigned pool_ix() { return rnd(6); }
static uint64_t pool_sid() { return SID_BASE + rnd(6); }
static uint64_t pool_da() { return DA_BASE + rnd(6); }
static uint16_t pool_vid() { return VIDS[rnd(3)]; }
// correlated {stream_id, DA, VID} so declarations and received values match
static uint64_t c_da(unsigned ix) { return chance(6) ? pool_da() : DA_BASE + ix; }
static uint16_t c_vid() { return chance(6) ? pool_vid() : 2; }

static void put16(std::vector<uint8_t>& b, uint16_t v) { b.push_back(v >> 8); b.push_back(v & 0xFF); }
static void putn(std::vector<uint8_t>& b, uint64_t v, int n) {
  for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

static std::vector<uint8_t> gen_fv(int type) {
  std::vector<uint8_t> b;
  switch (type) {
    case 1: case 2: {
      unsigned ix = pool_ix();
      putn(b, SID_BASE + ix, 8); putn(b, c_da(ix), 6); put16(b, c_vid());
      static const uint16_t mfs[4] = {64, 224, 1500, 0xFFFF};
      put16(b, mfs[rnd(4)]); put16(b, chance(4) ? rnd(65536) : 1);
      b.push_back(static_cast<uint8_t>((rnd(8) << 5) | (rnd(2) << 4)));
      putn(b, rnd(3) == 0 ? rng() & 0xFFFFFFFF : 125000 + rnd(4) * 1000, 4);
      if (type == 2) { putn(b, rng(), 8); b.push_back(rnd(20)); }
      break;
    }
    case 3: putn(b, pool_sid(), 8); break;
    case 4: b.push_back(chance(4) ? rnd(256) : 6); b.push_back(rnd(8)); put16(b, pool_vid()); break;
    default: put16(b, pool_vid()); break;   // MVRP VID
  }
  return b;
}

static std::vector<uint8_t> gen_pdu(bool msrp, bool noisy) {
  std::vector<uint8_t> b;
  b.push_back(0x00);
  int nmsg = 1 + rnd(3);
  for (int m = 0; m < nmsg; m++) {
    int type = msrp ? 1 + rnd(4) : 1;
    int alen = msrp ? (type == 1 ? 25 : type == 2 ? 34 : type == 3 ? 8 : 4) : 2;
    bool lst = msrp && type == 3;
    b.push_back(type); b.push_back(alen);
    std::vector<uint8_t> body;
    int nvec = 1 + rnd(2);
    for (int v = 0; v < nvec; v++) {
      bool la = chance(10);
      int nov = rnd(6);
      body.push_back((la ? 0x20 : 0) | ((nov >> 8) & 0x1F));
      body.push_back(nov & 0xFF);
      auto fv = gen_fv(msrp ? type : 0);
      body.insert(body.end(), fv.begin(), fv.end());
      for (int i = 0; i < nov; i += 3) {
        if (chance(40)) { body.push_back(216 + rnd(40)); continue; }   // out of alphabet
        int e[3] = {0, 0, 0};
        for (int j = 0; j < 3 && i + j < nov; j++) e[j] = rnd(6);
        body.push_back(static_cast<uint8_t>((e[0] * 6 + e[1]) * 6 + e[2]));
      }
      if (lst) for (int i = 0; i < nov; i += 4) body.push_back(rnd(256));
    }
    if (msrp) put16(b, body.size() + 2);
    b.insert(b.end(), body.begin(), body.end());
    put16(b, 0);
  }
  put16(b, 0);
  if (noisy && chance(4)) {
    if (chance(2) && b.size() > 2) b.resize(1 + rnd(b.size() - 1));
    else b[rnd(b.size())] ^= 1u << rnd(8);
  }
  return b;
}

static uint64_t plus_u64(const char* name, uint64_t def) {
  const char* a = Verilated::commandArgsPlusMatch(name);
  if (a && *a) { const char* e = std::strchr(a, '='); if (e) return std::strtoull(e + 1, nullptr, 0); }
  return def;
}

int main(int argc, char** argv) {
  auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  uint64_t seed = plus_u64("seed", 1), cycles = plus_u64("cycles", 1000000);
  bool compressed = Verilated::commandArgsPlusMatch("compressed")[0] != 0;
  bool noisy = Verilated::commandArgsPlusMatch("noisy")[0] != 0;
  rng.seed(seed * 0x9E3779B97F4A7C15ULL + 7);
  auto d = std::make_unique<Vtop>(ctx.get());
  const unsigned M = NSRC, N = NSNK;

  // stats
  uint64_t pdus = 0, reqs = 0, rsp_ok = 0, frames = 0, arms = 0, exps = 0, spurious = 0,
           resets = 0, regs = 0, draws = 0;
  // environment state
  std::deque<uint8_t> mq; bool mq_msrp = true; std::vector<uint8_t> cur;
  size_t mpos = 0;
  bool req_v = false;
  int rst_hold = 8;
  uint32_t now = rnd(1u << 31); int now_div = 8 + rnd(40);
  std::map<unsigned, uint32_t> tmr;   // slot -> deadline
  int gnt_wait = -1; int draw_wait = -1;
  d->own_mac_i = 0x001B21AABBCCULL; d->link_up_i = 1; d->p2p_i = 1; d->cfg_rank_i = 1;
  d->cfg_acc_lat_ns_i = 125000; d->port_rate_bps_i = 1000000000;
  d->mrp_valid_i = 0; d->req_valid_i = 0; d->alloc_gnt_i = 0; d->txreq_ready_i = 0;
  d->exp_valid_i = 0; d->draw_busy_i = 0; d->draw_valid_i = 0; d->now_ms_i = now;
  d->clk_i = 0; d->rst_n = 0; d->eval();

  for (uint64_t t = 0; t < cycles && !ctx->gotFinish(); t++) {
    // ---- low phase: drive inputs from pre-edge outputs ----
    d->clk_i = 0;
    if (rst_hold > 0) { d->rst_n = 0; rst_hold--; }
    else {
      d->rst_n = 1;
      if (chance(150000)) { rst_hold = 1 + rnd(20); resets++;
        mq.clear(); cur.clear(); req_v = false; tmr.clear(); gnt_wait = -1; draw_wait = -1; }
    }
    bool in_rst = !d->rst_n;
    // quasi-static configuration changes
    if (chance(400000)) d->link_up_i = !d->link_up_i;
    if (!d->link_up_i && chance(20000)) d->link_up_i = 1;
    if (chance(500000)) d->p2p_i = !d->p2p_i;
    if (chance(300000)) { static const uint32_t r[3] = {1000000000u, 100000000u, 10000000u}; d->port_rate_bps_i = r[rnd(3)]; }
    if (chance(300000)) { d->cfg_rank_i = rnd(2); d->cfg_acc_lat_ns_i = rnd(3) ? 125000 + rnd(9) * 1000 : rng(); }
    // now_ms
    if (--now_div <= 0) { now++; now_div = 8 + rnd(40); }
    d->now_ms_i = now;
    // MRPDU byte stream
    d->eval();
    if (mq.empty() && !in_rst && chance(compressed ? 40 : 150)) {
      mq_msrp = rnd(4) != 0;
      auto p = gen_pdu(mq_msrp, noisy);
      mq.assign(p.begin(), p.end()); pdus++;
    }
    bool gap = chance(16);
    d->mrp_valid_i = !mq.empty() && !gap;
    d->mrp_data_i = mq.empty() ? 0 : mq.front();
    d->mrp_last_i = mq.size() == 1;
    d->mrp_msrp_i = mq_msrp;
    // class-B request
    if (!req_v && !in_rst && chance(compressed ? 120 : 600)) {
      req_v = true; reqs++;
      unsigned r = rnd(100);
      unsigned op = r < 35 ? 0 : r < 50 ? 1 : r < 80 ? 2 : r < 92 ? 3 : r < 96 ? 4 : 5 + rnd(3);
      d->req_op_i = op;
      unsigned lim = (op <= 1) ? M : N;
      d->req_index_i = (op == 4) ? (chance(3) ? rnd(256) : 6) : (chance(25) ? lim + rnd(4) : rnd(lim));
      unsigned ix = pool_ix();
      d->req_stream_id_i = SID_BASE + ix; d->req_da_i = c_da(ix); d->req_vid_i = c_vid();
      static const uint16_t mfs[5] = {64, 224, 300, 1500, 0xFFFF};
      d->req_max_frame_i = mfs[rnd(5)]; d->req_max_interval_i = chance(5) ? rnd(65536) : 1;
      d->req_lstn_state_i = rnd(4);
    }
    if (in_rst) req_v = false;
    d->req_valid_i = req_v;
    // slot pool grant model
    d->alloc_gnt_i = 0;
    if (d->alloc_req_o && !in_rst) {
      if (gnt_wait < 0) gnt_wait = rnd(12);
      if (gnt_wait == 0) { d->alloc_gnt_i = 1; d->alloc_slot_i = rnd(5); gnt_wait = -1; }
      else gnt_wait--;
    } else gnt_wait = -1;
    d->txreq_ready_i = rnd(3) == 0;
    // PRNG model
    d->draw_valid_i = 0;
    if (draw_wait > 0) { draw_wait--; d->draw_busy_i = 1; }
    else if (draw_wait == 0) { d->draw_valid_i = 1; d->draw_busy_i = 0; draw_wait = -1;
      d->draw_ms_i = compressed ? 300 + rnd(1200) : 10000 + rnd(5001); draws++; }
    else d->draw_busy_i = 0;
    // timer expiry model: the lowest due slot, or a spurious one
    d->exp_valid_i = 0;
    if (!in_rst) {
      for (auto it = tmr.begin(); it != tmr.end(); ++it) {
        if (static_cast<int32_t>(now - it->second) >= 0) {
          d->exp_valid_i = 1; d->exp_slot_i = it->first; tmr.erase(it); exps++; break;
        }
      }
      if (!d->exp_valid_i && chance(20000)) { d->exp_valid_i = 1; d->exp_slot_i = rnd(64); spurious++; }
    }
    d->eval();
    // sample handshakes pre-edge
    bool m_acc = d->mrp_valid_i && d->mrp_ready_o;
    bool r_acc = d->req_valid_i && d->req_ready_o;
    bool arm = d->arm_valid_o && !in_rst;
    unsigned arm_slot = d->arm_slot_o; bool arm_cancel = d->arm_cancel_o; uint32_t arm_dl = d->arm_deadline_ms_o;
    bool dreq = d->draw_req_o && !in_rst;
    if (d->txreq_valid_o && d->txreq_ready_i) frames++;
    if (d->rsp_valid_o && d->rsp_status_o == 0) rsp_ok++;
    regs += __builtin_popcountll(static_cast<uint64_t>(d->evt_tk_registered_o));
    // ---- posedge ----
    d->clk_i = 1; d->eval();
    if (m_acc) mq.pop_front();
    if (r_acc) req_v = false;
    if (arm) { arms++; if (arm_cancel) tmr.erase(arm_slot); else tmr[arm_slot] = arm_dl; }
    if (dreq && draw_wait < 0) draw_wait = 2 + rnd(20);
  }
  d->final();
  std::printf("RAND SUMMARY M=%u N=%u seed=%llu cycles=%llu compressed=%d noisy=%d pdus=%llu reqs=%llu rsp_ok=%llu frames=%llu arms=%llu expiries=%llu spurious=%llu draws=%llu registrations=%llu resets=%llu\n",
              M, N, (unsigned long long)seed, (unsigned long long)cycles, compressed, noisy,
              (unsigned long long)pdus, (unsigned long long)reqs, (unsigned long long)rsp_ok,
              (unsigned long long)frames, (unsigned long long)arms, (unsigned long long)exps,
              (unsigned long long)spurious, (unsigned long long)draws, (unsigned long long)regs,
              (unsigned long long)resets);
  return 0;
}

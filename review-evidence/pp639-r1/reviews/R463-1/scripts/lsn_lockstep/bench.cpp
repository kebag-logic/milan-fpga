// Listener lockstep: main's KL_pp_acmp_listener (renamed _ref) beside the candidate's,
// identical inputs from emulated faces, every output compared after every evaluation.
// The bench snoops the reference's own PROBE_TX commands and answers part of them with
// a matching PROBE_TX_RESPONSE so that streams settle.
// Usage: Vlsn_ls SEED CYCLES NSINKS
#include "Vlsn_ls.h"
#include "verilated.h"
#include <array>
#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <map>
#include <random>
#include <vector>

namespace {
constexpr int X_LATCH = 4, X_STRT_AP = 18;
constexpr uint64_t EID = 0x0011223344556677ull;
constexpr uint32_t OWNER_BASE = 32;

struct Txn {
  int proto, msg, status, slot;
  uint64_t ctlr, target;
  uint16_t seq, uid;
};

struct Rsp {
  uint64_t due;
  Txn t;
  std::array<uint8_t, 64> img;
};
}  // namespace

int main(int argc, char** argv) {
  const uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  const uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1000000;
  const int nsinks = argc > 3 ? atoi(argv[3]) : 2;
  std::mt19937_64 rng(seed);
  auto rnd = [&](uint64_t n) { return n ? rng() % n : 0; };
  auto pct = [&](int p) { return static_cast<int>(rng() % 1000) < p; };  // per mille
  auto ctx = new VerilatedContext;
  ctx->randReset(2);
  ctx->randSeed(static_cast<int>(seed & 0x7fffffff));
  auto d = new Vlsn_ls{ctx};

  // talker profiles and controller pool
  struct Prof { uint64_t teid, sid; uint16_t tuid, flags, vlan; uint64_t da; };
  std::array<Prof, 3> prof{};
  for (auto& p : prof) {
    p.teid = rng(); p.sid = rng(); p.tuid = static_cast<uint16_t>(rnd(4));
    p.flags = static_cast<uint16_t>(rng()); p.vlan = static_cast<uint16_t>(rng());
    p.da = rng() & 0xffffffffffffull;
  }
  const std::array<uint64_t, 3> ctlrs = {rng(), rng(), rng()};
  auto put = [](std::array<uint8_t, 64>& b, int off, uint64_t v, int n) {
    for (int i = 0; i < n; ++i) b[off + i] = static_cast<uint8_t>(v >> (8 * (n - 1 - i)));
  };
  auto image_of = [&](const Prof& p) {
    std::array<uint8_t, 64> b{};
    for (auto& x : b) x = static_cast<uint8_t>(rng());
    put(b, 4, p.sid, 8); put(b, 20, p.teid, 8); put(b, 36, p.tuid, 2);
    put(b, 40, p.da, 6); put(b, 50, p.flags, 2); put(b, 52, p.vlan, 2);
    return b;
  };

  // face state
  std::array<std::array<uint8_t, 64>, 4> rxbuf{};
  std::array<bool, 4> rxbusy{};
  std::array<std::array<uint8_t, 64>, 8> txbuf{};
  bool txn_pend = false; Txn cur{};
  bool tk_pend = false, pre_pend = false, ss_pend = false;
  std::deque<Rsp> rsps;
  std::map<uint32_t, uint32_t> timers;  // owner -> deadline ms
  uint32_t now = 0;
  int draw_wait = -1, gnt_wait = -1;
  int rst_left = 3;
  uint8_t rx_next = 0;
  // rates for the current phase (per mille)
  int p_txn = 200, p_tk = 50, p_pre = 5, p_ss = 20, p_spur = 2, p_rst_inv = 150000;
  uint64_t phase_left = 0;

  // tallies
  uint64_t mism = 0, latch = 0, strt_ap = 0, recwr = 0, settles = 0, resets = 0, txns = 0;
  uint64_t probes_seen = 0, rsp_sent = 0, exps = 0, first_bad = 0;
  int64_t first_bad_cyc = -1;
  std::vector<uint32_t> ref_w(32), dut_w(32);
  bool synced = false;  // compared from the first reset edge on, as section AQ does
  auto cmp = [&](uint64_t c) {
    if (!synced) return;
    bool same = true;
    for (int i = 0; i < 32; ++i) same = same && (d->ref_o[i] == d->dut_o[i]);
    same = same && (d->ref_xs == d->dut_xs);
    if (!same) {
      ++mism;
      if (first_bad_cyc < 0) {
        first_bad_cyc = static_cast<int64_t>(c);
        for (int i = 31; i >= 0; --i) if (d->ref_o[i] != d->dut_o[i]) { first_bad = i; break; }
      }
    }
  };

  d->clk_i = 0; d->rst_n = 0; d->entity_id_i = EID; d->eval();
  for (uint64_t c = 0; c < cycles; ++c) {
    if (phase_left == 0) {
      phase_left = 1000 + rnd(50000);
      const int k = static_cast<int>(rnd(4));
      p_txn = k == 0 ? 900 : k == 1 ? 50 : 250;
      p_tk = k == 2 ? 400 : 40;
      p_ss = k == 3 ? 300 : 15;
      p_pre = static_cast<int>(rnd(10));
      p_spur = static_cast<int>(rnd(5));
    }
    --phase_left;
    if (rst_left == 0 && rnd(p_rst_inv) == 0) rst_left = 1 + static_cast<int>(rnd(3));
    const bool in_rst = rst_left > 0;
    if (rst_left > 0) --rst_left;
    if (in_rst) {
      ++resets;
      rxbusy.fill(false);
      timers.clear();
      draw_wait = gnt_wait = -1;
    }
    if (c % 5 == 0) ++now;
    d->now_ms_i = now;

    // ---- txn face (held until accepted)
    if (!txn_pend) {
      if (!rsps.empty() && rsps.front().due <= c) {
        int s = -1;
        for (int i = 0; i < 4; ++i) if (!rxbusy[(rx_next + i) & 3]) { s = (rx_next + i) & 3; break; }
        if (s >= 0) {
          cur = rsps.front().t; cur.slot = s; rxbuf[s] = rsps.front().img; rxbusy[s] = true;
          rx_next = static_cast<uint8_t>(s + 1); rsps.pop_front(); txn_pend = true; ++rsp_sent;
        }
      } else if (pct(p_txn)) {
        Txn t{};
        t.proto = pct(950) ? 1 : static_cast<int>(rnd(8));
        static const int msgs[] = {6, 6, 6, 8, 10, 10, 1, 0, 2, 7, 11, 13};
        t.msg = msgs[rnd(12)];
        t.status = pct(850) ? 0 : static_cast<int>(rnd(32));
        t.ctlr = ctlrs[rnd(3)];
        t.target = pct(950) ? EID : rng();
        t.seq = static_cast<uint16_t>(rng());
        t.uid = static_cast<uint16_t>(pct(900) ? rnd(nsinks) : rnd(nsinks + 3));
        t.slot = 7;
        int s = -1;
        for (int i = 0; i < 4; ++i) if (!rxbusy[(rx_next + i) & 3]) { s = (rx_next + i) & 3; break; }
        if (s >= 0 && pct(920)) {
          t.slot = s; rxbusy[s] = true; rx_next = static_cast<uint8_t>(s + 1);
          rxbuf[s] = image_of(prof[rnd(3)]);
        }
        cur = t; txn_pend = true;
      }
    }
    d->txn_valid_i = txn_pend && !in_rst;
    d->t_protocol = cur.proto; d->t_msg_type = cur.msg; d->t_status = cur.status;
    d->t_ctlr = cur.ctlr; d->t_target = cur.target; d->t_seq = cur.seq; d->t_uid = cur.uid;
    d->t_rx_slot = cur.slot;

    // ---- TK events, preloads, started/stopped requests (held until acked)
    if (!tk_pend && pct(p_tk)) {
      tk_pend = true;
      d->evt_tk_kind_i = static_cast<uint8_t>(rnd(4)); d->evt_tk_failed_i = pct(300);
      d->evt_tk_sink_i = static_cast<uint16_t>(pct(950) ? rnd(nsinks) : rnd(nsinks + 4));
    }
    d->evt_tk_valid_i = tk_pend && !in_rst;
    if (!pre_pend && pct(p_pre)) {
      pre_pend = true;
      const Prof& p = prof[rnd(3)];
      d->pre_sink_i = static_cast<uint16_t>(pct(950) ? rnd(nsinks) : rnd(nsinks + 4));
      d->pre_talker_eid_i = p.teid; d->pre_talker_uid_i = p.tuid;
      d->pre_ctlr_eid_i = ctlrs[rnd(3)]; d->pre_sw_i = pct(300); d->pre_started_i = pct(500);
    }
    d->pre_valid_i = pre_pend && !in_rst;
    if (!ss_pend && pct(p_ss)) {
      ss_pend = true;
      d->strm_set_sink_i = static_cast<uint16_t>(pct(950) ? rnd(nsinks) : rnd(nsinks + 4));
      d->strm_set_val_i = pct(500);
    }
    d->strm_set_valid_i = ss_pend && !in_rst;

    // ---- timer expiries: the earliest due arm, else a rare spurious one
    d->tmr_exp_valid_i = 0;
    if (!in_rst) {
      for (auto it = timers.begin(); it != timers.end(); ++it) {
        if (static_cast<int32_t>(now - it->second) >= 0) {
          d->tmr_exp_valid_i = 1; d->tmr_exp_owner_i = it->first;
          d->tmr_exp_slot_i = (it->first - OWNER_BASE + 9) & 0x7f;
          timers.erase(it); ++exps;
          break;
        }
      }
      if (!d->tmr_exp_valid_i && pct(p_spur)) {
        d->tmr_exp_valid_i = 1; d->tmr_exp_owner_i = static_cast<uint8_t>(OWNER_BASE - 2 + rnd(nsinks + 4));
        d->tmr_exp_slot_i = static_cast<uint8_t>(rnd(128));
      }
    }
    // ---- PRNG and TX slot grant
    d->draw_valid_i = 0;
    if (draw_wait == 0) { d->draw_valid_i = 1; d->draw_ms_i = static_cast<uint16_t>(rnd(300)); }
    d->draw_busy_i = draw_wait > 0;
    d->txs_alloc_gnt_i = 0;
    if (gnt_wait == 0) { d->txs_alloc_gnt_i = 1; d->txs_alloc_slot_i = static_cast<uint8_t>(rnd(4)); }
    if (pct(2)) { d->lock_held_i = !d->lock_held_i; d->lock_ctlr_i = ctlrs[rnd(3)]; }
    d->rst_n = in_rst ? 0 : 1;
    d->eval();
    cmp(c);

    // ---- sample the reference's outputs that the faces act on at this edge
    const bool acc_txn = d->txn_valid_i && d->o_txn_ready_o;
    const bool acc_tk = d->evt_tk_valid_i && d->o_evt_tk_ready_o;
    const bool acc_pre = d->pre_valid_i && d->o_pre_ready_o;
    const bool done_ss = d->strm_set_valid_i && (d->o_strm_set_ready_o || d->o_strm_set_error_o);
    const bool rd_en = d->o_rxs_rd_en_o;
    const int rd_slot = d->o_rxs_rd_slot_o & 3;
    const int rd_addr = d->o_rxs_rd_addr_o;
    if (d->dut_xs == X_LATCH) ++latch;
    if (d->dut_xs == X_STRT_AP) ++strt_ap;

    d->clk_i = 1;
    d->eval();
    if (in_rst) synced = true;
    cmp(c);
    // ---- after the edge: registered strobes and the faces' responses
    if (!in_rst) {
      if (acc_txn) { txn_pend = false; ++txns; }
      if (acc_tk) tk_pend = false;
      if (acc_pre) pre_pend = false;
      if (done_ss) ss_pend = false;
    }
    d->rxs_rd_data_i = rd_en ? rxbuf[rd_slot][rd_addr & 63] : static_cast<uint8_t>(rng());
    if (d->o_rxs_free_o) rxbusy[d->o_rxs_free_slot_o & 3] = false;
    if (d->o_dbg_recwr_o) ++recwr;
    if (d->o_act_settle_o) ++settles;
    if (d->o_tmr_arm_valid_o) {
      if (d->o_tmr_arm_cancel_o) timers.erase(d->o_tmr_arm_owner_o);
      else timers[d->o_tmr_arm_owner_o] = d->o_tmr_arm_deadline_ms_o;
    }
    if (draw_wait >= 0) --draw_wait;
    if (d->o_draw_req_o) draw_wait = 1 + static_cast<int>(rnd(8));
    if (gnt_wait >= 0) --gnt_wait;
    if (d->o_txs_alloc_req_o) gnt_wait = pct(900) ? 0 : static_cast<int>(rnd(20));
    if (d->o_txs_wr_valid_o) txbuf[d->o_txs_wr_slot_o & 7][d->o_txs_wr_addr_o & 63] = d->o_txs_wr_data_o;
    if (d->o_txreq_valid_o) {
      const auto& b = txbuf[d->o_txreq_slot_o & 7];
      if ((b[1] & 0xf) == 0) {  // PROBE_TX_COMMAND: answer some of them
        ++probes_seen;
        if (pct(550)) {
          auto rd = [&](int off, int n) { uint64_t v = 0; for (int i = 0; i < n; ++i) v = (v << 8) | b[off + i]; return v; };
          Rsp r{};
          r.due = c + 1 + rnd(300);
          r.t.proto = 1; r.t.msg = 1; r.t.status = pct(850) ? 0 : static_cast<int>(1 + rnd(31));
          r.t.ctlr = pct(970) ? rd(12, 8) : ctlrs[rnd(3)];
          r.t.target = EID; r.t.seq = static_cast<uint16_t>(pct(970) ? rd(48, 2) : rng());
          r.t.uid = static_cast<uint16_t>(rd(38, 2));
          const Prof& p = prof[rnd(3)];
          r.img = image_of(p);
          if (pct(950)) { put(r.img, 20, rd(20, 8), 8); put(r.img, 36, rd(36, 2), 2); }
          rsps.push_back(r);
        }
      }
    }
    d->clk_i = 0;
    d->eval();
    cmp(c);
  }
  printf("LSN seed=%" PRIu64 " nsinks=%d cycles=%" PRIu64 " mismatch=%" PRIu64
         " first_bad_cycle=%" PRId64 " first_bad_word=%" PRIu64 " txns=%" PRIu64
         " x_latch=%" PRIu64 " x_strt_ap=%" PRIu64 " rec_writes=%" PRIu64 " probes=%" PRIu64
         " probe_rsps=%" PRIu64 " settles=%" PRIu64 " expiries=%" PRIu64 " reset_clocks=%" PRIu64 "\n",
         seed, nsinks, cycles, mism, first_bad_cyc, first_bad, txns, latch, strt_ap, recwr,
         probes_seen, rsp_sent, settles, exps, resets);
  d->final();
  delete d;
  delete ctx;
  return mism ? 1 : 0;
}

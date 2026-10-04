// lockstep driver: main's KL_pp_acmp_listener beside the candidate, identical
// inputs from emulated faces, every output compared after each clock edge.
// argv: seed cycles mode   (mode 0: protocol-shaped pools; 1: wider random)
#include "Vtb_lsn.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <random>
#include <string>
#include <vector>

static std::vector<std::pair<std::string, int>> fields;
static int total_w = 0;
static std::string field_of(int bit) {  // bit index from LSB of the concat
  int msb = total_w - 1;
  for (auto& f : fields) {
    int lo = msb - f.second + 1;
    if (bit >= lo && bit <= msb) return f.first + "[" + std::to_string(bit - lo) + "]";
    msb = lo - 1;
  }
  return "?";
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1000000;
  int mode = argc > 3 ? atoi(argv[3]) : 0;
  int nsinks = argc > 4 ? atoi(argv[4]) : 2;
  {
    std::ifstream fi("fields.txt");
    std::string n, w;
    while (fi >> n >> w) {
      int wi = (w == "N_SINKS_P") ? nsinks : (w == "SINK_W_C") ? (nsinks > 1 ? (int)__builtin_ceil(__builtin_log2(nsinks)) : 1) : std::stoi(w);
      fields.push_back({n, wi});
      total_w += wi;
    }
  }
  std::mt19937_64 rng(seed);
  auto u = [&](double p) { return std::uniform_real_distribution<double>(0, 1)(rng) < p; };
  auto pick = [&](std::initializer_list<uint64_t> l) { return *(l.begin() + rng() % l.size()); };
  const uint64_t OUR = 0x0A0B0C0D0E0F1011ull;
  Vtb_lsn* t = new Vtb_lsn;
  t->entity_id_i = OUR;
  uint8_t pdu[4][64] = {{0}};
  bool txn_p = false, tk_p = false, pre_p = false, ss_p = false;
  int draw_left = -1, rst_left = 4;
  bool gnt_next = false, rd_next = false;
  uint8_t rd_next_data = 0;
  uint32_t now = 1000;
  uint64_t mism = 0, latch = 0, strtap = 0, recwr = 0, commits = 0, settles = 0, resets = 0, txns = 0;
  uint64_t lock_ctlr = 0x0011223344556677ull;
  uint8_t txb[64] = {0};            // bytes the listener writes into its TX slot
  bool probe_seen = false;          // a PROBE_TX_COMMAND was committed
  uint8_t probe[64] = {0};          // ...its bytes
  uint64_t probe_resps = 0;
  bool lock_held = false;
  const int words = (total_w + 31) / 32;
  auto cmp = [&](uint64_t cyc, const char* ph) {
    int first = -1;
    for (int w = 0; w < words && first < 0; w++) {
      uint32_t x = t->r_all_o[w] ^ t->d_all_o[w];
      if (x) first = w * 32 + __builtin_ctz(x);
    }
    if (first >= 0 || t->r_xs_o != t->d_xs_o) {
      if (mism < 5)
        printf("MISMATCH cyc %llu %s: first differing output bit %s, xs ref %u dut %u\n",
               (unsigned long long)cyc, ph, first >= 0 ? field_of(first).c_str() : "-", t->r_xs_o, t->d_xs_o);
      mism++;
    }
  };
  for (uint64_t c = 0; c < cycles; c++) {
    if (rst_left == 0 && rng() % (mode == 0 ? 300000 : 60000) == 0) { rst_left = 1 + rng() % 4; resets++; }
    t->rst_n = rst_left > 0 ? 0 : 1;
    if (rst_left > 0) { rst_left--; txn_p = tk_p = pre_p = ss_p = false; draw_left = -1; }
    if (c % 10 == 0) now++;
    t->now_ms_i = now;
    // ---- new requests
    double rate = mode == 0 ? 0.02 : 0.08;
    if (!txn_p && u(rate)) {
      txn_p = true; txns++;
      for (int w = 0; w < 13; w++) t->txn_raw_i[w] = (uint32_t)rng();
      t->txn_acmp_i = u(0.95);
      t->txn_msg_i = u(0.9) ? pick({1, 6, 6, 8, 10}) : rng() % 16;
      bool answer = probe_seen && u(mode == 0 ? 0.5 : 0.3);
      t->txn_eid_ours_i = u(0.9);
      t->txn_ctlr_i = u(0.9) ? pick({0x0011223344556677ull, 0x0099AABBCCDDEEFFull}) : rng();
      t->txn_uid_i = u(0.85) ? rng() % nsinks : rng() % 24;
      int slot = u(0.92) ? rng() % 4 : 7;
      t->txn_slot_i = slot;
      t->txn_status_i = u(0.7) ? 0 : pick({1, 5, 7, 13, 31});
      t->txn_seq_i = u(0.8) ? rng() % 4 : rng();
      auto be = [&](int o, int n) { uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | probe[o + i]; return v; };
      if (answer) {  // the response to the last committed probe, every guard term equal
        probe_resps++;
        t->txn_msg_i = 1;
        t->txn_acmp_i = 1;
        t->txn_eid_ours_i = 1;
        t->txn_ctlr_i = be(12, 8);
        t->txn_uid_i = (uint16_t)be(38, 2);
        t->txn_seq_i = (uint16_t)be(48, 2);
        t->txn_status_i = u(0.8) ? 0 : pick({5, 7, 13});
        slot = rng() % 4;
        t->txn_slot_i = slot;
      }
      if (slot < 4) {
        for (int b = 0; b < 64; b++) pdu[slot][b] = (uint8_t)rng();
        uint64_t tk = u(0.9) ? pick({0x00221100AABBCCDDull, 0x00221100AABBCC55ull}) : rng();
        uint16_t tku = u(0.9) ? pick({1, 2}) : rng();
        for (int i = 0; i < 8; i++) pdu[slot][20 + i] = uint8_t(tk >> (56 - 8 * i));
        pdu[slot][36] = tku >> 8; pdu[slot][37] = tku & 0xFF;
        if (answer) {
          for (int i = 20; i < 38; i++) pdu[slot][i] = probe[i];  // talker eid, uid
        }
        if (mode == 0) {  // tidy flags and vlan most of the time
          pdu[slot][50] = 0; pdu[slot][51] = u(0.5) ? 0x08 : 0x00;
          pdu[slot][52] = 0; pdu[slot][53] = 2;
        }
      }
    }
    t->txn_valid_i = txn_p;
    if (!tk_p && u(mode == 0 ? 0.005 : 0.03)) {
      tk_p = true;
      t->evt_tk_kind_i = rng() % 4; t->evt_tk_failed_i = u(0.2);
      t->evt_tk_sink_i = u(0.9) ? rng() % nsinks : rng() % 20;
    }
    t->evt_tk_valid_i = tk_p;
    if (!pre_p && u(mode == 0 ? 0.0005 : 0.005)) {
      pre_p = true;
      t->pre_sink_i = u(0.9) ? rng() % nsinks : rng() % 20;
      t->pre_talker_eid_i = pick({0x00221100AABBCCDDull, 0x00221100AABBCC55ull});
      t->pre_talker_uid_i = pick({1, 2});
      t->pre_ctlr_eid_i = pick({0x0011223344556677ull, 0x0099AABBCCDDEEFFull});
      t->pre_sw_i = u(0.5); t->pre_started_i = u(0.5);
    }
    t->pre_valid_i = pre_p;
    if (!ss_p && u(mode == 0 ? 0.003 : 0.02)) {
      ss_p = true;
      t->strm_set_sink_i = u(0.9) ? rng() % nsinks : rng() % 20;
      t->strm_set_val_i = u(0.5);
    }
    t->strm_set_valid_i = ss_p;
    t->tmr_exp_valid_i = u(mode == 0 ? 0.003 : 0.02);
    t->tmr_exp_owner_i = u(0.9) ? 32 + rng() % nsinks : rng() % 256;
    t->tmr_exp_slot_i = rng() % 128;
    if (u(0.0002)) lock_held = !lock_held;
    if (u(0.0002)) lock_ctlr = pick({0x0011223344556677ull, 0x0099AABBCCDDEEFFull});
    t->lock_held_i = lock_held; t->lock_ctlr_i = lock_ctlr;
    // ---- face responses decided at the previous edge
    t->txs_alloc_gnt_i = gnt_next; t->txs_alloc_slot_i = rng() % 4;
    t->rxs_rd_data_i = rd_next ? rd_next_data : (uint8_t)rng();
    t->draw_busy_i = draw_left > 0;
    t->draw_valid_i = draw_left == 0;
    t->draw_ms_i = rng() % 1000;
    t->clk_i = 0;
    t->eval();
    cmp(c, "low");
    // ---- sample handshakes before the edge (ref's outputs; equal unless mismatched)
    // concat order is MSB-first as fields.txt; read the handshake bits by name
    auto bit = [&](const char* name) -> int {
      int msb = total_w - 1;
      for (auto& f : fields) {
        int lo = msb - f.second + 1;
        if (f.first == name) return (t->r_all_o[lo / 32] >> (lo % 32)) & 1;
        msb = lo - 1;
      }
      return 0;
    };
    auto val = [&](const char* name) -> uint64_t {
      int msb = total_w - 1;
      for (auto& f : fields) {
        int lo = msb - f.second + 1;
        if (f.first == name) {
          uint64_t v = 0;
          for (int i = 0; i < f.second && i < 64; i++) v |= (uint64_t)((t->r_all_o[(lo + i) / 32] >> ((lo + i) % 32)) & 1) << i;
          return v;
        }
        msb = lo - 1;
      }
      return 0;
    };
    bool rst = !t->rst_n;
    bool acc_txn = txn_p && bit("txn_ready_o");
    bool acc_tk = tk_p && bit("evt_tk_ready_o");
    bool acc_pre = pre_p && bit("pre_ready_o");
    bool done_ss = ss_p && bit("strm_set_ready_o");
    gnt_next = !rst && bit("txs_alloc_req_o") && u(0.85);
    rd_next = bit("rxs_rd_en_o");
    rd_next_data = pdu[val("rxs_rd_slot_o") & 3][val("rxs_rd_addr_o") & 63];
    if (draw_left >= 0) draw_left--;
    if (draw_left < 0 && bit("draw_req_o") && !rst) draw_left = 1 + rng() % 4;
    if (t->r_xs_o == 4) latch++;
    if (t->r_xs_o == 18) strtap++;
    if (bit("dbg_recwr_o")) recwr++;
    if (bit("txs_wr_valid_o")) txb[val("txs_wr_addr_o") & 63] = (uint8_t)val("txs_wr_data_o");
    if (bit("txs_wr_commit_o")) {
      commits++;
      if ((txb[1] & 0x0F) == 0) { probe_seen = true; for (int i = 0; i < 64; i++) probe[i] = txb[i]; }
    }
    if (bit("act_settle_o")) settles++;
    t->clk_i = 1;
    t->eval();
    cmp(c, "high");
    if (!rst) {
      if (acc_txn) txn_p = false;
      if (acc_tk) tk_p = false;
      if (acc_pre) pre_p = false;
      if (done_ss) ss_p = false;
    }
  }
  printf("seed %llu mode %d sinks %d cycles %llu: txns %llu X_LATCH %llu X_STRT_AP %llu "
         "record-writes %llu commits %llu probe-responses %llu settles %llu resets %llu\nMISMATCHES %llu\n",
         (unsigned long long)seed, mode, nsinks, (unsigned long long)cycles, (unsigned long long)txns,
         (unsigned long long)latch, (unsigned long long)strtap, (unsigned long long)recwr,
         (unsigned long long)commits, (unsigned long long)probe_resps, (unsigned long long)settles, (unsigned long long)resets,
         (unsigned long long)mism);
  delete t;
  return mism ? 1 : 0;
}

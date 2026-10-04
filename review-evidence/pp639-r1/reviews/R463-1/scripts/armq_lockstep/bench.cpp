// Arm-port lockstep: main's block vs the candidate's, identical random arms every clock,
// compared after every edge; both also graded against an independent eight-FIFO model of
// the banner's contract. Usage: Varmq_ls SEED CYCLES AW
#include "Varmq_ls.h"
#include "verilated.h"
#include <array>
#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <random>

int main(int argc, char** argv) {
  const uint64_t seed = argc > 1 ? strtoull(argv[1], nullptr, 0) : 1;
  const uint64_t cycles = argc > 2 ? strtoull(argv[2], nullptr, 0) : 1000000;
  const int aw = argc > 3 ? atoi(argv[3]) : 6;
  std::mt19937_64 rng(seed);
  auto ctx = new VerilatedContext;
  ctx->randReset(2);  // unreset state starts random, not zero
  ctx->randSeed(static_cast<int>(seed & 0x7fffffff));
  auto d = new Varmq_ls{ctx};
  const uint64_t pmask = (aw >= 64) ? ~0ull : ((1ull << (1 + aw + 8 + 32)) - 1);
  // model
  std::array<std::deque<uint64_t>, 8> q;
  bool m_valid = false;
  uint64_t m_port = 0;
  uint16_t m_drop = 0;
  bool m_synced = false;
  // tallies
  uint64_t mism_lock = 0, mism_model = 0, arms = 0, offers_full = 0, full_pop_push = 0;
  uint64_t drop_rises = 0, resets = 0, sat_clocks = 0, first_bad = 0;
  int64_t first_bad_cyc = -1;
  // phase state
  std::array<double, 8> p{};
  uint64_t phase_left = 0;
  int rst_left = 4;
  const double levels[] = {0.0, 0.002, 0.02, 0.1, 0.3, 0.5, 0.8, 0.95, 1.0};
  std::uniform_real_distribution<double> u01(0.0, 1.0);
  d->clk_i = 0;
  d->rst_n = 0;
  d->eval();
  for (uint64_t c = 0; c < cycles; ++c) {
    // ---- choose inputs for this clock
    if (phase_left == 0) {
      phase_left = 50 + (rng() % 20000);
      const int kind = static_cast<int>(rng() % 8);
      for (int k = 0; k < 8; ++k) {
        if (kind == 0) p[k] = 1.0;                                   // saturation
        else if (kind == 1) p[k] = (k == static_cast<int>(rng() % 8)) ? 1.0 : 0.0;
        else if (kind == 2) p[k] = 0.0;                              // drain
        else p[k] = levels[rng() % 9];
      }
      if (kind == 0 && (rng() % 4) == 0) phase_left = 70000 + (rng() % 30000);  // saturate the counter
    }
    --phase_left;
    if (rst_left == 0 && (rng() % 250000) == 0) rst_left = 1 + static_cast<int>(rng() % 4);
    const bool in_rst = rst_left > 0;
    if (rst_left > 0) --rst_left;
    uint8_t vld = 0, can = 0;
    std::array<uint64_t, 8> arm{};
    for (int k = 0; k < 8; ++k) {
      const bool v = u01(rng) < p[k];
      vld |= static_cast<uint8_t>(v) << k;
      const uint64_t r = rng();
      arm[k] = r & pmask;
      const bool cn = (arm[k] >> (aw + 8 + 32)) & 1;
      can |= static_cast<uint8_t>(cn) << k;
      const uint64_t sl = (r >> 40) & ((1ull << aw) - 1);
      const uint64_t ow = (r >> 32) & 0xff;
      const uint32_t dl = static_cast<uint32_t>(r);
      arm[k] = (static_cast<uint64_t>(cn) << (aw + 40)) | (sl << 40) | (ow << 32) | dl;
      d->slot = (d->slot & ~(0xffull << (8 * k))) | (sl << (8 * k));
      d->owner = (d->owner & ~(0xffull << (8 * k))) | (ow << (8 * k));
      d->deadline[k] = dl;
    }
    d->vld = vld;
    d->cancel = can;
    d->rst_n = in_rst ? 0 : 1;
    d->eval();
    // coverage from the candidate's combinational view of this clock
    if (!in_rst) {
      for (int k = 0; k < 8; ++k) {
        if ((d->cov_full_pop_push >> k) & 1) ++full_pop_push;
        if ((d->cov_drop_face >> k) & 1) ++offers_full;
      }
    }
    // ---- model of the edge about to happen
    if (in_rst) {
      for (auto& f : q) f.clear();
      m_valid = false;
      m_port = 0;
      m_drop = 0;
      m_synced = true;
      ++resets;
    } else if (m_synced) {
      bool popped = false;
      m_valid = false;
      for (auto& f : q) {
        if (f.empty()) continue;
        m_valid = true;
        m_port = f.front();
        f.pop_front();
        popped = true;
        break;
      }
      if (popped) ++arms;
      bool dropped = false;
      for (int k = 0; k < 8; ++k) {
        if (!((vld >> k) & 1)) continue;
        if (q[k].size() == 4) { dropped = true; continue; }
        q[k].push_back(arm[k]);
      }
      if (dropped && m_drop != 0xFFFF) { ++m_drop; ++drop_rises; }
      if (m_drop == 0xFFFF) ++sat_clocks;
    }
    d->clk_i = 1;
    d->eval();
    // ---- compare after the rising edge
    const bool lock_ok = (d->ref_valid == d->dut_valid) && (d->ref_port == d->dut_port)
                         && (d->ref_drop == d->dut_drop);
    bool model_ok = true;
    if (m_synced && !in_rst) {
      model_ok = ((d->dut_valid != 0) == m_valid) && (d->dut_drop == m_drop)
                 && (!m_valid || d->dut_port == m_port);
    }
    if (!lock_ok) { ++mism_lock; if (first_bad_cyc < 0) first_bad_cyc = static_cast<int64_t>(c); }
    if (!model_ok) ++mism_model;
    d->clk_i = 0;
    d->eval();
    const bool lock_ok2 = (d->ref_valid == d->dut_valid) && (d->ref_port == d->dut_port)
                          && (d->ref_drop == d->dut_drop);
    if (!lock_ok2) ++first_bad;
  }
  printf("ARMQ seed=%" PRIu64 " aw=%d cycles=%" PRIu64 " lockstep_mismatch=%" PRIu64
         " negedge_mismatch=%" PRIu64 " model_mismatch=%" PRIu64 " first_bad=%" PRId64
         " arms=%" PRIu64 " offers_to_full=%" PRIu64 " full_pop_push=%" PRIu64
         " drop_rises=%" PRIu64 " sat_clocks=%" PRIu64 " reset_clocks=%" PRIu64 "\n",
         seed, aw, cycles, mism_lock, first_bad, mism_model, first_bad_cyc, arms, offers_full,
         full_pop_push, drop_rises, sat_clocks, resets);
  d->final();
  delete d;
  delete ctx;
  return (mism_lock || first_bad) ? 1 : 0;
}

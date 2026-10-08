// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R554-2): cycle-random stress of KL_pp_originator at the CA
// shape (CA_POOL_P = INFLIGHT_P = 4, PROBE_SLOTS_P = 0) for the premise the
// count-one report guard relies on:
//   once a cancel for owner o is presented in cycle s, no failure for owner o
//   is reported in any cycle after s, until a new exchange of o is granted.
// (A failure reported in the cancel cycle itself is allowed; the notify block
// ignores it there.) Inputs follow the top's contract: at most one live
// exchange per owner, an issue for o is withheld in a cycle that cancels o (the
// CA builder suppresses iss_valid on its cancel hit), and accepts, responses and
// expiries are produced from what the DUT armed and sent, plus stale noise.
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <vector>
#include "VKL_pp_originator.h"
#include "verilated.h"

static uint32_t rng = 0x16701A2Bu;
static uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  long cycles = argc > 1 ? atol(argv[1]) : 2000000;
  if (argc > 2) rng = static_cast<uint32_t>(strtoul(argv[2], nullptr, 0));
  VerilatedContext ctx;
  auto* d = new VKL_pp_originator{&ctx};
  constexpr int NOWN = 4;
  struct Arm { bool armed = false; uint8_t owner = 0; };
  std::array<Arm, 128> tmr{};
  std::deque<uint8_t> tx_q;                       // slots sent, awaiting accept
  std::array<bool, NOWN> live{};                  // an exchange of o was granted and not ended
  std::array<bool, NOWN> cancelled{};             // a cancel for o was presented since its last grant
  std::array<uint16_t, NOWN> seq{};
  std::array<uint16_t, NOWN> key{};
  long violations = 0, fails = 0, fails_in_cancel_cycle = 0, cancels = 0, grants = 0, routes = 0;
  long cancel_beside_exp = 0;
  uint32_t now = 1;
  auto zero = [&] {
    d->iss_valid_i = 0; d->cancel_valid_i = 0; d->rsp_valid_i = 0; d->send_accept_valid_i = 0;
    d->exp_valid_i = 0;
  };
  zero(); d->rst_n = 0;
  for (int i = 0; i < 4; ++i) { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }
  d->rst_n = 1;
  for (long c = 0; c < cycles; ++c) {
    zero();
    d->now_ms_i = now; now += rnd() % 3;
    // cancel: an owner, live or not, about 1 in 6 cycles
    int cx = -1;
    if (rnd() % 6 == 0) { cx = rnd() % NOWN; d->cancel_valid_i = 1; d->cancel_owner_i = cx; }
    // issue for an owner without a live exchange, never the cancelled owner
    int io = rnd() % NOWN;
    if (!live[io] && io != cx && rnd() % 4 == 0) {
      d->iss_valid_i = 1; d->iss_owner_i = io; d->iss_tx_slot_i = rnd() % 8;
      key[io] = static_cast<uint16_t>(0x100 + io);
      d->iss_key_i = key[io]; d->iss_tmr_slot_i = 57 + (rnd() % 4); d->iss_timeout_ms_i = 250;
    }
    // serializer accept of a sent slot (or a stray slot)
    if (!tx_q.empty() && rnd() % 3 == 0) {
      d->send_accept_valid_i = 1; d->send_accept_slot_i = tx_q.front(); tx_q.pop_front();
    } else if (rnd() % 50 == 0) {
      d->send_accept_valid_i = 1; d->send_accept_slot_i = rnd() % 8;
    }
    // response: matching a live owner's seq, or noise
    if (rnd() % 10 == 0) {
      int ro = rnd() % NOWN;
      d->rsp_valid_i = 1; d->rsp_key_i = key[ro];
      d->rsp_seq_i = (rnd() % 2) ? seq[ro] : static_cast<uint16_t>(rnd());
    }
    // expiry: fire an armed slot, or a stale one
    std::vector<int> armed;
    for (int s = 0; s < 128; ++s) if (tmr[s].armed) armed.push_back(s);
    if (!armed.empty() && rnd() % 3 == 0) {
      int s = armed[rnd() % armed.size()];
      d->exp_valid_i = 1; d->exp_slot_i = s; d->exp_owner_i = tmr[s].owner; tmr[s].armed = false;
    } else if (rnd() % 40 == 0) {
      d->exp_valid_i = 1; d->exp_slot_i = 57 + rnd() % 4; d->exp_owner_i = 0xC0 | (rnd() % 4);
    }
    if (d->exp_valid_i && d->cancel_valid_i) ++cancel_beside_exp;
    d->clk_i = 0; d->eval();
    // the top's CA builder names the timer slot by the granted inflight id
    if (d->iss_valid_i) { d->iss_tmr_slot_i = 57 + d->iss_id_o; d->eval(); }
    // outputs of this cycle (registered: they reflect the previous edge)
    if (d->fail_valid_o) {
      ++fails;
      const int fo = d->fail_owner_o;
      if (fo < NOWN) {
        if (cancelled[fo]) {
          ++violations;
          if (violations <= 10) printf("VIOLATION cycle %ld: failure for owner %d after its cancel\n", c, fo);
        }
        if (cx == fo) ++fails_in_cancel_cycle;
        live[fo] = false;
      }
    }
    if (d->rt_valid_o && d->rt_owner_o < NOWN) { ++routes; live[d->rt_owner_o] = false; }
    if (d->send_valid_o) tx_q.push_back(d->send_slot_o);
    if (d->resend_valid_o) tx_q.push_back(d->resend_slot_o);
    if (d->tmr_arm_valid_o) {
      Arm& a = tmr[d->tmr_arm_slot_o & 127];
      if (d->tmr_arm_cancel_o) a.armed = false;
      else { a.armed = true; a.owner = d->tmr_arm_owner_o; }
    }
    const bool gnt = d->iss_gnt_o;
    const int go = d->iss_owner_i;
    const uint16_t gseq = d->iss_seq_o;
    d->clk_i = 1; d->eval();
    // state after the edge
    if (cx >= 0) { ++cancels; cancelled[cx] = true; live[cx] = false; }
    if (gnt) { ++grants; live[go] = true; cancelled[go] = false; seq[go] = gseq; }
  }
  printf("orig-stress seed-run: %ld cycles, %ld grants, %ld cancels, %ld routes, %ld failures "
         "(%ld in a cancel cycle of the same owner), %ld cancel+expiry cycles, %ld violations\n",
         cycles, grants, cancels, routes, fails, fails_in_cancel_cycle, cancel_beside_exp, violations);
  d->final();
  delete d;
  return violations ? 1 : 0;
}

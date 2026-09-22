// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_normalizer + KL_pp_dispatch suite — independent expectations,
// never DUT logic.
//
// The reference below implements the 03 §4 RECORD CONTRACT (pp_txn_t, 393
// bits, packed struct: FIRST declared field = MSB) and the 03 §5 producer
// contract (fixed priority RX > TIMER > SELF > MGMT; stall, never drop)
// from the documents. pack/unpack is an independent C++ re-encoding of the
// record from the declared field widths; every popped record is compared
// word-for-word against it, so a single flipped bit anywhere in the
// normalize -> enqueue -> pop path fails a check.

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include "Vtb_dispatch_top.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- independent 393-bit record codec ----------------------------------
constexpr int REC_WORDS = 13;      // ceil(393 / 32)
constexpr int REC_BITS  = 393;

struct Rec {
  uint32_t w[REC_WORDS];
  Rec() { memset(w, 0, sizeof w); }
  void set(int lsb, int width, uint64_t v) {
    for (int i = 0; i < width; ++i) {
      int b = lsb + i;
      if ((v >> i) & 1ull) w[b >> 5] |= (1u << (b & 31));
      else                 w[b >> 5] &= ~(1u << (b & 31));
    }
  }
  uint64_t get(int lsb, int width) const {
    uint64_t v = 0;
    for (int i = 0; i < width; ++i) {
      int b = lsb + i;
      if ((w[b >> 5] >> (b & 31)) & 1u) v |= (1ull << i);
    }
    return v;
  }
  bool operator==(const Rec& o) const { return memcmp(w, o.w, sizeof w) == 0; }
};

// pp_txn_t field LSB offsets, derived from the 03 §4 declared widths in
// struct order (first field ends at the MSB). The widths sum to 393.
constexpr int F_DISP       = 0;     // resp_disposition  2
constexpr int F_DEADLINE   = 2;     // deadline         32
constexpr int F_TX_SLOT    = 34;    // tx_slot           3
constexpr int F_HZ_KEY     = 37;    // hazard_key       16
constexpr int F_HZ_CLASS   = 53;    // hazard_class      4
constexpr int F_RX_SLOT    = 57;    // rx_slot           3
constexpr int F_UNIQUE_ID  = 60;    // operands.unique_id     16
constexpr int F_CONFIG_IX  = 76;    // operands.config_index  16
constexpr int F_DESC_IX    = 92;    // operands.desc_index    16
constexpr int F_DESC_TYPE  = 108;   // operands.desc_type     16
constexpr int F_OPCODE     = 124;   // opcode           16
constexpr int F_CR         = 140;   // cr                1
constexpr int F_U          = 141;   // u_flag            1
constexpr int F_SEQ        = 142;   // sequence_id      16
constexpr int F_TARGET_EID = 158;   // target_eid       64
constexpr int F_CTLR_EID   = 222;   // controller_eid   64
constexpr int F_SRC_MAC    = 286;   // src_mac          48
constexpr int F_CDL        = 334;   // cdl              11
constexpr int F_STATUS     = 345;   // status_in         5
constexpr int F_MSG_TYPE   = 350;   // msg_type          4
constexpr int F_PROTOCOL   = 354;   // protocol          3
constexpr int F_ARRIVAL    = 357;   // arrival_ts       32
constexpr int F_IF_INDEX   = 389;   // interface_index   2
constexpr int F_ORIGIN     = 391;   // origin            2

// origins / protocols / dispositions (pp_pkg encodings, from the doc)
constexpr uint8_t O_RX    = 0;
constexpr uint8_t O_TIMER = 1;
constexpr uint8_t O_SELF  = 2;
constexpr uint8_t O_MGMT  = 3;
constexpr uint8_t P_ADP   = 0;
constexpr uint8_t P_ACMP  = 1;
constexpr uint8_t P_AEM   = 2;
constexpr uint8_t P_MVU   = 3;
constexpr uint8_t P_AA    = 4;
constexpr uint8_t P_MAAP  = 5;
constexpr uint8_t D_UNI     = 0;
constexpr uint8_t D_ACMP_MC = 1;
constexpr unsigned SLOT_NULL = 7;
constexpr unsigned DEPTH = 4;              // wrapper default per queue

// ---- RX parsed-header beat + its expected record -----------------------
struct RxBeat {
  uint8_t  if_ix = 0;
  uint8_t  proto = P_AEM;
  uint8_t  msg_type = 0;
  uint8_t  status = 0;
  uint16_t cdl = 0;
  uint64_t src_mac = 0;
  uint64_t ctlr = 0;
  uint64_t tgt = 0;
  uint16_t seq = 0;
  uint8_t  u = 0;
  uint8_t  cr = 0;
  uint16_t opcode = 0;
  uint64_t operands = 0;                   // {desc_type,desc_ix,cfg_ix,uid}
  uint8_t  rx_slot = 0;
  uint8_t  hz_class = 0;
  uint16_t hz_key = 0;
};

struct Budgets {
  uint16_t adp = 4000;
  uint16_t acmp = 50;
  uint16_t aecp = 100;
};

static Rec expectRx(const RxBeat& b, uint32_t now, const Budgets& bud) {
  Rec r;
  r.set(F_ORIGIN, 2, O_RX);
  r.set(F_IF_INDEX, 2, b.if_ix);
  r.set(F_ARRIVAL, 32, now);
  r.set(F_PROTOCOL, 3, b.proto);
  r.set(F_MSG_TYPE, 4, b.msg_type);
  r.set(F_STATUS, 5, b.status);
  r.set(F_CDL, 11, b.cdl);
  r.set(F_SRC_MAC, 48, b.src_mac);
  r.set(F_CTLR_EID, 64, b.ctlr);
  r.set(F_TARGET_EID, 64, b.tgt);
  r.set(F_SEQ, 16, b.seq);
  r.set(F_U, 1, b.u);
  r.set(F_CR, 1, b.cr);
  r.set(F_OPCODE, 16, b.opcode);
  r.set(F_UNIQUE_ID, 16, b.operands & 0xFFFFu);
  r.set(F_CONFIG_IX, 16, (b.operands >> 16) & 0xFFFFu);
  r.set(F_DESC_IX, 16, (b.operands >> 32) & 0xFFFFu);
  r.set(F_DESC_TYPE, 16, (b.operands >> 48) & 0xFFFFu);
  r.set(F_RX_SLOT, 3, b.rx_slot);
  r.set(F_HZ_CLASS, 4, b.hz_class);
  r.set(F_HZ_KEY, 16, b.hz_key);
  r.set(F_TX_SLOT, 3, SLOT_NULL);
  uint16_t bsel = (b.proto == P_ADP)  ? bud.adp
                : (b.proto == P_ACMP) ? bud.acmp : bud.aecp;
  r.set(F_DEADLINE, 32, uint32_t(now + bsel));       // mod-2^32 by cast
  r.set(F_DISP, 2, (b.proto <= P_ACMP) ? D_ACMP_MC : D_UNI);
  return r;
}

// deterministic fully-populated injected record (every field non-trivial)
static Rec makeInjected(uint8_t origin, uint8_t proto, uint16_t seq,
                        uint32_t seed) {
  uint64_t s = seed * 0x9E3779B97F4A7C15ull + 0x2545F4914F6CDD1Dull;
  auto nxt = [&s]() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; };
  Rec r;
  for (int i = 0; i < REC_WORDS; ++i) r.w[i] = uint32_t(nxt());
  r.w[REC_WORDS - 1] &= (1u << (REC_BITS - 32 * (REC_WORDS - 1))) - 1u;
  r.set(F_ORIGIN, 2, origin);
  r.set(F_PROTOCOL, 3, proto);
  r.set(F_SEQ, 16, seq);
  return r;
}

// ---- harness -----------------------------------------------------------
struct Hn {
  Vtb_dispatch_top* d;
  Budgets bud;
  std::deque<Rec> exp[4];                  // per-queue expected pop order
  int checks = 0;
  int fails = 0;

  explicit Hn(Vtb_dispatch_top* dd) : d(dd) {}

  void settle() { d->clk_i = 0; d->eval(); }
  void edge()   { d->clk_i = 1; d->eval(); }
  void cycle()  { settle(); edge(); }

  void clearIn() {
    d->rx_valid_i = 0; d->tmr_valid_i = 0; d->self_valid_i = 0;
    d->mgmt_valid_i = 0;
    d->adp_txn_ready_i = 0; d->acmp_txn_ready_i = 0; d->aecp_txn_ready_i = 0;
    d->maap_txn_ready_i = 0;
  }
  void idle(int n = 1) { clearIn(); for (int i = 0; i < n; ++i) cycle(); }

  void setBudgets() {
    d->budget_adp_ms_i = bud.adp; d->budget_acmp_ms_i = bud.acmp;
    d->budget_aecp_ms_i = bud.aecp;
  }

  static int queueOf(uint8_t proto) {
    return (proto == P_ADP) ? 0 : (proto == P_ACMP) ? 1
         : (proto == P_MAAP) ? 3 : 2;
  }
  uint8_t qValid(int q) {
    return q == 0 ? d->adp_txn_valid_o
         : q == 1 ? d->acmp_txn_valid_o
         : q == 3 ? d->maap_txn_valid_o : d->aecp_txn_valid_o;
  }
  void qReady(int q, int v) {
    if (q == 0) d->adp_txn_ready_i = v;
    else if (q == 1) d->acmp_txn_ready_i = v;
    else if (q == 3) d->maap_txn_ready_i = v;
    else d->aecp_txn_ready_i = v;
  }
  Rec qRec(int q) {
    Rec r;
    for (int i = 0; i < REC_WORDS; ++i)
      r.w[i] = (q == 0) ? d->adp_txn_o[i]
             : (q == 1) ? d->acmp_txn_o[i]
             : (q == 3) ? d->maap_txn_o[i] : d->aecp_txn_o[i];
    return r;
  }
  unsigned qLevel(int q) {
    return q == 0 ? d->adp_level_o
         : q == 1 ? d->acmp_level_o
         : q == 3 ? d->maap_level_o : d->aecp_level_o;
  }
  unsigned qStall(int q) {
    return q == 0 ? d->adp_stall_count_o
         : q == 1 ? d->acmp_stall_count_o
         : q == 3 ? d->maap_stall_count_o : d->aecp_stall_count_o;
  }

  void loadRxPorts(const RxBeat& b, uint32_t now) {
    d->now_ms_i = now;
    d->rx_if_index_i = b.if_ix;       d->rx_protocol_i = b.proto;
    d->rx_msg_type_i = b.msg_type;    d->rx_status_i = b.status;
    d->rx_cdl_i = b.cdl;              d->rx_src_mac_i = b.src_mac;
    d->rx_controller_eid_i = b.ctlr;  d->rx_target_eid_i = b.tgt;
    d->rx_sequence_id_i = b.seq;      d->rx_u_i = b.u;
    d->rx_cr_i = b.cr;                d->rx_opcode_i = b.opcode;
    d->rx_operands_i = b.operands;    d->rx_slot_i = b.rx_slot;
    d->hz_class_i = b.hz_class;       d->hz_key_i = b.hz_key;
  }

  // present an RX beat, expect acceptance within `guard` cycles; on accept
  // the expected record joins the target queue's deque
  bool driveRx(const RxBeat& b, uint32_t now, const char* ph,
               int guard = 20) {
    loadRxPorts(b, now);
    d->rx_valid_i = 1;
    bool took = false;
    for (int i = 0; i < guard; ++i) {
      settle();
      if (d->rx_ready_o) { took = true; break; }
      edge();
    }
    CHECK(took, "%s: RX beat not accepted in %d cycles", ph, guard);
    if (took) { edge(); exp[queueOf(b.proto)].push_back(expectRx(b, now, bud)); }
    d->rx_valid_i = 0;
    return took;
  }

  void loadWide(int who, const Rec& r) {   // 0=tmr 1=self 2=mgmt
    for (int i = 0; i < REC_WORDS; ++i) {
      if (who == 0) d->tmr_txn_i[i] = r.w[i];
      else if (who == 1) d->self_txn_i[i] = r.w[i];
      else d->mgmt_txn_i[i] = r.w[i];
    }
  }
  uint8_t injReady(int who) {
    return who == 0 ? d->tmr_ready_o
         : who == 1 ? d->self_ready_o : d->mgmt_ready_o;
  }
  void injValid(int who, int v) {
    if (who == 0) d->tmr_valid_i = v;
    else if (who == 1) d->self_valid_i = v;
    else d->mgmt_valid_i = v;
  }

  // present an injected record, expect acceptance within `guard` cycles
  bool driveInj(int who, const Rec& r, const char* ph, int guard = 20) {
    loadWide(who, r);
    injValid(who, 1);
    bool took = false;
    for (int i = 0; i < guard; ++i) {
      settle();
      if (injReady(who)) { took = true; break; }
      edge();
    }
    CHECK(took, "%s: injected record not accepted in %d cycles", ph, guard);
    if (took) { edge(); exp[queueOf(uint8_t(r.get(F_PROTOCOL, 3)))].push_back(r); }
    injValid(who, 0);
    return took;
  }

  // wait for the head, compare against the queue's expected deque, consume
  void popExpect(int q, const char* ph, int guard = 12) {
    bool got = false;
    for (int i = 0; i < guard; ++i) {
      settle();
      if (qValid(q)) { got = true; break; }
      edge();
    }
    CHECK(got, "%s: q%d head never valid", ph, q);
    if (!got) return;
    CHECK(!exp[q].empty(), "%s: q%d pop with empty expectation", ph, q);
    if (!exp[q].empty()) {
      Rec want = exp[q].front(); exp[q].pop_front();
      Rec have = qRec(q);
      CHECK(have == want,
            "%s: q%d record mismatch (seq want %u have %u)", ph, q,
            unsigned(want.get(F_SEQ, 16)), unsigned(have.get(F_SEQ, 16)));
    }
    qReady(q, 1); settle(); edge(); qReady(q, 0);
  }
};

namespace {

//! The DUT, the per-queue expectation deques and the tally under one owner
//! (Core Guidelines I.2). `checks`/`fails` live in `Hn` because the BFM's own
//! `driveRx`/`driveInj`/`popExpect` count too, and each phase below is named
//! for the contract clause it proves rather than for its T-number (F.3).
class DispatchHarness {
 public:
  DispatchHarness() : d(model.get()), h(d) {}

  int run() {
    hold_reset_then_release();
    check_reset_state();
    check_hazard_rom_seam_mirrors_the_beat();
    check_one_rx_beat_per_protocol_routes_and_records();
    check_deadline_arithmetic_rolls_over();
    check_injected_records_pass_through_bit_exact();
    check_fixed_producer_priority();
    check_queue_full_stalls_and_never_drops();
    check_head_is_bit_stable_through_a_pop_stall();
    check_cross_queue_interleave_keeps_fifo_order();
    check_maap_queue_stalls_but_never_drops();

    printf("%d checks: %d PASS, %d FAIL\n", h.checks, h.checks - h.fails, h.fails);
    return h.fails ? 1 : 0;
  }

 private:
  void hold_reset_then_release() {
    h.clearIn();
    h.setBudgets();
    d->now_ms_i = 0;
    d->rst_n = 0;
    h.idle(4);
    d->rst_n = 1;
    h.idle(2);
  }

  // ---- T1: reset state -------------------------------------------------
  void check_reset_state() {
    h.settle();
    CHECK(!d->adp_txn_valid_o && !d->acmp_txn_valid_o && !d->aecp_txn_valid_o,
          "T1 no head valid after reset");
    CHECK(h.qLevel(0) == 0 && h.qLevel(1) == 0 && h.qLevel(2) == 0,
          "T1 levels zero got %u %u %u", h.qLevel(0), h.qLevel(1), h.qLevel(2));
    CHECK(h.qStall(0) == 0 && h.qStall(1) == 0 && h.qStall(2) == 0,
          "T1 stall counters zero");
    CHECK(d->rx_ready_o == 0 && d->tmr_ready_o == 0, "T1 no accept strobes idle");
    h.edge();
  }

  // ---- T2: the hazard-ROM seam mirrors the presented beat --------------
  void check_hazard_rom_seam_mirrors_the_beat() {
    RxBeat b2; b2.proto = P_AEM; b2.opcode = 0x0024; b2.hz_class = 3;
    b2.hz_key = 0x00AA; b2.seq = 1;
    h.loadRxPorts(b2, 1000);
    d->rx_valid_i = 1;
    h.settle();
    CHECK(d->hz_valid_o == 1, "T2 hz_valid mirrors rx_valid");
    CHECK(d->hz_protocol_o == P_AEM && d->hz_opcode_o == 0x0024,
          "T2 hz query lines carry the beat got proto %u opcode 0x%04x",
          unsigned(d->hz_protocol_o), unsigned(d->hz_opcode_o));
    CHECK(d->rx_ready_o == 1, "T2 free pipeline accepts immediately");
    h.edge();
    d->rx_valid_i = 0;
    h.exp[2].push_back(expectRx(b2, 1000, h.bud));
    h.settle();
    CHECK(d->hz_valid_o == 0, "T2 hz_valid drops with rx_valid");
    h.edge();
    h.popExpect(2, "T2 AEM record");
  }

  // ---- T3: one RX beat per protocol — routing + full record integrity --
  // covers: origin/arrival stamping, per-class budget selection (ADP 4000 /
  // ACMP 50 / AEM+MVU+AA 100), disposition derivation, tx_slot = NULL
  void check_one_rx_beat_per_protocol_routes_and_records() {
    const uint8_t protos[6] = { P_ADP, P_ACMP, P_AEM,
                                P_MVU, P_AA, P_MAAP };
    for (int k = 0; k < 6; ++k) {
      RxBeat b;
      b.proto = protos[k]; b.if_ix = uint8_t(k & 3); b.msg_type = uint8_t(k);
      b.status = uint8_t(0x11 + k); b.cdl = uint16_t(56 + 100 * k);
      b.src_mac = 0x91E0F0000000ull + uint64_t(k);
      b.ctlr = 0x0011223344556677ull ^ uint64_t(k) << 56;
      b.tgt = 0x8899AABBCCDDEEFFull ^ uint64_t(k);
      b.seq = uint16_t(0x2000 + k); b.u = k & 1; b.cr = (k >> 1) & 1;
      b.opcode = uint16_t(0x4B00 + k); b.operands = 0x0007000600050004ull + uint64_t(k);
      b.rx_slot = uint8_t(k & 3); b.hz_class = uint8_t(k); b.hz_key = uint16_t(0x0100 + k);
      uint32_t now = 5000 + uint32_t(k) * 17;
      h.driveRx(b, now, "T3 drive");
      int q = Hn::queueOf(b.proto);
      // the three other queues must NOT receive it
      for (int oq = 0; oq < 4; ++oq) {
        if (oq == q) continue;
        h.settle();
        CHECK(h.exp[oq].empty() && !h.qValid(oq),
              "T3 proto %u leaked into q%d", b.proto, oq);
        h.edge();
      }
      h.popExpect(q, "T3 pop");
      // deadline arithmetic spot-check on top of the word compare
    }
  }

  // ---- T4: deadline ms rollover (arrival near 2^32) --------------------
  void check_deadline_arithmetic_rolls_over() {
    RxBeat b4; b4.proto = P_ACMP; b4.seq = 0x4444; b4.opcode = 0x0009;
    uint32_t now4 = 0xFFFFFFF0u;                     // + 50 -> 0x00000022
    h.driveRx(b4, now4, "T4 drive");
    {
      h.settle();
      bool got = false;
      for (int i = 0; i < 12 && !(got = h.qValid(1)); ++i) { h.edge(); h.settle(); }
      CHECK(got, "T4 head valid");
      if (got) {
        Rec have = h.qRec(1);
        CHECK(uint32_t(have.get(F_DEADLINE, 32)) == 0x00000022u,
              "T4 rollover deadline got 0x%08x",
              unsigned(have.get(F_DEADLINE, 32)));
        CHECK(uint32_t(have.get(F_ARRIVAL, 32)) == now4,
              "T4 arrival got 0x%08x", unsigned(have.get(F_ARRIVAL, 32)));
      }
      h.edge();
    }
    h.popExpect(1, "T4 pop");
  }

  // ---- T5: injected records pass through bit-exact ---------------------
  void check_injected_records_pass_through_bit_exact() {
    Rec r5t = makeInjected(O_TIMER, P_ADP,  0x5001, 71);
    Rec r5s = makeInjected(O_SELF,  P_ACMP, 0x5002, 72);
    Rec r5m = makeInjected(O_MGMT,  P_AEM,  0x5003, 73);
    h.driveInj(0, r5t, "T5 timer");
    h.driveInj(1, r5s, "T5 self");
    h.driveInj(2, r5m, "T5 mgmt");
    h.popExpect(0, "T5 timer->ADP");
    h.popExpect(1, "T5 self->ACMP");
    h.popExpect(2, "T5 mgmt->AECP");
  }

  // ---- T6: fixed producer priority RX > TIMER > SELF > MGMT ------------
  // all four presented in the SAME cycle, all targeting the AECP queue
  void check_fixed_producer_priority() {
    RxBeat b6; b6.proto = P_AEM; b6.seq = 0x6000; b6.opcode = 0x0004;
    Rec r6t = makeInjected(O_TIMER, P_MVU, 0x6001, 81);
    Rec r6s = makeInjected(O_SELF,  P_AA,  0x6002, 82);
    Rec r6m = makeInjected(O_MGMT,  P_AEM, 0x6003, 83);
    h.loadRxPorts(b6, 60000);
    h.loadWide(0, r6t); h.loadWide(1, r6s); h.loadWide(2, r6m);
    d->rx_valid_i = 1; d->tmr_valid_i = 1; d->self_valid_i = 1;
    d->mgmt_valid_i = 1;
    {
      const char* names[4] = { "RX", "TIMER", "SELF", "MGMT" };
      for (int slot = 0; slot < 4; ++slot) {
        h.settle();
        uint8_t rr = d->rx_ready_o;
        uint8_t tr = d->tmr_ready_o;
        uint8_t sr = d->self_ready_o;
        uint8_t mr = d->mgmt_ready_o;
        unsigned nacc = unsigned(rr) + tr + sr + mr;
        CHECK(nacc == 1, "T6 cycle %d exactly one accept got %u", slot, nacc);
        uint8_t want[4] = { rr, tr,
                            sr, mr };
        CHECK(want[slot] == 1, "T6 cycle %d winner must be %s", slot,
              names[slot]);
        h.edge();
        if (slot == 0) { d->rx_valid_i = 0;  h.exp[2].push_back(expectRx(b6, 60000, h.bud)); }
        if (slot == 1) { d->tmr_valid_i = 0; h.exp[2].push_back(r6t); }
        if (slot == 2) { d->self_valid_i = 0; h.exp[2].push_back(r6s); }
        if (slot == 3) { d->mgmt_valid_i = 0; h.exp[2].push_back(r6m); }
      }
    }
    for (int k = 0; k < 4; ++k) h.popExpect(2, "T6 in priority order");
  }

  // ---- T7: queue full = STALL (backpressure), never a drop -------------
  // pops disabled: AECP holds head (1) + RAM (DEPTH); the normalizer's
  // 1-deep stage takes one more; the next producer request must stall
  void check_queue_full_stalls_and_never_drops() {
    {
      unsigned accepted = 0;
      for (unsigned k = 0; k < DEPTH + 1; ++k) {
        Rec r = makeInjected(O_SELF, P_AEM, uint16_t(0x7000 + k), 100 + k);
        if (h.driveInj(1, r, "T7 fill")) ++accepted;
        h.idle(2);                        // let it sink to RAM/head
      }
      CHECK(accepted == DEPTH + 1, "T7 queue proper holds %u got %u",
            DEPTH + 1, accepted);
      h.settle();
      CHECK(h.qLevel(2) == DEPTH + 1, "T7 level %u got %u", DEPTH + 1,
            h.qLevel(2));
      h.edge();

      // ---- T8: with AECP full, ADP and ACMP still flow (independence) ----
      RxBeat b8a; b8a.proto = P_ADP;  b8a.seq = 0x8001; b8a.opcode = 0x0000;
      RxBeat b8c; b8c.proto = P_ACMP; b8c.seq = 0x8002; b8c.opcode = 0x000B;
      h.driveRx(b8a, 70000, "T8 ADP while AECP full", 4);
      h.driveRx(b8c, 70001, "T8 ACMP while AECP full", 4);
      h.popExpect(0, "T8 ADP pops");
      h.popExpect(1, "T8 ACMP pops");

      // occupy the normalizer stage with one more AECP record
      Rec r6th = makeInjected(O_SELF, P_AEM, uint16_t(0x7000 + DEPTH + 1),
                              200);
      h.driveInj(1, r6th, "T7 normalizer stage takes one more", 4);

      // the NEXT record must stall at the producer port — and not be lost
      Rec r7th = makeInjected(O_MGMT, P_AEM, uint16_t(0x7000 + DEPTH + 2),
                              201);
      h.loadWide(2, r7th);
      d->mgmt_valid_i = 1;
      bool leaked = false;
      for (int i = 0; i < 6; ++i) {
        h.settle();
        if (d->mgmt_ready_o) leaked = true;
        h.edge();
      }
      CHECK(!leaked, "T7 producer stalls while the chain is full");

      // stall-cycle counter: +1 per stalled cycle, exactly (5 edges between
      // the two pre-edge samples)
      h.settle();
      unsigned c0 = h.qStall(2);
      h.edge();
      for (int i = 0; i < 4; ++i) h.cycle();
      h.settle();
      unsigned c1 = h.qStall(2);
      h.edge();
      CHECK(c1 - c0 == 5, "T7 stall counter cycle-exact got +%u", c1 - c0);
      CHECK(h.qStall(0) == 0 && h.qStall(1) == 0,
            "T7 other queues never stalled");

      // drain: everything arrives, in order, bit-exact — nothing was dropped
      d->mgmt_valid_i = 1;                  // still presenting the 7th
      for (int i = 0; i < 40 && d->mgmt_valid_i; ++i) {  // pop + catch accept
        h.settle();
        bool acc = d->mgmt_ready_o != 0;
        bool vld = h.qValid(2) != 0;
        if (vld) h.qReady(2, 1);
        if (vld && !h.exp[2].empty()) {
          Rec want = h.exp[2].front();
          Rec have = h.qRec(2);
          CHECK(have == want, "T7 drain record (seq want %u have %u)",
                unsigned(want.get(F_SEQ, 16)),
                unsigned(have.get(F_SEQ, 16)));
          h.exp[2].pop_front();
        }
        h.edge();
        h.qReady(2, 0);
        if (acc) { d->mgmt_valid_i = 0; h.exp[2].push_back(r7th); }
      }
      CHECK(d->mgmt_valid_i == 0, "T7 stalled record finally accepted");
      while (!h.exp[2].empty()) h.popExpect(2, "T7 drain tail");
      h.settle();
      CHECK(h.qLevel(2) == 0 && !h.qValid(2), "T7 drained to empty got %u",
            h.qLevel(2));
      h.edge();

      // counter holds once the stall is over
      unsigned cs = h.qStall(2);
      h.idle(5);
      h.settle();
      CHECK(h.qStall(2) == cs, "T7 counter stops after drain");
      h.edge();
    }
  }

  // ---- T9: head is bit-stable through a pop stall (stall, never skip) --
  void check_head_is_bit_stable_through_a_pop_stall() {
    Rec r9a = makeInjected(O_TIMER, P_ACMP, 0x9001, 300);
    Rec r9b = makeInjected(O_TIMER, P_ACMP, 0x9002, 301);
    h.driveInj(0, r9a, "T9 first");
    h.driveInj(0, r9b, "T9 second");
    {
      bool got = false;
      for (int i = 0; i < 12; ++i) { h.settle(); if ((got = h.qValid(1))) break; h.edge(); }
      CHECK(got, "T9 head valid");
      Rec s1 = h.qRec(1);
      h.edge();
      h.idle(3);                             // ready low: nothing may move
      h.settle();
      Rec s2 = h.qRec(1);
      CHECK(s1 == s2, "T9 head stable across a 3-cycle stall");
      CHECK(h.qLevel(1) == 2, "T9 both records still queued got %u",
            h.qLevel(1));
      h.edge();
    }
    h.popExpect(1, "T9 pop first");
    h.popExpect(1, "T9 pop second");
  }

  // ---- T10: cross-queue interleave keeps per-queue FIFO order ----------
  void check_cross_queue_interleave_keeps_fifo_order() {
    {
      uint16_t sq = 0xA000;
      for (int round = 0; round < 3; ++round) {
        RxBeat ba; ba.proto = P_ADP;  ba.seq = sq++; h.driveRx(ba, 80000u + sq, "T10 rx adp");
        Rec rt = makeInjected(O_TIMER, P_AEM,  sq++, 400u + sq);
        h.driveInj(0, rt, "T10 tmr aecp");
        RxBeat bc; bc.proto = P_ACMP; bc.seq = sq++; h.driveRx(bc, 80000u + sq, "T10 rx acmp");
        Rec rm = makeInjected(O_MGMT, P_ACMP, sq++, 500u + sq);
        h.driveInj(2, rm, "T10 mgmt acmp");
      }
      // per-queue expected deques encode arrival order; drain everything
      while (!h.exp[0].empty()) h.popExpect(0, "T10 adp order");
      while (!h.exp[1].empty()) h.popExpect(1, "T10 acmp order");
      while (!h.exp[2].empty()) h.popExpect(2, "T10 aecp order");
      h.settle();
      CHECK(h.qLevel(0) == 0 && h.qLevel(1) == 0 && h.qLevel(2) == 0,
            "T10 all empty at end got %u %u %u",
            h.qLevel(0), h.qLevel(1), h.qLevel(2));
      h.edge();
    }
  }

  // ---- T9: the MAAP queue is real — depth 2 + head, stall-not-drop -----
  // Three MAAP records fill RAM (2) + head (1); the fourth stalls the
  // normalizer (stall counter moves, nothing dropped) until a pop frees
  // room, and every record pops in order and bit-exact.
  void check_maap_queue_stalls_but_never_drops() {
    {
      h.idle(4);
      RxBeat mb;
      mb.proto = P_MAAP; mb.msg_type = 1; mb.status = 1; mb.cdl = 16;
      mb.src_mac = 0x525400AAAA00ull;
      mb.ctlr = 0x91E0F00040000008ull;     // requested_start + count lane
      mb.operands = 0;                     // conflict lane (a PROBE carries 0)
      for (int k = 0; k < 3; ++k) {
        mb.seq = uint16_t(k);              // seq is 0 on the wire; used as a tag
        mb.tgt = uint64_t(k);
        h.driveRx(mb, 9000 + unsigned(k), "T9 fill");
        h.idle(2);
      }
      h.settle();
      CHECK(h.qLevel(3) == 3, "T9 level got %u want 3", h.qLevel(3));
      unsigned st0 = h.qStall(3);
      // the fourth is accepted into the NORMALIZER's 1-deep stage (its own
      // contract) but the full MAAP queue refuses the handoff: the stall
      // counter must move and the record must NOT be dropped
      mb.seq = 3; mb.tgt = 3;
      h.driveRx(mb, 9010, "T9 fourth");
      for (int i = 0; i < 6; ++i) { h.settle(); h.edge(); }
      CHECK(h.qStall(3) > st0, "T9 stall counter moved (got %u then %u)",
            st0, h.qStall(3));
      h.settle();
      CHECK(h.qLevel(3) == 3, "T9 still 3 in flight, got %u", h.qLevel(3));
      h.edge();
      // pop all four in order and bit-exact — the stalled one lands last
      for (int k = 0; k < 4; ++k) h.popExpect(3, "T9 pop");
      h.idle(4);                     // let the head/skid settle after the pops
      h.settle();
      CHECK(h.qLevel(3) == 0 && !h.qValid(3), "T9 drained");
      h.edge();
    }
  }

  const milan::tb::Model<Vtb_dispatch_top> model;
  Vtb_dispatch_top* const d;
  Hn h;

  //! `CHECK` names `checks`/`fails` unqualified, so the phases above reach the
  //! same two counters `Hn`'s own checked helpers move. Declared after `h` so
  //! they bind to a member that is already constructed.
  int& checks = h.checks;
  int& fails = h.fails;
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  DispatchHarness harness;
  return harness.run();
}

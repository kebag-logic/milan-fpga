// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_adp_engine suite — independent expectations, never DUT logic.
//
// The harness models the LANDED module contracts in C++ (timer service arm/
// expiry, KL_pp_tx_slots alloc/write/commit, KL_pp_rx_slots sync read/free,
// the dispatch pop handshake) and builds every expected ADPDU wire frame
// from the 04 §3 field-sourcing table + F04.5 offsets on its own — a DUT/
// model mismatch in any of the 82 bytes fails the run. The PRNG is the REAL
// KL_pp_prng (wired in tb_adp_top) so the T-ADP-DELAY-START (kind 1,
// 0..2000 ms) vs T-ADP-DELAY (kind 2, 0..4000 ms) draws are graded
// statistically against the actual rejection sampler.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Vtb_adp_top.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- fixed configuration driven into the DUT ---------------------------
constexpr uint64_t EID   = 0x1122334455667788ull;
constexpr uint64_t EMID  = 0x99AABBCCDDEEFF01ull;
constexpr uint64_t MAC   = 0x001B921122AAull;             // 48-bit
constexpr uint16_t TKSRC = 0x0008;
constexpr uint16_t TKCAP = 0x4801;
constexpr uint16_t LSNK  = 0x0008;
constexpr uint16_t LSCAP = 0x4801;
constexpr uint16_t CFGIX = 0x0002;
constexpr uint16_t IDIX  = 0x0005;
constexpr uint64_t GM0   = 0xA1A2A3A4A5A6A7A8ull;
constexpr uint8_t  DOM0  = 0x00;

// remote talkers
constexpr uint64_t T1 = 0xAAAA00000000AAA1ull;
constexpr uint64_t T2 = 0xBBBB00000000BBB2ull;
constexpr uint64_t T3 = 0xCCCC00000000CCC3ull;

// timer slot map (engine defaults: ADV base 0, NOADP base N_IF = 1)
constexpr unsigned SLOT_ADV    = 0;
constexpr unsigned SLOT_NOADP0 = 1;

// ---- independent F04.5 wire-frame model (doc offsets, not DUT code) ----
// One ADPDU on the wire: the 14-byte Ethernet header plus the 68-byte ADPDU
// body the F04.5 offsets below run out to.
constexpr int kAdpduBytes = 82;
// Per-slot payload capacity of KL_pp_tx_slots / KL_pp_rx_slots, in bytes.
constexpr unsigned kSlotBytes = 576;

static void putbe(uint8_t* p, uint64_t v, int n) {
  for (int i = 0; i < n; ++i) p[i] = uint8_t(v >> (8 * (n - 1 - i)));
}
static void model_frame(uint8_t f[kAdpduBytes], bool departing, uint64_t gm,
                        uint8_t dom, uint32_t aidx) {
  memset(f, 0, kAdpduBytes);
  putbe(f + 0, 0x91E0F0010000ull, 6);          // DA (03 §8)
  putbe(f + 6, MAC, 6);                        // SA
  putbe(f + 12, 0x22F0, 2);                    // EtherType
  f[14] = 0xFA;                                // subtype ADP
  f[15] = departing ? 0x01 : 0x00;             // h=0 ver=0 msg_type
  f[16] = uint8_t(((departing ? 0 : 10) << 3) | 0);  // valid_time | cdl[10:8]
  f[17] = 56;                                  // cdl
  putbe(f + 18, EID, 8);                       // entity_id @ wire byte 18
  putbe(f + 26, EMID, 8);
  putbe(f + 34, 0x0000C588ull, 4);             // F04.6 entity_capabilities
  putbe(f + 38, TKSRC, 2);
  putbe(f + 40, TKCAP, 2);
  putbe(f + 42, LSNK, 2);
  putbe(f + 44, LSCAP, 2);
  putbe(f + 46, 0, 4);                         // controller_capabilities
  putbe(f + 50, aidx, 4);                      // available_index
  putbe(f + 54, gm, 8);                        // gptp_grandmaster_id
  f[62] = dom;                                 // gptp_domain_number
  f[63] = 0;                                   // reserved
  putbe(f + 64, CFGIX, 2);
  putbe(f + 66, IDIX, 2);
  putbe(f + 68, 0, 2);                         // interface_index (if 0)
  putbe(f + 70, 0, 8);                         // association_id
  putbe(f + 78, 0, 4);                         // reserved
}

// ---- independent 393-bit pp_txn_t codec (03 §4 struct order) -----------
constexpr int REC_WORDS = 13;
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

// ADP message_type: ENTITY_AVAILABLE / ENTITY_DEPARTING / ENTITY_DISCOVER
constexpr uint8_t MSG_AVAIL    = 0;
constexpr uint8_t MSG_DEPART   = 1;
constexpr uint8_t MSG_DISCOVER = 2;

constexpr unsigned SLOT_NULL = 7;

static Rec adp_txn(uint8_t msg, uint64_t eid, uint8_t vt, uint8_t rx_slot,
                   uint32_t now) {
  Rec r;
  r.set(F_ORIGIN, 2, 0);                       // RX
  r.set(F_IF_INDEX, 2, 0);
  r.set(F_ARRIVAL, 32, now);
  r.set(F_PROTOCOL, 3, 0);                     // ADP
  r.set(F_MSG_TYPE, 4, msg);
  r.set(F_STATUS, 5, vt);
  r.set(F_CDL, 11, 56);
  r.set(F_SRC_MAC, 48, 0x0202DEADBEEFull);
  r.set(F_TARGET_EID, 64, eid);
  r.set(F_OPCODE, 16, msg);
  r.set(F_RX_SLOT, 3, rx_slot);
  r.set(F_TX_SLOT, 3, SLOT_NULL);
  r.set(F_DEADLINE, 32, now + 4000);
  r.set(F_DISP, 2, 1);
  return r;
}

namespace {

// ---- harness -----------------------------------------------------------
struct Evt { bool departed; unsigned sink; };
struct Arm { bool cancel; unsigned slot; uint32_t deadline; };
struct Draw { unsigned kind; unsigned ms; };

struct Harness {
  //! The engine, the four service models it is judged against, the event
  //! and draw logs and the tally in one object. `checks`/`fails` were
  //! file-scope mutables (I.2); the lettered phases below were one
  //! 465-line `main` (F.3).
  const milan::tb::Model<Vtb_adp_top> model;
  Vtb_adp_top* const d = model.get();
  uint32_t now = 10000;                        // absolute ms timebase
  // timer-service model
  bool     t_armed[128] = {false};
  uint32_t t_deadline[128] = {0};
  std::vector<Arm> arms;                       // arm/cancel log
  // tx-slot pool model
  enum SlotSt { FREE, ALLOC, READY };
  SlotSt   s_st[5] = {FREE, FREE, FREE, FREE, FREE};
  uint8_t  s_buf[5][kSlotBytes];
  int      gnt_withhold = 0;                   // refuse this many requests
  bool     gnt_sched = false;                  // grant to drive next cycle
  unsigned gnt_slot = 0;
  bool     write_before_gnt = false;
  bool     write_bad = false;                  // out-of-slot / non-ALLOC write
  bool     oversize_seen = false;
  bool     req_two_cycles = false;             // alloc_req high twice in a row
  bool     req_prev = false;
  int      alloc_reqs = 0;
  struct Frame { uint8_t b[kAdpduBytes]; unsigned len; unsigned slot; };
  std::vector<Frame> frames;                   // committed frames, in order
  int      txreqs = 0;
  bool     txreq_bad_slot = false;
  // rx-slot pool model
  uint8_t  rx_pdu[4][kSlotBytes];
  uint8_t  rd_next = 0;                        // sync-read pipeline register
  int      frees = 0;
  int      last_free_slot = -1;
  // events + draws
  std::vector<Evt>  evts;
  std::vector<Draw> draws;
  // expiry to inject this cycle
  bool     exp_pulse = false;
  unsigned exp_slot = 0;

  int checks = 0;
  int fails = 0;

  // Watermarks a phase takes before it acts and a later phase compares
  // against; they were locals of the one `main` every phase lived in.
  size_t arm0 = 0;
  size_t dn = 0;
  size_t fn = 0;
  size_t an = 0;
  size_t en = 0;
  int fr = 0;
  uint32_t idx_before_dep = 0;

  Harness() {
    memset(rx_pdu, 0, sizeof rx_pdu);
    memset(s_buf, 0, sizeof s_buf);
  }

  void tick() {
    // drive this cycle's inputs
    d->now_ms_i = now;
    d->rxs_rd_data_i = rd_next;
    d->tmr_exp_valid_i = exp_pulse;
    d->tmr_exp_slot_i = exp_slot;
    d->tmr_exp_owner_i = exp_slot;
    exp_pulse = false;
    d->txs_alloc_gnt_i = gnt_sched;
    d->txs_alloc_slot_i = gnt_slot;
    gnt_sched = false;

    d->clk_i = 0; d->eval();

    // ---- observe pre-edge (what the registers will see) ----
    // timer arm port
    if (d->tmr_arm_valid_o) {
      unsigned sl = d->tmr_arm_slot_o;
      Arm a{static_cast<bool>(d->tmr_arm_cancel_o), sl,
            static_cast<uint32_t>(d->tmr_arm_deadline_ms_o)};
      arms.push_back(a);
      if (a.cancel) t_armed[sl] = false;
      else { t_armed[sl] = true; t_deadline[sl] = a.deadline; }
    }
    // tx-slot pool
    if (d->txs_oversize_o) oversize_seen = true;
    if (d->txs_alloc_req_o) {
      ++alloc_reqs;
      if (req_prev) req_two_cycles = true;
      if (gnt_withhold > 0) { --gnt_withhold; }
      else {
        unsigned s = 0;
        bool ok = false;
        for (s = 0; s < 4; ++s) if (s_st[s] == FREE) { ok = true; break; }
        if (ok) { gnt_sched = true; gnt_slot = s; s_st[s] = ALLOC; }
      }
    }
    req_prev = d->txs_alloc_req_o;
    if (d->txs_wr_valid_o) {
      unsigned s = d->txs_wr_slot_o;
      unsigned a = d->txs_wr_addr_o;
      if (s > 4 || s_st[s] != ALLOC) { write_bad = true; write_before_gnt = true; }
      else if (a >= kSlotBytes) write_bad = true;
      else s_buf[s][a] = d->txs_wr_data_o;
    }
    if (d->txs_wr_commit_o) {
      unsigned s = d->txs_wr_slot_o;
      if (s > 4 || s_st[s] != ALLOC) write_bad = true;
      else {
        s_st[s] = READY;
        Frame f;
        f.len = d->txs_wr_len_o;
        f.slot = s;
        memcpy(f.b, s_buf[s], kAdpduBytes);
        frames.push_back(f);
      }
    }
    if (d->txreq_valid_o) {
      ++txreqs;
      unsigned s = d->txreq_slot_o;
      if (s > 4 || s_st[s] != READY) txreq_bad_slot = true;
      else s_st[s] = FREE;                     // arbiter streams + auto-free
    }
    // rx-slot sync read + free
    if (d->rxs_rd_en_o) rd_next = rx_pdu[d->rxs_rd_slot_o][d->rxs_rd_addr_o];
    if (d->rxs_free_o) { ++frees; last_free_slot = d->rxs_free_slot_o; }
    // events
    if (d->evt_valid_o)
      evts.push_back({static_cast<bool>(d->evt_departed_o),
                      static_cast<unsigned>(d->evt_sink_o)});
    // real-PRNG draw taps
    if (d->tap_draw_req_o) {
      // remember the requested kind; result pairs at tap_draw_valid_o
      pending_kind = d->tap_draw_kind_o;
    }
    if (d->tap_draw_valid_o)
      draws.push_back({pending_kind, static_cast<unsigned>(d->tap_draw_ms_o)});

    d->clk_i = 1; d->eval();
  }
  unsigned pending_kind = 0;

  void idle(int n) { for (int i = 0; i < n; ++i) tick(); }

  // wait (bounded) for the slot to be armed, jump time to its deadline,
  // fire one expiry pulse — models the timer-service sweep
  bool expire_slot(unsigned s, int patience = 200) {
    for (int i = 0; i < patience && !t_armed[s]; ++i) tick();
    if (!t_armed[s]) return false;
    if (int32_t(t_deadline[s] - now) > 0) now = t_deadline[s];
    t_armed[s] = false;
    exp_pulse = true; exp_slot = s;
    tick();
    return true;
  }

  // present one txn on the dispatch face and wait for full consumption
  bool send_txn(const Rec& r, int max_cycles = 200) {
    for (int i = 0; i < REC_WORDS; ++i) d->txn_i[i] = r.w[i];
    d->txn_valid_i = 1;
    int i = 0;
    for (; i < max_cycles && !(d->txn_ready_o); ++i) tick();
    if (i >= max_cycles) { d->txn_valid_i = 0; return false; }
    tick();                                    // handshake cycle
    d->txn_valid_i = 0;
    for (i = 0; i < max_cycles; ++i) { tick(); if (d->txn_ready_o) return true; }
    return false;
  }

  // load a remote ADPDU into an RX slot (PDU offsets, subtype at byte 0)
  void load_remote(unsigned slot, uint64_t eid, uint32_t aidx, uint64_t gm,
                   uint8_t dom, uint16_t ifx, uint8_t vt, uint8_t msg) {
    uint8_t* p = rx_pdu[slot];
    memset(p, 0, kSlotBytes);
    p[0] = 0xFA; p[1] = msg;
    p[2] = uint8_t((vt << 3) | 0); p[3] = 56;
    putbe(p + 4, eid, 8);
    putbe(p + 12, eid ^ 0x1234ull, 8);         // model id (unused by DUT)
    putbe(p + 36, aidx, 4);
    putbe(p + 40, gm, 8);
    p[48] = dom;
    putbe(p + 54, ifx, 2);
  }

  // wait until predicate or timeout
  template <typename F> bool wait_for(F f, int max_cycles = 400) {
    for (int i = 0; i < max_cycles; ++i) { if (f()) return true; tick(); }
    return f();
  }

  // crash-safe accessors: a missing frame/draw/event must FAIL checks, not
  // segfault the harness (poison values never match an expectation)
  Frame last_frame() const {
    if (!frames.empty()) return frames.back();
    Frame z;
    memset(&z, 0xEE, sizeof z);
    z.len = 0;
    z.slot = 9;
    return z;
  }
  Draw last_draw() const {
    return draws.empty() ? Draw{99, 65535} : draws.back();
  }
  Draw first_draw() const {
    return draws.empty() ? Draw{99, 65535} : draws.front();
  }

  void set_bound(unsigned s, uint64_t eid, bool on);
  void configure_the_entity_and_release_reset();
  void check_reset_state();
  void check_startup_draw_and_delay_arm();
  void check_first_entity_available_is_byte_exact();
  void check_advertise_cadence_restarts_per_send();
  void check_entity_discover_handling();
  void check_gm_change_readvertises_a_fresh_gm();
  void check_link_down_and_link_up();
  void check_disable_departs_then_restarts();
  void check_the_two_draw_kinds_are_separate();
  void check_talker_discovery_arms_and_refreshes();
  void check_one_available_discovers_every_bound_sink();
  void check_talker_restart_and_stale_index_rules();
  void check_departing_aging_unbind_and_backpressure();
  void check_pool_protocol_invariants();
  int report();
  int run_suite();
};

// find last arm (non-cancel) of a slot in a log slice
static int last_arm_of(const std::vector<Arm>& v, size_t from, unsigned slot,
                       bool cancel) {
  for (size_t i = v.size(); i > from; --i)
    if (v[i-1].slot == slot && v[i-1].cancel == cancel) return int(i-1);
  return -1;
}

// static configuration
void Harness::configure_the_entity_and_release_reset() {
  d->entity_id_i = EID;
  d->entity_model_id_i = EMID;
  d->own_mac_i = MAC;
  d->talker_sources_i = TKSRC;  d->talker_caps_i = TKCAP;
  d->listener_sinks_i = LSNK;   d->listener_caps_i = LSCAP;
  d->current_cfg_i = CFGIX;     d->identify_index_i = IDIX;
  d->gm_id_i = GM0;             d->gptp_domain_i = DOM0;
  d->entity_enable_i = 0;       d->link_up_i = 0;
  d->gm_change_i = 0;           d->txn_valid_i = 0;
  d->bound_i = 0;
  for (int i = 0; i < 16; ++i) d->bound_talker_eid_i[i] = 0;

  d->rst_n = 0;
  idle(5);
  d->rst_n = 1;
  idle(3);
}

// ---- P0: reset state -------------------------------------------------
void Harness::check_reset_state() {
  CHECK(d->txn_ready_o == 1, "P0 dispatch face ready after reset");
  CHECK((d->dbg_adv_state_o & 3) == 0, "P0 advertise SM in DOWN");
  CHECK(d->dbg_avail_index_o == 0, "P0 available_index = 0 at power-up");
  CHECK(frames.empty() && evts.empty(), "P0 quiescent");
}

// ---- P1: startup — enable with link up => kind-1 draw ---------------
void Harness::check_startup_draw_and_delay_arm() {
  arm0 = arms.size();
  d->link_up_i = 1;            // seeds the real PRNG
  d->entity_enable_i = 1;
  CHECK(wait_for([&]{ return !draws.empty(); }), "P1 startup draw runs");
  CHECK(draws.size() == 1, "P1 exactly one draw, got %zu", draws.size());
  CHECK(first_draw().kind == 1, "P1 startup draw kind 1 (T-ADP-DELAY-START), got %u",
        first_draw().kind);
  CHECK(first_draw().ms <= 2000, "P1 kind-1 range, got %u", first_draw().ms);
  idle(4);
  int a = last_arm_of(arms, arm0, SLOT_ADV, false);
  CHECK(a >= 0, "P1 delay timer armed on shared slot 0");
  if (a >= 0)
    CHECK(arms[a].deadline == now + first_draw().ms,
          "P1 delay deadline = now + draw (got %u want %u)",
          arms[a].deadline, now + first_draw().ms);
  CHECK((d->dbg_adv_state_o & 3) == 2, "P1 SM in DELAY, got %u",
        static_cast<unsigned>(d->dbg_adv_state_o & 3));
}

// ---- P2: first ENTITY_AVAILABLE, byte-exact, tx-slot protocol -------
void Harness::check_first_entity_available_is_byte_exact() {
  gnt_withhold = 3;          // starve the pool: engine must re-request
  size_t f0 = frames.size();
  CHECK(expire_slot(SLOT_ADV), "P2 delay expiry fires");
  CHECK(wait_for([&]{ return frames.size() > f0; }), "P2 frame committed");
  CHECK(!write_before_gnt, "P2 no slot write before grant");
  CHECK(!req_two_cycles, "P2 alloc_req is a one-cycle pulse (pool double-alloc hazard)");
  CHECK(alloc_reqs >= 4, "P2 re-requested after refusals, got %d", alloc_reqs);
  {
    uint8_t exp[kAdpduBytes];
    model_frame(exp, false, GM0, DOM0, 0);
    CHECK(last_frame().len == kAdpduBytes, "P2 committed length 82, got %u",
          last_frame().len);
    for (int i = 0; i < kAdpduBytes; ++i)
      CHECK(last_frame().b[i] == exp[i],
            "P2 AVAILABLE byte %d: got %02x want %02x", i,
            last_frame().b[i], exp[i]);
  }
  idle(3);
  CHECK(txreqs == 1, "P2 one TX request, got %d", txreqs);
  CHECK(!txreq_bad_slot, "P2 TX request carries the committed slot");
  CHECK(d->dbg_avail_index_o == 1, "P2 available_index incremented AFTER tx");
  CHECK((d->dbg_adv_state_o & 3) == 3, "P2 SM in WAITING");
  int a = last_arm_of(arms, arm0, SLOT_ADV, false);
  CHECK(a >= 0 && arms[a].deadline == now + 5000,
        "P2 T-ADP-ADV armed at 5 s (got %u want %u)",
        a >= 0 ? arms[a].deadline : 0, now + 5000);
}

// ---- P3: cadence — advertise restarts per send ----------------------
void Harness::check_advertise_cadence_restarts_per_send() {
  for (int k = 1; k <= 3; ++k) {
    size_t dn = draws.size();
    size_t fn = frames.size();
    size_t an = arms.size();
    CHECK(expire_slot(SLOT_ADV), "P3.%d T-ADP-ADV expiry", k);
    CHECK(wait_for([&]{ return draws.size() > dn; }), "P3.%d re-draw", k);
    CHECK(last_draw().kind == 2, "P3.%d cadence draw kind 2, got %u", k,
          last_draw().kind);
    CHECK(last_draw().ms <= 4000, "P3.%d kind-2 range, got %u", k,
          last_draw().ms);
    CHECK(expire_slot(SLOT_ADV), "P3.%d delay expiry", k);
    CHECK(wait_for([&]{ return frames.size() > fn; }), "P3.%d frame", k);
    CHECK(frames.size() == fn + 1, "P3.%d exactly one frame per cycle", k);
    uint32_t got = (uint32_t(last_frame().b[50]) << 24)
                 | (uint32_t(last_frame().b[51]) << 16)
                 | (uint32_t(last_frame().b[52]) << 8)
                 | uint32_t(last_frame().b[53]);
    CHECK(got == uint32_t(k), "P3.%d available_index sequence: got %u want %d",
          k, got, k);
    idle(3);
    int aa = last_arm_of(arms, an, SLOT_ADV, false);
    CHECK(aa >= 0 && arms[aa].deadline == now + 5000,
          "P3.%d ADV re-armed after send", k);
  }
  CHECK(d->dbg_avail_index_o == 4, "P3 index after 4 adverts, got %u",
        static_cast<unsigned>(d->dbg_avail_index_o));
}

// ---- P4: ENTITY_DISCOVER handling -----------------------------------
// (a) eid 0 in WAITING: stop ADV, delayed re-advertise
void Harness::check_entity_discover_handling() {
  dn = draws.size();
  fn = frames.size();
  an = arms.size();
  CHECK(send_txn(adp_txn(MSG_DISCOVER, 0, 0, 2, now)), "P4a discover consumed");
  CHECK(frees > 0 && last_free_slot == 2, "P4a rx slot freed");
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P4a draw after discover");
  CHECK(last_draw().kind == 2, "P4a discover delay is kind 2, got %u",
        last_draw().kind);
  CHECK(last_arm_of(arms, an, SLOT_ADV, true) >= 0, "P4a T-ADP-ADV cancelled");
  CHECK(expire_slot(SLOT_ADV), "P4a delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P4a responds ENTITY_AVAILABLE");
  idle(3);
  // (b) own eid in WAITING
  dn = draws.size(); fn = frames.size();
  CHECK(send_txn(adp_txn(MSG_DISCOVER, EID, 0, 1, now)), "P4b own-eid consumed");
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P4b draw for own eid");
  // (c) discover while in DELAY is ignored (Table 5.51)
  size_t dn2 = draws.size();
  CHECK(send_txn(adp_txn(MSG_DISCOVER, 0, 0, 1, now)), "P4c consumed in DELAY");
  idle(10);
  CHECK(draws.size() == dn2, "P4c DELAY ignores DISCOVER (no extra draw)");
  CHECK(expire_slot(SLOT_ADV), "P4c delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P4c advert sent");
  idle(3);
  // (d) foreign eid: ignored entirely
  dn = draws.size(); an = arms.size();
  fr = frees;
  CHECK(send_txn(adp_txn(MSG_DISCOVER, 0xF00DF00DF00DF00Dull, 0, 3, now)),
        "P4d foreign discover consumed");
  idle(10);
  CHECK(draws.size() == dn, "P4d foreign eid ignored (no draw)");
  CHECK(last_arm_of(arms, an, SLOT_ADV, true) < 0, "P4d no ADV cancel");
  CHECK(frees == fr + 1 && last_free_slot == 3, "P4d slot still freed");
}

// ---- P5: GM_CHANGE re-advertise + tick + fresh gm sampled -----------
constexpr uint64_t GM1 = 0x5150515051505150ull;
void Harness::check_gm_change_readvertises_a_fresh_gm() {
  dn = draws.size(); fn = frames.size(); an = arms.size();
  int ticks = 0;
  d->gm_change_i = 1;
  tick();
  d->gm_change_i = 0;
  for (int i = 0; i < 4; ++i) { if (d->gm_changed_tick_o & 1) ++ticks; tick(); }
  CHECK(ticks == 1, "P5 GPTP_GM_CHANGED ticks once, got %d", ticks);
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P5 re-advertise draw");
  CHECK(last_arm_of(arms, an, SLOT_ADV, true) >= 0, "P5 ADV cancelled");
  d->gm_id_i = GM1;                            // new GM before the build
  CHECK(expire_slot(SLOT_ADV), "P5 delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P5 frame after GM change");
  {
    uint8_t exp[kAdpduBytes];
    model_frame(exp, false, GM1, DOM0, 6);
    for (int i = 0; i < kAdpduBytes; ++i)
      CHECK(last_frame().b[i] == exp[i],
            "P5 gm-sampled byte %d: got %02x want %02x", i,
            last_frame().b[i], exp[i]);
  }
  idle(3);
  // GM_CHANGE in DELAY (after cancel+redraw start) must be ignored:
  dn = draws.size();
  CHECK(expire_slot(SLOT_ADV), "P5b ADV expiry into DELAY");
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P5b redraw");
  size_t dn3 = draws.size();
  d->gm_change_i = 1; tick(); d->gm_change_i = 0;
  idle(10);
  CHECK(draws.size() == dn3, "P5b DELAY ignores GM_CHANGE");
  size_t fn5 = frames.size();
  CHECK(expire_slot(SLOT_ADV), "P5b delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn5; }), "P5b advert sent");
  idle(3);
}

// ---- P6: LINK_DOWN / LINK_UP ----------------------------------------
void Harness::check_link_down_and_link_up() {
  fn = frames.size(); an = arms.size(); dn = draws.size();
  d->link_up_i = 0;
  idle(5);
  CHECK((d->dbg_adv_state_o & 3) == 0, "P6 LINK_DOWN -> DOWN");
  idle(150);   // long enough for any illegally queued frame to build out
  CHECK(frames.size() == fn, "P6 NO departing on link-down (Milan §5.6.3.5.6)");
  CHECK(last_arm_of(arms, an, SLOT_ADV, true) >= 0, "P6 timer cancelled");
  d->link_up_i = 1;
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P6 link-up draw");
  CHECK(last_draw().kind == 2,
        "P6 DOWN--LINK_UP-->DELAY uses kind 2 (F04.2), got %u", last_draw().kind);
  CHECK(expire_slot(SLOT_ADV), "P6 delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P6 advert after link-up");
  idle(3);
  idx_before_dep = d->dbg_avail_index_o;
}

// ---- P7: disable => ENTITY_DEPARTING, index rule, restart -----------
void Harness::check_disable_departs_then_restarts() {
  fn = frames.size();
  d->entity_enable_i = 0;
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P7 departing sent");
  {
    uint8_t exp[kAdpduBytes];
    model_frame(exp, true, GM1, DOM0, idx_before_dep);  // pre-reset value
    for (int i = 0; i < kAdpduBytes; ++i)
      CHECK(last_frame().b[i] == exp[i],
            "P7 DEPARTING byte %d: got %02x want %02x", i,
            last_frame().b[i], exp[i]);
  }
  idle(3);
  CHECK(d->dbg_avail_index_o == 0, "P7 index reset to 0 after DEPARTING");
  CHECK((d->dbg_adv_state_o & 3) == 0, "P7 SM DOWN after shutdown");
  // restart: enable with link up again -> kind 1 + index 0
  dn = draws.size(); fn = frames.size();
  d->entity_enable_i = 1;
  CHECK(wait_for([&]{ return draws.size() > dn; }), "P7 restart draw");
  CHECK(last_draw().kind == 1, "P7 restart uses T-ADP-DELAY-START, got %u",
        last_draw().kind);
  CHECK(expire_slot(SLOT_ADV), "P7 restart delay expiry");
  CHECK(wait_for([&]{ return frames.size() > fn; }), "P7 restart advert");
  {
    uint8_t exp[kAdpduBytes];
    model_frame(exp, false, GM1, DOM0, 0);
    bool same = memcmp(last_frame().b, exp, kAdpduBytes) == 0;
    CHECK(same, "P7 restart advert byte-exact with index 0");
  }
  idle(3);
}

// ---- P8: statistical draw separation (real KL_pp_prng) --------------
// collect kind-2 draws via DISCOVER cycles, kind-1 via disable/enable
void Harness::check_the_two_draw_kinds_are_separate() {
  unsigned max1 = 0;
  unsigned max2 = 0;
  int n1 = 0;
  int n2 = 0;
  bool r1ok = true;
  bool r2ok = true;
  for (int it = 0; it < 40; ++it) {
    dn = draws.size();
    CHECK(send_txn(adp_txn(MSG_DISCOVER, 0, 0, 0, now)), "P8 discover %d", it);
    if (!wait_for([&]{ return draws.size() > dn; })) break;
    unsigned ms = last_draw().ms;
    if (last_draw().kind == 2) { ++n2; if (ms > max2) max2 = ms; if (ms > 4000) r2ok = false; }
    CHECK(expire_slot(SLOT_ADV), "P8 delay expiry %d", it);
    wait_for([&]{ return (d->dbg_adv_state_o & 3) == 3; });
    idle(2);
  }
  for (int it = 0; it < 40; ++it) {
    d->entity_enable_i = 0;                    // departing
    wait_for([&]{ return (d->dbg_adv_state_o & 3) == 0 && d->txreq_valid_o == 0
                            && d->txn_ready_o; });
    idle(6);
    dn = draws.size();
    d->entity_enable_i = 1;
    if (!wait_for([&]{ return draws.size() > dn; })) break;
    unsigned ms = last_draw().ms;
    if (last_draw().kind == 1) { ++n1; if (ms > max1) max1 = ms; if (ms > 2000) r1ok = false; }
    CHECK(expire_slot(SLOT_ADV), "P8 startup delay expiry %d", it);
    wait_for([&]{ return (d->dbg_adv_state_o & 3) == 3; });
    idle(2);
  }
  CHECK(n1 == 40, "P8 forty kind-1 draws, got %d", n1);
  CHECK(n2 == 40, "P8 forty kind-2 draws, got %d", n2);
  CHECK(r1ok && max1 <= 2000, "P8 every kind-1 draw <= 2000 (max %u)", max1);
  CHECK(r2ok && max2 <= 4000, "P8 every kind-2 draw <= 4000 (max %u)", max2);
  CHECK(max2 > 2000, "P8 kind-2 exceeds the kind-1 span (max %u) — draws are DISTINCT", max2);
  CHECK(max1 != max2, "P8 observed maxima differ (%u vs %u)", max1, max2);
}

// ---- P9: talker-discovery SMs ---------------------------------------
// bindings: sink0 <- T1, sink1 <- T3, sink3 <- T2, sink5 <- T2
void Harness::set_bound(unsigned s, uint64_t eid, bool on) {
  d->bound_talker_eid_i[2*s]   = uint32_t(eid);
  d->bound_talker_eid_i[2*s+1] = uint32_t(eid >> 32);
  if (on) d->bound_i |= (1u << s); else d->bound_i &= ~(1u << s);
}

void Harness::check_talker_discovery_arms_and_refreshes() {
  set_bound(0, T1, true); set_bound(1, T3, true);
  set_bound(3, T2, true); set_bound(5, T2, true);
  idle(3);
  evts.clear();

  // (a) AVAILABLE from T1, gm/domain match -> one DISCOVERED for sink 0
  en = evts.size(); an = arms.size();
  load_remote(0, T1, 41, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9a consumed");
  idle(2);
  CHECK(evts.size() == en + 1, "P9a exactly one event, got %zu", evts.size() - en);
  CHECK(!evts.empty() && !evts.back().departed && evts.back().sink == 0,
        "P9a EVT_TK_DISCOVERED sink 0");
  CHECK(d->dbg_tk_discovered_o & 1, "P9a SM in TK_DISCOVERED");
  int a = last_arm_of(arms, an, SLOT_NOADP0 + 0, false);
  CHECK(a >= 0, "P9a T-ADP-NOADP armed");
  if (a >= 0)
    CHECK(arms[a].deadline == now + 20000,
          "P9a NOADP = rx valid_time (20 s), got +%u", arms[a].deadline - now);

  // (b) fresher index: no event, NOADP re-armed
  en = evts.size(); an = arms.size();
  load_remote(0, T1, 42, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9b consumed");
  idle(2);
  CHECK(evts.size() == en, "P9b no event on a fresh index");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 0, false) >= 0, "P9b NOADP re-armed");
}

// (c) one AVAILABLE from T2 discovers BOTH bound sinks, once each
void Harness::check_one_available_discovers_every_bound_sink() {
  en = evts.size(); an = arms.size();
  load_remote(1, T2, 7, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T2, 10, 1, now)), "P9c consumed");
  idle(2);
  CHECK(evts.size() == en + 2, "P9c two events, got %zu", evts.size() - en);
  if (evts.size() >= en + 2) {
    CHECK(!evts[en].departed && evts[en].sink == 3, "P9c DISCOVERED sink 3 first");
    CHECK(!evts[en+1].departed && evts[en+1].sink == 5, "P9c DISCOVERED sink 5 second");
  }
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 3, false) >= 0, "P9c NOADP sink 3");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 5, false) >= 0, "P9c NOADP sink 5");

  // (d) gm/domain guard (Milan §5.6.4.5.1; never fires on a conformant net)
  en = evts.size();
  load_remote(2, T3, 5, GM1 ^ 0xFFULL, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T3, 10, 2, now)), "P9d gm-mismatch consumed");
  idle(2);
  CHECK(evts.size() == en, "P9d GM mismatch ignored");
  load_remote(2, T3, 5, GM1, 0x07, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T3, 10, 2, now)), "P9d dom-mismatch consumed");
  idle(2);
  CHECK(evts.size() == en, "P9d domain mismatch ignored");
  CHECK(!(d->dbg_tk_discovered_o & 2), "P9d sink 1 still undiscovered");
  load_remote(2, T3, 5, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T3, 10, 2, now)), "P9d good consumed");
  idle(2);
  CHECK(evts.size() == en + 1 && !evts.back().departed && evts.back().sink == 1,
        "P9d matching AVAILABLE discovers sink 1");
}

// (e) talker restart: index <= last with matching GM => DEPARTED+DISCOVERED
void Harness::check_talker_restart_and_stale_index_rules() {
  en = evts.size();
  load_remote(0, T1, 2, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9e consumed");
  idle(3);
  CHECK(evts.size() == en + 2, "P9e restart fires a pair, got %zu", evts.size() - en);
  if (evts.size() >= en + 2) {
    CHECK(evts[en].departed && evts[en].sink == 0, "P9e DEPARTED first");
    CHECK(!evts[en+1].departed && evts[en+1].sink == 0, "P9e then DISCOVERED");
  }
  CHECK(d->dbg_tk_discovered_o & 1, "P9e still TK_DISCOVERED");
  // index stored: 3 > 2 is fresh, no event
  en = evts.size();
  load_remote(0, T1, 3, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9e2 consumed");
  idle(2);
  CHECK(evts.size() == en, "P9e2 restart stored the new index");

  // (f) stale index + GM mismatch => DEPARTED only, back to NOT_DISCOVERED
  en = evts.size(); an = arms.size();
  load_remote(0, T1, 1, GM1 ^ 0x1ULL, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9f consumed");
  idle(3);
  CHECK(evts.size() == en + 1 && evts.back().departed && evts.back().sink == 0,
        "P9f DEPARTED only");
  CHECK(!(d->dbg_tk_discovered_o & 1), "P9f back to TK_NOT_DISCOVERED");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 0, true) >= 0, "P9f NOADP stopped");
  // rediscover for the next steps
  en = evts.size();
  load_remote(0, T1, 5, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9f2 consumed");
  idle(2);
  CHECK(evts.size() == en + 1 && !evts.back().departed, "P9f2 rediscovered");

  // (g) interface_index mismatch in TK_DISCOVERED: ignored entirely
  en = evts.size(); an = arms.size();
  load_remote(0, T1, 9, GM1, DOM0, 1, 10, MSG_AVAIL);   // remote if 1 != saved 0
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9g consumed");
  idle(3);
  CHECK(evts.size() == en, "P9g interface mismatch: no events");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 0, false) < 0, "P9g no re-arm");
  // record was NOT updated by the mismatch: 6 > 5 is still fresh (no event)
  load_remote(0, T1, 6, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 10, 0, now)), "P9g2 consumed");
  idle(2);
  CHECK(evts.size() == en, "P9g2 record untouched by mismatched frame");
}

// (h) ENTITY_DEPARTING departs every matched discovered sink, once each
void Harness::check_departing_aging_unbind_and_backpressure() {
  en = evts.size(); an = arms.size();
  load_remote(1, T2, 0, GM1, DOM0, 0, 0, MSG_DEPART);
  CHECK(send_txn(adp_txn(MSG_DEPART, T2, 0, 1, now)), "P9h consumed");
  idle(3);
  CHECK(evts.size() == en + 2, "P9h two DEPARTED, got %zu", evts.size() - en);
  if (evts.size() >= en + 2) {
    CHECK(evts[en].departed && evts[en].sink == 3, "P9h DEPARTED sink 3");
    CHECK(evts[en+1].departed && evts[en+1].sink == 5, "P9h DEPARTED sink 5");
  }
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 3, true) >= 0, "P9h NOADP 3 stopped");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 5, true) >= 0, "P9h NOADP 5 stopped");
  // departing again: both already NOT_DISCOVERED -> no events
  en = evts.size();
  CHECK(send_txn(adp_txn(MSG_DEPART, T2, 0, 1, now)), "P9h2 consumed");
  idle(3);
  CHECK(evts.size() == en, "P9h2 departing when undiscovered: silent");

  // (i) T-ADP-NOADP aging: expiry fires exactly one DEPARTED
  en = evts.size();
  CHECK(t_armed[SLOT_NOADP0 + 0], "P9i NOADP armed for sink 0");
  CHECK(expire_slot(SLOT_NOADP0 + 0), "P9i NOADP expiry");
  idle(3);
  CHECK(evts.size() == en + 1 && evts.back().departed && evts.back().sink == 0,
        "P9i aging fires EVT_TK_DEPARTED");
  CHECK(!(d->dbg_tk_discovered_o & 1), "P9i SM left TK_DISCOVERED");

  // (j) NOADP deadline follows the received valid_time (vt = 5 -> 10 s)
  an = arms.size(); en = evts.size();
  load_remote(0, T1, 10, GM1, DOM0, 0, 5, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, T1, 5, 0, now)), "P9j consumed");
  idle(2);
  int a = last_arm_of(arms, an, SLOT_NOADP0 + 0, false);
  CHECK(a >= 0 && arms[a].deadline == now + 10000,
        "P9j NOADP = vt * 2 s (got +%u want 10000)",
        a >= 0 ? arms[a].deadline - now : 0);

  // (k) unbind disarms silently; NOADP cancelled
  en = evts.size(); an = arms.size();
  set_bound(0, T1, false);
  idle(4);
  CHECK(evts.size() == en, "P9k unbind: no event");
  CHECK(!(d->dbg_tk_discovered_o & 1), "P9k SM disarmed");
  CHECK(last_arm_of(arms, an, SLOT_NOADP0 + 0, true) >= 0, "P9k NOADP cancelled");
  set_bound(0, T1, true);
  idle(2);
  CHECK(!(d->dbg_tk_discovered_o & 1), "P9k re-bind starts NOT_DISCOVERED");

  // (l) unknown talker eid: consumed, freed, no events
  en = evts.size(); fr = frees;
  load_remote(3, 0xE0E0E0E0E0E0E0E0ull, 1, GM1, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, 0xE0E0E0E0E0E0E0E0ull, 10, 3, now)),
        "P9l consumed");
  idle(2);
  CHECK(evts.size() == en, "P9l unbound talker ignored");
  CHECK(frees == fr + 1 && last_free_slot == 3, "P9l slot freed");

  // (m) dispatch face backpressure: ready drops while processing
  load_remote(0, T1, 20, GM1, DOM0, 0, 10, MSG_AVAIL);
  {
    Rec r = adp_txn(MSG_AVAIL, T1, 10, 0, now);
    for (int i = 0; i < REC_WORDS; ++i) d->txn_i[i] = r.w[i];
    d->txn_valid_i = 1;
    wait_for([&]{ return d->txn_ready_o == 1; });
    tick();                                  // handshake
    d->txn_valid_i = 0;
    tick();
    CHECK(d->txn_ready_o == 0, "P9m ready low while a txn is processed");
    wait_for([&]{ return d->txn_ready_o == 1; });
  }
  idle(3);
}

// ---- P10: pool-protocol invariants accumulated over the whole run ----
void Harness::check_pool_protocol_invariants() {
  CHECK(!oversize_seen, "P10 ADP never requests the oversize slot");
  CHECK(!write_bad, "P10 every slot write in an ALLOC slot within bounds");
  CHECK(!write_before_gnt, "P10 no write before grant, ever");
  CHECK(!req_two_cycles, "P10 alloc_req always a one-cycle pulse");
  CHECK(!txreq_bad_slot, "P10 every TX request names a READY slot");
  CHECK(txreqs == static_cast<int>(frames.size()),
        "P10 one TX request per committed frame");
  {
    bool all82 = true;
    for (auto& f : frames) if (f.len != kAdpduBytes) all82 = false;
    CHECK(all82, "P10 every committed frame is 82 bytes");
  }
}


int Harness::report() {
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int Harness::run_suite() {
  configure_the_entity_and_release_reset();
  check_reset_state();
  check_startup_draw_and_delay_arm();
  check_first_entity_available_is_byte_exact();
  check_advertise_cadence_restarts_per_send();
  check_entity_discover_handling();
  check_gm_change_readvertises_a_fresh_gm();
  check_link_down_and_link_up();
  check_disable_departs_then_restarts();
  check_the_two_draw_kinds_are_separate();
  check_talker_discovery_arms_and_refreshes();
  check_one_available_discovers_every_bound_sink();
  check_talker_restart_and_stale_index_rules();
  check_departing_aging_unbind_and_backpressure();
  check_pool_protocol_invariants();
  return report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Harness h;
  return h.run_suite();
}

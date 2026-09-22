// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_acmp_talker suite — independent expectations, never DUT logic.
//
// Every expected response below is spelled out field-by-field from the
// 05 §6bis tables (F05.11) and the DA-gate law (F05.12), not derived from
// DUT state: the C++ model is the document. Covered: both response tables
// INCLUDING their deliberate difference (PROBE echoes FAST_CONNECT +
// STREAMING_WAIT and FORCES REGISTERING_FAILED = 0 — the flag law the
// pipewire reference inverted — while GET_TX_STATE zeroes the listener
// fields and reads REGISTERING_FAILED LIVE from the srp face); the DA
// lifecycle walk none -> maap-granted -> declared; MAAP conflict ->
// withdraw -> T-SRP-LEAVEALL2 (2 x PRNG draw, compressed by TB-driven
// expiry) -> re-alloc -> re-declare with the NEW DA; the PCP-change
// backoff that KEEPS the DA; T-SRP-DAFRESH freshness expiry; the V3
// truncated-PDU zero-fill; per-source independence; and the stateless
// property (identical query twice around interleaved traffic = identical
// response bytes). Sections I/J own the maap face: the gate level
// declaring_o is watched for EDGES (a refused ALLOC_DA keeps it shut even
// with a Listener registered, the following grant opens it), and an ABSENT
// maap must degrade — the request is abandoned after P-MAAP-ACCEPT-CYC and
// the walker keeps answering, which is the regression test for the
// S_EV_MAAP deadlock.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <utility>
#include <vector>
#include "VKL_acmp_talker.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- independent 393-bit pp_txn_t codec (03 §4 declared widths) --------
constexpr int REC_WORDS = 13;

struct Rec {
  uint32_t w[REC_WORDS];
  Rec() { memset(w, 0, sizeof w); }
  void set(int lsb, int width, uint64_t v) {
    for (int i = 0; i < width; ++i) {
      int b = lsb + i;
      if ((v >> i) & 1ull) w[b >> 5] |= (1u << (b & 31));
    }
  }
};

// the record's field offsets, in bits: a plain-integer address map, passed
// straight to Rec::set, so constexpr rather than an enum class (Enum.2/Enum.5)
constexpr int F_DISP = 0;
constexpr int F_DEADLINE = 2;
constexpr int F_TX_SLOT = 34;
constexpr int F_HZ_KEY = 37;
constexpr int F_HZ_CLASS = 53;
constexpr int F_RX_SLOT = 57;
constexpr int F_UNIQUE_ID = 60;
constexpr int F_CONFIG_IX = 76;
constexpr int F_DESC_IX = 92;
constexpr int F_DESC_TYPE = 108;
constexpr int F_OPCODE = 124;
constexpr int F_CR = 140;
constexpr int F_U = 141;
constexpr int F_SEQ = 142;
constexpr int F_TARGET_EID = 158;
constexpr int F_CTLR_EID = 222;
constexpr int F_SRC_MAC = 286;
constexpr int F_CDL = 334;
constexpr int F_STATUS = 345;
constexpr int F_MSG_TYPE = 350;
constexpr int F_PROTOCOL = 354;
constexpr int F_ARRIVAL = 357;
constexpr int F_IF_INDEX = 389;
constexpr int F_ORIGIN = 391;

constexpr int O_RX = 0;
constexpr int P_ACMP = 1;
constexpr int D_ACMP_MC = 1;
constexpr int HZ_STREAM_CFG = 2;

// ---- 05 §3 / F05.11 constants (the document, not the DUT) --------------
constexpr int MT_PROBE = 0;
constexpr int MT_DISC = 2;
constexpr int MT_GTXS = 4;
constexpr int MT_GTXC = 12;
constexpr int ST_OK = 0;
constexpr int ST_TK_UNKNOWN = 2;
constexpr int ST_DMAC_FAIL = 3;
constexpr int ST_NSUPP = 31;
constexpr uint16_t FL_FC = 0x0002;
constexpr uint16_t FL_SW = 0x0008;
constexpr uint16_t FL_RF = 0x0040;
// lstn_reg_state codes, 02 §6 F02.10: the SRP engine's four-packed Listener
// declaration (802.1Q §35.2.2.7.4, srp_pkg::srp_decl_e). Written here as the
// contract, never read from the package, so a package that moves a code
// fails this suite instead of moving it with it.
constexpr int LSN_NONE = 0;
constexpr int LSN_ASKING_FAILED = 1;
constexpr int LSN_READY = 2;
constexpr int LSN_READY_FAILED = 3;

constexpr int N_SRC = 8;
constexpr int TMR_BASE = 17;           // IF + 2*SI (08 §5 F08.4 order)
constexpr int OWNER_BASE = 0x50;
constexpr uint32_t T_DAFRESH = 15000;
// P-MAAP-ACCEPT-CYC: the documented accept window of the maap request face
// (KL_acmp_talker MAAP_ACCEPT_CYC_P default). Written here as the contract,
// not read from the DUT.
constexpr int MAAP_TMO = 1024;
// P-MAAP-RSP-MS: the documented response bound of an ACCEPTED maap request
// (KL_acmp_talker MAAP_RSP_MS_P default). Written here as the contract, not
// read from the DUT. Its lower bound is the IEEE 1722-2016 Annex B claim
// walk (3 x probe_timer, each < MAAP_PROBE_INTERVAL_BASE +
// MAAP_PROBE_INTERVAL_VARIATION = 600 ms, so <= 1800 ms per attempt); its
// upper bound is T-SRP-DAFRESH.
constexpr uint32_t MAAP_RSP_MS = 10000;

constexpr uint64_t OWN_EID = 0x0102030405060708ull;
static uint64_t sid_of(int s)  { return 0xAB00000000000000ull | unsigned(s); }
static uint64_t da_pool(int n) { return 0x91E0F0000100ull + unsigned(n); }
constexpr int VID = 2;

// the RX-slot model backing the DUT's sync-read face
constexpr int RX_SLOTS = 4;            // slots this harness backs
constexpr int SLOT_BYTES = 576;        // bytes held per backed slot

// ---- recorders ----------------------------------------------------------
struct Resp {
  uint8_t mt;
  uint8_t status;
  uint8_t ifx;
  uint64_t sid;
  uint64_t ceid;
  uint64_t teid;
  uint64_t leid;
  uint64_t da;
  uint16_t tuid;
  uint16_t luid;
  uint16_t cc;
  uint16_t seq;
  uint16_t flags;
  uint16_t vlan;
  bool operator==(const Resp& o) const { return memcmp(this, &o, sizeof o) == 0; }
};
struct GateEv { bool open; int src; uint64_t sid; uint64_t da; int vlan; };
struct Arm    { int slot; int owner; uint32_t dl; bool cancel; };
struct MReq   { int src; bool rel; };

namespace {

//! The talker, its four service models, the recorders and the tally in one
//! object. `checks`/`fails` were file-scope mutables (I.2) and the lettered
//! phases below were one 642-line `main` (F.3).
struct Hn {
  const milan::tb::Model<VKL_acmp_talker> model;
  VKL_acmp_talker* const d = model.get();
  // rx-slot model (sync read, committed length)
  uint8_t slot_mem[RX_SLOTS][SLOT_BYTES];
  uint16_t slot_len[RX_SLOTS];
  bool pend_rd = false;
  int pend_slot = 0;
  int pend_addr = 0;
  // maap auto-responder
  int  mrsp_cnt = 0;
  bool mrsp_ok = true;
  bool mrsp_rel = false;
  uint64_t mrsp_da = 0;
  bool auto_grant = true;
  int da_seq = 0;
  bool grant_ok = true;              // false = the allocator REFUSES the alloc
  // request-face observation (works with ready low, where no request is ever
  // accepted and the mreqs log below stays empty)
  int  offers = 0;                   // rising edges of maap_req_valid_o
  // offers split by kind. A RELEASE_DA has no stimulus that can ask for it
  // twice (the record naming the address is wiped by the same event that
  // asks for it), so "was it re-offered after an abandon" is the only
  // observation that can tell a held release from a lost one.
  int  offers_rel = 0;
  int  offers_alloc = 0;
  int  hold_cur = 0;                 // cycles a request has been offered
  int  hold_last = 0;                // cycles the last request was offered
  // declaring_o edge log: the gate LEVEL must be seen MOVING, not read once
  uint32_t decl_prev = 0;
  std::vector<std::pair<int, bool>> decl_edges;   // {src, rising}
  int last_send_cyc = 0;
  // prng responder
  int  draw_cnt = 0;
  uint16_t draw_val = 10000;
  bool prng_busy = false;
  std::vector<int> draws;
  // captures
  std::vector<Resp>   resps;
  std::vector<GateEv> gates;
  std::vector<Arm>    arms;
  std::vector<MReq>   mreqs;
  int frees = 0;
  int consumed = 0;

  int checks = 0;
  int fails = 0;

  // The eight boot-walk destination MACs, and the two values a later phase
  // reads back from an earlier one; all three were locals of `main`.
  uint64_t da[N_SRC];
  uint32_t t2 = 0;
  uint64_t da3b = 0;

  Hn() {
    memset(slot_mem, 0, sizeof slot_mem);
    memset(slot_len, 0, sizeof slot_len);
  }

  void tick() {
    // scheduled single-cycle inputs
    d->maap_rsp_valid_i = 0;
    d->prng_draw_valid_i = 0;
    if (mrsp_cnt > 0 && --mrsp_cnt == 0) {
      d->maap_rsp_valid_i = 1;
      d->maap_rsp_ok_i = mrsp_ok;
      d->maap_rsp_da_i = mrsp_da;
    }
    if (draw_cnt > 0 && --draw_cnt == 0) {
      d->prng_draw_valid_i = 1;
      d->prng_draw_ms_i = draw_val;
      prng_busy = false;
    }
    d->prng_draw_busy_i = prng_busy;
    // sync-read data from LAST cycle's request
    d->rxs_rd_data_i = pend_rd ? slot_mem[pend_slot][pend_addr] : 0;

    d->clk_i = 0; d->eval();
    d->rxs_slot_len_i = slot_len[d->rxs_rd_slot_o & 3];
    d->eval();

    // observe pre-edge (what the registers see)
    if (d->resp_valid_o) {
      Resp r{};
      r.mt = d->resp_msg_type_o;  r.status = d->resp_status_o;
      r.ifx = d->resp_if_index_o;
      r.sid = d->resp_stream_id_o; r.ceid = d->resp_controller_eid_o;
      r.teid = d->resp_talker_eid_o; r.leid = d->resp_listener_eid_o;
      r.da = d->resp_dest_mac_o;
      r.tuid = d->resp_talker_uid_o; r.luid = d->resp_listener_uid_o;
      r.cc = d->resp_conn_count_o; r.seq = d->resp_seq_id_o;
      r.flags = d->resp_flags_o; r.vlan = d->resp_vlan_id_o;
      resps.push_back(r);
    }
    if (d->gate_open_o || d->gate_close_o)
      gates.push_back({bool(d->gate_open_o), int(d->gate_src_o),
                       uint64_t(d->gate_stream_id_o),
                       uint64_t(d->gate_da_o), int(d->gate_vlan_o)});
    if (d->tmr_arm_valid_o)
      arms.push_back({int(d->tmr_arm_slot_o), int(d->tmr_arm_owner_o),
                      uint32_t(d->tmr_arm_deadline_ms_o),
                      bool(d->tmr_arm_cancel_o)});
    if (d->maap_req_valid_o) {
      if (hold_cur == 0) {
        ++offers;
        if (d->maap_req_release_o) ++offers_rel; else ++offers_alloc;
      }
      ++hold_cur;
    } else if (hold_cur != 0) {
      hold_last = hold_cur; hold_cur = 0;
    }
    if (d->maap_req_valid_o && d->maap_req_ready_i) {
      MReq m{int(d->maap_req_src_o), bool(d->maap_req_release_o)};
      mreqs.push_back(m);
      if (auto_grant) {
        mrsp_cnt = 3; mrsp_ok = grant_ok; mrsp_rel = m.rel;
        mrsp_da = (m.rel || !grant_ok) ? 0 : da_pool(da_seq++);
      }
    }
    {
      uint32_t dcl = uint32_t(d->declaring_o);
      if (dcl != decl_prev) {
        for (int s = 0; s < N_SRC; ++s)
          if (((dcl ^ decl_prev) >> s) & 1)
            decl_edges.push_back({s, bool((dcl >> s) & 1)});
        decl_prev = dcl;
      }
    }
    if (d->prng_draw_req_o) {
      draws.push_back(int(d->prng_draw_kind_o));
      prng_busy = true; draw_cnt = 2;
    }
    if (d->rxs_free_o) ++frees;
    if (d->txn_ready_o && d->txn_valid_i) ++consumed;
    pend_rd = d->rxs_rd_en_o; pend_slot = d->rxs_rd_slot_o & 3;
    pend_addr = d->rxs_rd_addr_o;

    d->clk_i = 1; d->eval();
    d->tmr_exp_valid_i = 0;           // expiry pulses last one edge
    d->srp_pcp_change_i = 0;
    d->maap_conflict_valid_i = 0;
  }

  void run(int n) { for (int i = 0; i < n; ++i) tick(); }

  // hand-drive ONE maap response on the next tick. Used where the timing of
  // the response relative to the bound is the thing under test, so the
  // auto-responder (which always answers 3 cycles after an accept) cannot
  // be used.
  void inject_rsp(bool ok, uint64_t dda, bool rel = false) {
    mrsp_cnt = 1; mrsp_ok = ok; mrsp_da = dda; mrsp_rel = rel;
  }

  // one talker command through the dispatch-in face + RX slot model
  bool send(int mt, uint16_t uid, uint64_t ctlr, uint16_t seq,
            uint64_t leid, uint16_t luid, uint16_t flags,
            int ifx = 0, uint16_t pdu_len = 56, uint64_t target = OWN_EID) {
    const int s = 1;
    memset(slot_mem[s], 0, SLOT_BYTES);
    for (int i = 0; i < 8; ++i)
      slot_mem[s][28 + i] = uint8_t(leid >> (8 * (7 - i)));
    slot_mem[s][38] = uint8_t(luid >> 8); slot_mem[s][39] = uint8_t(luid);
    slot_mem[s][50] = uint8_t(flags >> 8); slot_mem[s][51] = uint8_t(flags);
    slot_len[s] = pdu_len;

    Rec r;
    r.set(F_ORIGIN, 2, O_RX);          r.set(F_IF_INDEX, 2, unsigned(ifx));
    r.set(F_ARRIVAL, 32, d->now_ms_i); r.set(F_PROTOCOL, 3, P_ACMP);
    r.set(F_MSG_TYPE, 4, unsigned(mt)); r.set(F_CDL, 11, 44);
    r.set(F_SRC_MAC, 48, 0x00E04C000001ull);
    r.set(F_CTLR_EID, 64, ctlr);       r.set(F_TARGET_EID, 64, target);
    r.set(F_SEQ, 16, seq);             r.set(F_OPCODE, 16, unsigned(mt));
    r.set(F_UNIQUE_ID, 16, uid);       r.set(F_RX_SLOT, 3, unsigned(s));
    r.set(F_HZ_CLASS, 4, HZ_STREAM_CFG); r.set(F_HZ_KEY, 16, uid);
    r.set(F_TX_SLOT, 3, 7);
    r.set(F_DEADLINE, 32, uint32_t(d->now_ms_i + 50));
    r.set(F_DISP, 2, D_ACMP_MC);
    for (int i = 0; i < REC_WORDS; ++i) d->txn_i[i] = r.w[i];

    int before = consumed;
    int free_before = frees;
    d->txn_valid_i = 1;
    // budget > P-MAAP-ACCEPT-CYC on purpose: a command offered while a maap
    // request is outstanding must still be served once that window closes
    int i = 0;
    for (; i < 4 * MAAP_TMO && consumed == before; ++i) tick();
    last_send_cyc = i;
    d->txn_valid_i = 0;
    // txn_ready_o marks input acceptance. Keep the historical synchronous
    // helper contract by waiting for this command's RX slot retirement before
    // the caller grades its response and action strobes.
    for (int j = 0; j < 4 * MAAP_TMO && frees == free_before; ++j) tick();
    return consumed != before;
  }

  // ---- declaring_o (the per-source DA gate LEVEL) ----
  uint32_t decl_mask() const { return uint32_t(d->declaring_o); }
  bool saw_edge(int src, bool rising) const {
    for (const auto& e : decl_edges)
      if (e.first == src && e.second == rising) return true;
    return false;
  }
  void clear_edges() { decl_edges.clear(); }

  // ---- pop-checkers ----
  Resp pop_resp(const char* tag) {
    Resp r{};
    CHECK(!resps.empty(), "%s: response missing", tag);
    if (!resps.empty()) { r = resps.front(); resps.erase(resps.begin()); }
    return r;
  }
  void expect_resp(const char* t, const Resp& e) {
    Resp g = pop_resp(t);
    CHECK(g.mt == e.mt,       "%s msg_type got %u want %u", t, g.mt, e.mt);
    CHECK(g.status == e.status, "%s status got %u want %u", t, g.status, e.status);
    CHECK(g.sid == e.sid,     "%s stream_id got %016llx", t, static_cast<unsigned long long>(g.sid));
    CHECK(g.ceid == e.ceid,   "%s controller_eid got %016llx", t, static_cast<unsigned long long>(g.ceid));
    CHECK(g.teid == e.teid,   "%s talker_eid got %016llx", t, static_cast<unsigned long long>(g.teid));
    CHECK(g.leid == e.leid,   "%s listener_eid got %016llx", t, static_cast<unsigned long long>(g.leid));
    CHECK(g.tuid == e.tuid,   "%s talker_uid got %u", t, g.tuid);
    CHECK(g.luid == e.luid,   "%s listener_uid got %u", t, g.luid);
    CHECK(g.da == e.da,       "%s dest_mac got %012llx", t, static_cast<unsigned long long>(g.da));
    CHECK(g.cc == e.cc,       "%s connection_count got %u", t, g.cc);
    CHECK(g.seq == e.seq,     "%s sequence_id got %u", t, g.seq);
    CHECK(g.flags == e.flags, "%s flags got %04x want %04x", t, g.flags, e.flags);
    CHECK(g.vlan == e.vlan,   "%s vlan got %u", t, g.vlan);
    CHECK(g.ifx == e.ifx,     "%s if_index got %u", t, g.ifx);
  }
  void expect_open(const char* t, int src, uint64_t da) {
    CHECK(!gates.empty(), "%s: gate strobe missing", t);
    if (gates.empty()) return;
    GateEv g = gates.front(); gates.erase(gates.begin());
    CHECK(g.open,             "%s expected open, got close", t);
    CHECK(g.src == src,       "%s open src got %d", t, g.src);
    CHECK(g.sid == sid_of(src), "%s open sid got %016llx", t, static_cast<unsigned long long>(g.sid));
    CHECK(g.da == da,         "%s open da got %012llx want %012llx", t,
          static_cast<unsigned long long>(g.da), static_cast<unsigned long long>(da));
    CHECK(g.vlan == VID,      "%s open vlan got %d", t, g.vlan);
  }
  void expect_close(const char* t, int src) {
    CHECK(!gates.empty(), "%s: gate strobe missing", t);
    if (gates.empty()) return;
    GateEv g = gates.front(); gates.erase(gates.begin());
    CHECK(!g.open,      "%s expected close, got open", t);
    CHECK(g.src == src, "%s close src got %d", t, g.src);
  }
  void expect_arm(const char* t, int src, uint32_t dl, bool cancel) {
    CHECK(!arms.empty(), "%s: timer arm missing", t);
    if (arms.empty()) return;
    Arm a = arms.front(); arms.erase(arms.begin());
    CHECK(a.slot == TMR_BASE + src,    "%s arm slot got %d", t, a.slot);
    CHECK(a.owner == OWNER_BASE + src, "%s arm owner got %02x", t, a.owner);
    CHECK(a.cancel == cancel,          "%s arm cancel got %d", t, a.cancel);
    if (!cancel)
      CHECK(a.dl == dl, "%s arm deadline got %u want %u", t, a.dl, dl);
    else ++checks;   // deadline is dont-care on cancel: keep tallies even
  }
  void expect_mreq(const char* t, int src, bool rel) {
    CHECK(!mreqs.empty(), "%s: maap request missing", t);
    if (mreqs.empty()) return;
    MReq m = mreqs.front(); mreqs.erase(mreqs.begin());
    CHECK(m.src == src, "%s maap src got %d", t, m.src);
    CHECK(m.rel == rel, "%s maap rel got %d", t, m.rel);
  }
  void drained(const char* t) {
    CHECK(resps.empty() && gates.empty() && arms.empty() && mreqs.empty(),
          "%s: leftovers resp=%zu gate=%zu arm=%zu mreq=%zu", t,
          resps.size(), gates.size(), arms.size(), mreqs.size());
  }
  void fire_expiry(int src) {
    d->tmr_exp_valid_i = 1;
    d->tmr_exp_slot_i  = TMR_BASE + src;
    d->tmr_exp_owner_i = OWNER_BASE + src;
    tick();
  }
  void set_lsn(int src, int st) {
    uint16_t v = d->srp_lsn_reg_state_i;
    v = uint16_t((v & ~(3u << (2 * src))) | (unsigned(st) << (2 * src)));
    d->srp_lsn_reg_state_i = v;
    run(12);
  }

  void configure_the_talker_and_release_reset();
  void check_the_boot_walk_allocates_every_source_da();
  void check_probe_tx_success_and_the_two_trap_tables();
  void check_error_no_op_and_unsupported_paths();
  void check_dafresh_expiry();
  void check_a_maap_conflict_withdraws_and_reallocates();
  void check_a_conflict_while_da_ok_reallocates_without_backoff();
  void check_a_pcp_change_backs_off_and_keeps_the_da();
  void check_per_source_independence_across_interleave();
  void check_a_source_removed_from_the_configuration();
  void check_a_refused_maap_grant_keeps_the_gate_shut();
  void check_an_absent_maap_degrades_without_wedging();
  void check_an_unanswered_accept_strands_then_resumes();
  void check_a_late_stale_response_is_swallowed();
  void check_a_teardown_while_the_maap_face_is_busy();
  int report();
  int run_suite();
};

// common echo skeleton for an expected response
static Resp echo(int mt, int st, uint16_t uid, uint64_t ctlr, uint16_t seq,
                 uint64_t leid, uint16_t luid) {
  Resp e{};
  e.mt = uint8_t(mt | 1); e.status = uint8_t(st); e.ifx = 0;
  e.ceid = ctlr; e.teid = OWN_EID; e.leid = leid;
  e.tuid = uid; e.luid = luid; e.cc = 0; e.seq = seq;
  e.sid = 0; e.da = 0; e.flags = 0; e.vlan = 0;
  return e;
}

// The listener entity id and the controller entity id every phase quotes.
constexpr uint64_t L1 = 0x1111222233334444ull;
constexpr uint64_t C1 = 0xC0FFEE00000000C1ull;

// static configuration before reset release
void Hn::configure_the_talker_and_release_reset() {
  d->rst_n = 0; d->txn_valid_i = 0;
  d->own_entity_id_i = OWN_EID;
  d->cfg_src_en_i = 0xFF;
  d->cfg_src_iface_i = 0;                 // all sources on interface 0
  for (int s = 0; s < N_SRC; ++s) {
    d->cfg_stream_id_i[2 * s]     = uint32_t(sid_of(s));
    d->cfg_stream_id_i[2 * s + 1] = uint32_t(sid_of(s) >> 32);
  }
  d->srp_lsn_reg_state_i = 0;
  d->srp_class_vid_i = VID;
  d->srp_pcp_change_i = 0;
  d->maap_req_ready_i = 1;
  d->maap_rsp_valid_i = 0; d->maap_conflict_valid_i = 0;
  d->maap_conflict_src_i = 0;
  d->tmr_exp_valid_i = 0; d->tmr_exp_slot_i = 0; d->tmr_exp_owner_i = 0;
  d->prng_draw_busy_i = 0; d->prng_draw_valid_i = 0; d->prng_draw_ms_i = 0;
  d->now_ms_i = 100;
  for (int i = 0; i < 5; ++i) tick();
  d->rst_n = 1;
}

// ---- A: boot walk — every enabled source allocates its DA -----------
void Hn::check_the_boot_walk_allocates_every_source_da() {
  run(400);
  for (int s = 0; s < N_SRC; ++s) { da[s] = da_pool(s); }
  CHECK(mreqs.size() == N_SRC, "A allocs got %zu", mreqs.size());
  for (int s = 0; s < N_SRC; ++s) expect_mreq("A", s, false);
  CHECK(gates.empty(), "A no declarations without probe/listener");
  CHECK(resps.empty(), "A no responses");
  CHECK(arms.empty(), "A no timer arms");
  drained("A");
}

// ---- B: PROBE_TX success + the two trap tables ----------------------
void Hn::check_probe_tx_success_and_the_two_trap_tables() {
  uint32_t t1 = 1000; d->now_ms_i = t1;
  CHECK(send(MT_PROBE, 3, C1, 0x100, L1, 7, 0x804A), "B1 consumed");
  run(8);
  expect_arm("B1 dafresh", 3, t1 + T_DAFRESH, false);
  expect_open("B1 declare", 3, da[3]);
  CHECK(saw_edge(3, true), "B1 declaring_o[3] OBSERVED 0 -> 1");
  CHECK(decl_mask() == 0x08u, "B1 gate level, got 0x%02x", decl_mask());
  {
    Resp e = echo(MT_PROBE, ST_OK, 3, C1, 0x100, L1, 7);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;
    e.flags = FL_FC | FL_SW;                 // echoed; 0x8040 must NOT echo
    expect_resp("B1", e);
  }
  {
    CHECK(send(MT_GTXS, 3, C1, 0x101, L1, 7, 0xFFFF), "B2 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x101, 0, 0);  // listener fields 0
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID; e.flags = 0;
    expect_resp("B2", e);
  }
  // the deliberate difference: RF live in GET_TX_STATE, forced 0 in PROBE
  set_lsn(3, LSN_ASKING_FAILED);
  {
    CHECK(send(MT_GTXS, 3, C1, 0x102, 0, 0, 0), "B3 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x102, 0, 0);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;
    e.flags = FL_RF;                          // live ASKING_FAILED
    expect_resp("B3", e);
  }
  t2 = 2000; d->now_ms_i = t2;
  CHECK(send(MT_PROBE, 3, C1, 0x103, L1, 7, FL_FC | FL_SW), "B4 consumed");
  expect_arm("B4 re-ping", 3, t2 + T_DAFRESH, false);
  {
    Resp e = echo(MT_PROBE, ST_OK, 3, C1, 0x103, L1, 7);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;
    e.flags = FL_FC | FL_SW;                  // RF forced 0 despite ASKING_FAILED
    expect_resp("B4", e);
  }
  // stateless: identical query twice = identical bytes
  CHECK(send(MT_GTXS, 3, C1, 0x104, 0, 0, 0), "B5a consumed");
  Resp b5a = pop_resp("B5a");
  CHECK(send(MT_GTXS, 3, C1, 0x104, 0, 0, 0), "B5b consumed");
  Resp b5b = pop_resp("B5b");
  CHECK(b5a == b5b, "B5 identical query = identical answer");
  CHECK(b5a.flags == FL_RF && b5a.da == da[3], "B5 content sane");
  // RF answers ONE code: a registered Listener Ready Failed or Ready leaves
  // it clear. A talker keyed on the wrong code sets it for Ready Failed (#46)
  set_lsn(3, LSN_READY_FAILED);
  {
    CHECK(send(MT_GTXS, 3, C1, 0x105, 0, 0, 0), "B6 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x105, 0, 0);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;
    e.flags = 0;                              // Ready Failed: RF clear
    expect_resp("B6", e);
  }
  set_lsn(3, LSN_READY);
  {
    CHECK(send(MT_GTXS, 3, C1, 0x106, 0, 0, 0), "B7 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x106, 0, 0);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;
    e.flags = 0;                              // Ready: RF clear
    expect_resp("B7", e);
  }
  set_lsn(3, LSN_ASKING_FAILED);              // B3's state again for C and D
  drained("B");
}

// ---- C: error / no-op / unsupported paths ---------------------------
void Hn::check_error_no_op_and_unsupported_paths() {
  {
    CHECK(send(MT_PROBE, 8, C1, 0x110, L1, 2, 0x0003), "C1 consumed");
    Resp e = echo(MT_PROBE, ST_TK_UNKNOWN, 8, C1, 0x110, L1, 2);
    e.flags = FL_FC;                          // 0x0001 is not echoed
    expect_resp("C1 unknown-id", e);
  }
  {
    CHECK(send(MT_GTXS, 15, C1, 0x111, L1, 2, 0xFFFF), "C2 consumed");
    Resp e = echo(MT_GTXS, ST_TK_UNKNOWN, 15, C1, 0x111, 0, 0);
    expect_resp("C2 unknown-id", e);
  }
  { // ingress interface mismatch: silently ignored, still retired + freed
    int f0 = frees;
    CHECK(send(MT_PROBE, 2, C1, 0x112, L1, 2, FL_FC, 1), "C3 consumed");
    run(4);
    CHECK(resps.empty(), "C3 no response on wrong interface");
    CHECK(arms.empty(), "C3 no freshness ping on wrong interface");
    CHECK(frees == f0 + 1, "C3 slot freed");
  }
  {
    CHECK(send(MT_DISC, 3, C1, 0x113, L1, 7, 0xFFFF), "C4 consumed");
    Resp e = echo(MT_DISC, ST_OK, 3, C1, 0x113, L1, 7);  // flags forced 0
    expect_resp("C4 disconnect no-op", e);
    CHECK(gates.empty(), "C4 changes nothing");
  }
  {
    CHECK(send(MT_GTXC, 3, C1, 0x114, L1, 7, 0), "C5 consumed");
    Resp e = echo(MT_GTXC, ST_NSUPP, 3, C1, 0x114, L1, 7);
    expect_resp("C5 get_tx_connection", e);
  }
  { // V3: flags beyond the committed PDU length read as 0
    uint32_t t3 = 3000; d->now_ms_i = t3;
    CHECK(send(MT_PROBE, 0, C1, 0x115, L1, 4, FL_FC | FL_SW, 0, 44),
          "C6 consumed");
    run(8);
    expect_arm("C6 ping", 0, t3 + T_DAFRESH, false);
    expect_open("C6 declare", 0, da[0]);
    Resp e = echo(MT_PROBE, ST_OK, 0, C1, 0x115, L1, 4);
    e.sid = sid_of(0); e.da = da[0]; e.vlan = VID;
    e.flags = 0;                              // flags @50 beyond 44-B PDU
    expect_resp("C6 truncated", e);
  }
  { // non-talker transaction: consumed, freed, ignored
    int f0 = frees;
    CHECK(send(MT_PROBE, 3, C1, 0x116, L1, 7, 0, 0, 56, 0xDEADull),
          "C7 consumed");
    run(4);
    CHECK(resps.empty() && gates.empty() && arms.empty(),
          "C7 foreign talker_entity_id ignored");
    CHECK(frees == f0 + 1, "C7 slot freed");
  }
  drained("C");
}

// ---- D: T-SRP-DAFRESH freshness expiry ------------------------------
void Hn::check_dafresh_expiry() {
  set_lsn(3, LSN_NONE);                     // gate now rests on freshness
  CHECK(gates.empty(), "D1 still fresh: no withdraw on listener loss");
  d->now_ms_i = t2 + T_DAFRESH + 1;           // window of B4 has lapsed
  clear_edges();
  fire_expiry(3);
  run(8);
  expect_close("D2 freshness lapse", 3);
  CHECK(saw_edge(3, false), "D2 declaring_o[3] OBSERVED 1 -> 0");
  CHECK(decl_mask() == 0x01u,               // src0 (C6) is untouched
        "D2 only src3's gate closed, got 0x%02x", decl_mask());
  {
    CHECK(send(MT_GTXS, 3, C1, 0x121, 0, 0, 0), "D3 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x121, 0, 0);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID;  // DA kept while undeclared
    expect_resp("D3", e);
  }
  uint32_t t4 = 40000; d->now_ms_i = t4;
  CHECK(send(MT_PROBE, 3, C1, 0x122, L1, 7, FL_FC), "D4 consumed");
  run(8);
  expect_arm("D4 ping", 3, t4 + T_DAFRESH, false);
  expect_open("D4 re-declare", 3, da[3]);
  { Resp e = echo(MT_PROBE, ST_OK, 3, C1, 0x122, L1, 7);
    e.sid = sid_of(3); e.da = da[3]; e.vlan = VID; e.flags = FL_FC;
    expect_resp("D4", e); }
  drained("D");
}

// ---- E: MAAP conflict -> withdraw -> LEAVEALL2 -> new DA ------------
void Hn::check_a_maap_conflict_withdraws_and_reallocates() {
  uint32_t t5 = 50000; d->now_ms_i = t5;
  draw_val = 10000;                         // T-MRP-LEAVEALL draw
  d->maap_conflict_valid_i = 1; d->maap_conflict_src_i = 3;
  tick();
  run(20);
  expect_close("E1 conflict withdraw", 3);
  CHECK(draws.size() == 1 && draws[0] == 3, "E1 draw kind 3");
  draws.clear();
  expect_arm("E1 leaveall2", 3, t5 + 2 * 10000, false);  // 2x the draw
  {
    CHECK(send(MT_PROBE, 3, C1, 0x130, L1, 7, FL_FC), "E2 consumed");
    Resp e = echo(MT_PROBE, ST_DMAC_FAIL, 3, C1, 0x130, L1, 7);
    e.flags = FL_FC;                          // conflicted DA is invalid
    expect_resp("E2 backoff probe", e);
    CHECK(arms.empty(), "E2 no DAFRESH arm while BACKOFF holds the slot");
  }
  set_lsn(3, LSN_READY);                    // a listener is registered
  d->now_ms_i = t5 + 2 * 10000 + 1;
  fire_expiry(3);
  run(40);
  expect_mreq("E3 re-alloc", 3, false);
  da3b = da_pool(8);                 // ninth grant overall
  expect_open("E3 re-declare new DA", 3, da3b);
  {
    CHECK(send(MT_GTXS, 3, C1, 0x131, 0, 0, 0), "E4 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 3, C1, 0x131, 0, 0);
    e.sid = sid_of(3); e.da = da3b; e.vlan = VID;
    expect_resp("E4 new DA answered", e);
  }
  drained("E");
}

// ---- E7: conflict while DA_OK (nothing declared): re-alloc, no backoff
void Hn::check_a_conflict_while_da_ok_reallocates_without_backoff() {
  d->maap_conflict_valid_i = 1; d->maap_conflict_src_i = 7;
  tick();
  run(30);
  CHECK(draws.empty(), "E7 no backoff draw when nothing was declared");
  CHECK(gates.empty(), "E7 no withdraw when nothing was declared");
  expect_mreq("E7 re-alloc", 7, false);
  uint64_t da7b = da_pool(9);
  {
    CHECK(send(MT_GTXS, 7, C1, 0x132, 0, 0, 0), "E7b consumed");
    Resp e = echo(MT_GTXS, ST_OK, 7, C1, 0x132, 0, 0);
    e.sid = sid_of(7); e.da = da7b; e.vlan = VID;
    expect_resp("E7b", e);
  }
  drained("E7");
}

// ---- F: SR-class PCP change -> backoff that KEEPS the DA ------------
void Hn::check_a_pcp_change_backs_off_and_keeps_the_da() {
  set_lsn(1, LSN_READY);
  expect_open("F1 listener-driven declare", 1, da[1]);
  uint32_t t6 = 90000; d->now_ms_i = t6;
  draw_val = 12000;
  d->srp_pcp_change_i = 1;
  tick();
  run(90);                                  // src0 (C6), src1, src3 declaring
  expect_close("F2 pcp withdraw src0", 0);
  expect_arm("F2 leaveall2 src0", 0, t6 + 2 * 12000, false);
  expect_close("F2 pcp withdraw src1", 1);
  expect_arm("F2 leaveall2 src1", 1, t6 + 2 * 12000, false);
  expect_close("F2 pcp withdraw src3", 3);
  expect_arm("F2 leaveall2 src3", 3, t6 + 2 * 12000, false);
  CHECK(draws.size() == 3, "F2 three draws");
  draws.clear();
  {
    CHECK(send(MT_PROBE, 1, C1, 0x140, L1, 9, FL_SW), "F3 consumed");
    Resp e = echo(MT_PROBE, ST_OK, 1, C1, 0x140, L1, 9);
    e.sid = sid_of(1); e.da = da[1]; e.vlan = VID; e.flags = FL_SW;
    expect_resp("F3 pcp backoff keeps the DA", e);
    CHECK(arms.empty(), "F3 no DAFRESH arm while BACKOFF holds the slot");
  }
  // compressed exit: expiry fired while the F3 ping is still fresh — the
  // gate re-declares AND re-arms DAFRESH to the ABSOLUTE remaining window
  uint32_t tping = t6;                        // F3 was sent at t6
  fire_expiry(1);
  run(10);
  expect_open("F4 re-declare same DA", 1, da[1]);
  expect_arm("F4 remaining freshness", 1, tping + T_DAFRESH, false);
  d->now_ms_i = t6 + 2 * 12000 + 1;
  fire_expiry(3);
  run(10);
  expect_open("F5 re-declare src3 same DA", 3, da3b);
  // src0: backoff over, but stale ping + no listener = gate stays closed
  fire_expiry(0);
  run(10);
  CHECK(gates.empty() && arms.empty(),
        "F6 src0 exits backoff without declaring");
  drained("F");
}

// ---- G: per-source independence + stateless across interleave -------
void Hn::check_per_source_independence_across_interleave() {
  {
    CHECK(send(MT_GTXS, 2, C1, 0x150, 0, 0, 0), "G1 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 2, C1, 0x150, 0, 0);
    e.sid = sid_of(2); e.da = da[2]; e.vlan = VID;
    expect_resp("G1 src2 untouched by src1/src3 churn", e);
  }
  uint32_t t7 = 200000; d->now_ms_i = t7;
  CHECK(send(MT_PROBE, 4, C1, 0x151, L1, 5, FL_FC), "G2a consumed");
  run(8);
  Resp g2a = pop_resp("G2a");
  expect_open("G2a declare", 4, da[4]);
  expect_arm("G2a ping", 4, t7 + T_DAFRESH, false);
  // interleaved traffic on other sources
  CHECK(send(MT_GTXS, 5, C1, 0x152, 0, 0, 0), "G3 consumed");
  pop_resp("G3");
  set_lsn(5, LSN_READY);
  expect_open("G3 declare src5", 5, da[5]);
  CHECK(send(MT_DISC, 4, C1, 0x153, L1, 5, 0), "G4 consumed");
  pop_resp("G4");
  // identical PROBE again: byte-identical answer, no hidden state grew
  CHECK(send(MT_PROBE, 4, C1, 0x151, L1, 5, FL_FC), "G2b consumed");
  run(8);
  Resp g2b = pop_resp("G2b");
  CHECK(g2a == g2b, "G2 stateless: identical probe = identical bytes");
  CHECK(g2a.status == ST_OK && g2a.da == da[4], "G2 content sane");
  expect_arm("G2b re-ping", 4, t7 + T_DAFRESH, false);
  drained("G");
}

// ---- H: source removed from the configuration -----------------------
void Hn::check_a_source_removed_from_the_configuration() {
  d->cfg_src_en_i = 0xBF;                     // src6 leaves
  run(30);
  expect_arm("H1 cancel shared slot", 6, 0, true);
  expect_mreq("H1 release DA", 6, true);
  CHECK(gates.empty(), "H1 src6 was not declaring: no withdraw");
  {
    CHECK(send(MT_PROBE, 6, C1, 0x160, L1, 3, FL_FC), "H2 consumed");
    Resp e = echo(MT_PROBE, ST_TK_UNKNOWN, 6, C1, 0x160, L1, 3);
    e.flags = FL_FC;
    expect_resp("H2 disabled source", e);
  }
  drained("H");
}

// ---- I: the gate IS the maap grant — a refusal keeps it shut ---------
// F05.12 makes GS_DECLARING reachable only through GS_DA_OK, and GS_DA_OK
// only through an ALLOC_DA success. Both halves are proven on the PORT:
// the level must be seen MOVING, not read once at its reset value.
void Hn::check_a_refused_maap_grant_keeps_the_gate_shut() {
  CHECK(decl_mask() == 0x3Au, "I0 gates carried in from A-H, got 0x%02x",
        decl_mask());                       // src 1,3,4,5 declaring
  grant_ok = false;                         // the allocator REFUSES
  clear_edges();
  d->cfg_src_en_i = 0xFF;                     // src6 returns to the config
  run(60);
  expect_mreq("I1 alloc on re-enable", 6, false);
  CHECK(((decl_mask() >> 6) & 1) == 0, "I1 refused alloc: gate stays shut");
  CHECK(!saw_edge(6, true), "I1 no declare edge on a refusal");
  CHECK(gates.empty(), "I1 no DECLARE_TALKER on a refusal");
  {
    CHECK(send(MT_GTXS, 6, C1, 0x170, 0, 0, 0), "I2 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 6, C1, 0x170, 0, 0);
    e.sid = sid_of(6); e.da = 0; e.vlan = VID;   // no DA to answer with
    expect_resp("I2 refused source answers with no DA", e);
  }
  // a Listener registers: the gate's OTHER term is now true, so only the
  // missing DA can still hold it shut — and the allocator refuses again
  set_lsn(6, LSN_READY);
  run(40);
  expect_mreq("I3 listener retries the alloc", 6, false);
  CHECK(((decl_mask() >> 6) & 1) == 0,
        "I3 listener registered + alloc REFUSED: the gate is still shut");
  CHECK(!saw_edge(6, true), "I3 no declare edge on the second refusal");
  CHECK(gates.empty(), "I3 no DECLARE_TALKER without a DA");
  // the allocator answers: NOW the gate opens, on the grant alone
  grant_ok = true;
  uint32_t t7b = 210000; d->now_ms_i = t7b;
  {
    CHECK(send(MT_PROBE, 6, C1, 0x171, L1, 3, FL_SW), "I4 consumed");
    run(40);
    Resp e = echo(MT_PROBE, ST_DMAC_FAIL, 6, C1, 0x171, L1, 3);
    e.flags = FL_SW;                          // answered before the grant
    expect_resp("I4 no DA yet at answer time", e);
    expect_arm("I4 ping", 6, t7b + T_DAFRESH, false);
    expect_mreq("I4 retry alloc", 6, false);
    const uint64_t da6 = da_pool(10);         // eleventh GRANT overall
    expect_open("I4 grant declares", 6, da6);
    CHECK(saw_edge(6, true),
          "I4 declaring_o[6] OBSERVED 0 -> 1 on the grant");
    CHECK(decl_mask() == 0x7Au, "I4 only src6 moved, got 0x%02x",
          decl_mask());
  }
  drained("I");
}

// ---- J: an ABSENT maap must DEGRADE, never wedge the walker ----------
// The request face is a held valid/ready handshake and ONE walker serves
// every source and every command, so a shim that never asserts ready would
// silence the whole talker half of ACMP (and of SRP through the gate
// strobes). The regression: with maap gone, commands are still answered.
void Hn::check_an_absent_maap_degrades_without_wedging() {
  d->maap_req_ready_i = 0;                    // the allocator is GONE
  clear_edges();
  const int relo0 = offers_rel;
  d->cfg_src_en_i = 0xEF;                     // src4 (declaring) leaves
  run(8);
  expect_close("J1 withdraw on removal", 4);
  expect_arm("J1 cancel shared slot", 4, 0, true);
  CHECK(saw_edge(4, false), "J1 declaring_o[4] OBSERVED 1 -> 0");
  CHECK(d->maap_req_valid_o == 1 && d->maap_req_release_o == 1
        && int(d->maap_req_src_o) == 4,
        "J2 RELEASE_DA offered and unaccepted");
  CHECK(send(MT_GTXS, 2, C1, 0x180, 0, 0, 0),
        "J3 THE REGRESSION: a command is still consumed with maap hung");
  CHECK(last_send_cyc <= MAAP_TMO + 64,
        "J3 served inside the accept window (%d cycles)", last_send_cyc);
  {
    Resp e = echo(MT_GTXS, ST_OK, 2, C1, 0x180, 0, 0);
    e.sid = sid_of(2); e.da = da[2]; e.vlan = VID;
    expect_resp("J3 answer unaffected by the hung request", e);
  }
  CHECK(hold_last == MAAP_TMO,
        "J4 request abandoned after exactly %d cycles, got %d",
        MAAP_TMO, hold_last);
  d->cfg_src_en_i = 0xFF;                     // src4 returns, maap still gone
  run(MAAP_TMO + 80);
  uint32_t t8 = 300000; d->now_ms_i = t8;
  {
    CHECK(send(MT_PROBE, 4, C1, 0x181, L1, 5, FL_FC), "J5 consumed");
    run(8);
    Resp e = echo(MT_PROBE, ST_DMAC_FAIL, 4, C1, 0x181, L1, 5);
    e.flags = FL_FC;
    expect_resp("J5 abandoned alloc = the refused-alloc state", e);
    expect_arm("J5 ping still arms freshness", 4, t8 + T_DAFRESH, false);
    CHECK(((decl_mask() >> 4) & 1) == 0, "J5 no gate without a DA");
  }
  run(MAAP_TMO + 80);                       // the probe's retry times out too
  // An ALLOC_DA abandoned at the accept window is retried by its next
  // stimulus; a RELEASE_DA has none, so it is retried by the engine. The
  // owed release for src 4 must therefore still be on the face here: this
  // is the accept-window half of the lost-release defect.
  CHECK(offers_rel - relo0 >= 2,
        "J6 the owed RELEASE is re-offered after the abandon, got %d offers",
        offers_rel - relo0);
  CHECK(d->maap_req_valid_o == 1 && d->maap_req_release_o == 1
        && int(d->maap_req_src_o) == 4,
        "J6 and it is still src 4's release that is owed");
  CHECK(mreqs.empty(), "J6 nothing was ever accepted while maap was gone");
  d->maap_req_ready_i = 1;                    // the allocator comes back
  clear_edges();
  run(60);
  // The DEBT settles before the re-allocation. src 4 rejoined the
  // configuration while its old address was still owed, and the face is
  // single-outstanding: the other order would hand back the address the
  // rejoin had just been granted.
  const uint64_t da4b = da_pool(11);
  expect_mreq("J7 the owed RELEASE is taken FIRST", 4, true);
  expect_mreq("J7 ...and only then does the rejoin allocate", 4, false);
  expect_open("J7 grant re-declares", 4, da4b);
  CHECK(saw_edge(4, true),
        "J7 declaring_o[4] OBSERVED 0 -> 1: the source recovered");
  CHECK(decl_mask() == 0x7Au, "J7 final gates, got 0x%02x", decl_mask());
  uint32_t t9 = 320000; d->now_ms_i = t9;
  {
    CHECK(send(MT_PROBE, 4, C1, 0x182, L1, 5, FL_FC), "J7b consumed");
    run(8);
    Resp e = echo(MT_PROBE, ST_OK, 4, C1, 0x182, L1, 5);
    e.sid = sid_of(4); e.da = da4b; e.vlan = VID; e.flags = FL_FC;
    expect_resp("J7b the recovered source answers with its NEW DA", e);
    expect_arm("J7b ping", 4, t9 + T_DAFRESH, false);
  }
  // and the settled debt is settled ONCE: no second release for src 4
  {
    const int rel_end = offers_rel;
    run(400);
    CHECK(offers_rel == rel_end,
          "J8 a TAKEN release is never re-offered, got %d more",
          offers_rel - rel_end);
  }
  drained("J");
}

// ---- K: an ACCEPTED maap request that is never ANSWERED --------------
// P-MAAP-ACCEPT-CYC (section J) covers a request never TAKEN. This covers
// the other half, which is quieter and worse: maap_busy_r is a SINGLE
// GLOBAL tracker and maap_avail_w gates every source's ALLOC_DA, so one
// unanswered accept stops allocation for EVERY source — no source reaches
// GS_DA_OK, no DA gate opens, and there is no DECLARE_TALKER for SRP
// either. It does not wedge: dispatch outranks the pending-init flag, so
// every liveness signal stays healthy while no stream can ever start.
void Hn::check_an_unanswered_accept_strands_then_resumes() {
  uint32_t tk0 = 400000; d->now_ms_i = tk0;
  clear_edges();

  // src 2 and src 6 leave the configuration in the SAME cycle. That is the
  // race: the first EVC_OFF takes the single-outstanding face, so the second
  // one meets it BUSY. Both releases must still reach the allocator: the
  // second is owed and settled when the face frees, not dropped.
  d->cfg_src_en_i = 0xBB;                     // src 2 and src 6 out together
  run(200);
  expect_arm("K0 cancel src2 slot", 2, 0, true);
  expect_mreq("K0 src2 release", 2, true);
  expect_close("K0 withdraw on removal", 6);
  expect_arm("K0 cancel src6 slot", 6, 0, true);
  expect_mreq("K0 src6 release settled behind the busy face", 6, true);
  CHECK(decl_mask() == 0x3Au, "K0 gates after removal, got 0x%02x",
        decl_mask());
  drained("K0");

  // the allocator now ACCEPTS and goes quiet
  auto_grant = false;
  const int offK = offers;

  d->cfg_src_en_i = 0xFB;                     // src 6 returns: ALLOC_DA
  run(60);
  expect_mreq("K1 src6 alloc ACCEPTED", 6, false);
  CHECK(offers == offK + 1, "K1 exactly one request offered, got %d",
        offers - offK);

  set_lsn(2, LSN_READY);   // src 2's OTHER gate term, armed at GS_NO_DA
  d->cfg_src_en_i = 0xFF;                     // src 2 returns too
  run(400);
  CHECK(mreqs.empty(),
        "K2 THE DEFECT: src2's allocation is stranded by src6's unanswered "
        "request (%zu accepted)", mreqs.size());
  CHECK(offers == offK + 1,
        "K2 src2's request is never even OFFERED, got %d offers",
        offers - offK);
  CHECK(decl_mask() == 0x3Au, "K2 no gate can open, got 0x%02x",
        decl_mask());

  // the processor stays perfectly responsive while stranded — which is
  // exactly why this defect is invisible from outside
  {
    CHECK(send(MT_PROBE, 6, C1, 0x190, L1, 9, FL_FC), "K3 consumed");
    run(8);
    Resp e = echo(MT_PROBE, ST_DMAC_FAIL, 6, C1, 0x190, L1, 9);
    e.flags = FL_FC;
    expect_resp("K3 the waiting source degrades honestly", e);
    expect_arm("K3 ping still arms freshness", 6, tk0 + T_DAFRESH, false);
    CHECK(((decl_mask() >> 6) & 1) == 0, "K3 no gate without a DA");
  }

  // one millisecond short of the bound: still stranded
  d->now_ms_i = tk0 + MAAP_RSP_MS - 1;
  run(200);
  CHECK(mreqs.empty() && offers == offK + 1,
        "K4 the bound has NOT elapsed: nothing may be re-offered yet");

  // at the bound the request is abandoned and allocation RESUMES —
  // src 2 dispatches first (lowest pending index)
  d->now_ms_i = tk0 + MAAP_RSP_MS;
  run(200);
  expect_mreq("K5 THE REGRESSION: another source allocates again", 2,
                false);
  CHECK(((decl_mask() >> 2) & 1) == 0,
        "K5 accepted is not granted: src2's gate is still shut");
}

// src 6's abandoned response arrives LATE, with a poison address. It must
// be swallowed: src 2 is the tracked request now, and installing this
// would hand two sources the same stream destination MAC.
void Hn::check_a_late_stale_response_is_swallowed() {
  const uint64_t POISON = 0x0DEADBEEFCAFEull;
  inject_rsp(true, POISON);
  run(30);
  CHECK(gates.empty(),
        "K6 a STALE response must not open any gate (%zu strobes)",
        gates.size());
  CHECK(decl_mask() == 0x3Au,
        "K6 stale response changed the gate level to 0x%02x", decl_mask());
  {
    CHECK(send(MT_GTXS, 2, C1, 0x191, 0, 0, 0), "K6 consumed");
    Resp e = echo(MT_GTXS, ST_OK, 2, C1, 0x191, 0, 0);
    e.sid = sid_of(2); e.da = 0; e.vlan = VID;   // NOT the poison address
    e.flags = 0;                                 // Listener READY, not FAILED
    expect_resp("K6 src2 answers with NO DA, not the stale one", e);
  }

  // src 2's OWN response now completes normally: the swallow consumed
  // exactly one credit and the face is live again
  const uint64_t DA2 = 0x91E0F00001AAull;
  inject_rsp(true, DA2);
  run(30);
  expect_open("K7 src2 declares with ITS OWN DA", 2, DA2);
  CHECK(saw_edge(2, true), "K7 declaring_o[2] OBSERVED 0 -> 1");
  CHECK(decl_mask() == 0x3Eu, "K7 gates, got 0x%02x", decl_mask());

  // and the source that was abandoned recovers on its next stimulus, with a
  // DA of its own — never the poison one
  const uint64_t DA6 = 0x91E0F00001BBull;
  run(60);
  expect_mreq("K8 the abandoned source retries", 6, false);
  inject_rsp(true, DA6);
  run(30);
  expect_open("K8 abandoned source recovers with a FRESH DA", 6, DA6);
  CHECK(decl_mask() == 0x7Eu, "K8 final gates, got 0x%02x", decl_mask());
  drained("K");
}

// ---- L: a teardown while the maap face is BUSY -------------------------
// The face is single-outstanding and an ALLOC_DA maps onto a real MAAP
// claim walk, so BUSY is the normal state for seconds at a time (IEEE Std
// 1722-2016 Table B.7 with Table B.8: three probe intervals of up to
// 600 ms each per attempt, B.3.4.2). A source torn down in that window
// must still hand its address back. EVC_OFF wipes the record that names
// the address in the same cycle it asks for the release, and no later
// stimulus ever asks again, so a release skipped here is an address
// allocated forever with nothing left to notice it. Annex B permits the
// DELAY (B.3.5.2 attaches no deadline to Release!, and the machine sits
// legally in DEFEND until it arrives) but not the LOSS: footnote c to
// Table B.7 makes the range free only once Release! has reached INITIAL.
void Hn::check_a_teardown_while_the_maap_face_is_busy() {
  uint32_t tl0 = 500000; d->now_ms_i = tl0;
  clear_edges();

  // park the face on a claim walk that will not answer: src 7 leaves (its
  // release is taken and answered) and rejoins, and the rejoin's ALLOC_DA
  // sits on the face exactly as a real probe walk does
  d->cfg_src_en_i = 0x7F;                     // src 7 out
  run(30);
  expect_arm("L0 cancel src7 slot", 7, 0, true);
  expect_mreq("L0 src7 release", 7, true);
  inject_rsp(false, 0);                     // release answered: face free
  run(20);
  d->cfg_src_en_i = 0xFF;                     // src 7 back
  run(40);
  expect_mreq("L0 src7 ALLOC now PARKS the face", 7, false);
  drained("L0");

  // L1: the teardown itself never waits on the allocator
  const int rel_l = offers_rel;
  d->cfg_src_en_i = 0xFD;                     // src 1, declaring, leaves
  run(40);
  expect_close("L1 WITHDRAW_TALKER is not delayed by the busy face", 1);
  expect_arm("L1 cancel src1 slot", 1, 0, true);
  CHECK(((decl_mask() >> 1) & 1) == 0, "L1 the gate is shut in that cycle");
  CHECK(mreqs.empty(),
        "L1 and nothing can be accepted while the claim walk holds the face");
  {
    CHECK(send(MT_PROBE, 1, C1, 0x1A0, L1, 4, FL_FC), "L1 consumed");
    Resp e = echo(MT_PROBE, ST_TK_UNKNOWN, 1, C1, 0x1A0, L1, 4);
    e.flags = FL_FC;
    expect_resp("L1 the removed source answers at once", e);
  }
  CHECK(offers_rel == rel_l,
        "L1 nothing may be OFFERED while the face is busy either, got %d",
        offers_rel - rel_l);

  // L2: THE DEFECT, the release survives the busy window
  inject_rsp(false, 0);                     // the parked walk finally fails
  run(80);
  expect_mreq("L2 THE DEFECT: src1's RELEASE_DA survived a busy face", 1,
                true);
  CHECK(offers_rel == rel_l + 1,
        "L2 offered exactly once, got %d", offers_rel - rel_l);
  inject_rsp(false, 0);                     // the release is answered
  run(80);

  // L3: settled exactly once, a taken release is never re-offered
  CHECK(offers_rel == rel_l + 1,
        "L3 a TAKEN release is never re-offered, got %d",
        offers_rel - rel_l);
  CHECK(mreqs.empty(), "L3 no second request for src 1");

  // L4: several teardowns behind one busy face, every address comes back
  d->cfg_src_en_i = 0xFC;                     // src 0 leaves (src 1 stays out)
  run(40);
  expect_arm("L4 cancel src0 slot", 0, 0, true);
  expect_mreq("L4 src0 release takes the free face", 0, true);
  //   ...and now, with that release still unanswered, two more sources go
  d->cfg_src_en_i = 0xD4;                     // src 3 and src 5 leave together
  run(60);
  expect_close("L4 src3 withdraws at once", 3);
  expect_arm("L4 cancel src3 slot", 3, 0, true);
  expect_close("L4 src5 withdraws at once", 5);
  expect_arm("L4 cancel src5 slot", 5, 0, true);
  CHECK(mreqs.empty(), "L4 both are owed, neither is accepted yet");
  inject_rsp(false, 0);                     // src0's release is answered
  run(80);
  expect_mreq("L4 src3's owed release, lowest index first", 3, true);
  inject_rsp(false, 0);
  run(80);
  expect_mreq("L4 src5's owed release follows", 5, true);
  inject_rsp(false, 0);
  run(200);
  CHECK(mreqs.empty(),
        "L4 three teardowns, three releases, no fourth (%zu extra)",
        mreqs.size());
  CHECK(decl_mask() == 0x54u, "L4 final gates, got 0x%02x", decl_mask());
  drained("L");
}

int Hn::report() {
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int Hn::run_suite() {
  configure_the_talker_and_release_reset();
  check_the_boot_walk_allocates_every_source_da();
  check_probe_tx_success_and_the_two_trap_tables();
  check_error_no_op_and_unsupported_paths();
  check_dafresh_expiry();
  check_a_maap_conflict_withdraws_and_reallocates();
  check_a_conflict_while_da_ok_reallocates_without_backoff();
  check_a_pcp_change_backs_off_and_keeps_the_da();
  check_per_source_independence_across_interleave();
  check_a_source_removed_from_the_configuration();
  check_a_refused_maap_grant_keeps_the_gate_shut();
  check_an_absent_maap_degrades_without_wedging();
  check_an_unanswered_accept_strands_then_resumes();
  check_a_late_stale_response_is_swallowed();
  check_a_teardown_while_the_maap_face_is_busy();
  return report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Hn h;
  return h.run_suite();
}

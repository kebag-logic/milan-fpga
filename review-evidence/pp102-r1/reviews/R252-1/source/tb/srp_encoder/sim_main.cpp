// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_srp_encoder / KL_srp_domain / KL_srp_vlan suite — independent
// expectations, never DUT logic.
//
// The reference packer builds MRPDU byte images straight from 802.1Q
// §10.8.1/§35.2.2 (run grouping over +1 successors, ThreePacked radix-6,
// FourPacked radix-4, AttributeListLength INCLUDING the AttributeList
// EndMark, dual EndMark) and the frames captured for comparison crossed the
// REAL KL_pp_tx_slots RAM via its serialize port. Domain (F10.2) and VLAN
// (F10.3, corrected per-VID refcount) walks are checked event-by-event; a
// bridge phase plays the not-yet-landed event router and feeds both FSMs'
// declarations into the encoder for end-to-end frames.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include <utility>
#include "Vsrp_tb_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

// The tally lives in the suite object below; CHECK names those members, so it
// expands only inside a SrpSuite member function.
#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- independent 802.1Q reference packer ----------------------------------
// The widest FirstValue either application carries: Talker Failed is 34 bytes,
// so every FirstValue image in this file is a zero-padded buffer of that size.
constexpr int kFirstValueBytes = 34;

struct Ev {
  int app;            // 0 MSRP, 1 MVRP
  int type;           // AttributeType
  int event;          // 0 New, 1 JoinIn, 2 In, 3 JoinMt, 4 Mt, 5 Lv
  int fp;             // Listener FourPacked declaration parameter
  uint8_t val[kFirstValueBytes];  // FirstValue, wire order, zero-padded
};

static Ev mk_ev(int app, int type, int event, int fp,
                std::initializer_list<uint8_t> bytes) {
  Ev e{}; e.app = app; e.type = type; e.event = event; e.fp = fp;
  memset(e.val, 0, sizeof e.val);
  int i = 0; for (uint8_t b : bytes) e.val[i++] = b;
  return e;
}

// bytes [off, off+len) of a, incremented as one big-endian integer, == b?
static bool inc_eq(const uint8_t* a, const uint8_t* b, int off, int len) {
  uint8_t tmp[kFirstValueBytes];
  memcpy(tmp, a, kFirstValueBytes);
  for (int i = off + len - 1; i >= off; --i) { if (++tmp[i] != 0) break; }
  return memcmp(tmp + off, b + off, len) == 0;
}
static bool eq_rng(const uint8_t* a, const uint8_t* b, int off, int len) {
  return memcmp(a + off, b + off, len) == 0;
}

// +1 successor under the attribute's own increment rule (802.1Q §35.2.2.8/.9)
static bool is_succ(const Ev& p, const Ev& n) {
  if (p.app != n.app || p.type != n.type) return false;
  if (p.app == 1) return inc_eq(p.val, n.val, 0, 2) && eq_rng(p.val, n.val, 2, 32);
  switch (p.type) {
    case 1: case 2:   // Talker: stream_id and DA step together
      return inc_eq(p.val, n.val, 0, 8) && inc_eq(p.val, n.val, 8, 6)
          && eq_rng(p.val, n.val, 14, 20);
    case 3:           // Listener: stream_id steps
      return inc_eq(p.val, n.val, 0, 8) && eq_rng(p.val, n.val, 8, 26);
    case 4:           // Domain: SRclassID and priority step, VID pinned
      return inc_eq(p.val, n.val, 0, 1) && inc_eq(p.val, n.val, 1, 1)
          && eq_rng(p.val, n.val, 2, 32);
  }
  return false;
}

static int attr_len(int app, int type) {
  if (app == 1) return 2;
  switch (type) { case 1: return 25; case 2: return 34; case 3: return 8; }
  return 4;
}

// One MRPDU (Ethernet frame image) for one application's pending events.
static std::vector<uint8_t> model_pdu(const std::vector<Ev>& evs, bool leaveall,
                                      const uint8_t own[6]) {
  const int app = evs[0].app;
  static constexpr uint8_t da_msrp[6] = {0x01, 0x80, 0xC2,
                                         0x00, 0x00, 0x0E};
  static constexpr uint8_t da_mvrp[6] = {0x01, 0x80, 0xC2,
                                         0x00, 0x00, 0x21};
  std::vector<uint8_t> f;
  const uint8_t* da = app ? da_mvrp : da_msrp;
  f.insert(f.end(), da, da + 6);
  f.insert(f.end(), own, own + 6);
  const uint16_t et = app ? 0x88F5 : 0x22EA;
  f.push_back(uint8_t(et >> 8)); f.push_back(uint8_t(et & 0xFF));
  f.push_back(0x00);                                    // ProtocolVersion
  struct Run { int type; const Ev* first; std::vector<int> e3, e4; };
  std::vector<Run> runs;
  for (size_t i = 0; i < evs.size(); ++i) {
    if (!runs.empty() && runs.back().type == evs[i].type
        && int(runs.back().e3.size()) < 12 && is_succ(evs[i - 1], evs[i])) {
      runs.back().e3.push_back(evs[i].event);
      runs.back().e4.push_back(evs[i].fp);
    } else {
      runs.push_back({evs[i].type, &evs[i], {evs[i].event}, {evs[i].fp}});
    }
  }
  size_t r = 0;
  bool first_vec = true;
  while (r < runs.size()) {
    const int t = runs[r].type;
    const int alen = attr_len(app, t);
    f.push_back(uint8_t(t)); f.push_back(uint8_t(alen));
    size_t ll_pos = 0;
    if (app == 0) { ll_pos = f.size(); f.push_back(0); f.push_back(0); }
    while (r < runs.size() && runs[r].type == t) {
      const Run& R = runs[r];
      const int nov = int(R.e3.size());
      const int la = (first_vec && leaveall) ? 1 : 0;
      first_vec = false;
      f.push_back(uint8_t((la << 5) | ((nov >> 8) & 0x1F)));
      f.push_back(uint8_t(nov & 0xFF));
      f.insert(f.end(), R.first->val, R.first->val + alen);
      for (int k = 0; k < (nov + 2) / 3; ++k) {
        const int e0 = (3 * k     < nov) ? R.e3[size_t(3 * k)]     : 0;
        const int e1 = (3 * k + 1 < nov) ? R.e3[size_t(3 * k + 1)] : 0;
        const int e2 = (3 * k + 2 < nov) ? R.e3[size_t(3 * k + 2)] : 0;
        f.push_back(uint8_t(e0 * 36 + e1 * 6 + e2));
      }
      if (app == 0 && t == 3) {
        for (int k = 0; k < (nov + 3) / 4; ++k) {
          int v[4] = {0, 0,
                      0, 0};
          for (int m = 0; m < 4; ++m)
            if (4 * k + m < nov) v[m] = R.e4[size_t(4 * k + m)];
          f.push_back(uint8_t(v[0] * 64 + v[1] * 16 + v[2] * 4 + v[3]));
        }
      }
      ++r;
    }
    f.push_back(0); f.push_back(0);                    // AttributeList EndMark
    if (app == 0) {                                    // §35.2.2.6: EndMark counted
      const int ll = int(f.size()) - int(ll_pos) - 2;
      f[ll_pos] = uint8_t(ll >> 8); f[ll_pos + 1] = uint8_t(ll & 0xFF);
    }
  }
  f.push_back(0); f.push_back(0);                      // MRPDU EndMark
  return f;
}

// ---- harness ---------------------------------------------------------------
constexpr uint8_t OWN_MAC[6] = {0x02, 0x4B, 0x4C,
                                0x00, 0x00, 0x01};

// enc_ev_value_i is 272 bits wide: nine 32-bit Verilator words.
constexpr int kValueWords = 9;
// Cycles a ready handshake is given before the harness calls it backpressured.
constexpr int kHandshakeTimeoutCycles = 100;
// Cycles the TX request face is waited on before the drain is called lost.
constexpr int kTxreqTimeoutCycles = 5000;
// Loop guard on one slot's serialize walk: far longer than any legal frame.
constexpr int kSerializeGuardCycles = 8000;

struct H {
  Vsrp_tb_wrap* d;
  std::vector<std::pair<int, uint32_t>> dom_evs;
  std::vector<std::pair<int, int>>      vlan_evs;
  int dom_changes = 0;
  int vlan_errs = 0;
  int commits = 0;
  int allocs = 0;
  int drops = 0;
  // pre-edge samples
  bool last_enc_ready = false;
  bool last_txreq = false;
  int  last_txslot = 0;
  bool last_ser_valid = false;
  bool last_ser_last = false;
  uint8_t last_ser_data = 0;
  bool last_user_ready = false;
  bool last_vlan_ev_valid = false;

  explicit H(Vsrp_tb_wrap* dd) : d(dd) {}

  void tick() {
    d->clk_i = 0; d->eval();
    // observe PRE-EDGE — what the registers are about to consume
    last_enc_ready     = d->enc_ev_ready_o;
    last_txreq         = d->enc_txreq_valid_o;
    last_txslot        = d->enc_txreq_slot_o;
    last_ser_valid     = d->ser_valid_o;
    last_ser_last      = d->ser_last_o;
    last_ser_data      = d->ser_data_o;
    last_user_ready    = d->vlan_user_ready_o;
    last_vlan_ev_valid = d->vlan_ev_valid_o;
    if (d->dom_ev_valid_o && d->dom_ev_ready_i)
      dom_evs.push_back({int(d->dom_ev_event_o), uint32_t(d->dom_ev_value_o)});
    if (d->vlan_ev_valid_o && d->vlan_ev_ready_i)
      vlan_evs.push_back({int(d->vlan_ev_event_o), int(d->vlan_ev_vid_o)});
    if (d->dom_evt_change_o) ++dom_changes;
    if (d->vlan_user_err_o) ++vlan_errs;
    if (d->dbg_commit_o) ++commits;
    if (d->dbg_alloc_gnt_o) ++allocs;
    if (d->enc_ev_drop_o) ++drops;
    d->clk_i = 1; d->eval();
  }
  void run(int n) { for (int i = 0; i < n; ++i) tick(); }

  void set_val(const uint8_t v[kFirstValueBytes]) {
    for (int w = 0; w < kValueWords; ++w) d->enc_ev_value_i[w] = 0;
    for (int j = 0; j < kFirstValueBytes; ++j) {
      const int low = 264 - 8 * j;               // byte j at [271-8j : 264-8j]
      d->enc_ev_value_i[low / 32] |= uint32_t(v[j]) << (low % 32);
    }
  }

  bool push_enc(const Ev& e, int timeout = kHandshakeTimeoutCycles) {
    d->enc_ev_app_i       = uint8_t(e.app);
    d->enc_ev_attr_type_i = uint8_t(e.type);
    d->enc_ev_event_i     = uint8_t(e.event);
    d->enc_ev_fourpack_i  = uint8_t(e.fp);
    set_val(e.val);
    d->enc_ev_valid_i = 1;
    for (int i = 0; i < timeout; ++i) {
      tick();
      if (last_enc_ready) { d->enc_ev_valid_i = 0; return true; }
    }
    d->enc_ev_valid_i = 0;
    return false;
  }

  // wait for the TX request face, accept it, drain the slot via the pool
  bool wait_and_drain(std::vector<uint8_t>& out, int to = kTxreqTimeoutCycles) {
    int slot = -1;
    for (int i = 0; i < to && slot < 0; ++i) {
      tick();
      if (last_txreq) slot = last_txslot;
    }
    if (slot < 0) return false;
    d->enc_txreq_ready_i = 1; tick(); d->enc_txreq_ready_i = 0;
    d->ser_slot_i = uint8_t(slot); d->ser_req_i = 1; d->ser_ready_i = 1;
    out.clear();
    for (int i = 0; i < kSerializeGuardCycles; ++i) {
      tick();
      d->ser_req_i = 0;
      if (last_ser_valid) {
        out.push_back(last_ser_data);
        if (last_ser_last) { d->ser_ready_i = 0; return true; }
      }
    }
    d->ser_ready_i = 0;
    return false;
  }

  bool capture_pdu(int app, std::vector<uint8_t>& out,
                   int to = kTxreqTimeoutCycles) {
    d->enc_join_tick_i = uint8_t(1u << app);
    tick();
    d->enc_join_tick_i = 0;
    return wait_and_drain(out, to);
  }

  bool vlan_op(bool join, int vid, int timeout = kHandshakeTimeoutCycles) {
    d->vlan_user_join_i = join; d->vlan_user_vid_i = uint16_t(vid);
    d->vlan_user_valid_i = 1;
    for (int i = 0; i < timeout; ++i) {
      tick();
      if (last_user_ready) { d->vlan_user_valid_i = 0; run(30); return true; }
    }
    d->vlan_user_valid_i = 0;
    return false;
  }
};

namespace {

//! The whole SRP suite as one object: the tally, the Verilated model, the BFM
//! and the frame under comparison are members, so nothing this translation
//! unit mutates lives at file scope (I.2).
class SrpSuite {
 public:
  int run();

 private:
  void check_pdu(const char* name, const std::vector<uint8_t>& got,
                 const std::vector<uint8_t>& exp) {
    CHECK(got.size() == exp.size(), "%s: length got %zu exp %zu",
          name, got.size(), exp.size());
    const bool same = (got == exp);
    CHECK(same, "%s: byte-exact against the independent packer", name);
    if (!same) {
      printf("  exp:"); for (uint8_t b : exp) printf(" %02x", b); printf("\n");
      printf("  got:"); for (uint8_t b : got) printf(" %02x", b); printf("\n");
    }
  }

  void bring_out_of_reset();
  void encode_the_two_minimal_pdus();
  void aggregate_one_window_into_one_frame();
  void carry_a_wide_firstvalue_and_one_leaveall();
  void keep_the_two_participants_independent();
  void pad_the_packed_lanes_and_drop_unknown_types();
  void fold_a_full_table_then_backpressure_the_overflow();
  void domain_declares_adopts_and_ignores_repeats();
  void domain_surfaces_class_a_and_reverts_on_link_down();
  void vlan_refcounts_every_vid_and_freezes_the_old_one();
  void bridge_the_fsm_declarations_onto_real_frames();

  int checks = 0;
  int fails = 0;

  const milan::tb::Model<Vsrp_tb_wrap> model;
  Vsrp_tb_wrap* const d = model.get();
  H h{d};
  std::vector<uint8_t> got;
};

void SrpSuite::bring_out_of_reset() {
  // defaults
  d->rst_n = 0;
  d->enc_ev_valid_i = 0; d->enc_join_tick_i = 0; d->enc_leaveall_i = 0;
  d->enc_txreq_ready_i = 0;
  d->ser_req_i = 0; d->ser_ready_i = 0; d->ser_slot_i = 0;
  d->dom_link_up_i = 0; d->dom_rx_valid_i = 0;
  d->dom_periodic_tick_i = 0; d->dom_leaveall_tick_i = 0;
  d->dom_ev_ready_i = 1;
  d->vlan_user_valid_i = 0; d->vlan_periodic_tick_i = 0;
  d->vlan_leaveall_tick_i = 0; d->vlan_ev_ready_i = 1;
  uint64_t mac = 0;
  for (int i = 0; i < 6; ++i) mac = (mac << 8) | OWN_MAC[i];
  d->enc_own_mac_i = mac;
  h.run(5);
  d->rst_n = 1;
  h.run(3);
}

void SrpSuite::encode_the_two_minimal_pdus() {
  // =====================================================================
  // E1 — single Domain New: minimal MSRP PDU, both EndMarks, listlen rule
  // =====================================================================
  {
    std::vector<Ev> evs = {mk_ev(0, 4, 0, 0, {0x06, 0x03, 0x00, 0x02})};
    CHECK(h.push_enc(evs[0]), "E1 push accepted");
    const int c0 = h.commits;
    h.run(100);
    CHECK(h.commits == c0, "E1 no emission before the join tick");
    CHECK(h.capture_pdu(0, got), "E1 PDU captured");
    check_pdu("E1", got, model_pdu(evs, false, OWN_MAC));
    CHECK(got.size() == 30, "E1 frame is 30 bytes got %zu", got.size());
    CHECK(got[14] == 0x00, "E1 ProtocolVersion 0");
    CHECK(got[17] == 0x00 && got[18] == 0x09,
          "E1 AttributeListLength 9 INCLUDES the EndMark got %02x%02x",
          got[17], got[18]);
    CHECK(got[26] == 0 && got[27] == 0 && got[28] == 0 && got[29] == 0,
          "E1 dual EndMark explicit ahead of MAC padding");
    CHECK(h.commits == c0 + 1, "E1 exactly one commit");
    CHECK(d->enc_dbg_cnt_msrp_o == 0, "E1 pending table drained");
  }

  // =====================================================================
  // E2 — single MVRP VID New: no AttributeListLength field in MVRP
  // =====================================================================
  {
    std::vector<Ev> evs = {mk_ev(1, 1, 0, 0, {0x00, 0x02})};
    CHECK(h.push_enc(evs[0]), "E2 push accepted");
    CHECK(h.capture_pdu(1, got), "E2 PDU captured");
    check_pdu("E2", got, model_pdu(evs, false, OWN_MAC));
    CHECK(got.size() == 26, "E2 frame is 26 bytes got %zu", got.size());
    CHECK(got[12] == 0x88 && got[13] == 0xF5, "E2 MVRP EtherType");
    CHECK(got[15] == 1 && got[16] == 2,
          "E2 message header is {type, len} with NO list-length field");
  }
}

void SrpSuite::aggregate_one_window_into_one_frame() {
  // =====================================================================
  // E3 — cadence aggregation: N pushed events -> ONE frame on the tick
  // =====================================================================
  {
    std::vector<Ev> evs = {
      mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02}),
      mk_ev(0, 3, 0, 2, {0, 0, 0, 0, 0, 0, 0, 0x10}),
      mk_ev(0, 3, 1, 2, {0, 0, 0, 0, 0, 0, 0, 0x40}),   // not a successor
      mk_ev(0, 1, 0, 0, {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x07,
                         0x91, 0xE0, 0xF0, 0x00, 0x11, 0x22,
                         0x00, 0x02, 0x00, 0x64, 0x00, 0x01, 0x70, 0x00,
                         0x00, 0x0F, 0x42}),
    };
    const int c0 = h.commits;
    const int a0 = h.allocs;
    for (auto& e : evs) CHECK(h.push_enc(e), "E3 push accepted");
    h.run(200);
    CHECK(h.commits == c0 && h.allocs == a0,
          "E3 events accumulate silently between ticks");
    CHECK(d->enc_dbg_cnt_msrp_o == 4, "E3 four events pending");
    CHECK(h.capture_pdu(0, got), "E3 PDU captured");
    CHECK(h.commits == c0 + 1 && h.allocs == a0 + 1,
          "E3 one window -> one MRPDU (one alloc, one commit)");
    check_pdu("E3", got, model_pdu(evs, false, OWN_MAC));
    CHECK(d->enc_dbg_cnt_msrp_o == 0, "E3 drained");
  }

  // =====================================================================
  // E4 — Listener sorted run: NoV=3, mixed events, FourPacked lanes
  // =====================================================================
  {
    std::vector<Ev> evs = {
      mk_ev(0, 3, 0, 2, {0, 0, 0, 0, 0, 0, 0x01, 0x10}),
      mk_ev(0, 3, 1, 3, {0, 0, 0, 0, 0, 0, 0x01, 0x11}),
      mk_ev(0, 3, 1, 1, {0, 0, 0, 0, 0, 0, 0x01, 0x12}),
    };
    for (auto& e : evs) CHECK(h.push_enc(e), "E4 push accepted");
    CHECK(h.capture_pdu(0, got), "E4 PDU captured");
    check_pdu("E4", got, model_pdu(evs, false, OWN_MAC));
    CHECK(got[19] == 0x00 && got[20] == 0x03, "E4 NumberOfValues 3");
    CHECK(got[29] == 0 * 36 + 1 * 6 + 1, "E4 ThreePacked radix-6 byte");
    CHECK(got[30] == 2 * 64 + 3 * 16 + 1 * 4 + 0,
          "E4 FourPacked radix-4 byte (pad 0)");
  }

  // =====================================================================
  // E5 — Talker Advertise run of 2, then a same-type NON-successor
  //      (stream_id steps but DA does not): new vector, same message
  // =====================================================================
  {
    Ev t0 = mk_ev(0, 1, 0, 0, {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x07,
                               0x91, 0xE0, 0xF0, 0x00, 0x11, 0x22,
                               0x00, 0x02, 0x00, 0x64, 0x00, 0x01, 0x70, 0x00,
                               0x00, 0x0F, 0x42});
    Ev t1 = t0; t1.val[7] = 0x08; t1.val[13] = 0x23; t1.event = 1; // +1 both
    Ev t2 = t0; t2.val[7] = 0x09; t2.val[13] = 0x23;               // DA frozen
    std::vector<Ev> evs = {t0, t1, t2};
    for (auto& e : evs) CHECK(h.push_enc(e), "E5 push accepted");
    CHECK(h.capture_pdu(0, got), "E5 PDU captured");
    check_pdu("E5", got, model_pdu(evs, false, OWN_MAC));
    CHECK(got[19] == 0x00 && got[20] == 0x02,
          "E5 first vector aggregated NoV=2");
  }
}

void SrpSuite::carry_a_wide_firstvalue_and_one_leaveall() {
  // =====================================================================
  // E6 — Talker Failed: 34-byte FirstValue survives byte-exact
  // =====================================================================
  {
    Ev f0 = mk_ev(0, 2, 0, 0, {});
    for (int i = 0; i < kFirstValueBytes; ++i) f0.val[i] = uint8_t(0xA0 + i);
    std::vector<Ev> evs = {f0};
    CHECK(h.push_enc(f0), "E6 push accepted");
    CHECK(h.capture_pdu(0, got), "E6 PDU captured");
    check_pdu("E6", got, model_pdu(evs, false, OWN_MAC));
  }

  // =====================================================================
  // E7 — LeaveAll injection: flag on the FIRST VectorHeader only, then
  //      consumed — the next PDU carries none
  // =====================================================================
  {
    std::vector<Ev> evs = {
      mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02}),
      mk_ev(0, 3, 1, 2, {0, 0, 0, 0, 0, 0, 0x02, 0x50}),
    };
    d->enc_leaveall_i = 1; h.tick(); d->enc_leaveall_i = 0;
    for (auto& e : evs) CHECK(h.push_enc(e), "E7 push accepted");
    CHECK(h.capture_pdu(0, got), "E7 PDU captured");
    check_pdu("E7", got, model_pdu(evs, true, OWN_MAC));
    CHECK((got[19] >> 5) == 1, "E7 LeaveAllEvent rides vector 1");
    // second message: type@28 len@29 listlen@30-31 -> its VectorHeader @32
    CHECK((got[32] >> 5) == 0, "E7 second vector carries no LeaveAll");
    std::vector<Ev> ev2 = {mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02})};
    CHECK(h.push_enc(ev2[0]), "E7b push accepted");
    CHECK(h.capture_pdu(0, got), "E7b PDU captured");
    check_pdu("E7b", got, model_pdu(ev2, false, OWN_MAC));
    CHECK((got[19] >> 5) == 0, "E7b LeaveAll consumed by the first PDU");
  }
}

void SrpSuite::keep_the_two_participants_independent() {
  // =====================================================================
  // E8 — both participants pending; each tick drains ONLY its own table
  // =====================================================================
  {
    std::vector<Ev> em = {mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02})};
    std::vector<Ev> ev = {mk_ev(1, 1, 1, 0, {0x00, 0x02}),
                          mk_ev(1, 1, 0, 0, {0x00, 0x05})};
    CHECK(h.push_enc(em[0]), "E8 MSRP push");
    CHECK(h.push_enc(ev[0]) && h.push_enc(ev[1]), "E8 MVRP pushes");
    CHECK(h.capture_pdu(0, got), "E8 MSRP PDU captured");
    check_pdu("E8-msrp", got, model_pdu(em, false, OWN_MAC));
    CHECK(d->enc_dbg_cnt_mvrp_o == 2, "E8 MVRP table untouched by MSRP tick");
    CHECK(h.capture_pdu(1, got), "E8 MVRP PDU captured");
    check_pdu("E8-mvrp", got, model_pdu(ev, false, OWN_MAC));
    CHECK(d->enc_dbg_cnt_mvrp_o == 0, "E8 MVRP drained by its own tick");
  }

  // =====================================================================
  // E9 — simultaneous ticks: MSRP first, MVRP queued behind it
  // =====================================================================
  {
    std::vector<Ev> em = {mk_ev(0, 3, 5, 0, {0, 0, 0, 0, 0, 0, 0x03, 0x33})};
    std::vector<Ev> ev = {mk_ev(1, 1, 5, 0, {0x00, 0x07})};
    CHECK(h.push_enc(em[0]) && h.push_enc(ev[0]), "E9 pushes");
    d->enc_join_tick_i = 3; h.tick(); d->enc_join_tick_i = 0;
    CHECK(h.wait_and_drain(got), "E9 first PDU");
    check_pdu("E9-msrp", got, model_pdu(em, false, OWN_MAC));
    CHECK(h.wait_and_drain(got), "E9 second PDU follows automatically");
    check_pdu("E9-mvrp", got, model_pdu(ev, false, OWN_MAC));
  }
}

void SrpSuite::pad_the_packed_lanes_and_drop_unknown_types() {
  // =====================================================================
  // E10 — MVRP VID run + FourPacked absence; 5-element Listener run:
  //       ThreePacked and FourPacked padding both exercised
  // =====================================================================
  {
    std::vector<Ev> ev = {mk_ev(1, 1, 0, 0, {0x00, 0x10}),
                          mk_ev(1, 1, 1, 0, {0x00, 0x11}),
                          mk_ev(1, 1, 1, 0, {0x00, 0x12})};
    for (auto& e : ev) CHECK(h.push_enc(e), "E10 MVRP push");
    CHECK(h.capture_pdu(1, got), "E10 MVRP PDU captured");
    check_pdu("E10-mvrp", got, model_pdu(ev, false, OWN_MAC));
    std::vector<Ev> el;
    for (int i = 0; i < 5; ++i) {
      Ev e = mk_ev(0, 3, (i == 0) ? 0 : 1, (i % 4),
                   {0, 0, 0, 0, 0, 0, 0x09, uint8_t(0x60 + i)});
      el.push_back(e);
      CHECK(h.push_enc(e), "E10 Listener push");
    }
    CHECK(h.capture_pdu(0, got), "E10 Listener PDU captured");
    check_pdu("E10-lstn", got, model_pdu(el, false, OWN_MAC));
    CHECK(got[19] == 0x00 && got[20] == 0x05, "E10 NoV=5 aggregated");
  }

  // =====================================================================
  // E11 — unknown AttributeType is dropped with a strobe, never encoded
  // =====================================================================
  {
    const int dr0 = h.drops;
    Ev bad = mk_ev(0, 9, 0, 0, {0x01});
    CHECK(h.push_enc(bad), "E11 handshake still completes");
    CHECK(h.drops == dr0 + 1, "E11 drop strobe fired");
    CHECK(d->enc_dbg_cnt_msrp_o == 0, "E11 nothing pended");
  }
}

void SrpSuite::fold_a_full_table_then_backpressure_the_overflow() {
  // =====================================================================
  // E12 — full-table run: 12 consecutive Listeners fold to ONE NoV=12
  //       vector; the 13th push backpressures until the drain
  // =====================================================================
  {
    std::vector<Ev> el;
    for (int i = 0; i < 12; ++i) {
      Ev e = mk_ev(0, 3, (i == 0) ? 0 : 1, 2,
                   {0, 0, 0, 0, 0, 0, 0x0A, uint8_t(0x00 + i)});
      el.push_back(e);
      CHECK(h.push_enc(e), "E12 push %d accepted", i);
    }
    Ev extra = mk_ev(0, 3, 1, 2, {0, 0, 0, 0, 0, 0, 0x0A, 0x0C});
    CHECK(!h.push_enc(extra, 40), "E12 13th push backpressured while full");
    CHECK(h.capture_pdu(0, got), "E12 PDU captured");
    check_pdu("E12", got, model_pdu(el, false, OWN_MAC));
    CHECK(got[19] == 0x00 && got[20] == 0x0C, "E12 NoV=12 single vector");
    CHECK(h.push_enc(extra), "E12 push accepted after the drain");
    CHECK(h.capture_pdu(0, got), "E12b PDU captured");
    check_pdu("E12b", got, model_pdu({extra}, false, OWN_MAC));
  }
}

void SrpSuite::domain_declares_adopts_and_ignores_repeats() {
  // =====================================================================
  // D — Domain FSM walk (F10.2)
  // =====================================================================
  {
    // D1: startup with the link already up = declare the defaults
    h.dom_evs.clear();
    d->dom_link_up_i = 1;
    h.run(10);
    CHECK(h.dom_evs.size() == 1, "D1 one declaration got %zu", h.dom_evs.size());
    CHECK(h.dom_evs.size() == 1 && h.dom_evs[0].first == 0
          && h.dom_evs[0].second == 0x06030002u,
          "D1 New {6, 3, 2} got ev %d val %08x",
          h.dom_evs.empty() ? -1 : h.dom_evs[0].first,
          h.dom_evs.empty() ? 0u : h.dom_evs[0].second);
    CHECK(d->dom_class_a_prio_o == 3 && d->dom_class_a_vid_o == 2,
          "D1 class-D defaults {3, 2}");
    CHECK(d->dom_adopted_o == 0, "D1 DEFAULTS state");

    // D2: periodic re-join
    h.dom_evs.clear();
    d->dom_periodic_tick_i = 1; h.tick(); d->dom_periodic_tick_i = 0;
    h.run(10);
    CHECK(h.dom_evs.size() == 1 && h.dom_evs[0].first == 1
          && h.dom_evs[0].second == 0x06030002u, "D2 periodic JoinIn");

    // D3: LeaveAll re-declare
    h.dom_evs.clear();
    d->dom_leaveall_tick_i = 1; h.tick(); d->dom_leaveall_tick_i = 0;
    h.run(10);
    CHECK(h.dom_evs.size() == 1 && h.dom_evs[0].first == 1,
          "D3 LeaveAll re-join");

    // D4: adopt a differing Class A Domain {6, 5, VID 7}
    h.dom_evs.clear();
    const int ch0 = h.dom_changes;
    d->dom_rx_class_id_i = 6; d->dom_rx_prio_i = 5;
    d->dom_rx_vid_i = 7; d->dom_rx_nov_i = 1;
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(10);
    CHECK(h.dom_evs.size() == 2, "D4 withdraw + re-declare got %zu",
          h.dom_evs.size());
    CHECK(h.dom_evs.size() == 2 && h.dom_evs[0].first == 5
          && h.dom_evs[0].second == 0x06030002u,
          "D4 Lv of the old declaration first");
    CHECK(h.dom_evs.size() == 2 && h.dom_evs[1].first == 0
          && h.dom_evs[1].second == 0x06050007u,
          "D4 New of the adopted FirstValue second");
    CHECK(h.dom_changes == ch0 + 1, "D4 one DOMAIN_CHANGE strobe");
    CHECK(d->dom_class_a_prio_o == 5 && d->dom_class_a_vid_o == 7,
          "D4 levels track the adoption");
    CHECK(d->dom_adopted_o == 1, "D4 ADOPTED state");

    // D5: the same Domain again is NOT a change
    h.dom_evs.clear();
    const int ch1 = h.dom_changes;
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(10);
    CHECK(h.dom_evs.empty(), "D5 no re-adoption of identical parameters");
    CHECK(h.dom_changes == ch1, "D5 no DOMAIN_CHANGE strobe");
  }
}

void SrpSuite::domain_surfaces_class_a_and_reverts_on_link_down() {
  {
    // D6: the certified two-class bridge shape — FirstValue {5, 2, VID 2},
    // NoV=2: Class A is value 1, priority 2 + (6 - 5) = 3
    h.dom_evs.clear();
    const int ch2 = h.dom_changes;
    d->dom_rx_class_id_i = 5; d->dom_rx_prio_i = 2;
    d->dom_rx_vid_i = 2; d->dom_rx_nov_i = 2;
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(10);
    CHECK(h.dom_evs.size() == 2 && h.dom_evs[0].first == 5
          && h.dom_evs[0].second == 0x06050007u,
          "D6 two-class shape: old {5, 7} withdrawn");
    CHECK(h.dom_evs.size() == 2 && h.dom_evs[1].first == 0
          && h.dom_evs[1].second == 0x06030002u,
          "D6 surfaced Class A priority 3 VID 2 declared");
    CHECK(h.dom_changes == ch2 + 1, "D6 DOMAIN_CHANGE fired");
    CHECK(d->dom_class_a_prio_o == 3 && d->dom_class_a_vid_o == 2,
          "D6 levels from the range rule, not FirstValue equality");

    // D7: vectors that do NOT cover Class A are ignored
    h.dom_evs.clear();
    const int ch3 = h.dom_changes;
    d->dom_rx_class_id_i = 4; d->dom_rx_prio_i = 1;
    d->dom_rx_vid_i = 9; d->dom_rx_nov_i = 2;      // covers 4, 5 only
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(6);
    d->dom_rx_class_id_i = 7; d->dom_rx_nov_i = 5; // starts past 6
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(6);
    d->dom_rx_class_id_i = 6; d->dom_rx_nov_i = 0; // empty vector
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(6);
    CHECK(h.dom_evs.empty() && h.dom_changes == ch3,
          "D7 non-covering vectors ignored");

    // D8: adopt {6, 4, 8}; periodic and LeaveAll do NOT revert (F10.2)
    h.dom_evs.clear();
    d->dom_rx_class_id_i = 6; d->dom_rx_prio_i = 4;
    d->dom_rx_vid_i = 8; d->dom_rx_nov_i = 1;
    d->dom_rx_valid_i = 1; h.tick(); d->dom_rx_valid_i = 0;
    h.run(10);
    h.dom_evs.clear();
    d->dom_periodic_tick_i = 1; h.tick(); d->dom_periodic_tick_i = 0;
    h.run(10);
    d->dom_leaveall_tick_i = 1; h.tick(); d->dom_leaveall_tick_i = 0;
    h.run(10);
    CHECK(d->dom_class_a_prio_o == 4 && d->dom_class_a_vid_o == 8,
          "D8 cadence never reverts an adoption");
    CHECK(h.dom_evs.size() == 2 && h.dom_evs[0].first == 1
          && h.dom_evs[0].second == 0x06040008u
          && h.dom_evs[1].first == 1 && h.dom_evs[1].second == 0x06040008u,
          "D8 re-joins carry the ADOPTED declaration");
    CHECK(d->dom_adopted_o == 1, "D8 still ADOPTED");

    // D9: LINK_DOWN is the only revert; LINK_UP re-declares the defaults
    h.dom_evs.clear();
    const int ch4 = h.dom_changes;
    d->dom_link_up_i = 0;
    h.run(10);
    CHECK(h.dom_changes == ch4 + 1, "D9 revert fires DOMAIN_CHANGE");
    CHECK(d->dom_class_a_prio_o == 3 && d->dom_class_a_vid_o == 2,
          "D9 levels back to the defaults");
    CHECK(d->dom_adopted_o == 0, "D9 DEFAULTS state");
    d->dom_periodic_tick_i = 1; h.tick(); d->dom_periodic_tick_i = 0;
    h.run(10);
    CHECK(h.dom_evs.empty(), "D9 nothing declared while the link is down");
    d->dom_link_up_i = 1;
    h.run(10);
    CHECK(h.dom_evs.size() == 1 && h.dom_evs[0].first == 0
          && h.dom_evs[0].second == 0x06030002u,
          "D9 LINK_UP re-declares the defaults (New)");
  }
}

void SrpSuite::vlan_refcounts_every_vid_and_freezes_the_old_one() {
  // =====================================================================
  // V — VLAN FSM walk (corrected F10.3: per-VID refcount, frozen VID)
  // =====================================================================
  {
    // V1: first user of VID 2 declares it
    h.vlan_evs.clear();
    CHECK(h.vlan_op(true, 2), "V1 join accepted");
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].first == 0
          && h.vlan_evs[0].second == 2, "V1 first user -> New VID 2");
    CHECK(d->vlan_vid_active_o == 0x1, "V1 one live entry");

    // V2: second user of the same VID is silent
    h.vlan_evs.clear();
    CHECK(h.vlan_op(true, 2), "V2 join accepted");
    CHECK(h.vlan_evs.empty(), "V2 same VID -> refcount only, ONE join total");

    // V3: periodic re-join of every held VID (one)
    h.vlan_evs.clear();
    d->vlan_periodic_tick_i = 1; h.tick(); d->vlan_periodic_tick_i = 0;
    h.run(40);
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].first == 1
          && h.vlan_evs[0].second == 2, "V3 periodic JoinIn VID 2");

    // V4: Domain VID changed to 5 — a NEW user brings VID 5, the old
    // declaring users keep VID 2 (frozen): two VIDs briefly live
    h.vlan_evs.clear();
    CHECK(h.vlan_op(true, 5), "V4 join accepted");
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].first == 0
          && h.vlan_evs[0].second == 5, "V4 New VID 5");
    CHECK(d->vlan_vid_active_o == 0x3, "V4 two VIDs live across the change");

    // V5: LeaveAll re-joins EVERY VID with users
    h.vlan_evs.clear();
    d->vlan_leaveall_tick_i = 1; h.tick(); d->vlan_leaveall_tick_i = 0;
    h.run(60);
    CHECK(h.vlan_evs.size() == 2, "V5 LeaveAll re-joins both VIDs got %zu",
          h.vlan_evs.size());
    CHECK(h.vlan_evs.size() == 2
          && h.vlan_evs[0] == std::make_pair(1, 2)
          && h.vlan_evs[1] == std::make_pair(1, 5),
          "V5 JoinIn VID 2 and JoinIn VID 5");

    // V6: frozen VID 2 held until its LAST user leaves
    h.vlan_evs.clear();
    CHECK(h.vlan_op(false, 2), "V6 first leave accepted");
    CHECK(h.vlan_evs.empty(), "V6 a remaining user keeps the VID declared");
    CHECK(d->vlan_vid_active_o == 0x3, "V6 still two live entries");
    CHECK(h.vlan_op(false, 2), "V6 second leave accepted");
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].first == 5
          && h.vlan_evs[0].second == 2, "V6 last user out -> Lv VID 2");
    CHECK(d->vlan_vid_active_o == 0x2, "V6 only VID 5 remains");
    h.vlan_evs.clear();
    d->vlan_periodic_tick_i = 1; h.tick(); d->vlan_periodic_tick_i = 0;
    h.run(40);
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].second == 5,
          "V6 periodic now re-joins VID 5 only");

    // V7: leaving an unknown VID is an error strobe, never a wire event
    h.vlan_evs.clear();
    const int e0 = h.vlan_errs;
    CHECK(h.vlan_op(false, 9), "V7 op accepted");
    CHECK(h.vlan_errs == e0 + 1 && h.vlan_evs.empty(),
          "V7 unknown VID -> err strobe, no event");

    // V8: table capacity — 4 entries, the 5th distinct VID errs
    h.vlan_evs.clear();
    CHECK(h.vlan_op(true, 6) && h.vlan_op(true, 7) && h.vlan_op(true, 8),
          "V8 three more VIDs accepted");
    CHECK(h.vlan_evs.size() == 3, "V8 each first user declared");
    const int e1 = h.vlan_errs;
    CHECK(h.vlan_op(true, 10), "V8 overflow op accepted");
    CHECK(h.vlan_errs == e1 + 1, "V8 full table -> err strobe");

    // V9: retire and re-declare the same VID
    h.vlan_evs.clear();
    CHECK(h.vlan_op(false, 5), "V9 leave accepted");
    CHECK(h.vlan_evs.size() == 1 && h.vlan_evs[0].first == 5,
          "V9 Lv VID 5 when its only user leaves");
    CHECK(h.vlan_op(true, 5), "V9 re-join accepted");
    CHECK(h.vlan_evs.size() == 2 && h.vlan_evs[1].first == 0,
          "V9 fresh first user -> New again");
  }
}

void SrpSuite::bridge_the_fsm_declarations_onto_real_frames() {
  // =====================================================================
  // B — bridge: the FSMs' own declarations, through the encoder, onto
  //     real frames (harness plays the event router)
  // =====================================================================
  {
    // leave only VID 5 live for a deterministic re-join set
    CHECK(h.vlan_op(false, 6) && h.vlan_op(false, 7) && h.vlan_op(false, 8),
          "B0 trim table to one VID");
    // stop auto-draining the FSM event faces
    d->dom_ev_ready_i = 0; d->vlan_ev_ready_i = 0;
    d->dom_periodic_tick_i = 1; d->vlan_periodic_tick_i = 1;
    h.tick();
    d->dom_periodic_tick_i = 0; d->vlan_periodic_tick_i = 0;
    // bridge both faces into the encoder push port (domain first)
    int bridged_dom = 0;
    int bridged_vlan = 0;
    for (int i = 0; i < 300; ++i) {
      d->clk_i = 0; d->eval();
      const bool dv = d->dom_ev_valid_o;
      const bool vv = d->vlan_ev_valid_o;
      if (dv) {
        d->enc_ev_app_i = 0; d->enc_ev_attr_type_i = 4;
        d->enc_ev_event_i = d->dom_ev_event_o & 7; d->enc_ev_fourpack_i = 0;
        const uint32_t v = d->dom_ev_value_o;
        uint8_t val[kFirstValueBytes] = {0};
        val[0] = uint8_t(v >> 24); val[1] = uint8_t(v >> 16);
        val[2] = uint8_t(v >> 8);  val[3] = uint8_t(v);
        h.set_val(val);
        d->enc_ev_valid_i = 1;
      } else if (vv) {
        d->enc_ev_app_i = 1; d->enc_ev_attr_type_i = 1;
        d->enc_ev_event_i = d->vlan_ev_event_o & 7; d->enc_ev_fourpack_i = 0;
        const uint16_t v = d->vlan_ev_vid_o;
        uint8_t val[kFirstValueBytes] = {0};
        val[0] = uint8_t(v >> 8); val[1] = uint8_t(v);
        h.set_val(val);
        d->enc_ev_valid_i = 1;
      } else {
        d->enc_ev_valid_i = 0;
      }
      d->eval();
      const bool rdy = d->enc_ev_ready_o;
      d->dom_ev_ready_i = dv && rdy;
      d->vlan_ev_ready_i = !dv && vv && rdy;
      d->eval();
      if (dv && rdy) ++bridged_dom;
      if (!dv && vv && rdy) ++bridged_vlan;
      d->clk_i = 1; d->eval();
    }
    d->enc_ev_valid_i = 0; d->dom_ev_ready_i = 1; d->vlan_ev_ready_i = 1;
    CHECK(bridged_dom == 1 && bridged_vlan == 1,
          "B1 one Domain and one VLAN re-join bridged got %d %d",
          bridged_dom, bridged_vlan);
    std::vector<Ev> bm = {mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02})};
    std::vector<Ev> bv = {mk_ev(1, 1, 1, 0, {0x00, 0x05})};
    CHECK(h.capture_pdu(0, got), "B1 Domain frame captured");
    check_pdu("B1-domain", got, model_pdu(bm, false, OWN_MAC));
    CHECK(h.capture_pdu(1, got), "B1 VLAN frame captured");
    check_pdu("B1-vlan", got, model_pdu(bv, false, OWN_MAC));
  }
}

int SrpSuite::run() {
  bring_out_of_reset();
  encode_the_two_minimal_pdus();
  aggregate_one_window_into_one_frame();
  carry_a_wide_firstvalue_and_one_leaveall();
  keep_the_two_participants_independent();
  pad_the_packed_lanes_and_drop_unknown_types();
  fold_a_full_table_then_backpressure_the_overflow();
  domain_declares_adopts_and_ignores_repeats();
  domain_surfaces_class_a_and_reverts_on_link_down();
  vlan_refcounts_every_vid_and_freezes_the_old_one();
  bridge_the_fsm_declarations_onto_real_frames();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SrpSuite suite;
  return suite.run();
}

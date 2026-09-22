// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_maap suite — the IEEE 1722-2016 Annex B state machine against
// independent expectations (frame bytes from Figure B.1 offsets, the walk
// from Table B.7, intervals from B.3.4, compare_MAC from B.3.6.4 — never
// DUT logic). The engine runs with its REAL services (PRNG, timer at 1 ms =
// 10 clk, TX slot pool); the C++ side plays the TX arbiter's lane and the
// talker's allocator face. What is graded:
//   cold start -> 4 byte-exact PROBEs (1 + MAAP_PROBE_RETRANSMITS) at
//   spacings measured inside the exclusive (500, 600) ms bounds -> the
//   first ANNOUNCE back-to-back with the fourth -> the (30, 32) s announce
//   cadence; the claim publication (addr/valid/state) at each step; the
//   full Table B.7 conflict matrix including both compare_MAC tie-breaks;
//   DEFEND byte-exact with the B.3.6.6 overlap fields; yield ->
//   re-randomize -> per-source conflict fan-out (lowest first) -> re-probe;
//   the allocator seam contract (refuse fast while probing, grant base+s in
//   DEFEND, refuse s >= count, RELEASE acked); footnote-a seeding; the
//   engage/Release! and PortOperational! arcs; maap_version tolerance and
//   reserved-message ignore.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "Vmaap_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

typedef std::vector<uint8_t> Bytes;

// ---- Annex B constants (the standard, not the RTL) ------------------------
constexpr uint64_t MAAP_DA   = 0x91E0F000FF00ull;      // Table B.10
constexpr uint64_t POOL_HI   = 0x91E0F0000000ull;      // Table B.9 base
constexpr unsigned POOL_SIZE = 0xFE00;                 // Table B.9 extent
constexpr uint64_t OWN_MAC   = 0x02AABBCCDDEEull;
constexpr uint64_t EID       = 0x001BC5FFFE000042ull;
constexpr unsigned COUNT     = 8;

// ---- harness scales -------------------------------------------------------
constexpr size_t kMinFrameBytes = 60;    // the 802.3 minimum frame, padded to
constexpr int kClkPerMs = 10;            // the compressed timer: 1 ms = 10 clk
constexpr int kProbeBudgetMs = 700;      // one B.3.4.2 probe interval + slack
constexpr int kWalkRetryRounds = 8;      // probe walks awaited before giving up
constexpr int kRxAcceptCycles = 200;     // guard on the txn_ready_o handshake
constexpr int kAllocWaitCycles = 50;     // guard on the allocator-face answer

struct Frame { Bytes b; uint32_t ms = 0; };

// Figure B.1 frame, 42 real bytes zero-padded to the 60-byte minimum
static Bytes maap_frame(uint64_t da, uint64_t sa, int msg,
                        uint64_t req_start, uint16_t req_cnt,
                        uint64_t con_start, uint16_t con_cnt) {
  Bytes f;
  for (int i = 5; i >= 0; --i) f.push_back(uint8_t(da >> (8 * i)));
  for (int i = 5; i >= 0; --i) f.push_back(uint8_t(sa >> (8 * i)));
  f.push_back(0x22); f.push_back(0xF0);
  f.push_back(0xFE);                       // subtype MAAP
  f.push_back(uint8_t(msg & 0x0F));        // sv 0, version 0, message_type
  f.push_back(0x08);                       // maap_version 1, cdl[10:8] 0
  f.push_back(0x10);                       // cdl 16 (B.2.1)
  for (int i = 0; i < 8; ++i) f.push_back(0x00);   // stream_id (B.2.4)
  for (int i = 5; i >= 0; --i) f.push_back(uint8_t(req_start >> (8 * i)));
  f.push_back(uint8_t(req_cnt >> 8)); f.push_back(uint8_t(req_cnt));
  for (int i = 5; i >= 0; --i) f.push_back(uint8_t(con_start >> (8 * i)));
  f.push_back(uint8_t(con_cnt >> 8)); f.push_back(uint8_t(con_cnt));
  while (f.size() < kMinFrameBytes) f.push_back(0x00);
  return f;
}

// B.3.6.4 octet-wise reversed compare: true = a lower than b
static bool rev_lower(uint64_t a, uint64_t b) {
  uint64_t ra = 0;
  uint64_t rb = 0;
  for (int i = 0; i < 6; ++i) {
    ra = (ra << 8) | ((a >> (8 * i)) & 0xFF);
    rb = (rb << 8) | ((b >> (8 * i)) & 0xFF);
  }
  return ra < rb;
}

// ---- harness --------------------------------------------------------------
struct H {
  Vmaap_wrap* d;
  std::vector<Frame> tx;                   // captured frames, grant-time ms
  // lane/serializer state
  bool ser_busy = false;
  Bytes ser_cur;
  uint32_t ser_ms = 0;
  // conflict sweep capture
  bool confl_auto = false;
  std::vector<int> confl_srcs;

  explicit H(Vmaap_wrap* dd) : d(dd) {}

  void step() {
    d->clk_i = 0; d->eval();
    // TX arbiter lane: grant a committed request, then serialize the slot
    d->txreq_ready_i = 0;
    d->ser_ready_i = 1;
    if (!ser_busy && d->txreq_valid_o) {
      d->txreq_ready_i = 1;                // one-cycle lane grant
      d->ser_req_i = 1;
      d->ser_slot_i = d->txreq_slot_o;
      ser_busy = true;
      ser_cur.clear();
      ser_ms = d->now_ms_o;
    }
    if (ser_busy && d->ser_valid_o) {
      d->ser_req_i = 0;
      ser_cur.push_back(d->ser_data_o);
      if (d->ser_last_o) {
        tx.push_back({ser_cur, ser_ms});
        ser_busy = false;
      }
    }
    // conflict ack policy
    d->conflict_ack_i = 0;
    if (confl_auto && d->conflict_valid_o) {
      d->conflict_ack_i = 1;
      confl_srcs.push_back(int(d->conflict_src_o));
    }
    d->eval();
    d->clk_i = 1; d->eval();
  }
  void idle(int n) { for (int i = 0; i < n; ++i) step(); }
  void run_ms(int ms) { idle(ms * kClkPerMs); }
  uint32_t now() { return d->now_ms_o; }

  // wait until `count` frames are captured or the ms budget runs out
  bool wait_frames(size_t count, int budget_ms) {
    long cyc = long(budget_ms) * kClkPerMs;
    while (tx.size() < count && cyc-- > 0) step();
    return tx.size() >= count;
  }

  // inject one MAAP record (the validator's lanes, pre-parsed)
  void rx(int msg, uint64_t sa, uint64_t req_start, uint16_t req_cnt,
          uint64_t con_start = 0, uint16_t con_cnt = 0, int ver = 1) {
    d->txn_msg_i = msg & 0xF;
    d->txn_status_i = ver & 0x1F;
    d->txn_src_mac_i = sa;
    d->txn_req_i = (req_start << 16) | req_cnt;
    d->txn_conf_i = (con_start << 16) | con_cnt;
    d->txn_valid_i = 1;
    for (int g = 0; g < kRxAcceptCycles; ++g) {
      step();
      if (d->txn_ready_o) break;
    }
    d->txn_valid_i = 0;
    step();
  }

  // one allocator-face request; returns {got, ok, da, accept_lat, rsp_lat}.
  // rsp_lat is measured POST-EDGE: the seam registers the answer at the
  // accepting edge itself (the shim's decision 1), so a healthy request
  // reads back rsp_lat == 0 at this sampling granularity.
  struct AllocRes {
    bool got = false;
    bool ok = false;
    uint64_t da = 0;
    int acc_lat = -1;
    int rsp_lat = -1;
  };
  AllocRes alloc(int src, bool release = false) {
    AllocRes r;
    d->alloc_req_src_i = src & 7;
    d->alloc_req_release_i = release ? 1 : 0;
    d->alloc_req_valid_i = 1;
    bool accepted = false;
    for (int t = 0; t < kAllocWaitCycles; ++t) {
      d->clk_i = 0; d->eval();
      const bool take = !accepted && d->alloc_req_valid_i
                        && d->alloc_req_ready_o;   // handshake at THIS edge
      step_body();
      if (take) { accepted = true; r.acc_lat = t; d->alloc_req_valid_i = 0; }
      if (accepted && d->alloc_rsp_valid_o) {
        r.got = true;
        r.ok = d->alloc_rsp_ok_o;
        r.da = d->alloc_rsp_da_o;
        r.rsp_lat = t - r.acc_lat;
        break;
      }
    }
    d->alloc_req_valid_i = 0;
    step();
    return r;
  }
  // the second half of step() (after the pre-edge eval in alloc())
  void step_body() {
    d->txreq_ready_i = 0;
    d->ser_ready_i = 1;
    if (!ser_busy && d->txreq_valid_o) {
      d->txreq_ready_i = 1;
      d->ser_req_i = 1;
      d->ser_slot_i = d->txreq_slot_o;
      ser_busy = true; ser_cur.clear(); ser_ms = d->now_ms_o;
    }
    if (ser_busy && d->ser_valid_o) {
      d->ser_req_i = 0;
      ser_cur.push_back(d->ser_data_o);
      if (d->ser_last_o) { tx.push_back({ser_cur, ser_ms}); ser_busy = false; }
    }
    d->conflict_ack_i = 0;
    if (confl_auto && d->conflict_valid_o) {
      d->conflict_ack_i = 1;
      confl_srcs.push_back(int(d->conflict_src_o));
    }
    d->eval();
    d->clk_i = 1; d->eval();
  }
};

static void dump(const char* nm, const Bytes& f) {
  printf("  %s:", nm);
  for (size_t i = 0; i < f.size(); ++i) printf(" %02x", f[i]);
  printf("\n");
}

// ---- the suite ------------------------------------------------------------
// One object owns the model, the lane BFM and the tally, so every scenario
// below is a named member function rather than another thousand lines of
// `main` reading state nobody can scope (Core Guidelines I.2, F.3).
namespace {
class MaapAnnexBSuite {
 public:
  int run();

 private:
  void reset_leaves_the_machine_initial();
  void engage_probes_a_fresh_pool_range();
  void cold_walk_retransmits_then_announces();
  void announce_cadence_holds_inside_the_bounds();
  void allocator_seam_serves_the_valid_claim();
  void probe_over_our_block_is_defended();
  void probe_from_below_names_the_first_allocated_address();
  void non_overlapping_probe_is_ignored();
  void announce_from_a_higher_peer_is_ignored();
  void announce_from_a_lower_peer_yields_and_reprobes();
  void probe_from_a_higher_peer_leaves_our_walk_unmoved();
  void defend_during_probe_yields_without_tie_break();
  void reserved_message_types_change_nothing();
  void empty_range_never_conflicts();
  void higher_maap_version_is_still_processed();
  void release_parks_the_machine_without_a_pdu();
  void provisioned_seed_probes_first_and_is_not_reused();
  void alloc_is_refused_while_probing();

  const milan::tb::Model<Vmaap_wrap> model;
  Vmaap_wrap* const d = model.get();
  H h{d};
  int checks = 0;
  int fails = 0;
  uint64_t base = 0;                       // the claim under test, as it moves
  Bytes probe_exp;                         // the PROBE the cold walk must send
};
}  // namespace

// ---- reset + configuration ------------------------------------------------
void MaapAnnexBSuite::reset_leaves_the_machine_initial() {
  d->rst_n = 0;
  d->cfg_en_i = 0; d->cfg_count_i = COUNT;
  d->cfg_seed_offset_i = 0; d->cfg_seed_valid_i = 0;
  d->own_mac_i = OWN_MAC; d->entity_id_i = EID;
  d->link_up_i = 0;
  d->txn_valid_i = 0; d->alloc_req_valid_i = 0; d->conflict_ack_i = 0;
  d->txreq_ready_i = 0; d->ser_req_i = 0; d->ser_slot_i = 0; d->ser_ready_i = 1;
  h.idle(20);
  d->rst_n = 1;
  h.idle(10);

  CHECK(d->state_o == 0 && !d->addr_valid_o, "U0: INITIAL after reset");
}

// ---- U1: engage -> generate_address + ReserveAddress! -> first PROBE ------
void MaapAnnexBSuite::engage_probes_a_fresh_pool_range() {
  d->link_up_i = 1;                  // PRNG seeds; PortOperational! pending
  h.idle(5);
  d->cfg_en_i = 1;                   // Begin!: the machine may now transmit
  CHECK(h.wait_frames(1, kProbeBudgetMs), "U1: first PROBE within one probe interval");
  base = d->addr_o;
  unsigned off = unsigned(base & 0xFFFF);
  CHECK((base >> 16) == (POOL_HI >> 16),
        "U1: claim carries the pool prefix, got %012llx",
        static_cast<unsigned long long>(base));
  CHECK(off <= POOL_SIZE - COUNT,
        "U1: block fits the Table B.9 pool, offset 0x%04x", off);
  CHECK(d->state_o == 1 && !d->addr_valid_o,
        "U1: PROBE state, claim not yet valid");
  probe_exp = maap_frame(MAAP_DA, OWN_MAC, 1, base, COUNT, 0, 0);
  CHECK(h.tx.size() == 1 && h.tx[0].b == probe_exp, "U1: PROBE byte-exact");
  if (h.tx.size() == 1 && h.tx[0].b != probe_exp) {
    dump("got", h.tx[0].b); dump("exp", probe_exp);
  }
}

// ---- U2: 3 retransmits at (500, 600) ms, then ANNOUNCE + DEFEND -----------
void MaapAnnexBSuite::cold_walk_retransmits_then_announces() {
  CHECK(h.wait_frames(5, 4 * kProbeBudgetMs), "U2: 4 PROBEs + 1 ANNOUNCE on a cold walk");
  if (h.tx.size() >= 5) {
    for (int k = 1; k < 4; ++k) {
      CHECK(h.tx[size_t(k)].b == probe_exp, "U2: PROBE %d byte-exact", k + 1);
      long dt = long(h.tx[size_t(k)].ms) - long(h.tx[size_t(k) - 1].ms);
      // B.3.4.2: strictly 500 < T < 600; the grant-time measurement adds
      // at most one compressed ms of walk jitter either way
      CHECK(dt >= 500 && dt <= 601,
            "U2: probe interval %d = %ld ms outside (500, 600)", k, dt);
    }
    Bytes ann_exp = maap_frame(MAAP_DA, OWN_MAC, 3, base, COUNT, 0, 0);
    CHECK(h.tx[4].b == ann_exp, "U2: first ANNOUNCE byte-exact");
    if (h.tx[4].b != ann_exp) { dump("got", h.tx[4].b); dump("exp", ann_exp); }
    long dt_ann = long(h.tx[4].ms) - long(h.tx[3].ms);
    CHECK(dt_ann <= 50,
          "U2: probeCount! sends the ANNOUNCE immediately (dt %ld ms)", dt_ann);
  }
  CHECK(d->state_o == 2 && d->addr_valid_o && d->addr_o == base,
        "U2: DEFEND state, claim valid at the probed base");
  CHECK(d->conflicts_o == 0 && d->defends_o == 0, "U2: counters idle");
}

// ---- U3: announce cadence strictly inside (30, 32) s ----------------------
void MaapAnnexBSuite::announce_cadence_holds_inside_the_bounds() {
  CHECK(h.wait_frames(6, 33000), "U3: second ANNOUNCE inside 33 s");
  if (h.tx.size() >= 6) {
    long dt = long(h.tx[5].ms) - long(h.tx[4].ms);
    CHECK(dt >= 30000 && dt <= 32001,
          "U3: announce interval %ld ms outside (30000, 32000)", dt);
    CHECK(h.tx[5].b == maap_frame(MAAP_DA, OWN_MAC, 3, base, COUNT, 0, 0),
          "U3: periodic ANNOUNCE byte-exact");
  }
}

// ---- U4: the allocator seam over the valid claim --------------------------
void MaapAnnexBSuite::allocator_seam_serves_the_valid_claim() {
  auto r = h.alloc(0);
  CHECK(r.got && r.acc_lat <= 1 && r.rsp_lat == 0,
        "U4: ALLOC accepted at once, answered at the accept edge (acc %d rsp %d)",
        r.acc_lat, r.rsp_lat);
  CHECK(r.ok && r.da == base, "U4: source 0 granted base (got %012llx)",
        static_cast<unsigned long long>(r.da));
  r = h.alloc(5);
  CHECK(r.got && r.ok && r.da == base + 5, "U4: source 5 granted base + 5");
  // count guard: shrink the quasi-static count so source 5 falls outside
  d->cfg_count_i = 4;
  h.idle(2);
  r = h.alloc(5);
  CHECK(r.got && !r.ok && r.da == 0, "U4: source past the count refused");
  // that count change is a block-identity change: every source is told
  h.confl_auto = true;
  h.idle(30);
  h.confl_auto = false;
  CHECK(h.confl_srcs.size() == 8, "U4: %zu conflict events, want 8",
        h.confl_srcs.size());
  bool ordered = h.confl_srcs.size() == 8;
  for (size_t i = 0; ordered && i < 8; ++i) ordered = h.confl_srcs[i] == int(i);
  CHECK(ordered, "U4: conflict sweep lowest-source-first");
  h.confl_srcs.clear();
  d->cfg_count_i = COUNT;
  h.confl_auto = true; h.idle(30); h.confl_auto = false;   // and back
  h.confl_srcs.clear();
  r = h.alloc(3, /*release=*/true);
  CHECK(r.got && !r.ok && r.rsp_lat == 0,
        "U4: RELEASE acknowledged (a no-op on the block claim)");
  CHECK(d->addr_valid_o, "U4: the block survives a RELEASE");
}

// ---- U5: rProbe! in DEFEND -> byte-exact DEFEND (no tie-break) ------------
void MaapAnnexBSuite::probe_over_our_block_is_defended() {
  size_t n0 = h.tx.size();
  const uint64_t their_mac = 0x0A0000000001ull;  // rev-lower than ours,
  CHECK(rev_lower(their_mac, OWN_MAC),           // and STILL defended
        "U5: premise — the prober is rev-lower than us");
  // their probe wants [base+4, base+11]: overlap = [base+4, base+7]
  h.rx(1, their_mac, base + 4, 8);
  CHECK(h.wait_frames(n0 + 1, 100), "U5: DEFEND sent");
  if (h.tx.size() > n0) {
    Bytes def_exp = maap_frame(their_mac, OWN_MAC, 2, base + 4, 8,
                               base + 4, 4);
    CHECK(h.tx[n0].b == def_exp, "U5: DEFEND byte-exact (B.3.6.6 fields)");
    if (h.tx[n0].b != def_exp) { dump("got", h.tx[n0].b); dump("exp", def_exp); }
  }
  CHECK(d->defends_o == 1 && d->conflicts_o == 0 && d->addr_valid_o,
        "U5: defended, nothing yielded");
}

// ---- U5b: a probe from BELOW our base — the max() term of B.3.6.6 ---------
// requested [base-4, base+3]: the FIRST ALLOCATED address in conflict is
// our base, not the requested start; count = 4 overlapping addresses
void MaapAnnexBSuite::probe_from_below_names_the_first_allocated_address() {
  size_t n0 = h.tx.size();
  const uint64_t their_mac = 0x0A0000000002ull;
  h.rx(1, their_mac, base - 4, 8);
  CHECK(h.wait_frames(n0 + 1, 100), "U5b: DEFEND sent");
  if (h.tx.size() > n0) {
    Bytes def_exp = maap_frame(their_mac, OWN_MAC, 2, base - 4, 8,
                               base, 4);
    CHECK(h.tx[n0].b == def_exp,
          "U5b: conflict_start is the first ALLOCATED address (B.3.6.6)");
    if (h.tx[n0].b != def_exp) { dump("got", h.tx[n0].b); dump("exp", def_exp); }
  }
  CHECK(d->defends_o == 2 && d->addr_valid_o, "U5b: defended, claim kept");
}

// ---- U6: a PROBE with no overlap is ignored (footnote b) ------------------
void MaapAnnexBSuite::non_overlapping_probe_is_ignored() {
  size_t n0 = h.tx.size();
  h.rx(1, 0x0A0000000001ull, base + COUNT, 4);   // starts past our block
  h.run_ms(50);
  CHECK(h.tx.size() == n0 && d->defends_o == 2,
        "U6: non-overlapping PROBE ignored");
}

// ---- U7: rAnnounce! in DEFEND, we are rev-lower -> compare_MAC ignores ----
void MaapAnnexBSuite::announce_from_a_higher_peer_is_ignored() {
  const uint64_t hi_mac = 0xF2FFEEDDCCFFull;     // rev-HIGHER than ours
  CHECK(rev_lower(OWN_MAC, hi_mac), "U7: premise — we are rev-lower");
  h.rx(3, hi_mac, base, COUNT);
  h.run_ms(50);
  CHECK(d->addr_valid_o && d->addr_o == base && d->conflicts_o == 0,
        "U7: claim kept — compare_MAC TRUE takes no action");
}

// ---- U8: rAnnounce! in DEFEND, we are rev-higher -> yield -----------------
void MaapAnnexBSuite::announce_from_a_lower_peer_yields_and_reprobes() {
  size_t n0 = h.tx.size();
  const uint64_t lo_mac = 0x010000000000ull;     // rev-lower than ours
  CHECK(rev_lower(lo_mac, OWN_MAC), "U8: premise — they are rev-lower");
  h.confl_auto = true;
  h.rx(3, lo_mac, base, COUNT);
  h.idle(50);
  CHECK(!d->addr_valid_o && d->conflicts_o == 1,
        "U8: yielded — claim invalid, re-address counted");
  // the block moved: all 8 sources are told, lowest first
  h.idle(30);
  h.confl_auto = false;
  CHECK(h.confl_srcs.size() == 8, "U8: %zu conflict events, want 8",
        h.confl_srcs.size());
  h.confl_srcs.clear();
  // Restart!: a FRESH random range, 4 probes, announce, DEFEND again
  CHECK(h.wait_frames(n0 + 5, 5 * kProbeBudgetMs), "U8: re-probe walk completed");
  uint64_t base2 = d->addr_o;
  CHECK(base2 != base, "U8: generate_address drew a fresh range");
  CHECK((base2 & 0xFFFF) <= POOL_SIZE - COUNT, "U8: new block fits");
  if (h.tx.size() >= n0 + 5) {
    Bytes p2 = maap_frame(MAAP_DA, OWN_MAC, 1, base2, COUNT, 0, 0);
    Bytes a2 = maap_frame(MAAP_DA, OWN_MAC, 3, base2, COUNT, 0, 0);
    bool probes_ok = true;
    for (int k = 0; k < 4; ++k)
      probes_ok = probes_ok && (h.tx[n0 + size_t(k)].b == p2);
    CHECK(probes_ok, "U8: re-probe frames carry the fresh range");
    CHECK(h.tx[n0 + 4].b == a2, "U8: re-announce byte-exact");
  }
  CHECK(d->addr_valid_o && d->state_o == 2, "U8: claim re-established");
  base = base2;
}

// ---- U9: rProbe! in PROBE, we are rev-lower -> keep probing ---------------
void MaapAnnexBSuite::probe_from_a_higher_peer_leaves_our_walk_unmoved() {
  // force a fresh walk: PortOperational! bounce re-randomizes
  d->link_up_i = 0; h.idle(30);
  size_t n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "U9: walk restarted on link return");
  uint64_t b9 = d->addr_o;
  CHECK(d->state_o == 1, "U9: PROBE state");
  const uint64_t hi_mac = 0xF2FFEEDDCCFFull;
  h.rx(1, hi_mac, b9, COUNT);                    // their probe, we are lower
  h.run_ms(20);
  CHECK(d->addr_o == b9 && d->conflicts_o == 1,
        "U9: compare_MAC TRUE — our probe walk continues unmoved");
  // walk completes on the SAME range
  CHECK(h.wait_frames(n0 + 5, 5 * kProbeBudgetMs) && d->addr_o == b9 && d->addr_valid_o,
        "U9: claim lands on the contested range we won");
  base = b9;
}

// ---- U10: rDefend! in PROBE -> yield, no tie-break ------------------------
void MaapAnnexBSuite::defend_during_probe_yields_without_tie_break() {
  d->link_up_i = 0; h.idle(30);
  size_t n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "U10: probing again");
  uint64_t b10 = d->addr_o;
  const uint64_t hi_mac = 0xF2FFEEDDCCFFull;     // even a rev-higher peer
  h.confl_auto = true;
  // a DEFEND names its owner's range in the CONFLICT fields (B.2.7):
  // requested echoes some third party; the conflict range hits us
  h.rx(2, hi_mac, 0x91E0F0000000ull, 1, b10 + 2, 2);
  h.idle(50);
  h.confl_auto = false;
  h.confl_srcs.clear();
  CHECK(d->conflicts_o == 2, "U10: PROBE-state rDefend! yields, no tie-break");
  CHECK(h.wait_frames(n0 + 6, 6 * kProbeBudgetMs) && d->addr_valid_o,
        "U10: fresh walk completes");
  CHECK(d->addr_o != b10, "U10: range re-randomized");
  base = d->addr_o;
}

// ---- U11: reserved message_type ignored (B.2.2) ---------------------------
void MaapAnnexBSuite::reserved_message_types_change_nothing() {
  size_t n0 = h.tx.size();
  uint8_t c0 = d->conflicts_o;
  h.rx(4, 0x010000000000ull, base, COUNT);       // reserved type, overlaps
  h.rx(0, 0x010000000000ull, base, COUNT);
  h.run_ms(30);
  CHECK(h.tx.size() == n0 && d->conflicts_o == c0 && d->addr_valid_o,
        "U11: reserved message types change nothing");
}

// ---- U12: an empty range never conflicts ----------------------------------
void MaapAnnexBSuite::empty_range_never_conflicts() {
  uint8_t c0 = d->conflicts_o;
  h.rx(3, 0x010000000000ull, base, 0);           // count 0 = empty
  h.run_ms(30);
  CHECK(d->addr_valid_o && d->conflicts_o == c0,
        "U12: zero-count range is empty, no event");
}

// ---- U13: maap_version tolerance (B.2.3.2) --------------------------------
void MaapAnnexBSuite::higher_maap_version_is_still_processed() {
  h.confl_auto = true;
  h.rx(3, 0x010000000000ull, base, COUNT, 0, 0, /*ver=*/2);
  h.idle(50);
  CHECK(!d->addr_valid_o,
        "U13: a higher maap_version with a known type is still processed");
  CHECK(h.wait_frames(h.tx.size() + 1, kProbeBudgetMs), "U13: walk restarted");
  h.idle(50);
  h.confl_auto = false;
  h.confl_srcs.clear();
  // let the fresh walk finish before the next scenario
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
  CHECK(d->addr_valid_o, "U13: reclaimed");
  base = d->addr_o;
}

// ---- U14: Release! (engage fall) is local — no PDU, machine parks ---------
void MaapAnnexBSuite::release_parks_the_machine_without_a_pdu() {
  size_t n0 = h.tx.size();
  h.confl_auto = true;
  d->cfg_en_i = 0;
  h.idle(60);
  h.confl_auto = false;
  CHECK(!d->addr_valid_o && d->state_o == 0,
        "U14: INITIAL after Release!, claim withdrawn");
  CHECK(h.tx.size() == n0, "U14: Release! sends NOTHING (footnote c)");
  CHECK(h.confl_srcs.size() == 8, "U14: sources told the block is gone");
  h.confl_srcs.clear();
  // allocator refuses while parked, still in one cycle
  auto r = h.alloc(0);
  CHECK(r.got && !r.ok && r.rsp_lat == 0, "U14: parked ALLOC refused fast");
}

// ---- U15: footnote-a seeding — the provisioned range probes first ---------
void MaapAnnexBSuite::provisioned_seed_probes_first_and_is_not_reused() {
  size_t n0 = h.tx.size();
  d->cfg_seed_offset_i = 0x1234;
  d->cfg_seed_valid_i = 1;
  d->cfg_en_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "U15: seeded walk starts");
  CHECK((d->addr_o & 0xFFFF) == 0x1234,
        "U15: first attempt probes the provisioned offset (got 0x%04llx)",
        static_cast<unsigned long long>(d->addr_o & 0xFFFF));
  if (h.tx.size() > n0) {
    Bytes p = maap_frame(MAAP_DA, OWN_MAC, 1, POOL_HI | 0x1234, COUNT, 0, 0);
    CHECK(h.tx[n0].b == p, "U15: seeded PROBE byte-exact");
  }
  // a conflict must NOT reuse the seed: the conflicted range is known-bad
  h.confl_auto = true;
  h.rx(3, 0x010000000000ull, POOL_HI | 0x1234, COUNT);
  h.idle(50);
  CHECK(h.wait_frames(n0 + 2, kProbeBudgetMs), "U15: restart probes");
  CHECK((d->addr_o & 0xFFFF) != 0x1234,
        "U15: the conflicted seed is not probed again");
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
  h.confl_auto = false;
  h.confl_srcs.clear();
  CHECK(d->addr_valid_o, "U15: reclaimed after the seed conflict");
  d->cfg_seed_valid_i = 0;
}

// ---- U16: ALLOC refused during PROBE (the shim's decision 1/5 path) -------
void MaapAnnexBSuite::alloc_is_refused_while_probing() {
  d->link_up_i = 0; h.idle(30);
  size_t n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "U16: probing");
  CHECK(d->state_o == 1, "U16: PROBE state");
  auto r = h.alloc(0);
  CHECK(r.got && !r.ok && r.acc_lat <= 1 && r.rsp_lat == 0,
        "U16: still-probing ALLOC refused in one cycle, never parked");
  for (int g = 0; g < kWalkRetryRounds && !d->addr_valid_o; ++g) h.run_ms(kProbeBudgetMs);
  CHECK(d->addr_valid_o, "U16: claim completes after the refusal");
  auto r2 = h.alloc(1);
  CHECK(r2.got && r2.ok && r2.da == d->addr_o + 1,
        "U16: the same source path grants once the claim stands");
}

int MaapAnnexBSuite::run() {
  reset_leaves_the_machine_initial();
  engage_probes_a_fresh_pool_range();
  cold_walk_retransmits_then_announces();
  announce_cadence_holds_inside_the_bounds();
  allocator_seam_serves_the_valid_claim();
  probe_over_our_block_is_defended();
  probe_from_below_names_the_first_allocated_address();
  non_overlapping_probe_is_ignored();
  announce_from_a_higher_peer_is_ignored();
  announce_from_a_lower_peer_yields_and_reprobes();
  probe_from_a_higher_peer_leaves_our_walk_unmoved();
  defend_during_probe_yields_without_tie_break();
  reserved_message_types_change_nothing();
  empty_range_never_conflicts();
  higher_maap_version_is_still_processed();
  release_parks_the_machine_without_a_pdu();
  provisioned_seed_probes_first_and_is_not_reused();
  alloc_is_refused_while_probing();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  MaapAnnexBSuite suite;
  return suite.run();
}

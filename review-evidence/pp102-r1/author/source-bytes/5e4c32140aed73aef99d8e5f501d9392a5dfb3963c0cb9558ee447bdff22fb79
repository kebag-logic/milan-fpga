// SPDX-License-Identifier: CERN-OHL-W-2.0
// srp_top suite — END-TO-END through the REAL blocks: an MRPDU byte stream
// in produces registrations that flow to declarations out, byte-exact on
// the wire through a real KL_pp_tx_slots instance; DECLARE_TALKER TSpec ->
// Σ-slope admission cross-checked against an INDEPENDENT model of the
// Milan v1.2 §4.3.3.2 recipe (the silicon-measured KL_lwsrp_bw_gate
// formula) with the greedy index-order walk and the 75 % port-rate
// ceiling; over-ceiling refusal -> Talker Failed code 1 on the wire +
// granted 0; the certified two-class Domain arrival (FirstValue {5,2,VID},
// NumberOfValues 2) adopts and re-declares end-to-end; LeaveAll cycles run
// per application off the real KL_pp_prng (kind 3) + KL_pp_timer_service.
// Expectations are independent: MRPDU frames are built/parsed here from
// 802.1Q §10.8/§35.2.2, never from DUT logic.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <vector>
#include "Vsrp_top_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---------------------------------------------------------------------------
// constants (TB shape)
// ---------------------------------------------------------------------------
constexpr int         MS_CYC   = 40;                    // wrap: 1 ms = 40 clk
constexpr uint64_t    OWN_MAC  = 0x0A0B0C0D0E0FULL;
constexpr uint64_t    EID      = 0x123456789ABCDEF0ULL;
constexpr uint32_t    RATE     = 100000000u;            // 100 Mb/s port
constexpr uint64_t    LIMIT    = 75000000ull;           // 75 % ceiling
constexpr uint32_t    ACC_LAT  = 0x000186A0u;           // cfg initial latency
constexpr uint64_t    MSRP_DA  = 0x0180C200000EULL;
constexpr uint64_t    MVRP_DA  = 0x0180C2000021ULL;

// class-B request handshake guard, in clock cycles: the wait for req_ready_o
// and the wait for the matching rsp_valid_o
constexpr int         OP_GUARD = 200000;

// class-B ops / status (KL_srp_top banner)
constexpr int OP_DECL_TK = 0;
constexpr int OP_WDRW_TK = 1;
constexpr int OP_DECL_LS = 2;
constexpr int OP_WDRW_LS = 3;
constexpr int OP_GET_DOM = 4;
constexpr int ST_OK      = 0;
constexpr int ST_FAIL    = 1;
constexpr int ST_UNSUP   = 2;

// MRP attribute events (802.1Q §35.2.2.7.2) + Listener declarations
constexpr int EV_NEW         = 0;
constexpr int EV_JOININ      = 1;
constexpr int EV_IN          = 2;
constexpr int EV_JOINMT      = 3;
constexpr int EV_MT          = 4;
constexpr int EV_LV          = 5;
constexpr int DECL_IGNORE    = 0;
constexpr int DECL_ASKFAIL   = 1;
constexpr int DECL_READY     = 2;
constexpr int DECL_READYFAIL = 3;

// ---------------------------------------------------------------------------
// independent Σ-slope model (Milan v1.2 §4.3.3.2, reference formula)
// ---------------------------------------------------------------------------
static uint64_t slope_bps(uint32_t mfs, uint32_t mif) {
  uint64_t f = static_cast<uint64_t>(mfs) + 22;  // L2 hdr incl. VLAN tag + FCS
  if (f < 68) f = 68;                   // tagged minimum-size frame
  uint64_t w = f + 20;                  // preamble + IPG
  return w * mif * 8000ull * 8ull;      // class-A 8000 intervals/s
}

struct AdmModel {
  bool     req[8] = {};
  uint32_t mfs[8] = {};
  uint32_t mif[8] = {};
  bool     grant[8];
  uint64_t granted[8];
  uint64_t sum;
  bool     over;
  void walk() {                         // greedy in stream-index order
    uint64_t acc = 0;
    over = false;
    for (int s = 0; s < 8; s++) {
      grant[s] = false; granted[s] = 0;
      if (!req[s]) continue;
      uint64_t sl = slope_bps(mfs[s], mif[s]);
      if (acc + sl <= LIMIT) { grant[s] = true; granted[s] = sl; acc += sl; }
      else                   { over = true; }
    }
    sum = acc;
  }
};

// ---------------------------------------------------------------------------
// independent MRPDU builder (802.1Q §10.8.1.2 BNF, §35.2.2)
// ---------------------------------------------------------------------------
struct Vec {
  bool la = false;                      // LeaveAllEvent on this VectorHeader
  int nov = 1;
  std::vector<uint8_t> fv;              // FirstValue bytes
  std::vector<int> ev;                  // ThreePacked lane, one per value
  std::vector<int> fp;                  // FourPacked lane (Listener only)
};
struct Msg { int type; int alen; bool listener; std::vector<Vec> vecs; };

static void put16(std::vector<uint8_t>& b, uint16_t v) {
  b.push_back(v >> 8); b.push_back(v & 0xFF);
}
static void put_mac(std::vector<uint8_t>& b, uint64_t m) {
  for (int i = 5; i >= 0; i--) b.push_back((m >> (8 * i)) & 0xFF);
}
static std::vector<uint8_t> vec_bytes(const Vec& v, bool listener) {
  std::vector<uint8_t> b;
  b.push_back((v.la ? 0x20 : 0x00) | ((v.nov >> 8) & 0x1F));
  b.push_back(v.nov & 0xFF);
  b.insert(b.end(), v.fv.begin(), v.fv.end());
  for (int i = 0; i < v.nov; i += 3) {
    int e[3] = {0, 0,
                0};
    for (int j = 0; j < 3 && i + j < v.nov; j++) e[j] = v.ev[i + j];
    b.push_back(static_cast<uint8_t>(((e[0] * 6) + e[1]) * 6 + e[2]));
  }
  if (listener) {
    for (int i = 0; i < v.nov; i += 4) {
      int p[4] = {0, 0,
                  0, 0};
      for (int j = 0; j < 4 && i + j < v.nov; j++) p[j] = v.fp[i + j];
      b.push_back(
          static_cast<uint8_t>(p[0] * 64 + p[1] * 16 + p[2] * 4 + p[3]));
    }
  }
  return b;
}
// body = ProtocolVersion..EndMark (the shape fed to the decoder)
static std::vector<uint8_t> mrpdu_body(bool msrp, const std::vector<Msg>& ms) {
  std::vector<uint8_t> b;
  b.push_back(0x00);                    // ProtocolVersion
  for (const Msg& m : ms) {
    b.push_back(static_cast<uint8_t>(m.type));
    b.push_back(static_cast<uint8_t>(m.alen));
    std::vector<uint8_t> body;
    for (const Vec& v : m.vecs) {
      auto vb = vec_bytes(v, m.listener);
      body.insert(body.end(), vb.begin(), vb.end());
    }
    if (msrp) put16(b, static_cast<uint16_t>(body.size() + 2));  // + EndMark
    b.insert(b.end(), body.begin(), body.end());
    put16(b, 0x0000);                   // AttributeList EndMark
  }
  put16(b, 0x0000);                     // MRPDU EndMark
  return b;
}
// full expected TX frame (Ethernet header + body)
static std::vector<uint8_t> mrpdu_frame(bool msrp, const std::vector<Msg>& ms) {
  std::vector<uint8_t> b;
  put_mac(b, msrp ? MSRP_DA : MVRP_DA);
  put_mac(b, OWN_MAC);
  put16(b, msrp ? 0x22EA : 0x88F5);
  auto body = mrpdu_body(msrp, ms);
  b.insert(b.end(), body.begin(), body.end());
  return b;
}

// FirstValue builders
static std::vector<uint8_t> fv_talker(uint64_t sid, uint64_t da, uint16_t vid,
                                      uint16_t mfs, uint16_t mif, int prio,
                                      int rank, uint32_t lat) {
  std::vector<uint8_t> b;
  for (int i = 7; i >= 0; i--) b.push_back((sid >> (8 * i)) & 0xFF);
  put_mac(b, da);
  put16(b, vid); put16(b, mfs); put16(b, mif);
  b.push_back(static_cast<uint8_t>((prio << 5) | (rank << 4)));
  for (int i = 3; i >= 0; i--) b.push_back((lat >> (8 * i)) & 0xFF);
  return b;
}
static std::vector<uint8_t> fv_failed(uint64_t sid, uint64_t da, uint16_t vid,
                                      uint16_t mfs, uint16_t mif, int prio,
                                      int rank, uint32_t lat, uint64_t sysid,
                                      uint8_t code) {
  auto b = fv_talker(sid, da, vid, mfs, mif, prio, rank, lat);
  for (int i = 7; i >= 0; i--) b.push_back((sysid >> (8 * i)) & 0xFF);
  b.push_back(code);
  return b;
}
static std::vector<uint8_t> fv_sid(uint64_t sid) {
  std::vector<uint8_t> b;
  for (int i = 7; i >= 0; i--) b.push_back((sid >> (8 * i)) & 0xFF);
  return b;
}
static std::vector<uint8_t> fv_domain(uint8_t cid, uint8_t prio, uint16_t vid) {
  std::vector<uint8_t> b{cid, prio};
  put16(b, vid);
  return b;
}
static std::vector<uint8_t> fv_vid(uint16_t vid) {
  std::vector<uint8_t> b;
  put16(b, vid);
  return b;
}

// ---------------------------------------------------------------------------
// independent MRPDU parser (structure walk; used for set-style checks)
// ---------------------------------------------------------------------------
struct PVec { int type; bool la; int nov; std::vector<uint8_t> fv;
              std::vector<int> ev; std::vector<int> fp; };
struct PFrame { bool ok = false; bool msrp = false; std::vector<PVec> vecs; };

static PFrame parse_frame(const std::vector<uint8_t>& f) {
  PFrame r;
  if (f.size() < 17) return r;
  uint16_t et = (f[12] << 8) | f[13];
  if (et == 0x22EA) r.msrp = true;
  else if (et == 0x88F5) r.msrp = false;
  else return r;
  size_t i = 14;
  if (f[i++] != 0x00) return r;         // ProtocolVersion
  while (i + 1 < f.size()) {
    if (f[i] == 0x00 && f[i + 1] == 0x00) { i += 2; r.ok = true; break; }
    int type = f[i++];
    if (i >= f.size()) return r;
    int alen = f[i++];
    if (r.msrp) { if (i + 2 > f.size()) return r; i += 2; }  // list length
    for (;;) {                          // vectors until list EndMark
      if (i + 2 > f.size()) return r;
      if (f[i] == 0x00 && f[i + 1] == 0x00) { i += 2; break; }
      PVec v; v.type = type;
      v.la  = (f[i] & 0xE0) != 0;
      v.nov = ((f[i] & 0x1F) << 8) | f[i + 1];
      i += 2;
      if (i + static_cast<size_t>(alen) > f.size()) return r;
      v.fv.assign(f.begin() + i, f.begin() + i + alen);
      i += alen;
      int n3 = (v.nov + 2) / 3;
      if (i + static_cast<size_t>(n3) > f.size()) return r;
      for (int k = 0; k < n3; k++) {
        int b = f[i + k];
        v.ev.push_back(b / 36); v.ev.push_back((b / 6) % 6);
        v.ev.push_back(b % 6);
      }
      i += n3;
      if (r.msrp && type == 3) {
        int n4 = (v.nov + 3) / 4;
        if (i + static_cast<size_t>(n4) > f.size()) return r;
        for (int k = 0; k < n4; k++) {
          int b = f[i + k];
          v.fp.push_back(b / 64); v.fp.push_back((b / 16) % 4);
          v.fp.push_back((b / 4) % 4); v.fp.push_back(b % 4);
        }
        i += n4;
      }
      v.ev.resize(v.nov);
      if (r.msrp && type == 3) v.fp.resize(v.nov);
      r.vecs.push_back(v);
    }
  }
  return r;
}

static uint64_t fv_u64(const std::vector<uint8_t>& fv, int off, int n) {
  uint64_t v = 0;
  for (int i = 0; i < n; i++) v = (v << 8) | fv[off + i];
  return v;
}

// does the frame carry {type, key, event}? key = stream_id (types 1/2/3),
// SRclassID (type 4 MSRP), VID (MVRP type 1)
static bool frame_has(const std::vector<uint8_t>& f, bool msrp, int type,
                      uint64_t key, int ev) {
  auto p = parse_frame(f);
  if (p.msrp != msrp) return false;
  for (auto& v : p.vecs) {
    if (v.type != type) continue;
    uint64_t k = 0;
    if (!msrp)           k = fv_u64(v.fv, 0, 2);
    else if (type == 4)  k = v.fv[0];
    else                 k = fv_u64(v.fv, 0, 8);
    if (k == key && !v.ev.empty() && v.ev[0] == ev) return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// harness
// ---------------------------------------------------------------------------
struct H {
  Vsrp_top_wrap* d;
  vluint64_t t = 0;
  // frame capture
  bool streaming = false;
  std::vector<uint8_t> cur;
  std::deque<std::vector<uint8_t>> q_msrp;
  std::deque<std::vector<uint8_t>> q_mvrp;
  std::vector<std::vector<uint8_t>> archive;   // everything ever captured
  // strobe accounting
  int reg_cnt[8] = {};
  int unreg_cnt[8] = {};
  int domchg = 0;
  int malformed = 0;

  explicit H(Vsrp_top_wrap* dd) : d(dd) {}

  // one clock: low-phase observe (all strobes are registered and stable
  // across the cycle), drive the TX-arbiter emulation, posedge.
  // Returns the decoder's ready as sampled in the low phase.
  bool step() {
    d->clk_i = 0; d->eval();
    bool mready = d->mrp_ready_o != 0;
    for (int k = 0; k < 8; k++) {
      if ((d->evt_tk_registered_o >> k) & 1)   reg_cnt[k]++;
      if ((d->evt_tk_unregistered_o >> k) & 1) unreg_cnt[k]++;
    }
    if (d->evt_domain_change_o) domchg++;
    if (d->dbg_pdu_done_o && d->dbg_pdu_malformed_o) malformed++;
    // TX arbiter emulation (03 §8): accept requests, stream the slot out
    d->ser_ready_i = 1;
    d->txreq_ready_i = 0;
    d->ser_req_i = 0;
    if (streaming && d->ser_valid_o) {
      cur.push_back(d->ser_data_o);
      if (d->ser_last_o) {
        archive.push_back(cur);
        uint16_t et = cur.size() > 13 ? ((cur[12] << 8) | cur[13]) : 0;
        if (et == 0x22EA) q_msrp.push_back(cur);
        else              q_mvrp.push_back(cur);
        cur.clear();
        streaming = false;
      }
    }
    if (!streaming && d->txreq_valid_o) {
      d->txreq_ready_i = 1;
      d->ser_req_i = 1;
      d->ser_slot_i = d->txreq_slot_o;
      streaming = true;
      cur.clear();
    }
    d->clk_i = 1; d->eval();
    t++;
    return mready;
  }
  void cycle() { (void)step(); }
  void idle(int n) { for (int i = 0; i < n; i++) cycle(); }
  void run_ms(int ms) { idle(ms * MS_CYC); }

  void reset() {
    d->rst_n = 0;
    d->own_mac_i = OWN_MAC; d->entity_id_i = EID;
    d->link_up_i = 0; d->p2p_i = 1; d->cfg_rank_i = 1;
    d->cfg_acc_lat_ns_i = ACC_LAT; d->port_rate_bps_i = RATE;
    d->mrp_valid_i = 0; d->mrp_data_i = 0; d->mrp_last_i = 0;
    d->mrp_msrp_i = 1;
    d->req_valid_i = 0; d->req_op_i = 0; d->req_index_i = 0;
    d->req_stream_id_i = 0; d->req_da_i = 0; d->req_vid_i = 0;
    d->req_max_frame_i = 0; d->req_max_interval_i = 0;
    d->req_lstn_state_i = 0;
    d->txreq_ready_i = 0; d->ser_req_i = 0; d->ser_slot_i = 0;
    d->ser_ready_i = 1;
    idle(10);
    d->rst_n = 1;
    idle(5);
  }

  // feed one header-stripped MRPDU into the decoder (handshake honored)
  void feed(const std::vector<uint8_t>& b, bool msrp) {
    for (size_t i = 0; i < b.size();) {
      d->mrp_valid_i = 1;
      d->mrp_data_i = b[i];
      d->mrp_msrp_i = msrp ? 1 : 0;
      d->mrp_last_i = (i + 1 == b.size()) ? 1 : 0;
      if (step()) i++;                  // consumed at that posedge
    }
    d->mrp_valid_i = 0;
    d->mrp_last_i = 0;
    idle(8);
  }

  // class-B op; returns {status, data}
  struct Rsp { int status; uint32_t data; bool got; };
  Rsp op(int opc, int idx, uint64_t sid = 0, uint64_t da = 0, int vid = 0,
         int mfs = 0, int mif = 0, int lstn = 0) {
    int guard = OP_GUARD;
    while (!d->req_ready_o && guard--) cycle();
    d->req_valid_i = 1;
    d->req_op_i = opc; d->req_index_i = idx;
    d->req_stream_id_i = sid; d->req_da_i = da; d->req_vid_i = vid;
    d->req_max_frame_i = mfs; d->req_max_interval_i = mif;
    d->req_lstn_state_i = lstn;
    cycle();                             // accepted at this posedge
    d->req_valid_i = 0;
    Rsp r{ -1, 0, false };
    for (int i = 0; i < OP_GUARD; i++) {
      if (d->rsp_valid_o) {              // registered strobe, post-edge view
        r.status = d->rsp_status_o; r.data = d->rsp_data_o; r.got = true;
        cycle();
        break;
      }
      cycle();
    }
    return r;
  }

  // pop the next frame of an application matching pred (skips + keeps the
  // rest in the archive); empty vector on timeout
  template <typename P>
  std::vector<uint8_t> wait_frame(bool msrp, int timeout_ms, P pred) {
    long budget = static_cast<long>(timeout_ms) * MS_CYC;
    for (;;) {
      auto& q = msrp ? q_msrp : q_mvrp;
      while (!q.empty()) {
        auto f = q.front(); q.pop_front();
        if (pred(f)) return f;
      }
      if (budget-- <= 0) return {};
      cycle();
    }
  }
  std::vector<uint8_t> wait_any(bool msrp, int timeout_ms) {
    return wait_frame(msrp, timeout_ms,
                      [](const std::vector<uint8_t>&) { return true; });
  }
  // align inside a clean 200 ms slot: past the T-MRP-PERIODIC boundary
  // bundle (drained at boundary+0) AND the tick after it (boundary+200,
  // which carries the periodic! JoinMt re-joins), then flush the queues —
  // an action taken here drains alone at the next join tick, so its frame
  // can be checked byte-exact against the independent builder
  void sync() {
    for (;;) {
      uint32_t ph = d->now_ms_o % 1000u;
      if (ph >= 250 && ph <= 350) break;
      cycle();
    }
    while (!q_msrp.empty()) q_msrp.pop_front();
    while (!q_mvrp.empty()) q_mvrp.pop_front();
  }

  // wide/packed output helpers
  uint32_t granted(int s) { return d->granted_slope_bps_o[s]; }
  uint32_t acclat(int k)  { return d->acc_latency_o[k]; }
  uint64_t src_bridge(int s) {
    return (static_cast<uint64_t>(d->src_fail_bridge_o[2 * s + 1]) << 32)
         | d->src_fail_bridge_o[2 * s];
  }
  uint64_t snk_bridge(int k) {
    return (static_cast<uint64_t>(d->snk_fail_bridge_o[2 * k + 1]) << 32)
         | d->snk_fail_bridge_o[2 * k];
  }
  int tk_decl(int s)  { return (d->tk_decl_state_o   >> (2 * s)) & 3; }
  int tk_reg(int k)   { return (d->tk_reg_state_o    >> (2 * k)) & 3; }
  int ls_decl(int k)  { return (d->lstn_decl_state_o >> (2 * k)) & 3; }
  uint8_t src_fcode(int s) { return (d->src_fail_code_o >> (8 * s)) & 0xFF; }
  uint8_t snk_fcode(int k) { return (d->snk_fail_code_o >> (8 * k)) & 0xFF; }
};

static void dump(const char* tag, const std::vector<uint8_t>& f) {
  printf("  %s (%zu B):", tag, f.size());
  for (uint8_t c : f) printf(" %02x", c);
  printf("\n");
}

namespace {

//! The whole end-to-end bench under one owner (Core Guidelines I.2): the DUT,
//! the BFM that captures its wire, the independent admission model the wire is
//! judged against, and the tally. Each scenario below keeps the banner it had
//! in `main` and is named for what it proves rather than for its letter (F.3).
class SrpTopHarness {
 public:
  SrpTopHarness() : d(model.get()), h(d) {}

  int run() {
    bring_up_the_port();
    check_domain_default_declaration_is_byte_exact();
    check_get_domain_and_bad_ops();
    check_declare_talker_admits_and_advertises();
    check_over_ceiling_refusal_is_talker_failed();
    check_freed_capacity_admits_the_refused_source();
    check_listener_registration_becomes_a_ready_declaration();
    check_certified_domain_arrival_adopts_and_redeclares();
    check_own_msrp_leaveall_cycle();
    check_received_msrp_leaveall_ages_to_expiry();
    check_mvrp_leaveall_is_its_own_participant();
    check_peer_leaveall_cadence_stays_bounded();
    check_admission_sweep_matches_the_model();

    printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }

 private:
  static constexpr uint64_t SID0 = (OWN_MAC << 16) | 0x0001;
  static constexpr uint64_t SID1 = (OWN_MAC << 16) | 0x0002;
  static constexpr uint64_t DA0  = 0x91E0F00A0B01ULL;
  static constexpr uint64_t DA1  = 0x91E0F00A0B11ULL;
  static constexpr uint64_t SIDX = 0x1122334455660001ULL;
  static constexpr uint64_t DAX  = 0x91E0F0112233ULL;

  void bring_up_the_port() {
    h.reset();
    d->link_up_i = 1;                     // seeds the PRNG + Domain declares
    h.idle(10);
  }

  // ==== 0. bring-up: Domain default declaration, byte-exact ===============
  void check_domain_default_declaration_is_byte_exact() {
    auto f = h.wait_any(true, 1000);
    CHECK(!f.empty(), "0: first MSRP frame within 1 s");
    Msg m{4, 4, false, {Vec{false, 1, fv_domain(6, 3, 2), {EV_NEW}, {}}}};
    auto exp = mrpdu_frame(true, {m});
    CHECK(f == exp, "0: Domain New {6,3,2} byte-exact");
    if (!f.empty() && f != exp) { dump("got", f); dump("exp", exp); }
    CHECK(d->class_a_prio_o == 3 && d->class_a_vid_o == 2,
          "0: class-D domain defaults");
    CHECK(d->domain_adopted_o == 0, "0: DEFAULTS state");
    CHECK(h.q_mvrp.empty(), "0: no MVRP declaration yet");
    CHECK(h.malformed == 0, "0: no malformed PDUs");
  }

  // ==== A. GET_DOMAIN / bad ops ===========================================
  void check_get_domain_and_bad_ops() {
    auto r = h.op(OP_GET_DOM, 6);
    CHECK(r.got && r.status == ST_OK, "A: GET_DOMAIN class A OK");
    CHECK(((r.data >> 16) & 7) == 3 && (r.data & 0xFFF) == 2,
          "A: GET_DOMAIN {prio 3, vid 2}, got 0x%08x", r.data);
    r = h.op(OP_GET_DOM, 5);
    CHECK(r.got && r.status == ST_FAIL, "A: GET_DOMAIN class 5 FAILs");
    r = h.op(7, 0);
    CHECK(r.got && r.status == ST_UNSUP, "A: unknown op UNSUPPORTED");
    r = h.op(OP_DECL_TK, 9, SID0, DA0, 2, 100, 1);
    CHECK(r.got && r.status == ST_FAIL, "A: out-of-range source FAILs");
  }

  // ==== B. DECLARE_TALKER -> admission + Advertise on the wire ============
  void check_declare_talker_admits_and_advertises() {
    h.sync();
    auto r = h.op(OP_DECL_TK, 0, SID0, DA0, 2, 1024, 1);
    CHECK(r.got && r.status == ST_OK, "B: DECLARE_TALKER src 0 OK");
    mdl.req[0] = true; mdl.mfs[0] = 1024; mdl.mif[0] = 1; mdl.walk();
    h.idle(200);                        // > 2 admission rounds
    CHECK((d->sr_admitted_o & 1) == 1, "B: src 0 admitted");
    CHECK(h.granted(0) == mdl.granted[0],
          "B: granted slope %u vs model %llu", h.granted(0),
          static_cast<unsigned long long>(mdl.granted[0]));
    CHECK(d->sum_slope_bps_o == mdl.sum, "B: sum slope vs model");
    CHECK(d->over_limit_o == 0, "B: no over_limit");
    CHECK(h.tk_decl(0) == 1, "B: tk_decl_state ADVERTISE");
    CHECK(d->active_o == 0, "B: not ACTIVE without a Ready listener");
    // wire: Talker Advertise New byte-exact, then the Table 10-3 fresh-
    // declaration ladder (New again from AN, JoinMt from AA) as set-checks
    auto fv = fv_talker(SID0, DA0, 2, 1024, 1, 3, 1, ACC_LAT);
    auto exp1 = mrpdu_frame(true, {Msg{1, 25, false,
                                       {Vec{false, 1, fv, {EV_NEW}, {}}}}});
    auto f = h.wait_frame(true, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 1, SID0, EV_NEW);
    });
    CHECK(f == exp1, "B: Talker Advertise New byte-exact");
    if (!f.empty() && f != exp1) { dump("got", f); dump("exp", exp1); }
    f = h.wait_frame(true, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 1, SID0, EV_NEW);
    });
    CHECK(!f.empty(), "B: second tick repeats New (AN row)");
    f = h.wait_frame(true, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 1, SID0, EV_JOINMT);
    });
    CHECK(!f.empty(), "B: third tick JoinMt (AA row)");
    // MVRP: the talker's VID joins the membership -> VID 2 New, byte-exact
    auto expv = mrpdu_frame(false, {Msg{1, 2, false,
                                        {Vec{false, 1, fv_vid(2),
                                             {EV_NEW}, {}}}}});
    auto g = h.wait_frame(false, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, false, 1, 2, EV_NEW);
    });
    CHECK(g == expv, "B: MVRP VID 2 New byte-exact");
    if (!g.empty() && g != expv) { dump("got", g); dump("exp", expv); }
    CHECK(d->dbg_vid_active_o != 0, "B: a VID membership is live");
  }

  // ==== C. over-ceiling refusal -> Talker Failed code 1 on the wire =======
  void check_over_ceiling_refusal_is_talker_failed() {
    h.sync();
    // src 1 fits alone but pushes Σ over the 75 % ceiling
    auto r = h.op(OP_DECL_TK, 1, SID1, DA1, 2, 100, 1);
    CHECK(r.got && r.status == ST_OK, "C: DECLARE_TALKER src 1 OK");
    mdl.req[1] = true; mdl.mfs[1] = 100; mdl.mif[1] = 1; mdl.walk();
    CHECK(!mdl.grant[1] && mdl.over, "C: model refuses src 1");
    h.idle(400);                        // optimistic window + rounds
    CHECK((d->sr_admitted_o & 2) == 0, "C: src 1 refused");
    CHECK(h.granted(1) == 0, "C: granted slope 0 while refused");
    CHECK(d->over_limit_o == 1, "C: over_limit view");
    CHECK(d->sum_slope_bps_o == mdl.sum, "C: sum excludes the refused");
    CHECK(h.tk_decl(1) == 2, "C: tk_decl_state FAILED");
    CHECK(h.src_fcode(1) == 1, "C: msrp_fail_code 1");
    CHECK(h.src_bridge(1) == OWN_MAC, "C: system id = own MAC");
    auto fvf = fv_failed(SID1, DA1, 2, 100, 1, 3, 1, ACC_LAT, OWN_MAC, 1);
    auto expf = mrpdu_frame(true, {Msg{2, 34, false,
                                       {Vec{false, 1, fvf, {EV_NEW}, {}}}}});
    auto f = h.wait_frame(true, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 2, SID1, EV_NEW);
    });
    CHECK(f == expf, "C: Talker Failed code 1 byte-exact");
    if (!f.empty() && f != expf) { dump("got", f); dump("exp", expf); }
  }

  // ==== C2. capacity frees -> refused source admitted, swaps back =========
  void check_freed_capacity_admits_the_refused_source() {
    auto r = h.op(OP_WDRW_TK, 0);
    CHECK(r.got && r.status == ST_OK, "C2: WITHDRAW_TALKER src 0 OK");
    mdl.req[0] = false; mdl.walk();
    CHECK(mdl.grant[1], "C2: model admits src 1 after the free");
    h.idle(400);
    CHECK((d->sr_admitted_o & 2) == 2, "C2: src 1 admitted");
    CHECK(h.granted(1) == mdl.granted[1], "C2: granted slope vs model");
    CHECK(d->over_limit_o == 0, "C2: over_limit clears");
    CHECK(h.tk_decl(1) == 1, "C2: src 1 back to ADVERTISE");
    CHECK(h.src_fcode(1) == 0, "C2: fail code cleared");
    // wire: src 0 withdraws (Lv of the Advertise) and src 1 re-declares
    // Advertise (New), replacing the Failed in place
    auto f = h.wait_frame(true, 1600, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 1, SID0, EV_LV);
    });
    CHECK(!f.empty(), "C2: Lv of the withdrawn Advertise on the wire");
    bool saw_new1 = !f.empty() && frame_has(f, true, 1, SID1, EV_NEW);
    if (!saw_new1) {
      auto f2 = h.wait_frame(true, 1600, [&](const std::vector<uint8_t>& fr) {
        return frame_has(fr, true, 1, SID1, EV_NEW);
      });
      saw_new1 = !f2.empty();
    }
    CHECK(saw_new1, "C2: Advertise New replaces the Failed in place");
    h.sync();
    CHECK(h.tk_decl(0) == 0, "C2: src 0 declaration gone");
  }

  // ==== D. listener end-to-end: RX registration -> Ready declaration ======
  void check_listener_registration_becomes_a_ready_declaration() {
    auto r = h.op(OP_DECL_LS, 0, SIDX, DAX, 2, 0, 0, DECL_READY);
    CHECK(r.got && r.status == ST_OK, "D: DECLARE_LISTENER sink 0 OK");
    h.sync();
    int reg_before = h.reg_cnt[0];
    // peer talker declares: Talker Advertise JoinIn for the settled triple
    Msg adv{1, 25, false, {Vec{false, 1,
            fv_talker(SIDX, DAX, 2, 0x0100, 1, 3, 1, 0x00012345),
            {EV_JOININ}, {}}}};
    h.feed(mrpdu_body(true, {adv}), true);
    h.idle(10);
    CHECK(h.reg_cnt[0] == reg_before + 1, "D: TK_ATTR_REGISTERED fired once");
    CHECK(h.tk_reg(0) == 1, "D: tk_reg_state ADVERTISE");
    CHECK(h.acclat(0) == 0x00012345, "D: acc_latency latched");
    CHECK(h.ls_decl(0) == 2, "D: Listener READY declared (class-D)");
    // wire: Listener attribute New with FourPacked Ready, byte-exact
    Msg lsn{3, 8, true, {Vec{false, 1, fv_sid(SIDX),
                             {EV_NEW}, {DECL_READY}}}};
    auto expl = mrpdu_frame(true, {lsn});
    auto f = h.wait_frame(true, 800, [&](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 3, SIDX, EV_NEW);
    });
    CHECK(f == expl, "D: Listener Ready New byte-exact");
    if (!f.empty() && f != expl) { dump("got", f); dump("exp", expl); }
    h.sync();

    // in-place Advertise -> Failed swap: strobe, latch, AskingFailed
    reg_before = h.reg_cnt[0];
    int unreg_before = h.unreg_cnt[0];
    Msg fail{2, 34, false, {Vec{false, 1,
             fv_failed(SIDX, DAX, 2, 0x0100, 1, 3, 1, 0x00012345,
                       0xBBBBCCCCDDDDULL, 7),
             {EV_JOININ}, {}}}};
    h.feed(mrpdu_body(true, {fail}), true);
    h.idle(10);
    CHECK(h.reg_cnt[0] == reg_before + 1, "D: swap fires REGISTERED");
    CHECK(h.unreg_cnt[0] == unreg_before, "D: swap fires NO unregister");
    CHECK(h.tk_reg(0) == 2, "D: tk_reg_state FAILED");
    CHECK(h.snk_fcode(0) == 7, "D: sink failure code latched");
    CHECK(h.snk_bridge(0) == 0xBBBBCCCCDDDDULL, "D: sink system id latched");
    CHECK(h.ls_decl(0) == 1, "D: declaration follows to ASKING_FAILED");
    // and back: Advertise re-registers in place, clears the failure
    h.feed(mrpdu_body(true, {adv}), true);
    h.idle(10);
    CHECK(h.tk_reg(0) == 1, "D: swap back to ADVERTISE");
    CHECK(h.snk_fcode(0) == 0, "D: failure gated off");
    CHECK(h.ls_decl(0) == 2, "D: declaration back to READY");
    h.run_ms(800);   // let the re-declaration ladder finish its ticks
  }

  // ==== E. certified two-class Domain arrival adopts + re-declares ========
  void check_certified_domain_arrival_adopts_and_redeclares() {
    h.sync();
    int chg_before = h.domchg;
    // FirstValue {5, 2, VID 5}, NumberOfValues 2 — class A is value 1
    Msg dom{4, 4, false, {Vec{false, 2, fv_domain(5, 2, 5),
                              {EV_JOININ, EV_JOININ}, {}}}};
    h.feed(mrpdu_body(true, {dom}), true);
    h.idle(10);
    CHECK(h.domchg == chg_before + 1, "E: DOMAIN_CHANGE fired");
    CHECK(d->class_a_prio_o == 3 && d->class_a_vid_o == 5,
          "E: adopted {prio 3, vid 5}");
    CHECK(d->domain_adopted_o == 1, "E: ADOPTED state");
    auto r = h.op(OP_GET_DOM, 6);
    CHECK(r.got && r.status == ST_OK && (r.data & 0xFFF) == 5,
          "E: GET_DOMAIN reports the adopted VID");
    // wire: one Domain message, two vectors — Lv {6,3,2} then New {6,3,5}
    Msg re{4, 4, false, {Vec{false, 1, fv_domain(6, 3, 2), {EV_LV}, {}},
                         Vec{false, 1, fv_domain(6, 3, 5), {EV_NEW}, {}}}};
    auto expd = mrpdu_frame(true, {re});
    auto f = h.wait_frame(true, 800, [](const std::vector<uint8_t>& fr) {
      return frame_has(fr, true, 4, 6, EV_LV);
    });
    CHECK(f == expd, "E: Domain Lv+New re-declaration byte-exact");
    if (!f.empty() && f != expd) { dump("got", f); dump("exp", expd); }
  }

  // ==== F1. own MSRP LeaveAll end-to-end ==================================
  void check_own_msrp_leaveall_cycle() {
    // wait for the PRNG-drawn leavealltimer (10-15 s from arming)
    auto laf = h.wait_frame(true, 16000, [](const std::vector<uint8_t>& fr) {
      auto p = parse_frame(fr);
      return !p.vecs.empty() && p.vecs.front().la;
    });
    CHECK(!laf.empty(), "F1: MSRP LeaveAllEvent PDU within 16 s");
    // gather the LA PDU + trailing re-joins; the union must re-declare
    std::vector<PFrame> got{parse_frame(laf)};
    for (int i = 0; i < 3; i++) {
      auto f = h.wait_any(true, 400);
      if (f.empty()) break;
      got.push_back(parse_frame(f));
    }
    bool dom_rejoin = false;
    bool ls_rejoin = false;
    for (auto& p : got) {
      for (auto& v : p.vecs) {
        if (v.type == 4 && v.fv.size() == 4 && v.fv[0] == 6
            && !v.ev.empty() && v.ev[0] == EV_JOININ) dom_rejoin = true;
        if (v.type == 3 && fv_u64(v.fv, 0, 8) == SIDX
            && !v.fp.empty() && v.fp[0] == DECL_READY) ls_rejoin = true;
      }
    }
    CHECK(dom_rejoin, "F1: Domain JoinIn rides the LeaveAll cycle");
    CHECK(ls_rejoin, "F1: Listener Ready re-joins the LeaveAll cycle");
    // registration stays published through LV; a peer re-join keeps it IN
    CHECK(h.tk_reg(0) == 1, "F1: registration published through LV");
    int unreg_before = h.unreg_cnt[0];
    Msg adv{1, 25, false, {Vec{false, 1,
            fv_talker(SIDX, DAX, 2, 0x0100, 1, 3, 1, 0x00012345),
            {EV_JOININ}, {}}}};
    h.feed(mrpdu_body(true, {adv}), true);
    h.run_ms(200);
    CHECK(h.unreg_cnt[0] == unreg_before,
          "F1: re-confirmed attribute never unregisters");
    CHECK(h.tk_reg(0) == 1, "F1: still ADVERTISE after the cycle");
  }

  // ==== F2. received MSRP LeaveAll ages to expiry, per application ========
  void check_received_msrp_leaveall_ages_to_expiry() {
    h.sync();
    int unreg_before = h.unreg_cnt[0];
    auto vids_before = d->dbg_vid_active_o;
    // LeaveAllEvent on a Domain JoinIn vector matching the operating Domain
    Msg dom{4, 4, false, {Vec{true, 1, fv_domain(6, 3, 5),
                              {EV_JOININ}, {}}}};
    h.feed(mrpdu_body(true, {dom}), true);
    h.idle(10);
    CHECK(h.unreg_cnt[0] == unreg_before, "F2: no unregister at the frame");
    CHECK(d->dbg_vid_active_o == vids_before,
          "F2: MSRP LeaveAll never touches MVRP membership");
    // no re-declaration from the peer: T-MRP-LEAVE (5 s) ages LV -> MT
    h.run_ms(5400);
    CHECK(h.unreg_cnt[0] == unreg_before + 1,
          "F2: TK_ATTR_UNREGISTERED after T-MRP-LEAVE");
    CHECK(h.tk_reg(0) == 0, "F2: registration gone");
    CHECK(h.ls_decl(0) == 0, "F2: Listener declaration withdrawn");
    // the withdrawal reaches the wire as a Listener Lv
    bool saw_lv = false;
    for (auto& fr : h.archive) {
      if (frame_has(fr, true, 3, SIDX, EV_LV)) saw_lv = true;
    }
    CHECK(saw_lv, "F2: Listener Lv on the wire");
  }

  // ==== F3. the MVRP LeaveAll cycle is its own participant ================
  void check_mvrp_leaveall_is_its_own_participant() {
    // own MVRP LeaveAll must have fired by now (>= 16 s elapsed): its PDU
    // carries the LA flag and re-joins every held VID; MSRP attributes
    // cannot appear in it by construction (separate application)
    bool saw_mvrp_la = false;
    bool vid_rejoin = false;
    bool mvrp_lv = false;
    for (auto& f : h.archive) {
      auto p = parse_frame(f);
      if (p.msrp || p.vecs.empty()) continue;
      if (p.vecs.front().la) {
        saw_mvrp_la = true;
        for (auto& v : p.vecs)
          if (v.fv.size() == 2 && fv_u64(v.fv, 0, 2) == 2
              && !v.ev.empty() && v.ev[0] == EV_JOININ) vid_rejoin = true;
      }
      for (auto& v : p.vecs)
        if (!v.ev.empty() && v.ev[0] == EV_LV) mvrp_lv = true;
    }
    CHECK(saw_mvrp_la, "F3: own MVRP LeaveAll PDU seen");
    CHECK(vid_rejoin, "F3: held VID re-joined in the MVRP cycle");
    CHECK(!mvrp_lv, "F3: no spurious MVRP Lv (membership never flapped)");
    CHECK(d->dbg_vid_active_o != 0, "F3: membership still live");
    CHECK(h.malformed == 0, "F3: no PDU we fed was tolerance-discarded");
  }

  // ==== F4. peer LeaveAll cadence stays bounded (milan-fpga #75) ==========
  void check_peer_leaveall_cadence_stays_bounded() {
    h.sync();
    // The bench measured ~11 MSRP PDUs per second sustained after a
    // reconnect: the retired lwSRP engine answered EVERY received
    // LeaveAll with an immediate re-declaration and the peer's next
    // cycle echoed it back. A correct applicant answers rLA! by falling
    // to VP and re-declaring once, join-paced, per cycle. Six peer
    // LeaveAll cycles, each ridden on the bridge's own re-advertise
    // (the shape a real switch emits), must produce a bounded and
    // non-growing exchange - and every cycle must re-declare Ready.
    int total = 0;
    int ready_cycles = 0;
    int worst_cycle = 0;
    for (int k = 0; k < 6; k++) {
      Msg la{1, 25, false, {Vec{true, 1,
              fv_talker(SIDX, DAX, 2, 0x0100, 1, 3, 1, 0x00012345),
              {EV_JOININ}, {}}}};
      h.feed(mrpdu_body(true, {la}), true);
      bool ready = false;
      int cnt = 0;
      // ~0.9-0.95 s per cycle (20 polls, minus feed/parse overhead). The
      // 18/4 pins include the PRNG-scheduled own-LeaveAll burst landing
      // in cycle 4; an upstream timing edit that moves that burst across
      // a cycle boundary legitimately re-measures these two pins.
      for (int slice = 0; slice < 20; slice++) {
        auto f = h.wait_any(true, 50);
        if (f.empty()) continue;
        cnt++;
        auto p = parse_frame(f);
        for (auto& v : p.vecs)
          if (v.type == 3 && fv_u64(v.fv, 0, 8) == SIDX
              && !v.fp.empty() && v.fp[0] == DECL_READY) ready = true;
      }
      total += cnt;
      if (cnt > worst_cycle) worst_cycle = cnt;
      if (ready) ready_cycles++;
    }
    CHECK(total <= 18, "F4: six LeaveAll cycles emit a bounded exchange");
    CHECK(worst_cycle <= 4, "F4: no single cycle approaches the 11-PDU storm");
    CHECK(ready_cycles == 6, "F4: every cycle re-declares Listener Ready");
    CHECK(h.tk_reg(0) == 1, "F4: talker registration survives the cadence");
    CHECK(h.malformed == 0, "F4: no PDU we fed was tolerance-discarded");
  }

  // ==== G. admission sweep vs the independent Σ-slope model ===============
  void check_admission_sweep_matches_the_model() {
    // deterministic xorshift so the sweep is reproducible
    uint32_t rng = 0xC0FFEE01u;
    auto rnd = [&rng]() {
      rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng;
    };
    for (int iter = 0; iter < 30; iter++) {
      int s = rnd() % 8;
      if (mdl.req[s] && (rnd() & 1)) {
        auto r = h.op(OP_WDRW_TK, s);
        CHECK(r.got && r.status == ST_OK, "G%d: withdraw OK", iter);
        mdl.req[s] = false;
      } else {
        uint32_t mfs = rnd() % 2000;
        uint32_t mif = 1 + (rnd() % 4);
        auto r = h.op(OP_DECL_TK, s, (OWN_MAC << 16) | (0x100 + s),
                      0x91E0F0000000ULL + (static_cast<uint64_t>(s) << 8), 5,
                      mfs, mif);
        CHECK(r.got && r.status == ST_OK, "G%d: declare OK", iter);
        mdl.req[s] = true; mdl.mfs[s] = mfs; mdl.mif[s] = mif;
      }
      mdl.walk();
      h.idle(400);                      // optimistic window + rounds settle
      uint8_t exp_adm = 0;
      bool slopes_ok = true;
      for (int k = 0; k < 8; k++) {
        if (mdl.grant[k]) exp_adm |= (1 << k);
        if (h.granted(k) != mdl.granted[k]) slopes_ok = false;
      }
      CHECK(d->sr_admitted_o == exp_adm,
            "G%d: admitted vector 0x%02x vs model 0x%02x", iter,
            d->sr_admitted_o, exp_adm);
      CHECK(slopes_ok, "G%d: granted slopes match the model", iter);
      CHECK(d->over_limit_o == (mdl.over ? 1 : 0), "G%d: over_limit", iter);
      CHECK(d->sum_slope_bps_o == mdl.sum,
            "G%d: sum %u vs model %llu", iter, d->sum_slope_bps_o,
            static_cast<unsigned long long>(mdl.sum));
    }
  }

  const milan::tb::Model<Vsrp_top_wrap> model;
  Vsrp_top_wrap* const d;
  H h;
  AdmModel mdl;          // the independent Σ-slope model B/C/C2/G all walk
  int checks = 0;
  int fails = 0;
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SrpTopHarness harness;
  return harness.run();
}

// SPDX-License-Identifier: CERN-OHL-W-2.0
// srp_stream_fsms suite — independent expectations, never DUT logic.
//
// Walks BOTH stream-FSM modules' applicants through an independently
// transcribed IEEE 802.1Q-2018 Table 10-3 (all rx events x all 12 states x
// both operPointToPointMAC arms, plus every tx!/txLA! row with its message),
// the Table 10-4 registrar with the Milan Δ13 deviation (rLv = immediate
// IN->MT, LeaveAll cycle = the only LV path, aged by T-MRP-LEAVE), the
// F10.4 talker declare/Ready/ACTIVE/admission-failure walk, the F10.5
// listener match / in-place swap / unregister walks, per-application
// LeaveAll isolation, the acc_latency latch and the VLAN user handshakes.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Vsrp_stream_fsms_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---------------------------------------------------------------------------
// Independent transcription of IEEE 802.1Q-2018 Table 10-3 (applicant).
// States (columns), events (rows). H = no transition ("--" cell).
// ---------------------------------------------------------------------------
// Applicant states, in Table 10-3 column order. Plain integers: they index
// APP_TBL, SN and the DUT's packed t_dbg_app_state_o nibbles.
constexpr int VO = 0;
constexpr int VP = 1;
constexpr int VN = 2;
constexpr int AN = 3;
constexpr int AA = 4;
constexpr int QA = 5;
constexpr int LA = 6;
constexpr int AO = 7;
constexpr int QO = 8;
constexpr int AP = 9;
constexpr int QP = 10;
constexpr int LO = 11;
constexpr int NSTATES = 12;
// Applicant events, in Table 10-3 row order. eRNew..eRLA are ordered so that
// eRNew + <srp attribute-event code> names the received event.
constexpr int eNew = 0;
constexpr int eJoin = 1;
constexpr int eLv = 2;
constexpr int eRNew = 3;
constexpr int eRJoinIn = 4;
constexpr int eRIn = 5;
constexpr int eRJoinMt = 6;
constexpr int eRMt = 7;
constexpr int eRLv = 8;
constexpr int eRLA = 9;
constexpr int ePer = 10;
constexpr int eTx = 11;
constexpr int eTxLA = 12;
constexpr int NEVENTS = 13;
constexpr int H = -1;
constexpr int APP_TBL[NEVENTS][NSTATES] = {
  //            VO  VP  VN  AN  AA  QA  LA  AO  QO  AP  QP  LO
  /*New!    */ {VN, VN,  H,  H, VN, VN, VN, VN, VN, VN, VN, VN},
  /*Join!   */ {VP,  H,  H,  H,  H,  H, AA, AP, QP,  H,  H, VP},
  /*Lv!     */ { H, VO, LA, LA, LA, LA,  H,  H,  H, AO, QO,  H},
  /*rNew!   */ { H,  H,  H,  H,  H,  H,  H,  H,  H,  H,  H,  H},
  /*rJoinIn!*/ {AO, AP,  H,  H, QA,  H,  H, QO,  H, QP,  H,  H}, // notes 4
  /*rIn!    */ { H,  H,  H,  H, QA,  H,  H,  H,  H,  H,  H,  H}, // note 5
  /*rJoinMt!|rMt!*/
               { H,  H,  H,  H,  H, AA,  H,  H, AO,  H, AP, VO},
  /*rMt! (same row)*/
               { H,  H,  H,  H,  H, AA,  H,  H, AO,  H, AP, VO},
  /*rLv!|rLA!*/{LO,  H,  H, VN, VP, VP,  H, LO, LO, VP, VP,  H},
  /*rLA! (same row)*/
               {LO,  H,  H, VN, VP, VP,  H, LO, LO, VP, VP,  H},
  /*periodic!*/{ H,  H,  H,  H,  H, AA,  H,  H,  H,  H, AP,  H},
  /*tx!     */ { H, AA, AN, AA, QA,  H, VO,  H,  H, QA,  H, VO}, // AN: note 8
  /*txLA!   */ {LO, AA, AN, QA, QA,  H, LO, LO, LO, QA, QA,  H},
};

static int app_next(int st, int ev, bool reg_in, bool p2p) {
  if (ev == eRJoinIn && p2p && (st == VO || st == VP)) return st; // note 4
  if (ev == eRIn) return (p2p && st == AA) ? QA : st;             // note 5
  if (ev == eTx && st == AN) return reg_in ? QA : AA;             // note 8
  int nx = APP_TBL[ev][st];
  return (nx == H) ? st : nx;
}

// message sent at a tx opportunity: srp attribute-event code, or -1.
// sN=New(0), sJ=JoinIn(1)/JoinMt(3) by reg_in, sL=Lv(5), s=In(2)/Mt(4).
// Optional [s]/[sJ]/[sL] encodings are never sent by the DUT (banner).
static int app_msg(int st, bool txla, bool reg_in) {
  const int sj = reg_in ? 1 : 3;
  const int se = reg_in ? 2 : 4;
  if (!txla) {
    switch (st) {
      case VP: case AA: case AP: return sj;
      case VN: case AN:          return 0;
      case LA:                   return 5;
      case LO:                   return se;
      default:                   return -1;
    }
  }
  switch (st) {
    case VP:                            return se;
    case VN: case AN:                   return 0;
    case AA: case QA: case AP: case QP: return sj;
    default:                            return -1;
  }
}

constexpr const char* SN[NSTATES] =
  {"VO","VP","VN","AN","AA","QA","LA","AO","QO","AP","QP","LO"};
constexpr const char* EN[NEVENTS] =
  {"New!","Join!","Lv!","rNew!","rJoinIn!","rIn!","rJoinMt!","rMt!","rLv!",
   "rLA!","periodic!","tx!","txLA!"};

// ---------------------------------------------------------------------------
// harness
// ---------------------------------------------------------------------------
constexpr uint64_t MAC  = 0x02AABBCCDDEEull;
constexpr uint32_t NOW  = 100000;
constexpr uint32_t LEAVE_MS = 5000;

// N_STREAMS_P of the wrapper: every per-slot capture array is this wide.
constexpr int kStreams = 8;
// The MRPDU FirstValue busses are 272 bits, i.e. 34 bytes, wide.
constexpr int kFirstValueBytes = 34;
constexpr int kFirstValueMsb = 271;
// Guard on the wait for both modules to report a completed transmit
// opportunity: far more clock steps than a txop needs, never reached in a
// passing run.
constexpr int kTxopPollSteps = 300;

struct Push {
  uint8_t type;
  uint8_t code;
  uint8_t fp;
  uint8_t val[kFirstValueBytes];
};
struct Arm  { bool cancel; uint8_t slot; uint8_t owner; uint32_t deadline; };
struct VOp  { bool join; uint16_t vid; };

template <std::size_t N>
static uint64_t wget(const VlWide<N>& w, int lo, int width) {
  uint64_t v = 0;
  for (int i = width - 1; i >= 0; --i) {
    int b = lo + i;
    v = (v << 1) | ((w[b >> 5] >> (b & 31)) & 1u);
  }
  return v;
}

struct Hn {
  Vsrp_stream_fsms_wrap* d;
  std::vector<Push> t_push;
  std::vector<Push> l_push;
  std::vector<Arm>  t_arm;
  std::vector<Arm>  l_arm;
  std::vector<VOp>  t_vop;
  std::vector<VOp>  l_vop;
  int t_chg[kStreams] = {0};
  int l_reg[kStreams] = {0};
  int l_unreg[kStreams] = {0};
  bool t_uready = true;
  bool l_uready = true;

  explicit Hn(Vsrp_stream_fsms_wrap* dd) : d(dd) {}

  void clear_logs() {
    t_push.clear(); l_push.clear(); t_arm.clear(); l_arm.clear();
    t_vop.clear(); l_vop.clear();
    memset(t_chg, 0, sizeof t_chg);
    memset(l_reg, 0, sizeof l_reg);
    memset(l_unreg, 0, sizeof l_unreg);
  }

  void step() {
    d->now_ms_i = NOW;
    d->t_ev_ready_i = 1; d->l_ev_ready_i = 1;
    d->t_user_ready_i = t_uready; d->l_user_ready_i = l_uready;
    d->clk_i = 0; d->eval();
    // harvest (all DUT outputs are registered or stable-from-registers)
    if (d->t_ev_valid_o) {
      Push p;
      p.type = d->t_ev_attr_type_o;
      p.code = d->t_ev_event_o;
      p.fp = d->t_ev_fourpack_o;
      for (int i = 0; i < kFirstValueBytes; ++i)
        p.val[i] = static_cast<uint8_t>(
            wget(d->t_ev_value_o, kFirstValueMsb - 8 * i - 7, 8));
      t_push.push_back(p);
    }
    if (d->l_ev_valid_o) {
      Push p;
      p.type = d->l_ev_attr_type_o;
      p.code = d->l_ev_event_o;
      p.fp = d->l_ev_fourpack_o;
      for (int i = 0; i < kFirstValueBytes; ++i)
        p.val[i] = static_cast<uint8_t>(
            wget(d->l_ev_value_o, kFirstValueMsb - 8 * i - 7, 8));
      l_push.push_back(p);
    }
    if (d->t_arm_valid_o)
      t_arm.push_back({static_cast<bool>(d->t_arm_cancel_o),
                       static_cast<uint8_t>(d->t_arm_slot_o),
                       static_cast<uint8_t>(d->t_arm_owner_o),
                       static_cast<uint32_t>(d->t_arm_deadline_ms_o)});
    if (d->l_arm_valid_o)
      l_arm.push_back({static_cast<bool>(d->l_arm_cancel_o),
                       static_cast<uint8_t>(d->l_arm_slot_o),
                       static_cast<uint8_t>(d->l_arm_owner_o),
                       static_cast<uint32_t>(d->l_arm_deadline_ms_o)});
    if (d->t_user_valid_o && t_uready)
      t_vop.push_back({static_cast<bool>(d->t_user_join_o),
                       static_cast<uint16_t>(d->t_user_vid_o)});
    if (d->l_user_valid_o && l_uready)
      l_vop.push_back({static_cast<bool>(d->l_user_join_o),
                       static_cast<uint16_t>(d->l_user_vid_o)});
    for (int s = 0; s < kStreams; ++s) {
      if ((d->t_lstn_reg_change_o >> s) & 1) ++t_chg[s];
      if ((d->l_evt_tk_registered_o >> s) & 1) ++l_reg[s];
      if ((d->l_evt_tk_unregistered_o >> s) & 1) ++l_unreg[s];
    }
    d->clk_i = 1; d->eval();
    // one-shot inputs auto-clear
    d->evt_valid_i = 0; d->join_tick_i = 0; d->periodic_tick_i = 0;
    d->leaveall_rx_i = 0; d->leaveall_own_i = 0; d->exp_valid_i = 0;
    d->gate_valid_i = 0; d->ctl_valid_i = 0;
  }

  void idle(int n) { for (int i = 0; i < n; ++i) step(); }

  void reset() {
    d->rst_n = 0; d->p2p_i = 1; d->own_mac_i = MAC;
    d->sr_admitted_i = 0xFF;
    d->evt_valid_i = 0; d->join_tick_i = 0; d->periodic_tick_i = 0;
    d->leaveall_rx_i = 0; d->leaveall_own_i = 0; d->exp_valid_i = 0;
    d->gate_valid_i = 0; d->ctl_valid_i = 0; d->exp_slot_i = 0;
    t_uready = true; l_uready = true;
    idle(3);
    d->rst_n = 1;
    idle(2);
    clear_logs();
  }

  void gate(bool open, int src, uint64_t sid, uint64_t da, uint16_t vid,
            uint32_t lat = 500) {
    d->gate_valid_i = 1; d->gate_open_i = open; d->gate_src_i = src;
    d->gate_stream_id_i = sid; d->gate_da_i = da; d->gate_vid_i = vid;
    d->gate_max_frame_i = 217; d->gate_max_interval_i = 1;
    d->gate_prio_i = 3; d->gate_rank_i = 1; d->gate_acc_lat_i = lat;
    step(); idle(2);
  }

  void ctl(bool settle, int sink, uint64_t sid, uint64_t da, uint16_t vid) {
    d->ctl_valid_i = 1; d->ctl_settle_i = settle; d->ctl_sink_i = sink;
    d->ctl_stream_id_i = sid; d->ctl_da_i = da; d->ctl_vid_i = vid;
    step(); idle(2);
  }

  void inject(bool msrp, uint8_t type, uint64_t sid, uint64_t da,
              uint16_t vid, uint8_t ev, uint8_t fp = 0, uint32_t lat = 0,
              uint64_t sysid = 0, uint8_t fcode = 0) {
    d->evt_valid_i = 1; d->evt_msrp_i = msrp; d->evt_attr_type_i = type;
    d->evt_stream_id_i = sid; d->evt_da_i = da; d->evt_vid_i = vid;
    d->evt_mrp_event_i = ev; d->evt_fourpacked_i = fp;
    d->evt_acc_latency_i = lat; d->evt_failure_system_id_i = sysid;
    d->evt_failure_code_i = fcode;
    step(); idle(3);
  }

  void la_rx()  { d->leaveall_rx_i = 1;  step(); idle(3); }
  void la_own() { d->leaveall_own_i = 1; step(); idle(2); }
  void expire(int slot) { d->exp_valid_i = 1; d->exp_slot_i = slot; step(); idle(2); }

  bool tick() {
    d->join_tick_i = 1; step();
    bool td = false;
    bool ld = false;
    for (int i = 0; i < kTxopPollSteps && !(td && ld); ++i) {
      td |= (d->t_txop_done_o != 0); ld |= (d->l_txop_done_o != 0);
      if (td && ld) break;
      step();
      td |= (d->t_txop_done_o != 0); ld |= (d->l_txop_done_o != 0);
    }
    idle(2);
    return td && ld;
  }

  void ptick() { d->periodic_tick_i = 1; step(); idle(2); }

  int t_app(int s) const { return (d->t_dbg_app_state_o >> (4 * s)) & 15; }
  int l_app(int s) const { return (d->l_dbg_app_state_o >> (4 * s)) & 15; }
  int t_reg(int s) const { return (d->t_dbg_reg_state_o >> (2 * s)) & 3; }
  int l_regst(int s) const { return (d->l_dbg_reg_state_o >> (2 * s)) & 3; }
  int t_lstn(int s) const { return (d->t_lstn_reg_state_o >> (2 * s)) & 3; }
  int t_decl(int s) const { return (d->t_tk_decl_state_o >> (2 * s)) & 3; }
  int l_tkreg(int s) const { return (d->l_tk_reg_state_o >> (2 * s)) & 3; }
  int l_decl(int s) const { return (d->l_lstn_decl_state_o >> (2 * s)) & 3; }
  uint32_t l_lat(int s) const {
    return static_cast<uint32_t>(wget(d->l_acc_latency_o, 32 * s, 32));
  }
  uint64_t l_fbridge(int s) const { return wget(d->l_msrp_fail_bridge_o, 64 * s, 64); }
  uint8_t  l_fcode(int s) const { return (d->l_msrp_fail_code_o >> (8 * s)) & 0xFF; }
  uint64_t t_fbridge(int s) const { return wget(d->t_msrp_fail_bridge_o, 64 * s, 64); }
  uint8_t  t_fcode(int s) const { return (d->t_msrp_fail_code_o >> (8 * s)) & 0xFF; }
};

// stream identities used by the recipes
constexpr uint64_t SID0 = 0x02AABBCCDDEE0001ull;
constexpr uint64_t DA0  = 0x91E0F0001234ull;
constexpr uint16_t VID0 = 2;

// applicant-recipe drivers: land source/sink 0 in state S, tracking the
// model alongside; each returns the model state for a final CHECK
static int t_goto(Hn& h, int S) {
  int m = VO;
  h.gate(true, 0, SID0, DA0, VID0);                 // New!
  m = app_next(m, eNew, false, true);
  auto closev = [&]() { h.gate(false, 0, SID0, DA0, VID0); m = app_next(m, eLv, false, true); };
  auto tickv  = [&]() { h.tick(); m = app_next(m, eTx, false, true); };
  auto rx     = [&](uint8_t code, bool p2p) {
    h.d->p2p_i = p2p;
    h.inject(true, 1, SID0, DA0, VID0, code);
    m = app_next(m, eRNew + code, false, p2p);
    h.d->p2p_i = 1;
  };
  switch (S) {
    case VN: break;
    case AN: tickv(); break;
    case AA: tickv(); tickv(); break;
    case QA: tickv(); tickv(); tickv(); break;
    case LA: tickv(); tickv(); closev(); break;
    case VO: closev(); tickv(); break;                       // LA --tx/sL--> VO
    case VP: closev(); tickv(); h.gate(true, 0, SID0, DA0, VID0);   // Join!
             m = app_next(m, eJoin, false, true); break;
    case AO: closev(); tickv(); rx(1, false); break;         // VO+rJoinIn(!p2p)
    case QO: closev(); tickv(); rx(1, false); rx(1, true); break;
    case AP: closev(); tickv(); h.gate(true, 0, SID0, DA0, VID0);
             m = app_next(m, eJoin, false, true);
             rx(1, false); break;                            // VP+rJoinIn(!p2p)
    case QP: closev(); tickv(); h.gate(true, 0, SID0, DA0, VID0);
             m = app_next(m, eJoin, false, true);
             rx(1, false); rx(1, true); break;
    case LO: closev(); tickv(); rx(5, true); break;          // VO+rLv
    default: break;
  }
  return m;
}

static int l_goto(Hn& h, int S) {
  int m = VO;
  h.ctl(true, 0, SID0, DA0, VID0);                  // A15: armed, app VO
  auto adv = [&]() {                                // registrar -> New!
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    m = app_next(m, eNew, false, true);
  };
  auto tickv = [&]() { h.tick(); m = app_next(m, eTx, false, true); };
  auto rxl   = [&](uint8_t code, bool p2p) {        // Listener-type rx
    h.d->p2p_i = p2p;
    h.inject(true, 3, SID0, 0, 0, code, 2);
    m = app_next(m, eRNew + code, false, p2p);
    h.d->p2p_i = 1;
  };
  switch (S) {
    case VO: break;
    case VN: adv(); break;
    case AN: adv(); tickv(); break;
    case AA: adv(); tickv(); tickv(); break;
    case QA: adv(); tickv(); tickv(); tickv(); break;
    case LA: adv(); tickv(); tickv();
             h.ctl(false, 0, SID0, DA0, VID0);      // A8: Lv!
             m = app_next(m, eLv, false, true); break;
    case VP: adv(); tickv(); tickv(); h.la_rx();    // AA+rLA -> VP
             m = app_next(m, eRLA, false, true); break;
    case AO: rxl(1, false); break;
    case QO: rxl(1, false); rxl(1, true); break;
    case AP: adv(); tickv(); tickv(); h.la_rx();
             m = app_next(m, eRLA, false, true);
             rxl(1, false); break;                  // VP+rJoinIn(!p2p)
    case QP: adv(); tickv(); tickv(); h.la_rx();
             m = app_next(m, eRLA, false, true);
             rxl(1, false); rxl(1, true); break;
    case LO: rxl(5, true); break;
    default: break;
  }
  return m;
}

namespace {

//! The whole suite: one DUT, one BFM, one tally, one recipe walk per section.
class SrpStreamFsmsSuite {
 public:
  int run();

 private:
  void rx_events_match_table_10_3();
  void talker_tx_rows_send_the_table_10_3_message();
  void listener_tx_rows_send_the_table_10_3_message();
  void talker_registrar_follows_table_10_4_with_delta13();
  void talker_declaration_tracks_ready_and_admission();
  void listener_matcher_registers_swaps_and_unregisters();
  void vlan_user_handshake_holds_and_collapses();
  void talker_tracker_isolates_applications();

  const milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  Vsrp_stream_fsms_wrap* const d = model.get();
  int checks = 0;
  int fails = 0;
  Hn h{d};
};

// ==== A. Table 10-3 walk: all rx events x all 12 states x both p2p arms,
//         through BOTH modules (one attribute each) =======================
void SrpStreamFsmsSuite::rx_events_match_table_10_3() {
  constexpr int rxevs[7] = {
      eRNew, eRJoinIn, eRIn, eRJoinMt, eRMt, eRLv, eRLA};
  for (int p2p = 1; p2p >= 0; --p2p) {
    for (int S = 0; S < NSTATES; ++S) {
      for (int k = 0; k < 7; ++k) {
        const int ev = rxevs[k];
        // talker applicant (Talker Advertise attribute)
        h.reset();
        int m = t_goto(h, S);
        CHECK(h.t_app(0) == m && m == S, "T recipe %s: dut %s model %s",
              SN[S], SN[h.t_app(0)], SN[m]);
        d->p2p_i = p2p;
        if (ev == eRLA) h.la_rx();
        else h.inject(true, 1, SID0, DA0, VID0,
                      static_cast<uint8_t>(ev - eRNew));
        int exp = app_next(S, ev, false, p2p);
        CHECK(h.t_app(0) == exp, "T %s x %s p2p=%d: dut %s want %s",
              SN[S], EN[ev], p2p, SN[h.t_app(0)], SN[exp]);
        // listener applicant (Listener attribute)
        h.reset();
        m = l_goto(h, S);
        CHECK(h.l_app(0) == m && m == S, "L recipe %s: dut %s model %s",
              SN[S], SN[h.l_app(0)], SN[m]);
        d->p2p_i = p2p;
        if (ev == eRLA) h.la_rx();
        else h.inject(true, 3, SID0, 0, 0,
                      static_cast<uint8_t>(ev - eRNew), 2);
        exp = app_next(S, ev, false, p2p);
        CHECK(h.l_app(0) == exp, "L %s x %s p2p=%d: dut %s want %s",
              SN[S], EN[ev], p2p, SN[h.l_app(0)], SN[exp]);
      }
    }
  }
}

// ==== B. tx! / txLA! rows: transition + exact message, talker ===========
void SrpStreamFsmsSuite::talker_tx_rows_send_the_table_10_3_message() {
  for (int txla = 0; txla <= 1; ++txla) {
    for (int S = 0; S < NSTATES; ++S) {
      h.reset();
      (void)t_goto(h, S);
      if (txla) h.la_own();
      h.clear_logs();
      CHECK(h.tick(), "T tx walk %s txla=%d completes", SN[S], txla);
      int exp = app_next(S, txla ? eTxLA : eTx, false, true);
      CHECK(h.t_app(0) == exp, "T %s x %s: dut %s want %s",
            SN[S], txla ? "txLA!" : "tx!", SN[h.t_app(0)], SN[exp]);
      int msg = app_msg(S, txla, false);
      if (msg < 0) {
        CHECK(h.t_push.empty(), "T %s txla=%d: no message, got %zu",
              SN[S], txla, h.t_push.size());
      } else {
        CHECK(h.t_push.size() == 1 && h.t_push[0].code == msg,
              "T %s txla=%d: one msg code %d", SN[S], txla, msg);
        if (h.t_push.size() == 1) {
          const Push& p = h.t_push[0];
          CHECK(p.type == 1, "T %s: Talker Advertise type, got %u", SN[S], p.type);
          uint64_t sid = 0;
          uint64_t da = 0;
          for (int i = 0; i < 8; ++i) sid = (sid << 8) | p.val[i];
          for (int i = 8; i < 14; ++i) da = (da << 8) | p.val[i];
          CHECK(sid == SID0 && da == DA0, "T %s FirstValue stream_id/DA", SN[S]);
          CHECK(p.val[14] == 0 && p.val[15] == VID0, "T %s FirstValue VLAN", SN[S]);
          CHECK(p.val[16] == 0 && p.val[17] == 217, "T %s MaxFrameSize", SN[S]);
          CHECK(p.val[18] == 0 && p.val[19] == 1, "T %s MaxIntervalFrames", SN[S]);
          CHECK(p.val[20] == ((3 << 5) | (1 << 4)), "T %s prio/rank byte", SN[S]);
        }
      }
    }
  }
}

// ==== B2. tx! / txLA! rows on the listener (Listener attribute) =========
void SrpStreamFsmsSuite::listener_tx_rows_send_the_table_10_3_message() {
  for (int txla = 0; txla <= 1; ++txla) {
    for (int S = 0; S < NSTATES; ++S) {
      h.reset();
      (void)l_goto(h, S);
      // fourpack declared by the recipe: READY iff the recipe declared
      const bool declared = !(S == VO || S == AO || S == QO || S == LO);
      if (txla) h.la_own();
      h.clear_logs();
      CHECK(h.tick(), "L tx walk %s txla=%d completes", SN[S], txla);
      int exp = app_next(S, txla ? eTxLA : eTx, false, true);
      CHECK(h.l_app(0) == exp, "L %s x %s: dut %s want %s",
            SN[S], txla ? "txLA!" : "tx!", SN[h.l_app(0)], SN[exp]);
      int msg = app_msg(S, txla, false);
      if (msg < 0) {
        CHECK(h.l_push.empty(), "L %s txla=%d: no message, got %zu",
              SN[S], txla, h.l_push.size());
      } else {
        CHECK(h.l_push.size() == 1 && h.l_push[0].code == msg,
              "L %s txla=%d: one msg code %d", SN[S], txla, msg);
        if (h.l_push.size() == 1) {
          const Push& p = h.l_push[0];
          uint64_t sid = 0;
          for (int i = 0; i < 8; ++i) sid = (sid << 8) | p.val[i];
          CHECK(p.type == 3 && sid == SID0, "L %s Listener FirstValue", SN[S]);
          CHECK(p.fp == (declared ? 2 : 0), "L %s fourpack %u want %u",
                SN[S], p.fp, declared ? 2 : 0);
        }
      }
    }
  }
}

// ==== C. Δ13 + registrar walk, talker side (Listener tracker) ===========
void SrpStreamFsmsSuite::talker_registrar_follows_table_10_4_with_delta13() {
  h.reset();
  h.gate(true, 1, SID0 + 1, DA0 + 1, VID0);
  h.clear_logs();
  // JoinMt registers Ready -> IN, LISTENER_REG_CHANGE
  h.inject(true, 3, SID0 + 1, 0, 0, 3 /*JoinMt*/, 2 /*Ready*/);
  CHECK(h.t_reg(1) == 1 && h.t_lstn(1) == 2, "T reg: Ready registered");
  CHECK(h.t_chg[1] == 1, "T reg: one LISTENER_REG_CHANGE, got %d", h.t_chg[1]);
  CHECK(h.t_arm.empty(), "T reg: no timer op on registration");
  // Δ13: rLv -> immediate MT + change, never a leavetimer
  h.inject(true, 3, SID0 + 1, 0, 0, 5 /*Lv*/, 2);
  CHECK(h.t_reg(1) == 0 && h.t_lstn(1) == 0, "T reg: Δ13 immediate IN->MT");
  CHECK(h.t_chg[1] == 2, "T reg: change strobe on rLv, got %d", h.t_chg[1]);
  CHECK(h.t_arm.empty(), "T reg: Δ13 arms NO leavetimer");
  // LeaveAll-cycle exception: IN -> LV with T-MRP-LEAVE armed
  h.inject(true, 3, SID0 + 1, 0, 0, 1 /*JoinIn*/, 3 /*ReadyFailed*/);
  CHECK(h.t_lstn(1) == 3 && h.t_chg[1] == 3, "T reg: ReadyFailed registered");
  h.la_rx();
  CHECK(h.t_reg(1) == 2, "T reg: LeaveAll -> LV");
  CHECK(h.t_lstn(1) == 3, "T reg: LV keeps the registration published");
  CHECK(h.t_arm.size() == 1 && !h.t_arm[0].cancel && h.t_arm[0].slot == 17
        && h.t_arm[0].owner == 0x41 && h.t_arm[0].deadline == NOW + LEAVE_MS,
        "T reg: ARM slot 17 owner 0x41 now+5000 (got %zu ops)", h.t_arm.size());
  CHECK(h.t_chg[1] == 3, "T reg: no change strobe entering LV");
  // re-confirm within the cycle: -> IN, CANCEL, no strobes
  h.inject(true, 3, SID0 + 1, 0, 0, 1, 3);
  CHECK(h.t_reg(1) == 1 && h.t_chg[1] == 3, "T reg: re-join -> IN, silent");
  CHECK(h.t_arm.size() == 2 && h.t_arm[1].cancel && h.t_arm[1].slot == 17,
        "T reg: CANCEL on re-join");
  // age out: LV again, expire -> MT + change
  h.la_rx();
  CHECK(h.t_reg(1) == 2 && h.t_arm.size() == 3, "T reg: LV again + re-arm");
  h.expire(17);
  CHECK(h.t_reg(1) == 0 && h.t_lstn(1) == 0, "T reg: leavetimer! -> MT");
  CHECK(h.t_chg[1] == 4, "T reg: change strobe on expiry, got %d", h.t_chg[1]);
  // foreign expiry slots never touch this block
  h.inject(true, 3, SID0 + 1, 0, 0, 1, 2);
  h.expire(3);
  h.expire(24);
  CHECK(h.t_reg(1) == 1, "T reg: foreign slots ignored");
}

// ==== D. talker declare -> Ready -> ACTIVE -> admission-loss walk =======
void SrpStreamFsmsSuite::talker_declaration_tracks_ready_and_admission() {
  h.reset();
  h.clear_logs();
  h.gate(true, 2, SID0 + 2, DA0 + 2, 5);
  CHECK(h.t_decl(2) == 1, "T decl ADVERTISE after gate open");
  CHECK(h.t_vop.size() == 1 && h.t_vop[0].join && h.t_vop[0].vid == 5,
        "T VLAN user++ on open");
  CHECK(!((d->t_active_o >> 2) & 1), "T not ACTIVE before Ready");
  h.inject(true, 3, SID0 + 2, 0, 0, 3, 2 /*Ready*/);
  CHECK(((d->t_active_o >> 2) & 1) == 1, "T ACTIVE = declaring x Ready x admitted");
  // ReadyFailed also satisfies ACTIVE
  h.inject(true, 3, SID0 + 2, 0, 0, 1, 3 /*ReadyFailed*/);
  CHECK(((d->t_active_o >> 2) & 1) == 1, "T ACTIVE holds on ReadyFailed");
  // AskingFailed does not
  h.inject(true, 3, SID0 + 2, 0, 0, 1, 1 /*AskingFailed*/);
  CHECK(((d->t_active_o >> 2) & 1) == 0, "T not ACTIVE on AskingFailed");
  h.inject(true, 3, SID0 + 2, 0, 0, 1, 2);
  // admission loss: in-place swap to Talker Failed code 1, own MAC
  d->sr_admitted_i = 0xFF & ~(1u << 2);
  h.idle(3);
  CHECK(h.t_decl(2) == 2, "T decl FAILED on admission loss");
  CHECK(((d->t_active_o >> 2) & 1) == 0, "T ACTIVE drops on admission loss");
  CHECK(h.t_fcode(2) == 1, "T fail code 1 (insufficient bandwidth)");
  CHECK(h.t_fbridge(2) == MAC, "T fail bridge id = own MAC");
  CHECK(h.t_fcode(3) == 0 && h.t_fbridge(3) == 0, "T fail publication scoped");
  h.clear_logs();
  CHECK(h.tick(), "T failed-swap tick completes");
  CHECK(h.t_push.size() == 1 && h.t_push[0].type == 2 && h.t_push[0].code == 0,
        "T swap re-declares: New of Talker Failed");
  if (h.t_push.size() == 1) {
    const Push& p = h.t_push[0];
    uint64_t sys = 0;
    for (int i = 25; i < 33; ++i) sys = (sys << 8) | p.val[i];
    CHECK(sys == MAC && p.val[33] == 1,
          "T Failed FirstValue: system id own MAC + code 1");
  }
  // admission return: swap back to Advertise
  d->sr_admitted_i = 0xFF;
  h.idle(3);
  CHECK(h.t_decl(2) == 1 && h.t_fcode(2) == 0, "T back to ADVERTISE");
  CHECK(((d->t_active_o >> 2) & 1) == 1, "T ACTIVE returns with admission");
  h.clear_logs();
  h.tick();
  CHECK(h.t_push.size() == 1 && h.t_push[0].type == 1 && h.t_push[0].code == 0,
        "T swap-back re-declares: New of Talker Advertise");
  // gate close: Lv + VLAN user--
  h.clear_logs();
  h.gate(false, 2, 0, 0, 0);
  CHECK(h.t_decl(2) == 0, "T decl NONE after close");
  CHECK(h.t_vop.size() == 1 && !h.t_vop[0].join && h.t_vop[0].vid == 5,
        "T VLAN user-- on close");
  h.clear_logs();
  h.tick();
  CHECK(h.t_push.size() == 1 && h.t_push[0].code == 5 && h.t_push[0].type == 1,
        "T close withdraws with Lv");
}

// ==== E. listener matcher: match, near-miss, swap, unregister ===========
void SrpStreamFsmsSuite::listener_matcher_registers_swaps_and_unregisters() {
  h.reset();
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(h.l_vop.size() == 1 && h.l_vop[0].join && h.l_vop[0].vid == VID0,
        "L VLAN user++ on settle");
  // near-misses arm nothing (exact triple match, Milan §5.3.8.9)
  h.inject(true, 1, SID0 + 1, DA0, VID0, 3, 0, 111);
  h.inject(true, 1, SID0, DA0 + 1, VID0, 3, 0, 111);
  h.inject(true, 1, SID0, DA0, VID0 + 1, 3, 0, 111);
  CHECK(h.l_regst(0) == 0 && h.l_reg[0] == 0, "L near-misses never match");
  // MVRP application isolation: same bytes, wrong application
  h.inject(false, 1, SID0, DA0, VID0, 3, 0, 111);
  h.la_own(); // own MSRP LeaveAll must not fabricate registrations either
  CHECK(h.l_regst(0) == 0 && h.l_reg[0] == 0, "L MVRP/app isolation holds");
  // exact match registers ADVERTISE, latches acc_latency, declares Ready
  h.inject(true, 1, SID0, DA0, VID0, 0 /*New*/, 0, 777);
  CHECK(h.l_regst(0) == 1 && h.l_tkreg(0) == 1, "L ADVERTISE registered");
  CHECK(h.l_reg[0] == 1, "L EVT_TK_REGISTERED once, got %d", h.l_reg[0]);
  CHECK(h.l_lat(0) == 777, "L acc_latency latched, got %u", h.l_lat(0));
  CHECK(h.l_decl(0) == 2, "L declares READY");
  h.clear_logs();
  h.tick();
  CHECK(h.l_push.size() == 1 && h.l_push[0].code == 0 && h.l_push[0].fp == 2,
        "L Ready rides New on the next tick");
  // refresh with a new latency: silent re-latch (counters were cleared
  // before the tick above, so the running count restarts at zero)
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 888);
  CHECK(h.l_lat(0) == 888 && h.l_reg[0] == 0, "L refresh re-latches silently");
  // in-place swap Advertise -> Failed: strobe, no unregistration
  h.inject(true, 2, SID0, DA0, VID0, 1, 0, 999, 0xBBBB0000CCCCull, 7);
  CHECK(h.l_tkreg(0) == 2, "L in-place swap to FAILED");
  CHECK(h.l_reg[0] == 1, "L swap fires EVT_TK_REGISTERED, got %d", h.l_reg[0]);
  CHECK(h.l_unreg[0] == 0, "L swap fires NO unregistration");
  CHECK(h.l_fcode(0) == 7 && h.l_fbridge(0) == 0xBBBB0000CCCCull,
        "L failure info latched + published");
  CHECK(h.l_lat(0) == 999, "L Failed also carries acc_latency");
  CHECK(h.l_decl(0) == 1, "L declaration swaps to ASKING_FAILED");
  h.clear_logs();
  h.tick();
  CHECK(h.l_push.size() == 1 && h.l_push[0].code == 0 && h.l_push[0].fp == 1,
        "L AskingFailed rides New after the swap");
  // swap back: Failed -> Advertise
  h.inject(true, 1, SID0, DA0, VID0, 3, 0, 555);
  CHECK(h.l_tkreg(0) == 1 && h.l_reg[0] == 1, "L swap back to ADVERTISE");
  CHECK(h.l_fcode(0) == 0 && h.l_fbridge(0) == 0, "L failure gated off");
  CHECK(h.l_decl(0) == 2, "L declaration back to READY");
  // Δ13 unregister: on the withdrawing frame
  h.inject(true, 1, SID0, DA0, VID0, 5 /*Lv*/);
  CHECK(h.l_tkreg(0) == 0 && h.l_unreg[0] == 1, "L Δ13 rLv -> unregistered");
  CHECK(h.l_arm.empty(), "L Δ13 arms no leavetimer");
  CHECK(h.l_decl(0) == 0, "L declared state drops once withdrawal applies");
  h.clear_logs();
  h.tick();
  CHECK(h.l_push.size() == 1 && h.l_push[0].code == 5,
        "L withdraw rides Lv on the next tick");
  CHECK(h.l_decl(0) == 0, "L declared state NONE after withdraw");
  // LeaveAll cycle on the listener registrar
  h.inject(true, 1, SID0, DA0, VID0, 0, 0, 444);
  h.clear_logs();
  h.la_rx();
  CHECK(h.l_regst(0) == 2 && h.l_tkreg(0) == 1, "L LeaveAll -> LV, still ADV");
  CHECK(h.l_arm.size() == 1 && !h.l_arm[0].cancel && h.l_arm[0].slot == 24
        && h.l_arm[0].owner == 0x60 && h.l_arm[0].deadline == NOW + LEAVE_MS,
        "L ARM slot 24 owner 0x60 now+5000");
  h.expire(24);
  CHECK(h.l_regst(0) == 0 && h.l_unreg[0] == 1, "L expiry -> MT + unregistered");
  // teardown: no event, VLAN user--, declaration withdrawn
  h.inject(true, 1, SID0, DA0, VID0, 0, 0, 333);
  CHECK(h.l_tkreg(0) == 1, "L re-registered before teardown");
  h.clear_logs();
  h.ctl(false, 0, 0, 0, 0);
  CHECK(h.l_tkreg(0) == 0, "L teardown -> NONE");
  CHECK(h.l_unreg[0] == 0 && h.l_reg[0] == 0, "L teardown fires NO events");
  CHECK(h.l_vop.size() == 1 && !h.l_vop[0].join && h.l_vop[0].vid == VID0,
        "L VLAN user-- on teardown");
  h.clear_logs();
  h.tick();
  CHECK(h.l_push.size() == 1 && h.l_push[0].code == 5,
        "L teardown withdraws the declaration");
  // torn-down matcher is deaf
  h.clear_logs();
  h.inject(true, 1, SID0, DA0, VID0, 0, 0, 222);
  CHECK(h.l_regst(0) == 0 && h.l_reg[0] == 0, "L A8 disarms the matcher");
}

// ==== F. VLAN handshake back-pressure + collapse =========================
void SrpStreamFsmsSuite::vlan_user_handshake_holds_and_collapses() {
  h.reset();
  h.clear_logs();
  h.t_uready = false;
  h.gate(true, 3, SID0 + 3, DA0 + 3, 7);
  CHECK(d->t_user_valid_o && d->t_user_join_o && d->t_user_vid_o == 7,
        "T VLAN op held under back-pressure");
  h.idle(3);
  CHECK(d->t_user_valid_o, "T VLAN op still held");
  CHECK(h.t_vop.empty(), "T no op consumed while not ready");
  h.t_uready = true;
  h.idle(2);
  CHECK(h.t_vop.size() == 1 && h.t_vop[0].join && h.t_vop[0].vid == 7,
        "T held op lands once ready");
  // close-before-join collapses to nothing
  h.t_uready = false;
  h.gate(true, 4, SID0 + 4, DA0 + 4, 9);
  h.gate(false, 4, 0, 0, 0);
  h.t_uready = true;
  h.idle(4);
  CHECK(h.t_vop.size() == 1, "T open+close before issue = net zero, got %zu",
        h.t_vop.size());
}

// ==== G. per-application isolation on the talker tracker ================
void SrpStreamFsmsSuite::talker_tracker_isolates_applications() {
  h.reset();
  h.gate(true, 5, SID0 + 5, DA0 + 5, VID0);
  h.clear_logs();
  h.inject(false, 3, SID0 + 5, 0, 0, 3, 2);   // MVRP application: ignored
  CHECK(h.t_reg(5) == 0 && h.t_chg[5] == 0, "T MVRP-app Listener ignored");
  h.inject(false, 1, SID0 + 5, DA0 + 5, VID0, 5);  // MVRP VID type-1 collision
  CHECK(h.t_app(5) == VN, "T MVRP type-1 collision never reaches the applicant");
}

int SrpStreamFsmsSuite::run() {
  rx_events_match_table_10_3();
  talker_tx_rows_send_the_table_10_3_message();
  listener_tx_rows_send_the_table_10_3_message();
  talker_registrar_follows_table_10_4_with_delta13();
  talker_declaration_tracks_ready_and_admission();
  listener_matcher_registers_swaps_and_unregisters();
  vlan_user_handshake_holds_and_collapses();
  talker_tracker_isolates_applications();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SrpStreamFsmsSuite suite;
  return suite.run();
}

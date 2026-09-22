// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_acmp_listener suite — THE MTXW WALK (docs/architecture/09 §3).
//
// Every one of the 112 cells of F05.3 (14 events x 8 states) is driven
// against an INDEPENDENT C++ matrix model transcribed from the doc table
// WITHOUT gen_ltn_rom.py — the two transcriptions must agree through the
// DUT's behavior; that is the point. Every '—'/'ign' cell is proven inert
// (state unchanged, no action strobes, no frames, no timer ops, no notify).
// The harness emulates the four landed faces cycle-exactly (KL_pp_rx_slots
// sync read, KL_pp_tx_slots grant-after-request, KL_pp_timer_service arm
// bus, KL_pp_prng draw) and captures every observable: record write-backs,
// 56-byte committed ACMPDUs, timer arm/cancel ops, action strobes.
//
// Timer-row '—' cells come in two honest kinds: states with NO armed SM
// timer (UNB/PWA/SOK — 12 cells) get a spurious expiry injected and full
// inertness checked; states whose armed T-ID aliases the shared slot (15
// cells) are proven impossible by construction — the deadline armed on
// entry equals the state's own T-ID, so the foreign expiry cannot exist —
// plus the model's own transcription must mark the cell '—'.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <memory>
#include <string>
#include <vector>
#include "VKL_pp_acmp_listener.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- constants shared with the doc (not with the RTL) ---------------------
constexpr uint64_t OUR_EID = 0x0A0B0C0D0E0F1011ull;
constexpr uint64_t CTL1 = 0x0011223344556677ull;
constexpr uint64_t CTL2 = 0x0099AABBCCDDEEFFull;
constexpr uint64_t TK_A = 0x00221100AABBCCDDull;
constexpr uint64_t TK_B = 0x00221100AABBCC55ull;
constexpr uint16_t TKUID_A = 1;
constexpr uint16_t TKUID_B = 2;
constexpr uint32_t NOW = 50000;
constexpr uint16_t DRAWVAL = 777;            // scripted PRNG kind-0 draw
constexpr int N_SINKS = 8;
constexpr int N_ROWS = 14;      // F05.3 event rows
constexpr int N_STATES = 8;     // F05.3 listener states
constexpr int PDU_BYTES = 56;   // committed ACMPDU length
constexpr int TMR_BASE = 9;
constexpr int OWNER_BASE = 32;
constexpr int T_CMD = 200;
constexpr int T_RETRY = 4000;
constexpr int T_NOTK = 10000;
constexpr int ST_OK = 0;
constexpr int ST_LUID = 1;
constexpr int ST_TT = 7;
constexpr int ST_NOAUTH = 13;
constexpr int ST_NOBW = 5;
constexpr int M_PROBE_CMD = 0;
constexpr int M_PROBE_RESP = 1;
constexpr int M_BIND = 6;
constexpr int M_BIND_R = 7;
constexpr int M_UNBIND = 8;
constexpr int M_UNBIND_R = 9;
constexpr int M_GETRX = 10;
constexpr int M_GETRX_R = 11;
constexpr int S_UNB = 0;
constexpr int S_PWA = 1;
constexpr int S_PWD = 2;
constexpr int S_PWR = 3;
constexpr int S_PW2 = 4;
constexpr int S_PWT = 5;
constexpr int S_SNR = 6;
constexpr int S_SOK = 7;
constexpr int R_BIND_SAME = 0;
constexpr int R_BIND_NEW = 1;
constexpr int R_UNBIND = 2;
constexpr int R_GETRX = 3;
constexpr int R_PROBE_OK = 4;
constexpr int R_PROBE_FAIL = 5;
constexpr int R_TMR_DELAY = 6;
constexpr int R_TMR_CMD = 7;
constexpr int R_TMR_RETRY = 8;
constexpr int R_TMR_NOTK = 9;
constexpr int R_TK_DISC = 10;
constexpr int R_TK_DEP = 11;
constexpr int R_TK_REG = 12;
constexpr int R_TK_UNREG = 13;
constexpr const char* RN[N_ROWS] = {"BIND_SAME","BIND_NEW","UNBIND","GETRX",
  "PROBE_OK","PROBE_FAIL","TMR_DELAY","TMR_CMD","TMR_RETRY","TMR_NOTK",
  "TK_DISC","TK_DEP","TK_REG","TK_UNREG"};
constexpr const char* SN[N_STATES] = {"UNB","PWA","PWD","PWR","PW2","PWT",
                                      "SNR","SOK"};

// ---- bit helpers ----------------------------------------------------------
static void wput(uint32_t* w, int lsb, int width, uint64_t v) {
  for (int i = 0; i < width; ++i) {
    int b = lsb + i;
    if ((v >> i) & 1) w[b >> 5] |= 1u << (b & 31);
    else              w[b >> 5] &= ~(1u << (b & 31));
  }
}
static uint64_t wget(const uint32_t* w, int lsb, int width) {
  uint64_t v = 0;
  for (int i = 0; i < width; ++i) {
    int b = lsb + i;
    if ((w[b >> 5] >> (b & 31)) & 1) v |= 1ull << i;
  }
  return v;
}

// ---- the wire ACMPDU (F05.13 transcription — used for stimulus AND
// expectation; big-endian fields at the documented byte offsets) ------------
struct Pdu { uint8_t b[PDU_BYTES]; };
static void be(uint8_t* p, uint64_t v, int n) {
  for (int i = 0; i < n; ++i) p[i] = uint8_t(v >> (8 * (n - 1 - i)));
}
static Pdu mk_pdu(uint8_t msg, uint8_t status, uint64_t sid, uint64_t ctlr,
                  uint64_t tkeid, uint64_t leid, uint16_t tkuid,
                  uint16_t luid, uint64_t da, uint16_t cc, uint16_t seq,
                  uint16_t flags, uint16_t vlan) {
  Pdu p{};
  p.b[0] = 0xFC;                       // subtype
  p.b[1] = msg & 0x0F;                 // h=0, ver=0, message_type
  p.b[2] = uint8_t((status << 3) | 0); // status . cdl[10:8] (cdl 44)
  p.b[3] = 44;
  be(p.b + 4, sid, 8);
  be(p.b + 12, ctlr, 8);
  be(p.b + 20, tkeid, 8);
  be(p.b + 28, leid, 8);
  be(p.b + 36, tkuid, 2);
  be(p.b + 38, luid, 2);
  be(p.b + 40, da, 6);
  be(p.b + 46, cc, 2);
  be(p.b + 48, seq, 2);
  be(p.b + 50, flags, 2);
  be(p.b + 52, vlan, 2);
  return p;
}

// ---- record image (F07.6 transcription) -----------------------------------
struct Rec {
  uint8_t sm = 0;
  uint8_t pbsta = 0;
  uint8_t acmpsta = 0;
  uint8_t srp_decl = 0;
  bool bound = false;
  bool started = false;
  bool sw = false;
  bool retried = false;
  bool tk_reg = false;
  bool tk_disc = false;
  uint64_t talker_eid = 0;
  uint64_t bind_ctlr = 0;
  uint64_t sid = 0;
  uint64_t da = 0;
  uint16_t talker_uid = 0;
  uint16_t probe_seq = 0;
  uint16_t vlan = 0;
  uint32_t last_avail = 0;
  uint8_t ifx = 0;
  uint8_t smh = 0;
  uint8_t noadp = 0;
  bool operator==(const Rec& o) const {
    return sm == o.sm && pbsta == o.pbsta && acmpsta == o.acmpsta &&
           srp_decl == o.srp_decl && bound == o.bound &&
           started == o.started && sw == o.sw && retried == o.retried &&
           tk_reg == o.tk_reg && tk_disc == o.tk_disc &&
           talker_eid == o.talker_eid && bind_ctlr == o.bind_ctlr &&
           sid == o.sid && da == o.da && talker_uid == o.talker_uid &&
           probe_seq == o.probe_seq && vlan == o.vlan &&
           last_avail == o.last_avail && ifx == o.ifx && smh == o.smh &&
           noadp == o.noadp;
  }
};
static Rec unpack(const uint32_t* w) {
  Rec r;
  r.sm = uint8_t(wget(w, 0, 3));   r.pbsta = uint8_t(wget(w, 3, 3));
  r.acmpsta = uint8_t(wget(w, 6, 5));
  r.bound = wget(w, 11, 1);        r.started = wget(w, 12, 1);
  r.sw = wget(w, 13, 1);           r.retried = wget(w, 14, 1);
  r.srp_decl = uint8_t(wget(w, 15, 2));
  r.tk_reg = wget(w, 17, 1);       r.tk_disc = wget(w, 18, 1);
  r.talker_eid = wget(w, 32, 64);  r.talker_uid = uint16_t(wget(w, 96, 16));
  r.probe_seq = uint16_t(wget(w, 112, 16));
  r.bind_ctlr = wget(w, 128, 64);  r.sid = wget(w, 192, 64);
  r.da = wget(w, 256, 48);         r.vlan = uint16_t(wget(w, 304, 12));
  r.last_avail = uint32_t(wget(w, 320, 32));
  r.ifx = uint8_t(wget(w, 352, 8)); r.smh = uint8_t(wget(w, 360, 8));
  r.noadp = uint8_t(wget(w, 368, 8));
  return r;
}

// ---- stimulus -------------------------------------------------------------
struct Stim {
  enum K { TXN, EXP, TK } k = TXN;
  uint8_t msg = 0;
  uint8_t status = 0;
  uint16_t uid = 0;
  uint16_t seq = 0;
  uint16_t flags = 0;
  uint16_t tk_uid = 0;
  uint16_t vlan = 0;
  uint64_t ctlr = 0;
  uint64_t tk_eid = 0;
  uint64_t sid = 0;
  uint64_t da = 0;
  uint64_t target = OUR_EID;
  uint8_t tk_kind = 0;
  bool tk_fail = false;
  uint8_t protocol = 1;  // PP_PROTO_ACMP
};

// ---- expected effects -----------------------------------------------------
struct TOp { bool cancel; uint32_t deadline; };
struct Exp {
  bool wrote = false;
  std::vector<Pdu> frames;
  std::vector<TOp> tops;
  bool settle = false;
  bool teardown = false;
  bool disc_arm = false;
  bool disc_disarm = false;
  bool nvm = false;
  bool nvm_set = false;
  uint64_t disc_eid = 0;
  uint64_t settle_sid = 0;
  uint64_t settle_da = 0;
  uint16_t settle_vlan = 0;
  int notify = 0;
  int frees = 0;
  int row = -1;  // classified row (for walk bookkeeping)
};

// ==========================================================================
// THE INDEPENDENT MATRIX MODEL — F05.3 transcribed from the doc table,
// row by row, WITHOUT looking at gen_ltn_rom.py. Cell = {kind, next,
// action list in the doc's listed order}. 'cond' = the dagger legend:
// tk? PWD/A12 : PWA/A17 (base acts run first).
// ==========================================================================
constexpr int C_DASH = 0;
constexpr int C_IGN = 1;
constexpr int C_NORM = 2;
constexpr int C_COND = 3;
struct MCell { int t; int next; const char* acts; };
constexpr MCell M[N_ROWS][N_STATES] = {
  // BIND_RX same talker+source: UNB impossible, else self/A1 A6 A3
  {{C_DASH,0,""},        {C_NORM,S_PWA,"1 6 3"}, {C_NORM,S_PWD,"1 6 3"},
   {C_NORM,S_PWR,"1 6 3"},{C_NORM,S_PW2,"1 6 3"},{C_NORM,S_PWT,"1 6 3"},
   {C_NORM,S_SNR,"1 6 3"},{C_NORM,S_SOK,"1 6 3"}},
  // BIND_RX new/different source
  {{C_NORM,S_PWR,"1 2 3 4 5"},
   {C_NORM,S_PWR,"1 11 9 2 3 4 5"},  {C_NORM,S_PWR,"1 11 9 2 3 4 5"},
   {C_NORM,S_PWR,"1 11 9 2 3 4 5"},  {C_NORM,S_PWR,"1 11 9 2 3 4 5"},
   {C_NORM,S_PWR,"1 11 9 2 3 4 5"},
   {C_NORM,S_PWR,"1 11 8 9 2 3 4 5"},{C_NORM,S_PWR,"1 11 8 9 2 3 4 5"}},
  // UNBIND_RX
  {{C_NORM,S_UNB,"1 7"},
   {C_NORM,S_UNB,"1 11 9 10 7"},  {C_NORM,S_UNB,"1 11 9 10 7"},
   {C_NORM,S_UNB,"1 11 9 10 7"},  {C_NORM,S_UNB,"1 11 9 10 7"},
   {C_NORM,S_UNB,"1 11 9 10 7"},
   {C_NORM,S_UNB,"1 11 8 9 10 7"},{C_NORM,S_UNB,"1 11 8 9 10 7"}},
  // GET_RX_STATE
  {{C_NORM,S_UNB,"16"},{C_NORM,S_PWA,"16"},{C_NORM,S_PWD,"16"},
   {C_NORM,S_PWR,"16"},{C_NORM,S_PW2,"16"},{C_NORM,S_PWT,"16"},
   {C_NORM,S_SNR,"16"},{C_NORM,S_SOK,"16"}},
  // PROBE_RESP SUCCESS
  {{C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""},
   {C_NORM,S_SNR,"11 15"},{C_NORM,S_SNR,"11 15"},
   {C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""}},
  // PROBE_RESP != SUCCESS
  {{C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""},
   {C_NORM,S_PWT,"11 14"},{C_NORM,S_PWT,"11 14"},
   {C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""}},
  // T-ACMP-DELAY expiry
  {{C_DASH,0,""},{C_DASH,0,""},{C_NORM,S_PWR,"5"},{C_DASH,0,""},
   {C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""}},
  // T-ACMP-CMD expiry
  {{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_NORM,S_PW2,"13"},
   {C_NORM,S_PWT,"14"},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""}},
  // T-ACMP-RETRY expiry (dagger)
  {{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},
   {C_DASH,0,""},{C_COND,0,""},{C_DASH,0,""},{C_DASH,0,""}},
  // T-ACMP-NOTK expiry (dagger, A8 first)
  {{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},
   {C_DASH,0,""},{C_DASH,0,""},{C_COND,0,"8"},{C_DASH,0,""}},
  // EVT_TK_DISCOVERED ('ign (note)': bookkeeping still tracks)
  {{C_DASH,0,""},{C_NORM,S_PWD,"12"},{C_IGN,0,""},{C_IGN,0,""},
   {C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""},{C_IGN,0,""}},
  // EVT_TK_DEPARTED (SNR/SOK note only: reservation kept)
  {{C_DASH,0,""},{C_DASH,0,""},
   {C_NORM,S_PWA,"11 17"},{C_NORM,S_PWA,"11 17"},
   {C_NORM,S_PWA,"11 17"},{C_NORM,S_PWA,"11 17"},
   {C_IGN,0,""},{C_IGN,0,""}},
  // EVT_TK_REGISTERED — SNR only; SOK is the documented REF-BUG 'x'
  {{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},
   {C_DASH,0,""},{C_DASH,0,""},{C_NORM,S_SOK,"11"},{C_DASH,0,""}},
  // EVT_TK_UNREGISTERED (dagger, A8 first) — SOK only
  {{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},
   {C_DASH,0,""},{C_DASH,0,""},{C_DASH,0,""},{C_COND,0,"8"}},
};

struct Model {
  Rec rec[N_SINKS];
  uint16_t probe_ctr = 0;
  bool lock_held = false;
  uint64_t lock_eid = 0;

  // classify the physical stimulus onto an F05.3 row (mirrors 05 §3 + the
  // shared-SM-slot rule of 08 §5) — independent of the DUT's classifier
  int classify(int sink, const Stim& s) const {
    const Rec& r = rec[sink];
    if (s.k == Stim::TXN) {
      if (s.msg == M_BIND)
        return (r.bound && s.tk_eid == r.talker_eid &&
                s.tk_uid == r.talker_uid) ? R_BIND_SAME : R_BIND_NEW;
      if (s.msg == M_UNBIND) return R_UNBIND;
      if (s.msg == M_GETRX) return R_GETRX;
      return (s.status == ST_OK) ? R_PROBE_OK : R_PROBE_FAIL;
    }
    if (s.k == Stim::EXP) {
      switch (r.sm) {
        case S_PWD: return R_TMR_DELAY;
        case S_PWR: case S_PW2: return R_TMR_CMD;
        case S_PWT: return R_TMR_RETRY;
        case S_SNR: return R_TMR_NOTK;
        default:    return R_TMR_CMD;  // spurious: every such cell is '—'
      }
    }
    return R_TK_DISC + s.tk_kind;
  }

  Pdu f_bind(const Stim& s) const {
    return mk_pdu(M_BIND_R, ST_OK, 0, s.ctlr, s.tk_eid, OUR_EID, s.tk_uid,
                  s.uid, 0, 1, s.seq, uint16_t(s.flags & 0x0008), 0);
  }
  Pdu f_unbind(const Stim& s) const {
    return mk_pdu(M_UNBIND_R, ST_OK, 0, s.ctlr, s.tk_eid, OUR_EID, s.tk_uid,
                  s.uid, 0, 0, s.seq, 0, 0);
  }
  Pdu f_getrx(int sink, const Stim& s) const {
    const Rec& r = rec[sink];
    bool settled = (r.sm == S_SNR || r.sm == S_SOK);
    bool rf = (r.sm == S_SOK) && ((r.srp_decl >> 1) & 1);
    uint16_t fl = r.bound ? uint16_t(0x0002 | (r.sw ? 0x0008 : 0) |
                                     (rf ? 0x0040 : 0)) : 0;
    return mk_pdu(M_GETRX_R, ST_OK, settled ? r.sid : 0, s.ctlr,
                  r.bound ? r.talker_eid : 0, OUR_EID,
                  r.bound ? r.talker_uid : 0, s.uid,
                  settled ? r.da : 0, r.bound ? 1 : 0, s.seq, fl,
                  settled ? r.vlan : 0);
  }
  Pdu f_probe(int sink) const {
    const Rec& r = rec[sink];
    return mk_pdu(M_PROBE_CMD, ST_OK, 0, r.bind_ctlr, r.talker_eid, OUR_EID,
                  r.talker_uid, uint16_t(sink), 0, 0, r.probe_seq, 0x0002, 0);
  }
  Pdu f_err(uint8_t msg, uint8_t status, const Stim& s) const {
    return mk_pdu(uint8_t(msg + 1), status, 0, s.ctlr, s.tk_eid, OUR_EID,
                  s.tk_uid, s.uid, 0, 0, s.seq, 0, 0);
  }

 private:
  // 05 §3 admission for a received transaction: only an ACMP-protocol
  // command out of the listener's own message set, addressed to us, is let
  // through to the matrix. An out-of-range listener UID is answered
  // LISTENER_UNKNOWN_ID (a PROBE_RESP, being itself a response, is never
  // answered); a PROBE_RESP that does not match the record's outstanding
  // probe is dropped. False means the stimulus dies here, having already
  // left in `e` whatever it was owed.
  bool admit_txn(int sink, const Stim& s, Exp& e) const {
    if (s.protocol != 1 ||
        !(s.msg == M_PROBE_RESP || s.msg == M_BIND || s.msg == M_UNBIND ||
          s.msg == M_GETRX) || s.target != OUR_EID)
      return false;  // consumed silently, nothing else
    if (s.uid >= N_SINKS) {
      if (s.msg != M_PROBE_RESP)
        e.frames.push_back(f_err(s.msg, ST_LUID, s));
      return false;
    }
    if (s.msg == M_PROBE_RESP) {
      const Rec& r = rec[sink];
      if (!(s.ctlr == r.bind_ctlr && s.tk_eid == r.talker_eid &&
            s.tk_uid == r.talker_uid && s.seq == r.probe_seq))
        return false;  // 05 §3: silently ignore
    }
    return true;
  }

  // event bookkeeping, gated exactly by cell validity (not '—')
  void note_event(int sink, int row, const MCell& c, const Stim& s, Exp& e) {
    Rec& r = rec[sink];
    bool valid = (c.t != C_DASH);
    if (valid && row == R_TK_DISC) r.tk_disc = true;
    if (valid && row == R_TK_DEP) r.tk_disc = false;
    if (valid && c.t != C_IGN && row == R_TK_REG) {
      r.tk_reg = true;
      r.srp_decl = uint8_t((r.srp_decl & 1) | (s.tk_fail ? 2 : 0));
    }
    e.wrote = true;               // every classified work item writes back
    r.smh = uint8_t(TMR_BASE + sink);
  }

  // one cell read against one record: the doc's action numbers in the doc's
  // listed order, and the state the cell lands in
  struct Resolved { std::vector<int> acts; int next = 0; };

  // resolve the cell's action list + next state
  Resolved resolve_cell(const MCell& c, const Rec& r) const {
    Resolved rv;
    int tok = 0;
    for (const char* p = c.acts; *p;) {
      if (*p >= '0' && *p <= '9') { tok = tok * 10 + (*p - '0'); }
      else if (tok) { rv.acts.push_back(tok); tok = 0; }
      ++p;
    }
    if (tok) rv.acts.push_back(tok);
    rv.next = c.next;
    if (c.t == C_COND) {
      if (r.tk_disc) { rv.next = S_PWD; rv.acts.push_back(12); }
      else           { rv.next = S_PWA; rv.acts.push_back(17); }
    }
    return rv;
  }

  // run the resolved action list against the record, collecting into `e`
  // every observable the actions produce; the return is Table 5.22's
  // notify, i.e. whether any action actually moved the record
  bool apply_acts(int sink, int row, const std::vector<int>& acts,
                  const Stim& s, Exp& e) {
    Rec& r = rec[sink];
    bool mut = false;
    for (int a : acts) {
      switch (a) {
        case 1: break;
        case 2:
          r.talker_eid = s.tk_eid; r.talker_uid = s.tk_uid;
          r.bind_ctlr = s.ctlr; r.sw = (s.flags >> 3) & 1; r.bound = true;
          // Milan 5.3.8.7 leaves started/stopped undefined while unbound, so
          // the bind is what defines it, and IEEE 7.4.35 says which way:
          // START_STREAMING starts a stream "connected via ACMP with the
          // STREAMING_WAIT flag SET", so a bind carrying the flag lands
          // stopped and a bind without it lands started. Table 5.9 bit 28
          // agrees from the other side - it reports 1 only for a sink that
          // is "bound and stopped", and ACMP reports the SAVED flag, so the
          // two answers would contradict each other any other way.
          r.started = !((s.flags >> 3) & 1);
          e.nvm = true; e.nvm_set = true; mut = true; break;
        case 3: e.frames.push_back(f_bind(s)); break;
        case 4:
          e.disc_arm = true; e.disc_eid = r.talker_eid; r.pbsta = 1;
          mut = true; break;
        case 5:
          r.probe_seq = probe_ctr++; r.retried = false; r.pbsta = 2;
          r.acmpsta = 0; e.frames.push_back(f_probe(sink));
          e.tops.push_back({false, NOW + T_CMD}); mut = true; break;
        case 6:
          // 5.5.3.5.6 step 2 re-bind: the binding parameters are UPDATED
          // with the new command's STREAMING_WAIT, so started follows
          r.bind_ctlr = s.ctlr; r.sw = (s.flags >> 3) & 1;
          r.started = !((s.flags >> 3) & 1); mut = true; break;
        case 7: e.frames.push_back(f_unbind(s)); break;
        case 8:
          e.teardown = true; r.sid = 0; r.da = 0; r.vlan = 0;
          r.tk_reg = false; r.srp_decl = 0; mut = true; break;
        case 9: e.disc_disarm = true; r.tk_disc = false; mut = true; break;
        case 10:
          r.talker_eid = 0; r.talker_uid = 0; r.bind_ctlr = 0;
          r.probe_seq = 0; r.bound = false; r.sw = false;
          r.started = false; r.retried = false; r.pbsta = 0; r.acmpsta = 0;
          e.nvm = true; e.nvm_set = false; mut = true; break;
        case 11: e.tops.push_back({true, 0}); break;
        case 12:
          r.pbsta = 2; r.acmpsta = 0;
          e.tops.push_back({false, NOW + DRAWVAL}); mut = true; break;
        case 13:
          r.retried = true; e.frames.push_back(f_probe(sink));
          e.tops.push_back({false, NOW + T_CMD}); mut = true; break;
        case 14:
          e.tops.push_back({false, NOW + T_RETRY});
          r.acmpsta = (row == R_PROBE_FAIL) ? s.status : ST_TT;
          mut = true; break;
        case 15:
          r.sid = s.sid; r.da = s.da; r.vlan = uint16_t(s.vlan & 0xFFF);
          r.srp_decl |= 1; r.pbsta = 3; r.acmpsta = 0;
          e.settle = true; e.settle_sid = s.sid; e.settle_da = s.da;
          e.settle_vlan = uint16_t(s.vlan & 0xFFF);
          e.tops.push_back({false, NOW + T_NOTK}); mut = true; break;
        case 16: e.frames.push_back(f_getrx(sink, s)); break;
        case 17: r.pbsta = 1; r.acmpsta = 0; mut = true; break;
        default: break;
      }
    }
    return mut;
  }

 public:
  // predict all observable effects of one stimulus (the reference)
  Exp predict(int sink, const Stim& s) {
    Exp e;
    e.frees = (s.k == Stim::TXN) ? 1 : 0;
    if (s.k == Stim::TXN && !admit_txn(sink, s, e)) return e;
    int row = classify(sink, s);
    e.row = row;
    const MCell& c = M[row][rec[sink].sm];
    note_event(sink, row, c, s, e);
    if (c.t == C_DASH || c.t == C_IGN) return e;
    Resolved rv = resolve_cell(c, rec[sink]);

    // A1 gate (05 §6.3 legend)
    bool has_a1 = !rv.acts.empty() && rv.acts[0] == 1;
    if (has_a1 && lock_held && lock_eid != s.ctlr) {
      e.frames.push_back(f_err(s.msg, ST_NOAUTH, s));
      e.wrote = false;            // abort cell: no commit
      return e;
    }

    rec[sink].sm = uint8_t(rv.next);
    e.notify = apply_acts(sink, row, rv.acts, s, e) ? 1 : 0;
    return e;
  }
};

// ==========================================================================
// Harness: cycle-exact emulation of the landed faces + collectors
// ==========================================================================
struct ATop {
  bool cancel;
  uint8_t slot;
  uint8_t owner;
  uint32_t deadline;
};
struct Col {
  int wrotes = 0;
  int frees = 0;
  int notifies = 0;
  //! Milan Table 5.22's started/stopped trigger, counted separately from the
  //! generic record-change notify so a no-op can be told from a transition.
  int strt_chgs = 0;
  std::vector<Pdu> frames;
  std::vector<ATop> tops;
  bool settle = false;
  bool teardown = false;
  bool disc_arm = false;
  bool disc_disarm = false;
  bool nvm = false;
  bool nvm_set = false;
  uint64_t disc_eid = 0;
  uint64_t settle_sid = 0;
  uint64_t settle_da = 0;
  uint16_t settle_vlan = 0;
  uint8_t free_slot = 0xFF;
  void clear() { *this = Col(); }
};

struct Harness {
  VKL_pp_acmp_listener* d;
  Rec shadow[N_SINKS];
  Col col;
  uint8_t rxmem[4][576] = {};
  uint8_t txmem[5][1600] = {};
  uint16_t txlen[5] = {};
  bool txfree[5] = {
      true, true, true, true, true};
  bool gnt_pending = false;
  bool alloc_block = false;
  uint8_t gnt_slot = 0;
  uint8_t rx_pending_byte = 0;
  int prng_cnt = 0;
  bool prng_fire = false;
  // one-shot injections for the NEXT tick
  bool inj_exp = false;
  uint8_t inj_exp_sink = 0;
  int next_rx_slot = 0;
  uint32_t last_arm_deadline[N_SINKS] = {};

  explicit Harness(VKL_pp_acmp_listener* dut) : d(dut) {}

  void tick() {
    // inputs for this cycle (face responses to LAST cycle's outputs)
    d->rxs_rd_data_i = rx_pending_byte;
    d->txs_alloc_gnt_i = gnt_pending;
    d->txs_alloc_slot_i = gnt_slot;
    gnt_pending = false;
    d->draw_busy_i = (prng_cnt > 0);
    d->draw_valid_i = prng_fire;
    d->draw_ms_i = prng_fire ? DRAWVAL : 0;
    if (prng_fire) prng_fire = false;
    else if (prng_cnt > 0 && --prng_cnt == 0) prng_fire = true;
    d->tmr_exp_valid_i = inj_exp;
    d->tmr_exp_slot_i = uint8_t(TMR_BASE + inj_exp_sink);
    d->tmr_exp_owner_i = uint8_t(OWNER_BASE + inj_exp_sink);
    inj_exp = false;
    d->now_ms_i = NOW;

    d->clk_i = 0; d->eval();

    // sample this cycle's outputs (pre-edge)
    if (d->rxs_rd_en_o)
      rx_pending_byte = rxmem[d->rxs_rd_slot_o][d->rxs_rd_addr_o];
    if (d->txs_alloc_req_o && !d->txs_oversize_o && !alloc_block) {
      for (int i = 0; i < 4; ++i)
        if (txfree[i]) { txfree[i] = false; gnt_slot = uint8_t(i);
                         gnt_pending = true; break; }
    }
    if (d->txs_wr_valid_o && d->txs_wr_addr_o < 1600)
      txmem[d->txs_wr_slot_o][d->txs_wr_addr_o] = d->txs_wr_data_o;
    if (d->txs_wr_commit_o) txlen[d->txs_wr_slot_o] = d->txs_wr_len_o;
    if (d->txreq_valid_o) {
      Pdu p{};
      int n = txlen[d->txreq_slot_o] < PDU_BYTES ? txlen[d->txreq_slot_o]
                                                 : PDU_BYTES;
      memcpy(p.b, txmem[d->txreq_slot_o], size_t(n));
      col.frames.push_back(p);
      txfree[d->txreq_slot_o] = true;  // arbiter auto-free after serialize
    }
    if (d->draw_req_o && prng_cnt == 0 && !prng_fire) prng_cnt = 2;
    if (d->tmr_arm_valid_o) {
      col.tops.push_back({bool(d->tmr_arm_cancel_o), d->tmr_arm_slot_o,
                          d->tmr_arm_owner_o, d->tmr_arm_deadline_ms_o});
      if (!d->tmr_arm_cancel_o && d->tmr_arm_slot_o >= TMR_BASE &&
          d->tmr_arm_slot_o < TMR_BASE + N_SINKS)
        last_arm_deadline[d->tmr_arm_slot_o - TMR_BASE] =
            d->tmr_arm_deadline_ms_o;
    }
    if (d->rxs_free_o) { col.frees++; col.free_slot = d->rxs_free_slot_o; }
    if (d->act_settle_o) {
      col.settle = true; col.settle_sid = d->act_settle_sid_o;
      col.settle_da = d->act_settle_da_o; col.settle_vlan = d->act_settle_vlan_o;
    }
    if (d->act_teardown_o) col.teardown = true;
    if (d->act_disc_arm_o) { col.disc_arm = true;
                             col.disc_eid = d->act_disc_talker_eid_o; }
    if (d->act_disc_disarm_o) col.disc_disarm = true;
    if (d->act_nvm_o) { col.nvm = true; col.nvm_set = d->act_nvm_set_o; }
    if (d->act_notify_o) col.notifies++;
    if (d->act_strt_chg_o) col.strt_chgs++;
    if (d->dbg_recwr_o) {
      col.wrotes++;
      shadow[d->dbg_recwr_sink_o] = unpack(&d->dbg_recwr_rec_o[0]);
    }

    d->clk_i = 1; d->eval();
  }

  bool wait_idle(int cap = 4000) {
    for (int i = 0; i < cap; ++i) { if (d->txn_ready_o) return true; tick(); }
    return false;
  }
  // wait_idle returns on the first idle cycle WITHOUT sampling it; strobes
  // registered on the retire edge (rxs_free_o) are visible exactly then, so
  // every drive ends with one trailing sampled tick
  bool drain() { bool ok = wait_idle(); tick(); return ok; }

  // drive one stimulus to completion; returns false on hang/refusal
  bool drive(int sink, const Stim& s) {
    if (!wait_idle()) return false;
    if (s.k == Stim::TXN) {
      int slot = next_rx_slot; next_rx_slot = (next_rx_slot + 1) % 4;
      Pdu p = mk_pdu(s.msg, s.status, s.sid, s.ctlr, s.tk_eid, s.target,
                     s.tk_uid, s.uid, s.da, 0, s.seq, s.flags, s.vlan);
      memcpy(rxmem[slot], p.b, PDU_BYTES);
      uint32_t* w = &d->txn_i[0];
      for (int i = 0; i < 13; ++i) w[i] = 0;
      wput(w, 391, 2, 0);                    // origin RX
      wput(w, 354, 3, s.protocol);           // protocol
      wput(w, 350, 4, s.msg);                // msg_type
      wput(w, 345, 5, s.status);             // status_in
      wput(w, 334, 11, 44);                  // cdl
      wput(w, 222, 64, s.ctlr);              // controller_eid
      wput(w, 158, 64, s.target);            // target_eid (listener)
      wput(w, 142, 16, s.seq);               // sequence_id
      wput(w, 124, 16, s.msg);               // opcode mirror
      wput(w, 92, 16, s.tk_uid);             // operands.desc_index
      wput(w, 60, 16, s.uid);                // operands.unique_id
      wput(w, 57, 3, uint64_t(slot));        // rx_slot
      wput(w, 0, 2, 1);                      // resp_disposition ACMP mcast
      d->txn_valid_i = 1;
      tick();                                // accepted (ready was high)
      d->txn_valid_i = 0;
      tick();
      return drain();
    }
    if (s.k == Stim::EXP) {
      inj_exp = true; inj_exp_sink = uint8_t(sink);
      tick();                                // pendexp set
      tick();                                // popped
      return drain();
    }
    d->evt_tk_valid_i = 1;
    d->evt_tk_kind_i = s.tk_kind;
    d->evt_tk_failed_i = s.tk_fail;
    d->evt_tk_sink_i = uint16_t(sink);
    // ready requires idle && !txn_valid && !pend — we are idle already
    tick();                                  // accepted
    d->evt_tk_valid_i = 0;
    tick();
    return drain();
  }
};

// ==========================================================================
// The walk driver: the tally, the emulated faces and the matrix model live in
// one object, so no harness state sits at file scope (I.2).
// ==========================================================================
class ListenerWalk {
 public:
  explicit ListenerWalk(VKL_pp_acmp_listener* dut) : d(dut), h(dut) {}
  int run();

 private:
  void chk_rec(const char* tag, const Rec& got, const Rec& want);
  void chk_cell(const char* tag, int sink, const Exp& e);

  Exp step(int sink, const Stim& s, bool check, const char* tag);
  Stim S_bind(uint64_t tk, uint16_t tu, uint64_t ct, bool sw);
  Stim S_unbind();
  Stim S_getrx();
  Stim S_probe(int sink, uint8_t status);
  Stim S_exp();
  Stim S_tk(uint8_t kind, bool fail = false);
  unsigned started_bit(int sink);
  void post_started(int sink, int val, bool fail = false);
  void goto_state(int sink, int st, const char* tag);

  void reset_and_init_sweep();
  void park_sink_seven();
  void walk_every_mtxw_cell();
  void check_duplicate_probe_is_byte_identical(int sink);
  void check_double_timeout_reaches_pwt(int sink);
  void check_dagger_dual_arms(int sink);
  void check_ref_bug_guard_at_sok(int sink);
  void check_registering_failed_is_visible(int sink);
  void check_unknown_listener_id();
  void check_foreign_eid_and_protocol_are_silent();
  void check_probe_guard_mismatch(int sink);
  void check_lock_gate(int sink);
  void check_boot_preload_lands_in_pwa();
  void check_stale_expiry_is_swallowed();
  void check_parked_sink_untouched();
  void check_started_face_follows_bind_and_request(int sk);
  void check_started_trigger_fires_once_per_transition(int sk);
  void check_streaming_wait_rules_started(int sk);
  void check_every_acceptor_excludes_the_holder_arm();
  void check_expiry_survives_a_colliding_request();
  void check_rebind_raises_no_duplicate_trigger();
  void check_started_face_error_paths(int sk);

  VKL_pp_acmp_listener* d;
  Harness h;
  Model m;
  Rec park7;
  int checks = 0;
  int fails = 0;
};

// ---- comparators ----------------------------------------------------------
void ListenerWalk::chk_rec(const char* tag, const Rec& got, const Rec& want) {
  CHECK(got.sm == want.sm, "%s: sm_state got %s want %s", tag,
        SN[got.sm & 7], SN[want.sm & 7]);
  CHECK(got.pbsta == want.pbsta && got.acmpsta == want.acmpsta,
        "%s: pbsta/acmpsta got %u/%u want %u/%u", tag, got.pbsta,
        got.acmpsta, want.pbsta, want.acmpsta);
  CHECK(got.bound == want.bound && got.started == want.started &&
        got.sw == want.sw && got.retried == want.retried &&
        got.srp_decl == want.srp_decl && got.tk_reg == want.tk_reg &&
        got.tk_disc == want.tk_disc,
        "%s: flags got b%d s%d w%d r%d d%u g%d t%d want b%d s%d w%d r%d d%u g%d t%d",
        tag, got.bound, got.started, got.sw, got.retried, got.srp_decl,
        got.tk_reg, got.tk_disc, want.bound, want.started, want.sw,
        want.retried, want.srp_decl, want.tk_reg, want.tk_disc);
  CHECK(got.talker_eid == want.talker_eid && got.talker_uid == want.talker_uid
        && got.bind_ctlr == want.bind_ctlr,
        "%s: binding got %016lx/%u/%016lx want %016lx/%u/%016lx", tag,
        static_cast<unsigned long>(got.talker_eid), got.talker_uid,
        static_cast<unsigned long>(got.bind_ctlr),
        static_cast<unsigned long>(want.talker_eid),
        want.talker_uid, static_cast<unsigned long>(want.bind_ctlr));
  CHECK(got.probe_seq == want.probe_seq, "%s: probe_seq got %u want %u",
        tag, got.probe_seq, want.probe_seq);
  CHECK(got.sid == want.sid && got.da == want.da && got.vlan == want.vlan,
        "%s: settled got %016lx/%012lx/%u want %016lx/%012lx/%u", tag,
        static_cast<unsigned long>(got.sid), static_cast<unsigned long>(got.da),
        got.vlan, static_cast<unsigned long>(want.sid),
        static_cast<unsigned long>(want.da), want.vlan);
  CHECK(got.smh == want.smh && got.noadp == want.noadp &&
        got.last_avail == want.last_avail,
        "%s: plumbing smh %u want %u", tag, got.smh, want.smh);
}

void ListenerWalk::chk_cell(const char* tag, int sink, const Exp& e) {
  CHECK(h.col.wrotes == (e.wrote ? 1 : 0), "%s: writebacks got %d want %d",
        tag, h.col.wrotes, e.wrote ? 1 : 0);
  CHECK(h.col.frames.size() == e.frames.size(), "%s: frames got %zu want %zu",
        tag, h.col.frames.size(), e.frames.size());
  for (size_t i = 0; i < e.frames.size() && i < h.col.frames.size(); ++i) {
    bool eq = memcmp(h.col.frames[i].b, e.frames[i].b, PDU_BYTES) == 0;
    CHECK(eq, "%s: frame %zu bytes differ", tag, i);
    if (!eq) {
      for (int k = 0; k < PDU_BYTES; ++k)
        if (h.col.frames[i].b[k] != e.frames[i].b[k])
          printf("    byte %d got %02x want %02x\n", k,
                 h.col.frames[i].b[k], e.frames[i].b[k]);
    }
  }
  CHECK(h.col.tops.size() == e.tops.size(), "%s: timer ops got %zu want %zu",
        tag, h.col.tops.size(), e.tops.size());
  for (size_t i = 0; i < e.tops.size() && i < h.col.tops.size(); ++i) {
    const ATop& g = h.col.tops[i];
    CHECK(g.cancel == e.tops[i].cancel && g.slot == TMR_BASE + sink &&
          g.owner == OWNER_BASE + sink &&
          (g.cancel || g.deadline == e.tops[i].deadline),
          "%s: timer op %zu got {c%d s%u o%u %u} want {c%d s%u o%u %u}", tag,
          i, g.cancel, g.slot, g.owner, g.deadline, e.tops[i].cancel,
          unsigned(TMR_BASE + sink), unsigned(OWNER_BASE + sink),
          e.tops[i].deadline);
  }
  CHECK(h.col.settle == e.settle && h.col.teardown == e.teardown &&
        h.col.disc_arm == e.disc_arm && h.col.disc_disarm == e.disc_disarm &&
        h.col.nvm == e.nvm && (!e.nvm || h.col.nvm_set == e.nvm_set),
        "%s: strobes got st%d td%d da%d dd%d nv%d/%d want st%d td%d da%d dd%d nv%d/%d",
        tag, h.col.settle, h.col.teardown, h.col.disc_arm, h.col.disc_disarm,
        h.col.nvm, h.col.nvm_set, e.settle, e.teardown, e.disc_arm,
        e.disc_disarm, e.nvm, e.nvm_set);
  if (e.settle)
    CHECK(h.col.settle_sid == e.settle_sid && h.col.settle_da == e.settle_da
          && h.col.settle_vlan == e.settle_vlan,
          "%s: settle payload got %016lx/%012lx/%u", tag,
          static_cast<unsigned long>(h.col.settle_sid),
          static_cast<unsigned long>(h.col.settle_da),
          h.col.settle_vlan);
  if (e.disc_arm)
    CHECK(h.col.disc_eid == e.disc_eid, "%s: disc payload got %016lx want %016lx",
          tag, static_cast<unsigned long>(h.col.disc_eid),
          static_cast<unsigned long>(e.disc_eid));
  CHECK(h.col.notifies == e.notify, "%s: notify got %d want %d", tag,
        h.col.notifies, e.notify);
  CHECK(h.col.frees == e.frees, "%s: rx frees got %d want %d", tag,
        h.col.frees, e.frees);
}

// ==========================================================================
// ---- helpers over harness + model in lock-step --------------------------
Exp ListenerWalk::step(int sink, const Stim& s, bool check, const char* tag) {
  h.col.clear();
  Exp e = m.predict(sink, s);
  bool done = h.drive(sink, s);
  CHECK(done, "%s: completes", tag);
  if (check) {
    chk_cell(tag, sink, e);
    chk_rec(tag, h.shadow[sink], m.rec[sink]);
  } else {
    CHECK(h.shadow[sink].sm == m.rec[sink].sm,
          "%s(setup): state sync got %s want %s", tag,
          SN[h.shadow[sink].sm & 7], SN[m.rec[sink].sm & 7]);
  }
  return e;
}

Stim ListenerWalk::S_bind(uint64_t tk, uint16_t tu, uint64_t ct, bool sw) {
  Stim s; s.k = Stim::TXN; s.msg = M_BIND; s.tk_eid = tk; s.tk_uid = tu;
  s.ctlr = ct; s.flags = sw ? 0x0008 : 0; s.seq = 0x4100; return s;
}

Stim ListenerWalk::S_unbind() {
  Stim s; s.k = Stim::TXN; s.msg = M_UNBIND; s.ctlr = CTL1;
  s.tk_eid = TK_A; s.tk_uid = TKUID_A; s.seq = 0x4200; return s;
}

Stim ListenerWalk::S_getrx() {
  Stim s; s.k = Stim::TXN; s.msg = M_GETRX; s.ctlr = CTL2; s.seq = 0x4300;
  return s;
}

Stim ListenerWalk::S_probe(int sink, uint8_t status) {
  const Rec& r = m.rec[sink];
  Stim s; s.k = Stim::TXN; s.msg = M_PROBE_RESP; s.status = status;
  s.ctlr = r.bind_ctlr; s.tk_eid = r.talker_eid; s.tk_uid = r.talker_uid;
  s.seq = r.probe_seq; s.sid = 0x5544332211002233ull + uint64_t(sink);
  s.da = 0x91E0F0004455ull; s.vlan = 2;
  return s;
}

Stim ListenerWalk::S_exp() { Stim s; s.k = Stim::EXP; return s; }

Stim ListenerWalk::S_tk(uint8_t kind, bool fail) {
  Stim s; s.k = Stim::TK; s.tk_kind = kind; s.tk_fail = fail; return s;
}

  // ---- the exported started/stopped view (Milan 5.3.8.7) ----------------
  // The fabric admission gate reads this vector, NOT the record RAM, so a
  // record that says started while the vector says stopped would discard
  // every frame of a stream the controller was told is running. It is
  // written off the record RAM's own write bus, and this is what proves it.
unsigned ListenerWalk::started_bit(int sink) {
  return static_cast<unsigned>((d->strm_started_o >> sink) & 1u);
}

  //! Drive the AECP request face. Ready is completion, not holder space, so
  //! the record or required no-op check has finished when it rises.
void ListenerWalk::post_started(int sink, int val, bool fail) {
  d->strm_set_valid_i = 1;
  d->strm_set_sink_i  = uint16_t(sink);
  d->strm_set_val_i   = uint8_t(val);
  int guard = 64;
  int cycles = 0;
  while (guard-- > 0 && !d->strm_set_ready_o) {
    h.tick();
    cycles++;
  }
  CHECK(d->strm_set_ready_o == 1,
        "post_started(%d,%d): the face completed", sink, val);
  CHECK(cycles >= 2,
        "post_started(%d,%d): holder capture was not completion", sink, val);
  CHECK(bool(d->strm_set_error_o) == fail,
        "post_started(%d,%d): error got %u want %u", sink, val,
        unsigned(d->strm_set_error_o), unsigned(fail));
  h.tick();                       // retire the completion handshake
  d->strm_set_valid_i = 0;
  d->eval();
}

void ListenerWalk::goto_state(int sink, int st, const char* tag) {
  Stim b = S_bind(TK_A, TKUID_A, CTL1, false); b.uid = uint16_t(sink);
  Stim u = S_unbind(); u.uid = uint16_t(sink);
  step(sink, u, false, tag);                    // any state -> UNB
  if (st == S_UNB) return;
  step(sink, b, false, tag);                    // UNB -> PWR
  if (st == S_PWR) return;
  Stim s;
  switch (st) {
    case S_PWA:
      s = S_tk(1); step(sink, s, false, tag); break;      // DEP -> PWA
    case S_PWD:
      s = S_tk(1); step(sink, s, false, tag);
      s = S_tk(0); step(sink, s, false, tag); break;      // DISC -> PWD
    case S_PW2:
      step(sink, S_exp(), false, tag); break;             // CMD -> PW2
    case S_PWT: {
      Stim p = S_probe(sink, ST_NOBW); p.uid = uint16_t(sink);
      step(sink, p, false, tag); break;                   // fail -> PWT
    }
    case S_SNR: case S_SOK: {
      Stim p = S_probe(sink, ST_OK); p.uid = uint16_t(sink);
      step(sink, p, false, tag);                          // ok -> SNR
      if (st == S_SOK) { s = S_tk(2); step(sink, s, false, tag); }
      break;
    }
    default: break;
  }
}

  // ---- reset + init sweep -------------------------------------------------
void ListenerWalk::reset_and_init_sweep() {
  d->rst_n = 0; d->txn_valid_i = 0; d->evt_tk_valid_i = 0;
  d->pre_valid_i = 0; d->lock_held_i = 0; d->lock_ctlr_i = 0;
  d->entity_id_i = OUR_EID;
  for (int i = 0; i < 4; ++i) h.tick();
  d->rst_n = 1;
  for (int i = 0; i < 12; ++i) h.tick();
  CHECK(d->txn_ready_o == 1, "idle after reset + init sweep");
  {
    bool allz = true;
    for (int i = 0; i < N_SINKS; ++i) allz &= (h.shadow[i] == Rec());
    CHECK(allz, "init sweep zeroed all %d records", N_SINKS);
  }
  h.col.clear();
}

  // ---- park sink 7 in a settled state for the isolation check -------------
void ListenerWalk::park_sink_seven() {
  goto_state(7, S_SOK, "park7");
  park7 = m.rec[7];
}

  // ======================= THE MTXW WALK ==================================
  // every (event row x state) cell of F05.3; aliased timer '—' cells are
  // proven impossible-by-construction (own-T-ID deadline check) instead of
  // injected — the shared SM slot cannot carry the foreign T-ID.
void ListenerWalk::walk_every_mtxw_cell() {
  static constexpr int OWN_MS[N_STATES] = {-1, -1, DRAWVAL, T_CMD, T_CMD,
                                           T_RETRY, T_NOTK, -1};
  int cells = 0;
  for (int row = 0; row < N_ROWS; ++row) {
    for (int st = 0; st < N_STATES; ++st) {
      char tag[64];
      snprintf(tag, sizeof tag, "F05.3 %s x %s", RN[row], SN[st]);
      int sink = (row * 8 + st) % 7;   // sink 7 stays parked
      goto_state(sink, st, tag);
      ++cells;

      if (row >= R_TMR_DELAY && row <= R_TMR_NOTK) {
        bool own = (row == R_TMR_DELAY && st == S_PWD) ||
                   (row == R_TMR_CMD && (st == S_PWR || st == S_PW2)) ||
                   (row == R_TMR_RETRY && st == S_PWT) ||
                   (row == R_TMR_NOTK && st == S_SNR);
        if (own) {
          step(sink, S_exp(), true, tag);
        } else if (OWN_MS[st] < 0) {
          // no SM timer armed here: inject a spurious expiry, prove inert
          CHECK(M[row][st].t == C_DASH, "%s: model marks the cell em-dash",
                tag);
          step(sink, S_exp(), true, tag);
        } else {
          // aliased '—': the armed deadline is the state's own T-ID, so
          // this row's expiry cannot exist in this state
          CHECK(M[row][st].t == C_DASH, "%s: model marks the cell em-dash",
                tag);
          CHECK(h.last_arm_deadline[sink] == NOW + uint32_t(OWN_MS[st]),
                "%s: armed deadline %u proves the slot carries the state's "
                "own T-ID (+%d)", tag, h.last_arm_deadline[sink], OWN_MS[st]);
        }
        continue;
      }

      Stim s;
      switch (row) {
        case R_BIND_SAME:
          // craft 'same' from the model record; in UNB nothing is bound and
          // the classifier MUST take the new-source row (the '—' proof)
          s = S_bind(m.rec[sink].talker_eid, m.rec[sink].talker_uid, CTL2,
                     true);
          s.uid = uint16_t(sink);
          {
            Exp e = step(sink, s, true, tag);
            if (st == S_UNB)
              CHECK(e.row == R_BIND_NEW,
                    "%s: unreachable cell — classified as BIND_NEW", tag);
          }
          break;
        case R_BIND_NEW:
          s = S_bind(TK_B, TKUID_B, CTL1, false); s.uid = uint16_t(sink);
          step(sink, s, true, tag);
          break;
        case R_UNBIND:
          s = S_unbind(); s.uid = uint16_t(sink);
          step(sink, s, true, tag);
          break;
        case R_GETRX:
          s = S_getrx(); s.uid = uint16_t(sink);
          step(sink, s, true, tag);
          break;
        case R_PROBE_OK:
          s = S_probe(sink, ST_OK); s.uid = uint16_t(sink);
          step(sink, s, true, tag);
          break;
        case R_PROBE_FAIL:
          s = S_probe(sink, ST_NOBW); s.uid = uint16_t(sink);
          step(sink, s, true, tag);
          break;
        case R_TK_DISC: case R_TK_DEP: case R_TK_UNREG:
          s = S_tk(uint8_t(row - R_TK_DISC));
          step(sink, s, true, tag);
          break;
        case R_TK_REG:
          // Failed attr on purpose: at SOK this is the REF-BUG guard cell
          s = S_tk(2, st == S_SOK);
          step(sink, s, true, tag);
          break;
        default: break;
      }
    }
  }
  CHECK(cells == 112, "MTXW walked %d cells (want 112)", cells);
}

  // B1: exact-duplicate probe — A13 bytes == A5 bytes, same seq, retried
void ListenerWalk::check_duplicate_probe_is_byte_identical(int sink) {
  goto_state(sink, S_PWR, "B1");
  Pdu probe1 = h.col.frames.empty() ? Pdu{} : h.col.frames.back();
  {
    // re-collect probe #1 from a fresh bind for byte identity
    goto_state(sink, S_UNB, "B1");
    Stim b = S_bind(TK_A, TKUID_A, CTL1, false); b.uid = uint16_t(sink);
    h.col.clear();
    Exp e = m.predict(sink, b);
    CHECK(h.drive(sink, b), "B1: bind completes");
    CHECK(h.col.frames.size() == 2, "B1: bind resp + probe #1");
    if (h.col.frames.size() == 2) probe1 = h.col.frames[1];
    (void)e;
    uint16_t seq1 = m.rec[sink].probe_seq;
    step(sink, S_exp(), true, "B1 dup");           // PWR -CMD-> PW2 (A13)
    CHECK(!h.col.frames.empty() &&
          memcmp(h.col.frames[0].b, probe1.b, PDU_BYTES) == 0,
          "B1: probe #2 is the exact duplicate of probe #1");
    CHECK(m.rec[sink].probe_seq == seq1 && h.shadow[sink].probe_seq == seq1,
          "B1: same probe_seq %u", seq1);
    CHECK(h.shadow[sink].retried, "B1: retried flag set");
  }
}

  // B2: double timeout -> PWT with acmpsta 7, T-ACMP-RETRY armed
void ListenerWalk::check_double_timeout_reaches_pwt(int sink) {
  step(sink, S_exp(), true, "B2 dbl-timeout");     // PW2 -CMD-> PWT A14(=7)
  CHECK(h.shadow[sink].sm == S_PWT && h.shadow[sink].acmpsta == ST_TT,
        "B2: PWT with acmpsta LISTENER_TALKER_TIMEOUT got %s/%u",
        SN[h.shadow[sink].sm & 7], h.shadow[sink].acmpsta);
}

  // B3: dagger dual arms
  //   PWT + tk_disc: T-ACMP-RETRY -> PWD / A12 (walk covered the !tk arm)
void ListenerWalk::check_dagger_dual_arms(int sink) {
  { Stim s = S_tk(0); step(sink, s, false, "B3"); }  // ign cell sets tk_disc
  step(sink, S_exp(), true, "B3 RETRY tk arm");
  CHECK(h.shadow[sink].sm == S_PWD, "B3: RETRY with talker -> PWD got %s",
        SN[h.shadow[sink].sm & 7]);
  //   SNR + tk: NOTK -> A8 + PWD / A12
  goto_state(sink, S_SNR, "B3b");
  { Stim s = S_tk(0); step(sink, s, false, "B3b"); }
  step(sink, S_exp(), true, "B3b NOTK tk arm");
  CHECK(h.shadow[sink].sm == S_PWD, "B3b: NOTK with talker -> PWD got %s",
        SN[h.shadow[sink].sm & 7]);
  //   SOK + tk: UNREG -> A8 + PWD / A12
  goto_state(sink, S_SOK, "B3c");
  { Stim s = S_tk(0); step(sink, s, false, "B3c"); }
  { Stim s = S_tk(3); step(sink, s, true, "B3c UNREG tk arm"); }
  CHECK(h.shadow[sink].sm == S_PWD, "B3c: UNREG with talker -> PWD got %s",
        SN[h.shadow[sink].sm & 7]);
}

  // B4: REF-BUG guard — TalkerFailed rise in SETTLED_RSV_OK is inert
void ListenerWalk::check_ref_bug_guard_at_sok(int sink) {
  goto_state(sink, S_SOK, "B4");
  { Stim s = S_tk(2, true); step(sink, s, true, "B4 REF-BUG"); }
  CHECK(h.shadow[sink].sm == S_SOK && !((h.shadow[sink].srp_decl >> 1) & 1),
        "B4: no invented arc, no RF latch from the spurious rise");
}

  // B5: REGISTERING_FAILED visible — settle then register a Failed attr
void ListenerWalk::check_registering_failed_is_visible(int sink) {
  goto_state(sink, S_SNR, "B5");
  { Stim s = S_tk(2, true); step(sink, s, true, "B5 reg-failed"); }
  { Stim g = S_getrx(); g.uid = uint16_t(sink); h.col.clear();
    Exp e = m.predict(sink, g);
    CHECK(h.drive(sink, g), "B5: GET_RX_STATE completes");
    CHECK(!h.col.frames.empty() &&
          (uint16_t(h.col.frames[0].b[50]) << 8 | h.col.frames[0].b[51]) ==
          (0x0002 | 0x0040),
          "B5: flags carry REGISTERING_FAILED 0x0040");
    chk_cell("B5", sink, e);
  }
}

  // B6: LISTENER_UNKNOWN_ID for the three commands; probe resp dropped
void ListenerWalk::check_unknown_listener_id() {
  char tg[64];
  for (uint8_t mm : {uint8_t(M_BIND), uint8_t(M_UNBIND), uint8_t(M_GETRX)}) {
    snprintf(tg, sizeof tg, "B6 msg %u uid 8", mm);
    Stim s; s.k = Stim::TXN; s.msg = mm; s.uid = N_SINKS; s.ctlr = CTL1;
    s.tk_eid = TK_A; s.tk_uid = TKUID_A; s.seq = 0x5000;
    h.col.clear();
    Exp e = m.predict(0, s);
    CHECK(h.drive(0, s), "%s completes", tg);
    chk_cell(tg, 0, e);
    CHECK(!h.col.frames.empty() && (h.col.frames[0].b[2] >> 3) == ST_LUID,
          "%s: status LISTENER_UNKNOWN_ID", tg);
  }
  { Stim s; s.k = Stim::TXN; s.msg = M_PROBE_RESP; s.uid = N_SINKS;
    h.col.clear();
    Exp e = m.predict(0, s);
    CHECK(h.drive(0, s), "B6 probe uid 8 completes");
    chk_cell("B6 probe uid 8 (silent)", 0, e); }
}

  // B7: foreign listener EID and foreign protocol are consumed silently
void ListenerWalk::check_foreign_eid_and_protocol_are_silent() {
  { Stim s = S_bind(TK_A, TKUID_A, CTL1, false); s.target = 0xDEAD0001;
    h.col.clear(); Exp e = m.predict(0, s);
    CHECK(h.drive(0, s), "B7 foreign EID completes");
    chk_cell("B7 foreign EID", 0, e); }
  { Stim s = S_bind(TK_A, TKUID_A, CTL1, false); s.protocol = 2;  // AEM
    h.col.clear(); Exp e = m.predict(0, s);
    CHECK(h.drive(0, s), "B7 foreign protocol completes");
    chk_cell("B7 foreign protocol", 0, e); }
}

  // B8: probe-response guard mismatch (wrong seq) silently ignored
void ListenerWalk::check_probe_guard_mismatch(int sink) {
  goto_state(sink, S_PWR, "B8");
  { Stim s = S_probe(sink, ST_OK); s.uid = uint16_t(sink);
    s.seq = uint16_t(s.seq + 1);
    h.col.clear(); Exp e = m.predict(sink, s);
    CHECK(h.drive(sink, s), "B8 completes");
    chk_cell("B8 guard mismatch", sink, e);
    CHECK(h.col.wrotes == 0 && h.col.frees == 1,
          "B8: no write-back, slot returned");
    CHECK(h.shadow[sink].sm == S_PWR, "B8: still PRB_W_RESP"); }
}

  // B9: A1 lock gate — BIND/UNBIND blocked for a foreign holder,
  // unaffected for the holder itself and for GET_RX_STATE
void ListenerWalk::check_lock_gate(int sink) {
  d->lock_held_i = 1; d->lock_ctlr_i = CTL2;
  m.lock_held = true; m.lock_eid = CTL2;
  { Stim s = S_bind(TK_B, TKUID_B, CTL1, false); s.uid = uint16_t(sink);
    h.col.clear(); Exp e = m.predict(sink, s);
    CHECK(h.drive(sink, s), "B9 locked bind completes");
    chk_cell("B9 locked bind", sink, e);
    CHECK(!h.col.frames.empty() && (h.col.frames[0].b[2] >> 3) == ST_NOAUTH,
          "B9: CONTROLLER_NOT_AUTHORIZED");
    CHECK(h.shadow[sink].sm == S_PWR && h.col.wrotes == 0,
          "B9: cell aborted, no commit"); }
  { Stim s = S_unbind(); s.uid = uint16_t(sink);
    h.col.clear(); Exp e = m.predict(sink, s);
    CHECK(h.drive(sink, s), "B9 locked unbind completes");
    chk_cell("B9 locked unbind", sink, e); }
  { Stim g = S_getrx(); g.uid = uint16_t(sink); g.ctlr = CTL1;
    h.col.clear(); Exp e = m.predict(sink, g);
    CHECK(h.drive(sink, g), "B9 GET_RX_STATE under lock completes");
    chk_cell("B9 getrx under lock", sink, e);
    CHECK(!h.col.frames.empty() && (h.col.frames[0].b[2] >> 3) == ST_OK,
          "B9: GET_RX_STATE unaffected by the lock"); }
  { Stim s = S_bind(TK_B, TKUID_B, CTL2, true); s.uid = uint16_t(sink);
    h.col.clear(); Exp e = m.predict(sink, s);
    CHECK(h.drive(sink, s), "B9 holder bind completes");
    chk_cell("B9 holder bind", sink, e);
    CHECK(h.shadow[sink].talker_eid == TK_B,
          "B9: the lock holder's bind commits"); }
  d->lock_held_i = 0; m.lock_held = false;
}

  // B10: boot preload -> PRB_W_AVAIL with discovery armed (07 §5.3)
void ListenerWalk::check_boot_preload_lands_in_pwa() {
  goto_state(2, S_UNB, "B10");
  h.col.clear();
  d->pre_valid_i = 1; d->pre_sink_i = 2; d->pre_talker_eid_i = TK_A;
  d->pre_talker_uid_i = TKUID_A; d->pre_ctlr_eid_i = CTL1;
  d->pre_sw_i = 1; d->pre_started_i = 1;
  h.tick(); d->pre_valid_i = 0; h.tick(); h.wait_idle(); h.tick();
  {
    Rec& r = m.rec[2];
    r = Rec(); r.sm = S_PWA; r.pbsta = 1; r.bound = true; r.sw = true;
    r.started = true; r.talker_eid = TK_A; r.talker_uid = TKUID_A;
    r.bind_ctlr = CTL1; r.smh = uint8_t(TMR_BASE + 2);
    chk_rec("B10 preload", h.shadow[2], r);
    CHECK(h.col.disc_arm && h.col.disc_eid == TK_A,
          "B10: A4 discovery arm with the restored talker");
    // The restored bit must reach the ADMISSION VIEW, not just the record.
    // The mirror claims "one write, two destinations" over every path
    // including X_PRELOAD, and this is the only place that path is taken:
    // without this row, a mirror that ignored the preload would leave a
    // rebooted device reporting a started sink while discarding every frame.
    CHECK(started_bit(2) == 1,
          "B10: the RESTORED started bit reached the admission view (got %u)",
          started_bit(2));
    CHECK(h.col.wrotes == 1 && h.col.notifies == 0,
          "B10: one record write, no notification at boot");
  }
  { Stim s = S_tk(0); step(2, s, true, "B10 disc after preload"); }
  CHECK(h.shadow[2].sm == S_PWD, "B10: preloaded sink probes on discovery");
}

  // B11: A11 swallows a stale pending expiry (cancel wins the race)
void ListenerWalk::check_stale_expiry_is_swallowed() {
  goto_state(3, S_PWR, "B11");
  { Stim p = S_probe(3, ST_OK); p.uid = 3;
    h.col.clear();
    Exp e = m.predict(3, p);
    // expiry lands the same tick the settle txn arrives: txn wins dispatch,
    // A11 must clear the pend bit, and NO second work item may run
    int slot = h.next_rx_slot; h.next_rx_slot = (h.next_rx_slot + 1) % 4;
    Pdu pd = mk_pdu(p.msg, p.status, p.sid, p.ctlr, p.tk_eid, p.target,
                    p.tk_uid, p.uid, p.da, 0, p.seq, p.flags, p.vlan);
    memcpy(h.rxmem[slot], pd.b, PDU_BYTES);
    uint32_t* w = &d->txn_i[0];
    for (int i = 0; i < 13; ++i) w[i] = 0;
    wput(w, 354, 3, 1); wput(w, 350, 4, p.msg); wput(w, 345, 5, p.status);
    wput(w, 222, 64, p.ctlr); wput(w, 158, 64, p.target);
    wput(w, 142, 16, p.seq); wput(w, 60, 16, p.uid);
    wput(w, 57, 3, uint64_t(slot)); wput(w, 0, 2, 1);
    d->txn_valid_i = 1;
    h.inj_exp = true; h.inj_exp_sink = 3;
    h.tick();
    d->txn_valid_i = 0;
    h.tick(); h.wait_idle(); h.tick();
    chk_cell("B11 settle beats stale expiry", 3, e);
    // the swallowed expiry must never surface: a long quiet window with
    // ZERO activity (a second work item would need ~24 cycles to retire)
    h.col.clear();
    for (int i = 0; i < 60; ++i) h.tick();
    CHECK(h.col.wrotes == 0 && !h.col.teardown && h.col.tops.empty() &&
          h.col.notifies == 0 && h.shadow[3].sm == S_SNR,
          "B11: no second work item; still SETTLED_NO_RSV (got sm %s, "
          "wr %d td %d tops %zu nf %d)", SN[h.shadow[3].sm & 7],
          h.col.wrotes, h.col.teardown, h.col.tops.size(),
          h.col.notifies); }
}

  // B12: cross-sink isolation — the parked sink was never touched
void ListenerWalk::check_parked_sink_untouched() {
  CHECK(h.shadow[7] == park7 && m.rec[7] == park7,
        "B12: parked sink 7 record untouched through the whole walk");
}

  // ---- S1: the started/stopped face (Milan 5.3.8.7, 5.4.2.19/.20) -------
void ListenerWalk::check_started_face_follows_bind_and_request(int sk) {
  Stim u = S_unbind(); u.uid = uint16_t(sk);
  step(sk, u, false, "S1");
  CHECK(started_bit(sk) == 0,
        "S1a: an unbound sink reports stopped (got %u)", started_bit(sk));

  // a bind with STREAMING_WAIT CLEAR lands STARTED (IEEE 7.4.35's premise:
  // START_STREAMING exists for a stream connected WITH the flag set)
  Stim b0 = S_bind(TK_A, TKUID_A, CTL1, false); b0.uid = uint16_t(sk);
  step(sk, b0, false, "S1");
  CHECK(started_bit(sk) == 1,
        "S1b: a bind with STREAMING_WAIT clear lands STARTED (got %u)",
        started_bit(sk));

  // the AECP request face: stop it
  h.wait_idle();
  CHECK(d->strm_set_ready_o == 0,
        "S1c: idle is not completion before a request exists");
  // S1c2: capture and completion are separate. Ready must stay low until
  // the record write has reached the fabric-facing started mirror.
  {
    d->strm_set_valid_i = 1;
    d->strm_set_sink_i  = uint16_t(sk);
    d->strm_set_val_i   = 0;
    h.tick();                       // internal holder capture
    d->eval();
    CHECK(d->strm_set_ready_o == 0,
          "S1c2: holder capture is not reported as completion");
    int g = 64;
    while (g-- > 0 && !d->strm_set_ready_o) h.tick();
    d->eval();
    CHECK(d->strm_set_ready_o == 1,
          "S1c3: completion rises after the walker commits");
    CHECK(started_bit(sk) == 0,
          "S1c4: the started mirror is committed at completion");
    h.tick();
    d->strm_set_valid_i = 0;
    d->eval();
    CHECK(d->strm_set_ready_o == 0,
          "S1c5: completion retires with the held request");
  }
  CHECK(started_bit(sk) == 0,
        "S1d: STOP through the request face cleared the bit (got %u)",
        started_bit(sk));

  // ...and start it again
  post_started(sk, 1);
  CHECK(started_bit(sk) == 1,
        "S1e: START through the request face set the bit (got %u)",
        started_bit(sk));
}

void ListenerWalk::check_started_trigger_fires_once_per_transition(int sk) {
  // Table 5.22 + IEEE 7.4.35: a REAL transition pushes exactly one
  // GET_STREAM_INFO unsolicited notification...
  h.col.clear();
  post_started(sk, 0);
  CHECK(h.col.strt_chgs == 1,
        "S1i: a real STOP raises the Table 5.22 trigger once (got %d)",
        h.col.strt_chgs);
  // ...and repeating it changes nothing, so it must push NOTHING. A
  // notification saying "the state you already knew about" is worse than
  // none: it is indistinguishable on the wire from a real change.
  h.col.clear();
  post_started(sk, 0);
  CHECK(h.col.strt_chgs == 0,
        "S1j: a repeated STOP raises NO trigger (got %d)",
        h.col.strt_chgs);
  CHECK(started_bit(sk) == 0, "S1j2: ...and the bit is still clear");
  post_started(sk, 1);
}

void ListenerWalk::check_streaming_wait_rules_started(int sk) {
  // 5.3.8.7: unbind clears it, and a rebind does not resurrect it
  Stim u2 = S_unbind(); u2.uid = uint16_t(sk);
  step(sk, u2, false, "S1");
  CHECK(started_bit(sk) == 0,
        "S1f: unbind cleared the started bit (got %u)", started_bit(sk));

  // a bind WITH STREAMING_WAIT set lands STOPPED - the other half of the
  // rule, and the row that keeps S1b from passing on a constant 1
  Stim b1 = S_bind(TK_A, TKUID_A, CTL1, true); b1.uid = uint16_t(sk);
  step(sk, b1, false, "S1");
  CHECK(started_bit(sk) == 0,
        "S1g: a bind WITH STREAMING_WAIT lands STOPPED (got %u)",
        started_bit(sk));

  // S1k: a RE-BIND that flips STREAMING_WAIT moves started/stopped with no
  // START/STOP_STREAMING in sight (Milan 5.5.3.5.6 step 2 updates the
  // binding parameters, STREAMING_WAIT among them). Table 5.22 asks for a
  // push when the state CHANGES, not when a particular command caused it -
  // a trigger keyed on the AECP request alone missed this path entirely.
  {
    Stim b_on = S_bind(TK_A, TKUID_A, CTL1, false); b_on.uid = uint16_t(sk);
    step(sk, b_on, false, "S1");            // -> bound + started
    CHECK(started_bit(sk) == 1, "S1k0: precondition, re-bound and started");

    h.col.clear();
    Stim b_off = S_bind(TK_A, TKUID_A, CTL1, true); b_off.uid = uint16_t(sk);
    step(sk, b_off, false, "S1");           // same talker -> A6 short-circuit
    CHECK(started_bit(sk) == 0,
          "S1k: a re-bind WITH STREAMING_WAIT stops the sink (got %u)",
          started_bit(sk));
    CHECK(h.col.strt_chgs == 1,
          "S1l: ...and it raises the Table 5.22 trigger (got %d)",
          h.col.strt_chgs);

    h.col.clear();
    Stim b_same = S_bind(TK_A, TKUID_A, CTL1, true); b_same.uid = uint16_t(sk);
    step(sk, b_same, false, "S1");          // same flag: nothing changes
    CHECK(h.col.strt_chgs == 0,
          "S1m: a re-bind that changes nothing raises no trigger (got %d)",
          h.col.strt_chgs);
  }
}

void ListenerWalk::check_every_acceptor_excludes_the_holder_arm() {
  // ---- RV: the holder arm sits at the TOP of the X_IDLE priority chain,
  // so EVERY acceptor has to exclude it. On the cycle the holder drains,
  // this walker is leaving X_IDLE - and a source still told "ready" on
  // that cycle is consumed by its producer and never serviced. Fixing only
  // `pre_ready_o` left three others, and the `txn_ready_o` one silently
  // drops an ACMP command AND leaks one of four shared RX slots for good.
  // These rows post a request by hand and inspect ready on the drain cycle.
  {
    const int rvs = 6;                       // a sink this walk left alone
    d->strm_set_valid_i = 1;
    d->strm_set_sink_i  = uint16_t(rvs);
    d->strm_set_val_i   = 1;
    h.tick();                                // holder captured
    d->eval();
    CHECK(d->strm_set_ready_o == 0, "RV0: precondition, a request is pending");
    CHECK(d->txn_ready_o == 0,
          "RV3: txn_ready_o is LOW while a started/stopped request is "
          "pending - otherwise KL_pp_dispatch pops an ACMP command that "
          "this walk will never service, and its RX slot leaks");
    CHECK(d->evt_tk_ready_o == 0,
          "RV5: evt_tk_ready_o is LOW on the same cycle - the event router "
          "acks on it, so a talker event would be dropped");
    CHECK(d->pre_ready_o == 0,
          "RV6: pre_ready_o is LOW on the same cycle - the NVM shadow "
          "treats it as acceptance and would advance past a restored sink");
    int g = 64;
    while (g-- > 0 && !d->strm_set_ready_o) h.tick();
    h.tick();
    d->strm_set_valid_i = 0;
    d->eval();
    CHECK(d->txn_ready_o == 1,
          "RV7: ...and every acceptor is free again once it has drained");
  }
}

void ListenerWalk::check_expiry_survives_a_colliding_request() {
  // RV4: a timer expiry pending at the same moment as a started/stopped
  // request must still be SERVICED. `pend_clr_pop_w` clears the pendexp
  // bit, so if it fires on the drain cycle the expiry is consumed by
  // nothing - and a lost T-ACMP-CMD leaves the sink in PB_ACTIVE with no
  // retry. Park a probing sink, then collide the two.
  {
    const int rvt = 4;
    goto_state(rvt, S_PWR, "RV4");          // a sink with a live timer
    h.wait_idle();
    h.col.clear();

    // post the request, then raise the expiry while the holder is FULL
    d->strm_set_valid_i = 1;
    d->strm_set_sink_i  = uint16_t(rvt);
    d->strm_set_val_i   = 1;
    //! BOTH on the same edge. Raising the expiry a cycle later misses the
    //! window entirely: the walker has already left X_IDLE for the holder
    //! job by then, and `pend_clr_pop_w` needs `xs_r == X_IDLE`. The bug
    //! only exists on the ONE cycle where the drain and a pending expiry
    //! are both true.
    h.inj_exp = true; h.inj_exp_sink = uint8_t(rvt);
    h.tick();                               // holder captured + pendexp set
    int g = 64;
    while (g-- > 0 && !d->strm_set_ready_o) h.tick();
    h.tick();
    d->strm_set_valid_i = 0;
    for (int i = 0; i < 200; ++i) h.tick();
    h.wait_idle();

    const size_t tops_collided = h.col.tops.size();

    // CONTROL: the same expiry with NO request beside it. Without this the
    // row above has no scale - "some timer op happened" passes for many
    // reasons, and a check whose expected value is "not zero" is the trap
    // this suite exists to avoid.
    goto_state(rvt, S_PWR, "RV4");
    h.wait_idle();
    h.col.clear();
    h.inj_exp = true; h.inj_exp_sink = uint8_t(rvt);
    h.tick();
    for (int i = 0; i < 200; ++i) h.tick();
    h.wait_idle();
    const size_t tops_alone = h.col.tops.size();

    CHECK(tops_alone > 0,
          "RV4pre: the control leg's expiry IS serviced (%zu timer ops) - "
          "without this the comparison below means nothing", tops_alone);
    CHECK(tops_collided == tops_alone,
          "RV4: an expiry raised beside a started/stopped request is "
          "serviced exactly as it is alone (collided %zu vs alone %zu) - "
          "a pop that fires on the drain cycle loses it",
          tops_collided, tops_alone);
  }
}

void ListenerWalk::check_rebind_raises_no_duplicate_trigger() {
  // RV8: a BIND_NEW onto an ALREADY BOUND sink changes started/stopped
  // without ever unbinding (its cell is A1 A11 A9 A2 A3 A4 A5 - no A10),
  // and it already pushes from A4's discovery arm. It must NOT also raise
  // the started/stopped trigger, or one event puts two GET_STREAM_INFO
  // frames on the wire - the duplicate this trigger was narrowed to avoid.
  {
    const int rvb = 2;
    Stim ba = S_bind(TK_A, TKUID_A, CTL1, false); ba.uid = uint16_t(rvb);
    step(rvb, ba, false, "RV8");             // bound + started
    h.wait_idle();
    CHECK(started_bit(rvb) == 1, "RV8pre: bound to talker A and started");

    h.col.clear();
    Stim bb = S_bind(TK_B, TKUID_B, CTL1, true); bb.uid = uint16_t(rvb);
    step(rvb, bb, false, "RV8");             // different talker, SW set
    h.wait_idle();
    CHECK(started_bit(rvb) == 0,
          "RV8: the re-bind landed STOPPED (got %u)", started_bit(rvb));
    CHECK(h.col.strt_chgs == 0,
          "RV8b: ...and raised NO started/stopped trigger beside the "
          "bind's own notification (got %d)", h.col.strt_chgs);
  }
}

void ListenerWalk::check_started_face_error_paths(int sk) {
  // an unbound sink ignores the request entirely (5.4.2.19's Note)
  Stim u3 = S_unbind(); u3.uid = uint16_t(sk);
  step(sk, u3, false, "S1");

  // S1o: a walker that cannot retire must not stall the AECP execution
  // stage forever. Hold an ordinary ACMP response at TX allocation, post a
  // started request behind it, and require the bounded error completion to
  // leave the record untouched.
  {
    Stim stuck = S_getrx();
    stuck.uid = uint16_t(N_SINKS + 1);       // forces an error response
    const int slot = h.next_rx_slot;
    h.next_rx_slot = (h.next_rx_slot + 1) % 4;
    Pdu p = mk_pdu(stuck.msg, stuck.status, stuck.sid, stuck.ctlr,
                   stuck.tk_eid, stuck.target, stuck.tk_uid, stuck.uid,
                   stuck.da, 0, stuck.seq, stuck.flags, stuck.vlan);
    memcpy(h.rxmem[slot], p.b, PDU_BYTES);
    uint32_t* w = &d->txn_i[0];
    for (int i = 0; i < 13; ++i) w[i] = 0;
    wput(w, 354, 3, stuck.protocol);
    wput(w, 350, 4, stuck.msg);
    wput(w, 345, 5, stuck.status);
    wput(w, 334, 11, 44);
    wput(w, 222, 64, stuck.ctlr);
    wput(w, 158, 64, stuck.target);
    wput(w, 142, 16, stuck.seq);
    wput(w, 124, 16, stuck.msg);
    wput(w, 60, 16, stuck.uid);
    wput(w, 57, 3, uint64_t(slot));
    wput(w, 0, 2, 1);

    h.alloc_block = true;
    d->txn_valid_i = 1;
    h.tick();
    d->txn_valid_i = 0;
    for (int i = 0; i < 80; ++i) h.tick();
    CHECK(d->dbg_busy_o == 1,
          "S1o0: the control walk is blocked at response allocation");

    const unsigned before_started = started_bit(sk);
    d->strm_set_valid_i = 1;
    d->strm_set_sink_i  = uint16_t(sk);
    d->strm_set_val_i   = 1;
    int g = 96;
    while (g-- > 0 && !d->strm_set_ready_o) h.tick();
    CHECK(d->strm_set_ready_o == 1 && d->strm_set_error_o == 1,
          "S1o: a blocked walker returns bounded error completion");
    CHECK(started_bit(sk) == before_started,
          "S1o2: timeout has no record side effect");
    h.tick();
    d->strm_set_valid_i = 0;
    h.alloc_block = false;
    CHECK(h.drain(), "S1o3: the original ACMP walk retires after release");
  }

  // S1n: an out-of-range sink index is accepted (the engine already
  // answered) and DROPPED - counted, not silent. The shape gate ties the
  // descriptor count to N_SINKS_P so this should be unreachable in a real
  // build; a stale descriptor image shipped beside the bitstream is how it
  // would stop being unreachable, and then the command answers SUCCESS and
  // lands nowhere. Driving it here is what makes that arm exist.
  {
    const int before = static_cast<int>(d->dbg_strq_drop_o);
    post_started(N_SINKS + 3, 1, true);
    CHECK(static_cast<int>(d->dbg_strq_drop_o) == before + 1,
          "S1n: an out-of-range started/stopped request is COUNTED "
          "(%d -> %d)", before, static_cast<int>(d->dbg_strq_drop_o));
    CHECK(d->strm_set_error_o == 0 && d->strm_set_ready_o == 0,
          "S1n2: the failed completion retired cleanly");
  }

  post_started(sk, 1);
  CHECK(started_bit(sk) == 0,
        "S1h: START on an UNBOUND sink changed nothing (got %u)",
        started_bit(sk));
}

int ListenerWalk::run() {
  reset_and_init_sweep();
  park_sink_seven();
  walk_every_mtxw_cell();

  // ================== behavior checks beyond the walk =====================
  int sink = 0;

  check_duplicate_probe_is_byte_identical(sink);
  check_double_timeout_reaches_pwt(sink);
  check_dagger_dual_arms(sink);
  check_ref_bug_guard_at_sok(sink);
  check_registering_failed_is_visible(sink);
  check_unknown_listener_id();
  check_foreign_eid_and_protocol_are_silent();
  check_probe_guard_mismatch(sink);
  check_lock_gate(sink);
  check_boot_preload_lands_in_pwa();
  check_stale_expiry_is_swallowed();
  check_parked_sink_untouched();

  const int sk = 5;                       // a sink this walk left alone
  check_started_face_follows_bind_and_request(sk);
  check_started_trigger_fires_once_per_transition(sk);
  check_streaming_wait_rules_started(sk);
  check_every_acceptor_excludes_the_holder_arm();
  check_expiry_survives_a_colliding_request();
  check_rebind_raises_no_duplicate_trigger();
  check_started_face_error_paths(sk);

  h.wait_idle();
  CHECK(d->txn_ready_o == 1, "idle at the end");

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<VKL_pp_acmp_listener> model;
  auto walk = std::make_unique<ListenerWalk>(model.get());
  return walk->run();
}

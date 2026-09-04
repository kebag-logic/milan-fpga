// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// avtp_stream_parser deep harness - the listener ACCEPT VERDICT.
//
// One source, five builds (see Makefile): N_STREAMS = 1 / 4 / 8 and the
// BIG_ENDIAN=1 beat order, so the table-width-dependent compare and the
// wire-byte-order lift are both proved at every shape the SoC can ship.
//
// The reject leg is tested as hard as the accept leg: every negative here is
// asserted against the counter/latch signature that the 0x8B4 APRB probe
// group publishes to software (PARSED, MATCHED, the wire stream_id), so a
// silicon read of those five words can be mapped back to a case in this file.
//
// Frame layout parsed (IEEE 1722-2016 §5, big-endian on the wire):
//   [0..11]  dst/src MAC
//   [12..13] 0x8100 -> C-VLAN present (AVTP header +4), else the EtherType
//   AVTP EtherType 0x22F0 at [12] (untagged) or [16] (tagged)
//   AVTP common stream header at o = 14 (untagged) / 18 (tagged):
//     o+0 subtype · o+1 [7]sv [6:4]version [0]tv · o+2 sequence_num
//     o+3 [0]tu   · o+4..11 stream_id (MS byte first) · o+12..15 avtp_timestamp

#include "../../common/verilator_harness.hpp"
#include "Vavtp_stream_parser.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

// NSTREAMS_TB and SHAPE_NAME stay macros because the Makefile picks the shape
// with -D per build (see the five -CFLAGS lines) and because NSTREAMS_TB also
// selects between the scalar and the array cfg port with #if. Everything below
// reads the typed constants.
#ifndef NSTREAMS_TB
#define NSTREAMS_TB 8
#endif
#ifndef SHAPE_NAME
#define SHAPE_NAME "unnamed shape"
#endif

constexpr int kNstreamsTb = NSTREAMS_TB;
constexpr const char* kShapeName = SHAPE_NAME;

namespace {

constexpr long MAX_PRINT = 40;

void sect(const char* t) { printf("\n[%s]\n", t); }

// ---------------------------------------------------------------------------
//  frame construction
// ---------------------------------------------------------------------------
struct Fspec {
  bool     tagged = false;
  uint16_t tpid   = 0x8100;   // outer tag TPID when tagged
  uint16_t ethertype = 0x22F0;
  uint8_t  subtype = 0x02;    // AAF
  bool     sv = true;
  bool     tv = true;
  bool     tu = false;
  uint8_t  version = 0;       // AVTP version (4.4.3.4: only 0 parses)
  uint8_t  seq = 0;
  uint64_t sid = 0;
  uint32_t ts  = 0;
  int      len = 128;
};

//! Fill `out` with the frame `s` describes and hand back a reference to it, so
//! a call site reads `feed(build_frame(stim, s))` and reuses one buffer.
const std::vector<uint8_t>& build_frame(std::vector<uint8_t>& out,
                                        const Fspec& s) {
  out.assign(s.len, 0x00);          // assign KEEPS the capacity
  std::vector<uint8_t>& f = out;
  for (int i = 0; i < 6; i++) { f[i] = 0x91; f[6 + i] = 0x02; }
  int o;
  if (s.tagged) {
    f[12] = static_cast<uint8_t>(s.tpid >> 8); f[13] = static_cast<uint8_t>(s.tpid);
    f[14] = 0x20; f[15] = 0x02;                       // PCP 1, VID 2
    f[16] = static_cast<uint8_t>(s.ethertype >> 8);
    f[17] = static_cast<uint8_t>(s.ethertype);
    o = 18;
  } else {
    f[12] = static_cast<uint8_t>(s.ethertype >> 8);
    f[13] = static_cast<uint8_t>(s.ethertype);
    o = 14;
  }
  if (o + 32 > static_cast<int>(f.size())) return out;  // caller wanted a runt
  f[o + 0] = s.subtype;
  f[o + 1] = static_cast<uint8_t>((s.sv ? 0x80 : 0x00) | ((s.version & 0x07) << 4) |
                                  (s.tv ? 0x01 : 0x00));
  f[o + 2] = s.seq;
  f[o + 3] = s.tu ? 0x01 : 0x00;
  for (int i = 0; i < 8; i++) f[o + 4 + i]  = static_cast<uint8_t>(s.sid >> (8 * (7 - i)));
  for (int i = 0; i < 4; i++) f[o + 12 + i] = static_cast<uint8_t>(s.ts  >> (8 * (3 - i)));
  for (int i = o + 16; i < static_cast<int>(f.size()); i++)
    f[i] = static_cast<uint8_t>(0x40 + (i & 0x3F));
  return out;
}

//! Thin by-value wrapper, kept for the three sites that keep two frames alive
//! at once (B3/C2) and so genuinely want their own copy.
std::vector<uint8_t> mkframe(const Fspec& s) {
  std::vector<uint8_t> f;
  build_frame(f, s);
  return f;
}

// ---------------------------------------------------------------------------
//  independent reference model of the documented parse
// ---------------------------------------------------------------------------
struct Ref {
  bool     parse = false;
  bool     hit = false;
  bool     tv = false;
  bool     tu = false;
  uint64_t sid = 0;
  uint32_t ts = 0;
  uint8_t  sub = 0;
  uint8_t  seq = 0;
  int      idx = 0;
};

// ---------------------------------------------------------------------------
//  stimulus: observe every pulse, never just the last one
// ---------------------------------------------------------------------------
struct Obs {
  int      parses = 0;
  int      matches = 0;
  uint64_t sid = 0;
  uint32_t ts = 0;
  uint8_t  sub = 0xFF;
  uint8_t  seq = 0;
  bool     tv = false;
  bool     tu = false;
  int      idx = -1;
};

constexpr uint64_t SID_A = 0x0200000000020000ULL;  // the bench's live listener sid
constexpr uint64_t SID_B = 0x91E0F0000102A5A5ULL;
constexpr uint64_t SIDS[8] = {
  0x0200000000020000ULL, 0x0200000000020001ULL, 0x0200000000020002ULL,
  0x0200000000020003ULL, 0xAABBCCDD00112233ULL, 0x1122334455667788ULL,
  0xFFFFFFFFFFFFFFFFULL, 0x0000000000000001ULL
};

//! The whole harness: the model, the tally, the stream-match table shadow, the
//! AXI-Stream BFM and the nine sections that spend them. Every piece of state
//! a section reads is a member, so the state a reader must hold to follow one
//! section is exactly what is listed below and nothing else.
class StreamParserVerdictHarness {
 public:
  int run() {
    bring_up_and_announce();
    prove_stream_id_byte_order_as_lifted_off_the_wire();
    prove_vlan_tagged_and_untagged_header_offset();
    prove_subtype_and_sv_gate_reject_non_media();
    prove_non_zero_version_is_discarded();
    prove_every_table_entry_is_reachable_at_this_width();
    prove_sid_compare_reject_signatures();
    prove_frame_stream_integrity();
    prove_randomised_traffic_matches_the_reference_model();
    prove_reset_clears_the_probe_counters();
    return report();
  }

 private:
  // `model` is already the reference-model function above, so the owner is
  // `dut_model`; it runs final() and frees on every path out of main().
  const milan::tb::Model<Vavtp_stream_parser> dut_model;
  Vavtp_stream_parser* const dut = dut_model.get();
  long checks = 0;
  long fails = 0;
  long printed = 0;

  // -------------------------------------------------------------------------
  //  stream-match table access (the port is a scalar at N=1, a word array above)
  // -------------------------------------------------------------------------
  uint64_t tbl_sid[kNstreamsTb] = {};
  uint32_t tbl_en = 0;

  //! One reusable frame buffer for the whole run. build_frame() fills it through
  //! a reference and assign() keeps the capacity, so section G's 600 randomised
  //! frames cost ONE allocation between them instead of one per frame — and the
  //! widest frame (1518 B) sizes the buffer for every narrower one after it.
  std::vector<uint8_t> stim;

  Obs obs_acc;                  // accumulates across a whole feed run

  uint32_t rng_s = 0xC0FFEE01u;

  void ck(const char* t, long got, long exp) {
    checks++;
    if (got != exp) {
      fails++;
      if (++printed <= MAX_PRINT)
        printf("  [FAIL] %-46s got=%ld exp=%ld\n", t, got, exp);
    }
  }
  void ckx(const char* t, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
      fails++;
      if (++printed <= MAX_PRINT)
        printf("  [FAIL] %-46s got=%016llx exp=%016llx\n", t,
               static_cast<unsigned long long>(got),
               static_cast<unsigned long long>(exp));
    }
  }

  void lo() { dut->clk = 0; dut->eval(); }
  void hi() { dut->clk = 1; dut->eval(); }

  void tbl_clear() {
    for (int e = 0; e < kNstreamsTb; e++) tbl_sid[e] = 0;
    tbl_en = 0;
#if NSTREAMS_TB == 1
    dut->cfg_stream_id_i = 0;
#else
    for (int w = 0; w < 2 * kNstreamsTb; w++) dut->cfg_stream_id_i[w] = 0;
#endif
    dut->cfg_stream_en_i = 0;
  }

  void tbl_arm(int e, uint64_t sid, bool en = true) {
    tbl_sid[e] = sid;
    if (en) tbl_en |= (1u << e); else tbl_en &= ~(1u << e);
#if NSTREAMS_TB == 1
    dut->cfg_stream_id_i = sid;
#else
    dut->cfg_stream_id_i[2 * e]     = static_cast<uint32_t>(sid);
    dut->cfg_stream_id_i[2 * e + 1] = static_cast<uint32_t>(sid >> 32);
#endif
    dut->cfg_stream_en_i = tbl_en;
  }

  void tbl_enable(int e, bool en) {
    if (en) tbl_en |= (1u << e); else tbl_en &= ~(1u << e);
    dut->cfg_stream_en_i = tbl_en;
  }

  Ref model(const std::vector<uint8_t>& f) const {
    Ref r;
    // the parse fires only once the 56-byte header buffer is full: 7 beats fill
    // it, the 8th accepted beat fires -> frames of 56 bytes or fewer never parse
    int nbeats = (static_cast<int>(f.size()) + 7) / 8;
    if (nbeats < 8) return r;
    bool vlan = (f[12] == 0x81 && f[13] == 0x00);
    int eo = vlan ? 16 : 12;
    if (!(f[eo] == 0x22 && f[eo + 1] == 0xF0)) return r;
    int o = eo + 2;
    uint8_t sub = f[o];
    uint8_t b1 = f[o + 1];
    bool sv  = (b1 & 0x80) != 0;
    int  ver = (b1 >> 4) & 0x07;
    if (sub > 0x07 || !sv || ver != 0) return r;   // 4.4.3.4: v!=0 discarded
    r.parse = true;
    r.sub = sub;
    r.tv  = (b1 & 0x01) != 0;
    r.seq = f[o + 2];
    r.tu  = (f[o + 3] & 0x01) != 0;
    r.sid = 0;
    for (int i = 0; i < 8; i++) r.sid = (r.sid << 8) | f[o + 4 + i];
    r.ts = 0;
    for (int i = 0; i < 4; i++) r.ts = (r.ts << 8) | f[o + 12 + i];
    for (int e = 0; e < kNstreamsTb; e++)
      if ((tbl_en >> e) & 1u) if (tbl_sid[e] == r.sid) { r.hit = true; r.idx = e; }
    return r;
  }

  void sample() {
    if (dut->parse_valid_o) {
      obs_acc.parses++;
      obs_acc.sid = dut->stream_id_o;
      obs_acc.ts  = dut->avtp_ts_o;
      obs_acc.sub = dut->subtype_o;
      obs_acc.seq = dut->seq_num_o;
      obs_acc.tv  = dut->ts_valid_o != 0;
      obs_acc.tu  = dut->ts_uncertain_o != 0;
    }
    if (dut->match_valid_o) { obs_acc.matches++; obs_acc.idx = dut->match_index_o; }
  }

  void idle(int n) {
    dut->s_tvalid_i = 0; dut->s_tlast_i = 0; dut->s_tready_i = 1;
    for (int i = 0; i < n; i++) { lo(); hi(); sample(); }
  }

  //! drive one frame. ready_gap = insert a not-ready cycle every Nth beat
  //! (0 = never); the parser must see the same verdict either way.
  void drive(const std::vector<uint8_t>& f, int ready_gap = 0) {
    int nbeats = (static_cast<int>(f.size()) + 7) / 8;
    for (int b = 0; b < nbeats; b++) {
      uint64_t d = 0;
      int vb = 0;
      for (int k = 0; k < 8; k++) {
        size_t ix = static_cast<size_t>(b) * 8 + k;
        if (ix < f.size()) {
#ifdef BIG_ENDIAN_TB
          // frame byte 0 in the MS lane
          d |= static_cast<uint64_t>(f[ix]) << (8 * (7 - k));
#else
          // LE beats (datapath default)
          d |= static_cast<uint64_t>(f[ix]) << (8 * k);
#endif
          vb++;
        }
      }
      dut->s_tdata_i  = d;
      dut->s_tkeep_i  = (vb == 8) ? 0xFF : static_cast<uint8_t>((1u << vb) - 1);
      dut->s_tvalid_i = 1;
      dut->s_tlast_i  = (b == nbeats - 1);
      if (ready_gap && (b % ready_gap) == (ready_gap - 1)) {
        dut->s_tready_i = 0;             // master holds the beat, parser must skip
        lo(); hi(); sample();
      }
      dut->s_tready_i = 1;
      lo(); hi(); sample();
    }
    dut->s_tvalid_i = 0; dut->s_tlast_i = 0;
  }

  //! one frame + drain: returns everything observed for it
  Obs feed(const std::vector<uint8_t>& f, int ready_gap = 0) {
    obs_acc = Obs();
    drive(f, ready_gap);
    idle(4);
    return obs_acc;
  }

  //! compare one frame against the reference model; returns the observation
  Obs feed_ref(const std::vector<uint8_t>& f, const char* tag,
               int ready_gap = 0) {
    Ref r = model(f);
    Obs o = feed(f, ready_gap);
    char b[128];
    snprintf(b, sizeof b, "%s: parse pulses", tag);
    ck(b, o.parses, r.parse ? 1 : 0);
    snprintf(b, sizeof b, "%s: match pulses", tag);
    ck(b, o.matches, (r.parse && r.hit) ? 1 : 0);
    if (r.parse) {
      snprintf(b, sizeof b, "%s: wire stream_id", tag);
      ckx(b, o.sid, r.sid);
      snprintf(b, sizeof b, "%s: avtp_timestamp", tag);
      ck(b, o.ts, r.ts);
      snprintf(b, sizeof b, "%s: subtype", tag);
      ck(b, o.sub, r.sub);
      snprintf(b, sizeof b, "%s: seq_num", tag);
      ck(b, o.seq, r.seq);
      snprintf(b, sizeof b, "%s: tv", tag);
      ck(b, o.tv ? 1 : 0, r.tv ? 1 : 0);
      snprintf(b, sizeof b, "%s: tu", tag);
      ck(b, o.tu ? 1 : 0, r.tu ? 1 : 0);
      if (r.hit) {
        snprintf(b, sizeof b, "%s: match index", tag);
        ck(b, o.idx, r.idx);
      }
    }
    return o;
  }

  uint32_t rnd() {
    rng_s ^= rng_s << 13; rng_s ^= rng_s >> 17; rng_s ^= rng_s << 5;
    return rng_s;
  }

  void bring_up_and_announce() {
    dut->resetn = 0; dut->s_tvalid_i = 0; dut->s_tready_i = 1; dut->s_tlast_i = 0;
    tbl_clear();
    for (int i = 0; i < 8; i++) { lo(); hi(); }
    dut->resetn = 1;
    idle(2);

    printf("== avtp_stream_parser deep harness - shape: %s ==\n", kShapeName);
  }

  // =========================================================================
  //  A. stream_id byte order, as lifted off the wire
  // =========================================================================
  void prove_stream_id_byte_order_as_lifted_off_the_wire() {
    sect("A. stream_id byte order, as lifted off the wire");
    {
      tbl_clear(); tbl_arm(0, SID_A);
      Fspec s; s.sid = SID_A; s.ts = 0x12345678; s.seq = 0x5A; s.len = 128;
      Obs o = feed_ref(build_frame(stim, s), "A1 untagged AAF");
      ck("A1 matched entry 0", o.matches, 1);
      // the wire bytes o+4..o+11 are MS-first: SID_HI is the FIRST four wire
      // bytes, SID_LO the last four - the exact claim 0x8BC/0x8C0 makes
      ckx("A1 APRB SID_HI = first 4 wire bytes", (o.sid >> 32), 0x02000000ULL);
      ckx("A1 APRB SID_LO = last 4 wire bytes", (o.sid & 0xFFFFFFFFULL),
          0x00020000ULL);
      // and it is NOT the byte-reversed value: the classic LE/BE confusion
      uint64_t swapped = 0;
      for (int i = 0; i < 8; i++) swapped |= ((SID_A >> (8 * i)) & 0xFF) << (8 * (7 - i));
      ck("A1 lifted sid is not byte-reversed", o.sid == swapped ? 1 : 0, 0);
      // nor the 32-bit-halves transposition
      uint64_t transposed = (SID_A >> 32) | (SID_A << 32);
      ck("A1 lifted sid is not half-transposed", o.sid == transposed ? 1 : 0, 0);
    }
    {
      // an all-ones sid and a sid of 1: no field is masked or sign-extended
      tbl_clear(); tbl_arm(0, 0xFFFFFFFFFFFFFFFFULL);
      Fspec s; s.sid = 0xFFFFFFFFFFFFFFFFULL; s.ts = 0xFFFFFFFFu; s.len = 128;
      Obs o = feed_ref(build_frame(stim, s), "A2 all-ones sid");
      ck("A2 all-ones matched", o.matches, 1);
      tbl_clear(); tbl_arm(0, 0x0000000000000001ULL);
      s.sid = 0x0000000000000001ULL; s.ts = 0;
      o = feed_ref(build_frame(stim, s), "A3 sid=1");
      ck("A3 sid=1 matched", o.matches, 1);
    }
    {
      // sid = 0 with the entry ARMED must match (zero is a legal stream_id, and
      // the table's reset state is zero-sid/disabled - the enable is the gate)
      tbl_clear(); tbl_arm(0, 0);
      Fspec s; s.sid = 0; s.len = 128;
      Obs o = feed_ref(build_frame(stim, s), "A4 sid=0 armed");
      ck("A4 zero sid matches when armed", o.matches, 1);
      tbl_enable(0, false);
      o = feed_ref(build_frame(stim, s), "A5 sid=0 disarmed");
      ck("A5 zero sid misses when disarmed", o.matches, 0);
      ck("A5 parse still fired", o.parses, 1);
    }
  }

  // =========================================================================
  //  B. VLAN-tagged vs untagged header offset
  // =========================================================================
  void prove_vlan_tagged_and_untagged_header_offset() {
    sect("B. VLAN-tagged vs untagged header offset");
    {
      tbl_clear(); tbl_arm(0, SID_A);
      Fspec u; u.sid = SID_A; u.ts = 0xCAFEBABE; u.seq = 0x11; u.len = 128;
      Fspec t = u; t.tagged = true; t.seq = 0x12;
      Obs ou = feed_ref(build_frame(stim, u), "B1 untagged");
      Obs ot = feed_ref(build_frame(stim, t), "B2 tagged");
      ckx("B: tagged lifts the SAME sid as untagged", ot.sid, ou.sid);
      ck("B: tagged lifts the same avtp_ts", ot.ts, static_cast<long>(ou.ts));
      ck("B: both matched", ou.matches + ot.matches, 2);
      // the mis-offset negative: a tagged frame read at the UNTAGGED offset
      // would lift bytes 14..21, i.e. {2002,22F0,subtype,b1,seq,tu}. Prove the
      // parser did not do that.
      std::vector<uint8_t> tf = mkframe(t);
      uint64_t misread = 0;
      for (int i = 0; i < 8; i++) misread = (misread << 8) | tf[14 + 4 + i];
      ck("B: tagged sid is not the untagged-offset lift",
         ot.sid == misread ? 1 : 0, 0);
      // and the mirror: an untagged frame read at the TAGGED offset
      std::vector<uint8_t> uf = mkframe(u);
      uint64_t misread2 = 0;
      for (int i = 0; i < 8; i++) misread2 = (misread2 << 8) | uf[18 + 4 + i];
      ck("B: untagged sid is not the tagged-offset lift",
         ou.sid == misread2 ? 1 : 0, 0);
    }
    {
      // an 802.1ad S-tag (0x88A8) is NOT decoded by this parser: [12..13] is
      // then read as the EtherType, which is not 0x22F0 -> honest reject, no
      // parse, no counter movement. Documented limitation, asserted.
      tbl_clear(); tbl_arm(0, SID_A);
      uint32_t p0 = dut->avtp_frames_o;
      Fspec s; s.tagged = true; s.tpid = 0x88A8; s.sid = SID_A; s.len = 128;
      Obs o = feed(build_frame(stim, s));
      ck("B3 S-tag (0x88A8) frame: no parse", o.parses, 0);
      ck("B3 S-tag frame: no match", o.matches, 0);
      ck("B3 S-tag frame: PARSED did not move", dut->avtp_frames_o - p0, 0);
      // a QinQ frame whose OUTER tag is a C-VLAN and inner is another C-VLAN:
      // [16..17] is then 0x8100, not 0x22F0 -> reject, no false accept
      std::vector<uint8_t> q = mkframe(s);
      q[12] = 0x81; q[13] = 0x00; q[16] = 0x81; q[17] = 0x00;
      o = feed(q);
      ck("B4 QinQ frame: no parse", o.parses, 0);
      ck("B4 QinQ frame: no match", o.matches, 0);
    }
  }

  // =========================================================================
  //  C. subtype / sv gate and non-AVTP traffic
  // =========================================================================
  void prove_subtype_and_sv_gate_reject_non_media() {
    sect("C. subtype / sv gate and non-AVTP traffic");
    {
      tbl_clear(); tbl_arm(0, SID_A);
      // 0x00..0x07 are the stream subtypes; 0x08 and up are not
      for (int sub = 0; sub <= 8; sub++) {
        Fspec s; s.subtype = static_cast<uint8_t>(sub); s.sid = SID_A; s.len = 128;
        char tag[64]; snprintf(tag, sizeof tag, "C1 subtype 0x%02X", sub);
        Obs o = feed_ref(build_frame(stim, s), tag);
        ck(tag, o.parses, sub <= 7 ? 1 : 0);
      }
      // the control subtypes that share the wire with the media: none may parse,
      // so none can overwrite the APRB media evidence
      constexpr uint8_t ctl[5] = {0xFA /*ADP*/, 0xFB /*AECP*/, 0xFC /*ACMP*/,
                                  0xFE /*MAAP*/, 0x7F};
      for (int i = 0; i < 5; i++) {
        Fspec s; s.subtype = ctl[i]; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        char tag[64];
        snprintf(tag, sizeof tag, "C2 control 0x%02X: no parse", ctl[i]);
        ck(tag, o.parses, 0);
        snprintf(tag, sizeof tag, "C2 control 0x%02X: no match", ctl[i]);
        ck(tag, o.matches, 0);
      }
      // sv=0 on a stream subtype: stream_id is not valid, must not be trusted
      { Fspec s; s.sv = false; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("C3 sv=0: no parse", o.parses, 0);
        ck("C3 sv=0: no match", o.matches, 0); }
      // non-AVTP EtherTypes seen on a real bench port
      constexpr uint16_t et[4] = {0x0800 /*IPv4*/, 0x0806 /*ARP*/,
                                  0x88F7 /*gPTP*/, 0x22EA /*SRP*/};
      for (int i = 0; i < 4; i++) {
        Fspec s; s.ethertype = et[i]; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        char tag[64];
        snprintf(tag, sizeof tag, "C4 ethertype 0x%04X: no parse", et[i]);
        ck(tag, o.parses, 0);
      }
    }
  }

  // =========================================================================
  //  V. version gate - IEEE 1722-2016 4.4.3.4: non-zero version DISCARDED
  // =========================================================================
  void prove_non_zero_version_is_discarded() {
    sect("V. version gate - IEEE 1722-2016 4.4.3.4: non-zero version DISCARDED");
    {
      // Sweep the version nibble 0..7 on AAF and CRF, tagged and untagged.
      // Only version 0 may parse; 1..7 are discarded STRUCTURALLY - no
      // parse_valid, no match_valid, and the free-running PARSED counter
      // freezes, so the 0x8B4 APRB group shows a discarded PDU as nothing at
      // all. That is the clause's "it shall discard the AVTPDU" (stronger
      // than ignore): a v1 PDU with valid AAF fields must never be half-
      // parsed as v0 media, however healthy every other field looks.
      tbl_clear(); tbl_arm(0, SID_A);
      static constexpr uint8_t subs[2] = {
        0x02 /*AAF*/, 0x04 /*CRF*/};
      for (int tagged = 0; tagged <= 1; tagged++) {
        for (int si = 0; si < 2; si++) {
          for (int ver = 0; ver <= 7; ver++) {
            Fspec s;
            s.tagged  = tagged != 0;
            s.subtype = subs[si];
            s.version = static_cast<uint8_t>(ver);
            s.sid     = SID_A;
            s.seq     = static_cast<uint8_t>(ver);
            s.len     = 128;
            char tag[64];
            snprintf(tag, sizeof tag, "V1 %s %s ver %d",
                     tagged ? "tagged" : "untagged",
                     subs[si] == 0x02 ? "AAF" : "CRF", ver);
            uint32_t p0 = dut->avtp_frames_o;
            feed_ref(build_frame(stim, s), tag);          // parse/match pulses vs model
            char t2[96];
            snprintf(t2, sizeof t2, "%s: PARSED counter %s", tag,
                     ver == 0 ? "ticks" : "frozen");
            ck(t2, static_cast<long>(dut->avtp_frames_o - p0), ver == 0 ? 1 : 0);
          }
        }
      }
      // the recovery control: after the whole non-zero sweep, a version-0 PDU
      // on the same stream parses and matches first-shot (no wedge, no state)
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed_ref(build_frame(stim, s), "V2 version-0 recovery");
        ck("V2 recovery PDU matched", o.matches, 1); }
    }
  }

  // =========================================================================
  //  D. stream-table width: every entry reachable at this N
  // =========================================================================
  void prove_every_table_entry_is_reachable_at_this_width() {
    sect("D. stream-table width: every entry reachable at this N");
    {
      tbl_clear();
      for (int e = 0; e < kNstreamsTb; e++) tbl_arm(e, SIDS[e]);
      for (int e = 0; e < kNstreamsTb; e++) {
        Fspec s; s.sid = SIDS[e]; s.seq = static_cast<uint8_t>(e); s.len = 128;
        char tag[64]; snprintf(tag, sizeof tag, "D1 entry %d", e);
        Obs o = feed_ref(build_frame(stim, s), tag);
        snprintf(tag, sizeof tag, "D1 entry %d matched", e);
        ck(tag, o.matches, 1);
        snprintf(tag, sizeof tag, "D1 entry %d index", e);
        ck(tag, o.idx, e);
      }
      // the highest entry alone: at N=8 this is entry 7, which the N=1 and N=4
      // shapes cannot even express - the width IS the coverage
      tbl_clear(); tbl_arm(kNstreamsTb - 1, SID_B);
      { Fspec s; s.sid = SID_B; s.len = 128;
        Obs o = feed_ref(build_frame(stim, s), "D2 top entry only");
        ck("D2 top entry matched", o.matches, 1);
        ck("D2 top entry index", o.idx, kNstreamsTb - 1); }
      // a sid that would live in an entry BEYOND this N must simply miss
      { Fspec s; s.sid = SIDS[0]; s.len = 128;
        Obs o = feed_ref(build_frame(stim, s), "D3 sid armed nowhere");
        ck("D3 out-of-table sid misses", o.matches, 0);
        ck("D3 out-of-table sid still parsed", o.parses, 1); }
    }
  }

  // =========================================================================
  //  E. SID compare REJECT leg - the live-blocker signatures
  // =========================================================================
  void prove_sid_compare_reject_signatures() {
    sect("E. SID compare REJECT leg - the live-blocker signatures");
    {
      // Every case here reproduces a way software and the wire can disagree
      // while BOTH ends believe they agree. The assertion is the APRB
      // signature: PARSED climbs, MATCHED does not, and the latch shows the
      // stream_id AS LIFTED OFF THE WIRE (not the armed one).
      tbl_clear();
      uint32_t p0 = dut->avtp_frames_o;
      uint32_t m0 = dut->matched_frames_o;

      // E1 - software armed the byte-REVERSED stream_id
      uint64_t rev = 0;
      for (int i = 0; i < 8; i++) rev |= ((SID_A >> (8 * i)) & 0xFFULL) << (8 * (7 - i));
      tbl_arm(0, rev);
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E1 byte-reversed arm: parse fired", o.parses, 1);
        ck("E1 byte-reversed arm: NO match", o.matches, 0);
        ckx("E1 latch shows the WIRE sid", o.sid, SID_A);
        ck("E1 PARSED climbed", dut->avtp_frames_o - p0, 1);
        ck("E1 MATCHED static", dut->matched_frames_o - m0, 0); }

      // E2 - software transposed SID_LO / SID_HI (the 0x8BC/0x8C0 write order)
      p0 = dut->avtp_frames_o;
      m0 = dut->matched_frames_o;
      tbl_clear(); tbl_arm(0, (SID_A >> 32) | (SID_A << 32));
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E2 half-transposed arm: parse fired", o.parses, 1);
        ck("E2 half-transposed arm: NO match", o.matches, 0);
        ckx("E2 latch shows the WIRE sid", o.sid, SID_A);
        ck("E2 PARSED climbed", dut->avtp_frames_o - p0, 1);
        ck("E2 MATCHED static", dut->matched_frames_o - m0, 0); }

      // E3 - one bit off (a uid/entity-id typo)
      p0 = dut->avtp_frames_o;
      m0 = dut->matched_frames_o;
      tbl_clear(); tbl_arm(0, SID_A ^ 1ULL);
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E3 one-bit-off arm: NO match", o.matches, 0);
        ck("E3 PARSED climbed", dut->avtp_frames_o - p0, 1);
        ck("E3 MATCHED static", dut->matched_frames_o - m0, 0); }
      // and the top bit, so the compare is proved across the full 64
      tbl_clear(); tbl_arm(0, SID_A ^ (1ULL << 63));
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E3b bit-63-off arm: NO match", o.matches, 0); }

      // E4 - the right sid is in the table but the entry is NOT ARMED: the
      // APRB armed-entry count is what distinguishes this from E1-E3
      p0 = dut->avtp_frames_o;
      m0 = dut->matched_frames_o;
      tbl_clear(); tbl_arm(0, SID_A, /*en=*/false);
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E4 correct sid, entry disarmed: NO match", o.matches, 0);
        ck("E4 PARSED climbed", dut->avtp_frames_o - p0, 1);
        ck("E4 MATCHED static", dut->matched_frames_o - m0, 0);
        ck("E4 armed-entry count is 0", static_cast<long>(tbl_en), 0); }

      // E5 - arm it for real: the SAME frame now accepts. This is the positive
      // control that proves E1-E4 failed for the reason claimed and not because
      // the parser was wedged.
      tbl_enable(0, true);
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E5 same frame, entry armed: MATCH", o.matches, 1);
        ck("E5 match index 0", o.idx, 0);
        ck("E5 MATCHED climbed", dut->matched_frames_o - m0, 1); }

      // E6 - disarm live, mid-stream: the verdict flips back with no reset
      tbl_enable(0, false);
      { Fspec s; s.sid = SID_A; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        ck("E6 live disarm: back to NO match", o.matches, 0);
        ck("E6 live disarm: parse still fires", o.parses, 1); }

#if NSTREAMS_TB >= 4
      // E7 - N-way compare: fill every entry but leave ONE hole. The frame
      // whose sid landed in the hole must miss while its neighbours accept -
      // an N-way compare that collapses to entry 0 would pass D1 and fail here.
      tbl_clear();
      for (int e = 0; e < kNstreamsTb; e++) tbl_arm(e, SIDS[e]);
      tbl_enable(kNstreamsTb / 2, false);
      for (int e = 0; e < kNstreamsTb; e++) {
        Fspec s; s.sid = SIDS[e]; s.len = 128;
        Obs o = feed(build_frame(stim, s));
        char tag[72];
        snprintf(tag, sizeof tag, "E7 entry %d verdict (hole at %d)", e,
                 kNstreamsTb / 2);
        ck(tag, o.matches, e == kNstreamsTb / 2 ? 0 : 1);
      }
#endif
    }
  }

  // =========================================================================
  //  F. frame-stream integrity
  // =========================================================================
  void prove_frame_stream_integrity() {
    sect("F. frame-stream integrity");
    {
      tbl_clear(); tbl_arm(0, SID_A);
      // F1 - exactly one verdict per frame, however long the frame is
      for (int len : {64, 128, 512, 1024, 1518}) {
        Fspec s; s.sid = SID_A; s.len = len;
        Obs o = feed(build_frame(stim, s));
        char tag[64];
        snprintf(tag, sizeof tag, "F1 len %4d: one parse pulse", len);
        ck(tag, o.parses, 1);
        snprintf(tag, sizeof tag, "F1 len %4d: one match pulse", len);
        ck(tag, o.matches, 1);
      }
      // F2 - the header-length floor: the 56-byte buffer needs 7 beats to fill
      // and the 8th accepted beat fires, so <= 56 bytes never parses. Asserted
      // so the floor is a documented property and not a surprise.
      { Fspec s; s.sid = SID_A; s.len = 56;
        Obs o = feed(build_frame(stim, s));
        ck("F2 56-byte frame: no parse (below the floor)", o.parses, 0); }
      { Fspec s; s.sid = SID_A; s.len = 57;
        Obs o = feed(build_frame(stim, s));
        ck("F2 57-byte frame: parses", o.parses, 1); }
      { Fspec s; s.sid = SID_A; s.len = 60;   // Ethernet minimum payload frame
        Obs o = feed(build_frame(stim, s));
        ck("F2 60-byte frame: parses and matches", o.matches, 1); }

      // F3 - back-to-back frames with NO idle gap (line-rate AAF shape): the
      // per-frame re-arm must happen on tlast, not on an idle cycle
      {
        obs_acc = Obs();
        Fspec a; a.sid = SID_A; a.seq = 1; a.len = 128;
        Fspec b; b.sid = SID_A; b.seq = 2; b.len = 128;
        Fspec c; c.sid = SID_B; c.seq = 3; c.len = 128;   // unknown sid between
        drive(build_frame(stim, a)); drive(build_frame(stim, b)); drive(build_frame(stim, c));
        idle(4);
        ck("F3 back-to-back: 3 parses", obs_acc.parses, 3);
        ck("F3 back-to-back: 2 matches", obs_acc.matches, 2);
        ckx("F3 back-to-back: last sid is the LAST frame's", obs_acc.sid, SID_B);
        ck("F3 back-to-back: last seq is the last frame's", obs_acc.seq, 3);
      }

      // F4 - mid-frame backpressure: not-ready beats are not data
      for (int gap : {2, 3, 7}) {
        Fspec s; s.sid = SID_A; s.ts = 0xDEADBEEF; s.len = 200;
        Obs o = feed(build_frame(stim, s), gap);
        char tag[64];
        snprintf(tag, sizeof tag, "F4 gap %d: one parse", gap);
        ck(tag, o.parses, 1);
        snprintf(tag, sizeof tag, "F4 gap %d: matched", gap);
        ck(tag, o.matches, 1);
        snprintf(tag, sizeof tag, "F4 gap %d: sid intact", gap);
        ckx(tag, o.sid, SID_A);
        snprintf(tag, sizeof tag, "F4 gap %d: ts intact", gap);
        ck(tag, o.ts, 0xDEADBEEF);
      }

      // F5 - a runt non-AVTP frame immediately before an AVTP frame must not
      // poison the header buffer (the buffer is not cleared on tlast by design;
      // bytes_in is - this proves that is sufficient)
      {
        obs_acc = Obs();
        std::vector<uint8_t> runt(60, 0xEE);
        runt[12] = 0x08; runt[13] = 0x06;                     // ARP
        Fspec s; s.sid = SID_A; s.ts = 0x01020304; s.len = 128;
        drive(runt); drive(build_frame(stim, s)); idle(4);
        ck("F5 runt-then-AVTP: one parse", obs_acc.parses, 1);
        ckx("F5 runt-then-AVTP: sid intact", obs_acc.sid, SID_A);
        ck("F5 runt-then-AVTP: matched", obs_acc.matches, 1);
      }
    }
  }

  // =========================================================================
  //  G. randomised differential vs the reference model
  // =========================================================================
  void prove_randomised_traffic_matches_the_reference_model() {
    sect("G. randomised differential vs the reference model");
    {
      tbl_clear();
      for (int e = 0; e < kNstreamsTb; e++) tbl_arm(e, SIDS[e]);
      constexpr int N_FRAMES = 600;
      long g_parses = 0;
      long g_matches = 0;
      uint32_t base_p = dut->avtp_frames_o;
      uint32_t base_m = dut->matched_frames_o;
      for (int i = 0; i < N_FRAMES; i++) {
        Fspec s;
        uint32_t r = rnd();
        s.tagged = (r & 1) != 0;
        s.sv     = ((r >> 1) & 7) != 0;                 // sv=0 ~1 in 8
        s.tv     = ((r >> 4) & 1) != 0;
        s.tu     = ((r >> 5) & 1) != 0;
        s.seq    = static_cast<uint8_t>(r >> 8);
        uint32_t r2 = rnd();
        switch (r2 & 7) {
          case 0: case 1: case 2: case 3:
            s.subtype = static_cast<uint8_t>(rnd() % 8); break;    // stream subtypes
          case 4: s.subtype = 0xFA; break;
          case 5: s.subtype = 0xFC; break;
          case 6: s.subtype = 0xFE; break;
          default: s.subtype = static_cast<uint8_t>(rnd() & 0xFF); break;
        }
        s.ethertype = ((r2 >> 4) & 15) == 0 ? 0x0800 : 0x22F0;
        uint32_t r3 = rnd();
        if ((r3 & 3) != 0) {
          uint64_t pick = SIDS[r3 % kNstreamsTb];
          // half the "known" sids get one bit flipped: the near-miss population
          if ((r3 >> 8) & 1) pick ^= 1ULL << ((r3 >> 9) % 64);
          s.sid = pick;
        } else {
          s.sid = (static_cast<uint64_t>(rnd()) << 32) | rnd();
        }
        s.ts  = rnd();
        s.len = 60 + static_cast<int>(rnd() % 700);

        // one build, two readers: the reference model and the DUT must see the
        // SAME bytes, and the builder is a pure function of `s`, so building the
        // frame twice was pure waste
        const std::vector<uint8_t>& fr = build_frame(stim, s);
        Ref ref = model(fr);
        Obs o = feed(fr, static_cast<int>(rnd() % 5));    // random backpressure
        if (o.parses != (ref.parse ? 1 : 0) ||
            o.matches != ((ref.parse && ref.hit) ? 1 : 0)) {
          checks += 2; fails += 2;
          if (++printed <= MAX_PRINT)
            printf("  [FAIL] G frame %d: parses=%d(exp %d) matches=%d(exp %d) "
                   "tagged=%d sub=%02X sv=%d len=%d\n", i, o.parses,
                   ref.parse ? 1 : 0, o.matches, (ref.parse && ref.hit) ? 1 : 0,
                   s.tagged, s.subtype, s.sv, s.len);
        } else {
          checks += 2;
        }
        if (ref.parse) {
          ckx("G wire sid", o.sid, ref.sid);
          ck ("G avtp_ts",  o.ts,  ref.ts);
          ck ("G subtype",  o.sub, ref.sub);
          ck ("G seq",      o.seq, ref.seq);
          if (ref.hit) ck("G match index", o.idx, ref.idx);
          g_parses++;
          if (ref.hit) g_matches++;
        }
      }
      ck("G free-running PARSED counter agrees",
         static_cast<long>(dut->avtp_frames_o - base_p), g_parses);
      ck("G free-running MATCHED counter agrees",
         static_cast<long>(dut->matched_frames_o - base_m), g_matches);
      printf("  (G: %d random frames, %ld parsed, %ld matched)\n",
             N_FRAMES, g_parses, g_matches);
    }
  }

  // =========================================================================
  //  H. reset clears the probe counters
  // =========================================================================
  void prove_reset_clears_the_probe_counters() {
    sect("H. reset clears the probe counters");
    {
      ck("H counters non-zero before reset", dut->avtp_frames_o > 0 ? 1 : 0, 1);
      dut->resetn = 0;
      for (int i = 0; i < 6; i++) { lo(); hi(); }
      dut->resetn = 1;
      idle(2);
      ck("H PARSED cleared by reset",  dut->avtp_frames_o, 0);
      ck("H MATCHED cleared by reset", dut->matched_frames_o, 0);
      tbl_clear(); tbl_arm(0, SID_A);
      Fspec s; s.sid = SID_A; s.len = 128;
      Obs o = feed(build_frame(stim, s));
      ck("H parses again after reset", o.parses, 1);
      ck("H PARSED = 1 after reset",   dut->avtp_frames_o, 1);
      ck("H MATCHED = 1 after reset",  dut->matched_frames_o, 1);
    }
  }

  int report() const {
    printf("--------------------------------------------------------------\n");
    printf("shape: %s\n", kShapeName);
    if (printed > MAX_PRINT)
      printf("(%ld further failures suppressed)\n", printed - MAX_PRINT);
    printf("checks: %ld   failures: %ld\nRESULT: %s\n", checks, fails,
           fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
  }
};

}  // namespace

// ---------------------------------------------------------------------------
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  StreamParserVerdictHarness harness;
  return harness.run();
}

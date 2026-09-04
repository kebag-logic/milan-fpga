// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_stream_table + avtp_stream_parser at N=8 (parser_tbl_wrap) - the RX
// listener VERDICT chain exactly as milan_datapath wires it, at the shipping
// cfg_ax8x8 width.
//
// tb/verilator/avtp_stream/sim_table.cpp owns this pairing at N=4 with a
// [1:0] index port; entries 4..7 are not expressible there. This harness owns
//
//   * entries 4..7 (the half of the shipping table nothing else reaches),
//   * the ACMP entry-0 alias BYTE ORDER: the sid the listener SM hands the
//     table must be the sid the parser lifts off the wire, or the listener
//     binds clean and accepts nothing - the open 8x8 blocker's shape,
//   * the armed-entry count that 0x8C4[23:16] publishes, tracked across
//     arm / evict / disarm, and
//   * TRAP-1: any override write to entry 0 - INCLUDING an evict (valid=0) -
//     latches ovr_armed_r[0] and detaches the ACMP alias for good. See the
//     block comment on that section; this is characterised, not endorsed.

#include "../../common/verilator_harness.hpp"
#include "Vparser_tbl_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

namespace {

void sect(const char* t) { printf("\n[%s]\n", t); }

int popcnt8(uint32_t v) { int n = 0; for (int i = 0; i < 8; i++) n += (v >> i) & 1; return n; }

struct Obs { int parses = 0; int matches = 0; uint64_t sid = 0; int idx = -1;
             uint8_t sub = 0xFF; };

//! untagged AAF frame carrying `sid` MS-byte-first, the wire truth. Fills
//! `out` and hands back a reference to it.
const std::vector<uint8_t>& build_aaf(std::vector<uint8_t>& out,
                                      uint64_t sid, uint8_t seq = 0,
                                      int len = 128) {
  out.assign(len, 0x00);          // assign KEEPS the capacity
  std::vector<uint8_t>& f = out;
  constexpr uint8_t dmac[6] = {
      0x91, 0xE0, 0xF0, 0x00, 0x2A, 0x02};
  memcpy(f.data(), dmac, 6);
  for (int i = 0; i < 6; i++) f[6 + i] = 0x02;
  f[12] = 0x22; f[13] = 0xF0;
  f[14] = 0x02;              // AAF
  f[15] = 0x81;              // sv=1, version=0, tv=1
  f[16] = seq;
  for (int i = 0; i < 8; i++) f[18 + i] = static_cast<uint8_t>(sid >> (8 * (7 - i)));
  for (int i = 30; i < len; i++) f[i] = static_cast<uint8_t>(0x50 + (i & 0x3F));
  return out;
}

//! the live bench stream_id both boards agree on (HANDOVER / TROUBLESHOOTING
//! §21): 02:00:00:00:00:02 + uid 0
constexpr uint64_t SID_ACMP = 0x0200000000020000ULL;
constexpr uint64_t SIDS[8] = {
  0x0200000000020000ULL, 0x0200000000020001ULL, 0x0200000000020002ULL,
  0x0200000000020003ULL, 0x0200000000020004ULL, 0x0200000000020005ULL,
  0x0200000000020006ULL, 0x0200000000020007ULL
};

//! The whole harness: the model, the tally, the BFM and the six sections that
//! spend them. Everything the sections share is a member, so no section can
//! reach state a reader cannot see from here.
class StreamTableVerdictHarness {
 public:
  int run() {
    bring_up_and_announce();
    prove_entry0_alias_is_gated_only_by_bound();
    prove_acmp_alias_byte_order_is_the_8x8_blocker();
    prove_csr_window_reaches_entries_1_to_7();
    prove_evict_disarm_and_rearm_track_the_armed_count();
    prove_bind_rise_pulses_once_per_arm_edge();
    prove_entry0_evict_releases_to_the_alias();
    return report();
  }

 private:
  const milan::tb::Model<Vparser_tbl_wrap> dut_model;
  Vparser_tbl_wrap* const dut = dut_model.get();
  long checks = 0;
  long fails = 0;

  Obs obs;

  //! One reusable frame buffer for the whole run: build_aaf() fills it through a
  //! reference and assign() keeps the capacity, so the frame bytes cost ONE
  //! allocation for the entire simulation instead of one per frame.
  std::vector<uint8_t> stim;

  void ck(const char* t, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", t, got, exp); }
  }
  void ckx(const char* t, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp)
      { fails++; printf("  [FAIL] %-52s got=%016llx exp=%016llx\n", t,
                        static_cast<unsigned long long>(got),
                        static_cast<unsigned long long>(exp)); }
  }

  void lo() { dut->clk = 0; dut->eval(); }
  void hi() { dut->clk = 1; dut->eval(); }

  void sample() {
    if (dut->parse_valid_o) { obs.parses++; obs.sid = dut->stream_id_o;
                              obs.sub = dut->subtype_o; }
    if (dut->match_valid_o) { obs.matches++; obs.idx = dut->match_index_o; }
  }
  void cyc(int n = 1) {
    for (int i = 0; i < n; i++) { lo(); hi(); sample(); }
  }

  Obs feed(const std::vector<uint8_t>& f) {
    obs = Obs();
    int nbeats = (static_cast<int>(f.size()) + 7) / 8;
    for (int b = 0; b < nbeats; b++) {
      uint64_t d = 0;
      int vb = 0;
      for (int k = 0; k < 8; k++) {
        size_t ix = static_cast<size_t>(b) * 8 + k;
        if (ix < f.size()) { d |= static_cast<uint64_t>(f[ix]) << (8 * k); vb++; }
      }
      dut->s_tdata_i = d;
      dut->s_tkeep_i = (vb == 8) ? 0xFF : static_cast<uint8_t>((1u << vb) - 1);
      dut->s_tvalid_i = 1; dut->s_tready_i = 1;
      dut->s_tlast_i = (b == nbeats - 1);
      cyc();
    }
    dut->s_tvalid_i = 0; dut->s_tlast_i = 0;
    cyc(4);
    return obs;
  }

  //! CSR-window style entry write (milan_datapath's win_commit_glue drives this)
  void tblwr(int idx, uint64_t sid, bool valid) {
    dut->wr_en_i = 1; dut->wr_idx_i = idx; dut->wr_sid_i = sid;
    dut->wr_valid_i = valid;
    cyc();
    dut->wr_en_i = 0;
    cyc();
  }

  void bring_up_and_announce() {
    dut->bound0_i = 0; dut->sid0_i = 0; dut->wr_en_i = 0;
    dut->s_tvalid_i = 0; dut->s_tready_i = 1; dut->s_tlast_i = 0;
    dut->resetn = 0; cyc(8); dut->resetn = 1; cyc(2);

    printf("== KL_stream_table + avtp_stream_parser, N=8 (cfg_ax8x8 shape) ==\n");
  }

  // =========================================================================
  //  T1. entry-0 ACMP alias: bound is the ONLY gate
  // =========================================================================
  void prove_entry0_alias_is_gated_only_by_bound() {
    sect("T1. entry-0 ACMP alias: bound is the ONLY gate");
    dut->sid0_i = SID_ACMP;
    cyc(2);
    ck("armed entries with listener unbound", popcnt8(dut->tbl_en_o), 0);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("unbound: parse fired (frame reached the parser)", o.parses, 1);
      ck("unbound: NO match", o.matches, 0);
      ckx("unbound: wire sid still reported", o.sid, SID_ACMP); }
    dut->bound0_i = 1; cyc(2);
    ck("armed entries once bound", popcnt8(dut->tbl_en_o), 1);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("bound: MATCH", o.matches, 1);
      ck("bound: index 0", o.idx, 0);
      ck("bound: subtype AAF", o.sub, 0x02); }
  }

  // =========================================================================
  //  T2. ACMP alias BYTE ORDER - the open 8x8 blocker's shape
  // =========================================================================
  void prove_acmp_alias_byte_order_is_the_8x8_blocker() {
    sect("T2. ACMP alias BYTE ORDER - the open 8x8 blocker's shape");
    // The listener SM binds a stream_id; the parser lifts one off the wire.
    // If those two disagree only in byte order, ACMP reports a clean bind,
    // the reservation completes, and NOTHING is ever accepted. Each case
    // below is one such disagreement, asserted against the exact 0x8B4 probe
    // signature: PARSED climbs, MATCHED does not, the latch shows the wire.
    uint32_t p0 = dut->avtp_frames_o;
    uint32_t m0 = dut->matched_frames_o;

    uint64_t rev = 0;
    for (int i = 0; i < 8; i++) rev |= ((SID_ACMP >> (8 * i)) & 0xFFULL) << (8 * (7 - i));
    dut->sid0_i = rev; cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T2a byte-reversed bind: parse fired", o.parses, 1);
      ck("T2a byte-reversed bind: NO match", o.matches, 0);
      ckx("T2a latch = the WIRE sid, not the bound one", o.sid, SID_ACMP);
      ck("T2a armed entries still 1", popcnt8(dut->tbl_en_o), 1); }

    dut->sid0_i = (SID_ACMP >> 32) | (SID_ACMP << 32); cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T2b half-transposed bind: NO match", o.matches, 0);
      ckx("T2b latch = the WIRE sid", o.sid, SID_ACMP); }

    dut->sid0_i = SID_ACMP ^ 1ULL; cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T2c uid-off-by-one bind: NO match", o.matches, 0); }

    ck("T2 PARSED climbed by 3", static_cast<long>(dut->avtp_frames_o - p0), 3);
    ck("T2 MATCHED did not move", static_cast<long>(dut->matched_frames_o - m0), 0);

    // the positive control: bind the wire truth and the same frame accepts
    dut->sid0_i = SID_ACMP; cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T2 positive control: MATCH on the wire-truth bind", o.matches, 1);
      ck("T2 MATCHED climbed by 1", static_cast<long>(dut->matched_frames_o - m0), 1); }
  }

  // =========================================================================
  //  T3. entries 1..7 through the CSR window (4..7 reach nowhere else)
  // =========================================================================
  void prove_csr_window_reaches_entries_1_to_7() {
    sect("T3. entries 1..7 through the CSR window (4..7 reach nowhere else)");
    for (int e = 1; e < 8; e++) tblwr(e, SIDS[e], true);
    ck("armed entries = 8 (alias + 7 overrides)", popcnt8(dut->tbl_en_o), 8);
    for (int e = 0; e < 8; e++) {
      Obs o = feed(build_aaf(stim, SIDS[e], static_cast<uint8_t>(e)));
      char t[72];
      snprintf(t, sizeof t, "T3 entry %d matched", e);
      ck(t, o.matches, 1);
      snprintf(t, sizeof t, "T3 entry %d index", e);
      ck(t, o.idx, e);
      snprintf(t, sizeof t, "T3 entry %d wire sid", e);
      ckx(t, o.sid, SIDS[e]);
    }
    { Obs o = feed(build_aaf(stim, 0xDEADBEEF0BADF00DULL));
      ck("T3 unknown sid against a FULL table: no match", o.matches, 0);
      ck("T3 unknown sid: parse still fired", o.parses, 1); }
  }

  // =========================================================================
  //  T4. evict / disarm / re-arm, with the armed-entry count tracked
  // =========================================================================
  void prove_evict_disarm_and_rearm_track_the_armed_count() {
    sect("T4. evict / disarm / re-arm, with the armed-entry count tracked");
    tblwr(5, SIDS[5], false);                        // evict entry 5
    ck("T4 armed entries after evict", popcnt8(dut->tbl_en_o), 7);
    { Obs o = feed(build_aaf(stim, SIDS[5]));
      ck("T4 evicted sid: no match", o.matches, 0);
      ck("T4 evicted sid: parse fired", o.parses, 1); }
    { Obs o = feed(build_aaf(stim, SIDS[4]));
      ck("T4 neighbour entry 4 untouched", o.matches, 1);
      ck("T4 neighbour index still 4", o.idx, 4); }
    tblwr(5, SIDS[5], true);                         // re-arm
    ck("T4 armed entries after re-arm", popcnt8(dut->tbl_en_o), 8);
    { Obs o = feed(build_aaf(stim, SIDS[5]));
      ck("T4 re-armed sid matches again", o.matches, 1);
      ck("T4 re-armed index 5", o.idx, 5); }
    tblwr(7, SIDS[6], true);                         // duplicate sid in 6 and 7
    { Obs o = feed(build_aaf(stim, SIDS[6]));
      ck("T4 duplicate sid matches", o.matches, 1);
      ck("T4 duplicate sid resolves to the HIGHEST entry", o.idx, 7); }
    tblwr(7, SIDS[7], true);
    // out-of-range write index: N_LISTENERS_P=8, so idx 8..15 must be ignored
    tblwr(9, 0xFFFFFFFFFFFFFFFFULL, true);
    ck("T4 out-of-range write ignored (armed count unchanged)",
       popcnt8(dut->tbl_en_o), 8);
    { Obs o = feed(build_aaf(stim, 0xFFFFFFFFFFFFFFFFULL));
      ck("T4 out-of-range write did not arm anything", o.matches, 0); }
  }

  // =========================================================================
  //  T5. bind_rise: one pulse per not-bound -> bound edge
  // =========================================================================
  void prove_bind_rise_pulses_once_per_arm_edge() {
    sect("T5. bind_rise: one pulse per not-bound -> bound edge");
    tblwr(3, SIDS[3], false); cyc(2);
    long saw = 0;
    tblwr(3, SIDS[3], true);
    for (int i = 0; i < 8; i++) { cyc(); if ((dut->bind_rise_o >> 3) & 1) saw++; }
    // the write itself pulses; the following cycles must be quiet
    ck("T5 bind_rise quiet after the arming write", saw, 0);
    tblwr(3, SIDS[3], false);
    saw = 0;
    dut->wr_en_i = 1; dut->wr_idx_i = 3; dut->wr_sid_i = SIDS[3];
    dut->wr_valid_i = 1;
    for (int i = 0; i < 6; i++) {
      cyc();
      if ((dut->bind_rise_o >> 3) & 1) saw++;
      dut->wr_en_i = 0;
    }
    ck("T5 exactly one bind_rise on the arm edge", saw, 1);
  }

  // =========================================================================
  //  T6. RELEASE-TO-ALIAS: an entry-0 evict hands entry 0 back to ACMP
  // =========================================================================
  void prove_entry0_evict_releases_to_the_alias() {
    sect("T6. RELEASE-TO-ALIAS: an entry-0 evict hands entry 0 back to ACMP");
    // REGRESSION GUARD for the fabric-listener blocker (2026-07-26).
    //
    // KL_stream_table used to latch ovr_armed_r[0] on ANY write to entry 0 -
    // an evict (wr_valid_i=0) included - and from then on entry 0 was the
    // override, never the ACMP bound record again, until RESET. A listener
    // window CTRL write with en=0 at index 0 (the natural "clear this sink
    // before provisioning it" move, which milan_datapath's win_commit_glue
    // let through unconditionally via `| ~csr_lctx_wr_data_w[0]`) therefore
    // killed the alias permanently: the listener SM kept reporting a clean
    // bind and the parser never matched again.
    //
    // The fix gives {valid=0, sid=0} a meaning - RELEASE-TO-ALIAS - so the
    // evict DISARMS the override instead of arming it. An evict that carries
    // a real sid still arms (that is a deliberate disable-this-stream), which
    // the negative leg below pins.
    dut->resetn = 0; cyc(8); dut->resetn = 1;
    dut->bound0_i = 1; dut->sid0_i = SID_ACMP; cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 pre-write: ACMP alias matches", o.matches, 1); }
    tblwr(0, 0, /*valid=*/false);         // "clear sink 0" - no sid staged
    ck("T6 evict released entry 0: alias still enabled",
       popcnt8(dut->tbl_en_o), 1);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 post-evict: parse still fires", o.parses, 1);
      ck("T6 post-evict: ACMP alias SURVIVES the evict", o.matches, 1); }
    // re-binding the listener lands on a live alias
    dut->bound0_i = 0; cyc(2); dut->bound0_i = 1; cyc(2);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 re-bind keeps the alias alive", o.matches, 1); }
    // NEGATIVE leg: an evict carrying a REAL sid is a deliberate disable and
    // must still arm the override - release-to-alias is the zero-sid code
    // only, not "any evict"
    tblwr(0, SIDS[5], /*valid=*/false);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 evict WITH a sid still detaches (deliberate disable)",
         o.matches, 0); }
    // an explicit override write, or a reset, recovers it
    tblwr(0, SID_ACMP, true);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 explicit override recovers the match", o.matches, 1);
      ck("T6 override index 0", o.idx, 0); }
    dut->resetn = 0; cyc(8); dut->resetn = 1; cyc(2);
    ck("T6 reset cleared PARSED", dut->avtp_frames_o, 0);
    { Obs o = feed(build_aaf(stim, SID_ACMP));
      ck("T6 reset revives the ACMP alias", o.matches, 1); }
  }

  int report() const {
    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\nRESULT: %s\n", checks, fails,
           fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
  }
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  StreamTableVerdictHarness harness;
  return harness.run();
}

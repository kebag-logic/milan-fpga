// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gPTP fabric slice: KL_gptp_shadow (tap + engine + lane) + the real
// timestamp_counter + KL_gptp_txstamp as the boundary -- the loop closes
// ENTIRELY in fabric. Unlike tb/verilator/gptp_plane (byte faces, exact
// integer model), this bench drives the WIDE faces the datapath splice
// will connect and NO timestamp ever enters from the harness: ingress
// stamps ride the tap's commit-pulse side FIFO, egress stamps come from
// the boundary observer, and the pdelay/offset checks are RANGE
// assertions around harness-recorded fabric time.
//
//  1  boot -> Pdelay_Req appears on the wide lane, header byte-exact
//     through the gearbox; the boundary stamper supplies t1 by itself
//  2  a manual exchange: the responder computes its residence field
//     from observed fabric time so the measured delay lands ~600 ns;
//     asCapable stays low after one exchange
//  3  the auto-responder raises asCapable at the second exchange
//  4  announce -> adopt; sync pairs -> offset in range; a short closed
//     loop against a +100 ppm master locks the REAL counter
//  5  classify negatives: an AVTP ethertype frame between gPTP ones is
//     invisible; a runt is dropped harmlessly
//  6  an OVERSIZE gPTP frame (> the tap FIFO) is dropped inside the
//     FIFO -- the NEXT sync's ingress stamp must be its own (this is
//     the check that falsifies an accept-time ts push)
//  7  a back-to-back burst overflows the tap FIFO: drops are COUNTED,
//     and the plane keeps working afterwards

#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "Vgptp_shadow_wrap.h"
#include "../../common/verilator_harness.hpp"
#include "../../common/gptp_tx_flags.hpp"

constexpr uint64_t OUR_CID = 0x02A1B2FFFEC3D4E5ull;
constexpr uint64_t PEER_CID = 0x0080E1FFFE112233ull;
constexpr uint32_t OUR_CQ = 0xF8FE436A;
constexpr uint64_t GMID = 0x00AACCFFFE010203ull;
constexpr uint64_t GMID2 = 0x00AACCFFFE010204ull;
constexpr uint64_t GMID_EMPTY = 0x00AACCFFFE010205ull;
constexpr uint64_t PEER2_CID = 0x0080E1FFFE112244ull;
constexpr uint64_t PATH_HOP = 0x00DDBBFFFE000001ull;
constexpr uint64_t PATH_HOP2 = 0x00DDBBFFFE000002ull;
constexpr uint64_t PATH_HOP3 = 0x00DDBBFFFE000003ull;
constexpr uint64_t PATH_HOP4 = 0x00DDBBFFFE000004ull;
constexpr uint64_t PATH_HOP5 = 0x00DDBBFFFE000005ull;
constexpr uint64_t PATH_HOP6 = 0x00DDBBFFFE000006ull;

constexpr uint32_t FL_PRESENT = 1;
constexpr uint32_t FL_AMGM = 2;
constexpr uint32_t FL_ASCAP = 4;
constexpr uint32_t FL_SYNCOK = 8;

//! The lane the tap and the transmitter share is 64 bits: eight bytes per
//! beat, one tkeep bit each, and eight bits per byte in the packer's shift.
constexpr size_t kLaneBytes = 8;
constexpr unsigned kByteBits = 8;
//! Clocks rst_n is held low, at boot and at every warm reset below.
constexpr int kResetTicks = 8;

//! The reconstruction this bench must reproduce EXACTLY. The mean-corrected
//! crossing phase leaves half a PHC tick (4 ns at the 8 ns shape this
//! bench's counter runs) and the wrapper's ordered record queue costs one
//! further tick before the plane captures, so a correct reconstruction
//! lands 12 ns after the framer's own launch reference. In the product that
//! queue does not exist and the residue is the half tick alone.
constexpr int64_t kReconNominalNs = 12;
//! The only term of the published error budget that is not deterministic
//! here: `timestamp_out` is the integer field of a Q(64).24 accumulator, so
//! once the servo applies a fractional addend the reported value trails the
//! accumulator by up to one integer nanosecond. Nothing else is allowed to
//! move, which is what makes a dropped register stage - a whole 8 ns tick -
//! a failure rather than noise.
constexpr int64_t kPhcTruncNs = 1;
//! The plane's own history window, in its own cycles, and an addend far
//! outside the declared envelope. The envelope is the producer's own
//! integrator clamp at this configuration; three times it is unambiguously
//! outside, whatever rounding either side uses.
constexpr int kReconGuardCyc = 64;
constexpr int32_t kAdjExcursion = 3 * 1677722;

struct Frame {
  std::vector<uint8_t> b;
  void u8(uint8_t v) { b.push_back(v); }
  void u16(uint16_t v) { u8(v >> 8); u8(v & 0xFF); }
  void u32(uint32_t v) { u16(v >> 16); u16(v & 0xFFFF); }
  void u48(uint64_t v) { u16((v >> 32) & 0xFFFF); u32(v & 0xFFFFFFFF); }
  void u64(uint64_t v) { u32(v >> 32); u32(v & 0xFFFFFFFF); }
  void ts(uint64_t ns) { u48(ns / 1000000000ull); u32(ns % 1000000000ull); }
};

static Frame ptp(uint8_t mtype, uint16_t seq, uint64_t corr,
                 uint16_t flags, uint16_t body_len,
                 uint64_t src = PEER_CID, uint16_t etype = 0x88F7) {
  Frame f;
  f.u48(0x0180C200000Eull);
  f.u48(0x0080E1112233ull);
  f.u16(etype);
  f.u8(0x10 | mtype); f.u8(0x02);
  f.u16(34 + body_len);
  f.u8(0); f.u8(0);
  f.u16(flags);
  f.u64(corr);
  f.u32(0);
  f.u64(src); f.u16(1);
  f.u16(seq);
  f.u8(0x05); f.u8(0x7F);
  return f;
}

//! A complete Follow_Up: 802.1AS-2011 Table 11-9 makes the information TLV
//! of 11.4.4.3 a FIELD of the 76-octet message (11.4.4.2.2 places it first
//! after the fixed fields), so the header's 34 octets, the 10-octet
//! preciseOriginTimestamp and this 32-octet TLV are the shortest legal
//! Follow_Up; the parser refuses anything shorter (FPGA-gPTP #11), which is
//! why the bench cannot send the 44-octet shape it used to.
static Frame follow_up(uint16_t seq, uint64_t origin_ns) {
  // flags: ptpTimescale, "Reserved as TRUE, ignored on reception" for
  // every message type (802.1AS-2011 Table 10-6, clause 10.5.2.2.6,
  // octet 1 bit 3), which is what wire.py sends too
  Frame g = ptp(0x8, seq, 0, 0x0008, 42);
  g.ts(origin_ns);
  g.u16(0x0003); g.u16(28);              // tlvType, lengthField (11.4.4.3.2/3)
  g.u8(0x00); g.u8(0x80); g.u8(0xC2);    // organizationId 00-80-C2
  g.u8(0x00); g.u8(0x00); g.u8(0x01);    // organizationSubType 1
  g.u32(0);                              // cumulativeScaledRateOffset
  g.u16(0);                              // gmTimeBaseIndicator
  g.u64(0); g.u32(0);                    // lastGmPhaseChange (12 octets)
  g.u32(0);                              // scaledLastGmFreqChange
  return g;
}

static uint64_t fld48(const std::vector<uint8_t> &f, size_t o) {
  uint64_t v = 0;
  for (int i = 0; i < 6; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint16_t fld16(const std::vector<uint8_t> &f, size_t o) {
  return static_cast<uint16_t>((static_cast<uint16_t>(f[o]) << 8) | f[o + 1]);
}
static uint32_t fld32(const std::vector<uint8_t> &f, size_t o) {
  uint32_t v = 0;
  for (int i = 0; i < 4; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint64_t fld64(const std::vector<uint8_t> &f, size_t o) {
  uint64_t v = 0;
  for (int i = 0; i < 8; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint64_t timestamp_field_ns(const std::vector<uint8_t> &f, size_t o) {
  return fld48(f, o) * 1000000000ull + fld32(f, o + 6);
}

static bool near(int64_t v, int64_t c, int64_t tol) {
  return v >= c - tol && v <= c + tol;
}

namespace {

//! The whole bench: the fabric slice, the peer that answers its pdelay
//! exchanges, and the phases that prove the loop closes in fabric. Every
//! former file-scope variable is a member here, so no phase can be read
//! without the state it moves being in view (Core Guidelines I.2).
class GptpShadowHarness {
 public:
  //! Every phase, in order; what the body of `main` became. The
  //! single-argument `run(n)` below is the clock-stepping overload the
  //! phases call, and the two never collide: one takes a count.
  int run() {
    drive_boot_reset();
    const std::vector<uint8_t> req = check_boot_pdelay_request_is_exact();
    check_equal_sequence_request_collision(req);
    check_one_exchange_measures_the_delay();
    check_second_exchange_raises_capability();
    check_announce_adoption_and_path_trace();
    check_sync_offset_and_closed_loop_lock();
    check_gm_switch_marks_time_uncertain();
    check_foreign_ethertype_and_runt_are_invisible();
    check_oversize_frame_cannot_skew_the_next_stamp();
    check_overflow_drops_are_counted();
    check_burst_never_laps_the_stamp_ring();
    check_fifo_drops_do_not_leak_ring_slots();
    check_shed_path_does_not_leak_across_bursts();
    check_long_frame_shed_stays_atomic();
    check_shed_count_is_ethertype_gated();
    const size_t master_mark = ride_quietly_to_grandmaster();
    check_master_sync_collision(master_mark);
    check_master_emits_all_three_types(master_mark);
    check_same_type_response_ownership();
    check_warm_reset_clears_the_request_owner();
    check_warm_reset_clears_the_sync_owner();
    check_every_stamp_names_its_own_frame();
    check_a_record_that_is_not_this_frames_is_refused();
    check_recovery_demand_survives_an_unaccepted_request();
    check_phc_trajectory_qualification();
    check_an_aged_head_is_not_retired();

    milan::tb::GptpTxFlags tx_flags;
    for (const auto& frame : txf) tx_flags.observe(frame);
    tx_flags.report([this](const char* name, uint64_t got, uint64_t expected) {
      expect(name, got, expected);
    }, milan::tb::GptpTxFlags::all_types);

    printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }

 private:
  //! The Verilated model, owned for the harness's whole lifetime, and the
  //! observing pointer through which every phase drives it.
  const milan::tb::Model<Vgptp_shadow_wrap> model_;
  Vgptp_shadow_wrap *dut = model_.get();
  int checks = 0;
  int fails = 0;
  uint64_t cyc = 0;
  //! #214: every RESULT the engine accepted, in delivery order, with both
  //! of its tags. A result names the frame it belongs to by {sequenceId,
  //! messageType}; the sequence alone cannot, because a Pdelay_Req carries
  //! our own counter while a Pdelay_Resp echoes the peer's and the two can
  //! coincide. Since #360 the ledger delivers one result per admitted frame
  //! IN FRAME ORDER, so `stamps[k]` is frame `txf[k]`'s result and the
  //! pairing is positional rather than a tag lookup.
  struct Stamp { uint16_t seq; uint8_t type; uint64_t ns; uint8_t ok; };
  std::vector<Stamp> stamps;
  //! Every launch record the observer produced, in wire order.
  struct Rec { uint16_t seq; uint8_t type; uint16_t oidx; uint8_t delta;
               uint8_t abort; };
  std::vector<Rec> records;
  //! Per frame, in wire order: did the test-only record queue delay this
  //! frame's record? A delayed record is captured against a LATER PHC
  //! value, which is a fixture artefact rather than anything the wire can
  //! do, so the reconstruction VALUE law excludes exactly these frames and
  //! counts them. Their tag, position and ownership laws still apply.
  std::vector<uint8_t> rec_delayed;
  //! THE INDEPENDENT LAUNCH REFERENCE, one per framed frame in wire order:
  //! the PHC at the edge the bench framer launched frame octet 0. The
  //! reconstruction under test never touches it.
  std::vector<uint64_t> launch_ns;
  std::vector<std::vector<uint8_t>> txf;   // unpacked lane frames
  std::vector<uint64_t> tx_sof_phc;        // phc at each frame's beat0
  //! A root reset erases the ledger's transaction epoch: entries are
  //! dropped and no result is returned for them, which is the documented
  //! exception to one-result-per-frame. The run therefore checks that law
  //! PER EPOCH and keeps the totals across them, rather than pretending a
  //! reset never happened.
  size_t epoch_txf_base = 0;
  int law_frames = 0;
  int law_results = 0;
  int law_tag_wrong = 0;
  int law_seq_wrong = 0;
  int law_recon_wrong = 0;
  int law_type_mask = 0;
  int law_erased = 0;
  int law_recon_exempt = 0;
  std::vector<uint8_t> cur;
  bool in_tx = false;
  bool tx_first = true;

  //! The complete outward bank may change only with its commit pulse.
  bool pub_watch = false;
  uint64_t last_pub_gm = 0;
  uint64_t last_pub_parent = 0;
  uint64_t last_pub_annq = 0;
  uint64_t last_pub_path_tail0 = 0;
  uint64_t last_pub_path_tail1 = 0;
  uint64_t last_pub_path_tail6 = 0;
  uint32_t last_pub_flags = 0;
  uint32_t last_pub_pdelay = 0;
  uint32_t last_pub_offset = 0;
  uint8_t last_pub_path_count = 0;
  uint8_t last_pub_path_gen = 0;
  unsigned pub_commits = 0;
  unsigned pub_changes = 0;
  unsigned pub_unguarded_changes = 0;

  //! issue #122: capture the ingress-ts ring push/pop stamps during a burst
  std::vector<uint64_t> g_pushed;
  std::vector<uint64_t> g_popped;
  bool g_ts_capture = false;

  // ---- the peer: answers pdelay with residence computed from observed
  // fabric time, so the measured delay lands near D_NOM. The harness's
  // own records give the EXPECTED delay exactly, up to the few-tick skew
  // between its observation points and the fabric latches ---------------
  static constexpr int64_t D_NOM = 600;
  size_t pd_seen = 0;
  bool pd_on = false;
  int64_t pd_target = D_NOM;             // may be legal negative noise
  int64_t pd_expect = 0;                // the last exchange's D
  //! The last exchange's expected delay is only a prediction when the
  //! fixture did NOT delay that request's record: a delayed record is
  //! captured against a later PHC, so the plane's own t1 legitimately sits
  //! after the launch the peer measured. Phases that grade the delay wait
  //! for an undelayed exchange rather than widening their tolerance.
  bool pd_expect_valid = false;

  size_t tx_seen = 0;

  //! Phase 14's two peer requests: the sequence, requesting clock identity
  //! and requesting port every step of the ownership proof compares to.
  static constexpr uint16_t Q1 = 0x1111;
  static constexpr uint16_t Q2 = 0x2222;
  static constexpr uint64_t C1 = PEER_CID;
  static constexpr uint64_t C2 = 0x001122FFFE334455ull;
  static constexpr uint16_t P1 = 1;
  static constexpr uint16_t P2 = 2;

  void expect(const char *what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
      fails++;
      printf("FAIL %-32s got %016llx exp %016llx\n", what,
             static_cast<unsigned long long>(got),
             static_cast<unsigned long long>(exp));
    }
  }

  uint64_t phc() { return dut->phc_ns_o; }

  void tick() {
    dut->clk_i = 0; dut->eval();
    //! Sample the engine face immediately before the active edge: the tuple
    //! is consumed AT this edge and the queue head moves after it, so a
    //! post-edge read would miss the very delivery whose order this trace
    //! exists to prove.
    if (dut->dbg_eng_txts_v_o)
      stamps.push_back({static_cast<uint16_t>(dut->dbg_eng_txts_seq_o),
                        static_cast<uint8_t>(dut->dbg_eng_txts_type_o),
                        dut->dbg_eng_txts_ns_o,
                        static_cast<uint8_t>(dut->dbg_eng_txts_ok_o)});
    //! A transfer is the value presented immediately before the active edge.
    //! Sampling after the edge loses a last beat when a producer drops valid
    //! in response to that same handshake -- a distinction the backpressure
    //! phase deliberately exercises.
    if (dut->tx_tvalid_o && dut->tx_tready_i) {
      if (tx_first) {
        cur.clear();
        in_tx = true;
        tx_sof_phc.push_back(phc());
      }
      for (size_t i = 0; i < kLaneBytes; i++)
        if ((dut->tx_tkeep_o >> i) & 1)
          cur.push_back((dut->tx_tdata_o >> (kByteBits * i)) & 0xFF);
      if (dut->tx_tlast_o) {
        txf.push_back(cur);
        in_tx = false;
        tx_first = true;
      } else {
        tx_first = false;
      }
    }
    dut->clk_i = 1; dut->eval();
    if (!dut->rst_n) {
      // A later warm reset starts a new publication epoch.  Do not compare the
      // reset value against the pre-reset bank and call that reset transition an
      // uncommitted runtime publication.
      pub_watch = false;
    } else {
      if (!pub_watch) {
        pub_watch = true;
      } else {
        const bool changed = dut->pub_gm_id_o != last_pub_gm
                          || dut->pub_parent_id_o != last_pub_parent
                          || dut->pub_flags_o != last_pub_flags
                          || dut->pub_pdelay_ns_o != last_pub_pdelay
                          || dut->pub_offset_o != last_pub_offset
                          || dut->pub_annq_o != last_pub_annq
                          || dut->pub_path_count_o != last_pub_path_count
                          || dut->pub_path_tail0_o != last_pub_path_tail0
                          || dut->pub_path_tail1_o != last_pub_path_tail1
                          || dut->pub_path_tail6_o != last_pub_path_tail6
                          || dut->pub_path_gen_o != last_pub_path_gen;
        if (changed) {
          pub_changes++;
          if (!dut->pub_commit_o) pub_unguarded_changes++;
        }
      }
      if (dut->pub_commit_o) pub_commits++;
      last_pub_gm = dut->pub_gm_id_o;
      last_pub_parent = dut->pub_parent_id_o;
      last_pub_flags = dut->pub_flags_o;
      last_pub_pdelay = dut->pub_pdelay_ns_o;
      last_pub_offset = dut->pub_offset_o;
      last_pub_annq = dut->pub_annq_o;
      last_pub_path_count = dut->pub_path_count_o;
      last_pub_path_tail0 = dut->pub_path_tail0_o;
      last_pub_path_tail1 = dut->pub_path_tail1_o;
      last_pub_path_tail6 = dut->pub_path_tail6_o;
      last_pub_path_gen = dut->pub_path_gen_o;
    }
    if (g_ts_capture) {
      if (dut->dbg_tspush_v_o) g_pushed.push_back(dut->dbg_tspush_o);
      if (dut->dbg_tspop_v_o)  g_popped.push_back(dut->dbg_rx_ts_o);
    }
    //! the observer's own records and the framer's independent launch
    //! reference, both in wire order
    if (dut->dbg_launch_v_o) launch_ns.push_back(dut->dbg_launch_phc_o);
    if (dut->dbg_rec_v_o && !dut->dbg_rec_kind_o)
      records.push_back({static_cast<uint16_t>(dut->dbg_rec_seq_o),
                         static_cast<uint8_t>(dut->dbg_rec_type_o),
                         static_cast<uint16_t>(dut->dbg_rec_oidx_o),
                         static_cast<uint8_t>(dut->dbg_rec_delta_o),
                         static_cast<uint8_t>(dut->dbg_rec_abort_o)});
    if (dut->dbg_dut_rec_v_o && !dut->dbg_dut_rec_kind_o)
      rec_delayed.push_back(
          static_cast<uint8_t>(dut->dbg_dut_rec_delayed_o));
    cyc++;
  }

  void run(uint64_t n) { while (n--) tick(); }

  //! pack bytes into 64-bit beats and drive the tap (harness is the DMA
  //! consumer too: tready held high)
  void send_wide(const std::vector<uint8_t> &bytes) {
    size_t n = bytes.size();
    for (size_t off = 0; off < n; off += kLaneBytes) {
      uint64_t d = 0;
      uint8_t k = 0;
      for (size_t i = 0; i < kLaneBytes && off + i < n; i++) {
        d |= static_cast<uint64_t>(bytes[off + i]) << (kByteBits * i);
        k |= static_cast<uint8_t>(1u << i);
      }
      dut->rx_tdata_i = d;
      dut->rx_tkeep_i = k;
      dut->rx_tvalid_i = 1;
      dut->rx_tready_i = 1;
      dut->rx_tlast_i = (off + kLaneBytes >= n);
      tick();
    }
    dut->rx_tvalid_i = 0;
    dut->rx_tlast_i = 0;
  }

  void service_pdelay() {
    while (pd_seen < txf.size()) {
      size_t i = pd_seen;
      if (txf[i].size() <= 14 || (txf[i][14] & 0xF) != 0x2) {
        pd_seen++;
        continue;
      }
      pd_seen++;
      if (!pd_on) continue;
      uint16_t seq = static_cast<uint16_t>((txf[i][44] << 8) | txf[i][45]);
      //! THE PEER'S t1 IS THE HARNESS'S OWN LAUNCH REFERENCE, not the
      //! plane's computed one: the framer's PHC at the edge it launched
      //! this frame's octet 0. Since #360 the frame's timestamp point is
      //! its launch, so a peer that still used the lane's first accepted
      //! beat would be computing a delay against an instant the standard
      //! does not name - and would hide exactly the queueing error this
      //! work exists to remove.
      //! `launch_ns` and `rec_delayed` are per EPOCH - a root reset erases
      //! the plane's transaction epoch and the harness's view of it with
      //! the same edge - while `txf` is the whole run, so the frame's index
      //! inside its own epoch is what indexes them.
      if (i < epoch_txf_base) continue;
      const size_t ei = i - epoch_txf_base;
      for (int w = 0; w < 4000 && launch_ns.size() <= ei; w++) tick();
      if (launch_ns.size() <= ei) continue;
      uint64_t t1 = launch_ns[ei];
      pd_expect_valid = (ei >= rec_delayed.size()) || !rec_delayed[ei];
      run(300);                                // a real turnaround, > 2*D_NOM
      uint64_t t2 = 5000000ull + phc();
      Frame f = ptp(0x3, seq, 0, 0x0200, 20);
      f.ts(t2); f.u64(OUR_CID); f.u16(1);
      // residence = (fabric turnaround) - 2*D_NOM, computed at send time;
      // the tap stamps t4 within a beat of the first wide beat below
      int64_t resid = static_cast<int64_t>(phc() - t1) - 2 * pd_target;
      uint64_t t3 = t2 + static_cast<uint64_t>(resid);
      uint64_t t4_est = phc() + 8;             // the next tick's beat 0
      pd_expect = (static_cast<int64_t>(t4_est - t1) - resid) / 2;
      send_wide(f.b);
      run(50);
      Frame g = ptp(0xA, seq, 0, 0x0000, 20);
      g.ts(t3); g.u64(OUR_CID); g.u16(1);
      send_wide(g.b);
      run(50);
    }
  }

  void run_svc(uint64_t n) {
    while (n--) { tick(); if ((n & 255) == 0) service_pdelay(); }
  }

  bool wait_flags(uint32_t mask, uint32_t want, uint64_t max_ticks) {
    for (uint64_t n = 0; n < max_ticks; n++) {
      if ((dut->pub_flags_o & mask) == want) return true;
      tick();
      if ((n & 255) == 0) service_pdelay();
    }
    return false;
  }

  std::vector<uint8_t> wait_tx(int mtype, uint64_t max_cycles,
                               size_t *idx_out = nullptr) {
    for (uint64_t n = 0; n < max_cycles; n++) {
      while (tx_seen < txf.size()) {
        size_t i = tx_seen++;
        if (mtype < 0 || (txf[i].size() > 14 && (txf[i][14] & 0xF) == mtype)) {
          if (idx_out) *idx_out = i;
          return txf[i];
        }
      }
      tick();
      if ((n & 255) == 0) service_pdelay();
    }
    printf("FAIL wait_tx type %d: timeout\n", mtype);
    fails++; checks++;
    return {};
  }

  //! Index in `txf` of the first frame of message type `mt` and sequence
  //! `seq` transmitted since `mark`, or -1 when the lane never carried it.
  int find_frame(size_t mark, uint8_t mt, uint16_t seq) const {
    for (size_t i = mark; i < txf.size(); i++)
      if (txf[i].size() > 45 && (txf[i][14] & 0xF) == mt &&
          fld16(txf[i], 44) == seq)
        return static_cast<int>(i);
    return -1;
  }

  //! build a minimal classifiable 0x88F7 (or foreign-ethertype) frame
  std::vector<uint8_t> tapframe(size_t len, bool gptp) {
      std::vector<uint8_t> f(len, 0);
    const std::array<uint8_t, 6> da = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};
    const std::array<uint8_t, 6> sa = {0x00, 0x80, 0xE1, 0x11, 0x22, 0x33};
      for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
      f[12] = gptp ? 0x88 : 0x22;
      f[13] = gptp ? 0xF7 : 0xF0;
      f[14] = 0x10; f[15] = 0x02;
      return f;
  }

  void announce(uint16_t seq, uint8_t p1, uint64_t gmid,
                uint64_t src = PEER_CID) {
    //! Present-PathTrace control: use three identities so this wide-face
    //! integration bench proves more than a reconstructed `{GM,parent}` path.
    Frame a = ptp(0xB, seq, 0, 0x0008, 58, src);
    for (int i = 0; i < 10; i++) a.u8(0);
    a.u16(0xFFC4); a.u8(0);
    a.u8(p1); a.u32(OUR_CQ); a.u8(248);
    a.u64(gmid);
    a.u16(2); a.u8(0xA0);
    a.u16(0x0008); a.u16(24);
    a.u64(gmid); a.u64(PATH_HOP); a.u64(src);
    send_wide(a.b);
    run_svc(4000);
  }

  void announce_eight_path(uint16_t seq, uint8_t p1, uint64_t gmid,
                           uint64_t src = PEER_CID) {
    //! Exercise the parent's complete fixed-width ABI, including slot seven.
    //! A loop bound accidentally shortened to the smaller smoke-test path must
    //! fail even though the donor itself still publishes all eight entries.
    Frame a = ptp(0xB, seq, 0, 0x0008, 98, src);
    for (int i = 0; i < 10; i++) a.u8(0);
    a.u16(0xFFC4); a.u8(0);
    a.u8(p1); a.u32(OUR_CQ); a.u8(248);
    a.u64(gmid);
    a.u16(7); a.u8(0xA0);
    a.u16(0x0008); a.u16(64);
    a.u64(gmid); a.u64(PATH_HOP); a.u64(PATH_HOP2); a.u64(PATH_HOP3);
    a.u64(PATH_HOP4); a.u64(PATH_HOP5); a.u64(PATH_HOP6); a.u64(src);
    send_wide(a.b);
    run_svc(4000);
  }

  void announce_without_path(uint16_t seq, uint8_t p1, uint64_t gmid,
                             uint64_t src = PEER_CID) {
    //! An exact fixed Announce has no suffix. The donor publishes its selected
    //! GM/parent scalars but truthfully reports the absent PathTrace as count 0.
    Frame a = ptp(0xB, seq, 0, 0x0008, 30, src);
    for (int i = 0; i < 10; i++) a.u8(0);
    a.u16(0xFFC4); a.u8(0);
    a.u8(p1); a.u32(OUR_CQ); a.u8(248);
    a.u64(gmid);
    a.u16(0); a.u8(0xA0);
    send_wide(a.b);
    run_svc(4000);
  }

  void announce_one_path(uint16_t seq, uint8_t p1, uint64_t gmid) {
    //! Explicit one-entry PathTrace from a directly connected GM. This is not
    //! the absent-TLV spelling: its served sequence is exactly `[GM]`.
    Frame a = ptp(0xB, seq, 0, 0x0008, 42, gmid);
    for (int i = 0; i < 10; i++) a.u8(0);
    a.u16(0xFFC4); a.u8(0);
    a.u8(p1); a.u32(OUR_CQ); a.u8(248);
    a.u64(gmid);
    a.u16(0); a.u8(0xA0);
    a.u16(0x0008); a.u16(8); a.u64(gmid);
    send_wide(a.b);
    run_svc(4000);
  }

  void sync_pair(uint16_t seq, uint64_t origin_delta,
                 uint64_t *measured_at) {
    // origin = (tap-stamp-to-be) - origin_delta: the harness reads the
    // counter just before injecting; the tap stamps within a beat
    Frame f = ptp(0x0, seq, 0, 0x0208, 10);
    f.ts(0);
    uint64_t at = phc();
    send_wide(f.b);
    run(30);
    Frame g = follow_up(seq, at - origin_delta);
    send_wide(g.b);
    run(4000);
    if (measured_at) *measured_at = at;
  }

  //! The boot reset the whole run starts from: every input at its idle
  //! level while rst_n is held low for kResetTicks clocks.
  void drive_boot_reset() {
    dut->rst_n = 0;
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tdata_i = 0;
    dut->rx_tkeep_i = 0; dut->rx_tready_i = 1;
    dut->tx_tready_i = 1;
    dut->rechold_en_i = 0; dut->rechold_type_i = 0;
    dut->rechold_release_i = 0;
    dut->recfault_en_i = 0; dut->recfault_mode_i = 0;
    dut->linkg_dis_i = 0; dut->linkg_freeze_i = 0;
    dut->cfg_mac_reinit_i = 0; dut->eth_alive_i = 1; dut->obs_rst_i = 0;
    //! the PHC's own controls at their product values: running, at the
    //! 8.0 ns Q8.24 step this bench's counter is sized for, with the
    //! plane's own servo owning the addend
    dut->phc_en_i = 1; dut->phc_incr_i = 0x08000000u;
    dut->phc_adj_ovr_en_i = 0; dut->phc_adj_ovr_i = 0;
    dut->phc_load_i = 0; dut->phc_tod_wr_i = 0;
    for (int i = 0; i < kResetTicks; i++) tick();
    dut->rst_n = 1;
  }

  //! Wait until the ledger has delivered the result for frame `idx`. Since
  //! #360 a result is not produced at the frame's first MAC beat any more:
  //! it waits for the frame to LAUNCH and for its record to cross back, so
  //! a phase that reads `stamps[idx]` has to wait for it rather than assume
  //! it is already there.
  bool wait_result(size_t idx, uint64_t max_cycles = 200000) {
    for (uint64_t k = 0; k < max_cycles && stamps.size() <= idx; k++) tick();
    return stamps.size() > idx;
  }

  //! Wait until the record queue's head is the one the hold gate selected.
  bool wait_rec_held(uint64_t max_cycles = 500000) {
    for (uint64_t k = 0; k < max_cycles && !dut->dbg_rec_held_o; k++) tick();
    return dut->dbg_rec_held_o != 0;
  }

  //! Fold the epoch that is ending into the whole-run laws and start a new
  //! one. Called before every root reset and once at the end.
  void close_epoch() {
    const size_t n_frame = txf.size() - epoch_txf_base;
    law_frames  += static_cast<int>(n_frame);
    law_results += static_cast<int>(stamps.size());
    if (stamps.size() < n_frame)
      law_erased += static_cast<int>(n_frame - stamps.size());
    for (size_t k = 0; k < stamps.size() && k < n_frame; k++) {
      const std::vector<uint8_t> &f = txf[epoch_txf_base + k];
      if (f.size() < 46) continue;
      const int ty = f[14] & 0xF;
      if (stamps[k].type != ty) law_tag_wrong++;
      if (stamps[k].seq !=
          static_cast<uint16_t>((f[44] << 8) | f[45])) law_seq_wrong++;
      // THE RECONSTRUCTION, against a reference the design never produced:
      // the PHC the framer sampled when it launched this frame's octet 0.
      // The crossing's sampling phase is exactly one fabric tick in this
      // single-clock bench, so the mean-corrected result sits half a tick
      // late by construction; anything beyond one tick is a dropped term.
      if (stamps[k].ok && k < launch_ns.size() && k < rec_delayed.size()) {
        if (rec_delayed[k]) {
          law_recon_exempt++;
        } else {
          const int64_t err = static_cast<int64_t>(stamps[k].ns) -
                              static_cast<int64_t>(launch_ns[k]);
          const int64_t dev = err - kReconNominalNs;
          if (dev < -kPhcTruncNs || dev > kPhcTruncNs) law_recon_wrong++;
        }
      }
      law_type_mask |= 1 << ty;
    }
    epoch_txf_base = txf.size();
    stamps.clear();
    records.clear();
    launch_ns.clear();
    rec_delayed.clear();
  }

  //! Release exactly one held record.
  void release_rec() {
    dut->rechold_release_i = 1;
    tick();
    dut->rechold_release_i = 0;
    tick();
  }

  // ---- 1: boot -> Pdelay_Req byte-exact through the gearbox -------------
  // Hold its REAL launch record so a same-sequence response is admitted
  // behind it. Nothing is fabricated: the held record is the observer's own
  // and only its arrival at the ledger is delayed.
  std::vector<uint8_t> check_boot_pdelay_request_is_exact() {
    dut->rechold_type_i = 0x2;
    dut->rechold_en_i = 1;
    size_t req_idx = 0;
    std::vector<uint8_t> req = wait_tx(0x2, 3200000, &req_idx);
    if (!req.empty()) {
      expect("pdreq length", req.size(), 68);
      expect("pdreq DA", fld48(req, 0), 0x0180C200000Eull);
      expect("pdreq etype+type",
             (static_cast<uint64_t>(req[12]) << 16) |
                 (static_cast<uint64_t>(req[13]) << 8) | req[14],
             0x88F712ull);
      expect("pdreq srcCID", fld48(req, 34), OUR_CID >> 16);
    }
    expect("asCapable low at boot", dut->pub_flags_o & FL_ASCAP, 0);
    if (!req.empty()) {
      uint16_t req_seq = static_cast<uint16_t>((req[44] << 8) | req[45]);
      expect("the request's launch record reaches the ledger head",
             wait_rec_held() ? 1 : 0, 1);
      expect("held record keeps sequenceId", dut->dbg_rec_held_seq_o, req_seq);
      expect("held record keeps messageType",
             dut->dbg_rec_held_type_o, static_cast<uint8_t>(req[14] & 0xF));
      // #214: the record names the frame by BOTH tags, read off the frame's
      // own octets at the wire. A Pdelay_Req is messageType 0x2
      // (802.1AS-2011 Table 11-3), the low nibble of wire byte 14.
      if (req_idx < records.size()) {
        expect("the req's record carries messageType 0x2",
               records[req_idx].type, static_cast<uint8_t>(req[14] & 0xF));
        expect("the req's record carries its own sequenceId",
               records[req_idx].seq, req_seq);
        // the whole-frame cycle distance, measured and not assumed: a
        // fragmented frame produces another value and aborts
        expect("the req's record measured the contracted cycle distance",
               records[req_idx].delta, 45);
        expect("the req's record is not an abort", records[req_idx].abort, 0);
        expect("the req's record takes the next observer position",
               records[req_idx].oidx, static_cast<uint16_t>(req_idx));
      }
      // nothing has been delivered while the record is held: the ledger is
      // ordered, so the frame behind it waits too
      expect("a held record delivers no result", stamps.size(), req_idx);
    }
    return req;
  }

  // ---- 1c: equal-sequence Req/Resp claims, ORDERED ownership ------------
  // Both endpoints' request counters start at zero. While our type-2 claim
  // waits on its held launch record, a peer request with the SAME sequence
  // draws a type-3 response onto the wire. Two frames are then live carrying
  // one 16-bit sequence, which is precisely the case a tag lookup cannot
  // resolve. The ledger resolves it by POSITION: nothing is delivered while
  // the older record is held, and on release each frame receives its own
  // result, in the order the frames left.
  void check_equal_sequence_request_collision(const std::vector<uint8_t> &req) {
    expect("boot request record is held for collision", dut->dbg_rec_held_o, 1);
    dut->rechold_en_i = 0;
    uint16_t boot_clash = req.empty() ? 0 :
        static_cast<uint16_t>((req[44] << 8) | req[45]);
    size_t boot_eng_mark = stamps.size();
    uint16_t boot_ev_drop = dut->dbg_ev_drop_o;
    size_t mark = txf.size();
    tx_seen = mark;
    {
      Frame rq = ptp(0x2, boot_clash, 0, 0x0000, 20, PEER_CID);
      rq.u64(0); rq.u64(0); rq.u32(0);
      send_wide(rq.b);
      size_t ri = 0;
      std::vector<uint8_t> rsp = wait_tx(0x3, 200000, &ri);
      expect("equal request sequences: the peer request is answered",
             rsp.empty() ? 0 : 1, 1);
      if (!rsp.empty())
        expect("equal request sequences: Resp echoes the common sequence",
               static_cast<uint16_t>((rsp[44] << 8) | rsp[45]), boot_clash);
      run(4000);
      // The response's OWN Follow_Up is built from the response's RESULT,
      // and that result sits behind the held record. A plane that answered
      // it anyway would be crediting the response with somebody else's time.
      expect("a held record delivers no result to the engine",
             stamps.size(), boot_eng_mark);
      expect("no Resp_Follow_Up can be built while the result is owed",
             find_frame(mark, 0xA, boot_clash) < 0 ? 1 : 0, 1);
      expect("the held record is still held", dut->dbg_rec_held_o, 1);
    }
    release_rec();
    run(4000);
    expect("the released record delivers the request and then the response",
           stamps.size() >= boot_eng_mark + 2 ? 1 : 0, 1);
    if (stamps.size() >= boot_eng_mark + 2) {
      expect("collision delivery 1 is the older Pdelay_Req",
             stamps[boot_eng_mark].type, 0x2);
      expect("collision delivery 2 is the Pdelay_Resp behind it",
             stamps[boot_eng_mark + 1].type, 0x3);
      for (size_t k = boot_eng_mark; k < boot_eng_mark + 2; k++)
        expect("both collision deliveries share the sequenceId",
               stamps[k].seq, boot_clash);
      expect("collision delivery 1 is a measurement",
             stamps[boot_eng_mark].ok, 1);
      expect("collision delivery 2 is a measurement",
             stamps[boot_eng_mark + 1].ok, 1);
      expect("the two deliveries carry DIFFERENT times",
             stamps[boot_eng_mark].ns != stamps[boot_eng_mark + 1].ns ? 1 : 0,
             1);
    }
    std::vector<uint8_t> rfu = wait_tx(0xA, 400000);
    expect("the response's own result builds its Resp_Follow_Up",
           rfu.empty() ? 0 : 1, 1);
    if (!rfu.empty() && stamps.size() >= boot_eng_mark + 2) {
      expect("Resp_FU echoes the common sequence",
             static_cast<uint16_t>((rfu[44] << 8) | rfu[45]), boot_clash);
      expect("Resp_FU carries the RESPONSE's time, not the request's",
             timestamp_field_ns(rfu, 48), stamps[boot_eng_mark + 1].ns);
    }
    expect("request collision changed no engine-event drop count",
           dut->dbg_ev_drop_o, boot_ev_drop);
    expect("request collision discarded no record", dut->dbg_txts_disc_o, 0);
    expect("request collision raised no barrier", dut->dbg_txts_barr_o, 0);
  }

  // ---- 2: fabric-timed exchanges; not capable at one --------------------
  void check_one_exchange_measures_the_delay() {
    pd_seen = 0;                      // answer the boot request too
    pd_on = true;
    service_pdelay();
    run_svc(8000);
    expect("one exchange not capable", dut->pub_flags_o & FL_ASCAP, 0);
    // The boot request's record was deliberately delayed by the collision
    // fixture above, so its t1 is not the launch the peer measured. Grade
    // the first exchange the fixture did not touch instead.
    for (uint64_t n = 0; n < 8000000ull &&
                         !(pd_expect_valid && dut->pub_pdelay_ns_o != 0); n++) {
      tick();
      if ((n & 255) == 0) service_pdelay();
    }
    expect("an undelayed exchange was graded", pd_expect_valid ? 1 : 0, 1);
    expect("pdelay matches the records",
           near(static_cast<int32_t>(dut->pub_pdelay_ns_o), pd_expect, 32), 1);
  }

  // ---- 3: the second exchange raises asCapable ---------------------------
  void check_second_exchange_raises_capability() {
    expect("capable at the second exchange",
           wait_flags(FL_ASCAP, FL_ASCAP, 6000000ull), 1);

    // A symmetric exchange can legitimately measure a small negative delay.
    // The donor must retain that signed value for its acceptance decision (and
    // therefore keep asCapable), while the parent's unsigned public bank must
    // publish zero.  Removing the sign-bit clamp exposes ~2^32 ns here; forcing
    // every delay to zero instead fails the positive 600 ns phase above.
    pd_target = -40;
    for (uint64_t n = 0;
         n < 6000000ull && !(pd_expect < 0 && dut->pub_pdelay_ns_o == 0);
         n++) {
      tick();
      if ((n & 255) == 0) service_pdelay();
    }
    expect("negative pdelay exchange really measured below zero",
           pd_expect < 0, 1);
    expect("negative pdelay clamps at the unsigned publication boundary",
           dut->pub_pdelay_ns_o, 0);
    expect("negative pdelay noise preserves asCapable",
           dut->pub_flags_o & FL_ASCAP, FL_ASCAP);
    pd_target = D_NOM;
    for (uint64_t n = 0;
         n < 6000000ull && !(pd_expect > 0 && dut->pub_pdelay_ns_o > 0);
         n++) {
      tick();
      if ((n & 255) == 0) service_pdelay();
    }
    expect("positive pdelay resumes after the clamp probe",
           pd_expect > 0 && dut->pub_pdelay_ns_o > 0, 1);
  }

  // ---- 4: adopt; offsets in range; the counter locks ---------------------
  void check_announce_adoption_and_path_trace() {
    announce(10, 100, GMID);
    expect("adopted", dut->pub_flags_o & 3, FL_PRESENT);
    expect("pub gm id", dut->pub_gm_id_o, GMID);
    expect("pub parent id", dut->pub_parent_id_o, PEER_CID);
    expect("published full path count", dut->pub_path_count_o, 3);
    expect("published path middle hop", dut->pub_path_tail0_o, PATH_HOP);
    expect("published path source tail", dut->pub_path_tail1_o, PEER_CID);
    {
      //! Mutation bars for the parent contract. Reinstating either `raw<=1 ? 1`
      //! or an unconditional GM term in the path-generation comparator fails
      //! this arm. Scalar GM selection remains independent of the served path.
      const uint8_t gen_present = dut->pub_path_gen_o;
      announce_without_path(11, 100, GMID);
      expect("TLV-less selected GM remains published", dut->pub_gm_id_o, GMID);
      expect("TLV-less selected parent remains published",
             dut->pub_parent_id_o, PEER_CID);
      expect("TLV-less selected PathTrace stays raw empty",
             dut->pub_path_count_o, 0);
      expect("TLV-less selected path clears active tail 1",
             dut->pub_path_tail0_o, 0);
      expect("TLV-less selected path clears active tail 2",
             dut->pub_path_tail1_o, 0);
      expect("TLV-less selected path clears final ABI tail",
             dut->pub_path_tail6_o, 0);
      const uint8_t gen_empty = static_cast<uint8_t>((gen_present + 1u) & 0xFu);
      expect("present to absent spends exactly one path generation",
             dut->pub_path_gen_o, gen_empty);

      announce_without_path(12, 100, GMID);
      expect("identical absent refresh spends no path generation",
             dut->pub_path_gen_o, gen_empty);

      announce_without_path(13, 90, GMID_EMPTY, GMID_EMPTY);
      expect("better TLV-less Announce changes scalar GM",
             dut->pub_gm_id_o, GMID_EMPTY);
      expect("better TLV-less Announce still serves empty",
             dut->pub_path_count_o, 0);
      expect("absent GM A-to-B is path-generation silent",
             dut->pub_path_gen_o, gen_empty);

      announce_one_path(14, 90, GMID_EMPTY);
      const uint8_t gen_one = static_cast<uint8_t>((gen_empty + 1u) & 0xFu);
      expect("explicit one-entry PathTrace publishes count one",
             dut->pub_path_count_o, 1);
      expect("absent to explicit GM spends one path generation",
             dut->pub_path_gen_o, gen_one);

      announce_without_path(15, 90, GMID_EMPTY, GMID_EMPTY);
      const uint8_t gen_empty_again = static_cast<uint8_t>((gen_one + 1u) & 0xFu);
      expect("explicit GM withdrawal restores empty count",
             dut->pub_path_count_o, 0);
      expect("explicit GM to absent spends one path generation",
             dut->pub_path_gen_o, gen_empty_again);

      announce(16, 80, GMID);
      expect("present path restored for servo controls",
             dut->pub_path_count_o, 3);
      expect("restored path returns original scalar GM", dut->pub_gm_id_o, GMID);
      expect("absent to restored path spends one generation",
             dut->pub_path_gen_o, (gen_empty_again + 1u) & 0xFu);

      const uint8_t gen_restored = dut->pub_path_gen_o;
      announce_eight_path(17, 75, GMID);
      expect("maximum bounded PathTrace publishes count eight",
             dut->pub_path_count_o, 8);
      expect("maximum bounded PathTrace reaches final tail slot",
             dut->pub_path_tail6_o, PEER_CID);
      expect("three to eight entries spends one generation",
             dut->pub_path_gen_o, (gen_restored + 1u) & 0xFu);
    }
  }

  //! The sync half of phase 4: one pair puts the offset in range, then a
  //! short closed loop against a +100 ppm master locks the REAL counter.
  void check_sync_offset_and_closed_loop_lock() {
    {
      // offset = tap_stamp - (origin + pd): origin is written so the true
      // offset is ~+1000 ns; the tap stamps within a couple of beats
      sync_pair(0x100, 1000 + static_cast<uint64_t>(D_NOM), nullptr);
      expect("offset near +1000",
             near(static_cast<int32_t>(dut->pub_offset_o), 1000, 200), 1);
      expect("sync-ok rose", dut->pub_flags_o & FL_SYNCOK, FL_SYNCOK);
    }
    {
      // short closed loop: a master 1 ms ahead at +100 ppm in counter
      // time; one re-base then the addend carries the rate
      uint64_t mst_base = phc() + 1000000ull - cyc * 8ull - cyc / 1250ull;
      uint16_t sq = 0x200;
      for (int k = 0; k < 12; k++) {
        if ((k % 6) == 0) announce(static_cast<uint16_t>(20 + k), 100, GMID);
        run_svc(250000);
        uint64_t origin = mst_base + cyc * 8ull + cyc / 1250ull;
        Frame f = ptp(0x0, sq, 0, 0x0208, 10);
        f.ts(0);
        send_wide(f.b);
        run(30);
        // cancel pd so offset -> 0
        Frame g = follow_up(sq, origin + static_cast<uint64_t>(D_NOM));
        send_wide(g.b);
        run(4000);
        sq++;
      }
      expect("closed loop locked",
             near(static_cast<int32_t>(dut->pub_offset_o), 0, 300), 1);
    }
  }

  // A better Announce moves the registered bank on the same edge on which
  // talkers may launch. The pre-commit discontinuity must make tu visible
  // to both consumer-equivalent launch registers on that edge.
  void check_gm_switch_marks_time_uncertain() {
    run_svc(512);
    expect("healthy bank clears tu before GM switch", dut->ts_uncertain_o, 0);
    const uint16_t disc_before = dut->disc_launch_count_o;
    announce(0x2F0, 70, GMID2, PEER2_CID);
    expect("better Announce selects the new GM", dut->pub_gm_id_o, GMID2);
    expect("better Announce preserves full path count", dut->pub_path_count_o, 3);
    expect("better Announce preserves middle hop", dut->pub_path_tail0_o,
           PATH_HOP);
    expect("better Announce publishes new source tail", dut->pub_path_tail1_o,
           PEER2_CID);
    expect("registered bank emitted a pre-commit discontinuity",
           dut->disc_launch_count_o > disc_before, 1);
    expect("AAF same-edge launch samples tu=1", dut->aaf_launch_tu_o, 1);
    expect("CRF same-edge launch samples tu=1", dut->crf_launch_tu_o, 1);
  }

  // ---- 5: classify negatives ---------------------------------------------
  void check_foreign_ethertype_and_runt_are_invisible() {
    uint32_t pd_before = dut->pub_pdelay_ns_o;
    uint16_t drop_before = dut->dbg_tap_drop_o;
    Frame avtp = ptp(0x3, 0x7000, 0, 0x0200, 20, PEER_CID, 0x22F0);
    avtp.ts(123456); avtp.u64(OUR_CID); avtp.u16(1);
    send_wide(avtp.b);                 // AVTP ethertype: invisible
    run(2000);
    std::vector<uint8_t> runt = {1, 2, 3, 4, 5, 6};
    send_wide(runt);                   // runt: dropped atomically
    run(2000);
    expect("foreign ethertype invisible", dut->pub_pdelay_ns_o, pd_before);
    expect("negatives cost no drops", dut->dbg_tap_drop_o, drop_before);
  }

  // ---- 6: an oversize frame cannot skew the next sync's stamp -----------
  // the 3 KB gPTP frame overflows the 2 KB tap FIFO and is dropped
  // INSIDE it; with the commit-pulse ts transport the following sync
  // still pairs with its OWN arrival stamp (an accept-time push would
  // hand it the storm frame's)
  void check_oversize_frame_cannot_skew_the_next_stamp() {
    Frame storm = ptp(0x0, 0x7100, 0, 0x0208, 10);
    storm.ts(0);
    while (storm.b.size() < 3000) storm.u8(0xAA);
    send_wide(storm.b);
    run(2000);
    sync_pair(0x300, 2000 + static_cast<uint64_t>(D_NOM), nullptr);
    expect("oversize cannot skew the stamp",
           near(static_cast<int32_t>(dut->pub_offset_o), 2000, 200), 1);
  }

  // ---- 7: overflow drops are counted; the plane survives ----------------
  void check_overflow_drops_are_counted() {
    uint16_t drop_before = dut->dbg_tap_drop_o;
    for (int k = 0; k < 12; k++) {
      Frame f = ptp(0xC, static_cast<uint16_t>(0x7200 + k), 0, 0, 20);
      while (f.b.size() < 512) f.u8(0x55);
      send_wide(f.b);                  // back-to-back, no gap
    }
    run(20000);
    expect("overflow drops counted",
           dut->dbg_tap_drop_o > drop_before, 1);
    sync_pair(0x400, 3000 + static_cast<uint64_t>(D_NOM), nullptr);
    expect("the plane survives the burst",
           near(static_cast<int32_t>(dut->pub_offset_o), 3000, 200), 1);
  }

  // ---- 8: issue #122 -- a back-to-back 0x88F7 burst must NOT lap the ring.
  // [R0]'s repro: 40 two-beat 0x88F7 frames arrive far faster (2 beats each)
  // than the 1 B/clk serializer drains (16 clk each), so committed-but-
  // unserialized frames exceed the 32-entry ts ring. The shed guard drops
  // whole frames at sof when the ring is full, so no live stamp is ever
  // lapped: the popped stamps are exactly the pushed stamps in FIFO order,
  // and pops + gPTP sheds account for all 40. On the unguarded RTL the ring
  // laps and the popped stamps diverge from the pushed ones (the mutation).
  void check_burst_never_laps_the_stamp_ring() {
    g_pushed.clear(); g_popped.clear();
    uint16_t drop0 = dut->dbg_tap_drop_o;
    g_ts_capture = true;
    for (int k = 0; k < 40; k++) {
      std::vector<uint8_t> f(16, 0);
      // DA 01:80:C2:00:00:0E, SA 00:80:E1:11:22:33
      const std::array<uint8_t, 6> da = {0x01,0x80,0xC2,0x00,0x00,0x0E};
      const std::array<uint8_t, 6> sa = {0x00,0x80,0xE1,0x11,0x22,0x33};
      for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
      f[12] = 0x88; f[13] = 0xF7;             // EtherType (accepted by the tap)
      f[14] = 0x10; f[15] = 0x02;             // sv/version/message_type, ptp ver
      send_wide(f);                            // 2 wide beats, back-to-back
    }
    run(40000);                                // drain the whole burst
    g_ts_capture = false;
    uint16_t sheds = static_cast<uint16_t>(dut->dbg_tap_drop_o - drop0);

    // the FIFO/subsequence law: every popped stamp is the pushed stamp at the
    // same position -- no entry was lapped over a still-live one.
    bool law = (g_popped.size() == g_pushed.size()) && !g_popped.empty();
    for (size_t i = 0; law && i < g_popped.size(); i++)
      if (g_popped[i] != g_pushed[i]) law = false;
    expect("ts-ring burst: popped stamps are the pushed stamps, in order", law, 1);
    // the pushed stamps must be strictly increasing (each frame's own arrival
    // phc): proves they are real per-frame stamps, not a stuck value.
    bool mono = g_pushed.size() > 1;
    for (size_t i = 1; mono && i < g_pushed.size(); i++)
      if (g_pushed[i] <= g_pushed[i - 1]) mono = false;
    expect("ts-ring burst: pushed stamps strictly increasing (real arrivals)",
           mono, 1);
    // accounting: every one of the 40 frames either serialized (a pop) or was
    // shed at the tap; the ring never silently swallowed one.
    expect("ts-ring burst: pops + gPTP sheds == 40",
           static_cast<int>(g_popped.size()) + static_cast<int>(sheds), 40);
    // the guard must actually engage on this burst (else the law is vacuous).
    expect("ts-ring burst: the guard shed at least one frame", sheds > 0, 1);
  }

  // ---- 9: issue #122 -- the guard must not LEAK. A gPTP frame accepted at
  // the tap but then dropped INSIDE the frame FIFO (oversize, or FIFO-full)
  // never commits, so it never pushes and never pops. An occupancy counted at
  // the tap and released only on pop leaks one slot per such frame and, after
  // 32, wedges the guard into shedding EVERYTHING -- a permanently deaf
  // plane, which is worse than the lap this ticket fixes. Drive 40 oversize
  // gPTP frames (> the 2 KB frame FIFO, so the FIFO drops each one) and then
  // require a normal frame to still reach the engine.
  void check_fifo_drops_do_not_leak_ring_slots() {
    for (int k = 0; k < 40; k++) {
      Frame f = ptp(0x0, static_cast<uint16_t>(0x7300 + k), 0, 0x0208, 10);
      f.ts(0);
      while (f.b.size() < 3000) f.u8(0xAA);   // oversize: dropped in the FIFO
      send_wide(f.b);
      run(400);
    }
    run(20000);
    g_pushed.clear();
    g_ts_capture = true;
    Frame g = ptp(0x2, 0x7400, 0, 0, 20);     // a normal, well-spaced frame
    send_wide(g.b);
    run(4000);
    g_ts_capture = false;
    expect("no leak: the plane still accepts after 40 FIFO-dropped frames",
           g_pushed.size() >= 1, 1);
  }

  // ---- 10: issue #122 -- the SHED path must not leak either, and the guard
  // must not drift burst over burst. A shed frame never enters the frame
  // FIFO, so counting it as an entry would leak one slot per shed and wedge
  // the guard shut after 32 -- the same permanent deafness as phase 9, by a
  // different route, and phase 8 alone cannot see it because a single burst
  // sheds only a handful. Repeat the burst and require the per-burst shed
  // count NOT to grow: a leak makes every repetition shed strictly more,
  // ending in all-shed.
  void check_shed_path_does_not_leak_across_bursts() {
    long sheds[4];
    for (int rep = 0; rep < 4; rep++) {
      uint16_t d0 = dut->dbg_tap_drop_o;
      g_pushed.clear(); g_popped.clear();
      g_ts_capture = true;
      for (int k = 0; k < 40; k++) {
        std::vector<uint8_t> f(16, 0);
        const std::array<uint8_t, 6> da = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        const std::array<uint8_t, 6> sa = {0x00,0x80,0xE1,0x11,0x22,0x33};
        for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
        f[12] = 0x88; f[13] = 0xF7;
        f[14] = 0x10; f[15] = 0x02;
        send_wide(f);
      }
      run(40000);
      g_ts_capture = false;
      sheds[rep] =
          static_cast<long>(static_cast<uint16_t>(dut->dbg_tap_drop_o - d0));
      // the per-burst law still holds on every repetition. !empty() is NOT
      // decoration: without it a plane that sheds EVERYTHING satisfies every
      // check in this phase vacuously (0 == 0 pops, 0 + 40 == 40, and a flat
      // shed count) -- the phase added to catch a wedge would be blind to the
      // wedge. Phase 8 carries the same guard for the same reason.
      bool law = (g_popped.size() == g_pushed.size()) && !g_popped.empty();
      for (size_t i = 0; law && i < g_popped.size(); i++)
        if (g_popped[i] != g_pushed[i]) law = false;
      expect("repeat burst: no lap on this repetition", law, 1);
      expect("repeat burst: pops + sheds == 40",
             static_cast<int>(g_popped.size()) + static_cast<int>(sheds[rep]),
             40);
    }
    // EQUALITY, not <=: on correct RTL every repetition sheds exactly the
    // same count, so an exact compare is deterministic. A <= endpoint compare
    // passes or fails on pointer PHASE for the occupancy bugs this is meant to
    // lock out -- one measured pattern was [19,3,13,3], where 3 <= 19 sails
    // through the very regression it exists to catch.
    for (int rep = 1; rep < 4; rep++)
      expect("repeat burst: shed count identical across repetitions",
             sheds[rep] == sheds[0], 1);
  }

  // ---- 11: issue #122 -- the shed must stay ATOMIC for frames LONGER than
  // two beats. A shed frame is held out of the FIFO by routing FW_HEAD1 to
  // FW_SKIP; lose that route and beats 2..N of a shed frame enter as a
  // HEADLESS partial frame, commit as good, and push a ghost stamp with no
  // matching entry count -- the sum under-counts and the ring laps again,
  // which is precisely the defect this ticket fixes. Phases 8 and 10 cannot
  // see it: their frames are two beats, so a shed frame never leaves
  // FW_HEAD1. The size must also stay small enough that the 2 KB frame FIFO
  // does NOT saturate, or its own overflow drop masks the ghost push. 24 and
  // 56 bytes sit in that window (a real Pdelay_Req is 68).
  void check_long_frame_shed_stays_atomic() {
    for (int fb = 0; fb < 2; fb++) {
      const size_t flen = (fb == 0) ? 24 : 56;
      const int    nfr  = 60;
      uint16_t d0 = dut->dbg_tap_drop_o;
      g_pushed.clear(); g_popped.clear();
      g_ts_capture = true;
      for (int k = 0; k < nfr; k++) send_wide(tapframe(flen, true));
      run(120000);
      g_ts_capture = false;
      long sheds =
          static_cast<long>(static_cast<uint16_t>(dut->dbg_tap_drop_o - d0));
      bool law = (g_popped.size() == g_pushed.size()) && !g_popped.empty();
      for (size_t i = 0; law && i < g_popped.size(); i++)
        if (g_popped[i] != g_pushed[i]) law = false;
      expect("long-frame shed stays atomic: popped == pushed, in order", law, 1);
      expect("long-frame shed stays atomic: pops + sheds == 60",
             static_cast<int>(g_popped.size()) + static_cast<int>(sheds), nfr);
    }

  }

  // ---- 12: the shed diagnostic counts gPTP sheds ONLY. The guard sheds at
  // beat 0, BEFORE the EtherType verdict lands at beat 1, so on a busy link
  // most shed frames are not gPTP at all -- counting those would poison
  // dbg_tap_drop_o, which is what a silicon reader uses to size the loss.
  // Saturate the ring with short gPTP frames while interleaving AVTP ones:
  // the accounting law below holds only if the count is EtherType-gated.
  void check_shed_count_is_ethertype_gated() {
    const int npair = 60;
    uint16_t d0 = dut->dbg_tap_drop_o;
    g_pushed.clear(); g_popped.clear();
    g_ts_capture = true;
    for (int k = 0; k < npair; k++) {
      send_wide(tapframe(24, true));
      send_wide(tapframe(24, false));       // foreign ethertype, also shed-able
    }
    run(120000);
    g_ts_capture = false;
    long sheds =
        static_cast<long>(static_cast<uint16_t>(dut->dbg_tap_drop_o - d0));
    expect("mixed traffic: pops + gPTP sheds == the 60 gPTP frames sent",
           static_cast<int>(g_popped.size()) + static_cast<int>(sheds), npair);
  }

  // ---- 13: #214 -- the master role puts the other three types on the
  // lane. Until here the run emits Pdelay_Req, Pdelay_Resp and its
  // Follow_Up only, so the tag would be proved for three of the
  // six types the plane transmits and a mutation correct for everything
  // but Announce would pass. With no announce refreshed the receipt timeout
  // expires, the plane becomes grandmaster, and Announce, Sync and
  // Follow_Up join the lane. Last, because a plane that is its own
  // grandmaster no longer consumes the peer syncs the earlier phases use.
  //! Returns the frame index the master-role checks below start from.
  size_t ride_quietly_to_grandmaster() {
    size_t before = txf.size();        // the first Announce rides the
    uint64_t spent = 0;                // transition itself, so mark first
    size_t ann_stamp_mark = stamps.size();
    while (!(dut->pub_flags_o & FL_AMGM) && spent < 18000000ull) {
      run_svc(1000);
      spent += 1000;
    }
    expect("quiet ride to grandmaster",
           (dut->pub_flags_o & FL_AMGM) ? 1 : 0, 1);

    // Let the transition's Announce return and dispatch before arming the
    // selective Sync hold. Otherwise an Announce emitted immediately after
    // the first Sync can legitimately sit between the response-first pair
    // and the replay, obscuring the exact 3,A,0 delivery proof.
    bool ann_stamp_seen = false;
    for (uint64_t n = 0; n < 2000000ull && !ann_stamp_seen; n += 1000) {
      for (size_t k = ann_stamp_mark; k < stamps.size(); k++)
        if (stamps[k].type == 0xB) ann_stamp_seen = true;
      if (!ann_stamp_seen) run_svc(1000);
    }
    expect("master Announce stamp precedes the Sync collision",
           ann_stamp_seen ? 1 : 0, 1);
    run_svc(2000);                     // finish its timestamp handler
    return before;
  }

  //! Phase 13's collision arm: hold the next master Sync's launch record,
  //! then prove a same-sequence peer response cannot take its place.
  void check_master_sync_collision(size_t before) {
    dut->rechold_type_i = 0x0;         // hold the next Sync's record
    dut->rechold_en_i = 1;
    expect("the selected master Sync record is held",
           wait_rec_held(2000000) ? 1 : 0, 1);
    expect("held Sync record keeps messageType", dut->dbg_rec_held_type_o, 0x0);
    dut->rechold_en_i = 0;

    uint16_t clash = dut->dbg_rec_held_seq_o;
    uint16_t sync_ev_drop = dut->dbg_ev_drop_o;

    // Locate the Sync frame the observer recorded. The full-run
    // one-result-per-frame law below independently proves this positional map.
    size_t sync_idx = 0;
    bool held_sync_seen = false;
    for (size_t k = before; k < txf.size() && k < records.size(); k++) {
      if (txf[k].size() > 45 && (txf[k][14] & 0xF) == 0x0 &&
          static_cast<uint16_t>((txf[k][44] << 8) | txf[k][45]) == clash &&
          records[k].type == 0x0 && records[k].seq == clash) {
        sync_idx = k;
        held_sync_seen = true;
        break;
      }
    }
    expect("held Sync has a real launch record", held_sync_seen ? 1 : 0, 1);
    if (held_sync_seen)
      expect("the held Sync record is not an abort", records[sync_idx].abort, 0);

    if (held_sync_seen)
      check_sync_collision_delivers_in_frame_order(clash, sync_ev_drop);
  }

  //! The deliveries the held Sync collision must produce, in FRAME order:
  //! the Sync itself first, because it left first, then the response that
  //! was admitted behind it. Nothing at all while the Sync's record is held.
  void check_sync_collision_delivers_in_frame_order(uint16_t clash,
                                                    uint16_t sync_ev_drop) {
    size_t collision_mark = txf.size();
    size_t sync_eng_mark = stamps.size();
    tx_seen = collision_mark;

    // A peer request using the Sync sequence creates a type-3 claim with the
    // same 16-bit sequence. Only the frames' POSITIONS separate them now.
    Frame same = ptp(0x2, clash, 0, 0x0000, 20, PEER_CID);
    same.u64(0); same.u64(0); same.u32(0);
    send_wide(same.b);
    std::vector<uint8_t> rsp = wait_tx(0x3, 200000);
    expect("equal Sync/Resp sequences: the peer request is answered",
           rsp.empty() ? 0 : 1, 1);
    run(4000);
    int premature_sync_fu = 0;
    int premature_resp_fu = 0;
    for (size_t k = collision_mark; k < txf.size(); k++) {
      if (txf[k].size() <= 14) continue;
      if ((txf[k][14] & 0xF) == 0x8) premature_sync_fu++;
      if ((txf[k][14] & 0xF) == 0xA) premature_resp_fu++;
    }
    expect("no Sync Follow_Up while the Sync's own record is held",
           premature_sync_fu, 0);
    expect("no Resp_Follow_Up while an older record is held",
           premature_resp_fu, 0);
    expect("no result reaches the engine while the record is held",
           stamps.size(), sync_eng_mark);
    expect("the Sync record is still held", dut->dbg_rec_held_o, 1);

    release_rec();
    run(4000);
    expect("the collision delivers the Sync and then the response",
           stamps.size() >= sync_eng_mark + 2 ? 1 : 0, 1);
    if (stamps.size() >= sync_eng_mark + 2) {
      expect("Sync collision delivery 1 is the Sync that left first",
             stamps[sync_eng_mark].type, 0x0);
      expect("Sync collision delivery 2 is the Pdelay_Resp behind it",
             stamps[sync_eng_mark + 1].type, 0x3);
      for (size_t k = sync_eng_mark; k < sync_eng_mark + 2; k++)
        expect("both Sync-collision deliveries share the sequenceId",
               stamps[k].seq, clash);
      expect("the two Sync-collision deliveries carry DIFFERENT times",
             stamps[sync_eng_mark].ns != stamps[sync_eng_mark + 1].ns ? 1 : 0,
             1);
    }
    std::vector<uint8_t> fu = wait_tx(0x8, 400000);
    expect("the released Sync result builds its own Follow_Up",
           fu.empty() ? 0 : 1, 1);
    if (!fu.empty() && stamps.size() >= sync_eng_mark + 1) {
      expect("released Sync Follow_Up keeps the common sequence",
             static_cast<uint16_t>((fu[44] << 8) | fu[45]), clash);
      expect("released Sync Follow_Up carries the SYNC's own time",
             timestamp_field_ns(fu, 48), stamps[sync_eng_mark].ns);
    }
    expect("the held Sync record is consumed exactly once",
           dut->dbg_rec_held_o, 0);
    expect("Sync collision changed no engine-event drop count",
           dut->dbg_ev_drop_o, sync_ev_drop);
  }

  //! With the plane its own grandmaster, Announce, Sync and Follow_Up all
  //! reach the lane, so the stamp tag is proved for every type it emits.
  void check_master_emits_all_three_types(size_t before) {
    run_svc(1400000);                  // an announce interval and then some
    int saw_ann = 0;
    int saw_sync = 0;
    int saw_fu = 0;
    for (size_t k = before; k < txf.size(); k++) {
      if (txf[k].size() <= 14) continue;
      int t = txf[k][14] & 0xF;
      if (t == 0xB) saw_ann = 1;
      if (t == 0x0) saw_sync = 1;
      if (t == 0x8) saw_fu = 1;
    }
    expect("as master: an Announce reached the lane", saw_ann, 1);
    expect("as master: a Sync reached the lane", saw_sync, 1);
    expect("as master: its Follow_Up reached the lane", saw_fu, 1);
  }

  // ---- 14: #40 -- same-type response ownership under real backpressure --
  // Stop the production wide TX lane before two complete peer requests enter
  // through the real tap/FIFO/parser path. Request 2 can therefore reach the
  // donor while response 1 still has no boundary timestamp. Two valid
  // Signaling chasers then reuse both ping-pong message banks. The one-slot
  // test gate holds response 1's REAL stamper tuple: request 2 must stay
  // behind the open response owner, retain its event snapshot through that
  // bank churn, and keep its own requester identity and boundary time.
  void check_same_type_response_ownership() {
    pd_on = false;
    service_pdelay();
    for (int k = 0; k < 2000 && (dut->tx_tvalid_o || in_tx); k++) tick();
    //! Begin from a quiet, reset production lane so the first stalled frame
    //! can only be response 1; post-reset periodic traffic is still more than
    //! two million clocks away.
    close_epoch();
    dut->rst_n = 0;
    for (int i = 0; i < kResetTicks; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    pd_seen = txf.size();
    tx_seen = txf.size();
    epoch_txf_base = txf.size();
    run(512);

    Frame q1 = ptp(0x2, Q1, 0, 0x0000, 20, C1);
    q1.u64(0); q1.u64(0); q1.u32(0);
    Frame q2 = ptp(0x2, Q2, 0, 0x0000, 20, C2);
    q2.b[42] = static_cast<uint8_t>(P2 >> 8);
    q2.b[43] = static_cast<uint8_t>(P2);
    q2.u64(0); q2.u64(0); q2.u32(0);

    const size_t mark = txf.size();
    const uint16_t evdrop0 = dut->dbg_ev_drop_o;
    const uint16_t disc0 = dut->dbg_txts_disc_o;

    dut->rechold_type_i = 0x3;
    dut->rechold_en_i = 1;
    dut->tx_tready_i = 0;
    const uint64_t q1_rx = phc();
    send_wide(q1.b);
    const uint64_t q2_rx = phc();
    send_wide(q2.b);
    Frame chase1 = ptp(0xC, 0xD00D, 0, 0x0000, 0);
    Frame chase2 = ptp(0xC, 0xBEEF, 0, 0x0000, 0);
    send_wide(chase1.b);
    send_wide(chase2.b);
    check_backpressure_holds_the_lane();
    const int resp1 = check_response_one_owns_its_stamp(mark, q1_rx);
    check_second_response_waits_for_the_owner(mark, resp1, q2_rx, evdrop0,
                                              disc0);
  }

  //! Phase 14's lane half: a stalled production frame must hold its start
  //! beat and its mid-frame beat without losing or inventing a byte.
  void check_backpressure_holds_the_lane() {
    for (int k = 0; k < 200000 && !dut->tx_tvalid_o; k++) tick();
    expect("backpressure: a production frame is presented",
           dut->tx_tvalid_o, 1);
    uint64_t start_data = dut->tx_tdata_o;
    uint8_t start_keep = dut->tx_tkeep_o;
    uint8_t start_last = dut->tx_tlast_o;
    size_t start_frames = txf.size();
    run(32);
    expect("backpressure: start valid holds", dut->tx_tvalid_o, 1);
    expect("backpressure: start data holds", dut->tx_tdata_o, start_data);
    expect("backpressure: start keep holds", dut->tx_tkeep_o, start_keep);
    expect("backpressure: start last holds", dut->tx_tlast_o, start_last);
    expect("backpressure: start accepts no frame", txf.size(), start_frames);

    dut->tx_tready_i = 1;
    for (int k = 0; k < 200000 && !(in_tx && cur.size() >= 16); k++) tick();
    expect("backpressure: a production body advances",
           (in_tx && cur.size() >= 16) ? 1 : 0, 1);
    dut->tx_tready_i = 0;
    uint64_t mid_data = dut->tx_tdata_o;
    uint8_t mid_keep = dut->tx_tkeep_o;
    uint8_t mid_last = dut->tx_tlast_o;
    size_t mid_size = cur.size();
    run(32);
    expect("backpressure: mid valid holds", dut->tx_tvalid_o, 1);
    expect("backpressure: mid data holds", dut->tx_tdata_o, mid_data);
    expect("backpressure: mid keep holds", dut->tx_tkeep_o, mid_keep);
    expect("backpressure: mid last holds", dut->tx_tlast_o, mid_last);
    expect("backpressure: mid accepts no byte", cur.size(), mid_size);
    dut->tx_tready_i = 1;
  }

  //! Response 1 owns its ledger entry: it carries its own requester and its
  //! own launch record, and response 2 must wait behind it because the
  //! ledger is ordered and response 1's result is still owed.
  //! Returns response 1's frame index, or -1 when it never appeared.
  int check_response_one_owns_its_stamp(size_t mark, uint64_t q1_rx) {
    int resp1 = -1;
    for (int k = 0; k < 400000 &&
                         (resp1 < 0 || !dut->dbg_rec_held_o); k++) {
      tick();
      resp1 = find_frame(mark, 0x3, Q1);
    }
    expect("same-type owner: response 1 sent", resp1 >= 0 ? 1 : 0, 1);
    expect("same-type owner: response 1 record is held",
           dut->dbg_rec_held_o, 1);
    if (resp1 >= 0)
      expect("backpressure: the stalled frame is response 1",
             static_cast<size_t>(resp1), mark);
    dut->rechold_en_i = 0;
    if (resp1 >= 0) {
      expect("same-type owner: response 1 requestReceiptTimestamp",
             timestamp_field_ns(txf[resp1], 48), q1_rx);
      expect("same-type owner: response 1 requester",
             fld64(txf[resp1], 58), C1);
      expect("same-type owner: response 1 port", fld16(txf[resp1], 66), P1);
      expect("same-type owner: held sequence",
             dut->dbg_rec_held_seq_o, Q1);
      expect("same-type owner: held type",
             dut->dbg_rec_held_type_o, 0x3);
    }
    run(2000);
    expect("same-type owner: response 2 waits for response 1's result",
           find_frame(mark, 0x3, Q2) < 0 ? 1 : 0, 1);
    return resp1;
  }

  //! Releasing response 1's record must produce its result, then Follow_Up
  //! 1, then response 2 and its Follow_Up, each with its own requester, port
  //! and time.
  void check_second_response_waits_for_the_owner(size_t mark, int resp1,
                                                 uint64_t q2_rx,
                                                 uint16_t evdrop0,
                                                 uint16_t disc0) {
    size_t eng_mark = stamps.size();
    release_rec();
    run(2000);
    expect("same-type owner: response 1's record releases once",
           dut->dbg_rec_held_o, 0);
    expect("same-type owner: response 1's result is delivered first",
           stamps.size() > eng_mark ? 1 : 0, 1);
    if (stamps.size() > eng_mark) {
      expect("same-type owner: the first delivery is response 1",
             stamps[eng_mark].type, 0x3);
      expect("same-type owner: the first delivery keeps Q1",
             stamps[eng_mark].seq, Q1);
    }

    int fu1 = -1;
    int resp2 = -1;
    int fu2 = -1;
    for (int k = 0; k < 600000 && (fu1 < 0 || resp2 < 0 || fu2 < 0); k++) {
      tick();
      fu1 = find_frame(mark, 0xA, Q1);
      resp2 = find_frame(mark, 0x3, Q2);
      fu2 = find_frame(mark, 0xA, Q2);
    }
    expect("same-type owner: Follow_Up 1 sent", fu1 >= 0 ? 1 : 0, 1);
    expect("same-type owner: response 2 sent", resp2 >= 0 ? 1 : 0, 1);
    expect("same-type owner: Follow_Up 2 sent", fu2 >= 0 ? 1 : 0, 1);
    if (fu1 >= 0 && resp2 >= 0)
      expect("same-type owner: Follow_Up 1 precedes response 2",
             fu1 < resp2 ? 1 : 0, 1);
    if (fu1 >= 0 && resp1 >= 0) {
      expect("same-type owner: Follow_Up 1 requester",
             fld64(txf[fu1], 58), C1);
      expect("same-type owner: Follow_Up 1 port", fld16(txf[fu1], 66), P1);
      if (wait_result(static_cast<size_t>(resp1)))
        expect("same-type owner: Follow_Up 1 carries response 1's time",
               timestamp_field_ns(txf[fu1], 48), stamps[resp1].ns);
    }
    if (resp2 >= 0) {
      expect("same-type owner: response 2 requestReceiptTimestamp",
             timestamp_field_ns(txf[resp2], 48), q2_rx);
      expect("same-type owner: response 2 requester",
             fld64(txf[resp2], 58), C2);
      expect("same-type owner: response 2 port", fld16(txf[resp2], 66), P2);
    }
    if (fu2 >= 0 && resp2 >= 0) {
      expect("same-type owner: Follow_Up 2 requester",
             fld64(txf[fu2], 58), C2);
      expect("same-type owner: Follow_Up 2 port", fld16(txf[fu2], 66), P2);
      if (wait_result(static_cast<size_t>(resp2)))
        expect("same-type owner: Follow_Up 2 carries response 2's time",
               timestamp_field_ns(txf[fu2], 48), stamps[resp2].ns);
    }
    expect("same-type owner: no record was discarded",
           dut->dbg_txts_disc_o, disc0);
    expect("same-type owner: event queue loses no request",
           dut->dbg_ev_drop_o, evdrop0);
    dut->tx_tready_i = 1;
  }

  // ---- 15: #41 -- warm reset cannot preserve a stale timer owner --------
  // Hold a real Pdelay_Req stamp across reset. Scratch state intentionally
  // survives warm reset for Milan cease history, but a pre-reset egress owner
  // must be hidden until a fresh transmitter writes one; otherwise every
  // later timer request remains suppressed forever.
  void check_warm_reset_clears_the_request_owner() {
    pd_on = false;
    pd_seen = txf.size();
    dut->rechold_type_i = 0x2;
    dut->rechold_en_i = 1;
    tx_seen = txf.size();
    size_t lost_req_idx = 0;
    std::vector<uint8_t> lost_req = wait_tx(0x2, 4000000, &lost_req_idx);
    expect("warm reset request: request sent", lost_req.empty() ? 0 : 1, 1);
    expect("warm reset request: its record is held",
           wait_rec_held(200000) ? 1 : 0, 1);
    if (!lost_req.empty()) {
      expect("warm reset request: held type", dut->dbg_rec_held_type_o, 0x2);
      expect("warm reset request: held sequence",
             dut->dbg_rec_held_seq_o, fld16(lost_req, 44));
    }
    dut->rechold_en_i = 0;
    close_epoch();
    dut->rst_n = 0;
    for (int i = 0; i < kResetTicks; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    dut->rechold_release_i = 0;
    // The root reset erases the ledger epoch and the queued record with it:
    // nothing is owed for a frame whose owner no longer exists, and the
    // plane says so rather than returning a result for an erased entry.
    expect("warm reset request: the volatile record queue clears",
           dut->dbg_rec_held_o, 0);
    epoch_txf_base = txf.size();

    pd_seen = txf.size();
    tx_seen = txf.size();
    size_t fresh_req_idx = 0;
    std::vector<uint8_t> fresh_req =
        wait_tx(0x2, 4000000, &fresh_req_idx);
    expect("warm reset request: cadence restarts",
           fresh_req.empty() ? 0 : 1, 1);

    // Re-answer that fresh request, then let the reset-armed receipt timer
    // take the plane back through asCapable and autonomous mastership.
    pd_seen = fresh_req.empty() ? txf.size() : fresh_req_idx;
    pd_on = true;
    service_pdelay();
    expect("warm reset request: asCapable re-earned",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    expect("warm reset request: mastership recovers",
           wait_flags(FL_AMGM, FL_AMGM, 12000000ull), 1);
  }

  // ---- 16: #41 -- warm reset cannot preserve a stale Sync owner ---------
  // Lose a real master Sync return across reset independently of the request
  // case. Boot must re-arm both cadence and announce-receipt timers: the
  // plane re-earns capability, becomes master again, and emits a fresh Sync
  // plus Follow_Up without any harness-supplied timestamp.
  void check_warm_reset_clears_the_sync_owner() {
    dut->rechold_type_i = 0x0;
    dut->rechold_en_i = 1;
    tx_seen = txf.size();
    size_t lost_sync_idx = 0;
    std::vector<uint8_t> lost_sync = wait_tx(0x0, 1000000, &lost_sync_idx);
    expect("warm reset Sync: Sync sent", lost_sync.empty() ? 0 : 1, 1);
    expect("warm reset Sync: its record is held",
           wait_rec_held(200000) ? 1 : 0, 1);
    if (!lost_sync.empty()) {
      expect("warm reset Sync: held type", dut->dbg_rec_held_type_o, 0x0);
      expect("warm reset Sync: held sequence",
             dut->dbg_rec_held_seq_o, fld16(lost_sync, 44));
    }
    dut->rechold_en_i = 0;
    close_epoch();
    dut->rst_n = 0;
    for (int i = 0; i < kResetTicks; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    dut->rechold_release_i = 0;
    expect("warm reset Sync: the volatile record queue clears",
           dut->dbg_rec_held_o, 0);
    epoch_txf_base = txf.size();

    pd_on = true;
    pd_seen = txf.size();
    expect("warm reset Sync: asCapable re-earned",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    expect("warm reset Sync: mastership recovers",
           wait_flags(FL_AMGM, FL_AMGM, 12000000ull), 1);
    tx_seen = txf.size();
    size_t fresh_sync_idx = 0;
    std::vector<uint8_t> fresh_sync =
        wait_tx(0x0, 1000000, &fresh_sync_idx);
    std::vector<uint8_t> fresh_fu = wait_tx(0x8, 200000);
    expect("warm reset Sync: cadence restarts",
           fresh_sync.empty() ? 0 : 1, 1);
    expect("warm reset Sync: Follow_Up restarts",
           fresh_fu.empty() ? 0 : 1, 1);
    if (!fresh_sync.empty() && !fresh_fu.empty()) {
      expect("warm reset Sync: Follow_Up sequence matches",
             fld16(fresh_fu, 44), fld16(fresh_sync, 44));
      // the fresh Sync is the (fresh_sync_idx - post_reset_base)-th frame of
      // the new epoch; the Follow_Up carries that frame's own reconstructed
      // launch, which the plane produced with no harness timestamp anywhere
      expect("warm reset Sync: Follow_Up carries a fresh reconstruction",
             timestamp_field_ns(fresh_fu, 48) != 0 ? 1 : 0, 1);
    }
  }

  //! Drop the harness's per-epoch views without folding them into the
  //! whole-run laws. The recovery phases deliberately TEAR a frame at the
  //! fence: that frame never reaches the wire, so it has a result and no
  //! record, and the positional views stop lining up by design. Their own
  //! assertions are the point, and the laws say plainly which frames they
  //! covered.
  void drop_epoch() {
    epoch_txf_base = txf.size();
    stamps.clear();
    records.clear();
    launch_ns.clear();
    rec_delayed.clear();
    cur.clear();
    in_tx = false;
    tx_first = true;
  }

  //! Bit layout of `dbg_txts_state_o`, as KL_gptp_txret publishes it.
  bool sealed() const { return (dut->dbg_txts_state_o >> 15) & 1; }
  bool demand() const { return (dut->dbg_txts_state_o >> 13) & 1; }

  //! Run until `n` cycles have passed, answering the peer as usual.
  void idle(uint64_t n) { run_svc(n); }

  //! Wait for a barrier count to move past `before`, or give up.
  bool wait_barrier(uint16_t before, uint64_t max_cycles) {
    for (uint64_t k = 0; k < max_cycles; k++) {
      if (dut->dbg_txts_barr_o != before) return true;
      tick();
      if ((k & 255) == 0) service_pdelay();
    }
    return false;
  }

  bool wait_unsealed(uint64_t max_cycles) {
    for (uint64_t k = 0; k < max_cycles; k++) {
      if (!sealed()) return true;
      tick();
      if ((k & 255) == 0) service_pdelay();
    }
    return false;
  }

  // ---- 17: the recovery demand (issue #360) ------------------------------
  // A fence is owed a recovery episode that REALLY destroys the frames it
  // fenced off. The two reset levels cannot say whether one happened:
  // `reinit` also carries the firmware's own hand, and disabling the guard
  // drops both outputs at once without the sequence ever completing. These
  // arms drive the REAL guard FSM inside the wrapper and require that the
  // demand survives everything short of an accepted, completed episode.
  //! ONE BAD FIELD, AT THE RECORD INTERFACE.
  //!
  //! The ledger's identity is POSITION, and the generation and the frame's
  //! own tag are the two independent cross-checks on it. The observer reset
  //! the recovery phases use moves BOTH the position and the generation at
  //! once, so it cannot tell a plane that checks the generation from one
  //! that does not - and a bench that cannot tell them apart is not
  //! evidence about either. These phases corrupt exactly ONE field of one
  //! record on its way to the ledger, leave the position correct, and
  //! require the refusal each time: a barrier, a seal, and a recovery that
  //! ends in an unsealed plane.
  void check_one_corrupt_field_is_refused(unsigned mode, const char *what) {
    char label[96];
    const auto say = [&](const char *tail) {
      std::snprintf(label, sizeof label, "%s: %s", what, tail);
      return label;
    };
    drop_epoch();
    expect(say("the plane starts this phase unsealed"),
           wait_unsealed(4000000) ? 1 : 0, 1);
    const uint16_t barr0 = dut->dbg_txts_barr_o;
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    dut->recfault_mode_i = static_cast<uint8_t>(mode);
    dut->recfault_en_i = 1;
    //! polled FINELY: the refusal, the seal and the recovery that follows
    //! it all complete within a few thousand cycles, so a coarse poll would
    //! read the plane after it had already recovered and call the seal
    //! absent
    bool fired = false;
    for (int k = 0; k < 2000000 && !fired; k++) {
      idle(4);
      fired = dut->dbg_recfault_fired_o != 0;
    }
    expect(say("the corrupted record reached the ledger"), fired ? 1 : 0, 1);
    expect(say("the ledger refused it and raised a barrier"),
           wait_barrier(barr0, 4000000) ? 1 : 0, 1);
    expect(say("the barrier sealed the plane"), sealed() ? 1 : 0, 1);
    //! WHAT THE BARRIER OWES. The entries it cancels are marked, never
    //! removed: each one still closes, in order, as a counted loss. A
    //! barrier that simply forgot them would leave this counter still and
    //! the occupancy at zero, which is why both are graded.
    const unsigned owed = dut->dbg_txts_state_o & 0xF;
    const uint16_t lost0 = dut->dbg_txts_lost_o;
    dut->recfault_en_i = 0;
    dut->recfault_mode_i = 0;
    expect(say("a completed episode follows"),
           wait_epi_done(done0, 8000000) ? 1 : 0, 1);
    expect(say("and the plane unseals again"),
           wait_unsealed(8000000) ? 1 : 0, 1);
    expect(say("every cancelled entry closed as a counted loss"),
           static_cast<unsigned>(uint16_t(dut->dbg_txts_lost_o - lost0)) >= owed
               ? 1 : 0, 1);
    expect(say("and none is left owed"), dut->dbg_txts_state_o & 0xF, 0);
    drop_epoch();
  }

  void check_a_record_that_is_not_this_frames_is_refused() {
    check_one_corrupt_field_is_refused(1, "generation zero");
    check_one_corrupt_field_is_refused(2, "foreign tag");
    check_one_corrupt_field_is_refused(3, "lost record");
    check_the_seal_waits_for_the_echo();
  }

  //! AN EXPIRED HEAD IS A DIAGNOSTIC, NOT A RETIREMENT.
  //!
  //! The ledger's head can wait a long time - a record crosses a clock
  //! domain behind a frame that is still on the wire - and the age counter
  //! exists to SAY when that wait became implausible, not to end it.
  //! Retiring the head on age would hand the next record to the wrong
  //! entry, which is the one failure the whole positional scheme exists to
  //! prevent. So here one record is held past the age limit and then
  //! released, and the frame it belongs to still gets its own time.
  void check_an_aged_head_is_not_retired() {
    drop_epoch();
    expect("aged head: the plane starts this phase unsealed",
           wait_unsealed(4000000) ? 1 : 0, 1);
    const uint16_t stall0 = dut->dbg_txts_stall_o;
    const uint16_t barr0 = dut->dbg_txts_barr_o;
    dut->rechold_type_i = 0x2;      //! the plane's own Pdelay_Req cadence
    dut->rechold_en_i = 1;
    bool held = false;
    for (int k = 0; k < 400000 && !held; k++) {
      idle(16);
      held = dut->dbg_rec_held_o != 0;
    }
    expect("aged head: a record is held back", held ? 1 : 0, 1);
    const uint16_t held_seq = dut->dbg_rec_held_seq_o;
    const uint8_t held_type = dut->dbg_rec_held_type_o;
    //! past the million-cycle age limit, with room to spare
    idle(1200000);
    expect("aged head: the age expired and was counted",
           dut->dbg_txts_stall_o != stall0 ? 1 : 0, 1);
    expect("aged head: the entry is still owed",
           (dut->dbg_txts_state_o & 0xF) != 0 ? 1 : 0, 1);
    expect("aged head: an expiry is not a barrier",
           dut->dbg_txts_barr_o, barr0);
    const size_t res0 = stamps.size();
    dut->rechold_release_i = 1;
    idle(64);
    dut->rechold_release_i = 0;
    dut->rechold_en_i = 0;
    idle(200000);
    //! a MEASUREMENT, not a loss: a plane that retired the head on age
    //! would close this very entry with an explicit loss carrying the same
    //! identity, and that is the answer this phase exists to refuse
    bool delivered = false;
    for (size_t i = res0; i < stamps.size(); i++)
      if (stamps[i].seq == held_seq && stamps[i].type == held_type
          && stamps[i].ok)
        delivered = true;
    expect("aged head: the late record still delivers its own frame",
           delivered ? 1 : 0, 1);
    drop_epoch();
  }

  //! THE ECHO IS THE ACKNOWLEDGEMENT, and nothing else is.
  //!
  //! A completed recovery episode discharges the DEMAND - it proves the
  //! frames this plane handed over were destroyed. It says nothing about
  //! where the observer now is, and the plane cannot credit a position it
  //! has not re-established. So the seal has to outlast an episode that
  //! completed while the observer was still in reset, and lift only when
  //! the observer answers for the generation it was sealed with.
  void check_the_seal_waits_for_the_echo() {
    drop_epoch();
    expect("echo: the plane starts this phase unsealed",
           wait_unsealed(4000000) ? 1 : 0, 1);
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    //! raise the barrier at the RECORD interface, so the observer itself is
    //! untouched until this phase chooses to hold it
    dut->recfault_mode_i = 1;
    dut->recfault_en_i = 1;
    bool fired = false;
    for (int k = 0; k < 2000000 && !fired; k++) {
      idle(4);
      fired = dut->dbg_recfault_fired_o != 0;
    }
    expect("echo: a barrier was raised", fired ? 1 : 0, 1);
    //! ...and from here the observer cannot answer at all
    dut->obs_rst_i = 1;
    dut->recfault_en_i = 0;
    dut->recfault_mode_i = 0;
    expect("echo: the plane is sealed", sealed() ? 1 : 0, 1);
    expect("echo: an episode completes while the observer is held",
           wait_epi_done(done0, 8000000) ? 1 : 0, 1);
    const size_t res0 = stamps.size();
    idle(200000);
    expect("echo: the seal outlasts it", sealed() ? 1 : 0, 1);
    expect("echo: and nothing is resolved without a position",
           stamps.size(), res0);
    dut->obs_rst_i = 0;
    expect("echo: releasing the observer unseals the plane",
           wait_unsealed(8000000) ? 1 : 0, 1);
    drop_epoch();
  }

  void check_recovery_demand_survives_an_unaccepted_request() {
    drop_epoch();
    expect("recovery: the plane starts this phase unsealed and stamping",
           wait_unsealed(2000000) ? 1 : 0, 1);

    check_disabled_guard_holds_the_seal();
    check_masked_request_keeps_its_demand();
    check_aborted_episode_is_not_a_completion();
    check_held_firmware_reinit_holds_the_seal();
    check_stopped_eth_clock_holds_the_seal();
    check_torn_frame_is_discarded_and_counted();
  }

  //! A DISABLED GUARD refuses every trigger, so the demand cannot be met
  //! and nothing may be resolved or unsealed. The plane must also stop
  //! asking: each request rides the shared manual net, and a request the
  //! guard will certainly refuse would only disturb the MAC system side.
  void check_disabled_guard_holds_the_seal() {
    dut->linkg_dis_i = 1;
    idle(2000);
    const uint16_t barr0 = dut->dbg_txts_barr_o;
    // Reset the observer alone: its records then carry generation 0 and a
    // position the plane never expected, which is an internal invariant
    // violation and raises a barrier with no reset level involved.
    dut->obs_rst_i = 1;
    idle(200);
    dut->obs_rst_i = 0;
    expect("recovery: an observer reset raises a barrier",
           wait_barrier(barr0, 4000000) ? 1 : 0, 1);
    expect("recovery: the barrier seals the plane", sealed() ? 1 : 0, 1);
    expect("recovery: the barrier leaves a demand standing", demand() ? 1 : 0, 1);

    const uint16_t req0 = dut->dbg_recov_req_cnt_o;
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    const size_t res0 = stamps.size();
    idle(400000);
    expect("recovery: a disabled guard is not asked",
           dut->dbg_recov_req_cnt_o, req0);
    expect("recovery: a disabled guard completes no episode",
           dut->dbg_epi_done_cnt_o, done0);
    expect("recovery: nothing is resolved while the demand is unmet",
           stamps.size(), res0);
    expect("recovery: the seal is still closed", sealed() ? 1 : 0, 1);

    dut->linkg_dis_i = 0;
    expect("recovery: re-enabling the guard obtains an accepted episode",
           wait_epi_done(done0, 4000000) ? 1 : 0, 1);
    expect("recovery: the plane asked for exactly that episode",
           dut->dbg_recov_req_cnt_o > req0 ? 1 : 0, 1);
    expect("recovery: the completed episode unseals the plane",
           wait_unsealed(4000000) ? 1 : 0, 1);
    expect("recovery: stamping resumes", wait_result_growth(stamps.size(),
                                                            8000000) ? 1 : 0, 1);
  }

  //! A REQUEST THE GUARD CANNOT SEE discharges nothing. With the firmware's
  //! own LINK_CTRL[1] held high the shared manual net is already high, so
  //! the plane's one-cycle request creates no edge at all. The demand has
  //! to survive that, the request has to be retried - which means the line
  //! has to go low again - and releasing the firmware level has to let the
  //! very next attempt through.
  void check_masked_request_keeps_its_demand() {
    drop_epoch();
    dut->linkg_dis_i = 1;
    idle(2000);
    const uint16_t barr0 = dut->dbg_txts_barr_o;
    dut->obs_rst_i = 1;
    idle(200);
    dut->obs_rst_i = 0;
    expect("masked request: a barrier is raised",
           wait_barrier(barr0, 4000000) ? 1 : 0, 1);
    // Mask the trigger BEFORE the guard is re-enabled, so the level is
    // already high when the plane starts asking and no edge can form.
    dut->cfg_mac_reinit_i = 1;
    idle(64);
    dut->linkg_dis_i = 0;
    const uint16_t req0 = dut->dbg_recov_req_cnt_o;
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    idle(400000);
    expect("masked request: the plane keeps asking",
           dut->dbg_recov_req_cnt_o > req0 ? 1 : 0, 1);
    expect("masked request: no episode was accepted",
           dut->dbg_epi_done_cnt_o, done0);
    expect("masked request: the demand still stands", demand() ? 1 : 0, 1);
    expect("masked request: the seal still holds", sealed() ? 1 : 0, 1);

    dut->cfg_mac_reinit_i = 0;
    expect("masked request: releasing the mask lets a request through",
           wait_epi_done(done0, 4000000) ? 1 : 0, 1);
    expect("masked request: the plane unseals after that episode",
           wait_unsealed(4000000) ? 1 : 0, 1);
  }

  //! DISABLING THE GUARD MID-EPISODE drops both reset outputs at once,
  //! which is indistinguishable from a completed episode to anything
  //! watching the levels. It is not a completion, and it must not unseal.
  void check_aborted_episode_is_not_a_completion() {
    drop_epoch();
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    const uint16_t barr0 = dut->dbg_txts_barr_o;
    // one firmware edge starts a real episode, and its reset levels raise
    // the plane's barrier at the same instant
    dut->cfg_mac_reinit_i = 1;
    tick();
    dut->cfg_mac_reinit_i = 0;
    expect("aborted episode: the barrier is raised",
           wait_barrier(barr0, 100000) ? 1 : 0, 1);
    // let the episode reach the half of SETTLE where the eth reset has
    // already been released and only the system side is still held
    for (int k = 0; k < 200000 &&
                    !(dut->dbg_linkg_epi_busy_o && !dut->dbg_linkg_eth_rst_o &&
                      dut->dbg_linkg_reinit_o); k++)
      tick();
    expect("aborted episode: the guard released eth first",
           (dut->dbg_linkg_epi_busy_o && !dut->dbg_linkg_eth_rst_o &&
            dut->dbg_linkg_reinit_o) ? 1 : 0, 1);
    // abort it there: both outputs go low together, with no completion
    dut->linkg_dis_i = 1;
    idle(200);
    expect("aborted episode: both reset levels are low",
           (dut->dbg_linkg_reinit_o || dut->dbg_linkg_eth_rst_o) ? 1 : 0, 0);
    expect("aborted episode: the guard published no completion",
           dut->dbg_epi_done_cnt_o, done0);
    const size_t res0 = stamps.size();
    idle(200000);
    expect("aborted episode: low reset levels do NOT unseal the plane",
           sealed() ? 1 : 0, 1);
    expect("aborted episode: nothing is resolved by an abort",
           stamps.size(), res0);
    expect("aborted episode: the demand survives it", demand() ? 1 : 0, 1);

    dut->linkg_dis_i = 0;
    expect("aborted episode: a later episode completes",
           wait_epi_done(done0, 8000000) ? 1 : 0, 1);
    expect("aborted episode: only then does the plane unseal",
           wait_unsealed(4000000) ? 1 : 0, 1);
  }

  //! A HELD FIRMWARE LINK_CTRL[1] keeps the MAC system side in reset after
  //! the episode has completed. The plane must not resolve anything while
  //! that level stands, and must resolve as soon as it is released.
  void check_held_firmware_reinit_holds_the_seal() {
    drop_epoch();
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    dut->cfg_mac_reinit_i = 1;          // held, not pulsed
    expect("held reinit: the episode it triggered completes",
           wait_epi_done(done0, 4000000) ? 1 : 0, 1);
    const size_t res0 = stamps.size();
    idle(200000);
    expect("held reinit: the plane stays sealed while the level stands",
           sealed() ? 1 : 0, 1);
    expect("held reinit: nothing is resolved while the level stands",
           stamps.size(), res0);
    dut->cfg_mac_reinit_i = 0;
    expect("held reinit: releasing it unseals the plane",
           wait_unsealed(4000000) ? 1 : 0, 1);
  }

  //! A STOPPED ETH CLOCK is what the guard exists for. The episode it
  //! starts cannot finish while the clock is dead, so the seal legitimately
  //! holds; the plane claims nothing and recovers when the clock returns.
  void check_stopped_eth_clock_holds_the_seal() {
    drop_epoch();
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    dut->eth_alive_i = 0;
    for (int k = 0; k < 20000 && !dut->dbg_linkg_epi_busy_o; k++) tick();
    expect("stopped clock: the guard declares the clock dead",
           dut->dbg_linkg_epi_busy_o, 1);
    const size_t res0 = stamps.size();
    idle(200000);
    expect("stopped clock: no episode completes while it is dead",
           dut->dbg_epi_done_cnt_o, done0);
    expect("stopped clock: the plane stays sealed", sealed() ? 1 : 0, 1);
    expect("stopped clock: nothing is resolved", stamps.size(), res0);
    dut->eth_alive_i = 1;
    expect("stopped clock: the episode completes when it returns",
           wait_epi_done(done0, 4000000) ? 1 : 0, 1);
    expect("stopped clock: the plane unseals",
           wait_unsealed(4000000) ? 1 : 0, 1);
  }

  //! A FRAME MID-EGRESS AT THE FENCE is completed by local discard,
  //! independent of downstream ready, and counted as departed: its leading
  //! beats are already past this plane and the episode destroys them with
  //! everything else the MAC path held.
  void check_torn_frame_is_discarded_and_counted() {
    drop_epoch();
    const uint16_t torn0 = dut->dbg_txts_torn_o;
    const uint16_t done0 = dut->dbg_epi_done_cnt_o;
    bool armed = false;
    for (int k = 0; k < 8000000 && !armed; k++) {
      tick();
      if ((k & 255) == 0) service_pdelay();
      if (in_tx && cur.size() >= 8) {
        // a frame is part way out of this plane: fence it here
        dut->cfg_mac_reinit_i = 1;
        tick();
        dut->cfg_mac_reinit_i = 0;
        armed = true;
      }
    }
    expect("torn frame: a frame was mid-egress when the fence closed",
           armed ? 1 : 0, 1);
    idle(4000);
    expect("torn frame: the plane discarded it locally and counted it",
           dut->dbg_txts_torn_o > torn0 ? 1 : 0, 1);
    expect("torn frame: the episode that destroys it completes",
           wait_epi_done(done0, 8000000) ? 1 : 0, 1);
    expect("torn frame: the plane unseals afterwards",
           wait_unsealed(8000000) ? 1 : 0, 1);
    expect("torn frame: every entry was resolved, none left owed",
           (dut->dbg_txts_state_o & 0xF), 0);
    drop_epoch();
  }

  bool wait_epi_done(uint16_t before, uint64_t max_cycles) {
    for (uint64_t k = 0; k < max_cycles; k++) {
      if (dut->dbg_epi_done_cnt_o != before) return true;
      tick();
      if ((k & 255) == 0) service_pdelay();
    }
    return false;
  }

  bool wait_result_growth(size_t before, uint64_t max_cycles) {
    for (uint64_t k = 0; k < max_cycles; k++) {
      if (stamps.size() > before) return true;
      tick();
      if ((k & 255) == 0) service_pdelay();
    }
    return false;
  }

  // ---- 18: the PHC trajectory the reconstruction is valid across -------
  // The egress timestamp is a captured PHC value minus a fixed number of
  // clock periods. That arithmetic is only true if the counter was
  // running, at its nominal step, with a bounded addend, for the WHOLE
  // interval it reaches back across - so the qualification is over a
  // window of history and its guard is observable here, not inferred from
  // the refusals it causes.
  void check_phc_trajectory_qualification() {
    drop_epoch();
    idle(4000);
    expect("phc: the guard is clear on a nominal trajectory",
           dut->dbg_phc_dirtcyc_o, 0);

    check_held_disable_refuses_every_capture();
    check_non_nominal_increment_refuses_every_capture();
    check_restored_excursion_still_refuses();
    check_settime_reloads_the_guard();
    drop_epoch();
  }

  //! A DISABLE HELD BEYOND THE WINDOW. The counter stops, so no interval
  //! that overlaps the hold can be reconstructed; the guard stays loaded
  //! for the whole hold and for a full window after it.
  void check_held_disable_refuses_every_capture() {
    const uint16_t pl0 = dut->dbg_txts_phcl_o;
    dut->phc_en_i = 0;
    idle(400000);
    expect("phc: a held disable keeps the guard loaded",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    expect("phc: every capture inside the hold is an explicit loss",
           dut->dbg_txts_phcl_o > pl0 ? 1 : 0, 1);
    expect("phc: not one of them was published as a measurement",
           measurements_since(pl0), 0);
    dut->phc_en_i = 1;
    tick();                              // the edge that reloads the guard
    expect("phc: returning to nominal reloads the guard once more",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    for (int k = 0; k < kReconGuardCyc - 1; k++) tick();
    expect("phc: the guard is still loaded one cycle short of the window",
           dut->dbg_phc_dirtcyc_o != 0 ? 1 : 0, 1);
    tick();
    expect("phc: the guard clears after exactly the full window",
           dut->dbg_phc_dirtcyc_o, 0);
  }

  //! A NON-NOMINAL INCREMENT is a different clock, not a slow one: the
  //! correction is a count of nominal periods and it does not describe
  //! this trajectory at all.
  void check_non_nominal_increment_refuses_every_capture() {
    const uint16_t pl0 = dut->dbg_txts_phcl_o;
    dut->phc_incr_i = 0x08000001u;      // one Q8.24 unit off nominal
    idle(400000);
    expect("phc: one unit off nominal keeps the guard loaded",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    expect("phc: every capture at a non-nominal step is an explicit loss",
           dut->dbg_txts_phcl_o > pl0 ? 1 : 0, 1);
    expect("phc: not one of them was published as a measurement",
           measurements_since(pl0), 0);
    dut->phc_incr_i = 0x08000000u;
    idle(4000);
    expect("phc: the guard clears when the nominal step returns",
           dut->dbg_phc_dirtcyc_o, 0);
  }

  //! AN EXCURSION RESTORED JUST BEFORE A CAPTURE still fails. This is the
  //! arm a guard that only looked at the capture instant would pass: the
  //! addend is back inside the envelope by then, and the interval behind
  //! it is not.
  void check_restored_excursion_still_refuses() {
    dut->phc_adj_ovr_en_i = 1;
    dut->phc_adj_ovr_i = kAdjExcursion;
    idle(4000);
    expect("phc: an excessive addend keeps the guard loaded",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    dut->phc_adj_ovr_i = 0;             // restored, inside the envelope
    tick();                              // the edge that reloads the guard
    expect("phc: restoring the addend reloads the guard once more",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    for (int k = 0; k < kReconGuardCyc - 1; k++) tick();
    expect("phc: still loaded one cycle short of a full eligible window",
           dut->dbg_phc_dirtcyc_o != 0 ? 1 : 0, 1);
    tick();
    expect("phc: and clear only after the full window",
           dut->dbg_phc_dirtcyc_o, 0);
    dut->phc_adj_ovr_en_i = 0;
    idle(4000);
  }

  //! A SETTIME inside the window re-bases the counter, so nothing before
  //! it can be reconstructed from anything after it.
  void check_settime_reloads_the_guard() {
    expect("phc: the guard is clear before the settime",
           dut->dbg_phc_dirtcyc_o, 0);
    // load the counter with the value it already holds: the smallest
    // disturbance that is still a real settime
    dut->phc_tod_wr_i = dut->phc_ns_o;
    dut->phc_load_i = 1;
    tick();
    dut->phc_load_i = 0;
    expect("phc: a settime reloads the guard",
           dut->dbg_phc_dirtcyc_o, kReconGuardCyc);
    idle(4000);
    expect("phc: and it clears again afterwards", dut->dbg_phc_dirtcyc_o, 0);
  }

  //! Measurements delivered since the PHC-loss count was `pl0`. Every
  //! result the window produced must be a loss, so this has to be zero.
  int measurements_since(uint16_t pl0) {
    (void)pl0;
    int n = 0;
    for (const Stamp &s : stamps) if (s.ok) n++;
    return n;
  }

  //! The full-run laws: one result per transmitted frame within each
  //! transaction epoch, every result naming its own frame, every
  //! reconstruction inside its bound against an independent reference, and
  //! a publication bank that moved only on its commit pulse.
  void check_every_stamp_names_its_own_frame() {
    close_epoch();
    expect("the run transmitted frames", law_frames > 0, 1);
    expect("the run delivered results", law_results > 0, 1);
    // One result per admitted frame, except the entries a ROOT RESET erased:
    // those are the documented epoch discard and are counted rather than
    // claimed as delivered.
    expect("one result per transmitted frame, less the erased epochs",
           law_results + law_erased, law_frames);
    expect("the erased entries are only the reset epochs' own",
           law_erased <= 16 ? 1 : 0, 1);
    // ...and every result must name ITS OWN frame. The pairing is
    // positional, and the tags are checked against the frame's own header
    // bytes for EVERY type the run emits rather than a hard-coded few. Six
    // is what this plane transmits: Sync 0x0, Pdelay_Req 0x2, Pdelay_Resp
    // 0x3, Follow_Up 0x8, Pdelay_Resp_Follow_Up 0xA and Announce 0xB
    // (802.1AS-2011 Table 11-3 and Table 10-5).
    expect("every result carries its own frame's messageType",
           law_tag_wrong, 0);
    expect("every result carries its own frame's sequenceId",
           law_seq_wrong, 0);
    int types_seen = 0;
    for (int b = 0; b < 16; b++) if (law_type_mask & (1 << b)) types_seen++;
    expect("the tag is proved for all six transmitted types", types_seen, 6);
    // THE RECONSTRUCTION LAW: graded against the framer's own launch PHC,
    // which the design never reads, and graded EXACTLY. This bench is
    // single-clock, so every term of the correction is deterministic and a
    // dropped stage moves the answer by a whole tick.
    expect("every measured result reconstructs its own launch",
           law_recon_wrong, 0);
    expect("the reconstruction law covered the run",
           law_results - law_recon_exempt > 0, 1);
    // exactly the frames whose record this fixture delayed, and no more
    expect("only the deliberately delayed records are exempt",
           law_recon_exempt <= 16 ? 1 : 0, 1);

    expect("publication bank changed under stimulus", pub_changes > 0, 1);
    expect("publication commit pulse observed", pub_commits > 0, 1);
    expect("every publication change was commit-qualified",
           pub_unguarded_changes, 0);
  }
};

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  GptpShadowHarness harness;
  return harness.run();
}

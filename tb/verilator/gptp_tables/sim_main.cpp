// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp_tables -- per-table lockstep of the fabric gPTP plane (issue #640,
// lane M7).
//
// The wrapper runs the real plane and, beside it, each table it moved in the
// storage form it had before; it counts every cycle in which a table's
// consumer would have seen something else. This harness only has to make
// those comparisons mean something: drive enough of every kind of traffic
// that each table is written, read, filled, wrapped and reset, then require
// zero mismatches AND the coverage that makes zero informative.
//
// Two sources share the tap. A PEER answers each of the engine's Pdelay_Req
// frames, timed from the engine's own accepted egress result so the measured
// link delay is 600 ns, and in most phases is a better master (Announce,
// Sync and Follow_Up) that the engine follows as a synchronised slave; in
// the stall phase it stops announcing, so the engine becomes grandmaster and
// its own Sync, Follow_Up and Announce queue behind the stalled lane. Around
// the peer, a pseudo-random MIX from a fixed seed: every message type,
// malformed, foreign-EtherType, runt and oversize frames, corrupted byte
// enables, back-to-back bursts that overflow the tap FIFO, held launch
// records, and warm resets in the middle of traffic.

#include <cstdint>
#include <cstdio>
#include <deque>
#include <random>
#include <vector>
#include <verilated.h>
#include "Vgptp_tables_wrap.h"
#include "../../common/verilator_harness.hpp"

namespace {

constexpr uint64_t kPeerCid = 0x0080E1FFFE112233ull;
//! The engine's own clockIdentity, from the image's default MAC: the peer
//! names it as the requester, and a PathTrace that names it is a loop.
constexpr uint64_t kOurCid = 0x02A1B2FFFEC3D4E5ull;
constexpr uint64_t kGmA = 0x00AACCFFFE010203ull;
constexpr uint64_t kGmB = 0x00AACCFFFE010204ull;
//! One 64-bit lane: eight bytes per beat, one tkeep bit each.
constexpr size_t kLaneBytes = 8;
constexpr int kResetTicks = 8;
//! Bench clocks to the engine's cold initialisation and beyond: its first
//! timer handler runs 1200 ms after reset, at the 2 MHz bench clock.
constexpr uint64_t kColdBootTicks = 2600000;
//! The peer's cadences in bench clocks: Announce 1 s, Sync 125 ms.
constexpr uint64_t kAnnounceTicks = 2000000;
constexpr uint64_t kSyncTicks = 250000;
//! The link delay the peer's answers describe, in nanoseconds.
constexpr uint64_t kLinkNs = 600;
//! Ethernet's minimum frame without its FCS.
constexpr size_t kMinFrame = 60;
//! Bytes the tap FIFO holds; a longer gPTP frame is dropped inside it.
constexpr size_t kTapFifoBytes = 2048;
//! The PTP messageType codes the stimulus builds.
constexpr uint8_t kSync = 0x0, kPdReq = 0x2, kPdResp = 0x3, kFollowUp = 0x8,
                  kPdRespFu = 0xA, kAnnounce = 0xB, kSignaling = 0xC;

struct Frame {
  std::vector<uint8_t> b;
  void u8(uint8_t v) { b.push_back(v); }
  void u16(uint16_t v) { u8(static_cast<uint8_t>(v >> 8)); u8(v & 0xFF); }
  void u32(uint32_t v) { u16(static_cast<uint16_t>(v >> 16)); u16(v & 0xFFFF); }
  void u48(uint64_t v) { u16((v >> 32) & 0xFFFF); u32(v & 0xFFFFFFFF); }
  void u64(uint64_t v) { u32(static_cast<uint32_t>(v >> 32)); u32(v & 0xFFFFFFFF); }
  void ts(uint64_t ns) { u48(ns / 1000000000ull); u32(ns % 1000000000ull); }
  void zeros(size_t n) { b.insert(b.end(), n, 0); }
};

//! What the peer still owes for a frame once its first beat has entered
//! the tap: nothing, a Pdelay_Resp_Follow_Up, or a Sync's Follow_Up.
enum class Owed { nothing, resp_follow_up, sync_follow_up };

struct Beat {
  uint64_t data;
  uint8_t keep;
  bool last;
  bool first;       //! the beat the plane timestamps
  Owed owed;        //! what its arrival time completes
  uint16_t seq;     //! the sequence the completion carries
};

//! A peer frame due at a bench clock.
struct Due {
  uint64_t at;
  Frame frame;
  Owed owed;
  uint16_t seq;
};

class TablesHarness {
 public:
  int run() {
    dut->cnt_clr_i = 1;
    reset(kResetTicks);
    //! A cold engine initialises in its first timer handler, 1200 ms after
    //! reset; until then every receive handler drops its frame unread. Run
    //! traffic through the tap and the FIFOs meanwhile, then past it.
    traffic(kColdBootTicks, Mode::mixed);
    traffic(6000000, Mode::mixed);
    traffic(500000, Mode::burst);
    //! No better master for longer than the announce receipt timeout: the
    //! engine becomes grandmaster with its lane stalled for long stretches.
    traffic(9000000, Mode::stall);
    //! A warm reset keeps the engine's initialised scratch: handlers run at
    //! once, so the reset lands in the middle of live table traffic.
    warm_reset_in_traffic();
    traffic(4000000, Mode::mixed);
    traffic(3000000, Mode::held);
    traffic(500000, Mode::burst);
    warm_reset_in_traffic();
    traffic(3000000, Mode::mixed);
    drain(500000);
    grade();
    return check.report();
  }

 private:
  enum class Mode { mixed, burst, stall, held };

  const milan::tb::Model<Vgptp_tables_wrap> model_;
  Vgptp_tables_wrap* dut = model_.get();
  milan::tb::Checker check{"gptp_tables"};
  std::mt19937_64 rng{0x0640'0007ull};
  std::deque<Beat> rxq;
  std::deque<Due> peerq;
  bool presenting = false;
  uint64_t cyc = 0;
  uint16_t mix_seq = 0;
  uint16_t sync_seq = 0;
  uint16_t ann_seq = 0;
  uint64_t next_announce = 0;
  uint64_t next_sync = 0;
  uint32_t idle_gap = 0;
  //! the transmit lane's ready schedule: a level held for a drawn duration
  bool tx_level = true;
  uint32_t tx_left = 0;
  uint32_t held_left = 0;
  uint64_t frames_mixed = 0;
  uint64_t frames_peer = 0;
  uint64_t pdelay_answered = 0;

  uint32_t draw(uint32_t lo, uint32_t hi) {
    return std::uniform_int_distribution<uint32_t>(lo, hi)(rng);
  }
  bool chance(uint32_t pct) { return draw(0, 99) < pct; }

  // ---- clocking --------------------------------------------------------
  void tick(bool rx_ready, bool tx_ready) {
    if (!presenting && !rxq.empty()) presenting = true;
    if (presenting) {
      const Beat& h = rxq.front();
      dut->rx_tvalid_i = 1;
      dut->rx_tdata_i = h.data;
      dut->rx_tkeep_i = h.keep;
      dut->rx_tlast_i = h.last;
    } else {
      dut->rx_tvalid_i = 0;
    }
    dut->rx_tready_i = rx_ready;
    dut->tx_tready_i = tx_ready;
    dut->clk_i = 0;
    dut->eval();
    //! Both observations are the values present immediately before the
    //! active edge: that is the edge the plane latches them on.
    const bool took = dut->rx_tvalid_i && dut->rx_tready_i;
    const uint64_t phc_now = dut->phc_ns_o;
    if (dut->dbg_eng_txts_v_o && dut->dbg_eng_txts_ok_o &&
        dut->dbg_eng_txts_type_o == kPdReq)
      answer_pdelay(static_cast<uint16_t>(dut->dbg_eng_txts_seq_o),
                    dut->dbg_eng_txts_ns_o);
    dut->clk_i = 1;
    dut->eval();
    if (took) {
      const Beat beat = rxq.front();
      rxq.pop_front();
      presenting = false;
      if (beat.first) arrived(beat, phc_now);
    }
    cyc++;
  }

  void reset(int ticks) {
    dut->rst_n = 0;
    for (int i = 0; i < ticks; i++) tick(true, true);
    dut->rst_n = 1;
    dut->cnt_clr_i = 0;
  }

  // ---- frames ------------------------------------------------------------
  Frame ptp(uint8_t mtype, uint16_t seq, uint16_t body_len, uint16_t flags,
            uint64_t src) {
    Frame f;
    f.u48(0x0180C200000Eull);
    f.u48(0x0080E1112233ull);
    f.u16(0x88F7);
    f.u8(0x10 | mtype);
    f.u8(0x02);
    f.u16(static_cast<uint16_t>(34 + body_len));
    f.u8(0);
    f.u8(0);
    f.u16(flags);
    f.u64(0);
    f.u32(0);
    f.u64(src);
    f.u16(1);
    f.u16(seq);
    f.u8(0x05);
    f.u8(0x7F);
    return f;
  }

  Frame follow_up(uint16_t seq, uint64_t precise_ns, uint64_t src) {
    Frame f = ptp(kFollowUp, seq, 42, 0x0008, src);
    f.ts(precise_ns);
    f.u16(0x0003); f.u16(28);
    f.u8(0x00); f.u8(0x80); f.u8(0xC2);
    f.u8(0x00); f.u8(0x00); f.u8(0x01);
    f.u32(0); f.u16(0); f.u64(0); f.u32(0); f.u32(0);
    return f;
  }

  Frame announce(uint64_t gm, uint8_t priority1, uint64_t src, uint16_t hops) {
    Frame f = ptp(kAnnounce, ann_seq++, static_cast<uint16_t>(30 + 4 + 8 * hops),
                  0x0008, src);
    f.ts(0);
    f.u16(37);
    f.u8(0);
    f.u8(priority1);
    f.u32(0xF8FE436Au);
    f.u8(248);
    f.u64(gm);
    f.u16(static_cast<uint16_t>(hops > 0 ? hops - 1 : 0));
    f.u8(0xA0);
    f.u16(0x0008);
    f.u16(static_cast<uint16_t>(8 * hops));
    for (uint16_t h = 0; h < hops; h++) {
      if (h == 0) f.u64(gm);
      else if (chance(5)) f.u64(kOurCid);  // a loop: refused
      else f.u64(0x00DDBBFFFE000000ull | h);
    }
    return f;
  }

  // ---- the peer ----------------------------------------------------------
  //! The engine accepted its own Pdelay_Req's egress time t1: answer it.
  //! t2 = t1 + D and, once the response's arrival t4 is known, t3 = t4 - D,
  //! so the engine measures exactly D whatever the queueing in between.
  void answer_pdelay(uint16_t seq, uint64_t t1) {
    Frame f = ptp(kPdResp, seq, 20, 0x0200, kPeerCid);
    f.ts(t1 + kLinkNs);
    f.u64(kOurCid);
    f.u16(1);
    peerq.push_back({cyc + 2000, f, Owed::resp_follow_up, seq});
    pdelay_answered++;
  }

  //! A peer frame's first beat entered the tap at `phc`: complete it.
  void arrived(const Beat& beat, uint64_t phc) {
    if (beat.owed == Owed::resp_follow_up) {
      Frame f = ptp(kPdRespFu, beat.seq, 20, 0x0000, kPeerCid);
      f.ts(phc - kLinkNs);
      f.u64(kOurCid);
      f.u16(1);
      peerq.push_back({cyc + 1000, f, Owed::nothing, 0});
    } else if (beat.owed == Owed::sync_follow_up) {
      peerq.push_back({cyc + 1500, follow_up(beat.seq, phc - kLinkNs, kPeerCid),
                       Owed::nothing, 0});
    }
  }

  //! the peer as a better master: Announce, then a Sync and its Follow_Up
  void schedule_master(bool master) {
    if (!master) {
      next_announce = cyc + kAnnounceTicks;
      next_sync = cyc + kSyncTicks;
      return;
    }
    if (cyc >= next_announce) {
      peerq.push_back({cyc, announce(kGmA, 100, kPeerCid, 1), Owed::nothing, 0});
      next_announce = cyc + kAnnounceTicks;
    }
    if (cyc >= next_sync) {
      const uint16_t s = sync_seq++;
      Frame f = ptp(kSync, s, 10, 0x0200, kPeerCid);
      f.ts(0);
      peerq.push_back({cyc, f, Owed::sync_follow_up, s});
      next_sync = cyc + kSyncTicks;
    }
  }

  // ---- the mix -----------------------------------------------------------
  Frame mixed_frame() {
    const uint32_t pick = draw(0, 99);
    const uint64_t src = chance(50) ? kPeerCid : kGmB;
    Frame f;
    if (pick < 20) {
      f = ptp(kPdReq, mix_seq++, 20, 0x0000, src);
      f.zeros(20);
    } else if (pick < 25) {
      f = ptp(kSync, mix_seq++, 10, 0x0200, src);
      f.ts(draw(0, 1000000000));
    } else if (pick < 30) {
      f = follow_up(mix_seq++, draw(0, 1000000000), src);
    } else if (pick < 42) {
      const uint8_t type = chance(50) ? kPdResp : kPdRespFu;
      f = ptp(type, mix_seq++, 20, type == kPdResp ? 0x0200 : 0x0000, src);
      f.ts(draw(0, 1000000000));
      f.u64(chance(50) ? kOurCid : kPeerCid);
      f.u16(1);
    } else if (pick < 55) {
      //! never better than the peer or this end station: noise for BTCA
      f = announce(kGmB, 255, kGmB, static_cast<uint16_t>(draw(1, 10)));
    } else if (pick < 62) {
      f = ptp(kSignaling, mix_seq++, 10, 0x0000, src);
      f.u64(kOurCid);
      f.u16(1);
    } else if (pick < 72) {
      f.u48(0x0180C200000Eull);
      f.u48(0x0080E1112233ull);
      f.u16(chance(50) ? 0x22F0 : 0x0800);
      f.zeros(draw(46, 300));
    } else if (pick < 75) {
      f = ptp(kSync, mix_seq++, 10, 0x0200, src);
      f.zeros(kTapFifoBytes + draw(8, 400));   // oversize: dropped in the FIFO
    } else if (pick < 80) {
      f.u48(0x0180C200000Eull);                // a runt: one beat
      f.u16(0x88F7);
    } else {
      f = ptp(chance(50) ? kSync : kPdReq, mix_seq++, 20, 0x0200, src);
      f.zeros(20);
      f.b[15] ^= 0x01;                         // a wrong PTP version: refused
    }
    return f;
  }

  //! Split a frame into beats: trailing octets so every last lane occurs,
  //! and, for mixed frames only, an occasional corrupted byte enable.
  void enqueue(Frame f, Owed owed, uint16_t seq, bool corrupt) {
    if (f.b.size() > 8 && f.b.size() < kMinFrame) f.b.resize(kMinFrame, 0);
    f.zeros(draw(0, 7));
    for (size_t at = 0; at < f.b.size(); at += kLaneBytes) {
      Beat beat{0, 0, false, at == 0, owed, seq};
      for (size_t k = 0; k < kLaneBytes && at + k < f.b.size(); k++) {
        beat.data |= static_cast<uint64_t>(f.b[at + k]) << (8 * k);
        beat.keep = static_cast<uint8_t>(beat.keep | (1u << k));
      }
      beat.last = at + kLaneBytes >= f.b.size();
      if (corrupt && chance(3)) beat.keep = static_cast<uint8_t>(draw(0, 255));
      rxq.push_back(beat);
    }
  }

  // ---- phases ----------------------------------------------------------
  //! The transmit lane's ready, held at a level for a drawn duration. A
  //! stall long enough to fill the transmit FIFO and the egress ledger is
  //! part of every mode; `stall` makes it the rule.
  bool tx_ready(Mode mode) {
    if (tx_left == 0) {
      tx_level = !tx_level;
      if (tx_level) tx_left = draw(200, mode == Mode::stall ? 3000 : 20000);
      else tx_left = draw(50, mode == Mode::stall ? 400000 : 8000);
    }
    tx_left--;
    return tx_level && (mode == Mode::burst || !chance(10));
  }

  void traffic(uint64_t n, Mode mode) {
    const bool burst = (mode == Mode::burst);
    for (uint64_t i = 0; i < n; i++) {
      schedule_master(mode != Mode::stall);
      if (rxq.empty()) {
        if (!peerq.empty() && peerq.front().at <= cyc) {
          Due due = peerq.front();
          peerq.pop_front();
          enqueue(due.frame, due.owed, due.seq, false);
          frames_peer++;
        } else if (idle_gap > 0) {
          idle_gap--;
        } else {
          enqueue(mixed_frame(), Owed::nothing, 0, true);
          frames_mixed++;
          idle_gap = burst ? 0 : draw(20, 1500);
        }
      }
      if (mode == Mode::held) {
        //! hold one type's launch record, then release it, repeatedly
        if (held_left == 0) {
          dut->rechold_en_i = !dut->rechold_en_i;
          dut->rechold_release_i = !dut->rechold_en_i;
          static const uint8_t kTypes[] = {kSync, kPdReq, kPdResp, kFollowUp,
                                           kPdRespFu, kAnnounce};
          dut->rechold_type_i = kTypes[draw(0, 5)];
          held_left = draw(2000, 40000);
        }
        held_left--;
      } else {
        dut->rechold_en_i = 0;
        dut->rechold_release_i = 1;
      }
      tick(burst || !chance(15), tx_ready(mode));
    }
    dut->rechold_en_i = 0;
    dut->rechold_release_i = 1;
  }

  //! A reset in the middle of a frame, with frames queued on both sides.
  //! The reset clears the bench's PHC too, so the peer starts over.
  void warm_reset_in_traffic() {
    while (rxq.size() < 4) enqueue(mixed_frame(), Owed::nothing, 0, true);
    for (int i = 0; i < 3; i++) tick(true, true);
    reset(kResetTicks);
    rxq.clear();
    peerq.clear();
    presenting = false;
  }

  void drain(uint64_t n) {
    rxq.clear();
    peerq.clear();
    presenting = false;
    for (uint64_t i = 0; i < n; i++) tick(true, true);
  }

  // ---- grading ---------------------------------------------------------
  void grade() {
    std::printf("stimulus: %llu cycles, %llu mixed and %llu peer frames, %llu pdelay answers\n",
                static_cast<unsigned long long>(cyc),
                static_cast<unsigned long long>(frames_mixed),
                static_cast<unsigned long long>(frames_peer),
                static_cast<unsigned long long>(pdelay_answered));
    std::printf("rx_fifo: %u good, %u overflow, %u bad, lanes 0x%02x, %u beats deep\n",
                dut->rx_good_o, dut->rx_ovf_o, dut->rx_bad_o, dut->rx_tops_o,
                dut->rx_hiwater_o);
    std::printf("tx_fifo: %u frames, counts 0x%03x, %u stalled cycles, %u beats deep\n",
                dut->tx_frames_o, dut->tx_counts_o, dut->tx_stall_o, dut->tx_hiwater_o);
    std::printf("ledger: %u compared, heads 0x%02x, %u deep\n",
                dut->led_cmp_o, dut->led_heads_o, dut->led_maxn_o);
    std::printf("results: %u compared, heads 0x%02x, %u deep\n",
                dut->res_cmp_o, dut->res_heads_o, dut->res_maxn_o);
    std::printf("timer: %u compared, slots 0x%02x\n", dut->tmr_cmp_o, dut->tmr_slots_o);
    std::printf("plane: flags 0x%x, %u programs run, %u tap drops, %u parser drops, "
                "%u event drops, %u lost results, %u barriers\n",
                dut->pub_flags_o, dut->dbg_prog_run_o, dut->dbg_tap_drop_o,
                dut->dbg_rx_drop_o, dut->dbg_ev_drop_o, dut->dbg_txts_lost_o,
                dut->dbg_txts_barr_o);

    // the five lockstep verdicts: the names the mutation driver requires
    check.dec("rx_fifo lockstep: mismatching cycles", dut->rx_mm_o, 0);
    check.dec("tx_fifo lockstep: mismatching cycles", dut->tx_mm_o, 0);
    check.dec("ledger lockstep: mismatching cycles", dut->led_mm_o, 0);
    check.dec("results lockstep: mismatching cycles", dut->res_mm_o, 0);
    check.dec("timer lockstep: mismatching cycles", dut->tmr_mm_o, 0);

    // ...and what makes each zero mean something
    check.that("rx_fifo coverage: frames committed", dut->rx_good_o >= 1000);
    check.that("rx_fifo coverage: overflow drops", dut->rx_ovf_o >= 20);
    check.that("rx_fifo coverage: bad-frame drops", dut->rx_bad_o >= 100);
    check.dec("rx_fifo coverage: every highest lane delivered", dut->rx_tops_o, 0xFF);
    check.that("rx_fifo coverage: filled past half its depth", dut->rx_hiwater_o >= 128);
    check.that("tx_fifo coverage: frames transmitted", dut->tx_frames_o >= 200);
    //! the engine's frames end in two, four or eight lanes
    check.dec("tx_fifo coverage: lane counts 2, 4 and 8", dut->tx_counts_o, 0x114);
    check.that("tx_fifo coverage: stalled with a beat waiting", dut->tx_stall_o >= 10000);
    //! more than the 16 beats the wrong-depth control leaves the FIFO
    check.that("tx_fifo coverage: over 16 beats queued behind a stall",
               dut->tx_hiwater_o > 16);
    check.that("ledger coverage: head compared", dut->led_cmp_o >= 1000);
    check.dec("ledger coverage: every entry was the head", dut->led_heads_o, 0xFF);
    check.that("ledger coverage: three or more entries outstanding", dut->led_maxn_o >= 3);
    check.that("results coverage: head compared", dut->res_cmp_o >= 100);
    check.dec("results coverage: every entry was the head", dut->res_heads_o, 0xFF);
    check.that("timer coverage: armed sweeps compared", dut->tmr_cmp_o >= 1000);
    //! slots 0-3 as a master, 4 and 5 as a synchronised slave
    check.dec("timer coverage: slots 0 to 5", dut->tmr_slots_o, 0x3F);
  }
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  TablesHarness harness;
  return harness.run();
}

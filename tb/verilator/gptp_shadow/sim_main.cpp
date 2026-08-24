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

#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "Vgptp_shadow_wrap.h"

static const uint64_t OUR_CID = 0x02A1B2FFFEC3D4E5ull;
static const uint64_t PEER_CID = 0x0080E1FFFE112233ull;
static const uint32_t OUR_CQ = 0xF8FE436A;
static const uint64_t GMID = 0x00AACCFFFE010203ull;
static const uint64_t GMID2 = 0x00AACCFFFE010204ull;
static const uint64_t PEER2_CID = 0x0080E1FFFE112244ull;

static const uint32_t FL_PRESENT = 1, FL_AMGM = 2, FL_ASCAP = 4,
                      FL_SYNCOK = 8;

static int checks = 0, fails = 0;
static void expect(const char *what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("FAIL %-32s got %016llx exp %016llx\n", what,
           (unsigned long long)got, (unsigned long long)exp);
  }
}

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

static Vgptp_shadow_wrap *dut;
static uint64_t cyc = 0;
static uint16_t last_txts_seq = 0xFFFF;
//! #214: every returning stamp, in arrival order, with both of its tags.
//! A stamp names the frame it belongs to by {sequenceId, messageType}; the
//! sequence alone cannot, because a Pdelay_Req carries our own counter
//! while a Pdelay_Resp echoes the peer's and the two can coincide.
struct Stamp { uint16_t seq; uint8_t type; uint64_t ns; };
static std::vector<Stamp> stamps;
//! The exact tuples after the test-only return-order gate. Unlike `stamps`,
//! this stream records delivery to the engine, so the collision phases can
//! prove response-first order rather than inferring it from emitted frames.
static std::vector<Stamp> engine_stamps;
//! #214: the slice port must carry the tag AT the cycle the face is valid,
//! not one stamp later. The engine samples txts_* combinationally on the
//! valid pulse (KL_gptp_engine's `if (txts_valid_i) ... txts_pend_seq_r <=
//! txts_seq_i`, cited by the assignment because the pin under it moves),
//! so a registered mirror would
//! read the PREVIOUS stamp's type there and credit one leg's egress time
//! to another leg's claim. Every valid cycle is compared, and the count is
//! asserted non-zero so the check cannot pass by never running.
static int slice_skews = 0, slice_valids = 0;
static std::vector<std::vector<uint8_t>> txf;   // unpacked lane frames
static std::vector<uint64_t> tx_sof_phc;        // phc at each frame's beat0
static std::vector<uint8_t> cur;
static bool in_tx = false;
static bool tx_first = true;

//! The complete outward bank may change only with its commit pulse.
static bool pub_watch = false;
static uint64_t last_pub_gm, last_pub_parent, last_pub_annq;
static uint32_t last_pub_flags, last_pub_pdelay, last_pub_offset;
static unsigned pub_commits, pub_changes, pub_unguarded_changes;

//! issue #122: capture the ingress-ts ring push/pop stamps during a burst
static std::vector<uint64_t> g_pushed, g_popped;
static bool g_ts_capture = false;

static uint64_t phc() { return dut->phc_ns_o; }

static void tick() {
  dut->clk_i = 0; dut->eval();
  //! Sample the engine face immediately before the active edge: a replay
  //! valid is combinational from the held slot and is consumed at this edge,
  //! then disappears when the slot clears. Post-edge sampling would miss the
  //! very delivery whose order this trace exists to prove.
  if (dut->dbg_eng_txts_v_o)
    engine_stamps.push_back({(uint16_t)dut->dbg_eng_txts_seq_o,
                             (uint8_t)dut->dbg_eng_txts_type_o,
                             dut->dbg_eng_txts_ns_o});
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
    for (int i = 0; i < 8; i++)
      if ((dut->tx_tkeep_o >> i) & 1)
        cur.push_back((dut->tx_tdata_o >> (8 * i)) & 0xFF);
    if (dut->tx_tlast_o) {
      txf.push_back(cur);
      in_tx = false;
      tx_first = true;
    } else {
      tx_first = false;
    }
  }
  dut->clk_i = 1; dut->eval();
  if (dut->rst_n) {
    if (!pub_watch) {
      pub_watch = true;
    } else {
      const bool changed = dut->pub_gm_id_o != last_pub_gm
                        || dut->pub_parent_id_o != last_pub_parent
                        || dut->pub_flags_o != last_pub_flags
                        || dut->pub_pdelay_ns_o != last_pub_pdelay
                        || dut->pub_offset_o != last_pub_offset
                        || dut->pub_annq_o != last_pub_annq;
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
  }
  if (g_ts_capture) {
    if (dut->dbg_tspush_v_o) g_pushed.push_back(dut->dbg_tspush_o);
    if (dut->dbg_tspop_v_o)  g_popped.push_back(dut->dbg_rx_ts_o);
  }
  if (dut->dbg_txts_v_o) {
    slice_valids++;
    if (dut->dbg_slice_type_o != dut->dbg_txts_type_o) slice_skews++;
    last_txts_seq = dut->dbg_txts_seq_o;
    stamps.push_back({(uint16_t)dut->dbg_txts_seq_o,
                      (uint8_t)dut->dbg_txts_type_o, dut->dbg_txts_o});
  }
  cyc++;
}

static void run(uint64_t n) { while (n--) tick(); }

//! pack bytes into 64-bit beats and drive the tap (harness is the DMA
//! consumer too: tready held high)
static void send_wide(const std::vector<uint8_t> &bytes) {
  size_t n = bytes.size();
  for (size_t off = 0; off < n; off += 8) {
    uint64_t d = 0;
    uint8_t k = 0;
    for (size_t i = 0; i < 8 && off + i < n; i++) {
      d |= (uint64_t)bytes[off + i] << (8 * i);
      k |= (uint8_t)(1u << i);
    }
    dut->rx_tdata_i = d;
    dut->rx_tkeep_i = k;
    dut->rx_tvalid_i = 1;
    dut->rx_tready_i = 1;
    dut->rx_tlast_i = (off + 8 >= n);
    tick();
  }
  dut->rx_tvalid_i = 0;
  dut->rx_tlast_i = 0;
}

// ---- the peer: answers pdelay with residence computed from observed
// fabric time, so the measured delay lands near D_NOM. The harness's
// own records give the EXPECTED delay exactly, up to the few-tick skew
// between its observation points and the fabric latches ---------------
static const int64_t D_NOM = 600;
static size_t pd_seen = 0;
static bool pd_on = false;
static int64_t pd_expect = 0;                // the last exchange's D

static void service_pdelay() {
  while (pd_seen < txf.size()) {
    size_t i = pd_seen;
    if (txf[i].size() <= 14 || (txf[i][14] & 0xF) != 0x2) {
      pd_seen++;
      continue;
    }
    pd_seen++;
    if (!pd_on) continue;
    uint16_t seq = (uint16_t)((txf[i][44] << 8) | txf[i][45]);
    uint64_t t1 = tx_sof_phc[i];             // = the boundary stamp
    run(300);                                // a real turnaround, > 2*D_NOM
    uint64_t t2 = 5000000ull + phc();
    Frame f = ptp(0x3, seq, 0, 0x0200, 20);
    f.ts(t2); f.u64(OUR_CID); f.u16(1);
    // residence = (fabric turnaround) - 2*D_NOM, computed at send time;
    // the tap stamps t4 within a beat of the first wide beat below
    uint64_t resid = (phc() - t1) - 2 * (uint64_t)D_NOM;
    uint64_t t3 = t2 + resid;
    uint64_t t4_est = phc() + 8;             // the next tick's beat 0
    pd_expect = (int64_t)((t4_est - t1) - resid) / 2;
    send_wide(f.b);
    run(50);
    Frame g = ptp(0xA, seq, 0, 0x0000, 20);
    g.ts(t3); g.u64(OUR_CID); g.u16(1);
    send_wide(g.b);
    run(50);
  }
}

static void run_svc(uint64_t n) {
  while (n--) { tick(); if ((n & 255) == 0) service_pdelay(); }
}

static bool wait_flags(uint32_t mask, uint32_t want, uint64_t max_ticks) {
  for (uint64_t n = 0; n < max_ticks; n++) {
    if ((dut->pub_flags_o & mask) == want) return true;
    tick();
    if ((n & 255) == 0) service_pdelay();
  }
  return false;
}

static size_t tx_seen = 0;
static std::vector<uint8_t> wait_tx(int mtype, uint64_t max_cycles,
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

static uint64_t fld48(const std::vector<uint8_t> &f, size_t o) {
  uint64_t v = 0; for (int i = 0; i < 6; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint16_t fld16(const std::vector<uint8_t> &f, size_t o) {
  return (uint16_t)(((uint16_t)f[o] << 8) | f[o + 1]);
}
static uint32_t fld32(const std::vector<uint8_t> &f, size_t o) {
  uint32_t v = 0; for (int i = 0; i < 4; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint64_t fld64(const std::vector<uint8_t> &f, size_t o) {
  uint64_t v = 0; for (int i = 0; i < 8; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint64_t timestamp_field_ns(const std::vector<uint8_t> &f, size_t o) {
  return fld48(f, o) * 1000000000ull + fld32(f, o + 6);
}
static void announce(uint16_t seq, uint8_t p1, uint64_t gmid,
                     uint64_t src = PEER_CID) {
  Frame a = ptp(0xB, seq, 0, 0x0008, 30, src);
  for (int i = 0; i < 10; i++) a.u8(0);
  a.u16(0xFFC4); a.u8(0);
  a.u8(p1); a.u32(OUR_CQ); a.u8(248);
  a.u64(gmid);
  a.u16(0); a.u8(0xA0);
  send_wide(a.b);
  run_svc(4000);
}
static void sync_pair(uint16_t seq, uint64_t origin_delta,
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

static bool near(int64_t v, int64_t c, int64_t tol) {
  return v >= c - tol && v <= c + tol;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vgptp_shadow_wrap;

  dut->rst_n = 0;
  dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tdata_i = 0;
  dut->rx_tkeep_i = 0; dut->rx_tready_i = 1;
  dut->tx_tready_i = 1;
  dut->txts_hold_en_i = 0; dut->txts_hold_type_i = 0;
  dut->txts_release_i = 0;
  for (int i = 0; i < 8; i++) tick();
  dut->rst_n = 1;

  // ---- 1: boot -> Pdelay_Req byte-exact through the gearbox -------------
  // Hold its REAL boundary-stamper tuple so a same-sequence response can
  // return first. Nothing is fabricated: only the delivery order changes.
  dut->txts_hold_type_i = 0x2;
  dut->txts_hold_en_i = 1;
  size_t req_idx = 0;
  std::vector<uint8_t> req = wait_tx(0x2, 3200000, &req_idx);
  if (!req.empty()) {
    expect("pdreq length", req.size(), 68);
    expect("pdreq DA", fld48(req, 0), 0x0180C200000Eull);
    expect("pdreq etype+type",
           ((uint64_t)req[12] << 16) | ((uint64_t)req[13] << 8) | req[14],
           0x88F712ull);
    expect("pdreq srcCID", fld48(req, 34), OUR_CID >> 16);
  }
  expect("asCapable low at boot", dut->pub_flags_o & FL_ASCAP, 0);
  if (!req.empty()) {
    uint16_t req_seq = (uint16_t)((req[44] << 8) | req[45]);
    expect("stamper extracted the req's seq", last_txts_seq, req_seq);
    expect("held request tuple keeps sequenceId",
           dut->dbg_txts_held_seq_o, req_seq);
    expect("held request tuple keeps messageType",
           dut->dbg_txts_held_type_o, (uint8_t)(req[14] & 0xF));
    if (req_idx < stamps.size()) {
      expect("held request tuple keeps the real stamper time",
             dut->dbg_txts_held_ns_o, stamps[req_idx].ns);
      if (req_idx < tx_sof_phc.size())
        expect("held request time is the frame's SOF PHC",
               dut->dbg_txts_held_ns_o, tx_sof_phc[req_idx]);
    }
  }
  // #214: the stamp names the frame by BOTH tags. A Pdelay_Req is
  // messageType 0x2 (802.1AS-2011 Table 11-3), the low nibble of wire
  // byte 14, and the tag must be that frame's, not the previous one's.
  if (!req.empty() && !stamps.empty()) {
    expect("the req's stamp carries messageType 0x2",
           stamps.back().type, (uint8_t)(req[14] & 0xF));
    expect("the slice holds the same type at the engine boundary",
           dut->dbg_slice_type_o, (uint8_t)(req[14] & 0xF));
  }

  // ---- 1c: equal-sequence Req/Resp claims, response stamp first ---------
  // Both endpoints' request counters start at zero. While our type-2 claim
  // still waits on the held real stamp, a peer request with the same sequence
  // draws a type-3 response. Its stamp must build that response's type-A
  // Follow_Up, and the unclaimed type-A stamp must leave our type-2 claim for
  // the original tuple. Sequence-only credit fails all three observations.
  expect("boot request stamp is held for collision", dut->dbg_txts_held_o, 1);
  dut->txts_hold_en_i = 0;
  uint16_t boot_clash = req.empty() ? 0 :
      (uint16_t)((req[44] << 8) | req[45]);
  size_t boot_eng_mark = engine_stamps.size();
  uint16_t boot_ev_drop = dut->dbg_ev_drop_o;
  {
    size_t mark = txf.size();
    tx_seen = mark;
    Frame rq = ptp(0x2, boot_clash, 0, 0x0000, 20, PEER_CID);
    rq.u64(0); rq.u64(0); rq.u32(0);
    send_wide(rq.b);
    size_t ri = 0;
    std::vector<uint8_t> rsp = wait_tx(0x3, 200000, &ri);
    std::vector<uint8_t> rfu = wait_tx(0xA, 200000);
    expect("equal request sequences: the peer request is answered",
           rsp.empty() ? 0 : 1, 1);
    expect("response-first stamp builds its Resp_Follow_Up",
           rfu.empty() ? 0 : 1, 1);
    if (!rsp.empty())
      expect("equal request sequences: Resp echoes the common sequence",
             (uint16_t)((rsp[44] << 8) | rsp[45]), boot_clash);
    if (!rfu.empty()) {
      expect("equal request sequences: Resp_FU echoes the common sequence",
             (uint16_t)((rfu[44] << 8) | rfu[45]), boot_clash);
      if (ri < stamps.size())
        expect("Resp_FU carries the response's own boundary stamp",
               timestamp_field_ns(rfu, 48), stamps[ri].ns);
    }
    run(2000);  // let the unclaimed type-A stamp dispatch; donor #31 is open
    expect("unclaimed Resp_FU stamp leaves the request tuple held",
           dut->dbg_txts_held_o, 1);
  }
  dut->txts_release_i = 1;
  tick();
  dut->txts_release_i = 0;
  tick();
  expect("the original request tuple is released exactly once",
         dut->dbg_txts_held_o, 0);
  expect("request collision delivers exactly response, FU, request",
         engine_stamps.size(), boot_eng_mark + 3);
  if (engine_stamps.size() >= boot_eng_mark + 3) {
    expect("request collision delivery 1 is Pdelay_Resp",
           engine_stamps[boot_eng_mark].type, 0x3);
    expect("request collision delivery 2 is unclaimed Resp_FU",
           engine_stamps[boot_eng_mark + 1].type, 0xA);
    expect("request collision delivery 3 is held Pdelay_Req",
           engine_stamps[boot_eng_mark + 2].type, 0x2);
    for (size_t k = boot_eng_mark; k < boot_eng_mark + 3; k++)
      expect("all request-collision deliveries share sequenceId",
             engine_stamps[k].seq, boot_clash);
  }
  expect("request collision gate had no overlap/overflow",
         dut->dbg_txts_gate_conflict_o, 0);
  expect("request collision changed no engine-event drop count",
         dut->dbg_ev_drop_o, boot_ev_drop);

  // ---- 2: one fabric-timed exchange; not capable at one ------------------
  pd_seen = 0;                      // answer the boot request too
  pd_on = true;
  service_pdelay();
  run_svc(8000);
  expect("pdelay matches the records",
         near((int32_t)dut->pub_pdelay_ns_o, pd_expect, 32), 1);
  expect("one exchange not capable", dut->pub_flags_o & FL_ASCAP, 0);

  // ---- 3: the second exchange raises asCapable ---------------------------
  expect("capable at the second exchange",
         wait_flags(FL_ASCAP, FL_ASCAP, 6000000ull), 1);

  // ---- 4: adopt; offsets in range; the counter locks ---------------------
  announce(10, 100, GMID);
  expect("adopted", dut->pub_flags_o & 3, FL_PRESENT);
  expect("pub gm id", dut->pub_gm_id_o, GMID);
  expect("pub parent id", dut->pub_parent_id_o, PEER_CID);
  {
    // offset = tap_stamp - (origin + pd): origin is written so the true
    // offset is ~+1000 ns; the tap stamps within a couple of beats
    sync_pair(0x100, 1000 + (uint64_t)D_NOM, nullptr);
    expect("offset near +1000",
           near((int32_t)dut->pub_offset_o, 1000, 200), 1);
    expect("sync-ok rose", dut->pub_flags_o & FL_SYNCOK, FL_SYNCOK);
  }
  {
    // short closed loop: a master 1 ms ahead at +100 ppm in counter
    // time; one re-base then the addend carries the rate
    uint64_t mst_base = phc() + 1000000ull - cyc * 8ull - cyc / 1250ull;
    uint16_t sq = 0x200;
    for (int k = 0; k < 12; k++) {
      if ((k % 6) == 0) announce((uint16_t)(20 + k), 100, GMID);
      run_svc(250000);
      uint64_t origin = mst_base + cyc * 8ull + cyc / 1250ull;
      Frame f = ptp(0x0, sq, 0, 0x0208, 10);
      f.ts(0);
      send_wide(f.b);
      run(30);
      // cancel pd so offset -> 0
      Frame g = follow_up(sq, origin + (uint64_t)D_NOM);
      send_wide(g.b);
      run(4000);
      sq++;
    }
    expect("closed loop locked",
           near((int32_t)dut->pub_offset_o, 0, 300), 1);
  }

  // A better Announce moves the registered bank on the same edge on which
  // talkers may launch. The pre-commit discontinuity must make tu visible
  // to both consumer-equivalent launch registers on that edge.
  run_svc(512);
  expect("healthy bank clears tu before GM switch", dut->ts_uncertain_o, 0);
  const uint16_t disc_before = dut->disc_launch_count_o;
  announce(0x2F0, 90, GMID2, PEER2_CID);
  expect("better Announce selects the new GM", dut->pub_gm_id_o, GMID2);
  expect("registered bank emitted a pre-commit discontinuity",
         dut->disc_launch_count_o > disc_before, 1);
  expect("AAF same-edge launch samples tu=1", dut->aaf_launch_tu_o, 1);
  expect("CRF same-edge launch samples tu=1", dut->crf_launch_tu_o, 1);
  // ---- 5: classify negatives ---------------------------------------------
  {
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
  {
    Frame storm = ptp(0x0, 0x7100, 0, 0x0208, 10);
    storm.ts(0);
    while (storm.b.size() < 3000) storm.u8(0xAA);
    send_wide(storm.b);
    run(2000);
    sync_pair(0x300, 2000 + (uint64_t)D_NOM, nullptr);
    expect("oversize cannot skew the stamp",
           near((int32_t)dut->pub_offset_o, 2000, 200), 1);
  }

  // ---- 7: overflow drops are counted; the plane survives ----------------
  {
    uint16_t drop_before = dut->dbg_tap_drop_o;
    for (int k = 0; k < 12; k++) {
      Frame f = ptp(0xC, (uint16_t)(0x7200 + k), 0, 0, 20);
      while (f.b.size() < 512) f.u8(0x55);
      send_wide(f.b);                  // back-to-back, no gap
    }
    run(20000);
    expect("overflow drops counted",
           dut->dbg_tap_drop_o > drop_before, 1);
    sync_pair(0x400, 3000 + (uint64_t)D_NOM, nullptr);
    expect("the plane survives the burst",
           near((int32_t)dut->pub_offset_o, 3000, 200), 1);
  }

  // ---- 8: issue #122 -- a back-to-back 0x88F7 burst must NOT lap the ring.
  // [R0]'s repro: 40 two-beat 0x88F7 frames arrive far faster (2 beats each)
  // than the 1 B/clk serializer drains (16 clk each), so committed-but-
  // unserialized frames exceed the 32-entry ts ring. The shed guard drops
  // whole frames at sof when the ring is full, so no live stamp is ever
  // lapped: the popped stamps are exactly the pushed stamps in FIFO order,
  // and pops + gPTP sheds account for all 40. On the unguarded RTL the ring
  // laps and the popped stamps diverge from the pushed ones (the mutation).
  {
    g_pushed.clear(); g_popped.clear();
    uint16_t drop0 = dut->dbg_tap_drop_o;
    g_ts_capture = true;
    for (int k = 0; k < 40; k++) {
      std::vector<uint8_t> f(16, 0);
      // DA 01:80:C2:00:00:0E, SA 00:80:E1:11:22:33
      const uint8_t da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
      const uint8_t sa[6] = {0x00,0x80,0xE1,0x11,0x22,0x33};
      for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
      f[12] = 0x88; f[13] = 0xF7;             // EtherType (accepted by the tap)
      f[14] = 0x10; f[15] = 0x02;             // sv/version/message_type, ptp ver
      send_wide(f);                            // 2 wide beats, back-to-back
    }
    run(40000);                                // drain the whole burst
    g_ts_capture = false;
    uint16_t sheds = (uint16_t)(dut->dbg_tap_drop_o - drop0);

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
           (int)g_popped.size() + (int)sheds, 40);
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
  {
    for (int k = 0; k < 40; k++) {
      Frame f = ptp(0x0, (uint16_t)(0x7300 + k), 0, 0x0208, 10);
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
  {
    long sheds[4];
    for (int rep = 0; rep < 4; rep++) {
      uint16_t d0 = dut->dbg_tap_drop_o;
      g_pushed.clear(); g_popped.clear();
      g_ts_capture = true;
      for (int k = 0; k < 40; k++) {
        std::vector<uint8_t> f(16, 0);
        const uint8_t da[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        const uint8_t sa[6] = {0x00,0x80,0xE1,0x11,0x22,0x33};
        for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
        f[12] = 0x88; f[13] = 0xF7;
        f[14] = 0x10; f[15] = 0x02;
        send_wide(f);
      }
      run(40000);
      g_ts_capture = false;
      sheds[rep] = (long)(uint16_t)(dut->dbg_tap_drop_o - d0);
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
             (int)g_popped.size() + (int)sheds[rep], 40);
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

  //! build a minimal classifiable 0x88F7 (or foreign-ethertype) frame
  auto tapframe = [](size_t len, bool gptp) {
    std::vector<uint8_t> f(len, 0);
    const uint8_t da[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};
    const uint8_t sa[6] = {0x00, 0x80, 0xE1, 0x11, 0x22, 0x33};
    for (int i = 0; i < 6; i++) { f[i] = da[i]; f[6 + i] = sa[i]; }
    f[12] = gptp ? 0x88 : 0x22;
    f[13] = gptp ? 0xF7 : 0xF0;
    f[14] = 0x10; f[15] = 0x02;
    return f;
  };

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
  for (int fb = 0; fb < 2; fb++) {
    const size_t flen = (fb == 0) ? 24 : 56;
    const int    nfr  = 60;
    uint16_t d0 = dut->dbg_tap_drop_o;
    g_pushed.clear(); g_popped.clear();
    g_ts_capture = true;
    for (int k = 0; k < nfr; k++) send_wide(tapframe(flen, true));
    run(120000);
    g_ts_capture = false;
    long sheds = (long)(uint16_t)(dut->dbg_tap_drop_o - d0);
    bool law = (g_popped.size() == g_pushed.size()) && !g_popped.empty();
    for (size_t i = 0; law && i < g_popped.size(); i++)
      if (g_popped[i] != g_pushed[i]) law = false;
    expect("long-frame shed stays atomic: popped == pushed, in order", law, 1);
    expect("long-frame shed stays atomic: pops + sheds == 60",
           (int)g_popped.size() + (int)sheds, nfr);
  }

  // ---- 12: the shed diagnostic counts gPTP sheds ONLY. The guard sheds at
  // beat 0, BEFORE the EtherType verdict lands at beat 1, so on a busy link
  // most shed frames are not gPTP at all -- counting those would poison
  // dbg_tap_drop_o, which is what a silicon reader uses to size the loss.
  // Saturate the ring with short gPTP frames while interleaving AVTP ones:
  // the accounting law below holds only if the count is EtherType-gated.
  {
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
    long sheds = (long)(uint16_t)(dut->dbg_tap_drop_o - d0);
    expect("mixed traffic: pops + gPTP sheds == the 60 gPTP frames sent",
           (int)g_popped.size() + (int)sheds, npair);
  }

  // ---- 13: #214 -- the master role puts the other three types on the
  // lane. Until here the run emits Pdelay_Req, Pdelay_Resp and its
  // Follow_Up only, so the tag would be proved for three of the
  // six types the plane transmits and a mutation correct for everything
  // but Announce would pass. With no announce refreshed the receipt timeout
  // expires, the plane becomes grandmaster, and Announce, Sync and
  // Follow_Up join the lane. Last, because a plane that is its own
  // grandmaster no longer consumes the peer syncs the earlier phases use.
  {
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

    dut->txts_hold_type_i = 0x0;       // hold the next real Sync tuple
    dut->txts_hold_en_i = 1;
    spent = 0;
    while (!dut->dbg_txts_held_o && spent < 500000ull) {
      // Stop within 1,000 clocks of the held Sync, well inside the 125 ms
      // Sync interval, so a second Sync cannot replace the same claim.
      run_svc(1000);
      spent += 1000;
    }
    expect("the selected master Sync stamp is held for collision",
           dut->dbg_txts_held_o, 1);
    expect("held Sync tuple keeps messageType",
           dut->dbg_txts_held_type_o, 0x0);
    dut->txts_hold_en_i = 0;

    uint16_t clash = dut->dbg_txts_held_seq_o;
    uint64_t sync_stamp_ns = dut->dbg_txts_held_ns_o;
    uint16_t sync_ev_drop = dut->dbg_ev_drop_o;

    // Locate the raw boundary tuple that the wrapper held. The full-run
    // one-stamp-per-frame law below independently proves this positional map.
    size_t sync_idx = 0;
    bool held_sync_seen = false;
    for (size_t k = before; k < txf.size() && k < stamps.size(); k++) {
      if (txf[k].size() > 45 && (txf[k][14] & 0xF) == 0x0 &&
          (uint16_t)((txf[k][44] << 8) | txf[k][45]) == clash &&
          stamps[k].type == 0x0 && stamps[k].seq == clash &&
          stamps[k].ns == sync_stamp_ns) {
        sync_idx = k;
        held_sync_seen = true;
        break;
      }
    }
    expect("held Sync has a real boundary tuple", held_sync_seen ? 1 : 0, 1);
    if (held_sync_seen && sync_idx < tx_sof_phc.size())
      expect("held Sync time is the frame's SOF PHC",
             sync_stamp_ns, tx_sof_phc[sync_idx]);

    if (held_sync_seen) {
      size_t collision_mark = txf.size();
      size_t sync_eng_mark = engine_stamps.size();
      tx_seen = collision_mark;

      // A peer request using the Sync sequence creates a type-3 claim with
      // the same 16-bit sequence. Return its real stamp first. Only the type
      // distinguishes the mandatory Resp_FU from our pending Sync Follow_Up.
      Frame same = ptp(0x2, clash, 0, 0x0000, 20, PEER_CID);
      same.u64(0); same.u64(0); same.u32(0);
      send_wide(same.b);
      size_t ri = 0;
      std::vector<uint8_t> rsp = wait_tx(0x3, 200000, &ri);
      std::vector<uint8_t> rfu = wait_tx(0xA, 200000);
      expect("equal Sync/Resp sequences: the peer request is answered",
             rsp.empty() ? 0 : 1, 1);
      expect("response stamp builds Resp_FU rather than Sync Follow_Up",
             rfu.empty() ? 0 : 1, 1);
      if (!rfu.empty()) {
        expect("equal Sync/Resp sequences: Resp_FU keeps the common sequence",
               (uint16_t)((rfu[44] << 8) | rfu[45]), clash);
        if (ri < stamps.size())
          expect("equal Sync/Resp sequences: Resp_FU carries its own stamp",
                 timestamp_field_ns(rfu, 48), stamps[ri].ns);
      }
      int premature_sync_fu = 0;
      for (size_t k = collision_mark; k < txf.size(); k++)
        if (txf[k].size() > 14 && (txf[k][14] & 0xF) == 0x8)
          premature_sync_fu++;
      expect("response and unclaimed Resp_FU leave Sync pending",
             premature_sync_fu, 0);
      run(2000);  // dispatch the unclaimed type-A stamp; donor #31 is open
      expect("the original Sync tuple remains held after the type-A stamp",
             dut->dbg_txts_held_o, 1);
      expect("Sync collision has delivered response then unclaimed FU",
             engine_stamps.size(), sync_eng_mark + 2);

      dut->txts_release_i = 1;
      tick();
      dut->txts_release_i = 0;
      tick();
      expect("Sync collision delivers exactly response, FU, Sync",
             engine_stamps.size(), sync_eng_mark + 3);
      if (engine_stamps.size() >= sync_eng_mark + 3) {
        expect("Sync collision delivery 1 is Pdelay_Resp",
               engine_stamps[sync_eng_mark].type, 0x3);
        expect("Sync collision delivery 2 is unclaimed Resp_FU",
               engine_stamps[sync_eng_mark + 1].type, 0xA);
        expect("Sync collision delivery 3 is held Sync",
               engine_stamps[sync_eng_mark + 2].type, 0x0);
        for (size_t k = sync_eng_mark; k < sync_eng_mark + 3; k++)
          expect("all Sync-collision deliveries share sequenceId",
                 engine_stamps[k].seq, clash);
        expect("released engine tuple keeps the held Sync time",
               engine_stamps[sync_eng_mark + 2].ns, sync_stamp_ns);
      }
      std::vector<uint8_t> fu = wait_tx(0x8, 200000);
      expect("released Sync stamp builds its own Follow_Up",
             fu.empty() ? 0 : 1, 1);
      if (!fu.empty()) {
        expect("released Sync Follow_Up keeps the common sequence",
               (uint16_t)((fu[44] << 8) | fu[45]), clash);
        expect("released Sync Follow_Up carries the Sync boundary stamp",
               timestamp_field_ns(fu, 48), sync_stamp_ns);
      }
      expect("the held Sync tuple is consumed exactly once",
             dut->dbg_txts_held_o, 0);
      expect("Sync collision gate had no overlap/overflow",
             dut->dbg_txts_gate_conflict_o, 0);
      expect("Sync collision changed no engine-event drop count",
             dut->dbg_ev_drop_o, sync_ev_drop);
    }

    run_svc(1400000);                  // an announce interval and then some
    int saw_ann = 0, saw_sync = 0, saw_fu = 0;
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
  {
    pd_on = false;
    service_pdelay();
    for (int k = 0; k < 2000 && (dut->tx_tvalid_o || in_tx); k++) tick();
    //! Begin from a quiet, reset production lane so the first stalled frame
    //! can only be response 1; post-reset periodic traffic is still more than
    //! two million clocks away.
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    pd_seen = txf.size();
    tx_seen = txf.size();
    run(512);

    const uint16_t Q1 = 0x1111, Q2 = 0x2222;
    const uint64_t C1 = PEER_CID, C2 = 0x001122FFFE334455ull;
    const uint16_t P1 = 1, P2 = 2;
    Frame q1 = ptp(0x2, Q1, 0, 0x0000, 20, C1);
    q1.u64(0); q1.u64(0); q1.u32(0);
    Frame q2 = ptp(0x2, Q2, 0, 0x0000, 20, C2);
    q2.b[42] = (uint8_t)(P2 >> 8);
    q2.b[43] = (uint8_t)P2;
    q2.u64(0); q2.u64(0); q2.u32(0);

    const size_t mark = txf.size();
    const uint16_t evdrop0 = dut->dbg_ev_drop_o;
    const uint16_t conflict0 = dut->dbg_txts_gate_conflict_o;
    auto find_frame = [&](uint8_t mt, uint16_t seq) -> int {
      for (size_t i = mark; i < txf.size(); i++)
        if (txf[i].size() > 45 && (txf[i][14] & 0xF) == mt &&
            fld16(txf[i], 44) == seq)
          return (int)i;
      return -1;
    };

    dut->txts_hold_type_i = 0x3;
    dut->txts_hold_en_i = 1;
    dut->tx_tready_i = 0;
    const uint64_t Q1_RX = phc();
    send_wide(q1.b);
    const uint64_t Q2_RX = phc();
    send_wide(q2.b);
    Frame chase1 = ptp(0xC, 0xD00D, 0, 0x0000, 0);
    Frame chase2 = ptp(0xC, 0xBEEF, 0, 0x0000, 0);
    send_wide(chase1.b);
    send_wide(chase2.b);
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

    int resp1 = -1;
    for (int k = 0; k < 400000 &&
                         (resp1 < 0 || !dut->dbg_txts_held_o); k++) {
      tick();
      resp1 = find_frame(0x3, Q1);
    }
    expect("same-type owner: response 1 sent", resp1 >= 0 ? 1 : 0, 1);
    expect("same-type owner: response 1 stamp is held",
           dut->dbg_txts_held_o, 1);
    if (resp1 >= 0)
      expect("backpressure: the stalled frame is response 1",
             (size_t)resp1, mark);
    dut->txts_hold_en_i = 0;
    if (resp1 >= 0) {
      expect("same-type owner: response 1 requestReceiptTimestamp",
             timestamp_field_ns(txf[resp1], 48), Q1_RX);
      expect("same-type owner: response 1 requester",
             fld64(txf[resp1], 58), C1);
      expect("same-type owner: response 1 port", fld16(txf[resp1], 66), P1);
      expect("same-type owner: held sequence",
             dut->dbg_txts_held_seq_o, Q1);
      expect("same-type owner: held type",
             dut->dbg_txts_held_type_o, 0x3);
      if ((size_t)resp1 < stamps.size())
        expect("same-type owner: held real boundary time",
               dut->dbg_txts_held_ns_o, stamps[resp1].ns);
    }
    run(2000);
    expect("same-type owner: response 2 waits for response 1 stamp",
           find_frame(0x3, Q2) < 0 ? 1 : 0, 1);

    while (dut->dbg_txts_v_o) tick();
    dut->txts_release_i = 1;
    tick();
    dut->txts_release_i = 0;
    tick();
    expect("same-type owner: response 1 tuple releases once",
           dut->dbg_txts_held_o, 0);

    int fu1 = -1, resp2 = -1, fu2 = -1;
    for (int k = 0; k < 600000 && (fu1 < 0 || resp2 < 0 || fu2 < 0); k++) {
      tick();
      fu1 = find_frame(0xA, Q1);
      resp2 = find_frame(0x3, Q2);
      fu2 = find_frame(0xA, Q2);
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
      if ((size_t)resp1 < stamps.size())
        expect("same-type owner: Follow_Up 1 carries stamp 1",
               timestamp_field_ns(txf[fu1], 48), stamps[resp1].ns);
    }
    if (resp2 >= 0) {
      expect("same-type owner: response 2 requestReceiptTimestamp",
             timestamp_field_ns(txf[resp2], 48), Q2_RX);
      expect("same-type owner: response 2 requester",
             fld64(txf[resp2], 58), C2);
      expect("same-type owner: response 2 port", fld16(txf[resp2], 66), P2);
    }
    if (fu2 >= 0 && resp2 >= 0) {
      expect("same-type owner: Follow_Up 2 requester",
             fld64(txf[fu2], 58), C2);
      expect("same-type owner: Follow_Up 2 port", fld16(txf[fu2], 66), P2);
      if ((size_t)resp2 < stamps.size())
        expect("same-type owner: Follow_Up 2 carries stamp 2",
               timestamp_field_ns(txf[fu2], 48), stamps[resp2].ns);
    }
    expect("same-type owner: test gate loses no tuple",
           dut->dbg_txts_gate_conflict_o, conflict0);
    expect("same-type owner: event queue loses no request",
           dut->dbg_ev_drop_o, evdrop0);
    dut->tx_tready_i = 1;
  }

  // ---- 15: #41 -- warm reset cannot preserve a stale timer owner --------
  // Hold a real Pdelay_Req stamp across reset. Scratch state intentionally
  // survives warm reset for Milan cease history, but a pre-reset egress owner
  // must be hidden until a fresh transmitter writes one; otherwise every
  // later timer request remains suppressed forever.
  {
    pd_on = false;
    pd_seen = txf.size();
    dut->txts_hold_type_i = 0x2;
    dut->txts_hold_en_i = 1;
    tx_seen = txf.size();
    size_t lost_req_idx = 0;
    std::vector<uint8_t> lost_req = wait_tx(0x2, 4000000, &lost_req_idx);
    for (int k = 0; k < 2000 && !dut->dbg_txts_held_o; k++) tick();
    expect("warm reset request: request sent", lost_req.empty() ? 0 : 1, 1);
    expect("warm reset request: real stamp held", dut->dbg_txts_held_o, 1);
    if (!lost_req.empty()) {
      expect("warm reset request: held type", dut->dbg_txts_held_type_o, 0x2);
      expect("warm reset request: held sequence",
             dut->dbg_txts_held_seq_o, fld16(lost_req, 44));
      if (lost_req_idx < stamps.size())
        expect("warm reset request: held boundary time",
               dut->dbg_txts_held_ns_o, stamps[lost_req_idx].ns);
    }
    dut->txts_hold_en_i = 0;
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    dut->txts_release_i = 0;
    expect("warm reset request: volatile held tuple clears",
           dut->dbg_txts_held_o, 0);

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
  {
    while (dut->dbg_txts_v_o) tick();
    dut->txts_hold_type_i = 0x0;
    dut->txts_hold_en_i = 1;
    tx_seen = txf.size();
    size_t lost_sync_idx = 0;
    std::vector<uint8_t> lost_sync = wait_tx(0x0, 1000000, &lost_sync_idx);
    for (int k = 0; k < 2000 && !dut->dbg_txts_held_o; k++) tick();
    expect("warm reset Sync: Sync sent", lost_sync.empty() ? 0 : 1, 1);
    expect("warm reset Sync: real stamp held", dut->dbg_txts_held_o, 1);
    if (!lost_sync.empty()) {
      expect("warm reset Sync: held type", dut->dbg_txts_held_type_o, 0x0);
      expect("warm reset Sync: held sequence",
             dut->dbg_txts_held_seq_o, fld16(lost_sync, 44));
      if (lost_sync_idx < stamps.size())
        expect("warm reset Sync: held boundary time",
               dut->dbg_txts_held_ns_o, stamps[lost_sync_idx].ns);
    }
    dut->txts_hold_en_i = 0;
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    dut->tx_tready_i = 1;
    dut->txts_release_i = 0;
    expect("warm reset Sync: volatile held tuple clears",
           dut->dbg_txts_held_o, 0);

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
      if (fresh_sync_idx < stamps.size())
        expect("warm reset Sync: Follow_Up carries fresh boundary time",
               timestamp_field_ns(fresh_fu, 48), stamps[fresh_sync_idx].ns);
    }
  }

  // #214: the tag must be right where the engine reads it, every time
  expect("the slice port carried a tag at every stamp", slice_valids > 0, 1);
  expect("the slice port never lags the stamper at the valid cycle",
         slice_skews, 0);
  // ...and every stamp must name ITS OWN frame. One stamp per transmitted
  // frame, in order (the stamper's armed counting), so the pairing is
  // positional and the tags are checked against the frame's own header
  // bytes for EVERY type the run emits rather than a hard-coded few. Six
  // is what this plane transmits: Sync 0x0, Pdelay_Req 0x2, Pdelay_Resp
  // 0x3, Follow_Up 0x8, Pdelay_Resp_Follow_Up 0xA and Announce 0xB
  // (802.1AS-2011 Table 11-3 and Table 10-5).
  expect("one stamp per transmitted frame", (int)stamps.size(),
         (int)txf.size());
  int tag_wrong = 0, seq_wrong = 0, types_seen = 0, mask = 0;
  for (size_t k = 0; k < stamps.size() && k < txf.size(); k++) {
    if (txf[k].size() < 46) continue;
    int t = txf[k][14] & 0xF;
    if (stamps[k].type != t) tag_wrong++;
    if (stamps[k].seq != (uint16_t)((txf[k][44] << 8) | txf[k][45]))
      seq_wrong++;
    if (!(mask & (1 << t))) { mask |= 1 << t; types_seen++; }
  }
  expect("every stamp carries its own frame's messageType", tag_wrong, 0);
  expect("every stamp carries its own frame's sequenceId", seq_wrong, 0);
  expect("the tag is proved for all six transmitted types", types_seen, 6);

  expect("publication bank changed under stimulus", pub_changes > 0, 1);
  expect("publication commit pulse observed", pub_commits > 0, 1);
  expect("every publication change was commit-qualified",
         pub_unguarded_changes, 0);

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

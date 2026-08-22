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
  // flags: ptpTimescale, "Reserved as TRUE" for a gPTP Follow_Up
  // (802.1AS-2011 Table 11-6), which is what wire.py sends too
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
static std::vector<std::vector<uint8_t>> txf;   // unpacked lane frames
static std::vector<uint64_t> tx_sof_phc;        // phc at each frame's beat0
static std::vector<uint8_t> cur;
static bool in_tx = false;
static bool tx_first = true;

//! issue #122: capture the ingress-ts ring push/pop stamps during a burst
static std::vector<uint64_t> g_pushed, g_popped;
static bool g_ts_capture = false;

static uint64_t phc() { return dut->phc_ns_o; }

static void tick() {
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  if (g_ts_capture) {
    if (dut->dbg_tspush_v_o) g_pushed.push_back(dut->dbg_tspush_o);
    if (dut->dbg_tspop_v_o)  g_popped.push_back(dut->dbg_rx_ts_o);
  }
  if (dut->dbg_txts_v_o) last_txts_seq = dut->dbg_txts_seq_o;
  if (dut->tx_tvalid_o && dut->tx_tready_i) {
    if (tx_first) {
      cur.clear();
      in_tx = true;
      tx_sof_phc.push_back(phc());
    }
    for (int i = 0; i < 8; i++)
      if ((dut->tx_tkeep_o >> i) & 1) cur.push_back((dut->tx_tdata_o >> (8 * i)) & 0xFF);
    if (dut->tx_tlast_o) {
      txf.push_back(cur);
      in_tx = false;
      tx_first = true;
    } else {
      tx_first = false;
    }
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
  for (int i = 0; i < 8; i++) tick();
  dut->rst_n = 1;

  // ---- 1: boot -> Pdelay_Req byte-exact through the gearbox -------------
  std::vector<uint8_t> req = wait_tx(0x2, 3200000);
  if (!req.empty()) {
    expect("pdreq length", req.size(), 68);
    expect("pdreq DA", fld48(req, 0), 0x0180C200000Eull);
    expect("pdreq etype+type",
           ((uint64_t)req[12] << 16) | ((uint64_t)req[13] << 8) | req[14],
           0x88F712ull);
    expect("pdreq srcCID", fld48(req, 34), OUR_CID >> 16);
  }
  expect("asCapable low at boot", dut->pub_flags_o & FL_ASCAP, 0);
  if (!req.empty())
    expect("stamper extracted the req's seq", last_txts_seq,
           (uint16_t)((req[44] << 8) | req[45]));

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

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

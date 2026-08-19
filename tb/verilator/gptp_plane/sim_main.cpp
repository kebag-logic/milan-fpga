// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gPTP plane integration: the submodule's KL_gptp_engine steering the
// PARENT's real timestamp_counter -- the pairing the datapath splice
// will instantiate, proven closed-loop before any fabric is committed.
//
// The donor repo's own engine suite (gptp-processor/tb/verilator/engine)
// proves the 802.1AS protocol details against a MODEL of the counter;
// this suite replaces the model with hdl/ieee8021as/ptp_timestamp/
// timestamp_counter.sv itself (Q8.24 accumulator, 8.0 ns increment, the
// 125 MHz shape) and proves:
//
//  1  boot -> Pdelay_Req; one good exchange (D = 600 ns); asCapable
//     still low (Milan 4.2.6.2.4 needs two)
//  2  a live auto-answering peer -> second exchange -> asCapable
//  3  a better announce -> the plane adopts; publish bank carries the
//     GM identity and flags
//  4  closed loop: a +100 ppm master, 1 ms ahead in counter time --
//     ONE adjtime re-base near +1 ms (the master is ahead, the
//     correction is the offset's negation), then the PI addend slews the
//     REAL counter into lock: measured offset under 150 ns, the
//     latched adjfine level at the +100 ppm ideal (13,421 Q8.24 units
//     within 15%), and the counter's advance tracking the master's
//     over the last four intervals within 100 ns
//
// Timescale: the bench clock is 2 MHz while the counter keeps its
// 8.0 ns/tick shape, so "counter time" runs 62.5x slower than the
// bench's timer millisecond. That is deliberate and self-consistent:
// the µcode's servo gain is generated for the bench's
// ticks-per-sync-interval (--clk-hz 2000000, syncs every 250k ticks),
// and every timestamp below is counter-time ns.

#include <cstdint>
#include <cstdio>
#include <vector>
#include <verilated.h>
#include "Vgptp_plane_wrap.h"

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
    printf("FAIL %-30s got %016llx exp %016llx\n", what,
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
                 uint16_t flags, uint16_t body_len) {
  Frame f;
  f.u48(0x0180C200000Eull);
  f.u48(0x0080E1112233ull);
  f.u16(0x88F7);
  f.u8(0x10 | mtype); f.u8(0x02);
  f.u16(34 + body_len);
  f.u8(0); f.u8(0);
  f.u16(flags);
  f.u64(corr);
  f.u32(0);
  f.u64(PEER_CID); f.u16(1);
  f.u16(seq);
  f.u8(0x05); f.u8(0x7F);
  return f;
}

static Vgptp_plane_wrap *dut;
static uint64_t cyc = 0;
static std::vector<std::vector<uint8_t>> txf;
static std::vector<uint64_t> txns;
static std::vector<uint8_t> cur;
static bool in_tx = false;
static bool auto_txts = false;
static int auto_pend = -1;
static std::vector<uint64_t> steps_seen;
static std::vector<uint32_t> adj_seen;

static uint64_t phc() { return dut->phc_ns_o; }

static void tick() {
  if (auto_pend >= 0 && !dut->txts_valid_i) {
    uint64_t ns = phc() + 200;
    dut->txts_valid_i = 1;
    dut->txts_ns_i = ns;
    txns[auto_pend] = ns;
    auto_pend = -1;
  }
  dut->clk_i = 0; dut->eval();
  dut->clk_i = 1; dut->eval();
  if (dut->tap_adj_we_o) adj_seen.push_back(dut->tap_adj_o);
  if (dut->tap_step_we_o) steps_seen.push_back(dut->tap_step_o);
  if (dut->tx_valid_o) {
    if (dut->tx_sof_o) { cur.clear(); in_tx = true; }
    if (in_tx) cur.push_back(dut->tx_data_o);
    if (dut->tx_eof_o && in_tx) {
      txf.push_back(cur);
      txns.push_back(0);
      if (auto_txts) auto_pend = (int)txf.size() - 1;
      in_tx = false;
    }
  }
  dut->txts_valid_i = 0;
  cyc++;
}

static void run(uint64_t n) { while (n--) tick(); }

static void send_frame(const std::vector<uint8_t> &bytes, uint64_t rx_ts) {
  dut->rx_ts_i = rx_ts;
  for (size_t i = 0; i < bytes.size(); i++) {
    dut->rx_valid_i = 1;
    dut->rx_data_i = bytes[i];
    dut->rx_sof_i = (i == 0);
    dut->rx_eof_i = (i + 1 == bytes.size());
    dut->rx_err_i = 0;
    tick();
  }
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
}

static void txts(uint64_t ns) {
  dut->txts_valid_i = 1; dut->txts_ns_i = ns; dut->txts_seq_i = 0;
  tick();
  dut->txts_valid_i = 0;
}

// ---- auto peer: answers every Pdelay_Req the plane transmits --------------
static size_t pd_seen = 0;
static bool pd_on = false;

static uint64_t peer_ns(uint64_t ours) {
  return 5000000ull + ours + (ours >> 13);
}

static void service_pdelay() {
  while (pd_seen < txf.size()) {
    size_t i = pd_seen;
    if ((txf[i].size() <= 14) || ((txf[i][14] & 0xF) != 0x2)) {
      pd_seen++;
      continue;
    }
    if (txns[i] == 0) return;
    pd_seen++;
    if (!pd_on) continue;
    uint16_t seq = (uint16_t)((txf[i][44] << 8) | txf[i][45]);
    uint64_t t1 = txns[i];
    uint64_t t2 = peer_ns(t1 + 300);
    uint64_t t3 = t2 + 20000;                    // D = ~600 ns
    uint64_t t4 = t1 + 21200;
    Frame f = ptp(0x3, seq, 0, 0x0200, 20);
    f.ts(t2); f.u64(OUR_CID); f.u16(1);
    send_frame(f.b, t4);
    run(400);
    Frame g = ptp(0xA, seq, 0, 0x0000, 20);
    g.ts(t3); g.u64(OUR_CID); g.u16(1);
    send_frame(g.b, t4 + 1000);
    run(400);
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

static uint64_t fld48(const std::vector<uint8_t> &f, size_t o) {
  uint64_t v = 0; for (int i = 0; i < 6; i++) v = (v << 8) | f[o + i];
  return v;
}
static uint32_t fld32(const std::vector<uint8_t> &f, size_t o) {
  return ((uint32_t)f[o] << 24) | ((uint32_t)f[o + 1] << 16) |
         ((uint32_t)f[o + 2] << 8) | f[o + 3];
}

static size_t tx_seen = 0;
static std::vector<uint8_t> wait_tx(int mtype, uint64_t max_cycles) {
  for (uint64_t n = 0; n < max_cycles; n++) {
    while (tx_seen < txf.size()) {
      size_t i = tx_seen++;
      if (mtype < 0 || (txf[i].size() > 14 && (txf[i][14] & 0xF) == mtype))
        return txf[i];
    }
    tick();
    if ((n & 255) == 0) service_pdelay();
  }
  printf("FAIL wait_tx type %d: timeout\n", mtype);
  fails++; checks++;
  return {};
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vgptp_plane_wrap;

  dut->rst_n = 0;
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
  dut->rx_err_i = 0; dut->rx_data_i = 0; dut->rx_ts_i = 0;
  dut->tx_ready_i = 1;
  dut->txts_valid_i = 0; dut->txts_ns_i = 0; dut->txts_seq_i = 0;
  for (int i = 0; i < 8; i++) tick();
  dut->rst_n = 1;

  // ---- 1: boot -> Pdelay_Req; one exchange is not capable ---------------
  std::vector<uint8_t> req = wait_tx(0x2, 3200000);
  expect("counter is ticking", phc() > 0, 1);
  expect("asCapable low at boot", dut->pub_flags_o & FL_ASCAP, 0);
  uint64_t t1 = phc() + 200;
  txts(t1);
  run(2000);
  {
    uint64_t t2 = peer_ns(t1 + 300), t3 = t2 + 20000, t4 = t1 + 21200;
    Frame f = ptp(0x3, 0, 0, 0x0200, 20);
    f.ts(t2); f.u64(OUR_CID); f.u16(1);
    send_frame(f.b, t4);
    run(4000);
    Frame g = ptp(0xA, 0, 0, 0x0000, 20);
    g.ts(t3); g.u64(OUR_CID); g.u16(1);
    send_frame(g.b, t4 + 1000);
    run(6000);
  }
  expect("pdelay measured", dut->pub_pdelay_ns_o, 600);
  expect("one exchange not capable", dut->pub_flags_o & FL_ASCAP, 0);

  // ---- 2: the live peer raises asCapable at the second exchange ---------
  auto_txts = true;
  pd_seen = txf.size();
  pd_on = true;
  expect("second exchange -> capable",
         wait_flags(FL_ASCAP, FL_ASCAP, 6000000ull), 1);

  // ---- 3: better announce -> adopt; the publish bank is the contract ----
  {
    Frame f = ptp(0xB, 10, 0, 0x0008, 30);
    for (int i = 0; i < 10; i++) f.u8(0);
    f.u16(0xFFC4); f.u8(0);
    f.u8(100); f.u32(OUR_CQ); f.u8(248);
    f.u64(GMID);
    f.u16(0); f.u8(0xA0);
    send_frame(f.b, phc() + 150);
    run_svc(6000);
  }
  expect("adopted", dut->pub_flags_o & 3, FL_PRESENT);
  expect("pub gm id", dut->pub_gm_id_o, GMID);

  // ---- 4: closed loop -- the engine steers the REAL counter -------------
  // master: independent of the steered counter, +100 ppm in counter
  // time (8 ns + 8/10000 per bench cycle), starting 1 ms ahead
  {
    size_t steps_before = steps_seen.size();
    uint64_t mst_base =
        phc() + 1000000ull - cyc * 8ull - cyc / 1250ull;
    uint16_t sq = 0x0300;
    uint64_t c_lock = 0, m_lock = 0;             // window for rate check
    for (int k = 0; k < 24; k++) {
      if ((k % 8) == 0) {                        // keep the GM elected
        Frame a = ptp(0xB, (uint16_t)(20 + k), 0, 0x0008, 30);
        for (int i = 0; i < 10; i++) a.u8(0);
        a.u16(0xFFC4); a.u8(0);
        a.u8(100); a.u32(OUR_CQ); a.u8(248);
        a.u64(GMID);
        a.u16(0); a.u8(0xA0);
        send_frame(a.b, phc() + 150);
        run(4000);
      }
      run_svc(250000);                           // one sync interval
      if (k == 20) { c_lock = phc(); m_lock = mst_base + cyc * 8ull
                                              + cyc / 1250ull; }
      uint64_t origin = mst_base + cyc * 8ull + cyc / 1250ull;
      uint64_t local_rx = phc() + 150;
      Frame f = ptp(0x0, sq, 0, 0x0208, 10);
      f.ts(0);
      send_frame(f.b, local_rx);
      run(1000);
      Frame g = ptp(0x8, sq, 0, 0x0000, 10);
      g.ts(origin);
      send_frame(g.b, local_rx + 500);
      run(4000);
      sq++;
    }
    expect("one adjtime re-base", steps_seen.size(), steps_before + 1);
    int64_t step = (int64_t)steps_seen.back();
    expect("re-base near +1 ms",
           step > 995000 && step < 1005000, 1);
    int32_t final_off = (int32_t)dut->pub_offset_o;
    expect("measured offset locked",
           final_off > -150 && final_off < 150, 1);
    // +100 ppm of 8 ns/tick = 0.0008 ns/tick = 13,421 Q8.24 units
    int32_t final_adj = (int32_t)adj_seen.back();
    expect("addend at the +100 ppm ideal",
           final_adj > 11408 && final_adj < 15434, 1);
    // the REAL proof: the counter's advance tracks the master's
    uint64_t c_now = phc();
    uint64_t m_now = mst_base + cyc * 8ull + cyc / 1250ull;
    int64_t rate_err = (int64_t)(c_now - c_lock) -
                       (int64_t)(m_now - m_lock);
    expect("counter tracks the master",
           rate_err > -100 && rate_err < 100, 1);
    expect("sync-ok held through lock",
           dut->pub_flags_o & FL_SYNCOK, FL_SYNCOK);
  }

  // ---- 5: as master, the Sync origin carries the REAL counter -----------
  // announce silence rides out the receipt timeout (pdelay keeps
  // asCapable alive), the plane becomes grandmaster, and its Sync's
  // originTimestamp must be the live timestamp_counter value -- the
  // phc_ns_i observing check PR #113's review filed as its blind spot
  // (the submodule's v6 gather consumer makes it observable)
  {
    expect("quiet ride to grandmaster",
           wait_flags(FL_AMGM, FL_AMGM, 10000000ull), 1);
    tx_seen = txf.size();
    std::vector<uint8_t> sy = wait_tx(0x0, 800000);
    if (!sy.empty()) {
      uint64_t origin = fld48(sy, 48) * 1000000000ull + fld32(sy, 54);
      uint64_t now = phc();
      int64_t d = (int64_t)(now - origin);
      expect("origin is the real counter", d >= 0 && d < 300000, 1);
    }
  }

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}

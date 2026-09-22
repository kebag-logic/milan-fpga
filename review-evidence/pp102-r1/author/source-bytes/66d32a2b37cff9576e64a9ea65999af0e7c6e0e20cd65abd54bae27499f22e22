// SPDX-License-Identifier: CERN-OHL-W-2.0
// side_port suite — independent expectations, never DUT logic.
//
// Proves the 07 §5.5 window decode at every boundary address, the 07 §2
// access-rights enforcement (RO write refused with err + never forwarded;
// image writes only pre-enable), byte-exact RW forwarding through wait
// states, single-outstanding acceptance, and the P-TRACE-RING ring: 300
// writes wrap (counter 300, oldest overwritten), window-path read-back
// bit-exact against an independent C++ ring model, and read-during-write
// returning the OLD record (read-first).
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include "Vside_port_tb_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// P-TRACE-RING geometry: the ring holds kRingRecords records of kRecordLanes
// 32-bit lanes each, and the write counter is mod-2^16.
constexpr uint32_t kRingRecords = 256;
constexpr uint32_t kRecordLanes = 4;
constexpr uint32_t kRingIndexMask = kRingRecords - 1;
constexpr uint32_t kCountMask = 0xFFFFu;

// host-side transaction guard: hold req for at most this many cycles
constexpr int kXactTimeoutCycles = 32;

// deterministic environment data for the five stubbed windows
static uint32_t stub_val(int win, uint32_t off) {
  return (static_cast<uint32_t>(win) << 28) ^ (off * 2654435761u) ^ 0x005A17E5u;
}

// deterministic trace-record lanes; lane 0 = record bits [127:96] (MSB-first)
static uint32_t rec_lane(uint32_t k, uint32_t j) {
  return (k * 0x01000193u) ^ (j * 0x9E3779B9u) ^ 0xC0DE0000u;
}

struct Stub {
  int lat = 1;              // response latency in cycles (>= 1)
  int pend = 0;
  uint32_t resp = 0;
  int reqs = 0;
  bool last_we = false;
  uint32_t last_addr = 0;
  uint32_t last_wdata = 0;
};

struct Harness {
  Vside_port_tb_wrap* dut;
  Stub img;
  Stub dbg;
  Stub snap;
  Stub ctrl;
  Stub fw;
  int trace_reqs = 0;

  // ---- independent ring model (mod-2^16 count, 256 records × 4 lanes) ----
  uint32_t rcnt = 0;
  std::array<std::array<uint32_t, kRecordLanes>, kRingRecords> rmem{};

  bool rv_seen = false;
  bool err_seen = false;
  uint32_t rdata_seen = 0;
  bool b_rv_seen = false;
  bool b_err_seen = false;
  uint32_t b_rdata_seen = 0;

  explicit Harness(Vside_port_tb_wrap* d) : dut(d) {}

  void drive_stub(Stub& s, CData& rvalid, IData& rdata) {
    rvalid = 0;
    if (s.pend > 0) {
      if (s.pend == 1) { rvalid = 1; rdata = s.resp; }
      s.pend--;
    }
  }

  void observe_stub(Stub& s, int win, bool req, bool we, uint32_t addr,
                    uint32_t wdata) {
    if (!req) return;
    s.reqs++;
    s.last_we = we;
    s.last_addr = addr;
    s.last_wdata = wdata;
    s.resp = stub_val(win, addr);
    s.pend = s.lat;
  }

  void tick() {
    drive_stub(img,  dut->img_rvalid_i,  dut->img_rdata_i);
    drive_stub(dbg,  dut->dbg_rvalid_i,  dut->dbg_rdata_i);
    drive_stub(snap, dut->snap_rvalid_i, dut->snap_rdata_i);
    drive_stub(ctrl, dut->ctrl_rvalid_i, dut->ctrl_rdata_i);
    drive_stub(fw,   dut->fw_rvalid_i,   dut->fw_rdata_i);

    dut->clk_i = 0;
    dut->eval();

    // pre-edge observation: what the registers are about to see
    observe_stub(img, 0, dut->img_req_o, dut->img_we_o, dut->img_addr_o,
                 dut->img_wdata_o);
    observe_stub(dbg, 1, dut->dbg_req_o, false, dut->dbg_addr_o, 0);
    observe_stub(snap, 2, dut->snap_req_o, false, dut->snap_addr_o, 0);
    observe_stub(ctrl, 3, dut->ctrl_req_o, dut->ctrl_we_o, dut->ctrl_addr_o,
                 dut->ctrl_wdata_o);
    observe_stub(fw, 5, dut->fw_req_o, dut->fw_we_o, dut->fw_addr_o,
                 dut->fw_wdata_o);
    if (dut->trace_req_o) trace_reqs++;

    rv_seen = dut->rvalid_o;
    err_seen = dut->err_o;
    rdata_seen = dut->rdata_o;
    b_rv_seen = dut->b_rvalid_o;
    b_err_seen = dut->b_err_o;
    b_rdata_seen = dut->b_rdata_o;

    bool wv = dut->trc_wr_valid_i;
    std::array<uint32_t, kRecordLanes> lanes = {0, 0, 0, 0};
    if (wv) {  // VlWide word 0 = bits [31:0] = lane 3 (MSB-first lanes)
      lanes[0] = dut->trc_wr_data_i[3];
      lanes[1] = dut->trc_wr_data_i[2];
      lanes[2] = dut->trc_wr_data_i[1];
      lanes[3] = dut->trc_wr_data_i[0];
    }

    dut->clk_i = 1;
    dut->eval();

    // ring model commits with the posedge (read-first vs same-edge reads)
    if (wv) {
      rmem[rcnt & kRingIndexMask] = {lanes[0], lanes[1], lanes[2], lanes[3]};
      rcnt = (rcnt + 1) & kCountMask;
    }
  }

  // ---- host A transaction: hold req until rvalid (F02.7 semantics) ----
  struct Rsp { bool done; bool err; uint32_t data; int cycles; };
  Rsp xact(bool we, uint32_t addr, uint32_t wdata = 0,
           int timeout = kXactTimeoutCycles) {
    dut->req_valid_i = 1;
    dut->we_i = we;
    dut->addr_i = addr;
    dut->wdata_i = wdata;
    for (int i = 0; i < timeout; ++i) {
      tick();
      if (rv_seen) {
        dut->req_valid_i = 0;
        dut->we_i = 0;
        return {true, err_seen, rdata_seen, i};
      }
    }
    dut->req_valid_i = 0;
    dut->we_i = 0;
    return {false, false, 0, timeout};
  }

  Rsp b_xact(bool we, uint32_t addr, uint32_t wdata = 0,
             int timeout = kXactTimeoutCycles) {
    dut->b_req_valid_i = 1;
    dut->b_we_i = we;
    dut->b_addr_i = addr;
    dut->b_wdata_i = wdata;
    for (int i = 0; i < timeout; ++i) {
      tick();
      if (b_rv_seen) {
        dut->b_req_valid_i = 0;
        dut->b_we_i = 0;
        return {true, b_err_seen, b_rdata_seen, i};
      }
    }
    dut->b_req_valid_i = 0;
    dut->b_we_i = 0;
    return {false, false, 0, timeout};
  }

  void write_record(uint32_t k) {
    dut->trc_wr_data_i[3] = rec_lane(k, 0);  // bits [127:96]
    dut->trc_wr_data_i[2] = rec_lane(k, 1);
    dut->trc_wr_data_i[1] = rec_lane(k, 2);
    dut->trc_wr_data_i[0] = rec_lane(k, 3);  // bits [31:0]
    dut->trc_wr_valid_i = 1;
    tick();
    dut->trc_wr_valid_i = 0;
  }

  int total_fwd_reqs() const {
    return img.reqs + dbg.reqs + snap.reqs + ctrl.reqs + fw.reqs + trace_reqs;
  }
};

static uint32_t trace_addr(uint32_t rec, uint32_t lane) {
  return 0x40000u | (rec << 2) | lane;
}

namespace {

//! Owns the model, the two host BFMs and the tally, so every phase below
//! drives the same DUT and counts into the same summary line.
class SidePortSuite {
 public:
  SidePortSuite() : dut(model.get()), h(dut) {}

  int run();

 private:
  void reset_leaves_the_bus_quiet();
  void window_decode_at_every_boundary();
  void unmapped_addresses_are_refused();
  void read_only_windows_refuse_writes();
  void image_window_writes_only_before_enable();
  void rw_windows_forward_through_wait_states();
  void single_outstanding_request_is_accepted_once();
  void instance_b_drops_the_firmware_window();
  void ring_first_fill_reads_back_bit_exact();
  void three_hundred_writes_wrap_the_ring();
  void read_during_write_returns_the_old_record();
  void decode_still_exact_after_the_campaign();

  const milan::tb::Model<Vside_port_tb_wrap> model;
  Vside_port_tb_wrap* const dut;
  Harness h;
  int checks = 0;
  int fails = 0;
};

void SidePortSuite::reset_leaves_the_bus_quiet() {
  dut->rst_n = 0;
  dut->entity_enable_i = 0;
  dut->req_valid_i = 0;
  dut->b_req_valid_i = 0;
  dut->trc_wr_valid_i = 0;
  for (int i = 0; i < 4; ++i) h.tick();
  CHECK(!h.rv_seen && !h.b_rv_seen, "bus quiet in reset");
  dut->rst_n = 1;
  h.tick();
  CHECK(dut->trc_wr_count_o == 0, "ring count 0 after reset");
}

// ---- T1: window decode at every boundary (first/last word) ------------
void SidePortSuite::window_decode_at_every_boundary() {
  struct Bound { int win; uint32_t addr; Stub* s; };
  const Bound rd_bounds[] = {
      {0, 0x00000u, &h.img},  {0, 0x0FFFFu, &h.img},
      {1, 0x10000u, &h.dbg},  {1, 0x1FFFFu, &h.dbg},
      {2, 0x20000u, &h.snap}, {2, 0x2FFFFu, &h.snap},
      {3, 0x30000u, &h.ctrl}, {3, 0x300FFu, &h.ctrl},
      {5, 0x50000u, &h.fw},   {5, 0x5FFFFu, &h.fw},
  };
  for (const auto& b : rd_bounds) {
    int before = b.s->reqs;
    auto r = h.xact(false, b.addr);
    uint32_t off = (b.win == 3) ? (b.addr & 0xFFu) : (b.addr & 0xFFFFu);
    CHECK(r.done && !r.err, "read 0x%05X completes clean", b.addr);
    CHECK(b.s->reqs == before + 1 && !b.s->last_we && b.s->last_addr == off,
          "read 0x%05X forwarded once to win %d offset 0x%04X (got %d/%u)",
          b.addr, b.win, off, b.s->reqs - before, b.s->last_addr);
    CHECK(r.data == stub_val(b.win, off),
          "read 0x%05X routes win-%d data (got %08X)", b.addr, b.win, r.data);
  }

  // trace window boundaries: 0x40000 = record 0 lane 0; 0x4FFFF has offset
  // bit 10 set -> the counter per the TB glue map (count still 0 here)
  {
    int before = h.trace_reqs;
    auto r0 = h.xact(false, 0x40000u);
    CHECK(r0.done && !r0.err && h.trace_reqs == before + 1,
          "trace window first word forwards");
    auto r1 = h.xact(false, 0x4FFFFu);
    CHECK(r1.done && !r1.err && r1.data == 0,
          "trace window last word forwards (count map, got %08X)", r1.data);
  }
}

// ---- T2: out-of-range / unmapped -> err, nothing forwarded ------------
void SidePortSuite::unmapped_addresses_are_refused() {
  const std::array<uint32_t, 5> bad_addrs = {0x30100u, 0x3FFFFu, 0x60000u,
                                             0x70000u, 0xFFFFFu};
  for (uint32_t a : bad_addrs) {
    int before = h.total_fwd_reqs();
    auto r = h.xact(false, a);
    CHECK(r.done && r.err, "read 0x%05X refused with err", a);
    CHECK(h.total_fwd_reqs() == before, "read 0x%05X not forwarded", a);
    CHECK(r.data == 0, "error response rdata 0 (got %08X)", r.data);
  }
  {
    auto r = h.xact(true, 0x60000u, 0x12345678u);
    CHECK(r.done && r.err, "unmapped write refused with err");
    CHECK(r.cycles == 1, "error response is single-cycle (got %d)", r.cycles);
  }
}

// ---- T3: RO windows refuse writes, err, never forwarded ---------------
void SidePortSuite::read_only_windows_refuse_writes() {
  const std::array<uint32_t, 5> ro_wr = {0x10000u, 0x1FFFFu, 0x2ABCDu,
                                         0x40000u, 0x4B123u};
  for (uint32_t a : ro_wr) {
    int before = h.total_fwd_reqs();
    auto r = h.xact(true, a, 0xBADC0DEu);
    CHECK(r.done && r.err, "RO write 0x%05X refused with err", a);
    CHECK(h.total_fwd_reqs() == before, "RO write 0x%05X not forwarded", a);
  }
}

// ---- T4: image window W pre-enable only (07 §2) -----------------------
void SidePortSuite::image_window_writes_only_before_enable() {
  {
    dut->entity_enable_i = 0;
    auto r = h.xact(true, 0x00123u, 0xA5C31E7Bu);
    CHECK(r.done && !r.err, "image write pre-enable completes clean");
    CHECK(h.img.last_we && h.img.last_addr == 0x0123u &&
              h.img.last_wdata == 0xA5C31E7Bu,
          "image write forwarded byte-exact (we=%d addr=%04X data=%08X)",
          h.img.last_we, h.img.last_addr, h.img.last_wdata);

    dut->entity_enable_i = 1;
    int before = h.img.reqs;
    auto r2 = h.xact(true, 0x00123u, 0x11111111u);
    CHECK(r2.done && r2.err, "image write post-enable refused with err");
    CHECK(h.img.reqs == before, "image write post-enable not forwarded");

    auto r3 = h.xact(false, 0x00040u);
    CHECK(r3.done && !r3.err && r3.data == stub_val(0, 0x0040u),
          "image READ still allowed post-enable (07 §2 read-only everywhere)");
    dut->entity_enable_i = 0;
  }
}

// ---- T5: RW windows forward writes byte-exact through wait states -----
void SidePortSuite::rw_windows_forward_through_wait_states() {
  {
    h.ctrl.lat = 3;
    auto r = h.xact(true, 0x30040u, 0x0F1E2D3Cu);
    CHECK(r.done && !r.err, "ctrl write completes");
    CHECK(r.cycles == 3, "ctrl write waits for the backend ack (got %d)",
          r.cycles);
    CHECK(h.ctrl.last_we && h.ctrl.last_addr == 0x40u &&
              h.ctrl.last_wdata == 0x0F1E2D3Cu,
          "ctrl write byte-exact (addr=%02X data=%08X)", h.ctrl.last_addr,
          h.ctrl.last_wdata);
    h.ctrl.lat = 1;

    h.fw.lat = 4;
    auto r2 = h.xact(true, 0x5CAFEu, 0xFEEDF00Du);
    CHECK(r2.done && !r2.err && r2.cycles == 4, "fw write waits 4 (got %d)",
          r2.cycles);
    CHECK(h.fw.last_we && h.fw.last_addr == 0xCAFEu &&
              h.fw.last_wdata == 0xFEEDF00Du,
          "fw write byte-exact (addr=%04X data=%08X)", h.fw.last_addr,
          h.fw.last_wdata);
    h.fw.lat = 1;
  }
}

// ---- T6: single outstanding — held request accepted exactly once, and
//          a mid-wait address change must not fire another window -------
void SidePortSuite::single_outstanding_request_is_accepted_once() {
  {
    h.ctrl.lat = 4;
    int ctrl_before = h.ctrl.reqs;
    int dbg_before = h.dbg.reqs;
    dut->req_valid_i = 1;
    dut->we_i = 0;
    dut->addr_i = 0x30011u;
    h.tick();                    // accept
    dut->addr_i = 0x10011u;      // wander mid-wait: must be ignored
    int cycles = 1;
    while (!h.rv_seen && cycles < 16) { h.tick(); cycles++; }
    dut->req_valid_i = 0;
    CHECK(h.rv_seen && !h.err_seen, "held request completes");
    CHECK(h.ctrl.reqs == ctrl_before + 1, "accepted exactly once");
    CHECK(h.dbg.reqs == dbg_before, "mid-wait addr change fires nothing");
    CHECK(h.rdata_seen == stub_val(3, 0x11u), "response is the accepted addr");
    h.ctrl.lat = 1;
    h.tick();
  }
}

// ---- T7: instance B (P-EN-FIRMWARE-ASSIST = 0): window 5 vanishes -----
void SidePortSuite::instance_b_drops_the_firmware_window() {
  {
    auto r = h.b_xact(false, 0x30010u);
    CHECK(r.done && !r.err && r.data == 0xB0B0B0B0u,
          "B: ctrl read forwards (got %08X)", r.data);
    auto r2 = h.b_xact(false, 0x50000u);
    CHECK(r2.done && r2.err, "B: fw read refused when parameter off");
    auto r3 = h.b_xact(true, 0x5FFFFu, 1);
    CHECK(r3.done && r3.err, "B: fw write refused when parameter off");
  }
}

// ---- T8: ring first fill — 5 records, all lanes bit-exact -------------
void SidePortSuite::ring_first_fill_reads_back_bit_exact() {
  for (uint32_t k = 0; k < 5; ++k) h.write_record(k);
  CHECK(dut->trc_wr_count_o == 5, "count 5 after 5 writes (got %u)",
        dut->trc_wr_count_o);
  for (uint32_t rec = 0; rec < 5; ++rec) {
    for (uint32_t lane = 0; lane < kRecordLanes; ++lane) {
      auto r = h.xact(false, trace_addr(rec, lane));
      CHECK(r.done && !r.err && r.data == h.rmem[rec][lane],
            "rec %u lane %u via window (got %08X want %08X)", rec, lane,
            r.data, h.rmem[rec][lane]);
    }
  }
  {
    auto r = h.xact(false, 0x40400u);  // offset bit 10 -> counter
    CHECK(r.done && !r.err && r.data == (h.rcnt & kCountMask),
          "counter via window (got %08X)", r.data);
  }
}

// ---- T9: 300 writes wrap — counter 300, oldest overwritten ------------
void SidePortSuite::three_hundred_writes_wrap_the_ring() {
  for (uint32_t k = 5; k < 300; ++k) h.write_record(k);
  CHECK(dut->trc_wr_count_o == 300, "count 300 after 300 writes (got %u)",
        dut->trc_wr_count_o);
  {
    auto r = h.xact(false, 0x40400u);
    CHECK(r.done && !r.err && r.data == 300u, "counter 300 via window");
  }
  // model says: indices 0..43 hold records 256..299, 44..255 hold 44..255
  CHECK(h.rmem[0][0] == rec_lane(256, 0), "model: index 0 overwritten");
  CHECK(h.rmem[44][0] == rec_lane(44, 0), "model: index 44 is the oldest");
  for (uint32_t rec = 0; rec < kRingRecords; ++rec) {
    bool ok = true;
    std::array<uint32_t, kRecordLanes> got = {0, 0, 0, 0};
    for (uint32_t lane = 0; lane < kRecordLanes; ++lane) {
      auto r = h.xact(false, trace_addr(rec, lane));
      got[lane] = r.data;
      ok = ok && r.done && !r.err && (r.data == h.rmem[rec][lane]);
    }
    CHECK(ok, "post-wrap rec %u bit-exact (got %08X %08X %08X %08X)", rec,
          got[0], got[1], got[2], got[3]);
  }
}

// ---- T10: read during write — same record returns the OLD data --------
void SidePortSuite::read_during_write_returns_the_old_record() {
  {
    // write pointer is at 300 % 256 = 44; read record 44 in the same cycle
    uint32_t old0 = h.rmem[44][0];
    CHECK(old0 == rec_lane(44, 0), "precondition: index 44 still record 44");

    dut->trc_wr_data_i[3] = rec_lane(300, 0);
    dut->trc_wr_data_i[2] = rec_lane(300, 1);
    dut->trc_wr_data_i[1] = rec_lane(300, 2);
    dut->trc_wr_data_i[0] = rec_lane(300, 3);
    dut->trc_wr_valid_i = 1;
    dut->req_valid_i = 1;
    dut->we_i = 0;
    dut->addr_i = trace_addr(44, 0);
    h.tick();  // accept + RAM read + RAM write on the same edge
    dut->trc_wr_valid_i = 0;
    int cycles = 1;
    while (!h.rv_seen && cycles < 8) { h.tick(); cycles++; }
    dut->req_valid_i = 0;
    CHECK(h.rv_seen && !h.err_seen, "read-during-write completes");
    CHECK(h.rdata_seen == old0,
          "same-address read returns OLD record (got %08X want %08X)",
          h.rdata_seen, old0);
    CHECK(dut->trc_wr_count_o == 301, "count 301 after the concurrent write");

    auto r = h.xact(false, trace_addr(44, 0));
    CHECK(r.data == rec_lane(300, 0), "re-read sees the NEW record");

    // and a read of a DIFFERENT record during a write is undisturbed
    dut->trc_wr_data_i[3] = rec_lane(301, 0);
    dut->trc_wr_data_i[2] = rec_lane(301, 1);
    dut->trc_wr_data_i[1] = rec_lane(301, 2);
    dut->trc_wr_data_i[0] = rec_lane(301, 3);
    dut->trc_wr_valid_i = 1;
    dut->req_valid_i = 1;
    dut->we_i = 0;
    dut->addr_i = trace_addr(100, 2);
    h.tick();
    dut->trc_wr_valid_i = 0;
    cycles = 1;
    while (!h.rv_seen && cycles < 8) { h.tick(); cycles++; }
    dut->req_valid_i = 0;
    CHECK(h.rv_seen && h.rdata_seen == h.rmem[100][2],
          "other-address read during write bit-exact");
  }
}

// ---- T11: decode still exact after all traffic ------------------------
void SidePortSuite::decode_still_exact_after_the_campaign() {
  {
    auto r = h.xact(false, 0x2FFFFu);
    CHECK(r.done && !r.err && r.data == stub_val(2, 0xFFFFu),
          "snap boundary still exact after the campaign");
    auto r2 = h.xact(true, 0x40001u, 0);
    CHECK(r2.done && r2.err, "trace window still RO after the campaign");
  }

}

int SidePortSuite::run() {
  reset_leaves_the_bus_quiet();
  window_decode_at_every_boundary();
  unmapped_addresses_are_refused();
  read_only_windows_refuse_writes();
  image_window_writes_only_before_enable();
  rw_windows_forward_through_wait_states();
  single_outstanding_request_is_accepted_once();
  instance_b_drops_the_firmware_window();
  ring_first_fill_reads_back_bit_exact();
  three_hundred_writes_wrap_the_ring();
  read_during_write_returns_the_old_record();
  decode_still_exact_after_the_campaign();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SidePortSuite suite;
  return suite.run();
}

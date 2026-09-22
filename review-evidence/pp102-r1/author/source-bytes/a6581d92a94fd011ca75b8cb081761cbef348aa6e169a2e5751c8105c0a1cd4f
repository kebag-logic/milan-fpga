// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_aecp_resp_buf suite — independent expectations, never DUT logic.
//
// The AECP response buffer lives in the integrator's MAIN MEMORY (03 §7): the
// µCPU writes byte-strobed fields into it, the block gathers them into 64-bit
// lanes, writes each finished lane out over the read/write master, and streams
// the emitted payload back to the frame builder as one burst.
//
// Two independent models, neither of them a copy of the DUT:
//
//  1. A latency-injecting memory BFM with BOTH channels. Its read latency is
//     29 clocks and its write latency 23 BY DEFAULT and never zero — the
//     reference SoC measures ~1424 ns on a miss to main memory, and a buffer
//     tested only against zero-latency memory is untested against the thing
//     that makes it hard. The BFM also plays a bridge that never accepts
//     anything, one that answers a beat with rsp_err, and one that reports a
//     write error.
//
//  2. A byte-image model of what the CONTRACT says memory should end up
//     holding: bytes below 12 dropped, bytes at or above RESP_BYTES dropped,
//     the m strobed bytes of a write placed BIG-ENDIAN from wr_addr upward,
//     and a byte whose strobe is 0 left alone. Every check compares the DUT's
//     memory image and its streamed bytes against THAT, so a buffer that
//     agrees only with itself fails.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "VKL_aecp_resp_buf.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

constexpr uint32_t RESP_BASE  = 0x20100000u;   // the module's default
constexpr uint32_t RESP_BYTES = 592u;
constexpr uint8_t  POISON     = 0xC3;          // never a legal payload byte
constexpr int      TMO        = 96;            // -GMEM_TIMEOUT_CYC_P

//! The BFM's default latencies, in clocks. Neither is ever zero: the
//! reference SoC measures ~1424 ns on a miss to main memory. Individual arms
//! move them and put them back.
constexpr int kMemReadLatency  = 29;
constexpr int kMemWriteLatency = 23;

//! Clocks the reset is held low for.
constexpr int kResetTicks = 4;

//! Loop guards, not timing expectations: they only stop a hung DUT from
//! spinning forever. kWriteGuard bounds one held µCPU write and the wait for
//! the block to leave a transaction; kStreamGuard bounds a whole payload
//! drain.
constexpr int kWriteGuard  = 4000;
constexpr int kStreamGuard = 20000;

// ===========================================================================
// the memory BFM — read burst + single-beat writes, both with latency
// ===========================================================================
struct Mem {
  VKL_aecp_resp_buf* dut;
  std::vector<uint8_t> b;
  int  rlat = kMemReadLatency;
  int  wlat = kMemWriteLatency;
  bool off = false;          // a bridge that never accepts anything
  bool werr = false;         // ... one that fails every write
  int  rerr_at = -1;         // ... one that answers this beat with rsp_err

  bool rbusy = false;
  bool wbusy = false;
  uint32_t raddr = 0;
  uint32_t waddr = 0;
  uint64_t wdata = 0;
  uint8_t  wstrb = 0;
  int rbeats = 0;
  int ridx = 0;
  int rwait = 0;
  int wcnt = 0;
  uint64_t bursts = 0;
  uint64_t beats = 0;
  uint64_t writes = 0;

  explicit Mem(VKL_aecp_resp_buf* d) : dut(d), b(RESP_BYTES, POISON) {}

  uint64_t rd64(uint32_t a) const {
    uint64_t v = 0;
    for (int i = 0; i < 8; ++i) {
      uint32_t k = a + uint32_t(i);
      v = (v << 8) | ((k < b.size()) ? b[k] : 0x5Cu);
    }
    return v;
  }

  void drive() {
    dut->mem_req_ready_i = (!rbusy && !off) ? 1 : 0;
    dut->mem_rsp_valid_i = 0;
    dut->mem_rsp_data_i  = 0;
    dut->mem_rsp_last_i  = 0;
    dut->mem_rsp_err_i   = 0;
    if (rbusy && rwait == 0 && ridx < rbeats) {
      dut->mem_rsp_valid_i = 1;
      dut->mem_rsp_data_i  = rd64(raddr - RESP_BASE + uint32_t(8 * ridx));
      dut->mem_rsp_last_i  = (ridx == rbeats - 1) ? 1 : 0;
      dut->mem_rsp_err_i   = (rerr_at >= 0 && ridx == rerr_at) ? 1 : 0;
    }
    dut->mem_wr_ready_i = (!wbusy && !off) ? 1 : 0;
    dut->mem_wr_done_i  = 0;
    dut->mem_wr_err_i   = 0;
  }

  void update() {
    // ---- read burst ----
    if (!rbusy) {
      if (!off && dut->mem_req_valid_o) {
        rbusy  = true;
        raddr  = dut->mem_req_addr_o;
        rbeats = dut->mem_req_beats_o;
        ridx   = 0;
        rwait  = rlat;
        ++bursts;
      }
    } else if (rwait > 0) {
      --rwait;
    } else if (dut->mem_rsp_valid_i && dut->mem_rsp_ready_o) {
      ++beats;
      if (dut->mem_rsp_err_i)  rbusy = false;
      else if (++ridx >= rbeats) rbusy = false;
    }
    // ---- single-beat write ----
    if (!wbusy) {
      if (!off && dut->mem_wr_valid_o) {
        wbusy = true;
        waddr = dut->mem_wr_addr_o;
        wdata = dut->mem_wr_data_o;
        wstrb = dut->mem_wr_strb_o;
        wcnt  = wlat;
      }
    } else if (--wcnt <= 0) {
      if (!werr) {
        // byte n of the lane is bits [63-8n -: 8]; strobe 0 = untouched
        for (int i = 0; i < 8; ++i) {
          if ((wstrb >> i) & 1) {
            uint32_t k = waddr - RESP_BASE + uint32_t(i);
            if (k < b.size()) b[k] = uint8_t(wdata >> (56 - 8 * i));
          }
        }
      }
      wbusy = false;
      ++writes;
    }
  }

  // the write ACK is a one-cycle pulse in the cycle wcnt expires
  void ack() {
    dut->mem_wr_done_i = 1;
    dut->mem_wr_err_i  = werr ? 1 : 0;
  }
};

// ===========================================================================
// the CONTRACT model — what memory should hold, derived from the banner
// ===========================================================================
struct Ref {
  std::vector<uint8_t> b = std::vector<uint8_t>(RESP_BYTES, POISON);

  void reset() { b.assign(RESP_BYTES, POISON); }

  // wr_wdata carries the field value right-justified; wr_wstrb is
  // low-contiguous and gives the width; the m bytes go BIG-ENDIAN upward
  void write(uint32_t addr, uint32_t data, uint8_t strb) {
    int m = (strb & 0x8) ? 4 : (strb & 0x2) ? 2 : (strb & 0x1) ? 1 : 0;
    for (int j = 0; j < m; ++j) {
      uint32_t a = addr + uint32_t(j);
      if (a < 12 || a >= RESP_BYTES) continue;    // header record / past end
      uint8_t v;
      if (m == 1)      v = uint8_t(data);
      else if (m == 2) v = uint8_t(data >> (8 * (1 - j)));
      else             v = uint8_t(data >> (8 * (3 - j)));
      b[a] = v;
    }
  }
};

// ===========================================================================
// harness
// ===========================================================================
struct H {
  VKL_aecp_resp_buf* dut;
  Mem mem;
  Ref ref;
  uint64_t t = 0;
  std::vector<uint8_t> got;      // bytes the DUT streamed back

  explicit H(VKL_aecp_resp_buf* d) : dut(d), mem(d) {}

  void tick() {
    mem.drive();
    dut->clk_i = 0; dut->eval();
    // the write ACK has to be visible in the same cycle the model commits
    if (mem.wbusy && mem.wcnt == 1) { mem.ack(); dut->eval(); }
    mem.update();
    dut->clk_i = 1; dut->eval();
    ++t;
  }

  void idle(int n) { for (int i = 0; i < n; ++i) tick(); }

  void reset() {
    dut->rst_n = 0;
    dut->open_i = 0; dut->seal_i = 0; dut->seal_len_i = 0;
    dut->wr_we_i = 0; dut->wr_addr_i = 0; dut->wr_wdata_i = 0;
    dut->wr_wstrb_i = 0; dut->rd_take_i = 0;
    mem.rbusy = false; mem.wbusy = false; mem.rwait = 0; mem.wcnt = 0;
    for (int i = 0; i < kResetTicks; ++i) tick();
    dut->rst_n = 1;
    tick();
  }

  void open() {
    // the block only accepts a re-arm while it is not mid-transaction
    for (int i = 0; i < kWriteGuard && dut->busy_o; ++i) tick();
    dut->open_i = 1; tick(); dut->open_i = 0;
    ref.reset();
    got.clear();
  }

  // present one µCPU write and hold it until the buffer takes it; returns the
  // number of cycles it was held (0 = accepted immediately)
  int write(uint32_t addr, uint32_t data, uint8_t strb,
            int limit = kWriteGuard) {
    dut->wr_we_i = 1; dut->wr_addr_i = addr;
    dut->wr_wdata_i = data; dut->wr_wstrb_i = strb;
    int held = 0;
    for (int i = 0; i < limit; ++i) {
      dut->eval();
      if (dut->wr_ready_o) { tick(); break; }
      ++held; tick();
    }
    dut->wr_we_i = 0; dut->wr_wstrb_i = 0;
    ref.write(addr, data, strb);
    return held;
  }

  void seal(uint32_t len) {
    dut->seal_i = 1; dut->seal_len_i = len; tick();
    dut->seal_i = 0; dut->seal_len_i = 0;
  }

  // drain the payload stream; stops on err_o or when `len` bytes are in
  bool stream(uint32_t len, int limit = kStreamGuard) {
    got.clear();
    for (int i = 0; i < limit && got.size() < len; ++i) {
      dut->eval();
      if (dut->err_o) return false;
      if (dut->rd_valid_o) {
        got.push_back(uint8_t(dut->rd_data_o));
        dut->rd_take_i = 1; tick(); dut->rd_take_i = 0;
      } else {
        tick();
      }
    }
    return got.size() == len;
  }

  bool wait_idle(int limit = kStreamGuard) {
    for (int i = 0; i < limit; ++i) {
      dut->eval();
      if (!dut->busy_o) return true;
      tick();
    }
    return false;
  }
};

// ---------------------------------------------------------------------------
// a µCPU-shaped response: the 12-byte header record it discards, the 4-byte
// {configuration_index, reserved} prefix, then COPY_BUFFER's 32-bit word pairs
// ---------------------------------------------------------------------------
static uint32_t build(H& h, uint32_t desc_len, uint32_t seed) {
  h.write(0, 0xC0FFEE00u, 0xF);                    // BUILD_HEADER, discarded
  h.write(4, 0xDEADBEEFu, 0xF);
  h.write(8, 0x12340000u, 0xF);
  h.write(12, 0x0000u, 0x3);                       // configuration_index
  h.write(14, 0x0000u, 0x3);                       // reserved
  uint32_t cur = 16;
  for (uint32_t off = 0; off < desc_len; off += 8) {
    h.write(cur, seed + off * 0x01010101u, 0xF);
    h.write(cur + 4, ~(seed + off * 0x01010101u), 0xF);
    cur += 8;
  }
  return 4 + desc_len;                             // emitted payload bytes
}

// ---- the suite ----------------------------------------------------------
// One object owns the model, both independent models and the tally, so every
// phase below is a named member function rather than another stretch of a
// `main` nobody can scope (Core Guidelines I.2, F.3).
namespace {
class RespBufSuite {
 public:
  int run();

 private:
  void reset_leaves_the_buffer_idle();
  void a_whole_response_round_trips_through_main_memory();
  void the_header_record_is_dropped_not_written();
  void a_field_straddling_a_lane_boundary_survives();
  void a_backward_status_patch_keeps_both_passes();
  void the_write_face_is_flow_controlled();
  void latency_is_not_a_correctness_parameter();
  void the_read_burst_paces_itself_against_a_lazy_builder();
  void unread_beats_are_drained_never_left_on_the_bridge();
  void a_response_with_no_payload_costs_no_read_burst();
  void a_tied_off_master_degrades_never_hangs();
  void it_heals_on_the_next_response_with_no_reset();
  void a_write_error_voids_the_response();
  void a_read_error_voids_the_response_too();
  void a_byte_past_the_capacity_is_dropped_never_wrapped();
  void back_to_back_responses_do_not_bleed_into_each_other();

  const milan::tb::Model<VKL_aecp_resp_buf> model;
  VKL_aecp_resp_buf* const dut = model.get();
  H h{dut};
  int checks = 0;
  int fails = 0;
};
}  // namespace

void RespBufSuite::reset_leaves_the_buffer_idle() {
  h.reset();

  CHECK(dut->busy_o == 0, "idle after reset");
  CHECK(dut->err_o == 0, "no fault after reset");
  CHECK(dut->rd_valid_o == 0, "no byte offered before a response exists");
}

// ---- R1: a whole response round-trips through main memory -------------
void RespBufSuite::a_whole_response_round_trips_through_main_memory() {
  h.open();
  uint32_t pld = build(h, 80, 0x11223344u);
  h.seal(pld);
  CHECK(h.stream(pld), "R1: the payload stream stopped after %zu of %u bytes",
        h.got.size(), pld);
  bool ok = true;
  for (uint32_t i = 0; i < pld && ok; ++i)
    if (h.got[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R1: a streamed byte disagrees with the contract image");
  ok = true;
  for (uint32_t i = 0; i < RESP_BYTES && ok; ++i)
    if (h.mem.b[i] != h.ref.b[i]) ok = false;
  CHECK(ok, "R1: the memory image disagrees with the contract image");
  CHECK(h.mem.bursts == 1, "R1: %llu read bursts, want 1",
        static_cast<unsigned long long>(h.mem.bursts));
  // lanes 1 .. (11 + bytes written) >> 3
  uint64_t want_lanes = (11 + 4 + 80) >> 3;
  CHECK(h.mem.writes == want_lanes, "R1: %llu lane writes, want %llu",
        static_cast<unsigned long long>(h.mem.writes),
        static_cast<unsigned long long>(want_lanes));
  CHECK(dut->dbg_lane_wr_o == want_lanes,
        "R1: the block counted %u lane writes, memory saw %llu",
        static_cast<unsigned>(dut->dbg_lane_wr_o),
        static_cast<unsigned long long>(want_lanes));
  CHECK(dut->err_o == 0, "R1: a clean round trip reported a fault");
}

// ---- R2: the header record is dropped, not written --------------------
// bytes 0..11 have no reader (06 §8), and bytes 8..11 share a lane with
// byte 12 — a buffer that wrote them would corrupt nothing today and
// everything the day the lane is read back with a full strobe
void RespBufSuite::the_header_record_is_dropped_not_written() {
  CHECK(h.mem.b[0] == POISON && h.mem.b[7] == POISON,
        "R2: the discarded header record reached memory");
  CHECK(h.mem.b[8] == POISON && h.mem.b[9] == POISON &&
        h.mem.b[10] == POISON && h.mem.b[11] == POISON,
        "R2: bytes 8..11 share lane 1 with byte 12 and were clobbered "
        "(%02x %02x %02x %02x)", h.mem.b[8], h.mem.b[9], h.mem.b[10],
        h.mem.b[11]);
  CHECK(dut->dbg_drop_o == 12, "R2: %u bytes dropped, want 12",
        static_cast<unsigned>(dut->dbg_drop_o));
}

// ---- R3: a field that STRADDLES a lane boundary -----------------------
// BUILD_FIELD writes 1/2/4 bytes at any cursor, so a 4-byte field can span
// two lanes. The buffer absorbs a write one byte per cycle precisely so
// that case needs no special arm; prove the bytes land on both sides.
void RespBufSuite::a_field_straddling_a_lane_boundary_survives() {
  h.open();
  h.write(12, 0xAABBCCDDu, 0xF);
  h.write(16, 0x01u, 0x1);                       // a byte field at 16
  h.write(17, 0x2233u, 0x3);                     // a word at 17
  h.write(19, 0x44556677u, 0xF);                 // 19..22: crosses lane 2/3
  h.write(23, 0x8899AABBu, 0xF);                 // 23..26: crosses again
  h.seal(15);                                    // bytes 12..26
  CHECK(h.stream(15), "R3: the straddling response stopped short");
  bool ok = h.got.size() == 15;
  for (uint32_t i = 0; i < 15 && ok; ++i)
    if (h.got[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R3: a straddling field is not byte-exact");
  CHECK(h.mem.b[19] == 0x44 && h.mem.b[22] == 0x77,
        "R3: the 19..22 field did not survive the lane it crosses");
  CHECK(h.mem.b[23] == 0x88 && h.mem.b[26] == 0xBB,
        "R3: the 23..26 field did not survive the lane it crosses");
}

// ---- R3b: GET_DYNAMIC_INFO status patch may revisit an earlier lane --
// The getter writes its data after a placeholder record header. Once its
// status is known, the engine patches one byte in that earlier header and
// continues forward with the next record. Partial memory strobes must keep
// every byte from both passes.
void RespBufSuite::a_backward_status_patch_keeps_both_passes() {
  h.open();
  h.write(12, 0x00040000u, 0xF);                 // length + reserved
  h.write(16, 0x00000007u, 0xF);                 // status 0 + GET_CONFIG
  h.write(20, 0x00000000u, 0xF);                 // first record data
  h.write(24, 0x11223344u, 0xF);                 // force later-lane flush
  h.write(16, 0x02u, 0x1);                       // status patch: NO_SUCH
  h.write(28, 0x55667788u, 0xF);                 // resume forward
  h.seal(20);                                    // bytes 12..31
  CHECK(h.stream(20), "R3b: the patched response stopped short");
  bool ok = h.got.size() == 20;
  for (uint32_t i = 0; i < 20 && ok; ++i)
    if (h.got[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R3b: the backward status patch corrupted response bytes");
  CHECK(h.got.size() > 4 && h.got[4] == 0x02,
        "R3b: patched info_status is %02x, want 02",
        h.got.size() > 4 ? h.got[4] : 0xFF);
}

// ---- R4: the write face is FLOW CONTROLLED ----------------------------
// Every lane the write pattern closes is a memory round trip the µCPU has
// to be held for, and the block must not hold it for anything else. The
// property is measured against the MEMORY, not against a cycle count: the
// same eight writes over a bridge 30 clocks slower must cost the µCPU about
// 30 clocks more per lane it closes, and nothing else may change.
void RespBufSuite::the_write_face_is_flow_controlled() {
  auto burst8 = [&](int wlat) {
    h.mem.wlat = wlat;
    h.open();
    int held = 0;
    for (uint32_t a = 12; a < 44; a += 4)          // lanes 1..5, 4 crossings
      held += h.write(a, 0x11223344u + a, 0xF);
    return held;
  };
  int slow_held = 0;
  int fast_held = 0;
  int fast = burst8(10);
  h.seal(32);
  CHECK(h.stream(32), "R4: the fast-memory response stopped short");
  std::vector<uint8_t> fast_bytes = h.got;
  std::vector<uint8_t> fast_ref(h.ref.b.begin() + 12, h.ref.b.begin() + 44);
  fast_held = fast;

  int slow = burst8(40);
  h.seal(32);
  CHECK(h.stream(32), "R4: the slow-memory response stopped short");
  slow_held = slow;
  h.mem.wlat = kMemWriteLatency;

  CHECK(fast_held >= 4 * 10,
        "R4: 4 lane crossings at a 10-clock write cost only %d held cycles "
        "— the µCPU cannot have waited for the flushes", fast_held);
  CHECK(slow_held - fast_held >= 3 * 30,
        "R4: 30 clocks more per flush moved the µCPU stall by only %d "
        "cycles (%d -> %d)", slow_held - fast_held, fast_held, slow_held);
  CHECK(h.got == fast_bytes,
        "R4: harder back-pressure changed the bytes on the way out");
  CHECK(fast_bytes == fast_ref,
        "R4: the flow-controlled response is not byte-exact");
}

// ---- R5: latency is not a correctness parameter ------------------------
void RespBufSuite::latency_is_not_a_correctness_parameter() {
  std::vector<uint8_t> at_default;
  std::vector<uint8_t> at_slow;
  std::vector<uint8_t> at_fast;
  h.open();
  uint32_t pld = build(h, 48, 0x5A5A0000u);
  h.seal(pld);
  CHECK(h.stream(pld), "R5: default-latency run stopped short");
  at_default = h.got;

  h.mem.rlat = 0; h.mem.wlat = 1;
  h.open(); build(h, 48, 0x5A5A0000u); h.seal(pld);
  CHECK(h.stream(pld), "R5: fast-memory run stopped short");
  at_fast = h.got;

  h.mem.rlat = 71; h.mem.wlat = 61;
  h.open(); build(h, 48, 0x5A5A0000u); h.seal(pld);
  CHECK(h.stream(pld), "R5: slow-memory run stopped short");
  at_slow = h.got;
  h.mem.rlat = kMemReadLatency; h.mem.wlat = kMemWriteLatency;

  CHECK(at_default == at_fast && at_default == at_slow,
        "R5: the payload changed with memory latency");
  CHECK(at_default.size() == pld, "R5: %zu bytes, want %u",
        at_default.size(), pld);
}

// ---- R6: the read burst paces itself against a lazy builder ------------
// rsp_ready is real back-pressure: a builder that takes one byte every few
// cycles must still get every byte, in order, exactly once
void RespBufSuite::the_read_burst_paces_itself_against_a_lazy_builder() {
  h.open();
  uint32_t pld = build(h, 40, 0x0F0F0000u);
  h.seal(pld);
  std::vector<uint8_t> slow;
  for (int i = 0; i < kStreamGuard && slow.size() < pld; ++i) {
    dut->eval();
    if (dut->rd_valid_o) {
      slow.push_back(uint8_t(dut->rd_data_o));
      dut->rd_take_i = 1; h.tick(); dut->rd_take_i = 0;
      h.idle(5);                                 // a builder in no hurry
    } else {
      h.tick();
    }
  }
  bool ok = slow.size() == pld;
  for (uint32_t i = 0; i < pld && ok; ++i)
    if (slow[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R6: a slow builder did not get the payload byte-exact");
  CHECK(h.wait_idle(), "R6: the burst never drained");
  CHECK(dut->err_o == 0, "R6: pacing tripped the watchdog");
}

// ---- R7: unread beats are DRAINED, never left on the bridge ------------
// the last lane usually carries bytes past the emitted length; the bridge
// must not be left holding them
void RespBufSuite::unread_beats_are_drained_never_left_on_the_bridge() {
  h.open();
  build(h, 40, 0x1234u);                          // writes 4 + 40 bytes
  h.seal(20);                                     // emit only 20 of them
  CHECK(h.stream(20), "R7: the truncated response stopped short");
  CHECK(h.wait_idle(), "R7: the unread part of the burst was never drained");
  CHECK(h.mem.rbusy == false, "R7: the bridge is still holding a beat");
  CHECK(dut->err_o == 0, "R7: draining tripped the watchdog");
}

// ---- R8: a response with NO payload costs no read burst ----------------
void RespBufSuite::a_response_with_no_payload_costs_no_read_burst() {
  h.open();
  uint64_t b0 = h.mem.bursts;
  h.write(0, 0x1u, 0xF);
  h.seal(0);
  h.idle(200);
  CHECK(h.mem.bursts == b0, "R8: a zero-length seal issued a read burst");
  CHECK(dut->rd_valid_o == 0, "R8: a zero-length response offered a byte");
  CHECK(dut->err_o == 0, "R8: a zero-length response faulted");
}

// ---- R9: a TIED-OFF master degrades, never hangs -----------------------
void RespBufSuite::a_tied_off_master_degrades_never_hangs() {
  h.open();
  h.mem.off = true;
  h.write(12, 0x11223344u, 0xF);
  // the flush can never complete: the write face must go permanently ready
  // rather than park the µCPU on a dead bridge
  int held = 0;
  for (uint32_t a = 16; a < 40; a += 4)
    held += h.write(a, 0x55667788u, 0xF, 8 * TMO);
  CHECK(held < 8 * TMO,
        "R9: the write face never released the µCPU (%d cycles)", held);
  CHECK(dut->err_o == 1, "R9: a dead bridge raised no fault");
  CHECK(dut->dbg_fault_o == 1, "R9: fault %u, want 1 (write watchdog)",
        static_cast<unsigned>(dut->dbg_fault_o));
  h.seal(16);
  h.idle(4 * TMO);
  CHECK(dut->rd_valid_o == 0, "R9: a void response offered a byte");
  CHECK(dut->busy_o == 0, "R9: the block is still asking a dead bridge");
  h.mem.off = false;
}

// ---- R10: it heals on the next response, with no reset -----------------
void RespBufSuite::it_heals_on_the_next_response_with_no_reset() {
  h.open();
  CHECK(dut->err_o == 0, "R10: the fault survived the re-arm");
  uint32_t pld = build(h, 64, 0x77880000u);
  h.seal(pld);
  CHECK(h.stream(pld), "R10: the response after a fault stopped short");
  bool ok = true;
  for (uint32_t i = 0; i < pld && ok; ++i)
    if (h.got[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R10: the response after a fault is not byte-exact");
  CHECK(dut->err_o == 0, "R10: a clean response after a fault reported one");
}

// ---- R11: a bridge that reports a WRITE error voids the response -------
void RespBufSuite::a_write_error_voids_the_response() {
  h.open();
  h.mem.werr = true;
  h.write(12, 0x11223344u, 0xF);
  h.write(16, 0x55667788u, 0xF);                 // flushes lane 1 -> error
  h.write(20, 0x99AABBCCu, 0xF);
  h.idle(4 * TMO);
  h.mem.werr = false;
  CHECK(dut->err_o == 1, "R11: a write error raised no fault");
  CHECK(dut->dbg_fault_o == 2, "R11: fault %u, want 2 (write error)",
        static_cast<unsigned>(dut->dbg_fault_o));
  h.seal(16);
  h.idle(4 * TMO);
  CHECK(dut->rd_valid_o == 0, "R11: a voided response offered a byte");
}

// ---- R12: a bridge that reports a READ error voids it too --------------
void RespBufSuite::a_read_error_voids_the_response_too() {
  h.open();
  uint32_t pld = build(h, 32, 0x9999u);
  h.mem.rerr_at = 1;                             // fail the second beat
  h.seal(pld);
  bool done = h.stream(pld, 4 * TMO);
  h.mem.rerr_at = -1;
  CHECK(!done, "R12: a read error still produced a whole payload");
  CHECK(dut->err_o == 1, "R12: a read error raised no fault");
  CHECK(dut->dbg_fault_o == 4, "R12: fault %u, want 4 (read error)",
        static_cast<unsigned>(dut->dbg_fault_o));
  CHECK(h.got.size() > 0 && h.got.size() < pld,
        "R12: %zu bytes served before the error, want 1..%u",
        h.got.size(), pld - 1);
}

// ---- R13: a byte at or past the capacity is dropped, never wrapped -----
void RespBufSuite::a_byte_past_the_capacity_is_dropped_never_wrapped() {
  h.open();
  h.write(RESP_BYTES - 2, 0xAABBCCDDu, 0xF);     // half of it is past the end
  h.seal(0);
  h.idle(4 * TMO);
  CHECK(h.mem.b[0] == POISON && h.mem.b[8] == POISON,
        "R13: a write past the end wrapped to the start of the buffer");
  CHECK(dut->dbg_drop_o >= 2, "R13: %u bytes dropped, want at least 2",
        static_cast<unsigned>(dut->dbg_drop_o));
}

// ---- R14: back-to-back responses do not bleed into each other ----------
void RespBufSuite::back_to_back_responses_do_not_bleed_into_each_other() {
  h.open();
  uint32_t pld1 = build(h, 24, 0xA1A1A1A1u);
  h.seal(pld1);
  CHECK(h.stream(pld1), "R14: the first response stopped short");
  std::vector<uint8_t> first = h.got;
  std::vector<uint8_t> ref1(h.ref.b.begin() + 12, h.ref.b.begin() + 12 + pld1);

  h.open();
  uint32_t pld2 = build(h, 8, 0xB2B2B2B2u);      // a much SHORTER one
  h.seal(pld2);
  CHECK(h.stream(pld2), "R14: the second response stopped short");
  bool ok = h.got.size() == pld2;
  for (uint32_t i = 0; i < pld2 && ok; ++i)
    if (h.got[i] != h.ref.b[12 + i]) ok = false;
  CHECK(ok, "R14: the short response carries the long one's bytes");
  CHECK(first == ref1, "R14: the first response was not byte-exact");
  CHECK(h.got != first, "R14: two different responses came out identical");
}

int RespBufSuite::run() {
  reset_leaves_the_buffer_idle();
  a_whole_response_round_trips_through_main_memory();
  the_header_record_is_dropped_not_written();
  a_field_straddling_a_lane_boundary_survives();
  a_backward_status_patch_keeps_both_passes();
  the_write_face_is_flow_controlled();
  latency_is_not_a_correctness_parameter();
  the_read_burst_paces_itself_against_a_lazy_builder();
  unread_beats_are_drained_never_left_on_the_bridge();
  a_response_with_no_payload_costs_no_read_burst();
  a_tied_off_master_degrades_never_hangs();
  it_heals_on_the_next_response_with_no_reset();
  a_write_error_voids_the_response();
  a_read_error_voids_the_response_too();
  a_byte_past_the_capacity_is_dropped_never_wrapped();
  back_to_back_responses_do_not_bleed_into_each_other();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  RespBufSuite suite;
  return suite.run();
}

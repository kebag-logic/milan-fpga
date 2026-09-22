// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_aecp_dyn_state — the AECP dynamic-state store.
//
// WHAT THIS SUITE PROVES. That the store the whole SET_* family is about to
// be built on keeps a setting, keeps it PER DESCRIPTOR, tells a reader
// whether a setting exists at all, and refuses an index the shape does not
// have. Every check drives the real state port with the same handshake the
// microCPU drives (request held until ready/rvalid), because a store that
// only works when poked in a convenient order is a store that will fail in
// microcode.
//
// THE ONE THAT MATTERS MOST is the VALID FLAG (region 0x2). It is what lets a
// GET fall back to the descriptor image, so "unwritten reads back invalid"
// and "written reads back valid" are the two halves of the contract that
// every GET_* microprogram will branch on. A store that answered a plausible
// zero with the flag set would make every GET report a setting nobody made.
//
// Clauses: Milan v1.2 5.3.5.1 (sampling rate), 5.3.7.1/5.3.8.1 (formats),
// 5.3.7.6 (presentation offset), 5.3.8.7 (started/stopped), 5.3.11.1 (clock
// source), 5.3.12 (IDENTIFY, volatile, 0 after reset), 5.4.2.5 (current
// configuration).
#include <cstdio>
#include <cstdint>
#include "VKL_aecp_dyn_state.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// field selectors — mirror KL_aecp_dyn_state.sv's SEL_*_C.  Plain integers,
// not an enum class: they ride the address arithmetic below and every use
// site would otherwise need a cast back out.
constexpr int SEL_CFG     = 0;
constexpr int SEL_RATE    = 1;
constexpr int SEL_CLKSRC  = 2;
constexpr int SEL_FMTIN   = 3;
constexpr int SEL_FMTOUT  = 4;
constexpr int SEL_PTOFF   = 5;
constexpr int SEL_RETIRED = 6;
constexpr int SEL_IDENT   = 7;
// regions
constexpr uint32_t RGN_DYN  = 0x1u << 16;   // the value
constexpr uint32_t RGN_DYNV = 0x2u << 16;   // the valid flag

//! clocks the reset is held low for, and the bound on a request/ready
//! handshake — the DUT answers in one or two clocks, so the guard only ever
//! stops a hung port from spinning forever.
constexpr int kResetTicks = 4;
constexpr int kHandshakeGuard = 32;

#ifdef SHAPE_1x1
constexpr int NSI = 1;
constexpr int NSO = 1;
constexpr const char* SHAPE = "1x1";
#else
constexpr int NSI = 2;
constexpr int NSO = 2;
constexpr const char* SHAPE = "2x2";
#endif

//! address = region | selector<<3.  The DESCRIPTOR INDEX does not ride the
//! address — it is a separate port, which is the whole point of the design.
static uint32_t addr(uint32_t rgn, int sel) {
  return rgn | (static_cast<uint32_t>(sel) << 3);
}

namespace {

class DynStateHarness {
 public:
  int run();

 private:
  void tick();
  void reset();
  void wr(int sel, uint16_t index, uint64_t val);
  uint64_t rd(uint32_t rgn, int sel, uint16_t index);

  void read_everything_invalid_out_of_reset();
  void keep_a_write_and_set_its_valid_flag();
  void keep_settings_per_descriptor();
  void refuse_an_index_the_shape_lacks();
  void mark_dirty_only_for_persisted_fields();
  void publish_the_store_on_the_live_face();
  void keep_selector_six_retired();
  void leave_the_store_untouched_by_reads();

  VKL_aecp_dyn_state* d = nullptr;
  long checks = 0;
  long fails = 0;
};

void DynStateHarness::tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }

void DynStateHarness::reset() {
  d->rst_n = 0; d->st_req_i = 0; d->st_we_i = 0; d->st_addr_i = 0;
  d->st_wdata_i = 0; d->desc_index_i = 0;
  for (int i = 0; i < kResetTicks; i++) tick();
  d->rst_n = 1;
  tick();
}

void DynStateHarness::wr(int sel, uint16_t index, uint64_t val) {
  d->st_addr_i    = addr(RGN_DYN, sel);
  d->desc_index_i = index;
  d->st_wdata_i   = val;
  d->st_we_i      = 1;
  d->st_req_i     = 1;
  // hold the request until ready, exactly as the microCPU does
  int guard = kHandshakeGuard;
  while (guard-- > 0) { d->eval(); if (d->st_ready_o) break; tick(); }
  tick();
  d->st_req_i = 0; d->st_we_i = 0;
  d->eval();
}

uint64_t DynStateHarness::rd(uint32_t rgn, int sel, uint16_t index) {
  d->st_addr_i    = addr(rgn, sel);
  d->desc_index_i = index;
  d->st_we_i      = 0;
  d->st_req_i     = 1;
  uint64_t got = 0;
  int guard = kHandshakeGuard;
  while (guard-- > 0) {
    tick();
    d->eval();
    if (d->st_rvalid_o) { got = d->st_rdata_o; break; }
  }
  d->st_req_i = 0;
  d->eval();
  return got;
}

// ---- A: everything reads INVALID out of reset -------------------------
// The image is the authority until a controller says otherwise, so every
// valid flag must be clear and every value zero. A store that came up
// "valid" would make every GET report a setting nobody made.
void DynStateHarness::read_everything_invalid_out_of_reset() {
  const int sels[] = {SEL_CFG, SEL_RATE, SEL_CLKSRC, SEL_FMTIN,
                      SEL_FMTOUT, SEL_PTOFF, SEL_RETIRED, SEL_IDENT};
  for (int s : sels) {
    CHECK(rd(RGN_DYNV, s, 0) == 0,
          "A: selector %d reads VALID out of reset", s);
    CHECK(rd(RGN_DYN, s, 0) == 0,
          "A: selector %d reads non-zero out of reset", s);
  }
  CHECK(d->identify_o == 0,
        "A: Milan 5.3.12 makes IDENTIFY 0 after reset, got %u",
        static_cast<unsigned>(d->identify_o));
  CHECK(d->dirty_o == 0, "A: dirty is clear before any write");
}

// ---- B: a write is kept, and the flag goes valid -----------------------
void DynStateHarness::keep_a_write_and_set_its_valid_flag() {
  wr(SEL_RATE, 0, 96000);
  CHECK(rd(RGN_DYN,  SEL_RATE, 0) == 96000,
        "B: sampling rate did not read back, got %llu",
        static_cast<unsigned long long>(rd(RGN_DYN, SEL_RATE, 0)));
  CHECK(rd(RGN_DYNV, SEL_RATE, 0) == 1,
        "B: the valid flag did not set on a write");
}

// ---- C: settings are PER DESCRIPTOR ------------------------------------
// The bug this catches is the one the design exists to avoid: an address
// that carries the field but not the index, so every stream shares one row.
void DynStateHarness::keep_settings_per_descriptor() {
  if (NSI >= 2) {
    wr(SEL_FMTIN, 0, 0x0205022000406000ull);   // 48 kHz 1 ch  (Milan Table 6.2)
    wr(SEL_FMTIN, 1, 0x0205022002006000ull);   // 48 kHz 8 ch
    CHECK(rd(RGN_DYN, SEL_FMTIN, 0) == 0x0205022000406000ull,
          "C: input 0's format was clobbered by input 1's write");
    CHECK(rd(RGN_DYN, SEL_FMTIN, 1) == 0x0205022002006000ull,
          "C: input 1's format did not read back");
    //! ...and the flags are per descriptor too
    wr(SEL_PTOFF, 1, 250000);
    CHECK(rd(RGN_DYNV, SEL_PTOFF, 1) == 1, "C: output 1's offset is valid");
    CHECK(rd(RGN_DYNV, SEL_PTOFF, 0) == 0,
          "C: writing output 1 must NOT validate output 0");
  }
}

// ---- D: an index the shape does not have is REFUSED --------------------
// Milan sizes these arrays by the entity model. An index past the end must
// read invalid and its write must be dropped and counted — never aliased
// onto row zero, which would silently set the wrong stream's format.
void DynStateHarness::refuse_an_index_the_shape_lacks() {
  const uint16_t oob = static_cast<uint16_t>(NSI + 4);
  const uint16_t oob0 = d->dbg_oob_o;
  wr(SEL_FMTIN, oob, 0xDEADBEEFCAFEF00Dull);
  CHECK(d->dbg_oob_o == static_cast<uint16_t>(oob0 + 1),
        "D: an out-of-range write was not counted (%u -> %u)",
        static_cast<unsigned>(oob0), static_cast<unsigned>(d->dbg_oob_o));
  CHECK(rd(RGN_DYNV, SEL_FMTIN, oob) == 0,
        "D: an out-of-range read claims to be valid");
  CHECK(rd(RGN_DYN, SEL_FMTIN, oob) == 0,
        "D: an out-of-range read returned data");
  CHECK(rd(RGN_DYN, SEL_FMTIN, 0) == 0x0205022000406000ull ||
        NSI < 2,
        "D: the out-of-range write ALIASED onto row 0");
}

// ---- E: dirty marks the persisted set, and only it ---------------------
// Milan 5.3.13 & friends make these fields non-volatile; 5.3.12 makes the
// IDENTIFY value volatile. Raising dirty for IDENTIFY would commit flash
// every time a front panel blinked.
void DynStateHarness::mark_dirty_only_for_persisted_fields() {
  reset();
  CHECK(d->dirty_o == 0, "E: dirty is clear after reset");
  wr(SEL_IDENT, 0, 255);
  CHECK(d->identify_o == 255,
        "E: the IDENTIFY value did not reach its face, got %u",
        static_cast<unsigned>(d->identify_o));
  CHECK(d->dirty_o == 0,
        "E: a volatile IDENTIFY write marked the store dirty");
  wr(SEL_CLKSRC, 0, 2);
  CHECK(d->dirty_o == 1,
        "E: a persisted clock-source write did NOT mark the store dirty");
}

// ---- F: the live face tracks the store ---------------------------------
// These are the ports the fabric acts on, so a setting that reads back
// over AECP but never reaches the face would be a setting in name only.
void DynStateHarness::publish_the_store_on_the_live_face() {
  reset();
  wr(SEL_CFG, 0, 3);
  CHECK(d->cur_config_o == 3,
        "F: current_configuration face is %u",
        static_cast<unsigned>(d->cur_config_o));
  wr(SEL_CLKSRC, 0, 1);
  CHECK(d->clk_src_index_o == 1,
        "F: clock_source_index face is %u",
        static_cast<unsigned>(d->clk_src_index_o));
  CHECK(d->pt_offset_v_o == 0,
        "F: no presentation-offset row claims valid before a write");
  wr(SEL_PTOFF, 0, 2000000);
  CHECK(d->pt_offset_v_o == 0x1,
        "F: exactly row 0's presentation-offset valid rose, got 0x%X",
        static_cast<unsigned>(d->pt_offset_v_o));
#ifdef SHAPE_1x1
  // one row per direction: every published face is a plain scalar
  CHECK(d->pt_offset_o == 2000000,
        "F: presentation-offset row 0 face is %u",
        static_cast<unsigned>(d->pt_offset_o));
  wr(SEL_FMTIN, 0, 0x0205022000406000ull);
  CHECK(d->fmt_in_v_o == 0x1 && d->fmt_in_o == 0x0205022000406000ull,
        "F: format-in row 0 face holds the written qword (v=0x%X)",
        static_cast<unsigned>(d->fmt_in_v_o));
  wr(SEL_FMTOUT, 0, 0x0205022001406000ull);
  CHECK(d->fmt_out_v_o == 0x1 && d->fmt_out_o == 0x0205022001406000ull,
        "F: format-out row 0 face holds the written qword (v=0x%X)",
        static_cast<unsigned>(d->fmt_out_v_o));
#else
  CHECK(static_cast<uint32_t>(d->pt_offset_o) == 2000000,
        "F: presentation-offset row 0 face is %u",
        static_cast<unsigned>(static_cast<uint32_t>(d->pt_offset_o)));
  // the per-row publication must keep rows apart: row 1's value and valid
  // land beside row 0's, disturbing neither
  wr(SEL_PTOFF, 1, 750000);
  CHECK(static_cast<uint32_t>(d->pt_offset_o >> 32) == 750000
            && static_cast<uint32_t>(d->pt_offset_o) == 2000000
            && d->pt_offset_v_o == 0x3,
        "F: presentation-offset row 1 published beside row 0 (v=0x%X)",
        static_cast<unsigned>(d->pt_offset_v_o));
  // the format faces publish the same way, 64 bits per row: row 1 lives
  // in words 2..3 of the flat vector
  wr(SEL_FMTIN, 1, 0x0205022000406000ull);
  CHECK(d->fmt_in_v_o == 0x2
            && d->fmt_in_o.at(2) == 0x00406000u
            && d->fmt_in_o.at(3) == 0x02050220u,
        "F: format-in row 1 face holds the written qword (v=0x%X)",
        static_cast<unsigned>(d->fmt_in_v_o));
  wr(SEL_FMTOUT, 1, 0x0205022001406000ull);
  CHECK(d->fmt_out_v_o == 0x2
            && d->fmt_out_o.at(2) == 0x01406000u
            && d->fmt_out_o.at(3) == 0x02050220u,
        "F: format-out row 1 face holds the written qword (v=0x%X)",
        static_cast<unsigned>(d->fmt_out_v_o));
#endif
}

// ---- F2: selector 6 is RETIRED and cannot become a second source -------
// It used to hold started/stopped per Stream Input. Milan 5.3.8.7 makes
// that a property of the BINDING ("undefined when the Stream Input is not
// bound"), so it lives in the ACMP binding record, which is the only place
// with the lifecycle to clear it on unbind and restore it after a power
// cycle. A writable copy here would disagree with the record silently -
// both answer a plausible 0 or 1 and nothing says which is right.
//
// This is deliberately a test that the row is GONE rather than the absence
// of a test: a selector that owns no rows fails its range check, so the
// write is DROPPED AND COUNTED, and the read answers a clear valid flag.
// Without this, re-adding the field would turn the suite green again.
// (no reset() here: the counters below are read as deltas, and block G
//  downstream asserts on the configuration block F set)
void DynStateHarness::keep_selector_six_retired() {
  const uint16_t wr0  = d->dbg_writes_o;
  const uint16_t oob0 = d->dbg_oob_o;
  wr(SEL_RETIRED, 0, 1);
  CHECK(d->dbg_writes_o == wr0,
        "F2: a write to the retired selector was ACCEPTED (writes %u -> %u)",
        static_cast<unsigned>(wr0), static_cast<unsigned>(d->dbg_writes_o));
  CHECK(d->dbg_oob_o == static_cast<uint16_t>(oob0 + 1),
        "F2: the dropped write was not counted (oob %u -> %u)",
        static_cast<unsigned>(oob0), static_cast<unsigned>(d->dbg_oob_o));
  CHECK(rd(RGN_DYN, SEL_RETIRED, 0) == 0,
        "F2: the retired selector still reads a value back");
  CHECK(rd(RGN_DYNV, SEL_RETIRED, 0) == 0,
        "F2: the retired selector still reports itself valid");
  // ...and retiring it did not disturb the selector next to it
  wr(SEL_IDENT, 0, 0x5A);
  CHECK(d->identify_o == 0x5A,
        "F2: SEL_IDENT broke when selector 6 was retired (%u)",
        static_cast<unsigned>(d->identify_o));
}

// ---- G: a read never disturbs the store --------------------------------
// The valid-flag read happens on EVERY GET, so a read with side effects
// would corrupt state on the most common path in the system.
void DynStateHarness::leave_the_store_untouched_by_reads() {
  const uint16_t wr0 = d->dbg_writes_o;
  for (int i = 0; i < 4; i++) { rd(RGN_DYN, SEL_CFG, 0); rd(RGN_DYNV, SEL_CFG, 0); }
  CHECK(d->dbg_writes_o == wr0, "G: a read was counted as a write");
  CHECK(d->cur_config_o == 3, "G: a read changed current_configuration");
}

int DynStateHarness::run() {
  const milan::tb::Model<VKL_aecp_dyn_state> model;
  d = model.get();                  // the file's existing observing pointer
  reset();

  printf("== KL_aecp_dyn_state, shape %s ==\n", SHAPE);

  read_everything_invalid_out_of_reset();
  keep_a_write_and_set_its_valid_flag();
  keep_settings_per_descriptor();
  refuse_an_index_the_shape_lacks();
  mark_dirty_only_for_persisted_fields();
  publish_the_store_on_the_live_face();
  keep_selector_six_retired();
  leave_the_store_untouched_by_reads();

  //! NOT the canonical tally shape: this binary is ONE SHAPE of the suite,
  //! and run_suites.sh takes the LAST matching line, so a per-shape tally
  //! here would silently drop the other shape's checks from the total. The
  //! Makefile sums the two and prints the one canonical line.
  printf("[shape %s] %ld checks, %ld failures\n", SHAPE, checks, fails);
  FILE* acc = fopen("shape_tally.txt", "a");
  if (acc) { fprintf(acc, "%ld %ld\n", checks, fails); fclose(acc); }
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  DynStateHarness harness;
  return harness.run();
}

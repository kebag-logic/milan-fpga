// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Grades hdl/milan/KL_nvm_backend.sv, the device behind the processor's NVM
// port, against a BYTE-EXACT KLJ2 image (docs/design/SAVED_STATE_FASTCONNECT.md
// section 6.1) whose record offsets are produced independently by
//   scripts/check_nvm_record_space.py --emit-record-table
//
// Two implementations meet here and neither is allowed to define the answer:
//   * Python encodes the image and publishes ONLY {record_id, area offset,
//     framed length, payload length} plus the image's CRC-32.
//   * This file rebuilds every byte of that image from the record list and its
//     own F07.8 framing and CRC-16, then checks its CRC-32 against Python's.
//     A disagreement about ANY byte -- including where a record starts -- is a
//     CRC-32 mismatch before a single clock is driven.
//   * The RTL then has to find each record from the shape, the fixed group
//     bases and the firmware-loaded channel-map tables alone, and its answer is
//     graded against Python's offsets, through a model of the SoC's memory
//     bridge (protocol_processor_top's response-buffer contract: 64-bit
//     big-endian beats, one outstanding read burst, one outstanding
//     single-beat strobed write with a commit pulse).
//
// What it exists to catch:
//   * the two channel-map groups sharing ONE {prefix,length} table, so 0x60+k
//     and 0x70+k alias (an input port is 72 framed bytes and an output port
//     144 on the shipped 8x8 overlay);
//   * a group base advancing by a NOMINAL stride, although KLJ2 6.1
//     concatenates records with no padding;
//   * nvm_stale as a latch cleared only by reset with the published bit masked,
//     so a clean recovery republishes stale=1 on the next ordinary change;
//   * a READ served out of an image nobody validated, instead of blank flash.
// Each has a negative control (tb/verilator/nvm_backend/mutate.py) that MUST
// fail; the Makefile runs all four and reddens if any of them passes.

#include "Vnvm.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <set>
#include <string>
#include <vector>

constexpr size_t NOPOS = static_cast<size_t>(-1);

// The KLJ2 image is a fixed header, the record area, and a trailing CRC-32.
constexpr unsigned IMG_CRC_BYTES = 4;

namespace {

// ---- the two digests, both independent re-implementations -----------------
uint16_t crc16_ccitt(const uint8_t *d, size_t n) {
  uint16_t c = 0xFFFF;
  for (size_t i = 0; i < n; i++) {
    c ^= static_cast<uint16_t>(static_cast<uint16_t>(d[i]) << 8);
    for (int b = 0; b < 8; b++)
      c = (c & 0x8000) ? static_cast<uint16_t>((c << 1) ^ 0x1021)
                       : static_cast<uint16_t>(c << 1);
  }
  return c;
}

uint32_t crc32_ieee(const uint8_t *d, size_t n) {
  uint32_t c = 0xFFFFFFFFu;
  for (size_t i = 0; i < n; i++) {
    c ^= d[i];
    for (int b = 0; b < 8; b++)
      c = (c >> 1) ^
          (0xEDB88320u & static_cast<uint32_t>(-static_cast<int32_t>(c & 1)));
  }
  return ~c;
}

// ---- the fixture ----------------------------------------------------------
struct Rec {
  unsigned id;
  unsigned off;
  unsigned flen;
  unsigned plen;
  unsigned index;
  std::string group;
};

// The SoC bridge, modelled: one outstanding read burst of 64-bit beats
// carrying byte addr+n in bits [63-8n -: 8], one outstanding single-beat
// write with strobe bit n enabling byte n, committed by a one-cycle done pulse
// that is either STRICTLY LATER than the accept (the acknowledged bridge the
// SoC ships) or in the SAME cycle (a posted bridge, which the contract also
// allows and the RTL must accept).
struct Bridge {
  bool rd_busy = false;
  bool rd_present = false;
  uint32_t rd_addr = 0;
  int rd_lat = 0;
  bool wr_busy = false;
  bool wr_present = false;
  uint32_t wr_addr = 0;
  uint64_t wr_data = 0;
  uint8_t wr_strb = 0;
  int wr_lat = 0;
  bool posted = false;
  int latency = 3;
  unsigned reads = 0;
  unsigned writes = 0;
  std::set<uint32_t> poisoned;  // word addresses that answer err
};

// One graded run against one record table.
class NvmBackendHarness {
 public:
  int run(int argc, char **argv);

 private:
  void check(bool ok, const char *fmt, ...);
  void load_table(const char *path);
  void build_area();
  void prove_byte_exact();
  uint64_t word_at(uint32_t addr) const;
  void apply_write(uint32_t addr, uint64_t data, uint8_t strb);
  void settle();
  void posedge();
  void tick();
  void csr_write(unsigned addr, uint32_t data);
  uint32_t csr_read(unsigned addr);
  void reset_dut();
  void configure_image();
  void set_valid(bool valid, unsigned verdict);
  bool dev_cmd(int op, unsigned region, unsigned offset, unsigned len,
               std::vector<uint8_t> *rd, const uint8_t *wr);
  void program_map_tables();
  void test_unconfigured();
  void test_validity_gate();
  void test_regions();
  void test_writes_and_erase(bool posted);
  void test_bounds_and_errors();
  void test_status_word();
  void hb();
  void commit_ack(uint32_t cap_id);
  void commit_start();
  void pend(int level);
  void boot_load();
  void close_record();
  uint32_t capture();
  void idle_ms(int n);
  void expect_bits(const char *what, int b, int d, int s);
  void expect_pend(const char *what, int want);
  void test_stale();
  void test_stale_deadlines();
  void test_ownership();

  static constexpr uint32_t IMG_BASE = 0x40000000u;
  static constexpr int RESET_CYCLES = 8;
  static constexpr int CMD_GUARD_CYCLES = 400000;
  // Section 9.2. CLK_HZ_P is 10 kHz in this build, so a "millisecond" is 10
  // clocks and T_ALIVE_MS_P is 4.
  static constexpr int MS = 10;
  // R_STAT bit positions of the backend's status word (KL_nvm_backend.sv)
  static constexpr uint32_t STAT_BACKED = 1u << 6;
  static constexpr uint32_t STAT_IMG_VALID = 1u << 7;
  static constexpr uint32_t STAT_DIRTY = 1u << 8;
  static constexpr uint32_t STAT_STALE = 1u << 9;
  static constexpr uint32_t STAT_IMG_CFG = 1u << 5;
  // the snapshot-ownership contract's own bits
  // (docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 5.1)
  static constexpr uint32_t STAT_LOAD_ACC = 1u << 2;
  static constexpr uint32_t STAT_LOAD_PEND = 1u << 3;
  static constexpr uint32_t STAT_RELOAD_REF = 1u << 11;
  static constexpr uint32_t STAT_CAP_OPEN = 1u << 16;
  static constexpr uint32_t STAT_ATTESTED = 1u << 19;
  static constexpr uint32_t STAT_ACK_REF = 1u << 20;
  static constexpr uint32_t STAT_ARM_REF = 1u << 21;
  static constexpr uint32_t STAT_PEND = 1u << 22;
  static constexpr uint32_t STAT_UNRES = 1u << 23;
  static constexpr uint32_t STAT_TAG = 0xC3u << 24;
  static constexpr unsigned R_CAPID = 5;
  static constexpr unsigned R_OWN0 = 8;

  //! heartbeat the backend from inside a long device-face command: see
  //! dev_cmd(). Off by default, so every existing case is unchanged.
  bool hb_during_cmd_ = false;
  int checks_ = 0;
  int fails_ = 0;

  std::vector<Rec> recs_;
  std::string shape_;
  unsigned layout_ = 0;
  unsigned hdrbytes_ = 0;
  unsigned imglen_ = 0;
  unsigned nrec_ = 0;
  uint32_t crc32_ = 0;
  unsigned area_len_ = 0;

  // The record area, rebuilt byte for byte from the record list alone.
  std::vector<uint8_t> area_;

  Vnvm *dut_ = nullptr;
  std::vector<uint8_t> mem_;
  Bridge br_;
  bool watch_stale_ = false;
  int bad_pair_ = 0;
};

void NvmBackendHarness::check(bool ok, const char *fmt, ...) {
  checks_++;
  if (ok) return;
  fails_++;
  va_list ap;
  va_start(ap, fmt);
  fputs("FAIL: ", stdout);
  vprintf(fmt, ap);
  fputc('\n', stdout);
  va_end(ap);
}

void NvmBackendHarness::load_table(const char *path) {
  FILE *f = fopen(path, "r");
  if (!f) {
    printf("FAIL: cannot open record table %s\n", path);
    exit(2);
  }
  char line[512];
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    char k[64];
    char g[64];
    char sh[128];
    unsigned id;
    unsigned off;
    unsigned flen;
    unsigned plen;
    unsigned idx;
    unsigned v;
    if (sscanf(line, "rec 0x%x %u %u %u %63s %u", &id, &off, &flen, &plen, g,
               &idx) == 6) {
      Rec r;
      r.id = id;
      r.off = off;
      r.flen = flen;
      r.plen = plen;
      r.index = idx;
      r.group = g;
      recs_.push_back(r);
    } else if (sscanf(line, "crc32 0x%x", &v) == 1) {
      crc32_ = v;
    } else if (sscanf(line, "shape %127s", sh) == 1) {
      shape_ = sh;
    } else if (sscanf(line, "%63s %u", k, &v) == 2) {
      if (!strcmp(k, "layout")) layout_ = v;
      else if (!strcmp(k, "hdrbytes")) hdrbytes_ = v;
      else if (!strcmp(k, "imglen")) imglen_ = v;
      else if (!strcmp(k, "nrec")) nrec_ = v;
    }
  }
  fclose(f);
}

void NvmBackendHarness::build_area() {
  area_len_ = imglen_ - hdrbytes_ - IMG_CRC_BYTES;
  area_.assign(area_len_, 0);
  for (size_t n = 0; n < recs_.size(); n++) {
    const Rec &r = recs_[n];
    std::vector<uint8_t> fr(r.flen, 0);
    fr[0] = 0x17;
    fr[1] = 0x22;
    fr[2] = static_cast<uint8_t>(layout_);
    fr[3] = static_cast<uint8_t>(r.id);
    fr[4] = static_cast<uint8_t>(r.plen >> 8);
    fr[5] = static_cast<uint8_t>(r.plen & 0xFF);
    for (unsigned j = 0; j < r.plen; j++)
      fr[8 + j] = static_cast<uint8_t>((r.id * 131u + j * 17u) & 0xFF);
    // the crc16 accumulates the header WITHOUT its own two bytes, then the
    // payload, as one stream -- the donor's crc16_f() in KL_acmp_nvm_shadow
    std::vector<uint8_t> s;
    s.insert(s.end(), fr.begin(), fr.begin() + 6);
    s.insert(s.end(), fr.begin() + 8, fr.begin() + 8 + r.plen);
    uint16_t c = crc16_ccitt(s.data(), s.size());
    fr[6] = static_cast<uint8_t>(c >> 8);
    fr[7] = static_cast<uint8_t>(c & 0xFF);
    memcpy(&area_[r.off], fr.data(), r.flen);
  }
}

void NvmBackendHarness::prove_byte_exact() {
  std::vector<uint8_t> img;
  // The KLJ2 header is ten little-endian 32-bit words ahead of the record area.
  constexpr int HDR_WORDS = 10;
  const uint32_t hdr[HDR_WORDS] = {0x324A4C4Bu, 0x00020000u, 7u,
                                   nrec_,       imglen_,     0x44556677u,
                                   0x00112233u, 0xCCDDEEFFu, 0x8899AABBu,
                                   layout_};
  for (int w = 0; w < HDR_WORDS; w++)
    for (int b = 0; b < 4; b++)
      img.push_back(static_cast<uint8_t>(hdr[w] >> (8 * b)));
  img.insert(img.end(), area_.begin(), area_.end());
  uint32_t c = crc32_ieee(img.data(), img.size());
  for (int b = 0; b < 4; b++)
    img.push_back(static_cast<uint8_t>(c >> (8 * b)));

  check(img.size() == static_cast<size_t>(imglen_),
        "%s: the rebuilt image is %zu B, the fixture says %u", shape_.c_str(),
        img.size(), imglen_);
  check(c == crc32_,
        "%s: the rebuilt image CRC-32 is 0x%08X, the encoder's is 0x%08X -- "
        "this C++ and scripts/check_nvm_record_space.py do not agree on the "
        "bytes of the image, so nothing measured against it means anything",
        shape_.c_str(), c, crc32_);
}

// ---------------------------------------------------------------------------
// The bridge model. `settle` drives this cycle's inputs from the model's
// state alone (no combinational path from a DUT output to these inputs exists
// on the DUT side either, so one eval is enough); `posedge` advances the model
// on the handshakes visible in that settled cycle, then clocks the DUT.
uint64_t NvmBackendHarness::word_at(uint32_t addr) const {
  uint64_t w = 0;
  for (unsigned n = 0; n < 8; n++) {
    uint32_t a = addr - IMG_BASE + n;
    uint8_t b = a < mem_.size() ? mem_[a] : 0xEE;
    w |= static_cast<uint64_t>(b) << (56 - 8 * n);  // byte addr+n in [63-8n -: 8]
  }
  return w;
}

void NvmBackendHarness::apply_write(uint32_t addr, uint64_t data,
                                    uint8_t strb) {
  for (unsigned n = 0; n < 8; n++) {
    if (!(strb & (1u << n))) continue;  // a zero-strobe byte is NOT modified
    uint32_t a = addr - IMG_BASE + n;
    if (a < mem_.size())
      mem_[a] = static_cast<uint8_t>(data >> (56 - 8 * n));
  }
}

void NvmBackendHarness::settle() {
  dut_->eval();
  const uint32_t rword = br_.rd_addr & ~7u;
  dut_->mem_req_ready_i = br_.rd_busy ? 0 : 1;
  dut_->mem_rsp_valid_i = br_.rd_present ? 1 : 0;
  dut_->mem_rsp_data_i = br_.rd_present ? word_at(rword) : 0;
  dut_->mem_rsp_last_i = 1;
  dut_->mem_rsp_err_i = (br_.rd_present && br_.poisoned.count(rword)) ? 1 : 0;
  dut_->mem_wr_ready_i = br_.wr_busy ? 0 : 1;
  if (br_.posted) {
    // committed in the accept cycle: done rides with ready when a write is
    // presented
    bool accept = dut_->mem_wr_valid_o && !br_.wr_busy;
    dut_->mem_wr_done_i = accept ? 1 : 0;
    dut_->mem_wr_err_i =
        (accept && br_.poisoned.count(dut_->mem_wr_addr_o & ~7u)) ? 1 : 0;
  } else {
    dut_->mem_wr_done_i = br_.wr_present ? 1 : 0;
    dut_->mem_wr_err_i =
        (br_.wr_present && br_.poisoned.count(br_.wr_addr & ~7u)) ? 1 : 0;
  }
  dut_->eval();
}

void NvmBackendHarness::posedge() {
  // advance the bridge on the handshakes of the settled cycle
  if (dut_->mem_req_valid_o && dut_->mem_req_ready_i) {
    br_.rd_busy = true;
    br_.rd_present = false;
    br_.rd_addr = dut_->mem_req_addr_o;
    br_.rd_lat = br_.latency;
  } else if (br_.rd_busy && !br_.rd_present) {
    if (--br_.rd_lat <= 0) br_.rd_present = true;
  } else if (br_.rd_present && dut_->mem_rsp_ready_o) {
    br_.rd_present = false;
    br_.rd_busy = false;
    br_.reads++;
  }
  if (dut_->mem_wr_valid_o && dut_->mem_wr_ready_i) {
    if (br_.posted) {
      if (!br_.poisoned.count(dut_->mem_wr_addr_o & ~7u))
        apply_write(dut_->mem_wr_addr_o, dut_->mem_wr_data_o,
                    dut_->mem_wr_strb_o);
      br_.writes++;
    } else {
      br_.wr_busy = true;
      br_.wr_present = false;
      br_.wr_addr = dut_->mem_wr_addr_o;
      br_.wr_data = dut_->mem_wr_data_o;
      br_.wr_strb = dut_->mem_wr_strb_o;
      br_.wr_lat = br_.latency;
    }
  } else if (br_.wr_busy && !br_.wr_present) {
    if (--br_.wr_lat <= 0) br_.wr_present = true;
  } else if (br_.wr_present) {
    // the done pulse was visible this cycle: commit and release
    if (!br_.poisoned.count(br_.wr_addr & ~7u))
      apply_write(br_.wr_addr, br_.wr_data, br_.wr_strb);
    br_.wr_present = false;
    br_.wr_busy = false;
    br_.writes++;
  }

  dut_->clk_i = 1;
  dut_->eval();
  dut_->clk_i = 0;
  dut_->eval();
  if (watch_stale_ && dut_->nvm_backed_o && !dut_->nvm_dirty_o &&
      dut_->nvm_stale_o)
    bad_pair_++;
}

void NvmBackendHarness::tick() {
  settle();
  posedge();
}

void NvmBackendHarness::csr_write(unsigned addr, uint32_t data) {
  dut_->csr_sel_i = 1;
  dut_->csr_we_i = 1;
  dut_->csr_addr_i = addr;
  dut_->csr_wdata_i = data;
  tick();
  dut_->csr_sel_i = 0;
  dut_->csr_we_i = 0;
  dut_->csr_wdata_i = 0;
}

uint32_t NvmBackendHarness::csr_read(unsigned addr) {
  dut_->csr_sel_i = 1;
  dut_->csr_we_i = 0;
  dut_->csr_addr_i = addr;
  settle();
  uint32_t v = dut_->csr_rdata_o;
  dut_->csr_sel_i = 0;
  return v;
}

void NvmBackendHarness::reset_dut() {
  dut_->rst_n = 0;
  dut_->csr_sel_i = dut_->csr_we_i = 0;
  dut_->pend_i = 0;
  dut_->alarm_i = 0;
  dut_->dev_req_i = dut_->dev_wvalid_i = dut_->dev_rready_i = 0;
  br_ = Bridge();
  for (int i = 0; i < RESET_CYCLES; i++) tick();
  dut_->rst_n = 1;
  tick();
}

void NvmBackendHarness::configure_image() {
  csr_write(0, IMG_BASE);  // R_IMG_BASE points at the RECORD AREA
  csr_write(1, area_len_);
  program_map_tables();
}

void NvmBackendHarness::set_valid(bool valid, unsigned verdict) {
  csr_write(3, (valid ? 0x10u : 0u) | (verdict & 0xFu));
}

// One device-face command. Returns true on dev_done_o, false on dev_err_o.
bool NvmBackendHarness::dev_cmd(int op, unsigned region, unsigned offset,
                                unsigned len, std::vector<uint8_t> *rd,
                                const uint8_t *wr) {
  dut_->dev_req_i = 1;
  dut_->dev_op_i = op;
  dut_->dev_region_i = region;
  dut_->dev_offset_i = offset;
  dut_->dev_len_i = len;
  dut_->dev_rready_i = 1;
  dut_->dev_wvalid_i = wr ? 1 : 0;
  if (wr) dut_->dev_wdata_i = wr[0];
  tick();
  dut_->dev_req_i = 0;

  size_t wi = 0;
  for (int guard = 0; guard < CMD_GUARD_CYCLES; guard++) {
    settle();
    bool done = dut_->dev_done_o != 0;
    bool err = dut_->dev_err_o != 0;
    if (rd && dut_->dev_rvalid_o && dut_->dev_rready_i)
      rd->push_back(dut_->dev_rdata_o);
    // a byte is TRANSFERRED at the clock edge of the cycle in which both valid
    // and ready are high, so the next byte may only appear after that edge --
    // exactly as KL_pp_nvm_port drives its device face
    bool took = wr && dut_->dev_wvalid_i && dut_->dev_wready_o;
    //! A live writer answers the liveness deadline THROUGH a long operation
    //! (design page 9.4, and case A9 of the snapshot-ownership page keeps a
    //! 250 ms heartbeat gap through a 3 s erase). At this suite's scaled
    //! clock one "millisecond" is ten clocks, so a whole-record WRITE
    //! outlives T_ALIVE_MS_P, and section 9.2's rows would be measuring the
    //! scaled deadline instead of the rule under test. The strobe rides THIS
    //! cycle's edge: it must add no edge of its own, or the byte handshake
    //! below loses a byte and the command never completes.
    bool hb_now = hb_during_cmd_ && guard && (guard % 8) == 0;
    if (hb_now) {
      dut_->csr_sel_i = 1;
      dut_->csr_we_i = 1;
      dut_->csr_addr_i = 4;
      dut_->csr_wdata_i = 1u;
      settle();
    }
    posedge();
    if (hb_now) {
      dut_->csr_sel_i = 0;
      dut_->csr_we_i = 0;
    }
    if (took) {
      wi++;
      if (wi < len) dut_->dev_wdata_i = wr[wi];
    }
    if (done || err) {
      dut_->dev_rready_i = 0;
      dut_->dev_wvalid_i = 0;
      return done;
    }
  }
  dut_->dev_rready_i = 0;
  dut_->dev_wvalid_i = 0;
  check(false, "%s: a command on region 0x%02X never completed",
        shape_.c_str(), region);
  return false;
}

// ---------------------------------------------------------------------------
void NvmBackendHarness::program_map_tables() {
  // Firmware's job: the running sum of the framed lengths INSIDE each group.
  // The GROUP BASE is deliberately NOT programmed. The backend has to derive
  // it from the lengths it was given, which is exactly what a nominal stride
  // got wrong.
  for (int dir = 0; dir < 2; dir++) {
    const char *want = dir ? "MAPS_OUT" : "MAPS_IN";
    unsigned pref = 0;
    for (size_t n = 0; n < recs_.size(); n++) {
      const Rec &r = recs_[n];
      if (r.group != want) continue;
      csr_write(0x20u | (dir ? 0x10u : 0u) | (r.index & 0xFu),
                (static_cast<uint32_t>(r.flen) << 16) | pref);
      pref += r.flen;
    }
  }
}

// Before the firmware has configured an image the module IS the blank-flash
// responder it replaces: reads 0xFF with no bus traffic, writes accepted and
// discarded, erase completes -- and a discarded write still counts as an
// accepted change.
void NvmBackendHarness::test_unconfigured() {
  const Rec &r = recs_[0];
  std::vector<uint8_t> got;
  unsigned reads0 = br_.reads;
  unsigned writes0 = br_.writes;
  check(dev_cmd(0, r.id, 0, r.flen, &got, 0),
        "%s: unconfigured: a READ of 0x%02X was refused; blank flash must "
        "answer", shape_.c_str(), r.id);
  bool all_ff = got.size() == r.flen;
  for (size_t j = 0; j < got.size(); j++) all_ff = all_ff && got[j] == 0xFF;
  check(all_ff, "%s: unconfigured: a READ of 0x%02X did not return %u bytes "
        "of 0xFF", shape_.c_str(), r.id, r.flen);
  check(!(csr_read(3) & STAT_IMG_CFG),
        "%s: unconfigured: the status word claims a configured image",
        shape_.c_str());
  const std::array<uint8_t, 4> pat = {1, 2, 3, 4};
  check(dev_cmd(1, r.id, 0, 4, 0, pat.data()),
        "%s: unconfigured: a WRITE into 0x%02X was refused; blank flash "
        "accepts and discards", shape_.c_str(), r.id);
  check(!memcmp(&mem_[r.off], &area_[r.off], 4),
        "%s: unconfigured: a discarded WRITE reached memory", shape_.c_str());
  check(dev_cmd(2, r.id, 0, 0, 0, 0),
        "%s: unconfigured: an ERASE of 0x%02X did not complete", shape_.c_str(),
        r.id);
  check(br_.reads == reads0 && br_.writes == writes0,
        "%s: unconfigured: the bus saw %u read(s) and %u write(s); blank flash "
        "must cause none", shape_.c_str(), br_.reads - reads0,
        br_.writes - writes0);
  // Under the snapshot-ownership contract nvm_dirty is COMMITTABLE image
  // work, and a WRITE with no configured image mutates no record: it is
  // accepted and discarded, no record opens and none closes, so the bit
  // stays 0. The change is still not durable and the status still says so,
  // on the PENDING bit, which reads 1 here because every allocated record is
  // open until the boot window load is accepted (sections 4 and 6.1).
  check(dut_->nvm_dirty_o == 0,
        "%s: unconfigured: a discarded WRITE set nvm_dirty; it mutates no "
        "record, so there is nothing committable to report", shape_.c_str());
  check(dut_->nvm_pend_o == 1 && (csr_read(3) & (1u << 23)),
        "%s: unconfigured: a discarded WRITE is not reported on the pending "
        "bit, and every record is open until the boot load is accepted",
        shape_.c_str());
  check(dut_->nvm_backed_o == 0,
        "%s: unconfigured: nvm_backed is 1 with no writer ever heard from",
        shape_.c_str());
}

// Configured but not yet validated: a READ still answers blank flash and touches
// no memory; validation opens the image; moving the image closes it again.
void NvmBackendHarness::test_validity_gate() {
  const Rec &r = recs_[0];
  std::vector<uint8_t> got;
  unsigned reads0 = br_.reads;
  check(csr_read(3) & STAT_IMG_CFG,
        "%s: the status word does not show the configured image",
        shape_.c_str());
  check(!(csr_read(3) & STAT_IMG_VALID),
        "%s: the image reads as valid before the firmware said so",
        shape_.c_str());
  // the command runs BEFORE the check call, so the message's arguments
  // describe what it returned (function arguments are evaluated in an
  // unspecified order, and a call inside the condition may run last)
  bool ok = dev_cmd(0, r.id, 0, r.flen, &got, 0);
  check(ok && got.size() == r.flen && got[0] == 0xFF && got[1] == 0xFF &&
            got[r.flen - 1] == 0xFF && br_.reads == reads0,
        "%s: a READ before the image was validated served image bytes or "
        "touched the bus (done %d, %zu byte(s), first %02X %02X, %u bus "
        "read(s))",
        shape_.c_str(), ok ? 1 : 0, got.size(), got.empty() ? 0 : got[0],
        got.size() > 1 ? got[1] : 0, br_.reads - reads0);
  set_valid(true, 0);
  check(dut_->img_valid_o == 1 && (csr_read(3) & STAT_IMG_VALID),
        "%s: validation did not take", shape_.c_str());
  got.clear();
  ok = dev_cmd(0, r.id, 0, r.flen, &got, 0);
  check(ok && got.size() == r.flen && !memcmp(got.data(), &area_[r.off], r.flen),
        "%s: a READ after validation did not serve the image", shape_.c_str());
  // moving the image invalidates it: a READ answers blank again
  csr_write(0, IMG_BASE);
  check(dut_->img_valid_o == 0,
        "%s: writing R_IMG_BASE left the image marked valid", shape_.c_str());
  got.clear();
  ok = dev_cmd(0, r.id, 0, 4, &got, 0);
  check(ok && got.size() == 4 && got[0] == 0xFF,
        "%s: a READ after the image moved served stale image bytes (first byte "
        "%02X)", shape_.c_str(), got.empty() ? 0 : got[0]);
  set_valid(true, 0);
}

void NvmBackendHarness::test_regions() {
  for (size_t n = 0; n < recs_.size(); n++) {
    const Rec &r = recs_[n];
    std::vector<uint8_t> got;
    if (!dev_cmd(0 /*READ*/, r.id, 0, r.flen, &got, 0)) {
      check(false, "%s: a READ of record 0x%02X (%s[%u]) was REFUSED",
            shape_.c_str(), r.id, r.group.c_str(), r.index);
      continue;
    }
    if (got.size() != static_cast<size_t>(r.flen)) {
      check(false, "%s: a READ of record 0x%02X returned %zu B, wanted %u",
            shape_.c_str(), r.id, got.size(), r.flen);
      continue;
    }
    size_t bad = NOPOS;
    for (size_t j = 0; j < got.size(); j++)
      if (got[j] != area_[r.off + j]) { bad = j; break; }
    check(bad == NOPOS,
          "%s: %s[%u] (record 0x%02X, %u framed bytes at area offset %u) reads "
          "the wrong span: byte %zu came back 0x%02X, the image holds 0x%02X. "
          "The backend resolved this record to a different place in the image",
          shape_.c_str(), r.group.c_str(), r.index, r.id, r.flen, r.off,
          bad == NOPOS ? static_cast<size_t>(0) : bad,
          bad == NOPOS ? 0 : got[bad],
          bad == NOPOS ? 0 : area_[r.off + bad]);
  }

  // a partial read, so the offset adder is exercised as well as the base
  for (size_t n = 0; n < recs_.size(); n++) {
    const Rec &r = recs_[n];
    if (r.flen < 12) continue;
    std::vector<uint8_t> got;
    if (!dev_cmd(0, r.id, 8, 4, &got, 0)) {
      check(false, "%s: a partial READ of 0x%02X was refused", shape_.c_str(),
            r.id);
      continue;
    }
    check(got.size() == 4 && !memcmp(got.data(), &area_[r.off + 8], 4),
          "%s: a partial READ of 0x%02X at offset 8 returned the wrong bytes",
          shape_.c_str(), r.id);
  }

  // the word cache: consecutive bytes of one record cost one bus read per
  // eight-byte word, never one per byte
  {
    const Rec &r = recs_[recs_.size() - 1];
    std::vector<uint8_t> got;
    dev_cmd(0, recs_[0].id, 0, 4, &got, 0);   // park the cache on word 0
    got.clear();
    unsigned reads0 = br_.reads;
    dev_cmd(0, r.id, 0, r.flen, &got, 0);
    unsigned words = ((IMG_BASE + r.off + r.flen - 1) >> 3) -
                     ((IMG_BASE + r.off) >> 3) + 1;
    check(br_.reads - reads0 == words,
          "%s: a %u-byte READ of 0x%02X cost %u bus reads; the word cache "
          "should make it %u", shape_.c_str(), r.flen, r.id,
          br_.reads - reads0, words);
  }
}

// A WRITE must land where a READ found the record, byte-strobed so the
// neighbours are untouched; a later READ must see it (the word cache is
// invalidated by the write); an ERASE fills exactly the record with 0xFF.
void NvmBackendHarness::test_writes_and_erase(bool posted) {
  br_.posted = posted;
  const char *mode = posted ? "posted bridge" : "acknowledged bridge";
  for (size_t n = 0; n < recs_.size(); n++) {
    const Rec &r = recs_[n];
    if (r.group != "MAPS_OUT" || r.flen < 24) continue;
    const std::array<uint8_t, 8> pat = {0x5A, 0xA5, 0x00, 0xFF,
                                        0x11, 0x22, 0x33, 0x44};
    std::vector<uint8_t> before;
    dev_cmd(0, r.id, 16, 8, &before, 0);  // prime the word cache
    if (!dev_cmd(1 /*WRITE*/, r.id, 16, 8, 0, pat.data())) {
      check(false, "%s: %s: a WRITE into 0x%02X was refused", shape_.c_str(),
            mode, r.id);
      continue;
    }
    check(!memcmp(&mem_[r.off + 16], pat.data(), 8),
          "%s: %s: a WRITE into %s[%u] at offset 16 did not land at area "
          "offset %u", shape_.c_str(), mode, r.group.c_str(), r.index,
          r.off + 16);
    check(!memcmp(&mem_[r.off], &area_[r.off], 16) &&
              !memcmp(&mem_[r.off + 24], &area_[r.off + 24], r.flen - 24),
          "%s: %s: a WRITE into %s[%u] modified bytes outside its span",
          shape_.c_str(), mode, r.group.c_str(), r.index);
    std::vector<uint8_t> got;
    check(dev_cmd(0, r.id, 16, 8, &got, 0) && got.size() == 8 &&
              !memcmp(got.data(), pat.data(), 8),
          "%s: %s: a READ after the WRITE served the cached old word",
          shape_.c_str(), mode);
    // A PARTIAL write is not a completed logical record, so it does NOT
    // close its record and does NOT make the image committable: what it does
    // is OPEN the record, and the open bit and the pending bit report it
    // (snapshot-ownership section 4; mutant M03 of the contract page is
    // exactly the rule that closes on a partial write).
    check(dut_->nvm_dirty_o == 0,
          "%s: %s: a PARTIAL WRITE made the image committable", shape_.c_str(),
          mode);
    check((csr_read(R_OWN0 + (r.id >> 5)) >> (r.id & 31u)) & 1u,
          "%s: %s: a PARTIAL WRITE into 0x%02X left its record closed",
          shape_.c_str(), mode, r.id);
    memcpy(&mem_[r.off + 16], &area_[r.off + 16], 8);  // restore
  }
  // ERASE of one whole record: exactly its span reads 0xFF afterwards
  {
    const Rec &r = recs_[1];
    check(dev_cmd(2 /*ERASE*/, r.id, 0, 0, 0, 0),
          "%s: %s: an ERASE of 0x%02X was refused", shape_.c_str(), mode, r.id);
    bool span_ff = true;
    for (unsigned j = 0; j < r.flen; j++)
      span_ff = span_ff && mem_[r.off + j] == 0xFF;
    bool neighbours_ok =
        (r.off == 0 || mem_[r.off - 1] == area_[r.off - 1]) &&
        (r.off + r.flen >= mem_.size() ||
         mem_[r.off + r.flen] == area_[r.off + r.flen]);
    check(span_ff && neighbours_ok,
          "%s: %s: ERASE of 0x%02X did not fill exactly its %u bytes with 0xFF",
          shape_.c_str(), mode, r.id, r.flen);
    memcpy(&mem_[r.off], &area_[r.off], r.flen);  // restore
  }
  br_.posted = false;
}

void NvmBackendHarness::test_bounds_and_errors() {
  std::vector<uint8_t> got;
  check(!dev_cmd(0, 0x1A, 0, 4, &got, 0),
        "%s: a READ of unallocated region 0x1A was ACCEPTED", shape_.c_str());
  got.clear();
  check(!dev_cmd(0, recs_[0].id, 0, recs_[0].flen + 1, &got, 0),
        "%s: a READ one byte past the end of record 0x%02X was ACCEPTED",
        shape_.c_str(), recs_[0].id);
  // a span past the configured image is refused even inside the record
  const Rec &last = recs_[recs_.size() - 1];
  csr_write(1, last.off + 4);   // the image ends inside the last record
  set_valid(true, 0);
  got.clear();
  check(!dev_cmd(0, last.id, 0, last.flen, &got, 0),
        "%s: a READ past the configured image length was ACCEPTED",
        shape_.c_str());
  csr_write(1, area_len_);
  set_valid(true, 0);
  // a bus error ends the operation with err and no data served as good
  const Rec &r = recs_[0];
  br_.poisoned.insert((IMG_BASE + r.off) & ~7u);
  got.clear();
  check(!dev_cmd(0, r.id, 0, r.flen, &got, 0),
        "%s: a READ whose bus access failed reported done", shape_.c_str());
  const std::array<uint8_t, 2> pat = {0xAA, 0x55};
  check(!dev_cmd(1, r.id, 0, 2, 0, pat.data()),
        "%s: a WRITE whose bus access failed reported done", shape_.c_str());
  check(!memcmp(&mem_[r.off], &area_[r.off], 2),
        "%s: a failed WRITE modified memory", shape_.c_str());
  br_.poisoned.clear();
  got.clear();
  check(dev_cmd(0, r.id, 0, 4, &got, 0) && got.size() == 4 &&
            !memcmp(got.data(), &area_[r.off], 4),
        "%s: the backend did not recover after a bus error", shape_.c_str());
}

void NvmBackendHarness::test_status_word() {
  uint32_t s = csr_read(3);
  check((s & STAT_IMG_CFG) && (s & STAT_IMG_VALID),
        "%s: the status word does not show a configured, validated image "
        "(0x%08X)", shape_.c_str(), s);
  check(((s >> 12) & 0xF) == 0,
        "%s: the verdict field is not the 0 the firmware wrote (0x%08X)",
        shape_.c_str(), s);
  set_valid(true, 0xB);
  s = csr_read(3);
  check(((s >> 12) & 0xF) == 0xB && dut_->nvm_verdict_o == 0xB,
        "%s: a written verdict did not publish (0x%08X)", shape_.c_str(), s);
  set_valid(true, 0);
  check(csr_read(0) == IMG_BASE && csr_read(1) == area_len_,
        "%s: R_IMG_BASE / R_IMG_LEN do not read back", shape_.c_str());
  csr_write(2, 0x12345678u);
  check(csr_read(2) == 0x12345678u, "%s: R_SEQ does not read back",
        shape_.c_str());
}

// ---------------------------------------------------------------------------
void NvmBackendHarness::hb() { csr_write(4, 1u << 0); }
void NvmBackendHarness::commit_ack(uint32_t cap_id) {
  csr_write(4, (1u << 1) | (cap_id << 16));
}
void NvmBackendHarness::commit_start() { csr_write(4, 1u << 2); }

// The producer holds an accepted change it has not yet written through the
// device face. A LEVEL, and no acknowledgement retires it: it reaches
// nvm_pend_o and never nvm_dirty_o (snapshot-ownership section 6.1).
void NvmBackendHarness::pend(int level) {
  dut_->pend_i = level;
  tick();
}

// The boot window load of section 5.3: a re-base with nothing in flight arms
// the load flag, and the RELOAD the backend then ACCEPTS closes every record
// and is what lets any capture be armed at all (rule 9).
void NvmBackendHarness::boot_load() {
  configure_image();
  set_valid(true, 0);
  csr_write(4, 1u << 6);   // RELOAD
}

// A whole-record WRITE that completes with done: the ONE event that closes a
// record and is therefore the only thing that makes the image committable.
void NvmBackendHarness::close_record() {
  const Rec &r = recs_[0];
  std::vector<uint8_t> pat(r.flen, 0x5Au);
  check(dev_cmd(1 /*WRITE*/, r.id, 0, r.flen, 0, pat.data()),
        "%s: a whole-record WRITE of 0x%02X was refused", shape_.c_str(), r.id);
  tick();
  check(!((csr_read(R_OWN0 + (r.id >> 5)) >> (r.id & 31u)) & 1u) &&
            dut_->nvm_dirty_o,
        "%s: a whole-record WRITE of 0x%02X did not close it and make the "
        "image committable", shape_.c_str(), r.id);
}

// One capture, acknowledged: ARM, read the identity, ATTEST, ACK quoting it.
// Returns the identity the acknowledgement quoted, 0 if the ARM was refused.
uint32_t NvmBackendHarness::capture() {
  csr_write(4, 1u << 3);   // ARM
  uint32_t s = csr_read(3);
  if (!(s & STAT_CAP_OPEN) || (s & STAT_ARM_REF)) return 0;
  uint32_t id = csr_read(R_CAPID);
  csr_write(4, 1u << 4);   // ATTEST
  if (!(csr_read(3) & STAT_ATTESTED)) return 0;
  commit_ack(id);
  return id;
}

void NvmBackendHarness::idle_ms(int n) {
  for (int i = 0; i < n * MS + 2; i++) tick();
}

void NvmBackendHarness::expect_bits(const char *what, int b, int d, int s) {
  uint32_t word = csr_read(3);
  bool face = ((word & STAT_BACKED) != 0) == (b != 0) &&
              ((word & STAT_DIRTY) != 0) == (d != 0) &&
              ((word & STAT_STALE) != 0) == (s != 0);
  check(dut_->nvm_backed_o == b && dut_->nvm_dirty_o == d &&
            dut_->nvm_stale_o == s && face,
        "%s: %s -- read (backed=%d, dirty=%d, stale=%d), wanted (%d, %d, %d)"
        " (status word 0x%08X)",
        shape_.c_str(), what, static_cast<int>(dut_->nvm_backed_o),
        static_cast<int>(dut_->nvm_dirty_o),
        static_cast<int>(dut_->nvm_stale_o), b, d, s, word);
}

void NvmBackendHarness::test_stale() {
  watch_stale_ = true;

  // (a) a build that never had a writer is never stale
  reset_dut();
  boot_load();
  idle_ms(12);
  expect_bits("never backed, nothing outstanding", 0, 0, 0);
  close_record();
  idle_ms(12);
  expect_bits("never backed, changes accepted", 0, 1, 0);

  //! From here on a WRITER IS LIVE, so the long device-face commands below
  //! answer the liveness deadline as one does (dev_cmd). Case (a) above must
  //! NOT: it is the build that never had a writer, and a heartbeat inside its
  //! WRITE would make the idle that follows a LOSS rather than the honest
  //! never-backed state.
  hb_during_cmd_ = true;

  // (b) a loss with NOTHING outstanding, a clean recovery, and then an
  //     ordinary controller change. This is the row round 3 contradicted: the
  //     recovery made the loss good, so a later SET must not republish it.
  reset_dut();
  boot_load();
  hb();
  expect_bits("the writer answered", 1, 0, 0);
  idle_ms(12);
  expect_bits("writer lost, nothing outstanding", 0, 0, 1);
  hb();
  tick();
  expect_bits("a clean recovery clears the loss", 1, 0, 0);
  close_record();
  tick();
  expect_bits("an ordinary change after a healed outage is in flight, not "
              "stale",
              1, 1, 0);
  check(capture() != 0,
        "%s: the capture that retires the work was not acknowledged",
        shape_.c_str());
  hb();
  tick();
  expect_bits("the commit is acknowledged", 1, 0, 0);

  // (c) a loss WITH data outstanding stays stale through the recovery and
  //     clears only when the commit that makes it durable completes
  reset_dut();
  boot_load();
  hb();
  close_record();
  tick();
  expect_bits("in flight", 1, 1, 0);
  idle_ms(12);
  expect_bits("writer lost with data outstanding", 0, 1, 1);
  hb();
  tick();
  expect_bits("recovering: answering again, not yet durable", 1, 1, 1);
  check(capture() != 0, "%s: the recovery capture was not acknowledged",
        shape_.c_str());
  hb();
  tick();
  expect_bits("the outage is made good by the commit", 1, 0, 0);

  // (d) a SECOND loss sets it again
  idle_ms(12);
  expect_bits("a later second loss is stale again", 0, 0, 1);
  hb();
  tick();
  expect_bits("and is cleared again by the recovery", 1, 0, 0);

  test_stale_deadlines();
}

// (e) to (h): the two deadlines, the separate pending bit and the reported
// transaction failure. Split from the rows above because Rule 11 bounds a
// function's length; `watch_stale_` and `hb_during_cmd_` stay set across
// both, so the unreachable-row watch covers every cycle of either.
void NvmBackendHarness::test_stale_deadlines() {
  // (e) the commit deadline: a started commit nobody acknowledges is a loss
  reset_dut();
  boot_load();
  hb();
  commit_start();
  for (int i = 0; i < 3; i++) { hb(); idle_ms(2); }   // T_COMMIT_MS_P is 6
  expect_bits("a commit that outlives T-NVM-COMMIT-TIMEOUT revokes backing "
              "even with the heartbeat serviced", 0, 0, 1);
  // (f) a commit acknowledged in time is not. The acknowledgement must quote
  // an OPEN, ATTESTED capture to disarm the deadline: one that names nothing
  // this backend holds is refused and the deadline runs on.
  reset_dut();
  boot_load();
  hb();
  commit_start();
  hb(); idle_ms(2);
  check(capture() != 0, "%s: the in-deadline capture was refused",
        shape_.c_str());
  hb(); idle_ms(2);
  expect_bits("a commit acknowledged inside the deadline keeps backing",
              1, 0, 0);

  // (g) THE SEPARATE PENDING BIT (snapshot-ownership 6.1). A producer-held
  // change is reported on its own bit, drives no commit and is retired by
  // NO acknowledgement: only the producer dropping the level clears it.
  reset_dut();
  boot_load();
  hb();
  pend(1);
  tick();
  expect_bits("a producer-held change is NOT committable image work", 1, 0, 0);
  expect_pend("a producer-held change is reported on the pending bit", 1);
  check(capture() != 0, "%s: an arm was refused with a producer change held",
        shape_.c_str());
  tick();
  expect_pend("no acknowledgement retires a producer-held change", 1);
  pend(0);
  tick();
  expect_pend("the producer dropping the level clears it", 0);

  // (h) A REPORTED TRANSACTION FAILURE revokes when it is REPORTED, which is
  // the section 12 resolution: waiting for the 8000 ms commit deadline
  // advertises durability for up to eight seconds after a known failure.
  reset_dut();
  boot_load();
  hb();
  expect_bits("the writer answered", 1, 0, 0);
  set_valid(true, 0xD);   // VD_VERIFY
  tick();
  expect_bits("a reported read-back-verify failure revokes at once",
              0, 0, 1);

  watch_stale_ = false;
  hb_during_cmd_ = false;
  check(bad_pair_ == 0,
        "%s: (backed=1, dirty=0, stale=1) was observable on %d cycle(s), and "
        "section 9.3 calls that row unreachable",
        shape_.c_str(), bad_pair_);
}

void NvmBackendHarness::expect_pend(const char *what, int want) {
  uint32_t s = csr_read(3);
  int face = static_cast<int>(dut_->nvm_pend_o);
  check(face == want && ((s >> 22) & 1) == static_cast<uint32_t>(want),
        "%s: %s -- nvm_pend_o %d and status [22] %u, wanted %d",
        shape_.c_str(), what, face, (s >> 22) & 1, want);
}

// The open vector of section 4, the contract tag, and the two terms that
// refuse an arm. Everything here is read on the backend's OWN face, which is
// where the contract puts the per-record detail (section 16, option A).
void NvmBackendHarness::test_ownership() {
  reset_dut();
  uint32_t s = csr_read(3);
  check((s & 0xFF000000u) == STAT_TAG,
        "%s: the status word does not carry the contract tag 0xC3 (0x%08X)",
        shape_.c_str(), s);
  // the reset row: every allocated record OPEN, the boot load still open and
  // none accepted, so an ARM is refused even once the image is validated
  check((s & STAT_UNRES) && (s & STAT_PEND) && (s & STAT_LOAD_PEND) &&
            !(s & STAT_LOAD_ACC) && !(s & STAT_CAP_OPEN),
        "%s: the reset row is wrong (0x%08X)", shape_.c_str(), s);
  unsigned open_at_reset = 0;
  for (unsigned w = 0; w < 8; w++) {
    uint32_t bits = csr_read(R_OWN0 + w);
    for (unsigned b = 0; b < 32; b++) if ((bits >> b) & 1u) open_at_reset++;
  }
  check(open_at_reset == recs_.size(),
        "%s: %u record(s) open at reset, and this shape allocates %zu",
        shape_.c_str(), open_at_reset, recs_.size());
  configure_image();
  set_valid(true, 0);
  csr_write(4, 1u << 3);   // ARM, before any accepted RELOAD
  s = csr_read(3);
  check((s & STAT_ARM_REF) && !(s & STAT_CAP_OPEN) && csr_read(R_CAPID) == 0,
        "%s: an ARM was accepted with load accepted 0, and rule 9 refuses it "
        "(0x%08X)", shape_.c_str(), s);

  // the accepted boot load closes every record and lets a capture be armed
  reset_dut();
  boot_load();
  s = csr_read(3);
  check(!(s & STAT_RELOAD_REF) && (s & STAT_LOAD_ACC) && !(s & STAT_LOAD_PEND),
        "%s: the boot window load was refused (0x%08X)", shape_.c_str(), s);
  check(!(s & STAT_UNRES) && !(s & STAT_PEND),
        "%s: an accepted RELOAD did not close every record (0x%08X)",
        shape_.c_str(), s);

  // a mutating GRANT opens its record and NOTHING else's; only a
  // whole-record WRITE with done closes it again
  const Rec &r = recs_[0];
  std::vector<uint8_t> blank(r.flen, 0xFFu);
  check(dev_cmd(2 /*ERASE*/, r.id, 0, 0, 0, 0),
        "%s: an ERASE of 0x%02X was refused", shape_.c_str(), r.id);
  tick();
  check((csr_read(R_OWN0 + (r.id >> 5)) >> (r.id & 31u)) & 1u,
        "%s: an ERASE of 0x%02X left its record closed", shape_.c_str(), r.id);
  check((csr_read(3) & STAT_UNRES) && (csr_read(3) & STAT_PEND),
        "%s: an open record is not reported", shape_.c_str());
  close_record();
  check(!((csr_read(R_OWN0 + (r.id >> 5)) >> (r.id & 31u)) & 1u),
        "%s: a whole-record WRITE of 0x%02X did not close it", shape_.c_str(),
        r.id);
  // a PARTIAL write never closes a record: the logical record is not complete
  check(dev_cmd(2 /*ERASE*/, r.id, 0, 0, 0, 0) &&
            dev_cmd(1 /*WRITE*/, r.id, 0, 4, 0, blank.data()),
        "%s: the partial-write setup was refused", shape_.c_str());
  tick();
  check((csr_read(R_OWN0 + (r.id >> 5)) >> (r.id & 31u)) & 1u,
        "%s: a PARTIAL WRITE closed record 0x%02X", shape_.c_str(), r.id);

  // a second RELOAD after the boot is REFUSED and changes nothing
  csr_write(4, 1u << 6);
  s = csr_read(3);
  check((s & STAT_RELOAD_REF) && (s & STAT_UNRES),
        "%s: a RELOAD after the boot load was accepted (0x%08X)",
        shape_.c_str(), s);

  // an acknowledgement quoting ANOTHER capture names nothing this backend
  // holds: refused, and the work it aimed at stays owned
  reset_dut();
  boot_load();
  close_record();
  csr_write(4, 1u << 3);
  uint32_t id = csr_read(R_CAPID);
  csr_write(4, 1u << 4);
  commit_ack(id + 7u);
  s = csr_read(3);
  check((s & STAT_ACK_REF) && (s & STAT_CAP_OPEN) && dut_->nvm_dirty_o,
        "%s: a stale acknowledgement retired work (0x%08X)", shape_.c_str(), s);
  commit_ack(id);
  tick();
  check(!dut_->nvm_dirty_o,
        "%s: the acknowledgement quoting the open capture retired nothing",
        shape_.c_str());
}

// ---------------------------------------------------------------------------
int NvmBackendHarness::run(int argc, char **argv) {
  if (argc < 2) {
    printf("usage: %s <record table>\n", argv[0]);
    return 2;
  }
  load_table(argv[1]);
  if (recs_.empty() || !imglen_) {
    printf("FAIL: record table %s carries no records\n", argv[1]);
    return 2;
  }
  build_area();
  prove_byte_exact();

  mem_ = area_;
  mem_.resize(mem_.size() + 16, 0);

  const milan::tb::Model<Vnvm> model;
  dut_ = model.get();
  dut_->clk_i = 0;
  reset_dut();
  test_unconfigured();
  reset_dut();
  configure_image();
  test_validity_gate();
  test_regions();
  test_writes_and_erase(false);
  test_writes_and_erase(true);
  test_bounds_and_errors();
  test_status_word();
  test_stale();
  test_ownership();

  printf("nvm_backend[%s]: checks: %d  failures: %d\n", shape_.c_str(),
         checks_, fails_);
  return fails_ ? 1 : 0;
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  NvmBackendHarness harness;
  return harness.run(argc, argv);
}

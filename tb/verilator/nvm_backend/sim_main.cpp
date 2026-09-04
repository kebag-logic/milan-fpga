// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Grades syn/ooc/sizing/KL_nvm_backend_sizer.sv against a BYTE-EXACT KLJ2
// image (docs/design/SAVED_STATE_FASTCONNECT.md section 6.1) whose record
// offsets are produced independently by
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
//     graded against Python's offsets.
//
// What this exists to catch (review round 3, blockers 2 and 3):
//   * the two channel-map groups shared ONE {prefix,length} table indexed by
//     dev_region_i[3:0], so 0x60+k and 0x70+k aliased. On the shipped 8x8
//     overlay an input port is 72 framed bytes and an output port is 144, so
//     at least one direction read the wrong span.
//   * the group base after each channel-map group advanced by a NOMINAL
//     stride, although KLJ2 6.1 concatenates records with no padding.
//   * nvm_stale was a latch cleared only by reset with the published bit
//     masked, so a clean recovery republished stale=1 on the next ordinary
//     controller change.
// Each has a compiled-in negative control (NVM_MUT_*) that MUST fail; the
// Makefile runs all three and reddens if any of them passes.

#include "Vnvm.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"

#include <array>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
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

// One graded run against one record table. The image fixture, the memory
// behind the DUT's port and the tally used to sit at file scope, where no
// function could be read without reading every other one first; they are the
// state of a single run and live here now. The functions below moved with
// them unchanged, so every call site inside them still reads the same.
class NvmBackendHarness {
 public:
  // Everything main used to do: load the table named on the command line,
  // rebuild the image, drive the DUT against it, print the tally.
  int run(int argc, char **argv);

 private:
  void check(bool ok, const char *fmt, ...);
  void load_table(const char *path);
  void build_area();
  void prove_byte_exact();
  void settle();
  void posedge();
  void tick();
  void csr_write(unsigned addr, uint32_t data);
  void reset_dut();
  bool dev_cmd(int op, unsigned region, unsigned offset, unsigned len,
               std::vector<uint8_t> *rd, const uint8_t *wr);
  void program_map_tables();
  void test_regions();
  void hb();
  void commit_ack();
  void dirty_set();
  void idle_ms(int n);
  void expect_bits(const char *what, int b, int d, int s);
  void test_stale();

  static constexpr uint32_t IMG_BASE = 0x40000000u;

  // Cycles the reset is held asserted before the first command.
  static constexpr int RESET_CYCLES = 8;

  // Loop guard: a command still outstanding after this many cycles is hung, and
  // the harness reports that rather than spinning.
  static constexpr int CMD_GUARD_CYCLES = 400000;

  // Section 9.2. CLK_HZ_P is 10 kHz in this build, so a "millisecond" is 10
  // clocks and T_ALIVE_MS_P is 4.
  static constexpr int MS = 10;

  int checks_ = 0;
  int fails_ = 0;

  std::vector<Rec> recs_;
  std::string shape_;
  unsigned layout_ = 0;
  unsigned hdrbytes_ = 0;
  unsigned imglen_ = 0;
  unsigned nrec_ = 0;
  uint32_t crc32_ = 0;

  // The record area, rebuilt byte for byte from the record list alone.
  std::vector<uint8_t> area_;

  Vnvm *dut_ = nullptr;
  std::vector<uint8_t> mem_;
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
  area_.assign(imglen_ - hdrbytes_ - IMG_CRC_BYTES, 0);
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
// Settle the combinational world for THIS cycle, including the one-cycle
// memory ack, so every output read afterwards is what the DUT will see at the
// coming posedge.
void NvmBackendHarness::settle() {
  dut_->eval();
  dut_->mem_ack_i = dut_->mem_req_o;
  if (dut_->mem_req_o) {
    uint32_t a = dut_->mem_addr_o - IMG_BASE;
    if (static_cast<size_t>(a) + 3 < mem_.size()) {
      if (dut_->mem_we_o) {
        for (int b = 0; b < 4; b++)
          if (dut_->mem_wstrb_o & (1 << b))
            mem_[a + b] = static_cast<uint8_t>(dut_->mem_wdata_o >> (8 * b));
      }
      dut_->mem_rdata_i = static_cast<uint32_t>(mem_[a]) |
                          (static_cast<uint32_t>(mem_[a + 1]) << 8) |
                          (static_cast<uint32_t>(mem_[a + 2]) << 16) |
                          (static_cast<uint32_t>(mem_[a + 3]) << 24);
    } else {
      dut_->mem_rdata_i = 0xDEADBEEFu;
    }
  }
  dut_->eval();
}

void NvmBackendHarness::posedge() {
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

void NvmBackendHarness::reset_dut() {
  dut_->rst_n = 0;
  dut_->csr_sel_i = dut_->csr_we_i = 0;
  dut_->dev_req_i = dut_->dev_wvalid_i = dut_->dev_rready_i = 0;
  for (int i = 0; i < RESET_CYCLES; i++) tick();
  dut_->rst_n = 1;
  tick();
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
    if (wr && dut_->dev_wvalid_i && dut_->dev_wready_o) {
      wi++;
      if (wi < len) {
        dut_->dev_wdata_i = wr[wi];
        dut_->eval();
      }
    }
    posedge();
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

  // a WRITE must land where a READ found the record
  for (size_t n = 0; n < recs_.size(); n++) {
    const Rec &r = recs_[n];
    if (r.group != "MAPS_OUT" || r.flen < 24) continue;
    const std::array<uint8_t, 8> pat = {0x5A, 0xA5, 0x00, 0xFF,
                                        0x11, 0x22, 0x33, 0x44};
    if (!dev_cmd(1 /*WRITE*/, r.id, 16, 8, 0, pat.data())) {
      check(false, "%s: a WRITE into 0x%02X was refused", shape_.c_str(),
            r.id);
      continue;
    }
    check(!memcmp(&mem_[r.off + 16], pat.data(), 8),
          "%s: a WRITE into %s[%u] at offset 16 did not land at area offset %u",
          shape_.c_str(), r.group.c_str(), r.index, r.off + 16);
    memcpy(&mem_[r.off + 16], &area_[r.off + 16], 8);  // restore
  }

  // negative controls on the decode itself
  std::vector<uint8_t> got;
  check(!dev_cmd(0, 0x1A, 0, 4, &got, 0),
        "%s: a READ of unallocated region 0x1A was ACCEPTED", shape_.c_str());
  got.clear();
  check(!dev_cmd(0, recs_[0].id, 0, recs_[0].flen + 1, &got, 0),
        "%s: a READ one byte past the end of record 0x%02X was ACCEPTED",
        shape_.c_str(), recs_[0].id);
}

// ---------------------------------------------------------------------------
void NvmBackendHarness::hb() { csr_write(4, 1u << 0); }
void NvmBackendHarness::commit_ack() { csr_write(4, 1u << 1); }
void NvmBackendHarness::dirty_set() { csr_write(4, 1u << 3); }

void NvmBackendHarness::idle_ms(int n) {
  for (int i = 0; i < n * MS + 2; i++) tick();
}

void NvmBackendHarness::expect_bits(const char *what, int b, int d, int s) {
  check(dut_->nvm_backed_o == b && dut_->nvm_dirty_o == d &&
            dut_->nvm_stale_o == s,
        "%s: %s -- read (backed=%d, dirty=%d, stale=%d), wanted (%d, %d, %d)",
        shape_.c_str(), what, static_cast<int>(dut_->nvm_backed_o),
        static_cast<int>(dut_->nvm_dirty_o),
        static_cast<int>(dut_->nvm_stale_o), b, d, s);
}

void NvmBackendHarness::test_stale() {
  watch_stale_ = true;

  // (a) a build that never had a writer is never stale
  reset_dut();
  idle_ms(12);
  expect_bits("never backed, nothing outstanding", 0, 0, 0);
  dirty_set();
  idle_ms(12);
  expect_bits("never backed, changes accepted", 0, 1, 0);

  // (b) a loss with NOTHING outstanding, a clean recovery, and then an
  //     ordinary controller change. This is the row round 3 contradicted: the
  //     recovery made the loss good, so a later SET must not republish it.
  reset_dut();
  hb();
  expect_bits("the writer answered", 1, 0, 0);
  idle_ms(12);
  expect_bits("writer lost, nothing outstanding", 0, 0, 1);
  hb();
  tick();
  expect_bits("a clean recovery clears the loss", 1, 0, 0);
  dirty_set();
  tick();
  expect_bits("an ordinary change after a healed outage is in flight, not "
              "stale",
              1, 1, 0);
  commit_ack();
  tick();
  expect_bits("the commit is acknowledged", 1, 0, 0);

  // (c) a loss WITH data outstanding stays stale through the recovery and
  //     clears only when the commit that makes it durable completes
  reset_dut();
  hb();
  dirty_set();
  tick();
  expect_bits("in flight", 1, 1, 0);
  idle_ms(12);
  expect_bits("writer lost with data outstanding", 0, 1, 1);
  hb();
  tick();
  expect_bits("recovering: answering again, not yet durable", 1, 1, 1);
  commit_ack();
  tick();
  expect_bits("the outage is made good by the commit", 1, 0, 0);

  // (d) a SECOND loss sets it again
  idle_ms(12);
  expect_bits("a later second loss is stale again", 0, 0, 1);
  hb();
  tick();
  expect_bits("and is cleared again by the recovery", 1, 0, 0);

  watch_stale_ = false;
  check(bad_pair_ == 0,
        "%s: (backed=1, dirty=0, stale=1) was observable on %d cycle(s), and "
        "section 9.3 calls that row unreachable",
        shape_.c_str(), bad_pair_);
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
  mem_.resize(mem_.size() + 8, 0);

  const milan::tb::Model<Vnvm> model;
  dut_ = model.get();
  dut_->clk_i = 0;
  reset_dut();
  csr_write(0, IMG_BASE);   // R_IMG_BASE points at the RECORD AREA
  csr_write(1, static_cast<uint32_t>(imglen_ - hdrbytes_ - IMG_CRC_BYTES));
  program_map_tables();
  test_regions();
  test_stale();

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

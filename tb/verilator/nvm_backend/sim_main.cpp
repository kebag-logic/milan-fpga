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

#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

static const size_t NOPOS = (size_t)-1;

static int g_checks = 0;
static int g_fails = 0;

static void check(bool ok, const char *fmt, ...) {
  g_checks++;
  if (ok) return;
  g_fails++;
  va_list ap;
  va_start(ap, fmt);
  fputs("FAIL: ", stdout);
  vprintf(fmt, ap);
  fputc('\n', stdout);
  va_end(ap);
}

// ---- the two digests, both independent re-implementations -----------------
static uint16_t crc16_ccitt(const uint8_t *d, size_t n) {
  uint16_t c = 0xFFFF;
  for (size_t i = 0; i < n; i++) {
    c ^= (uint16_t)((uint16_t)d[i] << 8);
    for (int b = 0; b < 8; b++)
      c = (c & 0x8000) ? (uint16_t)((c << 1) ^ 0x1021) : (uint16_t)(c << 1);
  }
  return c;
}

static uint32_t crc32_ieee(const uint8_t *d, size_t n) {
  uint32_t c = 0xFFFFFFFFu;
  for (size_t i = 0; i < n; i++) {
    c ^= d[i];
    for (int b = 0; b < 8; b++)
      c = (c >> 1) ^ (0xEDB88320u & (uint32_t)(-(int32_t)(c & 1)));
  }
  return ~c;
}

// ---- the fixture ----------------------------------------------------------
struct Rec {
  unsigned id, off, flen, plen, index;
  std::string group;
};

static std::vector<Rec> g_recs;
static std::string g_shape;
static unsigned g_layout = 0, g_hdrbytes = 0, g_imglen = 0, g_nrec = 0;
static uint32_t g_crc32 = 0;

static void load_table(const char *path) {
  FILE *f = fopen(path, "r");
  if (!f) {
    printf("FAIL: cannot open record table %s\n", path);
    exit(2);
  }
  char line[512];
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    char k[64], g[64], sh[128];
    unsigned id, off, flen, plen, idx, v;
    if (sscanf(line, "rec 0x%x %u %u %u %63s %u", &id, &off, &flen, &plen, g,
               &idx) == 6) {
      Rec r;
      r.id = id; r.off = off; r.flen = flen; r.plen = plen; r.index = idx;
      r.group = g;
      g_recs.push_back(r);
    } else if (sscanf(line, "crc32 0x%x", &v) == 1) {
      g_crc32 = v;
    } else if (sscanf(line, "shape %127s", sh) == 1) {
      g_shape = sh;
    } else if (sscanf(line, "%63s %u", k, &v) == 2) {
      if (!strcmp(k, "layout")) g_layout = v;
      else if (!strcmp(k, "hdrbytes")) g_hdrbytes = v;
      else if (!strcmp(k, "imglen")) g_imglen = v;
      else if (!strcmp(k, "nrec")) g_nrec = v;
    }
  }
  fclose(f);
}

// The record area, rebuilt byte for byte from the record list alone.
static std::vector<uint8_t> g_area;

static void build_area() {
  g_area.assign(g_imglen - g_hdrbytes - 4, 0);
  for (size_t n = 0; n < g_recs.size(); n++) {
    const Rec &r = g_recs[n];
    std::vector<uint8_t> fr(r.flen, 0);
    fr[0] = 0x17;
    fr[1] = 0x22;
    fr[2] = (uint8_t)g_layout;
    fr[3] = (uint8_t)r.id;
    fr[4] = (uint8_t)(r.plen >> 8);
    fr[5] = (uint8_t)(r.plen & 0xFF);
    for (unsigned j = 0; j < r.plen; j++)
      fr[8 + j] = (uint8_t)((r.id * 131u + j * 17u) & 0xFF);
    // the crc16 accumulates the header WITHOUT its own two bytes, then the
    // payload, as one stream -- the donor's crc16_f() in KL_acmp_nvm_shadow
    std::vector<uint8_t> s;
    s.insert(s.end(), fr.begin(), fr.begin() + 6);
    s.insert(s.end(), fr.begin() + 8, fr.begin() + 8 + r.plen);
    uint16_t c = crc16_ccitt(s.data(), s.size());
    fr[6] = (uint8_t)(c >> 8);
    fr[7] = (uint8_t)(c & 0xFF);
    memcpy(&g_area[r.off], fr.data(), r.flen);
  }
}

static void prove_byte_exact() {
  std::vector<uint8_t> img;
  const uint32_t hdr[10] = {0x324A4C4Bu, 0x00020000u, 7u,          g_nrec,
                            g_imglen,    0x44556677u, 0x00112233u, 0xCCDDEEFFu,
                            0x8899AABBu, g_layout};
  for (int w = 0; w < 10; w++)
    for (int b = 0; b < 4; b++) img.push_back((uint8_t)(hdr[w] >> (8 * b)));
  img.insert(img.end(), g_area.begin(), g_area.end());
  uint32_t c = crc32_ieee(img.data(), img.size());
  for (int b = 0; b < 4; b++) img.push_back((uint8_t)(c >> (8 * b)));

  check(img.size() == (size_t)g_imglen,
        "%s: the rebuilt image is %zu B, the fixture says %u", g_shape.c_str(),
        img.size(), g_imglen);
  check(c == g_crc32,
        "%s: the rebuilt image CRC-32 is 0x%08X, the encoder's is 0x%08X -- "
        "this C++ and scripts/check_nvm_record_space.py do not agree on the "
        "bytes of the image, so nothing measured against it means anything",
        g_shape.c_str(), c, g_crc32);
}

// ---------------------------------------------------------------------------
static const uint32_t IMG_BASE = 0x40000000u;

static Vnvm *dut = 0;
static std::vector<uint8_t> g_mem;
static bool g_watch_stale = false;
static int g_bad_pair = 0;

// Settle the combinational world for THIS cycle, including the one-cycle
// memory ack, so every output read afterwards is what the DUT will see at the
// coming posedge.
static void settle() {
  dut->eval();
  dut->mem_ack_i = dut->mem_req_o;
  if (dut->mem_req_o) {
    uint32_t a = dut->mem_addr_o - IMG_BASE;
    if ((size_t)a + 3 < g_mem.size()) {
      if (dut->mem_we_o) {
        for (int b = 0; b < 4; b++)
          if (dut->mem_wstrb_o & (1 << b))
            g_mem[a + b] = (uint8_t)(dut->mem_wdata_o >> (8 * b));
      }
      dut->mem_rdata_i = (uint32_t)g_mem[a] | ((uint32_t)g_mem[a + 1] << 8) |
                         ((uint32_t)g_mem[a + 2] << 16) |
                         ((uint32_t)g_mem[a + 3] << 24);
    } else {
      dut->mem_rdata_i = 0xDEADBEEFu;
    }
  }
  dut->eval();
}

static void posedge() {
  dut->clk_i = 1;
  dut->eval();
  dut->clk_i = 0;
  dut->eval();
  if (g_watch_stale && dut->nvm_backed_o && !dut->nvm_dirty_o &&
      dut->nvm_stale_o)
    g_bad_pair++;
}

static void tick() {
  settle();
  posedge();
}

static void csr_write(unsigned addr, uint32_t data) {
  dut->csr_sel_i = 1;
  dut->csr_we_i = 1;
  dut->csr_addr_i = addr;
  dut->csr_wdata_i = data;
  tick();
  dut->csr_sel_i = 0;
  dut->csr_we_i = 0;
  dut->csr_wdata_i = 0;
}

static void reset_dut() {
  dut->rst_n = 0;
  dut->csr_sel_i = dut->csr_we_i = 0;
  dut->dev_req_i = dut->dev_wvalid_i = dut->dev_rready_i = 0;
  for (int i = 0; i < 8; i++) tick();
  dut->rst_n = 1;
  tick();
}

// One device-face command. Returns true on dev_done_o, false on dev_err_o.
static bool dev_cmd(int op, unsigned region, unsigned offset, unsigned len,
                    std::vector<uint8_t> *rd, const uint8_t *wr) {
  dut->dev_req_i = 1;
  dut->dev_op_i = op;
  dut->dev_region_i = region;
  dut->dev_offset_i = offset;
  dut->dev_len_i = len;
  dut->dev_rready_i = 1;
  dut->dev_wvalid_i = wr ? 1 : 0;
  if (wr) dut->dev_wdata_i = wr[0];
  tick();
  dut->dev_req_i = 0;

  size_t wi = 0;
  for (int guard = 0; guard < 400000; guard++) {
    settle();
    bool done = dut->dev_done_o != 0;
    bool err = dut->dev_err_o != 0;
    if (rd && dut->dev_rvalid_o && dut->dev_rready_i)
      rd->push_back(dut->dev_rdata_o);
    if (wr && dut->dev_wvalid_i && dut->dev_wready_o) {
      wi++;
      if (wi < len) {
        dut->dev_wdata_i = wr[wi];
        dut->eval();
      }
    }
    posedge();
    if (done || err) {
      dut->dev_rready_i = 0;
      dut->dev_wvalid_i = 0;
      return done;
    }
  }
  dut->dev_rready_i = 0;
  dut->dev_wvalid_i = 0;
  check(false, "%s: a command on region 0x%02X never completed",
        g_shape.c_str(), region);
  return false;
}

// ---------------------------------------------------------------------------
static void program_map_tables() {
  // Firmware's job: the running sum of the framed lengths INSIDE each group.
  // The GROUP BASE is deliberately NOT programmed. The backend has to derive
  // it from the lengths it was given, which is exactly what a nominal stride
  // got wrong.
  for (int dir = 0; dir < 2; dir++) {
    const char *want = dir ? "MAPS_OUT" : "MAPS_IN";
    unsigned pref = 0;
    for (size_t n = 0; n < g_recs.size(); n++) {
      const Rec &r = g_recs[n];
      if (r.group != want) continue;
      csr_write(0x20u | (dir ? 0x10u : 0u) | (r.index & 0xFu),
                ((uint32_t)r.flen << 16) | pref);
      pref += r.flen;
    }
  }
}

static void test_regions() {
  for (size_t n = 0; n < g_recs.size(); n++) {
    const Rec &r = g_recs[n];
    std::vector<uint8_t> got;
    if (!dev_cmd(0 /*READ*/, r.id, 0, r.flen, &got, 0)) {
      check(false, "%s: a READ of record 0x%02X (%s[%u]) was REFUSED",
            g_shape.c_str(), r.id, r.group.c_str(), r.index);
      continue;
    }
    if (got.size() != (size_t)r.flen) {
      check(false, "%s: a READ of record 0x%02X returned %zu B, wanted %u",
            g_shape.c_str(), r.id, got.size(), r.flen);
      continue;
    }
    size_t bad = NOPOS;
    for (size_t j = 0; j < got.size(); j++)
      if (got[j] != g_area[r.off + j]) { bad = j; break; }
    check(bad == NOPOS,
          "%s: %s[%u] (record 0x%02X, %u framed bytes at area offset %u) reads "
          "the wrong span: byte %zu came back 0x%02X, the image holds 0x%02X. "
          "The backend resolved this record to a different place in the image",
          g_shape.c_str(), r.group.c_str(), r.index, r.id, r.flen, r.off,
          bad == NOPOS ? (size_t)0 : bad, bad == NOPOS ? 0 : got[bad],
          bad == NOPOS ? 0 : g_area[r.off + bad]);
  }

  // a partial read, so the offset adder is exercised as well as the base
  for (size_t n = 0; n < g_recs.size(); n++) {
    const Rec &r = g_recs[n];
    if (r.flen < 12) continue;
    std::vector<uint8_t> got;
    if (!dev_cmd(0, r.id, 8, 4, &got, 0)) {
      check(false, "%s: a partial READ of 0x%02X was refused", g_shape.c_str(),
            r.id);
      continue;
    }
    check(got.size() == 4 && !memcmp(got.data(), &g_area[r.off + 8], 4),
          "%s: a partial READ of 0x%02X at offset 8 returned the wrong bytes",
          g_shape.c_str(), r.id);
  }

  // a WRITE must land where a READ found the record
  for (size_t n = 0; n < g_recs.size(); n++) {
    const Rec &r = g_recs[n];
    if (r.group != "MAPS_OUT" || r.flen < 24) continue;
    uint8_t pat[8] = {0x5A, 0xA5, 0x00, 0xFF, 0x11, 0x22, 0x33, 0x44};
    if (!dev_cmd(1 /*WRITE*/, r.id, 16, 8, 0, pat)) {
      check(false, "%s: a WRITE into 0x%02X was refused", g_shape.c_str(),
            r.id);
      continue;
    }
    check(!memcmp(&g_mem[r.off + 16], pat, 8),
          "%s: a WRITE into %s[%u] at offset 16 did not land at area offset %u",
          g_shape.c_str(), r.group.c_str(), r.index, r.off + 16);
    memcpy(&g_mem[r.off + 16], &g_area[r.off + 16], 8);  // restore
  }

  // negative controls on the decode itself
  std::vector<uint8_t> got;
  check(!dev_cmd(0, 0x1A, 0, 4, &got, 0),
        "%s: a READ of unallocated region 0x1A was ACCEPTED", g_shape.c_str());
  got.clear();
  check(!dev_cmd(0, g_recs[0].id, 0, g_recs[0].flen + 1, &got, 0),
        "%s: a READ one byte past the end of record 0x%02X was ACCEPTED",
        g_shape.c_str(), g_recs[0].id);
}

// ---------------------------------------------------------------------------
// Section 9.2. CLK_HZ_P is 10 kHz in this build, so a "millisecond" is 10
// clocks and T_ALIVE_MS_P is 4.
static const int MS = 10;

static void hb() { csr_write(4, 1u << 0); }
static void commit_ack() { csr_write(4, 1u << 1); }
static void dirty_set() { csr_write(4, 1u << 3); }

static void idle_ms(int n) {
  for (int i = 0; i < n * MS + 2; i++) tick();
}

static void expect_bits(const char *what, int b, int d, int s) {
  check(dut->nvm_backed_o == b && dut->nvm_dirty_o == d &&
            dut->nvm_stale_o == s,
        "%s: %s -- read (backed=%d, dirty=%d, stale=%d), wanted (%d, %d, %d)",
        g_shape.c_str(), what, (int)dut->nvm_backed_o, (int)dut->nvm_dirty_o,
        (int)dut->nvm_stale_o, b, d, s);
}

static void test_stale() {
  g_watch_stale = true;

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

  g_watch_stale = false;
  check(g_bad_pair == 0,
        "%s: (backed=1, dirty=0, stale=1) was observable on %d cycle(s), and "
        "section 9.3 calls that row unreachable",
        g_shape.c_str(), g_bad_pair);
}

// ---------------------------------------------------------------------------
int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 2) {
    printf("usage: %s <record table>\n", argv[0]);
    return 2;
  }
  load_table(argv[1]);
  if (g_recs.empty() || !g_imglen) {
    printf("FAIL: record table %s carries no records\n", argv[1]);
    return 2;
  }
  build_area();
  prove_byte_exact();

  g_mem = g_area;
  g_mem.resize(g_mem.size() + 8, 0);

  dut = new Vnvm;
  dut->clk_i = 0;
  reset_dut();
  csr_write(0, IMG_BASE);   // R_IMG_BASE points at the RECORD AREA
  csr_write(1, (uint32_t)(g_imglen - g_hdrbytes - 4));
  program_map_tables();
  test_regions();
  test_stale();

  printf("nvm_backend[%s]: checks: %d  failures: %d\n", g_shape.c_str(),
         g_checks, g_fails);
  delete dut;
  return g_fails ? 1 : 0;
}

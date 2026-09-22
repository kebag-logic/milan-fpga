// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_aecp_desc_store suite — independent expectations, never DUT logic.
//
// The store keeps the 07 §3.3 entity model in the integrator's MAIN MEMORY and
// serves the µCPU's st_* face from an on-chip line buffer. So this harness is
// two independent models:
//
//   1. a LATENCY-INJECTING memory BFM. Its default first-word latency is 24
//      clocks and it is never zero: a store that only ever gets zero-latency
//      answers is untested against the thing that makes this hard (the
//      reference SoC measures ~1424 ns on a miss to main memory). The BFM also
//      plays a bridge that never accepts, and one that answers with an error.
//   2. an independent PARSER/BUILDER of the documented image format
//      (hdl/aecp/desc/gen_desc_image.py header + index map). Expectations are
//      computed from the parsed image and the IEEE field offsets, never from
//      anything the DUT produced.
//
// The suite also loads the generator's own example image, so generator and RTL
// are proven to agree on the format rather than merely on each other.
#include <array>
#include <map>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include "VKL_aecp_desc_store.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// KL_aecp_desc_store parameters this suite elaborates against
constexpr uint32_t DESC_BASE   = 0x20000000u;
constexpr uint32_t LINE_BYTES  = 576;
constexpr uint32_t IDX_ENTRIES = 32;
constexpr uint32_t NAME_ENTRIES = 256;
constexpr uint32_t MEM_TIMEOUT = 64;   // -GMEM_TIMEOUT_CYC_P in the Makefile

// state-port regions (KL_aecp_desc_store banner)
constexpr uint32_t RGN_DATA   = 0x00000;
constexpr uint32_t RGN_NADDR  = 0xB0000;
constexpr uint32_t RGN_NBASE  = 0xC0000;
constexpr uint32_t RGN_NCFG   = 0xD0000;
constexpr uint32_t RGN_LEN    = 0xE0000;
constexpr uint32_t RGN_LOCATE = 0xF0000;

// fault codes: plain integers, because they are compared against the 4-bit
// dbg_fault_o word the model drives, never mixed with each other
constexpr uint8_t F_NONE    = 0;
constexpr uint8_t F_MAGIC   = 1;
constexpr uint8_t F_VERSION = 2;
constexpr uint8_t F_CKSUM   = 3;
constexpr uint8_t F_NIDX    = 4;
constexpr uint8_t F_NNAME   = 5;
constexpr uint8_t F_DESCLEN = 6;
constexpr uint8_t F_MEMERR  = 7;
constexpr uint8_t F_TIMEOUT = 8;

constexpr uint16_t NAME_NONE = 0xFFFF;

// ===========================================================================
// an independent builder + parser of the documented image format
// ===========================================================================
struct Entry {
  uint16_t cfg;
  uint16_t type;
  uint16_t count;
  uint16_t len;
  uint16_t nbase;
  uint16_t stride;
  uint32_t off;
};

struct Image {
  std::vector<uint8_t> b;
  uint16_t n_config = 0;
  uint16_t n_entries = 0;
  uint16_t n_names = 0;
  uint16_t desc_max = 0;
  uint32_t index_off = 0;
  uint32_t names_off = 0;
  std::vector<Entry> ents;

  static void put16(std::vector<uint8_t>& v, size_t at, uint16_t x) {
    v[at] = uint8_t(x >> 8); v[at + 1] = uint8_t(x);
  }
  static void put32(std::vector<uint8_t>& v, size_t at, uint32_t x) {
    v[at] = uint8_t(x >> 24); v[at + 1] = uint8_t(x >> 16);
    v[at + 2] = uint8_t(x >> 8); v[at + 3] = uint8_t(x);
  }
  static uint16_t get16(const std::vector<uint8_t>& v, size_t at) {
    return uint16_t(uint16_t(v[at]) << 8 | v[at + 1]);
  }
  static uint32_t get32(const std::vector<uint8_t>& v, size_t at) {
    return uint32_t(v[at]) << 24 | uint32_t(v[at + 1]) << 16 |
           uint32_t(v[at + 2]) << 8 | uint32_t(v[at + 3]);
  }

  // parse a flat image produced by anyone (used on gen_desc_image.py output)
  bool parse() {
    if (b.size() < 32) return false;
    n_config  = get16(b, 6);
    n_entries = get16(b, 8);
    n_names   = get16(b, 10);
    index_off = get32(b, 12);
    names_off = get32(b, 16);
    desc_max  = get16(b, 24);
    ents.clear();
    for (uint32_t i = 0; i < n_entries; ++i) {
      size_t at = index_off + 16 * i;
      if (at + 16 > b.size()) return false;
      Entry e;
      e.cfg = get16(b, at); e.type = get16(b, at + 2);
      e.count = get16(b, at + 4); e.len = get16(b, at + 6);
      e.off = get32(b, at + 8); e.nbase = get16(b, at + 12);
      e.stride = get16(b, at + 14);
      ents.push_back(e);
    }
    return get32(b, 0) == 0x41454D49u && get16(b, 4) == 1;
  }

  // build one from scratch (the format spelled out again, independently)
  void build(const std::vector<Entry>& in,
             const std::vector<std::vector<uint8_t>>& bodies,
             const std::vector<std::string>& names,
             uint16_t n_cfg) {
    ents = in;
    uint32_t idx_off = 32;
    uint32_t cur = idx_off + 16 * uint32_t(in.size());
    cur = (cur + 7) & ~7u;
    std::vector<uint32_t> where;
    size_t bi = 0;
    for (size_t i = 0; i < ents.size(); ++i) {
      ents[i].off = cur;
      for (uint32_t k = 0; k < ents[i].count; ++k) {
        where.push_back(cur);
        cur += ents[i].stride;
        ++bi;
      }
    }
    (void)bi;
    uint32_t nm_off = cur;
    cur += 64 * uint32_t(names.size());
    uint32_t total = (cur + 7) & ~7u;

    b.assign(total, 0);
    for (size_t i = 0; i < bodies.size() && i < where.size(); ++i) {
      memcpy(&b[where[i]], bodies[i].data(), bodies[i].size());
    }
    for (size_t i = 0; i < names.size(); ++i) {
      memcpy(&b[nm_off + 64 * i], names[i].data(),
             names[i].size() > 64 ? 64 : names[i].size());
    }
    uint16_t dmax = 0;
    for (auto& e : ents) if (e.len > dmax) dmax = e.len;

    put32(b, 0, 0x41454D49u);
    put16(b, 4, 1);
    put16(b, 6, n_cfg);
    put16(b, 8, uint16_t(ents.size()));
    put16(b, 10, uint16_t(names.size()));
    put32(b, 12, idx_off);
    put32(b, 16, nm_off);
    put32(b, 20, total);
    put16(b, 24, dmax);
    put16(b, 26, 0);
    for (size_t i = 0; i < ents.size(); ++i) {
      size_t at = idx_off + 16 * i;
      put16(b, at, ents[i].cfg); put16(b, at + 2, ents[i].type);
      put16(b, at + 4, ents[i].count); put16(b, at + 6, ents[i].len);
      put32(b, at + 8, ents[i].off); put16(b, at + 12, ents[i].nbase);
      put16(b, at + 14, ents[i].stride);
    }
    reseal();
    n_config = n_cfg; n_entries = uint16_t(ents.size());
    n_names = uint16_t(names.size());
    index_off = idx_off; names_off = nm_off; desc_max = dmax;
  }

  // the checksum rule: the eight header u32 words sum to 0xFFFFFFFF
  void reseal() {
    uint32_t s = 0;
    for (int i = 0; i < 7; ++i) s += get32(b, size_t(4 * i));
    put32(b, 28, 0xFFFFFFFFu - s);
  }

  const Entry* find(uint16_t cfg, uint16_t type) const {
    for (auto& e : ents) if (e.cfg == cfg && e.type == type) return &e;
    return nullptr;
  }
};

// ===========================================================================
// the memory BFM
// ===========================================================================
struct Dram {
  VKL_aecp_desc_store* dut;
  std::vector<uint8_t> mem;         // content at DESC_BASE
  int  latency = 24;                // clocks from accept to the first beat
  bool refuse  = false;             // a bridge that never accepts
  int  err_at  = -1;                // answer this beat index with rsp_err
  int  gap     = 0;                 // idle clocks between beats

  bool busy = false;
  uint32_t addr = 0;
  int beats = 0;
  int idx = 0;
  int wait = 0;
  uint64_t reqs = 0;
  uint64_t beats_served = 0;

  explicit Dram(VKL_aecp_desc_store* d) : dut(d) {}

  uint64_t rd64(uint32_t a) const {
    uint64_t v = 0;
    for (int i = 0; i < 8; ++i) {
      uint32_t k = a + uint32_t(i);
      // outside the loaded image the bus answers a recognisable non-zero
      // pattern, so nothing can pass by reading uninitialised memory as 0
      uint8_t byte = (k < mem.size()) ? mem[k] : 0xA5;
      v = (v << 8) | byte;
    }
    return v;
  }

  void drive() {
    dut->mem_req_ready_i = (!busy && !refuse) ? 1 : 0;
    dut->mem_rsp_valid_i = 0;
    dut->mem_rsp_data_i  = 0;
    dut->mem_rsp_last_i  = 0;
    dut->mem_rsp_err_i   = 0;
    if (busy && wait == 0 && idx < beats) {
      dut->mem_rsp_valid_i = 1;
      dut->mem_rsp_data_i  = rd64(addr - DESC_BASE + uint32_t(8 * idx));
      dut->mem_rsp_last_i  = (idx == beats - 1) ? 1 : 0;
      dut->mem_rsp_err_i   = (err_at >= 0 && idx == err_at) ? 1 : 0;
    }
  }

  void update() {
    if (!busy) {
      if (!refuse && dut->mem_req_valid_o) {
        busy  = true;
        addr  = dut->mem_req_addr_o;
        beats = dut->mem_req_beats_o;
        idx   = 0;
        wait  = latency;
        ++reqs;
      }
    } else if (wait > 0) {
      --wait;
    } else if (dut->mem_rsp_valid_i && dut->mem_rsp_ready_o) {
      ++beats_served;
      if (dut->mem_rsp_err_i) { busy = false; }
      else if (++idx >= beats) { busy = false; }
      else { wait = gap; }
    }
  }
};

// ===========================================================================
// harness
// ===========================================================================
struct H {
  VKL_aecp_desc_store* dut;
  Dram dram;
  bool     rv = false;
  bool     err = false;
  uint64_t rdata = 0;

  explicit H(VKL_aecp_desc_store* d) : dut(d), dram(d) {}

  void tick() {
    dram.drive();
    dut->clk_i = 0; dut->eval();
    rv    = dut->st_rvalid_o;
    err   = dut->st_err_o;
    rdata = dut->st_rdata_o;
    dram.update();
    dut->clk_i = 1; dut->eval();
  }

  void reset() {
    dut->rst_n = 0;
    dut->st_req_i = 0; dut->st_we_i = 0; dut->st_name_i = 0;
    dut->st_addr_i = 0; dut->st_wdata_i = 0; dut->st_wstrb_i = 0;
    dram.busy = false; dram.wait = 0;
    for (int i = 0; i < 6; ++i) tick();
    dut->rst_n = 1;
  }

  void settle(int n) { for (int i = 0; i < n; ++i) tick(); }

  // one read on the state port; returns false if it never answered
  bool rd(uint32_t addr, bool name, uint64_t key, int budget = 6000) {
    dut->st_req_i = 1; dut->st_we_i = 0; dut->st_name_i = name ? 1 : 0;
    dut->st_addr_i = addr; dut->st_wdata_i = key; dut->st_wstrb_i = 0;
    for (int i = 0; i < budget; ++i) {
      tick();
      if (rv) { dut->st_req_i = 0; tick(); return true; }
    }
    dut->st_req_i = 0; tick();
    return false;
  }

  void wr(uint32_t addr, bool name, uint64_t data, uint8_t strb) {
    dut->st_req_i = 1; dut->st_we_i = 1; dut->st_name_i = name ? 1 : 0;
    dut->st_addr_i = addr; dut->st_wdata_i = data; dut->st_wstrb_i = strb;
    for (int i = 0; i < 6000; ++i) {
      bool ready = dut->st_ready_o;
      tick();
      if (ready) break;
    }
    dut->st_req_i = 0; dut->st_we_i = 0; dut->st_wstrb_i = 0;
    tick();
  }

  bool locate(uint16_t cfg, uint16_t type, uint16_t index) {
    uint64_t key = (uint64_t(index) << 32) | (uint64_t(type) << 16) | cfg;
    return rd(RGN_LOCATE, false, key);
  }

  bool boot(const Image& img, int budget = 60000) {
    dram.mem = img.b;
    reset();
    for (int i = 0; i < budget; ++i) {
      tick();
      if (dut->dbg_img_valid_o || dut->dbg_fault_o != F_NONE) return true;
    }
    return false;
  }
};

static uint64_t img64(const std::vector<uint8_t>& b, uint32_t at) {
  uint64_t v = 0;
  for (int i = 0; i < 8; ++i) {
    uint32_t k = at + uint32_t(i);
    v = (v << 8) | ((k < b.size()) ? b[k] : 0xA5);
  }
  return v;
}

// Descriptor reads use the writable name table as their source of truth.
// This independent expectation overlays the two ENTITY names at their IEEE
// offsets and every other named descriptor's object_name at byte 4.
static uint64_t served64(const Image& img, const Entry& e, uint16_t member,
                         uint32_t desc_at, uint32_t lane_at) {
  uint64_t v = 0;
  for (uint32_t i = 0; i < 8; ++i) {
    const uint32_t off = lane_at + i;
    uint8_t byte = (desc_at + off < img.b.size()) ? img.b[desc_at + off] : 0xA5;
    if (e.nbase != NAME_NONE) {
      uint32_t name = uint32_t(e.nbase) + member;
      int32_t name_byte = -1;
      if (e.type == 0x0000) {
        if (off >= 48 && off < 112) name_byte = int32_t(off - 48);
        if (off >= 180 && off < 244) {
          ++name;
          name_byte = int32_t(off - 180);
        }
      } else if (off >= 4 && off < 68) {
        name_byte = int32_t(off - 4);
      }
      if (name_byte >= 0) {
        byte = img.b[img.names_off + 64u * name + uint32_t(name_byte)];
      }
    }
    v = (v << 8) | byte;
  }
  return v;
}

// a small synthetic model: two AUDIO_CLUSTERs of 90 bytes (not a multiple of
// 8) so the stride path is exercised, plus a 4-byte-typed marker descriptor
static Image synth_two_of_a_type() {
  std::vector<Entry> ents = {
    {0, 0x0000, 1, 312, 0, 312, 0},
    {0, 0x0014, 2, 90,  2, 96, 0},
    {0, 0x0024, 1, 78,  NAME_NONE, 80, 0},
  };
  std::vector<std::vector<uint8_t>> bodies;
  auto mk = [](uint16_t type, uint16_t ix, size_t len) {
    std::vector<uint8_t> v(len, 0);
    v[0] = uint8_t(type >> 8); v[1] = uint8_t(type);
    v[2] = uint8_t(ix >> 8);   v[3] = uint8_t(ix);
    for (size_t k = 4; k < len; ++k) v[k] = uint8_t((type + ix * 7 + k) & 0xFF);
    return v;
  };
  bodies.push_back(mk(0x0000, 0, 312));
  bodies.push_back(mk(0x0014, 0, 90));
  bodies.push_back(mk(0x0014, 1, 90));
  bodies.push_back(mk(0x0024, 0, 78));
  Image im;
  im.build(ents, bodies, {"entity", "group", "cluster0", "cluster1"}, 1);
  return im;
}

// More than one 9-bit memory request can carry. The DUT must split this
// table into whole-name chunks and preserve the absolute RAM address across
// the boundary.
static Image synth_many_names() {
  Entry ent = {0, 0x0000, 1, 312, 0, 312, 0};
  std::vector<uint8_t> body(312, 0);
  std::vector<std::string> names;
  for (unsigned i = 0; i < 80; ++i) {
    char text[32];
    snprintf(text, sizeof text, "chunked-name-%03u", i);
    names.push_back(text);
  }
  memcpy(body.data() + 48, names[0].data(), names[0].size());
  memcpy(body.data() + 180, names[1].data(), names[1].size());
  Image im;
  im.build({ent}, {body}, names, 1);
  return im;
}

// The shape a real Milan station has and the uniform-stride assumption could
// not express: ONE descriptor type whose members differ in length. STREAM_INPUT
// 0 is a 148-byte AAF sink (two formats), STREAM_INPUT 1 a 140-byte CRF sink
// (one), STREAM_INPUT 2 a second AAF sink - so the type splits into THREE runs
// and index 2 is only reachable by accumulating the two before it. Strides
// differ between runs (152 vs 144) and the third run repeats an earlier
// length, which a "remember the last length" shortcut would get wrong.
//
// 1722.1-2021 §7.2.6 sizes each stream descriptor by its own
// number_of_formats, and Milan §5.3.3.4 forbids one stream carrying both AAF
// and CRF, so this is not a corner case - it is the ordinary shape.
//
// The ABSOLUTE lengths are arbitrary and not Table 7-8's (which would make
// these 138+8*2 = 154 and 138+8*1 = 146). Only the 8-byte DIFFERENCE of one
// format carries meaning here: the store reads no descriptor field, so what is
// under test is the index map's run arithmetic, never a layout.
static Image synth_mixed_lengths() {
  std::vector<Entry> ents = {
    {0, 0x0000, 1, 312, 0,         312, 0},
    {0, 0x0005, 1, 148, NAME_NONE, 152, 0},   // index 0     AAF, N=2
    {0, 0x0005, 1, 140, NAME_NONE, 144, 0},   // index 1     CRF, N=1
    {0, 0x0005, 1, 148, NAME_NONE, 152, 0},   // index 2     AAF, N=2
    {0, 0x0024, 1, 78,  NAME_NONE, 80,  0},
  };
  std::vector<std::vector<uint8_t>> bodies;
  auto mk = [](uint16_t type, uint16_t ix, size_t len) {
    std::vector<uint8_t> v(len, 0);
    v[0] = uint8_t(type >> 8); v[1] = uint8_t(type);
    v[2] = uint8_t(ix >> 8);   v[3] = uint8_t(ix);
    // keyed on the index so a run mix-up shows up as wrong BYTES, not merely
    // as a wrong length - two runs here share a length
    for (size_t k = 4; k < len; ++k) v[k] = uint8_t((type + ix * 31 + k) & 0xFF);
    return v;
  };
  bodies.push_back(mk(0x0000, 0, 312));
  bodies.push_back(mk(0x0005, 0, 148));
  bodies.push_back(mk(0x0005, 1, 140));
  bodies.push_back(mk(0x0005, 2, 148));
  bodies.push_back(mk(0x0024, 0, 78));
  Image im;
  im.build(ents, bodies, {"entity", "group"}, 1);
  return im;
}

namespace {

//! Owns the model, the memory BFM, the parsed reference image and the tally,
//! so every phase below drives the same store and counts into the same
//! summary line.
class DescStoreSuite {
 public:
  DescStoreSuite() : dut(model.get()), h(dut) {}

  int run();

 private:
  //! False when the generator's image could not be read at all - the one
  //! condition that ends the run before any phase gets to count.
  bool load_the_generators_example_image();
  // walk every descriptor of an image and check the served bytes, byte-exactly
  void check_all_descriptors(const Image& img, const char* tag);
  void boots_from_the_generated_image();
  void serves_every_generated_descriptor_byte_exact();
  void index_map_boundaries_are_exact();
  void locate_misses_are_answered_cleanly();
  void the_name_region_is_the_writable_one();
  void chunked_name_tables_cross_the_burst_boundary();
  void the_image_is_read_only_at_run_time();
  void back_to_back_reads_with_req_held_high();
  void a_longer_memory_latency_changes_nothing();
  void an_unloaded_region_serves_nothing();
  void an_all_zero_region_serves_nothing();
  void a_stale_checksum_is_refused();
  void a_future_layout_version_is_refused();
  void too_many_index_entries_is_refused();
  void too_many_names_is_refused();
  void a_descriptor_past_the_line_buffer_is_refused();
  void a_late_image_load_self_heals();
  void the_heal_precedes_the_first_answer();
  void an_absent_bridge_times_out();
  void a_fetch_error_becomes_a_miss();
  void two_descriptors_of_one_type_are_strided();
  void one_type_of_several_runs_indexes_across_them();
  void an_inconsistent_stride_is_refused();
  void a_zero_length_entry_is_refused();

  const milan::tb::Model<VKL_aecp_desc_store> model;
  VKL_aecp_desc_store* const dut;
  H h;
  Image gen;
  int checks = 0;
  int fails = 0;
};

// ---------------------------------------------------------------------------
// walk every descriptor of an image and check the served bytes, byte-exactly
// ---------------------------------------------------------------------------
void DescStoreSuite::check_all_descriptors(const Image& img, const char* tag) {
  // A descriptor type may occupy SEVERAL entries - one per run of equal-length
  // descriptors - so an entry's members are not indices 0..count-1 but
  // first..first+count-1, where `first` is the number of indices the earlier
  // runs of the same (cfg, type) already covered. Tracked here independently
  // of the DUT, which is the point: if the RTL's own running base drifts, the
  // absolute index this asks for stops matching the bytes it gets.
  std::map<std::pair<uint16_t, uint16_t>, uint16_t> first;
  for (const Entry& e : img.ents) {
    const std::pair<uint16_t, uint16_t> key{e.cfg, e.type};
    const uint16_t run0 = first[key];
    first[key] = uint16_t(run0 + e.count);
    for (uint16_t k = 0; k < e.count; ++k) {
      const uint16_t ix = uint16_t(run0 + k);
      CHECK(h.locate(e.cfg, e.type, ix), "%s locate cfg %u type 0x%04X ix %u "
            "never answered", tag, e.cfg, e.type, ix);
      CHECK(!h.err, "%s locate cfg %u type 0x%04X ix %u errored",
            tag, e.cfg, e.type, ix);
      CHECK(h.rdata == 0, "%s locate base got %llu (line-buffer origin is 0)",
            tag, static_cast<unsigned long long>(h.rdata));

      CHECK(h.rd(RGN_LEN, false, 0) && !h.err && h.rdata == e.len,
            "%s type 0x%04X ix %u length got %llu want %u",
            tag, e.type, ix, static_cast<unsigned long long>(h.rdata), e.len);
      const uint16_t want_nbase = (e.nbase == NAME_NONE)
                                  ? NAME_NONE : uint16_t(e.nbase + k);
      CHECK(h.rd(RGN_NBASE, false, 0) && !h.err && h.rdata == want_nbase,
            "%s type 0x%04X name_base got %llu want %u",
            tag, e.type, static_cast<unsigned long long>(h.rdata), want_nbase);

      uint32_t lanes = (e.len + 7u) / 8u;
      // `e.off` is the offset of this RUN's first member, so the stride
      // multiplies the run-relative index. Using the absolute one would read
      // past the run whenever an earlier run of the same type exists.
      uint32_t base = e.off + uint32_t(e.stride) * k;
      for (uint32_t l = 0; l < lanes; ++l) {
        uint64_t want = served64(img, e, k, base, 8 * l);
        CHECK(h.rd(RGN_DATA + 8 * l, false, 0) && h.rdata == want,
              "%s type 0x%04X ix %u lane %u got %016llx want %016llx",
              tag, e.type, ix, l, static_cast<unsigned long long>(h.rdata),
              static_cast<unsigned long long>(want));
      }
      // a lane past the descriptor must read as zero, never as the next one
      CHECK(h.rd(RGN_DATA + 8 * lanes, false, 0) && h.rdata == 0,
            "%s type 0x%04X lane past the end got %016llx",
            tag, e.type, static_cast<unsigned long long>(h.rdata));
    }
  }
}

// ---- the generator's own example image ---------------------------------
bool DescStoreSuite::load_the_generators_example_image() {
  {
    FILE* f = fopen("image.bin", "rb");
    if (!f) { printf("0 checks: 0 PASS, 1 FAIL\nFAIL: image.bin missing\n");
              return false; }
    fseek(f, 0, SEEK_END); long n = ftell(f); fseek(f, 0, SEEK_SET);
    gen.b.resize(size_t(n));
    if (fread(gen.b.data(), 1, size_t(n), f) != size_t(n)) {
      printf("0 checks: 0 PASS, 1 FAIL\nFAIL: image.bin short read\n");
      fclose(f); return false;
    }
    fclose(f);
  }
  CHECK(gen.parse(), "gen_desc_image.py output does not parse as the "
        "documented format");
  CHECK(gen.n_entries == 8, "example has %u index entries, want the 07 §3.1 "
        "eight-descriptor tree", gen.n_entries);
  return true;
}

// ---- G1: boot from the generated image ----------------------------------
void DescStoreSuite::boots_from_the_generated_image() {
  CHECK(h.boot(gen), "G1 boot walk never finished");
  CHECK(dut->dbg_img_valid_o == 1, "G1 image not valid");
  CHECK(dut->dbg_fault_o == F_NONE, "G1 fault %u",
        static_cast<unsigned>(dut->dbg_fault_o));
  CHECK(h.rd(RGN_NCFG, false, 0) && h.rdata == gen.n_config,
        "G1 configurations_count got %llu want %u",
        static_cast<unsigned long long>(h.rdata), gen.n_config);
}

// ---- G2: every descriptor of the generated image, byte-exact ------------
void DescStoreSuite::serves_every_generated_descriptor_byte_exact() {
  check_all_descriptors(gen, "G2");
}

// ---- G3: index-map boundaries -------------------------------------------
void DescStoreSuite::index_map_boundaries_are_exact() {
  // first entry (lowest type) and last entry (highest) must BOTH be found:
  // a scan that stops one early or runs one past fails exactly here
  CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err,
        "G3 first index entry (type 0x%04X) missed", gen.ents.front().type);
  CHECK(h.locate(0, gen.ents.back().type, 0) && !h.err,
        "G3 last index entry (type 0x%04X) missed", gen.ents.back().type);
  // a type just past the last one must MISS
  CHECK(h.locate(0, uint16_t(gen.ents.back().type + 1), 0) && h.err,
        "G3 type past the last entry was served");
  // a type below the first one must MISS (there is no type < ENTITY, so use a
  // hole in the middle: 0x0003 sits between CONFIGURATION and STREAM_INPUT)
  CHECK(h.locate(0, 0x0003, 0) && h.err, "G3 hole type 0x0003 was served");
}

// ---- G4: locate misses ---------------------------------------------------
void DescStoreSuite::locate_misses_are_answered_cleanly() {
  CHECK(h.locate(0, 0x0099, 0) && h.err, "G4 unknown type served");
  CHECK(h.locate(0, gen.ents.front().type, 1) && h.err,
        "G4 descriptor_index past count served");
  CHECK(h.locate(1, gen.ents.front().type, 0) && h.err,
        "G4 unknown configuration served");
  uint16_t miss0 = dut->dbg_locate_miss_o;
  CHECK(miss0 >= 5, "G4 miss counter %u did not move", miss0);

  // a miss must not leave a servable descriptor behind: re-locating a good
  // one afterwards must still work (the machine is not wedged)
  CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err,
        "G4 store wedged after a miss");
}

// ---- G5: the name region (07 §3.4) --------------------------------------
void DescStoreSuite::the_name_region_is_the_writable_one() {
  for (uint16_t e = 0; e < gen.n_names; ++e) {
    uint64_t want = img64(gen.b, gen.names_off + 64u * e);
    CHECK(h.rd(uint32_t(e) * 64u, true, 0) && h.rdata == want,
          "G5 name entry %u lane 0 got %016llx want %016llx",
          e, static_cast<unsigned long long>(h.rdata),
          static_cast<unsigned long long>(want));
  }
  // the name region is the ONE writable one — it is overlay, not image
  h.wr(64u * 1u + 8u, true, 0x4E45575F4E414D45ull, 0xFF);
  CHECK(h.rd(64u * 1u + 8u, true, 0) && h.rdata == 0x4E45575F4E414D45ull,
        "G5 name write did not stick: got %016llx",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_DATA + 184u, false, 0)
        && h.rdata == 0x6E20456E4E45575Full,
        "G5 SET_NAME first descriptor lane is stale: %016llx",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_DATA + 192u, false, 0)
        && h.rdata == 0x4E414D4500000000ull,
        "G5 SET_NAME second descriptor lane is stale: %016llx",
        static_cast<unsigned long long>(h.rdata));
  // byte strobes
  h.wr(64u * 1u + 8u, true, 0x00000000000000FFull, 0x01);
  CHECK(h.rd(64u * 1u + 8u, true, 0) &&
        h.rdata == 0x4E45575F4E414DFFull,
        "G5 byte-strobed name write got %016llx",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_DATA + 192u, false, 0)
        && h.rdata == 0x4E414DFF00000000ull,
        "G5 byte-strobed name is stale in READ_DESCRIPTOR: %016llx",
        static_cast<unsigned long long>(h.rdata));

  // Semantic name_index lookup is intentionally separate from the 64-byte
  // overlay address. ENTITY exposes entity_name 0 and group_name 1.
  CHECK(h.rd(RGN_NADDR, false, 0) && !h.err && h.rdata == 0,
        "G5 ENTITY name_index 0 address got %llu",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_NADDR, false, 1) && !h.err && h.rdata == 64,
        "G5 ENTITY name_index 1 address got %llu",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_NADDR, false, 2) && h.err && h.rdata == 0,
        "G5 ENTITY name_index 2 was accepted");

  CHECK(h.locate(0, 0x0001, 0) && !h.err, "G5 locate CONFIGURATION");
  CHECK(h.rd(RGN_NADDR, false, 0) && !h.err && h.rdata == 128,
        "G5 CONFIGURATION name_index 0 address got %llu",
        static_cast<unsigned long long>(h.rdata));
  CHECK(h.rd(RGN_NADDR, false, 1) && h.err && h.rdata == 0,
        "G5 non-ENTITY name_index 1 was accepted");

  CHECK(h.locate(0, 0x0024, 0) && !h.err, "G5 locate CLOCK_DOMAIN");
  CHECK(h.rd(RGN_NADDR, false, 0) && !h.err && h.rdata == 512,
        "G5 CLOCK_DOMAIN name address got %llu",
        static_cast<unsigned long long>(h.rdata));
}

// ---- G5b: name tables larger than one 511-beat request -----------------
void DescStoreSuite::chunked_name_tables_cross_the_burst_boundary() {
  {
    const Image many = synth_many_names();
    CHECK(h.boot(many), "G5b chunked name-table boot never finished");
    CHECK(dut->dbg_img_valid_o == 1, "G5b chunked image not valid");
    const uint32_t last = many.n_names - 1;
    const uint64_t want = img64(many.b, many.names_off + 64u * last);
    CHECK(h.rd(64u * last, true, 0) && h.rdata == want,
          "G5b final name after the burst boundary got %016llx want %016llx",
          static_cast<unsigned long long>(h.rdata),
          static_cast<unsigned long long>(want));
    CHECK(h.boot(gen), "G5b generator image did not restore");
  }
}

// ---- G6: the image is READ-ONLY at run time (07 §2) ---------------------
void DescStoreSuite::the_image_is_read_only_at_run_time() {
  {
    CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err, "G6 relocate");
    uint64_t before = 0;
    CHECK(h.rd(RGN_DATA, false, 0), "G6 pre-read");
    before = h.rdata;
    uint16_t ro0 = dut->dbg_ro_write_o;
    h.wr(RGN_DATA, false, 0xDEADBEEFDEADBEEFull, 0xFF);
    CHECK(dut->dbg_ro_write_o == ro0 + 1,
          "G6 read-only write not counted (%u -> %u)",
          ro0, static_cast<unsigned>(dut->dbg_ro_write_o));
    CHECK(h.rd(RGN_DATA, false, 0) && h.rdata == before,
          "G6 a write reached the image: %016llx -> %016llx",
          static_cast<unsigned long long>(before),
          static_cast<unsigned long long>(h.rdata));
  }
}

// ---- G7: back-to-back reads with st_req held high -----------------------
void DescStoreSuite::back_to_back_reads_with_req_held_high() {
  // the µCPU never drops st_req between two consecutive state ops; a store
  // that latched the request edge would deadlock here
  {
    CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err, "G7 relocate");
    dut->st_req_i = 1; dut->st_we_i = 0; dut->st_name_i = 0;
    dut->st_wstrb_i = 0; dut->st_wdata_i = 0;
    int answered = 0;
    std::array<uint64_t, 2> got = {0, 0};
    dut->st_addr_i = RGN_DATA;
    for (int i = 0; i < 200 && answered < 2; ++i) {
      h.tick();
      if (h.rv) {
        got[answered++] = h.rdata;
        if (answered == 1) dut->st_addr_i = RGN_DATA + 8;   // no req gap
      }
    }
    dut->st_req_i = 0; h.tick();
    CHECK(answered == 2, "G7 only %d of 2 held-request reads answered",
          answered);
    CHECK(got[0] == img64(gen.b, gen.ents.front().off) &&
          got[1] == img64(gen.b, gen.ents.front().off + 8),
          "G7 held-request lanes %016llx %016llx",
          static_cast<unsigned long long>(got[0]),
          static_cast<unsigned long long>(got[1]));
  }
}

// ---- G8: a longer memory latency changes nothing ------------------------
void DescStoreSuite::a_longer_memory_latency_changes_nothing() {
  h.dram.latency = 47;
  h.dram.gap = 2;
  CHECK(h.boot(gen), "G8 boot at latency 47");
  CHECK(dut->dbg_img_valid_o == 1, "G8 image not valid at latency 47");
  {
    const Entry& e = gen.ents.front();
    CHECK(h.locate(0, e.type, 0) && !h.err, "G8 locate at latency 47");
    uint32_t lanes = (e.len + 7u) / 8u;
    for (uint32_t l = 0; l < lanes; ++l) {
      CHECK(h.rd(RGN_DATA + 8 * l, false, 0) &&
            h.rdata == img64(gen.b, e.off + 8 * l),
            "G8 lane %u differs at latency 47", l);
    }
  }
  h.dram.latency = 24;
  h.dram.gap = 0;
}

// ---- U1: SOFTWARE HAS NOT LOADED THE IMAGE ------------------------------
void DescStoreSuite::an_unloaded_region_serves_nothing() {
  // uninitialised DRAM is not a structural zero, so the store must recognise
  // it by the magic/version/checksum header and serve NOTHING
  {
    Image junk;
    junk.b.assign(4096, 0xA5);
    CHECK(h.boot(junk), "U1 walk never settled on garbage");
    CHECK(dut->dbg_img_valid_o == 0, "U1 garbage region was accepted");
    CHECK(dut->dbg_fault_o == F_MAGIC, "U1 fault %u want MAGIC",
          static_cast<unsigned>(dut->dbg_fault_o));
    // every locate must miss, and nothing plausible may come back
    CHECK(h.locate(0, 0x0000, 0) && h.err, "U1 ENTITY served from garbage");
    CHECK(h.rd(RGN_LEN, false, 0) && h.rdata == 0,
          "U1 a length (%llu) was reported for an unloaded image",
          static_cast<unsigned long long>(h.rdata));
    CHECK(h.rd(RGN_DATA, false, 0) && h.rdata == 0,
          "U1 descriptor bytes %016llx came back from an unloaded image",
          static_cast<unsigned long long>(h.rdata));
    CHECK(h.rd(RGN_NCFG, false, 0) && h.rdata == 0,
          "U1 configurations_count %llu from an unloaded image",
          static_cast<unsigned long long>(h.rdata));
  }
}

// ---- U2: all-zero DRAM (the other shape of "not loaded") ----------------
void DescStoreSuite::an_all_zero_region_serves_nothing() {
  {
    Image zeros;
    zeros.b.assign(4096, 0x00);
    CHECK(h.boot(zeros), "U2 walk never settled on a zeroed region");
    CHECK(dut->dbg_img_valid_o == 0, "U2 a zeroed region was accepted");
    CHECK(h.locate(0, 0x0000, 0) && h.err, "U2 ENTITY served from zeros");
  }
}

// ---- U3: a TRUNCATED / corrupted load survives magic but not checksum ---
void DescStoreSuite::a_stale_checksum_is_refused() {
  {
    Image bad = gen;
    bad.b[26] ^= 0x5A;                 // a reserved header byte, checksum stale
    CHECK(h.boot(bad), "U3 walk never settled");
    CHECK(dut->dbg_img_valid_o == 0, "U3 a stale-checksum image was accepted");
    CHECK(dut->dbg_fault_o == F_CKSUM, "U3 fault %u want CKSUM",
          static_cast<unsigned>(dut->dbg_fault_o));
    CHECK(h.locate(0, 0x0000, 0) && h.err, "U3 served a corrupted image");
  }
}

// ---- U4: wrong layout version -------------------------------------------
void DescStoreSuite::a_future_layout_version_is_refused() {
  {
    Image bad = gen;
    Image::put16(bad.b, 4, 2);
    bad.reseal();
    CHECK(h.boot(bad), "U4 walk never settled");
    CHECK(dut->dbg_fault_o == F_VERSION, "U4 fault %u want VERSION",
          static_cast<unsigned>(dut->dbg_fault_o));
    CHECK(dut->dbg_img_valid_o == 0, "U4 a future layout was accepted");
  }
}

// ---- U5: more index entries than the on-chip cache holds ----------------
void DescStoreSuite::too_many_index_entries_is_refused() {
  {
    Image bad = gen;
    Image::put16(bad.b, 8, uint16_t(IDX_ENTRIES + 1));
    bad.reseal();
    CHECK(h.boot(bad), "U5 walk never settled");
    CHECK(dut->dbg_fault_o == F_NIDX, "U5 fault %u want NIDX",
          static_cast<unsigned>(dut->dbg_fault_o));
    CHECK(h.locate(0, 0x0000, 0) && h.err,
          "U5 served a model that does not fit the index cache");
  }
}

// ---- U6: more names than the on-chip overlay holds ----------------------
void DescStoreSuite::too_many_names_is_refused() {
  {
    Image bad = gen;
    Image::put16(bad.b, 10, uint16_t(NAME_ENTRIES + 1));
    bad.reseal();
    CHECK(h.boot(bad), "U6 walk never settled");
    CHECK(dut->dbg_fault_o == F_NNAME, "U6 fault %u want NNAME",
          static_cast<unsigned>(dut->dbg_fault_o));
  }
}

// ---- U7: a descriptor longer than the line buffer -----------------------
void DescStoreSuite::a_descriptor_past_the_line_buffer_is_refused() {
  {
    Image bad = gen;
    Image::put16(bad.b, 24, uint16_t(LINE_BYTES + 8));
    bad.reseal();
    CHECK(h.boot(bad), "U7 walk never settled");
    CHECK(dut->dbg_fault_o == F_DESCLEN, "U7 fault %u want DESCLEN",
          static_cast<unsigned>(dut->dbg_fault_o));
    CHECK(h.locate(0, 0x0000, 0) && h.err,
          "U7 served an image whose descriptors do not fit the line");
  }
}

// ---- U8: SELF-HEAL — software loads late --------------------------------
void DescStoreSuite::a_late_image_load_self_heals() {
  {
    Image junk;
    junk.b.assign(4096, 0xA5);
    CHECK(h.boot(junk), "U8 garbage boot");
    CHECK(h.locate(0, 0x0000, 0) && h.err, "U8 pre-load locate must miss");
    h.dram.mem = gen.b;                       // software loads the image NOW
    bool healed = false;
    for (int i = 0; i < 40 && !healed; ++i) {
      if (h.locate(0, 0x0000, 0) && !h.err) healed = true;
    }
    CHECK(healed, "U8 a late image load never healed without a reset");
    CHECK(dut->dbg_img_valid_o == 1, "U8 image not valid after the late load");
    CHECK(h.rd(RGN_DATA, false, 0) &&
          h.rdata == img64(gen.b, gen.ents.front().off),
          "U8 healed descriptor bytes wrong");
  }
}

// ---- U9: HEAL BEFORE ANSWER - the silicon arrangement -------------------
void DescStoreSuite::the_heal_precedes_the_first_answer() {
  // (r49a/w3a evidence: the store parks at boot against empty memory, the
  //  loader lands the image later, and the FIRST wire command used to miss
  //  because the re-arm came after the answer. The first locate after the
  //  load must now trigger the walk, stall through it, and SERVE.)
  {
    h.dram.refuse = true;                     // pre-handover: memory absent
    h.reset();
    bool parked = false;
    for (int i = 0; i < 4 * int(MEM_TIMEOUT) + 200 && !parked; ++i) {
      h.tick();
      if (dut->dbg_fault_o != F_NONE) parked = true;
    }
    CHECK(parked, "U9 the boot walk did not park against absent memory");
    CHECK(dut->dbg_img_valid_o == 0, "U9 parked but image claims valid");
    h.dram.refuse = false;                    // handover: memory appears
    h.dram.mem = gen.b;                       // ...with the image loaded
    CHECK(h.locate(0, gen.ents.front().type, 0),
          "U9 the first post-load locate never answered");
    CHECK(!h.err,
          "U9 THE FIRST post-load locate missed - the answer preceded the heal");
    CHECK(dut->dbg_img_valid_o == 1, "U9 the heal walk did not validate");
    CHECK(h.rd(RGN_DATA, false, 0) &&
          h.rdata == img64(gen.b, gen.ents.front().off),
          "U9 the first-served descriptor bytes are wrong");
    CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err,
          "U9 the second command must serve too");
    //! ...and a first locate for a descriptor the fresh image genuinely
    //! lacks is the honest miss FROM THE WALKED image, not the parked state
    h.dram.refuse = true;
    h.reset();
    parked = false;
    for (int i = 0; i < 4 * int(MEM_TIMEOUT) + 200 && !parked; ++i) {
      h.tick();
      if (dut->dbg_fault_o != F_NONE) parked = true;
    }
    h.dram.refuse = false;
    h.dram.mem = gen.b;
    CHECK(h.locate(0, 0x0099, 0) && h.err,
          "U9 a genuinely absent descriptor must still miss after the heal");
    CHECK(dut->dbg_img_valid_o == 1,
          "U9 ...with the image validated by that same walk");

    //! ...and the RGN_NCFG pseudo-register heals the same way: it is the
    //! register E_RDESC range-checks BEFORE it ever locates, so a parked 0
    //! here is exactly the w3a silicon race (first READ_DESCRIPTOR answered
    //! BAD_ARGUMENTS) - the first read after the handover must answer the
    //! walked configurations_count, not the parked zero
    h.dram.refuse = true;
    h.reset();
    parked = false;
    for (int i = 0; i < 4 * int(MEM_TIMEOUT) + 200 && !parked; ++i) {
      h.tick();
      if (dut->dbg_fault_o != F_NONE) parked = true;
    }
    CHECK(parked, "U9c the second park never settled");
    h.dram.refuse = false;
    h.dram.mem = gen.b;
    CHECK(h.rd(RGN_NCFG, false, 0),
          "U9c the first post-load NCFG read never answered");
    CHECK(!h.err && (h.rdata & 0xFFFFu) == gen.n_config,
          "U9c the FIRST NCFG read answered %u, want the walked %u",
          static_cast<unsigned>(h.rdata & 0xFFFFu),
          static_cast<unsigned>(gen.n_config));
  }
}

// ---- M1: a bridge that never accepts a request --------------------------
void DescStoreSuite::an_absent_bridge_times_out() {
  {
    h.dram.refuse = true;
    Image any = gen;
    h.dram.mem = any.b;
    h.reset();
    bool settled = false;
    for (int i = 0; i < 4 * int(MEM_TIMEOUT) + 200 && !settled; ++i) {
      h.tick();
      if (dut->dbg_fault_o != F_NONE) settled = true;
    }
    CHECK(settled, "M1 an absent bridge hung the store");
    CHECK(dut->dbg_fault_o == F_TIMEOUT, "M1 fault %u want TIMEOUT",
          static_cast<unsigned>(dut->dbg_fault_o));
    CHECK(h.locate(0, 0x0000, 0) && h.err,
          "M1 a locate with no memory did not answer a clean miss");
    h.dram.refuse = false;
  }
}

// ---- M2: the bridge answers the descriptor fetch with an error ----------
void DescStoreSuite::a_fetch_error_becomes_a_miss() {
  {
    CHECK(h.boot(gen), "M2 boot");
    h.dram.err_at = 1;
    CHECK(h.locate(0, gen.ents.front().type, 0),
          "M2 a fetch error never answered");
    CHECK(h.err, "M2 a fetch error did not become a locate miss");
    h.dram.err_at = -1;
    CHECK(h.locate(0, gen.ents.front().type, 0) && !h.err,
          "M2 the store did not recover after a fetch error");
  }
}

// ---- S1: two descriptors of one type, length not a multiple of 8 --------
void DescStoreSuite::two_descriptors_of_one_type_are_strided() {
  // without a padded STRIDE, index 1 starts mid-beat and the whole line
  // buffer comes back byte-shifted
  {
    Image syn = synth_two_of_a_type();
    CHECK(h.boot(syn), "S1 boot of the synthetic model");
    CHECK(dut->dbg_img_valid_o == 1, "S1 synthetic model rejected: fault %u",
          static_cast<unsigned>(dut->dbg_fault_o));
    check_all_descriptors(syn, "S1");
    CHECK(h.locate(0, 0x0014, 2) && h.err, "S1 cluster index 2 served");
  }
}

// ---- S4: ONE TYPE, SEVERAL RUNS (the AAF + CRF stream shape) -------------
void DescStoreSuite::one_type_of_several_runs_indexes_across_them() {
  // The scan must accumulate the counts of the runs it walks past, or index 1
  // is served from the run that owns index 0 and every controller reads the
  // wrong stream. Byte-exact, so a right-length-wrong-run answer still fails.
  {
    Image syn = synth_mixed_lengths();
    CHECK(h.boot(syn), "S4 boot of the mixed-length model");
    CHECK(dut->dbg_img_valid_o == 1, "S4 mixed-length model rejected: fault %u",
          static_cast<unsigned>(dut->dbg_fault_o));
    check_all_descriptors(syn, "S4");

    // the lengths must come back PER INDEX, not per type: this is the check
    // the uniform-stride layout could not have passed
    const std::array<uint16_t, 3> want_len = {148, 140, 148};
    for (uint16_t ix = 0; ix < 3; ++ix) {
      CHECK(h.locate(0, 0x0005, ix) && !h.err, "S4 STREAM_INPUT %u missed", ix);
      CHECK(h.rd(RGN_LEN, false, 0) && h.rdata == want_len[ix],
            "S4 STREAM_INPUT %u length got %llu want %u", ix,
            static_cast<unsigned long long>(h.rdata), want_len[ix]);
      // byte 3 of every body is its own index - proof the run arithmetic
      // landed on the right descriptor and not merely on the right length
      CHECK(h.rd(RGN_DATA, false, 0) && ((h.rdata >> 32) & 0xFFFF) == ix,
            "S4 STREAM_INPUT %u served descriptor_index %llu", ix,
            static_cast<unsigned long long>((h.rdata >> 32) & 0xFFFF));
    }
    // one past the last run must still MISS: accumulating must not run away
    CHECK(h.locate(0, 0x0005, 3) && h.err, "S4 STREAM_INPUT 3 was served");
    // and a later type must remain reachable past the split
    CHECK(h.locate(0, 0x0024, 0) && !h.err, "S4 type after the split missed");
  }
}

// ---- S2: an entry whose stride is inconsistent must not be served -------
void DescStoreSuite::an_inconsistent_stride_is_refused() {
  {
    Image syn = synth_two_of_a_type();
    const Entry* e = syn.find(0, 0x0014);
    size_t at = syn.index_off + 16 * size_t(e - &syn.ents[0]);
    Image::put16(syn.b, at + 14, 90);        // stride == len, not 8-aligned
    syn.reseal();
    CHECK(h.boot(syn), "S2 boot");
    CHECK(dut->dbg_img_valid_o == 1, "S2 header still valid");
    CHECK(h.locate(0, 0x0014, 0) && h.err,
          "S2 a misaligned stride was served instead of refused");
    CHECK(h.locate(0, 0x0000, 0) && !h.err,
          "S2 one bad entry poisoned the rest of the model");
  }
}

// ---- S3: an entry with a zero length ------------------------------------
void DescStoreSuite::a_zero_length_entry_is_refused() {
  {
    Image syn = synth_two_of_a_type();
    const Entry* e = syn.find(0, 0x0024);
    size_t at = syn.index_off + 16 * size_t(e - &syn.ents[0]);
    Image::put16(syn.b, at + 6, 0);
    syn.reseal();
    CHECK(h.boot(syn), "S3 boot");
    CHECK(h.locate(0, 0x0024, 0) && h.err, "S3 a zero-length entry was served");
  }

}

int DescStoreSuite::run() {
  if (!load_the_generators_example_image()) return 1;
  boots_from_the_generated_image();
  serves_every_generated_descriptor_byte_exact();
  index_map_boundaries_are_exact();
  locate_misses_are_answered_cleanly();
  the_name_region_is_the_writable_one();
  chunked_name_tables_cross_the_burst_boundary();
  the_image_is_read_only_at_run_time();
  back_to_back_reads_with_req_held_high();
  a_longer_memory_latency_changes_nothing();
  an_unloaded_region_serves_nothing();
  an_all_zero_region_serves_nothing();
  a_stale_checksum_is_refused();
  a_future_layout_version_is_refused();
  too_many_index_entries_is_refused();
  too_many_names_is_refused();
  a_descriptor_past_the_line_buffer_is_refused();
  a_late_image_load_self_heals();
  the_heal_precedes_the_first_answer();
  an_absent_bridge_times_out();
  a_fetch_error_becomes_a_miss();
  two_descriptors_of_one_type_are_strided();
  one_type_of_several_runs_indexes_across_them();
  an_inconsistent_stride_is_refused();
  a_zero_length_entry_is_refused();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  DescStoreSuite suite;
  return suite.run();
}

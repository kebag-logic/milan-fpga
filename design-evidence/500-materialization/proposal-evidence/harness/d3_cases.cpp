// SPDX-License-Identifier: CERN-OHL-W-2.0
// The D3 co-simulation (design evidence, milan-fpga #500): the case scripts.
// STIMULUS ONLY. Every verdict is taken by run.py, which decodes the dumped
// journal slots with the repository's own scripts/nvm_klj2.py and grades
// NAMED checks over the event log this file prints. Nothing here grades.
//
// A case whose name ends in "a" writes the slots a later "b" case boots from:
// the POWER CYCLE is a new process with fresh RTL and fresh firmware, and the
// flash array is the only thing carried across it, as the tracked
// nvm_cosim's R_power_cycle does.
#include "d3_bridge.h"

#include <algorithm>
#include <array>
#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <functional>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

extern "C" {
#include "nvm_host.h"
}

using namespace d3;

namespace {

struct Rec {
  unsigned id, off, flen, plen, index;
  std::string group;
};
std::map<unsigned, Rec> recs;
unsigned img_len = 0;
std::string variant;

// ---- facts derived from the shape's AEMI image by run.py --------------------
std::vector<uint32_t> rates;            //! AUDIO_UNIT 0 sampling_rates list
unsigned clk_count = 1, n_cfg = 1;      //! CLOCK_DOMAIN 0 sources, configurations
std::vector<std::vector<uint8_t>> def_names;
std::vector<uint8_t> aem;

std::vector<uint8_t> be(uint64_t v, unsigned n) {
  std::vector<uint8_t> b;
  for (int i = int(n) - 1; i >= 0; --i) b.push_back(uint8_t(v >> (8 * i)));
  return b;
}

std::string hex(const std::vector<uint8_t> &v) {
  static const char *d = "0123456789abcdef";
  std::string s;
  for (uint8_t b : v) {
    s.push_back(d[b >> 4]);
    s.push_back(d[b & 15]);
  }
  return s;
}

// ---- slots of the D3 writer (ascending record id, the prototype's order) ----
unsigned slot_of(unsigned rid) {
  unsigned s = 0;
  for (const auto &r : recs) {
    const unsigned id = r.first;
    if (id == 0x01 || (id >= 0x12 && id < 0x1A) || (id >= 0x20 && id < 0x30)) continue;
    if (id == rid) return s;
    ++s;
  }
  fatal("record id has no D3 slot");
}

// ---- uCPU programs -------------------------------------------------------------
const unsigned SEL_CFG = 0, SEL_RATE = 1, SEL_CLKS = 2, SEL_FMTI = 3, SEL_FMTO = 4, SEL_PTOF = 5;

//! the descriptor type a dynamic-state SET names (its commit mark carries it)
unsigned dyn_type(unsigned sel) {
  switch (sel) {
    case SEL_RATE: return 0x0002;       // AUDIO_UNIT
    case SEL_CLKS: return 0x0024;       // CLOCK_DOMAIN
    case SEL_FMTI: return 0x0005;       // STREAM_INPUT
    case SEL_FMTO:
    case SEL_PTOF: return 0x0006;       // STREAM_OUTPUT
    default:       return 0x0000;       // ENTITY
  }
}

//! a SET program: the state write, then OP_NVM_MARK class 1 (gen_ucode.py),
//! which the D3 writer does not use and the tracked glue does not take
void set_dyn(unsigned sel, unsigned idx, uint64_t val, unsigned width, int rid) {
  UOp w{UOp::DYN_WR};
  w.sel = sel;
  w.idx = idx;
  w.val = val;
  w.rid = rid;
  w.value = be(val, width);
  UOp m{UOp::MARK};
  m.cls = 1;
  m.type = dyn_type(sel);
  m.idx = (sel == SEL_CFG) ? 0 : idx;
  UOp g{UOp::GAP};
  g.gap = 3;
  program({w, m, g});
}

void set_fmt_out(unsigned s, uint64_t f) { set_dyn(SEL_FMTO, s, f, 8, int(0x40 + s)); }
void set_fmt_in(unsigned s, uint64_t f) { set_dyn(SEL_FMTI, s, f, 8, int(0x30 + s)); }
void set_ptof(unsigned s, uint32_t v) { set_dyn(SEL_PTOF, s, v, 4, int(0x50 + s)); }
void set_rate(uint32_t v) { set_dyn(SEL_RATE, 0, v, 4, 0x02); }
void set_clks(unsigned v) { set_dyn(SEL_CLKS, 0, v, 2, 0x0A); }
void set_cfg(unsigned v) { set_dyn(SEL_CFG, 0, v, 2, 0x00); }

std::vector<uint8_t> name_value(const std::string &text) {
  std::vector<uint8_t> v(64, 0);
  for (size_t i = 0; i < text.size() && i < 64; ++i) v[i] = uint8_t(text[i]);
  return v;
}

//! SET_NAME: eight lane writes; `gap` idle cycles between two lanes
void set_name(unsigned ord, const std::vector<uint8_t> &v, unsigned gap = 2) {
  std::vector<UOp> p;
  for (unsigned l = 0; l < 8; ++l) {
    UOp w{UOp::NAME_WR};
    uint64_t lane = 0;
    for (unsigned b = 0; b < 8; ++b) lane = (lane << 8) | v[8 * l + b];
    w.val = lane;
    w.addr = (ord << 6) | (l << 3);
    if (l == 7) {
      w.rid = int(0x80 + ord);
      w.value = v;
    }
    p.push_back(w);
    UOp g{UOp::GAP};
    g.gap = gap;
    p.push_back(g);
  }
  //! SET_NAME's OP_NVM_MARK, class 7: the tracked glue's sticky source
  UOp m{UOp::MARK};
  m.cls = 7;
  p.push_back(m);
  program(p);
}

void map_add(bool out, unsigned port, const std::vector<Map> &m) {
  UOp o{UOp::MAP_ADD};
  o.out = out;
  o.idx = port;
  o.maps = m;
  program({o});
}

void map_remove(bool out, unsigned port, const std::vector<Map> &m) {
  UOp o{UOp::MAP_REMOVE};
  o.out = out;
  o.idx = port;
  o.maps = m;
  program({o});
}

void ident(unsigned v) {
  UOp w{UOp::IDENT_WR};
  w.sel = 7;
  w.idx = 0;
  w.val = v;
  program({w});
}

//! GET-equivalents: the valid flag (region 2) and the value (region 1)
void read_row(unsigned sel, unsigned idx, const std::string &tag) {
  UOp v{UOp::READ};
  v.addr = (2u << 16) | (sel << 3);
  v.idx = idx;
  v.tag = tag + ".valid";
  UOp r{UOp::READ};
  r.addr = (1u << 16) | (sel << 3);
  r.idx = idx;
  r.tag = tag + ".value";
  program({v, r});
}

void read_name(unsigned ord, const std::string &tag) {
  std::vector<UOp> p;
  for (unsigned l = 0; l < 8; ++l) {
    UOp r{UOp::READ};
    r.addr = (ord << 6) | (l << 3);
    r.name = true;
    r.tag = tag + ".lane" + std::to_string(l);
    p.push_back(r);
  }
  program(p);
}

//! the first AECP command after enable: a LOCATE of ENTITY 0
void locate_entity(const std::string &tag) {
  UOp l{UOp::LOCATE};
  l.val = 0;
  l.tag = tag;
  program({l});
}

// ---- observing -----------------------------------------------------------------
void dump(const std::string &tag) {
  host_dump_file((out_dir + "/" + tag + "-slotA.bin").c_str(),
                 nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u);
  host_dump_file((out_dir + "/" + tag + "-slotB.bin").c_str(),
                 nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u);
  host_dump_file((out_dir + "/" + tag + "-live.bin").c_str(),
                 nvm_host_ddr + NVM_HOST_IMAGE_OFF, img_len);
}

void note(const std::string &key, uint64_t value) {
  std::printf("NOTE {\"key\":\"%s\",\"value\":%" PRIu64 ",\"cycle\":%" PRIu64 "}\n",
              key.c_str(), value, cyc);
  std::fflush(stdout);
}

void snap(const std::string &tag) {
  host_catch_up();
  dump(tag);
  const Levels l = levels();
  struct host_counters c;
  host_counters(&c);
  std::ostringstream o;
  o << "OBS {\"tag\":\"" << tag << "\",\"cycle\":" << cyc << ",\"ms\":" << (c.now_ns / 1000000ull)
    << ",\"backed\":" << l.backed << ",\"dirty\":" << l.dirty << ",\"stale\":" << l.stale
    << ",\"pend\":" << l.pend << ",\"unres\":" << l.unres << ",\"img_valid\":" << l.img_valid
    << ",\"alarm\":" << l.alarm << ",\"d3_alarm\":" << l.d3_alarm << ",\"d3_unfl\":" << l.d3_unfl
    << ",\"restore_done\":" << l.restore_done << ",\"restore_fail\":" << l.restore_fail
    << ",\"d3_done\":" << l.d3_done << ",\"d3_fail\":" << l.d3_fail
    << ",\"rs_app\":" << l.rs_app << ",\"rs_ref\":" << l.rs_ref << ",\"rs_blank\":" << l.rs_blank
    << ",\"rs_rev\":" << l.rs_rev << ",\"d3_writes\":" << l.d3_writes
    << ",\"dirty_count\":" << dirty_count() << ",\"mgr_dirty\":" << l.mgr_dirty
    << ",\"desc_valid\":" << l.desc_valid << ",\"erases\":" << c.erases
    << ",\"programs\":" << c.programs << ",\"maps_out\":[";
  for (size_t p = 0; p < map_out.size(); ++p) {
    o << (p ? "," : "") << "\"" << hex(map_payload(true, unsigned(p))) << "\"";
  }
  o << "],\"maps_in\":[";
  for (size_t p = 0; p < map_in.size(); ++p) {
    o << (p ? "," : "") << "\"" << hex(map_payload(false, unsigned(p))) << "\"";
  }
  o << "]}";
  std::printf("%s\n", o.str().c_str());
  std::fflush(stdout);
}

void dump_log() {
  for (const auto &r : evlog.ops)
    std::printf("EVT {\"k\":\"op\",\"op\":%u,\"rid\":%u,\"gnt\":%" PRIu64 ",\"end\":%" PRIu64
                ",\"res\":\"%s\",\"bytes\":%u,\"w\":\"%s\"}\n",
                r.op, r.rid, r.gnt, r.end, r.res.c_str(), r.bytes, hex(r.wbytes).c_str());
  for (const auto &c : evlog.changes)
    std::printf("EVT {\"k\":\"chg\",\"cyc\":%" PRIu64 ",\"rid\":%u,\"v\":\"%s\"}\n", c.cyc, c.rid,
                hex(c.value).c_str());
  for (const auto &d : evlog.durable)
    std::printf("EVT {\"k\":\"dur\",\"cyc\":%" PRIu64 ",\"v\":%u}\n", d.first, d.second);
  for (const auto &a : evlog.acks)
    std::printf("EVT {\"k\":\"ack\",\"cyc\":%" PRIu64 ",\"n\":%u}\n", a.first, a.second);
  for (const auto &a : answers) {
    unsigned err = 0;
    for (const auto &e : answer_err)
      if (e.first == a.first) err = e.second;
    std::printf("EVT {\"k\":\"ans\",\"tag\":\"%s\",\"v\":\"0x%016" PRIx64 "\",\"err\":%u}\n",
                a.first.c_str(), a.second, err);
  }
  std::printf("EVT {\"k\":\"boot\",\"enable\":%" PRIu64 ",\"restore_done\":%" PRIu64
              ",\"d3_done\":%" PRIu64 ",\"own_max\":%" PRIu64 ",\"prog_waited\":%" PRIu64
              ",\"mem_errs\":%u,\"collisions\":%u}\n",
              evlog.enable_cyc, evlog.restore_done_cyc, evlog.d3_done_cyc, evlog.own_max,
              evlog.prog_waited_on_own, evlog.mem_errs, evlog.collisions);
}

// ---- stepping --------------------------------------------------------------------
void idle(uint64_t ms) { host_idle_ms(ms); }

bool idle_until(const std::function<bool()> &p, uint64_t max_ms) {
  for (uint64_t i = 0; i < max_ms; ++i) {
    if (p()) return true;
    host_idle_ms(1);
  }
  return p();
}

//! idle with the writer serviced until a program queue drains
void settle() { idle_until([] { return programs_idle(); }, 50); }

//! the status reads durable: backed, nothing committable, not stale, nothing pending
bool durable_now() {
  const Levels l = levels();
  return l.backed && !l.dirty && !l.stale && !l.pend;
}

void converge(uint64_t max_ms = 12000) {
  settle();
  idle_until(durable_now, max_ms);
}

void boot() {
  host_boot();
  idle(30);
  snap("boot");
}

void fault(unsigned rid, unsigned byte, int count) {
  auto it = recs.find(rid);
  if (it == recs.end()) fatal("fault on a record not in the table");
  faults.push_back(Fault{it->second.off + byte, 0, 2, count});
}

// ---- the image-default map sets of the MODEL: the first clusters of each port
// map to the first channels of one stream, cluster k to channel k -------------
void default_maps() {
  for (size_t p = 0; p < map_in.size(); ++p) {
    auto &mp = map_in[p];
    mp.def.clear();
    const unsigned s = n_si ? unsigned(p % n_si) : 0;
    const unsigned ch = n_si ? fmt_channels(def_fmt_in[s]) : 0;
    for (unsigned k = 0; k < mp.clusters && k < ch; ++k)
      mp.def.push_back(Map{uint16_t(s), uint16_t(k), uint16_t(k), 0});
    mp.cur = mp.def;
  }
  for (size_t p = 0; p < map_out.size(); ++p) {
    auto &mp = map_out[p];
    mp.def.clear();
    const unsigned s = n_so ? unsigned(p % n_so) : 0;
    const unsigned ch = n_so ? fmt_channels(def_fmt_out[s]) : 0;
    for (unsigned k = 0; k < mp.clusters && k < ch && k < 8; ++k)
      mp.def.push_back(Map{uint16_t(s), uint16_t(k), uint16_t(k), 0});
    mp.cur = mp.def;
  }
}

uint64_t narrower(uint64_t f, unsigned ch) {
  return (f & ~((uint64_t(1) << 52) | (uint64_t(0x3FF) << 22))) | (uint64_t(ch) << 22);
}

// ---- the cases ------------------------------------------------------------------
std::map<std::string, std::function<void()>> cases;

//! the phase-a mutation every restore case commits: one non-default value
//! in every materialized group the shape can express
//! narrow stream s to `ch` channels the way a conforming controller must
//! (Milan 5.4.2.7): first remove every mapping that names a channel the
//! narrower format does not have, then SET_STREAM_FORMAT
void narrow_stream(bool out, unsigned s, unsigned ch) {
  auto &ports = out ? map_out : map_in;
  for (unsigned p = 0; p < ports.size(); ++p) {
    std::vector<Map> gone;
    for (const auto &m : ports[p].cur)
      if (m.si == s && m.sc >= ch) gone.push_back(m);
    if (!gone.empty()) map_remove(out, p, gone);
  }
  if (out) set_fmt_out(s, narrower(def_fmt_out[s], ch));
  else set_fmt_in(s, narrower(def_fmt_in[s], ch));
}

void set_everything() {
  set_cfg(0);                                   // the only legal index: 1 configuration
  if (rates.size() > 1) set_rate(rates[1]);
  if (clk_count > 1) set_clks(1);
  narrow_stream(false, 0, 2);
  set_ptof(0, 1500000u);
  set_name(0, name_value("D3 restored entity name"));
  set_name(n_name - 1, name_value("D3 restored last name"));
  // OUT port 0: move channel 7 from cluster 7 to the last cluster
  const auto &d = map_out[0].def;
  if (!d.empty()) {
    const Map last = d.back();
    map_remove(true, 0, {last});
    map_add(true, 0, {Map{last.si, last.sc, uint16_t(map_out[0].clusters - 1), 0}});
  }
}

void register_cases() {
  // ================= THE CLEAR RULE =================
  cases["K1_single_change_converges"] = [] {
    boot();
    set_ptof(0, 1234567u);
    converge();
    snap("end");
  };
  cases["K2_change_during_record_write"] = [] {
    boot();
    set_ptof(0, 1111111u);
    // the second change lands while the writer's WRITE of 0x50 streams
    on_cycle([] {
      if (dut_dev_write_open(0x50)) {
        return force_dyn_write(SEL_PTOF, 0, 2222222u, 0x50, be(2222222u, 4));
      }
      return false;
    });
    converge();
    snap("end");
  };
  cases["K3_two_changes_one_debounce"] = [] {
    boot();
    set_ptof(0, 3000001u);
    idle(100);
    set_ptof(0, 3000002u);
    converge();
    snap("end");
  };
  cases["K4_second_record_in_flight"] = [] {
    boot();
    set_ptof(0, 4000001u);
    on_cycle([] {
      if (dut_dev_write_open(0x50)) return force_dyn_write(SEL_PTOF, 1, 4000002u, 0x51, be(4000002u, 4));
      return false;
    });
    converge();
    snap("end");
  };
  cases["K5_change_on_the_done_edge"] = [] {
    boot();
    set_ptof(0, 5000001u);
    on_cycle([] {
      if (writer_done_now() && levels().d3_slot == slot_of(0x50))
        return force_dyn_write(SEL_PTOF, 0, 5000002u, 0x50, be(5000002u, 4));
      return false;
    });
    converge();
    snap("end");
  };
  cases["K6a_cut_after_record_before_commit"] = [] {
    boot();
    set_ptof(0, 1234567u);
    converge();                                  // X is durable
    set_ptof(0, 6000001u);                       // Y is accepted...
    run_until([] {                               // ...and written into the window
      for (const auto &o : evlog.ops)
        if (o.rid == 0x50 && o.op == 1 && o.res == "done" && o.wbytes.size() == 12 &&
            o.wbytes[8] == 0x00 && o.wbytes[9] == 0x5B)
          return true;
      return false;
    }, 3000000);
    snap("cut");                                 // the power is cut HERE
  };
  cases["K6b_restore_after_cut"] = [] {
    boot();
    read_row(SEL_PTOF, 0, "ptof0");
    settle();
    snap("restored");
  };
  cases["K7a_cut_after_ack"] = [] {
    boot();
    set_ptof(0, 7000001u);
    converge();
    snap("cut");
  };
  cases["K7b_restore_after_ack"] = [] {
    boot();
    read_row(SEL_PTOF, 0, "ptof0");
    settle();
    snap("restored");
  };
  cases["K8_record_write_error_retried"] = [] {
    boot();
    fault(0x50, 8, 1);                           // the first payload byte, once
    set_ptof(0, 8000001u);
    converge();
    snap("end");
  };
  cases["K9_record_write_given_up"] = [] {
    boot();
    fault(0x50, 8, -1);                          // every attempt fails
    set_ptof(0, 9000001u);
    settle();
    idle(6000);
    snap("end");
  };
  cases["K10_name_change_converges"] = [] {
    boot();
    set_name(0, name_value("K10 entity"));
    converge();
    snap("end");
  };
  cases["K11_name_latch_waits_for_the_program"] = [] {
    boot();
    set_name(0, name_value("K11 first value AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"));
    settle();
    // the debounce closes 500 ms after the first change; a slow SET_NAME is
    // in progress across that instant, its lanes 5 ms apart
    idle(470);
    set_name(0, name_value("K11 second value BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"), 5000);
    converge();
    snap("end");
  };
  cases["K12_map_change_converges"] = [] {
    boot();
    const auto &d = map_out[0].def;
    if (!d.empty()) {
      const Map last = d.back();
      map_remove(true, 0, {last});
      map_add(true, 0, {Map{last.si, last.sc, uint16_t(map_out[0].clusters - 1), 0}});
    }
    converge();
    snap("end");
  };
  cases["K13_binding_and_d3_share_the_port"] = [] {
    boot();
    Binding b;
    b.sink = 0;
    b.uid = 7;
    b.teid = 0x1122334455667788ull;
    b.ceid = 0x0102030405060708ull;
    bind(b);
    set_ptof(0, 1300013u);
    converge();
    snap("end");
  };
  cases["K14_identify_is_not_persisted"] = [] {
    boot();
    ident(255);
    settle();
    idle(3000);
    snap("end");
  };
  cases["K4g_second_group_in_flight"] = [] {
    // a change to ANOTHER GROUP (clock source, record 0x0A, index 0) lands
    // while the WRITE of 0x50 (presentation offset, index 0) streams
    boot();
    set_ptof(0, 4100001u);
    on_cycle([] {
      if (dut_dev_write_open(0x50)) return force_dyn_write(SEL_CLKS, 0, 1u, 0x0A, be(1u, 2));
      return false;
    });
    converge();
    snap("end");
  };
  cases["K15_binding_on_the_d3_grant_cycle"] = [] {
    // variant g<N>: the D3 writer is held (prog_busy) until N cycles after
    // the binding manager starts its crc pass (H_FL_CRC, encoding 12), so
    // across the sweep one N puts the writer's grant on the cycle the
    // binding manager samples busy in H_FL_REQ
    const unsigned n = unsigned(std::stoul(variant.substr(1)));
    boot();
    hold(true);
    set_ptof(0, 1500015u);
    settle();
    Binding b;
    b.sink = 0;
    b.uid = 15;
    b.teid = 0x1515151515151515ull;
    b.ceid = 0x0101010101010101ull;
    bind(b);
    auto left = std::make_shared<int>(-1);
    on_cycle([left, n] {
      if (*left < 0 && m0_state() == 12u) *left = int(n);
      if (*left < 0) return false;
      if (*left == 0) {
        hold(false);
        return true;
      }
      --*left;
      return false;
    });
    converge();
    snap("end");
  };
  cases["K16_map_set_larger_than_its_record"] = [] {
    // OUT port 0 takes two stream channels OUT port 1 gave up, both fed from
    // its last cluster (fan-out): one more mapping than the port has
    // clusters, so its record (8 bytes a cluster) cannot hold the set
    boot();
    const unsigned cls = map_out[0].clusters;
    std::vector<Map> give;
    for (const auto &m : map_out[1].cur)
      if (m.sc < 2) give.push_back(m);
    map_remove(true, 1, give);
    std::vector<Map> extra;
    const unsigned need = cls + 1 - unsigned(map_out[0].cur.size());
    for (unsigned k = 0; k < need; ++k)
      extra.push_back(Map{give[k].si, give[k].sc, uint16_t(cls - 1), 0});
    map_add(true, 0, extra);
    settle();
    note("over_size", map_out[0].cur.size());
    idle(3000);                                  // several debounce windows
    snap("over");
    map_remove(true, 0, {extra.back()});         // the controller shrinks it to fit
    converge();
    snap("end");
  };
  cases["K17a_cut_during_record_write"] = [] {
    boot();
    set_ptof(0, 1717001u);
    converge();                                  // X is durable
    set_ptof(0, 1717002u);                       // Y is accepted...
    run_until([] { return dut_dev_write_bytes(0x50) >= 6; }, 3000000);
    note("cut_write_bytes", uint64_t(std::max(0, dut_dev_write_bytes(0x50))));
    snap("cut");                                 // ...and the power is cut mid-WRITE
  };
  cases["K17b_restore_after_cut_in_write"] = [] {
    boot();
    read_row(SEL_PTOF, 0, "ptof0");
    settle();
    snap("restored");
  };
  cases["K18a_cut_inside_the_debounce"] = [] {
    boot();
    set_ptof(0, 1818001u);
    converge();                                  // X is durable
    set_ptof(0, 1818002u);                       // Y is accepted...
    settle();
    idle(100);                                   // ...inside the 500 ms debounce
    snap("cut");
  };
  cases["K18b_restore_after_cut_in_debounce"] = [] {
    boot();
    read_row(SEL_PTOF, 0, "ptof0");
    settle();
    snap("restored");
  };

  // ================= RESTORE =================
  cases["V1a_set_everything"] = [] {
    boot();
    Binding b;
    b.sink = 0;
    b.uid = 9;
    b.teid = 0x0A0B0C0D0E0F1011ull;
    b.ceid = 0x2122232425262728ull;
    bind(b);
    set_everything();
    converge();
    snap("cut");
  };
  cases["V1b_restore_everything"] = [] {
    if (variant == "stale") {
      // VACUITY CONTROL: rows that "survived" the cut, as a store that was
      // never reset would hold them. Seeded with the writer's change snoop
      // held off, because a surviving row is not a controller change.
      snoop(false);
      set_fmt_in(0, narrower(def_fmt_in[0], 2));
      set_ptof(0, 1500000u);
      if (rates.size() > 1) set_rate(rates[1]);
      run_until([] { return programs_idle(); }, 100000);
      snoop(true);
      evlog.changes.clear();
    }
    // every restorable row, BEFORE the restore: the reset must have cleared it
    read_row(SEL_CFG, 0, "pre.cfg");
    read_row(SEL_RATE, 0, "pre.rate");
    read_row(SEL_CLKS, 0, "pre.clks");
    read_row(SEL_FMTI, 0, "pre.fmti0");
    read_row(SEL_PTOF, 0, "pre.ptof0");
    run_until([] { return programs_idle(); }, 100000);
    boot();
    idle(200);
    read_row(SEL_CFG, 0, "post.cfg");
    read_row(SEL_RATE, 0, "post.rate");
    read_row(SEL_CLKS, 0, "post.clks");
    read_row(SEL_FMTI, 0, "post.fmti0");
    read_row(SEL_PTOF, 0, "post.ptof0");
    read_name(0, "post.name0");
    read_name(n_name - 1, "post.namelast");
    settle();
    // the first AECP command after enable, then the names again
    locate_entity("first_command");
    read_name(0, "after.name0");
    read_name(n_name - 1, "after.namelast");
    settle();
    idle(3000);
    snap("restored");
  };
  cases["V2_refused_rate"] = [] {
    boot();
    idle(200);
    read_row(SEL_RATE, 0, "post.rate");
    settle();
    snap("restored");
  };
  cases["V3_refused_map_for_a_removed_cluster"] = [] {
    boot();
    idle(200);
    snap("restored");
  };
  cases["V4_refused_configuration_index"] = [] {
    boot();
    idle(200);
    read_row(SEL_CFG, 0, "post.cfg");
    settle();
    snap("restored");
  };
  cases["V5_record_corrupted_after_the_load"] = [] {
    // a byte of PTOF[0] flips in DDR after the writer filled the window and
    // before the walk reads it back: the container was verified, this record
    // no longer is (the per-record crc16 is the only check left)
    at("s_reload", 1, [] {
      auto it = recs.find(0x50);
      if (it == recs.end()) fatal("no record 0x50");
      area()[it->second.off + 8 + 3] ^= 0x01;
    });
    boot();
    idle(200);
    read_row(SEL_PTOF, 0, "post.ptof0");
    read_row(SEL_PTOF, 1, "post.ptof1");
    settle();
    snap("restored");
  };
  cases["V7_names_only"] = [] {
    // only a NAME record is saved, so nothing else the restore does can walk
    // the descriptor store first: the image check alone orders the names
    boot();
    idle(200);
    read_name(0, "post.name0");
    settle();
    locate_entity("first_command");
    read_name(0, "after.name0");
    settle();
    snap("restored");
  };
  cases["V6a_set_coupled_narrower_pair"] = [] {
    boot();
    // a consistent narrower pair: drop the mappings on channels 2.., then
    // narrow the stream to 2 channels (Milan 5.4.2.7 order)
    std::vector<Map> high;
    for (const auto &m : map_out[0].def)
      if (m.sc >= 2) high.push_back(m);
    map_remove(true, 0, high);
    set_fmt_out(0, narrower(def_fmt_out[0], 2));
    converge();
    snap("cut");
  };
  cases["V6b_restore_coupled_pair"] = [] {
    boot();
    idle(200);
    read_row(SEL_FMTO, 0, "post.fmto0");
    settle();
    snap("restored");
  };
  cases["V8_orphaning_format_reverted"] = [] {
    boot();
    idle(200);
    read_row(SEL_FMTO, 0, "post.fmto0");
    settle();
    snap("restored");
  };
  cases["V9_refused_maps_revert_their_formats"] = [] {
    boot();
    idle(200);
    read_row(SEL_FMTO, 0, "post.fmto0");
    settle();
    snap("restored");
  };
  cases["V10_blank_first_boot"] = [] {
    boot();
    idle(200);
    read_row(SEL_PTOF, 0, "post.ptof0");
    settle();
    snap("restored");
  };
}

void load_records(const std::string &path) {
  std::ifstream f(path);
  std::string line;
  while (std::getline(f, line)) {
    std::istringstream s(line);
    std::string k;
    s >> k;
    if (k == "imglen") s >> img_len;
    if (k != "rec") continue;
    std::string id;
    Rec r{};
    s >> id >> r.off >> r.flen >> r.plen >> r.group >> r.index;
    r.id = unsigned(std::stoul(id, nullptr, 0));
    recs[r.id] = r;
  }
  if (recs.empty() || !img_len) fatal("no record table");
}

void load_facts(const std::string &path) {
  std::ifstream f(path);
  std::string line;
  while (std::getline(f, line)) {
    std::istringstream s(line);
    std::string k, v;
    s >> k >> v;
    if (k == "fmt_in") def_fmt_in.push_back(std::stoull(v, nullptr, 16));
    else if (k == "fmt_out") def_fmt_out.push_back(std::stoull(v, nullptr, 16));
    else if (k == "rate") rates.push_back(uint32_t(std::stoul(v, nullptr, 16)));
    else if (k == "clk_count") clk_count = unsigned(std::stoul(v));
    else if (k == "n_cfg") n_cfg = unsigned(std::stoul(v));
  }
}

}  // namespace

int main(int argc, char **argv) {
  std::string name, table, facts, aem_path, slot_a, slot_b;
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    const char *v = (i + 1 < argc) ? argv[i + 1] : nullptr;
    if (a == "--case" && v) name = argv[++i];
    else if (a == "--out" && v) out_dir = argv[++i];
    else if (a == "--records" && v) table = argv[++i];
    else if (a == "--facts" && v) facts = argv[++i];
    else if (a == "--aem" && v) aem_path = argv[++i];
    else if (a == "--slot-a" && v) slot_a = argv[++i];
    else if (a == "--slot-b" && v) slot_b = argv[++i];
    else if (a == "--variant" && v) variant = argv[++i];
    else if (a == "--list") name = "--list";
    else {
      std::fprintf(stderr, "unknown argument %s\n", a.c_str());
      return 2;
    }
  }
  register_cases();
  if (name == "--list") {
    for (auto &c : cases) std::printf("%s\n", c.first.c_str());
    return 0;
  }
  load_records(table);
  load_facts(facts);
  std::vector<unsigned> cls_in, cls_out;
  for (const auto &r : recs) {
    if (r.first >= 0x60 && r.first < 0x70) cls_in.push_back(r.second.plen / 8);
    if (r.first >= 0x70 && r.first < 0x80) cls_out.push_back(r.second.plen / 8);
    if (r.first >= 0x30 && r.first < 0x40) ++n_si;
    if (r.first >= 0x40 && r.first < 0x50) ++n_so;
    if (r.first >= 0x80) ++n_name;
  }
  n_spi = unsigned(cls_in.size());
  n_spo = unsigned(cls_out.size());
  host_init();
  {
    std::ifstream f(aem_path, std::ios::binary);
    aem.assign(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
    if (aem.empty()) fatal("no AEMI image");
    host_aem_image(aem.data(), aem.size());
  }
  if (!slot_a.empty() && !host_load_file(slot_a.c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u))
    fatal("cannot load slot A");
  if (!slot_b.empty() &&
      !host_load_file(slot_b.c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u))
    fatal("cannot load slot B");
  d3::init(cls_in, cls_out);
  default_maps();
  auto it = cases.find(name);
  if (it == cases.end()) {
    std::fprintf(stderr, "unknown case %s\n", name.c_str());
    return 2;
  }
  it->second();
  dump_log();
  std::printf("CASE_DONE %s hooks_pending=%d\n", name.c_str(), all_fired() ? 0 : 1);
  d3::finish();
  return 0;
}

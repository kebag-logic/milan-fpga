// SPDX-License-Identifier: CERN-OHL-W-2.0
// The D3 co-simulation (design evidence, milan-fpga #500): the Verilated RTL
// (d3_top.sv), its models and the one clock shared with the host model.
// Derived from tb/verilator/nvm_cosim/cosim_bridge.cpp.
//
// WHAT IS REAL: every RTL module d3_top instantiates. WHAT IS A MODEL: the
// main-memory bridge of the backend (one outstanding single-beat write, done
// three cycles after acceptance; one outstanding one-beat read) with per-byte
// fault injection; the descriptor store's read-only DDR (the AEMI image the
// firmware copied, served in bursts); the uCPU (a program of state-bus
// operations with the dispatch hold-off); and the parent's map plane (the
// port mapping sets, the GET_AUDIO_MAP read face, the edit face and the
// format judge), whose rules are stated where they are coded.
#include "d3_bridge.h"

#include "Vd3_top.h"
#include "verilated.h"

#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <type_traits>
#include <vector>

extern "C" {
#include "nvm_host.h"
}

namespace d3 {

constexpr uint32_t kBase = 0x40000000u;   // the backend's view of the area
constexpr uint32_t kRoom = 0x10000u - 44u;
constexpr uint32_t kDesc = 0x20000000u;   // DESC_BASE_P: nvm_host_ddr offset 0

std::unique_ptr<VerilatedContext> ctx;
std::unique_ptr<Vd3_top> dut;
uint64_t cyc = 0;
Log evlog;
std::string out_dir;
unsigned n_si = 0, n_so = 0, n_spi = 0, n_spo = 0, n_name = 0;
std::vector<Fault> faults;
std::vector<MapPort> map_in, map_out;
std::vector<uint64_t> def_fmt_in, def_fmt_out;
std::vector<std::pair<std::string, uint64_t>> answers;
std::vector<std::pair<std::string, unsigned>> answer_err;

uint8_t *area() { return nvm_host_ddr + NVM_HOST_IMAGE_OFF + 40u; }

//! one bit of a Verilated port, whether it is packed as a scalar or wide
template <typename T> static bool bit_of(const T &v, unsigned b) {
  if constexpr (std::is_integral_v<T>) return (uint64_t(v) >> b) & 1u;
  else return (v[b / 32] >> (b % 32)) & 1u;
}
template <typename T> static uint64_t word64_of(const T &v, unsigned w) {
  if constexpr (std::is_integral_v<T>) return uint64_t(v);
  else return (uint64_t(v[2 * w + 1]) << 32) | v[2 * w];
}

//! a write forced onto the state bus by a same-edge trigger
struct Forced {
  bool on = false;
  int rid = -1;
  std::vector<uint8_t> value;
} forced;

//! the writer's change snoop (the stale-store control holds it off)
bool snoop_on = true;

// ------------------------------------------------------------ backend memory
struct Wr {
  bool busy = false;
  int delay = 0;
  uint32_t addr = 0;
  uint64_t data = 0;
  uint8_t strb = 0;
  bool err = false;
} wr;
struct Rd {
  bool busy = false;
  int delay = 0;
  uint32_t addr = 0;
} rd;

unsigned first_lane(uint8_t strb) {
  for (unsigned n = 0; n < 8; ++n)
    if (strb & (1u << n)) return n;
  return 8;
}

void mem_apply(uint32_t addr, uint64_t data, uint8_t strb) {
  for (unsigned n = 0; n < 8; ++n) {
    if (!(strb & (1u << n))) continue;
    const uint32_t off = addr - kBase + n;
    if (addr < kBase || off >= kRoom) fatal("memory write outside the record area");
    area()[off] = uint8_t(data >> (56 - 8 * n));
  }
}

uint64_t lane(uint32_t addr) {
  uint64_t v = 0;
  for (unsigned n = 0; n < 8; ++n) {
    const uint32_t off = addr - kBase + n;
    const uint8_t b = (addr >= kBase && off < kRoom) ? area()[off] : 0xA5;
    v |= uint64_t(b) << (56 - 8 * n);
  }
  return v;
}

//! mode 1: the READ response of the lane holding record-area offset `off`
//! comes back with mem_rsp_err (a record operation the backend aborts)
Fault *match_read_fault(uint32_t addr) {
  // Arm the existing V11 fault only after pass 1 has applied a record.
  if (addr < kBase || dut->d3_rs_applied_o == 0) return nullptr;
  const uint32_t lo = addr - kBase;
  for (auto &f : faults)
    if (f.count != 0 && f.mode == 1 && f.off >= lo && f.off < lo + 8) return &f;
  return nullptr;
}

Fault *match_fault(uint32_t off, uint8_t byte) {
  for (auto &f : faults) {
    if (f.count == 0 || f.off != off || f.mode != 0) continue;
    if (f.kind == 1 && byte != 0xFF) continue;
    if (f.kind == 2 && byte == 0xFF) continue;
    return &f;
  }
  return nullptr;
}

// --------------------------------------------------- descriptor store memory
struct DRd {
  bool busy = false;
  int delay = 0;
  uint32_t addr = 0;
  unsigned left = 0;
} drd;

uint64_t desc_lane(uint32_t addr) {
  uint64_t v = 0;
  for (unsigned n = 0; n < 8; ++n) {
    const uint32_t off = addr - kDesc + n;
    const uint8_t b = (addr >= kDesc && off < NVM_HOST_DDR_BYTES) ? nvm_host_ddr[off] : 0xA5;
    v |= uint64_t(b) << (56 - 8 * n);
  }
  return v;
}

// ------------------------------------------------------------ op tracking
struct OpTrack {
  bool active = false;
  OpRec r;
} cur;

// ------------------------------------------------------------ the uCPU model
std::deque<std::vector<UOp>> progs;
std::vector<UOp> prog;
size_t pc = 0;
enum class U { Idle, Bus, Gap, Mark } ust = U::Idle;
unsigned ugap = 0;
bool u_after_read = false;
//! the commit mark a program raises (KL_aecp_ucpu eff_nvm_stb_o/mark_o,
//! with the command's descriptor type and index beside it)
struct MarkQ {
  bool on = false;
  unsigned cls = 0;
  unsigned type = 0;
  unsigned idx = 0;
} mark, pend_mark;
//! the map edit face's commit-one-record beat (phase 5): the live map write,
//! which the class-6 mark follows only after the program's tail (the loop
//! exit, then FINISH, COMMIT, SET_STATUS, COMPARE and BR_STATUS in
//! gen_ucode.py's E_AMADD); the model spends kMapMarkTail cycles on it
struct EditQ {
  bool on = false;
  unsigned type = 0;
  unsigned idx = 0;
} edit;
constexpr unsigned kMapMarkTail = 4;
bool hold_on = false;

// ------------------------------------------------------------ the map model
struct MrState {
  bool busy = false;
  std::vector<Map> got;
  int done_in = -1;
  bool ok = false;
} mr;
unsigned am_cnt = 0, fj_cnt = 0;

unsigned fmt_channels(uint64_t f) {
  //! IEEE 1722-2016 7.3.1 as avdecc/aem_maps.py fmt_channels reads it: the
  //! AAF subtype is the top octet, channels_per_frame bits 31:22
  if ((f >> 56) != 0x02) return 0;
  return unsigned((f >> 22) & 0x3FF);
}

uint64_t live_fmt(bool out, unsigned s) {
  if (out) {
    if (!bit_of(dut->dyn_fmt_out_v_o, s)) return def_fmt_out[s];
    return word64_of(dut->dyn_fmt_out_o, s);
  }
  if (!bit_of(dut->dyn_fmt_in_v_o, s)) return def_fmt_in[s];
  return word64_of(dut->dyn_fmt_in_o, s);
}

//! MODEL of the integrator's "supported for this stream" (GSI(15) bit 0):
//! the stream's image-default format, or a Milan Base 48 kHz AAF PCM32 format
//! (avdecc/aem_maps.py base_channel_cover's stem) of 1, 2, 4, 6 or 8 channels
//! no wider than the default. A CRF stream supports its default alone.
bool fmt_supported(bool out, unsigned s, uint64_t f) {
  const uint64_t d = out ? def_fmt_out[s] : def_fmt_in[s];
  if (f == d) return true;
  if (fmt_channels(d) == 0) return false;
  const uint64_t stem = f & ~((uint64_t(1) << 52) | (uint64_t(0x3FF) << 22));
  const unsigned ch = fmt_channels(f);
  const bool base = ch == 1 || ch == 2 || ch == 4 || ch == 6 || ch == 8;
  return stem == 0x0205022000006000ull && base && ch <= fmt_channels(d);
}

//! MODEL of the integrator's staged-command judgement of a map set: every
//! cluster exists on the port, every stream exists, every mapped channel
//! exists in the stream's LIVE format, no key twice. The KEY is the parent's
//! (hdl/milan/milan_datapath.sv amap_edit_validate): an INPUT mapping is keyed
//! by its cluster, so an input set never outgrows its clusters; an OUTPUT
//! mapping is keyed by its stream channel, owned by at most one port, so one
//! cluster may feed several stream channels and an output set MAY outgrow
//! the record the saved-state allocation gives its port (8 bytes a cluster).
bool map_set_valid(bool out, unsigned port, const std::vector<Map> &set) {
  const MapPort &p = out ? map_out[port] : map_in[port];
  for (size_t i = 0; i < set.size(); ++i) {
    const Map &m = set[i];
    if (m.co >= p.clusters || m.cc != 0) return false;
    if (m.si >= (out ? n_so : n_si)) return false;
    const unsigned ch = fmt_channels(live_fmt(out, m.si));
    if (ch == 0 || m.sc >= ch) return false;
    for (size_t j = 0; j < i; ++j) {
      if (!out && set[j].co == m.co) return false;
      if (out && set[j].si == m.si && set[j].sc == m.sc) return false;
    }
    if (out) {
      //! a stream channel another output port already feeds is not free
      for (size_t q = 0; q < map_out.size(); ++q) {
        if (q == port) continue;
        for (const auto &o : map_out[q].cur)
          if (o.si == m.si && o.sc == m.sc) return false;
      }
    }
  }
  return true;
}

//! the record payload the writer must produce for a port: its live set in
//! order, 8 bytes each, then unused (0xFF) entries up to the cluster count
std::vector<uint8_t> map_payload(bool out, unsigned port) {
  const MapPort &p = out ? map_out[port] : map_in[port];
  std::vector<uint8_t> v;
  for (const auto &m : p.cur)
    for (int b = 7; b >= 0; --b) v.push_back(uint8_t(m.packed() >> (8 * b)));
  while (v.size() < 8u * p.clusters) v.push_back(0xFF);
  return v;
}

// ------------------------------------------------------------ bookkeeping
unsigned prev_durable = 2;
uint64_t own_since = 0;
bool prev_enable = false;
unsigned restore_go = 0;
struct CapPulse {
  bool on = false;
  Binding b;
} cap;
std::vector<std::function<bool()>> cycle_triggers;

void on_cycle(std::function<bool()> fn) { cycle_triggers.push_back(std::move(fn)); }

// ---------------------------------------------------------------- driving
static void drive_ucpu() {
  dut->ub_req_i = 0;
  dut->ub_we_i = 0;
  dut->ub_name_i = 0;
  if (ust == U::Idle && !progs.empty()) {
    //! the dispatch hold-off: no program starts while the writer owns the bus
    if (dut->own_o) {
      evlog.prog_waited_on_own++;
    } else {
      prog = progs.front();
      progs.pop_front();
      pc = 0;
      ust = U::Bus;
      ugap = 0;
      u_after_read = false;
    }
  }
  dut->prog_busy_i = (ust != U::Idle) || hold_on;
  if (ust != U::Bus || pc >= prog.size()) return;
  const UOp &o = prog[pc];
  switch (o.kind) {
    case UOp::DYN_WR:
    case UOp::IDENT_WR:
      dut->ub_req_i = 1;
      dut->ub_we_i = 1;
      dut->ub_addr_i = (1u << 16) | (o.sel << 3);
      dut->ub_didx_i = o.idx;
      dut->ub_wdata_i = o.val;
      break;
    case UOp::NAME_WR:
      dut->ub_req_i = 1;
      dut->ub_we_i = 1;
      dut->ub_name_i = 1;
      dut->ub_addr_i = o.addr;
      dut->ub_wdata_i = o.val;
      break;
    case UOp::READ:
      dut->ub_req_i = 1;
      dut->ub_name_i = o.name;
      dut->ub_addr_i = o.addr;
      dut->ub_didx_i = o.idx;
      break;
    case UOp::LOCATE:
      dut->ub_req_i = 1;
      dut->ub_addr_i = 0xF0000u;
      dut->ub_wdata_i = o.val;
      break;
    default:
      break;
  }
}

static void drive_maps() {
  // the GET_AUDIO_MAP read face: one hold cycle, then the answer
  dut->am_wait_i = 1;
  dut->am_data_i = 0;
  if (dut->am_req_o) {
    if (am_cnt >= 1) {
      const bool out = dut->am_type_o == 0x000F;
      const unsigned port = dut->am_idx_o;
      const auto &ports = out ? map_out : map_in;
      uint64_t d = 0;
      if (port < ports.size()) {
        const MapPort &p = ports[port];
        if (dut->am_sel_o == 0) d = 1;
        else if (dut->am_sel_o == 1) d = (uint64_t(1) << 16) | (dut->am_map_o == 0 ? p.cur.size() : 0);
        else if (dut->am_sel_o == 2 && dut->am_map_o == 0 && dut->am_rec_o < p.cur.size())
          d = p.cur[dut->am_rec_o].packed();
      }
      dut->am_wait_i = 0;
      dut->am_data_i = d;
    }
  }
  // the format judge
  dut->fj_wait_i = 1;
  dut->fj_data_i = 0;
  if (dut->fj_req_o && fj_cnt >= 1) {
    const bool out = dut->fj_out_o;
    const unsigned s = dut->fj_idx_o;
    const uint64_t f = dut->fj_fmt_o;
    unsigned bits = 0;
    if (s < (out ? n_so : n_si)) {
      if (fmt_supported(out, s, f)) bits |= 1;
      //! bit 1: no mapping of this direction that names the stream uses a
      //! channel the proposed format does not have (Milan 5.4.2.7)
      bool survives = true;
      const unsigned ch = fmt_channels(f);
      for (const auto &p : out ? map_out : map_in)
        for (const auto &m : p.cur)
          if (m.si == s && ch != 0 && m.sc >= ch) survives = false;
      if (survives) bits |= 2;
    }
    dut->fj_wait_i = 0;
    dut->fj_data_i = bits;
  }
  // the edit face
  dut->mr_ent_rdy_i = dut->mr_req_o && mr.busy && mr.done_in < 0;
  dut->mr_done_i = mr.busy && mr.done_in == 0;
  dut->mr_ok_i = mr.ok;
  // the map edit beat, and the commit mark of the program in flight
  dut->me_stb_i = edit.on;
  dut->me_type_i = edit.type;
  dut->me_idx_i = edit.idx;
  dut->mk_stb_i = mark.on;
  dut->mk_mark_i = mark.cls;
  dut->mk_type_i = mark.type;
  dut->mk_idx_i = mark.idx;
}

static void drive_cycle() {
  dut->clk_i = 0;
  drive_ucpu();
  drive_maps();
  dut->cap_wr_i = cap.on;
  dut->cap_sink_i = cap.b.sink;
  dut->cap_bound_i = cap.b.bound;
  dut->cap_started_i = cap.b.started;
  dut->cap_sw_i = cap.b.sw;
  dut->cap_uid_i = cap.b.uid;
  dut->cap_teid_i = cap.b.teid;
  dut->cap_ceid_i = cap.b.ceid;
  dut->restore_go_i = restore_go;
  dut->snoop_off_i = !snoop_on;
  dut->mem_req_ready_i = !rd.busy;
  dut->mem_rsp_valid_i = rd.busy && rd.delay == 0;
  dut->mem_rsp_data_i = rd.busy ? lane(rd.addr) : 0;
  dut->mem_rsp_last_i = 1;
  dut->mem_rsp_err_i = rd.busy && rd.delay == 0 && match_read_fault(rd.addr) != nullptr;
  dut->mem_wr_done_i = wr.busy && wr.delay == 0;
  dut->mem_wr_err_i = dut->mem_wr_done_i && wr.err;
  dut->mem_wr_ready_i = !wr.busy;
  dut->dm_req_ready_i = !drd.busy;
  dut->dm_rsp_valid_i = drd.busy && drd.delay == 0;
  dut->dm_rsp_data_i = drd.busy ? desc_lane(drd.addr) : 0;
  dut->dm_rsp_last_i = drd.busy && drd.left == 1;
  dut->dm_rsp_err_i = 0;
  dut->eval();
  // same-edge triggers: a case may change this cycle's inputs on a condition
  for (auto &t : cycle_triggers)
    if (t && t()) {
      t = nullptr;
      dut->eval();
    }
}

static void sample_cycle() {
  const bool wtake = dut->mem_wr_valid_o && dut->mem_wr_ready_i;
  const bool wfin = dut->mem_wr_done_i;
  const bool rtake = dut->mem_req_valid_o && dut->mem_req_ready_i;
  const bool rfin = dut->mem_rsp_valid_i && dut->mem_rsp_ready_o;
  const bool dtake = dut->dm_req_valid_o && dut->dm_req_ready_i;

  // device-face operations, as the backend sees them
  if (dut->dev_gnt_o && !cur.active) {
    cur = OpTrack{};
    cur.active = true;
    cur.r = OpRec{unsigned(dut->dev_op_o), unsigned(dut->dev_region_o), cyc, cyc, 0, "open", 0, {}};
  }
  if (cur.active && dut->dev_wvalid_o && dut->dev_wready_o) {
    cur.r.bytes++;
    if (cur.r.op == 1) cur.r.wbytes.push_back(uint8_t(dut->dev_wdata_o));
  }
  if (cur.active && (dut->dev_done_o || dut->dev_err_o)) {
    cur.r.end = cyc;
    cur.r.res = dut->dev_done_o ? "done" : "err";
    evlog.ops.push_back(cur.r);
    cur.active = false;
  }

  // backend memory effects at the edge
  if (wfin) {
    if (!wr.err) mem_apply(wr.addr, wr.data, wr.strb);
    else evlog.mem_errs++;
    wr.busy = false;
  } else if (wr.busy && wr.delay > 0) {
    --wr.delay;
  }
  if (wtake) {
    const uint32_t off = dut->mem_wr_addr_o - kBase + first_lane(dut->mem_wr_strb_o);
    const uint8_t byte = uint8_t(dut->mem_wr_data_o >> (56 - 8 * first_lane(dut->mem_wr_strb_o)));
    wr = Wr{true, 2, dut->mem_wr_addr_o, dut->mem_wr_data_o, uint8_t(dut->mem_wr_strb_o), false};
    if (Fault *f = match_fault(off, byte)) {
      wr.err = true;
      if (f->count > 0) --f->count;
    }
  }
  if (rfin) {
    if (Fault *f = match_read_fault(rd.addr)) {
      if (f->count > 0) --f->count;
    }
    rd.busy = false;
  }
  else if (rd.busy && rd.delay > 0) --rd.delay;
  if (rtake) rd = Rd{true, 2, dut->mem_req_addr_o};

  // descriptor store memory: one beat per cycle after a two-cycle latency
  if (drd.busy && drd.delay == 0 && dut->dm_rsp_valid_i) {
    drd.addr += 8;
    if (--drd.left == 0) drd.busy = false;
  } else if (drd.busy && drd.delay > 0) {
    --drd.delay;
  }
  if (dtake) drd = DRd{true, 2, dut->dm_req_addr_o, unsigned(dut->dm_req_beats_o)};

  // a forced same-edge write
  if (forced.on) {
    if (dut->ub_ready_o && forced.rid >= 0)
      evlog.changes.push_back(Change{cyc, unsigned(forced.rid), forced.value});
    if (!dut->ub_ready_o) fatal("a forced write was not taken in its cycle");
    forced.on = false;
  }
  // the uCPU's handshakes
  edit.on = false;
  if (ust == U::Bus && pc < prog.size()) {
    UOp &o = prog[pc];
    bool done = false;
    switch (o.kind) {
      case UOp::DYN_WR:
      case UOp::NAME_WR:
      case UOp::IDENT_WR:
        if (dut->ub_ready_o) {
          done = true;
          if (o.rid >= 0) evlog.changes.push_back(Change{cyc, unsigned(o.rid), o.value});
        }
        break;
      case UOp::READ:
      case UOp::LOCATE:
        if (dut->ub_rvalid_o) {
          done = true;
          answers.emplace_back(o.tag, dut->ub_rdata_o);
          answer_err.emplace_back(o.tag, unsigned(dut->ub_err_o));
          u_after_read = true;
        }
        break;
      case UOp::GAP:
        ugap = o.gap;
        done = true;
        break;
      case UOp::MARK:
        //! OP_NVM_MARK: one strobe cycle, after the state write it marks
        mark = MarkQ{true, o.cls, o.type, o.idx};
        ust = U::Mark;
        done = true;
        break;
      case UOp::MAP_ADD:
      case UOp::MAP_REMOVE: {
        auto &p = o.out ? map_out[o.idx] : map_in[o.idx];
        bool ok = true;
        if (o.kind == UOp::MAP_ADD) {
          std::vector<Map> next = p.cur;
          next.insert(next.end(), o.maps.begin(), o.maps.end());
          ok = map_set_valid(o.out, o.idx, next);
          if (ok) p.cur = next;
        } else {
          for (const auto &m : o.maps)
            for (size_t i = 0; i < p.cur.size(); ++i)
              if (p.cur[i] == m) { p.cur.erase(p.cur.begin() + long(i)); break; }
        }
        answers.emplace_back(o.tag.empty() ? "map_cmd" : o.tag, ok ? 1 : 0);
        if (ok) {
          edit = EditQ{true, o.out ? 0x000Fu : 0x000Eu, o.idx};
          pend_mark = MarkQ{true, 6u, o.out ? 0x000Fu : 0x000Eu, o.idx};
          evlog.changes.push_back(Change{cyc + 1, unsigned((o.out ? 0x70 : 0x60) + o.idx),
                                         map_payload(o.out, o.idx)});
          ugap = kMapMarkTail;
        }
        done = true;
        break;
      }
    }
    if (done && ust != U::Mark) {
      ++pc;
      if (ugap) ust = U::Gap;
      else if (u_after_read) { ust = U::Gap; ugap = 1; }
    } else if (done) {
      ++pc;
    }
  } else if (ust == U::Gap) {
    if (ugap > 0) --ugap;
    if (ugap == 0 && pend_mark.on) {
      mark = pend_mark;
      pend_mark.on = false;
      ust = U::Mark;
    } else if (ugap == 0) {
      ust = U::Bus;
      u_after_read = false;
    }
  } else if (ust == U::Mark) {
    mark.on = false;
    ust = U::Bus;
  }
  if (ust == U::Bus && pc >= prog.size()) ust = U::Idle;

  // the map model's handshakes
  if (dut->am_req_o) ++am_cnt; else am_cnt = 0;
  if (dut->fj_req_o) ++fj_cnt; else fj_cnt = 0;
  if (dut->am_req_o && !dut->am_wait_i) am_cnt = 0;
  if (dut->fj_req_o && !dut->fj_wait_i) fj_cnt = 0;
  if (dut->mr_req_o && !mr.busy) mr = MrState{true, {}, -1, false};
  if (mr.busy && mr.done_in < 0 && dut->mr_ent_v_o && dut->mr_ent_rdy_i) {
    const uint64_t e = dut->mr_ent_o;
    mr.got.push_back(Map{uint16_t(e >> 48), uint16_t(e >> 32), uint16_t(e >> 16), uint16_t(e)});
  }
  if (mr.busy && mr.done_in < 0 && mr.got.size() == dut->mr_cnt_o) {
    //! judge the staged set whole, then apply it or nothing
    const bool out = dut->mr_type_o == 0x000F;
    const unsigned port = dut->mr_idx_o;
    auto &p = out ? map_out[port] : map_in[port];
    if (dut->mr_add_o) {
      std::vector<Map> next = p.cur;
      next.insert(next.end(), mr.got.begin(), mr.got.end());
      mr.ok = map_set_valid(out, port, next);
      if (mr.ok) p.cur = next;
    } else {
      for (const auto &m : mr.got)
        for (size_t i = 0; i < p.cur.size(); ++i)
          if (p.cur[i] == m) { p.cur.erase(p.cur.begin() + long(i)); break; }
      mr.ok = true;
    }
    mr.done_in = 1;
  } else if (mr.busy && mr.done_in > 0) {
    --mr.done_in;
  } else if (mr.busy && mr.done_in == 0) {
    mr.busy = false;
    mr.done_in = -1;
  }

  //! K15's premise: the binding manager samples busy in H_FL_REQ (encoding 13,
  //! checked against the donor's enum by run.py) in the D3 writer's grant cycle
  if (dut->m0_state_o == 13u && dut->arb_m1_gnt_o) ++evlog.collisions;

  // the durable reading and the ownership window
  const unsigned durable = dut->nvm_backed_o && !dut->nvm_dirty_o && !dut->nvm_stale_o && !dut->nvm_pend_o;
  if (durable != prev_durable) evlog.durable.emplace_back(cyc, durable);
  prev_durable = durable;
  //! the latch windows of steady state: an ownership window that STARTS
  //! after the writer's boot restore completed (the restore owns the bus
  //! for its whole walk, before the entity is enabled)
  if (dut->own_o) {
    if (!own_since && dut->d3_restore_done_o) own_since = cyc;
  } else if (own_since) {
    if (cyc - own_since > evlog.own_max) evlog.own_max = cyc - own_since;
    own_since = 0;
  }
  if (!evlog.restore_done_cyc && dut->restore_done_o) evlog.restore_done_cyc = cyc;
  if (!evlog.d3_done_cyc && dut->d3_restore_done_o) evlog.d3_done_cyc = cyc;

  dut->clk_i = 1;
  dut->eval();
  ++cyc;
  cap.on = false;
  dut->clk_i = 0;
  dut->eval();
}

void edge() {
  drive_cycle();
  sample_cycle();
}

[[noreturn]] void fatal(const char *why) {
  std::fprintf(stderr, "D3 FATAL at cycle %" PRIu64 ": %s\n", cyc, why);
  std::fflush(stdout);
  std::exit(3);
}

// --------------------------------------------------------------------- hooks
std::map<std::string, unsigned> hook_count;
struct Sched {
  std::string name;
  unsigned n;
  std::function<void()> fn;
  bool fired = false;
};
std::vector<Sched> sched;

void at(const std::string &name, unsigned n, std::function<void()> fn) {
  sched.push_back(Sched{name, n, std::move(fn)});
}
unsigned hooks(const std::string &name) {
  auto it = hook_count.find(name);
  return it == hook_count.end() ? 0 : it->second;
}
bool all_fired() {
  for (auto &s : sched)
    if (!s.fired) return false;
  return true;
}

void run_cycles(uint64_t n) {
  for (uint64_t i = 0; i < n; ++i) edge();
  host_catch_up();
}

bool run_until(const std::function<bool()> &pred, uint64_t max_cycles) {
  for (uint64_t i = 0; i < max_cycles; ++i) {
    if (pred()) {
      host_catch_up();
      return true;
    }
    edge();
  }
  host_catch_up();
  return pred();
}

void bind(const Binding &b) {
  cap.b = b;
  cap.on = true;
  edge();
  host_catch_up();
}

void program(const std::vector<UOp> &ops) { progs.push_back(ops); }
bool programs_idle() { return progs.empty() && ust == U::Idle; }

void csr_drive(unsigned word, uint32_t value) {
  dut->csr_sel_i = 1;
  dut->csr_we_i = 1;
  dut->csr_addr_i = word;
  dut->csr_wdata_i = value;
  if (word == 4) evlog.strobes.emplace_back(cyc, value);
  edge();
  dut->csr_sel_i = 0;
  dut->csr_we_i = 0;
}

uint32_t csr_peek(unsigned word) {
  const auto keep = dut->csr_addr_i;
  dut->csr_addr_i = word;
  dut->eval();
  const uint32_t v = dut->csr_rdata_o;
  dut->csr_addr_i = keep;
  dut->eval();
  return v;
}

bool dirty_bit(unsigned slot) { return bit_of(dut->d3_dirty_o, slot); }

bool writer_done_now() { return dut->d3_mdone_o; }

bool dut_dev_write_open(unsigned rid) {
  return cur.active && cur.r.op == 1 && cur.r.rid == rid && cur.r.bytes > 0;
}

int dut_dev_write_bytes(unsigned rid) {
  if (!(cur.active && cur.r.op == 1 && cur.r.rid == rid)) return -1;
  return int(cur.r.bytes);
}

unsigned m0_state() { return unsigned(dut->m0_state_o); }

void hold(bool on) {
  hold_on = on;
  dut->prog_busy_i = (ust != U::Idle) || hold_on;
}

void snoop(bool on) { snoop_on = on; }

//! from a same-edge trigger: put one dynamic-state write on the bus THIS
//! cycle (the uCPU must be idle), logged as a change when it is taken
bool force_dyn_write(unsigned sel, unsigned idx, uint64_t val, int rid,
                     const std::vector<uint8_t> &value) {
  if (!programs_idle() || dut->own_o) return false;
  dut->prog_busy_i = 1;
  dut->ub_req_i = 1;
  dut->ub_we_i = 1;
  dut->ub_name_i = 0;
  dut->ub_addr_i = (1u << 16) | (sel << 3);
  dut->ub_didx_i = idx;
  dut->ub_wdata_i = val;
  forced = Forced{true, rid, value};
  return true;
}

unsigned dirty_count() {
  const unsigned n = 1 + 1 + 1 + n_si + 2 * n_so + n_spi + n_spo + n_name;
  unsigned c = 0;
  for (unsigned s = 0; s < n; ++s) c += dirty_bit(s);
  return c;
}

void init(const std::vector<unsigned> &cls_in, const std::vector<unsigned> &cls_out) {
  ctx = std::make_unique<VerilatedContext>();
  dut = std::make_unique<Vd3_top>(ctx.get());
  map_in.assign(cls_in.size(), MapPort{});
  map_out.assign(cls_out.size(), MapPort{});
  for (size_t i = 0; i < cls_in.size(); ++i) map_in[i].clusters = cls_in[i];
  for (size_t i = 0; i < cls_out.size(); ++i) map_out[i].clusters = cls_out[i];
  dut->rst_n = 0;
  dut->csr_sel_i = dut->csr_we_i = 0;
  for (int n = 0; n < 8; ++n) edge();
  dut->rst_n = 1;
  edge();
}

void finish() {
  dut->final();
  dut.reset();
  ctx.reset();
}

Levels levels() {
  Levels l;
  l.backed = dut->nvm_backed_o;
  l.dirty = dut->nvm_dirty_o;
  l.stale = dut->nvm_stale_o;
  l.verdict = dut->nvm_verdict_o;
  l.img_valid = dut->nvm_img_valid_o;
  l.pend = dut->nvm_pend_o;
  l.unres = dut->nvm_unres_o;
  l.restore_busy = dut->restore_busy_o;
  l.restore_done = dut->restore_done_o;
  l.restore_fail = dut->restore_fail_o;
  l.blank = dut->restore_blank_o;
  l.alarm = dut->alarm_o;
  l.d3_alarm = dut->d3_alarm_o;
  l.d3_unfl = dut->d3_unflushed_o;
  l.d3_done = dut->d3_restore_done_o;
  l.d3_fail = dut->d3_restore_fail_o;
  l.rs_app = dut->d3_rs_applied_o;
  l.rs_ref = dut->d3_rs_refused_o;
  l.rs_blank = dut->d3_rs_blank_o;
  l.rs_rev = dut->d3_rs_reverted_o;
  l.d3_writes = dut->d3_writes_o;
  l.d3_slot = dut->d3_slot_o;
  l.d3_taint = dut->d3_taint_o;
  l.mgr_dirty = dut->mgr_dirty_o;
  l.port_busy = dut->port_busy_o;
  l.dev_busy = dut->dev_busy_o;
  l.desc_valid = dut->desc_img_valid_o;
  l.own = dut->own_o;
  return l;
}

}  // namespace d3

// ------------------------------------------------------------ the C seam
extern "C" void cosim_rtl_sync(uint64_t now_ns) {
  while (d3::cyc * COSIM_NS_PER_CYCLE < now_ns) d3::edge();
}

extern "C" uint64_t cosim_rtl_now_ns(void) { return d3::cyc * COSIM_NS_PER_CYCLE; }

extern "C" uint32_t cosim_rtl_csr_read(unsigned word) { return d3::csr_peek(word); }

extern "C" void cosim_rtl_csr_write(unsigned word, uint32_t value) {
  if (word == 0) {
    const uint32_t expect = uint32_t(uintptr_t(d3::area()));
    if (value != expect) d3::fatal("image base is not the staged record area");
    value = d3::kBase;
  }
  d3::csr_drive(word, value);
  if (word == 4 && (value & 0x2u) && !((d3::csr_peek(3) >> 20) & 1u)) {
    //! an ACCEPTED acknowledgement: the slots now hold what it retired
    const unsigned n = unsigned(d3::evlog.acks.size());
    char a[64], b[64];
    std::snprintf(a, sizeof a, "/ack%u-slotA.bin", n);
    std::snprintf(b, sizeof b, "/ack%u-slotB.bin", n);
    host_dump_file((d3::out_dir + a).c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u);
    host_dump_file((d3::out_dir + b).c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u,
                   0x10000u);
    d3::evlog.acks.emplace_back(d3::cyc, n);
  }
}

extern "C" void cosim_rtl_restore_go(unsigned level) { d3::restore_go = level; }

extern "C" void cosim_rtl_pp_ctrl(uint32_t value) {
  const bool en = value & 1u;
  if (en && !d3::prev_enable && !d3::evlog.enable_cyc) d3::evlog.enable_cyc = d3::cyc;
  d3::prev_enable = en;
  d3::restore_go = (value >> 1) & 1u;
}

extern "C" void cosim_rtl_levels(struct cosim_levels *l) {
  const auto v = d3::levels();
  l->backed = v.backed;
  l->dirty = v.dirty;
  l->stale = v.stale;
  l->verdict = v.verdict;
  l->img_valid = v.img_valid;
  l->pend = v.pend;
  l->unres = v.unres;
  l->restore_busy = v.restore_busy;
  l->restore_done = v.restore_done;
  l->restore_fail = v.restore_fail;
  l->blank = v.blank;
  l->alarm = v.alarm;
}

extern "C" void cosim_hook(const char *name, uint32_t value) {
  (void)value;
  const std::string key(name);
  const unsigned n = ++d3::hook_count[key];
  for (size_t i = 0; i < d3::sched.size(); ++i) {
    if (!d3::sched[i].fired && d3::sched[i].name == key && d3::sched[i].n == n) {
      d3::sched[i].fired = true;
      auto fn = d3::sched[i].fn;
      fn();
    }
  }
}

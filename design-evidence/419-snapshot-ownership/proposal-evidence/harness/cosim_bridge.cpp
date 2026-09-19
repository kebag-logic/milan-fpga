// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #419 round 3 co-simulation: the Verilated RTL (cosim_top.sv), its
// bus-functional models and the one clock shared with the host model.
//
// WHAT IS REAL HERE: every RTL module the wrapper instantiates. WHAT IS A
// MODEL: the main-memory bridge (one outstanding single-beat write, done
// three cycles after acceptance; one outstanding one-beat read), with
// per-byte fault injection, and the device-face BFM (bfm_*), which is used
// only where a case says so.
#include "cosim_bridge.h"

#include "Vcosim_top.h"
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
#include <vector>

extern "C" {
#include "nvm_host.h"
}

namespace cosim {

constexpr uint32_t kBase = 0x40000000u;   // the backend's view of the area
constexpr uint32_t kRoom = 0x10000u - 44u;

std::unique_ptr<VerilatedContext> ctx;
std::unique_ptr<Vcosim_top> dut;
uint64_t cyc = 0;
Log evlog;

uint8_t *area() { return nvm_host_ddr + NVM_HOST_IMAGE_OFF + 40u; }

// ---------------------------------------------------------------- memory model
std::vector<Fault> faults;

struct Wr {
  bool busy = false;
  int delay = 0;
  uint32_t addr = 0;
  uint64_t data = 0;
  uint8_t strb = 0;
  bool err = false;
  bool silent = false;
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

uint32_t wr_off(uint32_t addr, uint8_t strb) {
  return addr - kBase + first_lane(strb);
}

uint8_t wr_byte(uint64_t data, uint8_t strb) {
  const unsigned n = first_lane(strb);
  return uint8_t(data >> (56 - 8 * n));
}

Fault *match_fault(uint32_t off, uint8_t byte, int mode) {
  for (auto &f : faults) {
    if (f.count == 0 || f.off != off || f.mode != mode) continue;
    if (f.kind == 1 && byte != 0xFF) continue;
    if (f.kind == 2 && byte == 0xFF) continue;
    return &f;
  }
  return nullptr;
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

// ------------------------------------------------------------ device-face BFM
std::deque<BfmOp> bfm_q;
enum class Bst { Idle, Req, Data, Wait } bst = Bst::Idle;
BfmOp bcur;
unsigned b_sent = 0;
int b_pace = 0;
bool b_sel = false;
bool b_resume = false;

// ---------------------------------------------------------------- op tracking
struct OpTrack {
  bool active = false;
  bool bfm = false;
  unsigned op = 0, rid = 0;
  uint64_t req = 0, gnt = 0;
  unsigned bytes = 0;
};
OpTrack cur;
bool req_seen = false;
uint64_t req_since = 0;

// --------------------------------------------------------------- harness pulse
struct CapPulse {
  bool on = false;
  Binding b;
} cap;
struct DynPulse {
  bool on = false;
  unsigned sel = 0, idx = 0;
  uint64_t val = 0;
} dyn;
unsigned restore_go = 0;
unsigned d1 = 0;
unsigned prev_backed = 0;

std::vector<Preload> preloads;

// ---------------------------------------------------------------------- edge
void drive_bfm() {
  dut->bfm_sel_i = b_sel;
  dut->bfm_req_i = 0;
  dut->bfm_wvalid_i = 0;
  dut->bfm_rready_i = 0;
  if (!b_sel) return;
  dut->bfm_op_i = bcur.op;
  dut->bfm_region_i = bcur.rid;
  dut->bfm_offset_i = bcur.offset;
  dut->bfm_len_i = bcur.len;
  if (bst == Bst::Req) dut->bfm_req_i = 1;
  if (bst == Bst::Data && b_pace == 0 && b_sent < bcur.data.size() &&
      (bcur.stop_after < 0 || int(b_sent) < bcur.stop_after || b_resume)) {
    dut->bfm_wvalid_i = 1;
    dut->bfm_wdata_i = bcur.data[b_sent];
  }
}

void bfm_start_if_possible() {
  if (bst != Bst::Idle || bfm_q.empty()) return;
  // one initiator at a time: the port must be idle in its whole logical
  // operation, and the backend must be idle
  if (dut->port_busy_o || dut->dev_busy_o || dut->dev_req_o) return;
  bcur = bfm_q.front();
  bfm_q.pop_front();
  b_sent = 0;
  b_pace = 0;
  b_resume = false;
  b_sel = true;
  bst = Bst::Req;
}

void edge() {
  dut->clk_i = 0;
  bfm_start_if_possible();
  drive_bfm();
  dut->cap_wr_i = cap.on;
  dut->cap_sink_i = cap.b.sink;
  dut->cap_bound_i = cap.b.bound;
  dut->cap_started_i = cap.b.started;
  dut->cap_sw_i = cap.b.sw;
  dut->cap_uid_i = cap.b.uid;
  dut->cap_teid_i = cap.b.teid;
  dut->cap_ceid_i = cap.b.ceid;
  dut->dyn_wr_i = dyn.on;
  dut->dyn_sel_i = dyn.sel;
  dut->dyn_idx_i = dyn.idx;
  dut->dyn_val_i = dyn.val;
  dut->restore_go_i = restore_go;
  dut->d1_en_i = d1;
  dut->mem_req_ready_i = !rd.busy;
  dut->mem_rsp_valid_i = rd.busy && rd.delay == 0;
  dut->mem_rsp_data_i = rd.busy ? lane(rd.addr) : 0;
  dut->mem_rsp_last_i = 1;
  dut->mem_rsp_err_i = 0;
  dut->mem_wr_done_i = wr.busy && !wr.silent && wr.delay == 0;
  dut->mem_wr_err_i = dut->mem_wr_done_i && wr.err;
  dut->mem_wr_ready_i = 0;
  dut->eval();
  // readiness: withheld while a no-ready fault names the presented byte
  bool ready = !wr.busy;
  if (ready && dut->mem_wr_valid_o) {
    const uint32_t off = wr_off(dut->mem_wr_addr_o, dut->mem_wr_strb_o);
    if (match_fault(off, wr_byte(dut->mem_wr_data_o, dut->mem_wr_strb_o), 2))
      ready = false;
  }
  dut->mem_wr_ready_i = ready;
  dut->eval();

  // ---- sample the cycle -------------------------------------------------
  const bool wtake = dut->mem_wr_valid_o && dut->mem_wr_ready_i;
  const bool wfin = dut->mem_wr_done_i;
  const bool rtake = dut->mem_req_valid_o && dut->mem_req_ready_i;
  const bool rfin = dut->mem_rsp_valid_i && dut->mem_rsp_ready_o;

  // device-face operation tracking (the backend's view)
  if (dut->dev_req_o && !req_seen) {
    req_seen = true;
    req_since = cyc;
  }
  if (dut->dev_gnt_o && !cur.active) {
    cur = OpTrack{};
    cur.active = true;
    cur.bfm = b_sel;
    cur.op = dut->dev_op_o;
    cur.rid = dut->dev_region_o;
    cur.req = req_since;
    cur.gnt = cyc;
    req_seen = false;
    evlog.ops.push_back(OpRec{cur.bfm, cur.op, cur.rid, cur.req, cur.gnt, 0, "open", 0});
  }
  if (cur.active && wtake) cur.bytes++;
  if (cur.active && (dut->dev_done_o || dut->dev_err_o)) {
    auto &r = evlog.ops.back();
    r.end = cyc;
    r.res = dut->dev_done_o ? "done" : "err";
    r.bytes = cur.bytes;
    cur.active = false;
  }
  if (cur.active && !evlog.ops.empty()) evlog.ops.back().bytes = cur.bytes;

  // the BFM's own handshake
  if (b_sel) {
    if (bst == Bst::Req && dut->dev_gnt_o) {
      bst = (bcur.op == 1) ? Bst::Data : Bst::Wait;
    } else if (bst == Bst::Data) {
      if (dut->bfm_wvalid_i && dut->dev_wready_o) {
        ++b_sent;
        b_pace = bcur.pace;
        if (b_sent == bcur.data.size()) bst = Bst::Wait;
      } else if (b_pace > 0) {
        --b_pace;
      }
      if (dut->dev_done_o || dut->dev_err_o) bst = Bst::Idle;   // ended early
    } else if (bst == Bst::Wait) {
      if (dut->dev_done_o || dut->dev_err_o) bst = Bst::Idle;
    }
    if (bst == Bst::Idle) b_sel = false;
  }

  // the preload face (pre_ready is tied high: accepted on valid)
  if (dut->pre_valid_o)
    preloads.push_back(Preload{unsigned(dut->pre_sink_o), dut->pre_talker_eid_o,
                               unsigned(dut->pre_talker_uid_o), dut->pre_ctlr_eid_o,
                               unsigned(dut->pre_sw_o), unsigned(dut->pre_started_o)});

  // memory effects at the edge
  if (wfin) {
    if (!wr.err) mem_apply(wr.addr, wr.data, wr.strb);
    else evlog.mem_errs++;
    wr.busy = false;
  } else if (wr.busy && !wr.silent && wr.delay > 0) {
    --wr.delay;
  }
  if (wtake) {
    const uint32_t off = wr_off(dut->mem_wr_addr_o, dut->mem_wr_strb_o);
    const uint8_t byte = wr_byte(dut->mem_wr_data_o, dut->mem_wr_strb_o);
    wr = Wr{true, 2, dut->mem_wr_addr_o, dut->mem_wr_data_o,
            uint8_t(dut->mem_wr_strb_o), false, false};
    evlog.mem_accepts++;
    if (Fault *f = match_fault(off, byte, 0)) {       // completes with error
      wr.err = true;
      if (f->count > 0) --f->count;
    } else if (Fault *s = match_fault(off, byte, 1)) { // accepted, then silent
      wr.silent = true;
      mem_apply(wr.addr, wr.data, wr.strb);           // worst case: it landed
      if (s->count > 0) --s->count;
      evlog.silent++;
    } else if (Fault *d = match_fault(off, byte, 3)) { // a slow completion
      wr.delay = d->delay;
      if (d->count > 0) --d->count;
      evlog.slow++;
    }
  }
  if (rfin) rd.busy = false;
  else if (rd.busy && rd.delay > 0) --rd.delay;
  if (rtake) rd = Rd{true, 2, dut->mem_req_addr_o};

  // every fall of nvm_backed and every cycle holding (1, 0, 1), per cycle
  if (prev_backed && !dut->nvm_backed_o) evlog.loss_cycles.push_back(cyc);
  if (dut->nvm_backed_o && !dut->nvm_dirty_o && dut->nvm_stale_o) ++evlog.bad101;
  prev_backed = dut->nvm_backed_o;

  dut->clk_i = 1;
  dut->eval();
  ++cyc;
  cap.on = false;
  dyn.on = false;
  dut->clk_i = 0;
  dut->eval();
}

[[noreturn]] void fatal(const char *why) {
  std::fprintf(stderr, "COSIM FATAL at cycle %" PRIu64 ": %s\n", cyc, why);
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

void stall_ms(uint64_t ms) { run_cycles(ms * 1000000ull / COSIM_NS_PER_CYCLE); }

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

void dyn_write(unsigned sel, unsigned idx, uint64_t val) {
  dyn = DynPulse{true, sel, idx, val};
  edge();
  host_catch_up();
}

void bfm(const BfmOp &op) { bfm_q.push_back(op); }
bool bfm_write_done_now() {
  return b_sel && bst == Bst::Wait && bcur.op == 1 && dut->dev_done_o;
}
bool bfm_req_pending() { return b_sel && bst == Bst::Req; }
void bfm_resume() { b_resume = true; }
bool bfm_idle() { return bst == Bst::Idle && bfm_q.empty(); }

void csr_drive(unsigned word, uint32_t value) {
  dut->csr_sel_i = 1;
  dut->csr_we_i = 1;
  dut->csr_addr_i = word;
  dut->csr_wdata_i = value;
  if (word == 4) evlog.strobes.push_back(StrobeRec{cyc, value, false});
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

void stray(unsigned word, uint32_t value) {
  csr_drive(word, value);
  evlog.strobes.back().stray = true;
  host_catch_up();
}

void reset_rtl() {
  dut->rst_n = 0;
  for (int n = 0; n < 4; ++n) edge();
  dut->rst_n = 1;
  edge();
  wr = Wr{};
  rd = Rd{};
  bst = Bst::Idle;
  b_sel = false;
  cur = OpTrack{};
  req_seen = false;
  host_catch_up();
}

void init(unsigned d1_en) {
  ctx = std::make_unique<VerilatedContext>();
  dut = std::make_unique<Vcosim_top>(ctx.get());
  d1 = d1_en;
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
  l.dirty_pub = dut->nvm_dirty_o;
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
  l.mgr_dirty = dut->mgr_dirty_o;
  l.port_busy = dut->port_busy_o;
  l.dev_busy = dut->dev_busy_o;
  l.dyn_dirty = dut->dyn_dirty_o;
  l.dyn_fmt0 = dut->dyn_fmt_in0_o;
  l.dyn_fmt0_v = dut->dyn_fmt_in0_v_o;
  return l;
}

}  // namespace cosim

// ------------------------------------------------------------ the C seam
extern "C" void cosim_rtl_sync(uint64_t now_ns) {
  while (cosim::cyc * COSIM_NS_PER_CYCLE < now_ns) cosim::edge();
}

extern "C" uint64_t cosim_rtl_now_ns(void) { return cosim::cyc * COSIM_NS_PER_CYCLE; }

extern "C" uint32_t cosim_rtl_csr_read(unsigned word) { return cosim::csr_peek(word); }

extern "C" void cosim_rtl_csr_write(unsigned word, uint32_t value) {
  if (word == 0) {
    // the firmware writes a host pointer; the backend sees a fixed, aligned
    // simulation address for the same byte, and nothing else is translated
    const uint32_t expect = uint32_t(uintptr_t(cosim::area()));
    if (value != expect) cosim::fatal("image base is not the staged record area");
    value = cosim::kBase;
  }
  cosim::csr_drive(word, value);
}

extern "C" void cosim_rtl_restore_go(unsigned level) { cosim::restore_go = level; }

extern "C" void cosim_rtl_levels(struct cosim_levels *l) {
  const auto v = cosim::levels();
  l->backed = v.backed;
  l->dirty = v.dirty_pub;
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
  const std::string key(name);
  const unsigned n = ++cosim::hook_count[key];
  cosim::evlog.hooks.push_back(cosim::HookRec{key, n, cosim::cyc, value});
  // by index, and by copy: an action may schedule another one
  for (size_t i = 0; i < cosim::sched.size(); ++i) {
    if (!cosim::sched[i].fired && cosim::sched[i].name == key && cosim::sched[i].n == n) {
      cosim::sched[i].fired = true;
      auto fn = cosim::sched[i].fn;
      fn();
    }
  }
}

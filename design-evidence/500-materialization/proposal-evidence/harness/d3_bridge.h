// SPDX-License-Identifier: CERN-OHL-W-2.0
// The D3 co-simulation: the bridge's types and entry points (design evidence,
// milan-fpga #500). Derived from tb/verilator/nvm_cosim/cosim_bridge.h.
#pragma once

#include <cstdint>
#include <deque>
#include <functional>
#include <map>
#include <string>
#include <vector>

#include "d3_api.h"

namespace d3 {

//! a memory-bridge fault on the byte at record-area offset `off`
//! mode 0: accepted, completes WITH ERROR, the byte is not written
//! kind 0: any byte, 1: only an erase byte (0xFF), 2: only a data byte
struct Fault {
  uint32_t off;
  int mode;
  int kind;
  int count;
  int pass = -1;          //! mode 1 only: the D3 pass it waits for (-1 any)
};
extern std::vector<Fault> faults;

//! A backend memory READ response HELD BACK (the restore containment cases).
//! It matches the nth memory read issued while the device face serves record
//! `rid` (any record if -1) in D3 pass `pass` (-1 any), and is released after
//! `hold` cycles (-1: never, silence), when the D3 writer's watchdog count
//! reaches `wd_release` (just before the deadline), or `after_abort` cycles
//! after the writer's abort (just after it). Only one hold is armed at once.
struct RdHold {
  bool armed = false;
  int rid = -1;
  int pass = -1;
  unsigned nth = 1;
  int64_t hold = -1;
  int64_t wd_release = -1;
  int64_t after_abort = -1;
  //! the same two releases keyed to the BINDING walk's deadline (seam S3):
  //! when its watchdog reaches m0_wd_release, or after_m0_abort cycles after
  //! it abandoned the read
  int64_t m0_wd_release = -1;
  int64_t after_m0_abort = -1;
  // observed
  unsigned seen = 0;
  bool active = false;
  bool released = false;
  uint64_t start = 0, end = 0;
  unsigned rid_seen = 0, pass_seen = 0;
  uint64_t wd_max = 0;      //! the writer's largest watchdog count while held
  uint64_t m0_wd_max = 0;   //! the binding manager's largest count while held
};
extern RdHold rdhold;

//! a face that stops answering from a trigger on: the GET_AUDIO_MAP read face
//! (am), the format judge (fj) or the map edit face (mr). It is silent from
//! the first request in D3 pass `pass` until the writer aborts (the face is
//! then healthy again, so the entity it recovers into works)
struct FaceSilence {
  int face = 0;           //! 0 none, 1 am, 2 fj, 3 mr
  int pass = 1;
  bool active = false, done = false;
  uint64_t start = 0;
};
extern FaceSilence facesil;

//! the descriptor store's memory face answers every beat with an error once
//! armed (the roll-back's re-walk then cannot validate the image)
extern bool desc_mem_fail;
//! arm desc_mem_fail when the roll-back's scoped reset rises
extern bool desc_fail_on_rollback;
//! the descriptor memory (the integrator's bridge behind an asynchronous
//! request FIFO): requests are ACCEPTED while earlier bursts are still owed
//! and served in order, as the parent's CDC FIFO in front of pp_desc_bridge
//! does; an error beat ends its burst (the bridge's err rides with blast).
//! One-shot faults on it, each armed by a case:
//!  - desc_delay_next: the first-beat latency of the next request accepted
//!    after arming (-1 none);
//!  - desc_err_next: the next request accepted after arming answers its
//!    first beat with an error, and only that beat;
//! and the reviewer R217's own trigger: desc_delay_after_apply arms
//! desc_delay_next on the first request accepted after the D3 writer's
//! applied count first reads non-zero.
extern int64_t desc_delay_next;
extern bool desc_err_next;
extern int64_t desc_delay_after_apply;
//! the SET_STREAM_FORMAT verdict the model applies: false = the SYNTHETIC
//! judge (a narrower 1/2/4/6/8-channel AAF format no wider than the default
//! is admitted in either direction, which the product does NOT do for an
//! output), true = the SHIPPING judge transcribed from milan_datapath.sv's
//! sfv_supported_w (an output admits exactly its declared format, an input
//! the 1/2/4/6/8 family on the declared base, a CRF row its own format)
extern bool judge_shipping;
//! a bench script requests the entity enable before the restore (the enable
//! request is held from reset): the entity must stay dark until done
extern bool early_enable;

struct Binding {
  unsigned sink = 0;
  unsigned bound = 1, started = 1, sw = 0;
  unsigned uid = 1;
  uint64_t teid = 0;
  uint64_t ceid = 0;
};

// ---- the pinned listener's producers (revision d, seam S4) ------------------
//! the listener's own entity_id (d3_top LSN_EID_C): a transaction targets it
constexpr uint64_t kLsnEid = 0x0011223344556677ull;
//! ACMP message types (pp_acmp_pkg)
constexpr unsigned kBindRx = 6, kUnbindRx = 8, kGetRxState = 10;
//! the RX slot handle that means "no payload" (pp_pkg PP_SLOT_NULL_C)
constexpr unsigned kSlotNull = 7;

//! A work item a producer presents to one of the listener's faces, from
//! cycle `from` on; the producer pops it on its face's handshake (the gate
//! masks that handshake while it owns the faces) and never withdraws it
//! before. A PERSISTENT producer (`persist`) presents the same item again
//! after every pop, as a held event level or a polling controller does,
//! until a pop at or after cycle `until` (0: for ever). The START/STOP face's
//! producer is the AECP engine, which holds its request until the listener
//! completes it (a persistent one then asks the opposite value).
struct LtItem {
  uint64_t from = 0;
  uint64_t until = 0;          //! a persistent item's last pop is the first from here
  bool persist = false;
  unsigned msg = kGetRxState, status = 0, uid = 0, slot = kSlotNull;
  uint64_t target = kLsnEid, ctlr = 0x0C0C0C0C0C0C0C0Cull;
  unsigned seq = 0;
  unsigned kind = 0, failed = 0, sink = 0, val = 0;   //! TK event / START-STOP
  //! observed
  unsigned pops = 0;
};
extern std::deque<LtItem> lt_txnq, lt_tkq, lt_strq;
//! injected expiries of owner `owner`, every `every` cycles in [from, until)
struct LtExp {
  bool on = false;
  uint64_t from = 0, until = 0;
  unsigned every = 1, owner = 32;
  unsigned injected = 0, injected_owned = 0;
};
extern LtExp lt_exp;
//! an RX slot's payload bytes (the ACMPDU a transaction's rx_slot names)
extern uint8_t lt_rxs[4][576];
//! what the listener lived through while the gate owned its faces, and the
//! release as the listener saw it
struct LtObs {
  uint64_t release = 0;        //! the first cycle the gate reads released
  uint64_t drained = 0;        //! the last cycle it still owned the faces
  unsigned states_owned = 0;   //! bitmask of listener states seen while owned
  unsigned side_owned = 0;     //! listener side effects while owned
  unsigned takes_owned = 0;    //! txn / TK / START-STOP / expiry takes while owned
  uint64_t pre_offer = 0;      //! the cycle the current preload was first presented
  uint64_t pre_first = 0;      //! the walk's first preload offer
  unsigned pre_wait_max = 0;   //! the longest a preload offer lasted untaken
  unsigned pre_withdrawn = 0;  //! offers that ended without a take
  unsigned pre_open = 0;       //! an offer still open when the case ended
  uint64_t first_walk_after = 0; //! the first cycle after release the listener left X_IDLE
};
extern LtObs ltobs;
bool lt_owned_now();
bool lt_released_now();
unsigned lt_state_now();
//! the gate still owns the faces and releases them at this cycle's edge
bool lt_drained_now();
//! re-drive the listener's producers from a same-edge trigger
void lt_drive_now();
//! the gate's count of listener-owner expiries it did not admit
unsigned lt_exp_dropped();
//! the listener takes a preload at this cycle's edge (its pre_ready_o AND valid)
bool pre_take_now();
//! close an offer still open at the end of a case (it waited until then)
void lt_close_offers();

//! one AUDIO_MAPPING: {stream_index, stream_channel, cluster_offset,
//! cluster_channel}, 1722.1-2021 7.4.44
struct Map {
  uint16_t si, sc, co, cc;
  uint64_t packed() const {
    return (uint64_t(si) << 48) | (uint64_t(sc) << 32) | (uint64_t(co) << 16) | cc;
  }
  bool operator==(const Map &o) const { return si == o.si && sc == o.sc && co == o.co && cc == o.cc; }
};

//! one uCPU state-bus operation inside a program
struct UOp {
  //! FMT_WR: SET_STREAM_FORMAT, judged when it runs (the program's
  //! verdict): accepted it is a DYN_WR of the format, refused it writes
  //! nothing and notes the refusal under its tag
  enum Kind { DYN_WR, NAME_WR, READ, LOCATE, GAP, MAP_ADD, MAP_REMOVE, IDENT_WR, MARK, FMT_WR } kind;
  unsigned sel = 0, idx = 0;       //! DYN_WR/READ: selector and descriptor index
  unsigned cls = 0, type = 0;      //! MARK: the class and the descriptor type (idx: its index)
  uint64_t val = 0;                //! DYN_WR/NAME_WR: the data; LOCATE: the key
  uint32_t addr = 0;               //! READ: the address; NAME_WR: the lane address
  bool name = false;               //! READ: the name table
  unsigned gap = 0;                //! GAP: idle cycles
  bool out = false;                //! MAP_*: 0 STREAM_PORT_INPUT, 1 OUTPUT
  std::vector<Map> maps;           //! MAP_*: the mappings
  std::string tag;                 //! READ/LOCATE: where the answer is noted
  int rid = -1;                    //! the record the op changes (-1 none)
  std::vector<uint8_t> value;      //! the record payload after the op (the oracle's)
};

struct OpRec {
  unsigned op, rid;
  uint64_t req, gnt, end;
  std::string res;
  unsigned bytes;
  std::vector<uint8_t> wbytes;     //! WRITE: the bytes the device face took
};

struct Change {                    //! an accepted change, for the durability oracle
  uint64_t cyc;
  unsigned rid;
  std::vector<uint8_t> value;
};

struct Log {
  //! restore writes as the model sees them: the writer's state-bus writes
  //! taken, the map sets it staged and the model applied, and its roll-back
  std::vector<std::pair<uint64_t, std::string>> rs_writes;
  uint64_t fw_enable_cyc = 0, terminal_cyc = 0, abort_cyc = 0, rb_cyc = 0;
  unsigned abort_cause = 0;
  std::vector<OpRec> ops;
  std::vector<Change> changes;
  std::vector<std::pair<uint64_t, unsigned>> durable;   //! (cycle, reading)
  std::vector<std::pair<uint64_t, unsigned>> acks;      //! (cycle, index of the dump)
  std::vector<std::pair<uint64_t, uint32_t>> strobes;
  std::vector<std::pair<std::string, uint64_t>> marks;  //! named cycles
  uint64_t enable_cyc = 0, restore_done_cyc = 0, d3_done_cyc = 0, own_max = 0;
  //! the binding walk: its terminal (done, failed or not), the cycle it
  //! abandoned a read to the drain, and every preload it drove
  uint64_t mgr_done_cyc = 0, m0_abort_cyc = 0;
  //! the firmware's restore go (PP_CTRL[1]) first read 1
  uint64_t go_cyc = 0;
  std::vector<std::pair<uint64_t, unsigned>> preloads;
  //! the roll-back: when its reset was released (after any memory debt)
  uint64_t rb_end_cyc = 0;
  //! the descriptor memory: a delayed request (accepted, first beat), an
  //! injected error beat, and the cycles the guard's debt rose and fell
  uint64_t desc_delay_acc = 0, desc_delay_beat = 0, desc_err_cyc = 0;
  std::vector<std::pair<uint64_t, unsigned>> desc_debt;
  uint64_t prog_waited_on_own = 0;
  unsigned mem_errs = 0;
  //! cycles in which the binding manager sat in H_FL_REQ while the arbiter
  //! granted the D3 writer: case K15's premise
  unsigned collisions = 0;
  //! THE LISTENER (revision d). Its acceptances at its faces and the
  //! producers' pops, per kind: how many, how many while the gate owned the
  //! faces, the first kLtFirst cycles and the last one (a held level makes
  //! one a cycle, so they are counted, never listed whole); and per face the
  //! cycles in which the producer's pop and the listener's take disagreed
  struct LtAgg {
    uint64_t n = 0, n_owned = 0, last = 0;
    std::vector<uint64_t> first;
  };
  std::map<std::string, LtAgg> ltagg;
  unsigned mismatch_txn = 0, mismatch_tk = 0;
  //! its record writes, one entry per RUN of identical writes (first and
  //! last cycle, how many), its A4 discovery arms, its side effects (the
  //! first kLtSide, and how many) and the ACMP PDUs it sent
  struct LRec {
    uint64_t cyc, last, n;
    unsigned sink, bound, started, sw, sm;
    uint64_t teid;
  };
  std::vector<LRec> lrec;
  unsigned lside_n = 0;
  struct LArm {
    uint64_t cyc;
    unsigned sink;
    uint64_t eid;
  };
  std::vector<LArm> larm;
  std::vector<std::pair<uint64_t, unsigned>> lside;
  struct LTx {
    uint64_t cyc;
    unsigned msg, status, luid, cc, flags;
    uint64_t teid;
  };
  std::vector<LTx> ltx;
};
extern Log evlog;

struct Levels {
  unsigned backed, dirty, stale, verdict, img_valid, pend, unres;
  unsigned restore_busy, restore_done, restore_fail, blank, alarm;
  unsigned d3_alarm, d3_unfl, d3_done, d3_fail, rs_app, rs_ref, rs_blank, rs_rev;
  unsigned d3_writes, d3_slot, d3_taint, mgr_dirty, port_busy, dev_busy, desc_valid, own;
  unsigned d3_rb, d3_closed, d3_cause, entity_en;
  unsigned mgr_done, mgr_fail, mgr_blank, mgr_cause, desc_debt, d3_pass;
};

extern uint64_t cyc;
extern std::string out_dir;
extern unsigned n_si, n_so, n_spi, n_spo, n_name;

[[noreturn]] void fatal(const char *why);
void init(const std::vector<unsigned> &cls_in, const std::vector<unsigned> &cls_out);
void finish();
void edge();
void run_cycles(uint64_t n);
bool run_until(const std::function<bool()> &pred, uint64_t max_cycles);
void at(const std::string &name, unsigned n, std::function<void()> fn);
unsigned hooks(const std::string &name);
bool all_fired();
void bind(const Binding &b);
uint32_t csr_peek(unsigned word);
Levels levels();
uint8_t *area();
bool dirty_bit(unsigned slot);
bool writer_done_now();
//! the device face has a WRITE of `rid` open this cycle (granted, not ended)
bool dut_dev_write_open(unsigned rid);
//! bytes the device face has taken for an open WRITE of `rid`, or -1
int dut_dev_write_bytes(unsigned rid);
//! the binding manager's state (KL_acmp_nvm_shadow hs_r encoding)
unsigned m0_state();
//! hold prog_busy_i high whatever the uCPU does (case K15 aligns the D3
//! writer's latch with it); releasing takes effect in the calling cycle
void hold(bool on);
//! the writer's change snoop (a harness knob for the stale-store control)
void snoop(bool on);
bool force_dyn_write(unsigned sel, unsigned idx, uint64_t val, int rid,
                     const std::vector<uint8_t> &value);
unsigned dirty_count();
//! lend the state bus to the uCPU BFM before the restore (harness knob)
void lend(bool on);
//! the harness peeks: a dynamic-state row (value, valid) and a name
std::pair<uint64_t, unsigned> peek_row(unsigned sel, unsigned idx);
std::vector<uint8_t> peek_name(unsigned ord);
//! a snapshot of every restorable row, name and map set, as one JSON object
std::string snapshot_json();
//! snapshots the bridge takes itself: when the D3 walk starts, when its
//! pass 1 starts (the names after the image walk) and at its terminal
extern std::string snap_prerestore, snap_pass1, snap_terminal;

//! the uCPU: queue a program; it starts when no program runs and the writer
//! does not own the bus, and runs to its end
void program(const std::vector<UOp> &ops);
bool programs_idle();
//! the answers READ and LOCATE ops noted, by tag
extern std::vector<std::pair<std::string, uint64_t>> answers;
extern std::vector<std::pair<std::string, unsigned>> answer_err;

//! the map model (the parent's map plane)
struct MapPort {
  unsigned clusters = 0;
  std::vector<Map> cur, def;
};
extern std::vector<MapPort> map_in, map_out;
//! image-default formats and supported ceilings per stream (from the image)
extern std::vector<uint64_t> def_fmt_in, def_fmt_out;
uint64_t live_fmt(bool out, unsigned s);
unsigned fmt_channels(uint64_t f);
bool fmt_supported(bool out, unsigned s, uint64_t f);
bool map_set_valid(bool out, unsigned port, const std::vector<Map> &set);
std::vector<uint8_t> map_payload(bool out, unsigned port);
//! a trigger evaluated at every cycle, before the edge (for same-edge cases)
void on_cycle(std::function<bool()> fn);

}  // namespace d3

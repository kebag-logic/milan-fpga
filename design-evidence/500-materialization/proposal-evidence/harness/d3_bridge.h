// SPDX-License-Identifier: CERN-OHL-W-2.0
// The D3 co-simulation: the bridge's types and entry points (design evidence,
// milan-fpga #500). Derived from tb/verilator/nvm_cosim/cosim_bridge.h.
#pragma once

#include <cstdint>
#include <functional>
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
};
extern std::vector<Fault> faults;

struct Binding {
  unsigned sink = 0;
  unsigned bound = 1, started = 1, sw = 0;
  unsigned uid = 1;
  uint64_t teid = 0;
  uint64_t ceid = 0;
};

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
  enum Kind { DYN_WR, NAME_WR, READ, LOCATE, GAP, MAP_ADD, MAP_REMOVE, IDENT_WR, MARK } kind;
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
  std::vector<OpRec> ops;
  std::vector<Change> changes;
  std::vector<std::pair<uint64_t, unsigned>> durable;   //! (cycle, reading)
  std::vector<std::pair<uint64_t, unsigned>> acks;      //! (cycle, index of the dump)
  std::vector<std::pair<uint64_t, uint32_t>> strobes;
  std::vector<std::pair<std::string, uint64_t>> marks;  //! named cycles
  uint64_t enable_cyc = 0, restore_done_cyc = 0, d3_done_cyc = 0, own_max = 0;
  uint64_t prog_waited_on_own = 0;
  unsigned mem_errs = 0;
  //! cycles in which the binding manager sat in H_FL_REQ while the arbiter
  //! granted the D3 writer: case K15's premise
  unsigned collisions = 0;
};
extern Log evlog;

struct Levels {
  unsigned backed, dirty, stale, verdict, img_valid, pend, unres;
  unsigned restore_busy, restore_done, restore_fail, blank, alarm;
  unsigned d3_alarm, d3_unfl, d3_done, d3_fail, rs_app, rs_ref, rs_blank, rs_rev;
  unsigned d3_writes, d3_slot, d3_taint, mgr_dirty, port_busy, dev_busy, desc_valid, own;
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

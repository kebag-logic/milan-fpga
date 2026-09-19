// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #419 round 3 co-simulation: the bridge's types and entry points.
#pragma once

#include <cstdint>
#include <functional>
#include <string>
#include <vector>

#include "cosim_api.h"

namespace cosim {

//! a memory-bridge fault on the byte at record-area offset `off`
//! mode 0: accepted, completes WITH ERROR, the byte is not written
//! mode 1: accepted, then PERMANENT SILENCE (no done); the byte is written
//! mode 2: readiness WITHHELD before acceptance, for as long as it is armed
//! mode 3: accepted, completes WITHOUT error but only `delay` cycles later
//! kind 0: any byte, 1: only an erase byte (0xFF), 2: only a data byte
//! count: how many times it fires (-1: until cleared)
struct Fault {
  uint32_t off;
  int mode;
  int kind;
  int count;
  int delay = 0;
};
extern std::vector<Fault> faults;

//! a device-face operation the BFM performs, when the port is idle
struct BfmOp {
  unsigned op;                 //! 1 WRITE, 2 ERASE
  unsigned rid;
  std::vector<uint8_t> data;   //! WRITE bytes
  uint16_t offset = 0;
  uint16_t len = 0;            //! WRITE: bytes; ERASE: 0 = the whole record
  int stop_after = -1;         //! abandon the stream after this many bytes
  int pace = 0;                //! idle cycles between two WRITE bytes
};

struct Binding {
  unsigned sink = 0;
  unsigned bound = 1, started = 1, sw = 0;
  unsigned uid = 1;
  uint64_t teid = 0, ceid = 0;
};

struct Preload {
  unsigned sink;
  uint64_t teid;
  unsigned uid;
  uint64_t ceid;
  unsigned sw, started;
};

struct OpRec {
  bool bfm;
  unsigned op, rid;
  uint64_t req, gnt, end;
  std::string res;
  unsigned bytes;
};

struct StrobeRec {
  uint64_t cyc;
  uint32_t value;
  bool stray;
};

struct HookRec {
  std::string name;
  unsigned n;
  uint64_t cyc;
  uint32_t value;
};

struct Log {
  std::vector<OpRec> ops;
  std::vector<StrobeRec> strobes;
  std::vector<HookRec> hooks;
  unsigned mem_accepts = 0, mem_errs = 0, silent = 0, slow = 0;
  std::vector<uint64_t> loss_cycles;
  uint64_t bad101 = 0;
};
extern Log evlog;

struct Levels {
  unsigned backed, dirty_pub, stale, verdict, img_valid, pend, unres;
  unsigned restore_busy, restore_done, restore_fail, blank, alarm;
  unsigned mgr_dirty, port_busy, dev_busy, dyn_dirty, dyn_fmt0_v;
  uint64_t dyn_fmt0;
};

extern uint64_t cyc;
extern std::vector<Preload> preloads;

[[noreturn]] void fatal(const char *why);
void init(unsigned d1_en);
void finish();
void edge();
void run_cycles(uint64_t n);
void stall_ms(uint64_t ms);
bool run_until(const std::function<bool()> &pred, uint64_t max_cycles);
void at(const std::string &name, unsigned n, std::function<void()> fn);
unsigned hooks(const std::string &name);
bool all_fired();
void bind(const Binding &b);
void dyn_write(unsigned sel, unsigned idx, uint64_t val);
void bfm(const BfmOp &op);
void bfm_resume();
bool bfm_idle();
bool bfm_write_done_now();
bool bfm_req_pending();
void stray(unsigned word, uint32_t value);
uint32_t csr_peek(unsigned word);
void reset_rtl();
Levels levels();
uint8_t *area();

}  // namespace cosim

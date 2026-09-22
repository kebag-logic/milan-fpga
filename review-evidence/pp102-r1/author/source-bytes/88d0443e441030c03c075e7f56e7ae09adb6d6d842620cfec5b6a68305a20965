// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_nvm_port suite — independent device model + manager BFM, never DUT
// logic.
//
// The harness plays BOTH neighbors of the class-F port (02 §8 / F02.8):
// a manager BFM that frames records per 07 §5.2 (magic 0x1722, layout
// version, record_id, payload_length, crc16 — 16-bit fields big-endian on
// the byte stream) and streams them with configurable stalls, and an
// independent region-port device model (req/gnt, op READ/WRITE/ERASE,
// region + offset + len, byte phases with stalls, busy/done/err, error
// injection at any op or data byte). It checks byte-exact delivery both
// directions, the ERASE-then-WRITE commit shape, busy/done/err sequencing
// (busy low at the pulse, pulses exactly once), back-to-back ops, req-
// while-busy refusal, header refusals (bad magic / oversize length) with
// zero device traffic, mid-op device errors surfacing exactly once, and --
// the three things a well-behaved backend cannot show -- a `done` pulsed for
// no command at all, which the port must not mistake for the completion of
// the next one it issues, and the two completions it MUST take: one riding
// its own grant, one riding a command's final byte.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <vector>
#include "VKL_pp_nvm_port.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// device-face op codes — mirror of the contract, independent of the RTL.
// Plain integers on purpose: they are compared against `DevOp::op`, which the
// harness fills from `dut->dev_op_o`, so an enum class would need a cast at
// every use and ES.49 would be the worse for it.
constexpr int OP_READ  = 0;
constexpr int OP_WRITE = 1;
constexpr int OP_ERASE = 2;

constexpr int N_REGIONS = 8;    // test ids stay 0..7
constexpr int REG_BYTES = 2048;
constexpr int MAXP      = 1024; // pinned by -GMAX_PAYLOAD_P in the Makefile

constexpr int  kResetTicks      = 4;      // clocks held in reset before rst_n
constexpr long kOpTimeoutCycles = 100000; // run_op guard: no done/err by then
constexpr int  kDrainCycles     = 30;     // ticked past a pulse to catch a second

// CRC-16/CCITT-FALSE — the manager's in-band integrity field; the DUT must
// carry it opaquely (07 §5.3 puts computation/validation in the manager).
static uint16_t crc16(const std::vector<uint8_t>& b) {
  uint16_t c = 0xFFFF;
  for (uint8_t x : b) {
    c ^= uint16_t(uint16_t(x) << 8);
    for (int i = 0; i < 8; ++i)
      c = (c & 0x8000) ? uint16_t(uint16_t(c << 1) ^ 0x1021)
                       : uint16_t(c << 1);
  }
  return c;
}

// frame a record per 07 §5.2 (big-endian 16-bit fields on the byte stream)
static std::vector<uint8_t> frame(uint8_t rec, const std::vector<uint8_t>& pl,
                                  uint16_t magic = 0x1722, int force_plen = -1) {
  uint16_t plen = (force_plen >= 0) ? uint16_t(force_plen)
                                    : uint16_t(pl.size());
  std::vector<uint8_t> f;
  f.push_back(uint8_t(magic >> 8));
  f.push_back(uint8_t(magic & 0xFF));
  f.push_back(0x01);                       // layout_version
  f.push_back(rec);
  f.push_back(uint8_t(plen >> 8));
  f.push_back(uint8_t(plen & 0xFF));
  std::vector<uint8_t> cb(f);              // crc over header-sans-crc + payload
  cb.insert(cb.end(), pl.begin(), pl.end());
  uint16_t c = crc16(cb);
  f.push_back(uint8_t(c >> 8));
  f.push_back(uint8_t(c & 0xFF));
  f.insert(f.end(), pl.begin(), pl.end());
  return f;
}

static std::vector<uint8_t> pattern(size_t n, uint8_t seed) {
  std::vector<uint8_t> p(n);
  for (size_t i = 0; i < n; ++i) p[i] = uint8_t(seed + 7 * i);
  return p;
}

struct DevOp {
  int op;
  int region;
  int offset;
  int len;
};

struct Harness {
  VKL_pp_nvm_port* dut;

  // ---- independent device model (region port backend) ----
  uint8_t store[N_REGIONS][REG_BYTES];
  std::vector<DevOp> ops;                 // every accepted device command
  int erase_count[N_REGIONS] = {0};
  int gnt_delay = 1;                      // req->gnt cycles
  int op_delay = 4;                       // data-end->done cycles
  int wstall = 0;                         // device-side inter-byte stalls
  int rstall = 0;
  int err_at_op = -1;                     // op index since arm to fail
  int err_after_bytes = -1;               // fail after N data bytes (-1: at once)
  int ops_since_arm = 0;
  bool fail_cur = false;

  // ---- unsolicited completion (issue #14) ----
  // A `done` that belongs to NO command. The model above only ever completes
  // a command it accepted, so the port's tolerance of a backend that does
  // otherwise was unobservable: "sticky per command" and "sticky globally"
  // look identical to a well-behaved peer. A real backend produces one --
  // the cycle it was aborted from finishes late, after the port has already
  // reported `err` and the manager has re-issued.
  //
  // Armed by a phase and fired ONCE, in a window named by what the BUS shows
  // rather than by DUT state: how many commands the backend has accepted, and
  // whether a request is up that it has not granted.
  int  unsol_after_ops = -1;              // fire at this accepted-command count
  bool unsol_in_req = false;              // ...with a request up, else with none
  int  unsol_dones = 0;                   // unsolicited completions emitted
  int  unsol_ops = -1;                    // commands accepted when it fired
  int  unsol_mgr = -1;                    // manager-face bytes moved when it fired
  bool unsol_req = false;                 // a request was up when it fired

  // ---- completion riding the grant ----
  // The other edge of the same window, and a PERMITTED coincidence rather than
  // a broken peer: the port's own header says backends without erase semantics
  // answer ERASE with done at once, and at once can mean the grant cycle. The
  // port owns the command from the handshake, so it must take that `done`.
  bool gnt_done_on_erase = false;         // arm the backend to answer that way
  bool gnt_done_now = false;              // this grant carries the completion
  int  gnt_done_pairs = 0;                // grant+done cycles presented

  // ---- completion riding a pump's final byte ----
  // The coincidence the sticky `done_seen_r` exists for, and the one the eight
  // state terms of `dev_cmd_owned_w` carry: the backend raises `done` on the
  // same edge that moves the command's last byte, while the port is still in
  // the pump or collect state. It is armed rather than always on, because it
  // is a contract freedom a backend may or may not take; `measure_figures.py`
  // turns it on for the whole run as the coincident-completion model.
  bool done_on_last_byte = false;         // arm: the backend answers on that edge
  bool coinc_now = false;                 // this tick's final byte carries it
  int  coinc_dones = 0;                   // final-byte completions presented

  // ---- what the port owes whichever neighbour it is talking to ----
  // Read off the BUS against the model's own record of a command it accepted
  // and has not yet completed, so none depends on what the array retains.
  // A completion the port did not own, once consumed, shows up as one of
  // three: the next command requested into a device still working, the manager
  // answered before the device answered the port, or a header the port
  // buffered handed up before the read that filled it had completed. The third
  // is the one a stray `done` taken by `S_RHWAIT` reaches FIRST -- the payload
  // request and the manager's pulse come a whole header forward later, so on a
  // backend whose completion delay is shorter than that forward the first two
  // are back to zero by the time they are read, and only this one still says
  // the read was closed early.
  int req_while_owed = 0;                 // cycles a new command was requested
  int pulse_while_owed = 0;               // cycles the manager was answered
  int fwd_while_owed = 0;                 // cycles a BUFFERED restore byte moved

  int  d_st = 0;                          // 0 idle, 1 data, 2 completion timer
  int  d_reqwait = 0;
  bool d_gnt = false;
  bool d_done = false;
  bool d_err = false;
  bool d_busy = false;
  DevOp d_cur{0, 0, 0, 0};
  int  d_bytes = 0;
  int  d_stall = 0;
  bool d_rhold = false;
  int  done_ctr = 0;
  int  err_ctr = 0;

  // ---- manager BFM ----
  int m_mode = 0;                         // 0 idle, 1 commit stream, 2 restore
  std::vector<uint8_t> m_wbytes;
  size_t m_widx = 0;
  int m_stall = 0;
  int mgr_wstall = 0;
  int mgr_rstall = 0;

  // per-op capture
  int done_pulses = 0;
  int err_pulses = 0;
  int dev_errs = 0;      // device-raised errors, not port refusals
  int dev_rd = 0;        // bytes the DEVICE delivered on the read bus
  bool busy_seen = false;                 // busy must be LOW at done/err (F02.8)
  bool busy_ok = true;
  std::vector<uint8_t> rbytes;
  // What the port SENT on the device write bus, captured at the handshake.
  // Distinct from `store` on purpose: after a device error, what the array
  // retained is the device model's choice (this model keeps every accepted
  // byte; a page-buffered NOR keeps none until the program cycle ends), while
  // what the port put on the bus is the port's own behaviour under any model.
  std::vector<uint8_t> sent;
  long cycles = 0;

  explicit Harness(VKL_pp_nvm_port* d) : dut(d) {
    memset(store, 0xEE, sizeof store);
  }

  void arm_err(int at_op, int after_bytes) {
    err_at_op = at_op; err_after_bytes = after_bytes; ops_since_arm = 0;
  }
  void disarm_err() { err_at_op = -1; err_after_bytes = -1; }

  //! Emit one `done` for no command, once, when `after_ops` commands have been
  //! accepted and a request is (`in_req`) or is not up. It disarms itself, so
  //! an arming that never found its window shows up as `unsol_dones == 0`
  //! rather than as a pulse somewhere later.
  void arm_unsolicited_done(int after_ops, bool in_req) {
    unsol_after_ops = after_ops; unsol_in_req = in_req;
  }

  //! The data phase just moved its final byte. Either the completion rode that
  //! byte -- `present_coincident_completion` has already put it on the pins for
  //! this very cycle, so the command is over -- or it is `op_delay` away.
  void finish_data_phase() {
    if (coinc_now) { d_busy = false; d_st = 0; }
    else { done_ctr = op_delay; d_st = 2; }
  }

  //! Raise `dev_done_i` on the same edge that moves the command's last byte.
  //!
  //! This cannot be done through the model's own `d_done`: that is driven at
  //! the top of the tick, so it presents a cycle late, by which time the port
  //! is in a WAIT state reading `dev_done_i` directly and the sticky latch is
  //! bypassed. Tuning `op_delay` cannot reach it either -- the delay is counted
  //! in ticks and this coincidence lives inside one. Writing the pin here,
  //! after the cycle's first `eval()` has settled the DUT's outputs so the
  //! final-byte handshake is visible, and re-evaluating before the posedge, is
  //! what lands the pulse on the right edge.
  //!
  //! The armed-error guard is load-bearing: without it the backend pulses
  //! `done` on the byte an armed error is about to land on, and T17/T18 stop
  //! testing what they name.
  void present_coincident_completion() {
    coinc_now = false;
    if (!done_on_last_byte || d_st != 1) return;
    if (fail_cur && err_after_bytes >= 0 && d_bytes + 1 == err_after_bytes) return;
    const bool last_write = (d_cur.op == OP_WRITE && d_bytes + 1 == d_cur.len
                             && dut->dev_wready_i && dut->dev_wvalid_o);
    const bool last_read = (d_cur.op == OP_READ && d_bytes + 1 == d_cur.len
                            && dut->dev_rvalid_i && dut->dev_rready_o);
    if (!(last_write || last_read)) return;
    dut->dev_done_i = 1;
    dut->dev_busy_i = 0;
    coinc_now = true;
    ++coinc_dones;
    dut->eval();
  }

  void drive_dev() {
    dut->dev_gnt_i  = d_gnt;
    dut->dev_done_i = d_done;
    dut->dev_err_i  = d_err;
    dut->dev_busy_i = d_busy;
    bool wr = (d_st == 1 && d_cur.op == OP_WRITE && d_stall == 0);
    dut->dev_wready_i = wr;
    bool rv = (d_st == 1 && d_cur.op == OP_READ && d_bytes < d_cur.len
               && (d_stall == 0 || d_rhold));
    dut->dev_rvalid_i = rv;
    dut->dev_rdata_i  = rv
        ? store[d_cur.region % N_REGIONS][(d_cur.offset + d_bytes) % REG_BYTES]
        : 0;
  }

  void sample_dev() {
    bool drove_gnt = d_gnt;
    bool drove_done = d_done;
    bool drove_err = d_err;

    // The port carries ONE device command at a time (F02.8 on the manager
    // face, the region port's own req/gnt here), and it cannot know an op
    // ended before the backend says so. `d_busy` is the model's record of a
    // command it accepted and has not yet completed; nothing below reads the
    // array, so both counters hold under every device model.
    if (d_busy && dut->dev_req_o) ++req_while_owed;
    if (d_busy && (dut->nvm_done_o || dut->nvm_err_o)) ++pulse_while_owed;
    // A restore byte with no device byte behind it on the same cycle is one
    // the port buffered earlier, which it may only hand up once the read that
    // filled the buffer has completed. Bus-side like the other two.
    if (d_busy && dut->nvm_rvalid_o && dut->nvm_rready_i && !dut->dev_rvalid_i)
      ++fwd_while_owed;

    // command accept
    if (drove_gnt && dut->dev_req_o) {
      const bool done_rode_the_grant = gnt_done_now;
      gnt_done_now = false;
      d_cur = {int(dut->dev_op_o), int(dut->dev_region_o),
               int(dut->dev_offset_o), int(dut->dev_len_o)};
      ops.push_back(d_cur);
      d_busy = true; d_bytes = 0; d_stall = 0; d_rhold = false;
      fail_cur = (err_at_op >= 0 && ops_since_arm == err_at_op);
      ++ops_since_arm;
      if (fail_cur && err_after_bytes < 0) {
        err_ctr = op_delay; d_st = 2;
      } else if (d_cur.op == OP_ERASE) {
        int r = d_cur.region % N_REGIONS;
        memset(store[r], 0xFF, REG_BYTES);
        ++erase_count[r];
        if (done_rode_the_grant) { d_busy = false; d_st = 0; }
        else { done_ctr = op_delay; d_st = 2; }
      } else if (d_cur.len == 0) {
        done_ctr = op_delay; d_st = 2;
      } else {
        d_st = 1;
      }
    }

    // write byte accept
    if (d_st == 1 && d_cur.op == OP_WRITE) {
      if (dut->dev_wready_i && dut->dev_wvalid_o) {
        sent.push_back(dut->dev_wdata_o);
        store[d_cur.region % N_REGIONS][(d_cur.offset + d_bytes) % REG_BYTES] =
            dut->dev_wdata_o;
        ++d_bytes;
        d_stall = wstall;
        if (fail_cur && d_bytes == err_after_bytes) { err_ctr = 2; d_st = 2; }
        else if (d_bytes == d_cur.len) { finish_data_phase(); }
      } else if (d_stall > 0) --d_stall;
    }

    // read byte delivery
    if (d_st == 1 && d_cur.op == OP_READ) {
      if (dut->dev_rvalid_i) {
        if (dut->dev_rready_o) {
          ++d_bytes; ++dev_rd; d_rhold = false; d_stall = rstall;
          if (fail_cur && d_bytes == err_after_bytes) { err_ctr = 2; d_st = 2; }
          else if (d_bytes == d_cur.len) { finish_data_phase(); }
        } else {
          d_rhold = true;               // hold the byte until accepted
        }
      } else if (d_stall > 0) --d_stall;
    }

    // one-cycle pulses
    if (drove_gnt)  d_gnt  = false;
    if (drove_done) d_done = false;
    if (drove_err)  d_err  = false;

    // grant scheduling
    if (d_st == 0 && !d_busy && dut->dev_req_o && !drove_gnt) {
      if (++d_reqwait >= gnt_delay) {
        d_gnt = true; d_reqwait = 0;
        // ...and, for a backend with no erase semantics, the completion with
        // it. `dev_op_o` is already valid: the port drives the command with
        // the request it is still holding.
        if (gnt_done_on_erase && int(dut->dev_op_o) == OP_ERASE) {
          d_done = true; gnt_done_now = true; ++gnt_done_pairs;
        }
      }
    }

    maybe_fire_unsolicited_done(drove_gnt, drove_done, drove_err);

    // completion timers
    if (d_st == 2) {
      if (done_ctr > 0 && --done_ctr == 0) { d_done = true; d_busy = false; d_st = 0; }
      if (err_ctr  > 0 && --err_ctr  == 0) { d_err  = true; d_busy = false; d_st = 0;
                                             ++dev_errs; }
    }
  }

  //! The unsolicited completion, fired in a cycle where this backend owns
  //! nothing: idle, no grant presented or scheduled, and no real pulse beside
  //! it -- so what reaches the port is unambiguously a `done` for a command
  //! that does not exist, rather than an early or doubled one for a command
  //! that does. Its own function because `sample_dev` is the whole backend and
  //! this is one armed behaviour inside it.
  void maybe_fire_unsolicited_done(bool drove_gnt, bool drove_done, bool drove_err) {
    const int mgr_moved = (m_mode == 1) ? int(m_widx) : int(rbytes.size());
    if (unsol_after_ops >= 0 && d_st == 0 && !d_busy
        && !d_gnt && !drove_gnt && !d_done && !drove_done
        && !d_err && !drove_err
        && int(ops.size()) == unsol_after_ops
        && bool(dut->dev_req_o) == unsol_in_req
        // With no request up, the window is a manager-face phase -- collecting
        // a header or forwarding one -- so require that this op has actually
        // moved a byte. "Busy with nothing requested" is ALSO what a wedged
        // port looks like, and firing there would rescue it: a stray `done` is
        // exactly the pulse a stuck wait state is waiting for. Measured: with
        // `S_WWAIT`'s error arm swallowed (M5) the port hangs, and without
        // this term T19a un-hung it and turned the end-of-run idle check green.
        && (unsol_in_req || (dut->nvm_busy_o && mgr_moved > 0))) {
      d_done = true;                      // presented on the next tick, 1 cycle
      ++unsol_dones;
      unsol_ops = int(ops.size());
      unsol_mgr = mgr_moved;
      unsol_req = bool(dut->dev_req_o);
      unsol_after_ops = -1;               // once per arming
    }
  }

  void tick() {
    // manager drive
    if (m_mode == 1) {
      bool v = (m_widx < m_wbytes.size() && m_stall == 0);
      dut->nvm_wvalid_i = v;
      dut->nvm_wdata_i  = v ? m_wbytes[m_widx] : 0;
      dut->nvm_rready_i = 0;
    } else if (m_mode == 2) {
      dut->nvm_wvalid_i = 0;
      dut->nvm_rready_i = (m_stall == 0);
    } else {
      dut->nvm_wvalid_i = 0;
      dut->nvm_rready_i = 0;
    }
    drive_dev();

    dut->clk_i = 0; dut->eval();
    present_coincident_completion();

    // pre-edge sampling: what the registers (and both neighbors) see
    if (dut->nvm_done_o) ++done_pulses;
    if (dut->nvm_err_o)  ++err_pulses;
    if (dut->nvm_busy_o) busy_seen = true;
    if ((dut->nvm_done_o || dut->nvm_err_o) && dut->nvm_busy_o) busy_ok = false;
    if (m_mode == 1) {
      if (dut->nvm_wvalid_i && dut->nvm_wready_o) { ++m_widx; m_stall = mgr_wstall; }
      else if (m_stall > 0) --m_stall;
    } else if (m_mode == 2) {
      if (dut->nvm_rvalid_o && dut->nvm_rready_i) {
        rbytes.push_back(dut->nvm_rdata_o);
        m_stall = mgr_rstall;
      } else if (m_stall > 0) --m_stall;
    }
    sample_dev();

    dut->clk_i = 1; dut->eval();
    ++cycles;
  }

  void clear_capture() {
    done_pulses = err_pulses = 0;
    dev_errs = 0;
    dev_rd = 0;
    busy_seen = false; busy_ok = true;
    rbytes.clear();
    sent.clear();
    // captures, not the arming: a phase arms before it starts the op, and
    // `commit`/`restore` clear here on the way in.
    unsol_dones = 0; unsol_ops = -1; unsol_mgr = -1; unsol_req = false;
    req_while_owed = 0; pulse_while_owed = 0; fwd_while_owed = 0;
    gnt_done_pairs = 0; coinc_dones = 0;
  }

  void start(bool we, uint8_t rec) {
    dut->nvm_req_i = 1;
    dut->nvm_we_i  = we;
    dut->nvm_record_id_i = rec;
    tick();
    dut->nvm_req_i = 0;
  }

  // run until done/err (+ drain to catch double pulses); 0 done, 1 err, -1 t/o
  int run_op(long max_cycles = kOpTimeoutCycles, int drain = kDrainCycles) {
    for (long i = 0; i < max_cycles; ++i) {
      tick();
      if (done_pulses + err_pulses > 0) {
        for (int d = 0; d < drain; ++d) tick();
        m_mode = 0;
        return err_pulses ? 1 : 0;
      }
    }
    m_mode = 0;
    return -1;
  }

  int commit(uint8_t rec, const std::vector<uint8_t>& f,
             int drain = kDrainCycles) {
    clear_capture();
    m_mode = 1; m_wbytes = f; m_widx = 0; m_stall = 0;
    start(true, rec);
    return run_op(kOpTimeoutCycles, drain);
  }

  int restore(uint8_t rec, int drain = kDrainCycles) {
    clear_capture();
    m_mode = 2; m_stall = 0;
    start(false, rec);
    return run_op(kOpTimeoutCycles, drain);
  }

  bool store_match(int region, const std::vector<uint8_t>& f) {
    for (size_t i = 0; i < f.size(); ++i)
      if (store[region][i] != f[i]) return false;
    return true;
  }
};

static bool op_is(const DevOp& o, int op, int region, int offset, int len) {
  return o.op == op && o.region == region && o.offset == offset && o.len == len;
}

// ---- the suite ----------------------------------------------------------
// One object owns the model, both neighbour BFMs and the tally, so every
// phase below is a named member function rather than another stretch of a
// `main` nobody can scope (Core Guidelines I.2, F.3).
namespace {
class NvmPortSuite {
 public:
  int run();

 private:
  void reset_leaves_the_port_idle();
  void commit_erases_then_writes_byte_exact();
  void restore_reads_header_then_payload_byte_exact();
  void zero_payload_record_round_trips();
  void stalls_on_every_byte_interface_are_survived();
  void back_to_back_ops_all_complete();
  void request_while_busy_is_ignored();
  void erase_error_stops_the_commit_then_recovers();
  void write_header_phase_error_surfaces_once();
  void read_payload_phase_error_surfaces_once();
  void bad_magic_commit_is_refused_before_the_device();
  void oversize_payload_length_is_refused();
  void bad_stored_magic_is_refused_on_restore();
  void oversize_stored_length_is_refused_on_restore();
  void refusals_leave_the_port_serviceable();
  void torn_commit_never_restores_as_valid();
  void torn_commit_leaves_every_other_region_untouched();
  void late_write_failure_reports_err_not_done();
  void read_completion_window_errors_report_err();
  void unsolicited_completion_during_a_commit();
  void unsolicited_completion_during_a_restore();
  void completion_riding_the_grant_is_taken();
  void completion_riding_the_last_byte_is_taken();
  void the_port_is_idle_at_the_end_of_the_run();

  const milan::tb::Model<VKL_pp_nvm_port> model;
  VKL_pp_nvm_port* const dut = model.get();
  Harness h{dut};
  int checks = 0;
  int fails = 0;
  std::vector<uint8_t> f2;   // T2's record: re-read by T9, T14 and T18
  std::vector<uint8_t> f7;   // T7's record: the WRITE T8 cuts short
};
}  // namespace

// ---- reset --------------------------------------------------------------
void NvmPortSuite::reset_leaves_the_port_idle() {
  dut->rst_n = 0;
  dut->nvm_req_i = 0; dut->nvm_we_i = 0; dut->nvm_record_id_i = 0;
  dut->nvm_wvalid_i = 0; dut->nvm_wdata_i = 0; dut->nvm_rready_i = 0;
  dut->dev_gnt_i = 0; dut->dev_wready_i = 0; dut->dev_rvalid_i = 0;
  dut->dev_rdata_i = 0; dut->dev_busy_i = 0; dut->dev_done_i = 0;
  dut->dev_err_i = 0;
  for (int i = 0; i < kResetTicks; ++i) h.tick();
  dut->rst_n = 1;
  h.tick();
  CHECK(!dut->nvm_busy_o && !dut->nvm_done_o && !dut->nvm_err_o,
        "idle after reset");
  CHECK(!dut->dev_req_o && !dut->dev_wvalid_o && !dut->nvm_rvalid_o,
        "no spontaneous device/read activity after reset");
}

// ---- T1: commit envelope — ERASE then WRITE, byte-exact ----------------
void NvmPortSuite::commit_erases_then_writes_byte_exact() {
  auto f1 = frame(3, pattern(24, 0x30));
  int rc = h.commit(3, f1);
  CHECK(rc == 0, "T1 commit completes with done, rc=%d", rc);
  CHECK(h.done_pulses == 1 && h.err_pulses == 0,
        "T1 exactly one done, no err (got %d/%d)", h.done_pulses, h.err_pulses);
  CHECK(h.busy_seen && h.busy_ok, "T1 busy high mid-op, low at the pulse");
  CHECK(h.ops.size() == 2, "T1 two device ops, got %zu", h.ops.size());
  CHECK(h.ops.size() >= 1 && op_is(h.ops[0], OP_ERASE, 3, 0, 0),
        "T1 op0 = ERASE region 3 len 0 (got op %d reg %d off %d len %d)",
        h.ops[0].op, h.ops[0].region, h.ops[0].offset, h.ops[0].len);
  CHECK(h.ops.size() >= 2 && op_is(h.ops[1], OP_WRITE, 3, 0, 32),
        "T1 op1 = WRITE region 3 off 0 len 32");
  CHECK(h.erase_count[3] == 1, "T1 erase pulsed region 3 once");
  CHECK(h.store_match(3, f1), "T1 device store byte-exact (header+crc+payload)");
  CHECK(h.store[3][f1.size()] == 0xFF, "T1 erase visible past the record");
}

// ---- T2: restore envelope — header read then payload read, byte-exact --
void NvmPortSuite::restore_reads_header_then_payload_byte_exact() {
  f2 = frame(5, pattern(40, 0xA0));
  memcpy(h.store[5], f2.data(), f2.size());
  h.ops.clear();
  int rc = h.restore(5);
  CHECK(rc == 0, "T2 restore completes with done, rc=%d", rc);
  CHECK(h.done_pulses == 1 && h.err_pulses == 0, "T2 exactly one done");
  CHECK(h.rbytes == f2, "T2 restored stream byte-exact (%zu bytes)",
        h.rbytes.size());
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_READ, 5, 0, 8)
            && op_is(h.ops[1], OP_READ, 5, 8, 40),
        "T2 device ops = READ hdr(8) then READ payload(40)");
  CHECK(h.erase_count[5] == 0, "T2 restore never erases");
}

// ---- T3: zero-payload record both directions ---------------------------
void NvmPortSuite::zero_payload_record_round_trips() {
  auto f3 = frame(6, {});
  h.ops.clear();
  int rc = h.commit(6, f3);
  CHECK(rc == 0 && h.done_pulses == 1, "T3 zero-payload commit done");
  CHECK(h.ops.size() == 2 && op_is(h.ops[1], OP_WRITE, 6, 0, 8),
        "T3 WRITE len 8 (header only)");
  CHECK(h.store_match(6, f3), "T3 store byte-exact");
  h.ops.clear();
  rc = h.restore(6);
  CHECK(rc == 0 && h.rbytes == f3, "T3 zero-payload restore byte-exact");
  CHECK(h.ops.size() == 1 && op_is(h.ops[0], OP_READ, 6, 0, 8),
        "T3 restore issues only the header READ");
}

// ---- T4: stall torture on all four byte interfaces ---------------------
void NvmPortSuite::stalls_on_every_byte_interface_are_survived() {
  h.mgr_wstall = 3; h.mgr_rstall = 2; h.wstall = 2; h.rstall = 3;
  h.gnt_delay = 5; h.op_delay = 9;
  auto f4 = frame(2, pattern(65, 0x11));
  int rc = h.commit(2, f4);
  CHECK(rc == 0 && h.done_pulses == 1, "T4 commit done under stalls");
  CHECK(h.store_match(2, f4), "T4 store byte-exact under stalls");
  rc = h.restore(2);
  CHECK(rc == 0 && h.done_pulses == 1, "T4 restore done under stalls");
  CHECK(h.rbytes == f4, "T4 restored stream byte-exact under stalls");
  h.mgr_wstall = 0; h.mgr_rstall = 0; h.wstall = 0; h.rstall = 0;
  h.gnt_delay = 1; h.op_delay = 4;
}

// ---- T5: back-to-back ops (req immediately after each pulse) -----------
void NvmPortSuite::back_to_back_ops_all_complete() {
  auto f5a = frame(0, pattern(12, 0x50));
  auto f5b = frame(1, pattern(20, 0x60));
  h.ops.clear();
  int rca = h.commit(0, f5a, /*drain=*/0);
  int rcb = h.commit(1, f5b, /*drain=*/0);
  int rcc = h.restore(0, /*drain=*/0);
  CHECK(rca == 0 && rcb == 0 && rcc == 0, "T5 back-to-back ops all done");
  CHECK(h.ops.size() == 6, "T5 2+2+2 device ops, got %zu", h.ops.size());
  CHECK(h.store_match(0, f5a) && h.store_match(1, f5b),
        "T5 both commits byte-exact");
  CHECK(h.rbytes == f5a, "T5 immediate re-read byte-exact");
}

// ---- T6: req while busy is ignored (single outstanding, F02.8) ---------
void NvmPortSuite::request_while_busy_is_ignored() {
  h.gnt_delay = 8; h.op_delay = 30;
  auto f6 = frame(7, pattern(16, 0x70));
  h.ops.clear();
  h.clear_capture();
  h.m_mode = 1; h.m_wbytes = f6; h.m_widx = 0; h.m_stall = 0;
  h.start(true, 7);
  for (int i = 0; i < 40; ++i) h.tick();
  CHECK(dut->nvm_busy_o, "T6 op still in flight at the poke");
  dut->nvm_req_i = 1; dut->nvm_we_i = 0; dut->nvm_record_id_i = 5;
  for (int i = 0; i < 5; ++i) h.tick();
  dut->nvm_req_i = 0; dut->nvm_we_i = 0;
  int rc = h.run_op();
  CHECK(rc == 0 && h.done_pulses == 1, "T6 exactly one done for the one op");
  CHECK(h.ops.size() == 2, "T6 no extra device op from the spurious req");
  bool no_read = true;
  for (auto& o : h.ops) if (o.op == OP_READ) no_read = false;
  CHECK(no_read, "T6 the spurious restore never reached the device");
  CHECK(h.store_match(7, f6), "T6 original commit still byte-exact");
  h.gnt_delay = 1; h.op_delay = 4;
}

// ---- T7: device error during ERASE — err exactly once, no WRITE -------
void NvmPortSuite::erase_error_stops_the_commit_then_recovers() {
  f7 = frame(4, pattern(10, 0x90));
  h.arm_err(0, -1);
  h.ops.clear();
  int rc = h.commit(4, f7);
  CHECK(rc == 1, "T7 commit fails, rc=%d", rc);
  CHECK(h.err_pulses == 1 && h.done_pulses == 0,
        "T7 err exactly once, done never (got %d/%d)",
        h.err_pulses, h.done_pulses);
  CHECK(h.busy_ok, "T7 busy low at the err pulse");
  CHECK(h.ops.size() == 1 && h.ops[0].op == OP_ERASE,
        "T7 the WRITE was never issued after the erase error");
  h.disarm_err();
  rc = h.commit(4, f7);
  CHECK(rc == 0 && h.done_pulses == 1, "T7b port recovered: retry commits");
  CHECK(h.store_match(4, f7), "T7b retry byte-exact");
}

// ---- T8: device error during the WRITE's HEADER pump -------------------
// op 1 is the WRITE and it carries the framed record, so a cut after 5
// bytes is still inside the 8-byte header -- the record's payload has not
// started. T15 cuts the same op at 12 bytes for the data phase proper.
void NvmPortSuite::write_header_phase_error_surfaces_once() {
  h.arm_err(1, 5);
  h.ops.clear();
  int rc = h.commit(4, f7);
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T8 write-phase error surfaces exactly once");
  CHECK(h.ops.size() == 2, "T8 no device op after the failed WRITE");
  h.disarm_err();
}

// ---- T9: device error mid READ payload phase ---------------------------
void NvmPortSuite::read_payload_phase_error_surfaces_once() {
  h.arm_err(1, 7);
  h.ops.clear();
  int rc = h.restore(5);
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T9 read-phase error surfaces exactly once");
  CHECK(h.rbytes.size() < f2.size(), "T9 stream cut short (%zu of %zu)",
        h.rbytes.size(), f2.size());
  h.disarm_err();
}

// ---- T10: unframed commit stream refused (magic, 07 §5.2) --------------
void NvmPortSuite::bad_magic_commit_is_refused_before_the_device() {
  auto fbad = frame(3, pattern(8, 0x22), /*magic=*/0xDEAD);
  h.ops.clear();
  int rc = h.commit(3, fbad);
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T10 bad-magic commit refused with one err");
  CHECK(h.ops.empty(), "T10 refusal before any device traffic");
}

// ---- T11: oversize payload_length refused ------------------------------
void NvmPortSuite::oversize_payload_length_is_refused() {
  auto fbig = frame(3, pattern(4, 0x33), 0x1722, /*force_plen=*/MAXP + 1);
  h.ops.clear();
  int rc = h.commit(3, fbig);
  CHECK(rc == 1 && h.err_pulses == 1,
        "T11 oversize payload_length refused with one err");
  CHECK(h.ops.empty(), "T11 refusal before any device traffic");
}

// ---- T12: stored record with bad magic refused on restore --------------
void NvmPortSuite::bad_stored_magic_is_refused_on_restore() {
  uint8_t save0 = h.store[5][0];
  h.store[5][0] = 0x00;
  h.ops.clear();
  int rc = h.restore(5);
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T12 bad stored magic -> one err");
  CHECK(h.ops.size() == 1 && op_is(h.ops[0], OP_READ, 5, 0, 8),
        "T12 only the header probe was issued");
  CHECK(h.rbytes.empty(), "T12 nothing forwarded to the manager");
  h.store[5][0] = save0;
}

// ---- T13: stored record with oversize length refused on restore --------
void NvmPortSuite::oversize_stored_length_is_refused_on_restore() {
  uint8_t save4 = h.store[5][4];
  uint8_t save5 = h.store[5][5];
  h.store[5][4] = 0xFF; h.store[5][5] = 0xFF;
  h.ops.clear();
  int rc = h.restore(5);
  CHECK(rc == 1 && h.err_pulses == 1, "T13 oversize stored length -> one err");
  CHECK(h.ops.size() == 1 && h.rbytes.empty(),
        "T13 header probe only, nothing forwarded");
  h.store[5][4] = save4; h.store[5][5] = save5;
}

// ---- T14: refusals leave the port serviceable --------------------------
void NvmPortSuite::refusals_leave_the_port_serviceable() {
  int rc = h.restore(5);
  CHECK(rc == 0 && h.rbytes == f2, "T14 clean restore after refusals");
  h.tick();
  CHECK(!dut->nvm_busy_o && !dut->nvm_done_o && !dut->nvm_err_o,
        "idle after the refusal phases");
}

// ---- T15: POWER CUT mid-commit (issue #70) -----------------------------
// A commit is ERASE(region) then WRITE(0, 8+plen). Cut the power inside the
// WRITE and the region is left erased-plus-partial: the record being written
// is gone AND so is whatever it replaced. That is a property of writing a
// slot in place, and it is the reason the flash map reserves A/B slots --
// so this phase pins what the port DOES guarantee rather than asserting a
// survival the single-slot layout cannot give.
//
// The guarantee that matters for #70 is the one on the next phase: a torn
// commit of ONE record must not disturb ANOTHER. Here we pin that the torn
// image never restores as a VALID record -- "never a half-record that
// restores as garbage" -- graded with the suite's own CRC, because the port
// carries the CRC opaquely and only the manager can reject on it.
void NvmPortSuite::torn_commit_never_restores_as_valid() {
  std::vector<uint8_t> whole = frame(7, pattern(24, 0x40));
  h.ops.clear();
  int rc = h.commit(7, whole);
  CHECK(rc == 0 && h.store_match(7, whole), "T15 seed record committed");

  std::vector<uint8_t> replacement = frame(7, pattern(24, 0x90));
  h.ops.clear();
  h.arm_err(1, 12);                 // op 0 = ERASE, op 1 = WRITE: cut at 12 B
  rc = h.commit(7, replacement);
  h.disarm_err();
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T15 torn commit reports err, never done");
  // busy_seen is added because busy_ok alone starts true and only clears
  // when a pulse coincides with busy high, so it passes for a port that
  // never pulsed. It does NOT catch a wedge: a wedged port holds busy high,
  // so busy_seen is true and no pulse ever contradicts busy_ok. The wedge is
  // caught by the rc check above; this pair only pins the pulse's timing.
  CHECK(h.busy_seen && h.busy_ok, "T15 busy raised then low at the err pulse");

  // The cut must be REAL, stated on the bus. Reading the array here was a
  // member of the same family as T16 and T17: under a backend that answers
  // ERASE with `done` without rewriting the array -- which the port's own
  // header names, and which 02 SS8 lists as the host-filesystem backing --
  // the old record survives the tear intact, and an array-negative check
  // reddens for a device doing the right thing.
  CHECK(h.ops.size() == 2
            && op_is(h.ops[1], OP_WRITE, 7, 0,
                     static_cast<int>(replacement.size()))
            && h.sent.size() == 12
            && std::equal(h.sent.begin(), h.sent.end(), replacement.begin()),
        "T15 the cut was real: ERASE then a WRITE stopped 12 bytes in");

  // ...and it must not read back as a valid record. Either the port refuses
  // it at the header, or the bytes it forwards fail the manager's CRC.
  h.ops.clear();
  rc = h.restore(7);
  bool refused = (rc == 1 && h.rbytes.empty());
  bool crc_rejects = false;
  if (!refused && h.rbytes.size() >= 8) {
    std::vector<uint8_t> cb(h.rbytes.begin(), h.rbytes.begin() + 6);
    cb.insert(cb.end(), h.rbytes.begin() + 8, h.rbytes.end());
    uint16_t stored = uint16_t(uint16_t(h.rbytes[6] << 8) | h.rbytes[7]);
    crc_rejects = (crc16(cb) != stored);
  }
  // Conditioned, not asserted: if the backend left the OLD record intact the
  // torn commit lost nothing, which is the outcome #70 wants, not a defect.
  bool old_intact = std::equal(whole.begin(), whole.end(), h.store[7]);
  CHECK(old_intact || refused || crc_rejects,
        "T15 unless the old record survived, a torn image never restores as valid");
  // ...and pin WHICH branch fired, so a regression toward refusing every
  // restore cannot satisfy the disjunction above in silence. Which branch
  // legitimately DIFFERS by device: this model keeps the bytes it accepted
  // so the header survives and only the CRC rejects, while a page-buffered
  // NOR discards them and the port rightly refuses at the header. So do not
  // pin a branch -- pin that the branch the port took AGREES with what the
  // array actually holds. That is the port's own behaviour under any model.
  bool hdr_intact = (h.store[7][0] == 0x17 && h.store[7][1] == 0x22
                     && ((h.store[7][4] << 8) | h.store[7][5]) <= MAXP);
  bool asked_payload = (h.ops.size() == 2 && h.ops[1].op == OP_READ
                        && h.ops[1].region == 7 && h.ops[1].offset == 8);
  CHECK(hdr_intact ? asked_payload : !asked_payload,
        "T15 the port forwarded or refused according to the stored header");

  // the port survives the cut: a clean re-commit is byte-exact again
  h.ops.clear();
  rc = h.commit(7, replacement);
  CHECK(rc == 0 && h.store_match(7, replacement),
        "T15 serviceable after the cut: clean re-commit is byte-exact");
}

// ---- T16: a torn commit must not disturb the REST of the saved set -----
// This is the #70 property proper. Records live in their own regions, so a
// power cut while writing one must leave every other record readable and
// byte-exact -- otherwise one interrupted save loses the whole set.
void NvmPortSuite::torn_commit_leaves_every_other_region_untouched() {
  std::vector<uint8_t> keep = frame(4, pattern(16, 0x11));
  int rc = h.commit(4, keep);
  CHECK(rc == 0 && h.store_match(4, keep), "T16 neighbour record committed");

  // snapshot EVERY region: checking only the neighbour goes blind if the
  // clobber lands one region over, and the README claims "every other
  // record", not "the record next door".
  int erases_before[N_REGIONS];
  std::vector<std::vector<uint8_t>> store_before(N_REGIONS);
  for (int r = 0; r < N_REGIONS; ++r) {
    erases_before[r] = h.erase_count[r];
    store_before[r].assign(h.store[r], h.store[r] + REG_BYTES);
  }
  h.ops.clear();
  std::vector<uint8_t> torn = frame(1, pattern(16, 0x22));
  h.arm_err(1, 5);
  rc = h.commit(1, torn);
  h.disarm_err();
  CHECK(rc == 1, "T16 the neighbouring commit was torn");

  bool other_erased = false;
  bool other_moved = false;
  for (int r = 0; r < N_REGIONS; ++r) {
    if (r == 1) continue;                       // the torn record's own region
    if (h.erase_count[r] != erases_before[r]) other_erased = true;
    if (!std::equal(store_before[r].begin(), store_before[r].end(),
                    h.store[r])) other_moved = true;
  }
  // Anti-vacuity: "no OTHER region moved" is trivially true if the commit
  // never reached the device at all. Pin that it DID touch its own region
  // first, so the isolation claim below is made about a real operation.
  // Both halves are needed: the ERASE alone fires even when zero data bytes
  // ever move (arm_err(1,-1) fails the WRITE before its first byte), so the
  // region's own bytes must be seen to change as well.
  CHECK(h.erase_count[1] > erases_before[1],
        "T16 the torn commit really did erase its own region");
  // Anti-vacuity rests on the TWO CHECKS BELOW THAT READ THE DUT, not on
  // the byte comparison after them. Two earlier spellings were vacuous:
  // "the bytes changed" is satisfied by the ERASE alone, and "some byte is
  // not 0xFF" is satisfied by residue -- region 1 still holds T5b's record
  // (the f5b commit in T5) eleven phases later, so that guard passed even when
  // the port wedged and issued no traffic at all. Note the byte comparison
  // does NOT separate those cases by itself either: torn[0..4] is
  // 17 22 01 01 00, byte-identical to the T5b prefix, so all its separating
  // power is in store[1][5] == 0xFF. The op log and the erase count are
  // what a no-traffic port cannot fake: both are driven by dev_req_o.
  //
  // The byte check reads `sent`, the bus handshake log, NOT the array. What
  // the array retained after an error is the device model's choice -- this
  // model keeps every accepted byte, a half-page model drops the last four,
  // a page-buffered NOR keeps none until the program cycle ends -- so an
  // array-relative assertion here tests the model. What the PORT put on the
  // bus is the port's behaviour under all three.
  CHECK(h.ops.size() == 2 && op_is(h.ops[1], OP_WRITE, 1, 0,
                                   static_cast<int>(torn.size())),
        "T16 the torn commit issued ERASE then the WRITE for this record");
  CHECK(h.sent.size() == 5 && std::equal(h.sent.begin(), h.sent.end(),
                                         torn.begin()),
        "T16 the port sent exactly the 5 record bytes before the cut");
  CHECK(!other_erased, "T16 the torn commit erased no other region");
  CHECK(!other_moved, "T16 no other region's bytes moved");
  CHECK(h.store_match(4, keep),
        "T16 the neighbour's stored bytes are untouched");
  h.ops.clear();
  rc = h.restore(4);
  CHECK(rc == 0 && h.rbytes == keep,
        "T16 the neighbour still restores byte-exactly after the cut");
}

// ---------------------------------------------------------------- T17
// The cut that NOR flash actually produces. T15/T16 cut mid-stream, while
// bytes are still moving. A real program failure is not reported then: the
// device latches the bytes, starts the program cycle, and raises its error
// only when that cycle ends -- after the LAST byte, with busy still high.
// That is the port's S_WWAIT arm (KL_pp_nvm_port.sv:262-265), the widest
// window in a commit, and no phase above enters it. Arming at exactly the
// write length takes the device's fail branch in preference to its done
// branch, so every byte is consumed and then err replaces done.
void NvmPortSuite::late_write_failure_reports_err_not_done() {
  std::vector<uint8_t> rec = frame(3, pattern(20, 0xC5));
  h.ops.clear();
  int rc = h.commit(3, rec);
  CHECK(rc == 0 && h.store_match(3, rec), "T17 seed record committed");

  std::vector<uint8_t> late = frame(3, pattern(20, 0xD6));
  h.ops.clear();
  // op 0 = ERASE, op 1 = WRITE. The WRITE carries the whole framed record,
  // so cutting after that many bytes lands in the completion window.
  h.arm_err(1, static_cast<int>(late.size()));
  rc = h.commit(3, late);
  h.disarm_err();
  CHECK(rc == 1 && h.err_pulses == 1 && h.done_pulses == 0,
        "T17 a failure in the completion window reports err, never done");
  // Pin that the cut actually landed in the COMPLETION window. Without this
  // the phase passes with the tear moved anywhere in the stream, and its
  // whole point is the window: every byte accepted, THEN the error. `sent`
  // holding the full record is what distinguishes S_WWAIT from S_WDPUMP.
  CHECK(h.sent.size() == late.size(),
        "T17 the cut was in the completion window: every byte sent first");
  CHECK(h.busy_seen && h.busy_ok,
        "T17 busy raised then low at the err pulse");
  // A wedge and a wrong answer are different failures and rc == 1 above
  // already excludes both, so do not restate it. Assert instead what only a
  // released port can show: busy low and idle once the pulse has passed.
  CHECK(!dut->nvm_busy_o, "T17 the port is idle after the late failure");

  // What the array holds afterwards is NOT pinned here, and deliberately.
  // This device model writes every byte and then reports the failure, so
  // region 3 now holds a well-formed `late`. Real NOR may leave the last
  // page half-programmed. The port cannot tell those apart and neither can
  // this model, so the phase pins what the PORT owes -- err not done, busy
  // released, bus not stranded -- and only that the port stays usable.
  // The read side after the error exit is a port property, but it must be
  // asserted where the array is KNOWN. What region 3 holds right after the
  // tear is the device model's choice, so restoring here would test the
  // model (two earlier spellings did exactly that). Commit a good record
  // first -- that ends in `done`, so every model agrees what the array now
  // holds -- and only then exercise the read side, pinning the device ops
  // the way T2 does so a fabricated restore cannot pass.
  h.ops.clear();
  rc = h.commit(3, rec);
  CHECK(rc == 0 && h.store_match(3, rec),
        "T17 the port accepts the next commit after a late failure");

  h.ops.clear();
  rc = h.restore(3);
  CHECK(rc == 0 && h.rbytes == rec,
        "T17 the read side works after the error exit: restore byte-exact");
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_READ, 3, 0, 8)
            && op_is(h.ops[1], OP_READ, 3, 8,
                     static_cast<int>(rec.size()) - 8),
        "T17 that restore really issued READ hdr then READ payload");
}

// ---------------------------------------------------------------- T18
// The RESTORE side of the same argument. T17 covers the completion window
// on a WRITE, but a NOR read fails the same way: an ECC or timeout error
// surfaces when the read cycle ends, not mid-stream. `S_RPWAIT` is the
// exact mirror of the arm T17 closed, `S_RHWAIT` is that window on the
// header probe, and `S_RHCOLL` is an error during the header collect --
// which sits on the boot restore walk, the one path where a torn image is
// actually consumed. All three survived the suite before this phase.
void NvmPortSuite::read_completion_window_errors_report_err() {
  h.ops.clear();
  h.arm_err(0, 3);
  int r = h.restore(5);
  h.disarm_err();
  CHECK(r == 1 && h.err_pulses == 1, "T18 an error collecting the header reports err (S_RHCOLL)");
  CHECK(h.ops.size() == 1 && op_is(h.ops[0], OP_READ, 5, 0, 8) && h.dev_rd == 3,
        "T18 S_RHCOLL was reached: the tear landed 3 bytes into the header");
  CHECK(h.dev_errs == 1, "T18 the DEVICE raised the error, not the port refusing");

  h.ops.clear();
  h.arm_err(0, 8);
  r = h.restore(5);
  h.disarm_err();
  CHECK(r == 1 && h.err_pulses == 1, "T18 an error closing the header read reports err (S_RHWAIT)");
  CHECK(h.ops.size() == 1 && op_is(h.ops[0], OP_READ, 5, 0, 8) && h.dev_rd == 8,
        "T18 S_RHWAIT was reached: all 8 header bytes delivered before the error");
  CHECK(h.dev_errs == 1, "T18 the DEVICE raised the error, not the port refusing");

  h.ops.clear();
  h.arm_err(1, 40);
  r = h.restore(5);
  h.disarm_err();
  CHECK(r == 1 && h.err_pulses == 1,
        "T18 an error in the payload completion window reports err (S_RPWAIT)");
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_READ, 5, 0, 8)
            && h.ops[1].op == OP_READ && h.ops[1].offset == 8
            && h.dev_rd == 48 && h.rbytes.size() == f2.size(),
        "T18 S_RPWAIT was reached: all 48 bytes delivered, whole record forwarded");
  CHECK(h.dev_errs == 1, "T18 the DEVICE raised the error, not the port refusing");

  h.ops.clear();
  r = h.restore(5);
  CHECK(r == 0 && h.rbytes == f2,
        "T18 serviceable after the three read cuts: restore is byte-exact");
}

// ---------------------------------------------------------------- T19
// Issue #14: a completion the port does NOT own, on the commit path.
//
// `done_seen_r` is sticky so a `done` landing on the same edge as a pump's
// last byte is not lost (KL_pp_nvm_port.sv:175-179). The set is gated on
// owning the command it completes -- from the grant handshake to the wait
// state that consumes it (`dev_cmd_owned_w`, :151-162). Ungated, a stray
// `done` while the header is still being collected is consumed by `S_WEWAIT`
// as the ERASE's, and the WRITE goes into a region the backend is still
// erasing -- reported as `done`, not `err`.
//
// This needs the device the harness could not play before: one that pulses
// `done` for no command at all. Each arm names its window on the BUS -- how
// many commands the backend has accepted, and whether a request is up that it
// has not granted -- so no check here reads DUT state, and the two things the
// port must not do are counted on the bus as well.
void NvmPortSuite::unsolicited_completion_during_a_commit() {
  h.gnt_delay = 6; h.op_delay = 8;    // open the ungranted-request window
  std::vector<uint8_t> rec = frame(2, pattern(24, 0x1E));

  // (a) S_WHDR -- the port is collecting the header and has issued nothing.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/0, /*in_req=*/false);
  int rc = h.commit(2, rec);
  CHECK(h.unsol_dones == 1 && !h.unsol_req && h.unsol_ops == 0
            && h.unsol_mgr > 0 && h.unsol_mgr < 8,
        "T19a the backend pulsed one done for no command, %d header bytes in "
        "(dones %d, req %d, ops %d)",
        h.unsol_mgr, h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec,
        "T19a the commit still completes with done, byte-exact on the bus");
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_ERASE, 2, 0, 0)
            && op_is(h.ops[1], OP_WRITE, 2, 0, static_cast<int>(rec.size())),
        "T19a ERASE then WRITE, both issued");
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0,
        "T19a the stray done was not consumed as the ERASE's: nothing "
        "requested (%d) or answered (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed);

  // (b) S_WEREQ -- the ERASE is requested and the backend has not granted it.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/0, /*in_req=*/true);
  rc = h.commit(2, rec);
  CHECK(h.unsol_dones == 1 && h.unsol_req && h.unsol_ops == 0,
        "T19b the pulse landed with the ERASE requested and ungranted "
        "(dones %d, req %d, ops %d)",
        h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec,
        "T19b the commit still completes with done, byte-exact on the bus");
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0,
        "T19b a done before the grant is not the granted command's: nothing "
        "requested (%d) or answered (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed);

  // (c) S_WWREQ -- the ERASE is complete, the WRITE is requested and ungranted.
  // This is the arm the withdrawn S_WHDR-only clear would have left open, and
  // the stale flag is consumed by `S_WWAIT` rather than `S_WEWAIT`: the commit
  // reports done while the backend is still programming.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/1, /*in_req=*/true);
  rc = h.commit(2, rec);
  CHECK(h.unsol_dones == 1 && h.unsol_req && h.unsol_ops == 1,
        "T19c the pulse landed with the WRITE requested and ungranted "
        "(dones %d, req %d, ops %d)",
        h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec,
        "T19c the commit still completes with done, byte-exact on the bus");
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0,
        "T19c the commit was not answered on someone else's done: nothing "
        "requested (%d) or answered (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed);

  h.gnt_delay = 1; h.op_delay = 4;
}

// ---------------------------------------------------------------- T20
// The same defect on the RESTORE path, which is why the one-line clear in
// `S_WHDR` this ticket first proposed was withdrawn: a restore goes
// S_IDLE -> S_RHREQ and never enters S_WHDR at all, while `S_RHWAIT` and
// `S_RPWAIT` consume the flag exactly as the commit's wait states do. The
// boot restore walk is the path that reads a torn image, so a completion
// consumed by the wrong read is the one that ends with the manager handed a
// record the backend never finished delivering.
void NvmPortSuite::unsolicited_completion_during_a_restore() {
  h.gnt_delay = 6; h.op_delay = 8;

  // (a) S_RHREQ -- the header READ is requested and ungranted.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/0, /*in_req=*/true);
  int rc = h.restore(5);
  CHECK(h.unsol_dones == 1 && h.unsol_req && h.unsol_ops == 0,
        "T20a the pulse landed with the header READ requested and ungranted "
        "(dones %d, req %d, ops %d)",
        h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.rbytes == f2,
        "T20a the restore still completes with done, stream byte-exact");
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_READ, 5, 0, 8)
            && op_is(h.ops[1], OP_READ, 5, 8,
                     static_cast<int>(f2.size()) - 8),
        "T20a READ hdr then READ payload, both issued");
  // The forward counter is the one that fails here. A completion taken in an
  // ungranted `S_RHREQ` is consumed by `S_RHWAIT` the cycle the eighth header
  // byte lands, so the port hands the buffered header up while the backend is
  // still counting out the completion for the read that filled it. The request
  // and pulse counters only catch that if the backend is still owing one a
  // whole header forward later, which is a property of `op_delay`, not of the
  // port: at the delay this phase runs they are both back to zero.
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0 && h.fwd_while_owed == 0,
        "T20a the header read was not closed on a stray done: nothing "
        "requested (%d), answered (%d) or forwarded from the header buffer "
        "(%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed, h.fwd_while_owed);

  // (b) S_RHFWD -- the header read is done and the payload READ is not yet
  // requested, so the port owns nothing while it hands the header up.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/1, /*in_req=*/false);
  rc = h.restore(5);
  CHECK(h.unsol_dones == 1 && !h.unsol_req && h.unsol_ops == 1
            && h.unsol_mgr > 0 && h.unsol_mgr < 8,
        "T20b the backend pulsed one done between the two reads, %d header "
        "bytes forwarded (dones %d, req %d, ops %d)",
        h.unsol_mgr, h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.rbytes == f2,
        "T20b the restore still completes with done, stream byte-exact");
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0 && h.fwd_while_owed == 0,
        "T20b the payload read was not closed on the header read's leftover: "
        "nothing requested (%d), answered (%d) or forwarded (%d) while the "
        "backend still owed one",
        h.req_while_owed, h.pulse_while_owed, h.fwd_while_owed);

  // (c) S_RPREQ -- the payload READ is requested and ungranted.
  h.ops.clear();
  h.arm_unsolicited_done(/*after_ops=*/1, /*in_req=*/true);
  rc = h.restore(5);
  CHECK(h.unsol_dones == 1 && h.unsol_req && h.unsol_ops == 1,
        "T20c the pulse landed with the payload READ requested and ungranted "
        "(dones %d, req %d, ops %d)",
        h.unsol_dones, int(h.unsol_req), h.unsol_ops);
  CHECK(rc == 0 && h.done_pulses == 1 && h.rbytes == f2,
        "T20c the restore still completes with done, stream byte-exact");
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0 && h.fwd_while_owed == 0,
        "T20c the payload read was not closed before its own done: nothing "
        "requested (%d), answered (%d) or forwarded (%d) while the backend "
        "still owed one",
        h.req_while_owed, h.pulse_while_owed, h.fwd_while_owed);

  h.gnt_delay = 1; h.op_delay = 4;
}

// ---------------------------------------------------------------- T21
// The PERMITTED coincidence at the other edge of the ownership window, and
// the reason the window opens at the grant rather than after it. The port's
// own header says a backend without erase semantics answers ERASE with done
// at once (KL_pp_nvm_port.sv:33-34), and at once can mean the cycle it takes
// the command: `dev_gnt_i` and `dev_done_i` together, while `S_WEREQ` is
// still driving the request. That completion IS the port's, and refusing it
// would wedge the commit in `S_WEWAIT` for a device that did nothing wrong.
//
// T19 and T20 pin what the port must not take; without this phase the grant
// term of `dev_cmd_owned_w` could be deleted with the suite still green, and
// a fix narrowed that far reads as correct while it hangs a real backend.
void NvmPortSuite::completion_riding_the_grant_is_taken() {
  h.gnt_delay = 3; h.op_delay = 6;
  h.gnt_done_on_erase = true;
  std::vector<uint8_t> rec = frame(6, pattern(28, 0x2B));
  h.ops.clear();
  int rc = h.commit(6, rec);
  h.gnt_done_on_erase = false;
  CHECK(h.gnt_done_pairs == 1,
        "T21 the backend answered ERASE on its own grant cycle (%d pairs)",
        h.gnt_done_pairs);
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec,
        "T21 the commit takes a completion that rode the grant, rc=%d", rc);
  CHECK(h.ops.size() == 2 && op_is(h.ops[0], OP_ERASE, 6, 0, 0)
            && op_is(h.ops[1], OP_WRITE, 6, 0, static_cast<int>(rec.size())),
        "T21 ERASE then WRITE, both issued");
  // One completion answers ONE command: consuming it twice would close the
  // WRITE as well, and the port would answer the manager while the backend
  // was still programming.
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0,
        "T21 the grant's done closed the ERASE only: nothing requested (%d) "
        "or answered (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed);
  h.gnt_delay = 1; h.op_delay = 4;
}

// ---------------------------------------------------------------- T22
// The coincidence the sticky latch was written for, and the one the eight
// state terms of `dev_cmd_owned_w` carry: the backend raises `done` on the
// same edge that moves the command's final byte, while the port is still in
// the pump or collect state. A cycle later the wait state reads `done_seen_r`,
// not `dev_done_i`, so a fix narrowed to the grant handshake alone drops the
// completion and the port waits forever for one the backend already sent.
//
// T21 is the same argument at the other end of the window. Between them the
// two edges of `dev_cmd_owned_w` are both defended by a standing check: T21
// the grant term, this phase the four states that can move a final byte --
// `S_WHPUMP`, `S_WDPUMP`, `S_RHCOLL` and `S_RPPUMP`. The four wait states in
// the expression cannot be pinned by any phase, and the suite README says so
// and says why.
//
// Every check here is on the bus or on the manager stream, so the phase holds
// under every device model; `measure_figures.py` runs it under all six.
void NvmPortSuite::completion_riding_the_last_byte_is_taken() {
  const bool was_armed = h.done_on_last_byte;   // the gate arms it for a whole run
  h.done_on_last_byte = true;

  // (a) the WRITE's payload pump: the completion rides the last data byte,
  // taken in `S_WDPUMP` and consumed by `S_WWAIT`.
  std::vector<uint8_t> rec = frame(4, pattern(20, 0x5C));
  h.ops.clear();
  int rc = h.commit(4, rec);
  CHECK(h.coinc_dones == 1,
        "T22a the backend answered the WRITE on the edge that moved its last "
        "byte (%d such completions)", h.coinc_dones);
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec,
        "T22a the commit takes a completion that rode the last byte, rc=%d", rc);
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0,
        "T22a one completion closed one command: nothing requested (%d) or "
        "answered (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed);

  // (b) a zero-payload record: the WRITE is the eight header bytes alone, so
  // its final byte moves in `S_WHPUMP` instead.
  std::vector<uint8_t> empty = frame(4, {});
  h.ops.clear();
  rc = h.commit(4, empty);
  CHECK(h.coinc_dones == 1 && h.ops.size() == 2
            && op_is(h.ops[1], OP_WRITE, 4, 0, 8),
        "T22b the header-only WRITE was answered on its last byte (%d, %zu ops)",
        h.coinc_dones, h.ops.size());
  CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == empty,
        "T22b the zero-payload commit completes on that completion, rc=%d", rc);

  // (c) both read phases at once: the header READ's eighth byte is collected
  // in `S_RHCOLL` and the payload READ's last byte moves in `S_RPPUMP`, so one
  // restore covers both. The forward counter is live here: the header may only
  // be handed up once its own read has completed, which on this backend is the
  // same edge rather than `op_delay` later.
  h.ops.clear();
  rc = h.restore(5);
  CHECK(h.coinc_dones == 2,
        "T22c both reads were answered on their last byte (%d)", h.coinc_dones);
  CHECK(rc == 0 && h.done_pulses == 1 && h.rbytes == f2,
        "T22c the restore takes both completions, stream byte-exact, rc=%d", rc);
  CHECK(h.req_while_owed == 0 && h.pulse_while_owed == 0 && h.fwd_while_owed == 0,
        "T22c neither read was closed early: nothing requested (%d), answered "
        "(%d) or forwarded (%d) while the backend still owed one",
        h.req_while_owed, h.pulse_while_owed, h.fwd_while_owed);

  h.done_on_last_byte = was_armed;
}

// The real close. The check above used to carry this name but T15/T16/T17
// were appended after it, so nothing pinned the port's state at the end of
// the run any more -- a tear phase could leave it busy and no check would say.
void NvmPortSuite::the_port_is_idle_at_the_end_of_the_run() {
  h.tick();
  CHECK(!dut->nvm_busy_o && !dut->nvm_done_o && !dut->nvm_err_o,
        "idle again at the end of the run");
}

int NvmPortSuite::run() {
  reset_leaves_the_port_idle();
  commit_erases_then_writes_byte_exact();
  restore_reads_header_then_payload_byte_exact();
  zero_payload_record_round_trips();
  stalls_on_every_byte_interface_are_survived();
  back_to_back_ops_all_complete();
  request_while_busy_is_ignored();
  erase_error_stops_the_commit_then_recovers();
  write_header_phase_error_surfaces_once();
  read_payload_phase_error_surfaces_once();
  bad_magic_commit_is_refused_before_the_device();
  oversize_payload_length_is_refused();
  bad_stored_magic_is_refused_on_restore();
  oversize_stored_length_is_refused_on_restore();
  refusals_leave_the_port_serviceable();
  torn_commit_never_restores_as_valid();
  torn_commit_leaves_every_other_region_untouched();
  late_write_failure_reports_err_not_done();
  read_completion_window_errors_report_err();
  unsolicited_completion_during_a_commit();
  unsolicited_completion_during_a_restore();
  completion_riding_the_grant_is_taken();
  completion_riding_the_last_byte_is_taken();
  the_port_is_idle_at_the_end_of_the_run();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  NvmPortSuite suite;
  return suite.run();
}

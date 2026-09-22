// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_acmp_nvm_shadow suite — persistence shadow against an INDEPENDENT
// record model, with the REAL KL_pp_nvm_port and the REAL KL_pp_acmp_listener
// in the loop (face compatibility by elaboration, not transcription).
//
// The harness plays the physical NVM (a region-store device model behind
// the port's device face, with grant/completion delays, per-byte stalls
// and targeted error injection) and independently re-implements the F07.8
// record contract: crc16 CCITT-FALSE, big-endian 16-bit header fields, and
// the 20-byte BINDING[i] payload {flags[valid,started,sw], rsv, uid, tk
// EID, ctlr EID} transcribed from 05 §5 / 07 §5 — never from the RTL.
// Injected F07.6 record images (transcribed from the doc figure) stand in
// for executor write-backs: settle, unbind, started-change, and volatile
// -field-only churn that must cost zero NVM traffic.
//
// Proven: debounce coalescing (N changes in one T-NVM-DEBOUNCE window ->
// one ERASE+WRITE burst per touched sink, byte-exact against the model);
// write-through on CHANGE only; boot replay driving the listener's exact
// pre_* face (all sinks ascending, field mapping checked at the accept AND
// against the PRB_W_AVAIL record the listener then writes, discovery
// armed); per-record vendor defaults (empty region, bad crc, bad layout
// version, bad length) that never abort; a TORN mid-record read-back that
// atomically aborts the WHOLE restore (no preload at all, restore_fail);
// change-during-restore ordering (the capture wins over the image, its
// sink is never preloaded, the live value is flushed back); bounded
// commit retry then the sticky alarm.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Vacmp_nvm_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- geometry (pinned by the Makefile / wrap params) ----------------------
constexpr int N_SINKS   = 8;
constexpr int REC_BASE  = 0x20;
constexpr int DEB_TICKS = 50;      // -GDEB_TICKS_P
constexpr int RETRY_MAX = 2;
constexpr int REG_BYTES = 64;
//! ACMP_REC_W_C (384 b, F07.6) carried as 32-bit Verilator words.
constexpr int REC_WORDS = 12;
// device opcodes: plain integers on the port's `dev_op_o`, so `constexpr`
// rather than an `enum class` that would need a cast at every use.
constexpr int OP_READ  = 0;
constexpr int OP_WRITE = 1;
constexpr int OP_ERASE = 2;

// ---- independent F07.8 record model (07 §5.2 transcription) ---------------
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

struct Bind {
  bool valid = false;
  bool started = false;
  bool sw = false;
  uint16_t uid = 0;
  uint64_t tk = 0;
  uint64_t ctlr = 0;
  bool operator==(const Bind& o) const {
    return valid == o.valid && started == o.started && sw == o.sw &&
           uid == o.uid && tk == o.tk && ctlr == o.ctlr;
  }
};

// the 20-byte BINDING payload (05 §5 shadow set; layout per the shadow's
// banner contract, transcribed independently)
static std::vector<uint8_t> payload_of(const Bind& b) {
  std::vector<uint8_t> p(20, 0);
  p[0] = uint8_t((b.valid ? 1 : 0) | (b.started ? 2 : 0) | (b.sw ? 4 : 0));
  p[2] = uint8_t(b.uid >> 8);
  p[3] = uint8_t(b.uid & 0xFF);
  for (int i = 0; i < 8; ++i) p[4 + i]  = uint8_t(b.tk >> (8 * (7 - i)));
  for (int i = 0; i < 8; ++i) p[12 + i] = uint8_t(b.ctlr >> (8 * (7 - i)));
  return p;
}

static std::vector<uint8_t> frame(uint8_t rid, const std::vector<uint8_t>& pl,
                                  uint8_t ver = 0x02, int force_plen = -1) {
  uint16_t plen = (force_plen >= 0) ? uint16_t(force_plen)
                                    : uint16_t(pl.size());
  std::vector<uint8_t> f;
  f.push_back(0x17);
  f.push_back(0x22);
  f.push_back(ver);
  f.push_back(rid);
  f.push_back(uint8_t(plen >> 8));
  f.push_back(uint8_t(plen & 0xFF));
  std::vector<uint8_t> cb(f);
  cb.insert(cb.end(), pl.begin(), pl.end());
  uint16_t c = crc16(cb);
  f.push_back(uint8_t(c >> 8));
  f.push_back(uint8_t(c & 0xFF));
  f.insert(f.end(), pl.begin(), pl.end());
  return f;
}

// ---- F07.6 record-image bit helpers (doc transcription) -------------------
static void wput(uint32_t* w, int lsb, int width, uint64_t v) {
  for (int i = 0; i < width; ++i) {
    int b = lsb + i;
    if ((v >> i) & 1) w[b >> 5] |= 1u << (b & 31);
    else              w[b >> 5] &= ~(1u << (b & 31));
  }
}
static uint64_t wget(const uint32_t* w, int lsb, int width) {
  uint64_t v = 0;
  for (int i = 0; i < width; ++i) {
    int b = lsb + i;
    if ((w[b >> 5] >> (b & 31)) & 1) v |= 1ull << i;
  }
  return v;
}

// build an F07.6 image: the persisted set from b, volatile fields = junk
// seeded by j (the shadow must ignore every one of them)
static void mk_rec(uint32_t* w, const Bind& b, uint8_t j) {
  for (int i = 0; i < REC_WORDS; ++i) w[i] = 0;
  wput(w, 0, 3, j % 8);                 // sm_state       (volatile)
  wput(w, 3, 3, j % 4);                 // pbsta          (volatile)
  wput(w, 6, 5, j % 32);                // acmpsta        (volatile)
  wput(w, 11, 1, b.valid ? 1 : 0);      // bound
  wput(w, 12, 1, b.started ? 1 : 0);    // started
  wput(w, 13, 1, b.sw ? 1 : 0);         // sw
  wput(w, 14, 1, j & 1);                // retried        (volatile)
  wput(w, 15, 2, j % 4);                // srp_decl       (volatile)
  wput(w, 17, 1, (j >> 1) & 1);         // tk_reg         (volatile)
  wput(w, 18, 1, (j >> 2) & 1);         // tk_disc        (volatile)
  wput(w, 32, 64, b.tk);                // talker_eid
  wput(w, 96, 16, b.uid);               // talker_uid
  wput(w, 112, 16, 0x1000u + j);        // probe_seq      (volatile)
  wput(w, 128, 64, b.ctlr);             // bind_ctlr_eid
  wput(w, 192, 64, 0xDEAD0000ull + j);  // settled sid    (volatile)
  wput(w, 256, 48, 0x91E0F0ull + j);    // settled da     (volatile)
  wput(w, 304, 12, 2);                  // settled vlan   (volatile)
  wput(w, 320, 32, 0x77000000u + j);    // last_avail     (volatile)
  wput(w, 352, 8, j);                   // if_idx         (volatile)
}

// ---- accepted-preload record ----------------------------------------------
struct Accept {
  int sink;
  Bind b;
};

namespace {

// ---- harness ---------------------------------------------------------------
struct Harness {
  //! The persistence shadow, the physical-NVM device model, the monitors and
  //! the tally in one object. `checks`/`fails` were file-scope mutables (I.2)
  //! and the lettered phases below were one 284-line `main` (F.3).
  const milan::tb::Model<Vacmp_nvm_wrap> model;
  Vacmp_nvm_wrap* const d = model.get();
  long cycles = 0;

  // device model
  uint8_t store[N_SINKS][REG_BYTES];
  struct DevOp {
    int op;
    int region;
    int offset;
    int len;
  };
  std::vector<DevOp> ops;
  int d_st = 0;                  // 0 idle, 1 data, 2 completing
  int d_reqwait = 0;
  bool d_gnt = false;
  bool d_done = false;
  bool d_err = false;
  bool d_busy = false;
  DevOp d_cur{0, 0, 0, 0};
  int d_bytes = 0;
  int d_stall = 0;
  bool d_rhold = false;
  int done_ctr = 0;
  int err_ctr = 0;
  int gnt_delay = 1;
  int op_delay = 2;
  int rstall = 0;
  int wstall = 0;
  // targeted error injection
  int err_op = -1;
  int err_region = -1;
  int err_offset = -1;
  int err_after = -1;
  int err_count = 0;
  bool fail_cur = false;

  // monitors
  std::vector<Accept> accepts;
  bool pre_valid_seen = false;
  int lsn_preload_wr = 0;        // listener PRB_W_AVAIL preload write-backs
  std::vector<Accept> lsn_pre_recs;
  int disc_arms = 0;
  uint64_t last_disc_eid = 0;

  int checks = 0;
  int fails = 0;

  // carried between phases B, C and D: the op count and the record the
  // started-change left behind
  size_t ops_b = 0;
  Bind b2b;

  Harness() {
    memset(store, 0, sizeof store);
  }

  int row(int region) const { return (region - REC_BASE) & (N_SINKS - 1); }

  void arm_err(int op, int region, int offset, int after, int count) {
    err_op = op; err_region = region; err_offset = offset;
    err_after = after; err_count = count;
  }
  void disarm_err() { err_op = -1; err_count = 0; }

  void seed_region(int sink, const std::vector<uint8_t>& bytes) {
    memset(store[sink], 0, REG_BYTES);
    for (size_t i = 0; i < bytes.size() && i < REG_BYTES; ++i)
      store[sink][i] = bytes[i];
  }
  bool store_match(int sink, const std::vector<uint8_t>& bytes) const {
    for (size_t i = 0; i < bytes.size(); ++i)
      if (store[sink][i] != bytes[i]) return false;
    return true;
  }

  void drive_dev() {
    d->dev_gnt_i  = d_gnt;
    d->dev_done_i = d_done;
    d->dev_err_i  = d_err;
    d->dev_busy_i = d_busy;
    bool wr = (d_st == 1 && d_cur.op == OP_WRITE && d_stall == 0);
    d->dev_wready_i = wr;
    bool rv = (d_st == 1 && d_cur.op == OP_READ && d_bytes < d_cur.len
               && (d_stall == 0 || d_rhold));
    d->dev_rvalid_i = rv;
    d->dev_rdata_i  = rv ? store[row(d_cur.region)]
                                [(d_cur.offset + d_bytes) % REG_BYTES]
                         : 0;
  }

  void sample_dev() {
    bool drove_gnt = d_gnt;
    bool drove_done = d_done;
    bool drove_err = d_err;

    if (drove_gnt && d->dev_req_o) {
      d_cur = {int(d->dev_op_o), int(d->dev_region_o),
               int(d->dev_offset_o), int(d->dev_len_o)};
      ops.push_back(d_cur);
      d_busy = true; d_bytes = 0; d_stall = 0; d_rhold = false;
      fail_cur = (err_count > 0)
                 && (err_op < 0 || d_cur.op == err_op)
                 && (err_region < 0 || d_cur.region == err_region)
                 && (err_offset < 0 || d_cur.offset == err_offset);
      if (fail_cur) --err_count;
      if (fail_cur && err_after < 0) {
        err_ctr = op_delay; d_st = 2;
      } else if (d_cur.op == OP_ERASE) {
        memset(store[row(d_cur.region)], 0xFF, REG_BYTES);
        done_ctr = op_delay; d_st = 2;
      } else if (d_cur.len == 0) {
        done_ctr = op_delay; d_st = 2;
      } else {
        d_st = 1;
      }
    }

    if (d_st == 1 && d_cur.op == OP_WRITE) {
      if (d->dev_wready_i && d->dev_wvalid_o) {
        store[row(d_cur.region)][(d_cur.offset + d_bytes) % REG_BYTES] =
            d->dev_wdata_o;
        ++d_bytes;
        d_stall = wstall;
        if (fail_cur && d_bytes == err_after) { err_ctr = 2; d_st = 2; }
        else if (d_bytes == d_cur.len) { done_ctr = op_delay; d_st = 2; }
      } else if (d_stall > 0) --d_stall;
    }

    if (d_st == 1 && d_cur.op == OP_READ) {
      if (d->dev_rvalid_i) {
        if (d->dev_rready_o) {
          ++d_bytes; d_rhold = false; d_stall = rstall;
          if (fail_cur && d_bytes == err_after) { err_ctr = 2; d_st = 2; }
          else if (d_bytes == d_cur.len) { done_ctr = op_delay; d_st = 2; }
        } else {
          d_rhold = true;
        }
      } else if (d_stall > 0) --d_stall;
    }

    if (drove_gnt)  d_gnt  = false;
    if (drove_done) d_done = false;
    if (drove_err)  d_err  = false;

    if (d_st == 0 && !d_busy && d->dev_req_o && !drove_gnt) {
      if (++d_reqwait >= gnt_delay) { d_gnt = true; d_reqwait = 0; }
    }
    if (d_st == 2) {
      if (done_ctr > 0 && --done_ctr == 0) { d_done = true; d_busy = false; d_st = 0; }
      if (err_ctr  > 0 && --err_ctr  == 0) { d_err  = true; d_busy = false; d_st = 0; }
    }
  }

  void sample_monitors() {
    if (d->pre_valid_o) pre_valid_seen = true;
    if (d->pre_valid_o && d->pre_ready_o) {
      Accept a;
      a.sink      = int(d->pre_sink_o);
      a.b.valid   = true;
      a.b.started = d->pre_started_o;
      a.b.sw      = d->pre_sw_o;
      a.b.uid     = uint16_t(d->pre_talker_uid_o);
      a.b.tk      = d->pre_talker_eid_o;
      a.b.ctlr    = d->pre_ctlr_eid_o;
      accepts.push_back(a);
    }
    if (d->lsn_recwr_o) {
      const uint32_t* w = &d->lsn_recwr_rec_o[0];
      // a preload write-back: PRB_W_AVAIL (sm 1) + bound, from X_PRELOAD
      if (wget(w, 0, 3) == 1 && wget(w, 11, 1) == 1) {
        Accept a;
        a.sink      = int(d->lsn_recwr_sink_o);
        a.b.valid   = true;
        a.b.started = wget(w, 12, 1) != 0;
        a.b.sw      = wget(w, 13, 1) != 0;
        a.b.uid     = uint16_t(wget(w, 96, 16));
        a.b.tk      = wget(w, 32, 64);
        a.b.ctlr    = wget(w, 128, 64);
        lsn_pre_recs.push_back(a);
        ++lsn_preload_wr;
      }
    }
    if (d->lsn_disc_arm_o) {
      ++disc_arms;
      last_disc_eid = d->lsn_disc_eid_o;
    }
  }

  void tick() {
    drive_dev();
    d->clk_i = 0; d->eval();
    sample_monitors();
    sample_dev();
    d->clk_i = 1; d->eval();
    ++cycles;
  }

  void run(int n) { for (int i = 0; i < n; ++i) tick(); }

  template <typename F>
  bool run_until(F cond, int max_cycles) {
    for (int i = 0; i < max_cycles; ++i) {
      if (cond()) return true;
      tick();
    }
    return cond();
  }

  void reset() {
    d->rst_n = 0;
    d->tick_i = 0;
    d->restore_go_i = 0;
    d->tb_cap_wr_i = 0;
    d->tb_cap_sink_i = 0;
    for (int i = 0; i < REC_WORDS; ++i) d->tb_cap_rec_i[i] = 0;
    d->evt_block_i = 0;
    d_st = 0; d_reqwait = 0; d_gnt = d_done = d_err = d_busy = false;
    d_bytes = d_stall = 0; d_rhold = false; done_ctr = err_ctr = 0;
    disarm_err();
    ops.clear(); accepts.clear(); lsn_pre_recs.clear();
    pre_valid_seen = false; lsn_preload_wr = 0; disc_arms = 0;
    run(5);
    d->rst_n = 1;
    d->tick_i = 1;               // 1 tick per cycle: window = DEB_TICKS cycles
    run(N_SINKS + 6);            // both init sweeps complete
  }

  void inject(int sink, const Bind& b, uint8_t junk) {
    uint32_t w[REC_WORDS];
    mk_rec(w, b, junk);
    d->tb_cap_sink_i = uint8_t(sink);
    for (int i = 0; i < REC_WORDS; ++i) d->tb_cap_rec_i[i] = w[i];
    d->tb_cap_wr_i = 1;
    tick();
    d->tb_cap_wr_i = 0;
    tick();
  }

  void go() {
    d->restore_go_i = 1;
    tick();
    d->restore_go_i = 0;
  }

  bool restore_done() { return d->restore_done_o != 0; }

  int count_ops(int op, int region = -1, int offset = -1) const {
    int n = 0;
    for (const DevOp& o : ops)
      if (o.op == op && (region < 0 || o.region == region)
          && (offset < 0 || o.offset == offset)) ++n;
    return n;
  }

  void check_empty_boot_reports_blank();
  void check_capture_debounce_and_write_through();
  void check_volatile_only_churn_costs_no_traffic();
  void check_unbind_capture_commits();
  void check_bounded_commit_retry_and_the_alarm();
  void check_boot_replay_from_a_seeded_image();
  void check_a_torn_readback_aborts_the_whole_restore();
  void check_a_change_during_restore_wins();
  void check_a_change_during_its_own_flush_reserializes();
  void check_the_unflushed_export_contract();
  int report();
  int run_suite();
};

// ---- constants -------------------------------------------------------------
constexpr uint64_t TK_A = 0x00221100AABBCCDDull;
constexpr uint64_t TK_B = 0x00221100AABBCC55ull;
constexpr uint64_t CTL1 = 0x0011223344556677ull;
constexpr uint64_t CTL2 = 0x0099AABBCCDDEEFFull;

// ======================================================== A: empty boot
void Harness::check_empty_boot_reports_blank() {
  reset();
  CHECK(d->pre_ready_o, "A0 listener idle, pre_ready high");
  go();
  CHECK(run_until([&] { return restore_done(); }, 5000),
        "A1 restore completes on an empty NVM");
  CHECK(!d->restore_fail_o, "A2 empty NVM is defaults, not a failure");
  // ...but "not a failure" is not "a restore happened". Milan 5.3.8.2 makes
  // the bound state reportable, and done is set on THIS path exactly as it is
  // on a walk that put every sink back, so an integrator reading done alone
  // cannot tell the two apart. restore_blank_o is the pin that can.
  CHECK(d->restore_blank_o,
        "A2b an empty NVM reports BLANK: done, but zero records validated");
  CHECK(!pre_valid_seen, "A3 no preload driven from an empty NVM");
  CHECK(count_ops(OP_READ) == N_SINKS,
        "A4 walk = one header read per sink (got %d)", count_ops(OP_READ));
  CHECK(d->dbg_dirty_o == 0, "A5 nothing dirty after restore");
  CHECK(d->dbg_valid_o == 0, "A6 nothing valid after restore");
}

// ============================= B: capture + debounce + write-through bytes
void Harness::check_capture_debounce_and_write_through() {
  Bind b2{true, false, true, 1, TK_A, CTL1};
  inject(2, b2, 0x11);
  run(10);
  CHECK(count_ops(OP_WRITE) == 0, "B1 no commit inside the debounce window");
  CHECK((d->dbg_dirty_o >> 2) & 1, "B2 change marked dirty");
  b2b = b2; b2b.started = true;                 // started-change
  inject(2, b2b, 0x12);
  Bind b5{true, false, false, 2, TK_B, CTL2};
  inject(5, b5, 0x13);
  CHECK(run_until([&] { return count_ops(OP_WRITE) >= 2; }, 3000),
        "B3 burst released after T-NVM-DEBOUNCE");
  run(300);                                    // drain + prove quiescence
  CHECK(count_ops(OP_WRITE) == 2,
        "B4 three changes coalesce to ONE burst of two records (got %d)",
        count_ops(OP_WRITE));
  CHECK(count_ops(OP_ERASE) == 2, "B5 each commit is ERASE then WRITE");
  CHECK(store_match(2, frame(uint8_t(REC_BASE + 2), payload_of(b2b))),
        "B6 sink 2 record byte-exact vs the model (latest fields win)");
  CHECK(store_match(5, frame(uint8_t(REC_BASE + 5), payload_of(b5))),
        "B7 sink 5 record byte-exact vs the model");
  CHECK(d->dbg_dirty_o == 0, "B8 dirty cleared after the burst");
  ops_b = ops.size();
}

// ============================= C: volatile-only churn costs zero traffic
void Harness::check_volatile_only_churn_costs_no_traffic() {
  inject(2, b2b, 0x77);                        // same persisted set, new junk
  run(DEB_TICKS * 3);
  CHECK(d->dbg_dirty_o == 0, "C1 volatile-field write-back never dirties");
  CHECK(ops.size() == ops_b, "C2 volatile-field write-back costs no NVM op");
}

// ======================================================= D: unbind capture
void Harness::check_unbind_capture_commits() {
  Bind un{};                                     // valid=0, all zero
  inject(5, un, 0x00);
  CHECK(run_until([&] { return ops.size() >= ops_b + 2; }, 3000),
        "D1 unbind commits after the window");
  run(200);
  CHECK(store_match(5, frame(uint8_t(REC_BASE + 5), payload_of(un))),
        "D2 unbind record byte-exact (valid=0 payload)");
  CHECK(ops.size() == ops_b + 2, "D3 exactly one ERASE+WRITE for the unbind");
}

// ================================== E: commit retry (bounded) + the alarm
void Harness::check_bounded_commit_retry_and_the_alarm() {
  Bind b1{true, true, false, 3, TK_B, CTL1};
  arm_err(OP_WRITE, REC_BASE + 1, -1, -1, 1);  // fail the first WRITE once
  inject(1, b1, 0x21);
  CHECK(run_until([&] {
          return count_ops(OP_WRITE, REC_BASE + 1) >= 2 && !d->dbg_dirty_o;
        }, 4000),
        "E1 errored commit is retried and lands");
  CHECK(store_match(1, frame(uint8_t(REC_BASE + 1), payload_of(b1))),
        "E2 retried record byte-exact");
  CHECK(!d->alarm_o, "E3 a recovered retry never alarms");
  Bind b1b = b1; b1b.started = false;
  arm_err(OP_WRITE, REC_BASE + 1, -1, -1, 100);  // fail every WRITE
  inject(1, b1b, 0x22);
  CHECK(run_until([&] { return d->alarm_o != 0; }, 6000),
        "E4 retries exhausted -> sticky side-port alarm");
  run(100);
  CHECK(d->dbg_dirty_o == 0, "E5 given-up record drops dirty (no livelock)");
  disarm_err();
  size_t ops_e = ops.size();
  Bind b4{true, false, true, 4, TK_A, CTL2};
  inject(4, b4, 0x23);
  CHECK(run_until([&] {
          return count_ops(OP_WRITE, REC_BASE + 4) >= 1 && !d->dbg_dirty_o;
        }, 4000),
        "E6 the engine still commits after an alarm");
  CHECK(store_match(4, frame(uint8_t(REC_BASE + 4), payload_of(b4))),
        "E7 post-alarm record byte-exact");
  (void)ops_e;
}

// ============================================ F: boot replay, seeded image
void Harness::check_boot_replay_from_a_seeded_image() {
  Bind f0{true, true, false, 5, 0x1111111122222222ull, CTL1};
  Bind f3{true, false, true, 6, 0x3333333344444444ull, CTL2};
  Bind f7{true, true, true, 7, 0x5555555566666666ull, 0x0123456789ABCDEFull};
  Bind f4{};                                      // a committed unbind
  for (int k = 0; k < N_SINKS; ++k) seed_region(k, {});
  seed_region(0, frame(uint8_t(REC_BASE + 0), payload_of(f0)));
  seed_region(3, frame(uint8_t(REC_BASE + 3), payload_of(f3)));
  seed_region(7, frame(uint8_t(REC_BASE + 7), payload_of(f7)));
  seed_region(4, frame(uint8_t(REC_BASE + 4), payload_of(f4)));
  {  // sink 6: crc corrupted; sink 1: wrong layout version; sink 2: bad length
    auto c = frame(uint8_t(REC_BASE + 6), payload_of(f0));
    c[15] ^= 0x40;
    seed_region(6, c);
    //! a version this build does NOT accept. It was 0x02 while the shadow
    //! was at 0x01; issue #78 moved the shadow to 0x02 (the record's bytes
    //! are unchanged but `started` means something now), which would have
    //! quietly turned this negative case into a valid record - the "wrong
    //! version is refused" property would then have been passing on a
    //! record the RTL accepts.
    seed_region(1, frame(uint8_t(REC_BASE + 1), payload_of(f3), 0x03));
    auto pl24 = payload_of(f7); pl24.resize(24, 0);
    seed_region(2, frame(uint8_t(REC_BASE + 2), pl24));
  }
  reset();
  go();
  // backpressure the first preload via the listener's own priority order
  CHECK(run_until([&] { return d->pre_valid_o != 0; }, 5000),
        "F0 replay reaches the first preload");
  {
    d->evt_block_i = 1;
    bool stable = true;
    uint64_t tk0 = d->pre_talker_eid_o;
    uint16_t s0 = d->pre_sink_o;
    for (int i = 0; i < 25; ++i) {
      tick();
      if (!d->pre_valid_o || d->pre_talker_eid_o != tk0
          || d->pre_sink_o != s0) stable = false;
    }
    CHECK(stable, "F1 pre_* held stable under listener backpressure");
    CHECK(accepts.empty(), "F2 no accept while the listener is busy");
    d->evt_block_i = 0;
  }
  CHECK(run_until([&] { return restore_done(); }, 20000),
        "F3 restore completes");
  run(5);              // let the listener's last X_PRELOAD strobes land
  CHECK(!d->restore_fail_o, "F4 per-record defaults never abort the restore");
  // the counter-case to A2b: three regions held framed, crc-clean records, so
  // the media ANSWERED and this walk is not blank even though five of the
  // eight sinks fell back to the vendor default.
  CHECK(!d->restore_blank_o,
        "F4b a walk that validated records is NOT reported blank");
  CHECK(accepts.size() == 3,
        "F5 exactly the three valid bindings preload (got %zu)",
        accepts.size());
  if (accepts.size() == 3) {
    CHECK(accepts[0].sink == 0 && accepts[1].sink == 3
              && accepts[2].sink == 7,
          "F6 replay walks sinks in ascending order");
    CHECK(accepts[0].b == f0, "F7 sink 0 preload fields exact");
    CHECK(accepts[1].b == f3, "F8 sink 3 preload fields exact");
    CHECK(accepts[2].b == f7, "F9 sink 7 preload fields exact");
  }
  CHECK(lsn_pre_recs.size() == 3,
        "F10 listener wrote three PRB_W_AVAIL records");
  if (lsn_pre_recs.size() == 3) {
    CHECK(lsn_pre_recs[0].sink == 0 && lsn_pre_recs[0].b == f0,
          "F11 listener record 0 carries the restored binding");
    CHECK(lsn_pre_recs[1].sink == 3 && lsn_pre_recs[1].b == f3,
          "F12 listener record 3 carries the restored binding");
    CHECK(lsn_pre_recs[2].sink == 7 && lsn_pre_recs[2].b == f7,
          "F13 listener record 7 carries the restored binding");
  }
  CHECK(disc_arms == 3 && last_disc_eid == f7.tk,
        "F14 discovery armed per preload (A4), talker EID exact");
  CHECK(d->dbg_valid_o == ((1u << 0) | (1u << 3) | (1u << 7)),
        "F15 valid bits mirror the restored image");
  CHECK(d->dbg_dirty_o == 0,
        "F16 the listener's preload write-backs are compare-equal, no dirty");
  run(DEB_TICKS * 3);
  CHECK(count_ops(OP_WRITE) == 0,
        "F17 a clean restore triggers no NVM write-back at all");
  CHECK(count_ops(OP_READ, REC_BASE + 0) == 2
            && count_ops(OP_READ, REC_BASE + 5) == 1,
        "F18 valid record = header+payload reads; empty region = header only");
}

// ===================================== G: torn read-back aborts the WHOLE
void Harness::check_a_torn_readback_aborts_the_whole_restore() {
  for (int k = 0; k < N_SINKS; ++k)
    seed_region(k, frame(uint8_t(REC_BASE + k), payload_of(
        Bind{true, (k & 1) != 0, (k & 2) != 0, uint16_t(k),
             0xAA00000000000000ull + uint64_t(k), CTL1 + k})));
  reset();
  arm_err(OP_READ, REC_BASE + 3, 8, 5, 1);   // tear region 3 payload @5 B
  go();
  CHECK(run_until([&] { return restore_done(); }, 20000),
        "G1 aborted restore still terminates");
  CHECK(d->restore_fail_o, "G2 torn mid-record read-back -> restore_fail");
  CHECK(!pre_valid_seen,
        "G3 atomic reject: not ONE preload was driven (sinks 0..2 included)");
  CHECK(d->dbg_valid_o == 0, "G4 the whole image is discarded");
  // three records were already validated before the tear; the atomic reject
  // throws them away, so the blank level has to follow the image and not the
  // history, or a torn walk would report records it no longer holds.
  CHECK(d->restore_blank_o,
        "G4b the atomic reject leaves the walk reporting ZERO records");
  CHECK(count_ops(OP_READ, REC_BASE + 4) == 0,
        "G5 the walk stops at the tear");
  disarm_err();
  Bind g0{true, false, false, 9, TK_A, CTL2};
  inject(0, g0, 0x31);
  CHECK(run_until([&] {
          return count_ops(OP_WRITE, REC_BASE + 0) >= 1 && !d->dbg_dirty_o;
        }, 4000),
        "G6 live capture still commits after an aborted restore");
  CHECK(store_match(0, frame(uint8_t(REC_BASE + 0), payload_of(g0))),
        "G7 post-abort record byte-exact");
}

// ============================== H: change during restore — the capture wins
void Harness::check_a_change_during_restore_wins() {
  std::vector<Bind> hv;
  for (int k = 0; k < N_SINKS; ++k) {
    hv.push_back(Bind{true, (k & 1) != 0, (k & 2) != 0, uint16_t(0x30 + k),
                      0xBB00000000000000ull + uint64_t(k), CTL2 + k});
    seed_region(k, frame(uint8_t(REC_BASE + k), payload_of(hv[k])));
  }
  reset();
  rstall = 2;                                 // stretch the walk
  go();
  // "before its read": live change for sink 6 while the walk is at sink 0
  CHECK(run_until([&] { return !ops.empty(); }, 2000),
        "H0 walk started");
  Bind n6{true, true, false, 0x66, 0x6666666677777777ull, CTL1};
  inject(6, n6, 0x41);
  // "after its read": live change for sink 2 once its record was stored
  CHECK(run_until([&] {
          return count_ops(OP_READ, REC_BASE + 3, 0) >= 1;
        }, 8000),
        "H1 walk reached sink 3 (sink 2 stored)");
  Bind n2{true, false, true, 0x22, 0x2222222233333333ull, CTL2};
  inject(2, n2, 0x42);
  CHECK(run_until([&] { return restore_done(); }, 30000),
        "H2 restore completes around the live changes");
  rstall = 0;
  CHECK(!d->restore_fail_o, "H3 live changes are not a failure");
  CHECK(((d->dbg_touched_o >> 2) & 1) && ((d->dbg_touched_o >> 6) & 1),
        "H4 both live changes marked touched");
  bool pre26 = false;
  for (const Accept& a : accepts)
    if (a.sink == 2 || a.sink == 6) pre26 = true;
  CHECK(!pre26, "H5 a changed sink is never preloaded (ordering)");
  CHECK(accepts.size() == 6, "H6 the six unchanged sinks preload (got %zu)",
        accepts.size());
  for (const Accept& a : accepts) {
    if (a.sink >= 0 && a.sink < N_SINKS && a.sink != 2 && a.sink != 6) {
      CHECK(a.b == hv[a.sink], "H7 sink %d preload fields exact", a.sink);
    }
  }
  CHECK(run_until([&] {
          return count_ops(OP_WRITE, REC_BASE + 2) >= 1
              && count_ops(OP_WRITE, REC_BASE + 6) >= 1
              && !d->dbg_dirty_o;
        }, 6000),
        "H8 the live changes flush after the restore");
  CHECK(store_match(2, frame(uint8_t(REC_BASE + 2), payload_of(n2))),
        "H9 sink 2 NVM ends at the LIVE value, not the restored one");
  CHECK(store_match(6, frame(uint8_t(REC_BASE + 6), payload_of(n6))),
        "H10 sink 6 NVM ends at the LIVE value, not the restored one");
}

// ============ I: change DURING the flush of its own record (taint path)
void Harness::check_a_change_during_its_own_flush_reserializes() {
  size_t wr_before = size_t(count_ops(OP_WRITE, REC_BASE + 5));
  Bind i5{true, false, false, 0x51, 0x5151515152525252ull, CTL1};
  inject(5, i5, 0x51);
  CHECK(run_until([&] {
          return size_t(count_ops(OP_WRITE, REC_BASE + 5)) > wr_before;
        }, 4000),
        "I0 flush of sink 5 starts");
  Bind i5b = i5; i5b.started = true; i5b.uid = 0x52;  // land mid-serialization
  inject(5, i5b, 0x52);
  CHECK(run_until([&] { return d->dbg_dirty_o == 0; }, 6000),
        "I1 the tainted commit re-serializes until clean");
  run(200);
  CHECK(store_match(5, frame(uint8_t(REC_BASE + 5), payload_of(i5b))),
        "I2 NVM converges to the NEWEST value after a mid-flush change");
  CHECK(count_ops(OP_WRITE, REC_BASE + 5) >= int(wr_before) + 2,
        "I3 the stale image was re-committed, not trusted");
}

// ===================== X: dbg_dirty_o IS the unflushed-state contract
// protocol_processor_top publishes this vector as nvm_unflushed_o (issue
// #90) and an integrator ORs it into a "saved state pending" bit, so the
// three edges the pin promises are graded here, at the source, cycle by
// cycle: it rises when a change is ACCEPTED (a capture whose persisted set
// differs), it never drops before that change is committed with done, and
// on retry exhaustion it drops on the SAME cycle the sticky alarm rises —
// never silently. The suite's earlier groups sample the vector at rest;
// what a pending bit needs is the span between those samples.
void Harness::check_the_unflushed_export_contract() {
  for (int k = 0; k < N_SINKS; ++k) seed_region(k, {});
  reset();
  go();
  CHECK(run_until([&] { return restore_done(); }, 5000),
        "X0 the walk that puts the manager in RUN completed");
  CHECK(d->dbg_dirty_o == 0, "X0b nothing unflushed before the change");

  // X1: a change is TAKEN -> exactly that sink reads unflushed
  Bind x3{true, true, false, 9, TK_A, CTL2};
  const size_t wr_before = size_t(count_ops(OP_WRITE, REC_BASE + 3));
  inject(3, x3, 0x31);
  CHECK(run_until([&] { return d->dbg_dirty_o != 0; }, 20),
        "X1 the accepted change raises the unflushed vector");
  CHECK(d->dbg_dirty_o == (1u << 3),
        "X1b only the changed sink reads unflushed (0x%02x)",
        unsigned(d->dbg_dirty_o));

  // X2: it HOLDS through the debounce and the burst, and only the commit's
  //     done clears it. Sampled every cycle, so a pin that pulsed, or that
  //     cleared when the burst started, fails here and not by luck of when
  //     the other groups happen to look.
  bool on_done = false;
  bool cleared = false;
  for (int i = 0; i < 4000 && !cleared; ++i) {
    //! the manager-face completion AS THIS CYCLE PRESENTS IT: the bit the
    //! shadow clears on it only reads 0 after the edge below
    const bool done_this_cycle = d->dbg_port_done_o != 0;
    tick();
    if (!(d->dbg_dirty_o & (1u << 3))) {
      cleared = true;
      on_done = done_this_cycle;
    }
  }
  CHECK(cleared && size_t(count_ops(OP_WRITE, REC_BASE + 3)) > wr_before,
        "X2 the change was committed and stopped reading unflushed");
  CHECK(on_done,
        "X3 the unflushed bit falls on the commit's done, not before it");
  CHECK(store_match(3, frame(uint8_t(REC_BASE + 3), payload_of(x3))),
        "X3b the record that cleared the bit is byte-exact");

  // X4: retries exhausted -> the bit drops, and NEVER without the alarm.
  //     The two are graded on the same cycle: a pin that cleared on the
  //     give-up while the alarm was still low would lose the change with
  //     nothing left to report it.
  Bind x5{true, false, true, 10, TK_B, CTL1};
  arm_err(OP_WRITE, REC_BASE + 5, -1, -1, 100);   // fail every WRITE
  inject(5, x5, 0x32);
  CHECK(run_until([&] { return (d->dbg_dirty_o >> 5) & 1; }, 20),
        "X4 the change that will be given up reads unflushed first");
  bool alarm_at_drop = false;
  bool dropped = false;
  for (int i = 0; i < 8000 && !dropped; ++i) {
    tick();
    if (!((d->dbg_dirty_o >> 5) & 1)) {
      dropped = true;
      alarm_at_drop = d->alarm_o != 0;
    }
  }
  CHECK(dropped, "X5 the given-up change stops reading unflushed");
  CHECK(alarm_at_drop,
        "X5b the give-up raises alarm_o on the cycle it clears the bit");
  disarm_err();
}

int Harness::report() {
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int Harness::run_suite() {
  check_empty_boot_reports_blank();
  check_capture_debounce_and_write_through();
  check_volatile_only_churn_costs_no_traffic();
  check_unbind_capture_commits();
  check_bounded_commit_retry_and_the_alarm();
  check_boot_replay_from_a_seeded_image();
  check_a_torn_readback_aborts_the_whole_restore();
  check_a_change_during_restore_wins();
  check_a_change_during_its_own_flush_reserializes();
  check_the_unflushed_export_contract();
  return report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Harness h;
  return h.run_suite();
}

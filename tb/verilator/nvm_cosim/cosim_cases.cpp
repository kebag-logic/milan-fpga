// SPDX-License-Identifier: CERN-OHL-W-2.0
// The saved-state co-simulation: the case scripts. STIMULUS ONLY. Every
// verdict is taken by run_cases.py, which decodes the dumped journal slots
// with the repository's own scripts/nvm_klj2.py and compares them with
// records it frames itself; nothing in this file grades anything.
//
// PRODUCER, per case (the tag after the name): "real" = the pinned donor
// KL_acmp_nvm_shadow and KL_pp_nvm_port behind a listener-capture BFM, with
// the donor's own 500 ms debounce and two retries; "bfm" = the device-face
// BFM, used only for orderings the donor manager does not produce on demand;
// "unit" = no firmware at all, the control face driven by this file.
#include "cosim_bridge.h"

#include <algorithm>
#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <functional>
#include <map>
#include <sstream>
#include <string>
#include <vector>

extern "C" {
#include "nvm_host.h"
}

using namespace cosim;

namespace {

struct Rec {
  unsigned id, off, len;
};
std::map<unsigned, Rec> recs;
std::string out_dir;
unsigned img_len = 0;

// ----------------------------------------------------------------- framing
uint16_t crc16(const std::vector<uint8_t> &d) {
  uint16_t c = 0xFFFF;
  for (uint8_t b : d) {
    c ^= uint16_t(b) << 8;
    for (int i = 0; i < 8; ++i) c = (c & 0x8000) ? uint16_t((c << 1) ^ 0x1021) : uint16_t(c << 1);
  }
  return c;
}

//! an F07.8 frame, layout_version 2, as the donor port expects it
std::vector<uint8_t> frame(unsigned rid, const std::vector<uint8_t> &pl) {
  std::vector<uint8_t> f = {0x17, 0x22, 0x02, uint8_t(rid), uint8_t(pl.size() >> 8),
                            uint8_t(pl.size())};
  std::vector<uint8_t> cov = f;
  cov.insert(cov.end(), pl.begin(), pl.end());
  const uint16_t c = crc16(cov);
  f.push_back(uint8_t(c >> 8));
  f.push_back(uint8_t(c));
  f.insert(f.end(), pl.begin(), pl.end());
  return f;
}

std::vector<uint8_t> bind_frame(const Binding &b) {
  std::vector<uint8_t> pl = {uint8_t(b.bound | (b.started << 1) | (b.sw << 2)), 0,
                             uint8_t(b.uid >> 8), uint8_t(b.uid)};
  for (int i = 7; i >= 0; --i) pl.push_back(uint8_t(b.teid >> (8 * i)));
  for (int i = 7; i >= 0; --i) pl.push_back(uint8_t(b.ceid >> (8 * i)));
  return frame(0x20 + b.sink, pl);
}

// X's controller id ends in 0xFF, so an ERASE failing on the record's LAST
// byte leaves the whole span 0xFF: the manager's round-1 counterexample
const Binding X{0, 1, 1, 0, 1, 0x1122334455667788ull, 0x99aabbccddeeffffull};
const Binding X2{0, 1, 0, 0, 1, 0x1122334455667788ull, 0x99aabbccddeeffffull};
const Binding X3{0, 1, 1, 1, 3, 0x2122232425262728ull, 0x99aabbccddeeffffull};
const Binding Z{1, 1, 1, 0, 2, 0x0102030405060708ull, 0x1112131415161718ull};
const Binding Z2{1, 1, 0, 0, 2, 0x0102030405060708ull, 0x1112131415161718ull};
const Binding Z3{1, 1, 1, 1, 4, 0x3132333435363738ull, 0x1112131415161718ull};

const std::vector<uint8_t> FMT_A = {0x00, 0xA0, 0x02, 0x01, 0x00, 0x40, 0x00, 0x08};
const std::vector<uint8_t> FMT_B = {0x00, 0xA0, 0x02, 0x02, 0x00, 0x40, 0x00, 0x08};

unsigned off_of(unsigned rid) {
  auto it = recs.find(rid);
  if (it == recs.end()) fatal("record id not in the table");
  return it->second.off;
}

// ---------------------------------------------------------------- observing
std::string hex64(uint64_t v) {
  char b[24];
  std::snprintf(b, sizeof b, "0x%016" PRIx64, v);
  return b;
}

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
  o << "OBS {\"tag\":\"" << tag << "\",\"cycle\":" << cyc
    << ",\"ms\":" << (c.now_ns / 1000000ull)
    << ",\"stat\":" << csr_peek(3) << ",\"capid\":" << csr_peek(5)
    << ",\"backed\":" << l.backed << ",\"dirty_pub\":" << l.dirty_pub
    << ",\"stale\":" << l.stale << ",\"pend\":" << l.pend << ",\"unres\":" << l.unres
    << ",\"verdict\":" << l.verdict << ",\"img_valid\":" << l.img_valid
    << ",\"alarm\":" << l.alarm << ",\"mgr_dirty\":" << l.mgr_dirty
    << ",\"port_busy\":" << l.port_busy << ",\"dev_busy\":" << l.dev_busy
    << ",\"restore_done\":" << l.restore_done << ",\"restore_fail\":" << l.restore_fail
    << ",\"blank\":" << l.blank << ",\"dyn_dirty\":" << l.dyn_dirty
    << ",\"dyn_fmt0\":\"" << hex64(l.dyn_fmt0) << "\",\"dyn_fmt0_v\":" << l.dyn_fmt0_v
    << ",\"erases\":" << c.erases << ",\"programs\":" << c.programs
    << ",\"hb\":" << c.hb << ",\"hb_max_gap_ms\":" << (c.hb_max_gap_ns / 1000000ull)
    << ",\"losses\":" << evlog.loss_cycles.size() << ",\"bad101\":" << evlog.bad101
    << ",\"mem_accepts\":" << evlog.mem_accepts << ",\"mem_errs\":" << evlog.mem_errs
    << ",\"own\":[";
  for (unsigned w = 0; w < 8; ++w) o << (w ? "," : "") << csr_peek(8 + w);
  o << "],\"preloads\":[";
  for (size_t i = 0; i < preloads.size(); ++i) {
    const auto &p = preloads[i];
    o << (i ? "," : "") << "{\"sink\":" << p.sink << ",\"teid\":\"" << hex64(p.teid)
      << "\",\"uid\":" << p.uid << ",\"ceid\":\"" << hex64(p.ceid) << "\",\"sw\":" << p.sw
      << ",\"started\":" << p.started << "}";
  }
  o << "]}";
  std::printf("%s\n", o.str().c_str());
  std::fflush(stdout);
}

void dump_log() {
  for (const auto &r : evlog.ops)
    std::printf("EVT {\"k\":\"op\",\"src\":\"%s\",\"op\":%u,\"rid\":%u,\"req\":%" PRIu64
                ",\"gnt\":%" PRIu64 ",\"end\":%" PRIu64 ",\"res\":\"%s\",\"bytes\":%u}\n",
                r.bfm ? "bfm" : "port", r.op, r.rid, r.req, r.gnt, r.end, r.res.c_str(),
                r.bytes);
  for (const auto &s : evlog.strobes)
    std::printf("EVT {\"k\":\"strobe\",\"cyc\":%" PRIu64 ",\"v\":%u,\"stray\":%d}\n", s.cyc,
                s.value, s.stray ? 1 : 0);
  for (const auto &h : evlog.hooks)
    if (h.name != "s_hb" && h.name != "f_rdsr" && h.name != "r_stat")
      std::printf("EVT {\"k\":\"hook\",\"name\":\"%s\",\"n\":%u,\"cyc\":%" PRIu64 ",\"v\":%u}\n",
                  h.name.c_str(), h.n, h.cyc, h.value);
  for (uint64_t c : evlog.loss_cycles)
    std::printf("EVT {\"k\":\"loss\",\"cyc\":%" PRIu64 "}\n", c);
}

// ---------------------------------------------------------------- stepping
void idle(uint64_t ms) { host_idle_ms(ms); }
void quiet(uint64_t ms) { host_quiet_ms(ms); }

bool idle_until(const std::function<bool()> &p, uint64_t max_ms) {
  for (uint64_t i = 0; i < max_ms; ++i) {
    if (p()) return true;
    host_idle_ms(1);
  }
  return p();
}

void on_next(const std::string &name, std::function<void()> fn) {
  at(name, hooks(name) + 1, std::move(fn));
}

void boot() {
  host_boot();
  idle(30);
  snap("boot");
}

void fault(unsigned rid, unsigned byte, int mode, int kind, int count = -1, int delay = 0) {
  faults.push_back(Fault{off_of(rid) + byte, mode, kind, count, delay});
}

bool port_quiet() {
  const Levels l = levels();
  return !l.port_busy && !l.mgr_dirty && !l.dev_busy;
}

//! the firmware is held at this point while the RTL runs until the real
//! manager has flushed everything it holds
void flush_now() {
  // the capture reaches the manager's dirty bit two edges after the pulse:
  // wait for the manager to TAKE the change, then for it to flush it
  if (!run_until([] { return levels().mgr_dirty != 0 || levels().port_busy != 0; }, 100))
    fatal("the manager did not take the change");
  if (!run_until(port_quiet, 2000000)) fatal("the manager did not flush");
}

//! the base state: X and Z bound through the real manager, committed once
void base() {
  boot();
  bind(X);
  bind(Z);
  idle(2200);
  snap("base");
}

//! the identity-wrap arm's TAIL (`--commits`): `n` further committing
//! changes, run AFTER the case body and all of its observations, so a case
//! graded without the tail is graded exactly as before. The backend counts
//! one capture identity per ACCEPTED ARM, and the contract's MINIMUM width
//! is 2 bits (KL_nvm_backend.sv, g_refuse_capid), so the identity reaches 0
//! on the FOURTH accepted arm -- which most cases here never take on their
//! own. The bindings ALTERNATE on one record because the manager takes a
//! CHANGE and re-binding the same value is not one.
void commit_tail(unsigned n) {
  for (unsigned i = 0; i < n; ++i) {
    const unsigned want = hooks("s_ack") + 1;
    bind((i % 2u) ? X2 : X);
    // BOUNDED, and it must be: a commit the flash refuses never acknowledges
    // and the tail must not hang waiting for it. The arm compares one case
    // with ITSELF across two identity widths, so a commit that does not land
    // does not land at either width.
    idle_until([want] { return hooks("s_ack") >= want; }, 8000);
    idle(200);
  }
}

void bfm_erase(unsigned rid) { bfm(BfmOp{2, rid, {}, 0, 0}); }

void bfm_write(unsigned rid, const std::vector<uint8_t> &f, int stop = -1, int pace = 0) {
  BfmOp op{1, rid, f, 0, uint16_t(f.size())};
  op.stop_after = stop;
  op.pace = pace;
  bfm(op);
}

bool bfm_done() { return bfm_idle() && !levels().dev_busy; }

//! the most recent device operation is the real port's ERASE of `rid`, and
//! it has just completed
bool port_erase_done(unsigned rid) {
  if (evlog.ops.empty()) return false;
  const auto &o = evlog.ops.back();
  return !o.bfm && o.op == 2 && o.rid == rid && o.end != 0;
}

//! the most recent device operation is the real port's `op` on `rid`,
//! granted (operations are recorded at their grant)
bool port_op_granted(unsigned rid, unsigned op) {
  if (evlog.ops.empty()) return false;
  const auto &o = evlog.ops.back();
  return !o.bfm && o.op == op && o.rid == rid;
}

void bfm_run() {
  if (!run_until(bfm_done, 2000000)) fatal("the BFM operation did not end");
}

uint32_t ack_word(uint32_t id) { return 0x2u | (id << 16); }

//! unit cases: the control face configured by hand, exactly as the writer
//! configures it, with no firmware running. The RE-BASE: base, length and
//! the channel-map tables (every record reads open; the load flag arms).
void unit_rebase() {
  cosim_rtl_csr_write(0, uint32_t(uintptr_t(cosim::area())));
  unsigned len = 0;
  for (auto &r : recs) len = std::max(len, r.second.off + r.second.len);
  cosim_rtl_csr_write(1, (len + 3u) & ~3u);
  unsigned pi = 0, po = 0;
  for (auto &r : recs) {
    if (r.first >= 0x60 && r.first < 0x70) {
      cosim_rtl_csr_write(0x20 | (r.first - 0x60), (r.second.len << 16) | pi);
      pi += r.second.len;
    }
    if (r.first >= 0x70 && r.first < 0x80) {
      cosim_rtl_csr_write(0x30 | (r.first - 0x70), (r.second.len << 16) | po);
      po += r.second.len;
    }
  }
  host_catch_up();
}

void unit_configure() {
  unit_rebase();
  cosim_rtl_csr_write(3, 0x10u);   // validated, VD_OK
  cosim_rtl_csr_write(4, 0x40u);   // reload (no such strobe on the tracked module)
  cosim_rtl_csr_write(4, 0x1u);    // heartbeat
  host_catch_up();
}

//! what a writer's window load does to one record: its framed bytes,
//! written straight into the live record area by the CPU
void load_record(unsigned rid, const std::vector<uint8_t> &f) {
  std::memcpy(cosim::area() + off_of(rid), f.data(), f.size());
}

//! the record's bytes in the live record area, as a hex string
std::string live_hex(unsigned rid) {
  const auto it = recs.find(rid);
  if (it == recs.end()) fatal("record id not in the table");
  std::string s;
  char b[4];
  for (unsigned i = 0; i < it->second.len; ++i) {
    std::snprintf(b, sizeof b, "%02x", cosim::area()[it->second.off + i]);
    s += b;
  }
  return s;
}

//! the writer's restart: appended by run_cases.py to the HOST build of a
//! writer that carries the contract (a CPU-only reset returns every static of
//! the writer to its initial value and runs its boot again); absent from a
//! pre-contract writer, which has no re-attach path to model
extern "C" void nvm_host_writer_restart(void) __attribute__((weak));

std::map<std::string, std::function<void()>> cases;

static void acknowledgement_cases_1() {
  // A. ACKNOWLEDGEMENT IDENTITY AND ORDERING --------------------------------
  cases["A1_stable_no_change"] = [] {                            // real
    base();
    idle(20000);
    snap("end");
  };
  cases["A2_write_between_verify_and_ack"] = [] {                // real, #418
    boot();
    bind(X);
    bind(Z);
    // the first commit's post-verify sequence store: the firmware is held
    // there while the real manager debounces and flushes a newer binding
    on_next("w_seq", [] {
      note("hook_w_seq", 1);
      bind(X2);
      flush_now();
    });
    idle_until([] { return hooks("s_ack") >= 1; }, 6000);
    idle(50);
    snap("post_ack");
    idle(5000);
    snap("end");
  };
  cases["A3_write_done_on_ack_edge"] = [] {                      // bfm, #418 control
    boot();
    bind(X);
    bind(Z);
    on_next("s_ack", [] {
      bfm_erase(0x20);
      bfm_write(0x20, bind_frame(X2));
      // stop with the WRITE's done pulse in the current cycle: the ACK the
      // firmware is about to write is then sampled on the same edge
      if (!run_until(bfm_write_done_now, 200000)) fatal("no WRITE done");
      note("ack_on_done_edge", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 1; }, 6000);
    idle(50);
    snap("post_ack");
    idle(5000);
    snap("end");
  };
  cases["A4_write_after_ack"] = [] {                             // real
    base();
    bind(X2);
    idle(3000);
    snap("end");
  };
  cases["A5_stray_duplicate_ack"] = [] {                         // real + stray ACK
    base();
    bind(X2);
    idle(600);            // flushed into the image; the writer's debounce runs
    const uint32_t id = csr_peek(5);
    note("stray_ack_id", id);
    stray(4, ack_word(id));   // a repeat of the last accepted acknowledgement
    snap("after_stray");
    idle(4000);
    snap("end");
  };
}

static void acknowledgement_cases_2() {
  cases["A6_late_ack_while_new_capture_open"] = [] {             // real + stray ACK
    base();
    bind(X2);
    // after the attestation and before the flash: the capture is open and
    // attested, so an acknowledgement quoting it would be accepted
    on_next("s_start", [] {
      const uint32_t id = csr_peek(5);
      note("open_capture_id", id);
      stray(4, ack_word(id - 1));   // the PREVIOUS capture's acknowledgement
      snap("stray");
    });
    idle(3000);
    snap("end");
  };
  cases["A8_identity_wrap"] = [] {                               // real + stray ACK
    base();                                   // capture 1
    bind(X2);
    idle(2500);                               // capture 2
    bind(X3);
    idle(2500);                               // capture 3
    bind(X);
    idle(2500);                               // capture 4
    bind(X2);                                 // capture 5 follows
    on_next("s_start", [] {
      const uint32_t id = csr_peek(5);
      note("capture5_id", id);
      // an acknowledgement quoting capture 1, arriving after capture 5 is
      // attested and before its slot verifies; the flash then fails
      stray(4, ack_word(1));
      snap("stray");
      host_flash_fail(0, 1, 0);
      on_next("s_release", [] { host_flash_fail(0, 0, 0); });
    });
    idle(6000);
    snap("end");
  };
  cases["A9_updates_during_slow_erase"] = [] {                   // real
    host_flash_erase_ms(3000);
    base();
    bind(X2);
    on_next("f_erase", [] { bind(X3); });  // lands 500 ms into a 3 s erase
    idle(16000);
    snap("end");
  };
  cases["A11_inflight_write_closes_after_arm"] = [] {            // real + bfm
    base();
    bfm_erase(0x21);
    bfm_run();                               // record 0x21 open, not closed
    bind(X2);
    on_next("s_arm", [] {
      // GRANTED BEFORE the arm edge and still in flight at it: a request in
      // the arm's own cycle is deferred since revision b (U4 is that edge)
      bfm_write(0x21, bind_frame(Z2), -1, 20);
      if (!run_until([] { return !evlog.ops.empty() && evlog.ops.back().bfm &&
                                 evlog.ops.back().op == 1 && evlog.ops.back().rid == 0x21; },
                     1000))
        fatal("the WRITE was not granted");
      run_cycles(5);
      note("write_granted_before_arm", evlog.ops.back().gnt);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    snap("first");
    idle(4000);
    snap("end");
  };

  cases["A12_last_byte_before_arm_done_after"] = [] {            // real + bfm
    base();
    bfm_erase(0x21);
    bfm_run();                               // record 0x21 open
    bind(X2);
    on_next("s_arm", [] {
      // the WRITE's last byte is ACCEPTED before the arm edge and completes
      // 300 cycles after it: every byte moved before the arm, the record
      // closes after it
      fault(0x21, 27, 3, 0, 1, 300);
      bfm_write(0x21, bind_frame(Z2));
      if (!run_until([] { return evlog.slow >= 1; }, 200000)) fatal("no slow byte");
      note("last_byte_accepted", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    snap("first");
    idle(4000);
    snap("end");
  };

}

static void acknowledgement_cases() {
  acknowledgement_cases_1();
  acknowledgement_cases_2();
}

static void capture_cases() {
  // B. CAPTURE, ERASE AND FAILED OPERATIONS -------------------------------
  auto erase_fault_case = [](unsigned byte, int kind) {
    return [byte, kind] {                                          // real
      base();
      fault(0x20, byte, 0, kind);      // every attempt fails at this byte
      bind(X2);
      idle(1500);                      // debounce, three attempts, give-up
      snap("gave_up");
      faults.clear();
      bind(Z2);
      idle(3000);
      snap("end");
    };
  };
  cases["B1_erase_error_full_span"] = erase_fault_case(27, 1);
  cases["B2_erase_error_partial_span"] = erase_fault_case(6, 1);
  cases["B3_erase_error_no_byte"] = erase_fault_case(0, 1);
  cases["B4_write_error_after_erase"] = erase_fault_case(0, 2);
  cases["B5_erase_then_no_write_yet"] = [] {                     // real + bfm
    base();
    bfm_erase(0x20);
    bfm_run();                       // the ERASE-to-WRITE gap, held open
    bind(Z2);
    idle(3000);
    snap("gap");
    bfm_write(0x20, bind_frame(X3));
    bfm_run();
    idle(3000);
    snap("end");
  };
  auto seq_case = [](unsigned byte20) {
    return [byte20] {                                             // real + bfm
      base();
      bfm_erase(0x30);
      bfm_write(0x30, frame(0x30, FMT_A));
      bfm_run();
      idle(2500);
      snap("base2");
      fault(0x20, byte20, 0, 1);
      bfm_erase(0x20);                 // fails part-way: record 0x20
      bfm_run();
      faults.clear();
      fault(0x30, 0, 0, 2);
      bfm_erase(0x30);                 // erases, then its WRITE fails: 0x30
      bfm_write(0x30, frame(0x30, FMT_B));
      bfm_run();
      faults.clear();
      bind(Z2);                        // a later record, on the real path
      idle(3000);
      snap("end");
    };
  };
  cases["B6_two_failed_records_partial"] = seq_case(6);
  cases["B6b_two_failed_records_full"] = seq_case(27);
  cases["B10_partial_write_never_closes"] = [] {                 // real + bfm
    base();
    const auto f = bind_frame(X3);
    bfm_erase(0x20);
    bfm_write(0x20, std::vector<uint8_t>(f.begin(), f.begin() + 8));   // header only
    bfm_run();
    bind(Z2);
    idle(3000);
    snap("end");
  };
  cases["B7_first_boot_erased_records"] = [] {                   // real
    boot();
    host_uart("milan_nvm commit");
    snap("blank_commit");
    bind(X);
    idle(3000);
    snap("end");
  };
  cases["B8_first_boot_failed_erase"] = [] {                     // real + bfm
    boot();
    fault(0x20, 0, 0, 1);
    bfm_erase(0x20);
    bfm_run();
    faults.clear();
    bind(Z);
    idle(3000);
    snap("end");
  };
  cases["B9_abandoned_write_stream"] = [] {                      // real + bfm
    base();
    bind(X2);
    idle(700);                       // flushed; the writer's debounce runs
    bfm_erase(0x21);
    bfm_write(0x21, bind_frame(Z2), 10);   // ten bytes, then silence
    idle(4000);
    snap("abandoned");
    bfm_resume();
    idle(4000);
    snap("end");
  };

}

static void hold_cases_1a() {
  // C. THE HOLD, THE ATTESTATION AND THE ROUND-2 CONCERN ----------------------
  cases["C1_request_during_hold_is_deferred"] = [] {             // real + bfm
    base();
    bind(X2);
    on_next("sel_own0", [] {
      bfm_erase(0x21);
      bfm_write(0x21, bind_frame(Z2));
    });
    idle(4000);
    snap("end");
  };
  cases["C2_hold_expiry_then_erase_with_stale_mask"] = [] {      // real + bfm
    base();
    bind(X2);
    // words 0 and 1 are read (record 0x21 reads COMPLETE); the firmware is
    // then held past the hold bound, and an ERASE of 0x21 is granted and
    // completes before it copies
    on_next("sel_own2", [] {
      note("erase_requested", cyc);
      bfm_erase(0x21);               // requested inside the hold: deferred
      stall_ms(60);                  // the hold lapses at 50 ms; it runs
      note("stall_end", cyc);
    });
    // the unattested attempt releases; the next one commits and is acked
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    idle(50);
    snap("after");
    bfm_write(0x21, bind_frame(Z3));
    bfm_run();
    idle(3000);
    snap("end");
  };
  cases["C1r_real_port_request_deferred"] = [] {                 // real
    base();
    bind(X2);
    // the arm lands while the real port collects its header: its ERASE
    // request reaches the backend a few cycles into the hold
    on_next("s_arm", [] {
      bind(Z2);
      if (!run_until([] { return levels().port_busy != 0; }, 2000000)) fatal("no flush");
      note("port_busy_at_arm", cyc);
    });
    idle(4000);
    snap("end");
  };
}

static void hold_cases_1b() {
  cases["C2r_real_port_torn_record_under_stale_mask"] = [] {     // real
    base();
    bind(X2);
    on_next("s_arm", [] {
      // the real manager's ERASE is deferred by the hold; one data byte of
      // its WRITE will complete only 200 ms after acceptance, so the record
      // is TORN while the firmware copies with a stale mask
      fault(0x21, 20, 3, 2, 1, 200000);
      bind(Z2);
      if (!run_until([] { return levels().port_busy != 0; }, 2000000)) fatal("no flush");
    });
    on_next("sel_own2", [] {
      stall_ms(60);                  // the hold lapses; ERASE then WRITE run
      note("stall_end", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    idle(50);
    snap("after");
    idle(4000);
    snap("end");
  };
  cases["C2e_real_port_erased_span_under_stale_mask"] = [] {     // real
    base();
    bind(X2);
    on_next("s_arm", [] {
      // as C2r, but the slow byte is the WRITE's FIRST one: while the
      // firmware copies under its stale mask, record 0x21 is one whole
      // erased span, which the KLJ2 erased-record rule accepts as valid, so
      // no content check can refuse it; only the attestation can
      fault(0x21, 0, 3, 2, 1, 200000);
      bind(Z2);
      if (!run_until([] { return levels().port_busy != 0; }, 2000000)) fatal("no flush");
    });
    on_next("sel_own2", [] {
      stall_ms(60);                  // the hold lapses; ERASE then WRITE run
      note("stall_end", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    idle(50);
    snap("after");
    idle(4000);
    snap("end");
  };
  cases["C1a_real_port_arm_after_erase_done"] = [] {             // real
    base();
    bind(X2);
    // the ARM lands in the real port's ERASE-to-WRITE gap (#420): the
    // manager's ERASE of record 0x21 has completed WITH done, the device
    // face is idle, and the WRITE that completes the logical record is
    // requested on the arm's own edge. Device-idle is not a record boundary.
    on_next("s_arm", [] {
      bind(Z2);
      if (!run_until([] { return port_erase_done(0x21); }, 2000000))
        fatal("no ERASE completion");
      note("erase_done_before_arm", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    idle(50);
    snap("after");
    idle(4000);
    snap("end");
  };
}

static void hold_cases_1() {
  hold_cases_1a();
  hold_cases_1b();
}

static void hold_cases_2() {
  cases["C1g_real_port_copy_inside_erase_write_gap"] = [] {      // real
    base();
    bind(X2);
    // The capture reads ownership while the real port sits in its
    // ERASE-to-WRITE gap (#420): the manager's ERASE of record 0x21 is
    // GRANTED BEFORE the arm (an already-granted logical write), completes
    // WITH done inside the capture, and the WRITE that completes the record
    // is deferred by the hold. The device face is idle and the record is one
    // erased span, a valid KLJ2 record by content: only its open bit says the
    // logical record is not complete.
    on_next("s_arm", [] {
      bind(Z2);
      if (!run_until([] { return port_op_granted(0x21, 2); }, 2000000))
        fatal("no ERASE grant");
      note("erase_granted_before_arm", cyc);
    });
    on_next("sel_own0", [] {
      if (!run_until([] { return port_erase_done(0x21); }, 200000))
        fatal("no ERASE completion");
      run_cycles(20);                // the WRITE request is up, and held
      note("gap_observed", cyc);
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 6000);
    idle(50);
    snap("after");
    idle(4000);
    snap("end");
  };
  cases["C3_hold_expiry_without_producer"] = [] {                // real
    base();
    bind(X2);
    on_next("sel_own2", [] { stall_ms(60); });
    idle(2500);
    snap("end");
  };
  cases["C5_concurrent_arm_refused"] = [] {                      // real + stray ARM
    base();
    bind(X2);
    on_next("sel_own0", [] {
      note("capid_before_stray", csr_peek(5));
      stray(4, 0x8u);
      snap("stray");
    });
    idle(3000);
    snap("end");
  };
  cases["C7_late_ack_after_commit_deadline"] = [] {              // real
    base();
    bind(X2);
    on_next("w_seq", [] {
      stall_ms(8200);
      on_next("s_hb", [] { snap("pre_hb"); });
    });
    idle_until([] { return hooks("s_ack") >= 2; }, 14000);
    idle(4000);
    snap("end");
  };
  cases["C8_ack_refused_after_verified_slot"] = [] {             // real + stray RELEASE
    base();
    bind(X2);
    on_next("w_seq", [] {
      stray(4, 0x20u);
      on_next("s_hb", [] { snap("pre_hb"); });
    });
    idle(4000);
    snap("end");
  };

}

static void hold_cases() {
  hold_cases_1();
  hold_cases_2();
}

static void liveness_cases() {
  // D. LIVENESS, DEADLINES AND THE FOUR MEMORY OUTCOMES ----------------------
  cases["D1_writer_loss_and_recovery"] = [] {                    // real
    base();
    quiet(2500);
    snap("lost");
    idle(1000);
    snap("back");
    bind(X2);
    idle(700);
    quiet(2500);
    snap("lost2");
    idle(3500);
    snap("end");
  };
  auto stuck_case = [](int mode) {
    return [mode] {                                               // real
      base();
      bind(X2);
      idle(700);
      fault(0x21, 0, mode, 2, mode == 1 ? 1 : -1);
      bind(Z2);                        // its WRITE's first byte never completes
      idle(3500);
      snap("stuck");
    };
  };
  cases["D4c_accepted_write_silent"] = stuck_case(1);
  cases["D4d_readiness_withheld"] = stuck_case(2);
  cases["D4e_silent_inside_capture"] = [] {                      // real
    base();
    bind(X2);
    on_next("s_arm", [] {
      fault(0x21, 0, 1, 2, 1);
      bind(Z2);
      if (!run_until([] { return evlog.silent >= 1; }, 2000000)) fatal("no silent write");
    });
    idle(3500);
    snap("stuck");
  };

}

static void producer_cases() {
  // E. PRODUCER-HELD AND UNMATERIALISED CHANGES (#420) -------------------------
  cases["E1_dyn_change_ack_then_second_change"] = [] {           // real dyn store
    boot();
    dyn_write(3, 0, 0x101);            // SET_STREAM_FORMAT, STREAM_INPUT 0
    idle(3000);
    snap("first");
    dyn_write(3, 0, 0x202);            // a second change, the level still high
    idle(3000);
    snap("end");
  };
  cases["E3_binding_inside_manager_debounce"] = [] {             // real
    base();
    bind(X2);
    idle(100);
    snap("in_debounce");
    idle(3000);
    snap("end");
  };

}

static void revocation_cases() {
  // F. REVOCATION CAUSES OF SECTION 9.2 ----------------------------------------
  cases["F2_reported_flash_failure"] = [] {                      // real
    base();
    host_flash_fail(1, 0, 0);
    bind(X2);
    idle(1800);
    snap("failed");
    host_flash_fail(0, 0, 0);
    idle(9000);
    snap("end");
  };

  cases["F3_flash_absent_producer_unblocked"] = [] {              // real
    base();
    host_flash_fail(0, 1, 0);          // every page program hangs: no media
    bind(X2);
    idle(2500);
    bind(Z2);
    idle(2500);
    bind(X3);
    idle(2500);
    snap("end");
  };

}

static void unit_cases_1() {
  // U. UNIT CASES: THE CONTROL FACE ALONE ---------------------------------------
  cases["U1_post_reset_ack"] = [] {                               // unit
    unit_configure();
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X));
    bfm_run();
    reset_rtl();
    unit_configure();
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X2));
    bfm_run();
    stray(4, ack_word(1));             // an acknowledgement from before the reset
    snap("after");
  };
  cases["U2_close_on_arm_edge"] = [] {                            // unit
    unit_configure();
    bfm_erase(0x21);
    bfm_run();
    bfm_write(0x21, bind_frame(Z));
    if (!run_until(bfm_write_done_now, 200000)) fatal("no WRITE done");
    stray(4, 0x8u);                    // ARM on the completion's edge
    stray(4, 0x10u);                   // attest
    stray(4, ack_word(csr_peek(5)));   // acknowledge that capture
    snap("acked");
  };
  cases["U3_grant_on_attest_edge"] = [] {                        // unit
    unit_configure();
    stray(4, 0x8u);                    // ARM: the hold is on
    bfm_erase(0x21);                   // requested, deferred
    run_cycles(1000);
    note("deferred_while_hold", levels().dev_busy);
    if (!run_until([] { return ((csr_peek(3) >> 17) & 1u) == 0; }, 200000))
      fatal("hold never lapsed");
    // the next edge grants the deferred ERASE: attest on that same edge
    stray(4, 0x10u);
    snap("attest");
  };
  cases["U4_grant_request_on_arm_edge"] = [] {                   // unit
    // Both reviews' ordering: a mutating request on a CLOSED record rises
    // in the ARM's own cycle. It must be deferred like any request inside
    // the hold, so no operation runs in a capture whose vector reads the
    // record closed.
    unit_configure();
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X));
    bfm_run();                               // record 0x20 CLOSED, committable
    bfm_erase(0x20);                         // its request rises on the next edge...
    stray(4, 0x8u);                          // ...which is the ARM's own edge
    note("arm_cycle", evlog.strobes.back().cyc);
    snap("arm");                             // the first cycle after the arm edge
    run_cycles(300);                         // longer than the whole ERASE takes
    stray(4, 0x10u);                         // ATTEST
    snap("attest");
    bfm_run();                               // the deferred ERASE runs after it
    stray(4, ack_word(csr_peek(5)));
    snap("acked");
  };
}

static void unit_cases_2() {
  cases["U5_reload_refused_inflight_at_rebase"] = [] {           // unit
    // Before the boot load is declared: an ERASE of 0x20 is granted, is
    // still writing when the image is re-based, and ends in err without
    // done after the writer's load of X. No grant follows the re-base, so
    // only the in-flight term can refuse the RELOAD.
    unit_rebase();
    fault(0x20, 10, 3, 1, 1, 400);           // byte 10 completes 400 cycles late
    fault(0x20, 27, 0, 1);                   // the last byte fails: err, no done
    bfm_erase(0x20);
    if (!run_until([] { return evlog.slow >= 1; }, 200000)) fatal("no slow byte");
    note("dev_busy_at_rebase", levels().dev_busy);
    cosim_rtl_csr_write(0, uint32_t(uintptr_t(cosim::area())));   // re-base, ERASE in flight
    load_record(0x20, bind_frame(X));        // the writer's load
    bfm_run();                               // the ERASE goes on over the load, then errs
    faults.clear();
    cosim_rtl_csr_write(3, 0x10u);
    stray(4, 0x40u);                         // RELOAD
    snap("after");
  };
  cases["U6_reload_refused_after_boot"] = [] {                   // unit
    unit_configure();                        // the boot load, accepted
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X));
    bfm_run();                               // 0x20 closed: committable work
    // (a) review probe P5: the ERASE-to-WRITE gap, then a RELOAD, no re-base
    bfm_erase(0x21);
    bfm_run();                               // 0x21 erased, open, device idle
    stray(4, 0x40u);
    snap("gap");
    // (b) review probe P3: a RELOAD with a whole-record WRITE in flight
    bfm_write(0x21, bind_frame(Z), -1, 50);
    run_cycles(40);
    note("dev_busy_at_reload", levels().dev_busy);
    stray(4, 0x40u);
    snap("inflight");
    bfm_run();                               // 0x21 closes: committable work
    // (c) a window load after the boot, over held work: a re-base with
    //     nothing in flight and no grant after it, the load of the older
    //     binding, a RELOAD. Only the once-per-reset rule can refuse it.
    cosim_rtl_csr_write(0, uint32_t(uintptr_t(cosim::area())));
    load_record(0x20, bind_frame(X2));
    stray(4, 0x40u);
    snap("reload");
  };
  cases["U7_reset_row_and_pre_reset_ack"] = [] {                 // unit
    unit_configure();
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X));
    bfm_run();
    stray(4, 0x8u);                          // capture 1
    stray(4, 0x10u);                         // attested
    note("pre_reset_id", csr_peek(5));
    reset_rtl();
    snap("reset");                           // the reset row
    stray(4, ack_word(1));                   // the pre-reset ACK, nothing configured yet
    snap("early_ack");
    unit_configure();                        // the post-reset boot load
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X2));
    bfm_run();                               // post-reset work, committable
    stray(4, ack_word(1));                   // the pre-reset ACK before any post-reset ARM
    snap("after");
  };

}

static void unit_cases() {
  unit_cases_1();
  unit_cases_2();
}

static void load_cases_1() {
  // R. THE LOAD WITH THE REAL WRITER (revision b) ------------------------------
  cases["R1_reload_after_failed_erase"] = [] {                   // real + bfm, slots preloaded
    // The reviewers' ordering, on the slots of an A1 run (slot A: X in
    // record 0x20). Between the writer's window load and its RELOAD strobe
    // an ERASE of 0x20 blanks the whole span and ends in err without done
    // (the round-1 shape). The backend refuses that RELOAD; the writer
    // re-bases and loads again; a later change commits.
    on_next("s_reload", [] {
      fault(0x20, 27, 0, 1);
      bfm_erase(0x20);
      bfm_run();
      faults.clear();
      note("own1_before_reload", csr_peek(9));
    });
    boot();
    bind(Z2);
    idle(3000);
    snap("end");
  };
  cases["U8_grant_on_rebase_edge"] = [] {                       // unit
    // Revision c, the fourth same-edge rule EXECUTED (the other reviewer's
    // probe as offered). A mutating request rises so that its grant lands
    // on the edge of the LAST re-base write: nothing is in flight at that
    // edge, so only the grant-wins-over-re-base PRIORITY can keep the load
    // flag clear. The ERASE then blanks the record the writer has just
    // loaded and ends in err without a done pulse.
    unit_rebase();
    fault(0x20, 27, 0, 1);                   // the last byte fails: err, no done
    bfm_erase(0x20);                         // its request rises on the next edge...
    note("rebase_cycle", cyc);
    cosim_rtl_csr_write(0, uint32_t(uintptr_t(cosim::area())));   // ...the re-base's
    load_record(0x20, bind_frame(X));        // the writer's load
    bfm_run();                               // the ERASE blanks it and errs
    faults.clear();
    cosim_rtl_csr_write(3, 0x10u);
    stray(4, 0x40u);                         // RELOAD
    snap("after");
  };
  cases["U10_arm_refused_while_request_deferred"] = [] {        // unit
    // Revision c, the hold's bound ACROSS captures. A mutating request
    // deferred by one capture may not be deferred by the next: an ARM in
    // the cycle the first hold drops is REFUSED and the waiting request
    // takes that cycle's grant, so no chain of captures can extend one
    // request's wait past T_HOLD_MS_P.
    unit_configure();
    bfm_erase(0x20);
    bfm_write(0x20, bind_frame(X));
    bfm_run();                               // record 0x20 closed
    stray(4, 0x8u);                          // capture 1: the hold is on
    bfm_erase(0x21);                         // requested inside the hold: deferred
    run_cycles(20000);                       // 20 ms into the hold
    note("dev_busy_in_hold", levels().dev_busy);
    stray(4, 0x20u);                         // RELEASE inside the hold
    stray(4, 0x8u);                          // ARM on the very next edge
    note("arm2_cycle", evlog.strobes.back().cyc);
    snap("arm2");
    bfm_run();                               // the deferred ERASE runs
    snap("end");
  };
  cases["U9_four_window_loads_refused"] = [] {                  // real + bfm, slots of A1
    // Revision c: the TERMINAL state of section 5.3, executed. Every one of
    // the writer's four window loads meets an ERASE of 0x20 that blanks the
    // span and ends in err without done, between the load and its RELOAD.
    // The boot ends with the window unvalidated, the restore walk blind and
    // the writer retired; a controller change after it is reported, never
    // read durable, and no slot is touched.
    for (unsigned k = 1; k <= 4; ++k)
      at("s_reload", hooks("s_reload") + k, [] {
        fault(0x20, 27, 0, 1);
        bfm_erase(0x20);
        bfm_run();
        faults.clear();
      });
    boot();                                  // snap("boot"): the terminal row
    bind(Z2);                                // a controller change on the live entity
    idle(3000);                              // longer than T-NVM-WRITER-ALIVE
    snap("end");
  };
}

static void load_cases_2() {
  cases["W2_restart_after_refused_loads"] = [] {                // real, writer restart model
    // Revision c: the composition the re-review found. Four refused window
    // loads, the entity live, a controller change accepted, then a WRITER
    // RESTART WITHOUT A FABRIC RESET. The restarted writer must not take
    // the cold-boot path over the live window: the window went live at the
    // restore walk, so the boot load is over and the writer re-attaches,
    // which keeps the change owned until a slot holds it.
    if (!nvm_host_writer_restart) {          // only a contract writer has it
      on_next("no_restart_model", [] {});
      return;
    }
    for (unsigned k = 1; k <= 4; ++k)
      at("s_reload", hooks("s_reload") + k, [] {
        fault(0x20, 27, 0, 1);
        bfm_erase(0x20);
        bfm_run();
        faults.clear();
      });
    boot();
    bind(Z2);
    idle(600);
    snap("live");
    nvm_host_writer_restart();
    snap("restarted");
    idle(6000);
    snap("end");
  };
  // REVISION D: NO CAPTURE WITHOUT AN ACCEPTED LOAD ---------------------------
  cases["U11_arm_refused_without_accepted_load"] = [] {          // unit
    // The new term, alone. The control face is re-based and VALIDATED
    // exactly as a writer validates it, but no RELOAD is ever accepted: a
    // mutating grant clears the load flag before the strobe, and a second
    // grant takes the window live. A writer that ignores the rule and arms
    // anyway -- revision c's re-attach is one -- is refused by the
    // backend's own flag and not by its own claim, so no capture opens, no
    // identity advances and an acknowledgement retires nothing.
    unit_rebase();
    bfm_erase(0x20);                         // the bracket's one grant
    bfm_run();
    cosim_rtl_csr_write(3, 0x10u);           // the writer's claim: validated
    stray(4, 0x40u);                         // RELOAD: refused, the flag is clear
    snap("refused");
    bfm_erase(0x21);                         // a grant the load did not bracket:
    bfm_write(0x21, bind_frame(Z));          // the window GOES LIVE, and this
    bfm_run();                               // whole-record WRITE closes 0x21
    snap("live");
    stray(4, 0x8u);                          // ARM: refused, no accepted load
    snap("stray");
    stray(4, 0x10u);                         // ATTEST over no capture
    stray(4, ack_word(1));                   // an ACK quoting capture 1
    snap("end");
  };
  cases["U12_window_live_stops_the_repeat"] = [] {               // real + bfm, slots of A1
    // Revision d, the writer half: one disturbed attempt of TWO grants, the
    // ordinary shape of a real record update (ERASE then WRITE). The second
    // grant meets a clear load flag, so the window goes live and no later
    // RELOAD can be accepted. The writer reads [3] after the refusal and
    // stops: it does not re-base and refill a window the producer owns.
    on_next("s_reload", [] {
      bfm_erase(0x21);
      bfm_write(0x21, bind_frame(Z));
      bfm_run();
    });
    boot();                                  // snap("boot")
    bind(Z2);                                // a controller change, reported
    idle(3000);
    snap("end");
  };
  cases["U13_four_refusals_with_the_device_busy"] = [] {         // real + bfm, slots of A1
    // The SECOND reading of the terminal row. Each of the four window loads
    // meets a paced whole-record WRITE still streaming at the strobe, which
    // is the case the bounded wait was added for; the wait heartbeats, so
    // nvm_backed SETS before the writer retires and the loss of a writer
    // that was once live raises nvm_stale. Same state, different row, and
    // never durable in either.
    for (unsigned k = 1; k <= 4; ++k)
      at("s_reload", hooks("s_reload") + k, [] {
        bfm_write(0x21, bind_frame(Z), -1, 60);
        if (!run_until([] { return levels().dev_busy != 0; }, 20000))
          fatal("the paced WRITE was not granted");
      });
    boot();                                  // snap("boot"): backed 1, dirty 1
    idle(3000);                              // past T-NVM-WRITER-ALIVE
    snap("end");                             // backed 0, stale 1, never durable
  };
}

static void load_cases_3() {
  cases["W3_write_across_refused_fill_then_restart"] = [] {      // real + bfm, restart, slots of A1
    // The re-review's probe H1 on revision d. Three refused loads as in U9;
    // then a whole-record WRITE of 0x21 carrying Z2 is granted just before
    // the LAST re-base -- the writer's status read has already told it the
    // device face is idle -- and is still streaming while the writer
    // re-bases and refills the window, so it ends with done over bytes the
    // FILL wrote and its record reads CLOSED. Then the writer restarts.
    // Nothing may promote that record: no load was accepted in this boot.
    if (!nvm_host_writer_restart) {          // only a contract writer has it
      on_next("no_restart_model", [] {});
      return;
    }
    for (unsigned k = 1; k <= 3; ++k)
      at("s_reload", hooks("s_reload") + k, [] {
        fault(0x20, 27, 0, 1);
        bfm_erase(0x20);
        bfm_run();
        faults.clear();
        if (hooks("s_reload") != 3)
          return;
        // the writer now reads [11], reads [3], then asks whether the
        // device face is idle; the value of that last read is sampled
        // BEFORE this hook runs, so the WRITE below is granted after the
        // writer has decided to repeat and before its re-base
        at("r_stat", hooks("r_stat") + 3, [] {
          bfm_write(0x21, bind_frame(Z2), -1, 300);
          if (!run_until([] { return levels().dev_busy != 0; }, 20000))
            fatal("the overlapping WRITE was not granted");
          note("overlap_grant", cyc);
        });
      });
    boot();
    snap("live");                            // 0x21 closed over the fill's bytes
    nvm_host_writer_restart();
    snap("restarted");
    idle(6000);
    snap("end");
  };
  cases["W4_all_records_rewritten_after_refused_fill"] = [] {    // real + bfm, restart, slots of A1
    // The re-review's probe H2: W3, and then every OTHER allocated record
    // rewritten whole on the device face, so that no record is left open by
    // accident. Under revision c that removed the last thing still
    // reporting and the status read durable over the lost change. Here the
    // boot accepted no load, so nothing was ever captured: the last
    // verified slot is untouched and the reading is not durable.
    if (!nvm_host_writer_restart) {
      on_next("no_restart_model", [] {});
      return;
    }
    cases["W3_write_across_refused_fill_then_restart"]();
    for (auto &r : recs) {
      if (r.first == 0x21 || r.second.len < 8u)
        continue;
      std::vector<uint8_t> pl(r.second.len - 8u, 0x5au);
      bfm_erase(r.first);
      bfm_write(r.first, frame(r.first, pl));
      bfm_run();
    }
    snap("rewritten");
    idle(3000);
    snap("end2");
  };
  cases["W1_writer_restart_reattaches"] = [] {                   // real
    // A CPU-only reset: the writer restarts, the fabric keeps its state,
    // with a newer binding in the window that no slot holds yet.
    if (!nvm_host_writer_restart) {          // only a contract writer has it
      on_next("no_restart_model", [] {});
      return;
    }
    base();
    bind(X2);
    idle(600);                               // flushed; the writer's debounce runs
    snap("before");
    nvm_host_writer_restart();
    snap("restarted");
    idle(3000);
    snap("end");
  };
}

static void load_cases() {
  load_cases_1();
  load_cases_2();
  load_cases_3();
}

// The case table, in the groups the contract page's section 9 reads
// them in. Split by group because Rule 11 bounds a function's length,
// and a table this long is easier to read by group in any case.
void register_cases() {
  acknowledgement_cases();
  capture_cases();
  hold_cases();
  liveness_cases();
  producer_cases();
  revocation_cases();
  unit_cases();
  load_cases();
}

// ------------------------------------------------------------------- main
void load_records(const std::string &path) {
  std::ifstream f(path);
  std::string line;
  while (std::getline(f, line)) {
    std::istringstream s(line);
    std::string k;
    s >> k;
    if (k == "imglen") s >> img_len;
    if (k != "rec") continue;
    std::string id, off, len;
    s >> id >> off >> len;
    Rec r{unsigned(std::stoul(id, nullptr, 0)), unsigned(std::stoul(off)),
          unsigned(std::stoul(len))};
    recs[r.id] = r;
  }
  if (recs.empty() || !img_len) fatal("no record table");
}

}  // namespace

// One 0/1 command-line flag, refused rather than defaulted: strtoul reports
// what it consumed, which atoi cannot, and a --d1 nobody parsed would model
// the donor export as ABSENT and quietly turn E3 into its expected failure.
static unsigned arg_flag(const char *text) {
  char *end = nullptr;
  const unsigned long value = std::strtoul(text, &end, 10);
  if (end == text || *end != '\0' || value > 1UL) {
    std::fprintf(stderr, "a 0/1 flag was expected, got %s\n", text);
    std::exit(2);
  }
  return static_cast<unsigned>(value);
}

// The identity-wrap arm's tail length, BOUNDED rather than defaulted, for
// the same reason and with the same call: a --commits nobody parsed would
// leave the arm short of the wrap and green because it never got there.
static unsigned arg_count(const char *text) {
  char *end = nullptr;
  const unsigned long value = std::strtoul(text, &end, 10);
  if (end == text || *end != '\0' || value > 8UL) {
    std::fprintf(stderr, "a commit count in 0..8 was expected, got %s\n", text);
    std::exit(2);
  }
  return static_cast<unsigned>(value);
}

int main(int argc, char **argv) {
  std::string name, table, slot_a, slot_b;
  unsigned d1 = 0, status = 0, commits = 0;
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    const char *v = (i + 1 < argc) ? argv[i + 1] : nullptr;
    if (a == "--case" && v) name = argv[++i];
    else if (a == "--out" && v) out_dir = argv[++i];
    else if (a == "--records" && v) table = argv[++i];
    // strtoul, not atoi: Rule 11 refuses an unbounded C call, and the
    // reason is the same here as anywhere -- atoi reports nothing, so a
    // typed --d1 would silently model the donor export as absent
    else if (a == "--d1" && v) d1 = arg_flag(argv[++i]);
    else if (a == "--slot-a" && v) slot_a = argv[++i];
    else if (a == "--slot-b" && v) slot_b = argv[++i];
    // the writer's own counters, asked for on the console AFTER the case
    // body and its observations: the identity-wrap arm reads
    // `captures refused` from it. It strobes nothing, so a case graded
    // without it is graded the same way with it.
    else if (a == "--status") status = 1;
    // further committing changes appended AFTER the case body and its
    // observations, so that a case which commits twice still reaches the
    // capture identity's fourth value -- 0 at the contract's minimum width
    else if (a == "--commits" && v) commits = arg_count(argv[++i]);
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
  host_init();
  if (!slot_a.empty() && !host_load_file(slot_a.c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET, 0x10000u))
    fatal("cannot load slot A");
  if (!slot_b.empty() &&
      !host_load_file(slot_b.c_str(), nvm_host_flash + NVM_HOST_JOURNAL_OFFSET + 0x10000u, 0x10000u))
    fatal("cannot load slot B");
  cosim::init(d1);
  if (name == "R_power_cycle") {
    // a retained-media boot: the slots of an earlier run, a fresh fabric
    boot();
    idle(200);
    snap("restored");
  } else {
    auto it = cases.find(name);
    if (it == cases.end()) {
      std::fprintf(stderr, "unknown case %s\n", name.c_str());
      return 2;
    }
    it->second();
  }
  if (commits) commit_tail(commits);
  if (status) host_uart("milan_nvm");
  dump_log();
  std::printf("CASE_DONE %s hooks_pending=%d\n", name.c_str(), all_fired() ? 0 : 1);
  cosim::finish();
  return 0;
}

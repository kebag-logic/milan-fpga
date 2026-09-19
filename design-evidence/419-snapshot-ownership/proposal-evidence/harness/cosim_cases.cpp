// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #419 round 3 co-simulation: the case scripts. STIMULUS ONLY. Every
// verdict is taken by proposal-evidence/run.py, which decodes the dumped
// journal slots with the repository's own scripts/nvm_klj2.py and compares
// them with records it frames itself; nothing in this file grades anything.
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
//! configures it, with no firmware running
void unit_configure() {
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
  cosim_rtl_csr_write(3, 0x10u);   // validated, VD_OK
  cosim_rtl_csr_write(4, 0x40u);   // reload (no such strobe on the tracked module)
  cosim_rtl_csr_write(4, 0x1u);    // heartbeat
  host_catch_up();
}

std::map<std::string, std::function<void()>> cases;

void register_cases() {
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
  cases["A6_late_ack_while_new_capture_open"] = [] {             // real + stray ACK
    base();
    bind(X2);
    // after the certificate and before the flash: the capture is open and
    // certified, so an acknowledgement quoting it would be accepted
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
      // certified and before its slot verifies; the flash then fails
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
      bfm_write(0x21, bind_frame(Z2), -1, 20);   // in flight at the arm edge
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

  // C. THE HOLD, THE CERTIFICATE AND THE ROUND-2 CONCERN ----------------------
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
    // the uncertified attempt releases; the next one commits and is acked
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
      // no content check can refuse it; only the certificate can
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
    stray(4, 0x10u);                   // certify
    stray(4, ack_word(csr_peek(5)));   // acknowledge that capture
    snap("acked");
  };
  cases["U3_grant_on_certify_edge"] = [] {                        // unit
    unit_configure();
    stray(4, 0x8u);                    // ARM: the hold is on
    bfm_erase(0x21);                   // requested, deferred
    run_cycles(1000);
    note("deferred_while_hold", levels().dev_busy);
    if (!run_until([] { return ((csr_peek(3) >> 17) & 1u) == 0; }, 200000))
      fatal("hold never lapsed");
    // the next edge grants the deferred ERASE: certify on that same edge
    stray(4, 0x10u);
    snap("cert");
  };
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

int main(int argc, char **argv) {
  std::string name, table, slot_a, slot_b;
  unsigned d1 = 0;
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    const char *v = (i + 1 < argc) ? argv[i + 1] : nullptr;
    if (a == "--case" && v) name = argv[++i];
    else if (a == "--out" && v) out_dir = argv[++i];
    else if (a == "--records" && v) table = argv[++i];
    else if (a == "--d1" && v) d1 = unsigned(std::atoi(argv[++i]));
    else if (a == "--slot-a" && v) slot_a = argv[++i];
    else if (a == "--slot-b" && v) slot_b = argv[++i];
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
  dump_log();
  std::printf("CASE_DONE %s hooks_pending=%d\n", name.c_str(), all_fired() ? 0 : 1);
  cosim::finish();
  return 0;
}

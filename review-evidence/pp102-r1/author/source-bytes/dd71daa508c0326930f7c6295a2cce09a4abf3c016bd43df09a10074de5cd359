// SPDX-License-Identifier: CERN-OHL-W-2.0
// CONTROLLER_AVAILABLE builder: owner sequence and cancellation lifecycle.
#include <array>
#include <cstdint>
#include <cstdio>
#include "VKL_aecp_ca_originator.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// One CONTROLLER_AVAILABLE frame is 60 bytes, written one byte per cycle.
constexpr int kFrameBytes = 60;
// Reset is held low for this many cycles before the builder is exercised.
constexpr int kResetCycles = 4;

namespace {

//! The builder, its bus BFM and the tally in one object. The BFM half was
//! already a `struct Harness`; the counters it checks against were file-scope
//! mutables and the lifecycle it exercises was a 132-line `main`, so I.2 and
//! F.3 join them up here.
struct Harness {
  const milan::tb::Model<VKL_aecp_ca_originator> model;
  VKL_aecp_ca_originator* const d = model.get();
  std::array<uint8_t, kFrameBytes> frame{};
  int writes = 0;
  bool pre_commit = false;
  bool pre_issue = false;
  int checks = 0;
  int fails = 0;

  static uint16_t owner_seq(unsigned owner) {
    return static_cast<uint16_t>(0x1100u + 0x101u * owner);
  }

  void settle() {
    d->clk_i = 0;
    d->eval();
    d->iss_seq_i = owner_seq(d->iss_owner_o);
    d->eval();
  }

  void tick() {
    settle();
    pre_commit = d->txs_wr_commit_o;
    pre_issue = d->iss_valid_o;
    if (d->txs_wr_valid_o && d->txs_wr_addr_o < frame.size()) {
      frame[d->txs_wr_addr_o] = d->txs_wr_data_o;
      writes++;
    }
    d->clk_i = 1;
    d->eval();
  }

  void reset() {
    d->rst_n = 0;
    for (int i = 0; i < kResetCycles; ++i) tick();
    d->rst_n = 1;
    tick();
  }

  void request(unsigned owner) {
    d->req_owner_i = owner;
    d->req_ctlr_eid_i = 0xA100000000000000ull | owner;
    d->req_mac_i = 0x020000000000ull | owner;
    d->req_valid_i = 1;
    tick();
    d->req_valid_i = 0;
  }

  void grant(unsigned slot) {
    d->txs_alloc_slot_i = slot;
    d->txs_alloc_gnt_i = 1;
    tick();
    d->txs_alloc_gnt_i = 0;
  }

  void write_frame() {
    for (int i = 0; i < kFrameBytes; ++i) tick();
  }

  void clear_cancel() {
    d->cancel_valid_i = 0;
    tick();
  }

  int run();

  void bring_the_builder_out_of_reset();
  void check_allocation_request_is_one_pulse_and_cancellable();
  void check_sequence_follows_the_captured_owner_through_issue();
  void check_pre_grant_cancellation_releases_no_slot();
  void check_cancellation_on_a_delayed_grant_releases_that_slot();
  void check_write_phase_cancellation_releases_the_slot();
  void check_commit_phase_cancellation_suppresses_commit();
  void check_issue_phase_cancellation_and_return_to_idle();
  int report();
};

void Harness::bring_the_builder_out_of_reset() {
  d->entity_id_i = 0x0011223344556677ull;
  d->own_mac_i = 0x020000001234ull;
  d->req_valid_i = 0;
  d->cancel_valid_i = 0;
  d->txs_alloc_gnt_i = 0;
  d->iss_ready_i = 1;
  d->iss_gnt_i = 0;
  d->iss_id_i = 2;
  reset();
}

// A request is pulsed for one cycle, then the builder waits one cycle for
// the registered pool result. A full pool causes another isolated pulse.
void Harness::check_allocation_request_is_one_pulse_and_cancellable() {
  request(0);
  settle();
  CHECK(d->txs_alloc_req_o,
        "A allocation request is asserted for one sampling cycle");
  tick();
  settle();
  CHECK(!d->txs_alloc_req_o,
        "A allocation request drops while the registered grant is pending");
  tick();
  settle();
  CHECK(d->txs_alloc_req_o,
        "A full-pool miss is retried without consecutive request cycles");
  d->txs_alloc_slot_i = 0;
  d->txs_alloc_gnt_i = 1;
  d->cancel_owner_i = 0;
  d->cancel_valid_i = 1;
  tick();
  d->txs_alloc_gnt_i = 0;
  CHECK(d->txs_abort_o && d->cancel_release_valid_o
            && d->cancel_release_slot_o == 0,
        "A retried allocation can be canceled without leaking its slot");
  clear_cancel();
}

// The sequence source is indexed by iss_owner_o. The builder starts with
// owner zero, then accepts owner three, so latching before owner capture
// writes the wrong sequence into bytes 34 and 35.
void Harness::check_sequence_follows_the_captured_owner_through_issue() {
  request(3);
  grant(2);
  write_frame();
  CHECK(writes == kFrameBytes, "B builder writes exactly 60 bytes");
  const uint16_t seq3 = Harness::owner_seq(3);
  CHECK(frame[34] == static_cast<uint8_t>(seq3 >> 8)
            && frame[35] == static_cast<uint8_t>(seq3),
        "B frame sequence follows the requested owner");
  tick();
  settle();
  CHECK(d->iss_valid_o && d->iss_owner_o == 3
            && d->iss_tx_slot_o == 2,
        "B committed frame issues for its captured owner and slot");
  d->iss_gnt_i = 1;
  tick();
  d->iss_gnt_i = 0;
  CHECK(d->issued_valid_o && d->issued_owner_o == 3,
        "B issue grant completes the builder");
  tick();
}

// Cancellation before an allocation grant has no slot to release, but it
// must still tell the shared writer arbiter to drop ownership.
void Harness::check_pre_grant_cancellation_releases_no_slot() {
  request(1);
  d->cancel_owner_i = 1;
  d->cancel_valid_i = 1;
  tick();
  CHECK(d->txs_abort_o && !d->cancel_release_valid_o
            && d->req_ready_o,
        "B pre-grant cancellation aborts without releasing a slot");
  clear_cancel();
}

// A registered allocation grant is visible one cycle after allocation.
// Cancellation on that cycle must release the granted slot, not ignore it.
void Harness::check_cancellation_on_a_delayed_grant_releases_that_slot() {
  request(2);
  d->txs_alloc_slot_i = 4;
  d->txs_alloc_gnt_i = 1;
  d->cancel_owner_i = 2;
  d->cancel_valid_i = 1;
  tick();
  d->txs_alloc_gnt_i = 0;
  CHECK(d->txs_abort_o && d->cancel_release_valid_o
            && d->cancel_release_slot_o == 4,
        "C cancellation on delayed grant aborts and releases that slot");
  clear_cancel();
}

void Harness::check_write_phase_cancellation_releases_the_slot() {
  request(4);
  grant(1);
  for (int i = 0; i < 7; ++i) tick();
  d->cancel_owner_i = 4;
  d->cancel_valid_i = 1;
  tick();
  CHECK(d->txs_abort_o && d->cancel_release_valid_o
            && d->cancel_release_slot_o == 1 && !d->txs_wr_commit_o,
        "D write-phase cancellation aborts and releases the allocated slot");
  clear_cancel();
}

void Harness::check_commit_phase_cancellation_suppresses_commit() {
  request(5);
  grant(2);
  write_frame();
  settle();
  CHECK(d->txs_wr_commit_o, "E builder reaches commit after byte 59");
  d->cancel_owner_i = 5;
  d->cancel_valid_i = 1;
  tick();
  CHECK(d->txs_abort_o && d->cancel_release_valid_o
            && d->cancel_release_slot_o == 2 && !pre_commit,
        "E commit-phase cancellation suppresses commit and releases the slot");
  clear_cancel();
}

void Harness::check_issue_phase_cancellation_and_return_to_idle() {
  request(6);
  grant(3);
  write_frame();
  tick();
  settle();
  CHECK(d->iss_valid_o, "F committed frame reaches issue phase");
  d->cancel_owner_i = 6;
  d->cancel_valid_i = 1;
  tick();
  CHECK(d->txs_abort_o && d->cancel_release_valid_o
            && d->cancel_release_slot_o == 3 && !pre_issue,
        "F issue-phase cancellation suppresses issue and releases the slot");
  clear_cancel();
  CHECK(d->req_ready_o && !d->txs_abort_o
            && !d->cancel_release_valid_o,
        "G builder returns cleanly to idle after cancellation");
}

int Harness::report() {
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int Harness::run() {
  bring_the_builder_out_of_reset();
  check_allocation_request_is_one_pulse_and_cancellable();
  check_sequence_follows_the_captured_owner_through_issue();
  check_pre_grant_cancellation_releases_no_slot();
  check_cancellation_on_a_delayed_grant_releases_that_slot();
  check_write_phase_cancellation_releases_the_slot();
  check_commit_phase_cancellation_suppresses_commit();
  check_issue_phase_cancellation_and_return_to_idle();
  return report();
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Harness h;
  return h.run();
}

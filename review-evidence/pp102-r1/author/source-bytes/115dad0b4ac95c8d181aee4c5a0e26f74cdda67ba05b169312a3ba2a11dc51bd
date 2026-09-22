// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_release_merge directed suite with independent expected sequences.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "VKL_pp_release_merge.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

namespace {

struct Harness {
  VKL_pp_release_merge* dut;
  std::vector<uint8_t> releases;

  explicit Harness(VKL_pp_release_merge* d) : dut(d) {}

  void drive(bool av, uint8_t as, bool bv, uint8_t bs) {
    dut->a_valid_i = av;
    dut->a_slot_i = as;
    dut->b_valid_i = bv;
    dut->b_slot_i = bs;
    dut->clk_i = 0;
    dut->eval();
  }

  void edge() {
    if (dut->rst_n && dut->release_valid_o)
      releases.push_back(static_cast<uint8_t>(dut->release_slot_o));
    dut->clk_i = 1;
    dut->eval();
  }

  void step(bool av = false, uint8_t as = 0,
            bool bv = false, uint8_t bs = 0) {
    drive(av, as, bv, bs);
    edge();
  }

  bool idle_now() {
    drive(false, 0, false, 0);
    return !dut->release_valid_o;
  }
};

// The tally the CHECK macro keeps was a pair of file-scope statics; it is the
// state of one run of this suite, so it belongs to the object that performs it.
class ReleaseMergeSuite {
 public:
  int run();

 private:
  int checks = 0;
  int fails = 0;
};

int ReleaseMergeSuite::run() {
  const milan::tb::Model<VKL_pp_release_merge> model;
  VKL_pp_release_merge* const dut = model.get();
  Harness h(dut);

  dut->rst_n = 0;
  h.step();
  h.step();
  dut->rst_n = 1;
  CHECK(h.idle_now(), "R idle after reset");

  h.step(true, 3, false, 0);
  CHECK(h.releases.size() == 1 && h.releases.back() == 3,
        "A source A releases slot 3");
  CHECK(h.idle_now(), "A drains in one cycle");

  h.step(false, 0, true, 2);
  CHECK(h.releases.size() == 2 && h.releases.back() == 2,
        "B source B releases slot 2");
  CHECK(h.idle_now(), "B drains in one cycle");

  size_t n = h.releases.size();
  h.step(true, 4, true, 1);
  h.step();
  CHECK(h.releases.size() == n + 2, "C both simultaneous handles emitted");
  CHECK(h.releases[n] == 1 && h.releases[n + 1] == 4,
        "C simultaneous handles serialize in slot order");
  CHECK(h.idle_now(), "C pending handle drained");

  n = h.releases.size();
  h.step(true, 2, true, 2);
  CHECK(h.releases.size() == n + 1 && h.releases.back() == 2,
        "D duplicate simultaneous release is idempotent");
  CHECK(h.idle_now(), "D duplicate leaves no pending copy");

  n = h.releases.size();
  h.step(true, 4, true, 3);
  h.step(true, 2, false, 0);
  h.step(false, 0, true, 1);
  h.step();
  CHECK(h.releases.size() == n + 4, "E four distinct handles conserved");
  CHECK(h.releases[n] == 3 && h.releases[n + 1] == 2
        && h.releases[n + 2] == 1 && h.releases[n + 3] == 4,
        "E pending set survives three cycles of fresh releases");
  CHECK(h.idle_now(), "E backlog fully drained");

  n = h.releases.size();
  h.step(true, 7, true, 6);
  CHECK(h.releases.size() == n, "F invalid handles ignored");
  CHECK(h.idle_now(), "F invalid handles never become pending");

  h.step(true, 4, true, 0);
  CHECK(h.releases.back() == 0, "G lower handle emitted before pending slot 4");
  dut->rst_n = 0;
  h.step();
  dut->rst_n = 1;
  CHECK(h.idle_now(), "G reset clears pending slot 4");

  CHECK(h.releases.size() == 10, "final exact release count got %zu",
        h.releases.size());

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  ReleaseMergeSuite suite;
  return suite.run();
}

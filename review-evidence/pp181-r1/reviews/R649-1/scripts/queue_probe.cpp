// Disposable interface stimulus for command-queue preservation.
#define main original_suite_main
#include "sim_main.cpp"
#undef main
#include "VKL_aecp_notify___024root.h"
#include <tuple>

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<VKL_aecp_notify> model;
  Harness h;
  h.d = model.get();
  auto* d = h.d;
  h.initialize_inputs();
  constexpr uint64_t eid[2] = {0x1111000000000001ull, 0x2222000000000002ull};
  constexpr uint64_t mac[2] = {0x020000000001ull, 0x020000000002ull};
  for (int i = 0; i < 2; ++i) h.register_row(eid[i], mac[i], false);
  using Job = std::tuple<unsigned, unsigned, unsigned, unsigned, unsigned, uint64_t, uint64_t, unsigned>;
  std::vector<Job> got, want;
  unsigned seq[2] = {};
  int failed = 0;
  auto check = [&](bool ok, const char* label) {
    if (!ok) { printf("FAIL: %s\n", label); ++failed; }
  };
  auto drive = [&](unsigned i) {
    d->ev_cmd_i = 1;
    d->ev_cmd_class_i = 7;
    d->ev_cmd_type_i = 5;
    d->ev_cmd_index_i = i;
    d->ev_cmd_arg0_i = 0x1230 + i;
    d->ev_cmd_arg1_i = 0xabc0 + i;
    d->ev_cmd_excl_eid_i = i % 3 == 0 ? eid[0] : 0;
  };
  auto expected = [&](unsigned i) {
    for (int row = 0; row < 2; ++row) {
      if (row == 0 && i % 3 == 0) continue;
      want.emplace_back(KIND_NAME, 5, i, 0x1230+i, 0xabc0+i, eid[row], mac[row], seq[row]++);
    }
  };
  unsigned cycle = 0;
  auto step = [&]() {
    d->clk_i = 0;
    d->eval();
    if (d->uns_valid_o && d->uns_done_i)
      got.emplace_back(d->uns_kind_o, d->uns_desc_type_o, d->uns_desc_index_o,
                       d->uns_arg0_o, d->uns_arg1_o, d->uns_ctlr_eid_o, d->uns_mac_o, d->uns_seq_o);
    printf("cycle %u busy %u valid %u count %u drop %u sent %zu\n", cycle++, unsigned(d->amap_busy_o),
           unsigned(d->uns_valid_o), unsigned(d->rootp->KL_aecp_notify__DOT__cmdq_count_r),
           unsigned(d->rootp->KL_aecp_notify__DOT__cmdq_drop_r), got.size());
    h.tick();
  };
  d->uns_done_i = 0;
  for (unsigned i = 0; i < 20; ++i) {
    drive(i);
    if (i < 17) expected(i);
    step();
  }
  check(d->rootp->KL_aecp_notify__DOT__cmdq_count_r == 16, "full queue retains sixteen waiting commands");
  check(d->rootp->KL_aecp_notify__DOT__cmdq_drop_r == 3, "three excess commands counted once");
  d->ev_cmd_i = 0;
  for (unsigned i = 0; i < 20; ++i) step();
  d->uns_done_i = 1;
  for (unsigned i = 0; i < 1000; ++i) step();
  check(got == want, "ordered content and per-controller sequence/exclusion after full queue");
  check(!d->amap_busy_o && d->rootp->KL_aecp_notify__DOT__cmdq_count_r == 0,
        "last pop clears occupancy and admission busy");
  drive(21); expected(21); step();
  drive(22); expected(22); step();
  d->ev_cmd_i = 0;
  for (unsigned i = 0; i < 100; ++i) step();
  check(got == want, "back-to-back refill after empty delivers both jobs");
  d->uns_done_i = 0;
  for (unsigned i = 0; i < 5; ++i) { drive(30+i); step(); }
  d->ev_cmd_i = 0;
  h.warm_reset();
  check(d->rootp->KL_aecp_notify__DOT__cmdq_count_r == 0 && !d->amap_busy_o,
        "warm reset clears a nonempty queue and busy");
  check(d->rootp->KL_aecp_notify__DOT__cmdq_drop_r == 0, "warm reset clears drop count");
  printf("queue probe: %d failures; %zu delivered jobs\n", failed + h.fails, got.size());
  return failed || h.fails ? 1 : 0;
}

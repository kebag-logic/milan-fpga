#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe P1: a read-only GET_RX_STATE of a sink stored before a
failed binding walk. Patches a COPY of tb/acmp_nvm/sim_main.cpp (argv[1]) so
that, with R278_PROBE set in the environment, the bench runs only the probe
cases below and reports its own check tally.

Each case seeds saved bindings for sinks 0, 3 and 7, makes the walk fail at
sink 3 (after sink 0 was read and stored), sends ONE read-only GET_RX_STATE
for sink 0, lets every flush run out, then grades the saved record of sink 0
in the device's store and a reset round trip on a healthy device.
"""
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()

decl_anchor = "  int report();\n"
assert src.count(decl_anchor) == 1
src = src.replace(decl_anchor, "  void probe_r278();\n" + decl_anchor)

run_anchor = "int Harness::run_suite() {\n"
assert src.count(run_anchor) == 1
src = src.replace(run_anchor, run_anchor
                  + "  if (getenv(\"R278_PROBE\")) { probe_r278(); return report(); }\n")

probe = r'''
void Harness::probe_r278() {
  struct C {
    const char* tag;
    int kind;      // 0 control, 1 device err, 2 deadline (late end), 3 torn
    unsigned cause;
  };
  const std::vector<C> cs = {
    {"P1-0 control: no fault", 0, 0},
    {"P1-1 a device error at sink 3's header read", 1, 2},
    {"P1-2 sink 3's read silent, the device ends it 2000 cycles late", 2, 3},
    {"P1-3 sink 3's payload read torn after 3 bytes", 3, 1},
  };
  for (const C& c : cs) {
    const Bind b3{true, false, false, 0x0A03, 0x00A3A3A3A3A30003ull,
                  0x00C0C0C0C0C00003ull};
    l_seed({{0, L_B0}, {3, b3}, {L_LAST, L_B7}});
    reset();
    if (c.kind == 1) arm_err(OP_READ, REC_BASE + 3, 0, -1, 1);
    if (c.kind == 2) { hold_region = REC_BASE + 3; hold_mode = 2; hold_n = 2000; }
    if (c.kind == 3) arm_err(OP_READ, REC_BASE + 3, 8, 3, 1);
    go();
    run_until([&] { return rel_cyc >= 0; }, 4 * RS_TMO);
    CHECK(d->restore_done_o && unsigned(d->restore_fail_o) == (c.cause ? 1u : 0u)
              && d->restore_cause_o == c.cause,
          "%s: walk done %u fail %u cause %u (want cause %u)", c.tag,
          unsigned(d->restore_done_o), unsigned(d->restore_fail_o),
          unsigned(d->restore_cause_o), c.cause);
    disarm_err();
    const size_t n_ops_before = ops.size();
    l_push(M_GETRX_CMD, 0, 0xE20, cycles);
    if (c.kind == 2) run_until([&] { return hold_rel; }, 8000);
    l_finish();
    run(DEB_TICKS * 4 + 2000);
    const auto g = l_resps(M_GETRX_RSP);
    printf("  [i] %s: %zu GET replies, dirty 0x%02x, %d writes, %zu device ops "
           "after the GET, sink 0 store magic %02x%02x valid-byte %02x\n",
           c.tag, g.size(), unsigned(d->dbg_dirty_o), count_ops(OP_WRITE),
           ops.size() - n_ops_before, store[0][0], store[0][1], store[0][8]);
    CHECK(count_ops(OP_WRITE) == 0 && count_ops(OP_ERASE) == 0,
          "%s: the read-only GET wrote nothing (%d writes, %d erases)", c.tag,
          count_ops(OP_WRITE), count_ops(OP_ERASE));
    CHECK(l_nvm_is(0, L_B0) && l_nvm_is(3, b3) && l_nvm_is(L_LAST, L_B7),
          "%s: sink 0's saved binding is still in NVM after the read-only GET",
          c.tag);
    Bind want[N_SINKS];
    want[0] = L_B0;
    want[3] = b3;
    want[L_LAST] = L_B7;
    std::string why;
    CHECK(l_round_trip(want, why),
          "%s: a reset on a healthy device restores the saved bindings: %s",
          c.tag, why.c_str());
  }
}
'''
rep_anchor = "int Harness::report() {\n"
assert src.count(rep_anchor) == 1
src = src.replace(rep_anchor, probe.lstrip("\n") + "\n" + rep_anchor)
open(path, "w", encoding="utf-8").write(src)
print("patched", path)

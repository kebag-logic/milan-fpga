#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe P3 (round 2): the edges of the capture compare's unbound
rule. Patches a COPY of tb/acmp_nvm/sim_main.cpp (argv[1]); with R278_P3 set
in the environment the bench runs only these cases and reports its own tally.

The rule keeps a failed walk's saved records against write-backs that restate
an unbound default. These cases check what it must NOT suppress, and pin the
recorded decision 5 (an UNBIND of a sink the failed walk left unbound writes
nothing):

  P3-1 failed walk (device error at sink 3), then BIND sink 0 to a new talker:
       the new binding is persisted and a healthy reset restores it.
  P3-2 failed walk, then BIND sink 0 and UNBIND sink 0: the device ends with
       sink 0 unbound and a healthy reset preloads only sinks 3 and 7 (the
       route an operator has to clear a saved binding the walk could not read).
  P3-3 failed walk, then UNBIND sink 0 only (decision 5): nothing written, and
       a healthy reset brings sink 0's saved binding back.
  P3-4 healthy walk, then UNBIND the restored sink 0: persisted unbound, and a
       healthy reset preloads only sink 7.
  P3-5 healthy walk, then BIND the restored sink 0 to another talker (bound to
       bound, only fields differ): persisted, and restored by a reset.
  P3-6 healthy walk, UNBIND sink 0 then two GETs of it: one unbound record in
       the device, a reset preloads only sink 7.
"""
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()

decl_anchor = "  int report();\n"
assert src.count(decl_anchor) == 1
src = src.replace(decl_anchor, "  void probe_r278_p3();\n" + decl_anchor)

run_anchor = "int Harness::run_suite() {\n"
assert src.count(run_anchor) == 1
src = src.replace(run_anchor, run_anchor
                  + "  if (getenv(\"R278_P3\")) { probe_r278_p3(); return report(); }\n")

probe = r'''
void Harness::probe_r278_p3() {
  const Bind b3{true, false, false, 0x0A03, 0x00A3A3A3A3A30003ull,
                0x00C0C0C0C0C00003ull};
  // what the listener's BIND of sink 0 to L_TKC persists (L22's expectation)
  const Bind nb{true, true, false, L_TKC_UID, L_TKC, L_CTLR};
  const Bind unb{};
  struct C {
    const char* tag;
    bool fail;        // walk fails at sink 3 with a device error
    int script;       // 1 BIND, 2 BIND+UNBIND, 3 UNBIND, 4 GET,GET after UNBIND
    Bind want0;       // sink 0 in the device afterwards
    bool untouched;   // nothing written at all
  };
  const std::vector<C> cs = {
    {"P3-1 failed walk, then BIND sink 0", true, 1, nb, false},
    {"P3-2 failed walk, then BIND and UNBIND sink 0", true, 2, unb, false},
    {"P3-3 failed walk, then UNBIND sink 0 only (decision 5)", true, 3, L_B0, true},
    {"P3-4 healthy walk, then UNBIND the restored sink 0", false, 3, unb, false},
    {"P3-5 healthy walk, then re-BIND sink 0 to another talker", false, 1, nb, false},
    {"P3-6 healthy walk, UNBIND then two GETs of sink 0", false, 4, unb, false},
  };
  for (const C& c : cs) {
    l_seed({{0, L_B0}, {3, b3}, {L_LAST, L_B7}});
    reset();
    if (c.fail) arm_err(OP_READ, REC_BASE + 3, 0, -1, 1);
    go();
    l_finish();
    CHECK(d->restore_done_o && unsigned(d->restore_fail_o) == (c.fail ? 1u : 0u),
          "%s: walk done %u fail %u cause %u", c.tag, unsigned(d->restore_done_o),
          unsigned(d->restore_fail_o), unsigned(d->restore_cause_o));
    disarm_err();
    const size_t n_resp = resps.size();
    if (c.script == 1 || c.script == 2)
      l_push(M_BIND_RX_CMD, 0, 0xF01, cycles, L_TKC, L_TKC_UID, 0);
    if (c.script == 2 || c.script == 3 || c.script == 4)
      l_push(M_UNBIND_CMD, 0, 0xF02, cycles);
    if (c.script == 4) {
      l_push(M_GETRX_CMD, 0, 0xF03, cycles);
      l_push(M_GETRX_CMD, 0, 0xF04, cycles);
    }
    l_finish();
    // only the answers to the commands pushed here: a BIND also transmits a
    // PROBE_TX command towards the talker, which is not a reply
    size_t nrsp = 0, nbad = 0;
    for (size_t i = n_resp; i < resps.size(); ++i) {
      if (resps[i].b.size() != size_t(PDU_BYTES)) continue;
      const uint8_t m = resps[i].b[1] & 0x0F;
      if (m != M_BIND_RX_RSP && m != M_UNBIND_RSP && m != M_GETRX_RSP) continue;
      ++nrsp;
      if ((resps[i].b[2] >> 3) != 0) ++nbad;
    }
    printf("  [i] %s: %zu frames, %zu replies, %d writes %d erases, dirty 0x%02x, "
           "sink 0 valid-byte %02x\n", c.tag, resps.size() - n_resp, nrsp,
           count_ops(OP_WRITE), count_ops(OP_ERASE), unsigned(d->dbg_dirty_o),
           store[0][8]);
    CHECK(nrsp == size_t(c.script == 2 ? 2 : c.script == 4 ? 3 : 1) && nbad == 0,
          "%s: every command answered SUCCESS (%zu replies, %zu non-zero status)",
          c.tag, nrsp, nbad);
    std::string why;
    if (c.untouched) {
      CHECK(l_nvm_untouched(why), "%s: nothing written: %s", c.tag, why.c_str());
    } else {
      CHECK(count_ops(OP_WRITE) >= 1 && d->dbg_dirty_o == 0,
            "%s: the change was written and nothing is pending (%d writes)", c.tag,
            count_ops(OP_WRITE));
    }
    CHECK(l_nvm_is(0, c.want0) && l_nvm_is(3, b3) && l_nvm_is(L_LAST, L_B7),
          "%s: the device holds the expected sink-0 record and the other saved "
          "records unchanged", c.tag);
    Bind want[N_SINKS];
    want[0] = c.want0;
    want[3] = b3;
    want[L_LAST] = L_B7;
    CHECK(l_round_trip(want, why),
          "%s: a reset on a healthy device restores exactly that: %s", c.tag,
          why.c_str());
  }
}
'''
rep_anchor = "int Harness::report() {\n"
assert src.count(rep_anchor) == 1
src = src.replace(rep_anchor, probe.lstrip("\n") + "\n" + rep_anchor)
open(path, "w", encoding="utf-8").write(src)
print("patched", path)

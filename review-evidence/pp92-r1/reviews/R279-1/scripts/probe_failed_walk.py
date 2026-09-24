#!/usr/bin/env python3
"""Reviewer probe (not a source change): does a read-only GET_RX_STATE after a
FAILED binding walk rewrite a saved binding that the walk had already stored?
Adds one case per failure cause to a SCRATCH copy of tb/acmp_nvm/sim_main.cpp:
sinks 0 and 7 saved, the walk fails at sink 3 (cause 2: device err on its
header read; cause 3: its header read held until 2000 cycles after the abort;
cause 1: sink 7's payload read torn after 5 bytes), then one GET of sink 0.
Grades: NVM writes after the GET, sink 0's record byte-exact, and a healthy
reset that restores sink 0.  usage: probe_failed_walk.py <head_tree> <scratch_dir>"""
import os, shutil, subprocess, sys
head, dst = sys.argv[1:3]
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(head, dst, ignore=shutil.ignore_patterns("obj_*"))
p = os.path.join(dst, "tb/acmp_nvm/sim_main.cpp")
s = open(p).read()
decl = "  int report();\n  int run_suite();\n"
assert s.count(decl) == 1
s = s.replace(decl, "  void probe_failed_walk();\n" + decl)
body = r'''
void Harness::probe_failed_walk() {
  for (int cause = 1; cause <= 3; ++cause) {
    l_seed({{0, L_B0}, {L_LAST, L_B7}});
    reset();
    if (cause == 2) arm_err(OP_READ, REC_BASE + 3, 0, -1, 1);
    if (cause == 3) { hold_region = REC_BASE + 3; hold_mode = 2; hold_n = 2000; }
    if (cause == 1) arm_err(OP_READ, REC_BASE + L_LAST, 8, 5, 1);
    go();
    l_finish();
    run(3000);                              // any drain has ended
    l_finish();
    const unsigned got_cause = unsigned(d->restore_cause_o);
    const bool failed = d->restore_fail_o;
    disarm_err();
    const int w0 = count_ops(OP_WRITE), e0 = count_ops(OP_ERASE);
    const bool kept_before = l_nvm_is(0, L_B0);
    l_push(M_GETRX_CMD, 0, uint16_t(0xF00 + cause), cycles);
    l_finish();
    run(DEB_TICKS * 10);
    l_finish();
    const int w1 = count_ops(OP_WRITE) - w0, e1 = count_ops(OP_ERASE) - e0;
    const bool kept_after = l_nvm_is(0, L_B0);
    printf("PROBE FW cause %d: walk failed=%d cause=%u; before GET sink0 kept=%d; "
           "after GET writes=%d erases=%d sink0 kept=%d byte8=%02x\n",
           cause, int(failed), got_cause, int(kept_before), w1, e1,
           int(kept_after), unsigned(store[0][8]));
    CHECK(failed && got_cause == unsigned(cause) && kept_before,
          "PROBE FW cause %d: the walk failed with its cause and NVM still held sink 0", cause);
    CHECK(w1 == 0 && e1 == 0 && kept_after,
          "PROBE FW cause %d: a read-only GET after the failed walk leaves sink 0's saved record (%d writes)", cause, w1);
    reset();                                   // a healthy boot
    go();
    l_finish();
    printf("PROBE FW cause %d: healthy reboot fail=%u valid=0x%02x\n", cause,
           unsigned(d->restore_fail_o), unsigned(d->dbg_valid_o));
    CHECK(!d->restore_fail_o && (d->dbg_valid_o & 1),
          "PROBE FW cause %d: the next healthy boot restores sink 0", cause);
  }
}
'''
anchor = "int Harness::run_suite() {\n"
assert s.count(anchor) == 1
s = s.replace(anchor, body + "\n" + anchor)
call = "  check_n7_a_talker_level_at_the_deadline();\n"
assert s.count(call) == 1
s = s.replace(call, call + "  probe_failed_walk();\n")
open(p, "w").write(s)
sys.exit(subprocess.call(["make", "VERILATOR=" + os.environ["PIN_VERILATOR"], "run"],
                         cwd=os.path.join(dst, "tb/acmp_nvm")))

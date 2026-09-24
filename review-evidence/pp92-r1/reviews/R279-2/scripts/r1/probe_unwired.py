#!/usr/bin/env python3
"""Reviewer probe (not a source change): add two cases to a SCRATCH copy of
tb/acmp_nvm/sim_main.cpp and run the suite there.
 P1 an unwired device face: the port's first READ is never granted.
 P2 a device face that answers every READ with err.
Each boots with no traffic and reports what the integrator pins show.
usage: probe_unwired.py <head_tree> <scratch_dir>"""
import shutil, subprocess, sys, os
head, dst = sys.argv[1:3]
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(head, dst, ignore=shutil.ignore_patterns("obj_*"))
p = os.path.join(dst, "tb/acmp_nvm/sim_main.cpp")
s = open(p).read()
decl = "  int report();\n  int run_suite();\n"
assert s.count(decl) == 1
s = s.replace(decl, "  void probe_unwired();\n" + decl)
body = r'''
void Harness::probe_unwired() {
  // P1: a face nobody wired: dev_gnt_i never rises
  reset();
  gnt_delay = 1 << 30;
  go();
  bool ended = run_until([&] { return restore_done(); }, 20000);
  run(8);                      // let the release follow the terminal
  printf("PROBE P1 unwired face (no grant): ended=%d done=%u fail=%u blank=%u "
         "cause=%u released=%d rel-done=%ld reads_granted=%d\n",
         int(ended), unsigned(d->restore_done_o), unsigned(d->restore_fail_o),
         unsigned(d->restore_blank_o), unsigned(d->restore_cause_o),
         int(d->gate_released_o), rel_cyc - done_cyc, count_ops(OP_READ));
  std::string why;
  CHECK(n_failed_walk(3, why), "PROBE P1 an unwired face fails the walk with cause 3: %s", why.c_str());
  gnt_delay = 1;
  // P2: every READ answered with err at once
  reset();
  arm_err(OP_READ, -1, -1, -1, 1000);
  go();
  ended = run_until([&] { return restore_done(); }, 20000);
  run(8);
  printf("PROBE P2 err-answering face: ended=%d done=%u fail=%u blank=%u cause=%u "
         "reads=%d\n", int(ended), unsigned(d->restore_done_o),
         unsigned(d->restore_fail_o), unsigned(d->restore_blank_o),
         unsigned(d->restore_cause_o), count_ops(OP_READ));
  CHECK(n_failed_walk(2, why), "PROBE P2 an err-answering face fails the walk with cause 2: %s", why.c_str());
  disarm_err();
}
'''
anchor = "int Harness::run_suite() {\n"
assert s.count(anchor) == 1
s = s.replace(anchor, body + "\n" + anchor)
call = "  check_n7_a_talker_level_at_the_deadline();\n"
assert s.count(call) == 1
s = s.replace(call, call + "  probe_unwired();\n")
open(p, "w").write(s)
rc = subprocess.call(["make", "VERILATOR=" + os.environ["PIN_VERILATOR"], "run"],
                     cwd=os.path.join(dst, "tb/acmp_nvm"))
sys.exit(rc)

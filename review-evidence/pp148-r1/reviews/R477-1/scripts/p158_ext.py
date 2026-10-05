#!/usr/bin/env python3
"""Reviewer extension of the published DEREGISTER mid-round probe (applied after
probe-dereg-mid-round.diff to tb/aecp_notify/sim_main.cpp): after the corrupted
round, raise one AVB_INTERFACE 0 change and print when the next counter round is
presented. Usage: p158_ext.py PATH/TO/sim_main.cpp"""
import sys
p = sys.argv[1]
s = open(p).read()
old = "    }\n  }\n  d->uns_done_i = 1;\n}\n#else"
assert s.count(old) == 1, s.count(old)
new = ("    }\n  }\n"
       "  // reviewer extension: after the corrupted round, when does the next\n"
       "  // counter round of AVB_INTERFACE 0 present?\n"
       "  const uint32_t t_change = now + 100;\n"
       "  hold_until(t_change);\n"
       "  counter_change();\n"
       "  const Job nx = counter_presented(t_change + 2000);\n"
       "  printf(\"  [x] next round: change at ms %u presented at ms %u (round selected at ms %u)\\n\",\n"
       "         t_change, nx.ms, c1.ms);\n"
       "  if (nx.ms) (void)retire();\n"
       "  d->uns_done_i = 1;\n}\n#else")
open(p, "w").write(s.replace(old, new))

#!/usr/bin/env python3
"""Remove the head's SH1 rider-VO CHECK from a COPY of sim_main.cpp, keeping
the four-tick ticks_follow_the_model, so the suggested tick extension alone
can be graded against listener-rider-not-quiet.
usage: drop_sh1_vo_check.py <copied sim_main.cpp>"""
import sys
p = sys.argv[1]
s = open(p).read()
old = ('  CHECK(h.l_app(1) == VO,\n'
       '        "SH1: a received LeaveAll: the rider takes no event, still VO (rider %s)",\n'
       '        SN[h.l_app(1)]);\n')
assert s.count(old) == 1
open(p, "w").write(s.replace(old, ''))

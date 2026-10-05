#!/usr/bin/env python3
"""Reviewer probe (R489-1-S1 recheck): drop both target Lvs from group S's stimulus.

usage: probe_harness_no_lv.py <tree>; then `make -C <tree>/tb/srp_top run RUN_ARGS=lvleave`.
If S1-S3 still pass, the plain group does not observe that the Lvs were decoded.
"""
import sys

p = sys.argv[1] + "/tb/srp_top/sim_main.cpp"
s = open(p).read()
a = '        lr.vecs.push_back(Vec{false, 1, fv_sid(own_sid(target)), {EV_LV}, {fp}});\n'
b = '        listener_event(target, EV_LV, fp);\n      }\n      const uint32_t lv1_ms'
c = '      listener_event(target, EV_LV, fp);\n      const uint32_t lv2_ms'
for x in (a, b, c):
    assert s.count(x) == 1, x
s = s.replace(a, '').replace(b, '      }\n      const uint32_t lv1_ms').replace(c, '      const uint32_t lv2_ms')
open(p, 'w').write(s)
print('removed both Lvs from group S stimulus')

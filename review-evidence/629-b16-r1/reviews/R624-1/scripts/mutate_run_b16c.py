#!/usr/bin/env python3
"""Plant one defect in a copy of run_b16c.py (B16c run tool) for the offline dry-run harness.

usage: mutate_run_b16c.py <run_b16c.py to edit in place> <R1 no peer restore | R2 DUT set before binds>
"""
import sys
p, mid = sys.argv[1], sys.argv[2]
t = open(p).read()
if mid == "R1":
    old = 'ag = step(ag, "clock-peer", lambda a, s0=src0: setclk(a, "peer", s0, "restore"))'
    new = 'pass  # R1: the peer is not restored'
elif mid == "R2":
    # the restore order inverted: the binds undone after the peer is restored
    old = '        ag = step(ag, "unbind", unbind_all)\n        for w, src0 in clk_changed:\n            if w == "peer":'
    new = '        for w, src0 in clk_changed:\n            if w == "peer":'
    assert t.count(old) == 1
    t = t.replace(old, new)
    old = '        marks_raw["restored"] = RAWT(MONO_RAW)'
    new = '        ag = step(ag, "unbind", unbind_all)\n        marks_raw["restored"] = RAWT(MONO_RAW)'
assert t.count(old) == 1, "anchor not unique"
open(p, "w").write(t.replace(old, new))
print("planted", mid)

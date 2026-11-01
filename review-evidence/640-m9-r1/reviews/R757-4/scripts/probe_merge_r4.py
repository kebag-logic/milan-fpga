#!/usr/bin/env python3
"""Reviewer probes of the listener merge at head 22f3cedb, driving the author's
merge model. Usage: python3 -I probe_merge_r4.py <dir holding merge_model.py>

Arm A: tu on both networks, both delivering, with a tu copy's own time skewed.
       The unchanged model; every copy of every packet is delivered.
Arm B: the sentence "A tu copy with no valid reference cannot make one" applied
       to rule 3's anchor as well, against the unchanged model.
Arm C: a sequence jump on both networks at once, tu on both.
Arm D: control: a tu copy with a valid reference skips rule 1's own-time check
       and is judged by rule 4's counted time alone.
"""
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location("merge_model", os.path.join(sys.argv[1], "merge_model.py"))
m = importlib.util.module_from_spec(spec)
sys.modules["merge_model"] = m
spec.loader.exec_module(m)
Base = m.Pair


class Literal(Base):
    """Rule 3 anchors, but a tu copy with no valid reference makes none."""
    def _anchor(self, port, t, t_id, tu, seq, pkt, c):
        had = c.seq_valid
        pos = self.own_pos(t)
        self.write(pos, pkt, self.now)
        self.head, self.head_pos, self.head_valid = t, pos, True
        self.wmap, self.last_tu, self.anchor_tu = 1, tu, tu
        self.sec += port
        if tu and not had:
            c.last_tu = tu
            return
        self._seen(c, t, tu, seq, t)


class CountOnly(Base):
    """Control: rule 1's time check does not read a referenced tu copy's time."""
    def copy(self, port, now, t, tu, seq, pkt, jumped=False):
        c = self.c[port]
        self.sweep(now)
        if tu and c.seq_valid:
            t_id = self._by_seq(c, seq)
            t = t_id if now < t_id <= now + m.SPAN else now + 1.0
        return Base.copy(self, port, now, t, tu, seq, pkt, jumped)


def run(case, cls=Base):
    m.Pair = cls
    try:
        return m.run(case)
    finally:
        m.Pair = Base


def line(name, r):
    keys = ('missing', 'bad', 'outside', 'late', 'early', 'tu_drop', 'dup', 'jump_dup')
    print(f"  {name}: " + " ".join(f"{k}={r[k]}" for k in keys))


FAST = {1: (60, 180)}
print("Arm A: tu on both from packet 100, both delivering, unchanged model; 3,900 packets carry tu")
print(" A1 both networks at the primary's latency (60-180 us), own-time skew on both copies")
for skew in (0, 200, 500, 700, 750, 800, 850, 1000, 2000):
    line(f"skew +{skew} us", run({'lat': FAST, 'tu': {0: (100, 4000, float(skew), 0.0), 1: (100, 4000, float(skew), 0.0)}}))
print(" A2 both at the primary's latency, negative skew on both copies")
for skew in (-1700, -1800, -1900, -2000):
    line(f"skew {skew} us", run({'lat': FAST, 'tu': {0: (100, 4000, float(skew), 0.0), 1: (100, 4000, float(skew), 0.0)}}))
print(" A3 the fast primary's tu copies early by own time, the slow secondary's fine (LAST_TU stays clear)")
for skew in (800, 1000):
    line(f"primary skew +{skew} us, secondary 0", run({'tu': {0: (100, 4000, float(skew), 0.0), 1: (100, 4000, 0.0, 0.0)}}))
print(" A4 a tu period that ends, both at the primary's latency, skew +1000 us: tu 100 to 600")
line("skew +1000 us", run({'lat': FAST, 'tu': {0: (100, 600, 1000.0, 0.0), 1: (100, 600, 1000.0, 0.0)}}))
print(" A5 primary cut at 1000, secondary tu 1200 to 3200: page says the audio gaps up to one presentation offset")
for skew in (500, 1500, 2500):
    line(f"skew +{skew} us", run({'cut': {0: 1000}, 'tu': {1: (1200, 3200, float(skew), 0.0)}}))

print("Arm B: tu from the first packet; unchanged model against the literal sentence")
for name, case in (
    ("unpaired, tu from packet 0", {'cut': {1: 0}, 'tu': {0: (0, 4000, 0.0, 0.0)}}),
    ("tu on both from packet 0", {'tu': {0: (0, 4000, 0.0, 0.0), 1: (0, 4000, 0.0, 0.0)}}),
    ("tu on both from packet 0, secondary faster", {'sec_fast': True, 'tu': {0: (0, 4000, 0.0, 0.0), 1: (0, 4000, 0.0, 0.0)}}),
    ("secondary tu from packet 0, skew -200 us, arrives first (the model's own startup case)",
     {'sec_fast': True, 'tu': {1: (0, 4000, -200.0, 20.0)}}),
):
    line(name + " [model]", run(case))
    line(name + " [literal]", run(case, Literal))

print("Arm C: tu on both from 100, both sequences jump at packet 1000; 22 packets is the stated unpaired gap")
for d in (40, -40):
    for fast in (False, True):
        c = {'tu': {0: (100, 4000, 0.0, 0.0), 1: (100, 4000, 0.0, 0.0)}, 'seqjump': {0: (1000, d), 1: (1000, d)}}
        if fast:
            c['sec_fast'] = True
        line(f"jump {d:+d}{', secondary faster' if fast else ''}", run(c))

print("Arm D: control, a referenced tu copy judged by its counted time only")
for skew in (1000, 2000, 5000):
    line(f"tu on both, same latency, skew +{skew} us", run({'lat': FAST, 'tu': {0: (100, 4000, float(skew), 0.0), 1: (100, 4000, float(skew), 0.0)}}, CountOnly))
line("primary +1000, secondary 0", run({'tu': {0: (100, 4000, 1000.0, 0.0), 1: (100, 4000, 0.0, 0.0)}}, CountOnly))
line("primary cut 1000, secondary tu 1200-3200 skew +2500", run({'cut': {0: 1000}, 'tu': {1: (1200, 3200, 2500.0, 0.0)}}, CountOnly))
ok = fails = 0
for name, case, want in m.CASES:
    if m.judge(run(case, CountOnly), want, case):
        ok += 1
    else:
        fails += 1
        print("  model case changes under the control:", name)
print(f"  the model's own 33 cases under the control: {ok} pass, {fails} change")

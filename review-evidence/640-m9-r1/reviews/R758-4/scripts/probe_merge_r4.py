#!/usr/bin/env python3
"""Falsifying probes on the published round-4 merge model (uses it unchanged
except where a probe says it models the page's literal text).
Usage: python3 -I probe_merge_r4.py <dir holding merge_model.py>"""
import random
import sys

sys.path.insert(0, sys.argv[1])
import merge_model as m  # noqa: E402


def show(name, case, mut=None, want=None):
    r = m.run(case, mut)
    keys = ('bad', 'missing', 'extra', 'dup', 'tu_drop', 'late', 'early', 'outside', 'jump_dup')
    print(f"{name}: " + ' '.join(f"{k}={r[k]}" for k in keys))
    return r


FAST = {'lat': {1: (60, 180)}}
N = 4000

print("A. tu on both, the copies' own time skewed; rule 1 still reads that time")
for skew in (200.0, 500.0, 700.0, 1000.0, 2000.0, -1000.0, -1900.0, -2500.0, 5000.0):
    show(f"  both networks at the primary's latency, tu 100 to 600, skew {skew:+.0f} us",
         dict(FAST, tu={0: (100, 600, skew, 0.0), 1: (100, 600, skew, 0.0)}))
for skew in (700.0, 1000.0, 2000.0, -1000.0, -2500.0):
    show(f"  model's latencies (secondary 1.1-1.5 ms), tu 100 to 600, skew {skew:+.0f} us",
         {'tu': {0: (100, 600, skew, 0.0), 1: (100, 600, skew, 0.0)}})
print("A control: same skews on the primary only, secondary clean and slower")
for skew in (1000.0, -2500.0):
    show(f"  primary tu 100 to 600, skew {skew:+.0f} us", {'tu': {0: (100, 600, skew, 0.0)}})
print("A control: unpaired stream with the same tu and skew")
for skew in (200.0, 1000.0, -2500.0):
    show(f"  unpaired, tu 100 to 600, skew {skew:+.0f} us",
         {'cut': {1: 0}, 'tu': {0: (100, 600, skew, 0.0)}})


class LiteralNoRef(m.Pair):
    """The page's sentence 'A tu copy with no valid reference cannot make one'
    applied to rule 3's anchoring copy too."""

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


def run_cls(cls, case):
    orig = m.Pair
    m.Pair = cls
    try:
        return m.run(case)
    finally:
        m.Pair = orig


print("B. does a tu anchor make a reference? model anchors make one; the page says none")
for name, case in (("unpaired, tu from the first packet", {'cut': {1: 0}, 'tu': {0: (0, 4000, 0.0, 0.0)}}),
                   ("unpaired, tu from 100, jump -40 at 1000", {'cut': {1: 0}, 'tu': {0: (100, 4000, 0.0, 0.0)}, 'seqjump': {0: (1000, -40)}}),
                   ("unpaired, tu from 100, jump +40 at 1000", {'cut': {1: 0}, 'tu': {0: (100, 4000, 0.0, 0.0)}, 'seqjump': {0: (1000, 40)}})):
    a = m.run(case)
    b = run_cls(LiteralNoRef, case)
    print(f"  {name}: model missing={a['missing']} bad={a['bad']}; literal text missing={b['missing']} bad={b['bad']}")


def step_run(step, c0, c1, lat1=(1100, 1500), ports=(0, 1), n=4000, seed=1):
    """Time step as tu clears; the networks clear at packets c0 and c1."""
    rnd = random.Random(seed)
    drift = 150e-6
    t0 = 10_000.0 + 7.3
    lat = {0: (60, 180), 1: lat1}
    seq0 = {0: 17, 1: 201}
    ev = []
    for j in range(n):
        tj = t0 + j * m.T * (1 + drift)
        for port in ports:
            t = tj + (rnd.uniform(-m.E_X, m.E_X) if port == 1 else 0.0)
            a = tj - m.PTO + rnd.uniform(*lat[port])
            clr = c0 if port == 0 else c1
            tu = 100 <= j < clr
            if j >= clr:
                t += step
            ev.append((a, port, t, tu, (seq0[port] + j) % 256, j))
    ev.sort()
    p = m.Pair(set())
    p.trec = m.T * (1 + drift)
    for a, port, t, tu, seq, j in ev:
        p.copy(port, a, t, tu, seq, j)
    written = {pkt for (pkt, i) in p.buf.values()}
    miss = [j for j in range(n) if j not in written]
    return len(miss), p.outside, p.rewrites


print("C. time step as tu clears, networks clearing apart: packets never written, outside, rewrites")
for st in (-1000, -300, 100, 300, 1000):
    one = step_run(st, 600, 600, ports=(0,))
    row = [f"one network {one}"]
    for c0, c1 in ((600, 600), (600, 604), (604, 600), (600, 640), (640, 600)):
        row.append(f"clear {c0}/{c1} {step_run(st, c0, c1)}")
    print(f"  step {st:+5d} " + ' | '.join(row))
print("C2. same, both networks at the primary's latency")
for st in (-1000, -300, 100, 300, 1000):
    one = step_run(st, 600, 600, ports=(0,))
    row = [f"one network {one}"]
    for c0, c1 in ((600, 600), (600, 604), (604, 600)):
        row.append(f"clear {c0}/{c1} {step_run(st, c0, c1, lat1=(60, 180))}")
    print(f"  step {st:+5d} " + ' | '.join(row))

print("D. arrival margin near the render point: reference lapses between packets")
for lo, hi in ((1800, 1850), (1880, 1890), (1900, 1950), (1950, 1990)):
    show(f"  tu on both, secondary arrives {2000-hi}-{2000-lo} us before its time",
         {'lat': {1: (lo, hi)}, 'tu': {0: (100, 600, 0.0, 0.0), 1: (100, 600, 0.0, 0.0)}})
    show(f"  tu on both, both arrive {2000-hi}-{2000-lo} us before their time",
         {'lat': {0: (lo, hi), 1: (lo, hi)}, 'tu': {0: (100, 600, 0.0, 0.0), 1: (100, 600, 0.0, 0.0)}})
    show(f"  unpaired tu, arrives {2000-hi}-{2000-lo} us before its time",
         {'lat': {0: (lo, hi)}, 'cut': {1: 0}, 'tu': {0: (100, 600, 0.0, 0.0)}})

print("E. burst loss on one network during tu on both (reference lapses: stated as rejoining)")
for b in (0.0,):
    show("  tu on both, 1 % loss on both", {'loss': {0: 0.01, 1: 0.01}, 'tu': {0: (100, 4000, 0.0, 0.0), 1: (100, 4000, 0.0, 0.0)}})
    show("  secondary fast with tu, primary 1 % loss", {'sec_fast': True, 'loss': {0: 0.01}, 'tu': {1: (100, 4000, 0.0, 0.0)}})

print("F. sequence step inside the span (open design item 2)")
for port_tu, name in (({0: (100, 4000, 0.0, 0.0), 1: (100, 4000, 0.0, 0.0)}, 'tu on both'),):
    show(f"  {name}, secondary steps +3 at 1000", {'tu': port_tu, 'seqjump': {1: (1000, 3)}})
show("  unpaired, tu, steps +3 at 1000", {'cut': {1: 0}, 'tu': {0: (100, 4000, 0.0, 0.0)}, 'seqjump': {0: (1000, 3)}})
show("  secondary tu, primary clean with 1 % loss, secondary steps +3 at 1000",
     {'loss': {0: 0.01}, 'tu': {1: (100, 4000, 0.0, 0.0)}, 'seqjump': {1: (1000, 3)}})

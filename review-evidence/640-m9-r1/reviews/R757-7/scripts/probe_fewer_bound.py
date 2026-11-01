#!/usr/bin/env python3
"""Does the page publish a bound for every fewer-reservations case?

Independent implementation of docs/design/MARK_II_STREAM_ENGINES.md at the
head under review: Table 4.4 frames and reservations, the phase rule (least
wire time, fixed spread tie order, never re-phased), the FIFO recursion of the
class A shaper, and the page's fixed terms. Calibration reproduces the page's
own rows before any new case is reported. No timing here is a measurement.
Usage: python3 -I probe_fewer_bound.py [seed]
"""
import random, sys
from fractions import Fraction as Fr

NS = {48: 6, 96: 12, 192: 24}
FIXED = {48: Fr(40325, 1000), 96: Fr(32491, 1000)}
FIXED_192_NO_PACKETIZER = Fr(18093, 1000)
FORMATS = (1, 2, 4, 6, 8)
def L(r, n): return 8 * (max(24 + NS[r] * 4 * n + 22, 68) + 20)
def RES(r, n): return 8 * (max(24 + NS[r] * 4 * n + 1 + 22, 68) + 20)
def spread(P):
    if P == 6: return [0, 3, 1, 4, 2, 5]
    out, k = [], 1
    while len(out) < P:
        for j in range(k):
            p = j * P // k
            if p not in out: out.append(p)
        k *= 2
    return out

class Port:
    def __init__(s, r):
        s.r, s.P = r, NS[r]
        s.tie = spread(s.P)
        s.ph = [[] for _ in range(s.P)]
    def start(s, n):
        p = min(s.tie, key=lambda q: (sum(L(s.r, m) for m in s.ph[q]), s.tie.index(q)))
        s.ph[p].append(n); return p
    def stop(s, p, n): s.ph[p].remove(n)
    def count(s): return sum(map(len, s.ph))
    def wait(s):
        a = Fr(sum(RES(s.r, n) for q in s.ph for n in q), 125)
        if not a: return Fr(0)
        fr = [(Fr(125 * p, s.P) + 125 * i, L(s.r, n), n) for i in range(3)
              for p in range(s.P) for n in sorted(s.ph[p])]
        free, worst = Fr(-10**6), Fr(0)
        for t, bits, _ in fr:
            st = max(t, free); worst = max(worst, st - t); free = st + bits / a
        return worst

def fixed_port(r, layout):
    p = Port(r)
    for ph, ns in layout.items(): p.ph[ph] = list(ns)
    return p

print("== calibration against the page's rows at 48 kHz")
for name, lay, want_w, want_t in (
    ("two in phase 0", {0: [8, 8]}, "62.259", "102.584"),
    ("three in phase 0", {0: [8, 8, 8]}, "83.012", "123.337"),
    ("two, phases 0 and 1", {0: [8], 1: [8]}, "41.425", "81.750"),
    ("two, phases 0 and 3", {0: [8], 3: [8]}, "0.000", "40.325")):
    w = fixed_port(48, lay).wait()
    print(f"{name}: wait {float(w):.3f} (page {want_w}); total {float(w + FIXED[48]):.3f} (page {want_t})")
w = fixed_port(48, {0: [8, 8, 8], 1: [2] * 5, 2: [1] * 3, 3: [1] * 2, 4: [1] * 2, 5: [1]}).wait()
print(f"16-reservation mix of 'What the rule cannot prevent': wait {float(w):.3f} (page 53.085)")

print("\n== witness: only starts and stops under the exact phase rule, 48 kHz")
p = Port(48); log = []
def st(n):
    q = p.start(n); log.append(f"start N={n} -> phase {q}")
st(1)
for _ in range(5): st(8)
st(1); st(1)
for _ in range(5): st(8)
for _ in range(3): st(1)
print("; ".join(log)); print("at 16 streams:", p.ph, "count", p.count())
for q in range(6):
    for n in list(p.ph[q]):
        if n == 8: p.stop(q, n)
print("after stopping every eight-channel stream:", p.ph)
w = p.wait(); idle = Fr(sum(RES(48, n) for q in p.ph for n in q), 125)
print(f"idleSlope {float(idle):.3f} Mb/s; last frame's wait {float(w):.3f} us; "
      f"total with every fixed term {float(w + FIXED[48]):.3f} us; page's largest fewer-reservations row 123.337 us")

print("\n== constructive search: k co-phased N-channel streams alone, helpers stopped")
for r in (48, 96, 192):
    best = None
    for n in FORMATS:
        if r == 192 and n == 8: continue
        for k in range(1, 17):
            q = Port(r); phase0 = 0; ok = True
            helper = 6 if r == 192 else 8
            for _ in range(k):
                # give every other phase enough helpers that the rule picks phase 0
                while True:
                    load0 = sum(L(r, m) for m in q.ph[0])
                    light = [x for x in range(1, q.P) if sum(L(r, m) for m in q.ph[x]) < load0]
                    # tie order: phase 0 wins ties
                    if not light: break
                    if q.count() >= 16: ok = False; break
                    x = q.start(helper)
                    if x == 0: ok = False; break
                if not ok: break
                if q.count() >= 16: ok = False; break
                if q.start(n) != 0: ok = False; break
            if not ok or len([m for m in q.ph[0] if m == n]) != k: continue
            c = fixed_port(r, {0: [n] * k})
            w = c.wait()
            total = w + (FIXED[r] if r in FIXED else FIXED_192_NO_PACKETIZER)
            if best is None or total > best[0]: best = (total, n, k, w)
    print(f"{r} kHz: largest reached N={best[1]} k={best[2]}: wait {float(best[3]):.3f}, "
          f"total {float(best[0]):.3f}" + (" (excludes the packetizer term)" if r == 192 else ""))

print("\n== random start/stop walks under the exact rule, fewest-stream cases included")
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 640
rng = random.Random(seed)
for r in (48, 96, 192):
    fmts = FORMATS if r != 192 else FORMATS[:-1]
    top, arg = Fr(0), None
    for walk in range(300):
        q = Port(r)
        for step in range(120):
            cnt = q.count()
            if cnt and (cnt >= 16 or rng.random() < .45):
                occ = [(x, m) for x in range(q.P) for m in q.ph[x]]
                q.stop(*rng.choice(occ))
            else:
                q.start(rng.choice(fmts))
            if step % 3 == 0 and q.count():
                w = q.wait()
                if w > top: top, arg = w, ([list(x) for x in q.ph], q.count())
    t = top + (FIXED[r] if r in FIXED else FIXED_192_NO_PACKETIZER)
    print(f"{r} kHz: largest wait {float(top):.3f}, total {float(t):.3f}, with {arg[1]} streams: {arg[0]}")

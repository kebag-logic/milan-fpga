#!/usr/bin/env python3
"""Sweep of a time step as tu clears with the networks clearing apart, against
one network alone, on the published merge model.
Usage: python3 -I probe_tu_step_apart.py <dir holding merge_model.py>"""
import random
import sys

sys.path.insert(0, sys.argv[1])
import merge_model as m  # noqa: E402


def run(step, c0, c1, lat1=(1100, 1500), ports=(0, 1), n=4000, seed=1):
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
    return len([j for j in range(n) if j not in written])


worst = {}
for st in (-1000, -700, -500, -300, -200, -100, 100, 300, 500, 700, 1000):
    alone = min(run(st, 600, 600, ports=(0,)), run(st, 600, 600, lat1=(1100, 1500), ports=(1,)))
    alone_p = run(st, 600, 600, ports=(0,))
    alone_s = run(st, 600, 600, ports=(1,))
    best = (0, None)
    for d in range(-80, 81, 2):
        c0, c1 = (600, 600 + d) if d >= 0 else (600 - d, 600)
        for lat1 in ((1100, 1500), (60, 180)):
            v = run(st, c0, c1, lat1=lat1)
            if v > best[0]:
                best = (v, (c0, c1, lat1))
    print(f"step {st:+5d}: primary alone {alone_p}, secondary alone {alone_s}; pair worst {best[0]} at {best[1]}")

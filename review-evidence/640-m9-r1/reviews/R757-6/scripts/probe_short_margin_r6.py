#!/usr/bin/env python3
"""Page-derived check of SE:624, :627-628, :660 and item 3 at the reviewed head.

Written from the page's rules alone: the head takes its copy's own time, a head
whose time the render point passed is invalid (rule 2), otherwise rule 4, 5 or 6
places by count. Every copy is clean and no time steps. A margin is the time a
copy arrives before its own time. Each row runs 64 grid phases of 2,000 packets.
"""
import math
import random

T = 125.0
EX = 2.744
RATES = ((48, 6), (96, 12), (192, 24))


def run(ns, phase, margins, n=2000, seed=1, drift=150e-6, loss=0.0, jitter=True):
    rnd = random.Random(seed)
    per = T * (1 + drift)
    spr = per / ns
    t0 = 400 * spr + phase * spr
    arr = []
    for j in range(n):
        tj = t0 + j * per
        err = rnd.uniform(-EX, EX) if jitter else 0.0
        for port, band in enumerate(margins):
            if band is None or rnd.random() < loss:
                continue
            t = tj + (err if port else 0.0)
            arr.append((t - rnd.uniform(*band), port, t, j))
    arr.sort()
    head = pos = None
    wmap = 0
    placed = {}
    anchors = 0
    for now, _port, t, j in arr:
        if head is None or head <= now:
            head, pos, wmap = t, math.floor(t / spr + 1e-9), 1
            anchors += 1
            placed.setdefault(j, pos)
            continue
        k = round((t - head) / T)
        if k >= 1:
            pos += ns * k
            wmap = ((wmap << k) | 1) & ((1 << 22) - 1)
            head = t
            placed.setdefault(j, pos)
        elif not (wmap >> -k) & 1:
            wmap |= 1 << -k
            placed.setdefault(j, pos + ns * k)
    err = [placed[j] - placed[j - 1] - ns for j in range(1, n) if j in placed and j - 1 in placed]
    return anchors, sum(1 for e in err if e), max((abs(e) for e in err), default=0), sum(e for e in err if e > 0)


def row(name, margins, **kw):
    for rate, ns in RATES:
        rs = [run(ns, p / 64, margins, seed=p + 1, **kw) for p in range(64)]
        print(f"{name} | {rate} kHz | anchors min/max {min(r[0] for r in rs)}/{max(r[0] for r in rs)}"
              f" | phases with a shift {sum(1 for r in rs if r[1])}/64 | worst shifts {max(r[1] for r in rs)}"
              f" | largest step error {max(r[2] for r in rs)} | worst unwritten {max(r[3] for r in rs)}")


print('A. Both networks, first arrival interleaved: is the head lapsed every packet under 125 us, and only there?')
for lo, hi in ((10, 50), (50, 100), (110, 120), (124.0, 124.9), (125.2, 126.0), (130, 140), (150, 200)):
    row(f"both {lo} to {hi} us", ((lo, hi), (lo, hi)))
print('B. Margins straddling 125 us on both networks')
row('both 100 to 150 us', ((100, 150), (100, 150)))
print('C. A short margin on one network only: does it lapse the head?')
row('primary 150 to 200, secondary 10 to 50', ((150, 200), (10, 50)))
row('primary 10 to 50, secondary 150 to 200', ((10, 50), (150, 200)))
print('D. SE:624 and SE:660: valid head, conversion error at its bound, interleaved, with and without loss')
row('both 150 to 200, 2.744 us error', ((150, 200), (150, 200)))
row('both 150 to 200, 2.744 us error, 1 % loss each', ((150, 200), (150, 200)), loss=0.01)
row('both 1,800 to 1,950, 2.744 us error', ((1800, 1950), (1800, 1950)))
print('E. Short margin without interleaving')
row('primary 110 to 120 first, secondary 10 to 50', ((110, 120), (10, 50)))
row('one network, 10 to 50, no jitter', ((10, 50), None), jitter=False)
print('F. Short margin, partners differing by a fixed 2.744 us (no packet-to-packet jitter)')


def fixed(ns, phase, n=2000, seed=1):
    rnd = random.Random(seed)
    per = T * (1 + 150e-6)
    spr = per / ns
    t0 = 400 * spr + phase * spr
    arr = []
    for j in range(n):
        tj = t0 + j * per
        for port in (0, 1):
            t = tj + (EX if port else 0.0)
            arr.append((t - rnd.uniform(10, 50), port, t, j))
    arr.sort()
    head = None
    placed = {}
    for now, _p, t, j in arr:
        if head is None or head <= now:
            head = t
            placed.setdefault(j, math.floor(t / spr + 1e-9))
    return [placed[j] - placed[j - 1] - ns for j in range(1, n) if j in placed and j - 1 in placed]


for rate, ns in RATES:
    es = [fixed(ns, p / 64, seed=p + 1) for p in range(64)]
    print(f"fixed 2.744 us | {rate} kHz | phases with a shift {sum(1 for e in es if any(e))}/64"
          f" | largest step error {max(max(abs(x) for x in e) for e in es)}")

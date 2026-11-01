#!/usr/bin/env python3
"""Clean copies on both networks with an arrival margin under one packet
interval, by the page's rule table at the reviewed head. Every copy is clean,
no frame is lost and no time steps.

A head whose time the render point passed is invalid (rule 2), so with such a
margin each packet is a new anchor at its own time. This probe measures how
often consecutive packets then land other than one packet of samples apart.

It also runs the round-4 model's clean path on the same arrivals, as a second
implementation, and a variant that keeps the head for counting until 1.5
intervals past the render point, to show that the shift comes from the lapse.

Usage: python3 -I probe_margin_r5.py <dir holding merge_model.py>
"""
import math
import random
import sys

sys.path.insert(0, sys.argv[1])
import merge_model as mm  # noqa: E402

T = 125.0
SPAN = 8000.0 / 3
PTO = 2000.0
EX = 2.744
DRIFT = 150e-6


def simulate(ns, lat, phase_us, n=2000, seed=1, hold=0.0, paired=True):
    rnd = random.Random(seed)
    spr = T / ns * (1 + DRIFT)
    t0 = round(10_000.0 / spr) * spr + phase_us
    ev = []
    for j in range(n):
        tj = t0 + j * T * (1 + DRIFT)
        for port in ((0, 1) if paired else (0,)):
            t = tj + (rnd.uniform(-EX, EX) if port == 1 else 0.0)
            ev.append((tj - PTO + rnd.uniform(*lat[port]), port, t, j))
    ev.sort()
    head = pos = None
    valid = False
    wmap = 0
    first = {}
    anchors = dup = 0
    for now, port, t, j in ev:
        if t <= now or t > now + SPAN:
            continue
        own = math.floor(t / spr + 1e-9)
        if not valid or head + hold <= now:
            head, pos, valid, wmap = t, own, True, 1
            first[j] = own
            anchors += 1
            continue
        k = round((t - head) / T)
        if k >= 1:
            pos += ns * k
            wmap = ((wmap << k) | 1) & ((1 << 22) - 1)
            head = t
            first.setdefault(j, pos)
        elif not (wmap >> -k) & 1:
            first.setdefault(j, pos + ns * k)
            wmap |= 1 << -k
        else:
            dup += 1
    steps = [first[j] - first[j - 1] for j in range(1, n) if j in first and j - 1 in first]
    shifts = sum(1 for s in steps if s != ns)
    return dict(anchors=anchors, dup=dup, shifts=shifts, gap=sum(s - ns for s in steps if s > ns),
                overlap=sum(ns - s for s in steps if s < ns), packets=len(first))


SHORT = {0: (1950, 1990), 1: (1950, 1990)}
print('A. Both networks 10 to 50 us before their time; 64 phases of the sample grid; 2,000 packets (0.25 s) each')
for rate, ns in ((48, 6), (96, 12), (192, 24)):
    sp = T / ns
    rows = [simulate(ns, SHORT, sp * p / 64, seed=p + 1) for p in range(64)]
    hit = sum(1 for r in rows if r['shifts'])
    print(f"  {rate} kHz: sample period {sp:.3f} us; phases with a shift {hit}/64;"
          f" worst shifts in 0.25 s {max(r['shifts'] for r in rows)};"
          f" worst samples left unwritten {max(r['gap'] for r in rows)};"
          f" anchors per run {rows[0]['anchors']}; lost packets {2000 - min(r['packets'] for r in rows)}")
print('B. Controls at 48 and 192 kHz, same phases')
CONTROL = [
    ('margin 150 to 200 us on both', {0: (1800, 1850), 1: (1800, 1850)}, 0.0, True),
    ('primary 60 to 180 us latency, secondary 10 to 50 us margin', {0: (60, 180), 1: (1950, 1990)}, 0.0, True),
    ('primary margin 110 to 120 us, secondary margin 10 to 50 us: primary always first',
     {0: (1880, 1890), 1: (1950, 1990)}, 0.0, True),
    ('one network only, margin 10 to 50 us', SHORT, 0.0, False),
    ('both margin 10 to 50 us, head kept for count 1.5 intervals past the render point', SHORT, 187.5, True),
]
for name, lat, hold, paired in CONTROL:
    for rate, ns in ((48, 6), (192, 24)):
        sp = T / ns
        rows = [simulate(ns, lat, sp * p / 64, seed=p + 1, hold=hold, paired=paired) for p in range(64)]
        print(f"  {name}, {rate} kHz: phases with a shift {sum(1 for r in rows if r['shifts'])}/64;"
              f" worst shifts {max(r['shifts'] for r in rows)}; anchors {rows[0]['anchors']}")
print('C. The round-4 model, clean copies only, unchanged, same setup at 48 kHz')
for name, case in (
    ('both 10 to 50 us, 1 us past a boundary', {'lat': {0: (1950, 1990), 1: (1950, 1990)}, 'past_boundary': 1.0}),
    ('both 150 to 200 us, 1 us past a boundary', {'lat': {0: (1800, 1850), 1: (1800, 1850)}, 'past_boundary': 1.0}),
):
    r = mm.run(case)
    print(f"  {name}: align={r['align']} bad={r['bad']} missing={r['missing']} rewrites={r['rewrites']}")

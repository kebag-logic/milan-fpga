#!/usr/bin/env python3
"""Falsification probe for the page's short-margin text: same arrival and rule
core as the published round-5 probe, with margin bands around 125 us, one-copy
short margins, a step histogram and the distance between partner copies.

Usage: python3 -I probe_margin_r6.py
"""
import collections
import math
import random

T = 125.0
SPAN = 8000.0 / 3
PTO = 2000.0
EX = 2.744
DRIFT = 150e-6


def simulate(ns, marg, phase_us, n=2000, seed=1, err="iid"):
    rnd = random.Random(seed)
    spr = T / ns * (1 + DRIFT)
    t0 = round(10_000.0 / spr) * spr + phase_us
    ev = []
    for j in range(n):
        tj = t0 + j * T * (1 + DRIFT)
        for port in (0, 1):
            if port == 0:
                e = 0.0
            elif err == "iid":
                e = rnd.uniform(-EX, EX)
            else:
                e = EX * math.sin(2 * math.pi * j / 4000.0)
            t = tj + e
            ev.append((t - rnd.uniform(*marg[port]), port, t, j))
    ev.sort()
    head = pos = None
    valid = False
    wmap = 0
    first = {}
    own_by = {}
    anchors = 0
    for now, port, t, j in ev:
        own_by.setdefault(j, {})[port] = math.floor(t / spr + 1e-9)
        if t <= now or t > now + SPAN:
            continue
        own = math.floor(t / spr + 1e-9)
        if not valid or head <= now:
            head, pos, valid, wmap = t, own, True, 1
            first.setdefault(j, own)
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
    hist = collections.Counter(first[j] - first[j - 1] - ns for j in range(1, n) if j in first and j - 1 in first)
    apart = max(abs(v[0] - v[1]) for v in own_by.values() if len(v) == 2)
    return anchors, hist, apart


def band(name, marg, err="iid"):
    for rate, ns in ((48, 6), (96, 12), (192, 24)):
        sp = T / ns
        tot = collections.Counter()
        anch = []
        apart = 0
        hit = 0
        for p in range(64):
            a, h, d = simulate(ns, marg, sp * p / 64, seed=p + 1, err=err)
            anch.append(a)
            tot.update(h)
            apart = max(apart, d)
            hit += any(k != 0 for k in h)
        steps = {k: tot[k] for k in sorted(tot) if k}
        print(f"  {name}, {rate} kHz: anchors {min(anch)}..{max(anch)} of 2000; phases with a shift {hit}/64;"
              f" step offsets in samples {steps}; partner copies at most {apart} samples apart")


both = lambda lo, hi: {0: (lo, hi), 1: (lo, hi)}
print("A. Both networks, margin bands around 125 us, jitter as the published probe")
for lo, hi in ((10, 50), (100, 120), (120, 122), (122.3, 124.9), (125.1, 127.6), (127.8, 130), (150, 200)):
    band(f"margin {lo} to {hi} us", both(lo, hi))
print("B. Short margin on one network only, the other at 150 to 200 us")
band("primary 150 to 200, secondary 10 to 50", {0: (150, 200), 1: (10, 50)})
band("primary 10 to 50, secondary 150 to 200", {0: (10, 50), 1: (150, 200)})
print("C. Both 10 to 50 us, secondary error slow (sine, 2.744 us peak over 0.5 s)")
band("slow error", both(10, 50), err="slow")


def counted(ns, marg, phase, n=2000, seed=1, map_on_anchor=1):
    """Rule table with a counter of counted placements whose k disagrees with
    the true packet distance, and the writes a partner gets after an anchor."""
    rnd = random.Random(seed)
    spr = T / ns * (1 + DRIFT)
    t0 = round(10_000.0 / spr) * spr + phase
    ev = []
    for j in range(n):
        tj = t0 + j * T * (1 + DRIFT)
        for port in (0, 1):
            t = tj + (rnd.uniform(-EX, EX) if port else 0.0)
            ev.append((t - rnd.uniform(*marg[port]), port, t, j))
    ev.sort()
    head = hj = None
    valid = False
    wmap = 0
    wrong = dups = rewrites = 0
    written = collections.Counter()
    for now, port, t, j in ev:
        if t <= now or t > now + SPAN:
            continue
        if not valid or head <= now:
            head, hj, valid, wmap = t, j, True, map_on_anchor
            written[j] += 1
            continue
        k = round((t - head) / T)
        wrong += k != j - hj
        if k >= 1:
            wmap = ((wmap << k) | 1) & ((1 << 22) - 1)
            head, hj = t, j
            written[j] += 1
        elif not (wmap >> -k) & 1:
            wmap |= 1 << -k
            written[j] += 1
        else:
            dups += 1
    rewrites = sum(v - 1 for v in written.values() if v > 1)
    return wrong, dups, rewrites


print("D. Rule table: counted placements whose k disagrees with the packet; duplicates; packets written twice")
for name, m in (("both 10 to 50", both(10, 50)), ("both 150 to 200", both(150, 200))):
    for label, bit0 in (("restart map with only bit 0", 1), ("clear the map entirely", 0)):
        r = [counted(ns, m, T / ns * p / 64, seed=p + 1, map_on_anchor=bit0) for ns in (6, 12, 24) for p in range(64)]
        print(f"  {name}, {label}: wrong k {sum(x[0] for x in r)}; duplicates worst {max(x[1] for x in r)};"
              f" packets written twice worst {max(x[2] for x in r)}")

print("E. Margins small enough that a partner can arrive after the head's time passed")
for lo, hi in ((0.1, 2.0), (2.0, 5.0), (5.0, 10.0), (10.0, 50.0)):
    r = [counted(ns, both(lo, hi), T / ns * p / 64, seed=p + 1) for ns in (6, 12, 24) for p in range(64)]
    print(f"  both {lo} to {hi} us: duplicates fewest {min(x[1] for x in r)} of 2000;"
          f" packets written twice worst {max(x[2] for x in r)}")

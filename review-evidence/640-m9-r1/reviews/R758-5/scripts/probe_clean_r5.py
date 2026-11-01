#!/usr/bin/env python3
"""Clean-copy merge built only from the rule table of the stream-engine page at
the reviewed head (rules 1 to 6, head upkeep, placement by count). It shares no
code with the earlier merge model.

Checks each case on the page's clean verification row and adds stimuli the row
does not name. Prints how often each rule fired, so a reader can see which
rules the named cases reach. The two mutations are the row's: an exact time
compare, and each copy placed by its own time.

Usage: python3 -I probe_clean_r5.py
"""
import math
import random

T = 125.0
NS = 6
SP = T / NS
SPAN = 8000.0 / 3
PTO = 2000.0
MAPBITS = 22
EX = 2.744
DRIFT = 150e-6


class Merge:
    def __init__(self, mut=None):
        self.mut = mut
        self.head = self.pos = None
        self.valid = False
        self.wmap = 0
        self.buf = {}
        self.hits = [0] * 7
        self.dup = self.sec = self.late = self.early = self.outside = 0
        self.dropped_only = 0
        self.rate = T * (1 + DRIFT) / NS

    def own(self, t):
        return math.floor(t / self.rate + 1e-9)

    def write(self, pos, pkt, now):
        rp = self.own(now)
        for i in range(NS):
            if not rp <= pos + i < rp + 128:
                self.outside += 1
            self.buf[pos + i] = (pkt, i)

    def anchor(self, port, t, pkt, now, rule):
        self.hits[rule] += 1
        self.pos = self.own(t)
        self.write(self.pos, pkt, now)
        self.head, self.valid, self.wmap = t, True, 1
        self.sec += port

    def copy(self, port, now, t, pkt):
        if t <= now:
            self.hits[1] += 1
            self.late += 1
            return
        if t > now + SPAN:
            self.hits[1] += 1
            self.early += 1
            return
        if not self.valid or self.head <= now:
            return self.anchor(port, t, pkt, now, 2)
        d = t - self.head
        if self.mut == 'exact':
            k = 0 if d == 0 else (math.ceil(d / T) if d > 0 else -math.ceil(-d / T))
        else:
            k = round(d / T)
        if abs(k) > 21:
            return self.anchor(port, t, pkt, now, 3)
        if k >= 1:
            self.hits[4] += 1
            pos = self.pos + NS * k
            if self.mut == 'own_time':
                pos = self.own(t)
            self.write(pos, pkt, now)
            self.wmap = ((self.wmap << k) | 1) & ((1 << MAPBITS) - 1)
            self.head, self.pos = t, pos
            self.sec += port
        elif not (self.wmap >> -k) & 1:
            self.hits[5] += 1
            pos = self.pos + NS * k
            if self.mut == 'own_time':
                pos = self.own(t)
            self.write(pos, pkt, now)
            self.wmap |= 1 << -k
            self.sec += port
        else:
            self.hits[6] += 1
            self.dup += 1


def run(case, mut=None, n=4000, seed=1):
    rnd = random.Random(seed)
    spr = SP * (1 + DRIFT)
    t0 = 10_000.0 + 7.3
    if 'past' in case:
        t0 = round(t0 / spr) * spr + case['past']
    lat = {0: (60, 180), 1: (1100, 1500)}
    if case.get('sec_fast'):
        lat = {0: (1100, 1500), 1: (60, 180)}
    lat.update(case.get('lat', {}))
    ev = []
    sent = {}
    for j in range(n):
        tj = t0 + j * T * (1 + DRIFT)
        for port in (0, 1):
            if j >= case.get('cut', {}).get(port, n):
                continue
            if rnd.random() < case.get('loss', {}).get(port, 0.0):
                continue
            t = tj + (rnd.uniform(-EX, EX) if port == 1 else 0.0)
            a = tj - PTO + rnd.uniform(*lat[port])
            step = case.get('step')
            if step and j >= step[0]:
                t += step[1]
                a += step[1]
            phase = 1 if step and j >= step[0] else 0
            ev.append((phase, a, port, t, j))
            sent[j] = sent.get(j, 0) + 1
    ev.sort()
    m = Merge(mut)
    for _, a, port, t, j in ev:
        m.copy(port, a, t, j)
    base = None
    tb = math.floor(t0 / spr + 1e-9)
    for b in (tb - 1, tb, tb + 1):
        if m.buf.get(b) == (0, 0):
            base = b
    if base is None:
        base = tb
    bad = missing = 0
    sent_missing = 0
    for j in range(n):
        lost = 0
        for i in range(NS):
            got = m.buf.get(base + NS * j + i)
            if got is None:
                missing += 1
                lost += 1
            elif got != (j, i):
                bad += 1
        if j in sent:
            sent_missing += lost
    return dict(bad=bad, missing=missing, sent_missing=sent_missing, dup=m.dup,
                sec=m.sec, late=m.late, early=m.early, outside=m.outside,
                rules='/'.join(str(h) for h in m.hits[1:]))


ROW = [
    ('both clean, secondary 1.1-1.5 ms slower', {}),
    ('both clean, secondary faster', {'sec_fast': True}),
    ('both clean, 1 us past a sample boundary', {'past': 1.0}),
    ('both clean, 1 us past a boundary, secondary faster', {'past': 1.0, 'sec_fast': True}),
    ('both clean, 2.8 us past a boundary, secondary faster', {'past': 2.8, 'sec_fast': True}),
    ('primary cut at 1500', {'cut': {0: 1500}}),
    ('secondary cut at 1500', {'cut': {1: 1500}}),
    ('secondary faster, secondary cut at 1500', {'sec_fast': True, 'cut': {1: 1500}}),
    ('1 % loss on the primary', {'loss': {0: 0.01}}),
    ('1 % loss on the secondary', {'loss': {1: 0.01}}),
    ('1 % loss on both', {'loss': {0: 0.01, 1: 0.01}}),
    ('1 % loss on both, 1 us past a boundary', {'loss': {0: 0.01, 1: 0.01}, 'past': 1.0}),
]
UNNAMED = [
    ('unpaired, secondary never sent', {'cut': {1: 0}}),
    ('short margin on both, 10 to 50 us, 1 us past a boundary',
     {'lat': {0: (1950, 1990), 1: (1950, 1990)}, 'past': 1.0}),
    ('short margin on both, 110 to 120 us', {'lat': {0: (1880, 1890), 1: (1880, 1890)}}),
    ('short margin, secondary only, 10 to 50 us', {'lat': {1: (1950, 1990)}}),
    ('both time bases step +1,000 us at 2000', {'step': (2000, 1000.0)}),
    ('both time bases step -1,000 us at 2000', {'step': (2000, -1000.0)}),
    ('both time bases step +3,000 us at 2000', {'step': (2000, 3000.0)}),
    ('both time bases step -3,000 us at 2000', {'step': (2000, -3000.0)}),
]


def show(name, case, mut=None):
    r = run(case, mut)
    print(f"  {name}: " + ' '.join(f"{k}={v}" for k, v in r.items()))
    return r


print('Rule hits read: rule1/rule2/rule3/rule4/rule5/rule6')
print('A. The cases on the clean verification row')
for name, case in ROW:
    show(name, case)
print('B. The row\'s two mutations: failing row cases out of ' + str(len(ROW)))
for mut in ('exact', 'own_time'):
    fails = []
    for name, case in ROW:
        r = run(case, mut)
        if r['bad'] or r['sent_missing']:
            fails.append(name)
    print(f"  {mut}: {len(fails)} fail; first: {fails[:2]}")
print('C. Stimuli the row does not name')
for name, case in UNNAMED:
    show(name, case)
print('D. Is rule 3 reachable with a valid head and a steady time base?')
reach = 0
rnd = random.Random(7)
for _ in range(200000):
    now = 0.0
    head = rnd.uniform(0.001, SPAN)
    t = rnd.uniform(0.001, SPAN)
    if abs(round((t - head) / T)) > 21:
        reach += 1
print(f"  any head and copy inside (render point, +{SPAN:.3f} us]: |k| over 21 in {reach} of 200000 draws;"
      f" largest |k| by arithmetic {round(SPAN / T)}")
print('E. Window sums')
print(f"  span {SPAN:.3f} us = {SPAN / T:.3f} intervals, map bits {MAPBITS}")
print(f"  22 packets at 200 ppm: {22 * T * 200e-6:.3f} us; window margin"
      f" {T / 2 - 2.744 - 22 * T * 200e-6:.3f} us;"
      f" neighbour separation {T - 2.744 - 22 * T * 200e-6:.3f} us")

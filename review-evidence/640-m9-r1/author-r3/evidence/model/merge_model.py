#!/usr/bin/env python3
"""Listener merge of a redundant pair (lane evidence, round 3; not a gate).

Models the merge rules of the stream-engine page, round 3, and checks them
against the clean stream: every sample of every packet lands at its counted
position, once, from either copy.

Rules, in order, per copy that reaches the merge:
  1 stream checks: late (t <= render point) or early (t > point + 2.667 ms)
  2 a tu copy is discarded while the partner holds clean data
    (partner CLEAN_VALID: its newest clean time is ahead of the point)
  3 no valid head, or a tu copy with no sequence reference: anchor
  4 a clean copy re-anchors when the head's grid came from a tu anchor, or
    when it lies more than 21 packets from the head
  5 newer than the head: render, becomes the head
  6 older, its map bit clear: render
  7 otherwise a duplicate: discarded
Identity: a clean copy's packet is k = round((t - head) / 125 us); a tu
copy's packet is its context's last (sequence, time) plus the signed 8-bit
sequence count since, in render-clock time.
Placement: by count from the head (6 samples per packet at 48 kHz).
Mutations (each must make a case fail): exact time compare instead of the
window; placement by each copy's own time; no rule 2.
Check: packet `first` sits within one sample of its true position (any
anchor's quantization); every later sample is contiguous from it, once.
Usage: python3 -I merge_model.py
"""
import math
import random
import sys

T = 125.0                 # packet interval, us
NS = 6                    # samples per packet at 48 kHz
SP = T / NS               # sample period, us
SPAN = 2666.667           # render buffer span, us
PTO = 2000.0              # presentation time offset, us
MAPBITS = 22              # packets 0..21 before the head
E_X = 2.210               # cross-port conversion error bound, us


class Ctx:
    def __init__(self):
        self.seq = None
        self.seq_pt = None
        self.seq_valid = False
        self.clean_pt = None
        self.clean_valid = False


class Pair:
    def __init__(self, mut=None):
        self.mut = mut or set()
        self.c = [Ctx(), Ctx()]
        self.head = None
        self.head_pos = None
        self.head_valid = False
        self.last_tu = False
        self.anchor_tu = False
        self.wmap = 0
        self.trec = T
        self.buf = {}
        self.dup = self.sec = self.tu_drop = self.late = self.early = self.writes = 0
        self.rewrites = 0

    def sweep(self, now):
        if self.head_valid and self.head <= now:
            self.head_valid = False
        for c in self.c:
            if c.clean_valid and c.clean_pt <= now:
                c.clean_valid = False
            if c.seq_valid and c.seq_pt <= now:
                c.seq_valid = False

    def write(self, pos, pkt):
        for i in range(NS):
            key = pos + i
            if key in self.buf and self.buf[key] != (pkt, i):
                self.rewrites += 1
            self.buf[key] = (pkt, i)
        self.writes += 1

    def own_pos(self, t):
        # the render clock runs at the recovered talker rate
        return math.floor(t / (self.trec / NS) + 1e-9)

    def copy(self, port, now, t, tu, seq, pkt):
        c, partner = self.c[port], self.c[port ^ 1]
        self.sweep(now)
        if t <= now or t > now + SPAN:                       # rule 1
            if t <= now:
                self.late += 1
            else:
                self.early += 1
            return
        if tu and partner.clean_valid and 'no_rule2' not in self.mut:   # rule 2
            self.tu_drop += 1
            self._seen(c, t, tu, seq, None)
            return
        if tu:
            t_id = self._by_seq(c, seq) if c.seq_valid else None
        else:
            t_id = t
        if not self.head_valid or t_id is None:              # rule 3
            return self._anchor(port, t, t_id, tu, seq, pkt, c)
        d = t_id - self.head
        if 'exact' in self.mut:
            k = 0 if d == 0 else (math.ceil(d / T) if d > 0 else -math.ceil(-d / T))
        else:
            k = round(d / T)
        if not tu and (self.anchor_tu or abs(k) >= MAPBITS):  # rule 4
            return self._anchor(port, t, t_id, tu, seq, pkt, c)
        if k >= 1:                                           # rule 5
            pos = self.head_pos + NS * k
            if 'own_time' in self.mut:
                pos = self.own_pos(t)
            self.write(pos, pkt)
            self.wmap = ((self.wmap << k) | 1) & ((1 << MAPBITS) - 1)
            self.head = t if not tu else self.head + k * self.trec
            self.head_pos = pos
            self.last_tu = tu
            self.sec += port
        elif -k < MAPBITS and not (self.wmap >> -k) & 1:     # rule 6
            pos = self.head_pos + NS * k
            if 'own_time' in self.mut:
                pos = self.own_pos(t)
            self.write(pos, pkt)
            self.wmap |= 1 << -k
            self.sec += port
        else:                                                # rule 7
            self.dup += 1
        self._seen(c, t, tu, seq, t_id)

    def _anchor(self, port, t, t_id, tu, seq, pkt, c):
        pos = self.own_pos(t)
        self.write(pos, pkt)
        self.head, self.head_pos, self.head_valid = t, pos, True
        self.wmap, self.last_tu, self.anchor_tu = 1, tu, tu
        self.sec += port
        self._seen(c, t, tu, seq, t)

    def _by_seq(self, c, seq):
        d = ((seq - c.seq + 128) % 256) - 128
        return c.seq_pt + d * self.trec

    def _seen(self, c, t, tu, seq, t_id):
        if t_id is None:
            if not c.seq_valid:
                return
            t_id = self._by_seq(c, seq)
        c.seq, c.seq_pt, c.seq_valid = seq, t_id, True
        if not tu:
            c.clean_pt, c.clean_valid = t, True


def run(case, mut=None, n=4000, seed=1):
    rnd = random.Random(seed)
    drift = 150e-6                      # talker media clock vs gPTP
    spr = SP * (1 + drift)              # render sample period
    T0 = 10_000.0 + 7.3                 # first presentation time, us
    if 'past_boundary' in case:         # times this far past a sample boundary
        T0 = round(T0 / spr) * spr + case['past_boundary']
    lat = {0: (60, 180), 1: (1100, 1500)}
    if case.get('sec_fast'):
        lat = {0: (1100, 1500), 1: (60, 180)}
    seq0 = {0: 17, 1: 201}              # independent sequence numbers
    ev = []
    for j in range(n):
        Tj = T0 + j * T * (1 + drift)
        for port in (0, 1):
            if port in case.get('cut', {}) and j >= case['cut'][port]:
                continue
            if rnd.random() < case.get('loss', {}).get(port, 0.0):
                continue
            t, tu = Tj, False
            if port == 1:
                t += rnd.uniform(-E_X, E_X)
            tw = case.get('tu', {}).get(port)
            if tw and tw[0] <= j < tw[1]:
                tu = True
                t += tw[2] + rnd.uniform(-tw[3], tw[3])
            a = Tj - PTO + rnd.uniform(*lat[port])
            ev.append((a, port, t, tu, (seq0[port] + j) % 256, j))
    ev.sort()
    p = Pair(mut)
    p.trec = T * (1 + drift)
    for a, port, t, tu, seq, j in ev:
        p.copy(port, a, t, tu, seq, j)
    first = case.get('first', 0)
    true_base = math.floor((T0 + first * T * (1 + drift)) / spr + 1e-9)
    # the anchor may round to a neighbouring sample (one-sample quantization
    # of any presentation time); every later sample must then be contiguous
    cands = [b for b in (true_base - 1, true_base, true_base + 1)
             if p.buf.get(b) == (first, 0)]
    base = cands[0] if cands else true_base
    align = base - true_base
    bad = missing = 0
    for j in range(first, n):
        for i in range(NS):
            got = p.buf.get(base + NS * (j - first) + i)
            if got is None:
                missing += 1
            elif got != (j, i):
                bad += 1
    span = range(base, base + NS * (n - first))
    extra = sum(1 for k in p.buf if k not in span)
    return dict(align=align, bad=bad, missing=missing, extra=extra, dup=p.dup, sec=p.sec,
                tu_drop=p.tu_drop, late=p.late, early=p.early, rewrites=p.rewrites)


CASES = [
    # (name, case, expectation); every case also requires bad == missing == 0
    ("both clean, secondary 1.1-1.5 ms slower, conversion error +-2.21 us", {}, dict(dup=4000, sec=0)),
    ("both clean, secondary faster", {'sec_fast': True}, dict(dup=4000, sec=4000)),
    ("both clean, times 1 us past a sample boundary, secondary faster",
     {'sec_fast': True, 'past_boundary': 1.0}, dict(dup=4000, sec=4000)),
    ("1 % loss on both, times 1 us past a sample boundary",
     {'loss': {0: 0.01, 1: 0.01}, 'past_boundary': 1.0}, {}),
    ("primary cut at packet 1500", {'cut': {0: 1500}}, dict(dup=1500)),
    ("secondary cut at packet 1500", {'cut': {1: 1500}}, dict(dup=1500, sec=0)),
    ("1 % frame loss on the faster primary, filled from the late copy", {'loss': {0: 0.01}}, {}),
    ("1 % frame loss on both networks", {'loss': {0: 0.01, 1: 0.01}}, {}),
    ("secondary tu from packet 100, skew +30 us, arrives first", {'sec_fast': True, 'tu': {1: (100, 4000, 30.0, 5.0)}}, dict(tu_drop=3900)),
    ("secondary tu from packet 100, skew -30 us, arrives first", {'sec_fast': True, 'tu': {1: (100, 4000, -30.0, 5.0)}}, dict(tu_drop=3900)),
    ("secondary tu from packet 100, skew +200 us, arrives first", {'sec_fast': True, 'tu': {1: (100, 4000, 200.0, 20.0)}}, dict(tu_drop=3900)),
    ("secondary tu from packet 100, skew -200 us, arrives first", {'sec_fast': True, 'tu': {1: (100, 4000, -200.0, 20.0)}}, dict(tu_drop=3900)),
    ("secondary tu from packet 100, skew +1 ms, arrives first", {'sec_fast': True, 'tu': {1: (100, 4000, 1000.0, 50.0)}}, dict(tu_or_early=3900)),
    ("secondary tu from the first packet, skew -200 us, arrives first", {'sec_fast': True, 'tu': {1: (0, 4000, -200.0, 20.0)}}, dict(extra_max=6 * 14)),
    ("primary cut, then grandmaster change on the secondary: tu 0.25 s, skew 500 us",
     {'cut': {0: 1000}, 'tu': {1: (1200, 3200, 500.0, 100.0)}}, {}),
]


def judge(res, want):
    good = res['bad'] == 0 and res['missing'] == 0
    good &= res['extra'] <= want.get('extra_max', 0)
    if 'dup' in want:
        good &= res['dup'] == want['dup']
    if 'sec' in want:
        good &= (res['sec'] == 0) if want['sec'] == 0 else (res['sec'] >= want['sec'] - 12)
    if 'tu_drop' in want:
        good &= res['tu_drop'] >= want['tu_drop']
    if 'tu_or_early' in want:
        good &= res['tu_drop'] + res['early'] >= want['tu_or_early']
    return good


def main():
    ok_all = True
    for name, case, want in CASES:
        res = run(case)
        good = judge(res, want)
        ok_all &= good
        print(f"{'PASS' if good else 'FAIL'}  {name}: {res}")
    print("mutations (each must FAIL at least one case):")
    for mut in ('exact', 'own_time', 'no_rule2'):
        fails = [name for name, case, want in CASES if not judge(run(case, {mut}), want)]
        ok_all &= bool(fails)
        print(f"  {mut}: {'caught' if fails else 'NOT CAUGHT'} by {len(fails)} case(s), first: {fails[:2]}")
    print("ALL PASS" if ok_all else "SOME FAIL")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

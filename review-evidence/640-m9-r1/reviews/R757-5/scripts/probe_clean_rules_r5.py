#!/usr/bin/env python3
"""Drives merge rules 1 to 6 of docs/design/MARK_II_STREAM_ENGINES.md (SE:637-674), built
from the page alone at the reviewed head, through the arms of the verification row SE:1148.

Checks that the clean-copy rules still hold with the tu rules gone: every delivered packet
renders at its true position, duplicates count once, secondary-first writes count exactly,
and the two mutations the row names fail. Also prints a census of which rule each arm reaches.
Usage: probe_clean_rules_r5.py  (no arguments; seeded, deterministic)
"""
import random

PKT = 125_000  # ns, class A interval
SPAN = 2_666_667  # ns, render buffer depth at every rate (SE:468-470)
RATE_SPP = {48: 6, 96: 12, 192: 24}  # samples per packet


class Merge:
    def __init__(self, spp, exact=False, own_time=False):
        self.spp, self.exact, self.own_time = spp, exact, own_time
        self.t_sample = PKT / spp
        self.head_t = None
        self.head_pos = 0
        self.wmap = 0
        self.dup = self.sec = 0
        self.hits = [0] * 7
        self.written = {}  # sample position -> payload id
        self.overwrites = 0
        self.late = self.early = 0

    def _write(self, pos, pid):
        for i in range(self.spp):
            p = pos + i
            if p in self.written and self.written[p] != (pid, i):
                self.overwrites += 1
            self.written[p] = (pid, i)

    def _pos_of_time(self, t):
        return int(t // self.t_sample)  # the buffer is indexed by time; a boundary is a whole sample

    def copy(self, now, t, pid, odd):
        # Rule 1: late or early time (SE:641)
        if t < now:
            self.late += 1
            self.hits[1] += 1
            return
        if t > now + SPAN:
            self.early += 1
            self.hits[1] += 1
            return
        if self.head_t is None or self.head_t <= now:  # rule 2 (SE:642)
            self._anchor(t, pid, odd, 2)
            return
        if self.exact:
            d = t - self.head_t
            k = d // PKT if d % PKT == 0 else None
            if k is None:  # an exact compare matches nothing: treat as a new newest packet
                k = max(1, round(d / PKT)) if d > 0 else round(d / PKT) - 1
        else:
            k = round((t - self.head_t) / PKT)
        if abs(k) > 21:  # rule 3 (SE:643)
            self._anchor(t, pid, odd, 3)
            return
        if k >= 1:  # rule 4 (SE:644)
            self.hits[4] += 1
            pos = self.head_pos + k * self.spp
            self._write(self._pos_of_time(t) if self.own_time else pos, pid)
            self.head_t, self.head_pos = t, pos
            self.wmap = ((self.wmap << k) | 1) & ((1 << 22) - 1)
            self.sec += odd
            return
        if not (self.wmap >> -k) & 1:  # rule 5 (SE:645)
            self.hits[5] += 1
            pos = self.head_pos + k * self.spp
            self._write(self._pos_of_time(t) if self.own_time else pos, pid)
            self.wmap |= 1 << -k
            self.sec += odd
            return
        self.hits[6] += 1  # rule 6 (SE:646)
        self.dup += 1

    def _anchor(self, t, pid, odd, rule):
        self.hits[rule] += 1
        pos = self._pos_of_time(t)
        self._write(pos, pid)
        self.head_t, self.head_pos = t, pos
        self.wmap = 1  # the register's definition: bit 0 is the head, written (SE:820)
        self.sec += odd


def run(arm, spp=6, n=4000, seed=1, **mut):
    rng = random.Random(seed)
    ev = []
    t0 = 10_000_000 + arm.get('phase', 0)
    offset = 2_000_000
    prim_lat = arm.get('prim', (60_000, 180_000))
    sec_lat = arm.get('sec', (60_000, 180_000))
    jit = arm.get('jit', 2_744)
    delivered_both = 0
    expected_any = set()
    sec_first_expected = 0
    arrivals = {}
    for i in range(n):
        tp = t0 + i * PKT + offset
        cap = t0 + i * PKT
        for net, lat in ((0, prim_lat), (1, sec_lat)):
            if net in arm.get('cut_net', {}) and i >= arm['cut_net'][net]:
                continue
            if arm.get('loss_net') == net and rng.random() < arm.get('loss', 0):
                continue
            arr = cap + rng.randint(*lat)
            e = rng.randint(-jit, jit) if net == 1 else 0
            ev.append((arr, tp + e, i, net))
            arrivals.setdefault(i, []).append((arr, net))
    ev.sort()
    m = Merge(spp, **mut)
    # The render point: the sample now at the pins, in the render time base.
    render_lag = 0
    for arr, t, i, net in ev:
        m.copy(arr - render_lag, t, i, net)
    for i, a in arrivals.items():
        expected_any.add(i)
        if len(a) == 2:
            delivered_both += 1
        if min(a)[1] == 1:
            sec_first_expected += 1
    # Truth: packet i occupies spp samples from the anchor's position, by count.
    base_pkt = min(pid for (pid, _s) in m.written.values())
    base_pos = min(p for p, v in m.written.items() if v == (base_pkt, 0))
    missing = misplaced = 0
    for i in expected_any:
        for s in range(spp):
            p = base_pos + (i - base_pkt) * spp + s
            if p not in m.written:
                missing += 1
            elif m.written[p] != (i, s):
                misplaced += 1
    extra = len(m.written) - spp * len(expected_any) + missing
    return dict(missing=missing, misplaced=misplaced, extra=extra, dup=m.dup,
                dup_expected=delivered_both, sec=m.sec, sec_expected=sec_first_expected,
                late=m.late, early=m.early, overwrites=m.overwrites, hits=m.hits[1:])


ARMS = {
    'both clean, jitter 2.744 us': {},
    'primary faster by 1.5 ms': {'sec': (1_560_000, 1_680_000)},
    'secondary faster by 1.5 ms': {'prim': (1_560_000, 1_680_000)},
    'times 1 us past a sample boundary': {'phase': 1_000},
    'primary cut mid-stream': {'cut_net': {0: 2000}},
    'secondary cut mid-stream': {'cut_net': {1: 2000}},
    'primary cut, secondary 1.5 ms slower': {'cut_net': {0: 2000}, 'sec': (1_560_000, 1_680_000)},
    '1 % loss on primary, later copy fills': {'loss_net': 0, 'loss': .01, 'prim': (60_000, 180_000), 'sec': (1_560_000, 1_680_000)},
    '1 % loss on secondary, later copy fills': {'loss_net': 1, 'loss': .01, 'prim': (1_560_000, 1_680_000), 'sec': (60_000, 180_000)},
}


def main():
    fails = 0
    print('arm | rate | missing misplaced extra | dup/expected | sec/expected | hits r1..r6')
    for name, arm in ARMS.items():
        for rate, spp in RATE_SPP.items():
            r = run(arm, spp=spp)
            ok = (r['missing'] == 0 and r['misplaced'] == 0 and r['extra'] == 0
                  and r['dup'] == r['dup_expected'] and r['sec'] == r['sec_expected'])
            fails += not ok
            print(f"{name} | {rate} | {r['missing']} {r['misplaced']} {r['extra']} | "
                  f"{r['dup']}/{r['dup_expected']} | {r['sec']}/{r['sec_expected']} | {r['hits']} | {'PASS' if ok else 'FAIL'}")
    print('arms failing:', fails)
    print()
    print('The row\'s two mutations (each must fail at least one arm):')
    for mut in ({'exact': True}, {'own_time': True}):
        caught = 0
        for name, arm in ARMS.items():
            r = run(arm, spp=6, **mut)
            bad = r['missing'] or r['misplaced'] or r['extra'] or r['dup'] != r['dup_expected']
            caught += bool(bad)
        print(f"  {list(mut)[0]}: caught by {caught} of {len(ARMS)} arms")
    print()
    total = [0] * 6
    for arm in ARMS.values():
        for rate, spp in RATE_SPP.items():
            for i, h in enumerate(run(arm, spp=spp)['hits']):
                total[i] += h
    print('rule census over the row\'s arms, r1..r6:', total)
    print('rule 3 reached by the row\'s named arms:', total[2] != 0)
    print('rule 2 reached only by the first packet of each arm (a head lapse is not a named arm):', total[1] == 27)
    print()
    print('Rule 3 reachability, from the page: a copy passing rule 1 has t in [now, now + 2.667 ms];')
    print('a valid head has head in (now, now + 2.667 ms]; so |t - head| < 2.667 ms, 21.33 packets, |k| <= 21.')
    print('A render point stepping back past the span breaks that bound:')
    m = Merge(6)
    m.copy(0, 2_000_000, 0, 0)
    m.copy(125_000, 2_125_000, 1, 0)
    m.copy(125_000 - 5_000_000, 2_250_000 - 5_000_000, 2, 0)
    print('  render point stepped back 5 ms, next clean copy: hits r1..r6 =', m.hits[1:])
    print()
    print('Outside the row: clean copies arriving under one packet before their time, surviving network only.')
    print('The head lapses between packets, so rule 2 re-anchors each copy by its own time (SE:625, :642).')
    for label, lat, jit, phase, spp in (
            ('48 kHz, margin 200 to 300 us, jitter 1 us, 1 us past a boundary', (1_700_000, 1_800_000), 1000, 1000, 6),
            ('48 kHz, margin 20 to 100 us, jitter 1 us, 1 us past a boundary', (1_900_000, 1_980_000), 1000, 1000, 6),
            ('48 kHz, margin 20 to 100 us, jitter 2.744 us, 1 us past a boundary', (1_900_000, 1_980_000), 2744, 1000, 6),
            ('48 kHz, margin 200 to 300 us, jitter 160 ns, 100 ns past a boundary', (1_700_000, 1_800_000), 160, 100, 6),
            ('48 kHz, margin 20 to 100 us, jitter 160 ns, 100 ns past a boundary', (1_900_000, 1_980_000), 160, 100, 6),
            ('192 kHz, margin 20 to 100 us, jitter 160 ns, 100 ns past a boundary', (1_900_000, 1_980_000), 160, 100, 24)):
        r = run({'cut_net': {0: 0}, 'sec': lat, 'jit': jit, 'phase': phase}, spp=spp)
        print(f"  {label}: missing {r['missing']} misplaced {r['misplaced']} of {4000 * spp} samples; hits r1..r6 {r['hits']}")
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(main())

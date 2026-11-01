#!/usr/bin/env python3
"""Can TU-1's test fail, and can a listener pass it? Runs the page's cases A to
D on the round-4 model unchanged, then on one disposable change: a tu copy with
a valid count is checked at its counted time, not its own. This is feasibility
evidence for the requirement only, not a proposed mechanism.

TU-1's differential test: the same stream with skew 0 against each skew.
Also prints case E mirrored (primary tu, clean secondary) next to case E.

Usage: python3 -I probe_tu_req_r5.py <dir holding merge_model.py>
"""
import sys

sys.path.insert(0, sys.argv[1])
import merge_model as m  # noqa: E402


class Counted(m.Pair):
    def copy(self, port, now, t, tu, seq, pkt, jumped=False):
        c = self.c[port]
        self.sweep(now)
        if tu and c.seq_valid:
            t = self._by_seq(c, seq)
        return super().copy(port, now, t, tu, seq, pkt, jumped)


def run(cls, case):
    orig = m.Pair
    m.Pair = cls
    try:
        return m.run(case)
    finally:
        m.Pair = orig


FAST = {'lat': {1: (60, 180)}}


def both(skew, end=4000, extra=None):
    c = dict(extra or {})
    c['tu'] = {0: (100, end, skew, 0.0), 1: (100, end, skew, 0.0)}
    return c


CASES = [('A', both(s, extra=FAST), s) for s in (700.0, 800.0, 850.0, -2000.0, 1.5e6, -1.5e6)]
CASES += [('B', both(s, end=600, extra=FAST), s) for s in (1000.0, -1900.0, -2500.0)]
CASES += [('C', both(s), s) for s in (5.0, -5.0, 200.0, -200.0, 1000.0, -1000.0)]
CASES += [('D', {'tu': {0: (100, 4000, 1000.0, 0.0), 1: (100, 4000, 0.0, 0.0)}}, 1000.0)]


def zero_of(tag):
    if tag == 'A':
        return both(0.0, extra=FAST)
    if tag == 'B':
        return both(0.0, end=600, extra=FAST)
    return both(0.0)


print('TU-1 differential, cases A to D: samples missing and wrong, model / with counted check')
fail_model = fail_counted = 0
for tag, case, skew in CASES:
    r0 = run(m.Pair, zero_of(tag))
    c0 = run(Counted, zero_of(tag))
    r = run(m.Pair, case)
    c = run(Counted, case)
    dm = (r['missing'], r['bad']) != (r0['missing'], r0['bad'])
    dc = (c['missing'], c['bad']) != (c0['missing'], c0['bad'])
    fail_model += dm
    fail_counted += dc
    print(f"  {tag} skew {skew:+.0f}: model missing={r['missing']} bad={r['bad']} (skew 0: {r0['missing']}, {r0['bad']}) test {'FAILS' if dm else 'passes'};"
          f" counted missing={c['missing']} bad={c['bad']} test {'FAILS' if dc else 'passes'}")
print(f"  of {len(CASES)}: the model fails TU-1's test in {fail_model}; the counted check in {fail_counted}")
print('Case E against its mirror, round-4 model')
for skew in (30.0, 200.0, 1000.0):
    e = run(m.Pair, {'sec_fast': True, 'tu': {1: (100, 4000, skew, 0.0)}})
    mir = run(m.Pair, {'tu': {0: (100, 4000, skew, 0.0)}})
    print(f"  skew {skew:+.0f}: secondary tu, arrives first: missing={e['missing']} bad={e['bad']};"
          f" primary tu, arrives first: missing={mir['missing']} bad={mir['bad']}")

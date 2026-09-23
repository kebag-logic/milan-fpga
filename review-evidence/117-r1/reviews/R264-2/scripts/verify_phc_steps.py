#!/usr/bin/env python3
"""Observation 7: the DUT PHC step at each return (console TAI_NS against the
build-box clock) versus the interval between consecutive outlet-on commands
(attempt 1's early 'on' precedes cycle 1).

usage: verify_phc_steps.py A202_BENCH_DIR
"""
import sys, os, re, datetime
bench = sys.argv[1]


def iso(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc).timestamp()


def on_cmd(d):
    for ln in open(os.path.join(d, 'powerstrip.txt')):
        m = re.search(r'T_ON_CMD ([0-9.]+)', ln)
        if m:
            return float(m.group(1))


# Attempt 1: the guard switched OUT4 back on early (lock.txt, first epoch
# line after PROOF_ABORT); the sequence's own later "on" found OUT4 already on.
_lk = open(os.path.join(bench, 'attempt1-aborted', 'lock.txt')).read()
prev_on = float(re.search(r'PROOF_ABORT[^\n]*\n([0-9]+\.[0-9]+)', _lk).group(1))
print('attempt 1 guard on-command %.3f; sequence on-command %.3f (OUT4 already on)' % (
    prev_on, on_cmd(os.path.join(bench, 'attempt1-aborted'))))
for c in range(1, 7):
    d = os.path.join(bench, 'cycle%d' % c)
    txt = open(os.path.join(d, 'console.txt'), encoding='latin-1').read()
    pts = [(iso(t), int(v, 16) / 1e9) for t, v in re.findall(
        r"^### (\S+) cmd='milan_status'.*?TAI_NS=0x([0-9a-f]+)", txt, flags=re.M | re.S)]
    diffs = [(t, tai - t) for t, tai in pts]
    step = min(((b[1] - a[1]), a[0]) for a, b in zip(diffs, diffs[1:]))
    on = on_cmd(d)
    print('cycle %d: PHC step %.3f s; on-to-on interval %.3f s; |sum| %.3f s' % (c, step[0], on - prev_on, abs(step[0] + (on - prev_on))))
    prev_on = on

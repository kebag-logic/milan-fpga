#!/usr/bin/env python3
"""Recompute the hook README's result tables from the published results.json receipts and compare.

Usage: python3 -I check_receipts.py <receipts dir> <README.md>
Prints one line per checked figure, and MISMATCH lines; exit 1 on any mismatch.
"""
import json
import re
import sys
from pathlib import Path

rec, readme = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
RUNS = {('1x1', 'idle'): '1x1-idle', ('1x1', 'answering'): '1x1-ans',
        ('8x8', 'idle'): '8x8-idle', ('8x8', 'answering'): '8x8-ans'}
HOOKS = ['H-ADP', 'H-DISC', 'H-ACMP', 'H-AECP', 'H-NOTIFY', 'H-COUNTERS', 'H-MAAP', 'H-SRP']
bad = 0


def say(ok, text):
    global bad
    bad += not ok
    print(('ok       ' if ok else 'MISMATCH ') + text)


def cell(rows, loaded):
    part = [r for r in rows if r['loaded'] == loaded]
    if not part:
        return '-', None
    top = max(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))
    v = 'never served' if top['unbounded'] else f"{top['ms']:.2f}"
    return (f'**{v}**' if not top['within'] else v), top


data = {k: json.loads((rec / 'runs' / v / 'results.json').read_text()) for k, v in RUNS.items()}
# run-level counts
counts = re.findall(r'^\| (1x1|8x8) \| (idle|answering) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$',
                    readme, re.M)
for point, arm, groups, paths, refusals, orders, narrow, late in counts:
    d = data[(point, arm)]
    log = (rec / 'runs' / RUNS[(point, arm)] / 'regrade.log').read_text()
    g = int(re.search(r'(\d+) groups', log).group(1))
    f = d['findings']
    got = (g, len(d['rows']), len(d['refusals']), sum(x.startswith('ORDER ') for x in f),
           sum(x.startswith('NARROW ') for x in f), sum(x.startswith('LATE ') for x in f))
    want = tuple(map(int, (groups, paths, refusals, orders, narrow, late)))
    say(got == want, f'{point} {arm}: groups/paths/refusals/order/narrow/late readme {want} receipts {got}')
    say(d['cpu_hz'] == 100_000_000 and d['cpu_clock'] == 'sys' and d['sys_hz'] == 100_000_000 and d['t_svc_ms'] == 20.0,
        f"{point} {arm}: clock {d['clock']!r}, cpu_hz {d['cpu_hz']}, t_svc {d['t_svc_ms']}")
    say(d['superseded'] == [], f'{point} {arm}: superseded {d["superseded"]}')
# hook tables
for point in ('1x1', '8x8'):
    sec = readme.split(f'{point}, CPU 100 MHz on `sys`:')[1].split('\n\n')[1]
    for line in sec.splitlines()[2:]:
        c = [x.strip() for x in line.strip('|').split('|')]
        hook, bound = c[0], float(c[1])
        got = []
        for loaded in (False, True):
            for arm in ('idle', 'answering'):
                rows = [r for r in data[(point, arm)]['rows'] if r['hook'] == hook]
                v, top = cell(rows, loaded)
                got.append(v)
                if top is not None:
                    say(top['bound_ms'] - top['wait_ms'] == bound,
                        f'{point} {hook} bound {bound} vs graded {top["bound_ms"] - top["wait_ms"]}')
        say(got == c[2:6], f'{point} {hook}: readme {c[2:6]} receipts {got}')
# per-hook miss counts and ordering
for line in readme.split('| Hook | 1x1 idle | 1x1 answering |')[1].split('\n\n')[0].splitlines()[2:]:
    c = [x.strip() for x in line.strip('|').split('|')]
    hook = c[0]
    got = []
    for (point, arm) in (('1x1', 'idle'), ('1x1', 'answering'), ('8x8', 'idle'), ('8x8', 'answering')):
        rows = [r for r in data[(point, arm)]['rows'] if r['hook'] == hook]
        got.append(f"{sum(not r['within'] for r in rows)} of {len(rows)}" if rows else '-')
    say(got == c[1:5], f'{hook} misses: readme {c[1:5]} receipts {got}')
    for k, (point, a, b) in enumerate((('1x1', 'idle', 'answering'), ('8x8', 'idle', 'answering'))):
        parts = []
        for arm in (a, b):
            ch = data[(point, arm)]['checks'][hook]
            parts.append('not applied' if not ch['applied'] else
                         f"{ch['applied']} ({ch['undecided']}), {len(ch['findings'])}")
        say(' / '.join(parts) == c[5 + k], f'{hook} ordering {point}: readme {c[5 + k]!r} receipts {" / ".join(parts)!r}')
# H-COUNTERS path table
for probe, p1, p8 in (('counters.first', '5.64', '10.16'), ('counters.all', '27.58', '218.71'),
                      ('counters.held', '5.19', '9.93'), ('counters.loaded', '20.76', '36.62')):
    for point, want in (('1x1', p1), ('8x8', p8)):
        r = [x for x in data[(point, 'answering')]['rows'] if x['path'] == probe]
        say(len(r) == 1 and f"{r[0]['ms']:.2f}" == want, f'{probe} {point}: readme {want} receipts '
            f"{[round(x['ms'], 3) for x in r]} W {[x['wait_ms'] for x in r]}")
# every row's verdict is consistent with its own bound, and no bound was relaxed
EXPECT = {'srp': 18.0}
for k, d in data.items():
    for r in d['rows']:
        base = EXPECT.get(r['family'], 20.0)
        # the held push is timed from its eligibility, after its W, so its bound carries no W (README, Grading)
        added = 0.0 if r['path'] == 'counters.held' else r['wait_ms']
        ok = abs(r['bound_ms'] - added - base) < 1e-9 and r['within'] == (not r['unbounded'] and r['ms'] <= r['bound_ms'])
        if not ok:
            say(False, f'{k} {r["probe"]}: bound {r["bound_ms"]} W {r["wait_ms"]} within {r["within"]}')
    say(True, f'{k}: every row bound = 20 ms (18 ms SRP) + W and verdict = ms <= bound, {len(d["rows"])} rows')
# rows with W > 0
for k, d in data.items():
    w = [(r['probe'], r['wait_ms'], r['ms'], r['bound_ms']) for r in d['rows'] if r['wait_ms']]
    print('info     ', k, 'rows with W:', w)
print('mismatches:', bad)
sys.exit(1 if bad else 0)

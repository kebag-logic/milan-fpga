#!/usr/bin/env python3
"""r1b_figures.py PACKET_DIR  (PACKET_DIR = .../review-evidence/cicd-r1)
Verifies the fetched files against MANIFEST.json published_sha256, then recomputes the
ccache (crf_rx mutants, avtp_rxmon) and -O3 budget L1d/task-clock figures, and checks the
crf_rx verdict lines across the nocc/cold/warm logs."""
import hashlib, json, os, statistics, sys
d = sys.argv[1]
m = json.load(open(os.path.join(d, 'MANIFEST.json')))
ok = bad = 0
for e in m:
    f = os.path.join(d, e['file'])
    if os.path.isfile(f):
        if hashlib.sha256(open(f, 'rb').read()).hexdigest() == e['published_sha256']: ok += 1
        else: bad += 1; print('MANIFEST MISMATCH', e['file'])
print(f'manifest: {ok} fetched files match published_sha256, {bad} mismatch')
def tm(p):
    w = open(os.path.join(d, p)).read().split()
    i = w.index('user'); return float(w[w.index('wall') - 1]), float(w[i - 1])
c = 'author-r1b/receipts/ccache/'
n, co, wa = (tm(c + f'crf_rx-mutants/{r}.time') for r in ('nocc', 'cold', 'warm'))
a0, a1 = tm(c + 'avtp_rxmon/nocc.time'), tm(c + 'avtp_rxmon/cold.time')
pc = lambda x, y: (y / x - 1) * 100
print(f'crf_rx mutants user: cold {pc(n[1], co[1]):.2f} %  warm {pc(n[1], wa[1]):.2f} %  (wall cold {pc(n[0], co[0]):.2f} %, warm {pc(n[0], wa[0]):.2f} %)')
print(f'avtp_rxmon user: cold {pc(a0[1], a1[1]):.2f} %  (wall {pc(a0[0], a1[0]):.2f} %)')
logs = {r: open(os.path.join(d, c + f'crf_rx-mutants/{r}.log')).read().splitlines() for r in ('nocc', 'cold', 'warm')}
v = {r: [l for l in L if l.startswith('[') or l.startswith('  named') or l.startswith('==')] for r, L in logs.items()}
print('crf_rx verdict lines:', {r: sum(l.startswith('[PASS]') for l in x) for r, x in v.items()},
      'identical' if v['nocc'] == v['cold'] == v['warm'] else 'DIFFER', '| non-PASS case lines:',
      sum(l.startswith('[') and not l.startswith('[PASS]') for l in v['nocc']), '|', v['nocc'][-1])
def perf(p):
    r = {}
    for l in open(os.path.join(d, 'author/receipts/budget', p)):
        f = l.strip().split(',')
        if len(f) > 2: r[f[2]] = float(f[0])
    return r
red = []
for s in ('', '-2', '-3'):
    b, o = perf(f'base{s}.perf'), perf(f'tbO3{s}.perf')
    l1 = (1 - o['L1-dcache-load-misses:u'] / b['L1-dcache-load-misses:u']) * 100; red.append(l1)
    print(f'pair "{s or "unsuffixed"}": L1d {int(b["L1-dcache-load-misses:u"]):,} -> {int(o["L1-dcache-load-misses:u"]):,} = {l1:.2f} % lower; '
          f'task-clock {(1 - o["task-clock:u"] / b["task-clock:u"]) * 100:.2f} % lower')
print(f'L1d range {min(red):.2f}..{max(red):.2f} %, median {statistics.median(red):.2f} %')

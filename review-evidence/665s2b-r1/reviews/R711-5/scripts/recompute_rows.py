#!/usr/bin/env python3
"""Recompute, from the published raw results, (a) the notice groups' rows (least to most per row) per leg and
(b) each head leg's least row margin outside the egress-held backlog-owed group, and the leg totals.
usage: recompute_rows.py MEASURE_DIR   (author-r16/receipts/measure)"""
import glob, gzip, json, os, re, sys
d = sys.argv[1]
for leg in ['NT-1', 'D-NT1', 'NT-8', 'D-NT8', 'X4-NT8']:
    r = json.load(gzip.open(f'{d}/{leg}/results.json.gz')); rows = {}
    for g in r['results']:
        if g['group'].startswith('notice-retried'):
            for p in g['probes']:
                if p.get('status') == 'measured' and p.get('ms') is not None:
                    rows.setdefault(p['probe'].split('.', 1)[1], []).append(p['ms'])
    print(leg, '; '.join(f'{k} {min(v):.2f}..{max(v):.2f}' for k, v in sorted(rows.items())))
for leg in ['N-A1', 'N-A8', 'N-B1', 'N-B8', 'D-A1', 'D-A8', 'D-B1', 'D-B8', 'X4-A8']:
    r = json.load(gzip.open(f'{d}/{leg}/results.json.gz')); least = None
    for g in r['results']:
        if g['group'] == 'backlog-owed':
            continue
        for p in g['probes']:
            if p.get('status') == 'measured' and p.get('ms') is not None and p.get('budget_ms') is not None:
                m = p['budget_ms'] - p['ms']
                if least is None or m < least[0]:
                    least = (m, p['ms'], p['budget_ms'], p['probe'])
    print(leg, 'least margin outside backlog-owed %.3f ms (%.3f of %s, %s)' % least)
groups = passes = 0
for f in sorted(glob.glob(f'{d}/*/regrade.log') + glob.glob(f'{d}/*/run.log')):
    for line in open(f):
        m = re.search(r'(\d+) groups graded, (\d+) refusals.* (\d+) of (\d+) work passes', line)
        if m:
            print(os.path.relpath(f, d), 'groups', m.group(1), 'refusals', m.group(2), 'over', m.group(3), 'of', m.group(4))

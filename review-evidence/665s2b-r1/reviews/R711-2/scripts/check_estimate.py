#!/usr/bin/env python3
"""Recompute section 14's U, L and S from raw results.json and the doc's own table.

usage: check_estimate.py <measure-dir> <SPLIT_CONTROL_MEMORY.md>"""
import json, re, sys, pathlib
root, doc = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text()
doc = doc[doc.index('## 14. The 32x32 estimate'):]
G = ('backlog', 'backlog-adp', 'backlog-adp-refill')
ROW = {'ACMP record, first': 'service.acmp.first', 'ADP record, first': 'service.adp.first', 'MAAP record, first': 'service.maap.first',
       'AECP record, first': 'service.aecp.first', 'SRP record, first': 'service.srp.first', 'ACMP record, last': 'service.acmp.last',
       'ADP record, last': 'service.adp.last', 'MAAP record, last': 'service.maap.last', 'AECP record, last': 'service.aecp.last',
       'SRP record, last': 'service.srp.last', 'An ACMP command behind a full ACMP ring': 'backlog.acmp_command',
       'An ENTITY_AVAILABLE behind a full ADP ring': 'backlog.adp_available', 'An event behind 15 others': 'backlog.event'}
load = lambda n: json.loads((root / n / 'results.json').read_text())
A1, A8, A81 = [load('N-A1'), load('N-B1')], [load('N-A8'), load('N-B8')], [load('P81-A8')]
def worst(runs, path):
    return max(p['ms'] for r in runs for g in r['results'] if g['group'] in G or (g['group'] == 'backlog-owed' and path != 'service.aecp.last') for p in g['probes']
               if p['path'][0] == path and p.get('status') == 'measured' and not p.get('unanswered'))
def longest(runs):
    return max(g['passes']['worst']['cycles'] for r in runs for g in r['results'] if g['group'] in G + ('backlog-owed',)) / 1e5
def cells(row):
    m = re.search(r'^\| ' + re.escape(row) + r' \| (\d+) \|(.*)\|$', doc, re.M)
    return [re.sub(r'\*|\(.*\)', '', c).strip() for c in m.group(2).split('|')] if m else None
bad = 0
for row, path in list(ROW.items()) + [('The longest work pass', None)]:
    a, m, b = (longest(A1), longest(A81), longest(A8)) if path is None else (worst(A1, path), worst(A81, path), worst(A8, path))
    U, L, S = 4 * b, b + (b - a) / 14 * 48, b + (m - a) / 14 * 48
    want = [f'{a:.2f}', f'{m:.2f}', f'{b:.2f}', f'{U:.1f}', f'{L:.1f}', f'{S:.1f}']
    got = cells(row)
    d = [abs(float(x) - float(y)) for x, y in zip(want, got)]
    flag = 'ok' if all(z <= (0.0051 if i < 3 else 0.051) for i, z in enumerate(d)) else 'DIFF'
    bad += flag != 'ok'
    print(f'{row:44} recomputed {want} doc {got} {flag}')
print('differences', bad)

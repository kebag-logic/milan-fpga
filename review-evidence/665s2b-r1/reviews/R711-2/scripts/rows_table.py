#!/usr/bin/env python3
"""Re-derive the REVIEW READY row table from raw results.json and compare it with the author's rows.md.

usage: rows_table.py <results-measure-dir> <rows.md>
Every instance is re-derived: its worst over interfaces of (end-start)/cpu clock where end_sys exists, and its
verdict against min(20 ms, the family's ceiling) from this script's own table, not the record's budget field."""
import json, re, sys, pathlib
root, rows = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
BOUND = {'srp': 18.0}          # min(T_svc = 20, 18) per the 2026-10-29 owner decision; every other family 20
RUNS = {'1x1': ('N-A1', 'N-B1'), '1x1d': ('D-A1', 'D-B1'), '8x8': ('N-A8', 'N-B8'), '8x8d': ('D-A8', 'D-B8')}
ROW = {'service.acmp.first': 'ACMP record, first', 'service.adp.first': 'ADP record, first', 'service.maap.first': 'MAAP record, first',
       'service.aecp.first': 'AECP record, first', 'service.srp.first': 'SRP record, first', 'service.acmp.last': 'ACMP record, last',
       'service.adp.last': 'ADP record, last', 'service.maap.last': 'MAAP record, last', 'service.aecp.last': 'AECP record, last',
       'service.srp.last': 'SRP record, last', 'backlog.acmp_command': 'an ACMP command behind a full acmp ring',
       'backlog.adp_available': 'an ENTITY_AVAILABLE behind a full adp ring', 'backlog.event': 'an event behind 15 others'}
data = {r: json.loads((root / r / 'results.json').read_text()) for pair in RUNS.values() for r in pair}
def worst(run, path):
    best = None
    for g in data[run]['results']:
        for p in g['probes']:
            if path == 'service.aecp.last' and g['group'] == 'backlog-owed':
                continue  # the owed window's own row, egress-held (tsn-c-stack #26)
            if p['path'][0] == path and p.get('status') == 'measured' and not p.get('unanswered'):
                if best is None or p['ms'] > best['ms']:
                    best = p
    return best
author = {}
for line in rows.read_text().splitlines():
    c = [x.strip() for x in line.split('|')]
    if len(c) > 6 and c[1] and c[2].replace('.', '').isdigit():
        author[c[1]] = c[3:7]
bad = 0
for path, name in ROW.items():
    cells = []
    for key in RUNS:
        vals = []
        for run in RUNS[key]:
            p = worst(run, path)
            ms = p['ms']
            if 'end_sys' in p:
                derived = (p['end_sys'] - p['start_sys']) / (data[run]['clock']['cpu_hz'] / 1000)
                if abs(derived - ms) > 0.0006:
                    print('  MISMATCH recorded/derived', run, path, ms, derived); bad += 1
            bound = BOUND.get(p['family'], 20.0)
            if p['budget_ms'] != bound and path.startswith('service.' + p['family']):
                print('  BUDGET FIELD', run, path, p['budget_ms'], 'want', bound); bad += 1
            if ms > bound: print('  OVER', run, path, ms); bad += 1
            vals.append(ms)
        cells.append(f'{vals[0]:.2f} / {vals[1]:.2f}')
    same = author.get(name) == cells
    bad += 0 if same else 1
    print(f"{name:48} {cells}  {'same as rows.md' if same else 'DIFFERS ' + str(author.get(name))}")
for key, pair in RUNS.items():
    for run in pair:
        r = data[run]; tot = over = 0; top = 0; held = [(w['group'], w['events_held']) for w in r['windows']]
        for g in r['results']:
            s = g['passes']['share']; tot += s['passes']; over += s['over']
            w = g['passes'].get('worst')
            if w: top = max(top, w['cycles'])
        print(run, f"passes {tot} over {over} longest {top/1e5:.3f} ms; cpu_hz {r['clock']['cpu_hz']} cpu_cd {r['clock']['cpu_cd']} sys {r['clock']['sys_hz']}; refusals {len(r['refusals'])}; groups {len(r['results'])}; misses {sorted(set(m.split(':')[0] for m in r['misses']))[:4]}; held {held}")
print('differences/over:', bad)

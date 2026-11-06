#!/usr/bin/env python3
"""R784-3: every published row against the amended column, read from the head's own hooks.py; each table re-rendered.

usage: amended_check.py TREE RUNS_DIR
"""
import json, sys
from pathlib import Path
tree, runs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_hooks'))
import run, hooks  # noqa: E402
for name, interfaces, point in (('1x1-idle', 1, '1x1'), ('1x1-ans', 1, '1x1'), ('8x8-idle', 2, '8x8'), ('8x8-ans', 2, '8x8')):
    d = json.loads((runs / name / 'results.json').read_text())
    rows = d['rows']
    moved = []
    srp_band = []
    for r in rows:
        am = hooks.amended_ms(r, interfaces)
        new = (not r['unbounded']) and r['ms'] <= am
        if new != r['within']:
            moved.append((r['hook'], r['probe'], r['ms'], r['bound_ms'], am, r['within'], new))
        if r['hook'] == 'H-SRP' and not r['unbounded'] and 18.0 + r['wait_ms'] < r['ms'] <= 20.0 + r['wait_ms']:
            srp_band.append((r['probe'], r['ms'], r['wait_ms']))
    allr = [r for r in rows if r['path'].startswith('counters.all')]
    per = [r for r in allr if r['path'] != 'counters.all']
    whole = [r for r in allr if r['path'] == 'counters.all']
    print(f'== {name}: {len(rows)} rows, moved {len(moved)}, SRP in the 18-20 band {len(srp_band)}')
    for m in moved:
        print('   moved', m)
    if allr:
        ceil = hooks.AMENDED_QUEUED_CEILING_MS[interfaces]
        print(f'   ALL one path {[(r["probe"], r["ms"]) for r in whole]}; per descriptor {len(per)}: over 20 {sum(r["ms"] > 20 for r in per)}, over {ceil} {sum(r["ms"] > ceil for r in per)}')
    hk = {}
    for r in rows:
        hk.setdefault(r['hook'], [0, 0])
        hk[r['hook']][0] += not r['within']
        hk[r['hook']][1] += (r['unbounded'] or r['ms'] > hooks.amended_ms(r, interfaces))
    print('   misses at base / under amended by hook', hk)
    first = [(r['probe'], r['ms']) for r in rows if r['path'] == 'counters.first']
    print('   first', first)
    spec = {k: d[k] for k in d if k in ('arm', 'cpu_clock', 'cpu_hz', 'sys_hz', 'product_cpu_hz')}
    spec['interfaces'] = interfaces
    spec.setdefault('product_cpu_hz', 100_000_000)
    graded = dict(rows=rows, refusals=d['refusals'], superseded=d.get('superseded', []), findings=d.get('findings', []),
                  checks=d.get('checks') or {})
    try:
        text = run.table(point, spec, graded)
        print('   table re-render identical:', text == (runs / name / 'table.md').read_text())
    except Exception as e:
        print('   table re-render', type(e).__name__, e, sorted(d))

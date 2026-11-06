#!/usr/bin/env python3
"""Published results at the head's own code: verdicts recomputed from the base bounds, the amended rules poisoned for
grading, and table.md regenerated and compared byte for byte. args: evidence root, clone root."""
import json, sys
from pathlib import Path
from unittest.mock import patch
ev, root = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks, hooks_build  # noqa
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import run
BASE = {'adp': 20.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 20.0, 'notify': 20.0, 'maap': 20.0, 'srp': 18.0}
for name, n_if, point in (('1x1-idle', 1, '1x1'), ('1x1-ans', 1, '1x1'), ('8x8-idle', 2, '8x8'), ('8x8-ans', 2, '8x8')):
    d = ev / f'author-r2/receipts/runs/{name}'
    res = json.load(open(d / 'results.json'))
    bad = 0
    for r in res['rows']:
        want = BASE[r['family']] + (0.0 if r['path'] == 'counters.held' else r['wait_ms'])
        ok = r['bound_ms'] == want and r['within'] == (not r['unbounded'] and r['ms'] <= want)
        bad += not ok
    def boom(*a):
        raise RuntimeError('a grade read the amended column')
    with patch.object(hooks, 'amended_service_ms', boom), patch.object(hooks, 'amended_ms', boom):
        s = run.summary(res)
    same = json.dumps(s, sort_keys=True) == json.dumps(res['summary'], sort_keys=True)
    b = json.load(open(d / 'build.json'))
    spec = dict(interfaces=n_if, arm=b['arm'], cpu_clock=b['cpu_clock'], cpu_hz=b['cpu_hz'], sys_hz=b['sys_hz'],
                product_cpu_hz=b['product_cpu_hz'])
    text = run.table(point, spec, res)
    pub = (d / 'table.md').read_text()
    print(f'{name}: {len(res["rows"])} rows, {bad} verdicts or bounds unlike the base rule; summary without the amended code equals published: {same}; '
          f'table regenerated at the head equals published: {text == pub}')

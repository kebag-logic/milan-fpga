#!/usr/bin/env python3
"""Regrade the published unloaded wire logs with the head's grader and compare to the published results.json.

usage: regrade_published.py <checkout> <evidence receipts dir> <out dir>
"""
import json, sys
from pathlib import Path
checkout, ev, out = map(Path, sys.argv[1:4])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_wire_timing'))
import wire_grade as g
out.mkdir(parents=True, exist_ok=True)
cases = [('head/ci-1x1-none', 1), ('head/8x8-none', 2)]
rc = 0
for stem, n_if in cases:
    log = (ev / f'{stem}__wire.log').read_text()
    run = json.loads((ev / f'{stem}__run.json').read_text())
    pub = json.loads((ev / f'{stem}__results.json').read_text())
    result, findings = g.grade(log, pub['sys_hz'], run['draws'], n_if, run['announces'])
    mine = dict(result, findings=findings)
    same = json.dumps(mine, sort_keys=True) == json.dumps(pub, sort_keys=True)
    (out / (stem.replace('/', '_') + '.regrade.json')).write_text(json.dumps(mine, indent=1) + '\n')
    print(f'{stem}: findings={len(findings)} identical_to_published={same} '
          f'probe_tx_n={[r["n"] for r in result["rows"] if r["path"]=="acmp.probe_tx"]}')
    rc |= (not same) or bool(findings)
sys.exit(1 if rc else 0)

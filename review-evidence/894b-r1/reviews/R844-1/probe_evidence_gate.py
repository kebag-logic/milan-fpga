"""Fault probe of the published 8x8/1if acceptance report. Supply archive root and scratch dir."""
import json
import subprocess
import sys
from pathlib import Path

archive, scratch = map(lambda x: Path(x).resolve(), sys.argv[1:3])
gate = archive / 'author-r3/scripts/gate_r3.py'
ledger = {'backlog.owed.if0': 63.24, 'backlog.owed_behind0.if0': 63.47,
          'backlog.owed_behind1.if0': 63.69, 'backlog.owed_behind2.if0': 63.91,
          'backlog.owed_behind3.if0': 64.20, 'backlog-owed.service.acmp.last.if0': 62.18,
          'backlog-owed.service.aecp.last.if0': 61.83}
for arm in ('control', 'larger-egress', 'unmeasured'):
    directory = scratch / arm
    directory.mkdir(parents=True, exist_ok=True)
    probes = [dict(probe=n, ms=ms, budget_ms=20, within_budget=False,
                   status='measured', path=['owed'], family='acmp') for n, ms in ledger.items()]
    if arm == 'larger-egress':
        probes[0]['ms'] = 100.0
    if arm == 'unmeasured':
        probes.append(dict(probe='required.cpu.row', status='unmeasured'))
    (directory / 'backlog-owed.json').write_text(json.dumps(dict(group='backlog-owed', probes=probes, passes={})))
    result = subprocess.run([sys.executable, '-I', str(gate), str(directory)], text=True, capture_output=True)
    print('ARM', arm, 'exit', result.returncode)
    print(result.stdout)
    print(result.stderr)
    # Reproduce the observed acceptance gap; this diagnostic exits nonzero if it changes.
    assert result.returncode == 0, (arm, result.returncode)
    if arm != 'control' and result.returncode == 0:
        print('ESCAPED', arm)

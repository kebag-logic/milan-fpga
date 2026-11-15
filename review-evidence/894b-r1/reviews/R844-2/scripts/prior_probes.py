"""R844-1 fixtures, unchanged; only gate invocation and expected rejection change.
Usage: prior_probes.py CHECKOUT ROUND4_GATE SCRATCH
Original: archive 843c40b1, reviews/R844-1/probe_evidence_gate.py.
"""
import json
import subprocess
import sys
from pathlib import Path

root, gate, scratch = (Path(x).resolve() for x in sys.argv[1:4])
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
    result = subprocess.run([sys.executable, '-I', '-B', str(gate), str(root), str(directory)],
                            text=True, capture_output=True)
    print('ARM', arm, 'exit', result.returncode)
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == (0 if arm == 'control' else 1)
    if arm == 'larger-egress':
        assert '- the ledger: backlog.owed.if0' in result.stdout
    if arm == 'unmeasured':
        assert '- the ledger: required.cpu.row' in result.stdout
print('PASS: original control passes; both original fault fixtures rejected by name')

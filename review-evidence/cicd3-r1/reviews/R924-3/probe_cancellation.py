#!/usr/bin/env python3
"""Usage: python3 probe_cancellation.py CHECKOUT. No files are mutated."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
import ci_events as p

world = p.parse_world(p.read_tree(root))
assert not p.check(world).findings
wf = world[p.RTL_FAST]
job = wf['jobs'][p.FIRMWARE_BOUNDARY_CAPTURE_JOB]
assert job['strategy']['fail-fast'] is True
assert not job.get('continue-on-error', False)
assert not job.get('permissions')
projected = p.project_gate_templates(world, p.Contract())
results = {}
for label, mutate, expected in p._boundary_leg_arms():
    changed = copy.deepcopy(projected)
    mutate(changed)
    c = p.check_semantic(changed)
    found = [f for f in c.findings if expected in f]
    assert found, (label, c.findings)
    results[label] = found
for setting in (False, None):
    changed = copy.deepcopy(wf)
    strategy = changed['jobs'][p.FIRMWARE_BOUNDARY_CAPTURE_JOB]['strategy']
    if setting is None:
        del strategy['fail-fast']
    else:
        strategy['fail-fast'] = setting
    c = p.Contract()
    p.check_boundary_legs(c, changed, 2)
    assert any('strategy must be exactly' in f for f in c.findings)
    results[f'independent configuration {setting}'] = c.findings
aggregate = wf['jobs']['rtl-fast']
step = next(s for s in aggregate['steps'] if s.get('name') == 'Require every applicable fast gate to pass')
aggregate_results = {}
for capture, judge, wanted in [('success', 'success', 0), ('failure', 'skipped', 1),
                                ('cancelled', 'skipped', 1), ('', 'skipped', 1)]:
    env = os.environ.copy()
    env.update({k: 'success' for k in step['env']})
    env.update(FIRMWARE_BOUNDARY_CAPTURE_RESULT=capture, FIRMWARE_BOUNDARY_RESULT=judge)
    proc = subprocess.run(['bash', '-c', step['run']], env=env, text=True, capture_output=True)
    assert proc.returncode == wanted, proc.stdout + proc.stderr
    aggregate_results[f'{capture or "missing"}/{judge}'] = proc.returncode
print(json.dumps({'matrix': job['strategy'], 'permissions': job.get('permissions'),
                  'watcher_if': wf['jobs']['ci-fail-fast']['if'],
                  'terminal_guard_if': wf['jobs']['ci-cancel-tail']['if'],
                  'boundary_arms': results, 'aggregate_exit_codes': aggregate_results}, indent=2))
print('PASS: seven standing boundary arms; false/absent fail-fast refused; failed/cancelled/missing capture cannot pass aggregate')

#!/usr/bin/env python3
"""Fresh-tree input refusal probes and focused listener/talker controls.
Usage: dynmap_probe.py FRESH_CHECKOUT PACKET VERILATOR
Runs actual generated-input recipes, then one mutation per affected leg.
"""
from pathlib import Path
import contextlib
import io
import os
import subprocess
import sys
from unittest.mock import patch

root, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
os.environ.update(VERILATOR=sys.argv[3], VERILATOR_JOBS='4', TMPDIR=str(packet / 'scratch'),
                  PYTHONDONTWRITEBYTECODE='1')
sys.path.insert(0, str(root / 'tb/verilator/milan_dp'))
import dynmap_mutants as dm

for leg, spec in dm.LEGS.items():
    suite, *_, keep = spec
    # A fake successful input recipe must not discharge the existence check.
    # Independent temporary suite paths keep the main run pristine.
    empty = packet / 'scratch' / ('missing-' + leg)
    empty.mkdir(exist_ok=True)
    replacement = (empty, *spec[1:])
    with patch.dict(dm.LEGS, {leg: replacement}), patch.object(dm.subprocess, 'run',
                      return_value=subprocess.CompletedProcess([], 0, '', '')):
        reason = dm.prepare(leg)
        assert reason and all(k in reason for k in keep), (leg, reason)
        # Check the actual campaign entry reports the refused leg and exits 1.
        mutation = next(m for m in dm.MUTATIONS if m[0] == leg)
        with patch.object(dm, 'selected', return_value=([mutation], 2)), \
             patch.object(dm, 'run_mutant', return_value=(True, ['probe: mutant execution stubbed'])):
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                rc = dm.main()
        assert rc == 1 and f'[FAIL] the {leg} leg\'s inputs are not made:' in capture.getvalue()
        print(capture.getvalue(), end='')

for leg in ('listener', 'talker'):
    suite, *_, keep = dm.LEGS[leg]
    assert not any((suite / k).exists() for k in keep), f'{leg} is not fresh'
    result = dm.prepare(leg)
    assert result is None, (leg, result)
    print(f'{leg}: actual input recipe PASS; ' + ', '.join(f'{k}={(suite/k).stat().st_size}' for k in keep), flush=True)

picks = [str(next(i for i, m in enumerate(dm.MUTATIONS, 1) if m[0] == leg)) for leg in ('listener', 'talker')]
cmd = [sys.executable, '-B', str(root / 'tb/verilator/milan_dp/dynmap_mutants.py'), '--jobs', '4', *picks]
print('COMMAND ' + repr(cmd), flush=True)
with (packet / 'dynmap-focused.log').open('w') as log:
    rc = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT).returncode
(packet / 'dynmap-focused.rc').write_text(str(rc) + '\n')
print('focused campaign rc', rc, flush=True)
sys.exit(rc)

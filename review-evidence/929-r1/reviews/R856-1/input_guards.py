#!/usr/bin/env python3
"""Exercise prepare's single-missing-file and failed-make cases without RTL builds.
Usage: input_guards.py CHECKOUT PACKET
"""
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

root, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/milan_dp'))
import dynmap_mutants as dm

checks = 0
for leg, spec in dm.LEGS.items():
    path = packet / 'scratch' / ('guard-' + leg)
    path.mkdir(exist_ok=True)
    keep = spec[-1]
    for name in keep:
        (path / name).write_bytes(b'input sentinel\n')
    with patch.dict(dm.LEGS, {leg: (path, *spec[1:])}):
        with patch.object(dm.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            assert dm.prepare(leg) is None
            for name in keep:
                (path / name).unlink()
                reason = dm.prepare(leg)
                assert reason.startswith(f'its suite did not make {name} (make rc 0:'), reason
                print(f'PASS {leg}: only {name} missing -> {reason}')
                checks += 1
                (path / name).write_bytes(b'input sentinel\n')
        with patch.object(dm.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7, '', 'input recipe failed')):
            reason = dm.prepare(leg)
            assert reason and 'make rc 7' in reason
            print(f'PASS {leg}: make failed despite all files present -> refusal')
            checks += 1
print(f'{checks} input guard probes PASS; mocked input recipes, no RTL execution')

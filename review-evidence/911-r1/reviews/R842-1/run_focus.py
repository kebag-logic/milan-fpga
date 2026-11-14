#!/usr/bin/env python3
"""Run bounded, read-only focused checks; all children are joined before exit."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

repo, packet, litex_python = map(Path, sys.argv[1:4])
scratch = packet / 'scratch'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
commands = {
    'board-table': ['python3', '-B', 'scripts/board_variants.py'],
    'board-table-controls': ['python3', '-B', 'scripts/board_variants.py', '--selftest'],
    'shape': ['python3', '-B', 'scripts/check_sweep_shape.py'],
    'shape-controls': ['python3', '-B', 'scripts/check_sweep_shape.py', '--selftest'],
    'timing-platform': ['python3', '-B', 'sw/builder/test_timing_grade.py', str(litex_python)],
    'flash-transaction': ['python3', '-B', '-c', "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; t.test_qspi_owner_transition_completed_write_prefixes()"],
    'diffcheck': ['git', 'diff', '--check', 'b7d69295', 'HEAD'],
    'variant-dry-run': ['bash', 'sw/litex/build.sh', 'ax7a200t', '--dry-run'],
    'diagrams': ['python3', '-B', 'docs/diagrams/flash_layout.gen.py', str(scratch / 'flash_layout')],
}

def run(item):
    name, cmd = item
    result = subprocess.run(cmd, cwd=repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=550)
    output = result.stdout.decode(errors='replace').replace(str(repo), '<review-tree>').replace(str(packet), '<packet>').replace(str(litex_python), '<litex-python>')
    (packet / (name + '.log')).write_text(output)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc=' + str(result.returncode), flush=True)
    return name, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, commands.items()))
(packet / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(int(any(results.values())))

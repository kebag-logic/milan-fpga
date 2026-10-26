#!/usr/bin/env python3
"""Run authorized lightweight checks in foreground; retain raw output and status."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
commands = {
    'generator-check': ['python3', 'scripts/ci_gate_workflows.py', '--check'],
    'events-check': ['python3', 'scripts/ci_events.py', '--check'],
    'events-selftest': ['python3', 'scripts/ci_events.py', '--selftest'],
    'generator-selftest': ['python3', 'scripts/ci_gate_workflows_selftest.py'],
    'workflow-plan-selftest': ['python3', 'scripts/ci_workflow_plan_selftest.py'],
    'yosys-shards-selftest': ['python3', 'scripts/yosys_shards.py', '--selftest'],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND: ' + ' '.join(command) + '\n')
        log.flush()
        try:
            result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            log.write('TIMEOUT after 540 seconds\n')
            rc = 124
    receipt = {'command': command, 'rc': rc, 'elapsed_seconds': round(time.monotonic()-start, 3)}
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, json.dumps(receipt), flush=True)
    return name, receipt

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = dict(pool.map(run, commands.items()))
(packet / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(result['rc'] for result in results.values()))

#!/usr/bin/env python3
"""Run bounded independent checks, retaining each command, log and status."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = out / 'scratch'
checks = [
    ('generator', ['scripts/ci_gate_workflows.py', '--check']),
    ('generator_selftest', ['scripts/ci_gate_workflows_selftest.py']),
    ('events_check', ['scripts/ci_events.py', '--check']),
    ('events_selftest', ['scripts/ci_events.py', '--selftest']),
    ('evidence_pins', ['scripts/generate_ci_evidence_pins.py', '--check']),
    ('scope_selftest', ['scripts/ci_scope.py', '--selftest']),
    ('workflow_plan', ['scripts/ci_workflow_plan_selftest.py']),
    ('manifest', ['scripts/ci_manifest_selftest.py']),
    ('runtime_evidence', ['scripts/ci_runtime_evidence_selftest.py']),
    ('install_cache', ['scripts/ci_install_cache_selftest.py']),
]

def run(entry):
    name, args = entry
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'TMPDIR': str(work), 'PYTHONDONTWRITEBYTECODE': '1'}
    started = time.time()
    with (out / (name + '.log')).open('w') as log:
        log.write('COMMAND: python3 ' + ' '.join(args) + '\n')
        log.flush()
        try:
            rc = subprocess.run([sys.executable, *args], cwd=root, env=env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=570).returncode
        except subprocess.TimeoutExpired:
            rc = 124
            log.write('CHECK TIMEOUT 570 seconds\n')
    record = {'command': ['python3', *args], 'rc': rc, 'elapsed_s': round(time.time()-started, 3)}
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, json.dumps(record), flush=True)
    return name, record

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, checks))
(out / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(int(any(item['rc'] for item in results.values())))

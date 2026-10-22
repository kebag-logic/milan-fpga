#!/usr/bin/env python3
"""Run bounded, read-only adoption checks; preserve each command and exit code."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
checks = {
    'resource-baseline': ['python3', 'syn/ooc/pp_resource_gate.py', 'check-baseline'],
    'submodule-records': ['python3', 'scripts/check_submodule_docs.py'],
    'gptp-records': ['python3', 'scripts/check_gptp_docs.py', '--with-submodule'],
    'boundary-generator': ['python3', 'docs/diagrams/submodule_boundaries.gen.py', '--check'],
    'timesync-generator': ['python3', 'docs/diagrams/timesync_chain.gen.py', '--check'],
    'diagram-pngs': ['python3', 'scripts/check_diagram_pngs.py'],
    'port-contracts': ['python3', 'scripts/check_port_contracts.py'],
    'naming': ['python3', 'scripts/measure_naming.py', '--check'],
    'test-evidence': ['python3', 'scripts/measure_test_evidence.py', '--check'],
    'capture': ['python3', 'scripts/check_nvm_capture.py'],
    'integrator-params': ['python3', 'protocol-processor/scripts/check-integrator-params.py'],
}

def run(item):
    name, command = item
    with (packet / (name + '.log')).open('wb') as log:
        p = subprocess.run(command, cwd=repo, env=env, stdout=log,
                           stderr=subprocess.STDOUT, timeout=300)
    result = {'command': command, 'rc': p.returncode}
    (packet / (name + '.rc')).write_text(str(p.returncode) + '\n')
    return name, result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, checks.items()))
(packet / 'check-results.json').write_text(json.dumps(results, indent=2) + '\n')
for name, result in results.items():
    print(name, result['rc'])
sys.exit(any(r['rc'] for r in results.values()))

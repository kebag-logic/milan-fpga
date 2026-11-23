#!/usr/bin/env python3
"""Run bounded review checks concurrently, retaining raw outputs and exits.

Usage: python3 run_focused.py REPO PACKET
No background shell jobs or detached processes are used.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True, parents=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
commands = {
    'focused-gates': ['python3', '-B', 'sw/builder/test_builder.py', '--gates',
        'test_builder_doc_key_map,test_host_profile_feeds_the_generators,test_host_profile_refusals',
        '--receipt', str(packet / 'focused-gates.json')],
    'docs-check': ['python3', '-B', 'scripts/docs_check.py'],
    'baremetal-check': ['python3', '-B', 'scripts/check_baremetal_only.py', '--check'],
    'baremetal-selftest': ['python3', '-B', 'scripts/check_baremetal_only.py', '--selftest'],
    'em-dash': ['python3', '-B', 'scripts/check_em_dash.py', '--base',
                '854bd7236792ce1adbd10c43b13a6a5002ad3bb6'],
    'doc-paths': ['python3', '-B', 'scripts/check_doc_paths.py'],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND: ' + json.dumps(command) + '\n')
        log.flush()
        result = subprocess.run(command, cwd=repo, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=540)
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return dict(name=name, rc=result.returncode, seconds=round(time.monotonic()-start, 3))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
(packet / 'focused-summary.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
sys.exit(any(r['rc'] for r in results))

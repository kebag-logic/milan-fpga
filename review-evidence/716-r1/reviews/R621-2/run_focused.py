#!/usr/bin/env python3
"""Run focused review gates from the candidate root; all children are joined."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
commands = {
    'ci-check': ['scripts/ci_events.py', '--check'],
    'ci-selftest': ['scripts/ci_events.py', '--selftest'],
    'command-census': ['scripts/ci_events.py', '--firmware-census'],
    'shard-selftest': ['sw/firmware/ctrl/test/test_ctrl_firmware_shards.py', '--census', str(packet / 'shards.json')],
    'scope-selftest': ['scripts/ci_scope.py', '--selftest'],
    'coverage-selftest': ['sw/firmware/gtest/fw_coverage.py', '--selftest'],
    'srp-comparator': ['sw/firmware/ctrl/test/srp_wire_compare.py', '--self-test'],
    'docs-check': ['scripts/docs_check.py'],
    'doc-style': ['scripts/check_doc_style.py'],
}
if len(sys.argv) > 1:
    commands = {name: commands[name] for name in sys.argv[1:]}

def run(item):
    name, args = item
    start = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        result = subprocess.run([sys.executable, *args], env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    seconds = time.monotonic() - start
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(f'{name}: rc={result.returncode}, {seconds:.3f}s', flush=True)
    return dict(name=name, command=['python3', *[a.replace(str(packet), '<packet>') for a in args]], rc=result.returncode, seconds=seconds)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
results_path = packet / 'focused-results.json'
prior = json.loads(results_path.read_text()) if results_path.exists() else []
results = [r for r in prior if r['name'] not in commands] + results
results_path.write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(int(any(r['rc'] for r in results)))

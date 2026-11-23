#!/usr/bin/env python3
"""Run independent light checks concurrently, joining all before return."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
budget = repo / 'tb/verilator/ctrl_service_budget'
jobs = {
 'focused-gates': (repo, [sys.executable, '-B', 'sw/builder/test_builder.py', '--gates', 'test_bad_configs_rejected,test_builder_doc_key_map,test_host_profile_feeds_the_generators,test_host_profile_refusals']),
 'delta-probe': (repo, [sys.executable, '-B', str(packet / 'delta_probe.py'), str(repo)]),
 'shape-check': (repo, [sys.executable, '-B', str(budget / 'shape_costs.py'), '--check']),
 'shape-selftest': (repo, [sys.executable, '-B', str(budget / 'shape_costs.py'), '--selftest']),
 'load-check': (repo, [sys.executable, '-B', str(budget / 'load_grade.py'), '--check']),
 'flip-1x1': (repo, [sys.executable, '-B', str(budget / 'flip_grade.py'), '--check', '--point', '1x1/1if']),
 'flip-all': (repo, [sys.executable, '-B', str(budget / 'flip_grade.py'), '--check']),
 'docs-check': (repo, [sys.executable, '-B', 'scripts/docs_check.py']),
}
def run(item):
    name, (cwd, cmd) = item
    with (packet / (name + '.log')).open('wb') as log:
        p = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=480)
    (packet / (name + '.rc')).write_text(str(p.returncode) + '\n')
    print(name, 'rc', p.returncode, flush=True)
    return name, p.returncode
with ThreadPoolExecutor(max_workers=4) as pool:
    result = dict(pool.map(run, jobs.items()))
(packet / 'focused-result.json').write_text(json.dumps(result, indent=2) + '\n')
assert all(rc == (1 if name == 'flip-all' else 0) for name, rc in result.items()), result

#!/usr/bin/env python3
"""Run bounded independent checks concurrently, waiting for every process."""
import concurrent.futures
import os
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['TMPDIR'] = str(out / 'scratch')
jobs = {
    'behave': (repo / 'tests', ['behave', '--no-capture', '-f', 'plain']),
    'module-matrix': (repo, ['python3', 'docs/traceability/gen_module_matrix.py', '--check']),
}
def run(item):
    name, (cwd, command) = item
    with (out / f'{name}.log').open('w') as log:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (out / f'{name}.rc').write_text(f'{result.returncode}\n')
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, jobs.items()))
for name, rc in results:
    print(f'{name}: rc={rc}')
sys.exit(any(rc for _, rc in results))

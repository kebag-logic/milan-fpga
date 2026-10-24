#!/usr/bin/env python3
"""Run the published review probes on source objects and disposable clones."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = out / 'scratch'
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
lock = json.loads((repo / 'ci/image/sources.lock.json').read_text())['host_tools']['shfmt']
binary = scratch / 'shfmt'
if not binary.exists():
    binary.write_bytes(urllib.request.urlopen(lock['url']).read())
assert hashlib.sha256(binary.read_bytes()).hexdigest() == lock['sha256']
binary.chmod(0o755)
env['CI_IMAGE_SHFMT'] = str(binary)
(out / 'shfmt-identity.log').write_text(f"{lock['version']} {lock['sha256']}\n")

def run(name, args, cwd=repo):
    with (out / f'{name}.log').open('w') as log:
        result = subprocess.run(args, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (out / f'{name}.rc').write_text(f'{result.returncode}\n')
    return name, result.returncode

def inventory(label, revision):
    clone = scratch / f'inventory-{label}'
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', str(repo), str(clone)], check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '-q', '--detach', revision], check=True)
    return run(f'inventory-{label}', [sys.executable, str(out / 'inventory_walk.py'), str(clone)], clone)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    tasks = [
        pool.submit(run, 'frame-bytes', [sys.executable, str(out / 'bdd_frame_bytes_probe.py'), str(repo), 'a032c6d6', 'HEAD']),
        pool.submit(run, 'matrix-clause', [sys.executable, str(out / 'matrix_clause_probe.py'), str(repo), 'HEAD']),
        pool.submit(inventory, 'head', '01fc54756f1ffb0a3aa836681215e8321ee7e86c'),
        pool.submit(inventory, 'base', 'a032c6d6e3775f145349d5a495c1e1ad12294936'),
    ]
    results = [task.result() for task in tasks]
for name, rc in results:
    print(f'{name}: rc={rc}')
sys.exit(any(rc for _, rc in results))

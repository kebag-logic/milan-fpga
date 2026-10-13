#!/usr/bin/env python3
"""Check merge composition and independently reconcile the live shard lists."""
import argparse
import ast
import concurrent.futures
import json
import os
import subprocess
from pathlib import Path

BASE = 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
DEV = 'd5858bbee328cf8d2c39a99ec14203f5d0ddd123'
SOURCE = '2c2f336979e4fdb1da444f041f37551e2c9175df'
HEAD = 'b89a1ded1596030c4e0baf45a8509a20cbe04933'
p = argparse.ArgumentParser()
p.add_argument('--repo', required=True, type=Path)
p.add_argument('--packet', required=True, type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'PYTHONDONTWRITEBYTECODE': '1',
       'TMPDIR': str(packet / 'scratch/tmp')}
def git(*args):
    return subprocess.check_output(['git', '-c', 'core.commitGraph=false', *args], cwd=repo, env=env)
def paths(start, end):
    return set(git('diff', '--no-renames', '--name-only', start, end).decode().splitlines())
def blob(rev, path):
    return git('show', f'{rev}:{path}')

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
source_paths, predecessor_paths = paths(BASE, SOURCE), paths(BASE, DEV)
overlap = sorted(source_paths & predecessor_paths)
assert overlap == ['docs/testing/CI_WORKFLOWS.md', 'docs/testing/TESTING.md']
assert paths(DEV, HEAD) == source_paths
print('Source changes:', sorted(source_paths))
print('Predecessor changes:', sorted(predecessor_paths))
print('Exact overlap:', overlap)
print(git('log', '--oneline', '--first-parent', f'{BASE}..{DEV}').decode())
scratch = packet / 'scratch/composition'
scratch.mkdir(parents=True, exist_ok=True)
for path in sorted(source_paths | predecessor_paths):
    if path in overlap:
        inputs = []
        for name, rev in [('dev', DEV), ('base', BASE), ('source', SOURCE)]:
            f = scratch / (path.replace('/', '_') + '.' + name)
            f.write_bytes(blob(rev, path)); inputs.append(str(f))
        r = subprocess.run(['git', 'merge-file', '-p', *inputs], capture_output=True, env=env)
        assert r.returncode == 0 and r.stdout == blob(HEAD, path), path
        print('PASS exact three-way text composition:', path)
    else:
        owner = SOURCE if path in source_paths else DEV
        assert git('ls-tree', HEAD, '--', path) == git('ls-tree', owner, '--', path), path
print('PASS every nonoverlapping changed entry retains its owning source mode and blob')
for path in ['.github/workflows/rtl.yml', 'scripts/run_all_suites.sh', 'scripts/suite_tally.py',
             'protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/lwSRP']:
    entries = [git('ls-tree', rev, '--', path) for rev in (BASE, DEV, SOURCE, HEAD)]
    assert len(set(entries)) == 1, path
    print('PASS unchanged across all four trees:', path, entries[0].decode().strip())
def inventory(rev):
    return sorted(x.split('/')[2] for x in git('ls-tree', '-r', '--name-only', rev, '--', 'tb/verilator').decode().splitlines()
                  if x.startswith('tb/verilator/') and x.count('/') == 3 and x.endswith('/Makefile'))
inventories = [inventory(rev) for rev in (BASE, DEV, SOURCE, HEAD)]
assert all(x == inventories[0] for x in inventories)
assert 'milan_dp_gptp' in inventories[0]
print('PASS unchanged full Makefile inventory:', len(inventories[0]))
def shard(index):
    cmd = ['bash', 'scripts/run_all_suites.sh', '--shard', f'{index}/5', '--list']
    r = subprocess.run(cmd, cwd=repo, env=env, text=True, capture_output=True, timeout=60)
    (packet / 'receipts' / f'shard-{index}.log').write_text(r.stdout + r.stderr)
    (packet / 'receipts' / f'shard-{index}.rc').write_text(str(r.returncode) + '\n')
    assert r.returncode == 0, r.stderr
    return r.stdout.splitlines()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    shards = list(pool.map(shard, range(5)))
flat = sum(shards, [])
expected = sorted(set(inventories[0]) - {'milan_dp_gptp'})
assert sorted(flat) == expected and len(flat) == len(set(flat))
assert shards[4] == ['milan_dp'] and 'tsn_fuzz' in shards[1] and 'chmap_capture' in shards[3]
print('PASS live driver lists are disjoint and complete:', len(flat), 'default suites')
module = ast.parse((repo / 'scripts/suite_shards.py').read_text())
values = {n.targets[0].id: ast.literal_eval(n.value) for n in module.body if isinstance(n, ast.Assign)
          and isinstance(n.targets[0], ast.Name) and n.targets[0].id in {'SUITE_SECONDS', 'WORKER_OVERHEAD_SECONDS'}}
seconds, overhead = values['SUITE_SECONDS'], values['WORKER_OVERHEAD_SECONDS']
assert sorted(seconds) == expected
prediction = [overhead[i] + sum(seconds[s] for s in shard) for i, shard in enumerate(shards)]
import yaml
workflow = yaml.safe_load((repo / '.github/workflows/rtl.yml').read_text())
job = workflow['jobs']['verilator-shards']
bound = job['timeout-minutes'] * 36
assert len(shards) == job['strategy']['matrix']['total'][0]
assert all(n <= bound for n in prediction)
print('PASS independent sum over real lists:', prediction, 'bound:', bound)
print('PASS composition introduces no durationless suite or provisional entry')

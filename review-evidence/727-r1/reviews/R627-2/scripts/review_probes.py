#!/usr/bin/env python3
"""Focused independent review. Usage: review_probes.py CHECKOUT PACKET."""
import ast
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import random
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
receipts = packet / 'receipts'
scratch = packet / 'scratch'
receipts.mkdir(exist_ok=True)
scratch.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))

def run(name, argv, cwd=root, expected=0, extra=None):
    result = subprocess.run(argv, cwd=cwd, env={**env, **(extra or {})},
                            text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=540)
    (receipts / (name + '.log')).write_text(result.stdout)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    assert result.returncode == expected, (name, result.returncode, result.stdout[-2000:])
    return result.stdout

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result

m = module(root / 'scripts/suite_shards.py', 'current_selector')
run('selector-selftest', ['python3', 'scripts/suite_shards.py', '--selftest'])
commands = [(f'list-{i}-5', ['bash', 'scripts/run_all_suites.sh', '--shard', f'{i}/5', '--list']) for i in range(5)]
commands += [('list-serial', ['bash', 'scripts/run_all_suites.sh', '--shard', '0/1', '--list']),
             ('list-default', ['bash', 'scripts/run_all_suites.sh', '--list']),
             ('list-physical', ['bash', 'scripts/run_all_suites.sh', '--physical-gptp', '--list'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    lists = dict(zip((n for n, _ in commands), pool.map(lambda x: run(*x), commands)))
inventory = sorted(p.parent.name for p in (root/'tb/verilator').glob('*/Makefile') if p.parent.name != 'milan_dp_gptp')
flat = [s for i in range(5) for s in lists[f'list-{i}-5'].splitlines()]
assert sorted(flat) == inventory and len(flat) == len(set(flat)) == 62
assert lists['list-serial'] == lists['list-default'] == ''.join(s+'\n' for s in inventory)
assert lists['list-physical'] == 'milan_dp_gptp\n'
assert lists['list-4-5'] == 'milan_dp\n'
assert 'tsn_fuzz' in lists['list-1-5'].splitlines()
assert 'chmap_capture' in lists['list-3-5'].splitlines()

# Implement the assignment independently from the stated law.
load = list(m.WORKER_OVERHEAD_SECONDS)
owners = {'milan_dp': 4, 'tsn_fuzz': 1, 'chmap_capture': 3}
for suite, worker in owners.items():
    load[worker] += m.SUITE_SECONDS[suite]
for suite in sorted(set(inventory)-owners.keys(), key=lambda s: (-m.SUITE_SECONDS[s], s)):
    worker = min(range(4), key=lambda i: (load[i], i))
    owners[suite] = worker
    load[worker] += m.SUITE_SECONDS[suite]
assert m.balance(inventory, 5) == (owners, load)
assert load == [4204, 4205, 4203, 4205, 2877]
for i in range(5):
    assert lists[f'list-{i}-5'].splitlines() == [s for s in inventory if owners[s] == i]
for seed in (0, 1, 2, 12345):
    for i in range(5):
        actual = run(f'hash-{seed}-{i}', ['python3', 'scripts/suite_shards.py', '--suite-root', 'tb/verilator', '--shard', f'{i}/5'], extra={'PYTHONHASHSEED': str(seed)})
        assert actual == lists[f'list-{i}-5']
rng = random.Random(727)
for _ in range(30):
    shuffled = inventory.copy()
    rng.shuffle(shuffled)
    assert m.balance(shuffled, 5) == (owners, load)

# Compare the old serial selector and round-1 assignment without editing source.
for rev, label in [('c6bd08c6','base'), ('a57d384d','round1')]:
    path = scratch / (label + '_selector.py')
    path.write_bytes(subprocess.check_output(['git', 'show', rev+':scripts/suite_shards.py'], cwd=root))
    old = module(path, label+'_selector')
    assert old.select_suites(inventory, 0, 1) == inventory
    if label == 'round1':
        assert m.SUITE_SECONDS == old.SUITE_SECONDS
        assert m.WORKER_OVERHEAD_SECONDS == old.WORKER_OVERHEAD_SECONDS
        for i in range(5):
            assert old.select_suites(inventory, i, 5) == lists[f'list-{i}-5'].splitlines()

# Independent fault plants call the shipped command inside minimal copies.
source = (root / 'scripts/suite_shards.py').read_text()
workflow = (root / '.github/workflows/rtl.yml').read_text()
faults = {
    'missing-duration': (source.replace('    "aaf": 73,\n', ''), workflow, 1, 'no recorded duration'),
    'stale-duration': (source.replace('SUITE_SECONDS = {', 'SUITE_SECONDS = {\n    "retired_suite": 1,', 1), workflow, 1, 'not in the inventory'),
    'zero-duration': (source.replace('    "aaf": 73,', '    "aaf": 0,'), workflow, 1, 'positive whole number'),
    'heavy-duration': (source.replace('    "milan_dp_mclk": 2038,', '    "milan_dp_mclk": 10000,'), workflow, 1, 'FAIL head worker'),
    'tight-timeout': (source, workflow.replace('    timeout-minutes: 120', '    timeout-minutes: 116'), 1, 'FAIL head worker'),
    'six-workers': (source, workflow.replace('        total: [5]', '        total: [6]'), 1, 'describes 5 workers'),
    'missing-workflow': (source, None, 1, 'FAIL head'),
}
summary = {}
for name, (text, config, code, needle) in faults.items():
    tree = scratch / ('fault-' + name)
    (tree / 'scripts').mkdir(parents=True, exist_ok=True)
    (tree / '.github/workflows').mkdir(parents=True, exist_ok=True)
    (tree / 'scripts/suite_shards.py').write_text(text)
    if config is not None:
        (tree / '.github/workflows/rtl.yml').write_text(config)
    for suite in inventory + ['milan_dp_gptp']:
        d = tree / 'tb/verilator' / suite
        d.mkdir(parents=True, exist_ok=True)
        (d / 'Makefile').touch()
    out = run('fault-'+name, ['python3','scripts/suite_shards.py','--selftest'], tree, code)
    assert needle in out
    summary[name] = {'rc':code,'diagnostic':needle}
    if name in ('missing-duration','stale-duration'):
        run('selection-'+name, ['python3','scripts/suite_shards.py','--suite-root','tb/verilator','--shard','0/5'], tree, 2)
        serial = run('serial-'+name, ['python3','scripts/suite_shards.py','--suite-root','tb/verilator','--shard','0/1'], tree)
        assert serial == lists['list-serial']

# The independent law is a literal 36 seconds/minute and reads neither DUT symbol.
tree = ast.parse(source)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='planted_selftest')
expected = next(n for n in fn.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='expected' for t in n.targets))
assert isinstance(expected.value, ast.DictComp)
assert ast.unparse(expected.value.value) == 'minutes * 36'
assert not {'HEADROOM_PERCENT','bound_seconds'} & {n.id for n in ast.walk(expected) if isinstance(n, ast.Name)}
unchanged = ['.github/workflows/rtl.yml','scripts/run_all_suites.sh','scripts/suite_tally.py']
for path in unchanged:
    assert subprocess.check_output(['git','show','c6bd08c6:'+path],cwd=root) == (root/path).read_bytes()
(receipts/'assignment.json').write_text(json.dumps({'owners':owners,'predicted_seconds':load,'counts':[len(lists[f'list-{i}-5'].splitlines()) for i in range(5)],'inventory':len(inventory),'seed_checks':[0,1,2,12345],'shuffle_checks':30,'unchanged':unchanged,'round1_lists_identical':True,'independent_bound_oracle':ast.unparse(expected),'faults':summary},indent=2)+'\n')
print('PASS: 62-suite union, disjointness, independent assignment, 4 process seeds, 30 input permutations, serial/base equality, round-1 equality, 7 fault plants, 36-second oracle.')

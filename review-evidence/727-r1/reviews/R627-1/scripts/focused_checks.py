#!/usr/bin/env python3
"""Reproduce R627's bounded selector review against an explicit checkout."""
import argparse
import concurrent.futures
import heapq
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--probes-only', action='store_true')
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
out, scratch = packet / 'receipts', packet / 'scratch'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch), GIT_NO_REPLACE_OBJECTS='1')
sys.dont_write_bytecode = True
source = (repo / 'scripts/suite_shards.py').read_text()
workflow = (repo / '.github/workflows/rtl.yml').read_text()

def run(label, command, cwd=repo, expected=0):
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
    (out / (label + '.log')).write_text(result.stdout)
    (out / (label + '.rc')).write_text(str(result.returncode) + '\n')
    print(label, 'rc=' + str(result.returncode), flush=True)
    if expected is not None:
        assert result.returncode == expected, (label, result.stdout[-3000:])
    return result

def namespace(text=source):
    ns = {'__file__': str(repo / 'scripts/suite_shards.py'), '__name__': 'review_selector'}
    exec(compile(text, ns['__file__'], 'exec'), ns)
    return ns

ns = namespace()
inventory = sorted(d.name for d in (repo / 'tb/verilator').iterdir()
                   if d.is_dir() and (d / 'Makefile').is_file() and d.name != 'milan_dp_gptp')

commands = [
    ('selector-selftest', [sys.executable, 'scripts/suite_shards.py', '--selftest']),
    ('ci-events-check', [sys.executable, 'scripts/ci_events.py', '--check']),
    ('ci-events-selftest', [sys.executable, 'scripts/ci_events.py', '--selftest']),
    ('cancellation', [sys.executable, 'scripts/test_suite_cancellation.py']),
    ('suite-tally-selftest', [sys.executable, 'scripts/suite_tally.py', '--selftest']),
    ('diff-check', ['git', 'diff', '--check', 'c6bd08c6', 'HEAD']),
]
if not a.probes_only:
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [pool.submit(run, label, command) for label, command in commands]
        for job in jobs:
            job.result()

lists = []
for i in range(5):
    lists.append(run(f'list-{i}-5', ['bash', 'scripts/run_all_suites.sh', '--shard', f'{i}/5', '--list']).stdout.splitlines())
serial = run('list-serial', ['bash', 'scripts/run_all_suites.sh', '--shard', '0/1', '--list']).stdout.splitlines()
default = run('list-default', ['bash', 'scripts/run_all_suites.sh', '--list']).stdout.splitlines()
physical = run('list-physical', ['bash', 'scripts/run_all_suites.sh', '--physical-gptp', '--list']).stdout.splitlines()
flat = sum(lists, [])
assert sorted(flat) == inventory == serial == default
assert len(flat) == len(set(flat)) == 62
assert lists[4] == ['milan_dp'] and 'tsn_fuzz' in lists[1] and 'chmap_capture' in lists[3]
assert physical == ['milan_dp_gptp']
old_source = subprocess.check_output(['git', 'show', 'c6bd08c6:scripts/suite_shards.py'], cwd=repo, text=True)
old = namespace(old_source)
assert old['sweep_suites'](repo / 'tb/verilator') == serial
assert old['select_suites'](serial, 0, 1) == serial
assert ns['select_suites'](['future_suite', 'milan_dp'], 0, 1, {}) == ['future_suite', 'milan_dp']

# A separate heap implementation checks every owner and load, including both tie rules.
seconds = ns['SUITE_SECONDS']
loads = list(ns['WORKER_OVERHEAD_SECONDS'])
owners = {'milan_dp': 4, 'tsn_fuzz': 1, 'chmap_capture': 3}
for suite, worker in owners.items():
    loads[worker] += seconds[suite]
heap = [(loads[i], i) for i in range(4)]
heapq.heapify(heap)
for suite in sorted(set(inventory) - set(owners), key=lambda s: (-seconds[s], s)):
    load, worker = heapq.heappop(heap)
    owners[suite] = worker
    loads[worker] = load + seconds[suite]
    heapq.heappush(heap, (loads[worker], worker))
assert ns['balance'](inventory, 5) == (owners, loads)
rng = random.Random(727627)
for _ in range(50):
    shuffled = rng.sample(inventory, len(inventory))
    assert ns['balance'](shuffled, 5) == (owners, loads)
assert [sorted(s for s in inventory if owners[s] == i) for i in range(5)] == lists
summary = {'inventory_count': len(inventory), 'list_counts': list(map(len, lists)),
           'loads': loads, 'owners': owners, 'independent_heap_oracle': 'PASS',
           '50_inventory_permutations': 'PASS', 'serial_matches_base': 'PASS',
           'serial_without_table': 'PASS', 'physical_partition': physical}
(out / 'assignment.json').write_text(json.dumps(summary, indent=2) + '\n')

# Every mutant stays in a disposable tree. The candidate remains untouched.
mutants = {
    'missing-free': source.replace('for suite in suites if suite not in seconds]',
                                   'for suite in suites if False]')
                         .replace('load[fixed[suite]] += seconds[suite]', 'load[fixed[suite]] += seconds.get(suite, 0)')
                         .replace('(-seconds[suite], suite)', '(-seconds.get(suite, 0), suite)')
                         .replace('load[worker] += seconds[suite]', 'load[worker] += seconds.get(suite, 0)'),
    'stale-ignored': source.replace('for suite in sorted(set(seconds) - inventory)]',
                                    'for suite in []]'),
    'timeout-mirrored': source.replace('bound = bound_seconds(timeout)', 'bound = bound_seconds(120)'),
    'overhead-dropped': source.replace('load = list(overhead) if layout else [0] * total',
                                       'load = [0] * total'),
    'mean-only': source.replace('if value > bound]', 'if sum(load) / len(load) > bound]'),
    'inclusive-bound': source.replace('if value > bound]', 'if value >= bound]'),
    'pin-dropped': source.replace('fixed.update(PINNED_SUITES)', 'pass'),
    'bound-disabled': source.replace('if value > bound]', 'if False]'),
    'measure-from-job-start': source.replace('windows, previous = {}, start', 'windows, previous = {}, first'),
}
mutation_summary = {}
for label, text in mutants.items():
    assert text != source
    root = scratch / ('mutant-' + label)
    (root / 'scripts').mkdir(parents=True, exist_ok=True)
    (root / '.github/workflows').mkdir(parents=True, exist_ok=True)
    (root / 'scripts/suite_shards.py').write_text(text)
    (root / '.github/workflows/rtl.yml').write_text(workflow)
    for suite in inventory + ['milan_dp_gptp']:
        d = root / 'tb/verilator' / suite
        d.mkdir(parents=True, exist_ok=True)
        (d / 'Makefile').touch()
    r = run('mutant-' + label, [sys.executable, 'scripts/suite_shards.py', '--selftest'], root, expected=1)
    markers = [line.strip() for line in r.stdout.splitlines() if 'ESCAPED' in line or 'FAIL' in line]
    mutation_summary[label] = markers
    if label in ('missing-free', 'stale-ignored', 'timeout-mirrored', 'overhead-dropped', 'mean-only', 'inclusive-bound', 'bound-disabled'):
        assert any('ESCAPED' in line for line in markers), label
(out / 'mutations.json').write_text(json.dumps(mutation_summary, indent=2) + '\n')

# Tree-level faults exercise the actual entry point before any suite runs.
faults = ['missing-duration', 'stale-duration', 'heavy-duration', 'tight-timeout', 'six-workers', 'missing-workflow']
for fault in faults:
    root = scratch / ('fault-' + fault)
    (root / 'scripts').mkdir(parents=True, exist_ok=True)
    (root / '.github/workflows').mkdir(parents=True, exist_ok=True)
    text = source.replace('"gptp_plane": 784,', '"gptp_plane": 1284,') if fault == 'heavy-duration' else source
    (root / 'scripts/suite_shards.py').write_text(text)
    wf = workflow
    if fault == 'tight-timeout':
        wf = ns['with_verilator_timeout'](wf, 116)
    if fault == 'six-workers':
        wf = wf.replace('        total: [5]', '        total: [6]')
    if fault != 'missing-workflow':
        (root / '.github/workflows/rtl.yml').write_text(wf)
    suites = inventory.copy()
    if fault == 'missing-duration':
        suites.append('unmeasured_suite')
    if fault == 'stale-duration':
        suites.remove('aaf')
    for suite in suites:
        d = root / 'tb/verilator' / suite
        d.mkdir(parents=True, exist_ok=True)
        (d / 'Makefile').touch()
    run('fault-' + fault, [sys.executable, 'scripts/suite_shards.py', '--selftest'], root, expected=1)
    if fault in ('missing-duration', 'stale-duration'):
        run('selection-' + fault, [sys.executable, 'scripts/suite_shards.py', '--suite-root', 'tb/verilator', '--shard', '0/5'], root, expected=2)
        run('serial-' + fault, [sys.executable, 'scripts/suite_shards.py', '--suite-root', 'tb/verilator', '--shard', '0/1'], root)
print('FOCUSED REVIEW PASS', flush=True)

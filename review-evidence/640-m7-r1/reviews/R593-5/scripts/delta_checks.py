#!/usr/bin/env python3
"""Independent inventory and guard probes; no source writes."""
import collections
import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo / 'scripts'))
import suite_shards as shards
import ci_events as ci

def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo, text=True)

before = '412e3f6c8c402bce63e94c291d2782b5579aaa1d'
changed = git('diff', '--name-only', before, 'HEAD').splitlines()
assert len(changed) == 7
assert not git('diff', before, 'HEAD', '--', 'hdl', 'gptp-processor')
print('PASS delta: seven files, no RTL or donor-pin change')
cpp = 'tb/verilator/gptp_tables/sim_main.cpp'
def executable(text):
    return [line for line in text.splitlines() if not line.lstrip().startswith('//')]
assert executable(git('show', f'{before}:{cpp}')) == executable((repo / cpp).read_text())
print('PASS harness delta contains whole-line comments only')

def inventory(rev):
    return sorted('/'.join(p.split('/')[2:-1]) for p in git('ls-tree', '-r', '--name-only', rev, 'tb/verilator').splitlines()
                  if p.startswith('tb/verilator/') and len(p.split('/')) == 4 and p.endswith('/Makefile'))
assert inventory(before) == inventory('HEAD')
print('PASS no suite Makefile added, removed or renamed in delta')

lists = []
for index in range(6):
    result = subprocess.run(['scripts/run_all_suites.sh', '--shard', f'{index}/6', '--list'], cwd=repo, capture_output=True, text=True, check=True)
    (packet / 'receipts' / f'shard-{index}.txt').write_text(result.stdout)
    lists.append(result.stdout.splitlines())
serial = subprocess.check_output(['scripts/run_all_suites.sh', '--list'], cwd=repo, text=True).splitlines()
(packet / 'receipts/serial-inventory.txt').write_text('\n'.join(serial) + '\n')
counts = collections.Counter(x for group in lists for x in group)
assert sorted(counts) == serial and set(counts.values()) == {1}
assert counts['gptp_tables'] == 1 and 'gptp_tables' in lists[0]
assert lists[5] == ['milan_dp'] and 'tsn_fuzz' in lists[1] and 'chmap_capture' in lists[3]
print(f'PASS {len(serial)} default suites exactly once; gptp_tables=0/6; milan_dp alone=5/6')

missing = dict(shards.SUITE_SECONDS)
del missing['gptp_tables']
try:
    shards.balance(serial, 6, missing)
except ValueError as exc:
    assert 'gptp_tables: inventory suite with no recorded duration' in str(exc)
    print('PASS missing-duration control:', exc)
else:
    raise AssertionError('missing duration accepted')
_, old_load = shards.balance(serial, 5, overhead=(83,115,80,93,80))
assert max(old_load) > 4320
print('PASS provisional duration at five workers exceeds bound:', old_load, '> 4320')
_, new_load = shards.balance(serial, 6)
assert max(new_load) <= 4320
print('PASS six-worker loads:', new_load, '<= 4320')

pristine = ci.parse_world(ci.read_tree(repo))
assert not ci.check(pristine).findings
for denominator in ('3', '4', '5', '7'):
    world = copy.deepcopy(pristine)
    job = ci.jobs(world[ci.RTL_FULL])['verilator-shards']
    job['name'] = job['name'].replace(ci.DERIVED_SHARD_TOTAL, denominator)
    findings = ci.check(world).findings
    assert any('denominator' in f for f in findings), findings
    print(f'PASS stale literal job-name denominator {denominator}:', findings)
for label, mutation in [
    ('matrix grows but denominator stays', ci._m_shard_denominator_stale),
    ('dedicated worker dropped', ci._m_dedicated_worker_dropped),
    ('matrix and total shrink but expect stays', ci._m_dedicated_worker_reverted),
    ('dedicated ownership arm dropped', ci._m_ownership_dedicated_arm_dropped),
    ('dedicated ownership widened', ci._m_ownership_dedicated_arm_widened),
    ('matrix grows but expect stays', ci._m_matrix_grows_expect_stays),
]:
    world = copy.deepcopy(pristine)
    mutation(world)
    findings = ci.check(world).findings
    assert findings
    print('PASS', label, ':', findings)
print('PASS independent delta checks')

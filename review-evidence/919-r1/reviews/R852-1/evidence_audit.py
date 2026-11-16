#!/usr/bin/env python3
"""Audit selected public receipts directly from their immutable Git archive; no builds or source edits."""
import ast
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

ARCHIVE = 'c129707b2d1d3b84c746849c9201b96ef2b1499d'
HEAD = 'afa3ea19d6a1075382c63e4fc1e188a9aadf33bb'
BASE = '70f4056f384e12520ccae254fe26f6286fd39db6'
PRE = 'c805f6999ee873240fcee63354a46022de1fd7bf'
PREFIX = 'review-evidence/919-r1/author-r2/receipts/'
packet = Path(__file__).resolve().parent
hashes = {}

def git(*args):
    return subprocess.check_output(['git', *args]).decode()

def receipt(name):
    path = PREFIX + name
    data = subprocess.check_output(['git', 'show', ARCHIVE + ':' + path])
    hashes[path] = hashlib.sha256(data).hexdigest()
    return data.decode()

print('Public author evidence archive', ARCHIVE)
print('Reviewed source', HEAD, 'merged base', BASE)
rows = [r.split('|')[1:-1] for r in receipt('workflows/verify-afa3ea19.md').splitlines()[2:] if r.startswith('|')]
counts = collections.Counter(r[4].strip() for r in rows)
assert counts == {'0': 118, 'NOT RUN': 130}, counts
print('Workflow inventory:', dict(counts), '; NOT RUN is not an executed pass')
executed_rcs = 0
for row in rows:
    if row[4].strip() != '0':
        continue
    log = row[5].strip().strip('`')
    if log.endswith('.log'):
        rc = receipt('workflows/logs/' + log[:-4] + '.rc').strip()
        assert rc == '0', (log, rc)
        executed_rcs += 1
print('Executed workflow rc files independently checked:', executed_rcs)
campaign = receipt('workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log')
assert 'mutants: 760 of 760 caught' in campaign
node = ast.parse(Path('sw/firmware/ctrl/test/plat_mutants.py').read_text())
fn = next(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == 'advertisement_mutants')
names = [n.args[0].value for n in ast.walk(fn) if isinstance(n, ast.Call)
         and isinstance(n.func, ast.Name) and n.func.id == 'm']
assert len(names) == 18
print('Control campaign: 760/760; all advertisement plants matched by name:')
for name in names:
    match = re.search(r'^\[ok\] mutant ' + re.escape(name) + r' .*$', campaign, re.M)
    assert match, name
    print(match.group())
for arm in ['aecp', 'srp']:
    tail = receipt('workflows/logs/rtl-fast__firmware-' + arm + '-mutants__ci_step_9.log.tail.txt')
    assert 'test_ctrl_firmware: PASS' in tail
    print(arm, 'campaign tail PASS; full large log represented by archive hash/tail')
coverage = receipt('workflows/logs/rtl-fast__firmware-unit__ci_step_12.log')
for line in coverage.splitlines():
    if 'ctrl_plat_phy.c' in line:
        print('Coverage:', line)
        assert '173/173' in line and '160/160' in line
suites = checks = 0
for i in range(4):
    result = json.loads(receipt(f'sweep/shard-{i}.results.json'))
    assert result['head'] == HEAD and all(x['exit_code'] == 0 for x in result['results'])
    log = receipt(f'sweep/shard-{i}.log')
    line = re.search(r'^suites:.*$', log, re.M).group()
    check = re.search(r'^checks:.*$', log, re.M).group()
    n, passed, failed, timed = map(int, re.findall(r'\d+', line))
    count, failures = map(int, re.findall(r'\d+', check))
    assert n == passed and failed == timed == failures == 0
    suites += n
    checks += count
    print('Sweep', i, line, check)
assert suites == 65 and checks == 2713040
print('Sweep total:', suites, 'suites;', checks, 'checks')
for shape, expected in [('1x1', '0'), ('8x8-1if', '1')]:
    assert receipt('budget/' + shape + '/regrade.rc').strip() == expected
    log = receipt('budget/' + shape + '/regrade.log')
    statements = [s for s in log.splitlines() if s.startswith('STATED ')]
    if shape == '8x8-1if':
        assert len(statements) == 11
    print('Budget', shape, 'rc', expected, 'stated-cost lines', len(statements))
    for line in log.splitlines():
        if 'groups graded' in line or line.startswith('STATED '):
            print(line)
for shape in ['1x1', '8x8']:
    log = receipt(f'boot/boot-{shape}-afa3ea19.txt')
    print('Boot', shape)
    for line in log.splitlines():
        if line.startswith('PHY ') or line.startswith('ctrl_split_boot:'):
            print(line)
print('Published linked-image ledger:')
ledger = receipt('boot/plat-ledger-self-test-afa3ea19.txt')
print('\n'.join(line for line in ledger.splitlines() if line.startswith(('POINT ', 'plat_ledger'))))
for name in ['budget/image-identity-base-70f4056f-head.txt', 'release-image/COMPARE.txt',
             'route/route-inputs-c805f699-afa3ea19.txt']:
    print(name)
    print(receipt(name))
for shape in ['1x1', '8x8']:
    for directive in ['ExtraPostPlacementOpt', 'ExtraTimingOpt', 'AltSpreadLogic_high']:
        print(receipt(f'route/{shape}-{directive}/signoff.txt'))
unchanged = git('diff', '--name-only', BASE, HEAD, '--', 'hdl', 'tb/verilator/ctrl_service_budget',
                'tb/verilator/fw_service_budget')
assert unchanged == '', unchanged
print('PASS merged-base RTL and budget harness paths unchanged')
names = git('diff', '--name-only', PRE, HEAD).splitlines()
assert names == ['sw/firmware/ctrl/plat/ctrl_plat_phy.h', 'tb/verilator/ctrl_split_boot/README.md',
                 'tb/verilator/ctrl_split_boot/run.py'], names
def without_comments(s):
    return re.sub(r'\s+', '', re.sub(r'//[^\n]*|/\*.*?\*/', '', s, flags=re.S))
path = names[0]
assert without_comments(git('show', PRE + ':' + path)) == without_comments(git('show', HEAD + ':' + path))
print('PASS c805f699..afa3ea19: firmware header changes comments only; remaining changes boot README/native controls')
conflicts = git('show', '--format=', '--remerge-diff', '--name-only', '8670bfb071e4935f2fd26bd25af9a9d4a3137ffd').splitlines()
assert len(conflicts) == 6, conflicts
print('Six merge resolutions:', ', '.join(conflicts))
print('Original-base changed paths:', len(git('diff', '--name-only', '659d7687', HEAD).splitlines()))
print('Merged-base changed paths:', len(git('diff', '--name-only', BASE, HEAD).splitlines()))
(packet / 'evidence-index.sha256').write_text(''.join(f'{digest}  {path}\n' for path, digest in sorted(hashes.items())))
print('PASS audit of', len(hashes), 'immutable public artifacts; source receipts are author execution, not manager execution')

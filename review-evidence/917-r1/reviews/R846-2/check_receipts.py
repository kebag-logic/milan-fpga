"""Inspect public receipt claims. Usage: python3 -B check_receipts.py EVIDENCE_ROOT.
Hashes are checked separately by audit.py. No campaign is executed here.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
p = root / 'author-r2/receipts'

def read(name):
    return (p / name).read_text()

mutants = read('mbx/mutants-full-8f73ade5.log')
assert mutants.count('[ok] positive control,') == 4
assert 'mbx mutants: 242 of 242 caught' in mutants
for name in ('rx-space-from-the-committed-head', 'rx-space-from-the-committed-head-axil',
             'rx-refused-behind-held-counted', 'rx-release-gated-on-open'):
    line = next(l for l in mutants.splitlines() if l.startswith('[ok] ' + name + ':'))
    print(line)
print('Mailbox: four positive controls, 242/242 named catches')
mbx = read('sweep-8f73ade5/logs/mbx.log')
assert 'mbx mutants: 13 of 13 caught' in mbx
rerun = read('sweep-8f73ade5/milan_dp_render-rerun.log')
assert rerun.count('RESULT: PASS') == 2 and 'RESULT: FAIL' not in rerun
assert '5 checks: 5 PASS, 0 FAIL' in rerun
print('Quick mutants: 13/13; render rerun: two PASS results and 5/5 leg checks')
for line in mbx.splitlines():
    if re.search(r'^== mbx.*checks:', line):
        print(line)
fw = read('workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log')
assert 'mutants: 699 of 699 caught' in fw
assert 'test_ctrl_firmware: PASS' in fw
print('Firmware control: 699/699 caught; published gate PASS')
budget_selftest = read('budget/selftest/selftest-final-excerpt.txt')
assert 'self-test: 0 failures' in budget_selftest
assert 'MUTANT caught lines: 214 at the head' in budget_selftest
assert 'MUTANT lines not caught: 0' in budget_selftest
print('Published budget self-test: zero failures, 214 caught, zero uncaught')
wf = read('workflows/verify-8f73ade5.md')
rows = [l.split('|')[1:-1] for l in wf.splitlines() if l.startswith('| ') and not l.startswith('| Workflow')]
executed = [r for r in rows if r[4].strip() == '0']
skipped = [r for r in rows if r[4].strip() == 'NOT RUN']
assert len(executed) == 139 and len(skipped) == 226
assert all(r[5].strip() for r in skipped)
readable = 0
for row in executed:
    name = row[5].strip().strip('`')
    rc = p / 'workflows/logs' / name.replace('.log', '.rc')
    assert rc.read_text().strip() == '0'
    log = p / 'workflows/logs' / name
    if log.is_file():
        assert '8f73ade54366cc832bad3386c8b6f3bbb12ca5e4' in log.read_text()[:300]
        readable += 1
print(f'Workflow receipt table: {len(executed)} zero exits, {len(skipped)} explicit skips; {readable} readable exact-head logs')
print(read('sweep-8f73ade5/shard-1-summary.txt'))
for label in ('held-1x1', 'held-8x8-1if'):
    result = json.loads(read(f'budget/{label}/results.json'))
    row = result['results'][0]['probes'][0]
    assert row['status'] == 'measured' and row['within_budget']
    assert row['budget_ms'] == 20 and row['ingress_allowance_ms'] == 6
    assert row['start_sys'] == 100001422 and row['ingress_sys'] == 498643
    print(label + ': ' + json.dumps({k: row[k] for k in ('start_sys', 'end_sys', 'ms', 'budget_ms', 'ingress_ms', 'ingress_allowance_ms')}))
    print(read(f'budget/{label}/attribution-evidence.txt'))
for label in ('held-8x8-1if', 'aecp-8x8-1if-control'):
    assert read(f'budget/{label}/run.rc').strip() == '1'
    costs = [line.partition(': ')[2] for line in read(f'budget/{label}/run.log').splitlines() if line.startswith('STATED ')]
    assert len(costs) == 3
    if label.startswith('held'):
        held_costs = costs
    else:
        assert costs == held_costs
print('8x8/1if held and ordinary controls both exit 1 for the same three stated-cost overruns; known #914 scope')
for side in ('base', 'head'):
    print(read(f'budget/regrade/r2-regrade-{side}-1x1.txt'))
baseline = read('images/split-images-round1-and-base.txt')
for label in ('1x1', '8x8-1if'):
    log = read(f'images/split-{label}-8f73ade5.log')
    image = re.search(r'ctrl_app.elf ([0-9a-f]{64}) (\d+)', log)
    assert image and image[1] in baseline and image[2] in baseline
    for sha, artifact in re.findall(r'^([0-9a-f]{64})  (\S+)$', log, re.M):
        if 'mem.init' not in artifact:
            assert sha in baseline, artifact
    print(f'{label} firmware {image[1]}, {image[2]} bytes; ROM banks and constraints match comparison receipt')
print(read('sv2v/rtl-comment-only.txt').split('git diff')[0])
print('Evidence limit: large CPU logs are published by digest/size and excerpts, not full bytes; regrade claims above are author receipts.')

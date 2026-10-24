#!/usr/bin/env python3
"""Summarize hash-verified public receipts and verify evidence carry."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
published = out / 'scratch/published/author-r2/receipts'
p = published / 'round2'
count = suites = 0
for k in range(4):
    text = (p / f'sweep/shard-{k}/spec-01.log').read_text()
    s, passed, failed, timed = map(int, re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', text).groups())
    checks, failures = map(int, re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', text).groups())
    meta = json.loads((p / f'sweep/shard-{k}/spec-complete.json').read_text())
    assert meta['head'] == '0d4b46204b905f4fced56b250f5f670a89fa3471'
    assert meta['exit_code'] == failed == timed == failures == 0 and s == passed
    count += checks
    suites += s
    print(f'shard {k}: {s}/{s} suites, {checks}/0 checks, rc=0')
assert (suites, count) == (64, 2189325)
print(f'PASS total: {suites}/64 suites, {count} checks, zero failures')
fast = json.loads((p / 'rtl-fast/receipts.json').read_text())
assert fast['head'] == fast['head_after'] == '01fc54756f1ffb0a3aa836681215e8321ee7e86c'
assert not fast['tracked_changes'] and not fast['failed']
for name, job in fast['jobs'].items():
    assert job['result'] == 'success' and job['rc'] == 0
    print(f'native replica job {name}: success; executed steps={sum("rc" in s for s in job["steps"])}')
print('Native run-body replica only; uses/setup substitutions are recorded in receipts.json.')
for revision, expected in [
    ('0d4b4620', {'ci/image/command-table.json', 'sw/firmware/ctrl/README.md'}),
    ('2a0085dd', {'sw/firmware/ctrl/README.md'}),
]:
    changed = set(subprocess.check_output(['git', '-C', str(repo), 'diff', '--name-only', revision+'..HEAD']).decode().splitlines())
    assert changed == expected
    print(f'PASS carry {revision}..HEAD: '+', '.join(sorted(changed)))
assert not subprocess.check_output(['git', '-C', str(repo), 'diff', 'a032c6d6..HEAD', '--', 'tests/features/crf_sr_class_a.feature', 'tests/steps/crf_class_a_steps.py'])
print('PASS BDD scenario and steps byte-identical to base')
table = json.loads((repo / 'ci/image/command-table.json').read_text())
script = 'tb/verilator/milan_dp/crflic_mutants.py'
assert hashlib.sha256((repo / script).read_bytes()).hexdigest() == table['scripts'][script]['sha256']
assert table['scripts'][script]['class'] == 'reviewed non-installing'
assert table['commands']['Vmilan_dp_tspec8']['patterns'] == table['commands']['Vmilan_dp_crflic']['patterns']
print('PASS command-table script digest, non-installing class and runtime pattern')
for label in ['head', 'base']:
    entries = [json.loads(x) for x in (out / f'learn-{label}.jsonl').read_text().splitlines()]
    assert not any(x.get('script') == script or x.get('command') == 'Vmilan_dp_tspec8' for x in entries)
    print(f'PASS {label} suite walk: no learned entry for changed script or new executable')
selected = [
    'round2/rtl-fast/full.out', 'round2/rtl-fast/full.rc', 'round2/rtl-fast/receipts.json',
    'round2/rtl-fast/logs/firmware-verilator.14.log',
    'round2/legs/crflic-run.log', 'round2/legs/tspec8-run.log',
    'round2/crflic_mutants/crflic-mutants-verdicts.txt',
    'round2/bdd/frame_mutants.log', 'round2/docs_gates/all.out',
    'round2/docs_gates/nogit_summary.txt', 'round2/vivado/route-1x1-check.log',
]
for k in range(4):
    selected.extend([f'round2/sweep/shard-{k}/spec-01.log', f'round2/sweep/shard-{k}/spec-complete.json'])
for name in selected:
    dest = out / 'published-receipts' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((published / name).read_bytes())
print('PASS selected raw public receipts copied without byte changes')

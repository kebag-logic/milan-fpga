#!/usr/bin/env python3
"""Audit the focused evidence and write the publication manifest."""
import hashlib
import json
from pathlib import Path
import re

packet = Path(__file__).resolve().parents[1]
receipts = packet / 'receipts'
inventory = json.loads((receipts / 'inventory.json').read_text())
assert inventory['cases'] == inventory['unique_cases'] == 94
audit = {'case_inventory': 94, 'profiles': {}, 'documentation': {}}
for profile, passes in [('OFF', 19901), ('ON', 19889)]:
    runner = (receipts / f'{profile}-unit.log').read_text()
    assert 'Running "main" (87 tests)...' in runner
    assert f'Completed "main": {passes} passes' in runner
    folder = receipts / f'reversals-{profile}'
    commands = json.loads((folder / 'commands.json').read_text())
    codes = {row['label']: row['rc'] for row in commands}
    for label in ['configure', 'baseline-build', 'baseline-check', 'restored-build', 'restored-check']:
        assert codes[label] == 0, (profile, label)
    outcomes = {}
    for label, required in inventory['required_failures'].items():
        assert codes[label + '-build'] == 0 and codes[label] == 8
        log = (folder / (label + '.log')).read_text()
        failed = re.findall(r'Failure: [^\n]* -> ([A-Za-z_0-9]+)', log)
        assert all(name in failed for name in required), (profile, label, failed)
        outcomes[label] = {'build_rc': 0, 'check_rc': 8, 'actual_failing_tests': sorted(set(failed))}
    audit['profiles'][profile] = {'tests': 87, 'assertions': passes, 'focused_mutants': outcomes,
                                  'baseline_and_restored_checks': 'PASS'}
for label in ['sentences', 'references', 'references-self-test', 'links', 'graphs', 'whitespace']:
    assert (receipts / (label + '.rc')).read_text().strip() == '0'
    audit['documentation'][label] = 0
checkout = json.loads((receipts / 'checkout-final.json').read_text())
assert checkout['clean_worktree_and_index'] and not checkout['gitlinks']
assert checkout['tracked_blob_count'] == 60
audit['tracked_blobs_and_modes_verified'] = 60
audit['gitlinks'] = []
(receipts / 'receipt-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
report = (packet / 'REPORT.md').read_text()
assert report.startswith('[R545] POSITIVE - exact head f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152\n')
assert 'SKELETON' not in report
assert report.rstrip().endswith('R545-2 FINISHED')
files = [packet / 'REPORT.md', packet / 'REPRODUCE.md']
files += sorted((packet / 'scripts').glob('*.py'))
files += sorted(path for path in receipts.rglob('*') if path.is_file())
lines = [hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + path.relative_to(packet).as_posix()
         for path in sorted(files)]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
print(f'PASS: {len(files)} publishable files; all expected measurements and named failures verified.')

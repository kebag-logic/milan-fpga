#!/usr/bin/env python3
"""Read the actual driver inventory and compare documentation measurements."""
import argparse
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd())
args = parser.parse_args()
root = args.repo.resolve()
packet = Path(__file__).resolve().parents[1]
driver = runpy.run_path(str(root / 'tests/check_reversals.py'))
cases = driver['CASES']
names = [case[0] for case in cases]
assert len(cases) == len(set(names)) == 94
expected = {
    'point-to-point-condition': ['applicant_receive_conditions_follow_link_mode',
                                'pending_applicant_joinin_obeys_note_four'],
    'pending-point-to-point-condition': ['pending_applicant_joinin_obeys_note_four'],
    'shared-in-condition': ['applicant_receive_conditions_follow_link_mode'],
}
for name, required in expected.items():
    assert driver['REQUIRED_FAILURES'][name] == required
assert 'Both profiles run all 94 reversals.' in (root / 'doc/tester.md').read_text()
for profile, count in [('OFF', 19901), ('ON', 19889)]:
    text = (packet / 'receipts' / f'{profile}-unit.log').read_text()
    assert 'Running "main" (87 tests)...' in text
    assert f'Completed "main": {count} passes' in text
    assert 'Failure:' not in text and 'Exception:' not in text
    assert (packet / 'receipts' / f'{profile}-unit.rc').read_text().strip() == '0'
    manager = (root / 'doc/manager.md').read_text()
    assert f'87 tests with {count} assertions.' in manager
print(json.dumps({'cases': len(cases), 'unique_cases': len(set(names)), 'case_names': names,
                  'required_failures': expected, 'profile_assertions': {'OFF': 19901, 'ON': 19889}}, indent=2))

#!/usr/bin/env python3
"""Focused boundary and guard-removal probes against the reviewed grader."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import grade
import held
import scenario
import selftest as st
from selftest_held import held_checks

for name, ok, detail in held_checks(st):
    assert ok, (name, detail)
    print('PASS', name)
for guard, needle in (('overtaken', 'a commit on the channel holding a record is refused'),
                      ('follows_hold', "a held record's commit stamped before its hold is refused")):
    with patch.object(held, guard, lambda *args: None):
        failed = [name for name, ok, _ in held_checks(st) if not ok]
        assert any(needle in name for name in failed), failed
        print('REMOVED', guard, 'CAUGHT BY', failed)
ch = scenario.CH['aecp']
prefix = ['RXS 1000 0 60 held', 'RXE 1059', f'RXH 1070 {ch}']
for cycle, good in ((1060, False), (1070, False), (1071, True), (601059, True), (601060, False)):
    try:
        log = grade.parse(st.synthetic(prefix + [f'RXR {cycle} {ch}']), st.SYS_HZ, st.CPU_HZ)
    except grade.Refusal as exc:
        assert not good, str(exc)
        print('BOUNDARY', cycle, 'REFUSED', exc)
    else:
        assert good
        print('BOUNDARY', cycle, 'ACCEPTED', log.held)
print('Focused ordering probes: PASS')

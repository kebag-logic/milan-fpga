#!/usr/bin/env python3
"""Reproduce join interval grading at and beyond the build search horizon."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade
import join_grade
import scenario
from selftest import synthetic, tx_record

def check(end_ms, timer_ms):
    lines = []
    word = 0
    for n, at in enumerate((1000, end_ms)):
        c = at * 100000
        frame = bytes(12) + bytes.fromhex('22ea') + bytes(46)
        lines += tx_record(scenario.CH['srp'], 0, frame, word, c)
        word += 17
        lines += [f'ENTRY {c - 2000} build_mrpdu',
                  f'PASS {n} {c - 3000} {c - 3000} 5000 instr=10']
    lines += [f'ENTRY {timer_ms * 100000} on_join_timer']
    log = grade.parse(synthetic(lines), 100000000, 100000000)
    return join_grade.held(log)

results = {str(end): check(end, 1190) for end in (1191, 1241, 1289, 1291, 1500)}
print(json.dumps(results, indent=2))
assert results['1191']['count'] == 1 and not results['1191']['over']
assert results['1241']['count'] == 1 and results['1241']['over']
assert results['1289']['count'] == 1 and results['1289']['over']
assert results['1291']['count'] == 0 and not results['1291']['over']
assert results['1500']['count'] == 0 and not results['1500']['over']
print('REPRODUCED: 291 ms and 500 ms intervals disappear beyond the 100 ms build horizon.')

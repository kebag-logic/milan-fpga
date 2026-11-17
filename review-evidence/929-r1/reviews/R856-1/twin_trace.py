#!/usr/bin/env python3
"""Inspect local wire captures and replay the base comparator on those bytes.
Usage: twin_trace.py CHECKOUT PACKET
"""
import importlib.util
from pathlib import Path
import subprocess
import sys

root, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suite = root / 'tb/verilator/milan_dp'
sys.path.insert(0, str(suite))
import twin_decode as td
import twin_mrp as mrp
import twin_compare as compare

caps = [td.load(suite / 'obj_twin' / (half + '.json')) for half in ('fabric', 'split')]
for cap in caps:
    keys = {}
    for frame in cap.frames.get('MSRP', []):
        events, la = td.msrp_events(frame)
        for event in events:
            if event.kind in (1, 2):
                keys.setdefault((event.kind, event.value), []).append((frame.ms, event.event))
    print(cap.placement, 'Talker FirstValues:', sorted(keys))
    assert keys and all(kind == 1 for kind, value in keys)
    for key in keys:
        print(mrp.trace_shown(cap, 'MSRP', key))
    print('LeaveAll declarations:', compare.runs(mrp.declarations(mrp.grade(cap), set())))
result = compare.compare(*caps)
assert not result['findings']
print('Head comparator: zero findings on local captures')
old = packet / 'scratch' / 'base_twin_compare.py'
old.write_bytes(subprocess.check_output(['git', '-C', str(root), 'show',
                                        '70f4056f:tb/verilator/milan_dp/twin_compare.py']))
spec = importlib.util.spec_from_file_location('base_twin_compare', old)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
result = module.compare(*caps)
assert len(result['findings']) == 1 and 'split-talker-failed' in result['findings'][0]
print('Base comparator on identical local captures:')
print(result['findings'][0])

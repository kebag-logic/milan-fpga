"""Capture grade differences for one disposable, hash-rebound published case.

Usage: python3 -B diagnose_grade.py SOURCE REBOUND_EXTRACT CASE OUTPUT_JSON
"""
import json
import sys
from pathlib import Path

source, packet = map(Path, sys.argv[1:3])
case, output = sys.argv[3:5]
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
import receipt_regrade as replay

path = packet / 'census' / case / 'manifest.json'
manifest = json.loads(path.read_text())
limit = json.loads((packet / 'census.json').read_text())['part_limit'] + 1
expected = json.loads(replay.read_parts(path.parent, manifest['grade'], limit))
original = replay.grade.grade

def differences(a, b, path='$'):
    if isinstance(a, dict) and isinstance(b, dict):
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                yield dict(path=path + '.' + key, expected=a.get(key), actual=b.get(key))
            else:
                yield from differences(a[key], b[key], path + '.' + key)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for index, (left, right) in enumerate(zip(a, b)):
            yield from differences(left, right, path + f'[{index}]')
    elif a != b:
        yield dict(path=path, expected=a, actual=b)

def capture(*args, **kwargs):
    got = original(*args, **kwargs)
    normalized = json.loads(json.dumps(got))
    changed = list(differences(expected, normalized))
    Path(output).write_text(json.dumps(dict(case=case, differences=changed), indent=2) + '\n')
    print('Different grade fields:', len(changed), flush=True)
    return got

replay.grade.grade = capture
try:
    replay.regrade(path, limit=limit)
except ValueError as error:
    print(str(error))
    raise SystemExit(1)

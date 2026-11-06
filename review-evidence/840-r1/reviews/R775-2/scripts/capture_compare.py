#!/usr/bin/env python3
"""Check the F2 prose against measurements.json: maxima, ratios, repeats.

Usage: capture_compare.py <repo> <git-rev-of-previous-receipt>
"""
import json
import subprocess
import sys

repo, prev = sys.argv[1:3]
now = json.load(open(repo + '/tb/verilator/nvm_capture_cpu/measurements.json'))
old = json.loads(subprocess.check_output(['git', '-C', repo, 'show', prev + ':tb/verilator/nvm_capture_cpu/measurements.json']))
print('base now', now['base'], 'previous', old['base'])
print('maxima now', now['maxima'])
print('maxima previous', old['maxima'])
ms = now['measurements']
print(type(ms), (list(ms.keys())[:8] if isinstance(ms, dict) else (len(ms), list(ms[0].keys()))))
def rows(doc):
    out = {}
    items = doc['measurements'] if isinstance(doc['measurements'], list) else [dict(v, key=k) for k, v in doc['measurements'].items()]
    for arm in items:
        key = (arm.get('shape'), arm.get('cpu_hz'), arm.get('traffic'))
        out[key] = arm
    return out
a, b = rows(now), rows(old)
total = same = 0
for key in sorted(a, key=str):
    arm = a[key]
    fields = [k for k, v in arm.items() if isinstance(v, list)]
    series = arm.get('sys_cycles') or arm.get('elapsed_sys_cycles') or arm.get('rows') or arm.get('captures')
    prior = b[key].get('sys_cycles') or b[key].get('elapsed_sys_cycles') or b[key].get('rows') or b[key].get('captures')
    if series and isinstance(series[0], dict):
        name = [k for k in series[0] if 'cycle' in k][0]
        series = [r[name] for r in series]
        prior = [r[name] for r in prior]
    eq = sum(x == y for x, y in zip(series, prior))
    total += len(series)
    same += eq
    print(key, 'captures', len(series), 'repeat', eq, 'min', min(series), 'max', max(series), 'fields', fields[:4])
print('repeat total', same, 'of', total)

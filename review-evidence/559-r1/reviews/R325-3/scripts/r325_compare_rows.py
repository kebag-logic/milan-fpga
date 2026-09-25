#!/usr/bin/env python3
"""[R325] R325-3: compare re-measured capture rows with the published receipt.

Usage: r325_compare_rows.py <clone at b02af048> <scratch dir>
Reads each scratch build's capture.log (the same CAPTURE-line parse as the
harness grader) and compares every field of every row with the same index in
measurements.json, then recomputes each shape's maximum over BOTH traffic arms
and compares it with the published maxima.
"""
import json
from pathlib import Path
import re
import sys

clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
receipt = json.loads((clone / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
arms = {(a['shape'], a['cpu_hz'], a['traffic']): a for a in receipt['measurements']}
bad = 0
mine = {}
for build in sorted(scratch.glob('b*_*_*_16')):
    spec = json.loads((build / 'sources.json').read_text())
    log = (build / 'capture.log').read_text()
    rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', line))
            for line in log.splitlines() if line.startswith('CAPTURE index=')]
    ref = arms[(spec['shape'], spec['cpu_hz'], spec['traffic'])]['rows']
    same = [r == ref[r['index']] for r in rows]
    bad += same.count(False) + (16 - len(rows))
    mine[(spec['shape'], spec['cpu_hz'], spec['traffic'])] = rows
    ms = [r['sys_cycles'] / spec['sys_hz'] * 1000 for r in rows]
    print(f"{build.name}: shape={spec['shape']} cpu_hz={spec['cpu_hz']} traffic={spec['traffic']} "
          f"phase={spec['phase']!r} finished={len(rows)}/16 identical_to_receipt={same.count(True)}/{len(rows)} "
          f"min_ms={min(ms):.5f} max_ms={max(ms):.5f} "
          f"receipt_arm_max_ms={max(r['sys_cycles'] for r in ref) / spec['sys_hz'] * 1000:.5f}")
    for r in rows:
        print('  ', 'SAME' if r == ref[r['index']] else 'DIFF', r)
for m in receipt['maxima']:
    key_on, key_off = (m['shape'], m['cpu_hz'], 'on'), (m['shape'], m['cpu_hz'], 'off')
    if key_on in mine and key_off in mine:
        worst = max(r['sys_cycles'] for k in (key_on, key_off) for r in mine[k]) / 1e8 * 1000
        ok = abs(worst - m['maximum_ms']) < 1e-9
        bad += not ok
        print(f"MAX over both arms {m['shape']} {m['cpu_hz']}: remeasured={worst:.5f} ms published={m['maximum_ms']} "
              f"{'SAME' if ok else 'DIFF'}; 49 ms floor margin={49 / worst:.4f}x; below 24.5 ms by {24.5 - worst:.5f} ms")
    else:
        print(f"MAX {m['shape']} {m['cpu_hz']}: not remeasured in this round")
print('ALL ROWS AND MAXIMA IDENTICAL' if not bad else f'{bad} DIFFERENCES OR MISSING ROWS')
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Compare reproduced capture arms with the tracked receipt, row by row.

Usage: compare_capture_rows.py <repo> <receipts-dir> <label>...
where each label is e.g. 8x8-50-on and <receipts-dir>/measurement-<label>.json
is the harness's own graded output. Exit 0 only when every reproduced arm
exists, passed its harness grading (rc file 0), and all rows equal the receipt.
"""
import json
import sys
from pathlib import Path

repo, rdir, labels = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
receipt = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
shapes = {'8x8': 'endstation_ax7101_8x8', '1x1_tdm8': 'endstation_ax7101_1x1_tdm8'}
bad = 0
worst = 0.0
for label in labels:
    shape, mhz, arm = label.rsplit('-', 2)
    rc = int((rdir / f'capture-{label}.rc').read_text())
    mine = json.loads((rdir / f'measurement-{label}.json').read_text())
    ref = next(a for a in receipt['measurements']
               if a['shape'] == shapes[shape] and a['cpu_hz'] == int(mhz) * 1_000_000
               and a['traffic'] == arm)
    equal = mine['rows'] == ref['rows']
    same = all(mine[k] == ref[k] for k in ('minimum_ms', 'maximum_ms', 'margin', 'captures',
                                           'sys_hz', 'cpu_hz', 'configured_cpu_hz', 'phase'))
    worst = max(worst, mine['maximum_ms'])
    print(f'{label}: harness rc={rc} rows={len(mine["rows"])} rows_equal={equal} '
          f'summary_equal={same} min={mine["minimum_ms"]} max={mine["maximum_ms"]} '
          f'receipt_max={ref["maximum_ms"]}')
    bad |= rc != 0 or not equal or not same
print(f'reproduced worst over arms: {worst} ms; limit 24.5 ms; slack {24.5 - worst:.5f} ms; '
      f'margin vs 49 ms floor {49 / worst:.4f}x')
print('RESULT', 'FAIL' if bad else 'PASS')
sys.exit(1 if bad else 0)

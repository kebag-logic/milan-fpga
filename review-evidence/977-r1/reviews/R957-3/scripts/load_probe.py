#!/usr/bin/env python3
"""Usage: python3 -I -B load_probe.py <repo-root>. Prints each point's load with and without the deliveries term,
at the dearest-before cost, and the flip check's verdict at 8x8/1if under ceilings 0.77 and 0.78 (in-process patches only)."""
import sys
from pathlib import Path
from unittest import mock
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as lg
import flip_grade as fg
for point in ('1x1/1if', '8x8/1if'):
    terms = lg.load(root, point, fg.COLUMN)
    tot = sum(terms.values())
    d = terms.get('deliveries', 0.0)
    dearest = tot - d + d * lg.DELIVERY_US_DEAREST[point] / lg.DELIVERY_US[point]
    print(f'{point}: load {tot:.5f}; without deliveries {tot - d:.5f}; deliveries {d:.5f} '
          f'(registrations {terms.get("registrations", 0):.5f}); at dearest-before cost {dearest:.5f}; '
          f'V {lg.record_values(point, root)}; JOIN_MIN_MS {lg.JOIN_MIN_MS}')
print('FLIP', fg.FLIP)
for ceil in (0.77, 0.78):
    with mock.patch.dict(fg.FLIP, {'8x8/1if': ceil}):
        out = fg.findings(root, fg.COLUMN, {"8x8/1if": ceil})
        bad = [f for f in (out or []) if '8x8/1if' in f]
        print(f'ceiling {ceil}: flip findings at 8x8/1if: {len(bad)}', *bad[:3], sep='\n  ')

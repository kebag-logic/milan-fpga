#!/usr/bin/env python3
"""figures_probe.py TREE: print, at 1x1/1if and 8x8/2if, every load_grade cost whose pin column (STATED_US) and donor
column (STATED_US_DONOR) differ, poll_grade's items beside them, the 1x1/1if retained chain, and whether the donor
column is at or above the pin's for each cost outside load_grade.WALK (its documented rule)."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade  # noqa: E402
bad = 0
for point, n in (('1x1/1if', 1), ('8x8/2if', 2)):
    pin, don = load_grade.STATED_US[point], load_grade.STATED_US_DONOR[point]
    polls = {('base' if k == 'base' else f'item.{k}'): v for k, v in poll_grade.STATED_US[n].items()}
    for k in sorted(set(pin) | set(don) | set(polls)):
        vals = {'pin': pin.get(k), 'donor': don.get(k), 'polls': polls.get(k)}
        if len({v for v in vals.values() if v is not None}) > 1:
            rule = ''
            if k not in load_grade.WALK and pin.get(k) is not None and don.get(k) is not None and don[k] < pin[k]:
                rule = '  DONOR BELOW PIN OUTSIDE WALK'; bad += 1
            print(f'{point} {k}: ' + ' '.join(f'{a}={b}' for a, b in vals.items() if b is not None) + rule)
r = (poll_grade.STATED_US[1]['retained'], load_grade.STATED_US['1x1/1if']['item.retained'],
     load_grade.STATED_US_DONOR['1x1/1if']['item.retained'], load_grade.STATED_US['1x1/1if']['record.srp'],
     load_grade.STATED_US_DONOR['1x1/1if']['record.srp'])
print('1x1/1if retained chain (polls, pin item, donor item, pin record.srp, donor record.srp):', r)
print('RESULT', 'FAIL' if bad else 'PASS')
sys.exit(1 if bad else 0)

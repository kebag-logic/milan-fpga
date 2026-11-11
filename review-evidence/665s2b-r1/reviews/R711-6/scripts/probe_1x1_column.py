"""Probe: which column does load_grade.py --check hold 1x1/1if to?  Raise a 1x1/1if cost in the pin column
(STATED_US) only, until the load at the pin is far over 0.70, and ask the merge gate's findings().
usage: python3 -I probe_1x1_column.py <repo-root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as g  # noqa: E402
for key in ('record.acmp', 'event.ACMP'):          # both WALK costs: the donor column may state them lower
    saved = g.STATED_US['1x1/1if'][key]
    g.STATED_US['1x1/1if'][key] = 100_000
    try:
        pin = sum(g.load(root, '1x1/1if', g.STATED_US).values())
        graded = sum(g.load(root, '1x1/1if').values())
        f = g.findings(root)
        print(f'{key} at the pin raised to 100000 us: load at the pin {pin:.3f}, graded {graded:.3f}; '
              f'merge gate findings: {f or "none (RESULT: PASS)"}')
    finally:
        g.STATED_US['1x1/1if'][key] = saved

#!/usr/bin/env python3
"""sensitivity.py EXPORT: the 1x1/1if rows and the slice rule at the polls' base and a pass's events' fixed part each
at its stated figure before and after round 6's restatement, on EXPORT, a scratch export of the tree (git archive of
the head with its tsn-c-stack and lwSRP exports), whose two tables this edits; each configuration is graded in a fresh
interpreter. Prints, for each (base, events_none): the slice rule's choice and margin, rows_tiers.ruled, the pace rule,
and the built design's last queued notice; then, at the restated pair, that row at each pace from 7 to 13 ms and every
row at the 900 and 950 us slices with their least margins (the six rows the slice rule reads, and every row)."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

export = Path(sys.argv[1]).resolve()
H = export / 'tb/verilator/ctrl_service_budget'


def set_tables(base: int, none: int) -> None:
    p = H / 'poll_grade.py'
    p.write_text(re.sub(r'STATED_US = \{1: dict\(base=\d+,', f'STATED_US = {{1: dict(base={base},', p.read_text()))
    q = H / 'load_grade.py'
    t = q.read_text()
    t = re.sub(r"'item.aecp.response': 60, 'item.aecp.probe': 60, 'base': \d+,",
               f"'item.aecp.response': 60, 'item.aecp.probe': 60, 'base': {base},", t)
    for name in ('STATED_US = {', 'STATED_US_DONOR = {'):
        i = t.index(name)
        j = t.index("'8x8/2if'", i)
        t = t[:i] + re.sub(r"'events_none': \d+", f"'events_none': {none}", t[i:j], count=1) + t[j:]
    q.write_text(t)


PROBE = r'''
import sys
from pathlib import Path
sys.path.insert(0, '.')
import load_grade, paced_rows, rows_tiers as rt
r = Path(sys.argv[1]); full = sys.argv[2] == 'full'
c = load_grade.STATED_US_DONOR['1x1/1if']
i = rt.point_inputs(r, '1x1/1if')
print(f"base {c['base']}, events_none {c['events_none']} / {load_grade.STATED_US['1x1/1if']['events_none']}: slice rule "
      f"{rt.slice_choice(r)}, ruled {rt.ruled(r)}, pace {paced_rows.choice(r)}, the built design's last "
      f"{rt.rows(r, '1x1/1if', rt.BUILT, i)['last'][0]} ms")
if full:
    print('  the last at 900 us by pace:', {p: rt.solve('last', i._replace(pace_ms=p), rt.BUILT)[0] for p in range(7, 14)})
    b = rt.bounds_at(i)
    six = {row: b[row] for row in (*rt.TIER_ROWS, *rt.SLICE_HELD)}
    for us in (900, 950):
        rows = rt.rows(r, '1x1/1if', rt.BUILT._replace(slice_us=us), i)
        print(f'  {us} us:', {k: v[0] for k, v in rows.items()}, 'least margin, the rule\'s six',
              round(rt.least_margin(rows, six), 4), 'every row', round(rt.least_margin(rows, b), 4))
'''
for base, none, full in ((205, 30, False), (215, 30, False), (205, 35, False), (210, 35, False), (215, 35, True)):
    set_tables(base, none)
    # the edits keep each file's size, so a cached module of the same second would be read stale: none is kept
    shutil.rmtree(H / '__pycache__', ignore_errors=True)
    out = subprocess.run([sys.executable, '-I', '-B', '-c', PROBE, str(export), 'full' if full else ''], cwd=H,
                         capture_output=True, text=True)
    sys.stdout.write(out.stdout + out.stderr)

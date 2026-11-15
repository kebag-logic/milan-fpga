#!/usr/bin/env python3
"""per_pass_threshold.py COPY: the per-pass cost (a pass's events' fixed part plus its polls' base, the pass's own
cost at 1x1/1if) at which the built design's last queued notice passes 140 ms, the queued rule's ceiling, and every
row's margin at the copy's own tables. COPY is a scratch copy of the tree (sw, tb, configs, tsn-c-stack, lwSRP); this
edits the polls' base in its two tables (poll_grade.STATED_US, load_grade.STATED_US_DONOR at 1x1/1if) a microsecond
at a time and grades each in a fresh interpreter with no bytecode cache, the built design's slice and the 140 ms
bound held. Prints the stated figures, every row with its bound and margin in ms and relative, then a binary search
over the base: the largest per-pass cost at which the last queued notice holds 140 ms and the smallest at which it
passes, each with its row."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

copy = Path(sys.argv[1]).resolve()
H = copy / 'tb/verilator/ctrl_service_budget'
PROBE = r'''
import sys, json
from pathlib import Path
sys.path.insert(0, '.')
import load_grade, rows_tiers as rt
r = Path(sys.argv[1]); i = rt.point_inputs(r, '1x1/1if'); b = rt.bounds_at(i); rows = rt.rows(r, '1x1/1if', rt.BUILT, i)
c = load_grade.STATED_US_DONOR['1x1/1if']
print(json.dumps({'base': c['base'], 'events_none': c['events_none'], 'slice': rt.built_constants(r, 1)[0],
                  'rows': {k: [v[0], b[k]] for k, v in rows.items()}}))
'''


def base_now() -> int:
    return int(re.search(r'STATED_US = \{1: dict\(base=(\d+),', (H / 'poll_grade.py').read_text())[1])


def set_base(v: int) -> None:
    p = H / 'poll_grade.py'
    p.write_text(re.sub(r'STATED_US = \{1: dict\(base=\d+,', f'STATED_US = {{1: dict(base={v},', p.read_text()))
    q = H / 'load_grade.py'
    q.write_text(re.sub(r"'item.aecp.response': 60, 'item.aecp.probe': 60, 'base': \d+,",
                        f"'item.aecp.response': 60, 'item.aecp.probe': 60, 'base': {v},", q.read_text()))


def grade(v: int) -> dict:
    import json
    set_base(v)
    shutil.rmtree(H / '__pycache__', ignore_errors=True)
    out = subprocess.run([sys.executable, '-I', '-B', '-c', PROBE, str(copy)], cwd=H, capture_output=True, text=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


stated = base_now()
g = grade(stated)
own = g['base'] + g['events_none']
print(f"stated: base {g['base']} us, events' fixed part {g['events_none']} us, a pass's own cost {own} us, "
      f"slice {g['slice']} us")
print('| Row | W, ms | Bound, ms | Margin, ms | Relative |')
print('|---|---:|---:|---:|---:|')
for k, (w, bound) in g['rows'].items():
    print(f'| {k} | {w:.2f} | {bound:g} | {bound - w:.2f} | {1 - w / bound:+.4f} |')
lo, hi = stated, stated
while grade(hi)['rows']['last'][0] <= 140:
    lo, hi = hi, hi + 16
while hi - lo > 1:
    mid = (lo + hi) // 2
    if grade(mid)['rows']['last'][0] <= 140:
        lo = mid
    else:
        hi = mid
a, b = grade(lo), grade(hi)
print(f"the last queued notice holds 140 ms up to a pass's own cost of {lo + g['events_none']} us (base {lo}: "
      f"{a['rows']['last'][0]:.2f} ms) and passes it at {hi + g['events_none']} us (base {hi}: {b['rows']['last'][0]:.2f} ms)")
lo, hi = stated, hi
over = lambda r: sorted(k for k, (w, bound) in r['rows'].items() if w > bound)
while hi - lo > 1:
    mid = (lo + hi) // 2
    if over(grade(mid)):
        hi = mid
    else:
        lo = mid
a, b = grade(lo), grade(hi)
print(f"every row holds its bound up to a pass's own cost of {lo + g['events_none']} us (base {lo}) and at "
      f"{hi + g['events_none']} us (base {hi}) {', '.join(over(b))} passes: "
      + ', '.join(f"{k} {b['rows'][k][0]:.2f} of {b['rows'][k][1]:g}" for k in over(b)))
set_base(stated)

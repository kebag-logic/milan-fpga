#!/usr/bin/env python3
"""base_spans.py HARNESS LOG [TOP]: in LOG, the TOP passes (default 3) with the heaviest polls' base by HARNESS's
poll_grade, each broken into the traced spans that lie inside its polls section (FIRST..LAST), outermost only: each
span's label and CPU cycles, and the items subtracted. Read-only."""
import sys
from pathlib import Path

harness, logp = Path(sys.argv[1]), Path(sys.argv[2])
top = int(sys.argv[3]) if len(sys.argv) > 3 else 3
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import poll_grade  # noqa: E402

log = grade.parse(logp.read_text(errors='replace'), 100_000_000, 100_000_000)
traced, commits = poll_grade.spans(log), poll_grade.committed(log)
rows = []
for start, end, start_sys in poll_grade.sections(traced):
    items = poll_grade.instances(log, traced, commits, start, end)
    rows.append((end - start - sum(c for _, c in items), start, end, start_sys, items))
rows.sort(reverse=True)
for base, start, end, start_sys, items in rows[:top]:
    inside = sorted((s, c, lab) for lab, spans in traced.items() for s, c, _ in spans if start <= s and s + c <= end)
    outer, reach = [], -1
    for s, c, lab in inside:
        if s >= reach:
            outer.append((lab, c))
            reach = s + c
    print(f"base {base} span {end - start} sys {start_sys} items {items}")
    print('   ' + ', '.join(f'{lab}:{c}' for lab, c in outer))

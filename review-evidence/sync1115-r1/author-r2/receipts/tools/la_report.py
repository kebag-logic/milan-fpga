#!/usr/bin/env python3
"""Report every LeaveAll run-out of a budget group's log and the group's MRPDU rows.

usage: la_report.py HARNESS_DIR RESULTS_DIR GROUP [GROUP...]
Prints, per group: each MRP timer run-out of kind leaveall (its time in ms, its outcome under mrpdu_grade.resolve,
how far its first frame, or first build where it sends none, lies after it, and the same from the centisecond TICK
that ran it out), then the group's mrpdu.* rows from its result JSON.
"""
import json
import sys
from bisect import bisect_right
from pathlib import Path

harness, results = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import mrpdu_grade  # noqa: E402

build = json.loads((results.parent / 'build.json').read_text()) if (results.parent / 'build.json').exists() else {}
sys_hz = int(build.get('sys_hz', 100_000_000))
cpu_hz = int(build.get('cpu_hz', sys_hz))
for group in sys.argv[3:]:
    text = (results / f'{group}.log').read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], sys_hz, cpu_hz)
    builds, _, sent, last = mrpdu_grade.index(log)
    posted = mrpdu_grade.ticks(log)
    print(f'GROUP {group} sys_hz {sys_hz} late_ms {mrpdu_grade.LATE_MS}')
    for entry, kind, outcome in mrpdu_grade.outcomes(log):
        if kind != 'leaveall':
            continue
        frames = mrpdu_grade.resolve(log, entry)[1]
        after = frames[0][0] if frames else next((b for b in builds if b > entry), last)
        k = bisect_right(posted, entry)
        deadline = posted[k - 1] if k else entry
        print(f'  leaveall run-out {entry * 1000 / sys_hz:10.3f} ms  {outcome:10s} first {(after - entry) * 1000 / sys_hz:8.3f}'
              f' ms after it, {(after - deadline) * 1000 / sys_hz:8.3f} ms after its TICK, frames {len(frames)}')
    counts = {}
    for _, kind, outcome in mrpdu_grade.outcomes(log):
        counts[outcome] = counts.get(outcome, 0) + 1
    print(f'  every MRP timer run-out: {counts}')
    data = json.loads((results / f'{group}.json').read_text())
    for p in data['probes']:
        if '.mrpdu.' in p.get('probe', ''):
            print(f"  ROW {p['probe']} {p['ms']:.3f} ms (deadline {p['start_sys'] * 1000 / sys_hz:.3f} ms)")

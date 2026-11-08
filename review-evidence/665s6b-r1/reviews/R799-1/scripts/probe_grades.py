#!/usr/bin/env python3
"""Print each half's raw grade findings (before the owed grade rows) and the MRP traces.

usage: probe_grades.py LEG_DIR FABRIC.json SPLIT.json
"""
import sys
from pathlib import Path

leg = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(leg))
import twin_decode as td  # noqa: E402
import twin_grades  # noqa: E402
import twin_mrp  # noqa: E402

for path in sys.argv[2:4]:
    cap = td.load(Path(path))
    found, _ = twin_grades.grade(cap)
    print(f"== {cap.placement}: {len(found)} raw grade finding(s)")
    for f in found:
        print("  ", f)
    for app in twin_mrp.APPLICATIONS:
        for key in twin_mrp.observations(cap, app):
            print("  trace", twin_mrp.trace_shown(cap, app, key))
        g = twin_mrp.grade(cap, app)
        print(f"  {app} LeaveAll declarations:", twin_mrp.declarations(g, set()))

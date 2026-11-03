#!/usr/bin/env python3
"""Print elaborate worker job and step durations from saved GitHub jobs JSON files."""
import json, sys
from datetime import datetime
def t(s): return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
for path in sys.argv[1:]:
    data = json.load(open(path))
    for job in data.get("jobs", []):
        if not job["name"].startswith("elaborate"): continue
        s, e = t(job["started_at"]), t(job["completed_at"])
        dur = (e - s).total_seconds() if s and e else None
        print(f"{path} | {job['name']} | {job['conclusion']} | job {dur}s")
        gate = 0
        for st in job["steps"]:
            a, b = t(st["started_at"]), t(st["completed_at"])
            d = (b - a).total_seconds() if a and b else None
            if d and d >= 20: print(f"    {d:7.0f}s {st['conclusion']} {st['name']}")

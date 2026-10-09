#!/usr/bin/env python3
"""Per-suite wall time from hosted run_all_suites shard logs (R474-4).

Usage: suite_times.py LOG...   Prints, per log, each suite's verdict and the
seconds since the previous verdict line (the sweep runs suites serially).
"""
import re, sys
from datetime import datetime
pat = re.compile(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z\s+(PASS|FAIL|TIMEOUT)\s+(\S+)")
start = re.compile(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z.*(run_all_suites|suites in this shard|shard \d/\d:)")
for path in sys.argv[1:]:
    prev = None
    rows = []
    for line in open(path, errors="replace"):
        m = pat.search(line)
        if m:
            t = datetime.fromisoformat(m.group(1)[:26])
            rows.append((m.group(3), m.group(2), (t - prev).total_seconds() if prev else None))
            prev = t
        elif prev is None:
            s = start.search(line)
            if s:
                prev = datetime.fromisoformat(s.group(1)[:26])
    print(path.rsplit("/", 1)[-1])
    for name, verdict, secs in rows:
        print(f"  {verdict:8s} {name:28s} {'' if secs is None else f'{secs:7.0f} s'}")

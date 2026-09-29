#!/usr/bin/env python3
"""Elapsed wall time of one suite in a run_all_suites.sh job log: from the
previous suite's verdict line to this suite's verdict line (the sweep runs
suites serially). Usage: hosted_timing.py <job.log> <suite> [guard_s]"""
import re, sys
from datetime import datetime
log, suite = sys.argv[1], sys.argv[2]
guard = float(sys.argv[3]) if len(sys.argv) > 3 else 1800.0
prev = None
for line in open(log, encoding="utf-8", errors="replace"):
    m = re.match(r"﻿?(\S+Z) (PASS|FAIL|TIMEOUT)\s+(\S+)", line)
    if not m:
        continue
    t = datetime.fromisoformat(m.group(1)[:26].rstrip("Z"))
    if m.group(3) == suite:
        dt = (t - prev[0]).total_seconds()
        print(f"{suite}: {m.group(2)} after {prev[1]} ; elapsed {dt:.2f} s ; guard {guard:.0f} s ; "
              f"margin {guard - dt:.2f} s = {100 * (guard - dt) / guard:.1f}% of the guard")
        break
    prev = (t, m.group(3))

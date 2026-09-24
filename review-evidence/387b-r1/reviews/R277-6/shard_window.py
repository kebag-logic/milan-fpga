#!/usr/bin/env python3
"""Window from 'shard: 4/5' to 'PASS milan_dp' in a hosted job log, and the
margin against a budget. Usage: shard_window.py <log> [budget_s=3600]"""
import re, sys
from datetime import datetime
log, budget = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 3600.0
ts = lambda l: datetime.strptime(l[:26], "%Y-%m-%dT%H:%M:%S.%f")
start = end = None; tail = []
for l in open(log, errors="replace"):
    if start is None and "shard: 4/5" in l: start = ts(l)
    if "PASS     milan_dp" in l or re.search(r"PASS\s+milan_dp\s*$", l): end = ts(l)
    if re.search(r"(suites: \d+ .*timed out|checks: \d+ )", l): tail.append(l[29:].strip())
w = (end - start).total_seconds()
print(f"window_s {w:.1f}"); print(f"budget_s {budget:.0f}")
print(f"margin_s {budget - w:.1f} ({100 * (budget - w) / budget:.1f}% of budget)")
for t in tail: print(t)

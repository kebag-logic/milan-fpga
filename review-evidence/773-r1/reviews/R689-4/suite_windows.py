#!/usr/bin/env python3
"""Print each suite's window in a hosted shard log: from the previous verdict line (or the
'selected suites' line) to its own PASS/FAIL/TIMEOUT line."""
import re, sys
from datetime import datetime
stamp = re.compile(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (.*)$")
prev = None
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    m = stamp.search(line)
    if not m:
        continue
    t = datetime.fromisoformat(m[1][:26])
    text = m[2]
    if "selected suites:" in text:
        prev = t
        print(text.strip())
        continue
    v = re.match(r"(PASS|FAIL|TIMEOUT)\s+(\S+)", text)
    if v and prev is not None:
        print(f"{v[1]:8s} {v[2]:32s} {(t - prev).total_seconds():8.1f} s")
        prev = t

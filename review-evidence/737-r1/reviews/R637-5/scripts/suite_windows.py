#!/usr/bin/env python3
"""Print every suite's verdict window from downloaded hosted job logs.

Usage: python3 suite_windows.py LOG...   (logs from `gh run view --log --job`)
A window runs from the previous suite verdict (or the step's first suite line)
to this suite's verdict line, matching the repository's measurement rule."""
import datetime
import sys

for path in sys.argv[1:]:
    prev = None
    for line in open(path, encoding="utf-8", errors="replace"):
        body = line.split("\t", 2)[-1].lstrip("﻿")
        ts, _, rest = body.partition(" ")
        word = rest.split()[0] if rest.split() else ""
        if word in ("PASS", "FAIL", "TIMEOUT"):
            t = datetime.datetime.fromisoformat(ts.rstrip("Z")[:26])
            if prev is not None:
                print(f"{path}\t{rest.split()[1]}\t{word}\t{(t - prev).total_seconds():.1f}")
            prev = t

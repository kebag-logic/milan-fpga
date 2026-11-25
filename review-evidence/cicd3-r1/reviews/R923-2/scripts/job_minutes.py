#!/usr/bin/env python3
"""Per-job minutes (completed_at - started_at) from Actions jobs API dumps (TSV: id, name, status,
conclusion, started_at, completed_at, attempt). usage: job_minutes.py jobs-*.tsv"""
import sys
from datetime import datetime
def t(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))
for path in sys.argv[1:]:
    print(f"== {path.rsplit('/',1)[-1]}")
    rows = []
    for line in open(path):
        i, name, status, concl, st, ct, att = line.rstrip("\n").split("\t")
        m = (t(ct) - t(st)).total_seconds() / 60 if st and ct else float("nan")
        rows.append((m, name, concl))
    for m, name, concl in sorted(rows, reverse=True):
        flag = "OVER30" if m > 30 else ""
        print(f"{m:6.1f}  {concl:9} {flag:6} {name}")

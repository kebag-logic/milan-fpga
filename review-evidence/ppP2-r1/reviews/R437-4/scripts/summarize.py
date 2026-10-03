#!/usr/bin/env python3
"""Summarize a probe.py JSON result: per probe, fails per (model, tmo) and the failing check IDs."""
import json, re, sys
from collections import defaultdict
res = json.load(open(sys.argv[1]))
by = defaultdict(list)
for r in res:
    if "error" in r:
        print(f"{r['job']}: ERROR {r['error']}"); continue
    by[r["probe"]].append(r)
for p, rs in sorted(by.items()):
    cells = []
    ids = set()
    for r in sorted(rs, key=lambda r: (r["model"], -int(r["tmo"]))):
        cells.append(f"{r['model'][:12]}@{r['tmo']}:{r['fail']}/{r['total']}")
        for n in r["fail_names"]:
            m = re.match(r"(T\d+[a-z]?|RW\d+|FZ\d+|Z\w+|BABBLE)", n)
            ids.add(m.group(1) if m else n[:30])
    print(f"{p}: " + " ".join(cells))
    if ids:
        print(f"    failing checks: {', '.join(sorted(ids))}")

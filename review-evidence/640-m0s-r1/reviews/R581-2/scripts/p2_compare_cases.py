#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare per-case fuzz logs written by p2_ruling_check.py.

Usage: p2_compare_cases.py <cases_base.json> <cases_head.json> <cases_hybrid.json>
Prints each tree's fuzz summary and failure count, then the cases where head and hybrid
(same fixture, base versus head gate code) disagree, with their labels and statuses.
"""
import json
import sys
from collections import Counter

base, head, hybrid = (json.load(open(path)) for path in sys.argv[1:4])
for run in (base, head, hybrid):
    print(f"{run['tree']}: fuzz rc {run['status']}; {run['summary']}; {len(run['cases'])} cases logged")
assert [(c["target"], c["label"], c["broken"]) for c in head["cases"]] == \
    [(c["target"], c["label"], c["broken"]) for c in hybrid["cases"]], "head and hybrid drew different cases"
diff = [(i, h, y) for i, (h, y) in enumerate(zip(head["cases"], hybrid["cases"])) if h["statuses"] != y["statuses"]]
print(f"head vs hybrid (same fixture, base vs head gate code): {len(diff)} of {len(head['cases'])} cases differ")
print("labels:", dict(Counter(h["label"] for _, h, _ in diff)))
print("targets:", dict(Counter(h["target"] for _, h, _ in diff)))
for i, h, y in diff:
    print(f"  case {i - 2}: {h['target']} {h['label']} broken={h['broken']} head {h['statuses']} "
          f"base-code {y['statuses']} | head reason {h['reason'][0][:150] if h['reason'] else '-'}")

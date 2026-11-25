#!/usr/bin/env python3
"""Recompute the planner's projections at 26 and 27 workers and compare the 27 with CI_WORKFLOWS.md's table.

usage: planner_probe.py TREE
"""
import re, sys
from pathlib import Path
tree = Path(sys.argv[1]); sys.path.insert(0, str(tree / "scripts"))
import suite_shards as s
suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
print("units", len(suites), "budget", s.CI_BUDGET_SECONDS)
for n in (26, 27):
    owner, load = s.balance(suites, n, overhead=(122,) * n)
    reg = load[:-1]
    print(n, "workers: max regular", max(reg), "over", [(i, v) for i, v in enumerate(reg) if v > s.CI_BUDGET_SECONDS], "last", load[-1],
          "loopback on", owner["input_loopback"], owner["input_loopback_dp"], "alone", [u for u, w in owner.items() if w == n - 1])
doc = (tree / "docs/testing/CI_WORKFLOWS.md").read_text()
rows = {int(a): (int(b), int(c), int(d)) for a, b, c, d in re.findall(r"\| `verilator-shards (\d+)/27` \| (\d+) \| (\d+) \| (\d+) \|", doc)}
owner, load = s.balance(suites, 27)
bad = [(i, v, rows.get(i)) for i, v in enumerate(load) if rows.get(i) is None or rows[i][0] != v or rows[i][1] - v != rows[i][2]]
print("doc rows", len(rows), "mismatches", bad)
t = dict(s.SUITE_SECONDS)
print("stale worker words:", [(p.name, m) for p in (tree/"docs/testing").glob("*.md") for m in re.findall(r"twenty-six[a-z -]{0,24}|/26\b", p.read_text())])
m = dict(s.SUITE_SECONDS)

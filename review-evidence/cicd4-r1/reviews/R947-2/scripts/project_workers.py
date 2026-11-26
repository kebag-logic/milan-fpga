#!/usr/bin/env python3
"""Recompute each rtl-full Verilator worker's projection from a checkout's suite_shards and compare it
with the policy page's verilator-shards rows. Usage: project_workers.py CHECKOUT"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import suite_shards as s
suites = s.expand_suites(s.sweep_suites(root / "tb/verilator"))
owners, load = s.balance(suites, 27)
doc = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
rows = {int(m[1]): (int(m[2]), int(m[3]), int(m[4]))
        for m in re.finditer(r"\| `verilator-shards (\d+)/27` \| (\d+) \| (\d+) \| (\d+) \|", doc)}
bad = 0
for w, v in enumerate(load):
    got = rows.get(w)
    ok = got is not None and got[0] == v and got[2] == got[1] - got[0]
    bad += not ok
    print(f"worker {w:2d}/27 computed {v:5d}  doc {got}  {'ok' if ok else 'MISMATCH'}")
print("gptp_shadow seconds", s.SUITE_SECONDS["gptp_shadow"], "worker", owners.get("gptp_shadow"))
print("budget", s.CI_BUDGET_SECONDS, "regular max", max(load[:-len(s.DEDICATED_SUITES)]))
print("mismatches", bad)
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""deal.py LANE_ROOT [W...]: deal the lane's current inventory and figures (suite_shards.balance) at each W
workers, each carrying the 122 s allowance, and print every worker's projection against the #998 budget."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import suite_shards as s  # noqa: E402

suites = s.expand_suites(s.sweep_suites(root / "tb" / "verilator"))
total = sum(s.SUITE_SECONDS[x] for x in suites)
print(f"{len(suites)} units, {total} s of figures; budget {s.CI_BUDGET_SECONDS} s")
for w in map(int, sys.argv[2:] or ["19"]):
    owners, load = s.balance(suites, w, s.SUITE_SECONDS, (122,) * w)
    over = [(i, v) for i, v in enumerate(load) if v > s.CI_BUDGET_SECONDS]
    print(f"W={w}: max {max(load)} min {min(load)} sum {sum(load)} over {over}")
    if len(sys.argv) > 2 and w == int(sys.argv[-1]):
        for i, v in enumerate(load):
            print(f"  {i:2} {v:5} {[x for x in suites if owners[x] == i]}")

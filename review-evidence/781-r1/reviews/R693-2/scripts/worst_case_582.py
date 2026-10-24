#!/usr/bin/env python3
"""Bound the stated open risk: SUITE_SECONDS["media_phase"] lowered to 582 s
while run_all_suites.sh still lets it run 1400 s. Balance the tree's inventory
with the lowered figure, then add the 818 s the estimate hides to the worker
that carries media_phase and compare with that worker's job timeout.

    python3 -E -s worst_case_582.py <tree>
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import suite_shards as ss  # noqa: E402

suites = ss.expand_suites(ss.sweep_suites(tree / "tb" / "verilator"))
workflow = (tree / ".github" / "workflows" / "rtl.yml").read_text(encoding="utf-8")
for figure in (1400, 582):
    seconds = {**ss.SUITE_SECONDS, "media_phase": figure}
    problems, load, bounds = ss.headroom_problems(suites, workflow, seconds)
    owners, _ = ss.balance(suites, len(load), seconds)
    worker = owners.get("media_phase")
    timeout_min = ss.verilator_worker_limits(workflow)[worker]
    print(f"figure {figure} s: problems={len(problems)} media_phase on worker "
          f"{worker}/{len(load)} predicted {load[worker]} s, bound {bounds[worker]} s")
    if figure == 582:
        actual = load[worker] - 582 + 1400
        print(f"  if media_phase then runs its full 1400 s deadline: {actual} s; "
              f"worker's timeout-minutes {timeout_min} min = "
              f"{timeout_min * 60} s; margin {timeout_min * 60 - actual} s")

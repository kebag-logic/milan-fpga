#!/usr/bin/env python3
"""Capacity replay for #799 option B. Run from the lane root:
    python3 -I <this> <measure-dir>
Reads the checkout's scripts/suite_shards.py and .github/workflows/rtl.yml,
balances the head's inventory with the head's table, then charges every
worker the hosted windows measured in this PR's runs instead of the table.
A suite with no window in those runs is charged its recorded figure."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
import suite_shards as s

LANE = ("40724689169", "40740015218")   # this PR, ca39dc1b and 4f3ebffb


def load(directory, run):
    text = (Path(directory) / f"measure-{run}.txt").read_text()
    return {k: int(v) for k, v in re.findall(r'"(\S+)": (\d+),', text)}


def main(directory):
    per_run = {run: load(directory, run) for run in LANE}
    measured = {}
    for windows in per_run.values():
        for k, v in windows.items():
            measured[k] = max(v, measured.get(k, 0))
    suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
    workflow = s.WORKFLOW.read_text(encoding="utf-8")
    limits = s.verilator_worker_limits(workflow)
    problems, predicted, bounds = s.headroom_problems(suites, workflow)
    owners, _ = s.balance(suites, len(limits))
    unmeasured = [x for x in suites if x not in measured]
    print(f"workers {len(limits)}, limits (min) {sorted(set(limits))}, "
          f"planner problems {problems}")
    print(f"charged at recorded figure (no window in {', '.join(LANE)}): "
          + ", ".join(f"{x} {s.SUITE_SECONDS[x]}" for x in unmeasured))
    print("table figures below this PR's largest window: "
          + (", ".join(f"{x} {s.SUITE_SECONDS[x]}<{measured[x]}" for x in suites
                       if x in measured and s.SUITE_SECONDS[x] < measured[x])
             or "none"))
    over_limit = over_budget = 0
    print("worker  predicted  bound  measured-replay  limit  verdict")
    for w, limit in enumerate(limits):
        replay = s.WORKER_OVERHEAD_SECONDS[w] + sum(
            measured.get(x, s.SUITE_SECONDS[x]) for x in suites if owners[x] == w)
        dedicated = w >= len(limits) - len(s.DEDICATED_SUITES)
        under_limit = replay < limit * 60
        under_budget = dedicated or replay <= 1620
        over_limit += not under_limit
        over_budget += not under_budget
        print(f"{w:>2}/{len(limits)}  {predicted[w]:>9}  {bounds[w]:>5}  {replay:>15}"
              f"  {limit * 60:>5}  {'under limit' if under_limit else 'OVER LIMIT'}"
              f"{'' if under_budget else ', over 1620 s'}")
    print(f"workers at or over their job limit: {over_limit}; regular workers over "
          f"1620 s at the measured windows: {over_budget}")
    return 1 if over_limit or problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

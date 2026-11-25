#!/usr/bin/env python3
"""plan.py: model milan_dp's legs at T legs from ci_make_cases.CASE_SECONDS (2-job LPT, the piece's start order),
and print each new leg's share of the old 4-leg leg that contains it.

usage: python3 -I plan.py LANE_ROOT T
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import ci_make_cases as cm  # noqa: E402

NAMES = ['gptp', 'gptp-lat', 'counters-1', 'counters-8', 'counters-1-frames', 'counters-8-frames', 'base', 'notify',
         'crflic', 'tspec8', 'sidmove', 'sidmove8', 'dynmap', 'nxn', 'nxndv', 'nxn8', 'nxn4c', 'nolpf', 'prune', 'ax1x1',
         'aclk', 'maprec8', 'maprec4', 'split', 'bootsa', 'render-mutants']
COST = cm.CASE_SECONDS["milan_dp"]


def makespan(cases, jobs=2):
    free = [0] * jobs
    for name in cm.start_order("milan_dp", cases):
        i = min(range(jobs), key=lambda j: free[j])
        free[i] += COST[name]
    return max(free)


T = int(sys.argv[2])
for k in range(T):
    new = NAMES[k::T]
    old = NAMES[k % 4::4]
    print(f"leg {k}/{T}: makespan {makespan(new):5}  old leg {k % 4}/4 {makespan(old):5}  ratio "
          f"{makespan(new) / makespan(old):.3f}  {new}")

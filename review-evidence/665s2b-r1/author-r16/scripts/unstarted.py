#!/usr/bin/env python3
"""A running leg's groups that have not started (no log in its results yet), in the order its run takes them
(scenario.all_groups, longest first, filtered by the leg's --groups), and the last COUNT of them, comma-separated,
for a helper run on the same build (leg2.sh). The leg and the helper are later combined by run.py --regrade.

usage: unstarted.py CHECKOUT BUILD_DIR GROUPS|all COUNT
"""
import json
import sys
from pathlib import Path

checkout, build_dir, wanted, count = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import run  # noqa: E402
import scenario  # noqa: E402

spec = json.loads((build_dir / 'build.json').read_text())
point = next(name for name, value in run.POINTS.items() if value == (spec['shape'], spec['interfaces']))
groups = scenario.all_groups(scenario.point(point, spec), spec)
if wanted != 'all':
    names = set(wanted.split(','))
    groups = [g for g in groups if g.name in names]
left = [g.name for g in groups if not (build_dir / 'results' / f'{g.name}.log').exists()]
print(f'{len(left)} of {len(groups)} not started', file=sys.stderr)
print(','.join(left[-count:]))

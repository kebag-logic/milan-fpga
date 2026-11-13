#!/usr/bin/env python3
"""Split a harness point's groups into K parts of about equal simulated time (lane 895, round 2).

usage: partition.py CLONE POINT SPEC_BUILD_JSON K OUT_PREFIX
Groups and their simulated ms come from run.all_groups(scenario.point(POINT, spec), spec) of CLONE's harness, with
the build spec of a build of that point and variant (the harness's group set does not depend on the firmware).
Longest first, each to the part with the least so far. Writes OUT_PREFIX<k>.groups and prints each part's total.
"""
import json, os, sys
from pathlib import Path
clone, point, spec_path, k, prefix = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
H = Path(clone) / 'tb/verilator/ctrl_service_budget'
sys.path[:0] = [str(H)]
os.chdir(H)
import run, scenario  # noqa: E402
spec = json.loads(Path(spec_path).read_text())
order = run.all_groups(scenario.point(point, spec), spec)
parts = [[] for _ in range(k)]
tot = [0.0] * k
for g in sorted(order, key=lambda g: -g.sim_ms):
    j = tot.index(min(tot))
    parts[j].append(g.name)
    tot[j] += g.sim_ms
for j in range(k):
    Path(f'{prefix}{j}.groups').write_text(','.join(parts[j]))
    print(f'part {j}: {len(parts[j])} groups, {tot[j] / 1000:.1f} simulated s')
print(f'{len(order)} groups')

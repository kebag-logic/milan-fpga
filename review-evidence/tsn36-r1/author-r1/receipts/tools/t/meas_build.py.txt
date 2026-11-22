#!/usr/bin/env python3
"""meas_build.py CLONE BUILD POINT VARIANT...: the CPU budget harness's build of each VARIANT at POINT, as run.py builds
by default (build.build: CPU regions cover, the split placement's L1, no XIP), into BUILD/<variant>, one after the
other; then each build's groups (run.all_groups) with their simulated time, in BUILD/<variant>/groups.json."""
import json
import subprocess
import sys
import time
from pathlib import Path

clone, root, point, variants = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4:]
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import build as builder  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402

assert builder.ROOT == clone
head = subprocess.run(['git', '-C', str(clone), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
shape, n_if = run.POINTS[point]
for v in variants:
    print(f'BUILD {point} {v} at {head} start {time.strftime("%H:%M:%S")}', flush=True)
    spec = builder.build(root / v, shape, n_if, mutation='none', variant=v, core=builder.Core('cover', 'split', False))
    groups = run.all_groups(scenario.point(point, spec), spec)
    (root / v / 'groups.json').write_text(json.dumps([{'name': g.name, 'sim_ms': g.sim_ms} for g in groups], indent=1))
    print(f'BUILT {point} {v}: {len(groups)} groups, end {time.strftime("%H:%M:%S")}', flush=True)

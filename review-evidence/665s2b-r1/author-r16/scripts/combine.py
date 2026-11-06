#!/usr/bin/env python3
"""Combine a leg with its helper run (helpers.sh): report which of the leg's groups each has finished (a log that ends
with the testbench's SUMMARY), and with --merge, once every group is finished by one of them, copy the helper's
scripts and logs into the leg's results, so `run.py --regrade` grades the whole leg from one directory.

usage: combine.py CHECKOUT BUILD_DIR HELPER[,HELPER...] GROUPS|all [--merge]
"""
import shutil
import sys
from pathlib import Path

checkout, build_dir, helper, wanted = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
merge = '--merge' in sys.argv[5:]
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import json  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402

spec = json.loads((build_dir / 'build.json').read_text())
point = next(name for name, value in run.POINTS.items() if value == (spec['shape'], spec['interfaces']))
groups = scenario.all_groups(scenario.point(point, spec), spec)
if wanted != 'all':
    names = set(wanted.split(','))
    groups = [g for g in groups if g.name in names]
own = build_dir / 'results'
done = lambda d, g: (d / f'{g}.log').is_file() and 'SUMMARY ' in (d / f'{g}.log').read_text(errors='replace')[-20000:]
mine = [g.name for g in groups if done(own, g.name)]
theirs: dict[str, Path] = {}
for name in helper.split(','):
    other = build_dir / f'results-{name}'
    theirs.update({g.name: other for g in groups if g.name not in mine and g.name not in theirs and done(other, g.name)})
missing = [g.name for g in groups if g.name not in mine and g.name not in theirs]
print(f'{build_dir.name}: {len(groups)} groups, {len(mine)} finished by the leg, {len(theirs)} by {helper}, '
      f'{len(missing)} by neither: {",".join(missing)}')
if merge:
    if missing:
        sys.exit('not merged: groups finished by neither')
    for g, other in theirs.items():
        for ext in ('txt', 'log'):
            shutil.copy2(other / f'{g}.{ext}', own / f'{g}.{ext}')
    print(f'merged {len(theirs)} groups from {helper}')

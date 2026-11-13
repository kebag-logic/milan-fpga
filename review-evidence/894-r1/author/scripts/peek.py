#!/usr/bin/env python3
"""Grade finished budget-harness logs with a tree's graders, without run.py: each group's share, stated-cost, round,
polls and slice findings, its rows' longest by ring, and its refusals. usage: peek.py TREE BUILD POINT LOG..."""
import json
import sys
from pathlib import Path

tree, build, point = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402

spec = json.loads((build / 'build.json').read_text())
groups = {g.name: g for g in run.all_groups(scenario.point(point, spec), spec)}
n_if = spec['interfaces']
results = []
for path in map(Path, sys.argv[4:]):
    g = groups[path.stem]
    try:
        r = grade.grade(path.read_text(errors='replace'), g, spec['sys_hz'], spec['cpu_hz'], n_if)
    except grade.Refusal as error:
        print(f'{path.stem}: REFUSED {error}')
        continue
    results.append(r)
    worst = {}
    for p in r['probes']:
        if p.get('status') == 'measured':
            k = p.get('ring')
            if k not in worst or p['ms'] > worst[k][0]:
                worst[k] = (p['ms'], p['probe'], p.get('budget_ms'))
    s = r['passes']
    print(f"{path.stem}: share over {s['share']['over']} of {s['share']['passes']}, worst pass "
          f"{s['worst']['cycles'] if s['worst'] else 0}; slices {s['slices']['slices']} longest {s['slices']['longest']} "
          f"limit {s['slices']['limit']}; " + ', '.join(f'{k} {v[0]:.3f} ({v[1]})' for k, v in sorted(worst.items())))
for line in run.share_misses(results) + run.stated_misses(results):
    print('MISS', line)

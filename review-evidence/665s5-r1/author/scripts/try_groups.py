#!/usr/bin/env python3
"""Feasibility: run named S2 scenario groups on a hook-harness build and grade them with S2's grader."""
import concurrent.futures, json, subprocess, sys
from pathlib import Path
ROOT = Path('$LANES/665-s5-hooks')
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import scenario, grade
b = Path(sys.argv[1]); names = sys.argv[2].split(',')
spec = json.loads((b / 'build.json').read_text())
p = scenario.point(spec['point'], spec)
groups = [g for g in scenario.all_groups(p, spec) if g.name in names]
out = b / 'try'; out.mkdir(exist_ok=True)
def one(g):
    (out / f'{g.name}.txt').write_text(g.script())
    with (out / f'{g.name}.log').open('w') as sink:
        subprocess.run([str(b / 'native/Vsim'), str(out / f'{g.name}.txt'), '-'], cwd=b / 'soc/gateware', stdout=sink, stderr=subprocess.STDOUT)
    return g
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    done = list(pool.map(one, groups))
for g in done:
    text = (out / f'{g.name}.log').read_text()
    try:
        r = grade.grade(text, g, spec['sys_hz'], spec['cpu_hz'])
    except grade.Refusal as e:
        print('REFUSED', g.name, e); print(text[-1500:]); continue
    for x in r['probes']:
        print(g.name, x['probe'], x['status'], x.get('ms'), x.get('reason', ''))

"""Probe: does run.py's plant verdict for counters-late depend on the plant?

Drives run.main() --plant counters-late with the build, the simulation and the grade replaced by the
author's published UNPLANTED 1x1 answering-arm results (runs/1x1-ans/results.json), restricted to the
plant's own group, hooks-counters. If main() prints 'caught' and returns 0, the verdict cannot fail
for the defect the plant claims to detect. Nothing is built; nothing is written in the checkout.
Usage: python3 -I plant_vacuity_probe.py <checkout> <results.json> <scratch dir>"""
import json, sys
from pathlib import Path
from unittest.mock import patch
root, results, scratch = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import run, hooks, hooks_build, scenario  # noqa: E402
pub = json.load(open(results))
group = hooks.plants()['counters-late'][1].group
unplanted = [f for f in pub['findings'] if f.endswith(f'({group})')]
print('plant group:', group)
print('unplanted findings in that group (published, no plant):', unplanted)
spec = dict(point='1x1', arm='answering', cpu_clock='sys', plant=None, cpu_hz=pub['cpu_hz'], sys_hz=pub['sys_hz'],
            executable_sha256=pub['build'])
def fake_grade(groups, logs, spec, out):
    return dict(rows=[], refusals=[], superseded=[], findings=list(unplanted),
                checks={h: dict(applied=0, undecided=0, findings=[]) for h in hooks.HOOKS})
build_dir = scratch / 'probe-counters-late'
build_dir.mkdir(parents=True, exist_ok=True)
with patch.object(sys, 'argv', ['run.py', '--plant', 'counters-late', '--build-dir', str(build_dir)]), \
     patch.object(hooks_build, 'build', lambda *a, **k: dict(spec)), \
     patch.object(scenario, 'point', lambda point, spec: None), \
     patch.object(hooks, 'groups', lambda p, spec: [scenario.Group(group)]), \
     patch.object(run, 'run_group', lambda b, o, g: o / f'{g.name}.log'), \
     patch.object(run, 'grade_all', fake_grade), \
     patch.object(run, 'table', lambda *a: ''):
    rc = run.main()
print('run.main() rc =', rc, '(0 = plant reported caught with NO plant applied)')

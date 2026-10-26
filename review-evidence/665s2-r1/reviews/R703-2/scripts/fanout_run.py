#!/usr/bin/env python3
"""Run and grade the sandbox's 'aecp-fanout-full' group on a finished build, without reuse.

Usage: fanout_run.py SANDBOX_HARNESS_DIR BUILD_DIR OUT_DIR
It writes the group's script, runs the build's native model on it exactly as run.py's run_group
does (cwd the build's gateware, flash '-'), and grades the log with the sandbox's grade.py.
"""
import json
import subprocess
import sys
from pathlib import Path

here, build, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(here))
import grade  # noqa: E402
import scenario  # noqa: E402

spec = json.loads((build / 'build.json').read_text())
point = '1x1' if spec['interfaces'] == 1 else '8x8'
g = next(x for x in scenario.all_groups(scenario.point(point, spec), spec) if x.name == 'aecp-fanout-full')
out.mkdir(parents=True, exist_ok=True)
script = out / f'{g.name}.txt'
script.write_text(g.script())
log = out / f'{g.name}.log'
with log.open('w') as sink:
    subprocess.run([str(build / 'native/Vsim'), str(script), '-'], cwd=build / 'gateware', stdout=sink,
                   stderr=subprocess.STDOUT, check=False)
r = grade.grade(log.read_text(), g, spec['sys_hz'], spec['cpu_hz'])
for row in r['probes']:
    print(json.dumps({k: row.get(k) for k in ('probe', 'status', 'reason', 'ms', 'within_t_svc', 'bound_ms',
                                              'passes', 'pass_cycles', 'ahead')}))
print('timeouts', r['timeouts'])

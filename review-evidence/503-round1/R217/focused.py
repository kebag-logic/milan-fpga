import importlib.util
import os
from pathlib import Path
import sys

evidence = Path('/data/milan/reviews/r217-scratch/evidence/design-evidence/500-materialization/proposal-evidence')
spec = importlib.util.spec_from_file_location('d3run', evidence / 'run.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
names = {
    'base-1x1', 'base-8x8', 'tracked-1x1',
    'mut-M01_taint_ignored', 'mut-M03_clear_wins_same_edge',
    'mut-M05_latch_ignores_program', 'mut-M13_restore_applies_nothing',
    'mut-M16_single_pass_restore', 'mut-A01_grant_cycle_not_busy',
    'mut-G02_restore_done_without_d3',
}
shapes = {n: r.prep_shape(n) for n in ['1x1', '8x8']}
results = {}
for build in r.all_builds(list(shapes)):
    if build.name not in names:
        continue
    r.do_build(build, shapes[build.shape], 8)
    print('BUILT', build.name, flush=True)
    results[build.name] = r.execute(build, shapes[build.shape])
    print('EXECUTED', build.name, len(results[build.name]), flush=True)
r.HERE = Path(os.environ['D3_OUT'])
r.report(results)

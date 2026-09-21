import importlib.util
import json
from pathlib import Path
import struct
import sys

ev = Path('/data/milan/reviews/r217-scratch/evidence/design-evidence/500-materialization/proposal-evidence')
spec = importlib.util.spec_from_file_location('d3map', ev / 'run.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
s = r.prep_shape('1x1')
b = r.Build('base-1x1', '1x1')
b.binary = r.OUT / 'build/base-1x1/obj/d3sim'
case = 'V3_refused_map_for_a_removed_cluster'
# A valid KLJ2 container and F07.8 frame, with an invalid stream index
# whose high byte aliases the prototype's single-byte padding test.
for stream in [0x0100, 0xff00]:
    over = {0x70: r.map_bytes([(stream, 0, 0, 0)], s.recs[0x70][2] // 8)}
    slots = r.crafted(s, f'reviewer-map-{stream:04x}', over)
    run = r.run_case(b, s, case, f'reviewer-{stream:04x}', slots)
    grade = r.grade_run(run, s, {'crafted': over})
    print(f'MAP stream={stream:04x} rc={run.rc} complete={run.done}')
    print(json.dumps(grade.checks, indent=2))
    print('RESTORE', run.obs.get('restored', {}).get('rs_ref'), run.obs.get('restored', {}).get('rs_app'))

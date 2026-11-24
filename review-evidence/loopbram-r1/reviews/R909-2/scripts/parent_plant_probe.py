#!/usr/bin/env python3
"""Run one of the parent harness's datapath connection plants at a chosen shape
(the harness's own driver runs them at 8x8 only). A plant is detected only if
the build succeeds and the run fails PARENT_SAMPLE.

usage: parent_plant_probe.py <tree> <out-dir> <shape 1|8> <plant>
plant: missing_edit_invalidation | disconnected_map
"""
import json
import subprocess
import sys
from pathlib import Path

tree, out, shape, plant = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
out.mkdir(parents=True, exist_ok=True)
dp = (tree / 'hdl/milan/milan_datapath.sv').read_text()
pulse = "else invalidate_r <= edit_change_w || direct_change_w || restore_change_w;"
plants = {
    'missing_edit_invalidation': (pulse, pulse.replace('edit_change_w', "1'b0", 1)),
    'disconnected_map': ("{(INPUT_LOOPBACK_P != 0){amap_in_store_r,",
                         "{(INPUT_LOOPBACK_P != 0){(AMAP_IN_KEYS_C*8)'(0),"),
}
old, new = plants[plant]
assert dp.count(old) == 1, (plant, dp.count(old))
src = out / 'milan_datapath.sv'
src.write_text(dp.replace(old, new, 1))
log = out / 'run.log'
with log.open('w') as sink:
    rc = subprocess.run([sys.executable, str(tree / 'tb/verilator/input_loopback_dp/run.py'), '--shape', shape,
                         '--work', str(out / 'work'), '--dp-source', str(src)], cwd=tree, stdout=sink,
                        stderr=subprocess.STDOUT, timeout=7200).returncode
text = log.read_text(errors='replace')
built = (out / 'work/obj/parent_loopback').is_file()
detected = built and rc != 0 and '[FAIL] PARENT_SAMPLE' in text and 'RESULT: FAIL' in text
res = dict(plant=plant, shape=int(shape), exit=rc, built=built, detected=detected,
           parent_sample_failures=text.count('[FAIL] PARENT_SAMPLE'))
(out / 'result.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res))
raise SystemExit(0 if detected else 1)

#!/usr/bin/env python3
"""Exercise the resource sweep's unmodified ship argv through the SoC instance probe."""
import json
import os
from pathlib import Path
import sys
repo, packet = map(Path,sys.argv[1:3])
sys.path[:0]=[str(repo/'sw/builder'),str(repo/'syn/resmap')]
import test_builder as t
import soc_sweep as sweep
cfg=t.eb.load_config(str(repo/'configs'/f'{sweep.yosys_sweep.BASE_CONFIG}.yaml'))
raw=t.eb.emit_soc_argv(cfg)
plan=json.loads((repo/'syn/resmap/sweep_plan.json').read_text())
ship=sweep.variant_argv(raw,plan['soc']['variants']['ship'])
ship+=['--entity-gen-dir',str(repo/'configs/generated'/cfg['name'])]
firmware=repo/ship[ship.index('--ctrl-firmware')+1]
print('ship expected:',plan['soc']['variants']['ship'].get('expect','accepted'))
print('control placement:',cfg['control']['placement'])
print('firmware exists:',firmware.exists())
assert not firmware.exists(), 'Probe needs a clean builder output with no prebuilt firmware'
out=t._instance_params(sys.argv[3],[('resource-ship',ship)])
print(json.dumps(out,indent=2))
assert 'No such file' in str(out) and 'ctrl_app.elf' in str(out)
print('REPRODUCED: resource ship export cannot load the firmware named by its generated argv')
base=t.eb.with_placement(cfg,'all-fabric')
base_argv=sweep.variant_argv(t.eb.emit_soc_argv(base),plan['soc']['variants']['ship'])
base_argv+=['--entity-gen-dir',str(repo/'configs/generated'/cfg['name'])]
control=t._instance_params(sys.argv[3],[('resource-ship-all-fabric',base_argv)])
print(json.dumps(control,indent=2))
assert 'error' not in control['resource-ship-all-fabric']
print('PASS baseline control: selecting all-fabric reaches the datapath with no firmware file')

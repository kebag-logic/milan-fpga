"""Retain the live wrong-name control at the current committed head."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
work = Path('$VALIDATION_STORAGE/607-a408-work')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
command = ['$WORKSPACE_HOME/litex-milan/venv/bin/python', '-B',
           'sw/builder/test_clock_constraints.py', '--vivado',
           '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado', '--checkpoint',
           '$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp',
           '--evidence-dir', str(work / ('live-plant-' + head[:9]))]
log = work / 'gates/live-plant-head.log'
started = time.monotonic()
with log.open('w') as stream:
    result = subprocess.run(command, cwd=root, env=dict(os.environ, TMPDIR=str(work)),
                            stdout=stream, stderr=subprocess.STDOUT, timeout=800)
row = dict(name='live-plant-head', head=head, command=command, rc=result.returncode,
           elapsed_s=round(time.monotonic() - started, 2), log=str(log),
           size=log.stat().st_size, sha256=hashlib.sha256(log.read_bytes()).hexdigest())
(out / 'live-plant-result.json').write_text(json.dumps(row, indent=2) + '\n')
print(json.dumps(row, indent=2))
raise SystemExit(result.returncode)

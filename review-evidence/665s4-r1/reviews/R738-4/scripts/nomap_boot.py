#!/usr/bin/env python3
"""Boots the no-map platform image on the boot SoC: exports it, builds the model and grades it with run.py's own
functions, the one change being that the image is linked with no --flash-map. Usage: nomap_boot.py CLONE RUN_DIR ELF OUT."""
import json, shutil, subprocess, sys
from pathlib import Path

clone, run_dir, elf, out = map(Path, sys.argv[1:5])
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_split_boot'))
import run as boot

shape = 'endstation_ax7101_1x1_tdm8'
out.mkdir(parents=True, exist_ok=True)
flash_map = run_dir / 'split-soc/flash-map'
spec = boot.export(out, 'soc', shape, elf, 1, flash_map)
spec['elf'] = str(elf)
exe = boot.verilate(out, spec)
with (out / 'sim.log').open('w') as sink:
    result = subprocess.run([str(exe), str(out / 'transcript.txt')], stdout=sink, stderr=subprocess.STDOUT,
                            check=False, cwd=out / 'soc/gateware')
(out / boot.STATUS).write_text(f'{result.returncode}\n')
findings, report = boot.grade((out / 'sim.log').read_text(), (out / 'transcript.txt').read_text(), spec,
                              out / 'baremetal', result.returncode)
print('\n'.join(report))
print('FINDINGS', json.dumps(findings, indent=1))
print('nomap boot:', 'FAIL' if findings else 'PASS', len(findings))

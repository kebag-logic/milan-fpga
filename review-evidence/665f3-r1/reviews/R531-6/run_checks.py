#!/usr/bin/env python3
"""Run independent checks concurrently, remain foreground, retain logs and return codes."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('--phase', choices=('sdk', 'checks', 'campaign'), default='checks')
ap.add_argument('--archive', type=Path)
a = ap.parse_args()
root = a.root.resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
(scratch / 'tmp').mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch / 'tmp'), PYTHONDONTWRITEBYTECODE='1',
           PYTHONUNBUFFERED='1', MILAN_RV32_CC=str(scratch / 'sdk/bin/riscv32-linux-gcc'))

def run(name, argv):
    start = time.monotonic()
    print(f'START {name}', flush=True)
    with (packet / f'{name}.log').open('w') as log:
        # subprocess.run waits here; no detached or background shell jobs.
        result = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    (packet / f'{name}.rc').write_text(f'{result.returncode}\n')
    receipt = {'name': name, 'argv': argv, 'rc': result.returncode,
               'seconds': round(time.monotonic() - start, 3)}
    (packet / f'{name}.command.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'END {name} rc={result.returncode} seconds={receipt["seconds"]}', flush=True)
    return receipt

if a.phase == 'sdk':
    cmd = [sys.executable, '-B', 'scripts/ci_rv32_sdk.py', '--destination', str(scratch / 'sdk')]
    if a.archive:
        cmd += ['--archive', str(a.archive.resolve())]
    sys.exit(run('sdk', cmd)['rc'])

tasks = [
    ('ctrl-suite', [sys.executable, '-B', 'sw/firmware/ctrl/test/test_ctrl_firmware.py',
                    '--require-rv32', '--jobs', '2', '--build-dir', str(scratch / 'suite')]),
    ('coverage', [sys.executable, '-B', 'sw/firmware/gtest/fw_coverage.py', '--check', '--jobs', '2']),
    ('images', [sys.executable, '-B', 'sw/firmware/ctrl/test/ctrl_image.py', '--base', '13e71513',
                '--out', str(scratch / 'images')]),
    ('focused', [sys.executable, '-B', str(packet / 'focused_probes.py'), str(root), str(packet), '--jobs', '2']),
]
# Three 3-job campaign slices + suite 2 + coverage 2 + focused 2 + image 1 = 16.
if a.phase == 'campaign':
    tasks = []
for index in range(3):
    tasks.append((f'campaign-{index}', [sys.executable, '-B', 'sw/firmware/ctrl/test/test_ctrl_firmware.py',
                 '--require-rv32', '--self-test', '--slice', f'{index + 1}/3',
                 '--jobs', '5' if a.phase == 'campaign' else '3',
                 '--build-dir', str(scratch / f'slice-{index}')]))
with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
    results = [f.result() for f in as_completed([pool.submit(run, name, argv) for name, argv in tasks])]
print(json.dumps(results, indent=2), flush=True)
sys.exit(int(any(r['rc'] != 0 for r in results)))

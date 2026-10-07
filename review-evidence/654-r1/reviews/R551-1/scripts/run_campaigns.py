#!/usr/bin/env python3
"""Foreground supervisor for two isolated export campaigns and cheap checks."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', required=True)
parser.add_argument('--packet', required=True)
parser.add_argument('--python', required=True)
parser.add_argument('--jobs', type=int, default=4)
args = parser.parse_args()
root, packet = Path(args.root).resolve(), Path(args.packet).resolve()
scratch = packet / 'scratch'
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0',
       'TMPDIR': str(scratch / 'tmp'), 'MAKEFLAGS': '-j16',
       'JAVA_TOOL_OPTIONS': f'-XX:ActiveProcessorCount={args.jobs} -Xmx2g',
       'MILAN_LITEX_PYTHON': args.python, 'VERILATOR_JOBS': str(args.jobs)}

def run(label, command, cwd, extra=None):
    start = time.monotonic()
    with (scratch / (label + '.log')).open('w') as log:
        result = subprocess.run(command, cwd=cwd, env={**env, **(extra or {})},
                                stdout=log, stderr=subprocess.STDOUT)
    (packet / 'receipts' / (label + '.rc')).write_text(str(result.returncode) + '\n')
    print(json.dumps({'case': label, 'rc': result.returncode, 'seconds': round(time.monotonic() - start, 2)}), flush=True)
    assert result.returncode == 0, label

def cpu():
    run('cpu-campaign', [args.python, str(packet / 'scripts/cpu_exports.py'),
        '--root', str(root), '--data', str(scratch / 'cpu'), '--out', str(scratch / 'cpu-exports'),
        '--expected', str(scratch / 'public/author/CPU-MEASUREMENTS.json'),
        '--result', str(packet / 'receipts/cpu-measurements.json'), '--jobs', str(args.jobs)], root)

def ax():
    for config in ('ax7101_8x8', 'ax7101_1x1_tdm8'):
        for phase in ('baseline-fixed', 'candidate-fixed'):
            run(f'ax-{config}-{phase}', [args.python, str(scratch / 'public/author/export_compare.py'), phase, config],
                scratch / 'export-tree', {'MEASURE_DIR': str(scratch / 'ax'),
                                         'VEX_DATA_DIR': str(scratch / 'cpu/vexiiriscv')})

def cheap():
    run('refusals', [args.python, 'sw/builder/test_soc_options.py'], root)

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(fn) for fn in (cpu, ax, cheap)]
    failures = []
    for future in futures:
        try:
            future.result()
        except Exception as exc:
            failures.append(str(exc))
    if failures:
        raise SystemExit('FAILED campaigns: ' + ', '.join(failures))
print('ALL FOCUSED CAMPAIGNS PASS', flush=True)

#!/usr/bin/env python3
"""Reproduce the focused review; all disposable output stays under scratch.

Run with --repo, --litex-python, --sdk-archive and --verilator paths.
The calling process owns and waits for every child; there are no detached jobs.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--litex-python', required=True)
ap.add_argument('--sdk-archive', type=Path, required=True)
ap.add_argument('--verilator', type=Path, required=True)
args = ap.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
logs = packet / 'receipts'
logs.mkdir(exist_ok=True)
tree = scratch / 'test-tree'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
           TMPDIR=str(scratch), MAKEFLAGS='-j16',
           PATH=str(args.verilator.parent) + ':' + os.environ['PATH'])

def run(label, command, cwd=None):
    """Run foreground, retaining the complete combined stream and return code."""
    with (logs / (label + '.log')).open('w') as output:
        rc = subprocess.run(command, cwd=cwd or args.repo, env=env,
                            stdout=output, stderr=subprocess.STDOUT).returncode
    (logs / (label + '.rc')).write_text(str(rc) + '\n')
    print(label, 'rc', rc, flush=True)
    return rc

if not tree.exists():
    subprocess.run(['git', 'clone', '--shared', '--no-hardlinks', '--quiet',
                    str(args.repo), str(tree)], check=True)
    for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
        subprocess.run(['git', '-c', 'protocol.file.allow=always', '-c',
                        f'submodule.{sub}.url={args.repo / sub}', 'submodule',
                        'update', '--init', sub], cwd=tree, check=True)

# Redirect the CPU data cache into scratch. Copy existing bytes; no shared cache writes.
vdir = Path(subprocess.check_output([args.litex_python, '-c',
    'import pythondata_cpu_vexiiriscv as d; print(d.data_location)'], text=True).strip())
cache = scratch / 'cpu-data'
cache.mkdir(exist_ok=True)
for path in vdir.iterdir():
    if path.is_file():
        shutil.copy2(path, cache / path.name)
hook = scratch / 'python-hook'
hook.mkdir(exist_ok=True)
(hook / 'sitecustomize.py').write_text(
    'import os\nimport pythondata_cpu_vexiiriscv as d\n'
    'd.data_location = os.environ["REVIEW_CPU_DATA"]\n')
env.update(PYTHONPATH=str(hook), REVIEW_CPU_DATA=str(cache),
           MILAN_RV32_CC=str(scratch / 'sdk/bin/riscv32-linux-gcc'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    tasks = [pool.submit(run, 'sdk', [sys.executable, 'scripts/ci_rv32_sdk.py',
              '--destination', str(scratch / 'sdk'), '--archive', str(args.sdk_archive)]),
             pool.submit(run, 'runner-selftest', ['bash', 'scripts/run_litex_sims.sh', '--selftest'], tree),
             pool.submit(run, 'diff-check', ['git', 'diff', '--check',
              'e8454e2751d05b02ee8e5a571857589ab358ab86', 'HEAD'], tree)]
    codes = [t.result() for t in tasks]
if any(codes):
    raise SystemExit(1)
(scratch / 'run-environment.json').write_text(json.dumps(env))
raise SystemExit(run('test-ctrl-memory', [args.litex_python,
                     'sw/litex/test_ctrl_memory.py'], tree))

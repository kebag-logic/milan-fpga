"""Reproduce the focused target run without modifying shared dependencies.

Usage: python3 run_target.py --litex-root DIR --sdk DIR --compiler FILE
Run from the reviewed checkout. Supply the existing product environment,
RV32 SDK and scoped pinned simulation compiler. Never installs dependencies.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--litex-root', type=Path, required=True)
ap.add_argument('--sdk', type=Path, required=True)
ap.add_argument('--compiler', type=Path, required=True)
args = ap.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
cpu = scratch / 'pythondata_cpu_vexiiriscv'
if not cpu.exists():
    shutil.copytree(args.litex_root / 'pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv', cpu)
bindir = scratch / 'tool-bin'
bindir.mkdir(exist_ok=True)
for name, target in [('verilator', args.compiler.resolve()), ('meson', Path('/usr/bin/meson'))]:
    link = bindir / name
    if not link.exists():
        link.symlink_to(target)
tmp = scratch / 'tmp'
tmp.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(tmp), PYTHONPATH=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           PYTHONHASHSEED='0', LITEX_ENV_CC_TRIPLE='riscv32-linux', COURSIER_MODE='offline',
           SBT_OPTS='-Dsbt.offline=true')
env['PATH'] = ':'.join(map(str, [bindir, args.litex_root/'venv/bin', args.sdk/'bin'])) + ':' + os.environ['PATH']
command = [str(args.litex_root/'venv/bin/python3'), '-B', 'tb/verilator/nvm_split_target/run.py',
           '--point', '1x1', '--jobs', '16', '--build-dir', str(scratch/'target-1x1')]
with (scratch/'target-build.log').open('w') as log:
    rc = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
(packet/'target-build.rc').write_text(f'{rc}\n')
raise SystemExit(rc)

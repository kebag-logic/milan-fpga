#!/usr/bin/env python3
"""Run bounded independent startup checks; all children are joined before exit.

Usage: python3 scripts/run_focused.py CHECKOUT SIMULATOR
Outputs and disposable source/build trees are relative to this packet.
"""
import concurrent.futures
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(sys.argv[1]).resolve()
SIM = str(Path(sys.argv[2]).resolve())
SCRATCH = ROOT / 'scratch'
RECEIPTS = ROOT / 'receipts'
HEAD = '41bc9dac031526c1fd637ff1e801d3c6dc1260b4'
BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'


def run(name, command, cwd, env, expected=0):
    raw = SCRATCH / (name + '.raw.log')
    with raw.open('w') as log:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=540)
    text = raw.read_text(errors='replace')
    text = text.replace(str(ROOT), '<packet>').replace(str(REPO), '<checkout>')
    text = text.replace(str(Path(SIM).parent), '<simulator-install>')
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator',
                  '<simulator-runtime>', text)
    (RECEIPTS / (name + '.log')).write_text(text)
    (RECEIPTS / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(f'{name}: rc={result.returncode}, expected={expected}', flush=True)
    if result.returncode != expected:
        raise RuntimeError(name)


def main():
    subprocess.run([SIM, '--version'], check=True)
    paths = ['tb/verilator/aaf', 'tb/common', 'hdl/ieee1722/aaf',
             'hdl/common/cdc_pair_fifo.sv']
    data = subprocess.check_output(['git', 'archive', HEAD, *paths], cwd=REPO)
    source = SCRATCH / 'focused-source'
    source.mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(source, filter='data')
    old = SCRATCH / 'base-packetizer.sv'
    old.write_bytes(subprocess.check_output(
        ['git', 'show', BASE + ':hdl/ieee1722/aaf/KL_aaf_packetizer.sv'], cwd=REPO))
    env = os.environ.copy()
    env.update(VERILATOR=SIM, VERILATOR_JOBS='2', TMPDIR=str(SCRATCH))
    suite = source / 'tb/verilator/aaf'
    # Each startup build has two workers. Four campaign arms plus the
    # independent red build stay below the assigned sixteen-worker ceiling.
    commands = [
        ('startup-head', ['make', '-j16', '--no-print-directory', 'startup-mutants',
                          'START_JOBS=4', 'VERILATOR_JOBS=2'], 0),
        ('startup-base', ['make', '-j16', '--no-print-directory', 'startup',
                          f'START_RTL={old}', f'START_MDIR={SCRATCH / "base-obj"}',
                          'VERILATOR_JOBS=2'], 2),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, name, command, suite, env, expected)
                   for name, command, expected in commands]
        for future in futures:
            future.result()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Run N=8 context-format contract and four plants with bounded build jobs.

Usage: python3 focused_rtl.py REPOSITORY PACKET --jobs 8 --verilator PATH
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=8)
p.add_argument('--verilator', required=True)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
here = root / 'tb/verilator/avtp_rxmon'
sys.path.insert(0, str(here))
import ctxfmt_mutants as cm
scratch = packet / 'scratch/rtl'
scratch.mkdir(parents=True, exist_ok=True)
version = subprocess.check_output([a.verilator, '--version'], text=True)
(packet / 'rtl-version.txt').write_text(version)
assert 'Verilator 5.050 ' in version, version
flags = subprocess.check_output(['make', '-s', '--eval=printflags:;@echo $(NXFLAGS)', 'printflags'], cwd=here, text=True)
flags = flags.strip().replace('-j 0', f'-j {a.jobs}')
# Preserve the quoted CFLAGS value, lost by the shell's echo above.
flags = flags.replace('-CFLAGS -std=c++17 -O2 -Wall -Wextra', '-CFLAGS "-std=c++17 -O2 -Wall -Wextra"')
original = cm.RTL.read_text()
failures = 0
cases = [('clean', original, None)]
for idx, (name, old, new, check) in enumerate(cm.MUTATIONS):
    assert original.count(old) == 1, name
    cases.append((f'plant{idx}', original.replace(old, new), check))
for label, source, check in cases:
    rtl = scratch / (label + '.sv')
    rtl.write_text(source)
    obj = scratch / ('obj-' + label)
    cmd = ['make', '-j16', '-C', str(here), 'ctxfmt-build', f'VERILATOR={a.verilator}',
           f'NXFLAGS={flags}', f'RXMON_SRC={rtl}', f'CF_MDIR={obj}']
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (packet / ('rtl-' + label + '-build.log')).write_text(run.stdout)
    assert run.returncode == 0, run.stdout[-4000:]
    run = subprocess.run([str(obj / cm.EXE_NAME)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (packet / ('rtl-' + label + '.log')).write_text(run.stdout)
    verdict = cm.verdict(run.returncode, run.stdout, check)
    ok = verdict == ('pass' if check is None else 'caught')
    print(f'{label}: {verdict}; expected check: {check}', flush=True)
    failures += not ok
print(f'focused RTL failures: {failures}', flush=True)
sys.exit(bool(failures))

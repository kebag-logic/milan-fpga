#!/usr/bin/env python3
"""Foreground supervisor: bounded concurrent focused checks, all children joined."""
from concurrent.futures import ThreadPoolExecutor
import os
import pathlib
import runpy
import subprocess
import sys

packet = pathlib.Path(__file__).resolve().parent
root = packet / 'scratch/probe'
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True)
env = os.environ.copy()
env['TMPDIR'] = str(packet / 'scratch')
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['CCACHE_DISABLE'] = '1'
sim = pathlib.Path(sys.argv[1]).resolve()
def run(name, commands, cwd=root):
    with (receipts / (name + '.log')).open('w') as log:
        for args in commands:
            print('COMMAND', repr(args), file=log, flush=True)
            p = subprocess.run(args, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
            print('EXIT', p.returncode, file=log, flush=True)
            if p.returncode:
                (receipts / (name + '.rc')).write_text(str(p.returncode) + '\n')
                return name, p.returncode
    (receipts / (name + '.rc')).write_text('0\n')
    return name, 0
def plane():
    flags = '--cc --exe --build -j 8 --top-module gptp_plane_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P=\'"gptp_ucode.hex"\' -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I. -Wall -Wextra -DOUR_CQ_TB=0xf822436a"'
    quality = hex(runpy.run_path(str(root / 'gptp-processor/hdl/ucode/gen_gptp_ucode.py'))['CQ_C'])
    flags = flags.replace('0xf822436a', quality)
    return run('plane', [
        [str(sim), '--version'],
        ['make', '-j16', 'run', 'VERILATOR=' + str(sim), 'VFLAGS=' + flags],
        ['python3', 'link_delay.py', '--work', str(packet / 'scratch/link-delay')],
    ], root / 'tb/verilator/gptp_plane')
def adp():
    return run('adp', [['python3', str(packet / 'adp_probe.py'), str(root), str(packet / 'scratch/adp')]])
def docs():
    return run('docs', [['python3', 'scripts/check_py_idiom.py'],
        ['python3', 'scripts/measure_test_evidence.py', '--check'],
        ['python3', 'scripts/check_submodule_docs.py'],
        ['python3', 'scripts/check_gptp_docs.py']])
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(f) for f in (plane, adp, docs)]
    results = [f.result() for f in futures]
print(results, flush=True)
raise SystemExit(any(rc for _, rc in results))

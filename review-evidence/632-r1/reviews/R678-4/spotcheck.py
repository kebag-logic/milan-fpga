#!/usr/bin/env python3
"""Run the two focused queue shapes in a disposable exact-head export."""
import concurrent.futures
import os
import re
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
compiler = Path(sys.argv[2]).resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/queue-spotcheck'
work.mkdir(parents=True, exist_ok=True)
archive = packet / 'scratch/head.tar'
with archive.open('wb') as out:
    subprocess.run(['git', '-C', str(repo), 'archive', 'HEAD'], stdout=out, check=True)
subprocess.run(['tar', '-xf', str(archive), '-C', str(work)], check=True)
identity = subprocess.check_output([str(compiler), '--version'], text=True).strip()
assert '5.050' in identity, identity

def run(shape):
    cmd = ['make', '-j16', '-C', str(work/'tb/verilator/render_queue'), 'run',
           f'VERILATOR={compiler}', 'VERILATOR_JOBS=8', f'MDIR=obj_{shape}']
    if shape == 'odd':
        cmd += ['N_STREAMS=1', 'N_CH=7', 'N_IF=1', 'LEAD1=0']
    raw = packet/f'scratch/queue-{shape}.log'
    with raw.open('w') as out:
        proc = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, timeout=300)
    text = raw.read_text().replace(str(work), '<disposable-checkout>').replace(str(compiler), '<scoped-compiler>')
    text = re.sub(r'/home/[^\s]+?/usr/share/verilator', '<compiler-install>', text)
    (packet/f'queue-{shape}.log').write_text(text)
    (packet/f'queue-{shape}.rc').write_text(str(proc.returncode)+'\n')
    print(shape, 'rc', proc.returncode, flush=True)
    assert proc.returncode == 0

print(identity, flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run, ['two-interface', 'odd']))

#!/usr/bin/env python3
"""Rebuild the public runtime and four head/base composition pairs."""
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parents[1];scratch=packet/'scratch'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(scratch),
         MILAN_RV32_CC=str(scratch/'sdk/bin/riscv32-linux-gcc'))
def command(args):
    print('ARGV',json.dumps(args),flush=True)
    subprocess.run(args,cwd=repo,env=env,check=True)
command([sys.executable,'sw/firmware/ctrl/test/ctrl_image_runtime.py',
 '--picolibc',str(scratch/'runtime-inputs/picolibc'),
 '--compiler-rt',str(scratch/'runtime-inputs/compiler-rt'),
 '--litex-software',str(scratch/'runtime-inputs/litex-software'),
 '--output',str(scratch/'runtime')])
base=scratch/'base';base.mkdir(exist_ok=True)
archive=scratch/'base.tar'
with archive.open('wb') as out:
    subprocess.run(['git','archive','db9aa8c9b135b34ff3d070a979dee70440b37cc6',
                    'sw/firmware/ctrl'],cwd=repo,stdout=out,check=True)
command(['tar','-xf',str(archive),'-C',str(base)])
def measure(item):
    shape,n,srp=item;name=f'{shape}-if{n}-'+('head' if srp else 'base')
    out=scratch/'sizes'/name
    cmd=[sys.executable,'sw/firmware/ctrl/test/ctrl_image.py',
         '--config',f'configs/endstation_ax7101_{shape}.yaml',
         '--interfaces',str(n),'--output',str(out),
         '--libc',str(scratch/'runtime/libc.a'),
         '--compiler-runtime',str(scratch/'runtime/libcompiler_rt.a')]
    if not srp:cmd+=['--without-srp','--ctrl-source',str(base/'sw/firmware/ctrl')]
    command(cmd)
    return dict(name=name,**json.loads((out/'size.json').read_text()))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(measure,[(shape,n,srp) for shape in ('1x1_tdm8','8x8')
                                  for n in (1,2) for srp in (False,True)]))
(packet/'receipts/sizes.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:print(r['name'],r['ram_span'],r['sections'])

#!/usr/bin/env python3
"""Twelve comparable links at base, round five, and review head."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve();packet=Path(__file__).resolve().parents[1];scratch=packet/'scratch'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(scratch),MILAN_RV32_CC=str(scratch/'sdk/bin/riscv32-linux-gcc'))
def command(args,log):
 r=subprocess.run(args,cwd=repo,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (packet/'receipts'/log).write_text(r.stdout.replace(str(repo),'${SOURCE}').replace(str(packet),'${PACKET}'))
 if r.returncode:raise RuntimeError((log,r.returncode))
command([sys.executable,'sw/firmware/ctrl/test/ctrl_image_runtime.py','--picolibc',str(scratch/'runtime-inputs/picolibc'),'--compiler-rt',str(scratch/'runtime-inputs/compiler-rt'),'--litex-software',str(scratch/'runtime-inputs/litex-software'),'--output',str(scratch/'runtime')],'runtime-build.log')
for mode,rev in [('base','db9aa8c9b135b34ff3d070a979dee70440b37cc6'),('round5','500b8f64443777685e6a54049d933476710d26f0')]:
 dest=scratch/mode;dest.mkdir(exist_ok=True);archive=scratch/(mode+'.tar')
 with archive.open('wb') as out:subprocess.run(['git','archive',rev,'sw/firmware/ctrl'],cwd=repo,stdout=out,check=True)
 subprocess.run(['tar','-xf',str(archive),'-C',str(dest)],check=True)
# The R5 and current dependency compiled sources must be identical.
subprocess.run(['git','-C',str(repo/'third_party/lwSRP'),'diff','--exit-code','a4cbe41d','HEAD','--','src'],check=True)
def measure(item):
 shape,n,mode=item;name=f'{shape}-if{n}-{mode}';out=scratch/'sizes'/name
 export=scratch/mode if mode!='head' else repo
 args=[sys.executable,str(packet/'scripts/image_one.py'),str(repo),mode,str(export),'--config',str(repo/f'configs/endstation_ax7101_{shape}.yaml'),'--interfaces',str(n),'--output',str(out),'--libc',str(scratch/'runtime/libc.a'),'--compiler-runtime',str(scratch/'runtime/libcompiler_rt.a')]
 if mode in ('base','round5'):args+=['--ctrl-source',str(export/'sw/firmware/ctrl')]
 if mode=='base':args+=['--without-srp']
 command(args,name+'.log')
 r={'name':name,**json.loads((out/'size.json').read_text())}
 (packet/'receipts'/(name+'-symbols.txt')).write_text((out/'symbols.txt').read_text())
 print(name,r['ram_span'],flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(measure,[(s,n,m) for s in ('1x1_tdm8','8x8') for n in (1,2) for m in ('base','round5','head')]))
(packet/'receipts/sizes.json').write_text(json.dumps(results,indent=2)+'\n')
(packet/'receipts/runtime-provenance.json').write_text((scratch/'runtime/provenance.json').read_text().replace(str(repo),'${SOURCE}').replace(str(packet),'${PACKET}'))

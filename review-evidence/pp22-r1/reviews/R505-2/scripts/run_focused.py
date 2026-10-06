#!/usr/bin/env python3
"""Foreground supervisor: four independent builds, four workers per build."""
import argparse, concurrent.futures, io, json, os, re, subprocess, tarfile, time
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('repo',type=Path)
p.add_argument('packet',type=Path)
p.add_argument('--verilator',required=True,type=Path)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
assert 1 <= a.jobs <= 4
version=subprocess.check_output([str(a.verilator),'--version'],text=True)
assert 'Verilator 5.050' in version
(a.packet/'receipts/compiler-version.txt').write_text(version)
root=a.packet/'scratch/focused'; root.mkdir(parents=True,exist_ok=True)
subprocess.run(['git','-C',str(a.repo),'archive','--output='+str(root/'source.tar'),'HEAD'],check=True)
with tarfile.open(root/'source.tar') as t: t.extractall(root/'tree',filter='data')
wrapper=root/'bounded-compiler.py'
wrapper.write_text('''#!/usr/bin/env python3
import os,sys
args=sys.argv[1:]
for i,x in enumerate(args[:-1]):
    if x == '-j': args[i+1]='4'
os.execv(os.environ['REVIEW_COMPILER'],[os.environ['REVIEW_COMPILER'],*args])
''')
wrapper.chmod(0o755)
env=os.environ.copy(); env.update(REVIEW_COMPILER=str(a.verilator),VERILATOR=str(wrapper),TMPDIR=str(root),MAKEFLAGS='-j16')
def run(suite):
    log=a.packet/'receipts'/f'{suite}.log'; start=time.monotonic()
    cmd=['make','-j16','-C',str(root/'tree/tb'/suite)]
    # The focused stream bank includes all four walk shapes. The SRP top
    # bank includes the complete default suite plus four storage shapes.
    with log.open('w') as f:
        rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (a.packet/'receipts'/f'{suite}.rc').write_text(str(rc)+'\n')
    tallies=re.findall(r'^.*\d+ checks:.*$',log.read_text(),re.M)
    row=dict(suite=suite,rc=rc,seconds=round(time.monotonic()-start,3),tallies=tallies)
    print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
    rows=list(ex.map(run,['originator','rx_validator','srp_stream_fsms','srp_top']))
(a.packet/'receipts/focused-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(any(r['rc'] or not r['tallies'] for r in rows))

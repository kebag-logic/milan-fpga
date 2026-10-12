#!/usr/bin/env python3
import argparse, concurrent.futures, os, pathlib, shutil, subprocess
p=argparse.ArgumentParser();p.add_argument('repo',type=pathlib.Path);p.add_argument('packet',type=pathlib.Path);a=p.parse_args();repo=a.repo.resolve();packet=a.packet.resolve()
def run(row):
 name,shape,variant=row; work=packet/'scratch'/name
 cmd=['python3','tb/verilator/milan_dp/stream_counter_f5.py','--shape',str(shape),'--variant',variant,'--work',str(work)]
 with (packet/'receipts'/f'{name}.driver.log').open('w') as log:
  r=subprocess.run(cmd,cwd=repo,env=dict(os.environ,TMPDIR=str(packet/'scratch'),PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=subprocess.STDOUT)
 (packet/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 for f in ('run.log','escape.log'):
  if (work/f).exists():shutil.copyfile(work/f,packet/'receipts'/f'{name}.{f}')
 print(name,r.returncode,flush=True);return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,[('f5-1',1,'clean'),('f5-8',8,'clean'),('f5-late',1,'late'),('f5-rate',1,'rate')]))
raise SystemExit(int(any(results)))

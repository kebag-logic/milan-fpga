#!/usr/bin/env python3
"""Run one foreground command with bounded runtime and durable receipts."""
import argparse, json, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--entry-bin',type=Path,required=True);p.add_argument('--name',required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
raw=a.packet/'scratch/raw';raw.mkdir(parents=True,exist_ok=True)
tmp=a.packet/'scratch/tmp';tmp.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j8',PATH=str(a.entry_bin)+os.pathsep+os.environ['PATH'])
command=a.command[1:] if a.command[:1]==['--'] else a.command
start=time.monotonic()
with (raw/(a.name+'.log')).open('w') as f:
 r=subprocess.run(command,cwd=a.root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
result=dict(name=a.name,argv=command,returncode=r.returncode,elapsed_seconds=round(time.monotonic()-start,3))
(raw/(a.name+'.run.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result));print((raw/(a.name+'.log')).read_text()[-5000:])
raise SystemExit(r.returncode)

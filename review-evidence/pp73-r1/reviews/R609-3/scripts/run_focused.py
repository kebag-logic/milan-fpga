#!/usr/bin/env python3
"""Run independent focused checks concurrently, waiting for every foreground child."""
import argparse,concurrent.futures,json,os,subprocess,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);a=ap.parse_args()
p=a.packet.resolve();root=p/'scratch/head';receipts=p/'receipts'
env=os.environ.copy();env.update(TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j16')
wrap=str(p/'scripts/bounded-verilator')
cases=[('command-controls',['python3','-B','tb/aecp_cmds/mutants.py','--jobs','4','--verilator',wrap,'--output',str(receipts/'command-controls')],root),
       ('ucpu',['make','-j16','run','VERILATOR='+wrap],root/'tb/ucpu'),
       ('focused-docs',['make','-j16','aecpcmd','links','matrix','modmatrix','params','ids','figures'],a.source.resolve()),
       ('pr-reference',['python3','-B','scripts/check_aecp_commands.py','--pr-body',str(receipts/'pr-body.md')],root)]
def run(case):
    name,cmd,cwd=case;t=time.monotonic()
    with (receipts/(name+'.log')).open('w') as f:
        f.write('COMMAND '+json.dumps(cmd)+'\n');f.flush()
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,check=False).returncode
    (receipts/(name+'.rc')).write_text(str(rc)+'\n')
    result=dict(name=name,rc=rc,elapsed_seconds=round(time.monotonic()-t,3));print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,cases))
(receipts/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(int(any(x['rc'] for x in results)))

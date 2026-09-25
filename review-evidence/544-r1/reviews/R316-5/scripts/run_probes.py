#!/usr/bin/env python3
"""Re-run published probe bytes unchanged, using foreground child processes."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--sdk',type=Path,required=True);a=p.parse_args()
raw=a.packet/'scratch/raw';tmp=a.packet/'scratch/tmp';env=dict(os.environ,TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j2')
pub=a.packet/'public-inputs/reviews';jobs=[]
probe=pub/'R316-2/scripts/r316-2/probe2.py'
for mode,disable in [('sdk',None),('absent',None),('sdk','assert_preprocessed_asm_allowlist'),('sdk','assert_preprocessed_identity_sample'),('absent','assert_identity_macro_free')]:
 name='r316-'+mode+('-'+disable if disable else '')
 cmd=[sys.executable,'-B',str(probe),mode,'--out',str(raw/(name+'.json')),'--scratch',str(tmp)]
 if mode=='sdk':cmd+=['--sdk',str(a.sdk)]
 if disable:cmd+=['--disable',disable]
 jobs.append((name,cmd))
probe=pub/'R316-2/scripts/r316-2/probe3.py'
for disable in [None,'mut:nested','mut:asm','mut:extblank','mut:register','mut:storage']:
 name='r316-sub-'+(disable or 'none').replace(':','-')
 cmd=[sys.executable,'-B',str(probe),'sdk','--sdk',str(a.sdk),'--out',str(raw/(name+'.json')),'--scratch',str(tmp)]
 if disable:cmd+=['--disable',disable]
 jobs.append((name,cmd))
probe=pub/'R317-2/probe_gate1b_r2.py'
for case in ['cases_544_r2','cases_544_r2b','cases_544_r2c','cases_544_r2d','cases_544_r2e']:
 for mode,disconnect in [('sdk',False),('absent',False),('sdk',True)]:
  name='public-'+case+'-'+mode+('-disconnected' if disconnect else '')
  cmd=[sys.executable,'-B',str(probe),'--mode',mode,'--rev','head','--cases',case,'--tag',name,'--outdir',str(raw)]
  if mode=='sdk':cmd+=['--sdk',str(a.sdk)]
  if disconnect:cmd+=['--disconnect']
  jobs.append((name,cmd))
results=[]
for name,cmd in jobs:
 print('START '+name,flush=True);start=time.monotonic()
 with (raw/(name+'.log')).open('w') as f:
  r=subprocess.run(cmd,cwd=a.root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
 row=dict(name=name,argv=cmd,returncode=r.returncode,elapsed_seconds=round(time.monotonic()-start,3));results.append(row)
 (raw/'probe-runs.json').write_text(json.dumps(results,indent=2)+'\n')
 print('DONE '+json.dumps(row),flush=True)
 if r.returncode:print((raw/(name+'.log')).read_text()[-4000:],flush=True)
assert all(r['returncode']==0 for r in results), 'probe process failed'

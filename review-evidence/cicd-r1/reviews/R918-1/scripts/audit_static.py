#!/usr/bin/env python3
"""Recalculate public performance claims and check cache guard selection."""
from pathlib import Path
import json, os, subprocess, sys
P=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
source=(repo/'scripts/run_all_suites.sh').read_text()
block=source[source.index('if [ -z "${OBJCACHE+set}" ]'):source.index('LOGS_READY=0')]
rows=[]
for installed in (False,True):
 d=P/'scratch'/('cache-present' if installed else 'cache-absent');d.mkdir(parents=True,exist_ok=True)
 if installed:
  (d/'ccache').write_text('#!/bin/sh\nexit 0\n');(d/'ccache').chmod(0o755)
 for value in (None,'','custom-cache'):
  env=dict(os.environ,PATH=str(d));env.pop('OBJCACHE',None)
  if value is not None:env['OBJCACHE']=value
  cp=subprocess.run(['/bin/bash','-uc',block+'printf "%s|%s\\n" "${OBJCACHE+set}" "${OBJCACHE-}"'],env=env,text=True,capture_output=True)
  want=('set|'+value+'\n') if value is not None else ('set|ccache\n' if installed else '|\n')
  assert cp.returncode==0 and cp.stdout==want,(installed,value,cp)
  rows.append({'installed':installed,'input':value,'observed':cp.stdout.strip(),'rc':cp.returncode})
print(json.dumps({'guard_cases':rows},indent=2))
A=P/'receipts/author'
def perf(name):
 result={}
 for line in (A/'budget'/name).read_text().splitlines():
  a=line.split(',')
  if len(a)>3 and a[0].replace('.','',1).isdigit():result[a[2]]=float(a[0])
 return result
for suffix in ('','-2','-3'):
 b=perf('base'+suffix+'.perf');h=perf('tbO3'+suffix+'.perf')
 print(json.dumps({'pair':suffix or '1', 'cpu_saving_pct':100*(1-h['task-clock:u']/b['task-clock:u']), 'l1d_miss_saving_pct':100*(1-h['L1-dcache-load-misses:u']/b['L1-dcache-load-misses:u'])}))
for name in ('nocc.time','cold.time','warm.time','cold.stats'):
 print('ccache/'+name+': '+(A/'ccache'/name).read_text().strip())

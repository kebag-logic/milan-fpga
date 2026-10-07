#!/usr/bin/env python3
"""Run focused SRP suites or mutation controls without modifying source."""
import argparse, json, os, re, shutil, sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('repo',type=Path);ap.add_argument('mode',choices=['suites','probes','campaign','new-if1']);ap.add_argument('--jobs',type=int,default=2);a=ap.parse_args()
repo=a.repo.resolve();packet=Path(__file__).resolve().parents[1];scratch=packet/'scratch';rec=packet/'receipts'
os.environ['TMPDIR']=str(scratch);os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import srp_arms, srp_mutants, fw_gtest
from ctrl_build import CTRL, Tree
lw=repo/'third_party/lwSRP';out=scratch/a.mode
build=fw_gtest.Build(jobs=a.jobs)
results=[]
def normalize(t):return t.replace(str(repo),'${SOURCE}').replace(str(packet),'${PACKET}')
def run_test(n,suite,selected='*',debug=False):
 tree=Tree(CTRL,out,out/'reuse',build)
 r=srp_arms.arm_srp(tree,lw,n,debug=debug,test=(suite,selected))
 name=Path(suite).stem+('-debug' if debug else '')+f'-if{n}'
 (rec/(name+'.log')).write_text(normalize(r.log));(rec/(name+'.rc')).write_text(str(r.rc)+'\n')
 results.append({'name':name,'rc':r.rc});print(name,r.rc,flush=True)
 return r
if a.mode in ('campaign','new-if1'):
 if a.mode=='new-if1':
  srp_mutants.DEFECTS=srp_mutants.DEFECTS[-12:]
  original=srp_mutants.arm_srp
  def one(tree,lwsrp,interfaces,**kw):return original(tree,lwsrp,1,**kw)
  srp_mutants.arm_srp=one
 failed=srp_mutants.campaign(out,lw,jobs=a.jobs)
 dest=rec/a.mode;dest.mkdir(exist_ok=True)
 for f in out.glob('*.log'):(dest/f.name).write_text(normalize(f.read_text()))
 results.append({'name':a.mode,'plants':len(srp_mutants.DEFECTS),'rc':int(failed)})
elif a.mode=='suites':
 for n in (1,2):
  for suite in ('srp_mbx.cpp','srp_rx_retry.cpp','srp_app.cpp','srp_latency.cpp','srp_walk.cpp'):
   run_test(n,suite)
  run_test(n,'srp_debug.cpp',debug=True)
elif a.mode=='probes':
 for n in (1,2):
  for f in ('r532_hol_probe.cpp','r532_flood_probe.cpp','r533_5_independent.cpp','r532_retry_probes.cpp'):
   selected='R532Hol.ManyDomainValuesInOneValidPdu:R532Hol.ThirtyDomainValues' if f=='r532_hol_probe.cpp' else '*'
   r=run_test(n,str(packet/'scripts'/f),selected)
   if f=='r532_hol_probe.cpp':
    starts=[int(x) for x in re.findall(r'N=\d+ bytes=\d+ pending=\d+ refused=\d+ received=(\d+)',r.log)]
    lines=[s for s in r.log.splitlines() if 't+5s ' in s]
    assert len(lines)==len(starts)==2
    assert all('pending=0 ' in s and f'received={before+1} ' in s and 'active=0 ' in s for before,s in zip(starts,lines)),lines
(rec/(a.mode+'.json')).write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(x['rc'] for x in results))

#!/usr/bin/env python3
"""Run foreground focused checks; all generated objects stay in packet scratch."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('repo',type=Path)
ap.add_argument('--mode',choices=['suites','campaign','probes'],required=True)
ap.add_argument('--jobs',type=int,default=4)
a=ap.parse_args(); repo=a.repo.resolve(); packet=Path(__file__).resolve().parents[1]
scratch=packet/'scratch'/a.mode; scratch.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import srp_arms, srp_mutants, ctrl_arms, fw_gtest
from ctrl_build import CTRL,Tree
lw=repo/'third_party/lwSRP'
ctrl_arms.lwsrp_pin(lw)
build=fw_gtest.Build(jobs=a.jobs)
failed=False
if a.mode=='campaign':
    sys.exit(int(srp_mutants.campaign(scratch,lw,jobs=a.jobs)))
if a.mode=='suites':
    tree=Tree(CTRL,scratch/'build',scratch/'reuse',build)
    for n in (1,2):
        for suite in ('srp_mbx.cpp','srp_walk.cpp','srp_latency.cpp'):
            r=srp_arms.arm_srp(tree,lw,n,test=suite)
            print(r.arm,r.rc,r.log,flush=True);failed |= bool(r.rc)
    sys.exit(int(failed))

srp_arms.HERE=packet/'scripts'
results=[]
def run(name,library,selected='Srp.Review*',src=CTRL):
    for n in (1,2):
        r=srp_arms.arm_srp(Tree(src,scratch/name/f'if{n}',scratch/'reuse',build),library,n,
                         test=('independent.cpp',selected))
        log=packet/'receipts'/f'{name}-if{n}.log';log.write_text(r.log)
        print(name,n,r.rc,r.log,flush=True)
        results.append({'name':name,'interfaces':n,'rc':r.rc,'log':log.name})
run('head-probes',lw)
# Raw source exports are intentional fault-control inputs, never offered as
# exact-pin production evidence. The original pin was checked above.
def export(rev,name):
    dest=scratch/name;dest.mkdir(exist_ok=True)
    archive=scratch/f'{name}.tar'
    with archive.open('wb') as out:
        subprocess.run(['git','-C',str(lw),'archive',rev],stdout=out,check=True)
    subprocess.run(['tar','-xf',str(archive),'-C',str(dest)],check=True)
    return dest
srp_arms.lwsrp_pin=lambda path: 'deliberate independent probe source'
old=export('23d9a8173b07503a0ee6e8528f922fceab4e67f0','old-library')
run('old-pin-withdraw-control',old,'Srp.ReviewWithdrawDuringExhaustionSurvivesRecovery')
plants=[
 ('atomic-prepass-removed','src/core/mrp_pdu.c',
  'int r = parse_pass(pdu, len, ops, NULL, NULL, NULL);','int r = 0;',
  'Srp.ReviewAtomicInvalidSuffixCannotStartTalker'),
 ('lv-changed-indication-removed','src/core/mrp_mad.c',
  'previous && previous->reg != MRP_REG_STATE_MT &&',
  'previous && previous->reg == MRP_REG_STATE_IN &&',
  'Srp.ReviewChangedListenerInLvIndicatesBeforePoll'),
 ('future-version-skip-removed','src/core/mrp_pdu.c',
  'bool unknown = !expected && later;','bool unknown = false;',
  'Srp.ReviewFutureUnknownMessageKeepsFollowingKnownListener'),
]
for name,path,before,after,selected in plants:
    copy=export('a4cbe41de1c80d43f26e0d348cbdb45075273a4f',name)
    p=copy/path;data=p.read_text();assert data.count(before)==1,(name,data.count(before))
    p.write_text(data.replace(before,after))
    run(name,copy,selected)
(packet/'receipts/probes.json').write_text(json.dumps(results,indent=2)+'\n')
# Failing head probes are reported; deliberate controls must behave as declared.
assert all(r['rc']==0 for r in results if r['name']=='old-pin-withdraw-control')
assert all(r['rc']!=0 for r in results if r['name'] not in ('head-probes','old-pin-withdraw-control'))

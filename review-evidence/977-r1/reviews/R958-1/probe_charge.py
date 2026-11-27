#!/usr/bin/env python3
"""Build the unchanged firmware with the mixed-vector review probe, in scratch."""
import argparse
import os
import shutil
import sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--root',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--point',choices=['1x1','8x8'],required=True)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
root=a.root.resolve(); packet=a.packet.resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build, srp_arms, fw_gtest
out=packet/'scratch'/('charge-'+a.point)
out.mkdir(parents=True,exist_ok=True)
shutil.copyfile(packet/'probe_charge.cpp',out/'probe_charge.cpp')
srp_arms.HERE=out
tree=ctrl_build.Tree(ctrl_build.CTRL,out,out/'reuse',fw_gtest.Build(jobs=a.jobs))
config=srp_arms.DEFAULT_ENTITY if a.point=='1x1' else srp_arms.ENTITY_8X8
os.environ['REVIEW_BOUND_ONLY']='1'
result=srp_arms.arm_srp(tree,root/'third_party/lwSRP',1,
    test=('probe_charge.cpp','Srp.ReviewMixedBoundAndKeptVector'),config=config)
print('BOUND-ONLY POSITIVE CONTROL\n'+result.log,flush=True)
os.environ.pop('REVIEW_BOUND_ONLY')
exe=out/result.arm/'suite'
ok, log=fw_gtest.run_binary(exe,['--gtest_filter=Srp.ReviewMixedBoundAndKeptVector'],cwd=exe.parent)
print('MIXED BOUND/KEPT PROBE\n'+log,flush=True)
sys.exit(0 if result.rc==0 and ok else 1)

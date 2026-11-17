#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--interfaces',type=int,choices=(1,2),default=1)
args=ap.parse_args()
packet=Path(__file__).resolve().parent
repo=args.repo.resolve()
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_build
import fw_gtest
import srp_arms
out=packet/'scratch'/f'rebind-if{args.interfaces}'
tests=out/'tests'
tests.mkdir(parents=True,exist_ok=True)
(tests/'srp_mbx.cpp').write_bytes((repo/'sw/firmware/ctrl/test/srp_mbx.cpp').read_bytes()+
                                (packet/'rebind.cpp').read_bytes())
srp_arms.HERE=tests
tree=ctrl_build.Tree(ctrl_build.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=8))
r=srp_arms.arm_srp(tree,repo/'third_party/lwSRP',args.interfaces,
                  test=('srp_mbx.cpp','SrpTalkerKinds.ReviewRebinding*'))
(packet/f'rebind-if{args.interfaces}.log').write_text(r.log)
(packet/f'rebind-if{args.interfaces}.rc').write_text(str(r.rc)+'\n')
print(r.log)
raise SystemExit(r.rc)

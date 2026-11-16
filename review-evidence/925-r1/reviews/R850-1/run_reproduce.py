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
out=packet/'scratch'/f'reproduce-if{args.interfaces}'
tests=out/'tests'
tests.mkdir(parents=True,exist_ok=True)
srp_arms.HERE=tests
tree=ctrl_build.Tree(ctrl_build.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=8))
failed=False
for suite,addition,selected in [('srp_mbx.cpp','reproduce.cpp','SrpTalkerKinds.ReviewMinimal*'),
                                ('test_acmp_mbx.cpp','reproduce_feedback.cpp','SrpFeedback.ReviewNew*')]:
    (tests/suite).write_bytes((repo/'sw/firmware/ctrl/test'/suite).read_bytes()+
                             (packet/addition).read_bytes())
    result=srp_arms.arm_srp(tree,repo/'third_party/lwSRP',args.interfaces,test=(suite,selected))
    stem=f'reproduce-if{args.interfaces}-{suite}'
    (packet/(stem+'.log')).write_text(result.log)
    (packet/(stem+'.rc')).write_text(str(result.rc)+'\n')
    print(result.log,flush=True)
    failed |= bool(result.rc)
raise SystemExit(int(failed))

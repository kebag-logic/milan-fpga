import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import CTRL,Tree
import srp_arms,fw_gtest
root=Path(os.environ["SCRATCH"])
probe=Path(os.environ["REVIEW_PACKET"])/"review-evidence/665f4-r1/reviews/R533-5/scripts/independent.cpp"
for n in (1,2):
 r=srp_arms.arm_srp(Tree(CTRL,root/"probe-build",root/"reuse",fw_gtest.Build(jobs=4)),Path.cwd()/"third_party/lwSRP",n,test=str(probe))
 print(r.arm,r.rc,r.log,flush=True)
 if r.rc: raise SystemExit(r.rc)

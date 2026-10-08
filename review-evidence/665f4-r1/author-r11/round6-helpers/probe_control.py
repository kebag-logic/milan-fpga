import os
import shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import CTRL,Tree
import srp_arms,srp_mutants,fw_gtest
root=Path(os.environ["SCRATCH"])
copy=root/"probe-control-src"
shutil.copytree(CTRL,copy,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
p=copy/"srp/srp_mbx.c"
s=p.read_text(); old="if (apply_receive(m,&m->pending_rx))"; assert s.count(old)==1
p.write_text(s.replace(old,"if (true)"))
probe=Path(os.environ["REVIEW_PACKET"])/"review-evidence/665f4-r1/reviews/R533-5/scripts/independent.cpp"
selected="Srp.ReviewWithdrawDuringExhaustionSurvivesRecovery"
for n in (1,2):
 r=srp_arms.arm_srp(Tree(copy,root/"probe-control-build",root/"reuse",fw_gtest.Build(jobs=4)),Path.cwd()/"third_party/lwSRP",n,test=(str(probe),selected))
 print(r.arm,r.rc,r.log,flush=True)
 if not srp_mutants.caught(selected,"adapter.ifs[0].active[0]",r): raise SystemExit(1)
print("Both interface counts reject removed retry")

from pathlib import Path
import shutil,sys,json
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import CTRL,ROOT,Tree
import srp_arms,fw_gtest
r=Path(__file__).resolve().parent
src=r/"probe-ctrl"
shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
p=src/"test/srp_feedback.hpp"
p.write_bytes(p.read_bytes()+b"\n"+(r/"r12_failed_intrapdu.hpp").read_bytes())
# Test compilation normally uses the canonical test directory. Override it
# only for this disposable tree, so the original reviewer probes also run.
srp_arms.HERE=src/"test"
for n in (1,2):
 result=srp_arms.arm_srp(Tree(src,r/"probe-build",r/"probe-reuse",fw_gtest.Build(jobs=4)),ROOT/"third_party/lwSRP",n,test=("test_acmp_mbx.cpp","SrpFeedback.R12*"))
 (r/f"review-probes-if{n}.log").write_text(result.log)
 print(result.log,flush=True)
 if result.rc: raise SystemExit(result.rc)

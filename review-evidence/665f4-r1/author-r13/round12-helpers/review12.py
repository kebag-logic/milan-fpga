from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_arms,fw_gtest
from ctrl_build import ROOT,CTRL,Tree
r=Path(__file__).resolve().parent
tests=r/"review12-tests"
shutil.copytree(CTRL/"test",tests,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
for p in (r/"review11").glob("*.hpp"): shutil.copyfile(p,tests/p.name)
shutil.copyfile(r/"review/r532_11_probe.hpp",tests/"r532_11_probe.hpp")
p=tests/"test_acmp_mbx.cpp"
p.write_text(p.read_text()+"\n"+"\n".join('#include "'+n+'"' for n in ("independent_feedback.hpp","r532_10_probe_kind.hpp","r532_10_probe_guard.hpp","r532_11_probe.hpp"))+"\n")
srp_arms.HERE=tests
selected="R11Feedback.*:R533Feedback.*:SrpBinding.R10KindChange*:SrpBinding.R10FailedToAdvertise*:SrpBinding.R10DiscoveredWithdrawal*:SrpBinding.R10Replacement*:SrpBinding.R10Earlier*"
for n in (1,2):
 out=r/"review12-build"
 result=srp_arms.arm_srp(Tree(CTRL,out,out/"reuse",fw_gtest.Build(jobs=4)),ROOT/"third_party/lwSRP",n,test=("test_acmp_mbx.cpp",selected))
 print(result.log,flush=True)
 (r/f"review12-if{n}.log").write_text(result.log)
 if result.rc: raise SystemExit(result.rc)

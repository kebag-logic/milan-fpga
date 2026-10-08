from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_arms,fw_gtest
from ctrl_build import CTRL,ROOT,Tree
r=Path(__file__).resolve().parent
for n in (1,2):
 for suite in ("srp_app.cpp","test_acmp_mbx.cpp"):
  o=srp_arms.arm_srp(Tree(CTRL,r/"focused",r/"focused/reuse",fw_gtest.Build(jobs=4)),ROOT/"third_party/lwSRP",n,test=suite)
  print(o.log,flush=True)
  if o.rc: raise SystemExit(o.rc)

from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import ROOT,CTRL,Tree
import srp_arms,fw_gtest
r=Path(__file__).resolve().parent
build=fw_gtest.Build(jobs=4,address_sanitizer=True)
for n in (1,2):
 for suite in ("srp_mbx.cpp","srp_rx_retry.cpp","srp_app.cpp","test_acmp_mbx.cpp","srp_latency.cpp","srp_walk.cpp","srp_debug.cpp"):
  out=r/"asan-build"
  result=srp_arms.arm_srp(Tree(CTRL,out,out/"reuse",build),ROOT/"third_party/lwSRP",n,debug=suite=="srp_debug.cpp",test=suite)
  (r/f"asan-{suite}-if{n}.log").write_text(result.log)
  print(result.log,flush=True)
  if result.rc: raise SystemExit(result.rc)

import sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import aecp_arms
from ctrl_build import Tree,CTRL
import fw_gtest
parts=[out.parent/"reviews/R565-1/scripts/probe_cases.cpp",out.parent/"reviews/R564-1/probes/probe_tests.cpp",out.parent/"reviews/R564-1/probes/probe_tests_p6.cpp"]
(out/"test_aecp.cpp").write_text((CTRL/"test/test_aecp.cpp").read_text()+"\n"+"\n".join(p.read_text() for p in parts))
aecp_arms.HERE=out
result=aecp_arms.core_arm(Tree(CTRL,out/"build",out/"reuse",fw_gtest.Build(jobs=4)),root/"configs/endstation_ax7101_1x1_tdm8.yaml",2,"core",sys.argv[3] if len(sys.argv)>3 else "Core.R565*:Core.P*")
print(result.log)
raise SystemExit(result.rc)

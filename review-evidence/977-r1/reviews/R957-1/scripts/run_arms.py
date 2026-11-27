#!/usr/bin/env python3
"""Reviewer driver: run named firmware gate arms of a checkout (read only) with builds under an out dir.

usage: run_arms.py <repo> <out dir> <arm>
  arm: port | adp | acmp | srp-mbx-1x1 | srp-mbx-8x8 | srp-acmp-1x1 | srp-acmp-8x8 | srp-talker-1x1 | srp-talker-8x8
"""
import sys
from pathlib import Path

repo, out, arm = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
import ctrl_arms  # noqa: E402
import srp_arms  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = Tree(src=repo / "sw/firmware/ctrl", out=out, reuse=out / "reuse", build=fw_gtest.Build(jobs=2))
lwsrp = repo / "third_party/lwSRP"
cfg = {"1x1": repo / "configs/endstation_ax7101_1x1_tdm8.yaml", "8x8": repo / "configs/endstation_ax7101_8x8.yaml"}
if arm == "port":
    r = ctrl_arms.arm_port(tree)
elif arm == "adp":
    r = ctrl_arms.arm_adp(tree)
elif arm == "acmp":
    r = ctrl_arms.arm_acmp(tree)
else:
    _, suite, point = arm.split("-")
    test = {"mbx": "srp_mbx.cpp", "acmp": ("test_acmp_mbx.cpp", "SrpBinding.*:SrpGate.*"),
            "talker": "srp_talker.cpp"}[suite]
    r = srp_arms.arm_srp(tree, lwsrp, 1, test=test, config=cfg[point])
for line in r.log.splitlines():
    if "[FAIL]" in line or "checks:" in line or "C0 " in line or "RESULT" in line:
        print(line)
print(f"ARM {r.arm} rc={r.rc}")
sys.exit(r.rc)

#!/usr/bin/env python3
"""Run the unchanged platform boot/PHY arm; all build products stay in packet scratch."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_build import Tree, CTRL, fw_gtest
from plat_arms import arm_platboot
out = packet / "scratch/focused"
out.mkdir(parents=True, exist_ok=True)
result = arm_platboot(Tree(CTRL, out, out / "reuse", fw_gtest.Build(jobs=8)), 1)
print(result.log)
print("focused platform arm rc=" + str(result.rc))
raise SystemExit(result.rc)

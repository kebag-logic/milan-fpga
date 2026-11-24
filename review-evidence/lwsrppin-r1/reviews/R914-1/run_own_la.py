#!/usr/bin/env python3
"""Focused reproduction. Arguments: checkout, output, dependency checkout, revision, shape."""
import sys
from pathlib import Path

root, out, dependency = map(lambda p: Path(p).resolve(), sys.argv[1:4])
revision, shape = sys.argv[4:6]
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build
import ctrl_arms
import srp_arms
import fw_gtest

# Select the historical dependency only in this isolated probe process.
# The normal pin verifier still checks its checkout and compiled source tree.
ctrl_arms.LWSRP_REV = revision
tree = ctrl_build.Tree(ctrl_build.CTRL, out, out / "reuse", fw_gtest.Build(jobs=4))
config = srp_arms.ENTITY_8X8 if shape == "8x8" else srp_arms.DEFAULT_ENTITY
result = srp_arms.arm_srp(tree, dependency, 1, test="srp_own_leaveall.cpp", config=config)
print(f"dependency={revision} shape={shape}/1if rc={result.rc}")
print(result.log)
raise SystemExit(result.rc)

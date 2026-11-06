#!/usr/bin/env python3
"""Reviewer driver: build and run the AECP mailbox gtest arm of a probe copy of the tree, with a gtest filter.
usage: run_aecp_mailbox_arm.py TREE_ROOT OUTPUT_DIR FILTER [INTERFACES]
The probe copy has no git metadata, so the stack pin check of aecp_arms.py's main() is not run here; the stack
sources are the copy's own (byte copies of the checked-out submodule at the reviewed head)."""
import sys
from pathlib import Path
root, out, flt = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
ifs = int(sys.argv[4]) if len(sys.argv) > 4 else 1
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import fw_gtest
from ctrl_build import CTRL, STACK, Tree
import aecp_arms
tree = Tree(CTRL, out, out / "reuse", fw_gtest.Build(jobs=4), STACK)
r = aecp_arms.core_arm(tree, root / "configs/endstation_ax7101_1x1_tdm8.yaml", ifs, "mailbox", flt)
print(r.log)
sys.exit(r.rc)

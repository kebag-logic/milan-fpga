#!/usr/bin/env python3
"""Run the exact core's host tests and RV32IM object audit."""
from pathlib import Path
import sys
p=Path(__file__).resolve().parent
(p/"scratch").mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode=True
r=Path(sys.argv[1]).resolve()
sys.path[:0]=[str(r/'sw/firmware/ctrl/test'),str(r/'sw/firmware/gtest')]
from ctrl_build import Tree
import fw_gtest
import gptp_arms
tree=Tree(r/'sw/firmware/ctrl',p/'scratch/core-arms',p/'scratch/core-reuse',fw_gtest.Build(jobs=2))
results=gptp_arms.all_arms(tree,True)
(p/'core-arms.log').write_text('\n'.join(x.log for x in results))
rc=max(x.rc for x in results)
(p/'core-arms.rc').write_text(str(rc)+'\n')
print((p/'core-arms.log').read_text())
sys.exit(rc)

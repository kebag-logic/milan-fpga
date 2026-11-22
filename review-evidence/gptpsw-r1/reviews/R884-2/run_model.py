#!/usr/bin/env python3
"""Run the host mailbox model arm, including the new GEN snapshot regression."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;R=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(R/'sw/firmware/ctrl/test'))
from ctrl_build import Tree
import ctrl_arms, fw_gtest
t=Tree(R/'sw/firmware/ctrl',P/'scratch/model',P/'scratch/model-reuse',fw_gtest.Build(jobs=4))
o=ctrl_arms.arm_model(t)
(P/'model.log').write_text(o.log)
(P/'model.rc').write_text(str(o.rc)+'\n')
print(o.log)
sys.exit(o.rc)

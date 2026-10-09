#!/usr/bin/env python3
import sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve();out=packet/'scratch/probes';out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import aecp_arms,fw_gtest
from ctrl_build import Tree,CTRL
parts=[packet/'scripts'/n for n in ('r565.cpp','r564.cpp','r564-p6.cpp')]
(out/'test_aecp.cpp').write_text((CTRL/'test/test_aecp.cpp').read_text()+'\n'+'\n'.join(p.read_text() for p in parts))
aecp_arms.HERE=out
result=aecp_arms.core_arm(Tree(CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=4)),root/'configs/endstation_ax7101_1x1_tdm8.yaml',2,'core','Core.R565*:Core.P2*:Core.P3*:Core.P6*')
print(result.log)
raise SystemExit(result.rc)

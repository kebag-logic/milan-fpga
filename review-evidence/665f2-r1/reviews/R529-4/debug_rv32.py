#!/usr/bin/env python3
import argparse,sys,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve()
sys.path.insert(0,str(r/'sw/firmware/ctrl/test'));import ctrl_arms,ctrl_build,fw_gtest,fw_rv32
ctrl_arms.RV32_FLAGS=tuple(x for x in ctrl_arms.RV32_FLAGS if x!='-DNDEBUG')
t=ctrl_build.Tree(r/'sw/firmware/ctrl',p/'scratch/debug-rv32',p/'scratch/reuse-debug',fw_gtest.Build(jobs=1))
o=ctrl_arms.arm_rv32(t,True);print(o.log);assert o.rc==0
cc=ctrl_arms.rv32_compiler();obj=t.out/'rv32/maap_maap.o'
u=subprocess.check_output([cc.removesuffix('gcc')+'nm','-u',str(obj)],text=True);print('MAAP DEBUG UNDEFINED\n'+u);assert '__assert_fail' in u
assert not fw_rv32.object_findings(cc,[obj])
print('PASS: all twelve debug objects; assertion handler unresolved as expected; no debug-runtime link claim')

#!/usr/bin/env python3
"""Focused target-object checks for the largest supported SRP entity."""
import argparse
import sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args(); root=a.repo.resolve(); packet=a.packet.resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
from ctrl_build import CTRL,Tree
import fw_gtest
from srp_arms import arm_srp_rv32
out=packet/'target'; out.mkdir(exist_ok=True)
tree=Tree(CTRL,packet/'scratch/target/build',packet/'scratch/target/reuse',fw_gtest.Build(jobs=a.jobs))
failed=False
for n in (1,2):
    r=arm_srp_rv32(tree,root/'third_party/lwSRP',n,root/'configs/endstation_ax7101_8x8.yaml')
    (out/f'if{n}.log').write_text(r.log)
    (out/f'if{n}.rc').write_text(str(int(r.rc))+'\n')
    print(f'target objects interfaces={n} rc={int(r.rc)}',flush=True)
    failed |= bool(r.rc)
raise SystemExit(int(failed))

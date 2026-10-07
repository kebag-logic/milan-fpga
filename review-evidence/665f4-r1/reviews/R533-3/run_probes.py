#!/usr/bin/env python3
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
from srp_arms import arm_srp
out=packet/'probes'; out.mkdir(exist_ok=True)
scratch=packet/'scratch/probes'
tree=Tree(CTRL,scratch/'build',scratch/'reuse',fw_gtest.Build(jobs=a.jobs))
failed=False
for n in (1,2):
    r=arm_srp(tree,root/'third_party/lwSRP',n,test=str(packet/'probe_lifecycle.cpp'))
    (out/f'if{n}.log').write_text(r.log)
    (out/f'if{n}.rc').write_text(str(r.rc)+'\n')
    print(f'independent probes interfaces={n} rc={r.rc}',flush=True)
    failed |= bool(r.rc)
raise SystemExit(int(failed))

#!/usr/bin/env python3
"""Build a separate checkpoint driver against the exact original compiled model archive."""
import concurrent.futures as cf, subprocess,sys
from pathlib import Path
T=Path('<scratch>')
def build(v):
 tree,point,arm=v; b=T/'meas/full'/tree/point/arm; n=b/'native'
 mk=(n/'Vsim.mk').read_text()
 mk=mk.replace('sim_main','checkpoint_main').replace(str(T/'clones'/tree/'tb/verilator/ctrl_service_budget/checkpoint_main.cpp'),str(T/'bin/checkpoint_main.cpp'))
 mk=mk.replace('default: Vsim','default: Vsim_checkpoint').replace('Vsim: $(VK_USER_OBJS)','Vsim_checkpoint: $(VK_USER_OBJS)')
 (n/'checkpoint.mk').write_text(mk)
 with (n/'checkpoint-build.log').open('w') as f:
  rc=subprocess.run(['make','-j16','-C',str(n),'-f','checkpoint.mk','Vsim_checkpoint'],stdout=f,stderr=subprocess.STDOUT).returncode
 return v,rc
jobs=[(t,p,a) for t in ('base','h4') for p in ('1x1','8x8-1if') for a in ('none','answering-ports')]
with cf.ThreadPoolExecutor(4) as pool:
 for row in pool.map(build,jobs): print(row,flush=True)

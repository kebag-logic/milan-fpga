#!/usr/bin/env python3
"""Build and run only the mailbox/loop and ADP suites, in independent scratch trees."""
import argparse
import concurrent.futures
import os
import sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--root',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args(); root=a.root.resolve(); packet=a.packet.resolve()
os.environ['TMPDIR']=str(packet/'scratch')
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build, ctrl_arms, fw_gtest
def run(name):
 out=packet/'scratch'/('native-'+name); out.mkdir(parents=True,exist_ok=True)
 tree=ctrl_build.Tree(ctrl_build.CTRL,out,out/'reuse',fw_gtest.Build(jobs=a.jobs))
 result=getattr(ctrl_arms,'arm_'+name)(tree)
 (packet/('native-'+name+'.log')).write_text(result.log)
 (packet/('native-'+name+'.rc')).write_text(str(result.rc)+'\n')
 return name,result.rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,['port','adp']))
for name,rc in results: print(name,rc)
sys.exit(int(any(rc for _,rc in results)))

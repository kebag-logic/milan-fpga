#!/usr/bin/env python3
"""Run the changed counter unit fixtures using exported production recipes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('packet',type=Path)
    ap.add_argument('--jobs',type=int,default=2)
    a=ap.parse_args();root=a.root.resolve();packet=a.packet.resolve()
    cases=[('tkdiag','tkdiag','VFLAGS','SRCS','sim_main.cpp',[]),
           ('crf-rx','crf_rx','VFLAGS','SRCS','sim_main.cpp',[]),
           ('rxmon-nx','avtp_rxmon','NXFLAGS','NXSRCS','sim_main_nx.cpp',[]),
           ('lockstep-1','avtp_rxmon','LSFLAGS','LSSRCS','sim_lockstep.cpp',['-GN_LISTENERS_P=1','-CFLAGS','-DN_TB=1']),
           ('lockstep-8','avtp_rxmon','LSFLAGS','LSSRCS','sim_lockstep.cpp',['-GN_LISTENERS_P=8','-CFLAGS','-DN_TB=8'])]
    def run(case):
        name,suite,fv,sv,cpp,extra=case
        d=root/'tb/verilator'/suite;work=packet/'scratch'/name;work.mkdir(parents=True,exist_ok=True)
        recipe=subprocess.check_output(['make','-j16','-s','--eval',f"review-print: ; @echo '$({fv})'; echo '$({sv})'",'review-print'],cwd=d,text=True).splitlines()
        flags=shlex.split(recipe[0]);flags[flags.index('-j')+1]='2'
        flags=[f.replace('../../../',str(root)+'/') for f in flags]
        sources=[str((d/s).resolve()) for s in shlex.split(recipe[1])]
        argv=[os.environ['VERILATOR'],*flags,*extra,'--Mdir',str(work/'obj'),*sources,str(d/cpp),'-o','unit']
        start=time.monotonic()
        with (packet/'receipts'/f'{name}.build.log').open('w') as log:
            result=subprocess.run(argv,cwd=work,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode==0:
            with (packet/'receipts'/f'{name}.run.log').open('w') as log:
                result=subprocess.run([str(work/'obj/unit')],cwd=work,stdout=log,stderr=subprocess.STDOUT)
        r=dict(name=name,argv=argv,rc=result.returncode,elapsed_s=round(time.monotonic()-start,3))
        (packet/'receipts'/f'{name}.json').write_text(json.dumps(r,indent=2)+'\n')
        (packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
        print(name,result.returncode,flush=True);return r
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:results=list(pool.map(run,cases))
    (packet/'receipts/unit-results.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(any(r['rc'] for r in results))

if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Build focused unit harnesses from their Makefile exports in isolated scratch."""
import argparse, pathlib, subprocess, os, shlex, time
p=argparse.ArgumentParser();p.add_argument('repo',type=pathlib.Path);p.add_argument('packet',type=pathlib.Path);a=p.parse_args()
repo=a.repo.resolve(); packet=a.packet.resolve()
for name,sub,flagsvar,srcsvar,cpp,extra in [
 ('tkdiag','tkdiag','VFLAGS','SRCS','sim_main.cpp',[]),
 ('crf-rx','crf_rx','VFLAGS','SRCS','sim_main.cpp',[]),
 ('rxmon-nx','avtp_rxmon','NXFLAGS','NXSRCS','sim_main_nx.cpp',[]),
 ('lockstep-1','avtp_rxmon','LSFLAGS','LSSRCS','sim_lockstep.cpp',['-GN_LISTENERS_P=1','-CFLAGS','-DN_TB=1']),
 ('lockstep-8','avtp_rxmon','LSFLAGS','LSSRCS','sim_lockstep.cpp',['-GN_LISTENERS_P=8','-CFLAGS','-DN_TB=8'])]:
    suite=repo/'tb/verilator'/sub; work=packet/'scratch'/name; work.mkdir(parents=True,exist_ok=True)
    recipe=subprocess.check_output(['make','-j16','-s','--eval',f"review-print: ; @echo '$({flagsvar})'; echo '$({srcsvar})'",'review-print'],cwd=suite,text=True).splitlines()
    flags=shlex.split(recipe[0]); flags[flags.index('-j')+1]='2'
    flags=[f.replace('../../../',str(repo)+'/') for f in flags]
    sources=[str((suite/f).resolve()) for f in shlex.split(recipe[1])]
    cmd=[os.environ.get('VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),*flags,*extra,'--Mdir',str(work/'obj'),*sources,str(suite/cpp),'-o','review-unit']
    with (packet/'receipts'/f'{name}.build.log').open('w') as log:
        r=subprocess.run(cmd,cwd=work,stdout=log,stderr=subprocess.STDOUT)
    if r.returncode: raise SystemExit(r.returncode)
    with (packet/'receipts'/f'{name}.run.log').open('w') as log:
        r=subprocess.run([str(work/'obj/review-unit')],cwd=work,stdout=log,stderr=subprocess.STDOUT)
    (packet/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
    print(name,r.returncode,flush=True)
    if r.returncode: raise SystemExit(r.returncode)

#!/usr/bin/env python3
"""Reproduce through public input faces; no RTL edits or internal-state forcing."""
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

p=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
head='57fb7dd21d316ce49c305c22812de5c16d6770f6'
sim=os.environ.get('REVIEW_SIM','<tools>/pinned-verilator-5.050/verilator')
assert 'Verilator 5.050' in subprocess.check_output([sim,'--version'],text=True)
tree=p/'scratch'/'parked-wire-probe'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
suite=tree/'tb'/'srp_top'
shutil.copyfile(p/'parked-wire-probe.cpp',suite/'parked-wire-probe.cpp')
mf=suite/'Makefile'
mf.write_text(mf.read_text().replace('--build -j 0','--build -j 2').replace('CPP  = sim_main.cpp','CPP  = parked-wire-probe.cpp'))
cmd=['make','-j4','-C',str(suite),'VERILATOR='+sim,'RUN_ARGS=share']
with (p/'parked-wire-probe.log').open('w') as log:
    log.write('Exact RTL '+head+'; only the test entry point is replaced.\n');log.flush()
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'parked-wire-probe.rc').write_text(str(rc)+'\n')
print('probe exit',rc)
print('\n'.join((p/'parked-wire-probe.log').read_text().splitlines()[-12:]))

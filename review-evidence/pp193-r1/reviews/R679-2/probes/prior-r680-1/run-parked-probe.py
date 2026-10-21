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
head='7b424cdfe111a426f00517ff471246b4b9650726'
sim=os.environ.get('REVIEW_SIM','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
assert 'Verilator 5.050' in subprocess.check_output([sim,'--version'],text=True)
tree=p/'scratch'/'parked-probe'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
suite=tree/'tb'/'srp_stream_fsms'
shutil.copyfile(p/'parked-probe.cpp',suite/'parked-probe.cpp')
mf=suite/'Makefile'
mf.write_text(mf.read_text().replace('--build -j 0','--build -j 8').replace('CPP  = sim_main.cpp','CPP  = parked-probe.cpp'))
cmd=['make','-j16','-C',str(suite),'VERILATOR='+sim,'RUN_ARGS=suite']
with (p/'parked-probe.log').open('w') as log:
    log.write('Exact RTL '+head+'; only the test entry point is replaced.\n');log.flush()
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'parked-probe.rc').write_text(str(rc)+'\n')
print('probe exit',rc)
print('\n'.join((p/'parked-probe.log').read_text().splitlines()[-12:]))

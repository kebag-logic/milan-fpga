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
head='6ddfcda4c3170b8f463c8623833f7541ca8c1faf'
sim=os.environ.get('REVIEW_SIM','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
assert 'Verilator 5.050' in subprocess.check_output([sim,'--version'],text=True)
tree=p/'scratch'/'handover-join-control'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
suite=tree/'tb'/'srp_stream_fsms'
shutil.copyfile(p/'handover-pairs.cpp',suite/'handover-pairs.cpp')
mf=suite/'Makefile'
mf.write_text(mf.read_text().replace('--build -j 0','--build -j 4').replace('CPP  = sim_main.cpp','CPP  = handover-pairs.cpp'))
rtl=tree/'hdl/srp/KL_srp_listener_fsm.sv'
before=rtl.read_text()
a="A_VP_C, A_AA_C, A_AP_C: m = {1'b1, sj_w};"
assert before.count(a)==1
after=before.replace(a,"A_VP_C, A_AA_C, A_AP_C: m = {1'b0, sj_w};")
rtl.write_text(after)
import difflib
(p/'handover-join-control.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/hdl/srp/KL_srp_listener_fsm.sv',tofile='b/hdl/srp/KL_srp_listener_fsm.sv')))
cmd=['make','-j16','-C',str(suite),'VERILATOR='+sim,'RUN_ARGS=suite']
with (p/'handover-join-control.log').open('w') as log:
    log.write('Fault control of RTL '+head+'; only the test entry point is replaced.\n');log.flush()
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'handover-join-control.rc').write_text(str(rc)+'\n')
print('probe exit',rc)
print('\n'.join((p/'handover-join-control.log').read_text().splitlines()[-12:]))

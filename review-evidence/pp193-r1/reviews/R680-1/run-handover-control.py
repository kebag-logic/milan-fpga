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
tree=p/'scratch'/'handover-control'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
suite=tree/'tb'/'srp_stream_fsms'
shutil.copyfile(p/'handover-pairs.cpp',suite/'handover-pairs.cpp')
mf=suite/'Makefile'
mf.write_text(mf.read_text().replace('--build -j 0','--build -j 4').replace('CPP  = sim_main.cpp','CPP  = handover-pairs.cpp'))
rtl=tree/'hdl/srp/KL_srp_listener_fsm.sv'
before=rtl.read_text()
a="rla_pend_r[t] <= rla_pend_r[take_src_w[t]] || la_rx_app_w;"
b="per_pend_r[t] <= per_pend_r[take_src_w[t]] || periodic_tick_i;"
assert before.count(a)==1 and before.count(b)==1
after=before.replace(a,"rla_pend_r[t] <= 1'b0;").replace(b,"per_pend_r[t] <= 1'b0;")
rtl.write_text(after)
import difflib
(p/'handover-control.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/hdl/srp/KL_srp_listener_fsm.sv',tofile='b/hdl/srp/KL_srp_listener_fsm.sv')))
cmd=['make','-j16','-C',str(suite),'VERILATOR='+sim,'RUN_ARGS=suite']
with (p/'handover-control.log').open('w') as log:
    log.write('Fault control of RTL '+head+'; only the test entry point is replaced.\n');log.flush()
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'handover-control.rc').write_text(str(rc)+'\n')
print('probe exit',rc)
print('\n'.join((p/'handover-control.log').read_text().splitlines()[-12:]))

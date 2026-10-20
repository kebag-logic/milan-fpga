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
tree=p/'scratch'/'wire-witness'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
suite=tree/'tb'/'srp_top'
cpp=suite/'sim_main.cpp'
text=cpp.read_text()
for tag,decl in [('ready','DECL_READY'),('ready-failed','DECL_ASKFAIL')]:
    anchor=f'CHECK(h.ls_decl(0) == DECL_READY && h.ls_decl(1) == {decl} && f == exp,'
    assert text.count(anchor)==1
    text=text.replace(anchor,f'dump("{tag}", f);\n    '+anchor)
cpp.write_text(text)
mf=suite/'Makefile'
mf.write_text(mf.read_text().replace('--build -j 0','--build -j 4'))
cmd=['make','-j16','-C',str(suite),'VERILATOR='+sim,'RUN_ARGS=share']
with (p/'wire-witness.log').open('w') as log:
    log.write('Exact RTL '+head+'; only the test entry point is replaced.\n');log.flush()
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'wire-witness.rc').write_text(str(rc)+'\n')
print('probe exit',rc)
print('\n'.join((p/'wire-witness.log').read_text().splitlines()[-12:]))

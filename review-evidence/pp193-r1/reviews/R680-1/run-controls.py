#!/usr/bin/env python3
"""Run only new shared-stream and reanchored owed-Leave mutation controls."""
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile

p=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
head='6ddfcda4c3170b8f463c8623833f7541ca8c1faf'
sim=os.environ.get('REVIEW_SIM','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
assert 'Verilator 5.050' in subprocess.check_output([sim,'--version'],text=True)
tree=p/'scratch'/'controls'
tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=source))) as a:
    a.extractall(tree,filter='data')
for mf in (tree/'tb').glob('*/Makefile'):
    mf.write_text(mf.read_text().replace('--build -j 0','--build -j 3'))
names=['settle-compare-dropped','rider-not-quiet','teardown-applies-lv','handover-drops-state',
       'withdraw-ignores-riders','teardown-keeps-declaring','group-order-reversed',
       'rider-settle-hands-over','type-not-combined','handover-forgets-walk-mark',
       'settle-parks-shared-stream','group-op-during-settle','lo-not-owed','lost-txla',
       'park-never-retires','park-retires-on-txla','rebind-abandons-leave',
       'reprobe-abandons-leave','reprobe-parks-own-stream','unrecorded-applicant-owes',
       'declaration-not-held']
out=p/'controls'
cmd=[sys.executable,str(tree/'tb/srp_top/mutants.py'),'--jobs','4','--only',
     ','.join('listener-'+n for n in names),'--output',str(out)]
env=dict(os.environ,VERILATOR=sim,MAKEFLAGS='-j16',TMPDIR=str(p/'scratch'))
with (p/'controls.log').open('w') as log:
    log.write('source '+head+'\ncommand '+repr(cmd)+'\n');log.flush()
    rc=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'controls.rc').write_text(str(rc)+'\n')
print('controls exit',rc)
print('\n'.join((p/'controls.log').read_text().splitlines()[-8:]))

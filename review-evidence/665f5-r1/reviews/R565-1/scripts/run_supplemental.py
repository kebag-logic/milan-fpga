#!/usr/bin/env python3
"""Focused image/debug and mutation checks, concurrent with mailbox co-simulation."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import io

p=argparse.ArgumentParser();p.add_argument('checkout',type=Path);p.add_argument('packet',type=Path)
p.add_argument('--verilator',required=True);args=p.parse_args()
root=args.checkout.resolve();packet=args.packet.resolve();scratch=packet/'scratch';receipts=packet/'receipts'
identity=subprocess.check_output([args.verilator,'--version'],text=True)
assert identity.startswith('Verilator 5.050 '),identity
(receipts/'simulator-identity.log').write_text(identity)
mbx=scratch/'mailbox';mbx.mkdir(exist_ok=True)
archive=subprocess.check_output(['git','archive','HEAD','tb/verilator/mbx','tb/common'],cwd=root)
with tarfile.open(fileobj=io.BytesIO(archive)) as source:source.extractall(mbx,filter='data')
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(scratch)}
def images():
 sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
 import aecp_arms
 from ctrl_build import Tree, CTRL
 import fw_gtest
 tree=Tree(CTRL,scratch/'supplemental-images',scratch/'reuse-images',fw_gtest.Build(jobs=4))
 outcomes=[aecp_arms.image_arm(tree,c) for c in sorted((root/'configs').glob('endstation_*.yaml'))]
 outcomes.append(aecp_arms.core_arm(tree,root/'configs/endstation_ax7101_1x1_tdm8.yaml',mode='debug'))
 (receipts/'images-debug.log').write_text('\n'.join(o.arm+'\n'+o.log for o in outcomes))
 rc=int(any(o.rc for o in outcomes));(receipts/'images-debug.rc').write_text(str(rc)+'\n')
 return 'images-debug',rc
def mutations():
 # A separate interpreter keeps the independent campaign's globals isolated.
 code='''import sys
from pathlib import Path
root,out=map(Path,sys.argv[1:]);sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import aecp_mutants
aecp_mutants.controls()
names={'descriptor-last-byte','scalar-refusal-reports-request','counter-spacing-short','app-notice-overtakes-unbind','nvm-hole-accepted'}
aecp_mutants.DEFECTS=tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
assert len(aecp_mutants.DEFECTS)==5
aecp_mutants.controls=lambda:None
raise SystemExit(aecp_mutants.campaign(out,jobs=4))
'''
 return run('selected-mutations',[sys.executable,'-B','-c',code,str(root),str(scratch/'selected-mutations')])
def run(name,argv):
 with (receipts/(name+'.log')).open('w') as log:
  log.write('command: '+repr(argv)+'\n');log.flush()
  try:rc=subprocess.run(argv,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=540).returncode
  except subprocess.TimeoutExpired:rc=124;log.write('\nTIMEOUT\n')
 (receipts/(name+'.rc')).write_text(str(rc)+'\n');return name,rc
def mailbox():
 return run('mailbox-cosim',['make','-j16','-C',str(mbx/'tb/verilator/mbx'),'run-cosim','ROOT='+str(root),
                           'VBUILD_JOBS=8','VERILATOR='+args.verilator])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(f) for f in (images,mutations,mailbox)]
 results=[f.result() for f in futures]
for name,rc in results:print(name,'rc',rc)
raise SystemExit(any(rc for name,rc in results))

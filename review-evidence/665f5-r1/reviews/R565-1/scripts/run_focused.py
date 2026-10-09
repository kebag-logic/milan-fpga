#!/usr/bin/env python3
"""Run independent focused jobs, joined by this foreground process; no source edits."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('packet',type=Path)
p.add_argument('--only',nargs='+')
args=p.parse_args()
root=args.checkout.resolve(); packet=args.packet.resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'
probe=scratch/'probes';probe.mkdir(parents=True,exist_ok=True)
(probe/'test_aecp.cpp').write_text((root/'sw/firmware/ctrl/test/test_aecp.cpp').read_text()+'\n'+(packet/'scripts/probe_cases.cpp').read_text())
worker=probe/'worker.py'
worker.write_text('''import sys
from pathlib import Path
root,out,probe=map(Path,sys.argv[1:])
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import aecp_arms
from ctrl_build import Tree,CTRL
import fw_gtest
aecp_arms.HERE=probe
tree=Tree(CTRL,out,out/'reuse',fw_gtest.Build(jobs=4))
result=aecp_arms.core_arm(tree,root/'configs/endstation_ax7101_1x1_tdm8.yaml',2,'core','Core.R565*')
print(result.log)
raise SystemExit(result.rc)
''')
jobs={
 'app-if1':[sys.executable,'-B','sw/firmware/ctrl/test/aecp_arms.py','--app','--interfaces','1','--output',str(scratch/'app-if1')],
 'app-if2':[sys.executable,'-B','sw/firmware/ctrl/test/aecp_arms.py','--app','--interfaces','2','--output',str(scratch/'app-if2')],
 'independent-probes':[sys.executable,'-B',str(worker),str(root),str(scratch/'probe-build'),str(probe)],
 'mailbox-generator':[sys.executable,'-B','sw/mailbox/gen_mailbox.py','--check'],
 'docs-check':[sys.executable,'-B','scripts/docs_check.py'],
}
if args.only: jobs={name:argv for name,argv in jobs.items() if name in args.only}
def run(item):
 name,argv=item
 with (receipts/(name+'.log')).open('w') as log:
  log.write('command: '+ ' '.join(argv)+'\n');log.flush()
  try:
   result=subprocess.run(argv,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=540,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(scratch)})
   rc=result.returncode
  except subprocess.TimeoutExpired: rc=124;log.write('\nTIMEOUT\n')
 (receipts/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,'rc',rc,flush=True)
 return name,rc
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(run,jobs.items()))
raise SystemExit(any(rc for name,rc in results if name!='independent-probes'))

#!/usr/bin/env python3
"""Focused read-only contract and documentation checks."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
args=p.parse_args()
repo,packet=args.repo.resolve(),args.packet.resolve()
env=dict(os.environ,TMPDIR=str(packet/'scratch'))
commands={
 'mailbox-generator':[sys.executable,'sw/mailbox/gen_mailbox.py','--check','--crosscheck','--selftest'],
 'submodule-docs':[sys.executable,'scripts/check_submodule_docs.py'],
 'docs-check':[sys.executable,'scripts/docs_check.py'],
 'doc-paths':[sys.executable,'scripts/check_doc_paths.py'],
 'diagram':[sys.executable,'docs/diagrams/submodule_boundaries.gen.py','--check'],
}
def run(item):
 name,argv=item
 res=subprocess.run(argv,cwd=repo,env=env,capture_output=True,text=True,timeout=500)
 (packet/(name+'.log')).write_text(res.stdout+res.stderr)
 (packet/(name+'.rc')).write_text(str(res.returncode)+'\n')
 return {'name':name,'command':argv,'rc':res.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 rows=list(pool.map(run,commands.items()))
(packet/'static-results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
sys.exit(any(r['rc'] for r in rows))

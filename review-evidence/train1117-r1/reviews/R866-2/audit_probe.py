#!/usr/bin/env python3
"""Verify the audit generator, detect its parent output, and restore exact bytes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
target=root/'docs/DOCUMENTATION_AUDIT.md';before=target.read_bytes()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
rows=[]
def run(args,want):
 r=subprocess.run(args,cwd=root,env=env,capture_output=True,text=True)
 rows.append({'command':args,'rc':r.returncode,'expected':want,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==want,(args,r.returncode,r.stdout,r.stderr)
 return r
try:
 for _ in range(2):
  run([sys.executable,'-B','scripts/docs_inventory.py','--write'],0)
  assert target.read_bytes()==before,'--write changed the committed bytes'
 run([sys.executable,'-B','scripts/docs_inventory.py','--check'],0)
 target.write_bytes(subprocess.check_output(['git','show','73272666:docs/DOCUMENTATION_AUDIT.md'],cwd=root))
 run([sys.executable,'-B','scripts/docs_inventory.py','--check'],1)
 run([sys.executable,'-B','scripts/docs_inventory.py','--write'],0)
 assert target.read_bytes()==before,'--write did not heal the parent output exactly'
 run([sys.executable,'-B','scripts/docs_inventory.py','--check'],0)
finally:
 target.write_bytes(before)
 (packet/'audit-probe.json').write_text(json.dumps({'sha256':hashlib.sha256(before).hexdigest(),'runs':rows,'restored':target.read_bytes()==before},indent=2)+'\n')
print('PASS: repeated --write byte-identical; parent audit rejected; --write healed exactly; original bytes restored')

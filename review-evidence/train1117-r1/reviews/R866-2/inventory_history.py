#!/usr/bin/env python3
"""Reconstruct inventory inputs at historical heads without altering checkout."""
import contextlib
import difflib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).resolve(); packet=Path(sys.argv[2]).resolve()
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('inventory',root/'scripts/docs_inventory.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
objects=Path(git('rev-parse','--git-path','objects').decode().strip()).resolve()
rows=[]
for rev in ['544fd72c','8f6fbb84','73272666','b1f1161b']:
 sha=git('rev-parse',rev).decode().strip();dest=packet/'scratch'/('inventory-'+rev);dest.mkdir(exist_ok=True)
 subprocess.run(['git','init','-q',str(dest)],check=True)
 (dest/'.git/objects/info/alternates').write_text(str(objects)+'\n')
 subprocess.run(['git','-C',str(dest),'read-tree',sha],check=True)
 paths=git('ls-tree','-r','--name-only',sha).decode().splitlines()
 for name in paths:
  if mod.is_document(name) or name in ['.gitmodules','scripts/docs_inventory.json']:
   out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(git('show',sha+':'+name))
 text=mod.generate(dest);committed=(dest/mod.OUTPUT).read_text()
 with contextlib.redirect_stdout(io.StringIO()) as out: rc=mod.main(['--check'],dest)
 changed=[line for line in difflib.unified_diff(committed.splitlines(),text.splitlines(),n=0) if line.startswith(('+','-')) and not line.startswith(('+++','---'))]
 rows.append({'head':sha,'generator_blob':git('rev-parse',sha+':scripts/docs_inventory.py').decode().strip(),'audit_blob':git('rev-parse',sha+':'+mod.OUTPUT).decode().strip(),'rc':rc,'current':next(x for x in text.splitlines() if x.startswith('| current |')),'diff':changed,'diagnostic':out.getvalue()})
 print(rev,'rc',rc,'changed rows',len(changed),'ctrl_reboot tracked', 'tb/verilator/ctrl_reboot/README.md' in paths)
(packet/'inventory-history.json').write_text(json.dumps(rows,indent=2)+'\n')
assert [r['rc'] for r in rows]==[0,1,1,0]
assert rows[0]['audit_blob']==rows[1]['audit_blob']==rows[2]['audit_blob']
assert len({r['generator_blob'] for r in rows})==1
print('PASS: #934 fresh; step-9 inherited its audit unchanged and stale; parent still same stale blob; delta heals it')

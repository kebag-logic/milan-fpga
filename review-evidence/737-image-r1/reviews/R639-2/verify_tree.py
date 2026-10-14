#!/usr/bin/env python3
"""Compare actual tracked bytes, modes, index entries and submodule gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
def git(*args):return subprocess.check_output(['git','--no-replace-objects',*args],cwd=root)
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='18f2df92b13cb3f4036b073ed76940187bf10487'
assert tree=='21c293548a85cfb4a9bd7dfd7c1e990c103d18bd'
expected={}; failures=[]; links=[];count=0
for line in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t');mode,kind,oid=meta.decode().split();name=os.fsdecode(path)
 expected[name]=(mode,oid)
 if kind=='commit':
  present=(root/name/'.git').exists()
  actual=subprocess.check_output(['git','-C',str(root/name),'rev-parse','HEAD'],text=True).strip() if present else None
  links.append({'path':name,'gitlink':oid,'initialized':present,'actual_head':actual})
  if present and actual!=oid:failures.append(name+': submodule head')
  continue
 p=root/name
 data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
 actual_mode='120000' if p.is_symlink() else ('100755' if p.stat().st_mode&0o111 else '100644')
 actual_oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if actual_mode!=mode or actual_oid!=oid:failures.append(name+': raw bytes or mode')
 count+=1
index={}
for line in git('ls-files','--stage','-z').split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t');mode,oid,stage=meta.decode().split();assert stage=='0'
 index[os.fsdecode(path)]=(mode,oid)
assert index==expected
diff=git('diff','--no-ext-diff','--no-textconv','fa7347fc59173f90e4feec2df207692e6e6e72ec..HEAD')
changed=git('diff','--name-only','fa7347fc59173f90e4feec2df207692e6e6e72ec..HEAD').decode().splitlines()
result={'head':head,'tree':tree,'raw_blob_bytes_and_modes_verified':count,'index_matches_head':True,'failures':failures,'submodules':links,'full_diff_sha256':hashlib.sha256(diff).hexdigest(),'changed_paths':changed,'workflow_changes':[p for p in changed if p.startswith('.github/workflows/')],'status':git('status','--porcelain').decode()}
(out/'final-tree.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert not failures and not result['status'] and not result['workflow_changes']

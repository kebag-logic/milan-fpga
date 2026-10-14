#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and initialized submodules against HEAD."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve(); packet=Path(__file__).resolve().parent
def git(path,*args):
 return subprocess.check_output(['git','--no-replace-objects',*args],cwd=path)
def verify(path,commit):
 tree=git(path,'ls-tree','-rz','--full-tree',commit)
 indexed=git(path,'ls-files','--stage','-z')
 expected=[]; files=0; links=[]; errors=[]
 for row in tree.split(b'\0'):
  if not row:continue
  metadata,name=row.split(b'\t',1); mode,kind,oid=metadata.split()
  expected.append(mode+b' '+oid+b' 0\t'+name+b'\0')
  file=path/os.fsdecode(name)
  if mode==b'160000':
   links.append((os.fsdecode(name),oid.decode()));continue
  info=file.lstat()
  if mode==b'120000':
   data=os.fsencode(os.readlink(file)); actual_mode=b'120000' if stat.S_ISLNK(info.st_mode) else b'wrong'
  else:
   data=file.read_bytes();actual_mode=(b'100755' if info.st_mode&0o111 else b'100644') if stat.S_ISREG(info.st_mode) else b'wrong'
  measured=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  if measured!=oid or actual_mode!=mode: errors.append(os.fsdecode(name))
  files+=1
 assert indexed==b''.join(expected),'index differs from tree'
 assert not errors,errors
 return {'head':commit,'tracked_blobs':files,'index_matches_tree':True,'byte_mode_differences':errors,'gitlinks':dict(links)}
head=git(root,'rev-parse','HEAD').decode().strip()
assert head=='e6b86814e6844ef61ba46a867a0fdbfbb925cceb'
result={'superproject':verify(root,head),'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'submodules':{}}
for name,pin in result['superproject']['gitlinks'].items():
 path=root/name
 if not (path/'.git').exists():
  result['submodules'][name]={'initialized':False,'gitlink':pin};continue
 assert git(path,'rev-parse','HEAD').decode().strip()==pin
 result['submodules'][name]=verify(path,pin)
 assert not git(path,'status','--porcelain=v1'),name
assert all('tracked_blobs' in result['submodules'][name] for name in ('gptp-processor','protocol-processor','third_party/tsn-c-stack','third_party/verilog-axis'))
assert not git(root,'status','--porcelain=v1')
base='fa7347fc59173f90e4feec2df207692e6e6e72ec'
changed=git(root,'diff','--name-only',base,head).decode().splitlines()
assert not any(n.startswith(('.github/','hdl/','sw/','tb/','third_party/')) or n in ('protocol-processor','gptp-processor') for n in changed)
result['changed_paths']=changed
result['full_diff_sha256']=hashlib.sha256(git(root,'diff','--no-ext-diff','--no-textconv',base,head)).hexdigest()
result['worktree_status']='clean'
(packet/'final-tree.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: tracked bytes, modes, index, all gitlinks and four initialized submodule trees; no workflow/product source changes.')

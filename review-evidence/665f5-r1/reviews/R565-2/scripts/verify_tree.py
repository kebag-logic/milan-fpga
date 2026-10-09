#!/usr/bin/env python3
"""Prove actual tracked bytes, kinds, modes, index and required gitlinks."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

p=argparse.ArgumentParser();p.add_argument('checkout',type=Path);args=p.parse_args()
root=args.checkout.resolve();env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
head='0ded1f269a44d107498f177c8276665656e07d30'
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],env=env)
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='634c2f44c08cc5f976ca74634daec54273de66b4'
def verify(path,commit):
 expected=git(path,'ls-tree','-rz',commit).split(b'\0')
 index=git(path,'ls-files','--stage','-z').split(b'\0')
 expected_index=[];count=0;links=[];errors=[]
 for row in expected:
  if not row:continue
  metadata,name=row.split(b'\t',1);mode,kind,oid=metadata.split()
  expected_index.append(mode+b' '+oid+b' 0\t'+name)
  if kind==b'commit':links.append((os.fsdecode(name),oid.decode()));continue
  file=path/os.fsdecode(name)
  try:
   s=file.lstat();symlink=stat.S_ISLNK(s.st_mode)
   actual_mode=b'120000' if symlink else b'100755' if s.st_mode&0o111 else b'100644'
   data=os.fsencode(os.readlink(file)) if symlink else file.read_bytes()
   sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if actual_mode!=mode or sha!=oid:errors.append(os.fsdecode(name))
  except OSError:errors.append(os.fsdecode(name))
  count+=1
 assert not errors,errors
 assert sorted(expected_index)==sorted(x for x in index if x), 'index differs from pinned tree'
 print(str(path.relative_to(root)) or '.',commit,'PASS',count,'tracked blobs, bytes/modes/index')
 return links
links=verify(root,head)
for name,oid in links:
 print('gitlink',name,oid)
 if name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP'):
  sub=root/name
  assert git(sub,'rev-parse','HEAD').decode().strip()==oid
  assert git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
  verify(sub,oid)
print('PASS exact-head tracked identity and required submodules')

#!/usr/bin/env python3
"""Verify raw tracked bytes, file kinds/modes, index entries, and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
repo=Path(sys.argv[1])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
expected='62477be4cb90336ca9b59ae7ab8377546e72557a'
def git(root,*args):
 return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,commit):
 assert git(root,'rev-parse','HEAD').decode().strip()==commit
 entries={}
 for row in git(root,'ls-tree','-rz',commit).split(b'\0'):
  if not row: continue
  facts,name=row.split(b'\t',1)
  mode,kind,oid=facts.split()
  entries[name]=(mode,oid)
  if kind==b'commit': continue
  p=root/os.fsdecode(name)
  st=p.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(st.st_mode),name
   data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode&0o111)==(mode==b'100755'),name
   data=p.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==oid,os.fsdecode(name)
 index={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row: continue
  facts,name=row.split(b'\t',1)
  mode,oid,stage=facts.split()
  assert stage==b'0',name
  index[name]=(mode,oid)
 assert index==entries,'index differs from commit tree'
 print('PASS',root.name,commit,len(entries),'tracked entries: bytes, modes, kinds and index')
 return entries
entries=verify(repo,expected)
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()=='568d04b01d0b137adaed668afb6a8d525a3c8a12'
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'):
 mode,pin=entries[os.fsencode(name)]
 assert mode==b'160000'
 verify(repo/name,pin.decode())
print('PASS exact parent tree and all required gitlinks; optional lwSRP verified too; external is intentionally uninitialized')

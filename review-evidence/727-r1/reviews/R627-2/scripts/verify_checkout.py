#!/usr/bin/env python3
"""Verify raw tracked bytes/modes/index and required gitlinks. Usage: verify_checkout.py CHECKOUT PACKET."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root, packet=map(lambda p:Path(p).resolve(),sys.argv[1:])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):
 return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def verify(repo, rev):
 entries={}
 for entry in git(repo,'ls-tree','-rz',rev).split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1)
  mode,kind,oid=meta.decode().split()
  entries[name]=(mode,kind,oid)
 index={}
 for entry in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1)
  mode,oid,stage=meta.decode().split()
  assert stage=='0', (name,'unmerged index')
  assert name not in index
  index[name]=(mode,oid)
 assert index=={name:(mode,oid) for name,(mode,kind,oid) in entries.items()}
 count=0
 for name,(mode,kind,oid) in entries.items():
  if kind=='commit':continue
  path=repo/os.fsdecode(name)
  info=path.lstat()
  if mode=='120000':
   assert stat.S_ISLNK(info.st_mode), name
   data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(info.st_mode),name
   assert bool(info.st_mode&stat.S_IXUSR)==(mode=='100755'),name
   data=path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert actual==oid,(name,actual,oid)
  count+=1
 assert not git(repo,'diff','--cached','--name-only',rev).strip()
 flags=git(repo,'ls-files','-v','-z').split(b'\0')
 assert not any(x and (x[:1].islower() or x[:1]==b'S') for x in flags)
 return {'tracked_blobs_verified':count,'index_entries_verified':len(index),'raw_modes_and_bytes_match':True,'index_matches':True,'hidden_index_flags':False,'gitlinks':{os.fsdecode(name):oid for name,(mode,kind,oid) in entries.items() if kind=='commit'}}
head='61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3'
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='8fd4dbd4f35e3892f7df8f2e404302e3658d443d'
assert subprocess.run(['git','-C',str(root),'symbolic-ref','-q','HEAD'],env=env,stdout=subprocess.DEVNULL).returncode==1
result={'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'parent':verify(root,head),'required_submodules':{}}
for name in ['third_party/verilog-axis','protocol-processor','gptp-processor']:
 pin=result['parent']['gitlinks'][name]
 sub=root/name
 assert git(sub,'rev-parse','HEAD').decode().strip()==pin
 assert (sub/'.git').is_file() and not sub.is_symlink()
 result['required_submodules'][name]={'head':pin,**verify(sub,pin)}
result['status_porcelain']=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status_porcelain']
(packet/'receipts/checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

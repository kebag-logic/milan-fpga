#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, indexes and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(cwd,*args):return subprocess.check_output(['git','-C',str(cwd),*args],env=env)
required=['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']
def verify(cwd,rev):
 raw=git(cwd,'ls-tree','-rz',rev); entries=[];errors=[];links={}
 for record in raw.split(b'\0'):
  if not record:continue
  prefix,path=record.split(b'\t',1);mode,kind,oid=prefix.decode().split();name=os.fsdecode(path);target=cwd/name
  entries.append(mode.encode()+b' '+oid.encode()+b' 0\t'+path+b'\0')
  if mode=='160000':links[name]=oid;continue
  try:
   st=target.lstat()
   if mode=='120000':
    assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(target))
   else:
    assert stat.S_ISREG(st.st_mode)
    assert bool(st.st_mode&0o111)==(mode=='100755')
    data=target.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   assert actual==oid
  except (AssertionError,OSError):errors.append(name)
 index=git(cwd,'ls-files','--stage','-z')
 assert index==b''.join(entries),'index differs from pinned tree'
 assert not errors,errors
 return {'head':rev,'tracked_entries':len(entries),'blob_or_mode_mismatches':errors,'index_exact':True,'gitlinks':links}
head=git(root,'rev-parse','HEAD').decode().strip();assert head=='b1f1161b0f72e6066f60c7e0fa5ba399e185493d'
result={'superproject':verify(root,head),'submodules':{}}
for name in required:
 pin=result['superproject']['gitlinks'][name];sub=root/name
 assert (sub/'.git').exists()
 assert git(sub,'rev-parse','HEAD').decode().strip()==pin
 result['submodules'][name]=verify(sub,pin)
result['tree']=git(root,'rev-parse','HEAD^{tree}').decode().strip()
assert result['tree']=='c84aa1e1d12890b82c806a370416a3b9aecbe902'
result['status']=git(root,'status','--porcelain=v1').decode()
assert not result['status']
(packet/'final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: head/tree, tracked bytes/modes, exact indexes and five required submodule pins; clean checkout')

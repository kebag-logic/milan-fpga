#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index, gitlinks, and delta scope."""
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp
import sys

repo=Path(sys.argv[1]).resolve()
def git(*args):
    return sp.check_output(['git',*args],cwd=repo)
head='55852269db3554900d2b71e6f9a7b153cff69e14'
assert git('rev-parse','HEAD').decode().strip()==head
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert tree=='64ee38ee54fec8de8fb847df31e54d087a7b50ef'
expected={}
links=[]
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not entry: continue
    meta,path=entry.split(b'\t',1)
    mode,kind,oid=meta.decode().split()
    name=path.decode()
    expected[name]=(mode,oid)
    if mode=='160000':
        links.append({'path':name,'gitlink':oid})
        continue
    p=repo/name
    data=os.readlink(p).encode() if mode=='120000' else p.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==oid,name
    actual_mode='120000' if p.is_symlink() else ('100755' if p.stat().st_mode&0o111 else '100644')
    assert actual_mode==mode,name
index={}
for entry in git('ls-files','-sz').split(b'\0'):
    if not entry: continue
    meta,path=entry.split(b'\t',1)
    mode,oid,stage=meta.decode().split()
    assert stage=='0'
    index[path.decode()]=(mode,oid)
assert index==expected
production={}
for base in ('715589c1','61a504ee'):
    production[base]=git('diff','--name-only',base+'..HEAD','--','src','include').decode().splitlines()
    assert not production[base]
result={'head':head,'tree':tree,'tracked_blobs_checked':len(expected)-len(links),'bytes_modes_index_match':True,'gitlinks':links,'production_changes':production,'status':git('status','--porcelain=v1').decode(),'delta_paths':git('diff','--name-only','61a504ee..HEAD').decode().splitlines()}
print(json.dumps(result,indent=2))

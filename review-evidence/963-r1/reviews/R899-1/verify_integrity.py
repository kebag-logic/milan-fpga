#!/usr/bin/env python3
"""Prove checkout bytes, modes and index independently of status flags."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
expected='4cca956932073b3f704f12f81c53f2934cfa215c'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(path,*args):
    return subprocess.check_output(['git','-C',str(path),*args],env=env)
def inspect(path,revision):
    assert git(path,'rev-parse','HEAD').decode().strip()==revision
    records=git(path,'ls-tree','-rz',revision).split(b'\0')
    wanted={}
    count=0
    links=[]
    for line in records:
        if not line: continue
        meta,name=line.split(b'\t',1)
        mode,kind,oid=meta.split()
        wanted[name]=(mode,oid,b'0')
        p=path/os.fsdecode(name)
        if kind==b'commit':
            links.append((os.fsdecode(name),oid.decode()))
            continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),name
            actual=b'100755' if st.st_mode&0o111 else b'100644'
            assert actual==mode,(name,actual,mode)
            data=p.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest==oid,name
        count+=1
    actual={}
    for line in git(path,'ls-files','--stage','-z').split(b'\0'):
        if not line: continue
        meta,name=line.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert name not in actual,name
        actual[name]=(mode,oid,stage)
    assert wanted==actual,'index differs from commit tree'
    return dict(head=revision,tree=git(path,'rev-parse',revision+'^{tree}').decode().strip(),
                verified_blobs=count,index_entries=len(actual),gitlinks=links)
result=inspect(root,expected)
assert result['tree']=='2f4e963dcaf2e5739003fbd3059610fe2f2ee9b0'
result['submodules']={}
for path,pin in result['gitlinks']:
    if path=='external':
        result['optional_external']='uninitialized; gitlink retained; not used by these probes'
        continue
    result['submodules'][path]=inspect(root/path,pin)
print(json.dumps(result,indent=2))

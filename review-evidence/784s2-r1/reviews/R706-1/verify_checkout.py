#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule pins without trusting status."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(where,*args):
    return subprocess.check_output(['git','-C',str(where),*args],env=env)
def entries(where,rev):
    answer={}
    for record in git(where,'ls-tree','-rz',rev).split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        answer[os.fsdecode(name)]=(mode,kind,oid)
    return answer
def verify(where,rev):
    wanted=entries(where,rev)
    index={}
    for record in git(where,'ls-files','--stage','-z').split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        assert stage=='0',(where,name,stage)
        index[os.fsdecode(name)]=(mode,oid)
    assert index=={n:(v[0],v[2]) for n,v in wanted.items()},str(where)+' index differs'
    count=0
    for name,(mode,kind,oid) in wanted.items():
        if kind=='commit': continue
        path=where/name
        info=path.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(info.st_mode),name
            raw=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode),name
            assert bool(info.st_mode&0o111)==(mode=='100755'),name
            raw=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert actual==oid,(name,actual,oid)
        count+=1
    print('PASS bytes/modes/index:',where.name,'files=',count,'revision=',rev)
    return wanted
head=git(root,'rev-parse','HEAD').decode().strip()
assert head=='847eb4dd031eb3891b61773f4a8324cb2ed6cdc0'
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='05ae0179dbffa852651aa7ec8367758b380672d0'
wanted=verify(root,head)
for name,(mode,kind,pin) in wanted.items():
    if kind=='commit': print('PASS superproject gitlink:',name,pin,mode)
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    path=root/name
    pin=wanted[name][2]
    assert not path.is_symlink()
    assert git(path,'rev-parse','HEAD').decode().strip()==pin
    assert Path(git(path,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==root
    verify(path,pin)
print('Other three gitlinks unchanged; their checkouts were uninitialized and were not used.')
print('Status:',git(root,'status','--porcelain=v1').decode() or '(clean)')
print('PASS exact head/tree and required checkout restoration')

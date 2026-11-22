#!/usr/bin/env python3
"""Verify tracked disk bytes, modes, index, and required submodule pins.
Usage: verify_checkout.py REPO
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env=env)

def verify(repo,expected):
    assert git(repo,'rev-parse','HEAD').decode().strip()==expected
    entries=git(repo,'ls-tree','-rz',expected).split(b'\0')
    want=[];pins={};count=0
    for row in filter(None,entries):
        info,name=row.split(b'\t',1);mode,kind,oid=info.split()
        want.append(mode+b' '+oid+b' 0\t'+name)
        p=repo/os.fsdecode(name)
        if kind==b'commit':
            pins[os.fsdecode(name)]=oid.decode();continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert (b'100755' if st.st_mode&0o111 else b'100644')==mode
            data=p.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest==oid.decode(),os.fsdecode(name)
        count+=1
    have=list(filter(None,git(repo,'ls-files','--stage','-z').split(b'\0')))
    assert sorted(have)==sorted(want),'index differs from pinned tree'
    print('PASS',repo.name,expected,'tracked blobs',count,'index and modes exact')
    return pins

head='dd163e41438acb86e0c4d4e76df90f3f91ace1c0'
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='0e7909a8d02c4123c604c4a168a8b0cbfdd94e7e'
pins=verify(root,head)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    verify(root/name,pins[name])
    print('PASS GITLINK',name,pins[name])
print('external gitlink retained, uninitialized:',pins['external'])
assert not git(root,'status','--porcelain').strip()
print('PASS exact source tree restored; clean status')

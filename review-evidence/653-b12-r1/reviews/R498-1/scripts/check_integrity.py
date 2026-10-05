#!/usr/bin/env python3
"""Verify pinned bytes, modes, index entries and required submodule checkout pins.

Usage: python3 check_integrity.py REPOSITORY
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

repo=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)


def verify(root,pin):
    assert git(root,'rev-parse','HEAD').decode().strip()==pin
    tree={}
    for record in git(root,'ls-tree','-rz',pin).split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,kind,oid=meta.split()
        tree[name]=(mode,oid)
    index={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0' and name not in index
        index[name]=(mode,oid)
    assert index==tree,'index differs from pinned tree'
    count=0;links={}
    for name,(mode,oid) in tree.items():
        p=root/os.fsdecode(name)
        if mode==b'160000':links[os.fsdecode(name)]=oid.decode();continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111)==(mode==b'100755')
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid.decode(),'tracked bytes differ: '+os.fsdecode(name)
        count+=1
    return {'tracked_blobs_verified':count,'index_matches':True,'gitlinks':links}


head='bef8dd7036f711bf286929fa4cba6bf724c7118d'
expected_tree='20594912f6c5e614d2686232569402d6b48a2473'
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()==expected_tree
result={'head':head,'tree':expected_tree,'parent':verify(repo,head),'required_submodules':{}}
for path in ('third_party/verilog-axis','protocol-processor','gptp-processor'):
    sub=repo/path
    assert sub.is_dir() and not sub.is_symlink() and (sub/'.git').is_file()
    assert git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()==str(repo)
    pin=result['parent']['gitlinks'][path]
    result['required_submodules'][path]={'head':pin,**verify(sub,pin)}
assert not git(repo,'status','--porcelain','--untracked-files=all')
result['status_clean']=True
print(json.dumps(result,indent=2,sort_keys=True))

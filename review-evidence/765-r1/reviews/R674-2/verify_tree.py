#!/usr/bin/env python3
"""Read-only raw blob/mode/index/submodule verification, independent of status."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
repo=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],env=env)
def entries(root,rev):
    result={}
    for row in git(root,"ls-tree","-rz",rev).split(b"\0"):
        if not row: continue
        meta,path=row.split(b"\t",1)
        mode,kind,oid=meta.split()
        result[path]=(mode,kind,oid)
    return result
required={b'protocol-processor',b'gptp-processor',b'third_party/verilog-axis',b'third_party/tsn-c-stack'}
def verify(root,rev,top=False):
    records=entries(root,rev)
    index={}
    for row in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not row: continue
        meta,path=row.split(b"\t",1)
        mode,oid,stage=meta.split()
        assert stage==b'0' and path not in index,repr(path)
        index[path]=(mode,oid)
    assert index=={p:(v[0],v[2]) for p,v in records.items()},"index differs from pinned tree"
    n=0
    for rel,(mode,kind,oid) in records.items():
        path=root/os.fsdecode(rel)
        if kind==b'commit':
            populated=(path/'.git').exists()
            if top and rel in required: assert populated,os.fsdecode(rel)
            if populated:
                assert not path.is_symlink()
                assert git(path,'rev-parse','HEAD').strip()==oid
                assert Path(os.fsdecode(git(path,'rev-parse','--show-superproject-working-tree').strip())).resolve()==root
                verify(path,oid.decode())
                print('PASS submodule pin:',os.fsdecode(rel),oid.decode())
            else: print('UNINITIALIZED optional gitlink:',os.fsdecode(rel),oid.decode())
            continue
        info=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(info.st_mode)
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & 0o111)==(mode==b'100755'),os.fsdecode(rel)
            data=path.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest==oid,os.fsdecode(rel)
        n+=1
    print('PASS raw blobs/modes/index:',root.name,n,'blobs',rev)
head='d4a27e6334118c9eef1023aa27e9fd2b7de9f076'
assert git(repo,'rev-parse','HEAD').strip().decode()==head
assert git(repo,'rev-parse','HEAD^{tree}').strip()==b'a78b680bc9ffdbd43e25035ed8ece9e6b746d839'
verify(repo,head,True)
assert not git(repo,'status','--porcelain').strip()
print('PASS exact head/tree and clean tracked checkout')

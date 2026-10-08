#!/usr/bin/env python3
"""Verify actual tracked bytes, modes, index entries and required gitlinks.
Usage: verify_tree.py REPO
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def verify(repo,rev):
    tree={}
    for row in git(repo,'ls-tree','-rz',rev).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1)
        mode,kind,oid=meta.split()
        tree[path]=(mode,oid)
    index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0' and path not in index
        index[path]=(mode,oid)
    assert index==tree, 'index differs from named commit'
    n=0
    for path,(mode,oid) in tree.items():
        if mode==b'160000': continue
        file=repo/os.fsdecode(path)
        st=file.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111)==(mode==b'100755'), path
            data=file.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest==oid, path
        n+=1
    print(repo.name, rev, 'PASS', n, 'tracked blobs/modes and complete index')
    return tree
head='48f12dc14099a3630a98eb07e9ec790695a72bfb'
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='7ed2f048f73734f671ae6eb5e1a008544fa0d0d0'
tree=verify(root,head)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    mode,oid=tree[name.encode()]
    assert mode==b'160000'
    repo=root/name
    assert not repo.is_symlink() and (repo/'.git').is_file()
    assert git(repo,'rev-parse','HEAD').strip()==oid
    assert git(repo,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
    verify(repo,oid.decode())
print('PASS exact head and tree; required submodule pins and actual tracked bytes verified.')

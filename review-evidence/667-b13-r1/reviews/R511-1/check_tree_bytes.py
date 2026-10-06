#!/usr/bin/env python3
"""Verify real tree objects, index, disk bytes and modes, and required gitlinks.

Usage: python3 check_tree_bytes.py REPOSITORY
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
head='afa4e687234b80e9474aa6dd0dc756de16a241bd'
tree='2f113aa1eda3744db77e9ea49818ef49309b63de'
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def audit(repo,rev):
    expected={}
    for entry in git(repo,'ls-tree','-rz',rev).split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1)
        mode,kind,oid=meta.split()
        expected[path]=(mode,oid)
        if kind==b'commit':continue
        f=repo/os.fsdecode(path)
        st=f.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),path
            b=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),path
            assert bool(st.st_mode&0o111)==(mode==b'100755'),path
            b=f.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
        assert actual==oid,path
    indexed={}
    for entry in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0' and path not in indexed,path
        indexed[path]=(mode,oid)
    assert indexed==expected
    assert git(repo,'rev-parse','HEAD').decode().strip()==rev
    return expected

assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==tree
parent=audit(root,head)
print('PASS parent:',head,'tree',tree,'entries',len(parent),'disk bytes/modes and index match.')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    mode,pin=parent[name.encode()]
    assert mode==b'160000'
    path=root/name
    assert path.is_dir() and not path.is_symlink() and (path/'.git').is_file()
    assert git(path,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
    entries=audit(path,pin.decode())
    print('PASS required submodule:',name,pin.decode(),'entries',len(entries),'disk bytes/modes and index match.')
assert not git(root,'status','--porcelain','--untracked-files=normal')
print('PASS parent status clean. No tracked source was modified by this review.')

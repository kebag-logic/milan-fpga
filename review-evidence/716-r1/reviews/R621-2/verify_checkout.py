#!/usr/bin/env python3
"""Prove worktree bytes, modes and index against exact committed objects."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT = Path.cwd()
HEAD = '941e15593ef3dbf561bd8ed75aaf680f5d146a41'
TREE = 'b089eed642dad5dc2af4a69c054b830609ab77cf'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args],env=ENV)

def verify(root, revision):
    assert git(root,'rev-parse','HEAD').decode().strip()==revision
    records=git(root,'ls-tree','-rz','--full-tree',revision).split(b'\0')
    expected={}
    blobs=0
    for record in records:
        if not record: continue
        entry,name=record.split(b'\t',1)
        mode,kind,oid=entry.split()
        expected[name]=(mode,oid,b'0')
        path=root/os.fsdecode(name)
        if kind==b'commit': continue
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),os.fsdecode(name)
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),os.fsdecode(name)
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),os.fsdecode(name)
            data=path.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==oid,os.fsdecode(name)
        blobs+=1
    actual={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record: continue
        entry,name=record.split(b'\t',1)
        mode,oid,stage=entry.split()
        assert stage==b'0' and name not in actual
        actual[name]=(mode,oid,stage)
    assert expected==actual,'index differs from committed tree'
    return dict(revision=revision,blobs_verified=blobs,index_entries=len(actual))

assert git(ROOT,'rev-parse',HEAD+'^{tree}').decode().strip()==TREE
out={'head':HEAD,'tree':TREE,'superproject':verify(ROOT,HEAD),'submodules':{}}
for path in ['third_party/verilog-axis','protocol-processor','gptp-processor','third_party/lwSRP']:
    mode,kind,sha=git(ROOT,'ls-tree',HEAD,path).split(b'\t')[0].split()
    assert mode==b'160000' and kind==b'commit'
    sub=ROOT/path
    assert sub.is_dir() and not sub.is_symlink() and (sub/'.git').is_file()
    assert Path(git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==ROOT.resolve()
    out['submodules'][path]=verify(sub,sha.decode())
out['status_porcelain']=git(ROOT,'status','--porcelain=v1').decode()
assert not out['status_porcelain']
print(json.dumps(out,indent=2))

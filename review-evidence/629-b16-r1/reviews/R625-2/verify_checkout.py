#!/usr/bin/env python3
"""Verify tracked bytes, modes, index and required submodule gitlinks.

Usage: verify_checkout.py REPOSITORY OUTPUT_JSON
Does not rely on status flags, filters, or replace objects for content proof.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve(); output=Path(sys.argv[2])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):
    return subprocess.run(['git','-C',str(repo),*args],env=env,check=True,capture_output=True).stdout
def entries(repo,rev):
    out={}
    for row in git(repo,'ls-tree','-r','-z',rev).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.split()
        out[name]=(mode,kind,oid)
    return out
def verify(repo,rev):
    tree=entries(repo,rev); index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0',(name,'unmerged index')
        assert name not in index,(name,'duplicate index')
        index[name]=(mode,oid)
    assert index=={n:(m,o) for n,(m,k,o) in tree.items()},'index differs from tree'
    count=0
    for name,(mode,kind,oid) in tree.items():
        if kind!=b'blob':continue
        p=repo/os.fsdecode(name);s=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(s.st_mode),name
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode),name
            assert (b'100755' if s.st_mode&0o111 else b'100644')==mode,name
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,(name,'disk blob differs')
        count+=1
    return dict(tracked_blobs_checked=count,index_entries=len(index),bytes_modes_index_equal=True)
head=git(root,'rev-parse','HEAD').decode().strip();treeid=git(root,'rev-parse','HEAD^{tree}').decode().strip()
assert head=='35e332b6be3de2b36c4aec0f1d0bc9f390447b74'
assert treeid=='870785667820e5cae10f060bbd48d0b524db4aeb'
result={'head':head,'tree':treeid,'repository':verify(root,head),'submodules':{}}
tree=entries(root,head)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    mode,kind,oid=tree[name.encode()]
    assert mode==b'160000' and kind==b'commit'
    p=root/name
    assert not p.is_symlink() and (p/'.git').is_file()
    assert git(p,'rev-parse','HEAD').strip()==oid
    assert Path(git(p,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==root
    result['submodules'][name]={'gitlink':oid.decode(),**verify(p,oid.decode())}
result['tracked_restore']='No tracked edits were made; all exact-head content, modes, indexes and required gitlinks verified.'
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

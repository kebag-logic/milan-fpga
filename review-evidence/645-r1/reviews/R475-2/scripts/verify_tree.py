#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries and required submodule pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
a=p.parse_args()
head='886e16201654ba0fd0c60c41c228ea4c75b2f6d3'
tree='f2eb9b9b349fd5a1c13df31143c7e20df40e1ba7'
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root)
def verify(root,expected):
    assert not root.is_symlink()
    assert Path(os.fsdecode(git(root,'rev-parse','--show-toplevel').strip())).resolve()==root.resolve()
    assert git(root,'rev-parse','HEAD').decode().strip()==expected
    entries={}
    for row in git(root,'ls-tree','-rz','--full-tree',expected).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.split()
        entries[name]=(mode,kind,oid)
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0'
        index[name]=(mode,oid)
    assert index=={name:(mode,oid) for name,(mode,_,oid) in entries.items()}
    checked=0
    for name,(mode,kind,oid) in entries.items():
        if kind==b'commit':continue
        path=root/os.fsdecode(name)
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),str(path)
            data=path.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest==oid.decode(),str(path)
        checked+=1
    return {'head':expected,'tree':git(root,'rev-parse',expected+'^{tree}').decode().strip(),'tracked_blobs_verified':checked,'index_matches_tree':True},entries

main,entries=verify(a.repo,head)
assert main['tree']==tree
sub={}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    mode,kind,pin=entries[name.encode()]
    assert mode==b'160000' and kind==b'commit'
    sub[name],_=verify(a.repo/name,pin.decode())
result={'superproject':main,'required_submodules':sub,'raw_bytes_modes_index_gitlinks':'PASS','status':git(a.repo,'status','--porcelain=v1').decode()}
assert result['status']==''
out=Path(__file__).resolve().parents[1]/'receipts/final-tree.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

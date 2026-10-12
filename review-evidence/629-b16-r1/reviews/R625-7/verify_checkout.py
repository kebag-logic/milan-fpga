#!/usr/bin/env python3
"""Prove checkout bytes, filesystem modes and index against immutable Git trees.
Usage: python verify_checkout.py REPO OUT_JSON
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def check(root,revision):
    records=git(root,'ls-tree','-rz',revision).split(b'\0')
    expected={}
    links={}
    errors=[]
    for record in records:
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        name=os.fsdecode(name)
        expected[name]=(mode,oid,'0')
        if mode=='160000':
            links[name]=oid
            continue
        path=root/name
        try:
            st=path.lstat()
            if mode=='120000':
                assert stat.S_ISLNK(st.st_mode)
                data=os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode&0o111)==(mode=='100755')
                data=path.read_bytes()
            h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert h==oid
        except (OSError,AssertionError):
            errors.append(name)
    index={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1)
        assert os.fsdecode(name) not in index, 'multiple index stages'
        index[os.fsdecode(name)]=tuple(meta.decode().split())
    assert index==expected,'index differs from tree'
    assert not errors,errors
    return dict(files=len(expected)-len(links),blob_bytes_and_modes_equal=True,index_equal=True,gitlinks=links)

head=git(repo,'rev-parse','HEAD').decode().strip()
assert head=='295ba9d7f7dfed65e95002478ed6d55ccc14e580'
tree=git(repo,'rev-parse','HEAD^{tree}').decode().strip()
assert tree=='160ba4535ed6caf63d23994b364b1f054bd95589'
result=dict(head=head,tree=tree,parent=check(repo,head),submodules={})
required={'protocol-processor','gptp-processor','third_party/verilog-axis'}
for name,oid in result['parent']['gitlinks'].items():
    sub=repo/name
    if not (sub/'.git').exists():
        assert name not in required
        result['submodules'][name]=dict(gitlink=oid,checkout='uninitialized as found; no execution from it')
        continue
    assert git(sub,'rev-parse','HEAD').decode().strip()==oid
    result['submodules'][name]=dict(gitlink=oid,**check(sub,oid))
result['status']=git(repo,'status','--porcelain=v1','--untracked-files=normal').decode()
assert not result['status'],result['status']
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact head/tree, tracked blob bytes and modes, index, required submodule checkouts and all gitlinks')

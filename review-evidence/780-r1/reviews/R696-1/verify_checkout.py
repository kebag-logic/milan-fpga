#!/usr/bin/env python3
"""Verify actual tracked bytes, modes, index records and accepted gitlinks.

Run from the original review clone. Git replacement objects are disabled.
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,label):
    head=git(root,'rev-parse','HEAD').decode().strip()
    tree=git(root,'rev-parse','HEAD^{tree}').decode().strip()
    entries={}
    links={}
    for entry in git(root,'ls-tree','-rz','HEAD').split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        path=path.decode();entries[path]=(mode,oid)
        if mode=='160000': links[path]=oid;continue
        f=root/path
        st=f.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(st.st_mode),path
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),path
            assert bool(st.st_mode&0o111)==(mode=='100755'),path
            data=f.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,(label,path,'blob mismatch')
    index={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        meta,path=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        assert stage=='0',path
        index[path.decode()]=(mode,oid)
    assert index==entries,(label,'index differs from HEAD')
    print(f'PASS {label}: HEAD {head}, tree {tree}; {len(entries)-len(links)} blobs/modes and complete index verified')
    for path,pin in links.items():print(f'GITLINK {path} {pin}')
    return head,tree,links

root=Path.cwd()
head,tree,links=verify(root,'parent')
assert head=='25f05752f7e50e3cf7e27008e434ffde930b4b6f'
assert tree=='5db8e8298734d18c8a50ba24cd8c46140292302b'
assert links['protocol-processor']=='ed2118035e4cec76fb1b59cfbf8a053aeacc8af8'
assert links['gptp-processor']=='55680bff3b287b9a7b0c759f51471fa617c17335'
for sub,pin in links.items():
    if not (root/sub/'.git').exists():
        assert sub=='external'
        print('LIMIT external historical unused checkout is uninitialized; accepted gitlink verified')
        continue
    subhead,_,_=verify(root/sub,sub)
    assert subhead==pin,(sub,'wrong checkout')
print('PASS original review checkout has exact tracked bytes, file modes, index and required initialized submodule pins.')

#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index records, and required gitlinks."""
import hashlib
from pathlib import Path
import os
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = '1b47a3dcff0cb65cb5cebe1f86327429a76f775d'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def audit(repo, commit):
    assert git(repo,'rev-parse','HEAD').decode().strip()==commit
    entries={}
    count=0
    for record in git(repo,'ls-tree','-rz',commit).split(b'\0'):
        if not record: continue
        head,name=record.split(b'\t',1)
        mode,kind,oid=head.split()
        entries[name]=(mode,oid)
        path=repo/os.fsdecode(name)
        if kind==b'commit': continue
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),name
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,name
        count+=1
    index={}
    for record in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not record: continue
        head,name=record.split(b'\t',1)
        mode,oid,stage=head.split()
        assert stage==b'0',name
        index[name]=(mode,oid)
    assert entries==index,'index differs from commit tree'
    return count,entries

count,entries=audit(root,expected)
print('Superproject HEAD',expected)
print('Superproject tree',git(root,'rev-parse','HEAD^{tree}').decode().strip())
print('Raw tracked blobs and modes verified:',count,'; index matches HEAD')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    mode,pin=entries[os.fsencode(name)]
    assert mode==b'160000'
    path=root/name
    assert not path.is_symlink() and (path/'.git').exists()
    assert git(path,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
    n,_=audit(path,pin.decode())
    print(name,pin.decode(),f'{n} raw blobs/modes and index verified')
print('PASS: required gitlinks and raw tracked contents unchanged')

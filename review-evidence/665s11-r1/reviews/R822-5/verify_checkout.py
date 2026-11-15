#!/usr/bin/env python3
"""Compare tracked bytes/modes and the complete index to immutable trees, including initialized gitlinks."""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

root=Path(sys.argv[1]).resolve()
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(where,*args):
    return subprocess.check_output(['git','-C',str(where),*args],env=env)

def check(where,revision,label):
    actual=git(where,'rev-parse','HEAD').decode().strip()
    assert actual==revision, (label,'HEAD',actual)
    entries={}
    for record in git(where,'ls-tree','-rz',revision).split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        entries[name]=(mode,kind,oid)
    indexed={}
    for record in git(where,'ls-files','-s','-z').split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        assert stage=='0', (label,name,'unmerged')
        indexed[name]=(mode,oid)
    assert indexed=={n:(m,o) for n,(m,k,o) in entries.items()}, (label,'index mismatch')
    count=0
    for name,(mode,kind,oid) in entries.items():
        p=where/os.fsdecode(name)
        if mode=='160000': continue
        s=p.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode), (label,name,'not symlink')
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), (label,name,'not regular')
            assert bool(s.st_mode & 0o111)==(mode=='100755'), (label,name,'mode mismatch')
            data=p.read_bytes()
        hashed=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert hashed==oid, (label,name,'byte mismatch')
        count+=1
    print('PASS',label,revision,':',count,'tracked blobs/modes; exact index')
    return [(os.fsdecode(n),o) for n,(m,k,o) in entries.items() if m=='160000']

head='d3566d44dcae75069f56d97402a5f1b351743008'
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='32693acb2b16ca8dc329fd20fcbc6b92f2b45db3'
links=check(root,head,'superproject')
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'}
for name,oid in links:
    if name not in required:
        print('Gitlink recorded, intentionally uninitialized:',name,oid)
        continue
    p=root/name
    assert (p/'.git').is_file() and not p.is_symlink(), (name,'not initialized submodule')
    check(p,oid,name)
assert required <= {n for n,o in links}
print('PASS exact checkout restoration; no tracked source edits')

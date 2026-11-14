#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index and initialized required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
head='62298ab5cbfeb7056e4567f70e69d578201c75e0'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(where,*args):
    return subprocess.check_output(['git','-C',str(where),*args],env=env)
def verify(where,expected,label):
    actual=git(where,'rev-parse','HEAD').decode().strip()
    assert actual==expected,(label,actual,expected)
    entries={}
    for record in git(where,'ls-tree','-rz',expected).split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1)
        mode,kind,oid=meta.split()
        entries[name]=(mode,oid)
        if kind==b'commit':continue
        p=where/os.fsdecode(name)
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),(label,name)
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),(label,name)
            assert bool(st.st_mode&stat.S_IXUSR)==(mode==b'100755'),(label,name,'mode')
            data=p.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==oid,(label,name,'blob bytes')
    indexed={}
    for record in git(where,'ls-files','-sz').split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0' and name not in indexed,(label,name,'index stage')
        indexed[name]=(mode,oid)
    assert indexed==entries,(label,'index differs from commit tree')
    print(label,actual,'tracked entries',len(entries),'bytes/modes/index EXACT')
    return entries
entries=verify(root,head,'source')
for name in ('gptp-processor','protocol-processor','third_party/lwSRP','third_party/tsn-c-stack','third_party/verilog-axis'):
    mode,pin=entries[name.encode()]
    assert mode==b'160000'
    p=root/name
    assert (p/'.git').is_file(),name
    superproject=git(p,'rev-parse','--show-superproject-working-tree').decode().strip()
    assert Path(superproject).resolve()==root,name
    verify(p,pin.decode(),name)
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='71f9951455c31270524f6931cf621c21af6a82cf'
print('TREE VERIFICATION PASS; external gitlink retained, optional checkout uninitialized.')

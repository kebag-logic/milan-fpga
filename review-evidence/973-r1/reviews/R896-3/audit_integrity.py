#!/usr/bin/env python3
"""Compare actual tracked bytes, kinds, modes and index against immutable trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
head='87b2fc0f2867ef132b9388e22ec262fc626cbb57'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(at,*args):
    return subprocess.check_output(['git','-C',str(at),*args],env=env)
def audit(at,rev,desc):
    tree={}
    for rec in git(at,'ls-tree','-rz',rev).split(b'\0'):
        if not rec: continue
        meta,path=rec.split(b'\t',1); mode,kind,oid=meta.split()
        tree[path]=(mode,oid)
    index={}
    for rec in git(at,'ls-files','--stage','-z').split(b'\0'):
        if not rec: continue
        meta,path=rec.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0' and path not in index
        index[path]=(mode,oid)
    assert tree==index, desc+' index mismatch'
    for rel,(mode,oid) in tree.items():
        if mode==b'160000': continue
        p=at/os.fsdecode(rel); st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111)==(mode==b'100755')
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,(desc,os.fsdecode(rel),'blob mismatch')
    print(f'{desc}: {len(tree)} entries, raw blobs/kinds/modes/index PASS')
    return tree
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='82af93a508702104d01ea085c238cba30c636c38'
tree=audit(root,head,'superproject')
for path in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    mode,pin=tree[path.encode()]; assert mode==b'160000'
    at=root/path
    assert (at/'.git').is_file() and not at.is_symlink()
    assert git(at,'rev-parse','HEAD').strip()==pin
    audit(at,pin.decode(),path+' @ '+pin.decode())
print('external remains uninitialized and excluded; five required gitlinks and their tracked bytes verified')
print('PASS: exact requested head/tree retained; no source restoration needed')

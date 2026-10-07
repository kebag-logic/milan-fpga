#!/usr/bin/env python3
"""Verify tracked bytes, kinds, modes, index entries and required gitlinks without trusting status flags."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
head='35fb2a95007ce6dd1ec4f51c2dcb793800623cfd'
tree='430abfdcb667dded3fd9b874a0a69c464ae1bd7c'
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root)
assert git(repo,'rev-parse','HEAD').decode().strip()==head
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()==tree

def verify(root,rev):
    entries={}
    for row in git(root,'ls-tree','-rz','--full-tree',rev).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1)
        mode,kind,oid=meta.split()
        entries[os.fsdecode(name)]=(mode.decode(),kind.decode(),oid.decode())
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0'
        index[os.fsdecode(name)]=(mode.decode(),oid.decode())
    assert index=={n:(m,o) for n,(m,k,o) in entries.items()},'index differs'
    blobs=0;links={}
    for name,(mode,kind,oid) in entries.items():
        path=root/name
        if kind=='commit':
            links[name]=oid;continue
        st=path.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert ('100755' if st.st_mode&stat.S_IXUSR else '100644')==mode,name
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,name
        blobs+=1
    return {'commit':rev,'verified_blobs':blobs,'index_matches':True,'gitlinks':links}

results={'root':verify(repo,head)}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    pin=results['root']['gitlinks'][name]
    assert git(repo/name,'rev-parse','HEAD').decode().strip()==pin,name
    assert (repo/name/'.git').is_file(),name
    results[name]=verify(repo/name,pin)
results['external']='not initialized; outside required validation inputs'
(packet/'final-tree-integrity.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: exact head/tree; all tracked blob bytes/kinds/modes and index entries match; all three required submodules match their gitlinks and pinned blobs')
print(json.dumps({n:r['verified_blobs'] for n,r in results.items() if isinstance(r,dict)}))

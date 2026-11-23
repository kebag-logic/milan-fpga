#!/usr/bin/env python3
"""Check actual tracked bytes, executable/symlink modes, index and gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess as sp
import sys
root=Path(sys.argv[1]).resolve()
head='64117b77cb9e5c421717835b5be032b5905c447d'
def git(tree,*args):
    return sp.check_output(['git','-C',str(tree),*args],env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})
assert git(root,'rev-parse','HEAD').decode().strip()==head
def check(tree,rev):
    expected=[]; blobs=0; links=[]
    for row in git(tree,'ls-tree','-rz',rev).split(b'\0'):
        if not row: continue
        metadata,path=row.split(b'\t',1)
        mode,kind,oid=metadata.decode().split()
        path=path.decode()
        expected.append(f'{mode} {oid} 0\t{path}')
        p=tree/path
        if kind=='commit': links.append((path,oid)); continue
        st=p.lstat()
        actualmode='120000' if stat.S_ISLNK(st.st_mode) else ('100755' if st.st_mode&stat.S_IXUSR else '100644')
        data=os.readlink(p).encode() if actualmode=='120000' else p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid and actualmode==mode,(path,'blob or mode mismatch')
        blobs+=1
    index=[x.decode() for x in git(tree,'ls-files','--stage','-z').split(b'\0') if x]
    assert sorted(index)==sorted(expected),'Index differs from pinned tree'
    return blobs,links
blobs,links=check(root,head)
print('Head',head)
print('Tree',git(root,'rev-parse','HEAD^{tree}').decode().strip())
print('Parent tracked blobs/modes verified:',blobs,'; index matches tree')
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'}
for path,pin in links:
    if path not in required:
        print(path,pin,'uninitialized; not required for focused probes'); continue
    sub=root/path
    assert (sub/'.git').is_file(),'Submodule registration missing'
    assert git(sub,'rev-parse','HEAD').decode().strip()==pin
    n,_=check(sub,pin)
    print(path,pin,'PASS',n,'tracked blobs/modes; index matches pin')
status=git(root,'status','--porcelain').decode()
assert not status,status
print('Original clone clean. No source restoration needed; probes used scratch clones.')

#!/usr/bin/env python3
"""Check all tracked bytes, modes, index entries and populated submodule pins."""
import hashlib
import os
import pathlib
import stat
import subprocess
import sys
def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args])
def audit(root,rev):
    assert git(root,'rev-parse','HEAD').decode().strip()==rev
    assert git(root,'write-tree').strip()==git(root,'rev-parse','HEAD^{tree}').strip()
    entries=git(root,'ls-tree','-rz','HEAD').split(b'\0')
    blobs=0; links=[]
    index=[]
    for raw in entries:
        if not raw: continue
        info,name=raw.split(b'\t',1); mode,kind,oid=info.split()
        path=root/os.fsdecode(name)
        index.append(mode+b' '+oid+b' 0\t'+name)
        if mode==b'160000':
            links.append((path,oid.decode())); continue
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode&0o111)==(mode==b'100755'),str(path)
            data=path.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest==oid.decode(),str(path)
        blobs+=1
    actual=git(root,'ls-files','--stage','-z').split(b'\0')
    assert sorted(x for x in actual if x)==sorted(index)
    flags=git(root,'ls-files','-v','-z').split(b'\0')
    assert all(not x or x[:1]==b'H' for x in flags),'hidden index flags'
    print('PASS',root.name,rev,'blobs',blobs,'index entries',len(index),'bytes/modes/index/flags')
    for path,pin in links:
        if (path/'.git').exists(): audit(path,pin)
        else:
            assert path.name=='external',str(path)
            print('OPTIONAL external uninitialized gitlink',pin)
root=pathlib.Path(sys.argv[1]).resolve()
audit(root,'4ff3642e8fe9a0bd48d28374350390cde553bc32')
print('PASS exact head/tree',git(root,'rev-parse','HEAD^{tree}').decode().strip())
print('Untracked parent entries:',len(git(root,'ls-files','--others','--exclude-standard','-z').split(b'\0'))-1)

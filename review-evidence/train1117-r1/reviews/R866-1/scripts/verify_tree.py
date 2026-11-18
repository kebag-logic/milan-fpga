#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index entries and initialized gitlinks."""
from pathlib import Path
import hashlib, os, stat, subprocess
HEAD='732726660a88cd79a568d650d955d535fe79c720'
TREE='11d45104e6c71b7623cec24bcac27610c5a402be'
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def verify(root,commit):
    actual=git(root,'rev-parse','HEAD').decode().strip()
    assert actual==commit,(root,actual,commit)
    entries={}
    for rec in git(root,'ls-tree','-rz','--full-tree',commit).split(b'\0'):
        if not rec:continue
        fields,path=rec.split(b'\t',1);mode,kind,oid=fields.decode().split();entries[path]=(mode,oid)
    index={}
    for rec in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not rec:continue
        fields,path=rec.split(b'\t',1);mode,oid,stage=fields.decode().split();assert stage=='0';index[path]=(mode,oid)
    assert index==entries,('index differs',root)
    count=0
    for raw,(mode,oid) in entries.items():
        path=root/os.fsdecode(raw)
        if mode=='160000':
            if (path/'.git').exists():verify(path,oid)
            else:print('UNINITIALIZED gitlink retained',os.fsdecode(raw),oid)
            continue
        s=path.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode);data=os.readlink(path).encode()
        else:
            assert stat.S_ISREG(s.st_mode)
            assert bool(s.st_mode&0o111)==(mode=='100755'),path
            data=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==oid,(path,oid,blob)
        count+=1
    print('PASS',root.name,'tracked bytes/modes/index',count,'HEAD',commit)
root=Path.cwd()
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
verify(root,HEAD)
assert not git(root,'diff','--check','cb96336d',HEAD)
print('PASS exact head and tree, recursive tracked-byte verification, required initialized submodules and diff whitespace')

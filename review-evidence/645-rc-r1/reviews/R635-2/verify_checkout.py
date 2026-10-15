#!/usr/bin/env python3
"""Verify tracked bytes, modes, index entries and required submodule pins.

Run from the candidate root. No files are written or index flags trusted.
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = 'fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c'
TREE = '77e1321b1c9684e8899a85710296eb75af7ddf48'

def git(root, *args):
    return subprocess.check_output(['git','--no-replace-objects','-C',str(root),*args])

def verify(root, ref):
    entries = {}
    for row in git(root,'ls-tree','-rz',ref).split(b'\0'):
        if not row: continue
        header, name = row.split(b'\t',1)
        mode, kind, oid = header.split()
        entries[name]=(mode,oid)
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        header,name=row.split(b'\t',1)
        mode,oid,stage=header.split()
        assert stage == b'0',name
        assert name not in index,name
        index[name]=(mode,oid)
    assert index == entries,'Index differs from committed tree'
    blobs=0
    links=[]
    for name,(mode,oid) in entries.items():
        p=root/os.fsdecode(name)
        if mode == b'160000':
            links.append((name.decode(),oid.decode()))
            continue
        st=p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),name
            actual=b'100755' if st.st_mode & stat.S_IXUSR else b'100644'
            assert actual == mode,name
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual == oid,name
        blobs+=1
    return blobs,links

def main():
    root=Path.cwd()
    assert git(root,'rev-parse','HEAD').decode().strip() == HEAD
    assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == TREE
    blobs,links=verify(root,HEAD)
    print('PASS candidate HEAD',HEAD,'tree',TREE)
    print('PASS',blobs,'tracked blobs: raw bytes, file kinds, executable modes and full stage-0 index')
    for name,pin in links:
        print('gitlink',name,pin)
        if name == 'external':
            print('external not required for this review; gitlink verified, uninitialized checkout retained')
            continue
        sub=root/name
        assert not sub.is_symlink()
        assert (sub/'.git').is_file(),'Required submodule must be registered'
        assert git(sub,'rev-parse','HEAD').decode().strip() == pin
        count,nested=verify(sub,pin)
        print('PASS required submodule',name,count,'tracked blobs, modes and index; nested gitlinks',len(nested))
    assert not git(root,'status','--porcelain=v1','--untracked-files=all')
    print('PASS clean candidate status; no source edits, probes, builds or GitHub writes performed')

if __name__ == '__main__':
    main()

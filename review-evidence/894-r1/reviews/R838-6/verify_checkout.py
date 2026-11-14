#!/usr/bin/env python3
"""Verify tracked bytes, modes, stage-zero index, and populated gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT=Path.cwd()
OUT=Path(__file__).resolve().parent

def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args])

def check(root,expected):
    assert git(root,'rev-parse','HEAD').decode().strip()==expected
    entries={}
    for r in git(root,'ls-tree','-rz','HEAD').split(b'\0'):
        if not r: continue
        meta,name=r.split(b'\t',1)
        mode,kind,oid=meta.split()
        entries[name]=(mode,kind,oid)
    index={}
    for r in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not r:continue
        meta,name=r.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0'
        index[name]=(mode,oid)
    assert index=={p:(m,o) for p,(m,k,o) in entries.items()}
    for r in git(root,'ls-files','-v','-z').split(b'\0'):
        if r: assert r.startswith(b'H '),r
    blobs=0
    children={}
    for name,(mode,kind,oid) in entries.items():
        p=root/os.fsdecode(name)
        if kind==b'commit':
            if (p/'.git').exists():children[os.fsdecode(name)]=check(p,oid.decode())
            else:children[os.fsdecode(name)]={'pin':oid.decode(),'populated':False}
            continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),str(p)
            data=p.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert got==oid.decode(),str(p)
        blobs+=1
    untracked=git(root,'ls-files','--others','--exclude-standard').decode().splitlines()
    assert not untracked,untracked
    return {'head':expected,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),
            'tracked_blobs_verified':blobs,'index_and_modes':'match','untracked':untracked,'submodules':children}

result=check(ROOT,'9606b3a915de284c71d3063c2e8d94b097f18241')
(OUT/'receipts/checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

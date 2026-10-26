#!/usr/bin/env python3
"""Verify raw tracked bytes, file modes, index and populated submodule pins.
Usage: script TREE. Does not modify a checkout.
"""
import os
import stat
import subprocess
import sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
def git(at,*args,**kw):
    return subprocess.check_output(['git','-C',str(at),*args],**kw)
def verify(at,expected=None):
    head=git(at,'rev-parse','HEAD').decode().strip()
    if expected: assert head==expected,(at,head,expected)
    assert not git(at,'diff','--cached','--raw','HEAD'),str(at)
    records=git(at,'ls-files','--stage','-z').split(b'\0')
    entries=[]; modules=[]
    for record in records:
        if not record: continue
        meta,raw=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split(); assert stage=='0'
        name=os.fsdecode(raw); p=at/name
        if mode=='160000':
            modules.append((name,oid)); continue
        data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
        got=subprocess.check_output(['git','hash-object','--stdin','--no-filters'],input=data).decode().strip()
        assert got==oid,(name,got,oid)
        actual='120000' if p.is_symlink() else '100755' if p.stat().st_mode & stat.S_IXUSR else '100644'
        assert actual==mode,(name,actual,mode)
        entries.append(name)
    print(at.name,head,'tree',git(at,'rev-parse','HEAD^{tree}').decode().strip(),len(entries),'raw blobs/modes and index match',flush=True)
    for name,oid in modules:
        if (at/name/'.git').exists():verify(at/name,oid)
        else: print('unpopulated gitlink',name,oid,flush=True)
verify(root,'44d95625bde2c46d7070c090fc29ed0ba85ab64a')

#!/usr/bin/env python3
"""Verify committed blob bytes, file modes, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(directory,*args):
    return subprocess.check_output(['git',*args],cwd=directory,env=env)
def verify(directory,expected,label):
    errors=[]
    actual=git(directory,'rev-parse','HEAD').decode().strip()
    if actual!=expected:
        errors.append('HEAD differs from pin')
    records=[]
    blobs=0
    links={}
    for raw in git(directory,'ls-tree','-rz',expected).split(b'\0'):
        if not raw: continue
        info,name=raw.split(b'\t',1)
        mode,kind,oid=info.decode().split()
        path=os.fsdecode(name)
        records.append((mode,oid,'0',path))
        if kind=='commit':
            links[path]=oid
            continue
        file=directory/path
        try:
            info=file.lstat()
            if mode=='120000':
                if not stat.S_ISLNK(info.st_mode): raise ValueError('not a symlink')
                data=os.fsencode(os.readlink(file))
            else:
                if not stat.S_ISREG(info.st_mode): raise ValueError('not a regular file')
                if bool(info.st_mode & 0o111)!=(mode=='100755'): raise ValueError('executable mode mismatch')
                data=file.read_bytes()
            digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if digest!=oid: raise ValueError('blob differs')
            blobs+=1
        except (OSError,ValueError) as error:
            errors.append(path+': '+str(error))
    index=[]
    for raw in git(directory,'ls-files','--stage','-z').split(b'\0'):
        if not raw: continue
        info,name=raw.split(b'\t',1)
        mode,oid,stage=info.decode().split()
        index.append((mode,oid,stage,os.fsdecode(name)))
    if sorted(index)!=sorted(records):errors.append('index differs from committed tree')
    return dict(repository=label,head=actual,blobs=blobs,index_entries=len(index),gitlinks=links,errors=errors)

head='43076d0f8c87b5118f6f4317d000a7eebdefc967'
main=verify(root,head,'superproject')
rows=[main]
for name in ('protocol-processor','gptp-processor','third_party/lwSRP','third_party/tsn-c-stack','third_party/verilog-axis'):
    rows.append(verify(root/name,main['gitlinks'][name],name))
print(json.dumps(rows,indent=2))
raise SystemExit(any(row['errors'] for row in rows))

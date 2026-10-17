#!/usr/bin/env python3
"""Prove repository blob bytes, modes, index entries and gitlinks against HEAD.

Usage: integrity.py CHECKOUT OUTPUT_JSON
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root, output = map(Path,sys.argv[1:3])
env = {**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
tree = {}
for record in git('ls-tree','-rz','HEAD').split(b'\0'):
    if record:
        meta,path = record.split(b'\t',1)
        mode,kind,oid = meta.decode().split()
        tree[os.fsdecode(path)]=(mode,kind,oid)
index = {}
for record in git('ls-files','--stage','-z').split(b'\0'):
    if record:
        meta,path = record.split(b'\t',1)
        mode,oid,stage = meta.decode().split()
        index.setdefault(os.fsdecode(path),[]).append((mode,oid,stage))
errors=[]
links={}
blobs=0
for name,(mode,kind,oid) in tree.items():
    if index.get(name)!=[(mode,oid,'0')]:
        errors.append(name+': index mismatch')
    path=root/name
    if kind=='commit':
        links[name]=dict(oid=oid,mode=mode,initialized=(path/'.git').exists())
        continue
    s=path.lstat()
    if mode=='120000':
        assert stat.S_ISLNK(s.st_mode)
        data=os.fsencode(os.readlink(path))
        actual='120000'
    else:
        assert stat.S_ISREG(s.st_mode)
        data=path.read_bytes()
        actual='100755' if s.st_mode&0o111 else '100644'
    hashed=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=mode or hashed!=oid:
        errors.append(name+': bytes/mode mismatch')
    blobs+=1
errors += [p+': extra index entry' for p in set(index)-set(tree)]
result=dict(head=git('rev-parse','HEAD').decode().strip(),tree=git('rev-parse','HEAD^{tree}').decode().strip(),
            blobs_checked=blobs,errors=errors,gitlinks=links,status=git('status','--porcelain').decode(),
            diff_paths=git('diff','--name-only','4a9b5a2a..HEAD').decode().splitlines(),
            round2_paths=git('diff','--name-only','867fb945..HEAD').decode().splitlines())
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert not errors and not result['status']

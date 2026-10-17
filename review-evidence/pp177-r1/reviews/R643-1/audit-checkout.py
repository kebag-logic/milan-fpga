#!/usr/bin/env python3
"""Verify worktree bytes, modes, index and gitlinks against the requested head."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
a = p.parse_args()
head = '6aaec5dfc45e84c8842f3f31f76910bfa91a96e1'
def git(*args):
    return subprocess.check_output(['git','-C',str(a.source),*args])
assert git('rev-parse','HEAD').decode().strip() == head
assert git('rev-parse','HEAD^{tree}').decode().strip() == '5f7ae4960def91d88b3c4c053a94c021c1d3e955'
expected = {}
for raw in git('ls-tree','-rz',head).split(b'\0'):
    if not raw: continue
    meta, path = raw.split(b'\t',1)
    mode, kind, oid = meta.decode().split()
    expected[os.fsdecode(path)] = (mode,kind,oid)
index = {}
for raw in git('ls-files','--stage','-z').split(b'\0'):
    if not raw: continue
    meta,path = raw.split(b'\t',1)
    mode,oid,stage = meta.decode().split()
    assert stage == '0'
    index[os.fsdecode(path)] = (mode,oid)
assert index == {p:(v[0],v[2]) for p,v in expected.items()}
blobs=[]; links=[]
for name,(mode,kind,oid) in expected.items():
    f=a.source/name
    if mode=='160000':
        links.append({'path':name,'oid':oid})
        assert subprocess.check_output(['git','-C',str(f),'rev-parse','HEAD']).decode().strip()==oid
        continue
    data=os.fsencode(os.readlink(f)) if mode=='120000' else f.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got==oid, name
    if mode!='120000':
        assert bool(f.stat().st_mode & 0o111) == (mode=='100755'), name
    blobs.append({'path':name,'mode':mode,'blob':got})
assert not git('diff','--raw',head)
assert not git('status','--porcelain=v1','--untracked-files=all')
print(json.dumps({'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(), 'tracked_blob_count':len(blobs), 'index_matches':True, 'worktree_bytes_and_modes_match':True, 'gitlinks':links, 'status':'clean', 'blobs':blobs},indent=2))

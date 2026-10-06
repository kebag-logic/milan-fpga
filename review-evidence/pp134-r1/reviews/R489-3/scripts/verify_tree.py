#!/usr/bin/env python3
"""Verify raw tracked bytes, executable/symlink modes, index and gitlinks.

Usage: python3 verify_tree.py CHECKOUT
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git','-C',str(root),*args])
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='ffc3a8e5733202384e55ea9094569cca86b78261'
assert tree=='a7c1bce09cefceda944558258f6b38cfba7ac7ed'
expected={}
gitlinks={}
failures=[]
for line in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not line: continue
    meta,name=line.split(b'\t',1)
    mode,kind,blob=meta.decode().split()
    rel=os.fsdecode(name)
    expected[rel]=(mode,blob,'0')
    if kind=='commit':
        gitlinks[rel]=blob
        actual=subprocess.check_output(['git','-C',str(root/rel),'rev-parse','HEAD']).decode().strip()
        if actual!=blob: failures.append([rel,'gitlink',actual,blob])
        continue
    file=root/rel
    body=os.fsencode(os.readlink(file)) if file.is_symlink() else file.read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    actual_mode='120000' if file.is_symlink() else ('100755' if file.stat().st_mode & stat.S_IXUSR else '100644')
    if (digest,actual_mode)!=(blob,mode): failures.append([rel,'blob/mode',digest,actual_mode,blob,mode])
index={}
for line in git('ls-files','--stage','-z').split(b'\0'):
    if not line: continue
    meta,name=line.split(b'\t',1)
    mode,blob,stage=meta.decode().split()
    index[os.fsdecode(name)]=(mode,blob,stage)
if index!=expected: failures.append(['index differs from tree'])
status=git('status','--porcelain=v1','--ignored','--untracked-files=all').decode()
if status: failures.append(['nonempty status',status])
result={'head':head,'tree':tree,'tracked_entries':len(expected),'gitlinks':gitlinks,
        'index_matches_tree':index==expected,'raw_blobs_and_modes_match':not failures,
        'status':status,'failures':failures}
print(json.dumps(result,indent=2))
raise SystemExit(bool(failures))

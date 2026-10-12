#!/usr/bin/env python3
"""Compare tracked bytes, modes, index entries and initialized pins directly.

Usage: python3 verify_integrity.py CHECKOUT
Replacement objects are disabled for every Git query. No checkout is changed.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD='5c6f489ac65f51763a6ccc41f338dde0e5fc90b5'
TREE='f2e72c84ee50dbd84ea0d37c98f18d2fc8bbdc24'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def oid(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def verify(root,commit,label):
    failures=[]
    observed=git(root,'rev-parse','HEAD').decode().strip()
    if observed!=commit:failures.append('HEAD mismatch')
    expected={}
    for line in git(root,'ls-tree','-rz',commit).split(b'\0'):
        if not line:continue
        header,rawpath=line.split(b'\t',1)
        mode,kind,sha=header.decode().split()
        expected[os.fsdecode(rawpath)]=(mode,kind,sha)
    actual={}
    for line in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not line:continue
        header,rawpath=line.split(b'\t',1)
        mode,sha,stage=header.decode().split()
        name=os.fsdecode(rawpath)
        if stage!='0' or name in actual:failures.append('nonunique stage-0 index: '+name)
        actual[name]=(mode,sha)
    want={p:(mode,sha) for p,(mode,kind,sha) in expected.items()}
    if actual!=want:failures.append('index differs from pinned tree')
    gitlinks=[]
    for name,(mode,kind,sha) in expected.items():
        path=root/name
        if kind=='commit':
            child={'path':name,'pin':sha}
            if (path/'.git').exists():
                child['verification']=verify(path,sha,label+'/'+name)
                if child['verification']['failures']:failures.append('submodule failed: '+name)
            else:
                child['checkout']='uninitialized; gitlink/index identity only'
            gitlinks.append(child)
            continue
        try:
            info=path.lstat()
            if mode=='120000':
                assert stat.S_ISLNK(info.st_mode)
                data=os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(info.st_mode)
                assert bool(info.st_mode&0o111)==(mode=='100755')
                data=path.read_bytes()
            if oid(data)!=sha:failures.append('blob mismatch: '+name)
        except (OSError,AssertionError):failures.append('missing or wrong kind/mode: '+name)
    untracked=git(root,'ls-files','--others','--exclude-standard','-z').split(b'\0')
    untracked=[os.fsdecode(p) for p in untracked if p]
    if untracked:failures.append('nonignored untracked paths: '+repr(untracked))
    return {'repository':label,'head':observed,'tree':git(root,'rev-parse',commit+'^{tree}').decode().strip(),
            'entries':len(expected),'byte_mode_index_match':not failures,'gitlinks':gitlinks,'failures':failures}
root=Path(sys.argv[1]).resolve()
result=verify(root,HEAD,'reviewed root')
if result['tree']!=TREE:result['failures'].append('root tree mismatch')
print(json.dumps(result,indent=2))
raise SystemExit(bool(result['failures']))

#!/usr/bin/env python3
"""Verify tree, index, tracked bytes and executable modes, including initialized gitlinks.
Usage: verify_checkout.py REPO OUTPUT_JSON
"""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys

repo=Path(sys.argv[1]).resolve();env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,commit):
    tree=git(root,'ls-tree','-rz',commit)
    index=git(root,'ls-files','--stage','-z')
    expected=[];actual=[];errors=[];subs=[];count=0
    for s in index.split(b'\0'):
        if not s:continue
        meta,path=s.split(b'\t');mode,oid,stage=meta.split()
        actual.append((path,mode,oid,stage))
    for s in tree.split(b'\0'):
        if not s:continue
        meta,path=s.split(b'\t');mode,typ,oid=meta.split();name=os.fsdecode(path)
        expected.append((path,mode,oid,b'0'));p=root/name
        if mode==b'160000':
            initialized=(p/'.git').exists()
            sub={'path':name,'gitlink':oid.decode(),'initialized':initialized}
            if initialized:
                sub['head']=git(p,'rev-parse','HEAD').decode().strip()
                sub['matches_pin']=sub['head']==oid.decode()
                sub['verification']=verify(p,oid.decode())
                if not sub['matches_pin'] or sub['verification']['errors']:errors.append(name+': submodule mismatch')
            subs.append(sub);continue
        try:
            st=p.lstat()
            if mode==b'120000':
                data=os.fsencode(os.readlink(p));goodmode=stat.S_ISLNK(st.st_mode)
            else:
                data=p.read_bytes();goodmode=stat.S_ISREG(st.st_mode) and bool(st.st_mode&0o111)==(mode==b'100755')
            digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if digest!=oid.decode() or not goodmode:errors.append(name+': bytes or mode differ')
        except OSError:errors.append(name+': missing or unreadable')
        count+=1
    if sorted(expected)!=sorted(actual):errors.append('index differs from tree')
    return {'commit':commit,'tree':git(root,'rev-parse',commit+'^{tree}').decode().strip(),'tracked_files_verified':count,'index_entries':len(actual),'index_equal':sorted(expected)==sorted(actual),'errors':errors,'submodules':subs}

d=verify(repo,'b522bb923fa59581478460b61633bce2cb90ac1d')
d['head']=git(repo,'rev-parse','HEAD').decode().strip();d['status']=git(repo,'status','--porcelain=v1').decode()
d['diff_names']=git(repo,'diff','--name-status','c20c85bd','HEAD').decode().splitlines()
Path(sys.argv[2]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d))
assert not d['errors'] and d['head']==d['commit'] and d['tree']=='66bd4852a98ca1065549515aa3c677d2fe482132'

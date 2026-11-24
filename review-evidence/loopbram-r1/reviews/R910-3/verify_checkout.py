#!/usr/bin/env python3
"""Verify tracked bytes and executable modes directly, plus index and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root, out = (Path(p).resolve() for p in sys.argv[1:3])
def git(where,*args):
    return subprocess.check_output(['git',*args],cwd=where)
def verify(where):
    entries={}
    for record in git(where,'ls-tree','-rz','HEAD').split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        entries[name]=(mode,oid)
    index={}
    for record in git(where,'ls-files','--stage','-z').split(b'\0'):
        if not record: continue
        meta,name=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        assert stage=='0'
        index[name]=(mode,oid)
    assert index==entries, 'index differs from HEAD'
    checked=0
    for name,(mode,oid) in entries.items():
        if mode=='160000': continue
        file=where/os.fsdecode(name)
        info=file.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(info.st_mode)
            data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode)
            actual='100755' if info.st_mode & 0o111 else '100644'
            assert actual==mode, os.fsdecode(name)
            data=file.read_bytes()
        measured=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert measured==oid, os.fsdecode(name)
        checked+=1
    return dict(head=git(where,'rev-parse','HEAD').decode().strip(),tree=git(where,'rev-parse','HEAD^{tree}').decode().strip(),tracked_blobs_verified=checked,index_matches=True,byte_and_mode_mismatches=0)
result={'root':verify(root),'submodules':{}}
for path in ('third_party/verilog-axis','protocol-processor','gptp-processor','third_party/tsn-c-stack'):
    pin=git(root,'rev-parse','HEAD:'+path).decode().strip()
    child=verify(root/path)
    assert child['head']==pin,path
    result['submodules'][path]=child
assert result['root']['head']=='9acb9b828b29aba71bd51303a4836f86c2278267'
result['status']=git(root,'status','--porcelain=v1').decode()
assert result['status']=='',result['status']
(out/'checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

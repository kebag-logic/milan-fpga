#!/usr/bin/env python3
"""Verify tracked bytes, executable bits, raw index entries, and required pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
HEAD='97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab'
BASE='a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(r,*args):
    return subprocess.check_output(['git','-C',str(r),*args],env=env)
def verify(r,commit):
    entries={}
    for row in git(r,'ls-tree','-rz',commit).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();entries[os.fsdecode(path)]=(mode,oid)
    index={}
    for row in git(r,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0'
        name=os.fsdecode(path);assert name not in index;index[name]=(mode,oid)
    assert entries==index,'index mismatch'
    n=0
    for name,(mode,oid) in entries.items():
        if mode=='160000':continue
        p=r/name;st=p.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(st.st_mode),name;data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode&stat.S_IXUSR)==(mode=='100755'),name
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,name;n+=1
    return entries,n
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
entries,n=verify(root,HEAD)
print('HEAD',HEAD)
print('TREE',git(root,'rev-parse','HEAD^{tree}').decode().strip())
print('SUPERPROJECT tracked blobs/modes verified',n,'index entries',len(entries))
base_links=git(root,'ls-tree','-r',BASE).decode().splitlines()
for name,(mode,oid) in entries.items():
    if mode!='160000':continue
    assert f'160000 commit {oid}\t{name}' in base_links
    print('UNCHANGED GITLINK',name,oid)
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    pin=entries[name][1]
    assert git(root/name,'rev-parse','HEAD').decode().strip()==pin
    _,count=verify(root/name,pin)
    print('REQUIRED SUBMODULE',name,'tracked blobs/modes/index verified',count)
changed=git(root,'diff','--name-only',BASE,HEAD).decode().splitlines()
assert len(changed)==8
assert all(x.startswith(('.github/workflows/','scripts/')) or x=='docs/testing/CI_WORKFLOWS.md' for x in changed)
print('CHANGED PATHS',json.dumps(changed))
print('RTL, firmware, configs, build inputs, interface authorities, and all gitlinks unchanged')
print('STATUS',git(root,'status','--short').decode().strip() or 'clean')
print('PASS')

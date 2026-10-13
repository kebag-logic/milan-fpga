#!/usr/bin/env python3
"""Compare raw tracked bytes, kinds, modes, index records and submodule pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
args=p.parse_args()
repo=args.repo.resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def check(root, revision):
    entries={}
    for row in git(root,'ls-tree','-rz',revision).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1)
        mode,kind,oid=meta.split()
        entries[name]=(mode,kind,oid)
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0',(root,name,'unmerged index')
        assert name not in index,(root,name,'duplicate index')
        index[name]=(mode,oid)
    assert index=={n:(m,o) for n,(m,k,o) in entries.items()},str(root)+' index differs'
    checked=0
    for name,(mode,kind,oid) in entries.items():
        if kind==b'commit':continue
        path=root/os.fsdecode(name)
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),str(path)
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),str(path)
            executable=bool(st.st_mode & 0o111)
            assert executable==(mode==b'100755'),str(path)+' mode'
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,str(path)+' bytes'
        checked+=1
    return {'revision':revision,'raw_blob_and_mode_matches':checked,'index_matches':len(index),
            'gitlinks':{os.fsdecode(n):o.decode() for n,(m,k,o) in entries.items() if k==b'commit'}}
head=git(repo,'rev-parse','HEAD').decode().strip()
assert head=='db29bdd07529fbc697b7956827092f64b1241714'
tree=git(repo,'rev-parse','HEAD^{tree}').decode().strip()
assert tree=='8102aa501042b366c2a8abb5a1555fde4eaac2bf'
records={'head':head,'tree':tree,'parent':git(repo,'rev-parse','HEAD^').decode().strip(),'repositories':{}}
records['repositories']['parent']=check(repo,head)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack']:
    pin=records['repositories']['parent']['gitlinks'][name]
    assert git(repo/name,'rev-parse','HEAD').decode().strip()==pin
    records['repositories'][name]=check(repo/name,pin)
records['status_porcelain']=git(repo,'status','--porcelain=v1').decode()
assert not records['status_porcelain']
(args.packet/'integrity-final.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))

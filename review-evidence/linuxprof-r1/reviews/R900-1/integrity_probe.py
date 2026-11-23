#!/usr/bin/env python3
"""Verify exact tracked bytes, filesystem modes, index entries and submodule pins.

Usage: python3 integrity_probe.py REPO PACKET
Does not rely on status or diff to detect hidden tracked modifications.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
expected='677d605f37c3a80654df1dd2cde053b57242845b'
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'}
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def audit(root,rev):
    assert git(root,'rev-parse','HEAD').decode().strip()==rev
    tree={}
    for entry in git(root,'ls-tree','-rz',rev).split(b'\0'):
        if not entry:continue
        info,name=entry.split(b'\t',1)
        mode,kind,oid=info.split()
        tree[name]=(mode,oid)
        path=root/os.fsdecode(name)
        if mode==b'160000':continue
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),path
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),path
            actual=b'100755' if st.st_mode&0o111 else b'100644'
            assert actual==mode,(path,actual,mode)
            data=path.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==oid,(path,got,oid)
    index={}
    for entry in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not entry:continue
        info,name=entry.split(b'\t',1)
        mode,oid,stage=info.split()
        assert stage==b'0' and name not in index,(root,name,stage)
        index[name]=(mode,oid)
    assert index==tree,root
    return dict(revision=rev,tree=git(root,'rev-parse',rev+'^{tree}').decode().strip(),
                tracked_entries=len(tree),raw_bytes_modes_and_index='PASS'),tree
root_result,tree=audit(repo,expected)
assert root_result['tree']=='79d523167a95861b8092b64574222db91bce5a07'
results={'superproject':root_result,'submodules':{}}
for path in sorted(required):
    mode,oid=tree[os.fsencode(path)]
    assert mode==b'160000'
    assert (repo/path/'.git').is_file(),path
    result,_=audit(repo/path,oid.decode())
    results['submodules'][path]=result
results['external']='Gitlink unchanged; intentionally uninitialized and not used.'
results['status']=git(repo,'status','--porcelain=v1').decode()
results['index_flags']=git(repo,'ls-files','-v').decode().splitlines()
assert not [line for line in results['index_flags'] if not line.startswith('H ')]
results['index_flags']='all H: no assume-unchanged or skip-worktree'
assert not results['status'],results['status']
(packet/'integrity-result.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))

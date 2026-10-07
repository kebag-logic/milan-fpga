#!/usr/bin/env python3
"""Verify tracked bytes, executable/symlink modes, indexes and required pins."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

HEAD='c1049de1970e93d2c36ace62891ee9d947cd3191'
TREE='168564db27f588e2eaf34d2fa3ff54947eecd00d'
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(); root=a.repo.resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def audit(repo,revision):
    entries={}
    for row in git(repo,'ls-tree','-rz',revision).split(b'\0'):
        if not row: continue
        fields,path=row.split(b'\t',1); mode,kind,oid=fields.decode().split()
        entries[path.decode()]=(mode,kind,oid)
    index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        fields,path=row.split(b'\t',1); mode,oid,stage=fields.decode().split()
        assert stage=='0' and path.decode() not in index, ('index-stage',path)
        index[path.decode()]=(mode,oid)
    assert index=={path:(mode,oid) for path,(mode,kind,oid) in entries.items()}, 'index differs from recorded tree'
    for row in git(repo,'ls-files','-v','-z').split(b'\0'):
        if row: assert row[:1]==b'H', ('hidden-index-flag',row)
    blobs=0; links={}
    for name,(mode,kind,oid) in entries.items():
        if mode=='160000':
            links[name]=oid
            continue
        f=repo/name
        for parent in f.parents:
            if parent==repo: break
            assert not parent.is_symlink(), ('symlink-parent',name)
        s=f.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode), name
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111)==(mode=='100755'), ('executable-mode',name)
            data=f.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid, ('blob-bytes',name)
        blobs+=1
    status=git(repo,'status','--porcelain=v1','--untracked-files=all').decode()
    assert not status, ('status',status)
    return {'head':git(repo,'rev-parse','HEAD').decode().strip(),
            'tree':git(repo,'rev-parse',revision+'^{tree}').decode().strip(),
            'tracked_blobs_verified':blobs,'index_entries_verified':len(index),
            'gitlinks':links,'status':status}
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
result={'parent':audit(root,HEAD),'submodules':{}}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP'):
    pin=result['parent']['gitlinks'][name]
    sub=root/name
    assert git(sub,'rev-parse','HEAD').decode().strip()==pin, ('pin',name)
    assert (sub/'.git').is_file(), ('registered-submodule',name)
    result['submodules'][name]=audit(sub,pin)
result['result']='PASS'
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

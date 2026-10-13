#!/usr/bin/env python3
"""Verify raw tracked bytes/modes, stage-zero index, and required gitlinks."""
import argparse
import hashlib
import os
import stat
import subprocess
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--repo',required=True,type=Path)
a=p.parse_args(); root=a.repo.resolve()
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(repo,*args):
    return subprocess.check_output(['git','-c','core.commitGraph=false',*args],cwd=repo,env=env)
def verify(repo,rev,label):
    tree={}
    for row in git(repo,'ls-tree','-rz',rev).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);mode,kind,oid=meta.split()
        tree[path]=(mode,oid)
        if kind==b'commit': continue
        f=repo/os.fsdecode(path); info=f.lstat()
        if stat.S_ISLNK(info.st_mode):
            actual_mode=b'120000';data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(info.st_mode),(label,path,'not regular')
            actual_mode=b'100755' if info.st_mode & 0o111 else b'100644'
            data=f.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual_mode==mode and digest==oid,(label,path,'bytes/mode mismatch')
    index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0' and path not in index,(label,path,'index stage')
        index[path]=(mode,oid)
    assert index==tree,(label,'index differs from head')
    hidden=[row for row in git(repo,'ls-files','-v','-z').split(b'\0') if row and row[:1]!=b'H']
    assert not hidden,(label,'hidden index flags',hidden)
    status=git(repo,'status','--porcelain=v1','--untracked-files=all')
    assert not status,(label,'status',status)
    blobs=sum(1 for mode,oid in tree.values() if mode!=b'160000')
    print(f'PASS {label}: {blobs} raw blobs, modes, stage-zero index, no hidden flags, clean status')
    return tree

head='b89a1ded1596030c4e0baf45a8509a20cbe04933'
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='7aa454c189276935ebf891dc9deb5250a35aaa24'
detached=subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=root,env=env,capture_output=True)
assert detached.returncode==1
print('PASS detached exact head',head,'tree 7aa454c189276935ebf891dc9deb5250a35aaa24')
tree=verify(root,head,'candidate')
required=['protocol-processor','gptp-processor','third_party/verilog-axis']
for name in required:
    sub=root/name; mode,pin=tree[os.fsencode(name)]
    assert mode==b'160000' and not sub.is_symlink()
    assert (sub/'.git').is_file() and not (sub/'.git').is_symlink()
    assert git(sub,'rev-parse','HEAD').strip()==pin
    parent=git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()
    assert Path(parent).resolve()==root
    print('PASS registered required gitlink',name,pin.decode())
    verify(sub,pin.decode(),name)
for name in ['external','third_party/lwSRP']:
    mode,pin=tree[os.fsencode(name)]
    print('Recorded uninitialized gitlink outside executed checks:',name,mode.decode(),pin.decode())
print('PASS final integrity; candidate source bytes were never edited')

#!/usr/bin/env python3
"""Verify every tracked byte, executable bit, index entry and required gitlink."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
head='7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783'
tree='2f8dac43d7c0efd0350b328818d89dc1cbebca47'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')

def git(repo,*args):
    return subprocess.check_output(['git',*args],cwd=repo,env=env)

def verify(repo, rev, label):
    assert git(repo,'rev-parse','HEAD').decode().strip()==rev
    expected={}
    gitlinks={}
    blobs=0
    for rec in git(repo,'ls-tree','-rz',rev).split(b'\0'):
        if not rec: continue
        meta,name=rec.split(b'\t',1)
        mode,kind,oid=meta.split()
        expected[name]=(mode,oid,b'0')
        file=repo/os.fsdecode(name)
        if kind==b'commit':
            gitlinks[os.fsdecode(name)]=oid.decode()
            continue
        st=file.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),name
            data=file.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,(label,name,'blob mismatch')
        blobs+=1
    index={}
    for rec in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not rec: continue
        meta,name=rec.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert name not in index,(name,'multiple stages')
        index[name]=(mode,oid,stage)
    assert expected==index,label+' index mismatch'
    print(label,'PASS',rev,'blobs='+str(blobs),'index='+str(len(index)))
    return gitlinks

assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==tree
links=verify(root,head,'parent')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    assert (root/name/'.git').is_file(),name+' not a registered submodule'
    verify(root/name,links[name],name)
changed=git(root,'diff','--name-only','5603c353137e90c1fa95429f6d00ef7a2298d9ee',head).decode().splitlines()
assert changed==['docs/design/AREA_BUDGET.md','docs/design/MARK_II_AREA_PLAN.md']
print('tree',tree,'PASS; only the two authorized documentation files changed')
print('External and lwSRP gitlinks checked in parent index; their uninitialized worktrees are outside this review.')

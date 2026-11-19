#!/usr/bin/env python3
"""Verify physical tracked bytes, modes, index and required submodule gitlinks."""
from pathlib import Path
import hashlib
import os
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = '0d1eb8e4c5821e9431097950882659f2083d96ba'
required = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'third_party/tsn-c-stack', 'third_party/lwSRP')

def git(repo, *args):
    return subprocess.check_output(['git','-C',str(repo),*args])

def verify(repo, label, head):
    assert git(repo,'rev-parse','HEAD').decode().strip() == head
    entries = {}
    for record in git(repo,'ls-tree','-rz',head).split(b'\0'):
        if not record:
            continue
        meta, path = record.split(b'\t',1)
        mode, kind, oid = meta.decode().split()
        entries[path] = (mode,oid)
        if kind == 'commit':
            continue
        p=repo/os.fsdecode(path)
        st=p.lstat()
        if stat.S_ISLNK(st.st_mode):
            actual_mode='120000'
            content=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode), path
            actual_mode='100755' if st.st_mode & 0o111 else '100644'
            content=p.read_bytes()
        actual_hash=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        assert (actual_mode,actual_hash)==(mode,oid), path
    index={}
    for record in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not record:
            continue
        meta,path=record.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        assert stage=='0'
        index[path]=(mode,oid)
    assert index==entries, label+' index mismatch'
    print(label, head, len(entries), 'tracked entries: physical bytes/modes/index PASS')
    return entries

entries=verify(root,'candidate',expected)
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='d1ec05dff82782f478eaddde89b396c0c070422c'
for sub in required:
    mode,oid=entries[os.fsencode(sub)]
    assert mode=='160000' and (root/sub/'.git').exists()
    verify(root/sub,sub,oid)
print('Optional external submodule is uninitialized; no review test reads it.')
print('RESULT PASS')

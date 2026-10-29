#!/usr/bin/env python3
"""Verify raw tracked bytes, executable/symlink modes, index and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
head = 'f884c7e9fb71cdb94c12e3228b1412801c34e1f4'
tree = '40ee92bf67435d4a2dd31ab2373ad05c9bdf24f5'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(where, *args):
    return subprocess.check_output(['git','-C',str(where),*args], env=env)
def verify(where, expected):
    assert git(where,'rev-parse','HEAD').decode().strip() == expected
    entries = {}
    links = {}
    count = 0
    for entry in git(where,'ls-tree','-rz','HEAD').split(b'\0'):
        if not entry: continue
        metadata, name = entry.split(b'\t',1)
        mode, kind, oid = metadata.decode().split()
        name = os.fsdecode(name)
        entries[name] = (mode,oid,'0')
        path = where/name
        if kind == 'commit':
            links[name] = oid
            continue
        info = path.lstat()
        actual_mode = '120000' if stat.S_ISLNK(info.st_mode) else ('100755' if info.st_mode & 0o111 else '100644')
        assert actual_mode == mode, (path,'mode',actual_mode,mode)
        data = os.fsencode(os.readlink(path)) if mode == '120000' else path.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual == oid, (path,'blob mismatch')
        count += 1
    index = {}
    for entry in git(where,'ls-files','--stage','-z').split(b'\0'):
        if not entry: continue
        metadata, name = entry.split(b'\t',1)
        index[os.fsdecode(name)] = tuple(metadata.decode().split())
    assert index == entries, (where,'index differs from HEAD')
    flags = git(where,'ls-files','-v','-z').split(b'\0')
    assert all(not item or item[:1] == b'H' for item in flags), (where,'index flags')
    print(where.name, expected, count, 'tracked blobs/modes and complete index PASS')
    for name, oid in links.items(): print('gitlink',name,oid)
    return links
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == tree
links = verify(root,head)
required = ['gptp-processor','protocol-processor','third_party/lwSRP','third_party/tsn-c-stack','third_party/verilog-axis']
for name in required:
    verify(root/name, links[name])
print('external gitlink verified in HEAD/index; external worktree not initialized or required for these probes')
status = git(root,'status','--porcelain=v1','--untracked-files=all').decode()
assert not status, status
print('Parent status empty; required submodule bytes/modes/index verified; exact head/tree retained')
print(subprocess.check_output(['$VALIDATION_TOOLS/pinned-verilator-5.050/verilator','--version'],text=True).strip())

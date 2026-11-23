#!/usr/bin/env python3
"""Prove raw tracked bytes, executable modes, index and required gitlinks."""
from pathlib import Path
import hashlib
import os
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(path,*args):
    return subprocess.check_output(['git','-C',str(path),*args],env=env)
def verify(path,revision):
    tree = git(path,'rev-parse',revision+'^{tree}').decode().strip()
    assert git(path,'write-tree').decode().strip() == tree, str(path)+' index differs'
    count = 0
    links = []
    for record in git(path,'ls-tree','-rz',revision).split(b'\0'):
        if not record:
            continue
        attrs,name = record.split(b'\t',1)
        mode,kind,oid = attrs.decode().split()
        item = path/os.fsdecode(name)
        if kind == 'commit':
            links.append((os.fsdecode(name),oid))
            continue
        info = item.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(item))
        else:
            assert stat.S_ISREG(info.st_mode), str(item)
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == '100755'), str(item)
            data = item.read_bytes()
        measured = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert measured == oid, str(item)+' bytes differ'
        count += 1
    return tree,count,links
head = git(root,'rev-parse','HEAD').decode().strip()
assert head == '8267b8951616cfd570baf690835d4b0d38f14596'
tree,count,links = verify(root,head)
assert tree == 'b8f11886504b95ab3f48d7553de8ef173d2a67cd'
print('Head:',head)
print('Tree:',tree)
print('Parent tracked blob bytes/modes and index:',count,'PASS')
for name,pin in links:
    if name == 'external':
        print('external gitlink:',pin,'uninitialized; no scoped test dependency')
        continue
    path = root/name
    assert (path/'.git').is_file(), name+' is not registered submodule'
    assert git(path,'rev-parse','HEAD').decode().strip() == pin, name
    assert Path(git(path,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve() == root
    _,count,_ = verify(path,pin)
    print(name,pin,':',count,'blob bytes/modes and index PASS')
status = git(root,'status','--porcelain').decode()
print('Status:',status or 'clean')
assert not status

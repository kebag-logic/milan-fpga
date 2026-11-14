#!/usr/bin/env python3
"""Usage: verify_checkout.py CHECKOUT. Verify raw blobs, modes, index and gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
head='8e523a2b17faf17c4564e5af155b73f95dc2a0a5'
def git(tree,*args):
    return subprocess.check_output(['git','-C',str(tree),*args],env=env)
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='2c53a871df1f717ba7cb72f77147c549155beed5'
def check(tree, rev, label):
    entries=git(tree,'ls-tree','-rz',rev).split(b'\0')
    expected={}; count=0; links={}
    for entry in entries:
        if not entry: continue
        meta,name=entry.split(b'\t',1); mode,kind,sha=meta.split()
        expected[name]=(mode,sha)
        if kind==b'commit': links[os.fsdecode(name)]=sha.decode(); continue
        f=tree/os.fsdecode(name); st=f.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode&0o111)==(mode==b'100755'),name
            data=f.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==sha,name
        count+=1
    actual={}
    for entry in git(tree,'ls-files','--stage','-z').split(b'\0'):
        if not entry: continue
        meta,name=entry.split(b'\t',1); mode,sha,stage=meta.split()
        assert stage==b'0' and name not in actual,name
        actual[name]=(mode,sha)
    assert actual==expected,label+' index mismatch'
    print(label,rev,':',count,'raw blobs/modes verified; index equals commit')
    return links
links=check(root,head,'superproject')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']:
    tree=root/name; pin=links[name]
    assert (tree/'.git').is_file() and not tree.is_symlink(),name
    assert git(tree,'rev-parse','HEAD').decode().strip()==pin,name
    assert Path(git(tree,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==root.resolve(),name
    check(tree,pin,name)
print('PASS: exact head, tree, tracked bytes/modes/index and four required submodule gitlinks.')

#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and gitlinks against the reviewed commit.

Arguments: checkout path. Submodule initialization is reported, never changed.
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

root=Path(sys.argv[1]);env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
head='867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='a5f405e02461121570f89d27955e245269ed87d2'
tree=git('ls-tree','-rz',head);expected={};blobs=0;pins={}
for row in tree.split(b'\0'):
    if not row:continue
    info,name=row.split(b'\t',1);mode,kind,oid=info.split();expected[name]=(mode,oid)
    path=root/os.fsdecode(name)
    if mode==b'160000':
        pins[os.fsdecode(name)]={'pin':oid.decode(),'initialized':(path/'.git').exists()};continue
    st=path.lstat()
    if mode==b'120000':assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
    else:
        assert stat.S_ISREG(st.st_mode),name
        assert bool(st.st_mode&0o111)==(mode==b'100755'),name
        data=path.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
    assert got==oid,name
    blobs+=1
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if not row:continue
    info,name=row.split(b'\t',1);mode,oid,stage=info.split();assert stage==b'0'
    index[name]=(mode,oid)
assert index==expected
assert git('diff','--name-only')==b''
assert git('diff','--cached','--name-only')==b''
needed={'protocol-processor':'2ad2f845dd583f8310075fa2380cb60a04fd091a',
        'gptp-processor':'e4869fd0c42889b2ac806587cc5c78afb1c33461',
        'third_party/verilog-axis':'48ff7a7e2ef782cf778d47910cf85835c64b1bce',
        'third_party/tsn-c-stack':'70936b77dc41981e192438388cd0aced69954f18'}
for name,pin in needed.items():assert pins[name]['pin']==pin
print(json.dumps({'head':head,'tree':'a5f405e02461121570f89d27955e245269ed87d2','verified_blobs':blobs,
 'tracked_modes_equal':True,'index_equal':True,'required_gitlinks':{k:pins[k] for k in needed},
 'all_gitlinks':pins,'tracked_tree_inventory_sha256':hashlib.sha256(tree).hexdigest()},indent=2))

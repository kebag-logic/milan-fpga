#!/usr/bin/env python3
"""Verify HEAD, index, every tracked blob's bytes/mode, and any gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
packet=Path(__file__).resolve().parent
head='6ddfcda4c3170b8f463c8623833f7541ca8c1faf'
tree='45faa5d3bd449cc0d8f8bee77f186d5e0c73022c'
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
assert git('write-tree').decode().strip()==tree
rows=[];links=[]
for raw in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not raw:continue
    meta,name=raw.split(b'\t',1); mode,kind,oid=meta.decode().split()
    rel=os.fsdecode(name);path=root/rel
    if kind=='commit':
        actual=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
        assert actual==oid,(rel,actual,oid)
        links.append(f'{mode} {oid} {rel}')
        continue
    st=path.lstat()
    if mode=='120000':
        assert stat.S_ISLNK(st.st_mode)
        data=os.fsencode(os.readlink(path))
    else:
        assert stat.S_ISREG(st.st_mode)
        assert bool(st.st_mode&0o111)==(mode=='100755'),rel
        data=path.read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert digest==oid,(rel,digest,oid)
    rows.append(f'{mode} {oid} {rel}')
assert not git('status','--porcelain','--untracked-files=all')
text=f'HEAD {head}\nTREE {tree}\nINDEX {tree}\n'
text+=f'Tracked blobs checked byte-for-byte with modes: {len(rows)}\n'
text+=f'Required gitlinks in processor tree: {len(links)}\n'
text+='\n'.join(links)+'\nClean tracked/index/untracked state: PASS\n'
(packet/'source-integrity.txt').write_text(text)
(packet/'tracked-blobs.txt').write_text('\n'.join(rows+links)+'\n')
print(text)

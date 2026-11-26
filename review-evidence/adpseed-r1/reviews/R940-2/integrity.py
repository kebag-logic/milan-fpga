#!/usr/bin/env python3
"""Verify exact tracked blob bytes, modes, index and gitlinks. Usage: integrity.py SOURCE PACKET."""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys

source,packet=map(lambda p:Path(p).resolve(),sys.argv[1:])
head='9590206015ead2cfd2ef955c2f4ef8d8c4e4762c'
tree='4064709bec5ebb15b18f16b13a5bae94688a4d56'
def git(*args):
    return subprocess.check_output(['git','-C',str(source),*args])
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
assert git('write-tree').decode().strip()==tree
rows=[]; links=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not row: continue
    metadata,name=row.split(b'\t'); mode,kind,oid=metadata.decode().split()
    name=name.decode(); path=source/name
    if kind=='commit':
        links.append(dict(path=name,oid=oid))
        assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD']).decode().strip()==oid
        continue
    content=os.readlink(path).encode() if mode=='120000' else path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
    assert actual==oid,name
    if mode!='120000': assert bool(path.stat().st_mode&stat.S_IXUSR)==(mode=='100755'),name
    rows.append(dict(path=name,mode=mode,blob=actual))
status=git('status','--porcelain=v1','--untracked-files=all').decode()
assert not status,status
result=dict(head=head,tree=tree,index_tree=tree,tracked_files=len(rows),mismatches=0,gitlinks=links,status=status,files=rows)
(packet/'receipts/integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'{len(rows)} tracked files verified; no mismatches; {len(links)} gitlinks; clean index and worktree')

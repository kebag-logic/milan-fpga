#!/usr/bin/env python3
"""Verify tracked bytes, modes, index, and required submodule gitlinks against HEAD."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1])
def git(where,*args):
    return subprocess.check_output(['git','-C',str(where),*args])
def check(where):
    failures=[]; checked=0; links={}
    head=git(where,'rev-parse','HEAD').decode().strip()
    for item in git(where,'ls-tree','-rz','--full-tree','HEAD').split(b'\0'):
        if not item: continue
        meta,name=item.split(b'\t',1); mode,kind,oid=meta.decode().split(); p=where/os.fsdecode(name)
        if kind=='commit': links[os.fsdecode(name)]=oid; continue
        data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        actual='120000' if p.is_symlink() else '100755' if p.stat().st_mode&0o111 else '100644'
        checked+=1
        if digest!=oid or mode!=actual: failures.append(os.fsdecode(name))
    index=git(where,'diff','--cached','--name-only','HEAD').decode().strip()
    print('TREE',where.name,head,'files',checked,'byte/mode failures',failures,'index differences',index or 'none')
    assert not failures and not index
    return links
links=check(root)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    sub=root/name
    actual=git(sub,'rev-parse','HEAD').decode().strip()
    print('GITLINK',name,links[name],actual,'MATCH' if actual==links[name] else 'MISMATCH')
    assert actual==links[name]
    check(sub)
print('HEAD tree',git(root,'rev-parse','HEAD^{tree}').decode().strip())
print('STATUS',git(root,'status','--porcelain=v2').decode().strip() or 'clean')
print('Archive signature status',git(root,'log','-1','--format=%H %G?','50e931db').decode().strip())

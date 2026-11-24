#!/usr/bin/env python3
"""Check tracked bytes, modes, index and required submodule gitlinks directly."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root):
    head=git(root,'rev-parse','HEAD').decode().strip()
    tree=git(root,'rev-parse','HEAD^{tree}').decode().strip()
    expected={}
    links={}
    errors=[]
    for entry in git(root,'ls-tree','-rz','HEAD').split(b'\0'):
        if not entry: continue
        meta,path=entry.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        name=os.fsdecode(path)
        expected[name]=(mode,oid,'0')
        if kind=='commit': links[name]=oid; continue
        f=root/name
        try:
            st=f.lstat()
            if mode=='120000':
                assert f.is_symlink()
                data=os.fsencode(os.readlink(f))
            else:
                assert f.is_file() and not f.is_symlink()
                assert bool(st.st_mode & 0o111)==(mode=='100755')
                data=f.read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if blob!=oid: errors.append([name,'blob mismatch'])
        except (OSError,AssertionError): errors.append([name,'missing or mode mismatch'])
    actual={}
    for entry in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not entry: continue
        meta,path=entry.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        actual[os.fsdecode(path)]=(mode,oid,stage)
    if actual!=expected: errors.append(['index','not equal to HEAD tree'])
    return dict(head=head,tree=tree,entries=len(expected),errors=errors,gitlinks=links)
root=a.checkout.resolve()
result={'parent':verify(root),'submodules':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']:
    r=verify(root/name)
    r['matches_parent_gitlink']=r['head']==result['parent']['gitlinks'][name]
    r['registered_submodule']=bool(git(root/name,'rev-parse','--show-superproject-working-tree').strip())
    result['submodules'][name]=r
a.output.write_text(json.dumps(result,indent=2)+'\n')
assert not result['parent']['errors']
assert all(not r['errors'] and r['matches_parent_gitlink'] and r['registered_submodule']
           for r in result['submodules'].values())
print('PASS tracked blob bytes, modes, index, and four registered submodule pins')

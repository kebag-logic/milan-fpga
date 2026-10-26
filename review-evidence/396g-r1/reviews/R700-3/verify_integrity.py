#!/usr/bin/env python3
"""Verify raw tracked bytes, modes and index independently of status flags."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
expected='4d69e1923ce8209029af6e084336f13cca834c29'
required=['third_party/verilog-axis','protocol-processor','gptp-processor','third_party/tsn-c-stack']
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(path,*args):
    return subprocess.check_output(['git','-C',str(path),*args],env=env)
def verify(path,pin):
    errors=[]; blobs=0; links={}; tree={}
    for rec in git(path,'ls-tree','-rz','--full-tree',pin).split(b'\0'):
        if not rec: continue
        meta,name=rec.split(b'\t',1); mode,kind,oid=meta.decode().split()
        tree[name]=(mode,oid)
        if mode=='160000': links[os.fsdecode(name)]=oid; continue
        p=path/os.fsdecode(name)
        try:
            s=p.lstat()
            if mode=='120000':
                assert stat.S_ISLNK(s.st_mode),'expected symlink'
                raw=os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(s.st_mode),'expected regular file'
                assert bool(s.st_mode&0o111)==(mode=='100755'),'mode differs'
                raw=p.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            assert actual==oid,'blob differs'
            blobs+=1
        except (OSError,AssertionError) as e: errors.append([os.fsdecode(name),str(e)])
    index={}
    for rec in git(path,'ls-files','--stage','-z').split(b'\0'):
        if not rec: continue
        meta,name=rec.split(b'\t',1); mode,oid,stage=meta.decode().split()
        if stage!='0': errors.append([os.fsdecode(name),'unmerged index'])
        index[name]=(mode,oid)
    if index!=tree: errors.append(['index','entries differ from pinned tree'])
    actual_head=git(path,'rev-parse','HEAD').decode().strip()
    if actual_head!=pin: errors.append(['HEAD','not the expected pin'])
    return dict(head=actual_head,tree=git(path,'rev-parse',pin+'^{tree}').decode().strip(),
                blobs_verified=blobs,index_entries=len(index),gitlinks=links,errors=errors)

result={'root':verify(root,expected),'required_submodules':{}}
for name in required:
    p=root/name
    pin=result['root']['gitlinks'][name]
    r=verify(p,pin)
    r['expected_gitlink']=pin
    r['registered_gitfile']=(p/'.git').is_file()
    if not r['registered_gitfile']: r['errors'].append(['.git','not registered submodule gitfile'])
    r['superproject_matches']=git(p,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
    if not r['superproject_matches']: r['errors'].append(['superproject','mismatch'])
    result['required_submodules'][name]=r
result['status_porcelain']=git(root,'status','--porcelain=v1').decode()
result['result']='PASS' if not result['root']['errors'] and all(not r['errors'] for r in result['required_submodules'].values()) else 'FAIL'
(out/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(result['result']!='PASS')

#!/usr/bin/env python3
"""Prove tracked bytes, file modes, index entries and required gitlinks directly."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(directory,*args):return subprocess.check_output(['git','-C',str(directory),*args],env=env)
def verify(directory,revision):
    entries=[];bad=[];links=[]
    for record in git(directory,'ls-tree','-rz',revision).split(b'\0'):
        if not record:continue
        info,name=record.split(b'\t',1);mode,kind,oid=info.decode().split();name=os.fsdecode(name)
        entries.append((mode,oid,'0',name))
        if mode=='160000':links.append((name,oid));continue
        p=directory/name
        try:
            st=p.lstat()
            if mode=='120000':
                assert stat.S_ISLNK(st.st_mode)
                data=os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode&0o111)==(mode=='100755')
                data=p.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if actual!=oid:bad.append([name,'blob'])
        except (OSError,AssertionError):bad.append([name,'missing or mode'])
    index=[]
    for record in git(directory,'ls-files','--stage','-z').split(b'\0'):
        if record:
            info,name=record.split(b'\t',1);mode,oid,stage=info.decode().split();index.append((mode,oid,stage,os.fsdecode(name)))
    if sorted(entries)!=sorted(index):bad.append(['INDEX','tree mismatch'])
    return {'revision':revision,'tracked_blobs':len(entries)-len(links),'index_matches':sorted(entries)==sorted(index),'failures':bad,'gitlinks':dict(links)}
head='701f294405d47a81eed1079d32b54e1eea4a4f31'
out={'head':git(root,'rev-parse','HEAD').decode().strip(),'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'parent':verify(root,head),'submodules':{}}
for name,pin in out['parent']['gitlinks'].items():
    path=root/name
    if name=='external' and not (path/'.git').exists():
        out['submodules'][name]={'gitlink':pin,'unpopulated':True};continue
    actual=git(path,'rev-parse','HEAD').decode().strip()
    result=verify(path,pin);result['head']=actual;result['registered_git_directory']=(path/'.git').is_file();result['head_matches_pin']=actual==pin
    out['submodules'][name]=result
(packet/'tree-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['head']==head and not out['parent']['failures']
assert all(v.get('unpopulated') or (v['head_matches_pin'] and v['registered_git_directory'] and not v['failures']) for v in out['submodules'].values())

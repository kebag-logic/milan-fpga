#!/usr/bin/env python3
"""Prove tracked bytes, Git modes, index entries and required submodule pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))

def verify(root,revision):
    entries={}
    for record in git(root,'ls-tree','-rz',revision).split(b'\0'):
        if not record:continue
        meta,path=record.split(b'\t',1);mode,kind,oid=meta.decode().split();entries[path]=(mode,kind,oid)
    index={}
    for record in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        meta,path=record.split(b'\t',1);mode,oid,stage=meta.decode().split()
        assert stage=='0' and path not in index,(root,path,stage)
        index[path]=(mode,oid)
    assert set(index)==set(entries),'index population differs'
    count=0;links={}
    for path,(mode,kind,oid) in entries.items():
        assert index[path]==(mode,oid),(path,'index')
        p=root/os.fsdecode(path)
        if kind=='commit':links[os.fsdecode(path)]=oid;continue
        info=p.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(info.st_mode);data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(info.st_mode),(path,'not regular')
            assert bool(info.st_mode & 0o111)==(mode=='100755'),(path,'mode')
            data=p.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert got==oid,(path,'bytes')
        count+=1
    return dict(revision=revision,tree=git(root,'rev-parse',revision+'^{tree}').decode().strip(),blobs=count,gitlinks=links,index_equal=True,bytes_and_modes_equal=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);a=ap.parse_args();root=a.root.resolve()
    head=git(root,'rev-parse','HEAD').decode().strip()
    assert head=='e893e4d13d99eb5ba00745f0f5cf74ee847972c2'
    result={'parent':verify(root,head),'submodules':{}}
    for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
        p=root/name;expected=result['parent']['gitlinks'][name]
        assert (p/'.git').is_file(),'not a registered submodule'
        assert git(p,'rev-parse','HEAD').decode().strip()==expected
        assert Path(git(p,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==root
        result['submodules'][name]=verify(p,expected)
    result['status']=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
    result['ignored']=git(root,'ls-files','--others','--ignored','--exclude-standard').decode().splitlines()
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

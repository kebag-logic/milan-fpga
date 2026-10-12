#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and required gitlinks. Args: repo out.json."""
import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys

root=pathlib.Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def verify(repo,revision):
    rows=git(repo,'ls-tree','-rz',revision).split(b'\0')
    expected={};blobs=0;links=[]
    for row in rows:
        if not row:continue
        info,path=row.split(b'\t',1);mode,kind,oid=info.split()
        expected[path]=(mode,oid,b'0')
        full=repo/os.fsdecode(path)
        if kind==b'commit':links.append(dict(path=os.fsdecode(path),pin=oid.decode()));continue
        st=full.lstat()
        gotmode=b'120000' if stat.S_ISLNK(st.st_mode) else b'100755' if st.st_mode&0o111 else b'100644'
        assert gotmode==mode,(os.fsdecode(path),'mode')
        data=os.fsencode(os.readlink(full)) if gotmode==b'120000' else full.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==oid,(os.fsdecode(path),'bytes')
        blobs+=1
    actual={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        info,path=row.split(b'\t',1);mode,oid,stage=info.split()
        assert path not in actual,'multiple index stages'
        actual[path]=(mode,oid,stage)
    assert actual==expected,'index differs from tree'
    return dict(head=git(repo,'rev-parse','HEAD').decode().strip(),tree=git(repo,'rev-parse',revision+'^{tree}').decode().strip(),
                blobs_verified=blobs,index_equal=True,raw_bytes_and_modes_equal=True,gitlinks=links)
head='cb5ff79f1f69117efba353484851eceb620e5c92'
assert git(root,'rev-parse','HEAD').decode().strip()==head
result=verify(root,head)
result['required_submodules']={}
for name in ['third_party/verilog-axis','protocol-processor','gptp-processor']:
    pin=next(x['pin'] for x in result['gitlinks'] if x['path']==name)
    sub=root/name
    assert (sub/'.git').is_file(), 'submodule must be registered, not a copied directory'
    assert git(sub,'rev-parse','HEAD').decode().strip()==pin
    result['required_submodules'][name]=verify(sub,pin)
result['status_porcelain']=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status_porcelain']
result['changed_paths']=git(root,'diff','--name-only','c20c85bd',head).decode().splitlines()
assert result['changed_paths']==['docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md','docs/findings/README.md']
pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(head=head,blobs=result['blobs_verified'],submodule_blobs=sum(x['blobs_verified'] for x in result['required_submodules'].values()),status='PASS')))

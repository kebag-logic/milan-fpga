#!/usr/bin/env python3
"""Read-only proof of exact commit bytes, modes, index and required submodules.
Usage: python3 verify_integrity.py REPO PACKET
"""
import hashlib, json, os, pathlib, stat, subprocess, sys
repo,packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def entries(root,rev):
    result={}
    for row in git(root,'ls-tree','-r','-z',rev).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.split()
        result[name]=(mode,kind,oid)
    return result
def verify(root,rev):
    tree=entries(root,rev);idx={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0' and name not in idx,('index stage',name)
        idx[name]=(mode,oid)
    assert idx=={p:(m,o) for p,(m,k,o) in tree.items()},'index differs from commit'
    count=0
    for name,(mode,kind,oid) in tree.items():
        if kind==b'commit':continue
        f=root/os.fsdecode(name);s=f.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(s.st_mode),name
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(s.st_mode),name
            gotmode=b'100755' if s.st_mode & 0o111 else b'100644'
            assert gotmode==mode,('mode',name)
            data=f.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert got==oid,('blob',name)
        count+=1
    return count,tree
head=git(repo,'rev-parse','HEAD').decode().strip()
assert head=='e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d'
treeid=git(repo,'rev-parse','HEAD^{tree}').decode().strip()
assert treeid=='ce7e90ddd1263ec89751eca6d836e451a87ecded'
detached=subprocess.run(['git','-C',str(repo),'symbolic-ref','-q','HEAD'],env=env,capture_output=True).returncode!=0
assert detached
n,tree=verify(repo,head)
result={'head':head,'tree':treeid,'detached':detached,'root_blobs_verified':n,'index':'exact stage-zero commit entries','submodules':{}}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    mode,kind,pin=tree[name.encode()];sub=repo/name
    assert mode==b'160000' and kind==b'commit' and (sub/'.git').is_file() and not sub.is_symlink()
    assert git(sub,'rev-parse','HEAD').strip()==pin
    assert pathlib.Path(git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==repo
    n,_=verify(sub,pin.decode())
    result['submodules'][name]={'pin':pin.decode(),'blobs_verified':n,'registered':True,'index':'exact stage-zero commit entries'}
result['status']=git(repo,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status'],result['status']
for base in ('fa450d301805881ad713b67521477bf042ddadfd','3ebd6ca30106a006c20fd2879dcad9c79bf51dca'):
    data=git(repo,'diff','--no-ext-diff','--no-textconv','--no-renames',base,head)
    result['diff_'+base[:8]+'_sha256']=hashlib.sha256(data).hexdigest()
result['source_restoration']='No source bytes or index entries were edited; all probes built from separate binaries or scratch copies.'
(packet/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

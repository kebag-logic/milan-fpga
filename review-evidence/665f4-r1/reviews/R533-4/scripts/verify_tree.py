#!/usr/bin/env python3
"""Verify tree bytes, filesystem types/modes, index records and required gitlinks."""
import argparse, hashlib, json, os, pathlib, stat, subprocess
p=argparse.ArgumentParser(); p.add_argument('--repo',type=pathlib.Path,required=True); p.add_argument('--output',type=pathlib.Path,required=True)
a=p.parse_args(); repo=a.repo.resolve(); env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
HEAD='6f7deea15a9160761b30aaa93fe152f20d416695'
REQUIRED=['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP']
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def prove(root,rev):
    entries=git(root,'ls-tree','-rz',rev).split(b'\0'); expected=[]; checked=0; links={}; digest=hashlib.sha256()
    for row in filter(None,entries):
        meta,name=row.split(b'\t',1); mode,kind,oid=meta.split(); expected.append(mode+b' '+oid+b' 0\t'+name)
        path=root/os.fsdecode(name)
        if mode==b'160000':links[os.fsdecode(name)]=oid.decode();continue
        s=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(s.st_mode),str(path); data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode),str(path)
            assert bool(s.st_mode & 0o111)==(mode==b'100755'),str(path)
            data=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==oid.decode(),str(path)
        digest.update(row+b'\0');checked+=1
    actual=git(root,'ls-files','--stage','-z').split(b'\0')
    assert sorted(filter(None,actual))==sorted(expected),'index differs: '+str(root)
    return {'revision':rev,'tree':git(root,'rev-parse',rev+'^{tree}').decode().strip(),'files_verified':checked,'verified_records_sha256':digest.hexdigest(),'index_matches':True,'gitlinks':links}
assert git(repo,'rev-parse','HEAD').decode().strip()==HEAD
result={'parent':prove(repo,HEAD),'submodules':{}}
for name in REQUIRED:
    root=repo/name; rev=result['parent']['gitlinks'][name]
    assert git(root,'rev-parse','HEAD').decode().strip()==rev,name
    assert (root/'.git').is_file(),'expected registered submodule: '+name
    result['submodules'][name]=prove(root,rev)
result['status']=git(repo,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status'],result['status']
result['external']='Uninitialized optional external gitlink retained; not needed by these probes.'
a.output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

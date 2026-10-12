#!/usr/bin/env python3
"""Verify raw tracked bytes, file modes, index and required submodule pins."""
import argparse, hashlib, json, os, pathlib, stat, subprocess
p=argparse.ArgumentParser();p.add_argument('repo',type=pathlib.Path);a=p.parse_args();repo=a.repo.resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,rev):
 tree={}
 for line in git(root,'ls-tree','-rz',rev).split(b'\0'):
  if not line:continue
  meta,path=line.split(b'\t',1);mode,kind,oid=meta.decode().split();tree[path]=(mode,kind,oid)
 index={}
 for line in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not line:continue
  meta,path=line.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0',(root,path,stage);assert path not in index;index[path]=(mode,oid)
 assert index=={path:(m,oid) for path,(m,k,oid) in tree.items()},str(root)+' index differs from pinned tree'
 count=0
 for path,(mode,kind,oid) in tree.items():
  if kind=='commit':continue
  f=root/os.fsdecode(path);s=f.lstat()
  if mode=='120000':assert stat.S_ISLNK(s.st_mode);data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(s.st_mode),(path,'not regular')
   assert bool(s.st_mode&stat.S_IXUSR)==(mode=='100755'),(path,'mode mismatch')
   data=f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert actual==oid,(path,'bytes mismatch');count+=1
 return tree,count
head=git(repo,'rev-parse','HEAD').decode().strip();assert head=='37944f8ac9d1a2212a3a32f36d921434ea0cbdeb'
tree_oid=git(repo,'rev-parse','HEAD^{tree}').decode().strip();assert tree_oid=='037ca71afbbb78009f8116a6f1227b81d38af79b'
tree,count=verify(repo,head);subs=[]
for path,(mode,kind,oid) in tree.items():
 if kind!='commit':continue
 assert mode=='160000'
 name=os.fsdecode(path);row=dict(path=name,pin=oid)
 if name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
  sub=repo/name;assert (sub/'.git').is_file();assert git(sub,'rev-parse','HEAD').decode().strip()==oid
  _,row['verified_blobs']=verify(sub,oid);row['initialized']=True
 else:row['initialized']=False
 subs.append(row)
index_file=pathlib.Path(git(repo,'rev-parse','--git-path','index').decode().strip());index_file=index_file if index_file.is_absolute() else repo/index_file
status=git(repo,'status','--porcelain=v1','--untracked-files=all').decode();assert not status,status
print(json.dumps(dict(head=head,tree=tree_oid,verified_parent_blobs=count,index_sha256=hashlib.sha256(index_file.read_bytes()).hexdigest(),submodules=subs,status='clean',result='PASS'),indent=2))

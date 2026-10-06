#!/usr/bin/env python3
"""Prove tracked worktree bytes, modes, index entries, and required gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve()
HEAD='0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe'
TREE='dfc55c6343d0c4c943e0c127dee9912ea94357fa'
REQUIRED=['protocol-processor','gptp-processor','third_party/verilog-axis']
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def entries(root,rev):
 out={}
 for rec in git(root,'ls-tree','-rz',rev).split(b'\0'):
  if rec:
   meta,name=rec.split(b'\t',1);mode,kind,oid=meta.split();out[os.fsdecode(name)]=(mode.decode(),kind.decode(),oid.decode())
 return out
def verify(root,rev):
 tracked=entries(root,rev);index={}
 for rec in git(root,'ls-files','--stage','-z').split(b'\0'):
  if rec:
   meta,name=rec.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0',(root,name,stage)
   index[os.fsdecode(name)]=(mode.decode(),oid.decode())
 assert index=={n:(v[0],v[2]) for n,v in tracked.items()},'index differs from pinned tree'
 count=0
 for name,(mode,kind,oid) in tracked.items():
  if kind=='commit':continue
  p=root/name;s=p.lstat()
  if mode=='120000':assert stat.S_ISLNK(s.st_mode),name;data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(s.st_mode),name
   assert bool(s.st_mode&0o111)==(mode=='100755'),name
   data=p.read_bytes()
  digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert digest==oid,(name,'blob mismatch');count+=1
 return tracked,count
assert git(repo,'rev-parse','HEAD').decode().strip()==HEAD
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()==TREE
tracked,count=verify(repo,HEAD)
result={'head':HEAD,'tree':TREE,'parent_blob_files_verified':count,'index':'matches HEAD','required_submodules':[]}
for name in REQUIRED:
 mode,kind,pin=tracked[name];assert (mode,kind)==('160000','commit')
 root=repo/name;assert (root/'.git').is_file() and not (root/'.git').is_symlink(),name
 assert git(root,'rev-parse','HEAD').decode().strip()==pin,name
 superproject=git(root,'rev-parse','--show-superproject-working-tree').decode().strip();assert pathlib.Path(superproject).resolve()==repo,name
 _,files=verify(root,pin)
 result['required_submodules'].append({'path':name,'gitlink':pin,'blob_files_verified':files,'index':'matches pin'})
result['optional_external_gitlink']=tracked.get('external')
result['status_porcelain']=git(repo,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status_porcelain'],'unexpected checkout edits or untracked files'
print(json.dumps(result,indent=2))
print('PASS: tracked blobs, modes, index, HEAD/tree and required submodule gitlinks match')

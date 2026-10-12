#!/usr/bin/env python3
"""Verify HEAD, tracked blob bytes/modes, index entries and required registered submodule pins."""
import hashlib,json,os,pathlib,stat,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2])
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,expected):
 assert not root.is_symlink()
 head=git(root,'rev-parse','HEAD').decode().strip();assert head==expected
 records=[];blobs=0;links={}
 for line in git(root,'ls-tree','-rz',expected).split(b'\0'):
  if not line:continue
  meta,name=line.split(b'\t',1);mode,kind,oid=meta.split();records.append((mode,oid,b'0',name))
  path=root/os.fsdecode(name)
  if kind==b'commit': links[os.fsdecode(name)]=oid.decode();continue
  st=path.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode) and not stat.S_ISLNK(st.st_mode),os.fsdecode(name)
   assert (mode==b'100755')==bool(st.st_mode&0o111),os.fsdecode(name)
   data=path.read_bytes()
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid.decode(),os.fsdecode(name)
  blobs+=1
 index=[]
 for line in git(root,'ls-files','--stage','-z').split(b'\0'):
  if line:
   meta,name=line.split(b'\t',1);mode,oid,stage=meta.split();index.append((mode,oid,stage,name))
 assert sorted(records)==sorted(index),'index differs from pinned tree'
 return {'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'blobs_verified':blobs,'index_entries_verified':len(index),'gitlinks':links}
result={'parent':verify(repo,'3619019350936d5af851933df0b5444ef8387e69'),'submodules':{}}
assert result['parent']['tree']=='11777358b03b38ceda5ade1e1ed59e31b08473e5'
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 root=repo/name
 assert (root/'.git').is_file(),f'{name}: unregistered checkout'
 assert pathlib.Path(git(root,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==repo
 result['submodules'][name]=verify(root,result['parent']['gitlinks'][name])
result['status_porcelain']=git(repo,'status','--porcelain=v1','--untracked-files=no').decode()
assert not result['status_porcelain']
out.write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['parent']['blobs_verified'],'parent blobs;',sum(x['blobs_verified'] for x in result['submodules'].values()),'required-submodule blobs; bytes, modes, indexes, gitlinks')

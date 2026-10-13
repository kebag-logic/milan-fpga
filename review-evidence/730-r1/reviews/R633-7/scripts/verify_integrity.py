#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index, and required submodule gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
ROOT=pathlib.Path(sys.argv[1]).resolve()
HEAD='b341e875d87c6aa2be355bad17f373782517f723'
TREE='82915e6c72b793bdf50a3b615afa5b03a6883c07'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(root,*args):
 return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,expected):
 head=git(root,'rev-parse','HEAD').strip().decode();assert head==expected,(root,head,expected)
 entries=[]
 for record in git(root,'ls-tree','-rz','--full-tree','HEAD').split(b'\0'):
  if not record:continue
  meta,path=record.split(b'\t',1);mode,kind,oid=meta.split();entries.append((mode,kind,oid,path))
 index={}
 for record in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not record:continue
  meta,path=record.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0';assert path not in index
  index[path]=(mode,oid)
 assert index=={path:(mode,oid) for mode,kind,oid,path in entries}
 blobs=0;links={}
 for mode,kind,oid,path in entries:
  file=root/os.fsdecode(path)
  if kind==b'commit':links[os.fsdecode(path)]=oid.decode();continue
  info=file.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(info.st_mode);data=os.fsencode(os.readlink(file))
  else:
   assert stat.S_ISREG(info.st_mode),(path,mode,info.st_mode)
   assert bool(info.st_mode & 0o111)==(mode==b'100755'),path
   data=file.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==oid,path;blobs+=1
 status=git(root,'status','--porcelain=v1','--untracked-files=all').decode();assert not status,(root,status)
 return {'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'entries':len(entries),'blobs_verified':blobs,'gitlinks':links,'index_bytes_modes_status':'PASS'}
result={'root':verify(ROOT,HEAD)};assert result['root']['tree']==TREE
result['required_submodules']={}
for relative in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 root=ROOT/relative;assert not root.is_symlink();assert (root/'.git').is_file()
 result['required_submodules'][relative]=verify(root,result['root']['gitlinks'][relative])
result['all_gitlinks_unchanged_from_source_base']=not git(ROOT,'diff','dc4d06cb','HEAD','--',*result['root']['gitlinks'])
assert result['all_gitlinks_unchanged_from_source_base']
print(json.dumps(result,indent=2))

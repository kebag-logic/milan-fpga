#!/usr/bin/env python3
"""Prove index entries, worktree blob bytes/modes and required submodule pins."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
expected='8383e929fab3ff57a768c88b8b1ff9b568afcf14';expected_tree='7002558568dadb29f501869b2bfce4c4e91230c7'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,revision):
 entries=[];index=[];links={};blobs=0
 for raw in git(root,'ls-tree','-rz',revision).split(b'\0'):
  if not raw:continue
  info,path=raw.split(b'\t',1);mode,kind,oid=info.split();entries.append((mode,oid,path));name=os.fsdecode(path)
  if kind==b'commit':links[name]=oid.decode();continue
  f=root/name;st=f.lstat()
  if mode==b'120000':assert stat.S_ISLNK(st.st_mode),name;data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode & stat.S_IXUSR)==(mode==b'100755'),name
   data=f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert actual==oid.decode(),name
  blobs+=1
 for raw in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not raw:continue
  info,path=raw.split(b'\t',1);mode,oid,stage=info.split();assert stage==b'0',path
  index.append((mode,oid,path))
 assert index==entries, 'index differs from pinned tree'
 assert git(root,'rev-parse','HEAD').decode().strip()==revision
 return dict(head=revision,tree=git(root,'rev-parse',revision+'^{tree}').decode().strip(),blobs_verified=blobs,index_entries=len(entries),gitlinks=links,entries_sha256=hashlib.sha256(repr(entries).encode()).hexdigest())
result={'superproject':verify(a.root,expected),'submodules':{}}
assert result['superproject']['tree']==expected_tree
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 f=a.root/name;assert (f/'.git').is_file(),name
 assert git(f,'rev-parse','--show-superproject-working-tree').decode().strip()==str(a.root.resolve()),name
 result['submodules'][name]=verify(f,result['superproject']['gitlinks'][name])
result['status']=git(a.root,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status'],result['status']
result['write_tree']=git(a.root,'write-tree').decode().strip();assert result['write_tree']==expected_tree
result['result']='PASS'
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

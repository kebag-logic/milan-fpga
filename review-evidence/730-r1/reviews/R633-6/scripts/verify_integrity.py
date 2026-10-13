#!/usr/bin/env python3
"""Verify raw worktree bytes/modes and stage-zero index against a pinned tree."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve();expected='73b8dcd667aa5bf1254e828dd1dd7217c8a103ce'
expected_tree='73657b81c74af58dde382e4f9ce49d5a0e9e80bc'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def validate(root,head,label):
 assert git(root,'rev-parse','HEAD').decode().strip()==head,label
 entries={}
 for row in git(root,'ls-tree','-rz','--full-tree',head).split(b'\0'):
  if not row:continue
  fields,name=row.split(b'\t',1);mode,kind,oid=fields.split();entries[name]=(mode,oid)
 index={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  fields,name=row.split(b'\t',1);mode,oid,stage=fields.split();assert stage==b'0'
  index[name]=(mode,oid)
 assert entries==index,(label,'index mismatch')
 links=[];blobs=0
 for name,(mode,oid) in entries.items():
  path=root/os.fsdecode(name)
  if mode==b'160000':
   links.append(dict(path=os.fsdecode(name),gitlink=oid.decode(),initialized=(path/'.git').exists()))
   if (path/'.git').exists():validate(path,oid.decode(),label+'/'+os.fsdecode(name))
   continue
  st=path.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),(label,name,'kind')
   actual=b'100755' if st.st_mode & stat.S_IXUSR else b'100644';assert actual==mode,(label,name,'mode')
   data=path.read_bytes()
  got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert got==oid.decode(),(label,name,'bytes')
  blobs+=1
 status=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
 assert not status,(label,status)
 reports.append(dict(repository=label,head=head,tree=git(root,'rev-parse','HEAD^{tree}').decode().strip(),tracked_entries=len(entries),raw_blobs_verified=blobs,index_exact=True,status_clean=True,gitlinks=links))
reports=[]
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()==expected_tree
validate(repo,expected,'review checkout')
expected_links={'external':'efeb541ae5fe1e078332d8462dca2fc2d9cb8db5','gptp-processor':'7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9','protocol-processor':'2ad2f845dd583f8310075fa2380cb60a04fd091a','third_party/lwSRP':'08ee86e812a0eb5e1dc6cd61b494d8baf3491348','third_party/verilog-axis':'48ff7a7e2ef782cf778d47910cf85835c64b1bce'}
assert {r['path']:r['gitlink'] for r in reports[-1]['gitlinks']}==expected_links
print(json.dumps(dict(result='PASS',head=expected,tree=expected_tree,repositories=reports),indent=2))

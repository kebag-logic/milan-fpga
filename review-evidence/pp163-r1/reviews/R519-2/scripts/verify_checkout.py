#!/usr/bin/env python3
"""Verify every tracked blob byte, mode, index entry, and nested gitlink."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*a):return subprocess.check_output(['git','-C',str(root),*a])
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='c4539ff107a6a4c7d2e4a4844182b00a2bf33c82';assert tree=='4378652558345d65dd87efd4f092f41f413226c8'
expected={};links=[];rows=[]
for item in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not item:continue
 meta,name=item.split(b'\t',1);mode,kind,oid=meta.decode().split();name=name.decode();path=root/name
 expected[name]=(mode,oid,'0')
 if kind=='commit':
  actual=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD']).decode().strip();assert actual==oid;links.append({'path':name,'head':oid});continue
 data=os.readlink(path).encode() if mode=='120000' else path.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert actual==oid,name
 actual_mode='120000' if path.is_symlink() else '100755' if path.stat().st_mode & stat.S_IXUSR else '100644';assert actual_mode==mode,name
 rows.append({'path':name,'mode':mode,'blob':oid,'sha256':hashlib.sha256(data).hexdigest()})
index={}
for item in git('ls-files','--stage','-z').split(b'\0'):
 if item:
  meta,name=item.split(b'\t',1);mode,oid,stage=meta.decode().split();index[name.decode()]=(mode,oid,stage)
assert index==expected
status=git('status','--porcelain=v1','--untracked-files=all').decode();assert not status,status
print(json.dumps({'head':head,'tree':tree,'tracked_blobs':len(rows),'gitlinks':links,'index_matches_tree':True,'worktree_clean':True,'files':rows},indent=2))

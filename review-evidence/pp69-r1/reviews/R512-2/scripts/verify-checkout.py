#!/usr/bin/env python3
"""Verify every tracked byte, executable/symlink mode, index entry and gitlink."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args();root=a.source.resolve()
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();errors=[];expected={};links=[];blobs=0
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not row:continue
 meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();path=os.fsdecode(path);expected[path]=(mode,oid);f=root/path
 if mode=='160000':
  actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=f,text=True).strip();links.append({'path':path,'expected':oid,'actual':actual});
  if actual!=oid:errors.append(path+': gitlink mismatch')
  continue
 blobs+=1
 if not f.exists() and not f.is_symlink():errors.append(path+': missing');continue
 actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&0o111 else '100644')
 data=os.fsencode(os.readlink(f)) if f.is_symlink() else f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if (actualmode,actual)!=(mode,oid):errors.append(path+': blob or mode mismatch')
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
 if not row:continue
 meta,path=row.split(b'\t',1);mode,oid,stage=meta.decode().split();path=os.fsdecode(path)
 if stage!='0':errors.append(path+': nonzero index stage')
 index[path]=(mode,oid)
if index!=expected:errors.append('index differs from HEAD tree')
if head!='75c4eee4589e9317aca3d07b91f94a38b4cc86af' or tree!='43f1dbf62f8151c5ad158546494174fd434032c3':errors.append('head/tree mismatch')
status=git('status','--porcelain=v1','--untracked-files=all').decode()
if status:errors.append('worktree status is not empty')
out={'head':head,'tree':tree,'tracked_blobs_checked':blobs,'index_entries_checked':len(index),'required_submodule_gitlinks':links,'gitlinks_count':len(links),'worktree_status':status,'errors':errors,'pass':not errors}
a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(bool(errors))

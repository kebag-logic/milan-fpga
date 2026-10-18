#!/usr/bin/env python3
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else os.getcwd()).resolve()
def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
head='e11fb36b366587b5e2403c5d47452c16aae6ec31';tree='cb3672c5ab26692249e8bacae5dfaf6d07c659a2'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
assert not git('diff','--cached','--raw','HEAD')
expected={}
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not entry:continue
 meta,path=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();expected[path.decode()]=(mode,kind,oid)
errors=[];links=[];blobs=0
for path,(mode,kind,oid) in expected.items():
 f=root/path
 if mode=='160000':links.append((path,oid));continue
 data=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 fm='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&stat.S_IXUSR else '100644')
 if actual!=oid or fm!=mode:errors.append(path)
 blobs+=1
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
 if not entry:continue
 meta,path=entry.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';index[path.decode()]=(mode,oid)
assert index=={p:(v[0],v[2]) for p,v in expected.items()}
status=git('status','--porcelain=v1').decode()
print(json.dumps(dict(head=head,tree=tree,tracked_blobs_checked=blobs,blob_or_mode_mismatches=errors,index_matches_HEAD=True,required_gitlinks=links,status=status),indent=2))
assert not errors and not status

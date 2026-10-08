import hashlib,json,os,subprocess,sys
from pathlib import Path
source=Path(sys.argv[1]).resolve()
def git(root,*args):
 return subprocess.check_output(['git','-C',str(root),*args],env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})
def verify(root):
 assert git(root,'rev-parse','--show-toplevel').decode().strip()==str(root)
 head=git(root,'rev-parse','HEAD').decode().strip()
 records=git(root,'ls-tree','-rz','HEAD').split(b'\0')
 expected=[];blobs=0;links=[]
 for rec in records:
  if not rec:continue
  meta,raw=rec.split(b'\t',1);mode,kind,oid=meta.split();path=root/os.fsdecode(raw)
  expected.append(mode+b' '+oid+b' 0\t'+raw)
  if kind==b'commit':links.append((os.fsdecode(raw),oid.decode()));continue
  assert path.is_symlink()==(mode==b'120000'),path
  data=os.fsencode(os.readlink(path)) if mode==b'120000' else path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert actual==oid.decode(),path
  if mode!=b'120000': assert bool(path.stat().st_mode&0o111)==(mode==b'100755'),path
  blobs+=1
 assert sorted(expected)==sorted(x for x in git(root,'ls-files','--stage','-z').split(b'\0') if x)
 return dict(head=head,blobs=blobs,gitlinks=links,exact_blobs_modes_index=True)
parent=verify(source)
subs={}
for rel,pin in parent['gitlinks']:
 if rel=='external':continue
 sub=source/rel
 # The top-level proof in verify runs before every dependency's other Git operations.
 subs[rel]=verify(sub)
 assert subs[rel]['head']==pin
record={'parent':parent,'submodules':subs,'source_status':git(source,'status','--porcelain=v1','--ignored','--untracked-files=all').decode()}
Path(sys.argv[2]).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))

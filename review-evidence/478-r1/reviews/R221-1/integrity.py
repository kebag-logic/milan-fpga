import os,sys,json,hashlib,stat,subprocess
from pathlib import Path
ROOT=Path('$VALIDATION_STORAGE/reviews/r221-478-r1')
def git(root,*args):
 return subprocess.check_output(['rtk','proxy','git','-C',str(root),*args],env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1','GIT_OPTIONAL_LOCKS':'0'})
def check(root, expected=None):
 head=git(root,'rev-parse','HEAD').decode().strip()
 tree=git(root,'rev-parse','HEAD^{tree}').decode().strip()
 entries=git(root,'ls-tree','-rz','--full-tree','HEAD')
 index=git(root,'ls-files','--stage','-z')
 expected_index=[]; files=[]; subs=[]; errors=[]
 for entry in entries.split(b'\0'):
  if not entry: continue
  meta,rawpath=entry.split(b'\t',1); mode,kind,oid=meta.decode().split(); name=rawpath.decode(); path=root/name
  expected_index.append(mode.encode()+b' '+oid.encode()+b' 0\t'+rawpath+b'\0')
  if kind=='commit':
   if not (path/'.git').exists():
    subs.append({'path':name,'expected':oid,'state':'uninitialized'}); continue
   sub=check(path,oid); subs.append({'path':name,**sub}); errors.extend([name+': '+e for e in sub['errors']]); continue
  try:
   s=path.lstat(); actualkind='symlink' if stat.S_ISLNK(s.st_mode) else 'file' if stat.S_ISREG(s.st_mode) else 'other'
   data=os.readlink(path).encode() if actualkind=='symlink' else path.read_bytes()
   actualmode='120000' if actualkind=='symlink' else '100755' if s.st_mode&0o111 else '100644'
   actualoid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if actualoid!=oid or actualmode!=mode or actualkind not in ('file','symlink'): errors.append(name+': blob/kind/mode mismatch')
   files.append({'path':name,'blob':oid,'actual_blob':actualoid,'mode':mode,'actual_mode':actualmode,'kind':actualkind})
  except Exception as e: errors.append(name+': '+str(e))
 if index!=b''.join(expected_index): errors.append('index differs from HEAD tree')
 if expected and head!=expected: errors.append('head differs from expected')
 return {'head':head,'tree':tree,'index_records_sha256':hashlib.sha256(index).hexdigest(),'files_checked':len(files),'files':files,'submodules':subs,'errors':errors}
r=check(ROOT,'d81a302760b84f32d2aa019643f57682bb6e052c')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ('files','submodules')},indent=2))
for s in r['submodules']: print({k:v for k,v in s.items() if k not in ('files','submodules')})
raise SystemExit(bool(r['errors']))

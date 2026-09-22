import os,sys,stat,json,hashlib,subprocess
from pathlib import Path
root=Path(sys.argv[1]); label=sys.argv[2]
def git(path,*args):
 return subprocess.check_output(['rtk','proxy','git','-C',str(path),*args],env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})
def inspect(path, expected=None):
 head=git(path,'rev-parse','HEAD').decode().strip()
 if expected: assert head==expected,(path,head,expected)
 tree=git(path,'ls-tree','-rz','--full-tree',head)
 wanted=[]; subs=[]; count=0
 for rec in tree.split(b'\0'):
  if not rec: continue
  meta,name=rec.split(b'\t',1);mode,kind,oid=meta.split(); p=path/os.fsdecode(name)
  wanted.append(mode+b' '+oid+b' 0\t'+name)
  if mode==b'160000':
   if name==b'external': subs.append({'path':str(p.relative_to(root)),'pin':oid.decode(),'excluded':'Unused historical Ethernet MAC import, uninitialized'});continue
   assert p.is_dir() and not p.is_symlink(),p
   assert (p/'.git').is_file(),p
   subs.append(inspect(p,oid.decode()));continue
  st=p.lstat()
  if mode==b'120000': assert stat.S_ISLNK(st.st_mode),p;data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(st.st_mode),p
   assert bool(st.st_mode&0o111)==(mode==b'100755'),p
   data=p.read_bytes()
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob==oid.decode(),(p,blob,oid)
  count+=1
 actual=git(path,'ls-files','--stage','-z').split(b'\0')
 assert sorted(filter(None,actual))==sorted(wanted),(path,'index differs')
 return {'path':str(path),'head':head,'tree':git(path,'rev-parse','HEAD^{tree}').decode().strip(),'tracked_blobs_verified':count,'index_exact':True,'submodules':subs,'status':git(path,'status','--porcelain=v1','--untracked-files=all').decode(),'index_sha256':hashlib.sha256((path/str(git(path,'rev-parse','--git-path','index').decode().strip())).read_bytes()).hexdigest()}
result=inspect(root,'a769d9dbc937fb324c4726e60dee5b2f7ad349e3')
Path(__file__).with_name('integrity-'+label+'.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

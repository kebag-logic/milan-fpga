import hashlib,json,os,pathlib,stat,subprocess,sys
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1')
EXPECTED='3d90958f3a82ca2a9617112c107a22f332117e17'
os.environ['GIT_NO_REPLACE_OBJECTS']='1'
def git(root,*args):
 return subprocess.check_output(['rtk','proxy','git','-C',str(root),*args])
def verify(root,commit):
 errors=[]; count=0; links={}; records=[]
 tree=git(root,'ls-tree','-rz',commit)
 for entry in tree.split(b'\0'):
  if not entry: continue
  meta,name=entry.split(b'\t',1); mode,kind,oid=meta.decode().split(); name=os.fsdecode(name); p=root/name
  records.append((mode,oid,'0',name))
  if kind=='commit': links[name]=oid; continue
  count+=1
  if not p.exists() and not p.is_symlink(): errors.append([name,'missing']); continue
  st=p.lstat()
  if mode=='120000':
   if not stat.S_ISLNK(st.st_mode): errors.append([name,'kind']); continue
   data=os.fsencode(os.readlink(p))
  else:
   if not stat.S_ISREG(st.st_mode): errors.append([name,'kind']); continue
   data=p.read_bytes()
   if bool(st.st_mode & 0o111)!=(mode=='100755'): errors.append([name,'mode'])
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  if actual!=oid: errors.append([name,'blob',oid,actual])
 indexed=[]
 for entry in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not entry: continue
  meta,name=entry.split(b'\t',1); mode,oid,stage=meta.decode().split(); indexed.append((mode,oid,stage,os.fsdecode(name)))
 if sorted(indexed)!=sorted(records): errors.append(['index differs from commit'])
 return {'root':str(root),'head':git(root,'rev-parse','HEAD').decode().strip(),'tree':git(root,'rev-parse',commit+'^{tree}').decode().strip(),'file_count':count,'gitlinks':links,'errors':errors,'index_equal':sorted(indexed)==sorted(records),'status':git(root,'status','--porcelain=v2','--untracked-files=normal').decode(),'index_flags':git(root,'ls-files','-v').decode().splitlines() if errors else 'bytes checked independently of flags'}
r=verify(ROOT,EXPECTED); assert r['head']==EXPECTED
subs=[]
for name in ('third_party/verilog-axis','protocol-processor','gptp-processor'):
 p=ROOT/name; assert p.is_dir() and not p.is_symlink(); assert (p/'.git').is_file() and not (p/'.git').is_symlink(); pin=r['gitlinks'][name]; x=verify(p,pin); x['registered_gitdir']=git(p,'rev-parse','--absolute-git-dir').decode().strip(); x['gitfile']=(p/'.git').read_text(); assert x['head']==pin; subs.append(x)
result={'parent':r,'submodules':subs}; print(json.dumps(result,indent=2)); assert not any(x['errors'] for x in [r,*subs])

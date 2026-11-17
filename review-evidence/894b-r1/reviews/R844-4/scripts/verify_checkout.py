import hashlib, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(repo,*args): return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def verify(repo,rev,label):
 tree=git(repo,'ls-tree','-rz','--full-tree',rev).split(b'\0'); expected={}; count=0; links=[]; bad=[]
 for entry in filter(None,tree):
  meta,name=entry.split(b'\t',1);mode,kind,oid=meta.split();expected[name]=(mode,oid)
  path=repo/os.fsdecode(name)
  if kind==b'commit':links.append((path,oid.decode()));continue
  try:
   st=path.lstat()
   if mode==b'120000':
    assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(path)); actualmode=b'120000'
   else:
    assert stat.S_ISREG(st.st_mode);data=path.read_bytes();actualmode=b'100755' if st.st_mode&0o111 else b'100644'
   digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if (actualmode,digest)!=(mode,oid):bad.append(os.fsdecode(name))
   count+=1
  except (OSError,AssertionError):bad.append(os.fsdecode(name))
 index={}
 for entry in filter(None,git(repo,'ls-files','--stage','-z').split(b'\0')):
  meta,name=entry.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0';index[name]=(mode,oid)
 print(label, 'HEAD',git(repo,'rev-parse','HEAD').decode().strip(),'tracked blobs',count,'byte/mode mismatches',bad,'index matches tree',index==expected)
 assert not bad and index==expected
 return links
print('Parent tree',git(root,'rev-parse','HEAD^{tree}').decode().strip())
links=verify(root,'HEAD','parent')
for path,pin in links:
 name=str(path.relative_to(root))
 if not (path/'.git').exists():
  print(name,'gitlink',pin,'UNINITIALIZED; no runtime/source evidence claimed');continue
 assert git(path,'rev-parse','HEAD').decode().strip()==pin
 verify(path,pin,name)
print('Parent status:',git(root,'status','--porcelain','--untracked-files=all').decode().strip() or 'clean')
print('RESULT: exact tracked bytes, modes, index and initialized required pins verified')

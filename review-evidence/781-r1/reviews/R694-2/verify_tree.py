import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected='41f4a53cc0b12f143fa3e61a5339a11e79806ce9'
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(cwd,*args): return subprocess.check_output(['git',*args],cwd=cwd,env=env)
def verify(cwd,ref):
 tree=git(cwd,'ls-tree','-rz',ref).split(b'\0'); records=[]; count=0
 for row in tree:
  if not row:continue
  header,path=row.split(b'\t',1);mode,kind,oid=header.split(); records.append(mode+b' '+oid+b' 0\t'+path+b'\0')
  if kind!=b'blob':continue
  file=cwd/os.fsdecode(path);info=file.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(info.st_mode),str(file);data=os.fsencode(os.readlink(file))
  else:
   assert stat.S_ISREG(info.st_mode),str(file)
   assert bool(info.st_mode & 0o111)==(mode==b'100755'),str(file)
   data=file.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==oid,os.fsdecode(path)
  count+=1
 assert b''.join(records)==git(cwd,'ls-files','--stage','-z'),'index differs from pinned tree'
 return count
assert git(root,'rev-parse','HEAD').decode().strip()==expected
counts={'superproject':verify(root,expected)};pins={}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack'):
 mode,kind,pin=git(root,'ls-tree',expected,name).split(b'\t')[0].split()
 assert mode==b'160000' and kind==b'commit'
 sub=root/name; assert not sub.is_symlink()
 assert git(sub,'rev-parse','HEAD').strip()==pin
 assert git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()==str(root)
 counts[name]=verify(sub,pin.decode());pins[name]=pin.decode()
print(json.dumps({'head':expected,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'verified_blob_counts':counts,'gitlinks':pins,'index_bytes_modes':'PASS','status':git(root,'status','--porcelain').decode()},indent=2))

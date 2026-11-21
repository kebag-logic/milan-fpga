#!/usr/bin/env python3
"""Compare tracked bytes, modes and index to the reviewed tree and pinned submodule trees."""
import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parent
head='4ceba3d40e3b94e9bda2407e64ef906c283b63a4';tree='62b09e5c2b550349fee753f4f3d2275422c05e20'
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args])
def audit(path,rev):
 errors=[];count=0
 for row in git(path,'ls-tree','-rz',rev).split(b'\0'):
  if not row:continue
  tag,name=row.split(b'\t',1);mode,kind,oid=tag.split();f=path/os.fsdecode(name)
  if kind==b'commit':continue
  try:
   st=f.lstat();data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
   actual=b'120000' if stat.S_ISLNK(st.st_mode) else b'100755' if st.st_mode&0o111 else b'100644'
   hashed=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if actual!=mode or hashed!=oid:errors.append(os.fsdecode(name))
  except OSError:errors.append(os.fsdecode(name))
  count+=1
 expected=git(path,'rev-parse',rev+'^{tree}').strip()
 if git(path,'write-tree').strip()!=expected:errors.append('INDEX TREE MISMATCH')
 flags=[x for x in git(path,'ls-files','-v').splitlines() if x[:1]!=b'H']
 if flags:errors.append('INDEX FLAGS '+repr(flags))
 return count,errors
lines=['head '+git(root,'rev-parse','HEAD').decode().strip(),'tree '+git(root,'rev-parse','HEAD^{tree}').decode().strip()]
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==tree
n,e=audit(root,head);lines.append(f'parent: {n} blobs checked; errors {e}');allerrors=list(e)
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
 pin=git(root,'rev-parse',head+':'+name).decode().strip();sub=root/name
 assert sub.joinpath('.git').is_file() and not sub.is_symlink()
 assert git(sub,'rev-parse','HEAD').decode().strip()==pin
 n,e=audit(sub,pin);lines.append(f'{name}: {pin}; {n} blobs checked; errors {e}');allerrors+=e
lines.append('tracked status '+repr(git(root,'status','--porcelain','--untracked-files=no').decode()))
lines.append('PASS' if not allerrors else 'FAIL')
out='\n'.join(lines)+'\n';(packet/'checkout-integrity.txt').write_text(out);print(out);sys.exit(bool(allerrors))

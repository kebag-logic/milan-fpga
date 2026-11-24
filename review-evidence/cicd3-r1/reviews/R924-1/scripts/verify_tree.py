#!/usr/bin/env python3
"""Verify tracked disk bytes, modes and index against immutable Git trees."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],env=env)
def verify(path,ref):
 tree={};bad=[]
 for row in git(path,'ls-tree','-rz',ref).split(b'\0'):
  if not row:continue
  entry,name=row.split(b'\t',1);mode,kind,oid=entry.split(); tree[name]=(mode,oid)
  disk=path/os.fsdecode(name)
  try:
   info=disk.lstat()
   if mode==b'160000':continue
   if mode==b'120000':
    assert stat.S_ISLNK(info.st_mode); data=os.fsencode(os.readlink(disk)); actual_mode=b'120000'
   else:
    assert stat.S_ISREG(info.st_mode);data=disk.read_bytes();actual_mode=b'100755' if info.st_mode&0o111 else b'100644'
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if actual!=oid or actual_mode!=mode:bad.append(os.fsdecode(name))
  except (OSError,AssertionError):bad.append(os.fsdecode(name))
 index={}
 for row in git(path,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  entry,name=row.split(b'\t',1);mode,oid,stage=entry.split()
  if stage!=b'0' or name in index:bad.append('index-stage:'+os.fsdecode(name))
  index[name]=(mode,oid)
 if index!=tree:bad.append('index-tree-mismatch')
 hidden=[os.fsdecode(row) for row in git(path,'ls-files','-v','-z').split(b'\0') if row and (row[:1].islower() or row[:1]==b'S')]
 if hidden:bad.append('hidden-index-flags')
 return tree,dict(files=len(tree),bytes_modes_index_match=not bad,failures=bad)
head=git(root,'rev-parse','HEAD').decode().strip();assert head=='13e6d869d842fc06155ef5dae9b0347596d6d4df'
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='1e43c6e433e84cf7dad9bc1ce86220f0a7f8bb8c'
tree,result=verify(root,head);print(json.dumps(dict(repository='reviewed-head',head=head,**result)));assert not result['failures']
for name in ['third_party/verilog-axis','protocol-processor','gptp-processor','third_party/tsn-c-stack','third_party/lwSRP']:
 mode,pin=tree[os.fsencode(name)];assert mode==b'160000'
 path=root/name;actual=git(path,'rev-parse','HEAD').strip();assert actual==pin
 superproject=git(path,'rev-parse','--show-superproject-working-tree').decode().strip();assert pathlib.Path(superproject).resolve()==root
 _,result=verify(path,pin.decode());print(json.dumps(dict(repository=name,pin=pin.decode(),registered=True,**result)));assert not result['failures']
print('Exact head bytes, modes, index and all five initialized gitlinks verified; external is intentionally uninitialized.')

#!/usr/bin/env python3
"""Prove tracked disk bytes, modes and index entries against immutable trees."""
import hashlib,json,os,pathlib,stat,subprocess,sys
source=pathlib.Path(sys.argv[1]);env=os.environ.copy();env['GIT_NO_REPLACE_OBJECTS']='1'
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,expected):
 actual=git(root,'rev-parse','HEAD').decode().strip();assert actual==expected,(str(root),actual,expected)
 tree=git(root,'ls-tree','-rz','HEAD').split(b'\0');expected_index=[];count=0;links={}
 for row in tree:
  if not row:continue
  fields,path=row.split(b'\t');mode,kind,oid=fields.split();expected_index.append(mode+b' '+oid+b' 0\t'+path)
  f=root/os.fsdecode(path)
  if kind==b'commit':links[os.fsdecode(path)]=oid.decode();continue
  st=f.lstat()
  if mode==b'120000':assert stat.S_ISLNK(st.st_mode);raw=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),(str(f),'not regular')
   assert bool(st.st_mode&0o111)==(mode==b'100755'),(str(f),'mode')
   raw=f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  assert actual==oid.decode(),(str(f),'bytes',actual,oid.decode());count+=1
 index=git(root,'ls-files','--stage','-z').split(b'\0');assert sorted(x for x in index if x)==sorted(expected_index),'index differs'
 assert git(root,'write-tree').strip()==git(root,'rev-parse','HEAD^{tree}').strip()
 return dict(head=expected,tree=git(root,'rev-parse','HEAD^{tree}').decode().strip(),tracked_blobs_proved=count,gitlinks=links)
head='8e4b1e53e9b5a8ef5f9854095347436ab84259b6';result={'root':verify(source,head),'submodules':{}}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP'):
 expected=result['root']['gitlinks'][name];root=source/name
 assert (root/'.git').is_file(),name
 assert pathlib.Path(git(root,'rev-parse','--show-toplevel').decode().strip()).resolve()==root.resolve()
 result['submodules'][name]=verify(root,expected)
result['status']=git(source,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status']
result['ignored']=git(source,'ls-files','--others','--ignored','--exclude-standard').decode()
result['external']='Uninitialized as received; superproject gitlink proved, not credited as populated.'
result['result']='PASS: exact tracked bytes, modes, index and four required populated gitlinks'
print(json.dumps(result,indent=2))

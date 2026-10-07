#!/usr/bin/env python3
"""Verify tracked bytes, file modes, stage-0 index and required gitlinks."""
import os,pathlib,subprocess,sys,hashlib,stat,json
root=pathlib.Path(sys.argv[1]).resolve(); expected='50d492c12789e1d80bf11f547e7fe53e02b4bdb9'
env=os.environ.copy();env['GIT_NO_REPLACE_OBJECTS']='1';env['GIT_OPTIONAL_LOCKS']='0'
def git(where,*args):return subprocess.check_output(['git','-C',str(where),*args],env=env)
fail=[];results=[]
def check(where,pin):
 head=git(where,'rev-parse','HEAD').decode().strip()
 if head!=pin:fail.append(str(where)+': HEAD mismatch')
 tree={};blobs=0;links={}
 for record in git(where,'ls-tree','-rz',pin).split(b'\0'):
  if not record:continue
  header,name=record.split(b'\t',1);mode,kind,oid=header.decode().split();name=os.fsdecode(name);tree[name]=(mode,oid)
  if mode=='160000':links[name]=oid;continue
  path=where/name
  try:
   st=path.lstat()
   if mode=='120000':
    if not stat.S_ISLNK(st.st_mode):raise ValueError('expected symlink')
    data=os.fsencode(os.readlink(path))
   else:
    if not stat.S_ISREG(st.st_mode):raise ValueError('expected regular file')
    actual='100755' if st.st_mode & stat.S_IXUSR else '100644'
    if actual!=mode:raise ValueError('file mode mismatch')
    data=path.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if actual!=oid:raise ValueError('blob mismatch')
   blobs+=1
  except (OSError,ValueError) as e:fail.append(str(path)+': '+str(e))
 index={}
 for record in git(where,'ls-files','--stage','-z').split(b'\0'):
  if not record:continue
  header,name=record.split(b'\t',1);mode,oid,stage=header.decode().split();name=os.fsdecode(name)
  if stage!='0' or name in index:fail.append(str(where)+': non-stage-0 or duplicate index '+name)
  index[name]=(mode,oid)
 if index!=tree:fail.append(str(where)+': index differs from commit tree')
 hidden=[os.fsdecode(x) for x in git(where,'ls-files','-v','-z').split(b'\0') if x and (x[:1]==b'S' or x[:1].islower())]
 if hidden:fail.append(str(where)+': hidden index flags '+str(hidden))
 results.append({'repository':'.' if where==root else str(where.relative_to(root)),'head':head,'tree':git(where,'rev-parse',pin+'^{tree}').decode().strip(),'verified_blobs_and_modes':blobs,'stage_zero_index_matches':index==tree,'hidden_index_flags':hidden,'gitlinks':links,'status':git(where,'status','--porcelain=v2','--untracked-files=normal').decode()})
 return links
links=check(root,expected)
for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP']:
 where=root/sub
 if pathlib.Path(git(where,'rev-parse','--show-toplevel').decode().strip()).resolve()!=where:fail.append(sub+': wrong checkout root')
 check(where,links[sub])
print(json.dumps({'expected_head':expected,'repositories':results,'failures':fail,'result':'PASS' if not fail else 'FAIL'},indent=2))
sys.exit(1 if fail else 0)

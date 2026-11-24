#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and required submodule gitlinks against commits."""
import hashlib,json,os,pathlib,stat,subprocess,sys
R=pathlib.Path(sys.argv[1]).resolve();env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,rev):
 rows={};errors=[];count=0
 for row in git(root,'ls-tree','-rz',rev).split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t',1);mode,kind,oid=meta.split();rows[name]=(mode,oid)
  if mode==b'160000':continue
  p=root/os.fsdecode(name)
  try:
   st=p.lstat()
   if mode==b'120000':
    assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(p))
   else:
    assert stat.S_ISREG(st.st_mode);assert bool(st.st_mode&0o111)==(mode==b'100755');data=p.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if actual!=oid:errors.append(os.fsdecode(name)+': blob differs')
   count+=1
  except (OSError,AssertionError):errors.append(os.fsdecode(name)+': missing or mode/type differs')
 index={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
  if stage!=b'0':errors.append(os.fsdecode(name)+': unmerged index')
  index[name]=(mode,oid)
 if index!=rows:errors.append('index differs from tree')
 return {'commit':rev,'tracked_blobs_verified':count,'errors':errors}
head=git(R,'rev-parse','HEAD').decode().strip();result={'root':verify(R,head),'tree':git(R,'rev-parse','HEAD^{tree}').decode().strip(),'submodules':{}}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'):
 row=git(R,'ls-tree',head,'--',name).split();assert row[0]==b'160000';pin=row[2].decode()
 actual=git(R/name,'rev-parse','HEAD').decode().strip();assert actual==pin,(name,actual,pin)
 assert (R/name/'.git').is_file(),name
 result['submodules'][name]=verify(R/name,pin)
print(json.dumps(result,indent=2))
assert not result['root']['errors'] and not any(x['errors'] for x in result['submodules'].values())

#!/usr/bin/env python3
"""Check raw tracked bytes, executable modes, index records and required pins."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
env=os.environ.copy();env['GIT_NO_REPLACE_OBJECTS']='1'
def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args],env=env)
def audit(root,ref):
 entries=git(root,'ls-tree','-rz',ref).split(b'\0'); expected=[]; bad=[]; n=0; pins={}
 for entry in entries:
  if not entry: continue
  meta,name=entry.split(b'\t',1);mode,kind,oid=meta.split();path=root/os.fsdecode(name)
  expected.append(mode+b' '+oid+b' 0\t'+name+b'\0')
  if mode==b'160000': pins[os.fsdecode(name)]=oid.decode();continue
  try:
   s=path.lstat()
   if mode==b'120000': data=os.fsencode(os.readlink(path)); actual=b'120000' if stat.S_ISLNK(s.st_mode) else b'invalid'
   else: data=path.read_bytes();actual=(b'100755' if s.st_mode&0o111 else b'100644') if stat.S_ISREG(s.st_mode) else b'invalid'
   digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   if actual!=mode or digest!=oid: bad.append(os.fsdecode(name))
  except OSError: bad.append(os.fsdecode(name))
  n+=1
 actual_index=git(root,'ls-files','--stage','-z')
 index_ok=sorted(actual_index.split(b'\0'))==sorted(b''.join(expected).split(b'\0'))
 return {'files':n,'mismatches':bad,'index_matches':index_ok,'gitlinks':pins}
root=a.repo.resolve(); head=git(root,'rev-parse','HEAD').decode().strip();result={'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'root':audit(root,head),'submodules':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']:
 pin=result['root']['gitlinks'][name];sub=root/name
 v=audit(sub,pin);v['head']=git(sub,'rev-parse','HEAD').decode().strip();v['expected']=pin;v['registered']=bool(git(sub,'rev-parse','--show-superproject-working-tree').strip());result['submodules'][name]=v
network='cc49123d2db1e01e80859efa10f8da43a01344ef';base='0c31faae6b^'
paths=git(root,'diff','--name-only',base,network).decode().splitlines()
result['network']={'revision':network,'count':len(paths),'identical':all(git(root,'rev-parse',network+':'+s)==git(root,'rev-parse',head+':'+s) for s in paths),'paths':paths}
result['pass']=not result['root']['mismatches'] and result['root']['index_matches'] and result['network']['identical'] and all(not s['mismatches'] and s['index_matches'] and s['head']==s['expected'] and s['registered'] for s in result['submodules'].values())
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pass':result['pass'],'tracked_files':result['root']['files'],'network_files':len(paths)}))
raise SystemExit(0 if result['pass'] else 1)

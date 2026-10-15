#!/usr/bin/env python3
"""Verify raw tracked blob bytes, executable modes, index and required gitlinks."""
import hashlib, json, os, stat, subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
root=Path(os.environ.get('CHECKOUT',os.getcwd())).resolve()
def git(where,*args): return subprocess.check_output(['git','-C',str(where),*args])
def examine(where):
 entries=git(where,'ls-tree','-rz','HEAD').split(b'\0')
 failures=[]; count=0; links=[]
 for raw in entries:
  if not raw: continue
  meta,name=raw.split(b'\t',1); mode,kind,oid=meta.decode().split()
  relative=os.fsdecode(name); path=where/relative
  if kind=='commit':
   links.append({'path':relative,'gitlink':oid}); continue
  count+=1
  try:
   st=path.lstat()
   actual_mode='120000' if stat.S_ISLNK(st.st_mode) else '100755' if st.st_mode & 0o111 else '100644'
   data=os.fsencode(os.readlink(path)) if mode=='120000' else path.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if actual_mode!=mode or actual!=oid: failures.append(relative)
  except OSError: failures.append(relative)
 head=git(where,'rev-parse','HEAD').decode().strip()
 tree=git(where,'rev-parse','HEAD^{tree}').decode().strip()
 index=git(where,'write-tree').decode().strip()
 status=git(where,'status','--porcelain=v1','--untracked-files=all').decode()
 assert not failures and tree==index and not status,(failures,tree,index,status)
 return {'head':head,'tree':tree,'index_tree':index,'tracked_blobs_verified':count,'blob_or_mode_failures':failures,'status':status,'gitlinks':links}
report={'source':examine(root),'required_submodules':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
 result=examine(root/name)
 expected=next(x['gitlink'] for x in report['source']['gitlinks'] if x['path']==name)
 assert result['head']==expected
 report['required_submodules'][name]=result
assert report['source']['head']=='feef7c9fd239ef62b7c6aad301e80a13275e47ef'
assert report['source']['tree']=='4f1e8d01c600c2bdb5ba5ea6ec64a5d5e7f1b808'
(p/'restore-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: exact source and required submodule raw bytes, modes, indexes and gitlinks')

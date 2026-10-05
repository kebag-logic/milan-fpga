#!/usr/bin/env python3
"""Check every tracked byte, executable mode, index, and any submodule gitlink."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

source=Path(sys.argv[1]).resolve()
head='5123548eb4de35f24d43eb088c12dab70b06d01d'
tree='33b4fe59951370299cad36ec1415ead003524d5f'
def git(*args):return subprocess.check_output(['git','-C',str(source),*args])
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
assert git('write-tree').decode().strip()==tree
records=[];links=[]
for entry in git('ls-tree','-rz',head).split(b'\0'):
 if not entry:continue
 meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(name);p=source/rel
 if mode=='160000':
  actual=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD']).decode().strip()
  assert actual==oid,(rel,actual,oid)
  links.append({'path':rel,'gitlink':oid,'checked_out':actual});continue
 assert kind=='blob'
 data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 actual_mode='120000' if p.is_symlink() else ('100755' if p.stat().st_mode&0o111 else '100644')
 assert actual==oid and actual_mode==mode,(rel,actual,oid,actual_mode,mode)
 records.append({'path':rel,'blob':oid,'mode':mode,'sha256':hashlib.sha256(data).hexdigest()})
status=git('status','--porcelain=v1','--untracked-files=all').decode()
assert not status,status
print(json.dumps({'head':head,'tree':tree,'index_tree':tree,'tracked_blobs':len(records),
                  'gitlinks':links,'status':status,'files':records},indent=2))

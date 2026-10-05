#!/usr/bin/env python3
"""Verify raw tracked blob bytes, modes, complete index, and submodule gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
root=a.root.resolve()
def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
expected_head='5123548eb4de35f24d43eb088c12dab70b06d01d'
expected_tree='33b4fe59951370299cad36ec1415ead003524d5f'
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert git('rev-parse','--show-object-format').strip()==b'sha1'
entries=[];bad=[];links=[]
for raw in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if not raw:continue
 meta,name=raw.split(b'\t',1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(name);path=root/rel
 if mode=='160000':links.append(dict(path=rel,sha=oid));continue
 if mode=='120000':data=os.fsencode(os.readlink(path));actual_mode='120000' if path.is_symlink() else 'wrong'
 else:
  data=path.read_bytes();actual_mode='100755' if path.stat().st_mode & 0o111 else '100644'
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 entries.append((mode,oid,rel));
 if actual!=oid or actual_mode!=mode:bad.append(dict(path=rel,expected=oid,actual=actual,mode=actual_mode,expected_mode=mode))
index=[]
for raw in git('ls-files','--stage','-z').split(b'\0'):
 if not raw:continue
 meta,name=raw.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0'
 index.append((mode,oid,os.fsdecode(name)))
want=entries+[('160000',x['sha'],x['path']) for x in links]
index_ok=sorted(index)==sorted(want)
for link in links:
 actual=subprocess.check_output(['git','-C',str(root/link['path']),'rev-parse','HEAD']).decode().strip()
 if actual!=link['sha']:bad.append(dict(path=link['path'],expected=link['sha'],actual=actual))
result=dict(head=head,tree=tree,index_tree=git('write-tree').decode().strip(),blobs=len(entries),regular=sum(e[0]=='100644' for e in entries),executable=sum(e[0]=='100755' for e in entries),gitlinks=links,index_entries_match=index_ok,mismatches=bad,status=git('status','--porcelain=v1').decode(),ok=head==expected_head and tree==expected_tree and not bad and index_ok)
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['ok']

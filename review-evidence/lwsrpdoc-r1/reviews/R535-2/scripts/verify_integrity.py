#!/usr/bin/env python3
"""Compare worktree bytes, executable bits, index, HEAD and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

source,packet=[Path(x).resolve() for x in sys.argv[1:3]]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=source)
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='cd659eb5e93c4da5e97fcbd6282b1efba16e565d'
assert tree=='e5bb35e6cd2efd707cbedaf5d799b8877a0aab30'
entries=[]
gitlinks=[]
for raw in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not raw:continue
    meta,name=raw.split(b'\t',1)
    mode,kind,oid=meta.decode().split()
    name=name.decode()
    f=source/name
    if mode=='160000':
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=f,text=True).strip()
        assert actual==oid
        gitlinks.append({'path':name,'expected':oid,'actual':actual})
        continue
    data=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    observed_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&0o111 else '100644')
    assert actual==oid,(name,'blob')
    assert observed_mode==mode,(name,'mode')
    entries.append({'path':name,'blob':oid,'mode':mode,'bytes_match':True,'mode_matches':True})
index_tree=git('write-tree').decode().strip()
assert index_tree==tree
initial=(packet/'receipts/initial_ls_files.txt').read_bytes()
assert git('ls-files','--stage')==initial
status=git('status','--porcelain=v1','--untracked-files=all','--ignored').decode()
assert not status,status
receipt={'head':head,'tree':tree,'index_tree':index_tree,'index_equal_initial':True,
         'status_porcelain_with_ignored':status,'tracked_files_verified':len(entries),
         'tracked_entries':entries,'required_gitlinks':gitlinks,'gitlink_count':len(gitlinks)}
(packet/'receipts/integrity.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'PASS {len(entries)} tracked blobs/modes; index unchanged; HEAD/tree exact; {len(gitlinks)} gitlinks; clean status including ignored files.')
